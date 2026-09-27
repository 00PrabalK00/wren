#!/usr/bin/env bash
# Stream the RealSense colour camera to the laptop as RTP JPEG (received by server.py's CameraHub).
# Finds the colour node by its YUYV format, so it survives /dev/video renumbering.
set -euo pipefail
LAPTOP=${LAPTOP_HOST:-10.42.0.1}
for dev in /dev/v4l/by-id/*RealSense*-video-index* /dev/v4l/by-path/*-video-index*; do
  node=$(readlink -f "$dev")
  if v4l2-ctl -d "$node" --info 2>/dev/null | grep -q RealSense && \
     v4l2-ctl -d "$node" --list-formats 2>/dev/null | grep -q "'YUYV'"; then
    echo "RealSense colour on $node -> $LAPTOP:5001"
    exec gst-launch-1.0 v4l2src device="$node" ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert \
      ! video/x-raw,format=I420 ! jpegenc quality=85 ! rtpjpegpay ! udpsink host="$LAPTOP" port=5001
  fi
done
echo "RealSense colour camera not found" >&2
exit 1
