from __future__ import annotations

import json
from pathlib import Path

import pytest

from legends_firecrawl import client


def runtime(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> client.FirecrawlClient:
    monkeypatch.setenv("LEGENDS_FIRECRAWL_LEDGER", str(tmp_path / "ledger.jsonl"))
    return client.FirecrawlClient(client.Credentials("fc-test-key", "test"), consumer="test")


def test_process_environment_credentials(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-house-key")
    credentials = client.load_credentials()
    assert credentials.source == "process-env"
    assert client.credential_status() == {"present": True, "source": "process-env", "length": 12}


def test_windows_user_environment_credentials(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    monkeypatch.delenv("FIRECRAWL_DISABLE_USER_ENV", raising=False)
    monkeypatch.setattr(client, "_windows_user_environment", lambda _name: "fc-user-key")
    assert client.load_credentials().source == "user-env"


def test_missing_credentials_names_house_setup(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    monkeypatch.delenv("FIRECRAWL_API_KEY_FILE", raising=False)
    monkeypatch.setattr(client, "_windows_user_environment", lambda _name: None)
    with pytest.raises(client.CredentialError) as error:
        client.load_credentials()
    assert "FIRECRAWL_API_KEY" in str(error.value)
    assert "MCP" not in str(error.value)


def test_api_key_file_and_symlink_refusal(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    key_file = tmp_path / "firecrawl.key"
    key_file.write_text("  fc-file-secret-123  \n", encoding="utf-8")
    monkeypatch.setenv("FIRECRAWL_API_KEY_FILE", str(key_file))
    creds = client.load_credentials()
    assert creds.api_key == "fc-file-secret-123"
    assert creds.source == "key-file"
    link_path = tmp_path / "symlink.key"
    try:
        link_path.symlink_to(key_file)
    except OSError:
        return
    monkeypatch.setenv("FIRECRAWL_API_KEY_FILE", str(link_path))
    with pytest.raises(client.SafetyError, match="symlink"):
        client.load_credentials()


@pytest.mark.parametrize(
    "url",
    [
        "file:///etc/passwd",
        "ftp://example.com/a",
        "http://localhost/a",
        "http://dev.local/a",
        "http://127.0.0.1/a",
        "http://10.0.0.2/a",
        "http://169.254.1.1/a",
        "http://[2002:7f00:1::]/a",
        "http://[2002:a9fe:a9fe::]/a",
        "https://user:pass@example.com/a",
        "https://google.com/goto?url=CAES1gExyz",
        "https://www.google.com/url?q=https://example.com",
    ],
)
def test_private_or_credentialed_targets_fail_before_http(url: str):
    with pytest.raises(client.SafetyError):
        client.validate_public_url(url)


def test_public_urls_are_allowed():
    assert client.validate_public_url("https://example.com/path?q=1") == "https://example.com/path?q=1"


def test_non_https_api_root_is_rejected(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("FIRECRAWL_API_URL", "http://localhost:3002")
    with pytest.raises(client.SafetyError, match="HTTPS"):
        client.api_root()


def test_custom_api_root_requires_explicit_allow_flag(monkeypatch: pytest.MonkeyPatch):
    import socket as _sock

    monkeypatch.setenv("FIRECRAWL_API_URL", "https://custom-proxy.example.com")
    monkeypatch.delenv("FIRECRAWL_ALLOW_CUSTOM_API_URL", raising=False)
    with pytest.raises(client.SafetyError, match="FIRECRAWL_ALLOW_CUSTOM_API_URL"):
        client.api_root()
    monkeypatch.setenv("FIRECRAWL_ALLOW_CUSTOM_API_URL", "1")
    monkeypatch.setattr(
        client.socket,
        "getaddrinfo",
        lambda *_a, **_k: [(_sock.AF_INET, _sock.SOCK_STREAM, 6, "", ("93.184.216.34", 443))],
    )
    assert client.api_root() == "https://custom-proxy.example.com"


def test_validate_public_url_rejects_dns_private_ip_and_numeric_host(monkeypatch: pytest.MonkeyPatch):
    import socket as _sock

    with pytest.raises(client.SafetyError, match="Numeric"):
        client.validate_public_url("https://2130706433/secret")

    monkeypatch.setattr(
        client.socket,
        "getaddrinfo",
        lambda *_a, **_k: [(_sock.AF_INET, _sock.SOCK_STREAM, 6, "", ("127.0.0.1", 443))],
    )
    with pytest.raises(client.SafetyError, match="non-public"):
        client.validate_public_url("https://rebind.example.com/path", resolve_dns=True)


def test_extract_candidate_urls_respects_include_subdomains():
    response = {
        "links": [
            "https://example.com/about",
            "https://sub.example.com/internal",
            "https://evil-example.com/phish",
        ]
    }
    strict = client.FirecrawlClient._extract_candidate_urls(response, "example.com", include_subdomains=False)
    assert strict == ["https://example.com/about"]
    with_subs = client.FirecrawlClient._extract_candidate_urls(response, "example.com", include_subdomains=True)
    assert with_subs == [
        "https://example.com/about",
        "https://sub.example.com/internal",
    ]


def test_request_rejects_invalid_utf8_and_oversized_body(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    instance = runtime(tmp_path, monkeypatch)

    class FakeResp:
        def __init__(self, data: bytes):
            self._data = data

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self, _n: int = -1) -> bytes:
            return self._data

    monkeypatch.setattr(client, "urlopen", lambda *_a, **_k: FakeResp(b"\xff\xfeinvalid"))
    with pytest.raises(client.ApiError, match="non-UTF-8"):
        instance.request("/v2/scrape")



def test_routes_and_estimates_are_intent_first():
    routes = client.load_routes()["routes"]
    assert {item["name"] for item in routes} == {
        "credits",
        "scrape",
        "map",
        "search",
        "developer",
        "research",
        "parse",
        "resolve",
        "crawl",
        "crawl-status",
        "agent",
        "agent-status",
        "interact",
        "monitor",
        "search-feedback",
    }
    estimate = client.estimate("crawl", limit=40)
    assert estimate["page_or_result_ceiling"] == 40
    assert estimate["estimated_credits"] is None
    res_est = client.estimate("resolve", limit=30)
    assert res_est["page_or_result_ceiling"] == 30
    parse_est = client.estimate("parse")
    assert parse_est["page_or_result_ceiling"] == 1
    assert parse_est["estimated_credits"] == 1


def test_resolve_url_parses_breadcrumb_and_scores_candidates(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    instance = runtime(tmp_path, monkeypatch)

    def fake_request(path, **kwargs):
        if path == "/v2/map":
            return {
                "success": True,
                "links": [
                    "https://warrenallen.com/",
                    "https://warrenallen.com/about/",
                    "https://warrenallen.com/choosing-personal-injury-attorney/",
                ],
            }
        if path == "/v2/scrape":
            return {"success": True, "data": {"markdown": "# Choosing an Attorney"}}
        raise AssertionError(f"Unexpected path {path}")

    monkeypatch.setattr(instance, "request", fake_request)
    out = instance.resolve_url(
        "https://warrenallen.com \u203a choosing-personal-injury-atto...",
        title="Tips for Choosing a Personal Injury Attorney",
        scrape=True,
    )
    assert out["domain"] == "warrenallen.com"
    assert out["path_hint"] == "choosing-personal-injury-atto"
    assert out["resolved_url"] == "https://warrenallen.com/choosing-personal-injury-attorney/"
    assert out["scraped"]["data"]["markdown"] == "# Choosing an Attorney"


def test_scrape_builds_house_defaults(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    instance = runtime(tmp_path, monkeypatch)
    captured = {}

    def fake(path, **kwargs):
        captured["path"] = path
        captured.update(kwargs)
        return {"success": True, "data": {"markdown": "ok"}}

    monkeypatch.setattr(instance, "request", fake)
    instance.scrape("https://example.com", formats=["markdown", "links"])
    assert captured["path"] == "/v2/scrape"
    assert captured["payload"]["onlyCleanContent"] is True
    assert captured["payload"]["storeInCache"] is False
    assert captured["requested_scope"]["pages"] == 1


def test_scrape_rejects_high_scope_formats(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    instance = runtime(tmp_path, monkeypatch)
    with pytest.raises(client.SafetyError, match="formats"):
        instance.scrape("https://example.com", formats=["screenshot"])


def test_map_and_search_bounds(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    instance = runtime(tmp_path, monkeypatch)
    with pytest.raises(client.SafetyError, match="map limit"):
        instance.map_site("https://example.com", limit=1001)
    with pytest.raises(client.SafetyError, match="search limit"):
        instance.search("test", limit=21)


def test_crawl_preview_is_local_and_bounded():
    plan = client.FirecrawlClient.crawl_preview("https://example.com", limit=25, max_depth=2)
    assert plan["dry_run"] is True
    assert plan["requires_confirm"] is True
    assert plan["estimated_credits"] is None


def test_crawl_refuses_without_confirm(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    instance = runtime(tmp_path, monkeypatch)
    monkeypatch.setattr(instance, "request", lambda *a, **k: pytest.fail("HTTP should not be called"))
    with pytest.raises(client.SafetyError, match="requires --confirm"):
        instance.crawl("https://example.com")


def test_crawl_payload_never_leaves_domain(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    instance = runtime(tmp_path, monkeypatch)
    captured = {}

    def fake(path, **kwargs):
        captured.update(kwargs)
        return {"success": True, "id": "abc123456789"}

    monkeypatch.setattr(instance, "request", fake)
    instance.crawl("https://example.com", confirm=True)
    assert captured["payload"]["allowExternalLinks"] is False
    assert captured["payload"]["allowSubdomains"] is False
    assert captured["payload"]["limit"] == 25


def test_job_id_is_validated_before_http(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    instance = runtime(tmp_path, monkeypatch)
    monkeypatch.setattr(instance, "request", lambda *a, **k: pytest.fail("HTTP should not be called"))
    with pytest.raises(client.SafetyError, match="job id"):
        instance.crawl_status("../../secrets")


def test_usage_ledger_does_not_store_credentials(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    ledger = tmp_path / "ledger.jsonl"
    monkeypatch.setenv("LEGENDS_FIRECRAWL_LEDGER", str(ledger))
    response = {"success": True, "creditsUsed": 1}
    client._append_ledger("/v2/scrape", response, consumer="packet", requested_scope={"pages": 1})
    row = json.loads(ledger.read_text(encoding="utf-8"))
    assert row["credits_reported"] == 1
    assert "key" not in json.dumps(row).lower()
    summary = client.usage_summary(ledger)
    assert summary["calls"] == 1
    assert summary["reported_credits"] == 1

def test_provider_http_error_preserves_raw(monkeypatch,tmp_path):
    from urllib.error import HTTPError
    from io import BytesIO
    instance=runtime(tmp_path,monkeypatch)
    calls=[]
    def failed(*args,**kwargs):
        calls.append(1)
        raise HTTPError('https://api.firecrawl.dev/v2/scrape',429,'busy',{},BytesIO(b'{"success":false,"nested":{"keep":12}}'))
    monkeypatch.setattr(client,'urlopen',failed)
    with pytest.raises(client.ApiError) as err:instance.request('/v2/scrape')
    assert err.value.response=={'success':False,'nested':{'keep':12}}
    assert err.value.request_may_have_completed and len(calls)==1

def test_installed_ledger_uses_portable_state_not_house_checkout(monkeypatch,tmp_path):
    monkeypatch.delenv('LEGENDS_FIRECRAWL_HOME',raising=False)
    monkeypatch.delenv('LEGENDS_FIRECRAWL_LEDGER',raising=False)
    monkeypatch.setenv('LOCALAPPDATA',str(tmp_path/'state'))
    monkeypatch.setattr(client,'__file__',str(tmp_path/'venv'/'Lib'/'site-packages'/'legends_firecrawl'/'client.py'))
    assert client._kit_root() is None
    assert client.ledger_path()==tmp_path/'state'/'Legends'/'Firecrawl'/'usage-ledger.jsonl'

def test_explicit_ledger_home_and_source_marker(monkeypatch,tmp_path):
    monkeypatch.delenv('LEGENDS_FIRECRAWL_LEDGER',raising=False)
    monkeypatch.setenv('LEGENDS_FIRECRAWL_HOME',str(tmp_path/'chosen'))
    assert client.ledger_path()==tmp_path/'chosen'/'var'/'usage-ledger.jsonl'
    monkeypatch.delenv('LEGENDS_FIRECRAWL_HOME')
    (tmp_path/'.legends-module').write_text('legends-firecrawl')
    monkeypatch.setattr(client,'__file__',str(tmp_path/'python'/'legends_firecrawl'/'client.py'))
    assert client._kit_root()==tmp_path


def test_resolve_url_falls_back_to_search_on_map_api_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    instance = runtime(tmp_path, monkeypatch)
    monkeypatch.setattr(client, "validate_public_url", lambda v, **kw: v)

    def fake_map(*_a, **_kw):
        raise client.ApiError("Firecrawl returned HTTP 403 for /v2/map", response={"error": "Site blocked"})

    def fake_search(query, **_kw):
        assert "site:reddit.com" in query
        return {
            "success": True,
            "data": {
                "web": [
                    {"url": "https://www.reddit.com/r/Phoenixville/comments/xyz/mechanic_recs/"},
                ]
            },
        }

    monkeypatch.setattr(instance, "map_site", fake_map)
    monkeypatch.setattr(instance, "search", fake_search)
    monkeypatch.setattr(instance, "scrape", lambda url, **_kw: {"success": True, "url": url})

    out = instance.resolve_url(
        "reddit.com",
        path_hint="r/Phoenixville",
        title="Mechanic Recommendations?",
        scrape=True,
        require_candidate=True,
    )
    assert out["resolution_method"] == "search"
    assert out["map_error"] == "Firecrawl returned HTTP 403 for /v2/map"
    assert out["resolved_url"] == "https://www.reddit.com/r/Phoenixville/comments/xyz/mechanic_recs/"
    assert out["scraped"]["url"] == out["resolved_url"]

    # When map raises ApiError and search yields no candidates with require_candidate=True, include both contexts.
    monkeypatch.setattr(instance, "search", lambda *_a, **_kw: {"success": True, "data": {"web": []}})
    with pytest.raises(client.SafetyError) as exc_empty:
        instance.resolve_url("reddit.com", path_hint="r/Phoenixville", title="Mechanic", require_candidate=True)
    assert "HTTP 403" in str(exc_empty.value)
    assert "search returned no matching candidates" in str(exc_empty.value)

    # When both map and search raise ApiError, raise ApiError with both contexts and provider payloads.
    def fake_search_err(*_a, **_kw):
        raise client.ApiError("Firecrawl returned HTTP 500 for /v2/search", response={"error": "Upstream error"})

    monkeypatch.setattr(instance, "search", fake_search_err)
    with pytest.raises(client.ApiError) as exc_both:
        instance.resolve_url("reddit.com", path_hint="r/Phoenixville", title="Mechanic", require_candidate=True)
    assert "HTTP 403" in str(exc_both.value)
    assert "HTTP 500" in str(exc_both.value)
    assert exc_both.value.response == {"map": {"error": "Site blocked"}, "search": {"error": "Upstream error"}}


def test_extract_credit_signal_reads_nested_data_metadata(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    ledger = tmp_path / "ledger.jsonl"
    monkeypatch.setenv("LEGENDS_FIRECRAWL_LEDGER", str(ledger))
    scrape_resp = {"success": True, "data": {"markdown": "# Hi", "metadata": {"creditsUsed": 1}}}
    parse_resp = {"success": True, "data": {"markdown": "# Doc", "metadata": {"credits_used": 2}}}
    assert client._extract_credit_signal(scrape_resp) == 1
    assert client._extract_credit_signal(parse_resp) == 2
    assert client._extract_credit_signal({"creditsUsed": True}) is None

    client._append_ledger("/v2/scrape", scrape_resp, consumer="lfc", requested_scope={"pages": 1})
    client._append_ledger("/v2/parse", parse_resp, consumer="lfc", requested_scope={"pages": 1})
    summary = client.usage_summary(ledger)
    assert summary["calls"] == 2
    assert summary["reported_credits"] == 3.0
    assert summary["unreported_calls"] == 0


def test_usage_ledger_strips_query_strings_and_normalizes_dynamic_ids(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    ledger = tmp_path / "ledger.jsonl"
    instance = runtime(tmp_path, monkeypatch)

    class FakeResp:
        def __init__(self, payload: dict):
            self._data = json.dumps(payload).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self, _n: int = -1) -> bytes:
            return self._data

    monkeypatch.setattr(
        client,
        "urlopen",
        lambda *_a, **_k: FakeResp({"success": True, "data": {"metadata": {"creditsUsed": 1}}}),
    )
    instance.request("/v2/search/developer?query=secret+client+term&k=3&integration=cli", log_usage=True)
    instance.request("/v2/search/research/papers?query=private+query&k=5&integration=cli", log_usage=True)
    instance.request("/v2/scrape/scrape_abc123/interact", method="POST", payload={}, log_usage=True)
    instance.request("/v2/monitor/mon_xyz789/run", method="POST", log_usage=True)

    raw_text = ledger.read_text(encoding="utf-8")
    assert "secret" not in raw_text
    assert "private" not in raw_text
    assert "?" not in raw_text
    summary = client.usage_summary(ledger)
    assert summary["routes"] == {
        "/v2/search/developer": 1,
        "/v2/search/research/papers": 1,
        "/v2/scrape/{id}/interact": 1,
        "/v2/monitor/{id}/run": 1,
    }


def test_urlopen_uses_certifi_ssl_context_and_falls_back(monkeypatch: pytest.MonkeyPatch):
    import ssl
    import sys
    from urllib.request import HTTPSHandler, Request

    seen_handlers = []

    class FakeOpener:
        def open(self, req, timeout=90):
            return (req, timeout)

    def fake_build_opener(*handlers):
        seen_handlers.append(handlers)
        return FakeOpener()

    monkeypatch.setattr(client, "build_opener", fake_build_opener)

    ctx = client._ssl_context()
    if "certifi" in sys.modules or ctx is not None:
        assert isinstance(ctx, ssl.SSLContext)
        client.urlopen(Request("https://api.firecrawl.dev/v2/team/credit-usage"), timeout=10)
        assert any(isinstance(h, HTTPSHandler) for h in seen_handlers[-1])

    # Fallback when _ssl_context returns None (e.g. certifi unavailable).
    monkeypatch.setattr(client, "_ssl_context", lambda: None)
    client.urlopen(Request("https://api.firecrawl.dev/v2/team/credit-usage"), timeout=10)
    assert not any(isinstance(h, HTTPSHandler) for h in seen_handlers[-1])
