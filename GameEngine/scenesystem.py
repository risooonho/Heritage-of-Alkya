#-*-coding: utf-8-*-

#§ Variables d'information du module
__version__ = "1.0.0"
__authors__ = "Lightpearl"

#§ Importation des modules complémentaires nécéssaires
from . import constants as cts
from . import widget
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
			"right": self.right,
			"special 1": self.special_1,
			"special 2": self.special_2
		}
		self.running = False

	def action(self, mod):
		pass

	def cancel(self, mod):
		pass

	def up(self, mod):
		pass

	def down(self, mod):
		pass

	def left(self, mod):
		pass

	def right(self, mod):
		pass

	def special_1(self, mod):
		pass
	
	def special_2(self, mod):
		pass

	def render(self):
		self.surface.fill((0, 0, 0, 0))

	def loop(self, display):
		self.running = True

		while self.running:
			for event in pygame.event.get():
				if event.type == cts.QUIT:
					pygame.quit()
					exit()

				elif event.type == cts.KEYDOWN:
					if event.key in cts.options.KEYMAP:
						func = self.event_dict[cts.options.KEYMAP[event.key]]
						func(1)

				elif event.type == cts.KEYUP:
					if event.key in cts.options.KEYMAP:
						func = self.event_dict[cts.options.KEYMAP[event.key]]
						func(0)
				
				else:
					pass

			self.render()
			display.fill((0, 0, 0))
			display.blit(self.surface, (0, 0))
			pygame.display.flip()

class TitleScreen(BaseScene):
	"""
	"""
	def __init__(self):
		BaseScene.__init__(self)
		self.options = widget.ChoiceBox(["New Game", "Continue", "Options", "Quit Game"], (cts.WINDOW_SIZE_X//4, 2*cts.WINDOW_SIZE_Y//6, cts.WINDOW_SIZE_X//2, cts.WINDOW_SIZE_Y//2))
	
	def action(self):
		self.running = False
		option = self.options.get()
		if option == "Quit Game":
			pygame.quit()
			exit()

		elif option == "New Game":
			pass

		elif option == "Continue":
			pass

		else:
			pass

	def up(self, mod):
		if mod:
			self.options.up()
	
	def down(self, mod):
		if mod:
			self.options.down()

	def render(self):
		BaseScene.render(self)
		font = pygame.font.SysFont("Arial", 32, bold=True, italic=True)
		title = font.render(cts.GAME_TITLE, True, (255, 255, 255))
		title_rect = title.get_rect(center=(cts.WINDOW_SIZE_X//2, cts.WINDOW_SIZE_Y//6))
		self.surface.blit(title, title_rect)
		self.options.blit(self.surface)

class OptionScene(BaseScene):
	"""
	"""
	def __init__(self):
		BaseScene.__init__(self)
