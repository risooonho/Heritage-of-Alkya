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
		self.is_highlighted = False

	def action(self, mod=1):
		pass

	def cancel(self, mod=1):
		pass

	def up(self, mod=1):
		pass

	def down(self, mod=1):
		pass

	def left(self, mod=1):
		pass

	def right(self, mod=1):
		pass

	def special_1(self, mod=1):
		pass

	def special_2(self, mod=1):
		pass

	def render(self):
		self.surface.fill((0, 0, 0, 0))

	def blit(self, surface):
		self.render()
		surface.blit(self.surface, (self.rect[0], self.rect[1]))

	def set_highlighted(self):
		self.is_highlighted = True

	def set_unhighlighted(self):
		self.is_highlighted = False

class ChoiceBox(BaseWidget):
	"""
	"""
	def __init__(self, options, rect, align="v"):
		BaseWidget.__init__(self, rect)
		self.options = options
		self.align = align
		self.cursor = 0
		self.bg_color = (0, 0, 0, 0)
		self.fg_color = (255, 255, 255)
		self.highlight_color = (100, 200, 0)
		self.border_color = (200, 200, 200)
		self.border_color_highlighted = (100, 200, 0)
		self.border_size = 2

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
		self.surface.fill(self.bg_color)
		font = pygame.font.SysFont("Arial", 16, bold=True)
		for i, option in enumerate(self.options):
			if self.align == "v":
				if i == self.cursor:
					pygame.draw.rect(self.surface, self.highlight_color, (0, i*self.rect[3]//len(self.options), self.rect[2], self.rect[3]//len(self.options)))
				text = font.render(option, True, self.fg_color)
				text_rect = text.get_rect(center=(self.rect[2]//2, i*self.rect[3]//len(self.options) + self.rect[3]//(2*len(self.options))))
				self.surface.blit(text, text_rect)
			else:
				if i == self.cursor:
					pygame.draw.rect(self.surface, self.highlight_color, (i*self.rect[2]//len(self.options), 0, self.rect[2]//len(self.options), self.rect[3]))
				text = font.render(option, True, self.fg_color)
				text_rect = text.get_rect(center=(i*self.rect[2]//len(self.options) + self.rect[2]//(2*len(self.options)), self.rect[3]//2))
				self.surface.blit(text, text_rect)
		if self.is_highlighted:
			pygame.draw.rect(self.surface, self.border_color_highlighted, (0, 0, self.rect[2], self.rect[3]), self.border_size)
		else:
			pygame.draw.rect(self.surface, self.border_color, (0, 0, self.rect[2], self.rect[3]), self.border_size)

class Scale(BaseWidget):
	"""
	"""
	def __init__(self, rect, init_value=0, start_value=0, end_value=0):
		BaseWidget.__init__(self, rect)
		self.value = init_value
		self.start_value = start_value
		self.end_value = end_value
		self.bg_color = (0, 0, 0, 0)
		self.fg_color = (255, 255, 255)
		self.highlight_color = (100, 200, 0)
		self.unhighlight_color = (50, 50, 50)
		self.add_value = False
		self.remove_value = False
		self.speed = 1

	def left(self, mod):
		if mod:
			self.remove_value = True
		else:
			self.remove_value = False

	def right(self, mod):
		if mod:
			self.add_value = True
		else:
			self.add_value = False

	def special_1(self, mod):
		if mod:
			self.speed = 2
		else:
			self.speed = 1

	def action(self, mod):
		pass

	def cancel(self, mod):
		pass

	def render(self):
		BaseWidget.render(self)
		if self.add_value:
			self.value = min(self.end_value, self.value + self.speed)
		if self.remove_value:
			self.value = max(self.start_value, self.value - self.speed)
		self.surface.fill(self.bg_color)
		pygame.draw.rect(self.surface, self.fg_color, (0, self.rect[3]//4, self.rect[2], self.rect[3]//2))
		if self.is_highlighted:
			progress = ((self.value-self.start_value)/(self.end_value-self.start_value))*self.rect[2]
			pygame.draw.rect(self.surface, self.highlight_color, (0, self.rect[3]//4, progress, self.rect[3]//2))
		else:
			progress = ((self.value-self.start_value)/(self.end_value-self.start_value))*self.rect[2]
			pygame.draw.rect(self.surface, self.unhighlight_color, (0, self.rect[3]//4, progress, self.rect[3]//2))

class SwitchButton(BaseWidget):
	"""
	"""
	def __init__(self, rect, init_value=False):
		BaseWidget.__init__(self, rect)
		self.value = init_value
		self.bg_color = (0, 0, 0, 0)
		self.fg_color = (255, 255, 255)
		self.highlight_color = (100, 200, 0)
		self.unhighlight_color = (50, 50, 50)

	def left(self, mod):
		if mod:
			self.value = not self.value

	def right(self, mod):
		if mod:
			self.value = not self.value

	def action(self, mod):
		if mod:
			self.value = not self.value

	def render(self):
		BaseWidget.render(self)
		self.surface.fill(self.fg_color)
		pygame.draw.rect(self.surface, self.unhighlight_color, (1, 1, self.rect[2]-2, self.rect[3]-2), 1)
		if self.value:
			pygame.draw.rect(self.surface, self.highlight_color, (self.rect[2]//2, 4, self.rect[2]//2-4, self.rect[3]-8))
		else:
			pygame.draw.rect(self.surface, self.unhighlight_color, (4, 4, self.rect[2]//2-4, self.rect[3]-8))

class Page(BaseWidget):
	"""
	"""
	def __init__(self, rect):
		BaseWidget.__init__(self, rect)
		self.widgets = []
		self.selected_widget = None
		self.cursor_pos = 0

	def add_widgets(self, *args):
		for widget in args:
			self.widgets.append(widget)
		self.widgets[0].set_highlighted()

	def up(self, mod):
		if self.selected_widget:
			self.selected_widget.up(mod)
		else:
			if mod:
				self.widgets[self.cursor_pos].set_unhighlighted()
				self.cursor_pos = (self.cursor_pos-1)%len(self.widgets)
				self.widgets[self.cursor_pos].set_highlighted()

	def down(self, mod):
		if self.selected_widget:
			self.selected_widget.down(mod)
		else:
			if mod:
				self.widgets[self.cursor_pos].set_unhighlighted()
				self.cursor_pos = (self.cursor_pos+1)%len(self.widgets)
				self.widgets[self.cursor_pos].set_highlighted()

	def left(self, mod):
		if self.selected_widget:
			self.selected_widget.left(mod)
		else:
			if mod:
				self.widgets[self.cursor_pos].set_unhighlighted()
				self.cursor_pos = (self.cursor_pos-1)%len(self.widgets)
				self.widgets[self.cursor_pos].set_highlighted()

	def right(self, mod):
		if self.selected_widget:
			self.selected_widget.right(mod)
		else:
			if mod:
				self.widgets[self.cursor_pos].set_unhighlighted()
				self.cursor_pos = (self.cursor_pos+1)%len(self.widgets)
				self.widgets[self.cursor_pos].set_highlighted()

	def action(self, mod):
		if self.selected_widget:
			self.selected_widget.action(mod)
		else:
			if mod:
				self.selected_widget = self.widgets[self.cursor_pos]

	def cancel(self, mod):
		if mod:
			if self.selected_widget:
				self.selected_widget = None
			else:
				return True

	def special_1(self, mod):
		if self.selected_widget:
			self.selected_widget.special_1(mod)

	def special_2(self, mod):
		if self.selected_widget:
			self.selected_widget.special_2(mod)

	def render(self):
		BaseWidget.render(self)
		for widget in self.widgets:
			pos = (widget.rect[0]-self.rect[0], widget.rect[1]-self.rect[1])
			widget.render()
			self.surface.blit(widget.surface, pos)

class SaveBox(BaseWidget):
	"""
	"""
	def __init__(self, rect, save_id):
		BaseWidget.__init__(self, rect)
		self.save_id = save_id
		self.name = "Empty"
		self.job = "None"
		self.timePlayed = 0
		self.load_infos()

	def convert_seconds(self):
		s, temp = self.timePlayed % 60, self.timePlayed // 60
		m, temp = temp % 60, temp // 60
		h, j = temp % 24, temp // 24
		return "{}J{}H{}m{}s".format(j, h, m, s)

	def load_infos(self):
		with open("GameData\\save_{}.sha".format(self.save_id), "r") as file:
			for line in file:
				if ": " in line:
					label, content = line[:-1].split(": ")
					if label == "PlayerName":
						self.name = content
					elif label == "PlayerClass":
						self.job = content
					elif label == "TimePlayed":
						self.timePlayed = int(content)
					else:
						pass
			file.close()

	def render(self):
		BaseWidget.render(self)
		if self.is_highlighted:
			self.surface.fill((30, 60, 0, 50))
		else:
			self.surface.fill((0, 0, 0, 50))
		font = pygame.font.SysFont("Arial", 16, bold=True)
		name = font.render(self.name, True, (255, 255, 255))
		name_rect = name.get_rect(topleft=(5, 5))
		self.surface.blit(name, name_rect)
		job = font.render(self.job, True, (255, 255, 255))
		job_rect = name.get_rect(topleft=(5, 35))
		self.surface.blit(job, job_rect)
		time = font.render(self.convert_seconds(), True, (255, 255, 255))
		time_rect = time.get_rect(bottomright=(self.rect[2]-5, self.rect[3]-5))
		self.surface.blit(time, time_rect)
