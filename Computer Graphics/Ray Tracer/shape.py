
from vectors import *
from ray import *
import numpy as N
from material import *

EPSILON = 0.1

class GeometricObject():
    def hit(self, ray):
        """Returns (t, point, normal, object) if hit and t > EPSILON"""
        return (None, None, None, None)
    def castShadows(self):
        return False

class Sphere(GeometricObject):
    def __init__(self, point=(0,0,0), radius=1, material=None, shadows=True):
        if not(material):
            material = Phong()
        self.point = vec(point)
        self.radius = radius
        self.material = material
        self.shadows = shadows

    def __repr__(self):
        return "Sphere: " + repr(self.point) + repr(self.radius)
    def castShadows(self):
        return self.shadows

    def hit(self, ray):
        # assume sphere at origin, so translate ray:
        raypoint = ray.point - self.point
        a = N.dot(ray.vector, ray.vector) #size of ray.vector
        b = 2*N.dot(raypoint, ray.vector)
        c = N.dot(raypoint, raypoint) - self.radius*self.radius
        disc = b*b - 4*a*c
        if disc > 0.0:
            t = (-b-N.sqrt(disc))/(2*a)
            if t > EPSILON:
                p = ray.pointAt(t)
                n = normalize(self.normalAt(p))
                return (t, p, n, self)
            t = (-b+N.sqrt(disc))/(2*a)
            if t > EPSILON:
                p = ray.pointAt(t)
                n = normalize(self.normalAt(p))
                return (t, p, n, self)
        return (None, None, None, None)

    def normalAt(self, point):
        return normalize(point - self.point)


class Plane(GeometricObject):
    def __init__(self, normal, point, material, shadows=False):
        self.point = vec(point)
        self.normal = normalize(vec(normal))
        self.material = material
        self.shadows = shadows

    def __repr__(self):
        return "Plane: "+repr(self.normal)+repr(self.point)
    def castShadows(self):
        return self.shadows

    def hit(self, ray):
        #pass
        point = self.point - ray.point
	denominator = N.dot(self.normal, ray.vector)
	t = N.dot(self.normal, point)/denominator
	p = ray.point + (t*ray.vector)
	#if (N.dot(ray.vector, self.normal) < 0):   #checks if im hitting the front
        if t > EPSILON:
                #print t
                return (t, p, self.normal, self)

	return (None, None, None, None)


    def normalAt(self, point):
        return self.normal

class PlaneIntersection(GeometricObject):
    def __init__(self, planes):
        self.planes = planes
        self.shadows = True

    def castShadows(self):
        return self.shadows
    
    def hit(self, ray):
        hasGoneOut = False
        hit = (None, None, None, None)
        for plane in self.planes:
            if (N.dot(ray.vector, plane.normal) and (not hasGoneOut)) < 0:
                hit = plane.hit(ray)
            else:
                hasGoneOut = True
        for plane in self.planes:
            if hit != (None, None, None, None):
                vec1 = hit[1] - plane.point
                vec2 = N.dot(vec1, plane.normal)
                if(vec2 < 0):
                    return (None, None, None, None)
        return hit
    '''        
    def hit(self, ray):
        maxin = 0
        minout = float('inf')
        lastin = (None, None, None, None)
        hasGoneOut = 0
        hit = (None, None, None, None)
        #dist1, point1, normal1, obj1 = (None, None, None, None)
        for plane in self.planes:
            dist, point, normal, obj = plane.hit(ray)
            #hit = plane.hit(ray)Ellpsiod
            #direction = N.dot(ray.vector, vec(normal))
            if (N.dot(ray.vector, plane.normal) and (hasGoneOut == 0)) < 0:
                #entering
                lastin = plane.hit(ray)
                #if(maxin < dist):
                #    maxin = dist
                #    hit = plane.hit(ray)
            
            else:
                #exiting
                hasGoneOut = 1
                #if(minout > dist):
                #    minout = dist
        if(lastin != (None, None, None, None)):
            for plane in self.planes:
                checkVec = plane.point - lastin[1]
                checkVec = N.dot(checkVec, plane.normal)
                if(checkVec < 0):
                    return (None, None, None, None)
            
        return lastin
       '''     
            
class Cube(PlaneIntersection):
    pass

class QuadricOfMyChoice(GeometricObject):   #hyperboloid 
    def __init__(self, point=(0,0,0), A=1, B=1, C=1, material=None, shadows=True):
        if not(material):
            material = Phong()
        self.point = vec(point)
        self.A = A
        self.B = B
        self.C = C
        #self.radius = radius
        self.material = material
        self.shadows = shadows

    def __repr__(self):
        return "Hyperboloid: " + repr(self.point) + repr(self.A) + repr(self.B) + repr(self.C)
    def castShadows(self):
        return self.shadows

    def hit(self, ray):
        # assume sphere at origin, so translate ray:
        raypoint = ray.point - self.point
        p0 = raypoint[0]
        p1 = raypoint[1]
        p2 = raypoint[2]
        v0 = ray.vector[0]
        v1 = ray.vector[1]
        v2 = ray.vector[2]
        a = ((N.square(v0))/(N.square(self.A))) - ((N.square(v1))/(N.square(self.B))) + ((N.square(v2))/(N.square(self.C)))
        b = ((2*p0*v0)/(N.square(self.A))) - ((2*p1*v1)/(N.square(self.B))) + ((2*p2*v2)/(N.square(self.C)))
        c = ((N.square(p0))/(N.square(self.A))) - ((N.square(p1))/(N.square(self.B))) + ((N.square(p2))/(N.square(self.C))) - 1
        disc = b*b - 4*a*c
        if disc > 0.0:
            t = (-b-N.sqrt(disc))/(2*a)
            if t > EPSILON:
                p = ray.pointAt(t)
                n = normalize(self.normalAt(p))
                return (t, p, n, self)
            t = (-b+N.sqrt(disc))/(2*a)
            if t > EPSILON:
                p = ray.pointAt(t)
                n = normalize(self.normalAt(p))
                return (t, p, n, self)
        return (None, None, None, None)

    def normalAt(self, point):
        p0 = point[0]
        p1 = point[1]
        p2 = point[2]
        v = vec( (2*p0/(N.square(self.A))), -(2*p1/(N.square(self.B))), (2*p2/(N.square(self.C))) )
        return normalize(v)
    
class QuadricOfMyChoice2(GeometricObject):   #hyperboloid 
    def __init__(self, point=(0,0,0), A=1, B=1, C=1, material=None, shadows=True):
        if not(material):
            material = Phong()
        self.point = vec(point)
        self.A = A
        self.B = B
        self.C = C
        #self.radius = radius
        self.material = material
        self.shadows = shadows

    def __repr__(self):
        return "Hyperboloid: " + repr(self.point) + repr(self.A) + repr(self.B) + repr(self.C)
    def castShadows(self):
        return self.shadows

    def hit(self, ray):
        # assume sphere at origin, so translate ray:
        raypoint = ray.point - self.point
        p0 = raypoint[0]
        p1 = raypoint[1]
        p2 = raypoint[2]
        v0 = ray.vector[0]
        v1 = ray.vector[1]
        v2 = ray.vector[2]
        a = ((N.square(v0))/(N.square(self.A))) + ((N.square(v1))/(N.square(self.B))) - ((N.square(v2))/(N.square(self.C)))
        b = ((2*p0*v0)/(N.square(self.A))) + ((2*p1*v1)/(N.square(self.B))) - ((2*p2*v2)/(N.square(self.C)))
        c = ((N.square(p0))/(N.square(self.A))) + ((N.square(p1))/(N.square(self.B))) - ((N.square(p2))/(N.square(self.C))) - 1
        disc = b*b - 4*a*c
        if disc > 0.0:
            t = (-b-N.sqrt(disc))/(2*a)
            if t > EPSILON:
                p = ray.pointAt(t)
                n = normalize(self.normalAt(p))
                return (t, p, n, self)
            t = (-b+N.sqrt(disc))/(2*a)
            if t > EPSILON:
                p = ray.pointAt(t)
                n = normalize(self.normalAt(p))
                return (t, p, n, self)
        return (None, None, None, None)

    def normalAt(self, point):
        p0 = point[0]
        p1 = point[1]
        p2 = point[2]
        v = vec( (2*p0/(N.square(self.A))), (2*p1/(N.square(self.B))), -(2*p2/(N.square(self.C))) )
        return normalize(v)
    
class Ellpsiod(GeometricObject):
    def __init__(self, point=(0,0,0), A=1, B=1, C=1, material=None, shadows=True):
        if not(material):
            material = Phong()
        self.point = vec(point)
        self.A = A
        self.B = B
        self.C = C
        #self.radius = radius
        self.material = material
        self.shadows = shadows

    def __repr__(self):
        return "Ellipsoid: " + repr(self.point) + repr(self.A) + repr(self.B) + repr(self.C)
    def castShadows(self):
        return self.shadows

    def hit(self, ray):
        # assume sphere at origin, so translate ray:
        raypoint = ray.point - self.point
        p0 = raypoint[0]
        p1 = raypoint[1]
        p2 = raypoint[2]
        v0 = ray.vector[0]
        v1 = ray.vector[1]
        v2 = ray.vector[2]
        a = ((N.square(v0))/(N.square(self.A))) + ((N.square(v1))/(N.square(self.B))) + ((N.square(v2))/(N.square(self.C)))
        b = ((2*p0*v0)/(N.square(self.A))) + ((2*p1*v1)/(N.square(self.B))) + ((2*p2*v2)/(N.square(self.C)))
        c = ((N.square(p0))/(N.square(self.A))) + ((N.square(p1))/(N.square(self.B))) + ((N.square(p2))/(N.square(self.C))) - 1
        disc = b*b - 4*a*c
        if disc > 0.0:
            t = (-b-N.sqrt(disc))/(2*a)
            if t > EPSILON:
                p = ray.pointAt(t)
                n = normalize(self.normalAt(p))
                return (t, p, n, self)
            t = (-b+N.sqrt(disc))/(2*a)
            if t > EPSILON:
                p = ray.pointAt(t)
                n = normalize(self.normalAt(p))
                return (t, p, n, self)
        return (None, None, None, None)

    def normalAt(self, point):
        p0 = point[0]
        p1 = point[1]
        p2 = point[2]
        v = vec( (2*p0/(N.square(self.A))), (2*p1/(N.square(self.B))), (2*p2/(N.square(self.C))) )
        return normalize(v)

if __name__ == "__main__":
    s1 = Sphere(vec(0,0,0), 2, Phong())
    print( s1.normalAt(vec(0,0,2)))
    r = Ray(vec(-10,0,0), vec(1,0,0))
    print( s1.hit(r))
    
