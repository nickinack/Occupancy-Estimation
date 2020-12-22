from centroid import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import scipy.stats as sc

def blob_size(input1 , input2):
    '''
    Given a frame and a second, returns the foreground pixels which are part of a blob
    '''
    flag = -1
    for i in range(len(blobs)):
        if blobs[i][0] == input1 and blobs[i][1] == input2:
            flag = i
    return np.shape(blobs[flag][3])[0]

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
for i in range(1,len(centroids)):
    unmapped = []
    mapped = []
    condition = -1
    if (not (centroids[i][0] == centroids[i-1][0] + 1 and centroids[i][1] == 0 and centroids[i-1][1] == 15)) and np.abs(centroids[i][0] - centroids[i-1][0]) >= 1:
        '''
        New blob(s) is/are born; track it
        '''
        for j in range(1 , centroids[i][2] + 1):
            condition = 0
            unmapped.append(j)                          # We are assuming we will be mapping every unmapped centroid in its next frame.
           
    elif centroids[i-1][2] < centroids[i][2]:

        '''
        New blob is incoming while the existing blob is present / New blob disintegrated from the previous blobs; map accordingly or the centroids merged
        '''
        if centroids[i-1][2] == 1 and centroids[i][2] > 1:
            '''
            Blobs may have disintegrated
            '''
            condition = 1
            mapped, unmapped = mapping(centroids[i] , centroids[i-1] , 1)
        else:
            mapped , unmapped = mapping(centroids[i] , centroids[i-1] , 2)
        
    elif centroids[i-1][2] == centroids[i][2]:
        '''
        The number of blobs are the same, map accordingly
        '''
        condition = 3
        mapped,unmapped = mapping(centroids[i] , centroids[i-1] , 3)


    elif centroids[i-1][2] > centroids[i][2]:
        '''
        Some of the blobs may have passed , count their entry/exit ; map accordingly
        '''
        if centroids[i][2] == 1 and centroids[i-1][2] > 1:
            condition = 4
            mapped,unmapped = mapping(centroids[i] , centroids[i-1] , 4)

        else:
            condition = 5
            mapped,unmapped = mapping(centroids[i] , centroids[i-1] , 5)
     
    

def mapping(centroid1 , centroid2 , condition):
    '''
    Given the conditions, map the centroid
    '''

    map = []
    unmapped = []
    if condition == 1:
        '''
        Blobs may have disintegrated
        '''
        if np.abs(blob_size(centroid1[0] , centroid1[1]) - blob_size(centroid2[0] , centroid2[1])) <= 50:
            '''
            Blobs have merged
            '''
            for j in range(1,centroid1[2] + 1):
                map.append((j , 1))
        else:
            condition = 2

    if condition == 2:
        '''
        New blob born when blobs are present
        '''
        visited = np.zeros(centroid2[2])
        for i in range(1,centroid1[2] + 1):
            mini = 1e9+7
            map_cur = i
            map_prev = -1
            for j in range(1,centroid2[2]+1):
                if visited[j-1] == 0:
                    dist = (centroid1[3][i-1][0]-centroid2[3][j-1][0])**2 + (centroid1[3][i-1][1]-centroid2[3][j-1][1])**2
                    if mini>dist:
                        mini = dist
                        map_prev = j
            visited[map_prev-1] = 1
            map.append((map_cur , map_prev))

        for i in range(1,centroid1[2] + 1):
            found = -1
            for j in map:
                if i == j[0]:
                    found = 1
            if found == -1:
                unmapped.append(i)

    if condition == 3:
        '''
        The number of blobs are the same
        '''
        visited = np.zeros(centroid2[2])
        for i in range(1,centroid1[2] + 1):
            mini = 1e9+7
            map_cur = i
            map_prev = -1
            for j in range(1,centroid2[2]+1):
                if visited[j-1] == 0:
                    dist = (centroid1[3][i-1][0]-centroid2[3][j-1][0])**2 + (centroid1[3][i-1][1]-centroid2[3][j-1][1])**2
                    if mini>dist:
                        mini = dist
                        map_prev = j
            visited[map_prev-1] = 1
            map.append((map_cur , map_prev))
    
    if condition == 4:
        '''
        Some of the blobs have passed; tricky edge case. We need to comapre the size of the blobs. 
        '''

        if np.abs(blob_size(centroid1[0] , centroid1[1]) - blob_size(centroid2[0] , centroid2[1])) <= 50:
            '''
            Blobs have merged
            '''

            for j in range(1,centroid2[2]+1):
                map.append((1 , j))
        
        else:
            '''
            Revert to condition 5
            '''
            condition = 5

    if condition == 5:
        '''
        Blobs are dissapearing; we now find which blob diappeared 
        '''
        visited = np.zeros(centroid2[2])
        for i in range(1,centroid1[2] + 1):
            mini = 1e9+7
            map_cur = i
            map_prev = -1
            for j in range(1,centroid2[2]+1):
                if visited[j-1] == 0:
                    dist = (centroid1[3][i-1][0]-centroid2[3][j-1][0])**2 + (centroid1[3][i-1][1]-centroid2[3][j-1][1])**2
                    if mini>dist:
                        mini = dist
                        map_prev = j
            visited[map_prev-1] = 1
            map.append((map_cur , map_prev))

        for i in range(1,centroid2[2] + 1):
            found = -1
            for j in map:
                if i == j[1]:
                    found = 1
            if found == -1:
                unmapped.append(i)  

    return (map , unmapped)
    