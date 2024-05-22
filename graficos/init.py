import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir el tamaño de la ventana
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)

# Crear la ventana
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Mi Ventana de Pygame")
bola = PhysicsObject((WIDTH/2, HEIGHT/2), (100, 100), (0, 0, 0), 5)
# Color de fondo
WHITE = (255, 255, 255)

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Llenar la ventana con el color de fondo
    window.fill(WHITE)
    bola.logic()
    bola.draw()
    # Actualizar la ventana
    pygame.display.update()