from visualize import *
import scipy.stats as sc

#Implement the RGA BS algorithm
#Initialise the constants

n = 0.015
mean = np.zeros((235,24,32,16))
sigma = 0.4
alpha = 0.01
M = 0
gmean = np.zeros((235,24,32,16))
gp = np.zeros((235,24,32,16))
event = np.zeros((235,24,32,16))

#For the frames, calculate the running average

fg = []
cnt = np.zeros((236,16))
bg = []
maxi = -1
for l in range(0,235):
    start = 0
    if l == 0:
        start = 1
    for k in range(start,16):
        for i in range(0,24):
            for j in range(0,32):
                if k==0:
                    mean[l,i,j,k] = alpha*data[l,i,j,k] + mean[l-1,i,j,15]*(1-alpha)    ## Mean if k==0 and l!=0
                else:
                    mean[l,i,j,k] = alpha*data[l,i,j,k] + mean[l,i,j,k-1]*(1-alpha)     ## Mean if k!=0 and l!=0

                gp[l,i,j,k] = gaussian_pdf(data[l,i,j,k] , sigma , mean[l,i,j,k])       ## Find the gaussian PDF 
                if gp[l,i,j,k]<n:                                                       ## Process is foreground
                    event[l,i,j,k] = 0
                    fg.append((data[l,i,j,k] , mean[l,i,j,k]))
                    cnt[l,k] = cnt[l,k] + 1
                    if k!=0:
                        mean[l,i,j,k] = mean[l,i,j,k-1]                                 ## Update the mean if the process is foreground
                    else:
                        mean[l,i,j,k] = mean[l-1,i,j,15]

                else:
                    event[l,i,j,k] = 1   
                    bg.append((data[l,i,j,k] , mean[l,i,j,k]))                          ## Process is Background
                if gp[l,i,j,k] > maxi:
                    maxi = gp[l,i,j,k]


        


        


