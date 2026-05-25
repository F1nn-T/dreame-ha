"""Helpers for recognising and normalising Dreame/MOVA model strings.

These helpers are intentionally pure-Python and have no Home Assistant or
third-party imports. That means a plain ``pytest`` run can exercise them
without spinning up the Home Assistant runtime.

Two responsibilities live here:

* :func:`is_supported_model` — used by ``config_flow`` to decide whether the
  device the user is trying to add is one this integration knows how to drive.
* :func:`normalize_capability_model` — used by
  :class:`~custom_components.dreame_mower.dreame.types.DreameMowerDeviceCapability`
  to translate a full MIoT model string (e.g. ``mova.vacuum.r2475a``) into the
  bare model code (e.g. ``r2475a``) used as a key in the bundled
  ``DREAME_MODEL_CAPABILITIES`` blob.

A small :data:`MODEL_DISPLAY_NAMES` map provides friendly names for the
device picker UI. Devices that are not in the map still work; their raw model
string is shown instead.
"""

from __future__ import annotations

from typing import Final

# Recognised model-string prefixes. A model is supported if it starts with one
# of these. Order does not matter.
SUPPORTED_MODEL_PREFIXES: Final[tuple[str, ...]] = (
    "dreame.mower.",
    "mova.mower.",
    "dreame.vacuum.",
    "mova.vacuum.",
)

# Optional friendly display names. Used only by the device-picker UI in
# ``config_flow``; the integration still works if a model is absent here.
MODEL_DISPLAY_NAMES: Final[dict[str, str]] = {
    # ---- Mowers ------------------------------------------------------------
    "dreame.mower.p2255": "A1",
    "dreame.mower.g2422": "A1 Pro",
    "dreame.mower.g2408": "A2",
    "dreame.mower.g3255": "unknown",
    # ---- MOVA P50 Pro Ultra family ----------------------------------------
    # Same hardware, regional / SKU variants. The model code is what the
    # device reports over MIoT.
    "mova.vacuum.r2475a": "MOVA P50 Pro Ultra",
    "mova.vacuum.r2475h": "MOVA P50 Pro Ultra",
    "mova.vacuum.r2475t": "MOVA P50 Pro Ultra",
    "mova.vacuum.r9416d": "MOVA P50 Pro Ultra",
    "mova.vacuum.r2587a": "MOVA P50 Pro Ultra",
}

# Segments to strip when turning a full model string into the bare model code
# used as a key in the ``DREAME_MODEL_CAPABILITIES`` blob.
_NORMALIZE_STRIP_SEGMENTS: Final[tuple[str, ...]] = (
    "mower.",
    "vacuum.",
    "dreame.",
    "mova.",
    "xiaomi.",
)


def is_supported_model(model: str | None) -> bool:
    """Return ``True`` if ``model`` is a MIoT model this integration drives.

    Any model whose name starts with one of :data:`SUPPORTED_MODEL_PREFIXES`
    is accepted. Empty / ``None`` strings are rejected.
    """
    if not model:
        return False
    return any(model.startswith(prefix) for prefix in SUPPORTED_MODEL_PREFIXES)


def normalize_capability_model(model: str | None) -> str:
    """Strip vendor/kind segments to leave the bare model code.

    Examples
    --------
    >>> normalize_capability_model("mova.vacuum.r2475a")
    'r2475a'
    >>> normalize_capability_model("dreame.mower.p2255")
    'p2255'
    >>> normalize_capability_model("xiaomi.vacuum.foo")
    'foo'
    >>> normalize_capability_model(None)
    ''
    """
    if not model:
        return ""
    out = model
    for segment in _NORMALIZE_STRIP_SEGMENTS:
        out = out.replace(segment, "")
    return out


def lookup_model_display_name(model: str | None) -> str | None:
    """Return the friendly display name for ``model``, or ``None``.

    Unknown models return ``None``; callers should fall back to the raw model
    string in that case (the device picker still needs *something* to show).
    """
    if not model:
        return None
    return MODEL_DISPLAY_NAMES.get(model)
