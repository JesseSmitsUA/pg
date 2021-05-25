#!/usr/bin/python

"""
So how to change a bool value? 
1) Read out the _bytearray your boolean values are in. 
2) In this byte_array you need to find the byte (byteindex) 
3) Find the bit in this byte (bitindex) so you can 
4) set the correct value with utility function set_bool which does all the hard work.
set_bool(_bytearray = data which you read out before.., byte_index, bool_index, value),
5) write back the changed bytearray back to the PLC.
A round trip wil take 5ms.
The example code
https://github.com/gijzelaerr/python-snap7/blob/master/example/
the minimun amount of data being read or written to a plc is 1 byte.
"""

import threading
import time
from datetime import datetime
import snap7
import requests
import os


# create/export env values in pi station: sudo nano /etc/profile

HOME = os.environ.get('HOME', '/home')
EP = os.environ.get('EP', 'root@0.0.0.0')
EPFR = os.environ.get('EPFR', '~/recordings/')
EPFL = os.environ.get('EPFL', '~/labels/')

# Threated plc read
def pull(plc):
	storage = 0
	while True:
		# load the PLC contents
		t = plc.db_read(43, 0, 15)    # read 1 byte from db 31 staring from byte 120
		# read the contents
		print(t[0])
		triggerprev = True if t[0]&128 != 0 else False
		trigger = snap7.util.get_bool(t,0,0)
		trigger2 = True if snap7.util.get_usint(t, 0) == 1 else False
		# print both
		print("trigger ",t[0], triggerprev, trigger, trigger2)


		id = int.from_bytes(t[2:4], byteorder='big',  signed=False)
		id2 = snap7.util.get_int(t, 2)
		# print both 
		print("id ", id, id2)

		position = t[4] >> 4
		# debug printing
		print("pos ", position)
		for value in reading[0:5]:
			print("Byte: ", value)
		#handle trigger
		if trigger:
			# startMEMS()
			x = threading.Thread(target=startMEMS,args=(trayID,))
			x.start()
		# handle block
		if storage != t[6]:
			handleBlock(t[6:10])
		# dont need to process others since PLC read every 0.1 sec (FIFO)
		time.sleep(0.1)

def startMEMS(trayID):
	t = str(datetime.utcnow())
	fn = (str(trayID) + "_" + t).replace(" ", "-")
	# call blocking thread
	o = os.system("arecord -D dmic_sv -c2 -r 44100 -f S32_LE -t wav -V mono  -d 1 {s}.wav".format(s=fn))
	# push sample to endpoint
	o = os.system("scp ./{s}.wav {ep}:{p}".format(s=fn, ep=EP,p=EPFR))

def handleBlock(bArray):
	id = int.from_bytes(t[0:2], byteorder='big',  signed=False)
	id2 = snap7.util.get_int(t, 0)
	# print both 
	print("blockid: ", id, id2)
	r = snap7.util.get_bool(bArray,2,0)
	result = True if bArray[2]&128 != 0 else False
	print("result block: ", r, result)
	position = bArray[3] >> 4
	print("block position: ", position)
	# forward to sharepoint ...


def pushData(sample,id, classification = None):
	if classification != None:
		url = 'sharepoint.pg'
		d = {'id': id, 'label': classification}
		x = requests.post(url, data = d)

def setupFS():
	os.system("mkdir {l}".format(l=EPFL[:-1]))
	os.system("mkdir {r}".format(r=EPFR[:-1]))
	os.system("touch {f}".format(f=EPFL+"labels.txt"))    

if __name__ == "__main__":

	setupFS()
	# os.system("cd ~")
	# startMEMS(123)

	print("listening...")
	plc = snap7.client.Client()
	plc.connect('10.2.60.1', 0, 0)
	thread.start_new_thread(pull,(plc, ))
	x = threading.Thread(target=pull,args=(plc,))
	x.start()
	x.join()
