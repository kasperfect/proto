__author__ = 'Thomas Kaland'
# _*_ coding: utf-8 _*_
from RPi import GPIO
import time
GPIO.VERBOSE = True

class Magnet:
    '''Klasse som styrer elektromagneter. Tar inn en liste med porter som magnetene er koblet inn i, Magnet([port1, port2])'''
    GPIO.setmode(GPIO.BCM)  # set up GPIO using BCM numbering

    def __init__(self, ports):
        """Setter opp portnummerering til magneter og gjør disse til OUTPUT med PULL-DOWN-resistor"""

        self.ports = ports
        for i in range(len(self.ports)):
            GPIO.setup(self.ports[i],GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)

    def Drop(self):
        """Objekt som skrur av og på magnetene"""
        self.Off()
        time.sleep(0.5)
        self.On()

    def On(self):
        """Objekt som skrur på alle magneter"""
        for i in range(len(self.ports)):
            GPIO.output(self.ports[i], True)

    def Off(self):
        """Objekt som skrur av alle magneter"""
        for i in range(len(self.ports)):
            GPIO.output(self.ports[i], False)

class Solution:
    """Klasse som sjekker om oppgaven er utført korrekt. Tar inn tre lister med porter, porter til resistor og porter til kablene (self.NB (North Bridge) og self.SB (South Bridge))"""

    def __init__(self, resistorinputs, NBInputs, SBInputs, resistorvalue, bateryvoltage):
        self.resistors = resistorinputs
        self.value = resistorvalue
        self.NB = NBInputs
        self.SB = SBInputs
        self.voltage = bateryvoltage

        for i in range(len(self.SB)):
            GPIO.setup(self.SB[i], GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)

        for i in range(len(self.NB)):
            GPIO.setup(self.NB[i], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        for i in range(len(self.resistors)):
            GPIO.setup(self.resistors[i], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    def Exist(self):
        """Objekt som sjekker om det er utført en løsning til problemet/oppgaven. Returnerer True hvis ja, False ellers"""
        paths = []

        for i in range(len(self.SB)):
            GPIO.output(self.SB[i], True)

            for j in range(len(self.NB)):
                if GPIO.input(self.NB[j]):
                    paths.append(self.NB[i])

            GPIO.output(self.SB[i], False)

        if len(paths) == len(self.SB)**len(self.NB):
            return True
        else:
            return False

    def Find(self):
        """Objekt som sjekker om den utførte løsingen er korrekt. Returnerer True hvis ja, False ellers"""

        resistors = self.FindResistors()

        return (resistors[1]/(resistors[0] + resistors[1]))*self.voltage

    def FindResistors(self):
        """Objekt som sjekker hvilke motstander som er koblet inn"""
        resistors = []
        for i in range (len(self.SB)):
            GPIO.output(self.SB[i], True)

            for j in range (len(self.resistors)):
                if GPIO.input(self.resistors[j]):
                    resistors.append(self.value[j])
            GPIO.output(self.SB[i], False)

        return resistors



#########TESTKODE#########


MagneterTest1 = Magnet([1])
Løsning = Solution([1, 2], [3], [6, 5], [1000, 2000], 12)
print(MagneterTest1.__doc__)
print(Løsning.__doc__)

MagneterTest1.On()
MagneterTest1.Drop()
MagneterTest1.Off()

print("Run Løsning.Is()")
print(Løsning.Exist())
print(Løsning.Find())





