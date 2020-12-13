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

for l in range(0,235):
    start = 0
    if l == 0:
        start = 1
    for k in range(start,16):
        for i in range(0,24):
            for j in range(0,32):
                mean[l,i,j,k] = alpha*data[l,i,j,k]
                if k==0:
                    mean[l,i,j,k] = mean[l,i,j,k] + mean[l-1,i,j,15]*(1-alpha)
                else:
                    mean[l,i,j,k] = mean[l,i,j,k] + mean[l,i,j,k-1]*(1-alpha)
                gmean[l,i,j,k] = data[l,i,j,k] - mean[l,i,j,k]
                gp[l,i,j,k] = sc.norm(gmean[l,i,j,k] , sigma).pdf(data[l,i,j,k])
                if gp[l,i,j,k]<n:
                    event[l,i,j,k] = 0
                else:
                    event[l,i,j,k] = 1
                print(l,k,i,j)

plt.imshow(event[4,:,:,10], cmap='Greys',  interpolation='nearest')
        


        


