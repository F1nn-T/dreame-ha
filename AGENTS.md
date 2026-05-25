# AGENTS.md

## Cursor Cloud specific instructions

This repository is a **Home Assistant custom integration** (HACS-compatible) for controlling Dreame/MOVA robots. It has no standalone entry point, build system, or test suite — it runs as a plugin inside Home Assistant.

### Running the development environment

1. **Start Home Assistant** with the integration symlinked:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   mkdir -p /workspace/ha_config/custom_components
   ln -sf /workspace/custom_components/dreame_mower /workspace/ha_config/custom_components/dreame_mower
   hass --config /workspace/ha_config
   ```
   HA will be available at `http://localhost:8123`. On first run, complete onboarding via the UI or API.

2. **Onboarding via API** (non-interactive):
   ```bash
   # Create user
   curl -X POST http://localhost:8123/api/onboarding/users \
     -H "Content-Type: application/json" \
     -d '{"client_id":"http://localhost:8123/","name":"Dev","username":"dev","password":"devpassword123","language":"en"}'
   # Exchange auth_code for token, then complete core_config + analytics + integration steps
   ```

3. **Verify integration loaded**: check HA logs for `We found a custom integration dreame_mower`.

### Linting

```bash
ruff check custom_components/dreame_mower/
```

The codebase has ~270 pre-existing lint warnings (mostly unused imports, bare exceptions, style). These are from upstream and not blockers.

### Key gotchas

- **No tests exist** in this repository. There is no pytest, tox, or test infrastructure.
- **No `requirements.txt` / `pyproject.toml`** — dependencies are declared only in `custom_components/dreame_mower/manifest.json`.
- **`py-mini-racer`** requires building native code; `python3-dev` and `build-essential` must be installed.
- **`netifaces`** (transitive dep of `python-miio`) also needs C compilation headers.
- **`go2rtc` and `libturbojpeg` errors** in HA logs are benign — they are optional HA components not needed for this integration.
- **Config flow** is the primary way to interact with the integration in development. It can be triggered via `Settings > Devices & Services > Add Integration > Dreame Mower`, or via the REST API at `/api/config/config_entries/flow`.
- **A physical Dreame/MOVA robot** (or cloud account) is needed to complete setup beyond the config flow. Without credentials/device, you can only test up to the credential entry form.
