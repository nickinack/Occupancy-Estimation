from centroid import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import scipy.stats as sc

# In this section of code, we count the number of people entering and exitting in the room
# We use the centroids calculated in the previous section in order to count the number of people

print("Counting the number of people \n")

# Before we count the number of people, we remove centroids which are likely due to incorrect readings by the sensor
# We do so by checking the consecutiveness of the frames in the centroid list we obtained

before_outlier = np.shape(centroids)

for i in range(1,len(centroids)-1):
    second = centroids[i][0]
    frame = centroids[i][1]
    if second != centroids[i-1][0] or second != centroids[i+1][0]:
        if (centroids[i-1][1] == 15 and frame == 0) or (centroids[i+1][1] == 0 and frame == 15):
            continue
        elif np.abs(centroids[i-1][0] - second) > 1 and np.abs(centroids[i+1][0] - second) > 1:
            centroids.remove(centroids[i])
            continue
    elif frame != centroids[i-1][1] + 1 or frame != centroids[i+1][1] - 1:
        if (np.abs(centroids[i-1][1] - frame) > 10 and np.abs(cnt[centroids[i-1][0] , centroids[i-1][1]] - cnt[second , frame]) > 100) or (np.abs(centroids[i+1][1] - frame) > 10 and np.abs(cnt[centroids[i+1][0] , centroids[i+1][1]] - cnt[second , frame]) > 100):
            centroids.remove(centroids[i])

after_outlier = np.shape(centroids)

if before_outlier == after_outlier:
    print("No outliers \n")

else:
    print("Outliers removed \n")

# Once the outliers are removed, we start the process of counting.
# For counting, we majorly use the 'y' axes of the centroid. If we notice the y axes moving , we count an entry/exit
# Initialize the parameters
entry = []
exits = []
count = 0

# Start the counting process
for i in range(0,len(centroids)):

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
        