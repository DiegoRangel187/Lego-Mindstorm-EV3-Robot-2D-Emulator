import pygame as pg
import sys
from logica.Physics import PhysicsObject, PhysicsObjectCollection, pi
from logica.Robot import Robot

# Inicializar Pygame
pg.init()

# Definir el tamaño de la ventana
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)

# Crear la ventana
window = pg.display.set_mode(WINDOW_SIZE)
pg.display.set_caption("Mi Ventana de pg")
robot = Robot.createRobot()
#robot.image.fill((255, 255, 255))
#pg.draw.circle(robot.image, (0, 0, 0), robot.bounds.center, 40)
# robot.addSpeed(
#     (1, 0)
# )
robot.addTorque(robot.i*0.04)
robot.addAcceleration(
    (0, 0)
)
robot.resistence = 0.001
rectangles = [
    #PhysicsObject((100,200), (50, 50), (0, 0, 0), 1000)
]

ob = PhysicsObjectCollection(rectangles)

# Color de fondo
WHITE = (255, 255, 255)

# Bucle principal del juego
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Llenar la ventana con el color de fondo
    window.fill((255, 255, 255))
    ob.logic()
    ob.draw(window)
    robot.logic()
    robot.draw(window)
    ob.isCollition(robot)
    if robot.bounds.centerx + robot.bounds.width/2 + robot.speed[0][0]*2 >= WIDTH and abs(robot.speed[0][0]) > 0.5:
        robot.onCollition((0, 0), (-robot.torque[0], 0), 0.001, pi/2, 1000)
    elif robot.bounds.centerx - robot.bounds.width/2 <= 0 and robot.speed[0][0]  < 0:
        robot.onCollition((0, 0), (-robot.torque[0], 0), 0.001, pi/2, 1000)
    if robot.bounds.centery + robot.bounds.height/2 >= HEIGHT and abs(robot.speed[0][0]) > 0.5:
        robot.onCollition((0, 0), (-robot.torque[0], 0), 0.001, pi/2, 1000)
    elif robot.bounds.centery - robot.bounds.height/2 <= 0 and robot.speed[0][1] < 0:
        robot.onCollition((0, 0), (-robot.torque[0], 0), 0.001, pi/2, 1000)
    pg.display.flip()
    pg.display.update()