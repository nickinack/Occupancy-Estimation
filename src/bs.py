from visualize import *
import scipy.stats as sc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# Scipy's complexity is higher due to preprocessing
def gaussian_pdf(x , sigma , mu):
    pdf1 = (1/(sigma*np.sqrt(2*np.pi)))
    pdf2 = np.exp(-0.5*((x-mu)/sigma)**2)
    return pdf1*pdf2

#Implement the RGA BS algorithm
#Initialise the constants

print("Basic Background Subtraction \n")

n = 0.01
mean = np.zeros((seconds,24,32,16))
mean[0,:,:,0] = np.copy(data[0,:,:,0])
sigma = 0.4
alpha = 0.0001
M = 0
gmean = np.zeros((seconds,24,32,16))
gp = np.zeros((seconds,24,32,16))
event = np.zeros((seconds,24,32,16))
maxi = np.zeros((seconds,24,32,16))
mini = np.zeros((seconds,24,32,16))
mini[0,:,:,0] = data[0,:,:,0]
maxi[0,:,:,0] = data[0,:,:,0]

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

#For the frames, calculate the running gaussian average
#For each pixel, if the gaussian probability, gp < n , the pixel is foreground.
#If the pixel is foreground, we represent it as a white pixel in event graph
#We use the baseline algorithm in order to develop the MRF algorithm in order to remove outlier foregrounds.

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

#Testing
#fig, axs = plt.subplots(3, 3)
#axs[0,0].imshow(event[140,:,:,9] , cmap='Greys')
#axs[1,0].imshow(event[140,:,:,10] , cmap='Greys')
#axs[2,0].imshow(event[140,:,:,11] , cmap='Greys')
#axs[0,1].imshow(event[140,:,:,12] , cmap='Greys')
#axs[1,1].imshow(event[140,:,:,13] , cmap='Greys')
#axs[2,1].imshow(event[140,:,:,14] , cmap='Greys')
#axs[0,2].imshow(event[140,:,:,15] , cmap='Greys')
#axs[1,2].imshow(event[141,:,:,1] , cmap='Greys')
#axs[2,2].imshow(event[141,:,:,2] , cmap='Greys')
#End Testing

