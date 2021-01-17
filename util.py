import cv2
from pynput.mouse import Button, Controller
from math import hypot

# measure how far the head tilt is from the initial position
def measureTiltDistance(initialPosition, currentPosition, scale):
    # words = ["left", "top"]
    difference = [0,0]
    for i in range(0, 2):
        # print("Current distance is " + str(initialPosition[i] - currentPosition[i]) + " from the " + words[i])
        difference[i] = (currentPosition[i] - initialPosition[i])/5
        if (difference[i] > -scale and difference[i] < scale):
            difference[i] = 0
    return difference

# functions used to detect blinking
font = cv2.FONT_HERSHEY_COMPLEX
blink_ratio = 0.21

def midpoint(p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def get_eye_ratio(eye_points, facial_landmarks):

    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - left_point[1]))
    ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = ver_line_length/hor_line_length

    return ratio

def detectBlink(left_ratio, right_ratio):
    if left_ratio < blink_ratio and right_ratio > blink_ratio:
        # left blink
        return -1
    if right_ratio < blink_ratio and left_ratio > blink_ratio:
        # right blink
        return 1
    else:
        return 0
