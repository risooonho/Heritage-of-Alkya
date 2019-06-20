#-*-coding: utf-8-*-

#§ Création des variables d'information
__version__ = "1.0.0"
__authors__ = "Lightpearl"

#§ Importation des modules complémentaires nécéssaires
from . import constants as cts
from multiprocessing import Queue
import threading

#§ Création des variables gloables du module
THREADS = []

#§ Création des objets du module
class Worker(threading.Thread):
	"""
	"""
	def __init__(self, name, task, *args, **kwargs):
		threading.Thread.__init__(self)
		self.name = name
		self.task = task
		self.args = args
		self.kwargs = kwargs
		self.process = Queue()
		THREADS.append(self)

	def run(self):
		self.task(*self.args, **self.kwargs)
