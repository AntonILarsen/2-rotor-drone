
def writeToBridge(camera):
    file1 = open("cameraBridge.txt","w")
    L = ["","","",""]
    for i in range(4): #fills up L with camera values, one at each line
        buf = "%f \n" % (camera[i])
        L[i]=buf
    
    #writes to the bridge file:
    file1.write("camera(x_y_dx_dy)=  \n")
    file1.writelines(L)
    file1.close()
  

def readFromBridge():
    file1 = open("cameraBridge.txt","r+") 
    file1.seek(0) #set cursor at the beggining of txt file
    readFromFile=file1.readlines()
    camera = [0,0,0,0] #x,y,dx,dy

    for i in range(4):
        splitted=(readFromFile[i+1].split())
        camera[i]=float(splitted[0])

    file1.close
    return camera


#How to use
#camera = [11,25,0.2,0.1]
#writeToBridge(camera)

#print("Values from readFromBridge(): ")
#print(readFromBridge())
