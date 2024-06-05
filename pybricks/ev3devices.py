from logica.robot import Robot
import threading
import time

class Motor:

    def __init__(self, port):
        time.sleep(1)
        self.__port = port
        self.__robot = Robot.createRobot()
        self.__hilo:Thread = None
        self.__continue:bool = False
        self.__ejecute:bool = False

    def run(self, speed):
        if not self.__hilo:
            self.__continue = True
            self.__hilo = threading.Thread(target=self.__run, args=(speed,))
            self.__hilo.start()

    def __run(self, speed):
        while self.__continue:
            if not self.__ejecute:
                match(self.__port):
                    case 0:
                        self.__ejecute = True
                        self.__robot.appendAction(self.__run0)
        print("stop")

    def __run0(self, robot:Robot):
        side = robot.getSide()
        robot.setSide(side - 1)
        robot.addTorque(robot.i*0.004)
        robot.setSpeed((1, 0))
        self.__ejecute = False

    def stop(self):
        self.__continue = False
