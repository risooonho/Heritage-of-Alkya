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
		self.specialevents = []
		self.specialeventsdict = {}
		self.running = False
		self.max_fps = 10000

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

		clock = pygame.time.Clock()

		while self.running:
			clock.tick(self.max_fps)
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

				elif event.type in self.specialevents:
					self.specialeventsdict[event.type]()
				
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
		self.page = widget.Page((0, 96, cts.WINDOW_SIZE_X, cts.WINDOW_SIZE_Y-96))
		self.page.add_widgets(
			widget.Scale((cts.WINDOW_SIZE_X-420, 116, 300, 30), init_value=100, end_value=100),
			widget.Scale((cts.WINDOW_SIZE_X-420, 166, 300, 30), init_value=100, end_value=100),
			widget.Scale((cts.WINDOW_SIZE_X-420, 216, 300, 30), init_value=100, end_value=100),
			widget.Scale((cts.WINDOW_SIZE_X-420, 266, 300, 30), init_value=100, end_value=100),
			widget.SwitchButton((cts.WINDOW_SIZE_X-170, 346, 50, 30)),
			widget.SwitchButton((cts.WINDOW_SIZE_X-170, 396, 50, 30)),
			widget.Scale((cts.WINDOW_SIZE_X-420, 446, 300, 30), init_value=12, start_value=0, end_value=24)
		)

	def up(self, mod):
		self.page.up(mod)

	def down(self, mod):
		self.page.down(mod)

	def left(self, mod):
		self.page.left(mod)

	def right(self, mod):
		self.page.right(mod)

	def action(self, mod):
		self.page.action(mod)

	def cancel(self, mod):
		self.page.cancel(mod)

	def special_1(self, mod):
		self.page.special_1(mod)

	def special_2(self, mod):
		self.page.special_2(mod)

	def render(self):
		BaseScene.render(self)
		self.surface.fill((150, 150, 150))
		self.page.blit(self.surface)
		font = pygame.font.SysFont("Arial", 24)
		text = font.render("Options", True, (255, 255, 255))
		text_rect = text.get_rect(center=(cts.WINDOW_SIZE_X//2, 48))
		self.surface.blit(text, text_rect)
