"""Save the D435i factory calibration (depth + colour intrinsics, depth->colour extrinsics, depth scale)."""
import json, sys
import pyrealsense2 as rs

W, H = 640, 480
dev = rs.context().query_devices()[0]
out = {"serial": dev.get_info(rs.camera_info.serial_number), "firmware": dev.get_info(rs.camera_info.firmware_version)}
profiles = {}
for s in dev.query_sensors():
    if s.is_depth_sensor():
        out["depth_scale"] = s.as_depth_sensor().get_depth_scale()
    for p in s.get_stream_profiles():
        v = p.as_video_stream_profile()
        if v.width() == W and v.height() == H and p.stream_type() in (rs.stream.depth, rs.stream.color):
            profiles.setdefault(str(p.stream_type()).split(".")[-1], v)
for name, v in profiles.items():
    i = v.get_intrinsics()
    out[name] = {"width": i.width, "height": i.height, "fx": i.fx, "fy": i.fy, "cx": i.ppx, "cy": i.ppy,
                 "model": str(i.model), "coeffs": list(i.coeffs)}
e = profiles["depth"].get_extrinsics_to(profiles["color"])
out["depth_to_color"] = {"rotation": list(e.rotation), "translation": list(e.translation)}
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(json.dumps(out, indent=1))
