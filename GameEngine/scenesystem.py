#-*-coding: utf-8-*-

#§ Variables d'information du module
__version__ = "1.0.0"
__authors__ = "Lightpearl"

#§ Importation des modules complémentaires nécéssaires
from . import constants as cts
import pygame

#§ Variables globales du module
SCENES = {}

#§ Création des objets du module
class BaseScene:
	"""
	"""
	def __init__(self):
		self.surface = pygame.Surface(cts.WINDOW_SIZE, cts.HWSURFACE | cts.SRCALPHA)
		self.event_dict = {
			"action": self.action,
			"cancel": self.cancel,
			"up": self.up,
			"down": self.down,
			"left": self.left,
			"right": self.right
		}

	def action(self):
		pass

	def cancel(self):
		pass

	def up(self):
		pass

	def down(self):
		pass

	def left(self):
		pass

	def right(self):
		pass

	def render(self):
		self.surface.fill((0, 0, 0, 0))
