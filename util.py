from pynput.mouse import Button, Controller

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
