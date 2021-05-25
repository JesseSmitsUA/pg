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

import _thread
import time
from datetime import datetime
import os

HOME = os.environ.get('HOME', '/home')
# EP = os.environ.get('EP', 'root@0.0.0.0')
# EPFR = os.environ.get('EPFR', '~/recordings/')
# EPFL = os.environ.get('EPFL', '~/labels/')

# Threated plc read

def startMEMS(trayID):
    t = str(datetime.utcnow())
    fn = (str(trayID) + "_" + t).replace(" ", "-")
    # call blocking thread
    o = os.system("arecord -D dmic_sv -c2 -r 44100 -f S32_LE -t wav -V mono  -d 1 {s}.wav".format(s=fn))
    # push sample to endpoint
    # o = os.system("scp ./{s}.wav {ep}:{p}".format(s=fn, ep=EP,p=EPFR))



if __name__ == "__main__":
    os.system("cd {h}".format(h=HOME))
    startMEMS(123)
