__author__ = 'Thomas Kaland'
# _*_ coding: utf-8 _*_

from RPi import GPIO
import random
import time
GPIO.setmode(GPIO.BCM)

class Led:
    """Klasse som styrer led-lysene under hver motstand"""

    def __init__(self, ports):
        """Setter opp gpio-portene til led-lysene til output. Ledportene maa tilsvare led-nummer i ROBO"""

        self.leds = ports
        GPIO.setup(self.leds, GPIO.OUT)

    def TurnOn(self, Lednr):
        """Skrur paa led-lys. Tar inn liste med lys-nr. Ikke portnummerering, men led-nr. 0 er forste til venstre inni ROBO, 5 er siste til hoyre."""
        for i in range(len(Lednr)):
            GPIO.output(self.leds[Lednr[i]], True)

    def TurnOff(self, Lednr):
        """Skrur av led-lys. Tar inn liste med lys-nr. Ikke portnummerering, men led-nr. 0 er forste til venstre inni ROBO, 5 er siste til hoyre."""
        for i in range(len(Lednr)):
            GPIO.output(self.leds[Lednr[i]], False)

    def BlinkRandom(self, Time, Delay = 0.03 ):
        """Skrur av og paa led-lysene i tilfeldig rekkefolge og ganger. Tar inn int med hvor lenge den skal holde paa i sekund"""
        for i in range(int(Time/Delay)):
            for j in range(len(self.leds)):
                randLed = random.randint(0, len(self.leds)-1) #Itererer seg igjennom led-lysene og skrur paa tilfeldige leds
                self.TurnOn([randLed])
                randLed = random.randint(0, len(self.leds)-1) #Itererer seg igjennom led-lysene og skrur av tilfeldige leds
                self.TurnOff([randLed])
            time.sleep(Delay)

    def Strobe(self, Times):
        """Lager rave!!!!!!!"""

        for i in range(int(Times)):
            self.TurnOn([0,1,2,3,4])
            time.sleep(0.025)
            self.TurnOff([0,1,2,3,4])
            time.sleep(0.05)

    def Reset(self):
        """Skur alle led-lysene av"""
        GPIO.output(self.leds, False)

