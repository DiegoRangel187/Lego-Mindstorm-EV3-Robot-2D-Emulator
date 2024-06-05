import threading
import pygame as pg
import sys
from logica.robot import Robot
from logica.Physics import pi, PhysicsObjectCollection, PhysicsObject

class Light:

    def __init__(self):
        pass

    def on(self, color):
        print("led encendido de color", color)

    def off(self):
        print("led apagado")

class EV3Brick:

    def __init__(self):
        self.light = Light()
        self.__hilo = threading.Thread(target=self.__initGame)
        self.__hilo.start()

    def __initGame(self):
        pg.init()
        WIDTH, HEIGHT = 800, 600
        WINDOW_SIZE = (WIDTH, HEIGHT)
        window = pg.display.set_mode(WINDOW_SIZE)
        pg.display.set_caption("Simulador")
        robot:Robot = Robot.createRobot((110, 110))
        WHITE = (255, 255, 255)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            window.fill((255, 255, 255))
            if robot.bounds.centerx + robot.bounds.width/2 + robot.speed[0][0]*2 >= WIDTH and abs(robot.speed[0][0]) > 0.5:
                robot.onCollition((0, 0), (-robot.torque[0], 0), 0.001, pi/2, 1000)
            elif robot.bounds.centerx - robot.bounds.width/2 <= 0 and robot.speed[0][0]  < 0:
                robot.onCollition((0, 0), (-robot.torque[0], 0), 0.001, pi/2, 1000)
            elif robot.bounds.centery + robot.bounds.height/2 >= HEIGHT and abs(robot.speed[0][0]) > 0.5:
                robot.onCollition((0, 0), (-robot.torque[0], 0), 0.001, pi/2, 1000)
            elif robot.bounds.centery - robot.bounds.height/2 <= 0 and robot.speed[0][1] < 0:
                robot.onCollition((0, 0), (-robot.torque[0], 0), 0.001, pi/2, 1000)
            else:
                robot.colition = False
            robot.logic()
            robot.draw(window)
            pg.display.flip()
            pg.display.update()