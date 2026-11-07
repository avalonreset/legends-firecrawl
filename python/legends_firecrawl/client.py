"""Credential-safe direct Firecrawl API client for house consumers.

The official ``firecrawl`` CLI remains the human/agent spine. This module is a
small compatibility surface for products such as Legends Packet that need a
Python API without installing a vendor SDK or an MCP server.
"""

from __future__ import annotations

import ipaddress
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


DEFAULT_API_ROOT = "https://api.firecrawl.dev"
JOB_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{12,128}$")


class CredentialError(RuntimeError):
    """Raised when the house API key is unavailable."""


class ApiError(RuntimeError):
    """Provider failure with complete received response, when available."""
    def __init__(self, message, *, response=None, request_may_have_completed=True):
        super().__init__(message)
        self.response = response
        self.request_may_have_completed = request_may_have_completed


class SafetyError(ValueError):
    """Raised before HTTP when a target or scope violates house bounds."""


@dataclass(frozen=True)
class Credentials:
    api_key: str
    source: str


def _windows_user_environment(name: str) -> str | None:
    if os.name != "nt":
        return None
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, name)
    except (ImportError, FileNotFoundError, OSError):
        return None
    return value if isinstance(value, str) and value else None


def read_api_key_file(path: str | Path) -> str:
    p = Path(path)
    if p.is_symlink():
        raise SafetyError("Refusing to read symlink API key file.")
    if not p.exists() or not p.is_file():
        raise CredentialError("FIRECRAWL_API_KEY_FILE does not exist or is not a regular file.")
    secret = p.read_text(encoding="utf-8").strip()
    if not secret:
        raise CredentialError("FIRECRAWL_API_KEY_FILE is empty.")
    return secret


def load_credentials() -> Credentials:
    value = os.environ.get("FIRECRAWL_API_KEY")
    if value:
        return Credentials(value, "process-env")
    key_file = os.environ.get("FIRECRAWL_API_KEY_FILE")
    if key_file:
        return Credentials(read_api_key_file(key_file), "key-file")
    if not os.environ.get("FIRECRAWL_DISABLE_USER_ENV"):
        value = _windows_user_environment("FIRECRAWL_API_KEY")
        if value:
            return Credentials(value, "user-env")
    raise CredentialError(
        "FIRECRAWL_API_KEY is unavailable at process or Windows user scope. "
        "Configure FIRECRAWL_API_KEY in your environment, "
        "then run python -m legends_firecrawl doctor."
    )


def credential_status() -> dict[str, Any]:
    try:
        credentials = load_credentials()
    except CredentialError:
        return {"present": False, "source": "missing", "length": 0}
    return {"present": True, "source": credentials.source, "length": len(credentials.api_key)}


def api_root() -> str:
    root = os.environ.get("FIRECRAWL_API_URL", DEFAULT_API_ROOT).strip().rstrip("/")
    parsed = urlparse(root)
    if parsed.scheme != "https" or not parsed.hostname:
        raise SafetyError("FIRECRAWL_API_URL must be an HTTPS API root.")
    return root


def validate_public_url(value: str) -> str:
    raw = value.strip()
    if not raw:
        raise SafetyError("URL is required.")
    parsed = urlparse(raw)
    if parsed.scheme not in {"http", "https"}:
        raise SafetyError("Only public HTTP(S) URLs are supported.")
    if not parsed.hostname:
        raise SafetyError("URL must include a hostname.")
    if parsed.username or parsed.password:
        raise SafetyError("Credentials embedded in URLs are forbidden.")
    host = parsed.hostname.lower().rstrip(".")
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
        raise SafetyError("Local hosts are outside the Kit's public-web boundary.")
    if host in {"google.com", "www.google.com"} and parsed.path.lower() in {"/goto", "/url"}:
        raise SafetyError(
            "Opaque Google redirect wrapper URLs (/goto or /url) cannot be scraped directly. "
            "Pass the resolved target domain or use 'lfc resolve <domain> --path-hint ...' first."
        )
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address is not None and not address.is_global:
        raise SafetyError("Private, loopback, reserved, and link-local IP targets are forbidden.")
    return raw


def _kit_root() -> Path | None:
    configured = os.environ.get("LEGENDS_FIRECRAWL_HOME")
    if configured:
        return Path(configured).expanduser()
    source_root = Path(__file__).resolve().parents[2]
    marker = source_root / ".legends-module"
    if marker.is_file() and marker.read_text(encoding="utf-8").strip() == "legends-firecrawl":
        return source_root
    return None


def ledger_path() -> Path:
    configured = os.environ.get("LEGENDS_FIRECRAWL_LEDGER")
    if configured:
        return Path(configured).expanduser()
    root = _kit_root()
    if root is not None:
        return root / "var" / "usage-ledger.jsonl"
    state_root = Path(os.environ.get("LOCALAPPDATA") or (Path.home() / ".local" / "state"))
    return state_root / "Legends" / "Firecrawl" / "usage-ledger.jsonl"


def _extract_credit_signal(response: dict[str, Any]) -> float | int | None:
    for key in ("creditsUsed", "credits_used", "costCredits", "cost_credits"):
        value = response.get(key)
        if isinstance(value, (int, float)):
            return value
    metadata = response.get("metadata")
    if isinstance(metadata, dict):
        for key in ("creditsUsed", "credits_used"):
            value = metadata.get(key)
            if isinstance(value, (int, float)):
                return value
    return None


def _append_ledger(
    route: str,
    response: dict[str, Any],
    *,
    consumer: str,
    requested_scope: dict[str, Any] | None = None,
) -> None:
    target = ledger_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "route": route,
        "consumer": consumer,
        "success": bool(response.get("success", True)),
        "credits_reported": _extract_credit_signal(response),
        "requested_scope": requested_scope or {},
    }
    with target.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, separators=(",", ":"), ensure_ascii=False) + "\n")


def load_routes() -> dict[str, Any]:
    return json.loads(Path(__file__).with_name("routes.json").read_text(encoding="utf-8"))


def route_for(operation: str) -> dict[str, Any]:
    needle = operation.strip().lower()
    for route in load_routes()["routes"]:
        if route["name"] == needle or needle in route.get("aliases", []):
            return route
    raise SafetyError(f"Unknown first-class operation '{operation}'. Run 'lfc routes'.")


def estimate(operation: str, *, limit: int | None = None, formats: list[str] | None = None) -> dict[str, Any]:
    route = route_for(operation)
    default_scope = dict(route.get("default_scope") or {})
    if limit is not None:
        if limit < 1:
            raise SafetyError("limit must be positive")
        default_scope["limit"] = limit
    if formats:
        default_scope["formats"] = formats
    page_ceiling = 0
    if route["name"] == "scrape":
        page_ceiling = 1
    elif route["name"] in {"map", "search", "resolve", "crawl"}:
        page_ceiling = int(default_scope.get("limit") or 0)
    return {
        "operation": route["name"],
        "charged": route["charged"],
        "estimate_only": True,
        "requested_scope": default_scope,
        "page_or_result_ceiling": page_ceiling,
        "estimated_credits": None if route["charged"] else 0,
        "note": (
            "Firecrawl billing varies by endpoint, formats, proxy, parsing, and current plan. "
            "The Kit reports bounded scope and actual provider-reported credits when returned; "
            "it does not invent a dollar estimate."
        ),
    }


def _error_detail(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")[:1000]
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return text or "no response body"
    if isinstance(payload, dict):
        return str(payload.get("error") or payload.get("message") or payload.get("code") or "request rejected")
    return "request rejected"


class FirecrawlClient:
    """Bounded Firecrawl v2 API client."""

    def __init__(self, credentials: Credentials | None = None, *, timeout: int = 90, consumer: str = "python"):
        self.credentials = credentials or load_credentials()
        self.timeout = timeout
        self.consumer = consumer

    def request(
        self,
        path: str,
        *,
        method: str = "GET",
        payload: dict[str, Any] | None = None,
        log_usage: bool = False,
        requested_scope: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        from . import __version__
        normalized = "/" + path.strip().lstrip("/")
        body = None if payload is None else json.dumps(payload, separators=(",", ":")).encode("utf-8")
        request = Request(
            api_root() + normalized,
            data=body,
            method=method.upper(),
            headers={
                "Authorization": f"Bearer {self.credentials.api_key}",
                "Content-Type": "application/json",
                "User-Agent": f"legends-firecrawl/{__version__}",
            },
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:  # nosec B310 - fixed HTTPS root
                raw = response.read().decode("utf-8")
                result = json.loads(raw)
        except HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try: received = json.loads(raw)
            except json.JSONDecodeError: received = {"raw_text":raw}
            raise ApiError(f"Firecrawl returned HTTP {exc.code} for {normalized}", response=received) from exc
        except URLError as exc:
            raise ApiError(f"Could not reach Firecrawl for {normalized}: {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise ApiError(f"Firecrawl returned invalid JSON for {normalized}", response={"raw_text":raw}) from exc
        if not isinstance(result, dict):
            raise ApiError(f"Firecrawl returned an unexpected response for {normalized}", response={"provider_response":result})
        if result.get("success") is False:
            raise ApiError(f"Firecrawl rejected {normalized}", response=result)
        if log_usage:
            _append_ledger(normalized, result, consumer=self.consumer, requested_scope=requested_scope)
        return result

    def credit_usage(self) -> dict[str, Any]:
        return self.request("/v2/team/credit-usage")

    def scrape(
        self,
        url: str,
        *,
        formats: list[str] | None = None,
        only_main_content: bool = True,
        max_age_ms: int = 86_400_000,
        country: str = "US",
    ) -> dict[str, Any]:
        target = validate_public_url(url)
        selected = formats or ["markdown"]
        allowed = {"markdown", "html", "rawHtml", "links", "images", "summary", "branding"}
        unknown = [item for item in selected if item not in allowed]
        if unknown:
            raise SafetyError(f"Unsupported default-safe scrape formats: {', '.join(unknown)}")
        if not 0 <= max_age_ms <= 604_800_000:
            raise SafetyError("max_age_ms must be between 0 and seven days")
        payload = {
            "url": target,
            "formats": selected,
            "onlyMainContent": only_main_content,
            "onlyCleanContent": True,
            "maxAge": max_age_ms,
            "location": {"country": country.upper(), "languages": ["en-US"]},
            "removeBase64Images": True,
            "blockAds": True,
            "storeInCache": False,
        }
        return self.request(
            "/v2/scrape",
            method="POST",
            payload=payload,
            log_usage=True,
            requested_scope={"pages": 1, "formats": selected, "max_age_ms": max_age_ms},
        )

    def map_site(
        self,
        url: str,
        *,
        limit: int = 100,
        search: str | None = None,
        sitemap: str = "include",
        include_subdomains: bool = False,
    ) -> dict[str, Any]:
        target = validate_public_url(url)
        if not 1 <= limit <= 1000:
            raise SafetyError("map limit must be between 1 and 1000")
        if sitemap not in {"only", "include", "skip"}:
            raise SafetyError("sitemap must be only, include, or skip")
        payload: dict[str, Any] = {
            "url": target,
            "limit": limit,
            "sitemap": sitemap,
            "includeSubdomains": include_subdomains,
            "ignoreQueryParameters": True,
        }
        if search:
            payload["search"] = search
        return self.request(
            "/v2/map",
            method="POST",
            payload=payload,
            log_usage=True,
            requested_scope={"limit": limit, "include_subdomains": include_subdomains},
        )

    def search(
        self,
        query: str,
        *,
        limit: int = 5,
        country: str = "US",
        location: str | None = None,
        scrape_results: bool = False,
    ) -> dict[str, Any]:
        needle = query.strip()
        if not needle:
            raise SafetyError("search query is required")
        if not 1 <= limit <= 20:
            raise SafetyError("house search limit must be between 1 and 20")
        payload: dict[str, Any] = {
            "query": needle,
            "limit": limit,
            "sources": ["web"],
            "country": country.upper(),
        }
        if location:
            payload["location"] = location
        if scrape_results:
            payload["scrapeOptions"] = {"formats": ["markdown"], "onlyMainContent": True}
        return self.request(
            "/v2/search",
            method="POST",
            payload=payload,
            log_usage=True,
            requested_scope={"limit": limit, "scrape_results": scrape_results},
        )

    @staticmethod
    def _parse_domain_or_breadcrumb(raw_target: str, path_hint: str | None = None) -> tuple[str, str, str | None]:
        cleaned = (raw_target or "").strip()
        if not cleaned:
            raise SafetyError("Target domain or URL is required.")
        split_parts = [seg.strip() for seg in re.split(r"\s*(?:\u203a|\u00bb|\ufffd|>)\s*", cleaned) if seg.strip()]
        first = split_parts[0] if split_parts else cleaned
        extracted_hint = path_hint.strip().rstrip(".\u2026").strip() if isinstance(path_hint, str) and path_hint.strip() else None
        if not extracted_hint and len(split_parts) > 1:
            for seg in reversed(split_parts[1:]):
                cand = seg.strip().rstrip(".\u2026").strip()
                if cand and cand not in {"...", "\u2026"}:
                    extracted_hint = cand
                    break
        if "://" not in first:
            first = "https://" + first.lstrip("/")
        validated = validate_public_url(first)
        parsed = urlparse(validated)
        host = (parsed.hostname or "").lower().rstrip(".")
        base_url = f"{parsed.scheme}://{host}"
        if not extracted_hint and parsed.path and parsed.path not in {"", "/"}:
            segs = [s.strip().rstrip(".\u2026") for s in parsed.path.split("/") if s.strip()]
            if segs:
                extracted_hint = segs[-1]
        return base_url, host.removeprefix("www."), extracted_hint

    @staticmethod
    def _extract_candidate_urls(payload: dict[str, Any], expected_domain: str) -> list[str]:
        urls: list[str] = []
        sources = []
        for key in ("links", "data", "results"):
            val = payload.get(key)
            if isinstance(val, list):
                sources.extend(val)
            elif isinstance(val, dict):
                for subkey in ("web", "links", "results"):
                    if isinstance(val.get(subkey), list):
                        sources.extend(val[subkey])
        for entry in sources:
            u = entry if isinstance(entry, str) else (entry.get("url") if isinstance(entry, dict) else None)
            if not isinstance(u, str) or not u.startswith(("http://", "https://")):
                continue
            host = (urlparse(u).hostname or "").lower().rstrip(".").removeprefix("www.")
            if host == expected_domain or host.endswith("." + expected_domain):
                if u not in urls:
                    urls.append(u)
        return urls

    @staticmethod
    def _score_candidate_url(url: str, *, path_hint: str | None, title: str | None, keyword: str | None) -> int:
        parsed = urlparse(url)
        path_lower = (parsed.path or "/").lower()
        score = 0
        if path_lower not in {"", "/"}:
            score += 5
        if path_hint:
            hint_clean = path_hint.lower().strip().rstrip(".\u2026")
            hint_slug = re.sub(r"[^a-z0-9]+", "-", hint_clean).strip("-")
            if hint_clean and hint_clean in path_lower:
                score += 100
            elif hint_slug and hint_slug in path_lower:
                score += 90
            else:
                for tok in re.findall(r"[a-z0-9]{3,}", hint_clean):
                    if tok in path_lower:
                        score += 15
        for text in (title, keyword):
            if text:
                for tok in re.findall(r"[a-z0-9]{3,}", text.lower()):
                    if tok in path_lower:
                        score += 8
        return score

    def resolve_url(
        self,
        domain_or_url: str,
        *,
        path_hint: str | None = None,
        title: str | None = None,
        keyword: str | None = None,
        limit: int = 25,
        scrape: bool = False,
        formats: list[str] | None = None,
        country: str = "US",
    ) -> dict[str, Any]:
        """Resolve an exact inner URL from a domain + breadcrumb slug/title hint and optionally scrape it."""
        if not 1 <= limit <= 200:
            raise SafetyError("resolve limit must be between 1 and 200")
        base_url, root_domain, effective_hint = self._parse_domain_or_breadcrumb(domain_or_url, path_hint)
        search_term = effective_hint or title or keyword
        map_resp = self.map_site(base_url, limit=limit, search=search_term)
        candidates = self._extract_candidate_urls(map_resp, root_domain)
        method_used = "map"

        scored = sorted(
            candidates,
            key=lambda u: self._score_candidate_url(u, path_hint=effective_hint, title=title, keyword=keyword),
            reverse=True,
        )
        best_score = (
            self._score_candidate_url(scored[0], path_hint=effective_hint, title=title, keyword=keyword)
            if scored
            else 0
        )

        if (not scored or (search_term and best_score < 15)) and (title or effective_hint or keyword):
            query_parts = [f"site:{root_domain}"]
            if title:
                query_parts.append(title)
            elif effective_hint:
                query_parts.append(effective_hint.replace("-", " "))
            elif keyword:
                query_parts.append(keyword)
            search_resp = self.search(" ".join(query_parts), limit=min(5, limit), country=country, scrape_results=False)
            search_candidates = self._extract_candidate_urls(search_resp, root_domain)
            for sc in search_candidates:
                if sc not in candidates:
                    candidates.append(sc)
            if search_candidates:
                scored = sorted(
                    candidates,
                    key=lambda u: self._score_candidate_url(u, path_hint=effective_hint, title=title, keyword=keyword),
                    reverse=True,
                )
                method_used = "map+search" if map_resp else "search"

        resolved_url = scored[0] if scored else base_url
        result: dict[str, Any] = {
            "success": True,
            "domain": root_domain,
            "base_url": base_url,
            "resolved_url": resolved_url,
            "resolution_method": method_used,
            "path_hint": effective_hint,
            "title": title,
            "candidates": scored[:10],
        }
        if scrape:
            result["scraped"] = self.scrape(resolved_url, formats=formats or ["markdown"], country=country)
        return result

    @staticmethod
    def crawl_preview(
        url: str,
        *,
        limit: int = 25,
        max_depth: int = 2,
        include_paths: list[str] | None = None,
        exclude_paths: list[str] | None = None,
    ) -> dict[str, Any]:
        target = validate_public_url(url)
        if not 1 <= limit <= 100:
            raise SafetyError("house crawl limit must be between 1 and 100")
        if not 0 <= max_depth <= 5:
            raise SafetyError("house crawl depth must be between 0 and 5")
        return {
            "operation": "crawl",
            "dry_run": True,
            "requires_confirm": True,
            "url": target,
            "limit": limit,
            "max_depth": max_depth,
            "include_paths": include_paths or [],
            "exclude_paths": exclude_paths or [],
            "estimated_credits": None,
            "note": "No HTTP request was made. Review scope and re-run crawl with --confirm.",
        }

    def crawl(
        self,
        url: str,
        *,
        confirm: bool = False,
        limit: int = 25,
        max_depth: int = 2,
        include_paths: list[str] | None = None,
        exclude_paths: list[str] | None = None,
    ) -> dict[str, Any]:
        preview = self.crawl_preview(
            url,
            limit=limit,
            max_depth=max_depth,
            include_paths=include_paths,
            exclude_paths=exclude_paths,
        )
        if not confirm:
            raise SafetyError("crawl is multi-page and requires --confirm after reviewing crawl-preview")
        payload = {
            "url": preview["url"],
            "limit": limit,
            "maxDiscoveryDepth": max_depth,
            "includePaths": include_paths or [],
            "excludePaths": exclude_paths or [],
            "ignoreQueryParameters": True,
            "crawlEntireDomain": False,
            "allowExternalLinks": False,
            "allowSubdomains": False,
            "scrapeOptions": {
                "formats": ["markdown"],
                "onlyMainContent": True,
                "onlyCleanContent": True,
                "removeBase64Images": True,
                "blockAds": True,
                "storeInCache": False,
            },
        }
        return self.request(
            "/v2/crawl",
            method="POST",
            payload=payload,
            log_usage=True,
            requested_scope={"limit": limit, "max_depth": max_depth},
        )

    def crawl_status(self, job_id: str) -> dict[str, Any]:
        value = job_id.strip()
        if not JOB_ID_PATTERN.fullmatch(value):
            raise SafetyError("crawl job id format is invalid")
        return self.request(f"/v2/crawl/{value}")


def usage_summary(path: Path | None = None) -> dict[str, Any]:
    target = path or ledger_path()
    if not target.is_file():
        return {"ledger": str(target), "calls": 0, "reported_credits": 0, "unreported_calls": 0, "routes": {}}
    calls = 0
    reported = 0.0
    unreported = 0
    routes: dict[str, int] = {}
    for raw in target.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        row = json.loads(raw)
        calls += 1
        routes[row["route"]] = routes.get(row["route"], 0) + 1
        credits = row.get("credits_reported")
        if isinstance(credits, (int, float)):
            reported += float(credits)
        else:
            unreported += 1
    return {
        "ledger": str(target),
        "calls": calls,
        "reported_credits": reported,
        "unreported_calls": unreported,
        "routes": routes,
        "warning": "reported_credits is incomplete when the provider omits per-response credit usage",
    }

