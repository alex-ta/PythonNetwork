import socket
import json

class StreamServer:
	
	def __init__ (self, port, logging = 1):
		self.socket = socket.socket()         # Create a socket object
		self.host = socket.gethostname()
		self.datasize = 5000000
		self.port = port
		self.exit = None
		self.logging = logging
		if self.logging:
			print("Created Instance")
		
	def bind(self):
		if self.logging:
			print("Server bound to "+str(self.port))
		self.socket.bind((self.host, self.port))
		self.socket.listen(1)
		self.connection, self.connectionAddr = self.socket.accept()  
	
	def pushAndWait(self, data):
		if self.logging:
			print("Send "+str(len(bytes(json.dumps(data),"UTF8")))+" bytes")
		self.connection.send(bytes(json.dumps(data),"UTF8"))
		ret = json.loads(str(self.connection.recv(self.datasize),"UTF8"))
		if ret is self.exit:
			c.close()
		return ret
		
	def getDefaultData(self, img = [], reward =	0, lastImg=[], lastKey = {"forward":0,"rotate":0,"exit":0}):
		return {"img":img, "reward":reward, "lastImg":lastImg, "lastKey":lastKey}
	


#server = StreamServer(2500)
#d = server.pushAndWait("Some Data")
#print(d)

