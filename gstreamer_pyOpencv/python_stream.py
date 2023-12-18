#!/usr/bin/env python
import cv2
import numpy as np
from multiprocessing import process

def receive():
    #cap = cv2.VideoCapture(f'rtsp://192.168.0.104:8900/live',cv2.CAP_GSTREAMER)
    cap = cv2.VideoCapture("rtspsrc location=rtsp://192.168.0.104:8900/live latency=150 ! decodebin ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1",cv2.CAP_GSTREAMER)


    while True:
        ret,frame = cap.read()
        if not ret:
            print('empty frame')
            continue

        cv2.imshow('receive', frame)
        if cv2.waitKey(1)&0xFF == ord('q'):
            break

    cap.release()


if __name__=='__main__':
    #pipeline = "udpsrc port=8900/live ! application/x-rtp,payload=96,encoding-name=H265 ! rtpjitterbuffer mode=1 ! rtph265depay ! h265parse ! decodebin ! videoconvert ! appsink drop=1"
    #pipeline = "uridecodebin uri=rtsp://192.168.0.104:8900/live ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1 "
    #pipeline = "uridecodebin uri=rtsp://192.168.0.104:8900/live "
   # pipeline = "rtspsrc location=rtsp://192.168.0.104:8900/live default-rtsp-version=32 ! application/x-rtp,media=video,encoding-name=H264 ! rtpjitterbuffer latency=1000 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1"
    #pipeline = "rtspsrc location=rtsp://192.168.0.104:8900/live ! queue max-size-buffers=2 ! rtph265depay ! h265parse ! decodebin ! autovideosink sync=false"
    receive()

