#-*-coding: utf-8-*-

#§ Variables d'information du module
__version__ = "1.0.0"
__authors__ = "Lightpearl"

#§ Importation des modules complémentaires nécéssaires
from . import constants as cts
import pygame

#§ Création des objets du module
class BaseWidget:
	"""
	"""
	def __init__(self, rect):
		self.surface = pygame.Surface((rect[2], rect[3]), cts.HWSURFACE | cts.SRCALPHA)
		self.event_dict = {
			"action": self.action,
			"cancel": self.cancel,
			"up": self.up,
			"down": self.down,
			"left": self.left,
			"right": self.right
		}
		self.rect = rect

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

	def blit(self, surface):
		self.render()
		surface.blit(self.surface, (self.rect[0], self.rect[1]))

class ChoiceBox(BaseWidget):
	"""
	"""
	def __init__(self, options, rect, align="v"):
		BaseWidget.__init__(self, rect)
		self.options = options
		self.align = align
		self.cursor = 0

	def left(self):
		if not self.align == "v":
			self.cursor -= 1
			self.cursor %= len(self.options)

	def right(self):
		if not self.align == "v":
			self.cursor += 1
			self.cursor %= len(self.options)

	def up(self):
		if not self.align == "h":
			self.cursor -= 1
			self.cursor %= len(self.options)

	def down(self):
		if not self.align == "h":
			self.cursor += 1
			self.cursor %= len(self.options)

	def get(self):
		return self.options[self.cursor]

	def render(self):
		BaseWidget.render(self)
		font = pygame.font.SysFont("Arial", 16, bold=True)
		for i, option in enumerate(self.options):
			if self.align == "v":
				if i == self.cursor:
					pygame.draw.rect(self.surface, (100, 200, 0), (0, i*self.rect[3]//len(self.options), self.rect[2], self.rect[3]//len(self.options)))
				text = font.render(option, True, (255, 255, 255))
				text_rect = text.get_rect(center=(self.rect[2]//2, i*self.rect[3]//len(self.options) + self.rect[3]//(2*len(self.options))))
				self.surface.blit(text, text_rect)
			else:
				if i == self.cursor:
					pygame.draw.rect(self.surface, (100, 200, 0), (i*self.rect[2]//len(self.options), 0, self.rect[2]//len(self.options), self.rect[3]))
				text = font.render(option, True, (255, 255, 255))
				text_rect = text.get_rect(center=(i*self.rect[2]//len(self.options) + self.rect[2]//(2*len(self.options)), self.rect[3]//2))
				self.surface.blit(text, text_rect)

		pygame.draw.rect(self.surface, (200, 200, 200), (0, 0, self.rect[2], self.rect[3]), 5)