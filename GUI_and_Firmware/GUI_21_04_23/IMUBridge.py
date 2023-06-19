
def writeToIMUBridge(camera):
    file1 = open("IMUBridge.txt","w")
    L = ["","","","","",""]
    for i in range(3): #fills up L with camera values, one at each line
        buf = "%f \n" % (camera[i])
        L[i]=buf
    
    writeToIMUBridge.sum[0]+=camera[0]
    writeToIMUBridge.sum[1]+=camera[1]
    writeToIMUBridge.sum[2]+=camera[2]
    
    for i in range(3): #fills up L with camera values, one at each line
        buf = "%f \n" % (writeToIMUBridge.sum[i])
        L[i+3]=buf
        
    #writes to the bridge file:
    file1.write("camera(x_y_dx_dy)=  \n")
    file1.writelines(L)
    file1.close()
writeToIMUBridge.sum=[0,0,0]
  

def readFromIMUBridge():
    file1 = open("IMUBridge.txt","r+") 
    file1.seek(0) #set cursor at the beggining of txt file
    readFromFile=file1.readlines()
    imu = [0,0,0,0,0,0] #x,y,dx,dy
    try:
        for i in range(6):
            splitted=(readFromFile[i+1].split())
            imu[i]=float(splitted[0])
    except:

        return readFromIMUBridge.prevVal
    file1.close
    readFromIMUBridge.prevVal=imu
    return imu
readFromIMUBridge.prevVal=[0,0,0,0,0,0]

#How to use
#camera = [11,25,0.2,0.1]
#writeToBridge(camera)

#print("Values from readFromBridge(): ")
#print(readFromBridge())
