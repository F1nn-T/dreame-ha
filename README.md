![Logo](https://raw.githubusercontent.com/Tasshack/dreame-vacuum/dev/docs/media/logo.png)

# Dreame/MOVA Home Assistant Integration

[![GitHub Release](https://img.shields.io/github/v/release/F1nn-T/dreame-ha?style=flat-square)](https://github.com/F1nn-T/dreame-ha/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square)](https://hacs.xyz/)

A community fork of [bhuebschen/dreame-mower](https://github.com/bhuebschen/dreame-mower) that extends Dreame/MOVA device support beyond lawn mowers to include **robot vacuum cleaners**.

This integration lets you control Dreame and MOVA robots — mowers and vacuums alike — directly from Home Assistant.

> **Fork goal:** A single integration for all Dreame/MOVA robots. Currently tested with the **MOVA P50 Pro Ultra** robot vacuum. Contributions for other devices are very welcome — see [Contributing](#contributing).

---

## Supported Devices

| Device | Type | Status |
|--------|------|--------|
| Dreame / MOVA lawn mowers | Mower | Supported (upstream) |
| MOVA P50 Pro Ultra | Robot Vacuum | Tested |
| Other Dreame/MOVA robots | Mower / Vacuum | Community contributions welcome |

---

## Features

- Start/Stop mowing or vacuuming
- Send robot back to dock
- Works with both Dreamehome and MOVAhome accounts

> **Note:** This is a modified version of Tasshack's [dreame-vacuum](https://github.com/Tasshack/dreame-vacuum) integration, adapted first for lawn mowers by bhuebschen, and now extended for robot vacuums. It may still produce some error messages in HA logs — contributions to improve stability are appreciated.

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

1. In Home Assistant, navigate to **Settings** > **Devices & Services**.
2. Click **Add Integration**.
3. Search for "Dreame Mower" and select it.
4. Enter the credentials from your Dreamehome/MOVAhome app.
5. Complete the setup process.

---

## Troubleshooting

- Ensure your Dreamehome/MOVAhome account credentials are correct.
- Check the Home Assistant logs for any errors related to `dreame_mower`.
- If your device is not working, open an issue and include your device model — it may just need a small mapping addition.

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
