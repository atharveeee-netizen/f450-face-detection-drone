#!/usr/bin/env python3
"""Onboard face detection for the F450 quadcopter.

Runs on the Raspberry Pi 3B+ companion computer with a Pi Camera.
Detects faces in the live camera feed using an OpenCV Haar cascade,
draws bounding boxes, and can save an annotated snapshot of every
detection for post-flight review.

Camera backends (tried in order):
  1. picamera2          -- Raspberry Pi OS Bullseye and newer
  2. cv2.VideoCapture   -- legacy camera stack / USB webcams

Usage:
  python3 face_detection.py                    # live preview window
  python3 face_detection.py --headless         # no display (SSH / boot script)
  python3 face_detection.py --save-dir out/    # save annotated detections
"""

import argparse
import os
import time

import cv2


class Camera:
    """Small wrapper that hides which camera backend is in use."""

    def __init__(self, width, height):
        self.picam2 = None
        self.cap = None
        try:
            from picamera2 import Picamera2

            self.picam2 = Picamera2()
            config = self.picam2.create_video_configuration(
                main={"size": (width, height), "format": "RGB888"}
            )
            self.picam2.configure(config)
            self.picam2.start()
            time.sleep(1)  # let AGC/AWB settle
            print("[camera] using picamera2 backend")
        except Exception as exc:
            print(f"[camera] picamera2 unavailable ({exc}); falling back to OpenCV")
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            if not self.cap.isOpened():
                raise RuntimeError(
                    "No camera found. Enable the Pi Camera (raspi-config) "
                    "or connect a USB webcam."
                )
            print("[camera] using OpenCV VideoCapture backend")

    def read(self):
        """Return one BGR frame, or None on failure."""
        if self.picam2 is not None:
            return self.picam2.capture_array()
        ok, frame = self.cap.read()
        return frame if ok else None

    def release(self):
        if self.picam2 is not None:
            self.picam2.stop()
        if self.cap is not None:
            self.cap.release()


def main():
    parser = argparse.ArgumentParser(description="Pi Camera face detection")
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--headless", action="store_true",
                        help="run without a display (log detections to stdout)")
    parser.add_argument("--save-dir", default=None,
                        help="directory to save annotated frames of detections")
    args = parser.parse_args()

    if args.save_dir:
        os.makedirs(args.save_dir, exist_ok=True)

    cascade_path = os.path.join(
        cv2.data.haarcascades, "haarcascade_frontalface_default.xml"
    )
    face_cascade = cv2.CascadeClassifier(cascade_path)
    if face_cascade.empty():
        raise RuntimeError(f"Failed to load Haar cascade from {cascade_path}")

    camera = Camera(args.width, args.height)
    frame_count = 0
    fps = 0.0
    t_last = time.time()
    last_save = 0.0

    print("[run] face detection started (press q to quit)")
    try:
        while True:
            frame = camera.read()
            if frame is None:
                print("[run] dropped frame, retrying...")
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)

            # Parameters tuned for the Pi 3B+ CPU at 640x480.
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.2, minNeighbors=5, minSize=(40, 40)
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "FACE", (x, y - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Rolling FPS estimate over 10-frame windows.
            frame_count += 1
            if frame_count % 10 == 0:
                now = time.time()
                fps = 10.0 / (now - t_last)
                t_last = now
            cv2.putText(frame, f"{fps:.1f} FPS  faces: {len(faces)}",
                        (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

            if len(faces) > 0:
                if args.headless:
                    print(f"[detect] {len(faces)} face(s) at "
                          + ", ".join(f"({x},{y},{w}x{h})" for x, y, w, h in faces))
                # Throttle snapshots to one per second so the SD card
                # is not flooded during a continuous detection.
                if args.save_dir and time.time() - last_save >= 1.0:
                    name = time.strftime("detect_%Y%m%d_%H%M%S.jpg")
                    cv2.imwrite(os.path.join(args.save_dir, name), frame)
                    last_save = time.time()

            if not args.headless:
                cv2.imshow("F450 onboard face detection", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    except KeyboardInterrupt:
        print("\n[run] stopped by user")
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
