import cv2
import numpy as np
import dlib

from util import *

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor  = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# set the initial position to start from
initialPosition = [0, 0, 0, 0]

# set the mouse controller
mouse = Controller()

# set scale of stillbox
scale = 5

# set the max size of the buffer
side = 0

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

        # numbers 36 - 41 depict the points associated with the left eye
        left_ratio = get_eye_ratio([36, 37, 38, 39, 40, 41], landmarks)

        # numbers 42 - 47 depict right eye points
        right_ratio = get_eye_ratio([42,43, 44, 45, 46, 47], landmarks)
        ratio_average = (right_ratio + left_ratio)/2

        side += detectBlink(left_ratio, right_ratio)

        if side < -10:
            mouse.press(Button.left)
            mouse.release(Button.left)
            side = 0
            # cv2.putText(frame, "Left Blink.", (100,100), font, 2, (0, 0, 255), 5)
        if side > 10:
            mouse.press(Button.right)
            mouse.release(Button.right)
            side = 0
            # cv2.putText(frame, "Right Blink.", (200,200), font, 2, (255, 0, 0), 5)
        #if left_ratio < blink_ratio and right_ratio < blink_ratio:
            #cv2.putText(frame, "Blinking.", (150,350), font, 2, (0, 255, 0), 5)
    '''
        for i in range(0, 68):
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
    '''
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 32:
        initialPosition = [x1, y1, x2, y2]
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
