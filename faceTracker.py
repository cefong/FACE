import cv2
import dlib

from util import *

# sets the video capture to the built in webcam
cap = cv2.VideoCapture(0)

# gets the face detector from dlib
detector = dlib.get_frontal_face_detector()
predictor  = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# set the initial position to start from
initialPosition = [0, 0, 0, 0]
initialLength = 0

# set the mouse controller
mouse = Controller()

# set scale of stillbox
scale = 8

# set the starting point of the frequency calculator
side = 0
blink = 0
mouth = 0

# infinite loop keeps generating new frames
while True:

    # gets the current frame from the video capture
    _, frame = cap.read()

    # flip the fram so it mirrors the user
    frame = cv2.flip(frame, 1)

    # grayscale the image (since face detector detects better in grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect face
    faces = detector(gray)

    # only let one face control the computer interface
    if len(faces) > 0:
        face = faces[0]

        # get the boundaries of the face detected
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        # the current position of the face provides these parameters
        currentPosition = [x1, y1, x2, y2]

        # draw a rectangle around the face that is being used for controls
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 255, 0), 3)

        # calculate 68 facial landmarks
        landmarks = predictor(gray, face)

        # draw a dot on the landmark being tracked for the double-click box
        x = landmarks.part(36).x
        y = landmarks.part(36).y
        cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)

        # numbers 36 - 41 depict the points associated with the left eye
        left_ratio = get_eye_ratio([36, 37, 38, 39, 40, 41], landmarks)

        # numbers 42 - 47 depict right eye points
        right_ratio = get_eye_ratio([42, 43, 44, 45, 46, 47], landmarks)
        ratio_average = (right_ratio + left_ratio)/2

        # numbers 49 - 56 depict inner mouth points
        mouth_ratio = get_mouth_ratio([49,50,51,52,53,54,55,56], landmarks)

       #if mouth_ratio > 0.7:
        #        cv2.putText(frame, "MOUTH OPEN.", (300, 300), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0))
        mouthInc = detect_mouth_open(mouth_ratio)
        mouth = max(0, mouthInc + mouth)

        # if there have been over 3 mouth triggers
        if mouth > 3:
            r = sr.Recognizer()
            keyboard = keyboardController()
            with sr.Microphone() as source:
                cv2.putText(frame, "Talk.", (300, 300), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0))
                audio_text = r.listen(source)
                cv2.putText(frame, "Time's Up.", (300, 300), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0))

            try:
                # using google speech recognition
                if r.recognize_google(audio_text) == 'enter':
                    keyboard.type('\n')
                else:
                    keyboard.type(r.recognize_google(audio_text))
            except:
                print("Sorry, I did not get that")
            mouth = 0

        # calculate the amount to increment blink and side triggers
        blinkInc, sideInc = detectBlink(left_ratio, right_ratio)
        blink = max(0, blinkInc + blink)

        # only do facial tilt calculations after calibration of initial postiion has been done
        if (initialPosition != [0, 0, 0, 0]):
            cv2.rectangle(frame, (initialPosition[0] - scale, initialPosition[1] + scale), (initialPosition[2] - scale, initialPosition[3] + scale), (255, 0, 0), 3)

            # draw rectangle for double click area
            quarter = 3*int(initialLength/4)
            cv2.rectangle(frame, (initialPosition[0] - scale, initialPosition[1] + scale), (initialPosition[2] - quarter, initialPosition[3] + scale), (255, 255, 0), 3)

            # move the mouse according to the relative distance of the current position of the head to the calibrated
            # initial position
            difference = measureTiltDistance(initialPosition[:2], currentPosition[:2], scale)
            mouse.move(difference[0], difference[1])
            side += sideInc

            # if the side is more negative it indicates a likely left wink (which maps to a left click)
            if side < -2:
                # if the left eye landmark is in the double click box, register a double click when they wink
                if (landmarks.part(36).x > initialPosition[0] - scale and landmarks.part(36).x < initialPosition[2] - quarter):
                    mouse.click(Button.left, 2)
                    cv2.putText(frame, "Double left click.", (100,100), font, 2, (0, 0, 255), 5)
                # register a normal single left click if they left eye landmark is not in the double click box
                else:
                    mouse.press(Button.left)
                    mouse.release(Button.left)
                    cv2.putText(frame, "Left click.", (100,100), font, 2, (0, 0, 255), 5)
                side = 0
            # if the side is more positive it indicates a likely right wink (maps to a right click)
            if side > 7:
                mouse.press(Button.right)
                mouse.release(Button.right)
                side = 0
                cv2.putText(frame, "Right Blink.", (200,200), font, 2, (255, 0, 0), 5)
        # if the blink has been triggered over 25 times, register a new calibrated initial position to measure facial tilt from
        if blink > 25:
            blink = 0
            cv2.putText(frame, "Blinking.", (150,350), font, 2, (0, 255, 0), 5)
            initialPosition = [x1, y1, x2, y2]
            initialLength = x2 - x1

    # show the frame on a window
    cv2.imshow("Frame", frame)

    # register a key
    key = cv2.waitKey(1)

    # if the spacebar is hit, trigger a new calibarated intial position
    if key == 32:
        initialPosition = [x1, y1, x2, y2]
        initialLength = x2 - x1

    # if the esc key is hit, trigger the exit of the program
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
