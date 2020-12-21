from blobs import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import scipy.stats as sc

#In this section, we calculate the Centroids for each of the blobs we identified.
#We do so using the data (list: blobs) in the previous section

print("Calculating Centroids \n")

# Use the obtained information in order to calculate centroid
# For a given frame, in order to calculate the centroid, we get the information on how many blobs are present
# We store the centroid in a similar way we stored the blob indices

blob_frames = np.shape(blobs)[0]
centroids = []

for i in range(0,blob_frames):
    colors = blobs[i][2]
    j = 1
    frame_centroids = []
    while j <= colors:
        local_centroid_x = 0
        local_centroid_y = 0
        numb = 0
        for k in range(0,len(blobs[i][3])):
            if blobs[i][3][k][2] == j:
                local_centroid_x = local_centroid_x + blobs[i][3][k][0]
                local_centroid_y = local_centroid_y + blobs[i][3][k][1]
                numb = numb + 1
        local_centroid_x = local_centroid_x/numb
        local_centroid_y = local_centroid_y/numb
        frame_centroids.append((j , local_centroid_x , local_centroid_y))
        j = j+1
    centroids.append((blobs[i][0],blobs[i][1],blobs[i][2],frame_centroids))

# In the next section, we analyse the movements of these centroids (between two consecutive frames) and perform relative centroid indexing

entry = []
exits = []
count = 0
new_blob = 0
# Start the counting process
for i in range(1,len(centroids)):
    if np.abs(centroids[i][0]-centroids[i-1][0] >=1 ):
        if not (centroids[i][0] == 0 and centroids[i-1][0] + 1 and centroids[i][1] == 0 and centroids[i-1][1] == 15):
             '''
             New blob is born; track it
             '''
             pass
           
    if centroids[i-1][2] < centroids[i][2]:
        '''
        New blob is incoming while the existing blob is present / New blob disintegrated from the previous blobs; map accordingly
        '''
        pass

    if centroids[i-1][2] == centroids[i][2]:
        '''
        The number of blobs are the same, map accordingly
        '''
        pass

    if centroids[i-1][2] >= centroids[i-1][1]:
        '''
        Some of the blobs have passes , count their entry/exit ; map accordingly
        '''
        pass
        
        
