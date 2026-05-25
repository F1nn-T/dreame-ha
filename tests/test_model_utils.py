"""Unit tests for ``custom_components.dreame_mower.model_utils``.

The helper module is pure-Python with zero Home Assistant or third-party
imports, so these tests run in a vanilla Python environment with only
``pytest`` installed.
"""

from __future__ import annotations

import pytest

from custom_components.dreame_mower import model_utils as mu


# ---------------------------------------------------------------------------
# is_supported_model
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "model",
    [
        "dreame.mower.p2255",
        "dreame.mower.g2422",
        "mova.mower.g2408",
        "dreame.vacuum.r2228",
        "mova.vacuum.r2475a",
        "mova.vacuum.r2475h",
        "mova.vacuum.r2475t",
        "mova.vacuum.r9416d",
        "mova.vacuum.r2587a",
    ],
)
def test_is_supported_model_accepts_known_prefixes(model: str) -> None:
    assert mu.is_supported_model(model) is True


@pytest.mark.parametrize(
    "model",
    [
        "",
        None,
        "zhimi.airpurifier.mc1",
        "dreame.fan.r2475a",
        "xiaomi.vacuum.foo",  # legit vacuum but a different brand we don't drive
        "dreame.mowerX.p2255",  # close but missing the trailing dot
        "mova.vacuumr2475a",  # missing the dot — must not match by accident
    ],
)
def test_is_supported_model_rejects_unrelated(model) -> None:
    assert mu.is_supported_model(model) is False


# ---------------------------------------------------------------------------
# normalize_capability_model
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("dreame.mower.p2255", "p2255"),
        ("dreame.vacuum.r2228", "r2228"),
        ("mova.vacuum.r2475a", "r2475a"),
        ("mova.vacuum.r9416d", "r9416d"),
        ("mova.mower.g2408", "g2408"),
        ("xiaomi.vacuum.foo", "foo"),
        # Already-bare model code passes through unchanged.
        ("r2475a", "r2475a"),
    ],
)
def test_normalize_capability_model_strips_segments(raw: str, expected: str) -> None:
    assert mu.normalize_capability_model(raw) == expected


@pytest.mark.parametrize("value", [None, ""])
def test_normalize_capability_model_handles_empty(value) -> None:
    assert mu.normalize_capability_model(value) == ""


def test_normalize_capability_model_mova_vacuum_resolves_against_capability_blob() -> None:
    """The whole point of this helper.

    A MOVA-vacuum model string should normalise to a bare model code shaped
    like the ones used as keys in the bundled ``DREAME_MODEL_CAPABILITIES``
    blob (lowercase, alphanumeric, no dots).
    """
    out = mu.normalize_capability_model("mova.vacuum.r2475a")
    assert "." not in out
    assert out.islower()
    assert out == "r2475a"


# ---------------------------------------------------------------------------
# lookup_model_display_name
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "model, expected_display",
    [
        ("dreame.mower.p2255", "A1"),
        ("dreame.mower.g2422", "A1 Pro"),
        ("mova.vacuum.r2475a", "MOVA P50 Pro Ultra"),
        ("mova.vacuum.r9416d", "MOVA P50 Pro Ultra"),
        ("mova.vacuum.r2587a", "MOVA P50 Pro Ultra"),
    ],
)
def test_lookup_model_display_name_known(model: str, expected_display: str) -> None:
    assert mu.lookup_model_display_name(model) == expected_display


@pytest.mark.parametrize(
    "model",
    [
        "dreame.mower.zzz9999",
        "mova.vacuum.r9999z",
        "",
        None,
    ],
)
def test_lookup_model_display_name_unknown_returns_none(model) -> None:
    assert mu.lookup_model_display_name(model) is None
