from tkinter import *
from tkinter import simpledialog
from PIL import Image, ImageTk
import Scripts.network.net.client as net
import cv2
import numpy as np
import time


class Gui:
	def __init__(self, width, height):
		# default
		self._port=2500
		self._hostname=""
		self._maxtimeout=1000
		self._datasize=5000000
		self._logging=True
		self._exit=False
		self._forward=0
		self._rotate=0
		self._connected=False
		self._lastdata={}
		self._stream=False
		# window component
		self.root = Tk()
		self.root.bind("<Key>", self.key)
		self.root.title("StreamClient")
		self.root.after(200, self.update)
		# main menu
		self.mainmenu = Menu(self.root)
		# option menu submenu
		self.options = Menu(self.mainmenu)
		self.options.add_command(label="Port("+str(self._port)+")", command=self.port)
		self.options.add_command(label="Hostname("+str(self._hostname)+")", command=self.hostname)
		self.options.add_command(label="Max Timout Count("+str(self._maxtimeout)+")", command=self.maxTimeout)
		self.options.add_command(label="Datasize("+str(self._datasize)+")", command=self.datasize)
		self.options.add_command(label="Logging("+str(self._logging)+")", command=self.logging)
		# main menu
		self.root.config(menu=self.mainmenu)
		self.mainmenu.add_cascade(label="Options", menu=self.options)
		self.mainmenu.add_command(label="Bind", command=self.bind)
		self.mainmenu.add_command(label="Start", command=self.stream)
		# canvas to draw images
		self.window_1 = Canvas(self.root, width=width, height=height)
		self.window_1.pack(expand=True, fill=BOTH)
	
	# setters for submenu
	def port(self):
		print("port")
		self._port = simpledialog.askinteger("", "Port:", parent=self.root)
		self.options.entryconfigure(1, label="Port("+str(self._port)+")")
	def hostname(self):
		print("hostname")
		self._hostname = simpledialog.askstring("", "Hostname:", parent=self.root)
		self.options.entryconfigure(2, label="Hostname("+str(self._hostname)+")")
	def maxTimeout(self):
		print("max timeout")
		self._maxtimeout = simpledialog.askinteger("", "Max Timout Count:", parent=self.root)
		self.options.entryconfigure(3, label="Max Timout Count("+str(self._maxtimeout)+")")
	def datasize(self):
		print("port")
		self._datasize = simpledialog.askinteger("", "Datasize(Byte):", parent=self.root)
		self.options.entryconfigure(4, label="Datasize("+str(self._datasize)+")")
	def logging(self):
		self._logging = not self._logging
		self.options.entryconfigure(5, label="Logging("+str(self._logging)+")")
		print("logging")
	# start ui
	def run(self):
		self.root.mainloop()
	# bind or unbind server
	def bind(self):
		if not self._connected:
			self.client = net.StreamClient(port=self._port, hostname = self._hostname, maxtimeout=self._maxtimeout, datasize=self._datasize, logging = self._logging)
			self.client.connect()
			self._lastdata = self.client.receive()
			self._connected = True
			self.mainmenu.entryconfigure(2, label="Unbind")
		else:
			self._exit = True
			self._disconnect()
			if not self._stream:
				self.root.after(20, self.update)
	# part of unbind
	def _disconnect(self):
		self._connected = False
		self.mainmenu.entryconfigure(2, label="Bind")
	# start or stop stream
	def stream(self):
		self._stream = not self._stream
		self.mainmenu.entryconfigure(3, label="Start")
		if self._stream:
			self.root.after(200, self.update)
			self.mainmenu.entryconfigure(3, label="Stop")
	# update loop fetching the image
	def update(self):
		print("current con & exit")
		print(self._connected)
		print(self._exit)
		if self._connected or self._exit:
			if self._lastdata is None:
				print("Connection closed")
				self._disconnect()
			elif len(self._lastdata) == 0:
				print("No connection")
				self._disconnect()
			else:
				img = self._lastdata["img"]
				img = np.array(img, dtype=np.uint8)
				img = Image.fromarray(img)
				img = ImageTk.PhotoImage(img)
				self.window_1.img=img
				self.window_1.create_image(20,20, anchor=NW, image=img)
				#cv2.imshow("img", numpy.array(img, dtype=numpy.uint8))
				#cv2.waitKey(0)
				print("new image shown")
				self.client.send(self.client.getDefaultData(forward=self._forward, rotate=self._rotate, exit=self._exit))
				self._lastdata = self.client.receive()
		self._exit=False
		if self._stream:
			self.root.after(200, self.update)
				
	def key(self,event):
		print("pressed: "+str(event.char))
				

gui = Gui(400,400)
gui.run()