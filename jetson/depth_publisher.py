#!/usr/bin/env python3
"""Stream RealSense D435i depth, aligned to the colour camera, from the Jetson over ZMQ.

Runs beside the existing colour pipeline (gst v4l2src /dev/video4 -> RTP JPEG), which it leaves alone: only
the depth sensor is opened here. Alignment reprojects each depth pixel into the colour camera using the
factory calibration saved by dump_calibration.py, so depth pixel (u, v) matches scene_cam pixel (u, v).

    python3 depth_publisher.py [--calibration d435i_calibration.json] [--port 5556] [--fps 15]

Messages: [header json, 16-bit PNG of depth in sensor units (x depth_scale = metres; 0 = no reading)].
Received by depth_stream.py on the laptop.
"""
import argparse
import json
import time

import cv2
import numpy as np
import pyrealsense2 as rs
import zmq

ap = argparse.ArgumentParser()
ap.add_argument("--calibration", default=str(__import__("pathlib").Path(__file__).with_name("d435i_calibration.json")))
ap.add_argument("--port", type=int, default=5556)
ap.add_argument("--fps", type=int, default=15)
args = ap.parse_args()

cal = json.load(open(args.calibration))
dep, col = cal["depth"], cal["color"]
W, H = col["width"], col["height"]
R = np.array(cal["depth_to_color"]["rotation"], dtype=np.float32).reshape(3, 3).T  # librealsense is column-major
T = np.array(cal["depth_to_color"]["translation"], dtype=np.float32)
scale = cal["depth_scale"]
u, v = np.meshgrid(np.arange(dep["width"], dtype=np.float32), np.arange(dep["height"], dtype=np.float32))
ray_x = ((u - dep["cx"]) / dep["fx"]).ravel()
ray_y = ((v - dep["cy"]) / dep["fy"]).ravel()


def align(depth):
    """Forward-project depth pixels into the colour image, nearest surface wins. The colour camera has the
    narrower field of view (fx 609 vs 384), so each depth pixel is splatted over 2x2 colour pixels."""
    d = depth.ravel()
    keep = d > 0
    z = d[keep].astype(np.float32) * scale
    p = np.stack([ray_x[keep] * z, ray_y[keep] * z, z])
    q = R @ p + T[:, None]
    uc = np.floor(q[0] / q[2] * col["fx"] + col["cx"]).astype(np.int32)
    vc = np.floor(q[1] / q[2] * col["fy"] + col["cy"]).astype(np.int32)
    dk = d[keep]
    order = np.argsort(-dk, kind="stable")  # far first, so nearer points overwrite them
    uc, vc, dk = uc[order], vc[order], dk[order]
    out = np.zeros((H + 1, W + 1), np.uint16)
    ok = (uc >= 0) & (uc < W) & (vc >= 0) & (vc < H)
    uc, vc, dk = uc[ok], vc[ok], dk[ok]
    for dv in (0, 1):
        for du in (0, 1):
            out[vc + dv, uc + du] = dk
    return out[:H, :W]


cv2.setNumThreads(1)
sock = zmq.Context.instance().socket(zmq.PUB)
sock.setsockopt(zmq.SNDHWM, 2)
sock.setsockopt(zmq.LINGER, 0)
sock.bind(f"tcp://*:{args.port}")

pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_stream(rs.stream.depth, dep["width"], dep["height"], rs.format.z16, args.fps)
profile = pipe.start(cfg)
sensor = profile.get_device().first_depth_sensor()
if sensor.supports(rs.option.emitter_enabled):
    sensor.set_option(rs.option.emitter_enabled, 1)
header = {"width": W, "height": H, "depth_scale": scale, "aligned_to": "color", "serial": cal["serial"],
          "fx": col["fx"], "fy": col["fy"], "cx": col["cx"], "cy": col["cy"], "fps": args.fps}
print(f"Publishing aligned depth on tcp://*:{args.port} at {args.fps} fps", flush=True)
seq, last_report, work = 0, time.time(), []
try:
    while True:
        frame = pipe.wait_for_frames(2000).get_depth_frame()
        t = time.time()
        aligned = align(np.asanyarray(frame.get_data()))
        ok, png = cv2.imencode(".png", aligned, [cv2.IMWRITE_PNG_COMPRESSION, 1])
        seq += 1
        sock.send_multipart([json.dumps({**header, "t": t, "seq": seq}).encode(), png.tobytes()])
        work.append(time.time() - t)
        if t - last_report > 10:
            print(f"{seq} frames, {len(work) / (t - last_report):.1f} fps, align+png {1000 * np.mean(work):.0f} ms, "
                  f"valid {(aligned > 0).mean():.2f}, {len(png) // 1024} KB", flush=True)
            last_report, work = t, []
finally:
    pipe.stop()
