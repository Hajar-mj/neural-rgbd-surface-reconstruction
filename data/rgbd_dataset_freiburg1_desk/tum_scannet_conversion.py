import numpy as np
import os 

def get_rotation(quat):
    w = quat[3]
    x = quat[0]
    y = quat[1]
    z = quat[2]
    Rq = np.array([[1-2*(y*y)-2*(z*z), 2*x*y-2*w*z, 2*x*z+2*w*y],[2*x*y+2*w*z, 1-2*(x*x)-2*(z*z), 2*y*z-2*w*x],[2*x*z-2*w*y, 2*y*z+2*w*x, 1-2*(x*x)-2*(y*y)]])
    return Rq

input_filename = "poses.txt"
output_filename = "neural_pose.txt"

tum = np.loadtxt(input_filename)
tum_len = len(tum)
LA = np.zeros((4,4))
for i in range(tum_len):
    tc = tum[i]
    timestamp = tc[0]
    position = tc[1:4]
    position = np.array([[1,0,0, -position[0]],[0,1,0,-position[1]],[0,0,1,-position[2]],[0,0,0,1]])
    quaternion = tc[4:]
    rotation = get_rotation(quaternion)
    #print(rotation.shape)
    rotation = np.concatenate((rotation,[[0],[0],[0]]),axis=1)
    #print(rotation.shape)
    rotation = np.concatenate((rotation,[[0,0,0,1]]),axis=0)
    #print(rotation.shape)
    if(i==0):
        LA = position * rotation
    else:
        LA = np.concatenate((LA, position * rotation), axis=0)
    if(LA.any()>1):
        print('WARNING')

np.savetxt(output_filename,LA,fmt='%.6f')
   



