## Captura de vídeo en un "pipeline" con python

Se debe verificar que la librería openCV cuenta con soporte de la librería "Gstreamer pipeline":
```
> import cv2

> print(cv2.getBuildInformation())

```

El output debería tener la siguiente línea:
```
Video I/O:
    DC1394:                      YES (2.2.5)
    FFMPEG:                      YES
      avcodec:                   YES (58.54.100)
      avformat:                  YES (58.29.100)
      avutil:                    YES (56.31.100)
      swscale:                   YES (5.5.100)
      avresample:                YES (4.0.0)
    GStreamer:                   YES (1.16.2)
    PvAPI:                       NO
    v4l/v4l2:                    YES (linux/videodev2.h)


```


