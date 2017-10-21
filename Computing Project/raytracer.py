# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 09:32:36 2017

@author: rkk216
"""
import numpy as np
class ray:
    rayList = []
    def __init__(self,startpoint,startdir):
        self.__startp = np.array(startpoint)
        self.__startdir = np.array(startdir)
        ray.rayList.append([self.__startp,self.__startdir])
    
    def startp(self):
        return self.__startp
    
    def startdir(self) :
        return self.__startdir
    
    def p(self):
        return ray.rayList[-1][0]
    
    def k(self):
        return ray.rayList[-1][1]
    
    def append(self,p,k):
        ray.rayList.append([np.array(p),np.array(k)])
        return
    
    def vertices(self):
        return ray.rayList

class OpticalElement:
  def propagate_ray(self, ray):
    "propagate a ray through the optical element"
    raise NotImplementedError()

class SphericalRefraction(OpticalElement):
    def __init__(self,z0,curv,n1,n2,aprad,centre):
        self.__z0 = z0
        self.__curv = curv
        self.__n1 = n1
        self.__n2 = n2
        self.__aprad = aprad
        self.__radius = 1/curv
        self.__centre = np.array(centre)
       
    def intercept(self,ray):
        #assume that the sphere is centered on the origin
        rdotk = np.dot(ray.k(),ray.p())
        magray = np.linalg.norm(ray.p())
        sqrt = rdotk**2 - (magray**2 - self.__radius**2)
        if sqrt < 0:
            raise Exception("No solution")
        else:
            sol1 = (-1*rdotk) - np.sqrt(sqrt)
            sol2 = (-1*rdotk) + np.sqrt(sqrt)
            absol1 = np.absolute(sol1)
            absol2 = np.absolute(sol2)
            if absol1 <absol2:
                return absol1
            else:
                return absol2
    
    def propagate_ray(self, ray):
        soln = self.intercept(ray)
        inci = soln*ray.k()
        incinorm = inci/np.linalg.norm(inci)
        normal = np.add(inci,np.subtract(ray.startp(),self.__centre))
        normalnorm = normal/np.linalg.norm(normal)
        vrefract = snell(self.__n1, self.__n2,incinorm,normalnorm)
        prefract = np.add(ray.startp(),inci)
        ray.rayList.append([prefract,vrefract])
        return [prefract,vrefract]

        
def snell(n1,n2,inci,normal): #inci and normal should be unit vectors
    relindex =n1/n2
    theta1 = np.arccos(np.dot(inci,normal))
    theta2 = relindex*np.sin(theta1)
    if np.sin(theta2) > (1/relindex):
        return None
    else:
        vrefract = (relindex*inci) + ((relindex*np.cos(theta1))-np.cos(theta2))*normal
    return vrefract


    
    
ray = ray([-2,0,0],[2,0.5,0])   
sp = SphericalRefraction(1,1,1,1.5,1,[0,0,0])
print(sp.intercept(ray))
print (sp.propagate_ray(ray))
    
    
    
    
    
    
    
        