import fcntl


def poseReadFromBridge(f):
    # Acquire a file lock
    fcntl.flock(f, fcntl.LOCK_SH)
        
    # Read some data from the file
    f.seek(0)
    data = f.read()
    dataSplit=data.split()
    dataFloat=[float(dataSplit[0]),float(dataSplit[1]),float(dataSplit[2]),float(dataSplit[3])]
    # Process the data
    #print(str(dataFloat))
    # Release the file lock
    fcntl.flock(f, fcntl.LOCK_UN)
    return dataFloat
    

def poseWriteToBridge(f,roll, pitch, yaw, height):
    # Acquire a file lock
    fcntl.flock(f, fcntl.LOCK_EX)
        
    # Write some data to the file
    f.seek(0)
    f.write(str(roll)+" "+str(pitch)+" "+str(yaw)+" "+str(height)+"\n")
    # Flush the buffer to ensure the data is written to disk
    f.flush()
        
    # Release the file lock
    fcntl.flock(f, fcntl.LOCK_UN)

#USE:
# from poseBridge import poseWriteToBridge
# from poseBridge import poseReadFromBridge

# f = open("shared_file.txt", "w")
# poseWriteToBridge(f,1)
# f = open("shared_file.txt", "r")
# poseReadFromBridge(f)

#EXIT:
#f.close()
