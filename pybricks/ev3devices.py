from logica.robot import Robot, RobotMotor
from logica.Physics import PhysicsObject
from .parameters import Port
import time

class Motor:

    def __init__(self, port):
        time.sleep(1)
        self.__robot:Robot = Robot.createRobot()
        match(port):
            case Port.A:
                self.motor:RobotMotor = self.__robot.motorA
            case Port.B:
                self.motor:RobotMotor = self.__robot.motorB
            case Port.C:
                self.motor:RobotMotor = self.__robot.motorC

    def angle(self):
        return self.motor.angle()

    def speed(self):
        return self.motor.speed()

    def run(self, speed):
        self.motor.run(speed)

    def stop(self):
        self.motor.stop()

class UltrasonicSensor:

    def __init__(self, port):
        time.sleep(1)
        robot:Robot = Robot.createRobot()
        self.__sensor = robot.head.robotSensor

    def distance(self):
        return self.__sensor.distance()