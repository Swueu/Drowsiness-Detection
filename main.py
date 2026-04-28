import cv2
import time
import winsound
import os

# Haar cascades
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml'
)

# Camera start
cap = cv2.VideoCapture(0)

eye_closed_frames = 0
last_alarm_time = 0

# 🔥 ALWAYS CORRECT PATH (MAIN FIX)
sound_path = os.path.join(os.path.dirname(__file__), "alarm.wav")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    eyes_detected = 0

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)

        eyes_detected = len(eyes)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

    # Logic
    if eyes_detected == 0:
        eye_closed_frames += 1
    else:
        eye_closed_frames = 0

    # Alert condition
    if eye_closed_frames > 20:
        cv2.putText(frame, "DROWSY ALERT!", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 3)

        # 🔊 SAFE SOUND PLAY (NO ERROR EVER)
        if time.time() - last_alarm_time > 3:
            if os.path.exists(sound_path):
                winsound.PlaySound(sound_path, winsound.SND_FILENAME)
            else:
                print("❌ alarm.wav missing in folder!")
            last_alarm_time = time.time()

    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()