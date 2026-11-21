"""Fail closed: scrape SERP-derived URL sets only when legends-dataforseo marked the SERP verified."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .client import SafetyError

SUSPECT_STATUSES = frozenset({"suspect_decoy", "suspect_poisoned", "unverified_decoy"})
OVERRIDE_ENV = "LEGENDS_FIRECRAWL_ALLOW_SUSPECT_SERP"
OVERRIDE_ENV_ALIAS = "LEGENDS_FIRECRAWL_ALLOW_UNVERIFIED_SERP"
MAX_SERP_URLS = 20


class SuspectSerpError(SafetyError):
    """A SERP-derived URL set is not verified clean; scraping it could faithfully copy a decoy."""

    def __init__(self, message: str, *, verdict: dict[str, Any]):
        super().__init__(message)
        self.verdict = verdict


UnverifiedSerpError = SuspectSerpError


def _integrities(envelope: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if not isinstance(envelope, dict):
        return found
    if isinstance(envelope.get("status"), str) and "organic_count" in envelope:
        return [envelope]  # a bare serp_integrity block
    for task in envelope.get("tasks") or []:
        if not isinstance(task, dict):
            continue
        for res_obj in task.get("result") or []:
            if isinstance(res_obj, dict) and isinstance(res_obj.get("serp_integrity"), dict):
                found.append(res_obj["serp_integrity"])
    return found


def _block_verified(integrity: dict[str, Any]) -> bool:
    return (integrity.get("verified") is True
            and integrity.get("integrity") != "unprotected"
            and integrity.get("status") == "clean"
            and integrity.get("unresolved") is not True)


def serp_verdict(envelope: Any) -> dict[str, Any]:
    """Summarize SERP provenance (never raises). `verified` is the fail-closed gate.

    verified is True only when every organic block carries legends-dataforseo >= 0.1.12
    `serp_integrity.verified: true`, is protected (resolve sent), clean and not unresolved.
    Missing, false, unprotected, suspect or unverified_decoy all mean verified False.
    """
    integrities = _integrities(envelope)
    warnings: list[str] = []
    reasons: list[str] = []
    if not integrities:
        return {"status": "unassessed", "verified": False, "suspect": False, "unresolved": False,
                "unverified": True, "unprotected": False, "reasons": ["SERP envelope has no serp_integrity block"],
                "warnings": ["SERP envelope has no serp_integrity block; ranking validity is unknown "
                             "(fetch it with legends-dataforseo >= 0.1.12)."]}
    statuses = [str(i.get("status") or "unassessed") for i in integrities]
    status = next((s for s in ("unverified_decoy", "suspect_poisoned", "suspect_decoy") if s in statuses),
                  statuses[0])
    unresolved = any(i.get("unresolved") is True for i in integrities)
    unprotected = any(i.get("integrity") == "unprotected" for i in integrities)
    verified = all(_block_verified(i) for i in integrities)
    for integrity in integrities:
        for r in list(integrity.get("reasons") or []) + list(integrity.get("unverified_reasons") or []):
            if isinstance(r, str) and r not in reasons:
                reasons.append(r)
        decoy = integrity.get("decoy")
        verification = integrity.get("verification") if isinstance(integrity.get("verification"), dict) else {}
        if "verified" not in integrity:
            warnings.append("serp_integrity has no verified field (pre-0.1.12 envelope); decoy SERPs are not ruled out.")
        if not isinstance(decoy, dict):
            warnings.append("serp_integrity has no decoy assessment (pre-0.1.12 envelope); decoy SERPs are not ruled out.")
        elif decoy.get("provider_resolve") == "not_requested":
            warnings.append("resolve_poisoned_results was not requested for this SERP; provider decoy repair was off.")
        if integrity.get("integrity") == "unprotected":
            warnings.append("SERP was pulled UNPROTECTED (LEGENDS_DFS_ALLOW_POISONED=1); decoy rankings are likely.")
        if integrity.get("verified") is not True and "verified" in integrity:
            warnings.append("legends-dataforseo marked this SERP unverified (verification: "
                            f"{verification.get('status') or 'unknown'}); decoy rankings are not ruled out.")
    suspect = status in SUSPECT_STATUSES or unresolved
    if not verified and not reasons:
        reasons.append("serp_integrity.verified is not true")
    return {"status": status, "verified": verified, "suspect": suspect, "unresolved": unresolved,
            "unverified": not verified, "unprotected": unprotected,
            "reasons": reasons, "warnings": list(dict.fromkeys(warnings))}


def load_serp_envelope(path: str | Path) -> dict[str, Any]:
    from .client import _safe_local_path

    target = _safe_local_path(path)
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SafetyError(f"Cannot read SERP envelope {target.name}: {exc.__class__.__name__}") from None
    if not isinstance(data, dict):
        raise SafetyError("SERP envelope must be a JSON object")
    # legends-dataforseo evidence exports and CLI --output files may wrap the raw envelope.
    for key in ("response", "envelope"):
        if isinstance(data.get(key), dict) and "tasks" in data[key]:
            return data[key]
    return data


def _is_google_wrapper(url: Any) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url.strip())
    host = (parsed.hostname or "").lower().rstrip(".")
    return host in {"google.com", "www.google.com"} and parsed.path.lower() in {"/goto", "/url"}


def serp_targets(envelope: dict[str, Any], *, limit: int = 10) -> dict[str, list[Any]]:
    """Top `limit` organic results split into directly scrapable URLs and /goto items needing resolve.

    Google now wraps most organic links in google.com/goto, which Firecrawl refuses by design.
    Wrapped items are returned under `needs_resolve` with the breadcrumb / domain / path hint /
    title that `lfc resolve` (or `scrape-serp --resolve-goto`) needs; they are never scraped as-is.
    """
    if type(limit) is not int or not 1 <= limit <= MAX_SERP_URLS:
        raise SafetyError(f"limit must be between 1 and {MAX_SERP_URLS}")
    urls: list[str] = []
    needs: list[dict[str, Any]] = []
    for task in envelope.get("tasks") or []:
        for res_obj in (task.get("result") or []) if isinstance(task, dict) else []:
            for item in (res_obj.get("items") or []) if isinstance(res_obj, dict) else []:
                if not isinstance(item, dict) or item.get("type") != "organic":
                    continue
                if len(urls) + len(needs) >= limit:
                    return {"urls": urls, "needs_resolve": needs}
                url = item.get("resolved_url") or item.get("url")
                if _is_google_wrapper(url):
                    domain = item.get("resolved_domain") or item.get("domain")
                    if isinstance(domain, str) and domain.lower().removeprefix("www.") == "google.com":
                        domain = None
                    breadcrumb = item.get("breadcrumb")
                    target = breadcrumb if isinstance(breadcrumb, str) and breadcrumb.startswith(("http://", "https://")) else domain
                    needs.append({"rank": item.get("rank_group"), "target": target, "domain": domain,
                                  "path_hint": item.get("breadcrumb_path_hint"), "title": item.get("title"),
                                  "website_name": item.get("website_name")})
                elif isinstance(url, str) and url.startswith(("http://", "https://")) and url not in urls:
                    urls.append(url)
    return {"urls": urls, "needs_resolve": needs}


def serp_urls(envelope: dict[str, Any], *, limit: int = 10) -> list[str]:
    """Directly scrapable organic URLs (unmasked `resolved_url` preferred); /goto wrappers excluded."""
    return serp_targets(envelope, limit=limit)["urls"]


def override_enabled(flag: bool = False) -> bool:
    truthy = {"1", "true", "yes", "on"}
    return bool(flag) or any(os.environ.get(name, "").strip().lower() in truthy
                             for name in (OVERRIDE_ENV, OVERRIDE_ENV_ALIAS))


def guard_serp(envelope: Any, *, allow_suspect: bool = False) -> dict[str, Any]:
    """Fail closed: raise SuspectSerpError unless the SERP is verified, or the operator overrides."""
    verdict = serp_verdict(envelope)
    if not verdict["verified"]:
        label = verdict["status"] if verdict["suspect"] else f"{verdict['status']} but unverified"
        if verdict["unprotected"]:
            label += ", unprotected"
        if not override_enabled(allow_suspect):
            detail = "; ".join(verdict["reasons"][:3]) or "no reason recorded"
            raise SuspectSerpError(
                f"Refusing to scrape URLs from a SERP marked {label}"
                f"{' (unresolved after re-pull)' if verdict['unresolved'] else ''}: {detail}. "
                "Only SERPs with serp_integrity.verified=true (legends-dataforseo >= 0.1.12) are scraped. "
                "Re-pull it with legends-dataforseo or pass --allow-unverified-serp (alias "
                f"--allow-suspect-serp) / {OVERRIDE_ENV}=1 to scrape it anyway.",
                verdict=verdict,
            )
        verdict["warnings"].append(f"OVERRIDE: scraping a SERP marked {label}; results may be decoy pages.")
        verdict["overridden"] = True
    return verdict
