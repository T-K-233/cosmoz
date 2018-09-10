import cv2

url = 'rtsp://192.168.1.10:554/user=admin&password=&channel=1&stream=0.sdp?real_stream--rtp-caching=100'
cap = cv2.VideoCapture(url)

while True:
    ret, img = cap.read()
    cv2.imshow('Robot Cam 0', img)
    key = cv2.waitKey(1)
