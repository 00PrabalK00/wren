#!/usr/bin/env python3
"""SO-101 teleoperation with on-demand LeRobot episode recording.

Arm control runs in its own process (leader -> follower at CONTROL_HZ) so camera
decoding and video encoding can never stall it. The main process owns the cameras
and the dataset, samples the shared arm state at the dataset fps, and takes
commands on stdin: record, finish, discard, stop.

Status lines are written to stdout as "@@ {json}" for server.py.
"""

import json
import multiprocessing as mp
import sys
import threading
import time
import traceback

CONTROL_HZ = 100
# While the follower first eases to the leader's pose: degrees (or gripper %) per control step.
RAMP_STEP = 0.5
# After both arms agree, only reject implausible jumps (e.g. a bad bus read).
SYNCED_STEP = 8.0
SYNC_TOLERANCE = 3.0
STATE_READ_EVERY = 3
# The scene camera streams over the network from the Jetson; tolerate brief hiccups.
CAMERA_MAX_AGE_MS = 2500
NAMES = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]


def keep_keyframe_interval_on_gpu():
    """LeRobot only passes the GOP size to software encoders, so NVENC falls back to a keyframe every
    250 frames and random access during training has to decode up to 250 frames per sample."""
    from lerobot.datasets import video_utils

    original = video_utils._get_codec_options

    def with_gop(vcodec, g=2, crf=30, preset=None):
        options = original(vcodec, g, crf, preset)
        if g is not None and vcodec in ("h264_nvenc", "hevc_nvenc"):
            options["g"] = str(g)
            options["bf"] = "0"  # NVENC requires GOP length > B-frames + 1
        return options

    video_utils._get_codec_options = with_gop


def emit(**status):
    sys.stdout.write("@@ " + json.dumps(status) + "\n")
    sys.stdout.flush()


def clip(value, limit):
    return max(-limit, min(limit, value))


def control_main(cfg, shared, stop, ready, stats):
    """Leader -> follower loop. Shared layout: [action x6, state x6]."""
    from lerobot.robots.so_follower import SOFollower, SOFollowerRobotConfig
    from lerobot.teleoperators.so_leader import SOLeader, SOLeaderTeleopConfig

    robot = SOFollower(SOFollowerRobotConfig(port=cfg["follower"], id="so101_follower"))
    teleop = SOLeader(SOLeaderTeleopConfig(port=cfg["leader"], id="so101_leader"))
    try:
        robot.connect(calibrate=False)
        teleop.connect(calibrate=False)
        if not robot.is_calibrated or not teleop.is_calibrated:
            raise RuntimeError("Motor calibration does not match the saved calibration files")
        present = robot.bus.sync_read("Present_Position")
        goal = dict(present)
        synced = False
        ready.set()

        period = 1.0 / CONTROL_HZ
        next_t = time.perf_counter()
        loops = 0
        errors = 0
        window_start = time.perf_counter()
        window_loops = 0
        worst = 0.0
        while not stop.is_set():
            start = time.perf_counter()
            try:
                lead = teleop.bus.sync_read("Present_Position")
                if loops % STATE_READ_EVERY == 0:
                    present = robot.bus.sync_read("Present_Position")
                # The commanded goal walks toward the leader; judging sync on the goal rather than
                # the measured position avoids waiting on gravity-induced tracking error.
                step = SYNCED_STEP if synced else RAMP_STEP
                goal = {n: goal[n] + clip(lead[n] - goal[n], step) for n in NAMES}
                if not synced:
                    synced = all(abs(lead[n] - goal[n]) < SYNC_TOLERANCE for n in NAMES)
                robot.bus.sync_write("Goal_Position", goal)
                errors = 0
            except Exception:
                errors += 1
                if errors > 20:
                    raise
                continue
            with shared.get_lock():
                for i, n in enumerate(NAMES):
                    shared[i] = lead[n]
                    shared[6 + i] = present[n]
            loops += 1
            window_loops += 1
            worst = max(worst, time.perf_counter() - start)
            now = time.perf_counter()
            if now - window_start >= 1.0:
                stats[0] = window_loops / (now - window_start)
                stats[1] = worst * 1000
                stats[2] = 1.0 if synced else 0.0
                window_start, window_loops, worst = now, 0, 0.0
            next_t += period
            delay = next_t - time.perf_counter()
            if delay > 0:
                time.sleep(delay)
            else:
                next_t = time.perf_counter()
    finally:
        if robot.is_connected:
            robot.disconnect()
        if teleop.is_connected:
            teleop.disconnect()


class Recorder:
    def __init__(self, cfg, shared):
        import cv2
        from lerobot.cameras.zmq.configuration_zmq import ZMQCameraConfig
        from lerobot.processor.factory import make_default_processors
        from lerobot.robots.so_follower import SOFollower, SOFollowerRobotConfig

        keep_keyframe_interval_on_gpu()
        self.cv2 = cv2
        self.cfg = cfg
        self.shared = shared
        cameras = {
            key: ZMQCameraConfig(server_address="127.0.0.1", port=5555, camera_name=name,
                                 color_mode="rgb", width=640, height=480, fps=cfg["fps"], warmup_s=2)
            for key, name in (("camera1", "scene_cam"), ("camera2", "arm_cam"))
        }
        # Never connected: provides feature definitions and owns the camera readers.
        self.robot = SOFollower(SOFollowerRobotConfig(port=cfg["follower"], id="so101_follower", cameras=cameras))
        self.action_proc, _, self.obs_proc = make_default_processors()
        self.dataset = None
        self.lock = threading.Lock()
        self.recording = False
        self.frames = 0
        self.episodes = 0
        self.failure = ""
        # Aligned RealSense depth from the Jetson, saved beside the dataset (see depth_stream.py).
        self.depth = None
        self.depth_frames = []
        self.depth_writes = []
        if cfg.get("depth_host"):
            from depth_stream import DepthSubscriber
            self.depth = DepthSubscriber(cfg["depth_host"])

    def depth_status(self):
        if self.depth is None:
            return None
        live = self.depth.get(max_age_s=1.0) is not None
        missing = sum(1 for f in self.depth_frames if f is None)
        return {"live": live, "missing": missing}

    def connect_cameras(self):
        for cam in self.robot.cameras.values():
            cam.connect()

    def open_dataset(self):
        from lerobot.datasets.lerobot_dataset import LeRobotDataset
        from lerobot.datasets.pipeline_features import aggregate_pipeline_dataset_features, create_initial_features
        from lerobot.datasets.utils import combine_feature_dicts
        from lerobot.utils.control_utils import sanity_check_dataset_robot_compatibility

        cfg = self.cfg
        features = combine_feature_dicts(
            aggregate_pipeline_dataset_features(
                pipeline=self.action_proc,
                initial_features=create_initial_features(action=self.robot.action_features),
                use_videos=True,
            ),
            aggregate_pipeline_dataset_features(
                pipeline=self.obs_proc,
                initial_features=create_initial_features(observation=self.robot.observation_features),
                use_videos=True,
            ),
        )
        # Streaming encoding drops frames when its queue fills, which shifts video against the
        # state/action rows. GPU encoding plus a ~20 s per-camera buffer keeps it ahead.
        options = dict(batch_encoding_size=1, vcodec=cfg.get("vcodec", "h264_nvenc"), streaming_encoding=True,
                       encoder_queue_maxsize=200, encoder_threads=2)
        writer_threads = 4 * len(self.robot.cameras)
        if cfg["resume"]:
            self.dataset = LeRobotDataset(cfg["repo_id"], root=cfg["root"], **options)
            self.dataset.start_image_writer(num_processes=0, num_threads=writer_threads)
            sanity_check_dataset_robot_compatibility(self.dataset, self.robot, cfg["fps"], features)
        else:
            self.dataset = LeRobotDataset.create(
                cfg["repo_id"], cfg["fps"], root=cfg["root"], robot_type=self.robot.name,
                features=features, use_videos=True, image_writer_processes=0,
                image_writer_threads=writer_threads, **options,
            )

    def capture(self):
        from lerobot.datasets.utils import build_dataset_frame
        from lerobot.utils.constants import ACTION, OBS_STR

        with self.shared.get_lock():
            values = list(self.shared[:])
        obs = {f"{n}.pos": values[6 + i] for i, n in enumerate(NAMES)}
        for key, cam in self.robot.cameras.items():
            # ZMQCamera returns cv2's BGR decode regardless of color_mode.
            obs[key] = self.cv2.cvtColor(cam.read_latest(max_age_ms=CAMERA_MAX_AGE_MS), self.cv2.COLOR_BGR2RGB)
        action = {f"{n}.pos": values[i] for i, n in enumerate(NAMES)}
        obs_frame = build_dataset_frame(self.dataset.features, self.obs_proc(obs), prefix=OBS_STR)
        action_frame = build_dataset_frame(self.dataset.features, self.action_proc((action, obs)), prefix=ACTION)
        self.dataset.add_frame({**obs_frame, **action_frame, "task": self.cfg["task"]})
        if self.depth is not None:
            self.depth_frames.append(self.depth.get())
        self.frames += 1

    def run(self, stop):
        period = 1.0 / self.cfg["fps"]
        next_t = time.perf_counter()
        while not stop.is_set():
            with self.lock:
                if self.recording:
                    try:
                        self.capture()
                    except Exception as exc:
                        # A partial episode would have a gap, so drop it rather than save it.
                        traceback.print_exc()
                        self.recording = False
                        self.dataset.clear_episode_buffer()
                        self.failure = f"Recording stopped and the attempt was discarded: {exc}"
            next_t += period
            delay = next_t - time.perf_counter()
            if delay > 0:
                time.sleep(delay)
            else:
                next_t = time.perf_counter()

    def check_encoder_memory(self):
        """NVENC needs some free GPU memory to open; with training runs filling the GPU it fails on the first
        frame with an opaque avcodec error, so check up front and say what to do."""
        import subprocess

        if "nvenc" not in self.cfg.get("vcodec", "h264_nvenc"):
            return
        try:
            out = subprocess.run(["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
                                 capture_output=True, text=True, timeout=5).stdout
            free = int(out.split()[0])
        except (OSError, ValueError, IndexError, subprocess.SubprocessError):
            return
        if free < 600:
            raise RuntimeError(f"GPU memory is full ({free} MB free), so the video encoder can't start. "
                               "Stop a training run (systemctl --user stop so101-train-...) and record again.")

    def start_episode(self):
        self.check_encoder_memory()
        with self.lock:
            if self.dataset is None:
                self.open_dataset()
            self.frames = 0
            self.depth_frames = []
            self.failure = ""
            self.recording = True

    def end_episode(self, save):
        with self.lock:
            was_recording = self.recording
            self.recording = False
            if not was_recording or self.dataset is None:
                return False
            if save and self.frames > 0:
                episode_index = self.dataset.episode_buffer["episode_index"]
                self.dataset.save_episode()
                self.episodes += 1
                if self.depth is not None and any(f is not None for f in self.depth_frames):
                    self.save_depth(episode_index, self.depth_frames)
                return True
            self.dataset.clear_episode_buffer()
            return False

    def save_depth(self, episode_index, frames):
        from depth_stream import write_episode

        def write():
            try:
                folder = write_episode(self.cfg["root"], episode_index, frames)
                missing = sum(1 for f in frames if f is None)
                print(f"Depth for episode {episode_index}: {len(frames) - missing}/{len(frames)} frames -> {folder}",
                      flush=True)
            except Exception:
                traceback.print_exc()

        thread = threading.Thread(target=write, daemon=True)
        thread.start()
        self.depth_writes.append(thread)

    def close(self):
        for thread in self.depth_writes:
            thread.join(timeout=30)
        if self.depth is not None:
            self.depth.close()
        with self.lock:
            if self.dataset is not None:
                self.dataset.finalize()
        for cam in self.robot.cameras.values():
            if cam.is_connected:
                cam.disconnect()


def main():
    cfg = json.loads(sys.argv[1])
    ctx = mp.get_context("spawn")
    shared = ctx.Array("d", 12)
    stats = ctx.Array("d", 3)
    stop = ctx.Event()
    ready = ctx.Event()
    state = {"phase": "connecting", "message": ""}
    emit(state="connecting", episodes=0)

    control = ctx.Process(target=control_main, args=(cfg, shared, stop, ready, stats), daemon=True)
    control.start()
    recorder = Recorder(cfg, shared)
    recorder.connect_cameras()
    while not ready.wait(0.2):
        if not control.is_alive():
            emit(state="error", message="Arm control process failed to connect; see log")
            sys.exit(1)

    record_stop = threading.Event()
    threading.Thread(target=recorder.run, args=(record_stop,), daemon=True).start()
    state["phase"] = "teleop"

    def report():
        while not record_stop.is_set():
            if recorder.failure and state["phase"] == "recording":
                state["phase"] = "teleop"
                state["message"] = recorder.failure
            if not control.is_alive() and state["phase"] != "stopping":
                state["phase"] = "error"
                state["message"] = "Arm control process stopped; see log"
            emit(state=state["phase"], episodes=recorder.episodes, frames=recorder.frames,
                 hz=round(stats[0], 1), worst_ms=round(stats[1], 1), synced=bool(stats[2]),
                 depth=recorder.depth_status(), message=state["message"])
            if state["phase"] == "error":
                record_stop.set()
                return
            time.sleep(0.5)

    reporter = threading.Thread(target=report, daemon=True)
    reporter.start()

    exit_code = 0
    try:
        for line in sys.stdin:
            command = line.strip()
            if state["phase"] == "error":
                break
            try:
                if command == "record":
                    recorder.start_episode()
                    state["phase"] = "recording"
                elif command in ("finish", "discard"):
                    state["phase"] = "saving" if command == "finish" else "teleop"
                    recorder.end_episode(save=command == "finish")
                    state["phase"] = "teleop"
                elif command == "stop":
                    break
                state["message"] = ""
            except Exception as exc:
                traceback.print_exc()
                state["message"] = f"{command} failed: {exc}"
                state["phase"] = "teleop"
        if state["phase"] == "error":
            exit_code = 1
    finally:
        state["phase"] = "stopping"
        try:
            recorder.end_episode(save=True)
        except Exception:
            traceback.print_exc()
        try:
            recorder.close()
        finally:
            record_stop.set()
            stop.set()
            control.join(timeout=5)
            if control.is_alive():
                control.terminate()
        emit(state="stopped", episodes=recorder.episodes)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
