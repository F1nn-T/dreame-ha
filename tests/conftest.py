"""Shared pytest fixtures for the dreame_mower test suite.

The integration's ``__init__.py`` imports Home Assistant at top level, so we
cannot ``import custom_components.dreame_mower`` directly in a vanilla Python
environment. Instead we register lightweight stub parent packages in
``sys.modules`` and load only the leaf modules we want to test (e.g.
``model_utils``) directly from their file paths. This keeps the test suite's
single dependency ``pytest``.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INTEGRATION_ROOT = REPO_ROOT / "custom_components" / "dreame_mower"


def _ensure_stub_package(name: str, path: Path) -> types.ModuleType:
    """Register ``name`` in ``sys.modules`` as a namespace-only package.

    Re-uses an existing module if one is already present (e.g. if the real
    integration was imported elsewhere in the test session).
    """
    if name in sys.modules:
        return sys.modules[name]
    module = types.ModuleType(name)
    module.__path__ = [str(path)]  # makes Python treat it as a package
    sys.modules[name] = module
    return module


def _load_submodule(package: str, sub: str, path: Path) -> types.ModuleType:
    """Load ``path`` as ``f"{package}.{sub}"`` without executing the parent
    package's ``__init__.py``."""
    full = f"{package}.{sub}"
    if full in sys.modules:
        return sys.modules[full]
    spec = importlib.util.spec_from_file_location(full, path)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError(f"could not load {full} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[full] = module
    spec.loader.exec_module(module)
    return module


# Register stub parent packages so ``custom_components.dreame_mower.X``
# import paths resolve without executing the real ``__init__.py``s.
_ensure_stub_package(
    "custom_components", REPO_ROOT / "custom_components"
)
_ensure_stub_package(
    "custom_components.dreame_mower", INTEGRATION_ROOT
)

# Pre-load the helper module(s) the tests care about. Doing this here means
# individual test files can ``from custom_components.dreame_mower import
# model_utils`` exactly as they would in production code.
_load_submodule(
    "custom_components.dreame_mower",
    "model_utils",
    INTEGRATION_ROOT / "model_utils.py",
)
