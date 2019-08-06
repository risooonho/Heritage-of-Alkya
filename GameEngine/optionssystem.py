#-*-coding: utf-8-*-

#§ Variables d'information du module
__version__ = "1.0.0"
__authors__ = "Lightpearl"

#§ Importation des modules complémentaires nécéssaires
from pygame.locals import *

class Options:
    """
    """
    def __init__(self):
        self.KEYMAP = {
            K_UP: "up",
            K_DOWN: "down",
            K_LEFT: "left",
            K_RIGHT: "right",
            K_q: "action",
            K_x: "action",
            K_SPACE: "action",
            K_RETURN: "action",
            K_w: "cancel",
            K_c: "cancel",
            K_ESCAPE: "cancel",
            K_BACKSPACE: "cancel",
            K_LCTRL: "special 1",
            K_RCTRL: "special 1",
            K_LSHIFT: "special 2",
            K_RSHIFT: "special 2"
        }