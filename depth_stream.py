"""RealSense depth from the Jetson (jetson/depth_publisher.py), received over ZMQ.

Each message is [header json, 16-bit PNG]: depth in raw sensor units (x depth_scale = metres), already
aligned to the colour camera's pixels so it matches the scene_cam image. The PNG bytes are kept as-is so
recording just writes them to disk; decode() gives the uint16 array.

Depth is stored beside the LeRobot dataset, not inside it, so policies trained on the dataset don't start
consuming it by accident:  <dataset root>/depth/episode_000065/frame_000000.png  plus  meta.json.
"""

import json
import os
import shutil
import threading
import time
from pathlib import Path

DEPTH_PORT = 5556


class DepthSubscriber:
    def __init__(self, host, port=DEPTH_PORT):
        import zmq

        self.lock = threading.Lock()
        self.latest = None  # (receive time, header, png bytes)
        self.frames = 0
        self.running = True
        self.socket = zmq.Context.instance().socket(zmq.SUB)
        self.socket.setsockopt(zmq.SUBSCRIBE, b"")
        self.socket.setsockopt(zmq.RCVHWM, 2)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.setsockopt(zmq.RCVTIMEO, 200)
        self.socket.connect(f"tcp://{host}:{port}")
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        import zmq

        while self.running:
            try:
                header, png = self.socket.recv_multipart()
            except zmq.Again:
                continue
            except zmq.ZMQError:
                break
            with self.lock:
                self.latest = (time.time(), json.loads(header), png)
                self.frames += 1

    def get(self, max_age_s=0.5):
        """The newest frame as (header, png bytes), or None when there is none this recent."""
        with self.lock:
            if self.latest is None or time.time() - self.latest[0] > max_age_s:
                return None
            return self.latest[1], self.latest[2]

    def close(self):
        self.running = False
        self.socket.close()


def decode(png):
    import cv2
    import numpy as np

    return cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_UNCHANGED)


def write_episode(root, episode_index, frames):
    """frames: one (header, png) or None per dataset frame. Writes PNGs and a meta.json; missing frames
    are listed so a loader can mask them."""
    folder = Path(root) / "depth" / f"episode_{episode_index:06d}"
    tmp = folder.with_name(folder.name + ".partial")
    tmp.mkdir(parents=True, exist_ok=True)
    missing, header = [], None
    for i, frame in enumerate(frames):
        if frame is None:
            missing.append(i)
            continue
        header = frame[0]
        (tmp / f"frame_{i:06d}.png").write_bytes(frame[1])
    meta = {"episode_index": episode_index, "frames": len(frames), "missing": missing,
            "camera": {k: v for k, v in (header or {}).items() if k not in ("t", "seq")}}
    (tmp / "meta.json").write_text(json.dumps(meta, indent=1))
    if folder.exists():
        shutil.rmtree(folder)  # left by an earlier episode with this index that was later deleted
    os.replace(tmp, folder)
    return folder
