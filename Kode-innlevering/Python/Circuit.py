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

    #I ROBO har en to ledninger over og to ledninger under motstandene som brukeren kan koble opp. Disse ledningene er her kalt for NB (North Bridge) og SB (South Bridge) (Hehe, you see what i did there? :P),
    #henholdsvis ovre og nedre ledninger. Her er NB konfigurert til inputs, mens SB er output og sender singal for aa finne ut hva ledningene er koblet til.

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

        for i in range(len(self.SB)): #Forste lokke itererer seg igjennom SB for aa skru vekselsvis koblingene paa/av.
            GPIO.output(self.SB[i], True)

            for j in range(len(self.NB)): #Andre lokke itererer seg igjennom NB og sjekker om noen av de er blitt high.
                if GPIO.input(self.NB[j]):
                    paths.append(self.NB[j])

            GPIO.output(self.SB[i], False)

        if len(paths) == len(self.SB): #Dersom hverledning i SB gaar til hver sin NB, da er kretsen koblet sammen og brukeren har gitt en losning.
            return True
        else:
            return False

    def Find(self):
        """Objekt som sjekker om den utforte losingen er korrekt. Returnerer """

        try: #I noen tilfeller kan det hende at koblingene blir tatt ut i det. Find blir kjoert. Da kan en faa 0-divisjonsfeil. Hvis dette skjer returnerer funksjonen bare 0

            resistors = self.FindResistors()
            Voltage_2 = math.fsum(resistors[1])
            Voltage_2 /=math.fsum(resistors[0])+math.fsum(resistors[1])
            Voltage_2 *= self.voltage #Utforer regnestykket for spenningsdeler

            return Voltage_2
        except:
            return 0


    def FindResistors(self):
        """Objekt som sjekker hvilke motstander som er koblet inn og returnerer med en liste"""
        resistors = [[],[]]
        for i in range (len(self.SB)): #Forste lokke itererer seg igjennom SB og skrur vekselsvis en paa og av.
            GPIO.output(self.SB[i], True)

            for j in range (len(self.resistors)): #Itererer seg igjennom motstandene for aa se hvilke av ledningene til SB som er koblet in hvor.
                if GPIO.input(self.resistors[j]):
                    resistors[i].append(self.value[j])
            GPIO.output(self.SB[i], False)

        return resistors

    def FindResistorNumbers(self):
        """Finner nummeret til motstandene som er koblet inn. Gjoer egentlig akkuratt det samme som FindResistors, men returnerer nummereringen til motstandene, ikke port."""
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
        #Enkel filtrering av signal. Sjekker bare om det er et stabilt True/False signal foer den returnerer True/False
        for i in range(30):

            if not(self.ExistNoFilter()):
                return False
        return True


