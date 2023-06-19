# pip install opencv-python==3.4.18.65

import numpy as np
import cv2
import time
from cameraBridge import writeToBridge
import os 		#for closing terminal
import signal 	#for closing terminal

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
smoothdx = StreamingMovingAverage(30) #FPS = ca.30, choose movingaverage order after this
smoothdy = StreamingMovingAverage(30)
smoothda = StreamingMovingAverage(30)
smoothtotaldx = 0
smoothtotaldy = 0
smoothtotalda = 0


prev_pts = []

# Read height from file
file1 = open("heightDataBridge.txt","r+") 
file1.seek(0) #set cursor at the beggining of txt file
readFromFile=file1.readlines()
try: #heightData = [z, dz]
	heightData = prevHeightData
except:
	heightData = [0,0]
try: 
	for i in range(2):
		splitted=(readFromFile[i+1].split())
		if(float(splitted[0])!=0):
			heightData[i]=float(splitted[0])
except:
	pass
try:
	if(abs(prevHeightData[0]-heightData[0])>1):
		heightData[0]=prevHeightData[0]
except:
	pass


isTrue, curr = cp.read()

curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)
prev_gray = curr_gray

prev_frame_time = 0
new_frame_time = 0

now=0
while True:
	isTrue, curr = cp.read()
	if not isTrue:
		break
	
	curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)
	try:
		#new (https://www.geeksforgeeks.org/feature-detection-and-matching-with-opencv-python/):
		#orb = cv2.ORB_create(nfeatures=80, scaleFactor=1.5, nlevels=6, edgeThreshold=20) #Can be adjusted
		#kp = orb.detect(prev_gray, None)
		#prev_pts = cv2.KeyPoint_convert(kp)
		#old (slower):
		prev_pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=40, qualityLevel=0.01, minDistance=30, blockSize=3) #maxCorners=40, qualityLevel=0.01, minDistance=30, blockSize=3
		
		
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

		idx = np.where(status==1)[0]
		prev_pts = prev_pts[idx]
		curr_pts = curr_pts[idx]
		assert prev_pts.shape == curr_pts.shape 
		
		
		

		# Read height from file
		file1 = open("heightDataBridge.txt","r+") 
		file1.seek(0) #set cursor at the beggining of txt file
		readFromFile=file1.readlines()
		try: #heightData = [z, dz]
			heightData = prevHeightData
		except:
			heightData = [0,0]
		try: 
			for i in range(2):
				splitted=(readFromFile[i+1].split())
				if(float(splitted[0])!=0):
					heightData[i]=float(splitted[0])
		except:
			pass
		try:
			if(abs(prevHeightData[0]-heightData[0])>1):
				heightData[0]=prevHeightData[0]
		except:
			pass
		
		file1.close
		
		#print(heightData)
	
		try:
			prev_pts_3d = []
			for p in range(len(prev_pts)):
				prev_pts_3d.append([[prev_pts[p][0][0], prev_pts[p][0][1], prevHeightData[0]]])
			prev_pts_3d = np.float32(prev_pts_3d)
			
			curr_pts_3d = []
			for c in range(len(curr_pts)):
				curr_pts_3d.append([[curr_pts[c][0][0], curr_pts[c][0][1], heightData[0]]])
			curr_pts_3d = np.float32(curr_pts_3d)
			
		except:
			print("passing??")
			pass
		prevHeightData = heightData
		
		# fullAffine= FAlse will set the degree of freedom to only 5 i.e translation, rotation and scaling
		# try fullAffine = True
		
		#print(len(prev_pts_3d))
		#print(xyz)
		
		print(curr_pts_3d[0][0])
		print(prev_pts_3d[0][0])
		
		ret, M, mask = cv2.estimateAffine3D(prev_pts_3d, curr_pts_3d,confidence = .9999999)
		
		# now = now +1
		# if now > 10:
			# retval, Rt, inliers = cv2.estimateAffine3D(prev_pts_3d, curr_pts_3d)
			# print(Rt)
		
		m = cv2.estimateRigidTransform(prev_pts, curr_pts, fullAffine=True)  # fullAffine=False
		
		#print(H)
		
		
		#H = cv2.estimateAffine3D(prev_pts,curr_pts)
		
		#m = np.matmul(H*[[m[0,2],m[1,2],1]])
		
		#print("m: ")
		#print(m)
		#print("mhomo: ")
		#print(mhomo)
		
		try:
			dx = M[0,3] #m[0,2]
		except:
			dx = 0
		try:
			dy = M[1,3]
		except:
			dy = 0
			
		totaldx = totaldx + dx
		totaldy = totaldy + dy

		smoothdx.process(dx)
		smoothdy.process(dy)
		smoothtotaldx = smoothtotaldx + smoothdx.values[-1]
		smoothtotaldy = smoothtotaldy + smoothdy.values[-1]

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
		




		#FPS calculation:
		new_frame_time = time.time()
		fps = 1/(new_frame_time-prev_frame_time)
		prev_frame_time = new_frame_time



		
		
		#Calibrating drift from height data
		height = heightData[0] #in meters
		offset_to_camera = 0.19 #in meters
		FOVx = 1.085594795 #in radians
		FOVy = 0.8517206750 #in radians
		resx = 640
		resy = 480
		dfiltx = (2*np.tan(FOVx/2)*(height+offset_to_camera))/resx
		dfilty = (2*np.tan(FOVx/2)*(height+offset_to_camera))/resy
		
		
		writeToBridge([totaldx*dfiltx,totaldy*dfilty,smoothdx.values[-1]*dfiltx,smoothdy.values[-1]*dfilty])
		
		
		showCamera = False
		# #Show video and data 
		if showCamera:
			#cv2.putText(curr, f'x (smooth) = {smoothtotaldx*dfiltx:.2f}', (0,200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,0,0), 1)
			#cv2.putText(curr, f'y (smooth) = {smoothtotaldy*dfilty:.2f}', (0,250), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,0,0), 1)
			#cv2.putText(curr, f'a (smooth) = {smoothtotalda:.2f}', (0,300), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,0,0), 1)
			#cv2.putText(curr, f'smoothdx = {smoothdx.values[-1]*dfiltx:.2f}', (0,350), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (0,255,0), 1)
			#cv2.putText(curr, f'smoothdy = {smoothdy.values[-1]*dfilty:.2f}', (0,400), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (0,255,0), 1)
			#cv2.putText(curr, f'smoothda = {smoothda.values[-1]:.2f}', (0,450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (0,255,0), 1)
			
			cv2.putText(curr, f'z = {height:.3f}', (50,150), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (0,0,255), 1)
			cv2.putText(curr, f'dz = {heightData[1]:.3f}', (50,200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (0,0,255), 1)
			cv2.putText(curr, f'x = {totaldx*dfiltx:.3f}', (400,200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,255,255), 5)
			cv2.putText(curr, f'y = {totaldy*dfilty:.3f}', (400,250), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,255,255), 5)
			cv2.putText(curr, f'x = {totaldx*dfiltx:.3f}', (400,200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,0,255), 1)
			cv2.putText(curr, f'y = {totaldy*dfilty:.3f}', (400,250), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,0,255), 1)
			cv2.putText(curr, f'a = {totalda:.3f}', (400,300), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,0,255), 1)
			cv2.putText(curr, f'dx = {dx*dfiltx:.3f}', (400,350), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,255,0), 1)
			cv2.putText(curr, f'dy = {dy*dfilty:.3f}', (400,400), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,255,0), 1)
			cv2.putText(curr, f'da = {da:.3f}', (400,450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, (255,255,0), 1)
			
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
			print(f'dz: {heightData[1]}, ')
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


# Close terminal
os.kill(os.getppid(),signal.SIGHUP)


