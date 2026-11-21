from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from legends_firecrawl.serp_guard import (
    SuspectSerpError,
    guard_serp,
    load_serp_envelope,
    serp_urls,
    serp_verdict,
)

ROOT = Path(__file__).resolve().parents[1]


def envelope(status, *, decoy=True, unresolved=False, provider="resolved", urls=None):
    integrity = {"status": status, "organic_count": 3, "reasons": [] if status == "clean" else ["Median dated organic result age 2400d exceeds 1095d"]}
    if decoy:
        integrity["decoy"] = {"provider_resolve": provider, "signals_evaluated": 1}
    if unresolved:
        integrity["unresolved"] = True
    items = [{"type": "organic", "url": u, "resolved_url": u} for u in (urls or ["https://a.example.com/x", "https://b.example.org/y"])]
    items.insert(0, {"type": "ai_overview"})
    return {"status_code": 20000, "tasks": [{"id": "t", "result": [{"items": items, "serp_integrity": integrity}]}]}


def run_cli(*args, env_extra=None):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "python")
    env.pop("FIRECRAWL_API_KEY", None)
    env.pop("LEGENDS_FIRECRAWL_ALLOW_SUSPECT_SERP", None)
    env["FIRECRAWL_DISABLE_USER_ENV"] = "1"
    env.update(env_extra or {})
    return subprocess.run([sys.executable, "-m", "legends_firecrawl.cli", *args], cwd=ROOT, env=env,
                          text=True, capture_output=True, check=False)


def test_suspect_decoy_is_refused_unless_overridden(monkeypatch):
    monkeypatch.delenv("LEGENDS_FIRECRAWL_ALLOW_SUSPECT_SERP", raising=False)
    with pytest.raises(SuspectSerpError) as exc:
        guard_serp(envelope("suspect_decoy"))
    assert exc.value.verdict["status"] == "suspect_decoy"
    assert "--allow-suspect-serp" in str(exc.value)
    verdict = guard_serp(envelope("suspect_decoy"), allow_suspect=True)
    assert verdict["overridden"] is True and any("OVERRIDE" in w for w in verdict["warnings"])
    monkeypatch.setenv("LEGENDS_FIRECRAWL_ALLOW_SUSPECT_SERP", "1")
    assert guard_serp(envelope("suspect_poisoned"))["overridden"] is True


def test_unresolved_flag_is_suspect_even_if_status_text_differs(monkeypatch):
    monkeypatch.delenv("LEGENDS_FIRECRAWL_ALLOW_SUSPECT_SERP", raising=False)
    with pytest.raises(SuspectSerpError):
        guard_serp(envelope("clean", unresolved=True))


def test_clean_and_unverified_warnings():
    assert guard_serp(envelope("clean"))["warnings"] == []
    assert serp_verdict({"tasks": []})["status"] == "unassessed"
    legacy = serp_verdict(envelope("clean", decoy=False))
    assert legacy["suspect"] is False and "pre-0.1.12" in legacy["warnings"][0]
    off = serp_verdict(envelope("clean", provider="not_requested"))
    assert "not requested" in off["warnings"][0]
    blind = serp_verdict({"tasks": [{"result": [{"items": [], "serp_integrity": {
        "status": "clean", "organic_count": 0, "decoy": {"provider_resolve": "requested_no_swap", "signals_evaluated": 0}}}]}]})
    assert "fail-open" in blind["warnings"][0]


def test_serp_urls_and_wrapped_files(tmp_path):
    env = envelope("clean", urls=["https://a.example.com/1", "https://a.example.com/1", "https://c.example.net/3"])
    assert serp_urls(env, limit=10) == ["https://a.example.com/1", "https://c.example.net/3"]
    with pytest.raises(Exception):
        serp_urls(env, limit=0)
    wrapped = tmp_path / "wrapped.json"
    wrapped.write_text(json.dumps({"response": env}), encoding="utf-8")
    assert load_serp_envelope(wrapped)["tasks"][0]["id"] == "t"


def test_cli_scrape_serp_refuses_suspect_before_http(tmp_path):
    path = tmp_path / "serp.json"
    path.write_text(json.dumps(envelope("suspect_decoy")), encoding="utf-8")
    result = run_cli("scrape-serp", str(path), "--confirm", "--no-save")
    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert payload["success"] is False and "Refusing to scrape" in payload["error"]
    assert payload["serp_provenance"]["status"] == "suspect_decoy"
    single = run_cli("scrape", "https://a.example.com/x", "--serp-envelope", str(path), "--no-save")
    assert single.returncode == 2 and "Refusing to scrape" in json.loads(single.stdout)["error"]


def test_cli_scrape_serp_requires_confirm_and_override_warns(tmp_path):
    path = tmp_path / "serp.json"
    path.write_text(json.dumps(envelope("suspect_decoy")), encoding="utf-8")
    result = run_cli("scrape-serp", str(path), "--allow-suspect-serp", "--no-save")
    assert result.returncode == 2
    assert "requires --confirm" in json.loads(result.stdout)["error"]
    assert "lfc WARNING: OVERRIDE" in result.stderr


def test_unverified_and_stable_verification_warnings():
    unverified = envelope("clean", provider="not_requested")
    unverified["tasks"][0]["result"][0]["serp_integrity"]["unverified"] = True
    unverified["tasks"][0]["result"][0]["serp_integrity"]["verification"] = {"status": "resolve_off"}
    verdict = serp_verdict(unverified)
    assert verdict["suspect"] is False and verdict["unverified"] is True
    assert any("unverified (verification: resolve_off)" in w for w in verdict["warnings"])
    assert guard_serp(unverified)["status"] == "clean"  # warns, does not refuse

    stable = envelope("clean", provider="requested_no_swap")
    integrity = stable["tasks"][0]["result"][0]["serp_integrity"]
    integrity["decoy"]["signals_evaluated"] = 0
    integrity["verification"] = {"status": "stable", "overlap": 0.9}
    verdict = serp_verdict(stable)
    assert verdict["unverified"] is False and verdict["warnings"] == []


def test_goto_wrapped_results_are_split_out_and_never_scraped_raw(tmp_path):
    from legends_firecrawl.serp_guard import serp_targets

    env = envelope("clean", urls=["https://a.example.com/1"])
    items = env["tasks"][0]["result"][0]["items"]
    items.append({"type": "organic", "rank_group": 2, "url": "https://google.com/goto?url=CAES1", "domain": "google.com",
                  "breadcrumb": "https://www.rotorooter.com › philadelphia", "resolved_domain": "rotorooter.com",
                  "breadcrumb_path_hint": "philadelphia", "title": "Philadelphia Plumber"})
    items.append({"type": "organic", "rank_group": 3, "url": "https://google.com/goto?url=CAES2", "domain": "google.com",
                  "website_name": "Reddit", "title": "Reputable Plumber"})
    split = serp_targets(env, limit=10)
    assert split["urls"] == ["https://a.example.com/1"]
    assert [w["target"] for w in split["needs_resolve"]] == ["https://www.rotorooter.com › philadelphia", None]
    assert serp_urls(env, limit=10) == ["https://a.example.com/1"]

    only_goto = envelope("clean", urls=["https://google.com/goto?url=CAES9"])
    path = tmp_path / "goto.json"
    path.write_text(json.dumps(only_goto), encoding="utf-8")
    result = run_cli("scrape-serp", str(path), "--confirm", "--no-save")
    assert result.returncode != 0
    assert "--resolve-goto" in (result.stdout + result.stderr)
