from net.server import StreamServer
import socket
import json
import cv2
import numpy

data = cv2.imread("images.jpg")
server = StreamServer(2500)
exit = 0
server.bind()
while not exit:
	print("wait")
	d = server.pushAndWait(server.getDefaultData(img = data.tolist()))
	exit = d["key"]["exit"]
	print(d)

#d = server.pushAndWait("Some Data")
#print(d)
