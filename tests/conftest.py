from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


@pytest.fixture
def t1_tiny_path() -> Path:
    return FIXTURES / "t1_tiny.json"
