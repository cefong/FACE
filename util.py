import cv2
from pynput.mouse import Button, Controller
from pynput.keyboard import Controller as keyboardController
import speech_recognition as sr

from math import hypot

# measure how far the head tilt is from the initial position
def measureTiltDistance(initialPosition, currentPosition, scale):
    difference = [0,0]
    # tilt left
    difference[0] = (currentPosition[0] - initialPosition[0])/10
    if (difference[0] > -scale and difference[0] < scale):
        difference[0] = 0

    # tilt top
    difference[1] = (currentPosition[1] - initialPosition[1])/7
    if (difference[0] > -(scale+2) and difference[0] < (scale-2)):
        difference[0] = 0
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
    if left_ratio < blink_ratio and right_ratio < blink_ratio:
        return (1, 0)
    if left_ratio < blink_ratio and right_ratio > blink_ratio:
        # left blink
        return (0, -1)
    if right_ratio < blink_ratio and left_ratio > blink_ratio:
        # right blink
        return (0, 1)
    else:
        # blink--
        return (0, 0)

# function to detect mouth ratio
def get_mouth_ratio(mouth_points, facial_landmarks):

    center_top = (facial_landmarks.part(mouth_points[2]).x, facial_landmarks.part(mouth_points[2]).y)
    center_bottom = (facial_landmarks.part(mouth_points[6]).x, facial_landmarks.part(mouth_points[6]).y)
    left_point = (facial_landmarks.part(mouth_points[0]).x, facial_landmarks.part(mouth_points[0]).y) 
    right_point = (facial_landmarks.part(mouth_points[4]).x, facial_landmarks.part(mouth_points[4]).y)

    hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = ver_line_length/hor_line_length
    return ratio

def detect_mouth_open(mouth_ratio):

    if mouth_ratio > 0.7:
        return 1

    return 0
