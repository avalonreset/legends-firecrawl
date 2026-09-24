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
    monkeypatch.setattr(client, "_windows_user_environment", lambda _name: None)
    with pytest.raises(client.CredentialError) as error:
        client.load_credentials()
    assert "setup-auth.ps1" in str(error.value)
    assert "MCP" not in str(error.value)


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
        "https://user:pass@example.com/a",
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


def test_routes_and_estimates_are_intent_first():
    routes = client.load_routes()["routes"]
    assert {item["name"] for item in routes} == {"credits", "scrape", "map", "search", "crawl", "crawl-status"}
    estimate = client.estimate("crawl", limit=40)
    assert estimate["page_or_result_ceiling"] == 40
    assert estimate["estimated_credits"] is None


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
