#-*-coding: utf-8-*-

#§ Création des variables d'information
__version__ = "1.0.0"
__authors__ = "Lightpearl"

#§ Importation des modules complémentaires nécéssaires
from pygame.locals import *

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

#§ variables de nom
GAME_TITLE = "Heritage of Alkya"

#§ Variables d'évennements
KEYMAP = {
    K_UP: "up",
    K_DOWN: "down",
    K_LEFT: "left",
    K_RIGHT: "right",
    K_a: "action",
    K_x: "action",
    K_q: "action",
    K_z: "cancel",
    K_w: "cancel",
    K_c: "cancel",
    K_LSHIFT: "special 1"}
