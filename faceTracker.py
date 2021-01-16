import cv2
import numpy as np
import dlib
from pynput.mouse import Button, Controller
from util import measureTiltDistance

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor  = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# set the initial position to start from
initialPosition = [0, 0, 0, 0]

# set the mouse controller
mouse = Controller()

# set scale of stillbox
scale = 5

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    if len(faces) > 0:
        face = faces[0]
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        currentPosition = [x1, y1, x2, y2]

        if (initialPosition != [0, 0, 0, 0]):
            cv2.rectangle(frame, (initialPosition[0] - scale, initialPosition[1] + scale), (initialPosition[2] - scale, initialPosition[3] + scale), (255, 0, 0), 3)
            difference = measureTiltDistance(initialPosition[:2], currentPosition[:2], scale)
            mouse.move(difference[0], difference[1])


        cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 255, 0), 3)

        landmarks = predictor(gray, face)

        for i in range(0, 68):
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 32:
        initialPosition = [x1, y1, x2, y2]
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
