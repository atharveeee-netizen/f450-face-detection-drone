# Firmware Setup & Calibration

How the Pixhawk 2.4.8 and Raspberry Pi were configured.

## 1. Flight Controller - ArduCopter via Mission Planner

1. Connect the Pixhawk over USB, open **Mission Planner**, and flash the latest stable **ArduCopter** firmware.
2. Frame class: **Quad**, frame type: **X**.

## 2. Mandatory Calibrations (Mission Planner → Setup)

| Calibration | Procedure | Notes |
|---|---|---|
| Accelerometer | Place the drone on each of its 6 faces when prompted | Use a flat, level surface |
| Compass | Rotate the drone through all axes until samples complete | Done **outdoors**, away from metal; the 3D-printed GPS mast noticeably reduced interference |
| Radio | Move all FS-i6 sticks/switches to their extremes | Verify channel directions match Mission Planner bars |
| ESC | All-at-once method: throttle high → plug battery → wait for beeps → throttle low | **Props off** |
| Battery monitor | Select the power module, verify voltage against a multimeter | Enables low-battery failsafe |

## 3. Flight Modes (FS-i6 3-position switch)

| Switch position | Mode | Use |
|---|---|---|
| 1 | **Stabilize** | Manual flying, takeoff/landing practice |
| 2 | **AltHold** | Barometer holds altitude |
| 3 | **Loiter** | GPS position + altitude hold |

**RTL (Return to Launch)** is mapped to a separate two-position switch as a panic option.

## 4. Failsafes

| Failsafe | Trigger | Action |
|---|---|---|
| Radio loss | RC signal lost > 1 s | RTL |
| Battery low | 10.5 V (3S) | RTL |
| Battery critical | 10.0 V | Land |
| GCS loss | Telemetry lost (when GCS-controlled) | Continue mission / RTL |

## 5. Telemetry Link

- Air module on `TELEM1`, ground module on the laptop's USB.
- Live HUD, GPS status, battery voltage, and mode changes visible in Mission Planner during all test flights.

## 6. Raspberry Pi Setup

```bash
# Raspberry Pi OS (Bullseye or newer) on a 32 GB microSD
sudo raspi-config          # enable camera + SSH
sudo apt update
sudo apt install -y python3-opencv python3-picamera2

# Get the vision code
git clone https://github.com/atharveeee-netizen/f450-face-detection-drone.git
cd f450-face-detection-drone
python3 src/face_detection.py --headless --save-dir detections/
```

To start face detection automatically on boot, add the script to
`/etc/rc.local` (before `exit 0`) or create a `systemd` service:

```ini
# /etc/systemd/system/face-detection.service
[Unit]
Description=Onboard face detection
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/f450-face-detection-drone/src/face_detection.py --headless --save-dir /home/pi/detections
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now face-detection.service
```
