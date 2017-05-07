__author__ = 'Thomas Kaland'
# _*_ coding: utf-8 _*_

from Servo import Lid
from Led import Led
from Circuit import Magnet, Solution
from TellArduino import TellArduino
from Sound import Sound
import random
import time

TestMode = True

#Setter opp klasser til test2
led = Led([21,16,25,12,20]) #Setter opp klasse som styrer led-lys
test2Solution = Solution([11,9,10,24,23], [19,26],  [6,13], [3000,1000,2000,1000,500], 12)
test2Magnet = Magnet([8])
PossibleSolutions = [3,4,6]

#Setter opp klasser til test1
test1Solution = Solution([], [27, 17], [22, 5], [], 24)
test1Magnet = Magnet([7])

#Setter opp generelle klasser
Arduino = TellArduino('/dev/ttyACM0')

#Lydfiler:
Correct = Sound('correct.wav')
Powerup = Sound('powerup.wav')
Down = Sound('down.wav')
TooLittle = Sound('TooLittle.wav')
TooMuch = Sound('TooMuch.wav')
PARTYTYME = Sound('Talking.wav')


lid = Lid(18, 2)
lid.Open()
time.sleep(2) #Gi litt tid saa arduinoen faar startet opp.
lid.Close()


######################## PROGRAMSTART #######################
while TestMode:

    ######### INTRO ###############

    Arduino.ShowFace(5)
    Down.Play()
    time.sleep(1)
    Arduino.ShowFace(8)
    time.sleep(1)
    Arduino.StartStopBlink()
    Arduino.ShowFace(3)


    ######### TEST 1 ##############

    test1Magnet.On()

    while not(test1Solution.Exist()):
        print('No solution')
    print('Solution found')

    ######### INTRO TEST 2 ########

    Powerup.Play()
    Arduino.StartStopBlink()
    Arduino.ShowFace(6)
    time.sleep(5)

    ######### TEST 2 ###########

    ThisSolution = PossibleSolutions[random.randint(0,2)] #Velger en tilfeldig losning ut fra mulige losningslisten
    lid.Open()
    time.sleep(0.5) #Delay bare fordi da funka det
    test2Magnet.On()
    Arduino.ShowNumber(int(ThisSolution))
    Arduino.ShowFace(2)


    while True:

        coupledResistors = test2Solution.FindResistorNumbers()
        led.TurnOn(coupledResistors)


        if test2Solution.Exist():
            SolutionVoltage = test2Solution.Find()

            if SolutionVoltage == ThisSolution: #Hvis riktig losning
                Arduino.ShowFace(1)

                Correct.Play()
                Arduino.ShowFace(1)
                time.sleep(1)

                PARTYTYME.Play()
                time.sleep(0.5)
                led.Strobe(150)

                break


            elif SolutionVoltage > ThisSolution: #Hvis feil losning m. for mye spenning

                TooMuch.Play()
                Arduino.ShowFace(7)
                led.BlinkRandom(1)
                test2Magnet.Drop()
                Arduino.ShowFace(0)

            elif SolutionVoltage < ThisSolution: #Hvis feil losning m. for lite spenning

                TooLittle.Play()
                Arduino.ShowFace(5)
                time.sleep(1)
                test2Magnet.Drop()
                Arduino.ShowFace(2)


        led.Reset()

    time.sleep(10)




