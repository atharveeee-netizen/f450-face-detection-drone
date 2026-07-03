# Assembly & Wiring Guide

Step-by-step record of how the drone was built, from bare frame to flight-ready.

## 1. Frame Assembly

1. Bolt the four F450 arms (2 red front, 2 white rear for orientation) to the **bottom PDB plate** using M2.5×6 screws.
2. Solder the four **30 A ESC** power leads to the PDB pads (⚠ check polarity — red to +, black to −).
3. Solder the battery lead (XT60) to the PDB main input **through the power module** (see wiring section).
4. Fit the top plate loosely — final tightening after all wiring is routed.

## 2. Motors & Propulsion

1. Mount one **A2212 1100 KV** motor on each arm with M3×6 screws.
2. Connect each motor's 3 bullet connectors to its ESC. Motor direction is corrected later by swapping any two of the three wires.
3. **Motor layout (ArduPilot Quad X):**

```text
        FRONT
   M3 (CW)   M1 (CCW)
       \\       //
        \\     //
         [ FC ]
        //     \\
       //       \\
   M2 (CCW)  M4 (CW)
        REAR
```

4. Propellers go on **last**, after all calibration: 10×4.5 — normal props on CW motors, "R" (pusher) props on CCW motors.

## 3. Flight Controller

1. Stick the **anti-vibration damper mount** to the top plate center; mount the **Pixhawk 2.4.8** on it with the arrow facing forward.
2. Vibration isolation matters here: raw prop/motor vibration corrupts the accelerometer data the Pixhawk uses for altitude and position estimation.

## 4. GPS on 3D-Printed Mast

1. The **u-blox NEO-M8N** sits on a **3D-printed mast mount** (PLA) bolted to the top plate.
2. The mast raises the GPS/compass ~10 cm above the PDB and ESC wiring — high-current wiring generates magnetic fields that corrupt compass readings; elevation fixed our compass interference warnings.
3. GPS arrow must point **forward**, same direction as the Pixhawk arrow.

## 5. Vision System (Raspberry Pi 3B+)

1. Mount the **Raspberry Pi 3B+** on the top plate with standoffs/foam tape, clear of the Pixhawk.
2. Connect the **Pi Camera** ribbon to the CSI port; mount the camera in the 3D-printed front bracket.
3. Power the Pi from a **5 V BEC** (ESC BEC line or separate UBEC from the PDB). The Pi 3B+ draws up to ~1.5 A under vision load — don't power it from the Pixhawk rail.

## 6. Wiring Map

| From | To | Notes |
|---|---|---|
| Battery (XT60) | Power module → PDB | Power module measures voltage/current |
| Power module 6-pin | Pixhawk `POWER` | Powers the FC + battery telemetry |
| ESC signal wires ×4 | Pixhawk `MAIN OUT 1–4` | Match motor numbers above |
| FS-iA6B receiver | Pixhawk `RCIN` | PPM/iBUS output from receiver |
| NEO-M8N GPS (6-pin) | Pixhawk `GPS` | UART serial |
| NEO-M8N compass (4-pin) | Pixhawk `I2C` | External compass |
| Telemetry radio (air) | Pixhawk `TELEM1` | Ground module → laptop USB |
| Buzzer | Pixhawk `BUZZER` | Arming/error tones |
| Safety switch | Pixhawk `SWITCH` | Pre-arm safety |
| Pi Camera | Raspberry Pi CSI | Ribbon cable |
| 5 V BEC | Raspberry Pi micro-USB / GPIO 5V | Independent of FC power |

## 7. Final Checks Before Power-Up

- [ ] All solder joints continuity-tested; no bridges on the PDB
- [ ] Battery polarity verified with a multimeter at every stage
- [ ] All wiring zip-tied clear of prop arcs
- [ ] Center of gravity at the frame center with the battery strapped underneath
- [ ] Props **OFF** for every bench test
