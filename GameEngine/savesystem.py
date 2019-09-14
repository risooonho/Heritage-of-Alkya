#-*-coding: utf-8-*-

#§ Variables d'information du module
__version__ = "1.0.0"
__authors__ = "Lightpearl"

import os

#§ Création des objets du module
class Save:
	"""
	"""
	def __init__(self):
		self.id = 0
		self.name = "Empty"
		self.job = "unemployed"
		self.time_played = 0

	def save(self):
		with open(os.getcwd() + "/GameData/save_{}.sha".format(self.id), "w") as file:
			file.write("Save of the game [Heritage of Alkya]\n\n")
			file.write("<System Informations>\n")
			file.write("TimePlayed: {}\n".format(self.time_played))
			file.write("\n<Player Informations>\n")
			file.write("PlayerName: {}\n".format(self.name))
			file.write("PlayerClass: {}\n".format(self.job))
			file.close()

	def load(self):
		with open(os.getcwd() + "/GameData/save_{}.sha".format(self.id), "r") as file:
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