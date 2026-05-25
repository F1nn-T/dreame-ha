"""Regression guard for the compressed JSON blobs in ``dreame/const.py``.

We intentionally do **not** ``import`` the const module — that would transitively
import ``dreame.protocol`` (which pulls in ``requests``, ``paho-mqtt``,
``pycryptodome``, ``python-miio``...). Instead the blobs are extracted from
the source file with a regex and decoded standalone. That keeps the test
suite's only dependency ``pytest``.
"""

from __future__ import annotations

import base64
import json
import re
import zlib
from pathlib import Path

import pytest

CONST_PATH = (
    Path(__file__).resolve().parent.parent
    / "custom_components"
    / "dreame_mower"
    / "dreame"
    / "const.py"
)


def _extract_blob(name: str) -> str:
    """Read ``const.py`` and return the base64 string assigned to ``name``."""
    source = CONST_PATH.read_text(encoding="utf-8")
    match = re.search(
        rf'{re.escape(name)}\s*:\s*Final\s*=\s*"([^"]+)"',
        source,
    )
    assert match is not None, f"could not find {name} blob in const.py"
    return match.group(1)


def _decode(blob: str) -> dict:
    return json.loads(zlib.decompress(base64.b64decode(blob), zlib.MAX_WBITS | 32))


# ---------------------------------------------------------------------------
# DREAME_MODEL_CAPABILITIES
# ---------------------------------------------------------------------------


def test_capabilities_blob_decodes_to_dict() -> None:
    data = _decode(_extract_blob("DREAME_MODEL_CAPABILITIES"))
    assert isinstance(data, dict)
    # The bundled blob has hundreds of model entries today. If somebody
    # accidentally shrinks it to a handful, fail loudly.
    assert len(data) > 100, f"capability blob unexpectedly small ({len(data)} entries)"


@pytest.mark.parametrize("known_model", ["r2104", "r2228", "p2259"])
def test_capabilities_blob_contains_known_dreame_models(known_model: str) -> None:
    """A handful of well-known Dreame model codes should always be present."""
    data = _decode(_extract_blob("DREAME_MODEL_CAPABILITIES"))
    assert known_model in data, f"expected {known_model!r} in capability blob"


def test_capability_entries_are_lists_or_aliases() -> None:
    """Each value is either a list of [cap_id, min_fw] pairs or a string alias.

    ``device.py`` follows string values to their target entry, so anything
    else would crash the capability lookup at runtime.
    """
    data = _decode(_extract_blob("DREAME_MODEL_CAPABILITIES"))
    for model, value in data.items():
        assert isinstance(value, (list, str)), (
            f"capability entry for {model!r} has unexpected type {type(value).__name__}"
        )


# ---------------------------------------------------------------------------
# DEVICE_KEY (per-model AES IV lookup)
# ---------------------------------------------------------------------------


def test_device_key_blob_decodes_to_dict_of_lists() -> None:
    data = _decode(_extract_blob("DEVICE_KEY"))
    assert isinstance(data, dict)
    assert data, "DEVICE_KEY blob is empty"
    for key, models in data.items():
        assert isinstance(key, str) and len(key) > 0
        assert isinstance(models, list), (
            f"DEVICE_KEY value for {key!r} is not a list (got {type(models).__name__})"
        )
        for model in models:
            assert isinstance(model, str) and model, (
                f"DEVICE_KEY[{key!r}] contains a non-string / empty model entry: {model!r}"
            )
