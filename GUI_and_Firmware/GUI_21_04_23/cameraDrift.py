# pip install opencv-python==3.4.18.65

import numpy as np
import cv2
import time
from cameraBridge import writeToBridge
import os 		#for closing terminal
import signal 	#for closing terminal
from poseBridge import poseReadFromBridge
from poseBridge import poseWriteToBridge
poseBridgeFile = open("poseBridge.txt", "r") #MINE#################################################################### 
cameraBridgeFile = open("cameraBridge.txt", "w") #MINE#################################################################### 

import serial
import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
import time as time
import re
import csv
import struct

from readFromTeensyV2 import readFromUSB
serUSB = serial.Serial("/dev/ttyACM0", 9600) #Read from usb
serUSB.flushInput()

class StreamingMovingAverage:
    def __init__(self, window_size):
        self.window_size = window_size
        self.values = []
        self.sum = 0

    def process(self, value):
        self.values.append(value)
        self.sum += value
        if len(self.values) > self.window_size:
            self.sum -= self.values.pop(0)
        return float(self.sum) / len(self.values)


cp = cv2.VideoCapture(0)
cp.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.60)
width = 640
print("width = " + str(width))
height = 480
print("height = " + str(height))
cp.set(3, width)
cp.set(4, height)
#transforms = np.zeros((n_frames-1, 3), np.float32) 

dx = 0
dy = 0
da = 0
totaldx = 0
totaldy = 0
totalda = 0

# Moving average of order: 30:
smoothdx = StreamingMovingAverage(1) #FPS = ca.30, choose movingaverage order after this
smoothdy = StreamingMovingAverage(1)
smoothda = StreamingMovingAverage(1)
smoothroll = StreamingMovingAverage(10)
smoothtotaldx = 0
smoothtotaldy = 0
smoothtotalda = 0


prev_pts = []

isTrue, curr = cp.read()

curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)
prev_gray = curr_gray

prev_frame_time = 0
new_frame_time = 0


xtest = 0
ytest = 0

prev_imu = [0,0,0]

drolltotal = 0
cmovetotal = 0 

# Initiate time
prev_frame_time = time.time()

while True:
	isTrue, curr = cp.read()
	if not isTrue:
		break
	
	#FPS calculation:
	new_frame_time = time.time()
	fps = 1/(new_frame_time-prev_frame_time)
	prev_frame_time = new_frame_time
	
	
	curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)
	
	
	try:
		#new (https://www.geeksforgeeks.org/feature-detection-and-matching-with-opencv-python/):
		#orb = cv2.ORB_create(nfeatures=80, scaleFactor=1.5, nlevels=6, edgeThreshold=20) #Can be adjusted
		#kp = orb.detect(prev_gray, None)
		#prev_pts = cv2.KeyPoint_convert(kp)
		#old (slower):
		prev_pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=50, qualityLevel=0.002, minDistance=100, blockSize=3) 
		
		# First: estimateRigidTransform. Second: np.mean.
		# maxCorners=40, qualityLevel=0.01, minDistance=30, blockSize=3
		# maxCorners=50, qualityLevel=0.002, minDistance=100, blockSize=3
		
		#Show top corners
		oldcorners = np.int0(prev_pts)
		
		for i in oldcorners:
			x,y = i.ravel()
			cv2.circle(curr,(x,y),5,(0,0,255),-1)
		
		# Track feature points
		# status = 1. if flow points are found
		# err if flow was not find the error is not defined
		# curr_pts = calculated new positions of input features in the second image
		curr_pts, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_pts, None)

		#Show top corners
		newcorners = np.int0(curr_pts)
		
		# Iterate over the corners and draw a circle at that location
		for i in newcorners:
			x,y = i.ravel()
			cv2.circle(curr,(x,y),5,(0,255,0),-1)
		
		
		# Sanity check
		assert prev_pts.shape == curr_pts.shape 
 
		# Filter only valid points
		idx = np.where(status==1)[0]
		prev_pts = prev_pts[idx]
		curr_pts = curr_pts[idx]

		# fullAffine= FAlse will set the degree of freedom to only 5 i.e translation, rotation and scaling
		# try fullAffine = True
		m = cv2.estimateRigidTransform(prev_pts, curr_pts, fullAffine=True)  # fullAffine=False
		
		motionVectors = curr_pts - prev_pts
		
		
		# # Read height from file
		# file1 = open("heightDataBridge.txt","r+") 
		# file1.seek(0) #set cursor at the beggining of txt file
		# readFromFile=file1.readlines()
		# try: #heightData = [z, dz]
			# heightData = prevHeightData
		# except:
			# heightData = [0,0]
		# try: 
			# for i in range(2):
				# splitted=(readFromFile[i+1].split())
				# if(float(splitted[0])!=0):
					# heightData[i]=float(splitted[0])
		# except:
			# pass
		# try:
			# if(abs(prevHeightData[0]-heightData[0])>1):
				# heightData[0]=prevHeightData[0]
		# except:
			# pass
		# file1.close
		# prevHeightData = heightData
		
		#print(heightData)
		
		
		#from ugyro import gyroData
		#ANTON
		# print("POSE DATA NEXT LINE")
		# print(str(poseReadFromBridge(poseBridgeFile)))
		# print("POSE DATA STOP")
		#pose = poseReadFromBridge(poseBridgeFile)
		#serUSB.flushInput()
		pose = readFromUSB(serUSB)
		#pose=[0,0,0,0]
		# print("READ FROM USB")
		# print(str(pose))
		
		imu = pose[0:3] # position in radians [roll, pitch, yaw] degrees/s (roll is x, pitch is y)
		dimu = np.array(imu) - np.array(prev_imu) #radians per frame
		
		FOVx = 1.085594795 		#in radians
		FOVy = 0.8517206750 	#in radians
		resx = 640 #pixels
		resy = 480 #pixels
		ppdx = resx/FOVx #pixels per radians
		ppdy = resy/FOVy #pixels per radians
		droll = dimu[0]*ppdx #pixels per frame
		dpitch = dimu[1]*ppdy #pixels per frame 
		
		prev_imu = imu
		
		#Calibrating drift from height data
		#height = heightData[0] #in meters
		height=pose[3]			#in meters
		offset_to_camera = 0    #in meters
		FOVx = 1.085594795 		#in radians
		FOVy = 0.8517206750 	#in radians
		resx = 640
		resy = 480
		dfiltx = (2*np.tan(FOVx/2)*(height+offset_to_camera))/resx
		dfilty = (2*np.tan(FOVx/2)*(height+offset_to_camera))/resy
		
		#print(droll)
		
		try:
			drolltotal = drolltotal + droll
			cmovetotal = cmovetotal + np.mean(motionVectors[:,0,0])
			print("DATA")
			print(drolltotal)
			print(cmovetotal)
			dx = dfiltx*(smoothroll.process(np.mean(motionVectors[:,0,0])*5/3.55 - droll)) #np.mean(motionVectors[:,0,0])*5/3.55 #m[0,2]
		except:
			dx = 0
		try:
			dpitch
			np.mean(motionVectors[:,0,1])
			dy = dfilty*(np.mean(motionVectors[:,0,1])*5/4.6 - dpitch)
		except:
			dy = 0
			
		totaldx = totaldx + dx
		totaldy = totaldy + dy


		smoothtotaldx = smoothtotaldx + smoothdx.process(dx)
		smoothtotaldy = smoothtotaldy + smoothdy.process(dy)

		# Extract rotation angle
		try:
			da = np.arctan2(m[1,0], m[0,0])
		except:
			da = 0
		totalda = totalda + da

		smoothda.process(da)
		smoothtotalda = smoothtotalda + smoothda.values[-1]
		#print(prev_pts)
		prev_gray = curr_gray
		
		
		#writeToBridge([totaldx,totaldy,smoothdx.values[-1]*dfiltx,smoothdy.values[-1]*dfilty])
		#poseWriteToBridge(cameraBridgeFile,totaldx,totaldy,smoothdx.values[-1]*dfiltx,smoothdy.values[-1]*dfilty)
		
		showCamera = True
		# #Show video and data 
		if showCamera:
			#cv2.putText(curr, f'x (smooth) = {smoothtotaldx*dfiltx:.2f}', (0,200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,0,0), 1)
			#cv2.putText(curr, f'y (smooth) = {smoothtotaldy*dfilty:.2f}', (0,250), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,0,0), 1)
			#cv2.putText(curr, f'a (smooth) = {smoothtotalda:.2f}', (0,300), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,0,0), 1)
			#cv2.putText(curr, f'smoothdx = {smoothdx.values[-1]*dfiltx:.2f}', (0,350), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (0,255,0), 1)
			#cv2.putText(curr, f'smoothdy = {smoothdy.values[-1]*dfilty:.2f}', (0,400), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (0,255,0), 1)
			#cv2.putText(curr, f'smoothda = {smoothda.values[-1]:.2f}', (0,450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (0,255,0), 1)
			
			cv2.putText(curr, f'z = {height:.3f}', (50,150), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (0,0,255), 1)
			#cv2.putText(curr, f'dz = {heightData[1]:.3f}', (50,200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (0,0,255), 1)
			cv2.putText(curr, f'x = {smoothtotaldx:.3f}', (400,200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,255,255), 5)
			cv2.putText(curr, f'y = {smoothtotaldy:.3f}', (400,250), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,255,255), 5)
			cv2.putText(curr, f'x = {smoothtotaldx:.3f}', (400,200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,0,255), 1)
			cv2.putText(curr, f'y = {smoothtotaldy:.3f}', (400,250), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,0,255), 1)
			cv2.putText(curr, f'a = {totalda:.3f}', (400,300), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,0,255), 1)
			# cv2.putText(curr, f'dx = {dx:.3f}', (400,350), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,255,0), 1)
			# cv2.putText(curr, f'dy = {dy:.3f}', (400,400), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,255,0), 1)
			# cv2.putText(curr, f'da = {da:.3f}', (400,450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,255,0), 1)
			cv2.putText(curr, str(pose), (200,350), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,255,255), 5)
			cv2.putText(curr, str(pose), (200,350), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,0,0), 1)
			
			cv2.putText(curr, f'{len(prev_pts):.2f} tracked point(s) found!', (0,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (0,0,255), 1)
			cv2.putText(curr, f'Dis. in [m]', (400,60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,255,255), 1)
			cv2.putText(curr, f'FPS = {fps:.2f}', (400,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,0,0), 1)
			cv2.imshow('Live Video', curr)
			
			#Exit the program and close the video:
			if cv2.waitKey(20) & 0xFF==ord('q'):
				break
		else:
			#Show only data
			print(f'FPS:  {fps}, ')
			print(f'z: {height}, ')
			#print(f'dz: {heightData[1]}, ')
			print(f'x: {totaldx*dfiltx}, ')
			print(f'y: {totaldy*dfilty}, ')
			print(f'dx: {dx*dfiltx}, ')
			print(f'dy: {dy*dfilty}, ')
	except:
		print("ERROR: Missing features")
		prev_gray = curr_gray
		pass


# Release video
cp.release()

# Close windows
cv2.destroyAllWindows()

serUSB.close()

# Close terminal
os.kill(os.getppid(),signal.SIGHUP)


