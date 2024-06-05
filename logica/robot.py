from .Physics import PhysicsObject
from .Object import Object
from collections import deque
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

    def setInitialPosition(self, position:tuple[int], angle:int):
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
        self.head:Head = Head((self.bounds.width/2-20, 0))
        self.__wait:bool = False
        self.__actions:deque = deque()
        self.head.setEvent(self.setWait)
        self.resistence = 0.1

    def draw(self, surface:Surface):
        image = self.image
        self.image = self.image.copy()
        self.head.draw(self.image)
        PhysicsObject.draw(self, surface)

    def setWait(self):
        self.__wait = not self.__wait

    def appendAction(self, action):
        self.__actions.append(action)

    def logic(self):
        if len(self.__actions) > 0 and not self.__wait:
            self.__actions.pop()(self)
        self.head.logic()
        PhysicsObject.logic(self)

class Head(Object):

    def __init__(self, coordinates:tuple[int]):
        Object.__init__(self, coordinates, shape=(100, 100))
        self.image = transform.scale(
            load("./Imagenes/cabeza.png").convert_alpha(),
            (self.bounds.width, self.bounds.height)
            )
        self.lazer:Lazer = Lazer(self.bounds.center, 0)
        self.lazer.i = 1
        self.__wait:bool = False
        self.angle = 0
        self.__event = None

    def logic(self):
        self.lazer.logic()

    def setEvent(self, event):
        self.__event = event

    def setWait(self):
        self.__wait = not self.__wait
        if self.__event:
            self.__event()