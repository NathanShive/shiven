# camera for ray tracer
# specify eye position and upper left, upper right,
# lower left, and lower right vectors

from ray import *
from vectors import *

class AbstractCamera():
    def ray(self, x, y):
        return Ray((0,0,0),(0,0,-1))

class Camera(AbstractCamera):
    def __init__(self,
                 eye = (0,0,10),
                 ul = (-10,10,-10),
                 ur = (10,10,-10),
                 ll = (-10,-10, -10),
                 lr = (10,-10,-10)):
        self.eye = vec(eye)
        self.ul = vec(ul)
        self.ur = vec(ur)
        self.ll = vec(ll)
        self.lr = vec(lr)
        
    def ray(self, x, y):
        """ given screen coords in [0,1]x[0,1] return ray from eye"""
        v1 = self.ul*(1-x) + self.ur*x
        v2 = self.ll*(1-x) + self.lr*x
        v = v1*(1-y) + v2*y
        return Ray(self.eye, normalize(v))

def lookAt(eye = (10,5,10),
           focus = (-20,-10,-20),
           up = (0,1,0),
           fovy = 45.0,
           aspect = 4.0/3.0):
    #pass
	#self.eye = vec(eye)
	v = vec(focus) - vec(eye)   #vector to focus
	dist = N.sqrt(N.dot(v,v)) #distance from eye to focus
	upVec = normalize(up)
	right = normalize(N.cross(v,upVec))
	hmag = dist*N.tan(fovy/2)
	vmag = hmag/aspect
        
        ur = vec(eye) + v + right*hmag + upVec * vmag 
        lr = vec(eye) + v + right*hmag - upVec * vmag
        ul = vec(eye) + v - right*hmag + upVec * vmag
        ll = vec(eye) + v - right*hmag - upVec * vmag
        
        return Camera(eye,ul,ur,ll,lr)
	#x = s * N.tan(fovy)
	#y = 4.0/3.0 * x
	#u = vec(up)
	#self.ul = vec(s*v + x*u)
	#self.
	
    
if __name__ == "__main__":
    c = Camera()
    print (c.ray(0.5,0.5))
