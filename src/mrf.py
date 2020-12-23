from visualize import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import scipy.stats as sc

#Implement the MRF algorithm
#Initialise the constants

print("Markov Random Field \n")

def gaussian_pdf(x , sigma , mu):
    pdf1 = (1/(sigma*np.sqrt(2*np.pi)))
    pdf2 = np.exp(-0.5*((x-mu)/sigma)**2)
    return pdf1*pdf2

n = 0.01
mean = np.zeros((seconds,24,32,16))
mean[0,:,:,0] = np.copy(data[0,:,:,0])
sigma = 0.4
alpha = 0.0001
M = 0
gmean = np.zeros((seconds,24,32,16))
gp = np.zeros((seconds,24,32,16))
event = np.zeros((seconds,24,32,16))

for i in range(0,1):
    for j in range(0,1):
        for k in range(0,24):
            for l in range(0,32):
                event[i,k,l,j] = 1

for j in range(0,16):
    mean[0,:,:,0] = mean[0,:,:,0] + data[0,:,:,j]
for j in range(0,9):
    mean[0,:,:,0] = mean[0,:,:,0] + data[1,:,:,j]

mean[0,:,:,0] = mean[0,:,:,0]/25

fg = []
cnt = np.zeros((236,16))
bg = []
maxi = np.zeros((seconds,24,32,16))
mini = np.zeros((seconds,24,32,16))
mini[0,:,:,0] = data[0,:,:,0]
maxi[0,:,:,0] = data[0,:,:,0]
theta = 0.015
gamma = 0.2

#For the frames, calculate the running gaussian average as we did in the baseline algorithm
#For each pixel, if the gaussian probability, gp < n , the pixel is foreground.
#If the pixel is foreground, we represent it as a white pixel in event graph

for l in range(0,seconds):
    start = 0
    if l == 0:
        start = 1
    for k in range(start,16):
        for i in range(0,24):
            for j in range(0,32):
                if k==0:
                    mean[l,i,j,k] = alpha*data[l,i,j,k] + mean[l-1,i,j,15]*(1-alpha)        ## Mean if k==0 and l!=0
                    maxi[l,i,j,k] = max(maxi[l-1,i,j,15] , data[l,i,j,k])
                    mini[l,i,j,k] = min(mini[l-1,i,j,15] , data[l,i,j,k])
                else:
                    mean[l,i,j,k] = alpha*data[l,i,j,k] + mean[l,i,j,k-1]*(1-alpha)                  ## Mean if k!=0 and l!=0
                    maxi[l,i,j,k] = max(maxi[l,i,j,k-1] , data[l,i,j,k])
                    mini[l,i,j,k] = min(mini[l,i,j,k-1] , data[l,i,j,k])

                gp[l,i,j,k] = gaussian_pdf(data[l,i,j,k] , sigma , mean[l,i,j,k])                    ## Find the gaussian PDF 
                if gp[l,i,j,k]<n and data[l,i,j,k]>mean[0,i,j,0]:                                   ## Process is foreground
                    event[l,i,j,k] = 0
                    fg.append((data[l,i,j,k] , mean[l,i,j,k]))
                    if k!=0:
                        mean[l,i,j,k] = mean[l,i,j,k-1]                                       ## Update the mean if the process is foreground
                    else:
                        mean[l,i,j,k] = mean[l-1,i,j,15]

                else:
                    event[l,i,j,k] = 1   
                    bg.append((data[l,i,j,k] , mean[l,i,j,k]))                              ## Process is Background

#Initialise MRF lists

diff = np.zeros((seconds,24,32,16))
mrf_event = np.zeros((seconds,24,32,16))
mrf_event[0,:,:,0] = 1

# Use the markov random field in order to remove outlier points
# Use the BS algorithm and check the neighbouring events
# Depending on the neighbours, weigh the MRF accordingly

for l in range(0,seconds):
    for k in range(0,16):
        for i in range(0,24):
            for j in range(0,32):
                qf = 0
                qb = 0
                ratio = gp[l,i,j,k]*25
                if i>0 and j>0:
                    if event[l,i-1,j-1,k] == 0:
                        qf = qf + 1
                    else:
                        qb = qb + 1
                if i>0:
                    if event[l,i-1,j,k] == 0:
                        qf = qf+1
                    else:
                        qb = qb+1
                if j<31 and i>0:
                    if event[l,i-1,j+1,k] == 0:
                        qf = qf + 1
                    else:
                        qb = qb + 1
                if j>0:
                    if event[l,i,j-1,k] == 0:
                        qf = qf + 1
                    else:
                        qb = qb + 1
                if j<31:
                    if event[l,i,j+1,k] == 0:
                        qf = qf + 1
                    else:
                        qb = qb + 1
                if i<23 and j>0:
                    if event[l,i+1,j-1,k] == 0:
                        qf = qf + 1
                    else:
                        qb = qb + 1
                if i<23:
                    if event[l,i+1,j,k] == 0:
                        qf = qf + 1
                    else:
                        qb = qb + 1
                if i<23 and j<31:
                    if event[l,i+1,j+1,k] == 0:
                        qf = qf + 1
                    else:
                        qb = qb + 1

                mrf = theta * np.exp((qf-qb)/gamma)
                if ratio < mrf and data[l,i,j,k] > mean[l,i,j,k] and data[l,i,j,k] > mean[0,i,j,0]:
                    mrf_event[l,i,j,k] = 0
                    cnt[l,k] = cnt[l,k] + 1
                else:
                    mrf_event[l,i,j,k] = 1
                diff[l,i,j,k] = ratio-mrf

# for l in range(0,seconds):
#    for k in range(0,16):
#        if cnt[l,k] > 500:
#            print(l,k)

#Testing
#def visualize(second):
#    fig, axs = plt.subplots(4, 4)
#    frame = 0
#    axs[0,0].imshow(mrf_event[second,:,:,frame] , cmap='Greys')
#    axs[1,0].imshow(mrf_event[second,:,:,frame+1] , cmap='Greys')
#    axs[2,0].imshow(mrf_event[second,:,:,frame+2] , cmap='Greys')
#    axs[3,0].imshow(mrf_event[second,:,:,frame+3] , cmap='Greys')
#    axs[0,1].imshow(mrf_event[second,:,:,frame+4] , cmap='Greys')
#    axs[1,1].imshow(mrf_event[second,:,:,frame+5] , cmap='Greys')
#    axs[2,1].imshow(mrf_event[second,:,:,frame+6] , cmap='Greys')
#    axs[3,1].imshow(mrf_event[second,:,:,frame+7] , cmap='Greys')
#    axs[0,2].imshow(mrf_event[second,:,:,frame+8] , cmap='Greys')
#    axs[1,2].imshow(mrf_event[second,:,:,frame+9] , cmap='Greys')
#    axs[2,2].imshow(mrf_event[second,:,:,frame+10] , cmap='Greys')
#   axs[3,2].imshow(mrf_event[second,:,:,frame+11] , cmap='Greys')
#    axs[0,3].imshow(mrf_event[second,:,:,frame+12] , cmap='Greys')
#    axs[1,3].imshow(mrf_event[second,:,:,frame+13] , cmap='Greys')
#    axs[2,3].imshow(mrf_event[second,:,:,frame+14] , cmap='Greys')
#    axs[3,3].imshow(mrf_event[second,:,:,frame+15] , cmap='Greys')
#End Testing


        


