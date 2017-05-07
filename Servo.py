__author__ = 'Thomas Kaland'
# _*_ coding: utf-8 _*_
from RPi import GPIO

GPIO.setmode(GPIO.BCM) #Setter opp pornummerering til BCM

class Servo:
    """Klasse som styrer servoen som aapner og lukker lokket til ROBO."""

    def __init__(self, port):
        """Setter opp port til data/servo og gir servoen et signal paa 50hz, gjoer at servoen gaar i lukket posisjon (40 grader)"""

        self.data = port
        GPIO.setup(port, GPIO.OUT)
        self.servo = GPIO.PWM(port, 50)
        self.closed = 8 #Servo Dutycycle hvor servoen staar i lukket posisjon
        self.open = 11 #Servo Dutycycle hvor servoen staar i aapen posisjon
        self.servo.start(self.closed)


    def Open(self):
        """Vrir servoen slik at den aapner lokket til ROBO"""
        self.servo.ChangeDutyCycle(self.open)

    def Close(self):
        """Vrir servoen slik at den lukker lokket til ROBO"""
        self.servo.ChangeDutyCycle(self.closed)

    def Turn(self, dc):
        """Vrir servoen i x-antall grader fra nulposisjon."""
        self.servo.ChangeDutyCycle(dc)

class Lid:
    """Klasse som styrer hele apne/lukke-mekanismen til ROBO. Bruker Servo-klassen til aa styre servoene. Se over i koden."""

    def __init__(self, servopin, magnetpin):
        self.servo = servopin
        self.magnet = magnetpin

        GPIO.setup(self.magnet, GPIO.OUT)
        self.Servo = Servo(servopin)

    def Open(self):
        """Objekt som aapner lokket til ROBO"""

        GPIO.output(self.magnet, False)
        self.Servo.Open()

    def Close(self):
        """Objekt som lukker lokket til ROBO"""
        self.Servo.Close()
        GPIO.output(self.magnet, True)








