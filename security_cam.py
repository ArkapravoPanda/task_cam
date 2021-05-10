import cv2, time, os
from playsound import playsound
import threading

def testDevice(source):
   cam = cv2.VideoCapture(source) 
   if cam is None or not cam.isOpened():
       print('Warning: unable to open video source: ', source)
       return source

#Saves the incorrect device number to a. Then we do not(a) to find
#the correct device number
a = testDevice(0)
a = testDevice(1)

cam = cv2.VideoCapture(int(not(a)))
while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    _, thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame1, contours, -1, (0,255,0),2)
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x,y), (x+w, y+h), (0, 255, 0), 2)

        threading.Thread(target=playsound, args=('alert.wav',), daemon=True).start()
       

    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow('Task Cam-press q to stop', frame1)
    time.sleep(0.2)
