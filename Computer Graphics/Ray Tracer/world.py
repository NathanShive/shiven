import random, numpy

from vectors import *
from camera import *
from light import *
from shape import *

EPSILON = 1.0e-10

class AbstractWorld():
    def colorAt(self, x, y):
        pass
    
class World(AbstractWorld):
    def __init__(self, 
                 objects=None, 
                 lights=None,
                 camera=None,
                 maxDepth = 5,
                 neutral = vec(.25,.5,1),
                 fogBegin = 1.0e10,
                 fogEnd = 1.0e10,
                 nsamples = 1):
        if not(objects):
            objects = [Sphere()]
        if not(lights):
            lights = [Light()]
        if not(camera):
            camera = Camera()

        self.objects = objects
        self.lights = lights
        self.camera = camera
        self.maxDepth = maxDepth
        self.neutral = vec(neutral)
        self.nsamples = nsamples
        self.fogBegin = fogBegin
        self.fogEnd = fogEnd

    def colorAt(self, x, y):
        ray = self.camera.ray(x,y)
        if ray.depth > self.maxDepth:
            return self.neutral
        else:
            return self.colorFromRay(ray)
        
    def colorFromRay(self, ray):
        if ray.depth > self.maxDepth:
            return self.neutral
        dist, point, normal, obj = ray.closestHit(self)
        if not(obj is None):
            if dist > self.fogEnd:
                return self.neutral
            elif dist < self.fogBegin:
                color = obj.material.colorAt(point,
                                             normal,
                                             ray,
                                             self)
                if color is None:
                    print "none color"
                    return self.neutral
                else:
                    return clamp(color, 0, 1)
            else:
                fogPortion = (dist-self.fogBegin)/(self.fogEnd-self.fogBegin)     
                color = obj.material.colorAt(point,
                                             normal,
                                             ray,
                                             self)
                if color is None:
                    print "none color"
                    return self.neutral
                finalColor = (1-fogPortion)*color + (fogPortion)*self.neutral
                return clamp(finalColor, 0, 1)
        else:
            return self.neutral
            
class ThreeSpheres(World):
    def __init__(self,
                 objects=None,
                 lights=None,
                 camera=None):
        if not(lights):
            lights = [Light((1,1,.5))]
        if not(objects):
            objects = [Sphere((2,2,-1),3,Reflector(color=(1,0,0))),
                       Sphere((2,-2,-0),3,Phong(color=(0,1,0))),
                       Sphere((-2,0,1),3,Phong(color=(0,0,1)))]
        if not(camera):
            camera = Camera()
        World.__init__(self, objects, lights, camera)

class MyWorld(World):
    #pass
    def __init__(self,
                 objects=None,
                 lights=None,
                 camera=None):
        if not(lights):
            #lights = [Light((1,1,2))]
            lights = [PointLight((1,1,1)),Light((1,1,2))]
            #lights = [Light((1,1,2))]
            #lights = [PointLight((2,7,-1))]
        if not(objects):
            top = Plane((0,1,0),(0,3,0),Phong(color=(0,0,1)))
            bottom = Plane((0,-1,0),(0,2,0),Phong(color=(1,1,0)))
            right = Plane((1,0,0),(1,0,0),Phong(color=(0,1,0)))
            left = Plane((-1,0,0),(-1,0,0),Phong(color=(0,0,1)))
            
            
            planes = [top, bottom, left, right]
            objects = [#Plane((0,1,0),(0,-10,-1),Phong(color=((102.0/256.0),(51.0/256.0),0))),       #ground
                        Plane((0,1,0),(0,-10,-1),Image(('images/''cobbles.jpg'),40)),                                         #sky ground
			#Plane((0,0,1),(-1,0,-1),Phong(color=(1,0,0))),
			Plane((0,10,0),(0,10,-1),Image()),     #sky 
			Ellpsiod((0,0,0),100 , .1, .1,Phong(color=(1,0,0))),                                           #X axis
			Ellpsiod((0,0,0),.1 , 100, .1,Phong(color=(0,1,0))),                                           #Y axis
			Ellpsiod((0,0,0),.1 , .1, 100,Phong(color=(0,0,1))),                                           #Z axis
			#Ellpsiod((-4,4,4),.1 , .1, 100,Phong(color=(1,0,1))),
			QuadricOfMyChoice((18,0,15),1 , 2, 1,Phong(color=((153.0/256.0),1,(51.0/256.0)))),              #hyperboliod thats holding up the sky
			#Sphere((-2,-2,-2),2,Phong(color=((76.0/256.0),0,(153.0/256.0)))),
			#Sphere((4,0,-3),4,Image()),
			#Sphere((4,-2,4),2,Phong(color=((153.0/256.0),1,(51.0/256.0)))),     greenish sphere
			Sphere((-7,-7,4),5,Phong(color=(1,1,1))),                                                       #snow man bottom
			Sphere((-7,-1,4),4,Phong(color=(1,1,1))),                                                       #snow man mid
			Sphere((-7,4,4),3,Phong(color=(1,1,1))),                                                        #snow man head
			Ellpsiod((-6,4,3),.2 , .2, 3.5,Phong(color=(1,(151/256.0),(13.0/256.0)))),                        #carrot noes
			#Ellpsiod((-6,4,3),4 , .2, .2,Phong(color=(1,(151/256.0),(13.0/256.0)))),                        #carrot noes diff direction
			Sphere((-7.5,5,2),.8,Phong(color=(0,0,0))),                                                     #snowman eye
			Sphere((-6.5,5,2),.8,Phong(color=(0,0,0))),                                                     #snowman eye
			Ellpsiod((-7,6.7,4),4 , .1, 4,Phong(color=((102/256.0),(51/256.0),0))),                         #snowman's Hat
			#Plane((0,0,-1),(0,0,-8),Phong(color=(0,1,1))),
			#Plane((1,0,1),(-10,0,-10),Reflector(color=(1,1,1))),                     #maybe a mirror
			#Plane((0,-1,0),(0,10,0),Image()),
			PlaneIntersection(planes),
			#Sphere((2,2,2),2,Reflector(color=(1,1,1))),
			#Sphere((2,2,2),2,Image()),
			#Sphere((0,2,2),3,Phong(color=(0,0,1)))
			]
        if not(camera):
            #camera = Camera()
            camera = lookAt()
        World.__init__(self, objects, lights, camera)



if __name__ == "__main__":
    w = World([Sphere()],[Light()],Camera())
    print(w.neutral)

                    
