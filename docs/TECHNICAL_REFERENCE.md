# Technical Reference — Dreame/MOVA Home Assistant Integration

This document covers how the integration communicates with Dreame/MOVA robots, the full MIoT property/action map, MOVA P50 Pro Ultra specifics, and how it all maps onto Home Assistant concepts.

---

## Table of Contents

1. [Communication Architecture](#1-communication-architecture)
2. [MIoT Property Mapping](#2-miot-property-mapping)
3. [MIoT Action Mapping](#3-miot-action-mapping)
4. [MOVA P50 Pro Ultra — Device Profile](#4-mova-p50-pro-ultra--device-profile)
5. [Home Assistant Integration Architecture](#5-home-assistant-integration-architecture)
6. [Known Quirks & Limitations](#6-known-quirks--limitations)

---

## 1. Communication Architecture

### 1.1 Three Transport Layers

The integration supports three communication paths, selected at setup time:

| # | Transport | When to use |
|---|-----------|-------------|
| 1 | **Dreame/MOVA Cloud + MQTT** | Default for most users; requires internet |
| 2 | **Local miIO (UDP)** | No cloud needed; requires device IP + 32-char token; maps unavailable |
| 3 | **Mova Cloud + MQTT** | Same as Dreame Cloud but for MOVAhome app accounts |

#### Cloud + MQTT flow

```
HA → HTTP REST → Dreame/MOVA cloud API → (relays to device)
Device state change → MQTT → Dreame/MOVA cloud → paho-mqtt client → HA
```

- Authentication: username + password → OAuth tokens (regional endpoints: cn, eu, us, ru, sg)
- Encryption: ARC4 cipher (`pycryptodome`) on MQTT payloads
- MQTT topic pattern: `/{key}/{device_id}/{uid}/{model}/{country}/`

#### Local miIO flow

```
HA → UDP port 54321 → device (python-miio library)
```

- Requires the device's local IP and a 32-hex-character token
- No map data, no cloud features

### 1.2 Key Source Files

| File | Role |
|------|------|
| `dreame/protocol.py` | HTTP REST client, MQTT client, local miIO client |
| `dreame/device.py` | All device logic, property cache, state machine (~5 400 lines) |
| `coordinator.py` | HA `DataUpdateCoordinator` — wires polling into HA lifecycle |
| `config_flow.py` | HA UI wizard for credential entry and account type selection |

### 1.3 Polling vs Push

| Mechanism | Interval | Trigger |
|-----------|----------|---------|
| **Periodic poll** | ~10 s (3 s while cleaning) | `coordinator._async_update_data()` |
| **MQTT push** | Immediate | Device-initiated state change relayed through cloud |

After any command is issued, the device's in-memory state is updated optimistically. If the device does not confirm within 5 s ("dirty data window"), the optimistic value is discarded and the polled value wins.

---

## 2. MIoT Property Mapping

All properties use the MIoT `siid` (service ID) / `piid` (property ID) addressing scheme. The table below reflects the actual mappings in `dreame/types.py`.

### Service 2 — Device State

| Property | siid | piid | Access | Description |
|----------|------|------|--------|-------------|
| `STATE` | 2 | 1 | R | Operational state enum (idle, cleaning, returning, charging…) |
| `ERROR` | 2 | 2 | R | Error code (117 defined codes) |

### Service 3 — Battery / Charging

| Property | siid | piid | Access | Description |
|----------|------|------|--------|-------------|
| `BATTERY_LEVEL` | 3 | 1 | R | 0–100 % |
| `CHARGING_STATUS` | 3 | 2 | R | Charging state enum |
| `OFF_PEAK_CHARGING` | 3 | 3 | R/W | Off-peak charge scheduling on/off |

### Service 4 — Cleaning / Task Control

| Property | siid | piid | Access | Description |
|----------|------|------|--------|-------------|
| `STATUS` | 4 | 1 | R | Operational status (standby, sweeping, mopping, docked…) |
| `CLEANING_TIME` | 4 | 2 | R | Current session duration (minutes) |
| `CLEANED_AREA` | 4 | 3 | R | Current session area (m²) |
| `TASK_STATUS` | 4 | 7 | R | Task type (auto, zone, segment, spot…) |
| `CLEANING_START_TIME` | 4 | 8 | R | Unix timestamp of session start |
| `CLEAN_LOG_FILE_NAME` | 4 | 9 | R | Cloud filename for cleaning log |
| `CLEANING_PROPERTIES` | 4 | 10 | R/W | JSON blob: suction, water, mop settings |
| `RESUME_CLEANING` | 4 | 11 | R/W | Auto-resume on recharge on/off |
| `CLEAN_LOG_STATUS` | 4 | 13 | R | Log upload status |
| `SERIAL_NUMBER` | 4 | 14 | R | Device serial number |
| `REMOTE_CONTROL` | 4 | 15 | R/W | Manual drive mode payload |
| `CLEANING_PAUSED` | 4 | 17 | R | Whether task is currently paused |
| `FAULTS` | 4 | 18 | R | Bitfield of active faults |
| `NATION_MATCHED` | 4 | 19 | R | Region match flag |
| `RELOCATION_STATUS` | 4 | 20 | R | LiDAR relocation state |
| `OBSTACLE_AVOIDANCE` | 4 | 21 | R/W | Obstacle avoidance level |
| `AI_DETECTION` | 4 | 22 | R/W | AI object detection settings (JSON) |
| `CLEANING_MODE` | 4 | 23 | R/W | Mode enum (vacuum only / mop only / both) |
| `UPLOAD_MAP` | 4 | 24 | W | Trigger map upload |
| `CUSTOMIZED_CLEANING` | 4 | 26 | R/W | Per-room cleaning settings (JSON) |
| `CHILD_LOCK` | 4 | 27 | R/W | Physical button lock on/off |
| `CLEANING_CANCEL` | 4 | 30 | R/W | Cancel current task |
| `Y_CLEAN` | 4 | 31 | R/W | Y-mopping pattern on/off |
| `WARN_STATUS` | 4 | 35 | R | Warning code |
| `CAPABILITY` | 4 | 38 | R | Device capability bitmask |
| `MAP_INDEX` | 4 | 42 | R | Currently active floor map index |
| `MAP_NAME` | 4 | 43 | R | Name of active floor map |
| `CRUISE_TYPE` | 4 | 44 | R/W | Patrol route type |
| `SCHEDULED_CLEAN` | 4 | 47 | R/W | Scheduled cleaning config (JSON) |
| `SHORTCUTS` | 4 | 48 | R/W | Shortcut tasks (JSON) |
| `INTELLIGENT_RECOGNITION` | 4 | 49 | R/W | AI room recognition on/off |
| `LENSBRUSH_LEFT` | 4 | 50 | R | Lens brush life remaining % |
| `NUMERIC_MESSAGE_PROMPT` | 4 | 56 | R | Numeric prompt code |
| `MESSAGE_PROMPT` | 4 | 57 | R | String prompt message |
| `TASK_TYPE` | 4 | 58 | R | Current task type enum |
| `PET_DETECTIVE` | 4 | 59 | R/W | Pet waste detection on/off |
| `BACK_CLEAN_MODE` | 4 | 62 | R/W | Back-area cleaning mode |
| `CLEANING_PROGRESS` | 4 | 63 | R | Cleaning progress 0–100 % |
| `DEVICE_CAPABILITY` | 4 | 83 | R | Extended capability flags |

### Service 5 — Do Not Disturb

| Property | siid | piid | Access | Description |
|----------|------|------|--------|-------------|
| `DND` | 5 | 1 | R/W | DND on/off |
| `DND_START` | 5 | 2 | R/W | DND start time (HH:MM) |
| `DND_END` | 5 | 3 | R/W | DND end time (HH:MM) |
| `DND_TASK` | 5 | 4 | R/W | DND task config |

### Service 6 — Map Data

| Property | siid | piid | Access | Description |
|----------|------|------|--------|-------------|
| `MAP_DATA` | 6 | 1 | R | Rendered map frame (base64-compressed) |
| `FRAME_INFO` | 6 | 2 | R | Frame metadata (I-frame vs P-frame) |
| `OBJECT_NAME` | 6 | 3 | R | Cloud object name for map file |
| `MAP_EXTEND_DATA` | 6 | 4 | R/W | Extended map payload (obstacles, zones, walls) |
| `ROBOT_TIME` | 6 | 5 | R | Device clock timestamp |
| `RESULT_CODE` | 6 | 6 | R | Last map operation result |
| `MULTI_FLOOR_MAP` | 6 | 7 | R/W | Multi-floor mode on/off |
| `MAP_LIST` | 6 | 8 | R | Saved floor map list |
| `RECOVERY_MAP_LIST` | 6 | 9 | R | Recoverable map list |
| `MAP_RECOVERY` | 6 | 10 | W | Trigger map recovery |
| `MAP_RECOVERY_STATUS` | 6 | 11 | R | Recovery operation status |
| `OLD_MAP_DATA` | 6 | 13 | R | Previous map frame |
| `MAP_BACKUP_STATUS` | 6 | 14 | R | Cloud backup status |
| `WIFI_MAP` | 6 | 15 | R/W | Wi-Fi signal strength map |

### Service 7 — Audio / Voice

| Property | siid | piid | Access | Description |
|----------|------|------|--------|-------------|
| `VOLUME` | 7 | 1 | R/W | Speaker volume 0–100 |
| `VOICE_PACKET_ID` | 7 | 2 | R/W | Active voice pack ID |
| `VOICE_CHANGE_STATUS` | 7 | 3 | R | Voice pack install status |
| `VOICE_CHANGE` | 7 | 4 | W | Trigger voice pack change |
| `VOICE_ASSISTANT` | 7 | 5 | R/W | Built-in voice assistant on/off |
| `EMPTY_STAMP` | 7 | 6 | R | Last auto-empty timestamp |
| `CURRENT_CITY` | 7 | 7 | R/W | City for weather voice |
| `VOICE_TEST` | 7 | 9 | W | Play test sound |
| `VOICE_ASSISTANT_LANGUAGE` | 7 | 10 | R/W | Voice assistant language |
| `LISTEN_LANGUAGE` | 7 | 10 | R/W | Wake-word language (same piid as above) |

### Service 8 — Schedule / Timezone

| Property | siid | piid | Access | Description |
|----------|------|------|--------|-------------|
| `TIMEZONE` | 8 | 1 | R/W | IANA timezone string |
| `SCHEDULE` | 8 | 2 | R/W | Cleaning schedule config (JSON) |
| `SCHEDULE_ID` | 8 | 3 | R | Active schedule ID |
| `SCHEDULE_CANCEL_REASON` | 8 | 4 | R | Why last schedule was skipped |
| `CRUISE_SCHEDULE` | 8 | 5 | R/W | Patrol schedule config |

### Services 9–19 — Consumables

| Property | siid | piid | Description |
|----------|------|------|-------------|
| `BLADES_TIME_LEFT` | 9 | 1 | Main brush / blades remaining hours |
| `BLADES_LEFT` | 9 | 2 | Main brush life % |
| `SIDE_BRUSH_TIME_LEFT` | 10 | 1 | Side brush remaining hours |
| `SIDE_BRUSH_LEFT` | 10 | 2 | Side brush life % |
| `FILTER_LEFT` | 11 | 1 | Filter life % |
| `FILTER_TIME_LEFT` | 11 | 2 | Filter remaining hours |
| `FIRST_CLEANING_DATE` | 12 | 1 | Unix timestamp of first ever clean |
| `TOTAL_CLEANING_TIME` | 12 | 2 | Lifetime cleaning hours |
| `CLEANING_COUNT` | 12 | 3 | Lifetime cleaning sessions |
| `TOTAL_CLEANED_AREA` | 12 | 4 | Lifetime cleaned area (m²) |
| `TOTAL_RUNTIME` | 12 | 5 | Total device runtime |
| `TOTAL_CRUISE_TIME` | 12 | 6 | Lifetime patrol time |
| `MAP_SAVING` | 13 | 1 | Map auto-save on/off |
| `SENSOR_DIRTY_LEFT` | 16 | 1 | Cliff/wall sensor life % |
| `SENSOR_DIRTY_TIME_LEFT` | 16 | 2 | Sensor remaining hours |
| `TANK_FILTER_LEFT` | 17 | 1 | Water tank filter life % |
| `TANK_FILTER_TIME_LEFT` | 17 | 2 | Tank filter remaining hours |
| `SILVER_ION_TIME_LEFT` | 19 | 1 | Silver-ion steriliser remaining hours |
| `SILVER_ION_LEFT` | 19 | 2 | Silver-ion life % |

### Services 24–28 — Additional Consumables & Status

| Property | siid | piid | Description |
|----------|------|------|-------------|
| `SQUEEGEE_LEFT` | 24 | 1 | Squeegee life % |
| `SQUEEGEE_TIME_LEFT` | 24 | 2 | Squeegee remaining hours |
| `LENSBRUSH_STATUS` | 27 | 4 | Lens brush status |
| `AI_MAP_OPTIMIZATION_STATUS` | 27 | 7 | AI map optimisation running |
| `SECOND_CLEANING_STATUS` | 27 | 8 | Second-pass cleaning status |
| `ADD_CLEANING_AREA_STATUS` | 27 | 10 | Add-area operation status |
| `ADD_CLEANING_AREA_RESULT` | 27 | 11 | Add-area result code |
| `CLEAN_EFFICIENCY` | 28 | 9 | Cleaning efficiency metric |

### Service 99 — Factory / Debug

| Property | siid | piid | Description |
|----------|------|------|-------------|
| `FACTORY_TEST_STATUS` | 99 | 1 | Factory test state |
| `FACTORY_TEST_RESULT` | 99 | 3 | Factory test result |
| `SELF_TEST_STATUS` | 99 | 8 | Self-test state |
| `LSD_TEST_STATUS` | 99 | 9 | LiDAR self-test state |
| `DEBUG_SWITCH` | 99 | 11 | Debug logging on/off |
| `SERIAL` | 99 | 14 | Device serial (alternate) |
| `CALIBRATION_STATUS` | 99 | 15 | Calibration state |
| `VERSION` | 99 | 17 | Firmware version string |
| `PERFORMANCE_SWITCH` | 99 | 24 | Performance mode on/off |
| `AI_TEST_STATUS` | 99 | 25 | AI subsystem test state |
| `PUBLIC_KEY` | 99 | 27 | Device public key |
| `AUTO_PAIR` | 99 | 28 | Auto-pair mode on/off |
| `MCU_VERSION` | 99 | 31 | MCU firmware version |
| `PLATFORM_NETWORK` | 99 | 95 | Network platform info |

### Service 10001 — Camera / Stream

| Property | siid | piid | Description |
|----------|------|------|-------------|
| `STREAM_STATUS` | 10001 | 1 | Live stream state |
| `STREAM_AUDIO` | 10001 | 2 | Audio stream on/off |
| `STREAM_RECORD` | 10001 | 4 | Recording on/off |
| `TAKE_PHOTO` | 10001 | 5 | Trigger single photo |
| `STREAM_KEEP_ALIVE` | 10001 | 6 | Keep-alive heartbeat |
| `STREAM_FAULT` | 10001 | 7 | Stream error code |
| `CAMERA_LIGHT_BRIGHTNESS` | 10001 | 9 | Spotlight brightness |
| `CAMERA_LIGHT` | 10001 | 10 | Spotlight on/off |
| `STREAM_CRUISE_POINT` | 10001 | 101 | Patrol waypoint for stream |
| `STEAM_HUMAN_FOLLOW` | 10001 | 110 | Person-following mode |
| `STREAM_PROPERTY` | 10001 | 99 | Stream property bundle |
| `STREAM_TASK` | 10001 | 103 | Stream task config |
| `STREAM_UPLOAD` | 10001 | 1003 | Upload stream to cloud |
| `STREAM_CODE` | 10001 | 1100 | Stream access code |
| `STREAM_SET_CODE` | 10001 | 1101 | Set stream access code |
| `STREAM_VERIFY_CODE` | 10001 | 1102 | Verify stream code |
| `STREAM_RESET_CODE` | 10001 | 1103 | Reset stream code |
| `STREAM_SPACE` | 10001 | 2003 | Cloud storage used |

---

## 3. MIoT Action Mapping

Actions use `siid` / `aiid` (action ID) addressing.

### Cleaning Control (siid 5)

| Action | siid | aiid | Description |
|--------|------|------|-------------|
| `START_MOWING` | 5 | 1 | Start or resume cleaning |
| `STOP` | 5 | 2 | Stop task (stay in place) |
| `DOCK` | 5 | 3 | Return to dock |
| `PAUSE` | 5 | 4 | Pause current task |
| `PULL_STATUS` | 5 | 10 | Force device to push full status |

### Task / Custom Cleaning (siid 4)

| Action | siid | aiid | Description |
|--------|------|------|-------------|
| `START_CUSTOM` | 4 | 1 | Start zone / segment / spot clean (params: area coordinates, segment IDs, or spot coordinates) |
| `CLEAR_WARNING` | 4 | 3 | Dismiss active warning |
| `GET_PHOTO_INFO` | 4 | 6 | Request obstacle photo metadata |
| `SHORTCUTS` | 4 | 8 | Execute a named shortcut task |

### Map Management (siid 6)

| Action | siid | aiid | Description |
|--------|------|------|-------------|
| `REQUEST_MAP` | 6 | 1 | Request a new full map upload |
| `UPDATE_MAP_DATA` | 6 | 2 | Push updated map data (obstacles, virtual walls, zones) |
| `BACKUP_MAP` | 6 | 3 | Trigger cloud map backup |
| `WIFI_MAP` | 6 | 4 | Request Wi-Fi signal map |

### Audio (siid 7)

| Action | siid | aiid | Description |
|--------|------|------|-------------|
| `LOCATE` | 7 | 1 | Play locating sound / flash light |
| `TEST_SOUND` | 7 | 2 | Play audio test |

### Schedule (siid 8)

| Action | siid | aiid | Description |
|--------|------|------|-------------|
| `DELETE_SCHEDULE` | 8 | 1 | Delete a cleaning schedule |
| `DELETE_CRUISE_SCHEDULE` | 8 | 2 | Delete a patrol schedule |

### Consumable Resets

| Action | siid | aiid | Description |
|--------|------|------|-------------|
| `RESET_BLADES` | 9 | 1 | Reset main brush / blades counter |
| `RESET_SIDE_BRUSH` | 10 | 1 | Reset side brush counter |
| `RESET_FILTER` | 11 | 1 | Reset filter counter |
| `RESET_SENSOR` | 16 | 1 | Reset cliff sensor counter |
| `RESET_TANK_FILTER` | 17 | 1 | Reset water tank filter counter |
| `RESET_SILVER_ION` | 19 | 1 | Reset silver-ion counter |
| `RESET_LENSBRUSH` | 1 | 3 | Reset lens brush counter |
| `RESET_SQUEEGEE` | 24 | 1 | Reset squeegee counter |

### Camera / Stream (siid 10001)

| Action | siid | aiid | Description |
|--------|------|------|-------------|
| `STREAM_VIDEO` | 10001 | 1 | Start / stop video stream |
| `STREAM_AUDIO` | 10001 | 2 | Start / stop audio stream |
| `STREAM_PROPERTY` | 10001 | 3 | Stream device properties |
| `STREAM_CODE` | 10001 | 4 | Manage stream access code |

---

## 4. MOVA P50 Pro Ultra — Device Profile

### 4.1 Hardware

| Category | Spec |
|----------|------|
| **Suction** | 19 000 Pa (4 levels: Quiet / Standard / Power / Max) |
| **Main brush** | Hybrid rubber roller with CleanChop anti-tangle + active hair-removal comb |
| **Side brush** | Single, auto-extending; lifts 10 mm on carpet detection |
| **Onboard dustbin** | 300 mL |
| **Battery** | 5 200 mAh — up to 170 min (Standard mode) |
| **Threshold** | 22 mm |

#### Navigation & Sensors

| Sensor | Role |
|--------|------|
| Spinning dual-line LiDAR | Primary room mapping |
| Front RGB camera + 3D structured light + LED spotlight | Obstacle identification (160+ categories, ≥2 cm); dirt detection |
| Cliff sensors | Drop prevention (known false positives on dark carpets — see quirks) |

- Up to 4 saved floor plans (2D + 3D view)
- Initial mapping: ~10–20 min

#### Mop System

| Feature | Value |
|---------|-------|
| Pad type | Dual rotary pads (~180 RPM) |
| Water levels | 32 adjustable |
| Mop lift | 10 mm auto-lift on carpet |
| Auto mop removal | Yes — pads eject at dock before carpet-only runs |
| Mop wash temp | 75 °C |

#### Dock Station

| Feature | Spec |
|---------|------|
| Clean water tank | 4 L |
| Dirty water tank | 3.5 L |
| Dust bag | 3.2 L (up to 75-day capacity) |
| Mop drying | Heated air ~45 °C for ~2 h |
| UV-C sterilisation | Yes |

### 4.2 MiIO Model IDs

| Model string | Notes |
|---|---|
| `mova.vacuum.r2475a` | Primary P50 Pro Ultra |
| `mova.vacuum.r2475h` | Regional H variant |
| `mova.vacuum.r2475t` | Regional T variant |
| `mova.vacuum.r9416d` | Auto water supply/drainage dock variant |
| `mova.vacuum.r2587a` | Newer SKU (added to Tasshack dev branch 2026) |
| `mova.vacuum.r2519a` | P50 Ultra (non-Pro, related model) |

### 4.3 HA Services Available for P50 Pro Ultra

| Service | Availability |
|---------|-------------|
| `vacuum.start` | Full home clean |
| `vacuum.pause` | Pause |
| `vacuum.stop` | Stop in place |
| `vacuum.return_to_base` | Return to dock |
| `vacuum.set_fan_speed` | Suction level (Quiet/Standard/Power/Max) |
| `vacuum.locate` | Audible/visual locate |
| `dreame_mower.vacuum_clean_segment` | Clean specific rooms |
| `dreame_mower.vacuum_clean_zone` | Clean rectangular zones by coordinates |
| `dreame_mower.vacuum_clean_spot` | Spot clean |
| `dreame_mower.vacuum_set_dnd` | Do Not Disturb schedule |
| `dreame_mower.vacuum_reset_consumable` | Reset brush/filter counters |
| `dreame_mower.select_map` / `delete_map` | Multi-floor map management |

---

## 5. Home Assistant Integration Architecture

### 5.1 Integration File Layout

```
custom_components/dreame_mower/
├── __init__.py          # async_setup_entry / async_unload_entry
├── manifest.json        # Domain, version, HACS metadata, dependencies
├── config_flow.py       # UI setup wizard (credential entry, account type)
├── coordinator.py       # DataUpdateCoordinator — single polling point
├── entity.py            # Shared base entity class
├── lawn_mower.py        # lawn_mower platform (mowers)
├── sensor.py            # Sensor entities (battery, area, time, consumables…)
├── switch.py            # Toggle entities (carpet boost, DND, AI detection…)
├── button.py            # One-shot actions (reset consumables, locate…)
├── number.py            # Numeric adjustments (volume, mop wash frequency…)
├── select.py            # Enum selections (suction level, cleaning mode…)
├── camera.py            # Map image + live obstacle camera
├── time.py              # DND start/end time pickers
└── dreame/
    ├── protocol.py      # Cloud HTTP + MQTT + local miIO transport
    ├── device.py        # Property cache, state machine, all device logic
    ├── types.py         # Enums, PropertyMapping, ActionMapping
    ├── const.py         # Code-to-name tables, capability maps
    ├── map.py           # Map frame parsing and rendering
    └── exceptions.py    # Custom exception types
```

### 5.2 Config Flow

The setup UI (`config_flow.py`) extends `homeassistant.config_entries.ConfigFlow`.

**Steps:**
1. `async_step_user` — choose account type (Dreame Cloud / MOVA Cloud / Local)
2. `async_step_cloud` — enter username, password, region → validate → create entry
3. `async_step_local` — enter IP address + token → validate → create entry
4. `async_step_reauth` — re-enter credentials after token expiry (no full reset needed)

A unique ID is derived from the device serial number so HA deduplicates entries correctly.

### 5.3 DataUpdateCoordinator Pattern

`coordinator.py` subclasses `DataUpdateCoordinator`. It is the single polling point shared by all entities.

```
Polling interval:
  - 3 s  while robot is actively cleaning
  - 10 s at all other times
  - 30 s when connection errors are detected

After any command:
  coordinator.async_request_refresh() → immediate re-poll
```

Entities subclass `CoordinatorEntity` and register a `_handle_coordinator_update` listener. They only re-render when their specific property value changes.

### 5.4 HA Entity Platforms

#### `lawn_mower` / `vacuum` — Primary Control Entity

The robot appears as one top-level entity.

**States:**

| HA State | Meaning |
|----------|---------|
| `mowing` / `CLEANING` | Active task |
| `docked` / `DOCKED` | At dock (includes charging) |
| `paused` / `PAUSED` | Task suspended |
| `returning` / `RETURNING` | Heading to dock |
| `idle` / `IDLE` | Inactive, no errors |
| `error` / `ERROR` | Fault condition |

**Feature flags that unlock services:**

| Flag | Service |
|------|---------|
| `START` | `vacuum.start` |
| `STOP` | `vacuum.stop` |
| `PAUSE` | `vacuum.pause` |
| `RETURN_HOME` | `vacuum.return_to_base` |
| `FAN_SPEED` | `vacuum.set_fan_speed` |
| `LOCATE` | `vacuum.locate` |
| `CLEAN_SPOT` | `vacuum.clean_spot` |
| `CLEAN_AREA` | Room-based cleaning |
| `MAP` | Map data access |
| `SEND_COMMAND` | Raw MIoT passthrough |

#### `sensor` — Read-Only State

Examples: battery %, charging status, cleaning time, cleaned area, current room, task status, error code, water tank status, mop pad status, brush/filter life levels, auto-empty status, lifetime stats.

#### `switch` — Boolean Toggles

Examples: carpet boost, carpet recognition, carpet avoidance, obstacle avoidance, child lock, DND, multi-floor map, auto dust collect, self-clean, auto drying, fill light, AI detection features (obstacle/pet/fluid/stain).

#### `select` — Enum Selection

Examples: suction level, water volume, cleaning mode (vacuum/mop/both), mopping type, carpet sensitivity, auto-empty frequency, mop wash level, drying time, map rotation, active floor map.

#### `button` — One-Shot Actions

Examples: reset main brush / side brush / filter / sensor, trigger auto-empty, clear warning, start mapping, manual mop wash / dry cycle.

#### `number` — Numeric Adjustments

Examples: volume, mop cleaning remainder (pause-for-wash frequency), DND start/end hours and minutes.

#### `camera` — Map & Obstacle Images

Only available with a cloud connection:
- Live map (rendered floor plan with robot position)
- Raw map data (for custom Lovelace cards like Xiaomi Vacuum Map Card)
- Saved map 1–4 (per stored floor plan)
- Obstacle photos

### 5.5 Dynamic Entity Generation

Rather than a fixed entity list, every entity descriptor carries `exists_fn` and `available_fn` lambda predicates evaluated against the live `DeviceStatus`. Entities are added or removed automatically as device capabilities change — a P50 Pro Ultra gets mop-removal and water-tank entities while a basic model without those features does not.

### 5.6 HACS Distribution

| Requirement | Detail |
|-------------|--------|
| Repo layout | `custom_components/<domain>/` at repo root |
| `hacs.json` | `{"name": "...", "render_readme": true}` in repo root |
| Version | `manifest.json` version must match a semver GitHub release tag |
| Public store listing | PR to `hacs/default` (not required for custom repo use) |

---

## 6. Known Quirks & Limitations

| # | Issue | Workaround |
|---|-------|------------|
| 1 | **Separate cloud accounts.** MOVAhome and Dreamehome are different backends. A device set up in the MOVA app is invisible to Dreame credentials and vice versa. | Use MOVAhome account type in the integration setup. Switching apps requires a factory reset. |
| 2 | **Region must match.** Wrong region during login returns "No compatible devices found." | Select the region where the MOVAhome/Dreamehome account was created (e.g., Europe for EU accounts). |
| 3 | **Maps unavailable in local mode.** Local miIO transport does not support the map subsystem. | Use cloud mode if map features are needed. |
| 4 | **Cliff sensor false positives.** Dark or low-pile carpets can trigger cliff sensors, causing the robot to abort and dock. | Adjust carpet sensitivity in the integration settings. |
| 5 | **Camera entities require cloud.** Live map and obstacle photos are cloud-only features. | No workaround; local mode cannot stream map data. |
| 6 | **Model variant gaps.** Newer SKUs (e.g., `r2587a`) may not be in the current stable release. | Install from the `dev` branch or check `Tasshack/dreame-vacuum` supported devices list. |
| 7 | **Map parse errors on some firmware.** Certain firmware versions cause `IndexError` during obstacle map decode. | Update device firmware via the MOVA app; report the specific firmware version in an issue. |

---

## References

- [Tasshack/dreame-vacuum](https://github.com/Tasshack/dreame-vacuum) — original integration this fork is based on
- [dreame-vacuum supported devices](https://github.com/Tasshack/dreame-vacuum/blob/dev/docs/supported_devices.md)
- [dreame-vacuum entity reference](https://github.com/Tasshack/dreame-vacuum/blob/master/docs/entities.md)
- [HA Developer Docs: Vacuum Entity](https://developers.home-assistant.io/docs/core/entity/vacuum/)
- [HA Developer Docs: Config Flow](https://developers.home-assistant.io/docs/config_entries_config_flow_handler/)
- [python-miio Dreame mappings](https://python-miio.readthedocs.io/en/latest/)
- [MOVA product catalog](https://www.mova.tech/collections/robot-vacuum)
