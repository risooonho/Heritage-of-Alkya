#-*-coding: utf-8-*-

#§ Variables d'information du module
__version__ = "1.0.0"
__authors__ = "Lightpearl"

#§ Importation des modules complémentaires nécéssaires
from pygame.locals import *

#§ Création des constantes du module
OPTION_PATH = "GameData\\options.sha"

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
        self.bgmVolume = 100
        self.bgsVolume = 100
        self.mseVolume = 100
        self.hardcoreMode = False
        self.dayNightCycle = True
        self.gameHour = 12

    def load(self):
        with open(OPTION_PATH, "r") as file:
            for line in file:
                if ": " in line:
                    label, content = line[:-1].split(": ")
                    if label == "BGM":
                        self.bgmVolume = int(content)
                    elif label == "BGS":
                        self.bgsVolume = int(content)
                    elif label == "MSE":
                        self.mseVolume = int(content)
                    elif label == "Hardcore":
                        self.hardcoreMode = eval(content)
                    elif label == "DNcycle":
                        self.dayNightCycle = eval(content)
                    else:
                        self.gameHour = int(content)
            file.close()

    def save(self):
        with open(OPTION_PATH, "w") as file:
            file.write("OPTIONS of game [Heritage of Alkya]\n\n")
            file.write("<VOLUMES>\n")
            file.write("BGM: {}\n".format(self.bgmVolume))
            file.write("BGS: {}\n".format(self.bgsVolume))
            file.write("MSE: {}\n\n".format(self.mseVolume))
            file.write("<SYSTEM>\n")
            file.write("Hardcore: {}\n".format(self.hardcoreMode))
            file.write("DNcycle: {}\n".format(self.dayNightCycle))
            file.write("GameHour: {}\n".format(self.gameHour))
            file.close()