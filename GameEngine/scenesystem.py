#-*-coding: utf-8-*-

#§ Variables d'information du module
__version__ = "1.0.0"
__authors__ = "Lightpearl"

#§ Importation des modules complémentaires nécéssaires
from . import constants as cts
from . import widget
import pygame

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
		self.display = display

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
	
	def action(self, mod):
		option = self.options.get()
		if option == "Quit Game":
			self.running = False
			pygame.quit()
			exit()

		elif option == "New Game":
			self.running = False

		elif option == "Continue":
			self.running = False

		else:
			SCENES["Options"].loop(self.display)

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
			widget.SwitchButton((cts.WINDOW_SIZE_X-170, 346, 50, 30)),
			widget.SwitchButton((cts.WINDOW_SIZE_X-170, 396, 50, 30)),
			widget.Scale((cts.WINDOW_SIZE_X-420, 446, 300, 30), init_value=12, start_value=0, end_value=24)
		)
		self.labels = ["Music volume", "Ambiance volume", "Effects Volume", "Hardcore mode", "Day / Night cycle", "Game Hour (if no Day / Night cycle)"]
		self.load()

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
		info = self.page.cancel(mod)
		if info:
			self.save()
			cts.options.load()
			self.running = False

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

		font = pygame.font.SysFont("Arial", 16, bold=True)
		for i in range(len(self.labels)):
			if isinstance(self.page.widgets[i], widget.Scale):
				text_2 = font.render(str(self.page.widgets[i].value), True, (255, 255, 255))
				text_2_rect = text_2.get_rect(midleft=(cts.WINDOW_SIZE_X-100, self.page.widgets[i].rect[1]+15))
				self.surface.blit(text_2, text_2_rect)
			if i == self.page.cursor_pos:
				if self.page.selected_widget:
					text = font.render(self.labels[i], True, (200, 100, 0))
				else:
					text = font.render(self.labels[i], True, (100, 200, 0))
			else:
				text = font.render(self.labels[i], True, (255, 255, 255))

			text_rect = text.get_rect(midleft=(48, self.page.widgets[i].rect[1]+15))
			self.surface.blit(text, text_rect)

	def save(self):
		with open(cts.OPTION_PATH, "w") as file:
			file.write("OPTIONS of game [Heritage of Alkya]\n\n")
			file.write("<VOLUMES>\n")
			file.write("BGM: {}\n".format(self.page.widgets[0].value))
			file.write("BGS: {}\n".format(self.page.widgets[1].value))
			file.write("MSE: {}\n\n".format(self.page.widgets[2].value))
			file.write("<SYSTEM>\n")
			file.write("Hardcore: {}\n".format(self.page.widgets[3].value))
			file.write("DNcycle: {}\n".format(self.page.widgets[4].value))
			file.write("GameHour: {}\n".format(self.page.widgets[5].value))
			file.close()

	def load(self):
		with open(cts.OPTION_PATH, "r") as file:
			for line in file:
				if ": " in line:
					label, content = line[:-1].split(": ")
					if label == "BGM":
						self.page.widgets[0].value = int(content)
					elif label == "BGS":
						self.page.widgets[1].value = int(content)
					elif label == "MSE":
						self.page.widgets[2].value = int(content)
					elif label == "Hardcore":
						self.page.widgets[3].value = eval(content)
					elif label == "DNcycle":
						self.page.widgets[4].value = eval(content)
					elif label == "GameHour":
						self.page.widgets[5].value = int(content)
			file.close()

class SaveChooserScene(BaseScene):
	"""
	"""
	def __init__(self):
		BaseScene.__init__(self)
		self.page = widget.Page((0, 0, cts.WINDOW_SIZE_X, cts.WINDOW_SIZE_Y))
		self.page.add_widgets(
			widget.SaveBox((0, 0, cts.WINDOW_SIZE_X, cts.WINDOW_SIZE_Y//4), 1),
			widget.SaveBox((0, cts.WINDOW_SIZE_Y//4, cts.WINDOW_SIZE_X, cts.WINDOW_SIZE_Y//4), 1),
			widget.SaveBox((0, cts.WINDOW_SIZE_Y//2, cts.WINDOW_SIZE_X, cts.WINDOW_SIZE_Y//4), 1),
			widget.SaveBox((0, 3*cts.WINDOW_SIZE_Y//4, cts.WINDOW_SIZE_X, cts.WINDOW_SIZE_Y//4), 1)
		)

#§ Variables globales du module
SCENES = {
	"TitleScreen": TitleScreen(),
	"Options": OptionScene(),
	"SaveChooser": SaveChooserScene()
}
