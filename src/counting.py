from mapping import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import scipy.stats as sc
# In this section, we count the number of people using the mapping and centroid arrays obtained from the previously obtained centroid and mapping lists
# We also take care of the "lingering condition over here"

print("Counting the number of people \n")

# In order to count the number of people entering and exiting the room , we use the centroid.
# If the y-axes of the centroid (n-1) is at the top and moves to the bottom in the next frame, then the person is moving into the room (entering)
# Else, if it is the latter case, the person is exitting the room

entry = 0
entry_index = []
exit_index = []
exit = 0
indices = []
prev_unmapped_index = 0
cur_unmapped_index = 0
for i in range(1 , np.shape(centroids)[0]):

    '''
    Check if the blob belongs to the same cluster a previous blob
    '''
    if np.shape(mapping_verbrose[i][2])[0] != 0:
        '''
        New blobs formed ; continue
        '''
        prev_unmapped_index = cur_unmapped_index
        cur_unmapped_index = i

        first_event = centroids[prev_unmapped_index + 1][3][0][1] - centroids[prev_unmapped_index + 2][3][0][1]
        last_event = centroids[cur_unmapped_index - 2][3][0][1] - centroids[cur_unmapped_index - 1][3][0][1]

        if (first_event < 0 and last_event > 0) or (first_event > 0 and last_event < 0) and np.abs(first_event) > 10 and np.abs(last_event) > 10:
            '''
            Lingering
            '''
            to_remove = []
            for i in range(0,len(indices)):
                if indices[i] >= prev_unmapped_index and indices[i] <= cur_unmapped_index:
                    to_remove.append(i)
            
            for index in sorted(to_remove, reverse=True):
                indices.remove(indices[index])

    else:
        '''
        Analyse the mappings
        '''
        for j in range(1, centroids[i][2] + 1):

            cur = mapping_verbrose[i][1][j-1][0]
            prev = mapping_verbrose[i][1][j-1][1]

            if centroids[i][3][cur-1][1] > 16 and centroids[i-1][3][prev-1][1] < 16:
                entry_index.append(i)
                indices.append(i)

            elif centroids[i][3][cur-1][1] < 16 and centroids[i-1][3][prev-1][1] > 16:
                exit_index.append(i)
                indices.append(i)

for i in indices:
    if i in entry_index:
        entry = entry+1
    if i in exit_index:
        exit = exit + 1
print("Number of entries and exits: " , len(indices))
print(entry,exit)

