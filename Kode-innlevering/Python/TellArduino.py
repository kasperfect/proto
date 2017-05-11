__author__ = 'Thomas Kaland'
# _*_ coding: utf-8 _*_

import serial

class TellArduino:
    """Klasse som kommuniserer med Arduinoen for aa vise oyne og tall."""

    def __init__(self, port):
        """Starter seriellkomunikasjon med arduino uno med baudrate 115000"""
        self.uno = serial.Serial(port, 115200, rtscts=True)

    def ShowNumber(self, Number):
        """Objekt som 'oversetter'/forskyver tall slik at arduinoen forstaar at han skal vise tallene paa 7-segmentsdisplayet."""
        convertlist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        self.uno.write(convertlist[Number].encode('utf-8'))

    def ShowFace(self, Number):
        """Objekt som sender hvilket fjes/oyne som arduinoen skal vise"""
        self.uno.write(str(Number).encode('utf-8'))

    def StartStopBlink(self):
        """Skrur av og paa blinking av oyner"""
        self.uno.write(b'8')

    def Mute(self):
        """Skrur av oyne og sevensegment"""
        self.uno.write(b'9')

