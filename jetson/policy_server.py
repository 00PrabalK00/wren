#!/usr/bin/env python3
"""Policy inference server on the Jetson, for eval_real.py --remote.

The laptop keeps the arm, cameras and control loop; for every query it sends the joint state and the camera
images here and gets the action chunk back. Checkpoints and the policy code (policy_runtime.py,
so101_policy/) are rsynced into this folder by eval_real.py before each run.

    venv/bin/python policy_server.py [--port 5557]

Protocol (ZMQ REQ/REP), request = [header json, JPEG per camera in header order]:
  {"cmd": "load", "checkpoint": "checkpoints/<run>/<step>/pretrained_model", "rtc": ..., ...}
      -> {"policy_type", "image_keys", "skipped_cameras", "rtc"}
  {"cmd": "infer", "state": [6], "task": str, "guide": null | {"left", "inference_delay", "execution_horizon"}}
      -> {"chunk", "raw", "timing"}
  {"cmd": "reset"} / {"cmd": "restart"} (re-exec after a code sync)
"""
import argparse
import gc
import json
import os
import sys
import time
import traceback
from pathlib import Path

import cv2
import numpy as np
import zmq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

ap = argparse.ArgumentParser()
ap.add_argument("--port", type=int, default=5557)
args = ap.parse_args()

sock = zmq.Context.instance().socket(zmq.REP)
sock.setsockopt(zmq.LINGER, 0)
sock.bind(f"tcp://*:{args.port}")
print(f"Policy server listening on tcp://*:{args.port}", flush=True)

policy, loaded = None, None
while True:
    header, *frames = sock.recv_multipart()
    try:
        req = json.loads(header)
        cmd = req["cmd"]
        if cmd == "load":
            from policy_runtime import LocalPolicy

            key = json.dumps(req, sort_keys=True)
            if key != loaded:
                policy = None
                gc.collect()
                import torch

                torch.cuda.empty_cache()
                t = time.perf_counter()
                policy = LocalPolicy(str(HERE / req["checkpoint"]), rtc=req.get("rtc", True),
                                     rtc_horizon=req.get("rtc_horizon", 6),
                                     rtc_max_guidance=req.get("rtc_max_guidance", 10.0), bf16=req.get("bf16", False))
                loaded = key
                print(f"Loaded {policy.policy_type} from {req['checkpoint']} in {time.perf_counter() - t:.1f}s",
                      flush=True)
            reply = {"policy_type": policy.policy_type, "image_keys": policy.image_keys,
                     "skipped_cameras": policy.skipped_cameras, "rtc": policy.rtc}
        elif cmd == "infer":
            if policy is None:
                raise RuntimeError("no policy loaded")
            t = time.perf_counter()
            images = {}
            for k, jpg in zip(policy.image_keys, frames):
                bgr = cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)
                images[k] = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            decode = time.perf_counter() - t
            chunk, raw, timing = policy.infer(req["state"], images, req["task"], req.get("guide"))
            reply = {"chunk": chunk.tolist(), "raw": raw.tolist(), "timing": {**timing, "decode": decode}}
        elif cmd == "reset":
            if policy is not None:
                policy.reset()
            reply = {"ok": True}
        elif cmd == "restart":
            sock.send(json.dumps({"ok": True}).encode())
            sock.close()
            os.execv(sys.executable, [sys.executable, *sys.argv])
        else:
            raise ValueError(f"unknown cmd {cmd}")
    except Exception as exc:
        traceback.print_exc()
        reply = {"error": f"{type(exc).__name__}: {exc}"}
    sock.send(json.dumps(reply).encode())
