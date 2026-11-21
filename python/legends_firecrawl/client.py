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
import socket
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlparse
from urllib.request import HTTPRedirectHandler, HTTPSHandler, ProxyHandler, Request, build_opener
from uuid import uuid4


DEFAULT_API_ROOT = "https://api.firecrawl.dev"
ALLOWED_API_HOSTS = frozenset({"api.firecrawl.dev"})
MAX_RESPONSE_BYTES = 50 * 1024 * 1024
MAX_ERROR_BYTES = 4 * 1024 * 1024
MAX_PARSE_BYTES = 50 * 1024 * 1024
JOB_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{12,128}$")
RESOURCE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{3,128}$")
_MACOS_SYSTEM_SYMLINKS = {Path("/var"), Path("/tmp"), Path("/etc")}
SCRAPE_ALLOWED_FORMATS = frozenset({"markdown", "html", "rawHtml", "links", "images", "summary", "branding"})
PARSE_ALLOWED_FORMATS = frozenset({"markdown", "html", "rawHtml", "links", "images", "summary", "json", "attributes"})
PARSE_CONTENT_TYPES = {
    ".html": "text/html",
    ".htm": "text/html",
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".doc": "application/msword",
    ".odt": "application/vnd.oasis.opendocument.text",
    ".rtf": "application/rtf",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xls": "application/vnd.ms-excel",
}
PARSE_SUPPORTED_EXTENSIONS = frozenset(PARSE_CONTENT_TYPES)
AGENT_MODELS = frozenset({"spark-1-mini", "spark-1-pro"})
MAX_AGENT_CREDITS = 500
INTERACT_LANGUAGES = frozenset({"node", "python", "bash"})
MONITOR_ACTIONS = frozenset({"create", "list", "get", "update", "delete", "run", "checks", "check"})
MONITOR_MUTATING_ACTIONS = frozenset({"create", "update", "delete", "run"})
MONITOR_SEARCH_WINDOWS = frozenset({"5m", "15m", "1h", "6h", "24h", "7d"})
MONITOR_PAGE_STATUSES = frozenset({"same", "new", "changed", "removed", "error"})
SEARCH_FEEDBACK_RATINGS = frozenset({"good", "bad", "partial"})
SEARCH_FEEDBACK_OPT_OUT_ENVS = ("FIRECRAWL_NO_SEARCH_FEEDBACK", "FIRECRAWL_DISABLE_SEARCH_FEEDBACK")
RESEARCH_MODES = frozenset({"papers", "inspect", "related", "read", "github"})
RESEARCH_RELATION_MODES = frozenset({"similar", "citers", "references"})


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _ssl_context():
    """Return a certifi-backed SSL context when certifi is importable."""
    try:
        import certifi
        import ssl

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return None


def urlopen(request: Request, timeout: float = 90):
    """Open request with redirects and ambient proxy overrides disabled."""
    handlers: list[Any] = [ProxyHandler({}), _NoRedirect()]
    ctx = _ssl_context()
    if ctx is not None:
        handlers.insert(1, HTTPSHandler(context=ctx))
    return build_opener(*handlers).open(request, timeout=timeout)


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


def _safe_local_path(value: str | Path) -> Path:
    """Refuse symlinks and Windows reparse points across leaf and non-system parents."""
    p = Path(value).expanduser().absolute()
    for idx, part in enumerate((p, *p.parents)):
        if idx > 0 and sys.platform == "darwin" and part in _MACOS_SYSTEM_SYMLINKS:
            continue
        if part.is_symlink() or getattr(part, "is_junction", lambda: False)():
            raise SafetyError("Refusing to access symlink or junction path.")
        try:
            st = part.lstat()
            if getattr(st, "st_reparse_tag", 0) == 0xA0000003 or (
                getattr(st, "st_file_attributes", 0) & 0x400
            ):
                raise SafetyError("Refusing to access reparse-point path.")
        except OSError:
            pass
    return p


def read_api_key_file(path: str | Path) -> str:
    p = _safe_local_path(path)
    if not p.exists() or not p.is_file():
        raise CredentialError("FIRECRAWL_API_KEY_FILE does not exist or is not a regular file.")
    if p.stat().st_size > 65536:
        raise SafetyError("FIRECRAWL_API_KEY_FILE exceeds maximum size limit.")
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


def _is_public_ip(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    if not (
        address.is_global
        and not address.is_loopback
        and not address.is_private
        and not address.is_link_local
        and not address.is_reserved
        and not address.is_multicast
        and not address.is_unspecified
    ):
        return False
    for attr in ("ipv4_mapped", "sixtofour"):
        inner = getattr(address, attr, None)
        if inner is not None and not _is_public_ip(inner):
            return False
    teredo = getattr(address, "teredo", None)
    if teredo is not None:
        if any(not _is_public_ip(ep) for ep in teredo if ep is not None):
            return False
    return True


def api_root(*, allow_custom: bool = False) -> str:
    root = os.environ.get("FIRECRAWL_API_URL", DEFAULT_API_ROOT).strip().rstrip("/")
    parsed = urlparse(root)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise SafetyError("FIRECRAWL_API_URL must be an HTTPS API root without embedded credentials.")
    host = parsed.hostname.lower().rstrip(".")
    custom_allowed = allow_custom or os.environ.get("FIRECRAWL_ALLOW_CUSTOM_API_URL") == "1"
    if host not in ALLOWED_API_HOSTS:
        if not custom_allowed:
            raise SafetyError(
                "FIRECRAWL_API_URL host is not in the default allowlist (api.firecrawl.dev). "
                "Pass --allow-custom-api-url or set FIRECRAWL_ALLOW_CUSTOM_API_URL=1 for a verified self-hosted HTTPS endpoint."
            )
        validate_public_url(root)
    return root


def validate_public_url(value: str, *, resolve_dns: bool = True) -> str:
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
    if (
        host in {"localhost", "localhost.localdomain"}
        or host.endswith((".local", ".localhost", ".internal"))
    ):
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
    if address is not None:
        if not _is_public_ip(address):
            raise SafetyError("Private, loopback, reserved, and link-local IP targets are forbidden.")
        return raw
    labels = host.split(".")
    if len(labels) < 2 or any(
        not lbl or lbl.isdigit() or re.fullmatch(r"0x[0-9a-f]+", lbl) for lbl in labels
    ):
        raise SafetyError("Numeric or single-label hostnames are forbidden.")
    if resolve_dns:
        try:
            infos = socket.getaddrinfo(host, None)
        except OSError:
            infos = []
        for info in infos:
            sockaddr = info[4]
            if not sockaddr:
                continue
            ip_text = str(sockaddr[0]).split("%", 1)[0]
            try:
                resolved_ip = ipaddress.ip_address(ip_text)
            except ValueError:
                continue
            if not _is_public_ip(resolved_ip):
                raise SafetyError("Hostname resolves to a non-public IP address.")
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
    credit_keys = ("creditsUsed", "credits_used", "costCredits", "cost_credits")
    containers: list[Any] = [response, response.get("metadata")]
    data = response.get("data")
    if isinstance(data, dict):
        containers.append(data)
        containers.append(data.get("metadata"))
    for container in containers:
        if not isinstance(container, dict):
            continue
        for key in credit_keys:
            value = container.get(key)
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return value
    return None


def _normalize_ledger_route(route: str) -> str:
    route_clean = route.split("?", 1)[0]
    route_clean = re.sub(r"^/v2/scrape/[^/]+/interact$", "/v2/scrape/{id}/interact", route_clean)
    route_clean = re.sub(r"^/v2/monitor/[^/]+/run$", "/v2/monitor/{id}/run", route_clean)
    route_clean = re.sub(
        r"^/v2/search/research/papers/[^/]+(/similar)?$",
        r"/v2/search/research/papers/{id}\1",
        route_clean,
    )
    return route_clean


def _append_ledger(
    route: str,
    response: dict[str, Any],
    *,
    consumer: str,
    requested_scope: dict[str, Any] | None = None,
) -> None:
    target = _safe_local_path(ledger_path())
    target.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "route": _normalize_ledger_route(route),
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
    if route["name"] in {"scrape", "parse"}:
        page_ceiling = 1
    elif route["name"] in {"map", "search", "developer", "research", "resolve", "crawl"}:
        page_ceiling = int(default_scope.get("limit") or 0)
    estimated_credits: int | None
    if not route["charged"]:
        estimated_credits = 0
    elif isinstance(default_scope.get("estimated_credits"), int):
        estimated_credits = int(default_scope["estimated_credits"])
    else:
        estimated_credits = None
    return {
        "operation": route["name"],
        "charged": route["charged"],
        "estimate_only": True,
        "requested_scope": default_scope,
        "page_or_result_ceiling": page_ceiling,
        "max_api_requests": (3 if default_scope.get("scrape") else 2) if route["name"] == "resolve" else 1,
        "estimated_credits": estimated_credits,
        "note": (
            "Firecrawl billing varies by endpoint, formats, proxy, parsing, and current plan. "
            "The Kit reports bounded scope and actual provider-reported credits when returned; "
            "it does not invent a dollar estimate."
        ),
    }


def _validate_resource_id(value: str, label: str) -> str:
    cleaned = (value or "").strip()
    if not RESOURCE_ID_PATTERN.fullmatch(cleaned):
        raise SafetyError(f"{label} format is invalid")
    return cleaned


def _validate_paper_id(value: str) -> str:
    cleaned = (value or "").strip()
    if not cleaned or len(cleaned) > 200 or ".." in cleaned or any(ord(ch) < 32 or ch.isspace() for ch in cleaned):
        raise SafetyError("paper id format is invalid")
    return cleaned


def _encode_multipart(
    file_field: str,
    filename: str,
    content_type: str,
    file_bytes: bytes,
    fields: dict[str, str],
) -> tuple[bytes, str]:
    boundary = f"legendsfc{uuid4().hex}"
    safe_name = filename.replace("\\", "_").replace("/", "_").replace('"', "_").replace("\r", "").replace("\n", "")
    chunks: list[bytes] = []
    chunks.append(
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{file_field}"; filename="{safe_name}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8")
    )
    chunks.append(file_bytes)
    chunks.append(b"\r\n")
    for key, val in fields.items():
        chunks.append(
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
                f"{val}\r\n"
            ).encode("utf-8")
        )
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def is_search_feedback_disabled_locally() -> bool:
    truthy = {"1", "true", "yes", "on"}
    return any(os.environ.get(name, "").strip().lower() in truthy for name in SEARCH_FEEDBACK_OPT_OUT_ENVS)


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
        raw_body: bytes | None = None,
        content_type: str | None = None,
        extra_headers: dict[str, str] | None = None,
        log_usage: bool = False,
        requested_scope: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        from . import __version__
        normalized = "/" + path.strip().lstrip("/")
        if raw_body is not None:
            body = raw_body
            resolved_ct = content_type or "application/octet-stream"
        else:
            body = None if payload is None else json.dumps(payload, separators=(",", ":")).encode("utf-8")
            resolved_ct = content_type or "application/json"
        headers = {
            "Authorization": f"Bearer {self.credentials.api_key}",
            "Content-Type": resolved_ct,
            "User-Agent": f"legends-firecrawl/{__version__}",
        }
        if extra_headers:
            for k, v in extra_headers.items():
                if k.lower() not in {"authorization", "user-agent"}:
                    headers[k] = v
        request = Request(
            api_root() + normalized,
            data=body,
            method=method.upper(),
            headers=headers,
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:  # nosec B310 - fixed HTTPS root
                raw_bytes = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw_bytes) > MAX_RESPONSE_BYTES:
                raise ApiError(f"Firecrawl response exceeds maximum size limit for {normalized}")
            raw = raw_bytes.decode("utf-8")
            result = json.loads(raw)
        except HTTPError as exc:
            raw = exc.read(MAX_ERROR_BYTES + 1)[:MAX_ERROR_BYTES].decode("utf-8", errors="replace")
            try: received = json.loads(raw)
            except json.JSONDecodeError: received = {"raw_text":raw}
            raise ApiError(f"Firecrawl returned HTTP {exc.code} for {normalized}", response=received) from exc
        except URLError as exc:
            raise ApiError(f"Could not reach Firecrawl for {normalized}: {exc.reason}") from exc
        except UnicodeDecodeError as exc:
            raise ApiError(
                f"Firecrawl returned non-UTF-8 response for {normalized}",
                response={"raw_text": raw_bytes[:1000].decode("utf-8", errors="replace")},
            ) from exc
        except json.JSONDecodeError as exc:
            raise ApiError(f"Firecrawl returned invalid JSON for {normalized}", response={"raw_text":raw}) from exc
        if not isinstance(result, dict):
            raise ApiError(f"Firecrawl returned an unexpected response for {normalized}", response={"provider_response":result})
        if result.get("success") is False:
            raise ApiError(f"Firecrawl rejected {normalized}", response=result)
        if log_usage:
            _append_ledger(
                _normalize_ledger_route(normalized),
                result,
                consumer=self.consumer,
                requested_scope=requested_scope,
            )
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
    def _extract_candidate_urls(
        payload: dict[str, Any],
        expected_domain: str,
        *,
        include_subdomains: bool = False,
    ) -> list[str]:
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
            if host == expected_domain or (include_subdomains and host.endswith("." + expected_domain)):
                if u not in urls:
                    urls.append(u)
        return urls

    @staticmethod
    def _score_candidate_url(url: str, *, path_hint: str | None, title: str | None, keyword: str | None) -> int:
        parsed = urlparse(url)
        path_lower = (parsed.path or "/").lower()
        score = 0
        has_hint = bool(path_hint and path_hint.strip())
        if has_hint and path_lower not in {"", "/"}:
            score += 5
        if has_hint and path_hint is not None:
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
        only_main_content: bool = True,
        max_age_ms: int = 86_400_000,
        country: str = "US",
        require_candidate: bool = False,
        allow_homepage_shortcircuit: bool = False,
    ) -> dict[str, Any]:
        """Resolve an exact inner URL from a domain + breadcrumb slug/title hint and optionally scrape it."""
        if not 1 <= limit <= 200:
            raise SafetyError("resolve limit must be between 1 and 200")
        base_url, root_domain, effective_hint = self._parse_domain_or_breadcrumb(domain_or_url, path_hint)
        if allow_homepage_shortcircuit and effective_hint is None:
            result: dict[str, Any] = {
                "success": True,
                "domain": root_domain,
                "base_url": base_url,
                "resolved_url": base_url,
                "resolution_method": "breadcrumb_root",
                "path_hint": None,
                "title": title,
                "candidates": [base_url],
            }
            if scrape:
                result["scraped"] = self.scrape(
                    base_url,
                    formats=formats or ["markdown"],
                    only_main_content=only_main_content,
                    max_age_ms=max_age_ms,
                    country=country,
                )
            return result

        search_term = effective_hint or title or keyword
        map_resp: dict[str, Any] | None = None
        map_error: str | None = None
        map_error_response: Any = None
        try:
            map_resp = self.map_site(base_url, limit=limit, search=search_term)
            candidates = self._extract_candidate_urls(map_resp, root_domain)
        except ApiError as exc:
            map_resp = None
            map_error = str(exc)
            map_error_response = exc.response
            candidates = []
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

        search_error: str | None = None
        search_error_response: Any = None
        if (not scored or (search_term and best_score < 15)) and (title or effective_hint or keyword):
            query_parts = [f"site:{root_domain}"]
            if title:
                query_parts.append(title)
            elif effective_hint:
                query_parts.append(effective_hint.replace("-", " "))
            elif keyword:
                query_parts.append(keyword)
            try:
                search_resp = self.search(
                    " ".join(query_parts),
                    limit=min(5, limit),
                    country=country,
                    scrape_results=False,
                )
                search_candidates = self._extract_candidate_urls(search_resp, root_domain)
            except ApiError as exc:
                search_candidates = []
                search_error = str(exc)
                search_error_response = exc.response
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

        if not scored and map_error and search_error:
            raise ApiError(
                f"Both /v2/map and /v2/search failed for {root_domain}: "
                f"map=({map_error}); search=({search_error})",
                response={"map": map_error_response, "search": search_error_response},
            )
        if require_candidate and not scored:
            detail_parts: list[str] = []
            if map_error:
                detail_parts.append(f"map failed: {map_error}")
            if search_error:
                detail_parts.append(f"search failed: {search_error}")
            elif title or effective_hint or keyword:
                detail_parts.append("search returned no matching candidates")
            detail = f" ({'; '.join(detail_parts)})" if detail_parts else ""
            raise SafetyError(
                f"Could not resolve an inner URL on {root_domain}"
                f"{f' for hint {effective_hint!r}' if effective_hint else ''}{detail}; "
                "refusing to substitute the site homepage."
            )
        if not scored and map_error and not (title or effective_hint or keyword):
            raise ApiError(map_error, response=map_error_response)

        resolved_url = scored[0] if scored else base_url
        result = {
            "success": True,
            "domain": root_domain,
            "base_url": base_url,
            "resolved_url": resolved_url,
            "resolution_method": method_used,
            "path_hint": effective_hint,
            "title": title,
            "candidates": scored[:10],
        }
        if map_error:
            result["map_error"] = map_error
        if search_error:
            result["search_error"] = search_error
        if scrape:
            result["scraped"] = self.scrape(
                resolved_url,
                formats=formats or ["markdown"],
                only_main_content=only_main_content,
                max_age_ms=max_age_ms,
                country=country,
            )
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

    @staticmethod
    def _canonical_url_from_paper_id(prefix: str, raw_id: str) -> str | None:
        scheme = (prefix or "").strip().lower()
        clean_id = (raw_id or "").strip()
        if clean_id.lower().startswith(f"{scheme}:"):
            clean_id = clean_id.split(":", 1)[1].strip()
        if (
            not clean_id
            or ".." in clean_id
            or "@" in clean_id
            or "://" in clean_id
            or any(ch.isspace() or ord(ch) < 32 for ch in clean_id)
        ):
            return None
        if scheme == "arxiv":
            return f"https://arxiv.org/abs/{clean_id}"
        if scheme in {"pubmed", "pmid"}:
            return f"https://pubmed.ncbi.nlm.nih.gov/{clean_id}/"
        if scheme == "biorxiv":
            return f"https://www.biorxiv.org/content/{clean_id}"
        if scheme == "medrxiv":
            return f"https://www.medrxiv.org/content/{clean_id}"
        if scheme == "doi":
            return f"https://doi.org/{clean_id}"
        return None

    @classmethod
    def _derive_result_item_url(cls, item: dict[str, Any]) -> str | None:
        direct = item.get("url") or item.get("readmeUrl") or item.get("pdfUrl")
        if isinstance(direct, str) and direct.strip().startswith(("http://", "https://")):
            return direct.strip()
        primary_id = item.get("primaryId")
        if isinstance(primary_id, str) and ":" in primary_id:
            prefix, raw_id = primary_id.split(":", 1)
            derived = cls._canonical_url_from_paper_id(prefix, raw_id)
            if derived:
                return derived
        ids = item.get("ids")
        if isinstance(ids, dict):
            lowered_ids = {str(k).strip().lower(): v for k, v in ids.items()}
            for key in ("arxiv", "pubmed", "pmid", "biorxiv", "medrxiv", "doi"):
                val = lowered_ids.get(key)
                raw_val: str | None = None
                if isinstance(val, str) and val.strip():
                    raw_val = val.strip()
                elif isinstance(val, (list, tuple)):
                    for elem in val:
                        if isinstance(elem, str) and elem.strip():
                            raw_val = elem.strip()
                            break
                if raw_val:
                    derived = cls._canonical_url_from_paper_id(key, raw_val)
                    if derived:
                        return derived
        return None

    def _scrape_result_urls(
        self,
        results: list[Any],
        *,
        limit: int,
        formats: list[str] | None,
        country: str,
    ) -> list[dict[str, Any]]:
        urls: list[str] = []
        for item in results:
            if not isinstance(item, dict):
                continue
            cand = self._derive_result_item_url(item)
            if not cand:
                continue
            try:
                validated = validate_public_url(cand, resolve_dns=False)
            except SafetyError:
                continue
            if validated not in urls:
                urls.append(validated)
            if len(urls) >= limit:
                break
        scraped: list[dict[str, Any]] = []
        for target in urls:
            try:
                scraped.append({
                    "url": target,
                    "response": self.scrape(target, formats=formats or ["markdown"], country=country),
                })
            except (ApiError, SafetyError) as exc:
                scraped.append({"url": target, "error": str(exc)})
        return scraped

    @staticmethod
    def developer_preview(
        query: str,
        *,
        limit: int = 10,
        scrape: bool = False,
        formats: list[str] | None = None,
    ) -> dict[str, Any]:
        needle = (query or "").strip()
        if not needle:
            raise SafetyError("developer search query is required")
        max_limit = 20 if scrape else 100
        if not 1 <= limit <= max_limit:
            raise SafetyError(f"developer search limit must be between 1 and {max_limit}")
        selected = formats or ["markdown"]
        if scrape:
            unknown = [item for item in selected if item not in SCRAPE_ALLOWED_FORMATS]
            if unknown:
                raise SafetyError(f"Unsupported default-safe scrape formats: {', '.join(unknown)}")
        params = urlencode([("query", needle), ("k", str(limit)), ("integration", "cli")])
        return {
            "operation": "developer",
            "dry_run": True,
            "requires_confirm": True,
            "method": "GET",
            "path": f"/v2/search/developer?{params}",
            "query": needle,
            "limit": limit,
            "scrape": scrape,
            "formats": selected if scrape else [],
            "estimated_credits": None,
            "note": "No HTTP request was made. Review scope and re-run developer with --confirm.",
        }

    def developer_search(
        self,
        query: str,
        *,
        limit: int = 10,
        scrape: bool = False,
        formats: list[str] | None = None,
        country: str = "US",
        confirm: bool = False,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        plan = self.developer_preview(query, limit=limit, scrape=scrape, formats=formats)
        if dry_run:
            return plan
        if not confirm:
            raise SafetyError("developer search requires --confirm (or pass --dry-run to preview)")
        response = self.request(
            plan["path"],
            method="GET",
            log_usage=True,
            requested_scope={"limit": limit, "scrape": scrape},
        )
        if scrape and isinstance(response.get("results"), list):
            response = {
                **response,
                "scraped_results": self._scrape_result_urls(
                    response["results"], limit=limit, formats=formats, country=country
                ),
            }
        return response

    @staticmethod
    def research_preview(
        query: str = "",
        *,
        limit: int = 10,
        scrape: bool = False,
        formats: list[str] | None = None,
        mode: str = "papers",
        authors: list[str] | None = None,
        categories: list[str] | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        paper_id: str | None = None,
        seed_ids: list[str] | None = None,
        intent: str | None = None,
        relation_mode: str | None = None,
        question: str | None = None,
        rerank: bool = False,
    ) -> dict[str, Any]:
        norm_mode = (mode or "papers").strip().lower()
        if norm_mode not in RESEARCH_MODES:
            raise SafetyError(f"research mode must be one of: {', '.join(sorted(RESEARCH_MODES))}")
        max_limit = 20 if scrape else 100
        if not 1 <= limit <= max_limit:
            raise SafetyError(f"research limit must be between 1 and {max_limit}")
        selected = formats or ["markdown"]
        if scrape:
            unknown = [item for item in selected if item not in SCRAPE_ALLOWED_FORMATS]
            if unknown:
                raise SafetyError(f"Unsupported default-safe scrape formats: {', '.join(unknown)}")
        pairs: list[tuple[str, str]] = []
        base = "/v2/search/research"
        if norm_mode == "papers":
            needle = (query or "").strip()
            if not needle:
                raise SafetyError("research query is required")
            pairs.append(("query", needle))
            pairs.append(("k", str(limit)))
            for author in authors or []:
                if author.strip():
                    pairs.append(("authors", author.strip()))
            for cat in categories or []:
                if cat.strip():
                    pairs.append(("categories", cat.strip()))
            if date_from:
                pairs.append(("from", date_from.strip()))
            if date_to:
                pairs.append(("to", date_to.strip()))
            endpoint = f"{base}/papers"
        elif norm_mode == "inspect":
            pid = _validate_paper_id(paper_id or query)
            endpoint = f"{base}/papers/{quote(pid, safe='')}"
        elif norm_mode == "read":
            pid = _validate_paper_id(paper_id or query)
            q = (question or "").strip()
            if not q:
                raise SafetyError("research read mode requires --question")
            pairs.append(("query", q))
            pairs.append(("k", str(limit)))
            endpoint = f"{base}/papers/{quote(pid, safe='')}"
        elif norm_mode == "related":
            seeds = [_validate_paper_id(s) for s in (seed_ids or ([paper_id] if paper_id else ([query] if query else [])))]
            if not seeds:
                raise SafetyError("research related mode requires at least one seed paper id")
            intent_clean = (intent or "").strip()
            if not intent_clean:
                raise SafetyError("research related mode requires --intent")
            pairs.append(("intent", intent_clean))
            if relation_mode:
                rm = relation_mode.strip().lower()
                if rm not in RESEARCH_RELATION_MODES:
                    raise SafetyError("relation mode must be similar, citers, or references")
                pairs.append(("mode", rm))
            pairs.append(("k", str(limit)))
            if rerank:
                pairs.append(("rerank", "true"))
            for anchor in seeds[1:]:
                pairs.append(("anchor", anchor))
            endpoint = f"{base}/papers/{quote(seeds[0], safe='')}/similar"
        else:  # github
            needle = (query or "").strip()
            if not needle:
                raise SafetyError("research github query is required")
            pairs.append(("query", needle))
            pairs.append(("k", str(limit)))
            endpoint = f"{base}/github"
        pairs.append(("integration", "cli"))
        full_path = f"{endpoint}?{urlencode(pairs)}"
        return {
            "operation": "research",
            "mode": norm_mode,
            "dry_run": True,
            "requires_confirm": True,
            "method": "GET",
            "path": full_path,
            "query": (query or "").strip(),
            "limit": limit,
            "scrape": scrape,
            "formats": selected if scrape else [],
            "estimated_credits": None,
            "note": "No HTTP request was made. Review scope and re-run research with --confirm.",
        }

    def research_search(
        self,
        query: str = "",
        *,
        limit: int = 10,
        scrape: bool = False,
        formats: list[str] | None = None,
        country: str = "US",
        mode: str = "papers",
        authors: list[str] | None = None,
        categories: list[str] | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        paper_id: str | None = None,
        seed_ids: list[str] | None = None,
        intent: str | None = None,
        relation_mode: str | None = None,
        question: str | None = None,
        rerank: bool = False,
        confirm: bool = False,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        plan = self.research_preview(
            query,
            limit=limit,
            scrape=scrape,
            formats=formats,
            mode=mode,
            authors=authors,
            categories=categories,
            date_from=date_from,
            date_to=date_to,
            paper_id=paper_id,
            seed_ids=seed_ids,
            intent=intent,
            relation_mode=relation_mode,
            question=question,
            rerank=rerank,
        )
        if dry_run:
            return plan
        if not confirm:
            raise SafetyError("research search requires --confirm (or pass --dry-run to preview)")
        response = self.request(
            plan["path"],
            method="GET",
            log_usage=True,
            requested_scope={"mode": plan["mode"], "limit": limit, "scrape": scrape},
        )
        if scrape and isinstance(response.get("results"), list):
            response = {
                **response,
                "scraped_results": self._scrape_result_urls(
                    response["results"], limit=limit, formats=formats, country=country
                ),
            }
        return response

    @staticmethod
    def parse_preview(
        file_path: str | Path,
        *,
        formats: list[str] | None = None,
        only_main_content: bool = True,
        query: str | None = None,
        include_tags: list[str] | None = None,
        exclude_tags: list[str] | None = None,
        timeout_ms: int | None = None,
    ) -> dict[str, Any]:
        target = _safe_local_path(file_path)
        if not target.exists() or not target.is_file():
            raise SafetyError(f"Parse target does not exist or is not a regular file: {target.name}")
        ext = target.suffix.lower()
        if ext not in PARSE_SUPPORTED_EXTENSIONS:
            raise SafetyError(
                f"Unsupported file type '{ext or '(none)'}'. Supported: {', '.join(sorted(PARSE_SUPPORTED_EXTENSIONS))}"
            )
        size = target.stat().st_size
        if size > MAX_PARSE_BYTES:
            raise SafetyError(f"File exceeds maximum /v2/parse upload size ({MAX_PARSE_BYTES} bytes)")
        selected = list(formats) if formats else ["markdown"]
        unknown = [item for item in selected if item not in PARSE_ALLOWED_FORMATS]
        if unknown:
            raise SafetyError(f"Unsupported parse formats: {', '.join(unknown)}")
        if timeout_ms is not None and not 1000 <= timeout_ms <= 300_000:
            raise SafetyError("parse timeout_ms must be between 1000 and 300000")
        api_formats: list[Any] = list(selected)
        if query and query.strip():
            api_formats.append({"type": "query", "prompt": query.strip()})
        options_payload: dict[str, Any] = {
            "formats": api_formats,
            "integration": "cli",
            "onlyMainContent": only_main_content,
        }
        if include_tags:
            options_payload["includeTags"] = include_tags
        if exclude_tags:
            options_payload["excludeTags"] = exclude_tags
        if timeout_ms is not None:
            options_payload["timeout"] = timeout_ms
        return {
            "operation": "parse",
            "dry_run": True,
            "requires_confirm": True,
            "method": "POST",
            "path": "/v2/parse",
            "file": str(target),
            "filename": target.name,
            "content_type": PARSE_CONTENT_TYPES[ext],
            "bytes": size,
            "options": options_payload,
            "estimated_credits": 1,
            "note": "No HTTP request was made. Review file scope and re-run parse with --confirm.",
        }

    def parse_file(
        self,
        file_path: str | Path,
        *,
        formats: list[str] | None = None,
        only_main_content: bool = True,
        query: str | None = None,
        include_tags: list[str] | None = None,
        exclude_tags: list[str] | None = None,
        timeout_ms: int | None = None,
        confirm: bool = False,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        plan = self.parse_preview(
            file_path,
            formats=formats,
            only_main_content=only_main_content,
            query=query,
            include_tags=include_tags,
            exclude_tags=exclude_tags,
            timeout_ms=timeout_ms,
        )
        if dry_run:
            return plan
        if not confirm:
            raise SafetyError("parse uploads a local file and requires --confirm (or pass --dry-run to preview)")
        target = Path(plan["file"])
        file_bytes = target.read_bytes()
        body, content_type = _encode_multipart(
            "file",
            plan["filename"],
            plan["content_type"],
            file_bytes,
            {"options": json.dumps(plan["options"], separators=(",", ":"))},
        )
        return self.request(
            "/v2/parse",
            method="POST",
            raw_body=body,
            content_type=content_type,
            log_usage=True,
            requested_scope={"pages": 1, "bytes": plan["bytes"], "formats": plan["options"]["formats"]},
        )

    @staticmethod
    def agent_preview(
        prompt: str,
        *,
        urls: list[str] | None = None,
        model: str = "spark-1-mini",
        max_credits: int = 25,
        schema: dict[str, Any] | None = None,
        schema_file: str | Path | None = None,
        strict_constrain_to_urls: bool = False,
    ) -> dict[str, Any]:
        needle = (prompt or "").strip()
        if not needle:
            raise SafetyError("agent prompt is required")
        if model not in AGENT_MODELS:
            raise SafetyError(f"agent model must be one of: {', '.join(sorted(AGENT_MODELS))}")
        if type(max_credits) is not int or not 1 <= max_credits <= MAX_AGENT_CREDITS:
            raise SafetyError(f"agent max_credits must be an integer between 1 and {MAX_AGENT_CREDITS}")
        validated_urls: list[str] = []
        for u in urls or []:
            validated_urls.append(validate_public_url(u))
        resolved_schema = schema
        if schema_file is not None:
            sp = _safe_local_path(schema_file)
            if not sp.is_file():
                raise SafetyError(f"Schema file not found: {sp.name}")
            try:
                loaded = json.loads(sp.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                raise SafetyError(f"Invalid JSON in schema file: {exc}") from None
            if not isinstance(loaded, dict):
                raise SafetyError("Agent schema must be a JSON object")
            resolved_schema = loaded
        elif resolved_schema is not None and not isinstance(resolved_schema, dict):
            raise SafetyError("Agent schema must be a JSON object")
        payload: dict[str, Any] = {
            "prompt": needle,
            "integration": "cli",
            "model": model,
            "maxCredits": max_credits,
        }
        if validated_urls:
            payload["urls"] = validated_urls
        if resolved_schema is not None:
            payload["schema"] = resolved_schema
        if strict_constrain_to_urls:
            payload["strictConstrainToURLs"] = True
        return {
            "operation": "agent",
            "dry_run": True,
            "requires_confirm": True,
            "method": "POST",
            "path": "/v2/agent",
            "payload": payload,
            "max_credits_cap": max_credits,
            "estimated_credits": None,
            "note": "No HTTP request was made. Review maxCredits cap and re-run agent with --confirm.",
        }

    def agent_start(
        self,
        prompt: str,
        *,
        urls: list[str] | None = None,
        model: str = "spark-1-mini",
        max_credits: int = 25,
        schema: dict[str, Any] | None = None,
        schema_file: str | Path | None = None,
        strict_constrain_to_urls: bool = False,
        confirm: bool = False,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        plan = self.agent_preview(
            prompt,
            urls=urls,
            model=model,
            max_credits=max_credits,
            schema=schema,
            schema_file=schema_file,
            strict_constrain_to_urls=strict_constrain_to_urls,
        )
        if dry_run:
            return plan
        if not confirm:
            raise SafetyError("agent runs autonomous multi-page extraction and requires --confirm (or --dry-run)")
        return self.request(
            "/v2/agent",
            method="POST",
            payload=plan["payload"],
            log_usage=True,
            requested_scope={"max_credits": max_credits, "model": model, "url_count": len(urls or [])},
        )

    def agent_status(self, job_id: str) -> dict[str, Any]:
        value = job_id.strip()
        if not JOB_ID_PATTERN.fullmatch(value):
            raise SafetyError("agent job id format is invalid")
        return self.request(f"/v2/agent/{value}")

    def agent_cancel(self, job_id: str, *, confirm: bool = False, dry_run: bool = False) -> dict[str, Any]:
        value = job_id.strip()
        if not JOB_ID_PATTERN.fullmatch(value):
            raise SafetyError("agent job id format is invalid")
        if dry_run:
            return {
                "operation": "agent-cancel",
                "dry_run": True,
                "requires_confirm": True,
                "method": "DELETE",
                "path": f"/v2/agent/{value}",
                "job_id": value,
                "estimated_credits": 0,
            }
        if not confirm:
            raise SafetyError("cancelling an agent job requires --confirm (or pass --dry-run to preview)")
        return self.request(f"/v2/agent/{value}", method="DELETE")

    @staticmethod
    def interact_preview(
        scrape_id: str,
        *,
        prompt: str | None = None,
        code: str | None = None,
        language: str = "node",
        timeout: int | None = None,
        stop: bool = False,
    ) -> dict[str, Any]:
        sid = _validate_resource_id(scrape_id, "scrape id")
        path = f"/v2/scrape/{sid}/interact"
        if stop:
            return {
                "operation": "interact",
                "action": "stop",
                "dry_run": True,
                "requires_confirm": True,
                "method": "DELETE",
                "path": path,
                "scrape_id": sid,
                "estimated_credits": 0,
                "note": "No HTTP request was made. Re-run interact --stop with --confirm to terminate the session.",
            }
        if bool(prompt) == bool(code):
            raise SafetyError("interact requires exactly one of --prompt or --code (or --stop)")
        payload: dict[str, Any] = {"origin": "cli", "integration": "cli"}
        if code:
            lang = (language or "node").strip().lower()
            if lang not in INTERACT_LANGUAGES:
                raise SafetyError(f"interact language must be one of: {', '.join(sorted(INTERACT_LANGUAGES))}")
            payload["code"] = code
            payload["language"] = lang
        else:
            payload["prompt"] = (prompt or "").strip()
        if timeout is not None:
            if not 1 <= timeout <= 300:
                raise SafetyError("interact timeout must be between 1 and 300 seconds")
            payload["timeout"] = timeout
        return {
            "operation": "interact",
            "action": "execute",
            "dry_run": True,
            "requires_confirm": True,
            "method": "POST",
            "path": path,
            "scrape_id": sid,
            "payload": payload,
            "estimated_credits": None,
            "note": "No HTTP request was made. Re-run interact with --confirm to execute in the browser session.",
        }

    def interact(
        self,
        scrape_id: str,
        *,
        prompt: str | None = None,
        code: str | None = None,
        language: str = "node",
        timeout: int | None = None,
        stop: bool = False,
        confirm: bool = False,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        plan = self.interact_preview(
            scrape_id, prompt=prompt, code=code, language=language, timeout=timeout, stop=stop
        )
        if dry_run:
            return plan
        if not confirm:
            raise SafetyError("interact operates a live cloud browser session and requires --confirm (or --dry-run)")
        if stop:
            return self.request(plan["path"], method="DELETE", log_usage=True, requested_scope={"action": "stop"})
        return self.request(
            plan["path"],
            method="POST",
            payload=plan["payload"],
            log_usage=True,
            requested_scope={"action": "execute", "mode": "code" if code else "prompt"},
        )

    @staticmethod
    def monitor_preview(
        action: str,
        *,
        monitor_id: str | None = None,
        check_id: str | None = None,
        name: str | None = None,
        cron: str | None = None,
        schedule_text: str | None = None,
        timezone_name: str | None = None,
        page: str | None = None,
        scrape_urls: list[str] | None = None,
        crawl_url: str | None = None,
        queries: list[str] | None = None,
        search_window: str | None = None,
        max_results: int | None = None,
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        webhook_url: str | None = None,
        webhook_events: list[str] | None = None,
        email_recipients: list[str] | None = None,
        retention_days: int | None = None,
        goal: str | None = None,
        state: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        skip: int | None = None,
        page_status: str | None = None,
    ) -> dict[str, Any]:
        act = (action or "").strip().lower()
        if act not in MONITOR_ACTIONS:
            raise SafetyError(f"monitor action must be one of: {', '.join(sorted(MONITOR_ACTIONS))}")
        method = "GET"
        path = "/v2/monitor"
        payload: dict[str, Any] | None = None
        if act == "create":
            if not (name and name.strip()):
                raise SafetyError("monitor create requires --name")
            if not (cron or schedule_text):
                raise SafetyError("monitor create requires --cron or --schedule")
            urls = list(scrape_urls or ([page] if page else []))
            has_scrape = bool(urls)
            has_crawl = bool(crawl_url)
            has_search = bool(queries)
            if not (has_scrape or has_crawl or has_search):
                raise SafetyError("monitor create requires --page, --scrape-urls, --crawl-url, or --queries")
            if has_search and not (goal and goal.strip()):
                raise SafetyError("monitor create with --queries requires --goal")
            schedule: dict[str, Any] = {}
            if cron:
                schedule["cron"] = cron.strip()
            if schedule_text:
                schedule["text"] = schedule_text.strip()
            if timezone_name:
                schedule["timezone"] = timezone_name.strip()
            targets: list[dict[str, Any]] = []
            if has_scrape:
                targets.append({"type": "scrape", "urls": [validate_public_url(u) for u in urls]})
            if has_crawl:
                targets.append({"type": "crawl", "url": validate_public_url(crawl_url or "")})
            if has_search:
                st: dict[str, Any] = {"type": "search", "queries": [q.strip() for q in (queries or []) if q.strip()]}
                if search_window:
                    if search_window not in MONITOR_SEARCH_WINDOWS:
                        raise SafetyError(f"search_window must be one of: {', '.join(sorted(MONITOR_SEARCH_WINDOWS))}")
                    st["searchWindow"] = search_window
                if max_results is not None:
                    if not 1 <= max_results <= 50:
                        raise SafetyError("monitor max_results must be between 1 and 50")
                    st["maxResults"] = max_results
                if include_domains:
                    st["includeDomains"] = include_domains
                if exclude_domains:
                    st["excludeDomains"] = exclude_domains
                targets.append(st)
            body: dict[str, Any] = {"name": name.strip(), "schedule": schedule, "targets": targets}
            if webhook_url:
                wh: dict[str, Any] = {"url": validate_public_url(webhook_url)}
                if webhook_events:
                    wh["events"] = webhook_events
                body["webhook"] = wh
            if email_recipients:
                body["notification"] = {"email": {"enabled": True, "recipients": email_recipients}}
            if retention_days is not None:
                if not 1 <= retention_days <= 365:
                    raise SafetyError("retention_days must be between 1 and 365")
                body["retentionDays"] = retention_days
            if goal is not None and goal.strip():
                body["goal"] = goal.strip()
            method = "POST"
            payload = body
        elif act == "list":
            qs: list[tuple[str, str]] = []
            if limit is not None:
                if not 1 <= limit <= 100:
                    raise SafetyError("monitor list limit must be between 1 and 100")
                qs.append(("limit", str(limit)))
            if offset is not None:
                if offset < 0:
                    raise SafetyError("monitor offset must be non-negative")
                qs.append(("offset", str(offset)))
            path = f"/v2/monitor?{urlencode(qs)}" if qs else "/v2/monitor"
        elif act == "get":
            mid = _validate_resource_id(monitor_id or "", "monitor id")
            path = f"/v2/monitor/{mid}"
        elif act == "update":
            mid = _validate_resource_id(monitor_id or "", "monitor id")
            body = {}
            if name:
                body["name"] = name.strip()
            if goal:
                body["goal"] = goal.strip()
            if state:
                if state not in {"active", "paused"}:
                    raise SafetyError("monitor state must be active or paused")
                body["status"] = state
            if retention_days is not None:
                if not 1 <= retention_days <= 365:
                    raise SafetyError("retention_days must be between 1 and 365")
                body["retentionDays"] = retention_days
            if cron or schedule_text or timezone_name:
                sched: dict[str, Any] = {}
                if cron:
                    sched["cron"] = cron.strip()
                if schedule_text:
                    sched["text"] = schedule_text.strip()
                if timezone_name:
                    sched["timezone"] = timezone_name.strip()
                body["schedule"] = sched
            if not body:
                raise SafetyError("monitor update requires at least one field to update")
            method = "PATCH"
            path = f"/v2/monitor/{mid}"
            payload = body
        elif act == "delete":
            mid = _validate_resource_id(monitor_id or "", "monitor id")
            method = "DELETE"
            path = f"/v2/monitor/{mid}"
        elif act == "run":
            mid = _validate_resource_id(monitor_id or "", "monitor id")
            method = "POST"
            path = f"/v2/monitor/{mid}/run"
        elif act == "checks":
            mid = _validate_resource_id(monitor_id or "", "monitor id")
            qs = []
            if limit is not None:
                if not 1 <= limit <= 100:
                    raise SafetyError("monitor checks limit must be between 1 and 100")
                qs.append(("limit", str(limit)))
            if offset is not None:
                if offset < 0:
                    raise SafetyError("monitor offset must be non-negative")
                qs.append(("offset", str(offset)))
            path = f"/v2/monitor/{mid}/checks" + (f"?{urlencode(qs)}" if qs else "")
        elif act == "check":
            mid = _validate_resource_id(monitor_id or "", "monitor id")
            cid = _validate_resource_id(check_id or "", "check id")
            qs = []
            if limit is not None:
                if not 1 <= limit <= 100:
                    raise SafetyError("monitor check limit must be between 1 and 100")
                qs.append(("limit", str(limit)))
            if skip is not None:
                if skip < 0:
                    raise SafetyError("monitor skip must be non-negative")
                qs.append(("skip", str(skip)))
            if page_status:
                if page_status not in MONITOR_PAGE_STATUSES:
                    raise SafetyError(f"page_status must be one of: {', '.join(sorted(MONITOR_PAGE_STATUSES))}")
                qs.append(("status", page_status))
            path = f"/v2/monitor/{mid}/checks/{cid}" + (f"?{urlencode(qs)}" if qs else "")
        requires_confirm = act in MONITOR_MUTATING_ACTIONS
        return {
            "operation": "monitor",
            "action": act,
            "dry_run": True,
            "requires_confirm": requires_confirm,
            "method": method,
            "path": path,
            "payload": payload,
            "estimated_credits": None if act in {"create", "run"} else 0,
            "note": (
                "No HTTP request was made. Review monitor scope and re-run with --confirm."
                if requires_confirm
                else "No HTTP request was made. This monitor action is read-only."
            ),
        }

    def monitor(
        self,
        action: str,
        *,
        confirm: bool = False,
        dry_run: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        plan = self.monitor_preview(action, **kwargs)
        if dry_run:
            return plan
        if plan["requires_confirm"] and not confirm:
            raise SafetyError(f"monitor {plan['action']} is mutating/recurring and requires --confirm (or --dry-run)")
        return self.request(
            plan["path"],
            method=plan["method"],
            payload=plan["payload"],
            extra_headers={"X-Origin": "cli"},
            log_usage=plan["action"] in {"create", "run"},
            requested_scope={"action": plan["action"]},
        )

    @staticmethod
    def search_feedback_preview(
        search_id: str,
        *,
        rating: str,
        valuable_sources: list[dict[str, str]] | None = None,
        missing_content: list[dict[str, str]] | None = None,
        query_suggestions: str | None = None,
    ) -> dict[str, Any]:
        sid = _validate_resource_id(search_id, "search id")
        norm_rating = (rating or "").strip().lower()
        if norm_rating not in SEARCH_FEEDBACK_RATINGS:
            raise SafetyError("rating must be one of: good, bad, partial")
        body: dict[str, Any] = {
            "rating": norm_rating,
            "origin": "cli",
            "integration": "cli",
        }
        if valuable_sources:
            cleaned_sources: list[dict[str, str]] = []
            for entry in valuable_sources:
                url = validate_public_url(str(entry.get("url", "")), resolve_dns=False)
                item: dict[str, str] = {"url": url}
                if entry.get("reason"):
                    item["reason"] = str(entry["reason"]).strip()
                cleaned_sources.append(item)
            if cleaned_sources:
                body["valuableSources"] = cleaned_sources
        if missing_content:
            cleaned_missing: list[dict[str, str]] = []
            for entry in missing_content[:20]:
                topic = str(entry.get("topic", "")).strip()
                if not topic:
                    continue
                item = {"topic": topic}
                if entry.get("description"):
                    item["description"] = str(entry["description"]).strip()
                cleaned_missing.append(item)
            if cleaned_missing:
                body["missingContent"] = cleaned_missing
        if query_suggestions and query_suggestions.strip():
            body["querySuggestions"] = query_suggestions.strip()
        return {
            "operation": "search-feedback",
            "dry_run": True,
            "requires_confirm": False,
            "method": "POST",
            "path": f"/v2/search/{sid}/feedback",
            "search_id": sid,
            "payload": body,
            "estimated_credits": 0,
            "refund_credits_on_first_submit": 1,
            "note": "No HTTP request was made. Search feedback is free and refunds 1 credit on first submission.",
        }

    def search_feedback(
        self,
        search_id: str,
        *,
        rating: str,
        valuable_sources: list[dict[str, str]] | None = None,
        missing_content: list[dict[str, str]] | None = None,
        query_suggestions: str | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        plan = self.search_feedback_preview(
            search_id,
            rating=rating,
            valuable_sources=valuable_sources,
            missing_content=missing_content,
            query_suggestions=query_suggestions,
        )
        if dry_run:
            return plan
        if is_search_feedback_disabled_locally():
            return {
                "success": True,
                "disabled": True,
                "disabledSource": "env",
                "creditsRefunded": 0,
                "warning": "Search feedback disabled by FIRECRAWL_NO_SEARCH_FEEDBACK; no data was sent.",
            }
        return self.request(
            plan["path"],
            method="POST",
            payload=plan["payload"],
            log_usage=False,
            requested_scope={"search_id": plan["search_id"], "rating": plan["payload"]["rating"]},
        )


def usage_summary(path: Path | None = None) -> dict[str, Any]:
    target = _safe_local_path(path or ledger_path())
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

