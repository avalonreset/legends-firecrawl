from __future__ import annotations

from pathlib import Path

from legends_firecrawl import packet_compat


class FakeClient:
    def __init__(self):
        self.calls = []

    def scrape(self, url, **kwargs):
        self.calls.append(("scrape", url, kwargs))
        return {"success": True}

    def map_site(self, url, **kwargs):
        self.calls.append(("map", url, kwargs))
        return {"success": True, "links": []}


def test_packet_scrape_uses_markdown_and_links():
    fake = FakeClient()
    packet_compat.scrape_page("https://example.com", client=fake)  # type: ignore[arg-type]
    assert fake.calls[0][2]["formats"] == ["markdown", "links"]


def test_packet_map_is_bounded():
    fake = FakeClient()
    packet_compat.discover_site_pages("https://example.com", client=fake, limit=50)  # type: ignore[arg-type]
    assert fake.calls[0][2]["limit"] == 50


def test_evidence_writer_creates_parent(tmp_path: Path):
    target = tmp_path / "nested" / "page.md"
    packet_compat.write_text_evidence(target, "evidence")
    assert target.read_text(encoding="utf-8") == "evidence"
