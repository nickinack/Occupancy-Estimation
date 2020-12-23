import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import scipy.stats as sc
from mrf import *

# Blob detection
# Use Recursive Blob Detection method (Similar to DBSCAN)

print("Blob Calculation \n")

# Radius and Minimum foreground count
K = 100
L = 100

# Returns unexplored blobs in a frame
# If the blob size > 100, we give the blob a color and index each of the positions of the blob
# The record is then stored in a list for further use

def blob_detector(i, j, visited, color, second, frame):
    '''
    Given a frame after BS, detects "blobs"
    '''
    
    blob_size = 1
    if visited[i,j] != 0 or mrf_event[second,i,j,frame] == 1:
        return 0
    
    record.append((i,j,color))
    visited[i,j] = color
    connected = 0
    if i>0 and j>0 and mrf_event[second,i-1,j-1,frame] == 0 and visited[i-1,j-1] == 0:
        blob_size = blob_size + blob_detector(i-1,j-1,visited,color,second,frame)
        connected = connected + 1
        
    if i>0 and mrf_event[second,i-1,j,frame] == 0 and visited[i-1,j] == 0:
        blob_size  = blob_size + blob_detector(i-1,j,visited,color,second,frame)
        connected = connected + 1
       
    if j<31 and i>0 and mrf_event[second,i-1,j+1,frame] == 0 and visited[i-1,j+1] == 0:
        blob_size  = blob_size + blob_detector(i-1,j+1,visited,color,second,frame)
        connected = connected + 1
       
    if j>0 and mrf_event[second,i,j-1,frame] == 0 and visited[i,j-1] == 0:
        blob_size  = blob_size + blob_detector(i,j-1,visited,color,second,frame)
        connected = connected + 1
       
    if j<31 and mrf_event[second,i,j+1,frame] == 0 and visited[i,j+1] == 0:
        blob_size  = blob_size + blob_detector(i,j+1,visited,color,second,frame)
        connected = connected + 1
        
    if i<23 and j>0 and mrf_event[second,i+1,j-1,frame] == 0 and visited[i+1,j-1] == 0:
        blob_size  = blob_size + blob_detector(i+1,j-1,visited,color,second,frame)
        connected = connected + 1
       
    if i<23 and mrf_event[second,i+1,j,frame] == 0 and visited[i+1,j] == 0:
        blob_size  = blob_size + blob_detector(i+1,j,visited,color,second,frame)
        connected = connected + 1
       
    if i<23 and j<31 and mrf_event[second,i+1,j+1,frame] == 0 and visited[i+1,j+1] == 0:
        blob_size  = blob_size + blob_detector(i+1,j+1,visited,color,second,frame)
        connected = connected + 1
  
    return blob_size

#For the given dataset, calculate the blob information and store them

blobs = []
for l in range(0,seconds):
    for k in range(0,16):
        if cnt[l,k] < K:
            continue
        record = []
        color = 1
        visited = np.zeros((24,32))
        for i in range(0,24):
            for j in range(0,32):
                size = blob_detector(i,j,visited,color,l,k)
                if size>=L:
                    color = color + 1
        blobs.append((l,k,color-1,record))
        

input1 = int(input("Enter second: "))
input2 = int(input("Enter frame: "))

print("----------------------------------------------")
print("-------------Blob information-----------------")
print("Second: " , input1)
print("Frame: ", input2)
flag = -1
for i in range(len(blobs)):
    if blobs[i][0] == input1-1 and blobs[i][1] == input2-1:
        flag = i

if flag == -1:
    print("No blobs in the requested frame!")
else:
    print("Number of Blobs: " , blobs[flag][2])
    print("Blob indices along with their color: " , blobs[flag][3])
print("----------------------------------------------")