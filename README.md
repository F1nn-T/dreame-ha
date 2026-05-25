![Logo](https://raw.githubusercontent.com/Tasshack/dreame-vacuum/dev/docs/media/logo.png)

# Dreame/MOVA Home Assistant Integration

[![GitHub Release](https://img.shields.io/github/v/release/F1nn-T/dreame-ha?style=flat-square)](https://github.com/F1nn-T/dreame-ha/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square)](https://hacs.xyz/)

A community fork of [bhuebschen/dreame-mower](https://github.com/bhuebschen/dreame-mower) that extends Dreame/MOVA device support beyond lawn mowers to include **robot vacuum cleaners**.

This integration lets you control Dreame and MOVA robots — mowers and vacuums alike — directly from Home Assistant.

> **Fork goal:** A single integration for all Dreame/MOVA robots. Currently tested with the **MOVA P50 Pro Ultra** robot vacuum. Contributions for other devices are very welcome — see [Contributing](#contributing).

> **Note:** This is a modified version of Tasshack's [dreame-vacuum](https://github.com/Tasshack/dreame-vacuum) integration, adapted first for lawn mowers by bhuebschen, and now extended for robot vacuums. It may still produce some error messages in HA logs.

---

## Features

- Start / Stop / Pause cleaning
- Return to dock
- Zone, segment, and spot cleaning
- Multi-floor map support
- Do Not Disturb scheduling
- Consumable life tracking and resets
- Live map camera entity (cloud mode only)
- Works with both Dreamehome and MOVAhome accounts

---

## Supported Devices

Legend: **✅ Tested** · **🟡 Should work** (same protocol, untested) · **❓ Unknown** · **🚧 In progress**

### Robot Vacuum Cleaners — MOVA

#### P-Series

| Model | MiIO ID | Suction | Mopping | Auto-Empty | Status |
|-------|---------|---------|---------|------------|--------|
| MOVA P50 Pro Ultra | `r2475a/h/t`, `r9416d`, `r2587a` | 19 000 Pa | Dual rotary + auto-wash | Yes (75 °C wash) | ✅ Tested |
| MOVA P50 Ultra | `r2519a` | — | Yes | Yes | 🟡 Should work |
| MOVA P50s Ultra | `r9427h` | — | Yes | Yes | 🟡 Should work |
| MOVA P50 (Standard) | `r9416`, `r94745`, `r94165` | — | Yes | — | 🟡 Should work |
| MOVA P50 Pro | `r9474` | — | Yes | — | 🟡 Should work |
| MOVA P10 Ultra | `r2462a` | — | Dual spinning | Yes | 🟡 Should work |
| MOVA P10 Pro Ultra | `r2491a` | — | Dual spinning + hot wash | Yes | 🟡 Should work |
| MOVA P10 Pro Ultra Gen 2 | `r5730c` | 26 000 Pa | Dual spinning | Yes | 🟡 Should work |
| MOVA P20 Ultra | `r2432b` | — | Yes | Yes | 🟡 Should work |
| MOVA P60 | `r9427`, `r9427x`, `r5747`, `r5730` | — | Yes | — | 🟡 Should work |
| MOVA P60 Pro | `r9482`, `r2535` | — | Yes | — | 🟡 Should work |
| MOVA P70 Pro Ultra | `r590q`, `r5770`, `r5977a/f/g/h` | 30 000 Pa | Yes | Yes | 🟡 Should work |

#### V-Series

| Model | MiIO ID | Suction | Mopping | Auto-Empty | Status |
|-------|---------|---------|---------|------------|--------|
| MOVA V50 Ultra | `r2525a/e/h` | 24 000 Pa | DuoSolution warm-water | Yes | 🟡 Should work |
| MOVA V50 Ultra Complete | `r2582a/c/h/k` | 24 000 Pa | DuoSolution warm-water | Yes (full dock) | 🟡 Should work |
| MOVA V60 MOBIUS | `r2599` | — | Yes | — | 🟡 Should work |

#### Z-Series

| Model | MiIO ID | Suction | Mopping | Auto-Empty | Status |
|-------|---------|---------|---------|------------|--------|
| MOVA Z50 Ultra | `r2430a/u` | — | Yes | Yes | 🟡 Should work |
| MOVA Z60 Pro | `r9473`, `r2561` | — | Yes | Yes | 🟡 Should work |
| MOVA Z60 Ultra Roller Complete | `r9540a/h/k/n/u` | 28 000 Pa | DuoBrush dual rollers + hot wash | Yes | 🟡 Should work |
| MOVA Z70 Pro | `r5766` | — | Yes | Yes | 🟡 Should work |
| MOVA Z70 Ultra Roller Complete | `r5765h` | — | Yes | Yes | 🟡 Should work |

#### S-Series

| Model | MiIO ID | Suction | Mopping | Auto-Empty | Status |
|-------|---------|---------|---------|------------|--------|
| MOVA S10 | — | 7 000 Pa | Vibrating | No | 🟡 Should work |
| MOVA S10 Plus | — | 7 000 Pa | Vibrating | Yes | 🟡 Should work |
| MOVA S20 Ultra | — | 8 300 Pa | Yes | Yes (wash+dry) | 🟡 Should work |
| MOVA S70 Roller | `r5769a/f/g/h/q/t` | 28 000 Pa | DuoBrush rollers + real-time wash | Yes | 🟡 Should work |
| MOVA S70 Ultra Roller | `r5770a/g/h/t`, `r590qf` | — | HydroForce real-time wash | Yes | 🟡 Should work |

#### E-Series

| Model | MiIO ID | Suction | Mopping | Auto-Empty | Status |
|-------|---------|---------|---------|------------|--------|
| MOVA E20 Plus | — | 5 000 Pa | Flat pad + mop lift | — | 🟡 Should work |
| MOVA E20s Pro | `r2569c` | — | Yes | — | 🟡 Should work |
| MOVA E30 Pro | `r2533h` | 19 000 Pa | Flat pad | — | 🟡 Should work |
| MOVA E30 Pro Ultra | `r95046` | — | Yes + auto-wash | Yes | 🟡 Should work |
| MOVA E40 Ultra | `r9504a`, `r5732a` | 19 000 Pa | Dual spinning | Yes | 🟡 Should work |

#### Concept / Upcoming (not yet supported)

| Model | Type | Notes | Status |
|-------|------|-------|--------|
| MOVA Mobius 60 | Vacuum + mop | 30 000 Pa, MopSwap 3-pad system, 100 °C mop wash | 🚧 In progress |
| MOVA Sirius 60 | Vacuum + robot arms | IFA 2025 concept, extendable sweep/grab arms | ❓ Unknown |
| MOVA Zeus 60 | Vacuum | Stair-climbing, 25 cm step height | ❓ Unknown |

---

### Robot Lawn Mowers — MOVA

| Model | Coverage | Navigation | Slope | Status |
|-------|----------|------------|-------|--------|
| MOVA ViAX 250 | 250 m² | Dual-camera AI (UltraEyes 1.0), wire-free | 40 % | 🟡 Should work |
| MOVA ViAX 300 | 300 m² | Dual-camera AI (UltraEyes 1.0), wire-free | 40 % | 🟡 Should work |
| MOVA ViAX 500 | 500 m² | Dual-camera + 360° LiDAR (UltraEyes 2.0) | 40 % | 🟡 Should work |
| MOVA LiDAX Ultra 800 | 800 m² | 360° 3D LiDAR + AI Vision | 45 % | 🟡 Should work |
| MOVA LiDAX Ultra 1000 | 1 000 m² | 360° 3D LiDAR + AI Vision | 45 % | 🟡 Should work |
| MOVA LiDAX Ultra 1200 | 1 200 m² | 360° 3D LiDAR + AI Vision | 45 % | 🟡 Should work |
| MOVA LiDAX Ultra 1600 | 1 600 m² | 360° 3D LiDAR + AI Vision + 4G | 45 % | 🟡 Should work |
| MOVA LiDAX Ultra 2000 | 2 000 m² | 360° 3D LiDAR + AI Vision + 4G | 45 % | 🟡 Should work |
| MOVA LiDAX Ultra 3000 AWD | ~3 000 m² | UltraView 3.0 + Dual AI Vision, AWD | 80 % | 🟡 Should work |

> **Mower note:** Mower support comes from the original [bhuebschen/dreame-mower](https://github.com/bhuebschen/dreame-mower) fork. Current features are limited to start/stop/dock. Additional mower features (zone mowing, scheduling, blade stats) are under active development.

---

### Your device is missing?

If your MOVA robot is not listed, it very likely still works — there are dozens of model variants sharing the same MIoT protocol. Please open an issue with your model name and MiIO ID (visible in the MOVAhome app under device info). See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Installation

### HACS (Recommended)

1. Ensure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=F1nn-T&repository=dreame-ha&category=integration)

— or —

2. Add this repository as a custom repository in HACS:
   - Open HACS in Home Assistant.
   - Go to **Integrations**.
   - Click the three dots in the top-right corner and select **Custom repositories**.
   - Add the following URL: `https://github.com/F1nn-T/dreame-ha`
   - Select **Integration** as the category.
3. Search for "Dreame" or "MOVA" in the HACS integrations list and install it.

### Manual Installation

1. Download the latest release from the [GitHub Releases page](https://github.com/F1nn-T/dreame-ha/releases).
2. Extract the downloaded archive.
3. Copy the `custom_components/dreame_mower` folder to your Home Assistant `custom_components` directory.
   - Example: `/config/custom_components/dreame_mower`
4. Restart Home Assistant.

---

## Configuration

<a href="https://my.home-assistant.io/redirect/config_flow_start/?domain=dreame_mower" target="_blank"><img src="https://my.home-assistant.io/badges/config_flow_start.svg" alt="Open your Home Assistant instance and start setting up a new integration." /></a>

— or —

1. In Home Assistant, navigate to **Settings** → **Devices & Services**.
2. Click **Add Integration**.
3. Search for "Dreame Mower" and select it.
4. Choose your account type:
   - **Dreame Cloud** — if your device is set up in the Dreamehome app
   - **MOVA Cloud** — if your device is set up in the MOVAhome app *(most MOVA users)*
   - **Local** — if you want to skip the cloud (requires device IP + token; no maps)
5. Enter your credentials and select the correct region (e.g., Europe for EU accounts).
6. Complete the setup.

---

## Troubleshooting

- **"No compatible devices found"** — double-check the region matches where your account was created.
- **MOVA device not found with Dreame credentials** — the MOVAhome and Dreamehome cloud backends are separate. Select "MOVA Cloud" as the account type.
- **Map not available** — maps require cloud mode; they are not supported in local mode.
- **Cliff sensor aborts** — reduce carpet sensitivity in the integration settings.
- Check Home Assistant logs for errors tagged `dreame_mower`.
- If your specific model variant is not working, open an issue with your model name and MiIO ID.

---

## Technical Reference

For a deep dive into the communication protocol, full MIoT property/action tables, MOVA P50 Pro Ultra device profile, and Home Assistant integration architecture, see [docs/TECHNICAL_REFERENCE.md](docs/TECHNICAL_REFERENCE.md).

---

## Contributing

Contributions are very welcome, especially for adding support for more Dreame/MOVA devices!

- Fork this repository and open a pull request against the `main` branch.
- If you're adding a new device, include the device model and describe what changes were needed.
- See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Credits & Thanks

- [Tasshack](https://github.com/Tasshack) — original dreame-vacuum integration
- [bhuebschen](https://github.com/bhuebschen) — dreame-mower fork this is based on
- [Laurentiu Tanase](https://github.com/larieu)
- [Josef Kyrian](https://github.com/josef-kyrian)
- [Anton Daubert](https://github.com/antondaubert)
- [Loïc](https://github.com/zoic21)
