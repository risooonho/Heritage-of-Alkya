#-*-coding: utf-8-*-

#§ Variables d'information du module
__version__ = "1.0.0"
__authors__ = "Marklinmax"

#§ Importation des modules complémentaires nécéssaires
import sys
import time
import os
import datetime
from tkinter import *
from threading import Thread
from multiprocessing import Queue

#§ Création des variables gloables du module
DEFAULT_FG = "white"
DEFAULT_BG = "black"

#§ Création des objets du module
class Console(Thread, Tk):
	
	def __init__(self):
		self.running = True
		
		self.to_disp = Queue()
		self.to_execute = Queue()

		self.line_count = 0

		self.main = None
		self.text = None

		self.q = Queue()

		self.t = Thread(target=self.window, daemon=True)
		self.t.start()

		##time.sleep(1)
		##self.main.quit()
		

	def window(self):
		self.main = Tk()
		self.main.title("Console - Heritage of Alkya")

		self.text = Text(self.main, bg="black", fg="white", insertbackground="white", state=DISABLED)
		self.text.pack(side=LEFT, fill=BOTH, expand=YES)

		self.main.after(100, self.update)
			
		self.main.mainloop()
		

	def update(self, event=None):
		while self.running:
			while not self.q.empty():
				msg = self.q.get()
				if msg == "0":
					self.main.destroy()
					self.running = False
				elif msg[-1] == "text":
					fg = msg[-3]
					bg = msg[-2]
					string = msg[-4]
					
					start = self.text.index("end")
					self.text.config(state=NORMAL)
					if self.line_count != 0:
						self.text.insert("end", "\n" + string)
						self.line_count += 1
					else:
						self.text.insert("end", string)
						self.line_count += 1

					end = self.text.index("insert lineend")
					
					self.text.tag_add(string, start, end)
					self.text.tag_config(string, background=bg, foreground=fg)

					self.text.config(state=DISABLED)
					self.text.update()
			try:
				self.main.update()
			except(Exception):
				self.running = False
					

	def cprint(self, text, fg=DEFAULT_FG, bg=DEFAULT_BG):
		self.q.put((text, fg, bg, "text"))

	def stop(self):
		self.q.put("0")

class Logger:

	def __init__(self, log_abs_path, con=None, cons_enabled=True):


		if con == None and cons_enabled == True:
			self.cons = Console()
		else:
			self.cons = console

		self.cons_enabled = cons_enabled

		self.running = True

		self.abs_path = log_abs_path

		self.to_log = Queue()
		self.to_write = Queue()

		self.file = None
		self.openFile()

		self.threads = []

		self.threads.append(Thread(target=self.writer, args=(self.to_write,), daemon=True).start())

		if self.cons_enabled == True:
			self.threads.append(Thread(target=self.printer, args=(self.to_log,), daemon=True).start())
		


	def getDate(self):
		return str(datetime.datetime.today()).split(".")[0]

	def writer(self, q):
		while self.file != None and self.running:
			while not q.empty():
				try:
					self.file.write(q.get() + "\n")
				except(Exception):
					pass

	def printer(self, q):
		while self.cons_enabled:
			while not q.empty():
				msg = q.get()
				self.cons.cprint(*msg)
		self.cons.stop()
		
	def openFile(self):
		try:
			date = self.getDate().replace(":","-").replace(" ", "_")
			os.chdir(self.abs_path)
			
			ok = True
			x = 1
			name = "{}.txt".format(date)
			while ok == True:
				if name in os.listdir():
					x += 1
					name = "{}-{}.txt".format(date, x)
				else:
					ok = False
			
			self.file = open(name, "w")
		except(Exception) as error:
			print("Logger failed to open the log file.")
			print(error)

	def closeFile(self):
		try:
			self.file.close()
			self.file = None
		except(Exception) as error:
			print("Logger failed to close the log file.")
			print(error)

	def garbageCollect(self):
		for t in self.threads:
			if not t.isAlive():
				del t

	def openConsole(self, console=None):
		if self.cons == None and self.cons_enabled == False:
			if console == None:
				self.cons = Console()
			else:
				self.cons = console
			self.garbageCollect()
			self.threads.append(Thread(target=self.printer, args=(self.to_log,), daemon=True).start())
			self.cons_enabled = True
		else:
			self.log("A console is already runnig.")

	def closeConsole(self):
		if self.cons != None and self.cons_enabled == True:
			self.cons_enabled = False
		else:
			self.log("There is no console to close.")
			
			

	def log(self, text, thread_name="MAIN-THREAD", msgtype="default"):
		if not self.running:
			print("The logger is stopped and can't log anymore.")
		else:
			try:
				format_text = "[{}][{}][{}]: {}".format(self.getDate(), thread_name, msgtype.capitalize(), text)
				if msgtype == "error":
					if self.cons_enabled:
						self.to_log.put((format_text, "red"))
					self.to_write.put(format_text)
				elif msgtype == "info":
					if self.cons_enabled:
						self.to_log.put((format_text, "cyan"))
					self.to_write.put(format_text)
				elif msgtype == "warning":
					if self.cons_enabled:
						self.to_log.put((format_text, "yellow"))
					self.to_write.put(format_text)
				else:
					if self.cons_enabled:
						self.to_log.put((format_text,)) ##It is a TUPLE !
					self.to_write.put(format_text)
			except(Exception) as error:
				print("Logger failed to log the message.")
				print(error)

	def stop(self):
		while not self.to_write.empty():
			pass
		
		while not self.to_log.empty():
			pass

		self.running = False
		self.closeConsole()
		self.closeFile()

	def __del__(self):
		try:
			while not self.to_write.empty():
				pass
			
			while not self.to_log.empty():
				pass

			self.running = False
			self.closeConsole()
			self.closeFile()
			
		except(Exception):
			pass
