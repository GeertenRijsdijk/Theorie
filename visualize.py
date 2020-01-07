import numpy as np
import pygame

WIDTH, HEIGHT = (720, 640)
WHITE = (255,255,255)
BLACK = (0,0,0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption('AmstelHague')
clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, WIDTH, 4):
        pygame.draw.line(screen, BLACK, (x,0), (x,HEIGHT))
    for y in range(0, HEIGHT, 4):
        pygame.draw.line(screen, BLACK, (0,y), (WIDTH,y))

in_loop = True
while in_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill(WHITE)
    draw_grid()
    pygame.display.flip()
    clock.tick(30)
