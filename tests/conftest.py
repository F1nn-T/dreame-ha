"""Shared pytest fixtures for the dreame_mower test suite.

The integration code lives under ``custom_components/dreame_mower/`` which is
not normally on ``sys.path`` — Home Assistant adds it at runtime. For the
tests to import it directly, we prepend the repo root.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
