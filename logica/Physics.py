from .Object import Object
from math import sin, sqrt
from pygame import transform, Surface
class PhysicsObject(Object):

    def __init__(self, coordinates:tuple[int]=(0,0), shape:tuple[int] = (0,0), color:tuple[int] = (0, 0), mass:int = 0):
        Object.__init__(self, coordinates, shape, color)
        self.maxSpeed:tuple[int] = (0, 0)
        self.acceleration:list[tuple[int]] = [(0,0), (0,0)]
        self.massCenter:tuple[int] = self.bounds.center
        self.torque:list[int] = [0, 0]
        self.mass:int = mass
        self.speed:list[tuple[int]] = [(0,0), (0,0)]
        self.angle = 0
        self.resistence = 0
        self.gravity = 0
        self.i = self.mass*(self.bounds.width**2 + self.bounds.height**2)/12

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
        self.acceleration[1] = (Acceleration_X + AccelerationX, Acceleration_Y + AccelerationY)

    def addTorque(self, torque:int):
        self.torque[1] += torque

    def onCollition(self, speed:tuple[int], aceletarion:tuple[int], ratio:int, force:int, angle:int, mass:int):
        mt = mass + self.mass
        speedX, speedY = self.speed[0]
        speed_X, speed_Y = speed
        aceletarionX, aceletarionY = self.acceleration[0]
        aceletarion_X, aceletarion_Y = aceletarion
        self.setSpeed((
            (self.mass*speedX - mass*speedX + 2*mass*speed_X)/mt,
            (self.mass*speedY - mass*speedY + 2*mass*speed_Y)/mt
        ))
        self.setAcceleration((
            (self.mass*aceletarionX - mass*aceletarionX + 2*mass*aceletarion_X)/mt,
            (self.mass*aceletarionY - mass*aceletarionY + 2*mass*aceletarion_Y)/mt
        ))
        self.addTorque(
            ratio*force*sin(angle)
        )
        print(self.speed[0])

    def draw(self, matriz:list[bool], surface:Surface):
        rotated_image = transform.rotate(self.image, 45)
        rotated_rect = rotated_image.get_rect(center=self.bounds.center)
        surface.blit(rotated_image, rotated_rect.topleft)

    def logic(self):
        acceleration = (
            self.acceleration[0][0] + self.acceleration[1][0],
            self.acceleration[0][1] + self.acceleration[1][1]
            )
        normal = PhysicsObject.normalVector(acceleration)
        self.acceleration[0] = (
            acceleration[0] - normal[0]*self.gravity*self.resistence,   
            acceleration[1] - normal[1]*self.gravity*self.resistence
        )
        self.acceleration[1] = (0, 0)
        self.speed[0] = (
            self.speed[0][0] + self.speed[1][0] + self.acceleration[0][0],
            self.speed[0][1] + self.speed[1][1] + self.acceleration[0][1]
            )
        self.speed[1] = (0, 0)
        self.setPosition((
            self.bounds.x + self.speed[0][0],
            self.bounds.y + self.speed[0][1]
        ))
        torque = (self.torque[0] + self.torque[1]) - ((self.torque[0] + self.torque[1])/self.i)*self.mass*self.bounds.width*self.resistence
        self.angle += torque/self.i
        self.torque[0] = torque
        self.torque[1] = 0

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
    def dotProduct(vector:tuple[int]):
        return sqrt(vector[0]**2 + vector[1]**2)
    
    @staticmethod
    def normalVector(vector:tuple[int]):
        dot = PhysicsObject.dotProduct(vector)
        if dot == 0:
            return (0, 0)
        return (vector[0]/dot, vector[1]/dot)