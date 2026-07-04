# Flight Testing & Results

## Pre-Flight Checklist

- [ ] Frame screws + prop nuts tight, props free of cracks
- [ ] Battery fully charged (12.6 V) and strapped securely
- [ ] Transmitter on **first**, throttle at zero, correct model selected
- [ ] GPS: 3D fix with 8+ satellites before arming in Loiter
- [ ] Telemetry link green in Mission Planner; HUD level when drone is level
- [ ] Safety switch pressed, arm in Stabilize, brief hover check for oscillation
- [ ] Bystanders clear; open area, low wind

## Test Campaign

| # | Test | Purpose | Result |
|---|---|---|---|
| 1 | Bench: motor order & direction (props off) | Verify MAIN OUT mapping and rotation | Two motors reversed → fixed by swapping wire pairs |
| 2 | First hover (Stabilize, ~1 m) | Basic stability, vibration check | Stable; minor drift corrected with trim |
| 3 | AltHold hover | Barometer altitude hold | Holds altitude within ~0.5 m |
| 4 | Loiter (GPS hold) | GPS + compass health | Holds position within ~1-1.5 m circle |
| 5 | RTL trigger | Failsafe behaviour | Climbs, returns and lands within ~2 m of takeoff point |
| 6 | Endurance test (hover + gentle cruise) | Flight time on 2200 mAh 3S | **~18 minutes** to low-battery failsafe |
| 7 | Onboard face detection | Vision system in flight | Faces detected and snapshots saved from the Pi Camera feed |

## Face Detection Performance (Raspberry Pi 3B+)

| Metric | Value |
|---|---|
| Resolution | 640×480 |
| Detector | OpenCV Haar cascade (frontal face) |
| Throughput | ~5-8 FPS on the Pi 3B+ CPU |
| Effective range | Reliable detection up to ~4-5 m in daylight |
| Output | Bounding boxes + timestamped snapshots per detection |

## Flight Videos

- [Full flight test](../media/flight-test-full.mp4)
- [Short flight clip](../media/flight-test-short.mp4)

## Lessons Learned

1. **Compass interference is real** - the GPS sitting near the PDB threw constant compass errors; the 3D-printed mast mount fixed it.
2. **Vibration dampening pays off** - damper-mounted Pixhawk gave visibly cleaner accelerometer logs and steadier AltHold.
3. **Power the Pi separately** - an independent 5 V BEC avoids brownouts of the flight controller under vision load.
4. **Calibrate outdoors** - indoor compass calibration produced unusable offsets near rebar/furniture.

## Future Improvements

- MAVLink bridge (Pi `TELEM2` ↔ Pixhawk) so detections can trigger flight behaviour (e.g. follow / orbit)
- Swap Haar cascade for a lightweight DNN (e.g. MobileNet-SSD) for better angle/lighting robustness
- Larger battery (3S 5200 mAh) trade study for extended endurance
- Gimbal-stabilised camera for cleaner detection footage
