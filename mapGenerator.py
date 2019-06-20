#!usr/bin/env python
#-*-coding: utf-8-*-

#§ Création des variables d'information
__version__ = "1.0.0"
__authors__ = "Lightpearl"

#§ Importation des modules complémentaires nécéssaires
import GameEngine as GE
from GameEngine.constants import *
import pygame
import tkinter.filedialog as tkfd

#§ Création des variables globales du programme
WINDOW_X = 21*48+8*48+50
WINDOW_Y = 17*48+40
GE.mapsystem.cts.TILE_NUMBER_X = 21
GE.mapsystem.cts.TILE_NUMBER_Y = 17
GE.mapsystem.cts.WINDOW_SIZE = (21*48, 17*48)

#§ Création des objets du jeu
class App:
	"""
	"""
	def __init__(self):
		self.display = pygame.display.set_mode((WINDOW_X, WINDOW_Y), HWSURFACE | SRCALPHA)
		self.running = False
		self.camera_pos = [0, 0]
		self.map = None
		self.tiles = []

	def mainloop(self):
		# Création des booléens
		self.running = True
		side_bar_x_click = False
		side_bar_y_click = False

		# Création des informations de temps de l'application
		fps = MIN_FPS

		clock = pygame.time.Clock()

		# Création des timers de l'application
		FPS_UPDATE = USEREVENT + 1

		pygame.time.set_timer(FPS_UPDATE, 500)

		while self.running:
			# Gestion des temps
			clock.tick(MAX_FPS)

			# Prise en compte des evennements créés par l'utilisateur
			for event in pygame.event.get():
				if event.type == QUIT:
					self.running = False

				if event.type == FPS_UPDATE:
					fps = max(MIN_FPS, clock.get_fps())

				if event.type == KEYDOWN:
					if event.key == K_F1:
						self.map = GE.mapsystem.Map((100, 50), 0, tiles=[(("A2", 0), (x%100, x//100)) for x in range(100*50)])
						self.tiles = []

				if event.type == MOUSEBUTTONDOWN:
					pos_x, pos_y = pygame.mouse.get_pos()
					if 20+8*48 <= pos_x <= WINDOW_X-30 and WINDOW_Y-30 <= pos_y <= WINDOW_Y-10 and not self.map == None:
						side_bar_x_click = True
					elif WINDOW_X-30 <= pos_x <= WINDOW_X-10 and 10 <= pos_y <= WINDOW_Y-30 and not self.map == None:
						side_bar_y_click = True

				if event.type == MOUSEBUTTONUP:
					side_bar_x_click = False
					side_bar_y_click = False

			# Processus logique de la frame
			if not self.map == None:
				side_bar_x_size = min(21*48, (21*48)*(21*48)/(self.map.size[0]*48))
				side_bar_y_size = min(17*48, (17*48)*(17*48)/(self.map.size[1]*48))
				side_bar_x = min(21*48-side_bar_x_size, 21*48*(self.camera_pos[0]/(self.map.size[0]*48)))
				side_bar_y = min(17*48-side_bar_y_size, 17*48*(self.camera_pos[1]/(self.map.size[1]*48)))
			else:
				side_bar_x = 0
				side_bar_y = 0
				side_bar_x_size = 21*48
				side_bar_y_size = 17*48

			if side_bar_x_click:
				pos_x, pos_y = pygame.mouse.get_pos()
				self.camera_pos[0] = int(max(0, min(self.map.size[0]*48-21*48, (pos_x-8*48-20-side_bar_x_size/2)/(21*48)*(self.map.size[0]*48))))

			if side_bar_y_click:
				pos_x, pos_y = pygame.mouse.get_pos()
				self.camera_pos[1] = int(max(0, min(self.map.size[1]*48-17*48, (pos_y-10-side_bar_y_size/2)/(17*48)*(self.map.size[1]*48))))

			# Affichage de la frame
			self.display.fill((255, 255, 255))
			pygame.draw.rect(self.display, (0, 0, 0), (8*48+10, 0, 10, WINDOW_Y))
			pygame.draw.rect(self.display, (0, 0, 0), (0, 0, WINDOW_X, 10))
			pygame.draw.rect(self.display, (0, 0, 0), (0, WINDOW_Y-10, WINDOW_X, 10))
			pygame.draw.rect(self.display, (0, 0, 0), (0, 0, 10, WINDOW_Y))
			pygame.draw.rect(self.display, (0, 0, 0), (WINDOW_X-10, 0, 10, WINDOW_Y))
			pygame.draw.rect(self.display, (0, 0, 0), (WINDOW_X-30, WINDOW_Y-30, 20, 20))
			pygame.draw.rect(self.display, (100, 100, 100), (8*48+20+side_bar_x, WINDOW_Y-30, side_bar_x_size, 20))
			pygame.draw.rect(self.display, (100, 100, 100), (WINDOW_X-30, 10+side_bar_y, 20, side_bar_y_size))
			if not self.map == None:
				self.map.update(fps, self.camera_pos)
				for layout in self.map.layouts:
					self.display.blit(layout, (8*48+20, 10))
				x = 0
				for tile in self.map.tileset.tiles["A1"]:
					self.display.blit(tile.pictures[0][0], ((x%8)*48+10, (x//8)*48+10))
					x += 1

				for tile in self.map.tileset.tiles["A2"]:
					self.display.blit(tile.pictures[0][0], ((x%8)*48+10, (x//8)*48+10))
					x += 1

			pygame.display.flip()

#§ Lancement du programme
pygame.init()
app = App()
app.mainloop()