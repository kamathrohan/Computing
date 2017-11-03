#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 11:00:33 2017

@author: rohankamath
"""

import raytracer 
class OpticalElement():
    def propagate_ray(self, ray):
        "propagate a ray through the optical element"
        raise NotImplementedError()
        
        
class SphericalReflection(OpticalElement):
    def __init__(self,z0,curv, aprad,centre = None):
        self.__z0 = z0
        self.__curv = curv
        self.__aprad = aprad
        if self.__curv != 0:
            self.__radius = 1/curv
        self.__centre = np.array(centre)
        
    def centre(self):
        return np.array(self.__centre)
        
    def intercept(self,ray):
        if self.__curv == 0:
            lamb = (self.__z0 - ray.p()[-1])/ray.k()[-1]
            point = ray.p() + lamb*ray.k()
            absdistance = np.linalg.norm(np.subtract(ray.p(),point))
            return [point,absdistance*ray.k()]
        else:
            r = ray.p() - self.centre()
            rdotk = np.inner(ray.k(),r)
            magray = np.linalg.norm(r)
            sqrt = rdotk**2 - (magray**2 - self.__radius**2)
            if sqrt < 0:
                return None
            else:
                sol1 = (-1*rdotk) - np.sqrt(sqrt)
                sol2 = (-1*rdotk) + np.sqrt(sqrt)
                absol1 = np.absolute(sol1)
                absol2 = np.absolute(sol2)
                if self.__curv> 0:
                    if absol1 <absol2:
                        soln = absol1
                    else:
                        soln = absol2
                elif self.__curv <0:
                    if absol1 <absol2:
                        soln = absol2
                    else:
                        soln = absol1
                    
                inci = soln*ray.k()
                point = np.add(ray.p(),inci)
                return [point, inci]
            
            
    def reflect_ray(self, ray):
        point = np.array(self.intercept(ray)[0])
        inci = np.array(self.intercept(ray)[-1])
        incinorm = inci/np.linalg.norm(inci)
        if self.__curv == 0:
           normal = np.array([0,0,1])
        else:
            normal = np.add(inci,np.subtract(ray.p(),self.__centre))
        normalnorm = normal/np.linalg.norm(normal)
        vreflect = reflect(incinorm,normalnorm)
        preflect = point
        ray.append(preflect,vreflect)
        return

"""
----------------------------------------------------------------------
Reflection is a function which takes in a normalised incident ray and a normal,
and returns a reflected ray. Again, this a generic reflection function, and 
doesn't depend on the surface, and hence is defined as a seperate function 
outside all the classes.
 
----------------------------------------------------------------------
"""
      
def reflect(inci,normal):
    vreflect = inci + 2*(np.dot(inci,normal))*normal
    return vreflect

sp = SphericalReflection(95,0.2,1.,[0,0,100])
op = OutputPlane(70)

def reflectparallel(start,stop,number):
    space = np.linspace(start,stop,number)
    for i in space:
        ray1 = ray([0.1*i,0.,80.],[0.,0.,1.0])
        sp.reflect_ray(ray1)
        op.finalpoint(ray1)
        verts = ray1.vertices()
        xcord = [i[0] for i in verts]
        zcord = [i[-1] for i in verts]
        plt.plot(zcord,xcord)
    plt.show()
    
reflectparallel(-10,10,10)
    
        
