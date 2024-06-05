from .Object import Object, ObjectColletion
from math import sin, sqrt, cos, ceil
from pygame import transform, Surface, Rect
pi = 3.1415926
class PhysicsObject(Object):

    def __init__(self, coordinates:tuple[int]=(0,0), shape:tuple[int] = (0,0), color:tuple[int] = (0, 0, 0), mass:int = 0, directionable:bool = False, side:int = 0):
        Object.__init__(self, coordinates, shape, color)
        self.maxSpeed:tuple[int] = (0, 0)
        self.acceleration:list[tuple[int]] = [(0,0), (0,0)]
        self.massCenter:tuple[int] = self.bounds.center
        self.torque:list[int] = [0, 0]
        self.mass:int = mass
        self.speed:list[tuple[int]] = [(0,0), (0,0)]
        self.angle = 0
        self.resistence = 0.05
        self.gravity = 9.8
        self.i = self.mass*(self.bounds.width**2 + self.bounds.height**2)/12
        self.directionable:bool = directionable
        self.__side = side

    def setSpeed(self, speed:tuple[int]):
        self.speed[0] = speed

    def setAcceleration(self, acceleration:tuple[int]):
        self.acceleration[0] = acceleration

    def setTorque(self, torque:int):
        self.torque[0] = torque

    def addSpeed(self, speed:tuple[int]):
        speedX, speedY = speed
        speed_X, speed_Y = self.speed[1]
        self.speed[1] = (speed_X + speedX, speed_Y + speedY)

    def addAcceleration(self, acceleration:tuple[int]):
        AccelerationX, AccelerationY = acceleration
        Acceleration_X, Acceleration_Y = self.acceleration[1]
        res = self.gravity*self.resistence
        self.acceleration[1] = (
            0 if abs(Acceleration_Y + AccelerationY) < res else (Acceleration_X + AccelerationX- res), 
            o if abs(Acceleration_Y + AccelerationX) < res else (Acceleration_Y + AccelerationY - res)
        )

    def addTorque(self, torque:int):
        self.torque[1] += torque

    def onCollition(self, speed:tuple[int], aceletarion:tuple[int], ratio:int, angle:int, mass:int):
        mt = mass + self.mass
        speedX, speedY = self.speed[0]
        speed_X, speed_Y = speed
        self.setSpeed((
            (self.mass*speedX - mass*speedX + 2*mass*speed_X)/mt,
            (self.mass*speedY - mass*speedY + 2*mass*speed_Y)/mt
        ))
        if(self.directionable):
            self.__side = 0
        self.setAcceleration((
            0, 0
        ))
        self.addTorque(
            ratio*PhysicsObject.force(aceletarion, mass)[0]*sin(angle)
        )

    def setSide(self, side:int):
        if(side == 1 or side == 0 or side == -1):
            self.__side = side

    def getSide(self)->int:
        return self.__side

    def logic(self):
        self.acceleration[0] = (
            (self.acceleration[0][0] + self.acceleration[1][0]),   
            (self.acceleration[0][1] + self.acceleration[1][1])
        )
        self.acceleration[1] = (0, 0)
        self.speed[0] = (
            (self.speed[0][0] + self.speed[1][0] + self.acceleration[0][0])*(1-self.resistence),
            (self.speed[0][1] + self.speed[1][1] + self.acceleration[0][1])*(1-self.resistence)
        )
        self.speed[1] = (0, 0)
        torque = (self.torque[0] + self.torque[1])*(1-self.resistence)
        self.angle += torque/self.i
        self.angle %= 2*pi
        self.torque[0] = torque
        self.torque[1] = 0
        if(self.directionable):
            normaSpeed = PhysicsObject.norma(self.speed[0])
            normalAngle = PhysicsObject.vectorNormalAngle(self.angle)
            signedX = (torque/(abs(torque)+0.00000000000001))*self.__side
            signedY = -signedX
            if abs(signedX) > 0:
                self.setSpeed((
                    normalAngle[0]*normaSpeed*signedX,
                    normalAngle[1]*normaSpeed*signedY
                ))
        self.setPosition((
            self.bounds.x + self.speed[0][0],
            self.bounds.y + self.speed[0][1]
        ))

    def isCollition(self, rect:Rect):
        return self.bounds.colliderect(rect)

    @staticmethod
    def momentum(speed:tuple[int], mass:int):
        return (speed[0]*mass, speed[1]*mass)

    @staticmethod
    def torque(ratio:int, force:int, angle:int):
        return ratio*force*sin(angle)

    @staticmethod
    def force(acceleration:tuple[int], mass:int):
        return (acceleration[0]*mass, acceleration[1]*mass)

    @staticmethod
    def norma(vector:tuple[int]):
        return sqrt(vector[0]**2 + vector[1]**2)
    
    @staticmethod
    def normalVector(vector:tuple[int]):
        dot = PhysicsObject.dotProduct(vector)
        if dot == 0:
            return (0, 0)
        return (vector[0]/dot, vector[1]/dot)

    @staticmethod
    def vectorNormalAngle(angle):
        return (
            cos(angle),
            sin(angle)
        )

class PhysicsObjectCollection(ObjectColletion):

    def __init__(self, objects:list[Object]):
        ObjectColletion.__init__(self, objects)

    def isCollition(self, object:PhysicsObject):
        for i in self.getObjects():
            if i.bounds.colliderect(object.bounds) and ((abs(object.speed[0][0]) > 0.5 or abs(object.speed[0][1]) > 0.5)):
                speed = i.speed[0]
                acceleration = i.acceleration[0]
                torque = i.torque
                angle = i.angle
                ratio = sqrt((i.bounds.centerx-object.bounds.centerx)**2 + (i.bounds.centery - object.bounds.centery)**2)
                i.onCollition(
                    object.speed[0], 
                    object.acceleration[0], 
                    ratio,
                    object.angle,
                    object.mass
                    )
                print(i.bounds.x, i.bounds.y)
                object.onCollition(speed, acceleration, ratio, angle, i.mass)
                return True
        return False