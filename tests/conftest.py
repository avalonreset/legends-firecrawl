from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON_ROOT = ROOT / "python"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

# macOS commonly exposes /var as a symlink. Tests use the canonical test-owned
# directory so production linked-path refusal remains strict and unchanged.
import pytest
@pytest.fixture
def tmp_path(tmp_path):
    return tmp_path.resolve()
