#-*-coding: utf-8-*-

#§ Variables d'information du module
__version__ = "1.0.0"
__authors__ = "Lightpearl"

#§ Importation des modules complémentaires nécéssaires
from . import constants as cts
import pygame
import random
import os

# Création des variables globales au module

# Création des objets du module
class Entity:
	"""
	"""
	def __init__(self, name, pos, sprite, hitbox, walk_speed, walk_frequency, walk_schema, code_page):
		self.name = name
		self.pos = pos
		self.sprites = cut_sprites(sprite)
		self.hitbox = hitbox
		self.walk_speed = walk_speed
		self.walk_frequency = walk_frequency
		self.walk_schema = walk_schema
		self.walk_schema_cursor = 0
		self.code_page = code_page
		self.facing = "south"
		self.current_frame = 0
		self.is_walking = False
		self.walk_vector = (0, 0)
		self.walk_real_added_pos = 0

	def init_walk(self):
		if not self.is_walking:
			if walk_schema == None:
				self.facing = random.choice(["north", "south", "east", "west"])
			else:
				self.facing = walk_schema[self.walk_schema_cursor]
				self.walk_schema_cursor += 1
				self.walk_schema_cursor %= len(self.walk_schema)
			if self.facing == "north":
				self.walk_vector = (0, -1)
			elif self.facing == "south":
				self.walk_vector = (0, 1)
			elif self.facing == "east":
				self.walk_vector = (1, 0)
			else:
				self.walk_vector = (-1, 0)
			self.is_moving = True

	def move(self, fps):
		self.walk_real_added_pos += cts.TILE_SIZE//(self.walk_speed*fps)
		if int(self.walk_real_added_pos) == cts.TILE_SIZE:
			self.is_walking = False
			self.walk_real_added_pos = 0
			self.pos = self.pos[0] + self.walk_vector[0], self.pos[1] + self.walk_vector[1]
			self.walk_vector = (0, 0)

	def on_screen_pos(self, camera):
		pos_x = self.pos[0]*cts.TILE_SIZE + self.walk_vector[0]*int(self.walk_real_added_pos) - camera[0]
		pos_y = self.pos[1]*cts.TILE_SIZE + self.walk_vector[1]*int(self.walk_real_added_pos) - camera[1]
		return pos_x, pos_y

	def render(self, fps):
		pictures = self.sprites[self.facing]
		if self.is_walking:
			frame = self.current_frame//int(max(cts.MIN_FPS, fps)*self.walk_speed)%2
			if frame == 1:
				frame += 1
			picture = pictures[frame]
			self.current_frame += 1
		else:
			picture = pictures[1]
			self.current_frame = 0
		return picture

# Création des fonctions du module
def cut_sprites(sprite):
	picture = pygame.Surface((cts.SPRITE_SIZE, cts.SPRITE_SIZE), cts.HWSURFACE | cts.SRCALPHA)
	sprites = {
		"north": [],
		"south": [],
		"east": [],
		"west": []
	}

	picture.fill((0, 0, 0, 0))
	picture.blit(sprite, (0, 0))
	sprites["south"].append(picture.convert_alpha())

	picture.fill((0, 0, 0, 0))
	picture.blit(sprite, (-cts.SPRITE_SIZE, 0))
	sprites["south"].append(picture.convert_alpha())

	picture.fill((0, 0, 0, 0))
	picture.blit(sprite, (-2*cts.SPRITE_SIZE, 0))
	sprites["south"].append(picture.convert_alpha())

	picture.fill((0, 0, 0, 0))
	picture.blit(sprite, (0, -cts.SPRITE_SIZE))
	sprites["west"].append(picture.convert_alpha())

	picture.fill((0, 0, 0, 0))
	picture.blit(sprite, (-cts.SPRITE_SIZE, -cts.SPRITE_SIZE))
	sprites["west"].append(picture.convert_alpha())

	picture.fill((0, 0, 0, 0))
	picture.blit(sprite, (-2*cts.SPRITE_SIZE, -cts.SPRITE_SIZE))
	sprites["west"].append(picture.convert_alpha())

	picture.fill((0, 0, 0, 0))
	picture.blit(sprite, (0, -2*cts.SPRITE_SIZE))
	sprites["east"].append(picture.convert_alpha())

	picture.fill((0, 0, 0, 0))
	picture.blit(sprite, (-cts.SPRITE_SIZE, -2*cts.SPRITE_SIZE))
	sprites["east"].append(picture.convert_alpha())

	picture.fill((0, 0, 0, 0))
	picture.blit(sprite, (-2*cts.SPRITE_SIZE, -2*cts.SPRITE_SIZE))
	sprites["east"].append(picture.convert_alpha())

	picture.fill((0, 0, 0, 0))
	picture.blit(sprite, (0, -3*cts.SPRITE_SIZE))
	sprites["north"].append(picture.convert_alpha())

	picture.fill((0, 0, 0, 0))
	picture.blit(sprite, (-cts.SPRITE_SIZE, -3*cts.SPRITE_SIZE))
	sprites["north"].append(picture.convert_alpha())

	picture.fill((0, 0, 0, 0))
	picture.blit(sprite, (-2*cts.SPRITE_SIZE, -3*cts.SPRITE_SIZE))
	sprites["north"].append(picture.convert_alpha())

	return sprites

# Création des contenants du module
