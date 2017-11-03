#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 10:18:29 2017

@author: rohankamath
"""

import raytracer

rms = []
xaxis = []
for i in range(300):
    val = 101+ 0.01*i
    xaxis.append(val)
    op = OutputPlane(val)
    rsum = 0
    bundlepolar(0.0,0.1,3)
    for i in range(len(xcord)):
        rsq = xcord[i]**2 + ycord[i]**2
        rsum = rsum + rsq
    meansq = rsum/len(xcord)
    rms.append(np.sqrt(meansq))

    
        
plt.plot(xaxis,rms)
plt.show()