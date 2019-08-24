#!usr/bin/env python
#-*-coding: utf-8-*-

#§ Création des variables d'information
__version__ = "1.0.0"
__authors__ = "Lightpearl"

#§ Importation des modules nécéssaires
import GameEngine as GE
import GameEngine.constants as cts
import pygame

pygame.init()

display = pygame.display.set_mode(cts.WINDOW_SIZE, cts.HWSURFACE | cts.DOUBLEBUF)

"""GE.scenesystem.SCENES["TitleScreen"].loop(display)"""
GE.mapsystem.init()
MAP = GE.mapsystem.MAPS["MAP001"]
print(MAP.hitbox_map)
clock = pygame.time.Clock()
FPS_UPDATE = cts.USEREVENT + 1
pygame.time.set_timer(FPS_UPDATE, 5000)
fps = cts.MIN_FPS
while True:
	clock.tick()
	
	for event in pygame.event.get():
		if event.type == cts.QUIT:
			pygame.quit()

		elif event.type == FPS_UPDATE:
			fps = int(clock.get_fps())
			print(fps)

		else:
			pass
	display.fill((0, 0, 0))
	MAP.update(max(cts.MIN_FPS, fps), (0, 0))
	display.blit(MAP.layout1, (0, 0))
	display.blit(MAP.layout2, (0, 0))
	pygame.display.flip()



