#!/usr/bin/env python3
"""Local SO-101 teleoperation and LeRobot episode capture UI."""

import base64
import glob
import json
import os
import re
import signal
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import cv2
import numpy as np
import zmq


ROOT = Path("/home/zuci/ripple-research")
PYTHON = ROOT / ".venv-smolvla/bin/python"
DATASET_NAME = "so101_pumpkin_v1"
DATA_ROOT = ROOT / "data/lerobot" / DATASET_NAME
LOG = Path(__file__).parent / "recording.log"
POLICY_LOG = Path(__file__).parent / "policy.log"
TRAIN_ROOT = ROOT / "outputs/train"
POLICY_MIN_FREE_MB = 2500
JETSON_HOST = os.environ.get("JETSON_HOST", "192.168.1.182")
LAPTOP_HOST = os.environ.get("LAPTOP_HOST", "192.168.1.201")
UDP_PORT = 5001
POLICY_SERVER_PORT = 5557
# Aligned RealSense depth published by jetson/depth_publisher.py; saved beside each episode when live.
RECORD_DEPTH = os.environ.get("RECORD_DEPTH", "0") == "1"
ZMQ_PORT = 5555
ARM_CAMERA = "/dev/video2"
SCENE_CAMERA = "/dev/video4"
# Arms are identified by USB adapter serial because ttyACM numbering can change on replug.
LEADER_SERIAL = "5B8E114310"
FOLLOWER_SERIAL = "5B8E114307"
JETSON_KNOWN_HOSTS = Path("/tmp/so101_jetson_known_hosts")
LEADER_CALIBRATION = Path.home() / ".cache/huggingface/lerobot/calibration/teleoperators/so_leader/so101_leader.json"
FOLLOWER_CALIBRATION = Path.home() / ".cache/huggingface/lerobot/calibration/robots/so_follower/so101_follower.json"
MOTOR_HELPER = """import json,sys,scservo_sdk as s
results={}
packet=s.PacketHandler(0)
for port in sys.argv[1:-1]:
    disarm=sys.argv[-1]=="disarm"
    handler=s.PortHandler(port)
    found=[]
    changed=[]
    try:
        if not handler.openPort() or not handler.setBaudRate(1000000):
            raise RuntimeError("could not open at 1 Mbps")
        for motor_id in range(1,7):
            _model,comm,error=packet.ping(handler,motor_id)
            if comm==s.COMM_SUCCESS and error==0:
                found.append(motor_id)
                if disarm:
                    comm,error=packet.write1ByteTxRx(handler,motor_id,40,0)
                    if comm==s.COMM_SUCCESS and error==0:
                        changed.append(motor_id)
    except Exception as exc:
        results[port]={"motors":found,"error":str(exc)}
    else:
        results[port]={"motors":found,"torque_off":changed if disarm else None}
    finally:
        handler.closePort()
print(json.dumps(results))"""
CALIBRATION_HELPER = """import json,sys
from lerobot.motors import Motor,MotorCalibration,MotorNormMode
from lerobot.motors.feetech import FeetechMotorsBus
names=["shoulder_pan","shoulder_lift","elbow_flex","wrist_flex","wrist_roll","gripper"]
results={}
for port,path,role in zip(sys.argv[1::3],sys.argv[2::3],sys.argv[3::3]):
    expected_raw=json.load(open(path))
    expected={name:MotorCalibration(**expected_raw[name]) for name in names}
    motors={name:Motor(i+1,"sts3215",MotorNormMode.DEGREES if name!="gripper" else MotorNormMode.RANGE_0_100) for i,name in enumerate(names)}
    bus=FeetechMotorsBus(port,motors,calibration=expected)
    try:
        bus.connect()
        actual=bus.read_calibration()
        positions=bus.sync_read("Present_Position")
        results[role]={"port":port,"matches":actual==expected,"actual":{name:vars(value) for name,value in actual.items()},"positions":positions}
    except Exception as exc:
        results[role]={"port":port,"matches":False,"error":str(exc)}
    finally:
        if bus.is_connected:
            bus.disconnect(disable_torque=False)
print(json.dumps(results))"""


def port_for_serial(serial):
    for link in glob.glob(f"/dev/serial/by-id/*{serial}*"):
        return os.path.realpath(link)
    return None


def arm_ports():
    return sorted(glob.glob("/dev/ttyACM*"), key=lambda p: int(re.sub(r"\D", "", p) or 0))


def read_v4l2(device):
    result = subprocess.run(
        ["v4l2-ctl", "-d", device, "--get-ctrl=brightness,contrast,gain"],
        capture_output=True, text=True, timeout=3,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "Could not read camera controls")
    values = {key: int(value) for key, value in re.findall(r"(brightness|contrast|gain):\s*(-?\d+)", result.stdout)}
    if len(values) != 3:
        raise RuntimeError("Camera did not return brightness, contrast, and gain")
    return values


def normalize_controls(values, contrast_max, gain_max):
    return {
        "brightness": round((values["brightness"] + 64) * 100 / 128),
        "contrast": round(values["contrast"] * 100 / contrast_max),
        "gain": round(values["gain"] * 100 / gain_max),
    }


def read_v4l2_values(output):
    values = {key: int(value) for key, value in re.findall(r"(brightness|contrast|gain):\s*(-?\d+)", output)}
    if len(values) != 3:
        raise RuntimeError("Camera did not return brightness, contrast, and gain")
    return values


class CameraHub:
    def __init__(self):
        self.lock = threading.Lock()
        self.frames = {"arm_cam": None, "scene_cam": None}
        self.updated = {"arm_cam": 0.0, "scene_cam": 0.0}
        self.running = True
        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.setsockopt(zmq.SNDHWM, 2)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.bind(f"tcp://127.0.0.1:{ZMQ_PORT}")
        self.gst = None
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def publish(self, name, frame):
        ok, encoded = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 78])
        if not ok:
            return None
        return self.publish_jpeg(name, encoded.tobytes())

    def publish_jpeg(self, name, payload):
        with self.lock:
            self.frames[name] = payload
            self.updated[name] = time.time()
        return base64.b64encode(payload).decode("ascii")

    def _start_receiver(self):
        pattern = "/tmp/so101-scene-%08d.jpg"
        args = [
            "gst-launch-1.0", "-q", "udpsrc", f"port={UDP_PORT}",
            "caps=application/x-rtp,media=(string)video,clock-rate=(int)90000,encoding-name=(string)JPEG,payload=(int)26",
            "!", "rtpjpegdepay", "!",
            "multifilesink", f"location={pattern}", "max-files=3", "sync=false",
        ]
        # A receiver left over from an earlier run would share the UDP port and split the stream.
        subprocess.run(["pkill", "-f", f"udpsrc port={UDP_PORT}"], capture_output=True)
        for stale in glob.glob("/tmp/so101-scene-*.jpg"):
            try:
                os.remove(stale)
            except OSError:
                pass
        try:
            self.gst = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            self.gst = None

    def run(self):
        self._start_receiver()
        cap = cv2.VideoCapture("/dev/video2", cv2.CAP_V4L2)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        zmq_pub = self.socket
        arm_image = None
        scene_image = None
        last_scene_mtime = 0.0
        last_publish = 0.0
        while self.running:
            now = time.time()
            if cap.isOpened():
                ok, frame = cap.read()
                if ok:
                    arm_image = self.publish("arm_cam", frame)
            files = glob.glob("/tmp/so101-scene-*.jpg")
            if files:
                try:
                    newest = max(files, key=os.path.getmtime)
                    mtime = os.path.getmtime(newest)
                    if mtime > last_scene_mtime and now - mtime < 2:
                        scene_image = self.publish_jpeg("scene_cam", Path(newest).read_bytes())
                        last_scene_mtime = mtime
                except OSError:
                    pass
            if now - last_publish >= 0.1 and arm_image and scene_image:
                message = {"timestamps": {"arm_cam": now, "scene_cam": last_scene_mtime},
                           "images": {"arm_cam": arm_image, "scene_cam": scene_image}}
                try:
                    zmq_pub.send_string(json.dumps(message), zmq.NOBLOCK)
                except zmq.Again:
                    pass
                last_publish = now
            time.sleep(0.005)
        cap.release()
        if self.gst and self.gst.poll() is None:
            self.gst.terminate()

    def get(self, name):
        with self.lock:
            return self.frames.get(name), self.updated.get(name, 0)


class AppState:
    def __init__(self):
        self.lock = threading.RLock()
        self.process = None
        self.data_root = DATA_ROOT
        self.phase = "ready"
        self.error = ""
        self.jetson_password = None
        self.scene_controls_connected = False
        self.arm_probe = {}
        self.last_exit = None
        self.started_at = None
        self.task = "Pick up the pumpkin and place it in the tray"
        self.runner = {}
        self.policy_process = None
        self.policy = {}
        self.policy_error = ""
        self.hub = CameraHub()
        self.depth = None
        if RECORD_DEPTH:
            from depth_stream import DepthSubscriber
            self.depth = DepthSubscriber(JETSON_HOST)
        threading.Thread(target=self.watch, daemon=True).start()

    def watch(self):
        while True:
            with self.lock:
                process = self.process
                if process and process.poll() is not None:
                    self.last_exit = process.returncode
                    self.process = None
                    self.phase = "ready" if process.returncode == 0 else "error"
                    if process.returncode:
                        code = process.returncode
                        reason = f"killed by signal {-code}" if code < 0 else f"exit code {code}"
                        self.error = f"Teleop runner {reason}\n" + self.tail_log()
            time.sleep(0.4)

    def read_runner(self, process, log_file):
        """Copy runner output to the log and track its "@@ {json}" status lines."""
        for line in process.stdout:
            log_file.write(line)
            if not line.startswith(b"@@ "):
                continue
            try:
                status = json.loads(line[3:])
            except ValueError:
                continue
            with self.lock:
                if self.process is not process:
                    continue
                self.runner = status
                state = status.get("state")
                if state in ("connecting", "teleop", "recording", "saving"):
                    self.phase = state
                elif state == "error":
                    self.phase = "error"
                    self.error = status.get("message", "") + "\n" + self.tail_log()
                    self._send("stop")
        log_file.close()

    def _send(self, command):
        try:
            self.process.stdin.write(f"{command}\n".encode())
            self.process.stdin.flush()
        except (BrokenPipeError, OSError, AttributeError):
            pass

    def policy_checkpoints(self):
        # Oldest first; the page preselects the last entry, i.e. the newest checkpoint.
        found = sorted(TRAIN_ROOT.glob("*/checkpoints/[0-9]*/pretrained_model"), key=lambda p: p.stat().st_mtime)
        return [{"path": str(p), "label": f"{p.parts[-4]} · step {int(p.parts[-2])}"} for p in found]

    def gpu_free_mb(self):
        try:
            out = subprocess.run(["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
                                 capture_output=True, text=True, timeout=5).stdout
            return int(out.split()[0])
        except (OSError, ValueError, IndexError, subprocess.SubprocessError):
            return None

    def start_policy(self, data):
        with self.lock:
            if self.policy_process and self.policy_process.poll() is None:
                raise ValueError("A policy test is already running")
            if self.process and self.process.poll() is None:
                raise ValueError("Disconnect the arms from teleoperation before testing a policy")
            checkpoint = str(data.get("checkpoint", ""))
            if checkpoint not in {c["path"] for c in self.policy_checkpoints()}:
                raise ValueError("Choose a checkpoint")
            for cam in ("arm_cam", "scene_cam"):
                frame, stamp = self.hub.get(cam)
                if frame is None or time.time() - stamp > 3:
                    raise ValueError(f"{cam} has no live frames; the policy needs both cameras")
            remote = bool(data.get("remote"))
            free = None if remote else self.gpu_free_mb()
            if free is not None and free < POLICY_MIN_FREE_MB:
                raise ValueError(f"Only {free} MB of GPU memory free; stop training first (the policy needs about {POLICY_MIN_FREE_MB} MB)")
            args = [str(PYTHON), "-u", str(Path(__file__).parent / "eval_real.py"), "--checkpoint", checkpoint,
                    "--task", str(data.get("task") or self.task), "--seconds", str(float(data.get("seconds", 600))),
                    "--n-action-steps", str(int(data.get("n_action_steps", 6)))]
            if data.get("dry_run", True):
                args.append("--dry-run")
            if remote:
                # Model runs on the Jetson GPU (jetson/policy_server.py) so training can keep the laptop GPU.
                args += ["--remote", f"{JETSON_HOST}:{POLICY_SERVER_PORT}"]
            log_file = POLICY_LOG.open("wb", buffering=0)
            log_file.write(("$ " + " ".join(args) + "\n").encode())
            env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
            self.policy_process = subprocess.Popen(args, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                                   stderr=subprocess.STDOUT, start_new_session=True, env=env)
            self.policy = {"state": "starting", "dry_run": bool(data.get("dry_run", True)), "checkpoint": checkpoint,
                           "remote": remote}
            self.policy_error = ""
            threading.Thread(target=self.read_policy, args=(self.policy_process, log_file), daemon=True).start()
            return {"ok": True}

    def read_policy(self, process, log_file):
        for line in process.stdout:
            log_file.write(line)
            if line.startswith(b"@@ "):
                try:
                    status = json.loads(line[3:])
                except ValueError:
                    continue
                with self.lock:
                    if self.policy_process is process:
                        self.policy.update(status)
        code = process.wait()
        log_file.close()
        with self.lock:
            if self.policy_process is process:
                self.policy["state"] = "stopped"
                if code not in (0, -signal.SIGTERM):
                    try:
                        tail = POLICY_LOG.read_text(errors="replace").splitlines()[-6:]
                    except OSError:
                        tail = []
                    self.policy_error = f"Policy run exited with code {code}\n" + "\n".join(tail)

    def stop_policy(self):
        with self.lock:
            if not self.policy_process or self.policy_process.poll() is not None:
                return {"ok": True}
            self.policy["state"] = "stopping"
            self.policy_process.send_signal(signal.SIGTERM)
            return {"ok": True}

    def tail_log(self):
        try:
            return "\n".join(LOG.read_text(errors="replace").splitlines()[-8:])
        except OSError:
            return ""

    def probe_arms(self, ports, disarm=False):
        result = subprocess.run(
            [str(PYTHON), "-c", MOTOR_HELPER, *ports, "disarm" if disarm else "probe"],
            capture_output=True, text=True, timeout=15, env=os.environ.copy(),
        )
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or "Could not probe motor buses")
        return json.loads(result.stdout)

    def check_calibration(self, leader, follower):
        result = subprocess.run(
            [str(PYTHON), "-c", CALIBRATION_HELPER,
             leader, str(LEADER_CALIBRATION), "leader",
             follower, str(FOLLOWER_CALIBRATION), "follower"],
            capture_output=True, text=True, timeout=30, env=os.environ.copy(),
        )
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or "Could not read motor calibration")
        return json.loads(result.stdout)

    def _jetson_client(self, password=None):
        import paramiko

        client = paramiko.SSHClient()
        client.load_system_host_keys()
        if JETSON_KNOWN_HOSTS.exists():
            client.load_host_keys(str(JETSON_KNOWN_HOSTS))
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        client.connect(
            JETSON_HOST, username="kurat", password=password or self.jetson_password,
            look_for_keys=False, allow_agent=False, timeout=5, banner_timeout=5, auth_timeout=5,
        )
        return client

    def _remote_controls(self, password=None, settings=None):
        client = self._jetson_client(password)
        streams = []
        try:
            if settings:
                brightness = round(settings["brightness"] * 128 / 100 - 64)
                contrast = round(settings["contrast"])
                command = f"v4l2-ctl -d {SCENE_CAMERA} --set-ctrl=brightness={brightness},contrast={contrast}"
                stdin, stdout, stderr = client.exec_command(command, timeout=5)
                streams = [stdin, stdout, stderr]
                error = stderr.read().decode().strip()
                code = stdout.channel.recv_exit_status()
                if code:
                    raise RuntimeError(error or "RealSense controls failed")
                for stream in streams:
                    stream.close()
                streams = []
                command = f"v4l2-ctl -d {SCENE_CAMERA} --get-ctrl=brightness,contrast,gain"
            else:
                command = f"v4l2-ctl -d {SCENE_CAMERA} --get-ctrl=brightness,contrast,gain"
            stdin, stdout, stderr = client.exec_command(command, timeout=5)
            streams = [stdin, stdout, stderr]
            output = stdout.read().decode()
            error = stderr.read().decode().strip()
            code = stdout.channel.recv_exit_status()
            if code:
                raise RuntimeError(error or "RealSense controls failed")
            if settings:
                return read_v4l2_values(output)
            return read_v4l2_values(output)
        finally:
            for stream in streams:
                stream.close()
            client.close()

    def camera_status(self):
        arm_values = normalize_controls(read_v4l2(ARM_CAMERA), contrast_max=64, gain_max=100)
        scene_values = None
        if self.scene_controls_connected:
            try:
                scene_values = normalize_controls(self._remote_controls(), contrast_max=100, gain_max=128)
            except Exception as exc:
                self.scene_controls_connected = False
                raise RuntimeError(f"Jetson camera connection was lost: {exc}") from exc
        return {"arm": arm_values, "scene": scene_values, "scene_connected": self.scene_controls_connected}

    def connect_scene_controls(self, password):
        if not password:
            raise ValueError("Enter the Jetson password to connect its camera controls")
        values = self._remote_controls(password=password)
        self.jetson_password = password
        self.scene_controls_connected = True
        return normalize_controls(values, contrast_max=100, gain_max=128)

    def set_camera_controls(self, camera, settings):
        if camera not in ("arm", "scene"):
            raise ValueError("Unknown camera")
        controls = {}
        for name in ("brightness", "contrast", "gain"):
            value = settings.get(name)
            if not isinstance(value, (int, float)) or not 0 <= value <= 100:
                raise ValueError(f"{name} must be between 0 and 100")
            controls[name] = round(value)
        if camera == "arm":
            brightness = round(controls["brightness"] * 128 / 100 - 64)
            contrast = round(controls["contrast"] * 64 / 100)
            gain = controls["gain"]
            command = f"brightness={brightness},contrast={contrast},gain={gain}"
            result = subprocess.run(
                ["v4l2-ctl", "-d", ARM_CAMERA, f"--set-ctrl={command}"],
                capture_output=True, text=True, timeout=3,
            )
            if result.returncode:
                raise RuntimeError(result.stderr.strip() or "Wrist camera setting failed")
            return normalize_controls(read_v4l2(ARM_CAMERA), contrast_max=64, gain_max=100)
        if not self.scene_controls_connected:
            raise ValueError("Connect the Jetson camera controls first")
        values = self._remote_controls(settings=controls)
        return normalize_controls(values, contrast_max=100, gain_max=128)

    def status(self):
        with self.lock:
            now = time.time()
            feeds = {}
            for key, label in (("arm_cam", "Wrist camera"), ("scene_cam", "RealSense")):
                frame, stamp = self.hub.get(key)
                feeds[key] = {"name": label, "online": frame is not None and now - stamp < 2, "age": round(now - stamp, 1) if stamp else None}
            serials = arm_ports()
            return {
                "phase": self.phase,
                "active": self.process is not None and self.process.poll() is None,
                "runner": self.runner,
                "policy": {**self.policy, "active": self.policy_process is not None and self.policy_process.poll() is None,
                           "error": self.policy_error},
                "feeds": feeds,
                "depth": None if self.depth is None else {"online": self.depth.get(max_age_s=2) is not None,
                                                          "frames": self.depth.frames},
                "ports": serials,
                "leader_port": port_for_serial(LEADER_SERIAL),
                "follower_port": port_for_serial(FOLLOWER_SERIAL),
                "task": self.task,
                "uptime": int(now - self.started_at) if self.started_at else 0,
                "dataset": str(self.data_root),
                "arm_probe": self.arm_probe,
                "error": self.error,
                "log": self.tail_log(),
            }

    def start(self, data):
        with self.lock:
            if self.process and self.process.poll() is None:
                raise ValueError("A teleoperation session is already running")
            if self.policy_process and self.policy_process.poll() is None:
                raise ValueError("Stop the policy test before connecting the arms")
            follower = data.get("follower")
            leader = data.get("leader")
            if follower not in arm_ports() or leader not in arm_ports() or follower == leader:
                raise ValueError("Choose different connected ports for leader and follower")
            task = str(data.get("task", "")).strip()
            if not task:
                raise ValueError("Enter the task instruction for this dataset")
            if not all(os.path.exists(port) for port in (follower, leader)):
                raise ValueError("An arm port is no longer connected")
            missing_calibrations = [str(path) for path in (LEADER_CALIBRATION, FOLLOWER_CALIBRATION) if not path.is_file()]
            if missing_calibrations:
                raise ValueError("Calibrate both arms before connecting. Missing: " + ", ".join(missing_calibrations))
            self.arm_probe = self.probe_arms([leader, follower])
            expected_ids = set(range(1, 7))
            for role, port in (("Leader", leader), ("Follower", follower)):
                result = self.arm_probe.get(port, {})
                found = set(result.get("motors", []))
                if result.get("error") or found != expected_ids:
                    missing = sorted(expected_ids - found)
                    detail = f"{role} port {port} sees motor IDs {sorted(found)}"
                    if missing:
                        detail += f"; missing IDs {missing}"
                    if result.get("error"):
                        detail += f" ({result['error']})"
                    raise ValueError(detail)
            calibration = self.check_calibration(leader, follower)
            for role in ("leader", "follower"):
                result = calibration.get(role, {})
                if not result.get("matches"):
                    raise ValueError(
                        f"{role.title()} calibration on {result.get('port')} does not match its saved file. "
                        "No calibration was written. Confirm the arm-to-port assignment before continuing."
                    )
            leader_pose = calibration["leader"].get("positions", {})
            follower_pose = calibration["follower"].get("positions", {})
            pose_errors = {}
            for joint in ("shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"):
                if joint not in leader_pose or joint not in follower_pose:
                    continue
                delta = abs(float(leader_pose[joint]) - float(follower_pose[joint]))
                if joint in ("shoulder_pan", "wrist_roll"):
                    delta = min(delta, 360 - delta)
                limit = 15 if joint == "gripper" else 30
                if delta > limit:
                    pose_errors[joint] = round(delta)
            # Not blocking: teleop_runner eases the follower onto the leader's pose slowly
            # before switching to full-speed tracking.
            pose_warning = ""
            if pose_errors:
                details = ", ".join(f"{joint} {angle} degrees" for joint, angle in pose_errors.items())
                pose_warning = f"Pose offset at start ({details}); follower will move there slowly."
            for cam in ("arm_cam", "scene_cam"):
                frame, stamp = self.hub.get(cam)
                if frame is None or time.time() - stamp > 3:
                    raise ValueError(f"{cam} has no live frames; check the camera connection and stream")
            resume_dataset = False
            self.data_root = DATA_ROOT
            if DATA_ROOT.exists():
                info_path = DATA_ROOT / "meta/info.json"
                tasks_path = DATA_ROOT / "meta/tasks.parquet"
                has_episode_index = any(DATA_ROOT.glob("meta/episodes/chunk-*/file-*.parquet"))
                has_saved_episodes = False
                if info_path.is_file() and tasks_path.is_file() and has_episode_index:
                    try:
                        info = json.loads(info_path.read_text())
                        has_saved_episodes = int(info.get("total_episodes", 0)) > 0
                    except (OSError, ValueError, TypeError):
                        pass
                if has_saved_episodes:
                    resume_dataset = True
                elif not any(DATA_ROOT.iterdir()):
                    DATA_ROOT.rmdir()
                else:
                    suffix = int(time.time())
                    self.data_root = DATA_ROOT.with_name(f"{DATA_ROOT.name}_run_{suffix}")
                    while self.data_root.exists():
                        suffix += 1
                        self.data_root = DATA_ROOT.with_name(f"{DATA_ROOT.name}_run_{suffix}")
            self.task = task
            self.error = ""
            config = {
                "leader": leader, "follower": follower, "task": task, "fps": 10,
                "repo_id": f"local/{DATASET_NAME}", "root": str(self.data_root), "resume": resume_dataset,
                "depth_host": JETSON_HOST if RECORD_DEPTH else None,
            }
            args = [str(PYTHON), "-u", "-X", "faulthandler", str(Path(__file__).parent / "teleop_runner.py"), json.dumps(config)]
            log_file = LOG.open("wb", buffering=0)
            log_file.write(("$ " + " ".join(args) + "\n").encode())
            self.process = subprocess.Popen(args, cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
            self.runner = {}
            threading.Thread(target=self.read_runner, args=(self.process, log_file), daemon=True).start()
            self.phase = "connecting"
            self.started_at = time.time()
            return {"ok": True, "warning": pose_warning}

    def key(self, key):
        with self.lock:
            if not self.process or self.process.poll() is not None:
                raise ValueError("Arms are not connected")
            if key == "stop":
                self._send("stop")
                if self.phase == "connecting":
                    self.process.terminate()
                self.phase = "finishing"
                return {"ok": True}
            allowed = {"record": ("teleop",), "finish": ("recording",), "discard": ("recording",)}
            if key not in allowed:
                raise ValueError("Unknown command")
            if self.phase not in allowed[key]:
                raise ValueError({"record": "Wait until teleoperation is running before recording",
                                  "finish": "No episode is being recorded",
                                  "discard": "No episode is being recorded"}[key])
            self._send(key)
            self.phase = {"record": "recording", "finish": "saving", "discard": "teleop"}[key]
            return {"ok": True}

    def release_torque(self):
        with self.lock:
            if self.process and self.process.poll() is None:
                raise ValueError("End the active recording session before releasing torque")
            ports = arm_ports()
            result = self.probe_arms(ports, disarm=True)
            self.arm_probe = result
            return result

    def calibration_status(self, leader, follower):
        with self.lock:
            if self.process and self.process.poll() is None:
                raise ValueError("End the active session before checking motor calibration")
            if leader == follower or leader not in arm_ports() or follower not in arm_ports():
                raise ValueError("Select different connected leader and follower ports")
            result = self.check_calibration(leader, follower)
            leader_pose = result.get("leader", {}).get("positions", {})
            follower_pose = result.get("follower", {}).get("positions", {})
            differences = {}
            for joint in ("shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"):
                if joint not in leader_pose or joint not in follower_pose:
                    continue
                delta = abs(float(leader_pose[joint]) - float(follower_pose[joint]))
                if joint in ("shoulder_pan", "wrist_roll"):
                    delta = min(delta, 360 - delta)
                differences[joint] = round(delta)
            return {"calibration": result, "pose_differences": differences}


STATE = AppState()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def send_json(self, value, code=200):
        body = json.dumps(value).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/status":
            return self.send_json(STATE.status())
        if path == "/api/policy/checkpoints":
            return self.send_json({"checkpoints": STATE.policy_checkpoints(), "gpu_free_mb": STATE.gpu_free_mb()})
        if path == "/api/cameras":
            try:
                return self.send_json(STATE.camera_status())
            except Exception as exc:
                return self.send_json({"error": str(exc)}, 503)
        if path.startswith("/feed/"):
            name = path.rsplit("/", 1)[-1]
            if name not in ("arm_cam", "scene_cam"):
                return self.send_error(404)
            self.send_response(200)
            self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            last = None
            try:
                while True:
                    frame, stamp = STATE.hub.get(name)
                    if frame is not None and stamp != last:
                        self.wfile.write(b"--frame\r\nContent-Type: image/jpeg\r\nContent-Length: " + str(len(frame)).encode() + b"\r\n\r\n" + frame + b"\r\n")
                        self.wfile.flush()
                        last = stamp
                    time.sleep(0.05)
            except (BrokenPipeError, ConnectionResetError):
                return
        if path in ("/", "/index.html"):
            html = (Path(__file__).parent / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return self.wfile.write(html)
        self.send_error(404)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length) or b"{}")
            path = urlparse(self.path).path
            if path == "/api/start":
                result = STATE.start(data)
            elif path == "/api/arms/disarm":
                result = {"motors": STATE.release_torque()}
            elif path == "/api/arms/calibration":
                result = STATE.calibration_status(data.get("leader"), data.get("follower"))
            elif path == "/api/policy/start":
                result = STATE.start_policy(data)
            elif path == "/api/policy/stop":
                result = STATE.stop_policy()
            elif path == "/api/episode":
                result = STATE.key(data.get("action"))
            elif path == "/api/cameras/connect":
                result = {"scene": STATE.connect_scene_controls(data.get("password", "")), "scene_connected": True}
            elif path == "/api/cameras/settings":
                result = {"settings": STATE.set_camera_controls(data.get("camera"), data)}
            else:
                return self.send_error(404)
            self.send_json(result)
        except (ValueError, json.JSONDecodeError) as exc:
            self.send_json({"error": str(exc)}, 400)
        except Exception as exc:
            self.send_json({"error": str(exc)}, 500)


if __name__ == "__main__":
    print("SO-101 Episode Studio: http://127.0.0.1:8765", flush=True)
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        STATE.hub.running = False
        STATE.hub.thread.join(timeout=3)
        STATE.hub.socket.close(0)
