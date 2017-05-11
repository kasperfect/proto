__author__ = 'Thomas Kaland'
# _*_ coding: utf-8 _*_

from Servo import Lid
from Led import Led
from Circuit import Magnet, Solution
from TellArduino import TellArduino
from Sound import Sound
import random
import time
from RPi import GPIO

GPIO.setmode(GPIO.BCM)

TestMode = False
Jazzmode = False
Salsamode = False

#Setter opp klasser til test2
led = Led([21,16,25,12,20]) #Setter opp klasse som styrer led-lys
test2Solution = Solution([11,9,10,24,23], [19,26],  [6,13], [3000,1000,2000,1000,500], 12)
test2Magnet = Magnet([8])
PossibleSolutions = [3,4,6]
lid = Lid(18, 2)

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

#Inputs/output fra/til skuffekontroll:
GPIO.setup((14,15), GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
interrupt = False

def Edgedetect(Channel): #Bakgrunnsprosess for interrupt naar resetknappen (Roed knapp) blir trykket inn
    time.sleep(0.01)
    if GPIO.input(15): #Sjekker input en gang til for aa sjekke om det er en ekte rising edge. Dette for aa filtrere ut falske inputs naar elektromagnetene blir startet
        print('Resetsignal funnet. Resetter spill...')
        lid.Close()
        global interrupt
        interrupt = True

GPIO.add_event_detect(15, GPIO.RISING, callback = Edgedetect)
GameDone = 4
GPIO.setup(GameDone, GPIO.OUT)
GPIO.output(GameDone, False)

################## PRETEST OG TEGN TIL PROGRAMSTART ##########

lid.Open()
time.sleep(5) #Gi litt tid saa arduinoen faar startet opp skikkelig
lid.Close()

################## BAKGRUNNSMUSIKK TIL JOBBING #####################

if Jazzmode: #Jazzmodus for folk som liker jazz og Whiplash-sangen
    jazz = Sound('Whiplash.wav')
    jazz.Play(-1)

if Salsamode: #Salsamode!!!!!!!!
    salsa = Sound('Salsa.wav')
    salsa.Play(-1)

################## RESET GAME OG GAMESTART FUNKSJON #######################

def Gamestart(): #Funksjon som returnerer verdien paa pin 14. Er bare saa koden blir litt lettere aa lese. Pin 14 er "start spill" knappen. Det er den hvite knappen bak til hoyre.
    return GPIO.input(14)

def ResetGame():
    test1Magnet.Off()
    test2Magnet.Off()
    Arduino.Mute()
    lid.Close()
    GPIO.output(GameDone, False)
    global interrupt
    interrupt = False


######################## PROGRAMSTART ###############################################################################

while True:

    while Gamestart() or TestMode:

        print('Gamestart!')

        Arduino.Mute() #Unmute Arduino

        ######### INTRO ###############

        Arduino.ShowFace(5)
        time.sleep(1)
        Down.Play()
        time.sleep(1)
        Arduino.ShowFace(7)
        time.sleep(1)
        Arduino.StartStopBlink()
        Arduino.ShowFace(3)


        ######### TEST 1 ##############

        test1Magnet.On()

        while not(test1Solution.Exist()) and not interrupt:
            pass
        print('Solution found')

        ######### INTRO TEST 2 ########

        Powerup.Play()
        Arduino.StartStopBlink()
        Arduino.ShowFace(6)
        time.sleep(5)

        ######### TEST 2 ###########

        ThisSolution = PossibleSolutions[random.randint(0,2)] #Velger en tilfeldig losning ut fra mulige losningslisten
        lid.Open()
        test2Magnet.On()
        Arduino.ShowNumber(int(ThisSolution))
        Arduino.ShowFace(2)


        while not interrupt:

            coupledResistors = test2Solution.FindResistorNumbers()
            led.TurnOn(coupledResistors)


            if test2Solution.Exist():
                SolutionVoltage = test2Solution.Find()

                if SolutionVoltage == ThisSolution: #Hvis riktig losning
                    Arduino.ShowFace(1)

                    Correct.Play()
                    Arduino.ShowFace(1)
                    lid.Close()
                    #time.sleep(0.5)

                    PARTYTYME.Play()
                    time.sleep(1)
                    led.Strobe(2, 20, 5)

                    GPIO.output(GameDone, True) #Gir signal til kontrollsystem at spillet er klart
                    break


                elif SolutionVoltage > ThisSolution: #Hvis feil losning m. for mye spenning

                    TooMuch.Play()
                    Arduino.ShowFace(7)
                    led.BlinkRandom(1)
                    test2Magnet.Drop()
                    Arduino.ShowFace(0)
                    time.sleep(0.5)
                    Arduino.ShowFace(2)

                elif SolutionVoltage < ThisSolution: #Hvis feil losning m. for lite spenning

                    TooLittle.Play()
                    Arduino.ShowFace(4)
                    led.Fade(coupledResistors)
                    test2Magnet.Drop()
                    Arduino.ShowFace(2)


            led.Reset()

        time.sleep(9)

        ############ RESET GAME ############
        print('Resetting')
        ResetGame()
        print('Game reset.')
        time.sleep(1)







