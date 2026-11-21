from __future__ import annotations

import json
from pathlib import Path

import legends_firecrawl


ROOT = Path(__file__).resolve().parents[1]


def test_version_consistency():
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    routes = json.loads((ROOT / "python" / "legends_firecrawl" / "routes.json").read_text(encoding="utf-8"))
    assert version == legends_firecrawl.__version__ == routes["version"]


def test_release_builder_is_allowlisted():
    import importlib.util

    text = (ROOT / "scripts" / "build_release.py").read_text(encoding="utf-8")
    assert "ALLOW_FILES" in text and "ALLOW_DIRS" in text
    for excluded in ("var", ".git", "dist"):
        assert f'"{excluded}"' not in text.split("ALLOW_DIRS", 1)[1].split("}", 1)[0]

    spec = importlib.util.spec_from_file_location("build_release", ROOT / "scripts" / "build_release.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    included = {p.relative_to(ROOT).as_posix() for p in mod.included_files()}
    for required in ("LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md", "MANIFEST.in", "SECURITY.md", "CONTRIBUTING.md", "CITATION.cff"):
        assert required in included


def test_secret_files_are_not_in_source_package():
    assert not (ROOT / ".env").exists()
    assert not any(path.name.lower().endswith("credentials.json") for path in ROOT.rglob("*"))
