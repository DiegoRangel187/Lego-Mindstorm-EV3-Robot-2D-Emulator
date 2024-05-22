import pygame as pg
import sys
from logica.Physics import PhysicsObject

# Inicializar Pygame
pg.init()

# Definir el tamaño de la ventana
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)

# Crear la ventana
window = pg.display.set_mode(WINDOW_SIZE)
pg.display.set_caption("Mi Ventana de pg")
bola = PhysicsObject((10, 10), (100, 100), (10, 10, 10), 10000)
bola.addSpeed(
    (6, 16)
)
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
    bola.logic()
    bola.draw([], window)
    if bola.bounds.x + bola.bounds.width - 1 >= WIDTH and bola.speed[0][0] > 0:
        bola.onCollition((0, 0), (0, 0), 0, 0, 0, 1000)
    elif bola.bounds.x + 1 <= 0 and bola.speed[0][0]  < 0:
        bola.onCollition((0, 0), (0, 0), 0, 0, 0, 1000)
    if bola.bounds.y + bola.bounds.height >= HEIGHT and bola.speed[0][1] > 0:
        bola.onCollition((0, 0), (0, 0), 0, 0, 0, 1000)
    elif bola.bounds.y <= 0 and bola.speed[0][1] < 0:
        bola.onCollition((0, 0), (0, 0), 0, 0, 0, 1000)
    pg.display.flip()
    pg.display.update()