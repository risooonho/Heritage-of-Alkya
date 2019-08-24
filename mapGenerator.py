#!usr/bin/env python
#-*-coding: utf-8-*-

#§ Création des variables d'information de l'application
__version__ = "1.0.0"
__authors__ = "Lightpearl"

import pygame
import tkinter as tk
import tkinter.filedialog as tkfd
import threading
import sys

pygame.init()

THREAD_RUN = True
display = pygame.display.set_mode((500, 50))

def run_thread():
	while THREAD_RUN:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			else:
				pass

		display.fill((255, 255, 255))
		font = pygame.font.SysFont("Arial", 20)
		text = font.render("Chargement des composants du jeu", True, (0, 0, 0))
		text_rect = text.get_rect(center=(250, 25))
		display.blit(text, text_rect)
		pygame.display.flip()

#§ Importation des modules complémentaires nécéssaires
import GameEngine as GE
from GameEngine.constants import *

thread = threading.Thread(target=run_thread)
thread.start()

GE.mapsystem.init()

THREAD_RUN = False
thread.join()

print(GE.mapsystem.MAPS)

#§ Création des variables globales de l'application
WINDOW_X = 70+29*48
WINDOW_Y = 40+21*48
GE.mapsystem.cts.TILE_NUMBER_X = 21
GE.mapsystem.cts.TILE_NUMBER_Y = 21
GE.mapsystem.cts.WINDOW_SIZE = (21*48, 21*48)
GE.mapsystem.cts.TILE_ANIMATION_PERIOD = 0.1

#§ Création des objets du jeu
class App:
	"""
	Application
	"""

	def __init__(self):
		self.display = pygame.display.set_mode((WINDOW_X, WINDOW_Y), HWSURFACE|DOUBLEBUF)

		# Création des booléens de l'objet
		self.running = False # l'application est en train de tourner
		self.scrolling_x_map = False # Le click est maintenu sur le scroll x de la map
		self.scrolling_y_map = False # Le click est maintenu sur le scroll y de la map
		self.scrolling_tileset = False # Le click est maintenu sur le scroll de tileset
		self.select_tiles = False # L'utilisateur est en train de selectionner des tiles
		self.pencil = False # L'outil pencil est en cours d'utilisation
		self.rectangle = False # L'outil rectangle est en cours d'utilisation
		self.filler = False # L'outil filler est en cours d'utilisation

		# Création des variables de temps de l'objet
		self.FPS_UPDATE = USEREVENT + 1
		self.fps = MIN_FPS

		# Création des curseurs de l'application
		self.current_tool = "rectangle"
		self.current_tileset_type = "A"
		self.current_tiles = [[("A1", 0)]]

		# Création des variables de camera de l'objet
		self.camera = [0, 0]
		self.tileset_scroll = 0

		# Création des variables de position de l'objet
		self.start_selection = (0, 0)
		self.end_selection = (0, 0)

		# Création des objets rattachés à l'objet
		self.map = GE.mapsystem.Map("GameAssets\\Maps\\MAP001.sha")

		# Création de la surface de font et des composants pygame sur la fenêtre
		self.font = pygame.font.SysFont("Arial", 16)
		self.background = pygame.Surface((WINDOW_X, WINDOW_Y), HWSURFACE|SRCALPHA)
		pygame.draw.rect(self.background, (0, 0, 0), (0, 0, 10, WINDOW_Y))
		pygame.draw.rect(self.background, (0, 0, 0), (0, 0, WINDOW_X, 10))
		pygame.draw.rect(self.background, (0, 0, 0), (0, WINDOW_Y-10, WINDOW_X, 10))
		pygame.draw.rect(self.background, (0, 0, 0), (WINDOW_X-10, 0, 10, WINDOW_Y))
		pygame.draw.rect(self.background, (0, 0, 0), (30+8*48, 0, 10, WINDOW_Y))
		pygame.draw.rect(self.background, (0, 0, 0), (10+8*48, WINDOW_Y-30, 20, 20))
		pygame.draw.rect(self.background, (0, 0, 0), (WINDOW_X-30, WINDOW_Y-30, 20, 20))
		self.text1 = self.font.render("A", True, (0, 0, 0))
		self.text2 = self.font.render("B", True, (0, 0, 0))
		self.text3 = self.font.render("C", True, (0, 0, 0))
		self.text1_rect = self.text1.get_rect(center=(10+8*8, WINDOW_Y-20))
		self.text2_rect = self.text2.get_rect(center=(10+8*24, WINDOW_Y-20))
		self.text3_rect = self.text3.get_rect(center=(10+8*40, WINDOW_Y-20))

	def get_tiles(self, start_selection, end_selection):
		x1 = (start_selection[0]-10)//48
		y1 = (start_selection[1]+self.tileset_scroll-10)//48
		x2 = (end_selection[0]-10)//48
		y2 = (end_selection[1]+self.tileset_scroll-10)//48
		xmin, xmax = min(x1, x2), max(x1, x2)
		ymin, ymax = min(y1, y2), max(y1, y2)
		self.current_tiles = [[None for _ in range(ymax-ymin+1)] for _ in range(xmax-xmin+1)]
		for x in range(xmin, xmax+1):
			for y in range(ymin, ymax+1):
				if self.current_tileset_type == "A":
					if y < 2:
						self.current_tiles[x-xmin][y-ymin] = ("A1", y*8+x)
					elif y < 6:
						self.current_tiles[x-xmin][y-ymin] = ("A2", (y-2)*8+x)
					elif y < 10:
						self.current_tiles[x-xmin][y-ymin] = ("A3", (y-6)*8+x)
					elif y < 16:
						self.current_tiles[x-xmin][y-ymin] = ("A4", (y-10)*8+x)
					else:
						self.current_tiles[x-xmin][y-ymin] = ("A5", (y-16)*8+x)
				else:
					self.current_tiles[x-xmin][y-ymin] = (self.current_tileset_type, y*8+x)

	def filler_action(self, pos):
		x, y = pos
		if len(self.current_tiles) == 1 and len(self.current_tiles[0]) == 1:
			tile_hitbox = self.map.tileset[self.current_tiles[0][0]].hitbox
			cibled_tile = self.map.tile_map[x][y][-1]
			replace_tile = self.current_tiles[0][0]
			pile = []
			pile.append((x, y))
			while pile != []:
				x1, y1 = pile.pop()
				for i in range(tile_hitbox+1, 3):
					self.map.tile_map[x1][y1] = [("B", 0)]
				seen = False
				tile_list = []
				for tile_2 in self.map.tile_map[x1][y1]:
					if tile_2 == replace_tile:
						seen = True
					if not seen:
						tile_list.append(tile_2)
				tile_list.append(replace_tile)
				self.map.tile_map[x1][y1] = tile_list
				if not x1 == self.map.size[0]-1 and self.map.tile_map[x1+1][y1][-1] == cibled_tile:
					pile.append((x1+1, y1))
				if not x1 == 0 and self.map.tile_map[x1-1][y1][-1] == cibled_tile:
					pile.append((x1-1, y1))
				if not y1 == self.map.size[1]-1 and self.map.tile_map[x1][y1+1][-1] == cibled_tile:
					pile.append((x1, y1+1))
				if not y1 == 0 and self.map.tile_map[x1][y1-1][-1] == cibled_tile:
					pile.append((x1, y1-1))

	def create_new_map(self):
		name = ""
		size = (-1, -1)
		tileset_id = -1
		fenetre = tk.Tk()
		fenetre.title("Créer un nouvelle Map")
		fenetre.resizable(False, False)
		label_name = tk.Label(fenetre, text="Nom de la map :")
		label_name.grid(row=0, column=0)
		entry_name = tk.Entry(fenetre, width=20)
		entry_name.grid(row=0, column=1)
		label_size = tk.Label(fenetre, text="Dimension de la map")
		label_size.grid(row=1, column=0)
		frame_size = tk.Frame(fenetre)
		entry_x_size = tk.Entry(frame_size, width=10)
		entry_x_size.grid(row=0, column=0)
		entry_y_size = tk.Entry(frame_size, width=10)
		entry_y_size.grid(row=0, column=1)
		frame_size.grid(row=1, column=1)
		label_tileset = tk.Label(fenetre, text="ID du tileset")
		label_tileset.grid(row=2, column=0)
		entry_tileset = tk.Entry(fenetre, width=2)
		entry_tileset.grid(row=2, column=1)
		def new_map():
			if not entry_name.get() == "":
				name=entry_name.get()
			if not entry_x_size == "" or entry_y_size == "":
				size = (int(entry_x_size.get()), int(entry_y_size.get()))
			if not entry_tileset.get() == "":
				tileset_id = int(entry_tileset.get())
			if not name == "" or size == (-1, -1) or tileset_id == -1:
				self.map = GE.mapsystem.Map(size, tileset_id)
				self.map.name = name
			fenetre.destroy()
		button_validate = tk.Button(fenetre, text="Valider", command=new_map)
		button_validate.grid(row=3, column=1)
		fenetre.mainloop()


	def save_current_map(self):
		fenetre = tk.Tk()
		fenetre.geometry("0x0")
		filename = tkfd.asksaveasfilename(title="Enregistrer la map", defaultextension=".sha", filetypes=[("Map", ".sha"), ("Tous", "*")], initialdir="GameAssets\\Maps\\")
		fenetre.destroy()
		if not filename == "":
			with open(filename, "w") as file:
				file.write("Name={}\n".format(self.map.name))
				file.write("Size={}\n".format(self.map.size))
				file.write("TilesetId={}\n".format(self.map.tileset.tileset_id))
				file.write("BGM={}\n".format(self.map.BGM))
				tiles = []
				for x in range(self.map.size[0]):
					for y in range(self.map.size[1]):
						for level in range(3):
							for tile in self.map.tile_map[level][x][y]:
								if not tile == ("B", 0):
									tiles.append(str((tile, (x, y))))
				file.write("Tiles={}\n".format(";".join(tiles)))
				file.close()

	def load_map(self):
		fenetre = tk.Tk()
		fenetre.geometry("0x0")
		filename = tkfd.askopenfilename(title="Ouvrir une map", defaultextension=".sha", filetypes=[("Map", ".sha"), ("Tous", "*")], initialdir="GameAssets\\Maps\\")
		fenetre.destroy()
		if not filename == "":
			name = ""
			size = (-1, -1)
			BGM = ""
			tileset_id = -1
			tiles = []
			with open(filename, "r") as file:
				for line in file:
					if not line == "":
						label, content = line[:-1].split("=")
						if label == "Name":
							name = content
						elif label == "Size":
							size = eval(content)
						elif label == "BGM":
							BGM = content
						elif label == "TilesetId":
							tileset_id = int(content)
						elif label == "Tiles":
							tiles = [eval(tile) for tile in content.split(";")]
				self.map = GE.mapsystem.Map(size, tileset_id, tiles)
				self.map.name = name
				self.map.BGM = BGM
				file.close()

	def mainloop(self):
		""" Lancement de l'application """
		self.running = True
		clock = pygame.time.Clock()
		pygame.time.set_timer(self.FPS_UPDATE, 500)

		while self.running:
			clock.tick(MAX_FPS)
			mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()

			# Gestion des evennements de l'application
			for event in pygame.event.get():
				if event.type == QUIT:
					# On quitte l'application
					self.running = False

				elif event.type == self.FPS_UPDATE:
					self.fps = max(MIN_FPS, clock.get_fps())

				elif event.type == KEYDOWN:
					tkey = pygame.key.get_pressed()
					if event.key == K_F1:
						# On crée une nouvelle map
						self.create_new_map()

					elif event.key == K_F2:
						self.current_tool = "pencil"

					elif event.key == K_F3:
						self.current_tool = "rectangle"

					elif event.key == K_F4:
						self.current_tool = "filler"

					elif event.key == K_F5:
						self.save_current_map()

					elif event.key == K_F6:
						self.load_map()

					elif event.key == K_s:
						if tkey[K_LCTRL] or tkey[K_RCTRL]:
							self.save_current_map()

				elif event.type == MOUSEBUTTONDOWN:
					if 40+8*48 <= mouse_pos_x <= WINDOW_X-30 and WINDOW_Y-30 <= mouse_pos_y <= WINDOW_Y-10:
						# On débloque le scroll x de la map
						self.scrolling_x_map = True

					elif WINDOW_X-30 <= mouse_pos_x <= WINDOW_X-10 and 10 <= mouse_pos_y <= WINDOW_Y-30:
						# On débloque le scroll y de la map
						self.scrolling_y_map = True

					elif 10+8*48 <= mouse_pos_x <= 30+8*48 and 10 <= mouse_pos_y <= WINDOW_Y-30:
						# On débloque le scroll de tileset
						self.scrolling_tileset = True

					elif 8*48+40 <= mouse_pos_x <= WINDOW_X-30 and 10 <= mouse_pos_y <= WINDOW_Y-30:
						# On active l'outil selectionné
						if self.current_tool == "pencil":
							self.pencil = True

						elif self.current_tool == "rectangle":
							self.rectangle = True
							self.start_selection = (mouse_pos_x, mouse_pos_y)

						else:
							pos = (mouse_pos_x+self.camera[0]-40-8*48)//48, (mouse_pos_y+self.camera[0]-10)//48
							self.filler_action(pos)

					elif 10 <= mouse_pos_x <= 10+8*48 and 10 <= mouse_pos_y <= WINDOW_Y-30:
						# On débloque la selection de tiles
						self.select_tiles = True
						self.start_selection = (mouse_pos_x, mouse_pos_y)

					elif 10 <= mouse_pos_x <= 10+8*16 and WINDOW_Y-30 <= mouse_pos_y <= WINDOW_Y-10:
						# On selectionne le type A de tileset
						self.current_tileset_type = "A"

					elif 10+8*16 <= mouse_pos_x <= 10+8*32 and WINDOW_Y-30 <= mouse_pos_y <= WINDOW_Y-10:
						# On selectionne le type B de tileset
						self.current_tileset_type = "B"

					elif 10+8*32 <= mouse_pos_x <= 10+8*48 and WINDOW_Y-30 <= mouse_pos_y <= WINDOW_Y-10:
						# On selectionne le type C de tileset
						self.current_tileset_type = "C"

					else:
						pass

				elif event.type == MOUSEBUTTONUP:
					self.end_selection = (mouse_pos_x, mouse_pos_y)
					self.scrolling_x_map = False
					self.scrolling_y_map = False
					self.scrolling_tileset = False
					self.pencil = False
					if self.rectangle:
						x1, y1 = self.start_selection
						x2, y2 = self.end_selection
						xmin, xmax = min(x1, x2), max(x1, x2)
						ymin, ymax = min(y1, y2), max(y1, y2)
						tile_xmin = (xmin+self.camera[0]-40-8*48)//48
						tile_xmax = (xmax+self.camera[0]-40-8*48)//48
						tile_ymin = (ymin+self.camera[1]-10)//48
						tile_ymax = (ymax+self.camera[1]-10)//48
						for x1 in range(tile_xmin, tile_xmax+1):
							for y1 in range(tile_ymin, tile_ymax+1):
								tile_pos = x1, y1
								for x, line in enumerate(self.current_tiles):
									for y, tile in enumerate(line):
										tile_hitbox = self.map.tileset[tile].hitbox
										if not (tile_pos[0]+x >= self.map.size[0] or tile_pos[1]+y >= self.map.size[1]):
											for i in range(tile_hitbox+1, 3):
												self.map.tile_map[tile_pos[0]+x][tile_pos[1]+y] = [("B", 0)]

											seen = False
											tile_list = []
											for tile_2 in self.map.tile_map[tile_pos[0]+x][tile_pos[1]+y]:
												if tile_2 == tile:
													seen = True
												if not seen:
													tile_list.append(tile_2)
											tile_list.append(tile)
											self.map.tile_map[tile_pos[0]+x][tile_pos[1]+y] = tile_list
					self.rectangle = False
					self.filler = False
					self.select_tiles = False

				else:
					pass

			# Partie de calcul de la frame

			# Calcul des scrolls
			scroll_x_map_size = min(21*48, (21*48)**2/(self.map.size[0]*48))
			scroll_y_map_size = min(21*48, (21*48)**2/(self.map.size[1]*48))
			scroll_x_map = min(21*48-scroll_x_map_size, 21*48*(self.camera[0]/(self.map.size[0]*48)))
			scroll_y_map = min(21*48-scroll_y_map_size, 21*48*(self.camera[1]/(self.map.size[1]*48)))
			if self.current_tileset_type == "A":
				nb_tile = len(self.map.tileset.tiles["A1"]) + len(self.map.tileset.tiles["A2"]) + len(self.map.tileset.tiles["A3"]) + len(self.map.tileset.tiles["A4"]) + len(self.map.tileset.tiles["A5"])
			else:
				nb_tile = len(self.map.tileset.tiles[self.current_tileset_type])
			scroll_tileset_size = min(21*48, (21*48)**2/((nb_tile//8)*48))
			scroll_tileset = min(21*48-scroll_tileset_size, 21*48*(self.tileset_scroll/((nb_tile//8)*48)))

			# Evennements de scroll
			if self.scrolling_x_map:
				self.camera[0] = int(max(0, min(self.map.size[0]*48-21*48, (mouse_pos_x-8*48-40-scroll_x_map_size/2)/(21*48)*(self.map.size[0]*48))))

			if self.scrolling_y_map:
				self.camera[1] = int(max(0, min(self.map.size[1]*48-21*48, (mouse_pos_y-10-scroll_y_map_size/2)/(21*48)*(self.map.size[1]*48))))

			if self.scrolling_tileset:
				self.tileset_scroll = int(max(0, min(nb_tile//8*48-21*48, (mouse_pos_y-10-scroll_tileset_size/2)/(21*48)*(nb_tile//8*48))))

			# Evennements de selection
			if self.select_tiles:
				self.get_tiles(self.start_selection, (mouse_pos_x, mouse_pos_y))

			# Evennements d'outil
			if self.pencil:
				tile_pos = (self.camera[0]+mouse_pos_x-8*48-40)//48, (self.camera[1]+mouse_pos_y-10)//48
				for x, line in enumerate(self.current_tiles):
					for y, tile in enumerate(line):
						tile_hitbox = self.map.tileset[tile].hitbox
						if not (tile_pos[0]+x >= self.map.size[0] or tile_pos[1]+y >= self.map.size[1]):
							for i in range(tile_hitbox+1, 3):
								self.map.tile_map[tile_pos[0]+x][tile_pos[1]+y] = [("B", 0)]

							seen = False
							tile_list = []
							for tile_2 in self.map.tile_map[tile_pos[0]+x][tile_pos[1]+y]:
								if tile_2 == tile:
									seen = True
								if not seen:
									tile_list.append(tile_2)
							tile_list.append(tile)
							self.map.tile_map[tile_pos[0]+x][tile_pos[1]+y] = tile_list

			# Affichage de la frame
			self.display.fill((255, 255, 255))
			pygame.draw.rect(self.display, (100, 100, 100), (WINDOW_X-30, 10+scroll_y_map, 20, scroll_y_map_size))
			pygame.draw.rect(self.display, (100, 100, 100), (8*48+40+scroll_x_map, WINDOW_Y-30, scroll_x_map_size, 20))
			self.map.update(self.fps, self.camera)
			self.display.blit(self.map.layout1, (8*48+40, 10))
			self.display.blit(self.map.layout2, (8*48+40, 10))
			if self.current_tileset_type == "A":
				x = 0
				for tile in self.map.tileset.tiles["A1"]:
					self.display.blit(tile.pictures[0][0], ((x%8)*48+10, (x//8)*48+10-self.tileset_scroll))
					x += 1

				for tile in self.map.tileset.tiles["A2"]:
					self.display.blit(tile.pictures[0][0], ((x%8)*48+10, (x//8)*48+10-self.tileset_scroll))
					x += 1

				for tile in self.map.tileset.tiles["A3"]:
					self.display.blit(tile.pictures[0][0], ((x%8)*48+10, (x//8)*48+10-self.tileset_scroll))
					x += 1

				for tile in self.map.tileset.tiles["A4"]:
					self.display.blit(tile.pictures[0][0], ((x%8)*48+10, (x//8)*48+10-self.tileset_scroll))
					x += 1
				for tile in self.map.tileset.tiles["A5"]:
					self.display.blit(tile.pictures[0][0], ((x%8)*48+10, (x//8)*48+10-self.tileset_scroll))
					x += 1

			else:
				for x, tile in enumerate(self.map.tileset.tiles[self.current_tileset_type]):
					self.display.blit(tile.pictures[0][0], ((x%8)*48+10, (x//8)*48+10-self.tileset_scroll))

			pygame.draw.rect(self.display, (100, 100, 100), (10+8*48, 10+scroll_tileset, 20, scroll_tileset_size))

			if self.current_tileset_type == "A":
				pygame.draw.rect(self.display, (100, 200, 0), (10, WINDOW_Y-30, 8*16, 20))
			else:
				pygame.draw.rect(self.display, (200, 200, 200), (10, WINDOW_Y-30, 8*16, 20))

			if self.current_tileset_type == "B":
				pygame.draw.rect(self.display, (100, 200, 0), (10+8*16, WINDOW_Y-30, 8*16, 20))
			else:
				pygame.draw.rect(self.display, (200, 200, 200), (10+8*16, WINDOW_Y-30, 8*16, 20))

			if self.current_tileset_type == "C":
				pygame.draw.rect(self.display, (100, 200, 0), (10+8*32, WINDOW_Y-30, 8*16, 20))
			else:
				pygame.draw.rect(self.display, (200, 200, 200), (10+8*32, WINDOW_Y-30, 8*16, 20))

			if self.current_tileset_type == "A":
				dico_adder = {"A1": 0, "A2": 2, "A3": 6, "A4": 10, "A5": 16, "B": 0, "C": 0}
				x = 10+(self.current_tiles[0][0][1]%8)*48
				y = 10+(self.current_tiles[0][0][1]//8+dico_adder[self.current_tiles[0][0][0]])*48-self.tileset_scroll
				lx = abs((self.current_tiles[0][0][1]%8-self.current_tiles[len(self.current_tiles)-1][len(self.current_tiles[0])-1][1]%8))*48+48
				ly = abs((self.current_tiles[0][0][1]//8+dico_adder[self.current_tiles[0][0][0]]-self.current_tiles[len(self.current_tiles)-1][len(self.current_tiles[0])-1][1]//8-dico_adder[self.current_tiles[len(self.current_tiles)-1][len(self.current_tiles[0])-1][0]]))*48+48

			else:
				x = 10+(self.current_tiles[0][0][1]%8)*48
				y = 10+(self.current_tiles[0][0][1]//8)*48-self.tileset_scroll
				lx = abs((self.current_tiles[0][0][1]%8-self.current_tiles[len(self.current_tiles)-1][len(self.current_tiles[0])-1][1]%8))*48+48
				ly = abs((self.current_tiles[0][0][1]//8-self.current_tiles[len(self.current_tiles)-1][len(self.current_tiles[0])-1][1]//8))*48+48

			if self.rectangle:
				x = (min(self.start_selection[0], mouse_pos_x)+self.camera[0]-8*48-40)//48*48+40+8*48-self.camera[0]
				y = (min(self.start_selection[1], mouse_pos_y)+self.camera[1]-10)//48*48+10-self.camera[1]
				lx = (((max(self.start_selection[0], mouse_pos_x)+self.camera[0]-8*48-40)//48)-((min(self.start_selection[0], mouse_pos_x)+self.camera[0]-8*48-40)//48))*48+48
				ly = (((max(self.start_selection[1], mouse_pos_y)+self.camera[1]-10)//48)-((min(self.start_selection[1], mouse_pos_y)+self.camera[1]-10)//48))*48+48
				pygame.draw.rect(self.display, (100, 100, 100), (x, y, lx, ly), 4)

			pygame.draw.rect(self.display, (100, 100, 100), (x, y, lx, ly), 4)

			self.display.blit(self.text1, self.text1_rect)
			self.display.blit(self.text2, self.text2_rect)
			self.display.blit(self.text3, self.text3_rect)

			self.display.blit(self.background, (0, 0))

			pygame.display.flip()

#§ Lancement de l'application
if __name__ == "__main__":
	app = App()
	app.mainloop()
