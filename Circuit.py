__author__ = 'Thomas Kaland'
# -*- coding: utf-8 -*-
from RPi import GPIO
import time
import math

GPIO.VERBOSE = True
GPIO.setmode(GPIO.BCM)  # set up GPIO using BCM numbering

class Magnet:
    '''Klasse som styrer elektromagneter. Tar inn en liste med porter som magnetene er koblet inn i, Magnet([port1, port2])'''

    def __init__(self, ports):
        """Setter opp portnummerering til magneter og gjor disse til OUTPUT"""

        self.ports = ports
        for i in range(len(self.ports)):
            GPIO.setup(self.ports[i],GPIO.OUT)

    def Drop(self):
        """Objekt som skrur av og paa magnetene"""
        self.Off()
        time.sleep(0.5)
        self.On()

    def On(self):
        """Objekt som skrur paa alle magneter"""
        for i in range(len(self.ports)):
            GPIO.output(self.ports[i], True)

    def Off(self):
        """Objekt som skrur av alle magneter"""
        for i in range(len(self.ports)):
            GPIO.output(self.ports[i], False)

class Solution:
    """Klasse som sjekker om oppgaven er utfort korrekt. Tar inn tre lister med porter, porter til resistor og porter til kablene (self.NB (North Bridge) og self.SB (South Bridge))"""

    def __init__(self, resistorinputs, NBInputs, SBInputs, resistorvalue, bateryvoltage):
        self.resistors = resistorinputs
        self.value = resistorvalue
        self.NB = NBInputs
        self.SB = SBInputs
        self.voltage = bateryvoltage

        for i in range(len(self.SB)):
            GPIO.setup(self.SB[i], GPIO.OUT)

        for i in range(len(self.NB)):
            GPIO.setup(self.NB[i], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        for i in range(len(self.resistors)):
            GPIO.setup(self.resistors[i], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    def ExistNoFilter(self):
        """Objekt som sjekker om det er utfort en losning til problemet/oppgaven. Returnerer True hvis ja, False ellers"""
        paths = []

        for i in range(len(self.SB)):
            GPIO.output(self.SB[i], True)

            for j in range(len(self.NB)):
                if GPIO.input(self.NB[j]):
                    paths.append(self.NB[j])

            GPIO.output(self.SB[i], False)

        if len(paths) == len(self.SB):
            return True
        else:
            return False

    def Find(self):
        """Objekt som sjekker om den utforte losingen er korrekt. Returnerer """

        resistors = self.FindResistors()
        Voltage_2 = math.fsum(resistors[1])
        Voltage_2 /=math.fsum(resistors[0])+math.fsum(resistors[1])
        Voltage_2 *= self.voltage

        return Voltage_2

    def FindResistors(self):
        """Objekt som sjekker hvilke motstander som er koblet inn og returnerer med en liste"""
        resistors = [[],[]]
        for i in range (len(self.SB)):
            GPIO.output(self.SB[i], True)

            for j in range (len(self.resistors)):
                if GPIO.input(self.resistors[j]):
                    resistors[i].append(self.value[j])
            GPIO.output(self.SB[i], False)

        return resistors

    def FindResistorNumbers(self):
        resistors = []
        for i in range(len(self.SB)):
            GPIO.output(self.SB[i], True)

            for j in range(len(self.resistors)):
                if GPIO.input(self.resistors[j]):
                    resistors.append(j)
            GPIO.output(self.SB[i], False)
        return resistors

    def Exist(self):
        """Utforer self.ExistNoFilter 10 ganger. Returnerer True hvis alle iterasjonene faar True fra self.NoFilter, False ellers"""
        for i in range(10):

            if not(self.ExistNoFilter()):
                return False
        return True


