import pygame
from . import constants
display = pygame.display.set_mode(constants.WINDOW_SIZE, constants.HWSURFACE | constants.DOUBLEBUF)

from . import widget
from . import scenesystem
from . import mapsystem

#§ Création des fonctions du fichier
def launch():
    pygame.init()
    TitleScene = scenesystem.TitleScreen()
    TitleScene.loop(display)