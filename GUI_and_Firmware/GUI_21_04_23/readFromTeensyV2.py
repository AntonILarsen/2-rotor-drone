# from uusb import UUsb 

#HUSK AT SUB INDE FRA GUI'EN FøRST, DEREFTER LUK GUI
#sub med 10ms

import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
import time as time
import re
import serial
import csv
import struct
#from drawnow import *


#input_freq_start = '15500000'#input('Enter starting frequency: ')
#input_freq_stop = '16500000'#input('Enter stopping frequency: ')
#input_freq_step = '100'#input('Enter frequency stepsize: ')



serUSB = serial.Serial("/dev/ttyACM0", 9600) #Read from usb /dev/ttyACM0
# serGPIO = serial.Serial("/dev/serial0", 9600) #Read from GPIO
# serGPIO.flushInput()
serUSB.flushInput()
#ser.write((input_freq_start+';'+input_freq_stop+';'+input_freq_step+'\n').encode())

data = ''
Sweep = True
Input = False
receivedtotal=""
#while Sweep == True:
def readFromUSB(serUSB):
        serUSB.flushInput()
        receivedUSB = serUSB.readline().decode('ascii')
        split=receivedUSB.split()
        if split[0][3:6] =="pos":
          dataString=split[1:5]
          dataFloat=[float(dataString[0]),float(dataString[1]),float(dataString[2]),float(dataString[3])]
          print(str(dataFloat))
          if dataFloat[3]!=0: #checks if height is zero.
            readFromUSB.prevVal=dataFloat
            return dataFloat
          else:
            return readFromUSB.prevVal
        else:
          return readFromUSB.prevVal
readFromUSB.prevVal=[0,0,0,0]

# while True:
  # # #print("waiting...")
  # (str(readFromUSB(serUSB)))

#ser.close()
#alti -1.17 -1.30 29.2 9.54 1 5
#brug serial 6, det er den eneste der er ledig på teensy

##TEENSY CODE###########################
# void setup() {
  # Serial.begin(9600);
  # Serial4.begin(9600);
# }
# int count =1;
# void loop() {
  # //byte b =1;
  # //Serial.write(b);
  # count+=1;
  # Serial.print(count);
  # Serial.println("HEJ from USB");
  # Serial4.print(count);
  # Serial4.println("HEJ from GPIO_PIN");
  # if (count==100)
    # count=0;
  # //delay(2000);
# }
