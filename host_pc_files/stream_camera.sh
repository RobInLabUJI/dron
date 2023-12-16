#!/usr/bin/env bash
sudo gst-launch-1.0 -v playbin uri=rtsp://192.168.0.104:8900/live uridecodebin0::source::latency=150
