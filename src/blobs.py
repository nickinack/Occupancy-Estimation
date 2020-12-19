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

visited = np.zeros((24,32))
blobs = []
record = []
color = 1
for i in range(0,24):
    for j in range(0,32):
        size = blob_detector(i,j,visited,color,210,15)
        if size>100:
            blobs.append((i,j,size))
            color = color+1
        

print("Blobs" , blobs)
print("Record Shape" , np.shape(record))