#-*-coding: utf-8-*-

#§ Création des variables d'information
__version__ = "1.0.0"
__authors__ = "Lightpearl"

#§ Importation des modules complémentaires nécéssaires
from pygame.locals import *
from . import optionssystem
from . import savesystem

#§ Variables de taille
TILE_SIZE = 48 #px
SPRITE_SIZE = 48 #px
TILE_NUMBER_X = 17
TILE_NUMBER_Y = 13

WINDOW_SIZE_X = TILE_NUMBER_X*TILE_SIZE
WINDOW_SIZE_Y = TILE_NUMBER_Y*TILE_SIZE
WINDOW_SIZE = (WINDOW_SIZE_X, WINDOW_SIZE_Y)

#§ Variables de temps
TILE_ANIMATION_PERIOD = 0.25 #s
SPEED_WALK = 0.5 #s
SPEED_SPRINT = 0.25 #s
SPEED_GOD = 1/30 #s

#§ Variables de fréquence
MIN_FPS = 1/SPEED_GOD
MAX_FPS = 120

#§ Variables de nom
GAME_TITLE = "Heritage of Alkya"

#§ Variables d'options
options = optionssystem.Options()
save = savesystem.Save()

#§ Variables de chemins
OPTION_PATH = optionssystem.OPTION_PATH

#§ Variables de system
NB_WORKER_MAPUPDATE = 1
