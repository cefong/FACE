# FACE
fully accessible controller emulator

# Dependencies
This project requires Python 3.7 interpreter, as well as opencv-python, dlib, SpeechRecognition, and pynput packages to be installed

# To run this project
1. `git clone https://github.com/cefong/FACE.git`
2. `cd ./FACE`
3. `python faceTracker.py`

# To use the controller emulator

## Calibration
Before you can use the controller emulator to control the keyboard and mouse input, you need to mark the neutral position of your face in the screen. This can be done either by positioning your face and hitting the space bar, or by holding both eyes closed for 5-10 seconds. After the neutral position is calibrated, you should see a dark blue box, indicating the neutral position of your face, and a light blue box within it that will be used for special controls. 

## Mouse input
To control the position of the mouse pointer on the screen, simply tilt your head in the direction you wish to go. For example, to bring the mouse pointer upwards you would tilt your head back (you should see the green box that tracks the current position of your head move up). 

To control clicking, wink using your left eye (and hold for approx. 2-3 seconds) to produce a single left click. If you move the red dot on the corner of your left eye into the light blue box and wink using your left eye, you will produce a double left click. Similarily, if you wink with your right eye you will produce a right click

## Keyboard input
To start keyboard input, open your mouth and hold for 2-3 seconds. The screen streaming live face tracking should stop, which indicates that the program is ready to receive audio input. Speak loudly and clearly what you intend to type and wait a few seconds after you have finished for the text to appear. If you require the use of the 'Enter' button to make a search, simply open your mouth again and say just the word 'Enter', and voila! The computer will register an 'Enter' button press.
