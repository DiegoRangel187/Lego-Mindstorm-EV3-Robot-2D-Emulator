from .Physics import PhysicsObject
from .Object import Object
from pygame.image import load
from pygame import transform, Surface, Rect
from math import sqrt

class Lazer(PhysicsObject):

    maxDistance = 2000

    def __init__(self, position:tuple[int], angle:int):
        PhysicsObject.__init__(self, coordinates=position, shape=(1, 1), color=(255, 0, 0), mass=0)
        self.distance:int = 0
        self.__colitionEvent = None

    def setColitionEvent(self, event):
        self.__colitionEvent = event

    def setPosition(self, position:tuple[int], angle:int):
        normalVector = PhysicsObject.vectorNormalAngle(angle)
        speed = 40
        self.setSpeed((
            normalVector[0]*speed,
            normalVector[1]*speed
        ))

    def onCollition(self, speed:tuple[int], aceletarion:tuple[int], ratio:int, angle:int, mass:int):
        self.setSpeed((
            0, 0
        ))
        robot = Robot.createRobot()
        self.distance = sqrt((robot.bounds.centerx-self.bounds.centerx)**2 + (robot.bounds.centery - self.bounds.centery)**2)
        if self.__colitionEvent:
            self.__colitionEvent(self.getDistance())

    def getDistance(self):
        distance = self.distance
        if(distance > Lazer.maxDistance):
            return Lazer.maxDistance
        self.distance = 0
        return distance

class Robot(PhysicsObject):

    robot = None

    @staticmethod
    def createRobot(coordinates:tuple[int] = (0, 0)):
        if(Robot.robot):
            return Robot.robot
        Robot.robot = Robot(coordinates)
        return Robot.robot

    def __init__(self, coordinates:tuple[int]):
        PhysicsObject.__init__(self, coordinates, (100, 100), mass=1, directionable=True)
        self.image = transform.scale(
            load("./Imagenes/cuerpo.png").convert_alpha(),
            (self.bounds.width, self.bounds.height)
            )
        self.head:Head = Head(self.bounds.center)

    def draw(self, surface:Surface):
        PhysicsObject.draw(self, surface)
        self.head.draw(surface)

    def logic(self):
        self.head.setPosition(self.bounds.center)

class Head(Object):

    def __init__(self, coordinates:tuple[int]):
        Object.__init__(self, coordinates, shape=(100, 100))
        self.image = transform.scale(
            load("./Imagenes/cabeza.png").convert_alpha(),
            (self.bounds.width, self.bounds.height)
            )
        lazer:Lazer = Lazer(self.bounds.center, 0)
        self.__wait:bool = False
        self.angle = 0

    def setWait(self):
        self.__wait = not self.__wait