import cv2
import time
import serial

ser = serial.Serial('COM7', 9600)  
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

eyes_closed = False
eyes_closed_start_time = 0
eyes_closed_duration = 0
threshold_time = 3  

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 5)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        
        if len(eyes) == 0:
            if not eyes_closed:
                eyes_closed_start_time = time.time()
                eyes_closed = True
            else:
                eyes_closed_duration = time.time() - eyes_closed_start_time
                if eyes_closed_duration > threshold_time:
                    print("Eyes closed! Activating buzzer until eyes open.")
                    ser.write(b'1')  
        else:  
            if eyes_closed:
                print("Eyes open. Deactivating buzzer.")
                ser.write(b'0')  
            eyes_closed = False  
            eyes_closed_duration = 0  
        
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
ser.close()

