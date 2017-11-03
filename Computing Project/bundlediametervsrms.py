
"""
Created on Fri Nov  3 10:20:35 2017

@author: rohankamath
"""

import raytracer

rms = []
xaxis = []
rsum = 0
for i in range(300):
    xaxis.append(0.001*i)
    bundlepolar(0.0,0.001*i,5)
    for i in range(len(xcord)):
        rsq = xcord[i]**2 + ycord[i]**2
        rsum = rsum + rsq
    meansq = rsum/len(xcord)
    rms.append(np.sqrt(meansq))
plt.plot(xaxis,rms)
plt.show()