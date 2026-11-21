from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from legends_firecrawl.serp_guard import (
    OVERRIDE_ENV,
    OVERRIDE_ENV_ALIAS,
    SuspectSerpError,
    guard_serp,
    load_serp_envelope,
    serp_urls,
    serp_verdict,
)

ROOT = Path(__file__).resolve().parents[1]
_ABSENT = object()


def envelope(status, *, decoy=True, unresolved=False, provider="resolved", urls=None, verified=None,
             integrity_label="protected"):
    integrity = {"status": status, "organic_count": 3,
                 "reasons": [] if status == "clean" else ["AI Overview cites 5 sites; 0.00 overlap with organic top 20"]}
    if decoy:
        integrity["decoy"] = {"provider_resolve": provider, "signals_evaluated": 1}
    if unresolved:
        integrity["unresolved"] = True
    if verified is None:
        verified = status == "clean" and not unresolved
    if verified is not _ABSENT:
        integrity["verified"] = verified
        integrity["integrity"] = integrity_label
        if not verified:
            integrity["unverified"] = True
            integrity["unverified_reasons"] = [f"serp_integrity.status is {status}"]
    items = [{"type": "organic", "url": u, "resolved_url": u} for u in (urls or ["https://a.example.com/x", "https://b.example.org/y"])]
    items.insert(0, {"type": "ai_overview"})
    return {"status_code": 20000, "tasks": [{"id": "t", "result": [{"items": items, "serp_integrity": integrity}]}]}


@pytest.fixture(autouse=True)
def _no_override_env(monkeypatch):
    monkeypatch.delenv(OVERRIDE_ENV, raising=False)
    monkeypatch.delenv(OVERRIDE_ENV_ALIAS, raising=False)


def run_cli(*args, env_extra=None):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "python")
    env.pop("FIRECRAWL_API_KEY", None)
    env.pop(OVERRIDE_ENV, None)
    env.pop(OVERRIDE_ENV_ALIAS, None)
    env["FIRECRAWL_DISABLE_USER_ENV"] = "1"
    env.update(env_extra or {})
    return subprocess.run([sys.executable, "-m", "legends_firecrawl.cli", *args], cwd=ROOT, env=env,
                          text=True, capture_output=True, check=False)


def test_verified_clean_serp_passes_without_warnings():
    verdict = guard_serp(envelope("clean"))
    assert verdict["verified"] is True and verdict["warnings"] == [] and "overridden" not in verdict


@pytest.mark.parametrize("env", [
    envelope("suspect_decoy"),
    envelope("suspect_poisoned"),
    envelope("unverified_decoy", unresolved=True),
    envelope("clean", unresolved=True, verified=True),
    envelope("clean", verified=False),
    envelope("clean", verified=_ABSENT),
    envelope("clean", decoy=False, verified=_ABSENT),
    envelope("clean", verified=True, integrity_label="unprotected"),
    {"tasks": []},
])
def test_anything_not_verified_is_refused(env):
    with pytest.raises(SuspectSerpError) as exc:
        guard_serp(env)
    assert exc.value.verdict["verified"] is False
    assert "--allow-unverified-serp" in str(exc.value) and "--allow-suspect-serp" in str(exc.value)


def test_overrides_flag_env_and_alias_env(monkeypatch):
    verdict = guard_serp(envelope("unverified_decoy", unresolved=True), allow_suspect=True)
    assert verdict["overridden"] is True and any("OVERRIDE" in w for w in verdict["warnings"])
    monkeypatch.setenv(OVERRIDE_ENV, "1")
    assert guard_serp(envelope("suspect_poisoned"))["overridden"] is True
    monkeypatch.delenv(OVERRIDE_ENV)
    monkeypatch.setenv(OVERRIDE_ENV_ALIAS, "1")
    assert guard_serp(envelope("clean", verified=False))["overridden"] is True


def test_verdict_fields_and_warnings():
    empty = serp_verdict({"tasks": []})
    assert empty["status"] == "unassessed" and empty["verified"] is False
    legacy = serp_verdict(envelope("clean", decoy=False, verified=_ABSENT))
    assert legacy["suspect"] is False and legacy["verified"] is False
    assert any("pre-0.1.12" in w for w in legacy["warnings"])
    off = serp_verdict(envelope("clean", provider="not_requested", verified=False, integrity_label="unprotected"))
    assert off["unprotected"] is True
    assert any("not requested" in w for w in off["warnings"]) and any("UNPROTECTED" in w for w in off["warnings"])
    decoy = serp_verdict(envelope("unverified_decoy", unresolved=True))
    assert decoy["status"] == "unverified_decoy" and decoy["suspect"] is True and decoy["unresolved"] is True
    assert "serp_integrity.status is unverified_decoy" in decoy["reasons"]


def test_serp_urls_and_wrapped_files(tmp_path):
    env = envelope("clean", urls=["https://a.example.com/1", "https://a.example.com/1", "https://c.example.net/3"])
    assert serp_urls(env, limit=10) == ["https://a.example.com/1", "https://c.example.net/3"]
    with pytest.raises(Exception):
        serp_urls(env, limit=0)
    wrapped = tmp_path / "wrapped.json"
    wrapped.write_text(json.dumps({"response": env}), encoding="utf-8")
    assert load_serp_envelope(wrapped)["tasks"][0]["id"] == "t"


@pytest.mark.parametrize("status,verified", [("suspect_decoy", None), ("clean", False), ("clean", _ABSENT)])
def test_cli_scrape_serp_refuses_unverified_before_http(tmp_path, status, verified):
    path = tmp_path / "serp.json"
    path.write_text(json.dumps(envelope(status, verified=verified)), encoding="utf-8")
    result = run_cli("scrape-serp", str(path), "--confirm", "--no-save")
    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert payload["success"] is False and "Refusing to scrape" in payload["error"]
    assert payload["serp_provenance"]["verified"] is False
    single = run_cli("scrape", "https://a.example.com/x", "--serp-envelope", str(path), "--no-save")
    assert single.returncode == 2 and "Refusing to scrape" in json.loads(single.stdout)["error"]


@pytest.mark.parametrize("flag", ["--allow-unverified-serp", "--allow-suspect-serp"])
def test_cli_override_flags_warn_and_still_require_confirm(tmp_path, flag):
    path = tmp_path / "serp.json"
    path.write_text(json.dumps(envelope("suspect_decoy")), encoding="utf-8")
    result = run_cli("scrape-serp", str(path), flag, "--no-save")
    assert result.returncode == 2
    assert "requires --confirm" in json.loads(result.stdout)["error"]
    assert "lfc WARNING: OVERRIDE" in result.stderr


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
    assert [w["target"] for w in split["needs_resolve"]] == ["https://www.rotorooter.com › philadelphia", "reddit.com"]
    assert serp_urls(env, limit=10) == ["https://a.example.com/1"]

    only_goto = envelope("clean", urls=["https://google.com/goto?url=CAES9"])
    path = tmp_path / "goto.json"
    path.write_text(json.dumps(only_goto), encoding="utf-8")
    result = run_cli("scrape-serp", str(path), "--confirm", "--no-save")
    assert result.returncode != 0
    assert "--resolve-goto" in (result.stdout + result.stderr)


@pytest.mark.parametrize("name,domain,hint", [
    ("Reddit\xa0·\xa0r/Phoenixville", "reddit.com", "r/Phoenixville"),  # L08 rank 3 verbatim
    ("Reddit · r/philadelphia", "reddit.com", "r/philadelphia"),
    ("Reddit", "reddit.com", None),
    ("Reddit · 30+ comments", "reddit.com", None),              # engagement qualifier dropped
    ("Facebook\xa0·\xa0Roxborough Rants & Raves", "facebook.com", "Roxborough Rants & Raves"),
    ("Instagram\xa0·\xa0scott_plumbing", "instagram.com", "scott_plumbing"),
    ("YouTube\xa0·\xa0Plumbing Pals", "youtube.com", "Plumbing Pals"),
    ("TikTok · @phillyplumber", "tiktok.com", "phillyplumber"),
    ("Yelp", "yelp.com", None),
])
def test_website_name_target_allowlist(name, domain, hint):
    from legends_firecrawl.serp_guard import website_name_target
    got = website_name_target(name)
    assert got == {"target": domain, "domain": domain, "path_hint": hint,
                   "resolution_basis": "website_name"}


@pytest.mark.parametrize("name", ["David Kanaskie's Auto Repair", "Saunders Auto Center",
                                  "Some Local Blog", "", "   ", None, 123])
def test_website_name_target_never_guesses_a_business_domain(name):
    from legends_firecrawl.serp_guard import website_name_target
    assert website_name_target(name) is None


def test_serp_targets_website_name_only_rank3_l08_shape():
    from legends_firecrawl.serp_guard import serp_targets
    env = envelope("clean", urls=["https://a.example.com/1"])
    items = env["tasks"][0]["result"][0]["items"]
    items.append({"type": "organic", "rank_group": 3, "url": "https://google.com/goto?url=CAES3",
                  "domain": "google.com", "resolved_domain": None,
                  "breadcrumb": "30+ comments  ·  2 years ago", "breadcrumb_path_hint": None,
                  "website_name": "Reddit\xa0·\xa0r/Phoenixville",
                  "title": "Mechanic Recommendations? : r/Phoenixville"})
    items.append({"type": "organic", "rank_group": 4, "url": "https://google.com/goto?url=CAES4",
                  "domain": "reddit.com", "breadcrumb": "50+ comments  ·  9 months ago",
                  "breadcrumb_path_hint": "2 years ago",   # poisoned hint must be dropped
                  "website_name": "Reddit · r/philadelphia", "title": "Reputable Plumber : r/philadelphia"})
    split = serp_targets(env, limit=10)
    r3, r4 = split["needs_resolve"]
    assert (r3["target"], r3["domain"], r3["path_hint"], r3["resolution_basis"]) == \
        ("reddit.com", "reddit.com", "r/Phoenixville", "website_name")
    assert (r4["target"], r4["path_hint"], r4["resolution_basis"]) == \
        ("reddit.com", "r/philadelphia", "breadcrumb")  # domain wins, name enriches


def test_resolve_url_website_name_item_search_fallback_and_no_homepage_substitute(monkeypatch):
    from legends_firecrawl import client as client_mod
    from legends_firecrawl.client import FirecrawlClient, SafetyError

    monkeypatch.setattr(client_mod, "validate_public_url", lambda v, **kw: v)  # no DNS
    c = FirecrawlClient.__new__(FirecrawlClient)
    seen = {}
    c.map_site = lambda base_url, **kw: {"links": ["https://www.reddit.com/"]}
    def fake_search(query, **kw):
        seen["query"] = query
        return {"data": {"web": [{"url": "https://www.reddit.com/r/Phoenixville/comments/abc/mechanic_recommendations/"}]}}
    c.search = fake_search
    c.scrape = lambda url, **kw: {"markdown": "thread body", "url": url}

    out = c.resolve_url("reddit.com", path_hint="r/Phoenixville",
                        title="Mechanic Recommendations? : r/Phoenixville",
                        scrape=True, require_candidate=True)
    assert out["resolved_url"].endswith("/r/Phoenixville/comments/abc/mechanic_recommendations/")
    assert "site:reddit.com" in seen["query"]
    assert out["scraped"]["markdown"] == "thread body"

    c.map_site = lambda base_url, **kw: {"links": []}
    c.search = lambda query, **kw: {"data": {"web": []}}
    with pytest.raises(SafetyError, match="refusing to substitute"):
        c.resolve_url("reddit.com", path_hint="r/Phoenixville", title="x", require_candidate=True)
    # Standalone `lfc resolve` behavior unchanged when the flag is off:
    assert c.resolve_url("reddit.com", path_hint="r/Phoenixville", title="x")["resolved_url"] == "https://reddit.com"
