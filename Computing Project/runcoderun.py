#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 11:09:36 2017

@author: rohankamath
"""
import raytracer

bundleparallel(-11,11,10);
bundlepolar(0.0,0.01,5)
plt.plot(x,y,'ro')
plt.show()
plt.plot(xcord,ycord,'ro')
plt.show()



rms = []
outputplaneaxis = []

for i in range(300):
    val = 101+ 0.01*i
    outputplaneaxis.append(val)
    op = OutputPlane(val)
    rsum = 0
    bundlepolar(0.0,0.1,3)
    for i in range(len(xcord)):
        rsq = xcord[i]**2 + ycord[i]**2
        rsum = rsum + rsq
    meansq = rsum/len(xcord)
    rms.append(np.sqrt(meansq))
    
    
for i in range(len(rms)):
    if rms[i] == min(rms):
        minval = outputplaneaxis[i]
plt.plot(outputplaneaxis,rms)
plt.show()

rsum = 0
rms = []
bundlediameter = []
op = OutputPlane(minval)
for i in range(300):
    bundlediameter.append(0.001*i)
    bundlepolar(0.0,0.001*i,5)
    for i in range(len(xcord)):
        rsq = xcord[i]**2 + ycord[i]**2
        rsum = rsum + rsq
    meansq = rsum/len(xcord)
    rms.append(np.sqrt(meansq))
plt.plot(bundlediameter,rms)
plt.show()


    