"""
----------------------------------------------------------------------
Rohan Kamath 01209729
rkk216@ic.ac.uk

"An Optical Ray Tracer"
----------------------------------------------------------------------
"""

import numpy as np
import matplotlib.pyplot as plt


"""
----------------------------------------------------------------------
First, I've initialised a ray class. It has a start point, and a start 
direction. Methods have been written to return start point, 
start direction,current point, current direction, and to append new 
points.
----------------------------------------------------------------------
"""

class ray:
    rayList = []
    def __init__(self,startpoint,startdir):
        self.__startp = np.array(startpoint) 
        self.__startdir = np.array(startdir)
        self.__pos = [self.__startp]
        self.__dir = [self.__startdir]
    def startp(self):
        return self.__startp
    
    def startdir(self) :
        return self.__startdir
    
    def p(self):
        return self.__pos[-1]
    
    def k(self):
        return self.__dir[-1]
    
    def append(self,p,k):
        self.__pos.append(np.array(p))
        self.__dir.append(np.array(k))
        
        return
    
    def vertices(self):
        return self.__pos


"""
----------------------------------------------------------------------
Then, there's a class called optical element, with the inherited class 
of Spherical Refrection. The spherical refraction class is instantiated
with a Z intercept, curvature, two refractive indices and an aperture 
radius and a centre. The methods are intercept, which finds the intercept
with a ray. It returns the point of incidence, and the incident ray.
The method propagate ray propagates the ray and returns the refracted ray
----------------------------------------------------------------------
"""
class OpticalElement:
  def propagate_ray(self, ray):
    "propagate a ray through the optical element"
    raise NotImplementedError()
    

class SphericalRefraction(OpticalElement):
    def __init__(self,z0,curv,n1,n2,aprad,centre = None):
        self.__z0 = z0
        self.__curv = curv
        self.__n1 = n1
        self.__n2 = n2
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
    
    def propagate_ray(self, ray): 
        if self.intercept(ray) == None or np.absolute(self.intercept(ray)[0][0]) > self.__aprad:
            ray.append(ray.p(),ray.k())
        else:
            point = np.array(self.intercept(ray)[0])
            inci = np.array(self.intercept(ray)[-1])
            incinorm = inci/np.linalg.norm(inci)
            if self.__curv == 0:
               normal = np.array([0,0,1])
            else:
                normal = np.add(inci,np.subtract(ray.p(),self.__centre))
            normalnorm = normal/np.linalg.norm(normal)
            vrefract = snell(self.__n1, self.__n2,incinorm,normalnorm)
            prefract = point
            ray.append(prefract,vrefract)
        return
        
    

class OutputPlane(OpticalElement):
    def __init__(self,z0):
        self.__z0 = z0
    def z0(self):
        return self.__z0
    
    def finalpoint(self,ray):
        lamb = (self.__z0 - ray.p()[-1])/ray.k()[-1]
        point = ray.p() + lamb*ray.k()
        absdistance = np.linalg.norm(np.subtract(ray.p(),point))
        ray.append(point,absdistance*ray.k())
        return [point,absdistance*ray.k()]

        
"""
----------------------------------------------------------------------

Snell's law is written as a seperate function outside all of the classes
as it is a generic snells law function, and does not depend on the refractive
surface. It takes in normalised incidence and normal vectors and gives out
a refracted vector.

It can be reused for any surface, and isn't specific to a spherical refracting 
one.
----------------------------------------------------------------------
"""
        
def snell(n1,n2,inci,normal): #inci and normal should be unit vectors
    relindex =n2/n1
    theta1 = np.arccos(np.dot(inci,normal))
    theta2 = relindex*np.sin(theta1)
    if np.sin(theta2) > (1/relindex):
        raise Exception("total internal reflection")
    else:
        vrefract = (relindex*inci) + ((relindex*np.cos(theta1))-np.cos(theta2))*normal
    return vrefract



    
sp = SphericalRefraction(95,0.2,1,1.5,1.,[0,0,100])  #(self,z0,curv,n1,n2,aprad,centre)
sp2 = SphericalRefraction(102,0,1.5,1.,1)




def bundleparallel(start,stop,number):
    space = np.linspace(start,stop,number)
    for i in space:
        ray1 = ray([0.1*i,0.,80.],[0.,0.,1.0])
        sp.propagate_ray(ray1)
        sp2.propagate_ray(ray1)
        op.finalpoint(ray1)
        verts = ray1.vertices()
        xcord = [i[0] for i in verts]
        zcord = [i[-1] for i in verts]
        plt.plot(zcord,xcord)
    plt.show()

def bundlepolar(start,stop,number): 
    space = np.linspace(start,stop,number)
    global x,y,xcord,ycord
    x = [];    y = [];    xcord = [];    ycord = [];
    for i in space:
        for j in range(10):
            x.append(i*np.sin(j*np.pi/5))
            y.append(i*np.cos(j*np.pi/5))
    for i in range(len(x)):
        ray1 = ray([x[i],y[i],0],[0,0,1.0])
        sp.propagate_ray(ray1)
        sp2.propagate_ray(ray1)
        op.finalpoint(ray1)
        xcord.append(ray1.p()[0])
        ycord.append(ray1.p()[1])
    return

    
    

        