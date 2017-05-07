__author__ = 'Thomas Kaland'
# _*_ coding: utf-8 _*_

from RPi import GPIO

GPIO.setmode(GPIO.BCM) #Setter opp pin-nummerering
GPIO.VERBOSE = True

class Display:
    """Klasse som styrer 7-segment display til ROBO."""

    def __init__(self, ports):
        """Setter opp portnummerering til 7-segment. Nummerering i form av liste med [ovre venstre, ovre midt, ovre hoyre, midt, nedre venstre, nedre midt, nedre hoyre]."""

        self.ports = ports
        GPIO.setup(ports, GPIO.OUT) #Gjoer portene til output.

        self.numberconfig = [[0,0,0, #nr 0              Numerconfig er en liste som forteller programmet hvilket led som skal lyse til hvilket tall. Oppsettet i listen er
                                0,                     #én til én for hvordan displayet er bygget opp.
                              0,0,0],

                             [0,0,1, #nr 1
                                0,
                              0,0,1],

                             [0,1,1, #nr 2
                                1,
                              1,1,0],

                             [0,1,1, #nr 3
                                1,
                              0,1,1],

                             [1,0,1, #nr 4
                                1,
                              0,0,1],

                             [1,1,0, #nr 5
                                1,
                              0,1,1],

                             [1,1,0, #nr 6
                                1,
                              1,1,1],

                             [0,1,1, #nr 7
                                0,
                              0,0,1],

                             [1,1,1, #nr 8
                                1,
                              1,1,1],

                             [1,1,1, #nr 9
                                1,
                              0,1,1]]

    def Show(self, number):
        """Objekt som skriver ut et tall til displayet"""

        GPIO.output(self.ports, False)

        for i in range(len(self.numberconfig[number])):             #for-lokken går igjennom numberconfig for ett gitt tall og ser hvilke porter som skal være HIGH, og hvilket som skal være LOW.
            GPIO.output(self.ports[i], self.numberconfig[number][i])

display = Display([1,2,3,4,5,6,7])

display.Show(5)


