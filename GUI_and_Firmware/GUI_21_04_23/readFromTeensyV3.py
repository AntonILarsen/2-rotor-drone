#Bruges kun til TEST

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



serUSB = serial.Serial("/dev/ttyACM0", 9600) #Read from usb
# serGPIO = serial.Serial("/dev/serial0", 9600) #Read from GPIO
# serGPIO.flushInput()
serUSB.flushInput()
#ser.write((input_freq_start+';'+input_freq_stop+';'+input_freq_step+'\n').encode())

data = ''
Sweep = True
Input = False
receivedtotal=""
#while Sweep == True:
while True:
    # if serGPIO.inWaiting()>0:
        # receivedGPIO = serGPIO.readline().decode('ascii')
        # print(receivedGPIO)
    if serUSB.inWaiting()>0:
        receivedUSB = serUSB.readline().decode('ascii')
        split=receivedUSB.split()
        if split[0][3:6] =="pos":
          dataString=split[1:5]
          dataFloat=[float(dataString[0]),float(dataString[1]),float(dataString[2]),float(dataString[3])]
          print(str(dataFloat))
    time.sleep(0.1)
    serUSB.flushInput()
         
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
