__author__ = 'Thomas Kaland'
# _*_ coding: utf-8 _*_
import pygame
import time
class Sound:
    """Klasse som enkelt aapner og spiller av lyder"""
    #Denne klassen er egentlig bare lagd saa det blir enklere og raskere aa bruke pygame til aa spille av lyder.

    def __init__(self, file):
        """Henter frem filer"""
        self.file = file
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(self.file)

    def Play(self, loops = 0):
        self.sound.play(loops)




