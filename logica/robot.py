from .Physics import PhysicsObject, pi
from .Object import Object
from collections import deque
from pygame.image import load
from pygame import transform, Surface, Rect
from math import sqrt
import time
import threading

class RobotSensor:

    def __init__(self, head):
        self.__head = head
        self.__continue = False
        self.__head.setEvent(self.__encontrado)
        self.__distance:int = 0

    def __encontrado(self, distance:int):
        self.__continue = False
        self.__distance = distance

    def distance(self):
        self.__continue = True
        self.__head.initLazer()
        while self.__continue:
            time.sleep(0.01)
        return self.__distance

class RobotMotor:

    def __init__(self, port, robot):
        self.__port = port
        self.__robot:Robot = robot
        self.__hilo:Thread = None
        self.__continue:bool = False
        self.__ejecute:bool = False
        self.__speed:int = 0
        self.__initialBoundsRobot = self.__robot.bounds

    def setSpeed(self, speed:int):
        self.__speed = speed

    def speed(self):
        return self.__speed

    def run(self, speed):
        if not self.__hilo:
            self.__continue = True
            self.__robot.colition = False
            self.__hilo = threading.Thread(target=self.__run, args=(speed,))
            self.__hilo.start()

    def __run(self, speed):
        while self.__continue:
            if self.__robot.colition:
                time.sleep(0.1)
            elif not self.__ejecute:
                self.__speed = speed
                self.__ejecute = True
                match(self.__port):
                    case 0:
                        self.__robot.appendAction(self.__run0)
                    case 1:
                        self.__robot.appendAction(self.__run1)
                    case 2:
                        self.__robot.appendAction(self.__run2)

    def __run0(self, robot):
        velAngu = self.__speed*pi/180
        vel = (self.__initialBoundsRobot.width-20)*velAngu/2
        if robot.motorB.speed() == 0:
            robot.setSide(-1)
            robot.setTorque(-robot.i*velAngu)
            robot.setSpeed((vel, 0))
        elif (not robot.function):
            robot.setSide(0)
            velAnguMotor = robot.motorB.speed()*pi/180
            velMotor = self.__initialBoundsRobot.width*velAnguMotor/2
            robot.setTorque(robot.i*(velAnguMotor-velAngu))
            vector = PhysicsObject.vectorNormalAngle(robot.angle)
            robot.addSpeed(((vel + velMotor)*vector[0], -(vel + velMotor)*vector[1]))
            robot.function = True
        self.__ejecute = False

    def __run1(self, robot):
        velAngu = self.__speed*pi/180
        vel = (self.__initialBoundsRobot.width-20)*velAngu/2
        if robot.motorA.speed() == 0:
            robot.setSide(1)
            robot.setTorque(robot.i*velAngu)
            robot.setSpeed((vel, 0))
        elif (not robot.function):
            robot.setSide(0)
            velAnguMotor = robot.motorA.speed()*pi/180
            velMotor = self.__initialBoundsRobot.width*velAnguMotor/2
            robot.setTorque(robot.i*(velAngu-velAnguMotor))
            vector = PhysicsObject.vectorNormalAngle(robot.angle)
            robot.addSpeed(((vel + velMotor)*vector[0], -(vel + velMotor)*vector[1]))
            robot.function = True
        self.__ejecute = False

    def __run2(self, robot):
        robot.head.angle += self.__speed
        robot.head.angle %= 2*pi
        self.__ejecute = False

    def angle(self):
        return self.__robot.angle

    def stop(self):
        self.__speed = 0
        self.__continue = False

class Lazer(PhysicsObject):

    maxDistance = 2000

    def __init__(self, position:tuple[int], angle:int):
        PhysicsObject.__init__(self, coordinates=position, shape=(1, 1), color=(255, 0, 0), mass=0)
        self.distance:int = 0
        self.__colitionEvent = None
        self.__positionInitial = self.bounds.center
        self.resistence = 0

    def setColitionEvent(self, event):
        self.__colitionEvent = event

    def setInitialPosition(self, position:tuple[int], angle:int):
        normalVector = PhysicsObject.vectorNormalAngle(angle)
        speed = 1
        self.__positionInitial = position
        self.setPosition(position)
        self.setSpeed((
            normalVector[0]*speed,
            normalVector[1]*speed
        ))

    def logic(self):
        norma = PhysicsObject.norma((
            self.__positionInitial[0]-self.bounds.x,
            self.__positionInitial[1]-self.bounds.y
        ))
        if norma < 200:
            PhysicsObject.logic(self)
            # print(self.bounds.x, self.bounds.y)
        else:
            self.setSpeed((
                0, 0
            ))
            robot = Robot.createRobot()
            self.distance = sqrt((robot.bounds.centerx-self.bounds.centerx)**2 + (robot.bounds.centery - self.bounds.centery)**2)
            if self.__colitionEvent:
                self.__colitionEvent(self.getDistance())

    def onCollition(self, speed:tuple[int], aceletarion:tuple[int], ratio:int, angle:int, mass:int):
        self.setSpeed((
            0, 0
        ))
        robot = Robot.createRobot()
        if self.__colitionEvent:
            self.__colitionEvent(self.getDistance())

    def getDistance(self):
        norma = PhysicsObject.norma((
            self.__positionInitial[0]-self.bounds.x,
            self.__positionInitial[1]-self.bounds.y
        ))
        if(norma > Lazer.maxDistance):
            return Lazer.maxDistance
        return norma

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
        self.resistence = 0.5
        self.motorA:RobotMotor = RobotMotor(0, self)
        self.motorB = RobotMotor(1, self)
        self.motorC = RobotMotor(2, self)
        self.function:bool = False
        self.colition:bool = False

    def draw(self, surface:Surface):
        image = self.image
        self.image = self.image.copy()
        self.head.draw(self.image)
        PhysicsObject.draw(self, surface)
        self.image = image

    def setWait(self):
        self.__wait = not self.__wait

    def appendAction(self, action):
        self.__actions.append(action)

    def onCollition(self, speed:tuple[int], aceletarion:tuple[int], ratio:int, angle:int, mass:int):
        self.colition = True
        PhysicsObject.onCollition(self, speed, aceletarion, ratio, angle, mass)

    def logic(self):
        if len(self.__actions) > 0 and not self.__wait:
            self.__actions.pop()(self)
        self.head.logic()
        PhysicsObject.logic(self)
        self.function = False

class Head(Object):

    def __init__(self, coordinates:tuple[int]):
        Object.__init__(self, coordinates, shape=(100, 100))
        self.image = transform.scale(
            load("./Imagenes/cabeza.png").convert_alpha(),
            (self.bounds.width, self.bounds.height)
            )
        self.__event = None
        self.lazer:Lazer = Lazer(self.bounds.center, 0)
        self.lazer.i = 1
        self.__wait:bool = False
        self.angle = 0
        self.robotSensor:RobotSensor = RobotSensor(self)
        self.lazer.setColitionEvent(self.__event)

    def initLazer(self):
        robot:Robot = Robot.createRobot()
        self.lazer.setInitialPosition(robot.bounds.center, self.angle)

    def logic(self):
        self.lazer.logic()

    def setEvent(self, event):
        self.__event = event

    def draw(self, surface:Surface):
        self.lazer.draw(surface)
        PhysicsObject.draw(self, surface)

    def setWait(self):
        self.__wait = not self.__wait
        if self.__event:
            self.__event()