import net.client as net
import cv2
import numpy
import time

client = net.StreamClient(2500)
client.connect()
while 1:
	data = client.receive()
	if data is None:
		break
	elif len(data) == 0:
		print("No connection")
	else:
		img = data["img"]
		cv2.imshow("img", numpy.array(img, dtype=numpy.uint8))
		cv2.waitKey(0)
		print("new image shown")
		client.send(client.getDefaultData())
