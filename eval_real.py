#!/usr/bin/env python3
"""Run any LeRobot chunking policy (SmolVLA, ACT, ...) on the real SO-101 follower, asynchronously.

Cameras come from server.py's ZMQ stream (the same one used for recording), so start server.py first
with both feeds live and the arms NOT connected in its page.

    python eval_real.py --checkpoint <run>/checkpoints/020000/pretrained_model --dry-run   # predict only
    python eval_real.py --checkpoint <run>/checkpoints/020000/pretrained_model             # move the arm

How it runs (research/FINAL_REPORT.md section 6):
  * Every chunk is timestamped with the moment its observation was taken; action k is the target for
    t_obs + k/fps. The executor runs at --hz, interpolating inside the current chunk, so actions whose time
    has already passed while the model was thinking are skipped rather than replayed late.
  * An inference thread asks for a new chunk every --execute-s; the executor switches to each one outright.
    No blending or averaging between chunks. For flow-matching policies (SmolVLA) real-time chunking (RTC)
    is on: the new chunk is generated so its first steps match the part of the current chunk that will run
    while the model is thinking, which removes the jump at the switch. The jump is logged either way.
  * Every query (per-stage timing, switch jump, state, chunk) goes to policy_runs/<time>.jsonl.

Ctrl+C / SIGTERM stops the policy; the arm holds its last position (torque stays on) so it doesn't drop.
"""

import argparse
import glob
import json
import os
import signal
import sys
import threading
import time
from pathlib import Path

import cv2
import numpy as np

FOLLOWER_SERIAL = "5B8E114307"
JOINTS = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]
TASK = "Pick up the pumpkin and place it in the tray"
CAMERA_STREAMS = {"camera1": "scene_cam", "camera2": "arm_cam"}  # dataset image key -> server.py ZMQ stream
RUN_DIR = Path(__file__).parent / "policy_runs"
# Median first-frame joint state of the 100 training episodes (rest pose; spread under 4 deg on the big joints).
# Starting every trial here matches how every demo began.
HOME_POSE = np.array([-7.6, 1.0, -0.2, 68.9, 2.8, 1.5], dtype=np.float32)
HOME_SPEED = 30.0  # deg/s while homing: slow enough to be harmless if something is in the way


class PolicyStop(Exception):
    """Raised when server.py asks the policy subprocess to stop."""


def emit(**status):
    """Status line for server.py (ignored when run from a terminal)."""
    print("@@ " + json.dumps(status), flush=True)


def follower_port():
    for link in glob.glob(f"/dev/serial/by-id/*{FOLLOWER_SERIAL}*"):
        return os.path.realpath(link)
    sys.exit(f"Follower USB adapter (...{FOLLOWER_SERIAL[-4:]}) is not plugged in")


def smooth_chunk(actions, sigma):
    """Zero-phase Gaussian smoothing along time. A chunk is a whole plan, so filtering it with both past and
    future steps removes the model's step-to-step sampling noise without adding any lag."""
    if sigma <= 0:
        return actions
    radius = int(np.ceil(3 * sigma))
    k = np.exp(-0.5 * (np.arange(-radius, radius + 1) / sigma) ** 2)
    k /= k.sum()
    padded = np.pad(actions, ((radius, radius), (0, 0)), mode="edge")
    return np.stack([np.convolve(padded[:, j], k, mode="valid") for j in range(actions.shape[1])], axis=1)


JETSON_KEY = Path.home() / ".ssh/id_ed25519_jetson"


def sync_to_jetson(checkpoint, host):
    """rsync the checkpoint and the policy code into ~/so101 on the Jetson; returns the checkpoint path there.
    If the code changed, the policy server re-executes itself so it runs the same code as the laptop."""
    import subprocess

    ckpt = Path(checkpoint).resolve()
    rel = f"checkpoints/{ckpt.parts[-4]}/{ckpt.parts[-2]}/pretrained_model"
    ssh = f"ssh -i {JETSON_KEY} -o BatchMode=yes -o ConnectTimeout=5"
    here = Path(__file__).resolve().parent
    subprocess.run(["ssh", "-i", str(JETSON_KEY), "-o", "BatchMode=yes", f"kurat@{host}", f"mkdir -p so101/{rel}"],
                   check=True)
    # Keep only this checkpoint on the Jetson (its 56 GB card filled up with old copies once); the laptop has all.
    subprocess.run(["ssh", "-i", str(JETSON_KEY), "-o", "BatchMode=yes", f"kurat@{host}",
                    "find /home/kurat/so101/checkpoints -mindepth 2 -maxdepth 2 -type d "
                    f"! -path '/home/kurat/so101/{rel.rsplit('/', 1)[0]}' -exec rm -rf {{}} +"], check=True)
    subprocess.run(["rsync", "-a", "--delete", "-e", ssh, f"{ckpt}/", f"kurat@{host}:so101/{rel}/"], check=True)
    code = subprocess.run(["rsync", "-a", "-i", "--exclude", "__pycache__", "-e", ssh,
                           str(here / "policy_runtime.py"), str(here / "so101_policy"),
                           str(here / "jetson/policy_server.py"), f"kurat@{host}:so101/"],
                          check=True, capture_output=True, text=True).stdout
    if code.strip():
        import zmq

        sock = zmq.Context.instance().socket(zmq.REQ)
        sock.setsockopt(zmq.LINGER, 0)
        sock.connect(f"tcp://{host}:5557")
        sock.send(json.dumps({"cmd": "restart"}).encode())
        sock.poll(5000)
        sock.close()
        time.sleep(3)
    return rel


class SimulatedFollower:
    """Stand-in for the follower (--no-arm): reports the last commanded position as its state, so the whole
    pipeline (cameras, model, RTC, executor, logging) can be tested without an arm."""

    def __init__(self):
        outer = self

        class Bus:
            def sync_read(self, _register, **_kwargs):
                return dict(zip(JOINTS, outer.position))

            def sync_write(self, _register, values):
                outer.position = [values[j] for j in JOINTS]

            def disable_torque(self):
                pass

        self.position = [0.0, -100.0, 95.0, 70.0, 0.0, 2.0]  # roughly the rest pose
        self.bus = Bus()

    def disconnect(self):
        pass


class Plan:
    """A chunk of joint targets; action k is the target for time t0 + k * dt."""

    def __init__(self, t0, dt, actions, raw=None):
        self.t0, self.dt, self.actions = t0, dt, actions
        self.raw = raw  # the model's normalized output, which RTC conditions the next chunk on

    def target(self, t):
        x = (t - self.t0) / self.dt
        if x <= 0:
            return self.actions[0]
        if x >= len(self.actions) - 1:
            return self.actions[-1]
        i = int(x)
        w = x - i
        return (1 - w) * self.actions[i] + w * self.actions[i + 1]

    def ends(self):
        return self.t0 + (len(self.actions) - 1) * self.dt


class Crossfade:
    """Glide from the plan being followed to a new one over `duration` s (smoothstep) instead of jumping.
    For deterministic heads without RTC (ACT), whose consecutive chunks can disagree by tens of degrees; a
    flow policy with RTC doesn't need it, and averaging two different modes of a flow policy would be wrong."""

    def __init__(self, old, new, start, duration):
        self.old, self.new, self.start, self.duration = old, new, start, duration
        self.t0, self.raw = new.t0, new.raw

    def target(self, t):
        a = min(max((t - self.start) / self.duration, 0.0), 1.0)
        if a >= 1:
            return self.new.target(t)
        a = a * a * (3 - 2 * a)
        return (1 - a) * self.old.target(t) + a * self.new.target(t)

    def ends(self):
        return self.new.ends()

    def settled(self, t):
        return t >= self.start + self.duration


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--task", default=TASK)
    ap.add_argument("--fps", type=float, default=10.0, help="dataset rate; chunk actions are 1/fps apart")
    ap.add_argument("--hz", type=float, default=50.0, help="rate targets are sent to the servos")
    ap.add_argument("--execute-s", type=float, default=0.6,
                    help="seconds of each chunk executed before the next one takes over")
    ap.add_argument("--n-action-steps", type=int, default=None,
                    help="same as --execute-s, in dataset steps (kept for server.py)")
    ap.add_argument("--max-speed", type=float, default=100.0, help="joint speed limit in deg/s (gripper: %%/s)")
    ap.add_argument("--bf16", action="store_true", help="run the model under bf16 autocast")
    ap.add_argument("--smooth", type=float, default=1.0,
                    help="Gaussian smoothing of each chunk along time, sigma in dataset steps (0 = off)")
    ap.add_argument("--crossfade", type=float, default=None,
                    help="seconds to glide into each new chunk (default 0 = switch outright; try 0.3 for ACT)")
    ap.add_argument("--no-rtc", action="store_true", help="disable real-time chunking for flow policies")
    ap.add_argument("--rtc-horizon", type=int, default=None,
                    help="steps of the previous chunk the new one is guided towards (default: execute-s in steps)")
    ap.add_argument("--rtc-max-guidance", type=float, default=10.0)
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--remote", default=None, metavar="HOST:PORT",
                    help="run the model on the Jetson policy server (jetson/policy_server.py), e.g. 10.42.0.81:5557")
    ap.add_argument("--dry-run", action="store_true", help="predict without moving the arm (torque off)")
    ap.add_argument("--no-home", action="store_true", help="start from wherever the arm is instead of the rest pose")
    ap.add_argument("--no-frames", action="store_true", help="don't save the camera frames of each query")
    ap.add_argument("--no-arm", action="store_true",
                    help="pipeline test with a simulated follower; the real arm is not touched")
    args = ap.parse_args()
    if args.n_action_steps:
        args.execute_s = args.n_action_steps / args.fps
    dt = 1.0 / args.fps

    # server.py stops a run with SIGTERM; treat it like Ctrl+C so the arm is left holding.
    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(PolicyStop()))

    robot = None
    cameras = {}
    stop = threading.Event()
    queries = 0
    log = None

    try:
        emit(state="loading", message="Loading policy on GPU")

        from lerobot.cameras.zmq.camera_zmq import ZMQCamera
        from lerobot.cameras.zmq.configuration_zmq import ZMQCameraConfig
        from lerobot.robots.so_follower import SOFollower, SOFollowerRobotConfig

        from policy_runtime import CAMERA_STREAMS, LocalPolicy, RemotePolicy

        rtc_horizon = args.rtc_horizon or max(1, round(args.execute_s * args.fps))
        options = dict(rtc=not args.no_rtc, rtc_horizon=rtc_horizon, rtc_max_guidance=args.rtc_max_guidance,
                       bf16=args.bf16)
        if args.remote:
            print(f"Syncing checkpoint and policy code to the Jetson ({args.remote})...")
            remote_checkpoint = sync_to_jetson(args.checkpoint, args.remote.split(":")[0])
            print("Loading the policy on the Jetson GPU...")
            runtime = RemotePolicy(args.remote, remote_checkpoint, **options)
        else:
            print("Loading the policy on the GPU...")
            runtime = LocalPolicy(args.checkpoint, **options)
        rtc = runtime.rtc
        crossfade = args.crossfade if args.crossfade is not None else 0.0
        if runtime.skipped_cameras:
            print(f"No camera stream for {runtime.skipped_cameras}; running without them")
        for key in runtime.image_keys:
            name = key.rsplit(".", 1)[-1]
            cameras[key] = ZMQCamera(ZMQCameraConfig(server_address="127.0.0.1", port=5555,
                                                     camera_name=CAMERA_STREAMS[name],
                                                     width=640, height=480, fps=int(args.fps), warmup_s=2))
            cameras[key].connect()

        if args.no_arm:
            robot = SimulatedFollower()
        else:
            robot = SOFollower(SOFollowerRobotConfig(port=follower_port(), id="so101_follower",
                                                     disable_torque_on_disconnect=False))
            robot.connect(calibrate=False)
            if not robot.is_calibrated:
                sys.exit("Follower calibration doesn't match its motors")
        if args.dry_run:
            robot.bus.disable_torque()

        # Only the executor loop touches the motor bus; it shares the latest joint reading with the
        # inference thread through `latest`.
        lock = threading.Lock()
        latest = {"state": None, "plan": None}
        plans = []  # new chunks handed from the inference thread to the executor

        def read_state():
            s = robot.bus.sync_read("Present_Position", num_retry=3)  # one garbled packet shouldn't end a run
            return np.array([s[j] for j in JOINTS], dtype=np.float32)

        def infer(state, guide=None):
            t = time.perf_counter()
            # ZMQCamera hands back cv2's BGR decode; the dataset was recorded as RGB.
            images = {key: cv2.cvtColor(cam.read_latest(max_age_ms=2500), cv2.COLOR_BGR2RGB)
                      for key, cam in cameras.items()}
            obs = time.perf_counter() - t
            chunk, raw, timing = runtime.infer(state, images, args.task, guide)
            if frame_dir is not None:
                # What the model saw for this query: all cameras side by side at half size.
                views = [cv2.resize(images[k], (320, 240), interpolation=cv2.INTER_AREA) for k in sorted(images)]
                cv2.imwrite(str(frame_dir / f"q{queries + 1:04d}.jpg"), cv2.cvtColor(np.hstack(views), cv2.COLOR_RGB2BGR),
                            [cv2.IMWRITE_JPEG_QUALITY, 80])
            return chunk, raw, {"obs": obs, **timing}

        def go_home():
            """Glide to HOME_POSE at HOME_SPEED, then settle, before the policy takes over."""
            emit(state="homing", dry_run=args.dry_run, queries=0)
            print("Moving to the demos' start pose...", flush=True)
            command = read_state()
            step = HOME_SPEED / 50.0
            deadline = time.perf_counter() + 12.0
            while time.perf_counter() < deadline:
                command = command + np.clip(HOME_POSE - command, -step, step)
                robot.bus.sync_write("Goal_Position", {j: float(v) for j, v in zip(JOINTS, command)})
                if np.abs(HOME_POSE - command).max() < 0.1 and np.abs(HOME_POSE - read_state())[:5].max() < 3.0:
                    break
                time.sleep(0.02)
            time.sleep(0.5)
            print(f"At start pose (off by {np.abs(HOME_POSE - read_state()).round(1).tolist()} deg)", flush=True)

        if not args.dry_run and not args.no_home:
            go_home()

        frame_dir = None  # set once the run's log is opened; warm-up queries aren't saved
        # Warm up CUDA kernels and allocator so the first real query isn't several times slower.
        state = read_state()
        for _ in range(2):
            infer(state)
        runtime.reset()

        latency_est = [0.2]

        def inference_loop():
            nonlocal queries
            request_at = 0.0
            while not stop.is_set():
                if time.perf_counter() < request_at:
                    time.sleep(0.002)
                    continue
                with lock:
                    state = latest["state"]
                    current = latest["plan"]
                if state is None:
                    time.sleep(0.005)
                    continue
                t_obs = time.perf_counter()
                guide = None
                if rtc and current is not None and current.raw is not None:
                    # Unexecuted part of the current chunk from this observation on, and how many of its
                    # steps will already have run by the time the new chunk arrives.
                    start_idx = int(np.ceil((t_obs - current.t0) / dt))
                    left = current.raw[start_idx:]
                    if len(left) > 0:
                        guide = {"left": left,
                                 "inference_delay": min(len(left), int(np.ceil(latency_est[0] / dt))),
                                 "execution_horizon": rtc_horizon}
                chunk, raw, timing = infer(state, guide)
                latency = time.perf_counter() - t_obs
                latency_est[0] = 0.7 * latency_est[0] + 0.3 * latency
                chunk = smooth_chunk(chunk, args.smooth).astype(np.float32)
                with lock:
                    plans.append((Plan(t_obs, dt, chunk, raw), state, timing, latency))
                queries += 1
                # Each chunk then runs for about execute_s of wall time before the next one replaces it.
                request_at = t_obs + args.execute_s

        RUN_DIR.mkdir(exist_ok=True)
        log_path = RUN_DIR / time.strftime("%Y%m%d-%H%M%S.jsonl")
        log = log_path.open("w")
        if not args.no_frames:
            frame_dir = log_path.with_suffix("")
            frame_dir.mkdir()
        log.write(json.dumps({"checkpoint": args.checkpoint, "policy": runtime.policy_type, "task": args.task,
                              "dry_run": args.dry_run, "fps": args.fps, "hz": args.hz,
                              "execute_s": args.execute_s, "max_speed": args.max_speed, "bf16": args.bf16, "smooth": args.smooth,
                              "rtc": rtc, "rtc_horizon": rtc_horizon if rtc else None, "remote": args.remote,
                              "crossfade": crossfade,
                              "rtc_max_guidance": args.rtc_max_guidance}) + "\n")

        emit(state="running", dry_run=args.dry_run, queries=0)
        print(f"\n{'DRY RUN: arm will not move' if args.dry_run else 'Running policy on the arm'} "
              f"for up to {args.seconds:.0f}s. {runtime.policy_type}{' on the Jetson' if args.remote else ''}, execute {args.execute_s:.2f}s of each chunk, "
              f"RTC {'on' if rtc else 'off'}, crossfade {crossfade:.1f}s, "
              f"servo targets at {args.hz:.0f} Hz. Log: {log_path}\nCtrl+C to stop.\n")

        with lock:
            latest["state"] = read_state()
        threading.Thread(target=inference_loop, daemon=True).start()

        start = time.perf_counter()
        period = 1.0 / args.hz
        max_step = args.max_speed * period
        plan = None
        command = latest["state"].copy()  # last target sent; the speed limit is applied relative to it
        starved = overruns = 0
        next_t = start
        while time.perf_counter() - start < args.seconds:
            now = time.perf_counter()
            state = read_state()
            with lock:
                latest["state"] = state
                new = plans[:]
                plans.clear()
            for new_plan, obs_state, timing, latency in new:
                jump = None
                if plan is not None:
                    jump = np.abs(new_plan.target(now) - plan.target(now))
                plan = Crossfade(plan, new_plan, now, crossfade) if plan is not None and crossfade > 0 else new_plan
                with lock:
                    latest["plan"] = new_plan
                late_steps = (now - new_plan.t0) / dt
                record = {"t": round(now - start, 3), "latency_ms": round(latency * 1000, 1),
                          **{f"{k}_ms": round(v * 1000, 1) for k, v in timing.items()},
                          "late_steps": round(late_steps, 2),
                          "jump": None if jump is None else [round(float(v), 2) for v in jump],
                          "obs_state": obs_state.round(2).tolist(), "chunk": new_plan.actions.round(2).tolist()}
                log.write(json.dumps(record) + "\n")
                log.flush()
                target_now = plan.target(now)
                print(f"query {queries:3d} | {latency*1000:4.0f} ms (model {timing['model']*1000:4.0f}) "
                      f"| {late_steps:3.1f} steps late | jump {0 if jump is None else jump[:5].max():4.1f}° "
                      f"| now " + " ".join(f"{v:6.1f}" for v in state) +
                      " | target " + " ".join(f"{v:6.1f}" for v in target_now), flush=True)
                emit(state="running", dry_run=args.dry_run, queries=queries, latency_ms=round(latency * 1000),
                     model_ms=round(timing["model"] * 1000), late_steps=round(late_steps, 1),
                     jump_deg=None if jump is None else round(float(jump[:5].max()), 1),
                     starved=starved, overruns=overruns, elapsed=round(now - start, 1),
                     now=[round(float(v), 1) for v in state], target=[round(float(v), 1) for v in target_now])
            if isinstance(plan, Crossfade) and plan.settled(now):
                plan = plan.new
            if plan is not None:
                if now > plan.ends():
                    starved += 1  # past the end of the chunk before the next arrived; hold its last target
                target = plan.target(now)
                command = command + np.clip(target - command, -max_step, max_step)
                if not args.dry_run:
                    robot.bus.sync_write("Goal_Position", {j: float(v) for j, v in zip(JOINTS, command)})
            next_t += period
            delay = next_t - time.perf_counter()
            if delay > 0:
                time.sleep(delay)
            else:
                overruns += 1
                next_t = time.perf_counter()
    except (KeyboardInterrupt, PolicyStop):
        pass
    finally:
        stop.set()
        print("\nStopping." + (" The arm holds its last position." if robot is not None else ""))
        emit(state="stopped", queries=queries)
        if log is not None:
            log.close()
        if robot is not None:
            robot.disconnect()
        for cam in cameras.values():
            cam.disconnect()


if __name__ == "__main__":
    main()
