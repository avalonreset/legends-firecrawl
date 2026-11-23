"""Fail closed: scrape SERP-derived URL sets only when legends-dataforseo marked the SERP verified."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .client import SafetyError

SUSPECT_STATUSES = frozenset({"suspect_decoy", "suspect_poisoned", "unverified_decoy"})
LEGACY_PROVIDER_ONLY_BASES = frozenset({
    "provider_from_web",
    "double_pull_stable",
    "provider_clean_no_decoy_signals",
})
TRUSTED_VERIFIED_BASES = frozenset({"independent_consensus", "independent_consensus_repaired"})
OVERRIDE_ENV = "LEGENDS_FIRECRAWL_ALLOW_SUSPECT_SERP"
OVERRIDE_ENV_ALIAS = "LEGENDS_FIRECRAWL_ALLOW_UNVERIFIED_SERP"
MAX_SERP_URLS = 20

# Closed allowlist: SERP `website_name` first segment -> registrable domain.
# Only platforms whose display name maps to exactly one domain belong here.
# Anything else (a business name) stays unresolved; never slug-guess a domain.
WEBSITE_NAME_PLATFORMS = {
    "reddit": "reddit.com", "youtube": "youtube.com", "facebook": "facebook.com",
    "instagram": "instagram.com", "x": "x.com", "twitter": "x.com",
    "linkedin": "linkedin.com", "tiktok": "tiktok.com", "yelp": "yelp.com",
    "nextdoor": "nextdoor.com", "quora": "quora.com", "pinterest": "pinterest.com",
    "tripadvisor": "tripadvisor.com", "medium": "medium.com",
}
_WEBSITE_NAME_SPLIT_RE = re.compile(r"\s*[·•|]\s*")
_ENGAGEMENT_HINT_RE = re.compile(r"\b(comments?|likes?|views?|followers?|reactions?|ago|subscribers?)\b", re.I)
_HANDLE_RE = re.compile(r"^@?[A-Za-z0-9._-]{2,40}$")
_SUBREDDIT_RE = re.compile(r"^r/([A-Za-z0-9_]{2,25})$")
_HANDLE_PLATFORMS = frozenset({"instagram.com", "tiktok.com", "x.com", "medium.com"})


def _clean_path_hint(hint: Any) -> str | None:
    """Drop empty hints and engagement breadcrumb text ('30+ comments', '2 years ago')."""
    if not isinstance(hint, str) or not hint.strip() or _ENGAGEMENT_HINT_RE.search(hint):
        return None
    return hint.strip()


def website_name_target(website_name: Any) -> dict[str, Any] | None:
    """Resolve a website_name-only SERP item ('Reddit · r/Phoenixville') to a domain + hint.

    Returns None unless the leading segment is an allowlisted platform. The qualifier
    after the middot becomes a path hint for resolve_url search/scoring; it is never
    used to construct a final URL (the ranked thread is not the subreddit front page).
    """
    if not isinstance(website_name, str) or not website_name.strip():
        return None
    flat = website_name.replace("\xa0", " ").strip()
    parts = [p.strip() for p in _WEBSITE_NAME_SPLIT_RE.split(flat) if p.strip()]
    if not parts:
        return None
    platform = parts[0]
    non_engagement = [p for p in parts[1:] if not _ENGAGEMENT_HINT_RE.search(p)]
    qualifier = " · ".join(non_engagement) or None
    domain = WEBSITE_NAME_PLATFORMS.get(platform.casefold())
    if domain is None:
        return None
    path_hint = None
    if qualifier:
        subreddit = _SUBREDDIT_RE.match(qualifier)
        if domain == "reddit.com" and subreddit:
            path_hint = f"r/{subreddit.group(1)}"
        elif domain in _HANDLE_PLATFORMS and _HANDLE_RE.match(qualifier):
            path_hint = qualifier.lstrip("@")
        else:
            path_hint = qualifier  # page / channel / company name: search term only
    return {"target": domain, "domain": domain, "path_hint": path_hint,
            "resolution_basis": "website_name"}


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
    raw_blocks: list[dict[str, Any] | None] = []
    for task in envelope.get("tasks") or []:
        if not isinstance(task, dict):
            continue
        for res_obj in task.get("result") or []:
            if not isinstance(res_obj, dict):
                continue
            si = res_obj.get("serp_integrity")
            raw_blocks.append(si if isinstance(si, dict) else None)
    if not raw_blocks or all(b is None for b in raw_blocks):
        return []
    for block in raw_blocks:
        if block is None:
            found.append({
                "status": "unassessed",
                "reasons": ["SERP result block is missing serp_integrity"],
            })
        else:
            found.append(block)
    return found


def _block_verified(integrity: dict[str, Any]) -> bool:
    basis = integrity.get("verified_basis")
    if basis in LEGACY_PROVIDER_ONLY_BASES:
        return False
    if basis is not None and basis not in TRUSTED_VERIFIED_BASES:
        return False
    return (integrity.get("verified") is True
            and integrity.get("integrity") != "unprotected"
            and integrity.get("status") == "clean"
            and integrity.get("unresolved") is not True)


def serp_verdict(envelope: Any) -> dict[str, Any]:
    """Summarize SERP provenance (never raises). `verified` is the fail-closed gate.

    verified is True only when every organic block carries `serp_integrity.verified: true`,
    is protected (resolve sent), clean, not unresolved, and not stamped with a legacy
    provider-only basis (`provider_from_web`, `double_pull_stable`, `provider_clean_no_decoy_signals`).
    """
    integrities = _integrities(envelope)
    warnings: list[str] = []
    reasons: list[str] = []
    if not integrities:
        return {"status": "unassessed", "verified": False, "suspect": False, "unresolved": False,
                "unverified": True, "unprotected": False, "reasons": ["SERP envelope has no serp_integrity block"],
                "warnings": ["SERP envelope has no serp_integrity block; ranking validity is unknown "
                             "(fetch it with legends-dataforseo)."]}
    statuses = [str(i.get("status") or "unassessed") for i in integrities]
    status = next(
        (s for s in ("unverified_decoy", "suspect_poisoned", "suspect_decoy") if s in statuses),
        next((s for s in statuses if s != "clean"), statuses[0]),
    )
    unresolved = any(i.get("unresolved") is True for i in integrities)
    unprotected = any(i.get("integrity") == "unprotected" for i in integrities)
    verified = all(_block_verified(i) for i in integrities)
    for integrity in integrities:
        for r in list(integrity.get("reasons") or []) + list(integrity.get("unverified_reasons") or []):
            if isinstance(r, str) and r not in reasons:
                reasons.append(r)
        basis = integrity.get("verified_basis")
        if basis in LEGACY_PROVIDER_ONLY_BASES:
            msg = f"SERP used legacy provider-only verification basis ({basis}) without independent consensus"
            if msg not in reasons:
                reasons.append(msg)
            warnings.append(msg + "; re-pull through the SERP Truth Gate.")
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
    from .client import MAX_RESPONSE_BYTES, _safe_local_path

    target = _safe_local_path(path)
    if not target.exists() or not target.is_file():
        raise SafetyError(f"Cannot read SERP envelope {target.name}: not a regular file")
    if target.stat().st_size > MAX_RESPONSE_BYTES:
        raise SafetyError(f"SERP envelope {target.name} exceeds maximum size limit")
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SafetyError(f"Cannot read SERP envelope {target.name}: {exc.__class__.__name__}") from None
    if not isinstance(data, dict):
        raise SafetyError("SERP envelope must be a JSON object")
    # legends-dataforseo evidence exports and CLI --output files may wrap the raw envelope.
    cur = data
    for _ in range(2):
        unwrapped = next(
            (
                cur[key]
                for key in ("response", "envelope")
                if isinstance(cur.get(key), dict)
                and any(k in cur[key] for k in ("tasks", "response", "envelope"))
            ),
            None,
        )
        if unwrapped is None:
            break
        cur = unwrapped
    return cur


def _is_google_wrapper(url: Any) -> bool:
    if not isinstance(url, str):
        return False
    try:
        parsed = urlparse(url.strip())
    except ValueError:
        return False
    host = (parsed.hostname or "").lower().rstrip(".")
    path = parsed.path.lower().rstrip("/")
    return host in {"google.com", "www.google.com"} and path in {"/goto", "/url"}


def serp_targets(envelope: dict[str, Any], *, limit: int = 10) -> dict[str, list[Any]]:
    """Top `limit` organic results split into directly scrapable URLs and /goto items needing resolve.

    Google now wraps most organic links in google.com/goto, which Firecrawl refuses by design.
    Wrapped items are returned under `needs_resolve` with the breadcrumb / domain / path hint /
    title that `lfc resolve` (or `scrape-serp --resolve-goto`) needs; they are never scraped as-is.
    Also returns `direct_items` (rank/url/title/domain) and `ordered_targets` (combined in SERP order).
    """
    if type(limit) is not int or not 1 <= limit <= MAX_SERP_URLS:
        raise SafetyError(f"limit must be between 1 and {MAX_SERP_URLS}")
    urls: list[str] = []
    direct_items: list[dict[str, Any]] = []
    needs: list[dict[str, Any]] = []
    ordered_targets: list[dict[str, Any]] = []
    reached_limit = False
    for task in envelope.get("tasks") or []:
        if reached_limit:
            break
        for res_obj in (task.get("result") or []) if isinstance(task, dict) else []:
            if reached_limit:
                break
            raw_items = (res_obj.get("items") or []) if isinstance(res_obj, dict) else []
            organic_items = [it for it in raw_items if isinstance(it, dict) and it.get("type") == "organic"]
            if organic_items and all(type(it.get("rank_group")) is int for it in organic_items):
                organic_items.sort(key=lambda it: it["rank_group"])
            for item in organic_items:
                if len(urls) + len(needs) >= limit:
                    reached_limit = True
                    break
                res_u = item.get("resolved_url")
                raw_u = item.get("url")
                url = raw_u if (_is_google_wrapper(res_u) and isinstance(raw_u, str) and not _is_google_wrapper(raw_u)) else (res_u or raw_u)
                if _is_google_wrapper(url):
                    raw_dom = item.get("resolved_domain") or item.get("domain")
                    domain = raw_dom.strip().rstrip(".") if isinstance(raw_dom, str) and raw_dom.strip() else None
                    if domain and (domain.lower().removeprefix("www.") == "google.com" or domain.lower().endswith(".google.com")):
                        domain = None
                    raw_bc = item.get("breadcrumb")
                    breadcrumb = raw_bc.strip() if isinstance(raw_bc, str) and raw_bc.strip() else None
                    bc_is_url = False
                    if breadcrumb and breadcrumb.startswith(("http://", "https://")):
                        bc_first = re.split(r"\s*(?:\u203a|\u00bb|\ufffd|>)\s*", breadcrumb, maxsplit=1)[0].strip()
                        try:
                            bc_host = (urlparse(bc_first).hostname or "").lower().rstrip(".")
                        except ValueError:
                            bc_host = ""
                        bc_is_url = bool(bc_host) and bc_host.removeprefix("www.") != "google.com" and not bc_host.endswith(".google.com")
                    target = breadcrumb if bc_is_url else domain
                    entry: dict[str, Any] = {"rank": item.get("rank_group"), "target": target, "domain": domain,
                                             "path_hint": _clean_path_hint(item.get("breadcrumb_path_hint")),
                                             "title": item.get("title"), "website_name": item.get("website_name"),
                                             "resolution_basis": "breadcrumb" if target else "none"}
                    via_name = website_name_target(item.get("website_name"))
                    if via_name and target is None:
                        entry.update(target=via_name["target"], domain=via_name["domain"],
                                     path_hint=via_name["path_hint"] or entry["path_hint"],
                                     resolution_basis="website_name")
                    elif via_name and entry["path_hint"] is None and isinstance(domain, str):
                        dom_clean = domain.lower().removeprefix("www.")
                        if dom_clean == via_name["domain"] or dom_clean.endswith("." + via_name["domain"]):
                            entry["path_hint"] = via_name["path_hint"]  # domain wins; name only enriches
                    needs.append(entry)
                    ordered_targets.append({"kind": "goto", **entry})
                elif isinstance(url, str) and url.strip().startswith(("http://", "https://")):
                    clean_url = url.strip()
                    if clean_url in urls:
                        continue
                    raw_direct_dom = item.get("resolved_domain") or item.get("domain")
                    direct_domain = raw_direct_dom.strip().rstrip(".") if isinstance(raw_direct_dom, str) and raw_direct_dom.strip() else None
                    if not direct_domain or direct_domain.lower().removeprefix("www.") == "google.com" or direct_domain.lower().endswith(".google.com"):
                        try:
                            direct_domain = (urlparse(clean_url).hostname or "").lower().rstrip(".") or None
                        except ValueError:
                            direct_domain = None
                    direct_entry: dict[str, Any] = {
                        "rank": item.get("rank_group"),
                        "url": clean_url,
                        "title": item.get("title"),
                        "domain": direct_domain,
                    }
                    urls.append(clean_url)
                    direct_items.append(direct_entry)
                    ordered_targets.append({"kind": "direct", **direct_entry})
    if ordered_targets and all(type(t.get("rank")) is int for t in ordered_targets):
        ordered_targets.sort(key=lambda t: t["rank"])
        urls = [t["url"] for t in ordered_targets if t["kind"] == "direct"]
        direct_items = [{k: v for k, v in t.items() if k != "kind"} for t in ordered_targets if t["kind"] == "direct"]
        needs = [{k: v for k, v in t.items() if k != "kind"} for t in ordered_targets if t["kind"] == "goto"]
    return {
        "urls": urls,
        "direct_items": direct_items,
        "needs_resolve": needs,
        "ordered_targets": ordered_targets,
    }


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
