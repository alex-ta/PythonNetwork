import socket
import json

class StreamClient:
	def __init__ (self, port, hostname = "", maxtimeout=1000, datasize=5000000, logging = 1):
		self.socket = socket.socket()
		self.host = hostname
		if len(self.host) == 0:
			self.host = socket.gethostname()
		self.maxtimeout = maxtimeout
		self.timeout = 0
		self.exit = None
		self.datasize = datasize
		self.port = port
		self.logging = logging
		if self.logging:
			print("Created Instance")
			
	def connect(self):
		if self.logging:
			print("Connecting to "+self.host+" "+str(self.port))
		self.socket.connect((self.host, self.port))
	
	def receive(self):
		data = self.socket.recv(self.datasize)
		if self.logging:
			print("Send "+str(len(data))+" bytes")
		if data is self.exit:
			self.close()
		elif len(data) == 0:
			self.timeout = self.timeout + 1
			if self.timeout > self.maxtimeout:
				self.close()
			else:
				return ""
		else:
			self.timeout = 0
			return json.loads(str(data, "UTF8"))
		return self.exit
		
			
	def send(self, data):
		self.socket.send(bytes(json.dumps(data), "UTF8"))
	
	def close(self):
		self.socket.close()
		
	def getDefaultData(self, forward=0, rotate=0, exit=0):
		return {"key":{"forward":forward,"rotate":rotate,"exit":exit}}

#client = StreamClient(2500)
#msg = client.receive()
#client.send("Message: "+msg)