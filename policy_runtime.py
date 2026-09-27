"""Load a LeRobot chunking policy and turn one observation into one action chunk.

Used in-process by eval_real.py (laptop GPU) and by jetson/policy_server.py (Jetson GPU), so both paths
preprocess, run RTC and postprocess identically. RemotePolicy is the laptop-side client for the Jetson server
with the same interface.

infer(state, images, task, guide) -> (chunk, raw, timing)
  state   6 joint positions (degrees / gripper %)
  images  {"observation.images.cameraN": RGB uint8 (H, W, 3)}
  guide   None or {"left": normalized leftover of the current chunk from this observation on,
                   "inference_delay": steps that will run before the new chunk lands,
                   "execution_horizon": RTC guidance horizon}
  chunk   (T, 6) joint targets; raw (T, 6) the same chunk in the model's normalized space, kept for RTC
"""

import json
import os
import time

import numpy as np

CAMERA_STREAMS = {"camera1": "scene_cam", "camera2": "arm_cam"}  # dataset image key -> server.py ZMQ stream


class LocalPolicy:
    def __init__(self, checkpoint, device="cuda", rtc=True, rtc_horizon=6, rtc_max_guidance=10.0, bf16=False):
        import torch
        from lerobot.configs.policies import PreTrainedConfig
        from lerobot.policies.factory import get_policy_class, make_pre_post_processors

        try:
            import so101_policy  # noqa: F401  registers our own policy type (so101flow)
        except ImportError:
            pass

        self.torch = torch
        self.device = device
        self.bf16 = bf16
        cfg = PreTrainedConfig.from_pretrained(checkpoint)
        self.policy_type = cfg.type
        self.policy = get_policy_class(cfg.type).from_pretrained(checkpoint).to(device).eval()
        if not hasattr(self.policy, "predict_action_chunk"):
            raise ValueError(f"{cfg.type} has no predict_action_chunk; only chunking policies are supported")
        # SmolVLA does RTC through LeRobot's guidance processor; so101flow was trained for it (native_rtc)
        # and takes the same arguments directly.
        native = getattr(self.policy, "native_rtc", False)
        self.rtc = rtc and (native or hasattr(self.policy, "init_rtc_processor"))
        self.rtc_horizon = rtc_horizon
        if self.rtc and not native:
            from lerobot.policies.rtc.configuration_rtc import RTCConfig

            self.policy.config.rtc_config = RTCConfig(enabled=True, execution_horizon=rtc_horizon,
                                                      max_guidance_weight=rtc_max_guidance)
            self.policy.init_rtc_processor()
        if device.startswith("cuda") and hasattr(self.policy, "enable_cuda_graph") \
                and os.environ.get("SO101_CUDA_GRAPH", "1") != "0":
            self.policy.enable_cuda_graph()  # one launch per query instead of thousands (see GraphSampler)
        self.pre, self.post = make_pre_post_processors(
            policy_cfg=self.policy.config, pretrained_path=checkpoint,
            preprocessor_overrides={"device_processor": {"device": device}})
        wanted = [k for k in self.policy.config.input_features if k.startswith("observation.images.")]
        # e.g. SmolVLA's base config carries a camera3 slot this dataset never had; it skips absent images.
        self.skipped_cameras = [k for k in wanted if k.rsplit(".", 1)[-1] not in CAMERA_STREAMS]
        self.image_keys = [k for k in wanted if k not in self.skipped_cameras]
        if not self.image_keys:
            raise ValueError("None of the policy's camera inputs has a stream")

    def _sync(self):
        if self.device.startswith("cuda"):
            self.torch.cuda.synchronize()

    def infer(self, state, images, task, guide=None):
        torch = self.torch
        timing = {}
        t = time.perf_counter()
        batch = {"observation.state": torch.from_numpy(np.asarray(state, np.float32)).unsqueeze(0), "task": [task]}
        for key in self.image_keys:
            batch[key] = torch.from_numpy(images[key]).permute(2, 0, 1).unsqueeze(0).float() / 255
        x = self.pre(batch)
        self._sync()
        timing["pre"] = time.perf_counter() - t
        kwargs = {}
        if self.rtc and guide is not None and len(guide["left"]) > 0:
            kwargs = {"prev_chunk_left_over": torch.as_tensor(np.asarray(guide["left"], np.float32),
                                                              device=self.device),
                      "inference_delay": int(guide["inference_delay"]),
                      "execution_horizon": int(guide.get("execution_horizon") or self.rtc_horizon)}
        t = time.perf_counter()
        # RTC computes its guidance with autograd internally (it re-enables grad for that step).
        with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16, enabled=self.bf16):
            raw = self.policy.predict_action_chunk(x, **kwargs)
        self._sync()
        timing["model"] = time.perf_counter() - t
        t = time.perf_counter()
        chunk = self.post(raw.float()).squeeze(0).cpu().numpy().astype(np.float32)
        timing["post"] = time.perf_counter() - t
        return chunk, raw.detach().float().squeeze(0).cpu().numpy(), timing

    def reset(self):
        self.policy.reset()


class RemotePolicy:
    """Client for jetson/policy_server.py: same interface as LocalPolicy, the model runs on the Jetson."""

    def __init__(self, address, checkpoint, rtc=True, rtc_horizon=6, rtc_max_guidance=10.0, bf16=False,
                 timeout_s=300):
        import zmq

        self.zmq = zmq
        self.address = address
        self.warm_calls = 0  # the first CUDA calls on the Jetson compile and tune kernels (tens of seconds)
        self._connect()
        reply = self._call({"cmd": "load", "checkpoint": checkpoint, "rtc": rtc, "rtc_horizon": rtc_horizon,
                            "rtc_max_guidance": rtc_max_guidance, "bf16": bf16}, timeout_s=timeout_s)
        self.policy_type = reply["policy_type"]
        self.image_keys = reply["image_keys"]
        self.skipped_cameras = reply["skipped_cameras"]
        self.rtc = reply["rtc"]
        self.rtc_horizon = rtc_horizon

    def _connect(self):
        self.socket = self.zmq.Context.instance().socket(self.zmq.REQ)
        self.socket.setsockopt(self.zmq.LINGER, 0)
        self.socket.connect(f"tcp://{self.address}")

    def _call(self, header, frames=(), timeout_s=5.0):
        self.socket.send_multipart([json.dumps(header).encode(), *frames])
        if not self.socket.poll(int(timeout_s * 1000)):
            # A REQ socket that missed its reply can't send again; start a fresh one for the next call.
            self.socket.close()
            self._connect()
            raise TimeoutError(f"Jetson policy server at {self.address} did not answer in {timeout_s:.0f}s")
        reply = json.loads(self.socket.recv())
        if "error" in reply:
            raise RuntimeError(f"Jetson policy server: {reply['error']}")
        return reply

    def infer(self, state, images, task, guide=None):
        import cv2

        t = time.perf_counter()
        frames = []
        for key in self.image_keys:
            ok, jpg = cv2.imencode(".jpg", cv2.cvtColor(images[key], cv2.COLOR_RGB2BGR),
                                   [cv2.IMWRITE_JPEG_QUALITY, 95])
            frames.append(jpg.tobytes())
        header = {"cmd": "infer", "state": [float(v) for v in state], "task": task,
                  "guide": None if guide is None else {**guide, "left": np.asarray(guide["left"]).tolist()}}
        encode = time.perf_counter() - t
        reply = self._call(header, frames, timeout_s=5.0 if self.warm_calls >= 2 else 300.0)
        self.warm_calls += 1
        total = time.perf_counter() - t
        timing = {k: v for k, v in reply["timing"].items()}
        timing["net"] = total - encode - sum(timing.values())
        timing["encode"] = encode
        return (np.asarray(reply["chunk"], np.float32), np.asarray(reply["raw"], np.float32), timing)

    def reset(self):
        self._call({"cmd": "reset"})
