#!usr/bin/env python
#-*-coding: utf-8-*-

#§ Création des variables d'informations
__version__ = "1.0.1"
__authors__ = "Lightpearl"

#§ Importation des modules complémentaires nécéssaires
from pygame.locals import *
import GameEngine as GE
import tkinter as tk
import tkinter.filedialog as fd
import pygame

#§ Création des variables globales du script
GE.constants.WINDOW_SIZE = (19*48, 19*48)
GE.constants.TILE_NUMBER_X = 19
GE.constants.TILE_NUMBER_Y = 19
GE.constants.TILE_ANIMATION_PERIOD = 0.33
WINDOW_X = 70+8*48+19*48
WINDOW_Y = 50+19*48

#§ Création des objets du script
class App:
	"""
	"""
	def __init__(self):
		# Création de la fenetre
		self.display = pygame.display.set_mode((WINDOW_X, WINDOW_Y), HWSURFACE | DOUBLEBUF)

		pygame.display.set_caption("MapGenerator - Heritage of Alkya | Map [default]")

		# Génération de la map
		GE.mapsystem.init()

		# Création des variables de scroll
		self.tileset_scroll_y = 0
		self.map_scroll_x = 0
		self.map_scroll_y = 0

		# Création des variables booléennes
		self.scrolling_tileset_y = False
		self.scrolling_map_x = False
		self.scrolling_map_y = False
		self.use_pencil_tool = False
		self.use_rectangle_tool = False
		self.running = False
		self.select_tiles = False

		# Création des variables de choix
		self.current_tool = "pencil"
		self.tileset_type_selected = "A"
		self.tiles_selected = [[("B", 0)]]
		self.current_map = "default"

		# Création des images de l'app
		self.icon_new_file = pygame.image.load("GameAssets\\MapGenerator\\new-file.png").convert_alpha()
		self.icon_save_file = pygame.image.load("GameAssets\\MapGenerator\\save.png").convert_alpha()
		self.icon_load_file = pygame.image.load("GameAssets\\MapGenerator\\open-folder-with-document.png").convert_alpha()
		self.icon_pencil = pygame.image.load("GameAssets\\MapGenerator\\edit.png").convert_alpha()
		self.icon_rectangle = pygame.image.load("GameAssets\\MapGenerator\\rectangle.png").convert_alpha()
		self.icon_filler = pygame.image.load("GameAssets\\MapGenerator\\paint-brush.png").convert_alpha()

		# Création des variables system de l'app
		self.fps = GE.constants.MIN_FPS
		self.maps_name = GE.mapsystem.MAPS.keys()
		self.font = pygame.font.SysFont("Arial", 16, bold=True)
		self.rect_save_coordinates = (0, 0)

	def create_new_map(self):
		print("Creating a new map")

	def load_map(self):
		print("Loading a map")

	def save_map(self):
		print("Saving the current map")
		filename = GE.mapsystem.MAPS[self.current_map].filename
		MAP = GE.mapsystem.MAPS[self.current_map]
		with open(filename, "w") as file:
			file.write("Name={}\n".format(MAP.name))
			file.write("Size={}\n".format(MAP.size))
			file.write("TilesetId={}\n".format(MAP.tileset.tileset_id))
			file.write("BGM={}\n".format(MAP.bgm))
			file.write("Tiles={}\n".format(";".join([str(tile) for tile in MAP.tiles])))
			file.close()

	def action(self, mod=1):
		if mod:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			if 0 <= mouse_y <= 20:
				if 20 <= mouse_x <= 40:
					self.create_new_map()

				elif 60 <= mouse_x <= 80:
					self.load_map()

				elif 100 <= mouse_x <= 120:
					self.save_map()

				elif 180 <= mouse_x <= 200:
					self.current_tool = "pencil"

				elif 220 <= mouse_x <= 240:
					self.current_tool = "rectangle"

				elif 260 <= mouse_x <= 280:
					self.current_tool = "filler"

			elif 20 <= mouse_y <= WINDOW_Y-10:
				if 10 <= mouse_x <= 30+8*48:
					if 20 <= mouse_y <= WINDOW_Y-30:
						if 10 <= mouse_x <= 10+8*48:
							self.select_tiles = True
							self.rect_save_coordinates = (mouse_x, mouse_y)

						else:
							self.scrolling_tileset_y = True

					elif WINDOW_Y-30 <= mouse_y <= WINDOW_Y-10:
						if 10 <= mouse_x <= 10+8*16:
							self.tileset_type_selected = "A"

						elif 10+8*16 <= mouse_x <= 10+8*32:
							self.tileset_type_selected = "B"

						elif 10+8*32 <= mouse_x <= 10+8*48:
							self.tileset_type_selected = "C"

				elif 40+8*48 <= mouse_x <= WINDOW_X-10:
					if 20 <= mouse_y <= WINDOW_Y-30:
						if 40+8*48 <= mouse_x <= WINDOW_X-30:
							if self.current_tool == "pencil":
								self.use_pencil_tool = True

							elif self.current_tool == "rectangle":
								self.use_rectangle_tool = True
								self.rect_save_coordinates = (mouse_x, mouse_y)

							else:
								self.use_filler((mouse_x+self.map_scroll_x-40-8*48)//48, (mouse_y+self.map_scroll_y-20)//48)

						else:
							self.scrolling_map_y = True

					else:
						if 40+8*48 <= mouse_x <= WINDOW_X-30:
							self.scrolling_map_x = True

		else:
			if self.scrolling_map_x:
				self.scrolling_map_x = False
				mouse_x, mouse_y = pygame.mouse.get_pos()
				x = min(max(40+8*48+min(WINDOW_X-70-8*48, (19*48)/(GE.mapsystem.MAPS[self.current_map].size[0]*48)*(WINDOW_X-70-8*48))/2, mouse_x), WINDOW_X-30-min(WINDOW_X-70-8*48, (19*48)/(GE.mapsystem.MAPS[self.current_map].size[0]*48)*(WINDOW_X-70-8*48))/2)
				self.map_scroll_x = (GE.mapsystem.MAPS[self.current_map].size[0]*48)*(x-40-8*48-min(WINDOW_X-70-8*48, (19*48)/(GE.mapsystem.MAPS[self.current_map].size[1]*48)*(WINDOW_X-70-8*48))/2)/(19*48)

			if self.scrolling_map_y:
				self.scrolling_map_y = False
				mouse_x, mouse_y = pygame.mouse.get_pos()
				y = min(max(20+min(WINDOW_Y-50, (19*48)/(GE.mapsystem.MAPS[self.current_map].size[1]*48)*(WINDOW_Y-50))/2, mouse_y), WINDOW_Y-30-min(WINDOW_Y-50, (19*48)/(GE.mapsystem.MAPS[self.current_map].size[1]*48)*(WINDOW_Y-50))/2)
				self.map_scroll_y = (GE.mapsystem.MAPS[self.current_map].size[1]*48)*(y-20-min(WINDOW_Y-50, (19*48)/(GE.mapsystem.MAPS[self.current_map].size[1]*48)*(WINDOW_Y-50))/2)/(19*48)

			if self.scrolling_tileset_y:
				self.scrolling_tileset_y = False
				mouse_x, mouse_y = pygame.mouse.get_pos()
				y = min(max(20+min(WINDOW_Y-50, (19*48)/(32*48)*(WINDOW_Y-50))/2, mouse_y), WINDOW_Y-30-min(WINDOW_Y-50, (19*48)/(32*48)*(WINDOW_Y-50))/2)
				self.tileset_scroll_y = (32*48)*(y-20-min(WINDOW_Y-50, (19*48)/(32*48)*(WINDOW_Y-50))/2)/(19*48)

			if self.use_pencil_tool:
				self.use_pencil_tool = False

			if self.use_rectangle_tool:
				self.use_rectangle_tool = False
				old_x, old_y = self.rect_save_coordinates
				new_x, new_y = pygame.mouse.get_pos()
				old_case_x = (old_x-8*48+self.map_scroll_x)//48
				old_case_y = (old_y-20+self.map_scroll_y)//48
				new_case_x = (new_x-8*48+self.map_scroll_x)//48
				new_case_y = (new_y-20+self.map_scroll_y)//48
				for x in range(int(min(old_case_x, new_case_x)), int(max(old_case_x, new_case_x)+1)):
					for y in range(int(min(old_case_y, new_case_y)), int(max(old_case_y, new_case_y)+1)):
						try:
							self.add_tiles(self.tiles_selected, (x, y))
						except Exception as e:
							print(e)

			if self.select_tiles:
				self.select_tiles = False
				mouse_x, mouse_y = pygame.mouse.get_pos()
				mouse_x, mouse_y = min(max(10, mouse_x), 9+8*48), min(max(20, mouse_y), WINDOW_Y-29)
				old_x, old_y = self.rect_save_coordinates
				if self.tileset_type_selected == "A":
					old_case_x = (old_x-10)//48
					old_case_y = (old_y-20+self.tileset_scroll_y)//48
					new_case_x = (mouse_x-10)//48
					new_case_y = (mouse_y-20+self.tileset_scroll_y)//48
					self.tiles_selected = [[None for _ in range(int(abs(new_case_y-old_case_y)+1))] for _ in range(int(abs(new_case_x-old_case_x)+1))]
					for j, y in enumerate(range(int(min(old_case_y, new_case_y)), int(max(old_case_y, new_case_y))+1)):
						for i, x in enumerate(range(int(min(old_case_x, new_case_x)), int(max(old_case_x, new_case_x))+1)):
							if y < 2:
								self.tiles_selected[i][j] = ("A1", y*8+x)
							elif y < 6:
								self.tiles_selected[i][j] = ("A2", (y-2)*8+x)
							elif y < 10:
								self.tiles_selected[i][j] = ("A3", (y-6)*8+x)
							elif y < 16:
								self.tiles_selected[i][j] = ("A4", (y-10)*8+x)
							else:
								self.tiles_selected[i][j] = ("A5", (y-16)*8+x)

				else:
					old_case_x = (old_x-10)//48
					old_case_y = (old_y-20+self.tileset_scroll_y)//48
					new_case_x = (mouse_x-10)//48
					new_case_y = (mouse_y-20+self.tileset_scroll_y)//48
					self.tiles_selected = [[(self.tileset_type_selected, y*8+x) for y in range(int(min(old_case_y, new_case_y)), int(max(old_case_y, new_case_y)+1))] for x in range(int(min(old_case_x, new_case_x)), int(max(old_case_x, new_case_x)+1))]

	def use_filler(self, x, y):
		if len(self.tiles_selected) == 1 and len(self.tiles_selected[0]) == 1:
			pass

	def add_tiles(self, tiles, pos):
		pass

	def render(self):
		self.display.fill((5, 10, 20))

		# Map
		self.display.blit(GE.mapsystem.MAPS[self.current_map].layout1, (40+8*48, 20))
		self.display.blit(GE.mapsystem.MAPS[self.current_map].layout2, (40+8*48, 20))

		# Tileset
		if self.tileset_type_selected == "A":
			for x in range(16):
				self.display.blit(GE.mapsystem.MAPS[self.current_map].tileset[("A1", x)].pictures[0][0], (10+x%8*48, 20+x//8*48-self.tileset_scroll_y))
			for x in range(32):
				self.display.blit(GE.mapsystem.MAPS[self.current_map].tileset[("A2", x)].pictures[0][0], (10+x%8*48, 20+(2+x//8)*48-self.tileset_scroll_y))
			for x in range(32):
				self.display.blit(GE.mapsystem.MAPS[self.current_map].tileset[("A3", x)].pictures[0][0], (10+x%8*48, 20+(6+x//8)*48-self.tileset_scroll_y))
			for x in range(48):
				self.display.blit(GE.mapsystem.MAPS[self.current_map].tileset[("A4", x)].pictures[0][0], (10+x%8*48, 20+(10+x//8)*48-self.tileset_scroll_y))
			for x, tile in enumerate(GE.mapsystem.MAPS[self.current_map].tileset.tiles["A5"]):
				self.display.blit(tile.pictures[0][0], (10+x%8*48, 20+(16+x//8)*48-self.tileset_scroll_y))
		else:
			for x, tile in enumerate(GE.mapsystem.MAPS[self.current_map].tileset.tiles[self.tileset_type_selected]):
				self.display.blit(tile.pictures[0][0], (10+x%8*48, 20+x//8*48-self.tileset_scroll_y))

		# Contours
		pygame.draw.rect(self.display, (255, 255, 255), (0, 0, WINDOW_X, 20))
		pygame.draw.rect(self.display, (255, 255, 255), (0, 20, 10, WINDOW_Y-20))
		pygame.draw.rect(self.display, (255, 255, 255), (WINDOW_X-10, 20, 10, WINDOW_Y-20))
		pygame.draw.rect(self.display, (255, 255, 255), (0, WINDOW_Y-10, WINDOW_X, 10))
		pygame.draw.rect(self.display, (255, 255, 255), (30+8*48, 20, 10, WINDOW_Y-20))
		pygame.draw.rect(self.display, (255, 255, 255), (10+8*48, WINDOW_Y-30, 20, 20))
		pygame.draw.rect(self.display, (255, 255, 255), (WINDOW_X-30, WINDOW_Y-30, 20, 20))

		# Boutons
		if self.current_tool == "pencil":
			pygame.draw.rect(self.display, (200, 255, 200), (170, 0, 40, 20))
		elif self.current_tool == "rectangle":
			pygame.draw.rect(self.display, (200, 255, 200), (210, 0, 40, 20))
		elif self.current_tool == "filler":
			pygame.draw.rect(self.display, (200, 255, 200), (250, 0, 40, 20))
		pygame.draw.line(self.display, (177, 177, 177), (10, 2), (10, 18))
		pygame.draw.line(self.display, (177, 177, 177), (50, 2), (50, 18))
		pygame.draw.line(self.display, (177, 177, 177), (90, 2), (90, 18))
		pygame.draw.line(self.display, (177, 177, 177), (130, 2), (130, 18))
		pygame.draw.line(self.display, (177, 177, 177), (170, 2), (170, 18))
		pygame.draw.line(self.display, (177, 177, 177), (210, 2), (210, 18))
		pygame.draw.line(self.display, (177, 177, 177), (250, 2), (250, 18))
		pygame.draw.line(self.display, (177, 177, 177), (290, 2), (290, 18))
		self.display.blit(self.icon_new_file, (22, 2))
		self.display.blit(self.icon_load_file, (62, 2))
		self.display.blit(self.icon_save_file, (102, 2))
		self.display.blit(self.icon_pencil, (182, 2))
		self.display.blit(self.icon_rectangle, (222, 2))
		self.display.blit(self.icon_filler, (262, 2))
		if self.tileset_type_selected == "A":
			pygame.draw.rect(self.display, (200, 255, 200), (10, WINDOW_Y-30, 8*16, 20))
		else:
			pygame.draw.rect(self.display, (255, 255, 255), (10, WINDOW_Y-30, 8*16, 20))
		if self.tileset_type_selected == "B":
			pygame.draw.rect(self.display, (200, 255, 200), (8*16+10, WINDOW_Y-30, 8*16, 20))
		else:
			pygame.draw.rect(self.display, (255, 255, 255), (8*16+10, WINDOW_Y-30, 8*16, 20))
		if self.tileset_type_selected == "C":
			pygame.draw.rect(self.display, (200, 255, 200), (16*16+10, WINDOW_Y-30, 8*16, 20))
		else:
			pygame.draw.rect(self.display, (255, 255, 255), (16*16+10, WINDOW_Y-30, 8*16, 20))
		text_A = self.font.render("A", True, (0, 0, 0))
		text_B = self.font.render("B", True, (0, 0, 0))
		text_C = self.font.render("C", True, (0, 0, 0))
		text_A_rect = text_A.get_rect(center=(10+4*16, WINDOW_Y-20))
		text_B_rect = text_B.get_rect(center=(10+12*16, WINDOW_Y-20))
		text_C_rect = text_C.get_rect(center=(10+20*16, WINDOW_Y-20))
		self.display.blit(text_A, text_A_rect)
		self.display.blit(text_B, text_B_rect)
		self.display.blit(text_C, text_C_rect)

		# Scrollbars Map
		pygame.draw.rect(self.display, (200, 200, 200), (WINDOW_X-30, 20, 20, WINDOW_Y-50))
		pygame.draw.rect(self.display, (200, 200, 200), (40+8*48, WINDOW_Y-30, WINDOW_X-70-8*48, 20))
		pygame.draw.rect(self.display, (100, 100, 100), (WINDOW_X-30, 20+self.map_scroll_y/(GE.mapsystem.MAPS[self.current_map].size[1]*48)*(WINDOW_Y-50), 20, min(WINDOW_Y-50, (19*48)/(GE.mapsystem.MAPS[self.current_map].size[1]*48)*(WINDOW_Y-50))))
		pygame.draw.rect(self.display, (100, 100, 100), (40+8*48+self.map_scroll_x/(GE.mapsystem.MAPS[self.current_map].size[0]*48)*(WINDOW_X-70-8*48), WINDOW_Y-30, min(WINDOW_X-70-8*48, (19*48)/(GE.mapsystem.MAPS[self.current_map].size[0]*48)*(WINDOW_X-70-8*48)), 20))

		# Scrollbars Tileset
		pygame.draw.rect(self.display, (200, 200, 200), (10+8*48, 20, 20, WINDOW_Y-50))
		pygame.draw.rect(self.display, (100, 100, 100), (10+8*48, 20+self.tileset_scroll_y/(32*48)*(WINDOW_Y-50), 20, min(WINDOW_Y-50, (19*48)/(32*48)*(WINDOW_Y-50))))

		# Case Selection tiles
		if self.tileset_type_selected == "A":
			x1, y1 = self.tiles_selected[0][0][1]%8, self.tiles_selected[0][0][1]//8
			x2, y2 = self.tiles_selected[-1][-1][1]%8, self.tiles_selected[-1][-1][1]//8
			if self.tiles_selected[0][0][0] == "A1":
				pass
			elif self.tiles_selected[0][0][0] == "A2":
				y1 += 2
			elif self.tiles_selected[0][0][0] == "A3":
				y1 += 6
			elif self.tiles_selected[0][0][0] == "A4":
				y1 += 10
			else:
				y1 += 16
			if self.tiles_selected[-1][-1][0] == "A1":
				pass
			elif self.tiles_selected[-1][-1][0] == "A2":
				y2 += 2
			elif self.tiles_selected[-1][-1][0] == "A3":
				y2 += 6
			elif self.tiles_selected[-1][-1][0] == "A4":
				y2 += 10
			else:
				y2 += 16
			pygame.draw.rect(self.display, (200, 255, 200), (10+x1*48, 20+y1*48-self.tileset_scroll_y, (x2-x1+1)*48, (y2-y1+1)*48), 4)
		else:
			x1, y1 = self.tiles_selected[0][0][1]%8, self.tiles_selected[0][0][1]//8
			x2, y2 = self.tiles_selected[-1][-1][1]%8, self.tiles_selected[-1][-1][1]//8
			pygame.draw.rect(self.display, (200, 255, 200), (10+x1*48, 20+y1*48-self.tileset_scroll_y, (x2-x1+1)*48, (y2-y1+1)*48), 4)

		if self.use_rectangle_tool:
			old_x, old_y = self.rect_save_coordinates
			new_x, new_y = pygame.mouse.get_pos()
			old_case_x = (old_x-40-8*48+self.map_scroll_x)//48
			old_case_y = (old_y-20+self.map_scroll_y)//48
			new_case_x = (new_x-40-8*48+self.map_scroll_x)//48
			new_case_y = (new_y-20+self.map_scroll_y)//48
			pygame.draw.rect(self.display, (100, 100, 100), (40+8*48+min(old_case_x, new_case_x)*48-self.map_scroll_x, 20+min(old_case_y, new_case_y)*48-self.map_scroll_y, (abs(old_case_x-new_case_x)+1)*48, (abs(old_case_y-new_case_y)+1)*48), 4)

	def loop(self):
		self.running = True

		FPSUPDATE = USEREVENT + 1

		pygame.time.set_timer(FPSUPDATE, 5000)

		clock = pygame.time.Clock()

		while self.running:
			clock.tick()
			for event in pygame.event.get():
				if event.type == QUIT:
					self.running = False

				elif event.type == MOUSEBUTTONDOWN:
					if event.button == 1:
						self.action(1)

				elif event.type == MOUSEBUTTONUP:
					if event.button == 1:
						self.action(0)

				elif event.type == FPSUPDATE:
					self.fps = clock.get_fps()

				else:
					pass

			# Calcul des frames
			GE.mapsystem.MAPS[self.current_map].update(self.fps, (int(self.map_scroll_x), int(self.map_scroll_y)))

			# Update la selection de tiles
			if self.select_tiles:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				mouse_x, mouse_y = min(max(10, mouse_x), 9+8*48), min(max(20, mouse_y), WINDOW_Y-29)
				old_x, old_y = self.rect_save_coordinates
				if self.tileset_type_selected == "A":
					old_case_x = (old_x-10)//48
					old_case_y = (old_y-20+self.tileset_scroll_y)//48
					new_case_x = (mouse_x-10)//48
					new_case_y = (mouse_y-20+self.tileset_scroll_y)//48
					self.tiles_selected = [[None for _ in range(int(abs(new_case_y-old_case_y)+1))] for _ in range(int(abs(new_case_x-old_case_x)+1))]
					for j, y in enumerate(range(int(min(old_case_y, new_case_y)), int(max(old_case_y, new_case_y))+1)):
						for i, x in enumerate(range(int(min(old_case_x, new_case_x)), int(max(old_case_x, new_case_x))+1)):
							if y < 2:
								self.tiles_selected[i][j] = ("A1", y*8+x)
							elif y < 6:
								self.tiles_selected[i][j] = ("A2", (y-2)*8+x)
							elif y < 10:
								self.tiles_selected[i][j] = ("A3", (y-6)*8+x)
							elif y < 16:
								self.tiles_selected[i][j] = ("A4", (y-10)*8+x)
							else:
								self.tiles_selected[i][j] = ("A5", (y-16)*8+x)

				else:
					old_case_x = (old_x-10)//48
					old_case_y = (old_y-20+self.tileset_scroll_y)//48
					new_case_x = (mouse_x-10)//48
					new_case_y = (mouse_y-20+self.tileset_scroll_y)//48
					self.tiles_selected = [[(self.tileset_type_selected, y*8+x) for y in range(int(min(old_case_y, new_case_y)), int(max(old_case_y, new_case_y)+1))] for x in range(int(min(old_case_x, new_case_x)), int(max(old_case_x, new_case_x)+1))]

			if self.scrolling_tileset_y:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				y = min(max(20+min(WINDOW_Y-50, (19*48)/(32*48)*(WINDOW_Y-50))/2, mouse_y), WINDOW_Y-30-min(WINDOW_Y-50, (19*48)/(32*48)*(WINDOW_Y-50))/2)
				self.tileset_scroll_y = (32*48)*(y-20-min(WINDOW_Y-50, (19*48)/(32*48)*(WINDOW_Y-50))/2)/(19*48)

			if self.scrolling_map_y:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				y = min(max(20+min(WINDOW_Y-50, (19*48)/(GE.mapsystem.MAPS[self.current_map].size[1]*48)*(WINDOW_Y-50))/2, mouse_y), WINDOW_Y-30-min(WINDOW_Y-50, (19*48)/(GE.mapsystem.MAPS[self.current_map].size[1]*48)*(WINDOW_Y-50))/2)
				self.map_scroll_y = (GE.mapsystem.MAPS[self.current_map].size[1]*48)*(y-20-min(WINDOW_Y-50, (19*48)/(GE.mapsystem.MAPS[self.current_map].size[1]*48)*(WINDOW_Y-50))/2)/(19*48)

			if self.scrolling_map_x:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				x = min(max(40+8*48+min(WINDOW_X-70-8*48, (19*48)/(GE.mapsystem.MAPS[self.current_map].size[0]*48)*(WINDOW_X-70-8*48))/2, mouse_x), WINDOW_X-30-min(WINDOW_X-70-8*48, (19*48)/(GE.mapsystem.MAPS[self.current_map].size[0]*48)*(WINDOW_X-70-8*48))/2)
				self.map_scroll_x = (GE.mapsystem.MAPS[self.current_map].size[0]*48)*(x-40-8*48-min(WINDOW_X-70-8*48, (19*48)/(GE.mapsystem.MAPS[self.current_map].size[1]*48)*(WINDOW_X-70-8*48))/2)/(19*48)

			# Affichage des frames
			self.render()
			pygame.display.flip()

#§ Lancement du script
pygame.init()
app = App()
app.loop()
