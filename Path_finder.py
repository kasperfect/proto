__author__ = 'Thomas Kaland'
# _*_ coding: utf-8 _*_
from RPi import GPIO

def PiEmu (input, check):

    Relations = [[1],[5,6],[],[],[],[9],[],[10],[]]

    if(check in Relations[input]):
        return True
    else:
        return False

GPIO.setmode(GPIO.BCM) #set up GPIO using BCM numbering

GPIO.VERBOSE = True

IO = [       #List of Inputs/outputs and where they are
    1, #IO 1
    2, #IO 2
    3, #IO 3
    4, #IO 4
    5, #IO 5
    6, #IO 6
    7, #IO 7
    8 ]#IO 8


Start = 0   #Start-pin
Goal = 9   #Goal-pin
Goal_2 = 10

def find_path(Start, checkpoint, goal, path = []): #Function to find game-path. Returns list with path, empty list if direct path and False if no path.

    GPIO.setup(Start, GPIO.OUT)
    GPIO.output(Start, GPIO.HIGH) #Sets Start as an output, and brings it to High state
    GPIO.setup(checkpoint, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #sets all checkpoint to inputs with pulldown resistor
    GPIO.setup(goal, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    if GPIO.output(goal):
        return path

    for i in range(len(checkpoint)):

        if GPIO.input(checkpoint[i]):
            path.append(checkpoint[i])
            checkpoint.remove(checkpoint[i])

            find_path(checkpoint[i], checkpoint, goal, path)
            break
    return False

print(find_path(Start, IO, Goal))
