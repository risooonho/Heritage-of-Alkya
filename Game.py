#!usr/bin/env python3
#-*-coding: utf-8-*-

#§ Création des variables d'information
__version__ = "1.0.0"
__authors__ = "Lightpearl"

#§ Importation des modules nécéssaires
import GameEngine as GE
import GameEngine.constants as cts
import pygame
import os

pygame.init()

display = pygame.display.set_mode(cts.WINDOW_SIZE, cts.HWSURFACE | cts.DOUBLEBUF)

GE.scenesystem.SCENES["MapScene"].load_map("default")
GE.scenesystem.SCENES["MapScene"].loop(display)
