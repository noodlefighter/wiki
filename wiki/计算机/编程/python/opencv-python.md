# opencv-python



## opencv打开RTSP流

```
import cv2

cap = cv2.VideoCapture('rtsp://192.168.8.1:7070')
cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)  # 不缓存帧，减小延迟

while cap.isOpened():
    pressed_key = cv2.waitKey(1)

    _, frame = cap.read()
    cv2.imshow("Live Feed", frame)

    if pressed_key == 27: # ESC Key
        break

cv2.destroyAllWindows()
cap.release()
```



