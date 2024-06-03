import pygame as pg
import sys
from logica.Physics import PhysicsObject, PhysicsObjectCollection, pi

# Inicializar Pygame
pg.init()

# Definir el tamaño de la ventana
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)

# Crear la ventana
window = pg.display.set_mode(WINDOW_SIZE)
pg.display.set_caption("Mi Ventana de pg")
bola = PhysicsObject((200, 130), (100, 100), (10, 10, 10), 10, directionable=True, side=1)
bola.image = pg.transform.scale(pg.image.load("./Imagenes/cuerpo.png").convert_alpha(), [100, 100])
#bola.image.fill((255, 255, 255))
#pg.draw.circle(bola.image, (0, 0, 0), bola.bounds.center, 40)
# bola.addSpeed(
#     (1, 0)
# )
bola.addTorque(bola.i)
bola.addAcceleration(
    (1, 0)
)
bola.resistence = 0.1
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
    bola.logic()
    bola.draw(window)
    ob.isCollition(bola)
    if bola.bounds.centerx + bola.bounds.width/2 + bola.speed[0][0]*2 >= WIDTH and abs(bola.speed[0][0]) > 0.5:
        bola.onCollition((0, 0), (-bola.torque[0], 0), 0.001, pi/2, 1000)
    elif bola.bounds.centerx - bola.bounds.width/2 <= 0 and bola.speed[0][0]  < 0:
        bola.onCollition((0, 0), (-bola.torque[0], 0), 0.001, pi/2, 1000)
    if bola.bounds.centery + bola.bounds.height/2 >= HEIGHT and abs(bola.speed[0][0]) > 0.5:
        bola.onCollition((0, 0), (-bola.torque[0], 0), 0.001, pi/2, 1000)
    elif bola.bounds.centery - bola.bounds.height/2 <= 0 and bola.speed[0][1] < 0:
        bola.onCollition((0, 0), (-bola.torque[0], 0), 0.001, pi/2, 1000)
    pg.display.flip()
    pg.display.update()