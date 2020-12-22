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
exit = 0
indices = []
for i in range(1 , np.shape(centroids)[0]):

    '''
    Check if the blob belongs to the same cluster a previous blob
    '''
    if np.shape(mapping_verbrose[i][2])[0] != 0:
        '''
        New blobs formed ; continue
        '''
        continue
    else:
        '''
        Analyse the mappings
        '''
        for j in range(1, centroids[i][2] + 1):

            cur = mapping_verbrose[i][1][j-1][0]
            prev = mapping_verbrose[i][1][j-1][1]

            if centroids[i][3][cur-1][2] > 16 and centroids[i-1][3][prev-1][2] < 16:
                entry = entry + 1
                indices.append(i)

            elif centroids[i][3][cur-1][2] < 16 and centroids[i-1][3][prev-1][2] > 16:
                exit = exit + 1
                indices.append(i)
print(entry , exit)
