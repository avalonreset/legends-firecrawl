"""Hermetic tests for Firecrawl v2 / firecrawl-cli@1.23.3 catalog expansion."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from legends_firecrawl import cli, client

ROOT = Path(__file__).resolve().parents[1]


def runtime(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> client.FirecrawlClient:
    monkeypatch.setenv("LEGENDS_FIRECRAWL_LEDGER", str(tmp_path / "ledger.jsonl"))
    return client.FirecrawlClient(client.Credentials("fc-test-key", "test"), consumer="test")


def run_cli(*args: str, env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "python")
    env.pop("FIRECRAWL_API_KEY", None)
    env["FIRECRAWL_DISABLE_USER_ENV"] = "1"
    env.update(env_extra or {})
    return subprocess.run(
        [sys.executable, "-m", "legends_firecrawl.cli", *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_routes_catalog_includes_all_v2_capabilities():
    catalog = client.load_routes()
    assert catalog["schema"] == "legends-firecrawl-routes/v1"
    assert catalog["vendor_cli"] == "firecrawl-cli@1.23.3"
    by_name = {item["name"]: item for item in catalog["routes"]}
    expected = {
        "developer": ("GET", "/v2/search/developer", True),
        "research": ("GET", "/v2/search/research/papers", True),
        "parse": ("POST", "/v2/parse", True),
        "agent": ("POST", "/v2/agent", True),
        "agent-status": ("GET", "/v2/agent/{id}", False),
        "interact": ("POST", "/v2/scrape/{id}/interact", True),
        "monitor": ("POST", "/v2/monitor", True),
        "search-feedback": ("POST", "/v2/search/{searchId}/feedback", False),
    }
    for name, (method, path, charged) in expected.items():
        assert name in by_name
        assert by_name[name]["method"] == method
        assert by_name[name]["path"] == path
        assert by_name[name]["charged"] is charged
        assert client.route_for(name)["name"] == name

    assert client.estimate("developer", limit=15)["page_or_result_ceiling"] == 15
    assert client.estimate("research", limit=20)["page_or_result_ceiling"] == 20
    assert client.estimate("parse")["estimated_credits"] == 1
    assert client.estimate("search-feedback")["estimated_credits"] == 0
    assert client.estimate("agent")["requested_scope"]["max_credits"] == 25


def test_developer_dry_run_confirm_guard_and_mocked_http(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    plan = client.FirecrawlClient.developer_preview("tokio select cancellation", limit=5)
    assert plan["dry_run"] is True
    assert plan["requires_confirm"] is True
    assert plan["method"] == "GET"
    assert plan["path"].startswith("/v2/search/developer?")
    assert "query=tokio+select+cancellation" in plan["path"]
    assert "k=5" in plan["path"]
    assert "integration=cli" in plan["path"]

    instance = runtime(tmp_path, monkeypatch)
    monkeypatch.setattr(instance, "request", lambda *a, **k: pytest.fail("HTTP must not run without confirm"))
    with pytest.raises(client.SafetyError, match="--confirm"):
        instance.developer_search("tokio select")
    assert instance.developer_search("tokio select", dry_run=True)["dry_run"] is True

    with pytest.raises(client.SafetyError, match="limit"):
        instance.developer_search("tokio", limit=25, scrape=True, dry_run=True)

    calls: list[tuple[str, str]] = []

    def fake_request(path: str, **kwargs):
        calls.append((kwargs.get("method", "GET"), path))
        if path.startswith("/v2/search/developer"):
            return {"success": True, "results": [{"id": "doc:1", "url": "https://docs.rs/tokio"}]}
        if path == "/v2/scrape":
            return {"success": True, "data": {"markdown": "# Tokio docs"}}
        raise AssertionError(path)

    monkeypatch.setattr(client, "validate_public_url", lambda v, **kw: v)
    monkeypatch.setattr(instance, "request", fake_request)
    res = instance.developer_search("tokio select", limit=2, scrape=True, confirm=True)
    assert calls[0][0] == "GET" and calls[0][1].startswith("/v2/search/developer?")
    assert calls[1] == ("POST", "/v2/scrape")
    assert res["scraped_results"][0]["url"] == "https://docs.rs/tokio"


def test_research_modes_dry_run_confirm_guard_and_mocked_http(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    plan = client.FirecrawlClient.research_preview(
        "CRISPR base editing",
        limit=12,
        authors=["Doudna"],
        categories=["q-bio.GN"],
        date_from="2024-01-01",
        date_to="2026-01-01",
    )
    assert plan["dry_run"] is True
    assert plan["path"].startswith("/v2/search/research/papers?")
    assert "k=12" in plan["path"]
    assert "authors=Doudna" in plan["path"]
    assert "categories=q-bio.GN" in plan["path"]
    assert "from=2024-01-01" in plan["path"]
    assert "to=2026-01-01" in plan["path"]
    assert "integration=cli" in plan["path"]

    inspect_plan = client.FirecrawlClient.research_preview(mode="inspect", paper_id="arxiv:1706.03762")
    assert inspect_plan["path"] == "/v2/search/research/papers/arxiv%3A1706.03762?integration=cli"

    read_plan = client.FirecrawlClient.research_preview(
        mode="read", paper_id="pmid:40953549", question="Sample size?", limit=4
    )
    assert read_plan["path"].startswith("/v2/search/research/papers/pmid%3A40953549?")
    assert "query=Sample+size%3F" in read_plan["path"]

    rel_plan = client.FirecrawlClient.research_preview(
        mode="related",
        seed_ids=["pmcid:PMC12530322", "pmid:40953549"],
        intent="in vivo delivery",
        relation_mode="similar",
        rerank=True,
    )
    assert rel_plan["path"].startswith("/v2/search/research/papers/pmcid%3APMC12530322/similar?")
    assert "anchor=pmid%3A40953549" in rel_plan["path"]
    assert "rerank=true" in rel_plan["path"]

    gh_plan = client.FirecrawlClient.research_preview("queue worker shutdown", mode="github", limit=5)
    assert gh_plan["path"].startswith("/v2/search/research/github?")

    with pytest.raises(client.SafetyError, match="paper id"):
        client.FirecrawlClient.research_preview(mode="inspect", paper_id="../etc/passwd")

    instance = runtime(tmp_path, monkeypatch)
    monkeypatch.setattr(instance, "request", lambda *a, **k: pytest.fail("HTTP must not run without confirm"))
    with pytest.raises(client.SafetyError, match="--confirm"):
        instance.research_search("CRISPR")

    seen: list[str] = []
    monkeypatch.setattr(client, "validate_public_url", lambda v, **kw: v)

    def fake_request(path: str, **kwargs):
        seen.append(path)
        if path.startswith("/v2/search/research/papers"):
            return {"success": True, "results": [{"primaryId": "arxiv:1706.03762", "url": "https://arxiv.org/abs/1706.03762"}]}
        return {"success": True, "data": {"markdown": "Attention Is All You Need"}}

    monkeypatch.setattr(instance, "request", fake_request)
    out = instance.research_search("attention mechanism", limit=3, scrape=True, confirm=True)
    assert seen[0].startswith("/v2/search/research/papers?")
    assert seen[1] == "/v2/scrape"
    assert out["scraped_results"][0]["url"] == "https://arxiv.org/abs/1706.03762"


def test_parse_dry_run_symlink_refusal_and_multipart_upload(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    sample = tmp_path / "report.pdf"
    sample.write_bytes(b"%PDF-1.4\nhello")

    plan = client.FirecrawlClient.parse_preview(sample, formats=["markdown", "links"], query="Total revenue?")
    assert plan["dry_run"] is True
    assert plan["method"] == "POST"
    assert plan["path"] == "/v2/parse"
    assert plan["content_type"] == "application/pdf"
    assert plan["estimated_credits"] == 1
    assert plan["options"]["formats"] == ["markdown", "links", {"type": "query", "prompt": "Total revenue?"}]

    bad_ext = tmp_path / "script.exe"
    bad_ext.write_bytes(b"MZ")
    with pytest.raises(client.SafetyError, match="Unsupported file type"):
        client.FirecrawlClient.parse_preview(bad_ext)

    link_path = tmp_path / "linked.pdf"
    try:
        link_path.symlink_to(sample)
    except OSError:
        pass
    else:
        with pytest.raises(client.SafetyError, match="symlink"):
            client.FirecrawlClient.parse_preview(link_path)

    instance = runtime(tmp_path, monkeypatch)
    monkeypatch.setattr(instance, "request", lambda *a, **k: pytest.fail("HTTP must not run without confirm"))
    with pytest.raises(client.SafetyError, match="--confirm"):
        instance.parse_file(sample)

    captured: dict = {}

    def fake_request(path: str, **kwargs):
        captured["path"] = path
        captured.update(kwargs)
        return {"success": True, "data": {"markdown": "# Parsed PDF"}}

    monkeypatch.setattr(instance, "request", fake_request)
    out = instance.parse_file(sample, formats=["markdown", "links"], confirm=True)
    assert out["data"]["markdown"] == "# Parsed PDF"
    assert captured["path"] == "/v2/parse"
    assert captured["method"] == "POST"
    assert captured["content_type"].startswith("multipart/form-data; boundary=")
    assert b'filename="report.pdf"' in captured["raw_body"]
    assert b"Content-Type: application/pdf" in captured["raw_body"]
    assert b"%PDF-1.4\nhello" in captured["raw_body"]
    assert b'name="options"' in captured["raw_body"]
    assert b'"integration":"cli"' in captured["raw_body"]


def test_agent_and_agent_status_guards_and_mocked_http(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr(client, "validate_public_url", lambda v, **kw: v)
    schema_path = tmp_path / "schema.json"
    schema_path.write_text(json.dumps({"type": "object", "properties": {"price": {"type": "string"}}}), encoding="utf-8")

    plan = client.FirecrawlClient.agent_preview(
        "Extract pricing tiers",
        urls=["https://example.com/pricing"],
        model="spark-1-mini",
        max_credits=15,
        schema_file=schema_path,
        strict_constrain_to_urls=True,
    )
    assert plan["dry_run"] is True
    assert plan["path"] == "/v2/agent"
    assert plan["payload"]["maxCredits"] == 15
    assert plan["payload"]["strictConstrainToURLs"] is True
    assert plan["payload"]["schema"]["type"] == "object"

    with pytest.raises(client.SafetyError, match="max_credits"):
        client.FirecrawlClient.agent_preview("Extract", max_credits=9999)
    with pytest.raises(client.SafetyError, match="max_credits"):
        client.FirecrawlClient.agent_preview("Extract", max_credits=0)
    with pytest.raises(client.SafetyError, match="model"):
        client.FirecrawlClient.agent_preview("Extract", model="unknown-model")

    instance = runtime(tmp_path, monkeypatch)
    monkeypatch.setattr(instance, "request", lambda *a, **k: pytest.fail("HTTP must not run without confirm"))
    with pytest.raises(client.SafetyError, match="--confirm"):
        instance.agent_start("Extract pricing")
    with pytest.raises(client.SafetyError, match="job id"):
        instance.agent_status("../bad")
    with pytest.raises(client.SafetyError, match="--confirm"):
        instance.agent_cancel("agent_job_123456")

    seen: list[tuple[str, str, dict | None]] = []

    def fake_request(path: str, **kwargs):
        seen.append((kwargs.get("method", "GET"), path, kwargs.get("payload")))
        return {"success": True, "id": "agent_job_123456", "status": "processing"}

    monkeypatch.setattr(instance, "request", fake_request)
    instance.agent_start("Extract pricing", max_credits=10, confirm=True)
    instance.agent_status("agent_job_123456")
    instance.agent_cancel("agent_job_123456", confirm=True)
    assert seen[0][0] == "POST" and seen[0][1] == "/v2/agent" and seen[0][2]["maxCredits"] == 10
    assert seen[1] == ("GET", "/v2/agent/agent_job_123456", None)
    assert seen[2] == ("DELETE", "/v2/agent/agent_job_123456", None)


def test_interact_guards_and_mocked_http(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    with pytest.raises(client.SafetyError, match="exactly one"):
        client.FirecrawlClient.interact_preview("scrape_123456")
    with pytest.raises(client.SafetyError, match="scrape id"):
        client.FirecrawlClient.interact_preview("../evil", prompt="click")

    exec_plan = client.FirecrawlClient.interact_preview("scrape_123456", prompt="Click pricing tab", timeout=30)
    assert exec_plan["path"] == "/v2/scrape/scrape_123456/interact"
    assert exec_plan["payload"]["prompt"] == "Click pricing tab"

    stop_plan = client.FirecrawlClient.interact_preview("scrape_123456", stop=True)
    assert stop_plan["method"] == "DELETE"

    instance = runtime(tmp_path, monkeypatch)
    seen: list[tuple[str, str]] = []
    monkeypatch.setattr(instance, "request", lambda path, **kw: (seen.append((kw.get("method", "GET"), path)) or {"success": True}))
    with pytest.raises(client.SafetyError, match="--confirm"):
        instance.interact("scrape_123456", prompt="Click")
    instance.interact("scrape_123456", code="await page.title()", language="node", confirm=True)
    instance.interact("scrape_123456", stop=True, confirm=True)
    assert seen == [
        ("POST", "/v2/scrape/scrape_123456/interact"),
        ("DELETE", "/v2/scrape/scrape_123456/interact"),
    ]


def test_monitor_actions_guards_and_x_origin_header(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr(client, "validate_public_url", lambda v, **kw: v)
    create_plan = client.FirecrawlClient.monitor_preview(
        "create",
        name="Pricing watch",
        schedule_text="every 6 hours",
        timezone_name="UTC",
        page="https://example.com/pricing",
        goal="Alert on price changes",
    )
    assert create_plan["method"] == "POST"
    assert create_plan["path"] == "/v2/monitor"
    assert create_plan["requires_confirm"] is True
    assert create_plan["payload"]["targets"] == [{"type": "scrape", "urls": ["https://example.com/pricing"]}]

    with pytest.raises(client.SafetyError, match="--goal"):
        client.FirecrawlClient.monitor_preview(
            "create", name="Search watch", schedule_text="daily", queries=["llm release"]
        )
    with pytest.raises(client.SafetyError, match="monitor id"):
        client.FirecrawlClient.monitor_preview("get", monitor_id="../bad")

    instance = runtime(tmp_path, monkeypatch)
    with pytest.raises(client.SafetyError, match="--confirm"):
        instance.monitor("create", name="Watch", schedule_text="daily", page="https://example.com")
    with pytest.raises(client.SafetyError, match="--confirm"):
        instance.monitor("run", monitor_id="mon_abc123")
    with pytest.raises(client.SafetyError, match="--confirm"):
        instance.monitor("delete", monitor_id="mon_abc123")

    seen: list[tuple[str, str, dict | None]] = []

    def fake_request(path: str, **kwargs):
        seen.append((kwargs.get("method", "GET"), path, kwargs.get("extra_headers")))
        return {"success": True, "data": {"id": "mon_abc123"}}

    monkeypatch.setattr(instance, "request", fake_request)
    instance.monitor("list", limit=20)
    instance.monitor("get", monitor_id="mon_abc123")
    instance.monitor("create", name="Watch", schedule_text="daily", page="https://example.com", confirm=True)
    instance.monitor("update", monitor_id="mon_abc123", state="paused", confirm=True)
    instance.monitor("run", monitor_id="mon_abc123", confirm=True)
    instance.monitor("checks", monitor_id="mon_abc123", limit=5)
    instance.monitor("check", monitor_id="mon_abc123", check_id="chk_xyz", page_status="changed")
    instance.monitor("delete", monitor_id="mon_abc123", confirm=True)

    assert [row[:2] for row in seen] == [
        ("GET", "/v2/monitor?limit=20"),
        ("GET", "/v2/monitor/mon_abc123"),
        ("POST", "/v2/monitor"),
        ("PATCH", "/v2/monitor/mon_abc123"),
        ("POST", "/v2/monitor/mon_abc123/run"),
        ("GET", "/v2/monitor/mon_abc123/checks?limit=5"),
        ("GET", "/v2/monitor/mon_abc123/checks/chk_xyz?status=changed"),
        ("DELETE", "/v2/monitor/mon_abc123"),
    ]
    assert all(row[2] == {"X-Origin": "cli"} for row in seen)


def test_search_feedback_preview_opt_out_and_mocked_http(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    plan = client.FirecrawlClient.search_feedback_preview(
        "srch_123456",
        rating="good",
        valuable_sources=[{"url": "https://example.com/docs", "reason": "exact spec"}],
        missing_content=[{"topic": "rate limits", "description": "no burst numbers"}],
        query_suggestions="include rate limits",
    )
    assert plan["dry_run"] is True
    assert plan["path"] == "/v2/search/srch_123456/feedback"
    assert plan["estimated_credits"] == 0
    assert plan["refund_credits_on_first_submit"] == 1
    assert plan["payload"]["rating"] == "good"
    assert plan["payload"]["valuableSources"] == [{"url": "https://example.com/docs", "reason": "exact spec"}]

    with pytest.raises(client.SafetyError, match="rating"):
        client.FirecrawlClient.search_feedback_preview("srch_123456", rating="meh")
    with pytest.raises(client.SafetyError, match="Local hosts|Private"):
        client.FirecrawlClient.search_feedback_preview(
            "srch_123456", rating="good", valuable_sources=[{"url": "http://127.0.0.1/secret"}]
        )

    instance = runtime(tmp_path, monkeypatch)
    monkeypatch.setenv("FIRECRAWL_NO_SEARCH_FEEDBACK", "1")
    monkeypatch.setattr(instance, "request", lambda *a, **k: pytest.fail("HTTP must not run when disabled"))
    disabled = instance.search_feedback("srch_123456", rating="good")
    assert disabled["disabled"] is True and disabled["creditsRefunded"] == 0

    monkeypatch.delenv("FIRECRAWL_NO_SEARCH_FEEDBACK")
    seen: list[tuple[str, str, dict]] = []

    def fake_request(path: str, **kwargs):
        seen.append((kwargs.get("method", "GET"), path, kwargs.get("payload")))
        return {"success": True, "feedbackId": "fb_1", "creditsRefunded": 1}

    monkeypatch.setattr(instance, "request", fake_request)
    res = instance.search_feedback("srch_123456", rating="partial", query_suggestions="narrow date")
    assert res["creditsRefunded"] == 1
    assert seen[0][0] == "POST"
    assert seen[0][1] == "/v2/search/srch_123456/feedback"
    assert seen[0][2]["origin"] == "cli"


def test_cli_dry_run_and_confirm_gates_work_offline_without_auth(tmp_path: Path):
    sample = tmp_path / "doc.html"
    sample.write_text("<h1>Hello</h1>", encoding="utf-8")

    dry_cases = [
        (["developer", "axum middleware", "--limit", "5", "--dry-run"], "developer"),
        (["research", "CRISPR editing", "--limit", "8", "--dry-run"], "research"),
        (["parse", str(sample), "--formats", "markdown,links", "--dry-run"], "parse"),
        (["agent", "Find founders", "--max-credits", "15", "--dry-run"], "agent"),
        (["agent-status", "agent_job_123456", "--dry-run"], "agent-status"),
        (["agent-status", "agent_job_123456", "--cancel", "--dry-run"], "agent-cancel"),
        (["interact", "scrape_123456", "--prompt", "Click docs", "--dry-run"], "interact"),
        (["monitor", "list", "--limit", "10", "--dry-run"], "monitor"),
        (["monitor", "create", "--name", "Blog", "--schedule", "daily", "--page", "https://example.com", "--dry-run"], "monitor"),
        (["search-feedback", "srch_123456", "--rating", "good", "--dry-run"], "search-feedback"),
    ]
    for argv, expected_op in dry_cases:
        res = run_cli(*argv)
        assert res.returncode == 0, f"{argv} failed: {res.stdout} {res.stderr}"
        payload = json.loads(res.stdout)
        assert payload["dry_run"] is True
        assert payload["operation"] == expected_op

    refuse_cases = [
        ["developer", "axum middleware"],
        ["research", "CRISPR editing"],
        ["parse", str(sample)],
        ["agent", "Find founders"],
        ["agent-status", "agent_job_123456", "--cancel"],
        ["interact", "scrape_123456", "--prompt", "Click"],
        ["monitor", "create", "--name", "Blog", "--schedule", "daily", "--page", "https://example.com"],
        ["monitor", "delete", "mon_abc123"],
        ["monitor", "run", "mon_abc123"],
    ]
    for argv in refuse_cases:
        res = run_cli(*argv)
        assert res.returncode == 2, f"{argv} should fail closed without --confirm"
        assert "--confirm" in json.loads(res.stdout)["error"]


def test_cli_mocked_dispatch_and_capture_archival(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys):
    monkeypatch.setenv("LEGENDS_FIRECRAWL_CAPTURE_ROOT", str(tmp_path))
    called: list[str] = []

    class FakeClient:
        def __init__(self, **kwargs):
            pass

        def developer_search(self, query, **kwargs):
            called.append("developer")
            return {"success": True, "results": [{"id": "doc:1", "title": query}]}

        def research_search(self, query, **kwargs):
            called.append("research")
            return {"success": True, "results": [{"primaryId": "arxiv:1706.03762"}]}

        def parse_file(self, file_path, **kwargs):
            called.append("parse")
            return {"success": True, "data": {"markdown": "# Parsed"}}

        def agent_start(self, prompt, **kwargs):
            called.append("agent")
            return {"success": True, "id": "agent_job_123456"}

        def agent_status(self, job_id):
            called.append("agent-status")
            return {"success": True, "id": job_id, "status": "completed"}

        def monitor(self, action, **kwargs):
            called.append(f"monitor:{action}")
            return {"success": True, "action": action}

        def search_feedback(self, search_id, **kwargs):
            called.append("search-feedback")
            return {"success": True, "creditsRefunded": 1}

    sample = tmp_path / "notes.html"
    sample.write_text("<p>Hi</p>", encoding="utf-8")
    monkeypatch.setattr(cli, "FirecrawlClient", FakeClient)
    # Keep preview methods available on FakeClient
    for attr in ("developer_preview", "research_preview", "parse_preview", "agent_preview",
                 "interact_preview", "monitor_preview", "search_feedback_preview"):
        setattr(FakeClient, attr, getattr(client.FirecrawlClient, attr))

    for argv in [
        ["developer", "tokio", "--confirm"],
        ["research", "transformers", "--confirm"],
        ["parse", str(sample), "--confirm"],
        ["agent", "Extract prices", "--max-credits", "10", "--confirm"],
        ["agent-status", "agent_job_123456"],
        ["monitor", "list"],
        ["search-feedback", "srch_123456", "--rating", "good", "--valuable-sources", "https://example.com/a"],
    ]:
        assert cli.main(argv) == 0
        out = json.loads(capsys.readouterr().out)
        assert out["success"] is True
        assert "_capture" in out
        assert Path(out["_capture"]["rawFilePath"]).is_file()

    assert called == ["developer", "research", "parse", "agent", "agent-status", "monitor:list", "search-feedback"]


def test_research_scrape_derives_canonical_urls_from_primary_id_and_ids(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    instance = runtime(tmp_path, monkeypatch)
    monkeypatch.setattr(client, "validate_public_url", lambda v, **kw: v)
    scraped_urls: list[str] = []

    def fake_request(path: str, **kwargs):
        if path.startswith("/v2/search/research/papers"):
            return {
                "success": True,
                "results": [
                    {"paperId": "p1", "primaryId": "arxiv:2505.12065", "ids": {"arxiv": ["2505.12065"]}},
                    {"paperId": "p2", "primaryId": "pubmed:40953549"},
                    {"paperId": "p3", "ids": {"pmid": "12345678"}},
                    {"paperId": "p4", "primaryId": "biorxiv:10.1101/2024.01.01.573829v1"},
                    {"paperId": "p5", "primaryId": "medrxiv:10.1101/2024.02.02.24302100v1"},
                    {"paperId": "p6", "ids": {"doi": ["10.1038/s41586-021-03819-2"]}},
                    {"paperId": "p7", "primaryId": "arxiv:../../etc/passwd"},
                ],
            }
        if path == "/v2/scrape":
            scraped_urls.append(kwargs["payload"]["url"])
            return {"success": True, "data": {"markdown": "# Paper"}}
        raise AssertionError(path)

    monkeypatch.setattr(instance, "request", fake_request)
    out = instance.research_search("retrieval", limit=10, scrape=True, confirm=True)
    expected = [
        "https://arxiv.org/abs/2505.12065",
        "https://pubmed.ncbi.nlm.nih.gov/40953549/",
        "https://pubmed.ncbi.nlm.nih.gov/12345678/",
        "https://www.biorxiv.org/content/10.1101/2024.01.01.573829v1",
        "https://www.medrxiv.org/content/10.1101/2024.02.02.24302100v1",
        "https://doi.org/10.1038/s41586-021-03819-2",
    ]
    assert scraped_urls == expected
    assert [row["url"] for row in out["scraped_results"]] == expected


def test_search_feedback_does_not_register_dead_confirm_flag():
    res = run_cli("search-feedback", "srch_123456", "--rating", "good", "--confirm")
    assert res.returncode == 2
    assert "unrecognized arguments: --confirm" in res.stderr


def test_interact_monitor_feedback_multipart_and_inspect_scrape_hardening(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    # Whitespace-only prompt/code and conflicting --stop + --prompt fail closed.
    with pytest.raises(client.SafetyError):
        client.FirecrawlClient.interact_preview("scrape_123456", prompt="   ")
    with pytest.raises(client.SafetyError):
        client.FirecrawlClient.interact_preview("scrape_123456", code="   ")
    with pytest.raises(client.SafetyError, match="cannot be combined"):
        client.FirecrawlClient.interact_preview("scrape_123456", prompt="click", stop=True)

    # Whitespace-only monitor schedule, queries, or update fields fail closed.
    with pytest.raises(client.SafetyError, match="--cron or --schedule"):
        client.FirecrawlClient.monitor_preview("create", name="Watch", cron="   ", page="https://example.com")
    with pytest.raises(client.SafetyError, match="--page"):
        client.FirecrawlClient.monitor_preview("create", name="Watch", schedule_text="daily", queries=["   "], goal="g")
    with pytest.raises(client.SafetyError, match="at least one field"):
        client.FirecrawlClient.monitor_preview("update", monitor_id="mon_123", name="   ")

    # Malformed JSON entries in --valuable-sources / --missing-content fail closed instead of silent drop.
    with pytest.raises(client.SafetyError, match="--valuable-sources"):
        cli._parse_valuable_sources('[{"wrong": 1}]')
    with pytest.raises(client.SafetyError, match="--missing-content"):
        cli._parse_missing_content(['[{"wrong": 1}]'])

    # Multipart encoder rotates boundary if payload contains initial UUID hex.
    seq = iter(["deadbeef" * 4, "cafebabe" * 4])

    class FakeUUID:
        def __init__(self, h: str):
            self.hex = h

    monkeypatch.setattr(client, "uuid4", lambda: FakeUUID(next(seq)))
    body, ct = client._encode_multipart(
        "file",
        'tricky"name\r\n.html',
        "text/html",
        b"contains legendsfc" + (b"deadbeef" * 4),
        {"options": "{}"},
    )
    assert "cafebabe" in ct and b"legendsfccafebabe" in body
    assert b'filename="tricky_name.html"' in body

    # research --mode inspect --scrape derives and scrapes single-paper response.
    instance = runtime(tmp_path, monkeypatch)
    monkeypatch.setattr(client, "validate_public_url", lambda v, **kw: v)
    monkeypatch.setattr(
        instance,
        "request",
        lambda path, **kw: (
            {"success": True, "paperId": "p1", "primaryId": "arxiv:2505.12065"}
            if path.startswith("/v2/search/research/papers/")
            else {"success": True, "data": {"markdown": "# Full Paper"}}
        ),
    )
    inspected = instance.research_search(
        mode="inspect", paper_id="arxiv:2505.12065", scrape=True, confirm=True
    )
    assert inspected["scraped_results"][0]["url"] == "https://arxiv.org/abs/2505.12065"
