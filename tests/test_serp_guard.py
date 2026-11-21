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


def test_resolve_url_homepage_shortcircuit_and_scoring_without_path_hint(monkeypatch):
    from legends_firecrawl import client as client_mod
    from legends_firecrawl.client import FirecrawlClient

    monkeypatch.setattr(client_mod, "validate_public_url", lambda v, **kw: v)
    c = FirecrawlClient.__new__(FirecrawlClient)
    calls = []
    c.map_site = lambda *a, **kw: (calls.append("map") or {"links": []})
    c.search = lambda *a, **kw: (calls.append("search") or {"data": {"web": []}})
    scraped_args = {}

    def fake_scrape(url, **kw):
        calls.append("scrape")
        scraped_args["url"] = url
        scraped_args.update(kw)
        return {"success": True, "data": {"markdown": "# Home"}}

    c.scrape = fake_scrape

    # Bare homepage breadcrumb shortcircuits directly without spending map/search credits.
    out = c.resolve_url(
        "https://davidkanaskiesautorepair.com",
        path_hint=None,
        title="David Kanaskie's Auto Repair | Phoenixville PA",
        scrape=True,
        only_main_content=False,
        max_age_ms=0,
        require_candidate=True,
        allow_homepage_shortcircuit=True,
    )
    assert out["resolved_url"] == "https://davidkanaskiesautorepair.com"
    assert out["resolution_method"] == "breadcrumb_root"
    assert calls == ["scrape"]
    assert scraped_args["only_main_content"] is False
    assert scraped_args["max_age_ms"] == 0

    # Breadcrumb with an inner segment must NOT shortcircuit even when allow_homepage_shortcircuit=True.
    calls.clear()
    c.map_site = lambda *a, **kw: (
        calls.append("map")
        or {"links": ["https://www.rotorooter.com/", "https://www.rotorooter.com/philadelphia/"]}
    )
    inner = c.resolve_url(
        "https://www.rotorooter.com › philadelphia",
        path_hint=None,
        title="Philadelphia Plumber",
        require_candidate=True,
        allow_homepage_shortcircuit=True,
    )
    assert calls == ["map"]
    assert inner["resolved_url"] == "https://www.rotorooter.com/philadelphia/"

    # _score_candidate_url must not award the +5 inner-page bonus when path_hint is empty/None.
    root_score = FirecrawlClient._score_candidate_url(
        "https://example.com/", path_hint=None, title=None, keyword=None
    )
    inner_score = FirecrawlClient._score_candidate_url(
        "https://example.com/blog/unrelated", path_hint=None, title=None, keyword=None
    )
    assert root_score == 0 and inner_score == 0
    inner_with_hint = FirecrawlClient._score_candidate_url(
        "https://example.com/blog/unrelated", path_hint="services", title=None, keyword=None
    )
    assert inner_with_hint == 5


def test_serp_targets_preserves_rank_and_mixed_order():
    from legends_firecrawl.serp_guard import serp_targets

    env = envelope("clean", urls=[])
    env["tasks"][0]["result"][0]["items"] = [
        {"type": "organic", "rank_group": 3, "url": "https://c.example.com/page", "domain": "c.example.com", "title": "Three"},
        {"type": "organic", "rank_group": 1, "url": "https://a.example.com/", "domain": "a.example.com", "title": "One"},
        {
            "type": "organic",
            "rank_group": 2,
            "url": "https://google.com/goto?url=CAES2",
            "domain": "google.com",
            "breadcrumb": "https://b.example.com",
            "resolved_domain": "b.example.com",
            "breadcrumb_path_hint": None,
            "title": "Two",
        },
    ]
    split = serp_targets(env, limit=10)
    assert split["urls"] == ["https://a.example.com/", "https://c.example.com/page"]
    assert [d["rank"] for d in split["direct_items"]] == [1, 3]
    assert split["direct_items"][0]["domain"] == "a.example.com"
    assert [(t["kind"], t["rank"]) for t in split["ordered_targets"]] == [
        ("direct", 1),
        ("goto", 2),
        ("direct", 3),
    ]


def test_cli_scrape_serp_mixed_order_shortcircuit_options_and_provider_error(monkeypatch, tmp_path, capsys):
    from legends_firecrawl import cli
    from legends_firecrawl.client import ApiError

    env = envelope("clean", urls=[])
    env["tasks"][0]["result"][0]["items"] = [
        {
            "type": "organic",
            "rank_group": 1,
            "url": "https://google.com/goto?url=CAES1",
            "domain": "google.com",
            "breadcrumb": "https://davidkanaskiesautorepair.com",
            "resolved_domain": "davidkanaskiesautorepair.com",
            "breadcrumb_path_hint": None,
            "title": "David Kanaskie Auto Repair",
        },
        {
            "type": "organic",
            "rank_group": 2,
            "url": "https://direct.example.com/shop",
            "domain": "direct.example.com",
            "title": "Direct Shop",
        },
        {
            "type": "organic",
            "rank_group": 3,
            "url": "https://google.com/goto?url=CAES3",
            "domain": "google.com",
            "breadcrumb": "30+ comments · 2 years ago",
            "breadcrumb_path_hint": None,
            "website_name": "Reddit\xa0·\xa0r/Phoenixville",
            "title": "Mechanic Recommendations?",
        },
        {
            "type": "organic",
            "rank_group": 4,
            "url": "https://blocked.example.com/page",
            "domain": "blocked.example.com",
            "title": "Blocked Direct",
        },
    ]
    serp_path = tmp_path / "mixed.json"
    serp_path.write_text(json.dumps(env), encoding="utf-8")

    resolve_calls = []
    scrape_calls = []

    class FakeClient:
        def __init__(self, **kwargs):
            pass

        def resolve_url(self, target, **kwargs):
            resolve_calls.append((target, kwargs))
            if target == "reddit.com":
                raise ApiError(
                    "Firecrawl returned HTTP 403 for /v2/scrape",
                    response={"success": False, "error": "Website Not Supported"},
                )
            return {
                "success": True,
                "resolved_url": target,
                "resolution_method": "breadcrumb_root",
                "base_url": target,
                "path_hint": None,
                "scraped": {"success": True, "data": {"markdown": "# Home"}},
            }

        def scrape(self, url, **kwargs):
            scrape_calls.append((url, kwargs))
            if "blocked.example.com" in url:
                raise ApiError(
                    "Firecrawl returned HTTP 403 for /v2/scrape",
                    response={"success": False, "error": "Blocked by policy"},
                )
            return {"success": True, "data": {"markdown": f"# {url}"}}

    monkeypatch.setattr(cli, "FirecrawlClient", FakeClient)
    code = cli.main([
        "scrape-serp",
        str(serp_path),
        "--resolve-goto",
        "--full-page",
        "--max-age-ms",
        "1234",
        "--confirm",
        "--no-save",
    ])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["success"] is True
    assert [p["rank"] for p in payload["pages"]] == [1, 2, 4]
    assert payload["pages"][0]["url"] == "https://davidkanaskiesautorepair.com"
    assert payload["pages"][1]["url"] == "https://direct.example.com/shop"
    assert payload["pages"][2]["provider_error"] == {"success": False, "error": "Blocked by policy"}

    # Bare breadcrumb root got allow_homepage_shortcircuit=True; website_name got False.
    assert resolve_calls[0][1]["allow_homepage_shortcircuit"] is True
    assert resolve_calls[0][1]["only_main_content"] is False
    assert resolve_calls[0][1]["max_age_ms"] == 1234
    assert resolve_calls[1][0] == "reddit.com"
    assert resolve_calls[1][1]["allow_homepage_shortcircuit"] is False
    assert scrape_calls[0][1]["only_main_content"] is False
    assert scrape_calls[0][1]["max_age_ms"] == 1234

    assert len(payload["needs_resolve"]) == 1
    assert payload["needs_resolve"][0]["rank"] == 3
    assert payload["needs_resolve"][0]["provider_error"] == {"success": False, "error": "Website Not Supported"}


def test_post_resolution_scrape_error_preserves_resolved_url_in_pages_and_standalone_resolve(
    monkeypatch, tmp_path, capsys
):
    from legends_firecrawl import cli, client as client_mod
    from legends_firecrawl.client import ApiError, Credentials, FirecrawlClient

    monkeypatch.setattr(client_mod, "validate_public_url", lambda v, **kw: v)
    env = envelope("clean", urls=[])
    env["tasks"][0]["result"][0]["items"] = [
        {
            "type": "organic",
            "rank_group": 1,
            "url": "https://google.com/goto?url=CAES1",
            "domain": "google.com",
            "breadcrumb": "https://blocked-root.example.com",
            "resolved_domain": "blocked-root.example.com",
            "breadcrumb_path_hint": None,
            "title": "Blocked Root Shop",
        },
        {
            "type": "organic",
            "rank_group": 3,
            "url": "https://google.com/goto?url=CAES3",
            "domain": "google.com",
            "resolved_domain": None,
            "breadcrumb": "30+ comments  ·  2 years ago",
            "breadcrumb_path_hint": None,
            "website_name": "Reddit\xa0·\xa0r/Phoenixville",
            "title": "Mechanic Recommendations? : r/Phoenixville",
        },
    ]
    serp_path = tmp_path / "l08_rank3.json"
    serp_path.write_text(json.dumps(env), encoding="utf-8")

    reddit_thread = "https://www.reddit.com/r/Phoenixville/comments/1bqm14z/mechanic_recommendations/"

    def fake_map(self, base_url, **kw):
        raise ApiError("Firecrawl returned HTTP 403 for /v2/map", response={"error": "map unsupported"})

    def fake_search(self, query, **kw):
        return {"success": True, "data": {"web": [{"url": reddit_thread}]}}

    def fake_scrape(self, url, **kw):
        raise ApiError(
            "Firecrawl returned HTTP 403 for /v2/scrape",
            response={"success": False, "error": "we do not support this site"},
        )

    monkeypatch.setattr(FirecrawlClient, "map_site", fake_map)
    monkeypatch.setattr(FirecrawlClient, "search", fake_search)
    monkeypatch.setattr(FirecrawlClient, "scrape", fake_scrape)
    monkeypatch.setattr(
        cli,
        "FirecrawlClient",
        lambda **kw: FirecrawlClient(Credentials("fc-test-key", "test"), consumer="lfc"),
    )

    code = cli.main(["scrape-serp", str(serp_path), "--resolve-goto", "--confirm", "--no-save"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["needs_resolve"] == []
    assert len(payload["pages"]) == 2

    p1, p3 = payload["pages"]
    assert p1["rank"] == 1
    assert p1["url"] == "https://blocked-root.example.com"
    assert p1["goto_resolved"] is True
    assert p1["resolution"] == {
        "resolution_method": "breadcrumb_root",
        "base_url": "https://blocked-root.example.com",
    }
    assert p1["resolution_basis"] == "breadcrumb"
    assert p1["provider_error"] == {"success": False, "error": "we do not support this site"}

    assert p3["rank"] == 3
    assert p3["url"] == reddit_thread
    assert p3["goto_resolved"] is True
    assert p3["resolution"] == {
        "resolution_method": "search",
        "base_url": "https://reddit.com",
        "path_hint": "r/Phoenixville",
        "map_error": "Firecrawl returned HTTP 403 for /v2/map",
    }
    assert p3["resolution_basis"] == "website_name"
    assert "HTTP 403" in p3["error"]
    assert p3["provider_error"] == {"success": False, "error": "we do not support this site"}

    # Standalone lfc resolve --scrape also retains resolved_result in the error envelope.
    rc = cli.main([
        "resolve",
        "reddit.com",
        "--path-hint",
        "r/Phoenixville",
        "--title",
        "Mechanic Recommendations? : r/Phoenixville",
        "--scrape",
        "--no-save",
    ])
    assert rc == 2
    standalone_err = json.loads(capsys.readouterr().out)
    assert standalone_err["resolved_result"]["resolved_url"] == reddit_thread


def test_multi_block_serp_missing_integrity_on_second_block_fails_closed():
    valid = envelope("clean", urls=["https://safe.example.com/a"])
    valid["tasks"][0]["result"].append({
        "items": [{"type": "organic", "rank_group": 1, "url": "https://decoy.example.org/trap"}]
    })
    with pytest.raises(SuspectSerpError) as exc:
        guard_serp(valid)
    assert exc.value.verdict["verified"] is False
    assert exc.value.verdict["status"] == "unassessed"
    assert "SERP result block is missing serp_integrity" in exc.value.verdict["reasons"]


def test_resolve_url_rejects_homepage_in_map_links_and_bare_subreddit_container(monkeypatch):
    from legends_firecrawl import client as client_mod
    from legends_firecrawl.client import FirecrawlClient, SafetyError

    monkeypatch.setattr(client_mod, "validate_public_url", lambda v, **kw: v)
    c = FirecrawlClient.__new__(FirecrawlClient)
    search_calls = []

    # Map returns both root / and bare /r/Phoenixville/; search finds the actual thread.
    c.map_site = lambda base_url, **kw: {
        "links": ["https://www.reddit.com/", "https://www.reddit.com/r/Phoenixville/"]
    }
    c.search = lambda q, **kw: (
        search_calls.append(q)
        or {"data": {"web": ["https://www.reddit.com/r/Phoenixville/comments/9xyz/best_shop/"]}}
    )
    resolved = c.resolve_url(
        "reddit.com",
        path_hint="r/Phoenixville",
        title="Mechanic Recommendations? : r/Phoenixville",
        require_candidate=True,
    )
    assert len(search_calls) == 1
    assert resolved["resolved_url"] == "https://www.reddit.com/r/Phoenixville/comments/9xyz/best_shop/"

    # When search returns empty, bare /r/Phoenixville/ and / must NOT satisfy require_candidate=True.
    c.search = lambda q, **kw: {"data": {"web": []}}
    with pytest.raises(SafetyError, match="refusing to substitute"):
        c.resolve_url(
            "reddit.com",
            path_hint="r/Phoenixville",
            title="Mechanic Recommendations?",
            require_candidate=True,
        )

    # Invalid scrape format fails before spending map_site credits.
    map_invoked = []
    c.map_site = lambda *a, **kw: (map_invoked.append(1) or {"links": []})
    with pytest.raises(SafetyError, match="formats"):
        c.resolve_url("example.com", path_hint="pricing", scrape=True, formats=["screenshot"])
    assert map_invoked == []


def test_scrape_serp_dry_run_engagement_breadcrumb_and_unordered_limit(monkeypatch, tmp_path):
    from legends_firecrawl import cli
    from legends_firecrawl.serp_guard import serp_targets

    env = envelope("clean", urls=[])
    env["tasks"][0]["result"][0]["items"] = [
        {"type": "organic", "rank_group": 3, "url": "https://three.example.com/", "domain": "three.example.com"},
        {"type": "organic", "rank_group": 1, "url": "https://one.example.com/", "domain": "one.example.com"},
        {"type": "organic", "rank_group": 2, "url": "https://two.example.com/", "domain": "two.example.com"},
    ]
    assert serp_targets(env, limit=2)["urls"] == ["https://one.example.com/", "https://two.example.com/"]

    serp_path = tmp_path / "dry.json"
    serp_path.write_text(json.dumps(env), encoding="utf-8")
    res = run_cli("scrape-serp", str(serp_path), "--limit", "2", "--dry-run")
    assert res.returncode == 0
    dry = json.loads(res.stdout)
    assert dry["dry_run"] is True and dry["planned_pages"] == 2

    # Engagement breadcrumb on non-allowlist forum and platform subdomain must NOT short-circuit to homepage.
    forum_env = envelope("clean", urls=[])
    forum_env["tasks"][0]["result"][0]["items"] = [
        {
            "type": "organic",
            "rank_group": 1,
            "url": "https://google.com/goto?url=CAES1",
            "domain": "stackoverflow.com",
            "breadcrumb": "12 answers · 3 years ago",
            "title": "How to cancel tokio task",
        },
        {
            "type": "organic",
            "rank_group": 2,
            "url": "https://google.com/goto?url=CAES2",
            "domain": "old.reddit.com",
            "breadcrumb": "https://old.reddit.com",
            "title": "Thread title",
        },
    ]
    forum_path = tmp_path / "forum.json"
    forum_path.write_text(json.dumps(forum_env), encoding="utf-8")
    seen_shortcircuit = []

    class StubClient:
        def __init__(self, **kw):
            pass

        def resolve_url(self, target, **kw):
            seen_shortcircuit.append((target, kw.get("allow_homepage_shortcircuit")))
            return {
                "success": True,
                "resolved_url": f"https://{target.removeprefix('https://')}/t/1",
                "resolution_method": "search",
                "base_url": f"https://{target.removeprefix('https://')}",
                "path_hint": None,
                "scraped": {"success": True, "data": {"markdown": "ok"}},
            }

    monkeypatch.setattr(cli, "FirecrawlClient", StubClient)
    assert cli.main(["scrape-serp", str(forum_path), "--resolve-goto", "--confirm", "--no-save"]) == 0
    assert seen_shortcircuit == [("stackoverflow.com", False), ("https://old.reddit.com", False)]
