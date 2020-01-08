import numpy as np
import pygame
import random

WIDTH, HEIGHT = (3*160, 3*180)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (50, 50, 50)
BLUE = (0, 0, 255)
GREEN = (20, 255, 20)
BROWN = (160, 80, 20)
RED = (255,0,0)

def draw_grid(screen):
    for x in range(0, WIDTH, 3):
        pygame.draw.line(screen, GREY, (x,0), (x,HEIGHT))
    for y in range(0, HEIGHT, 3):
        pygame.draw.line(screen, GREY, (0,y), (WIDTH,y))


pygame.init()


def visualize_map(matrix):
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption('AmstelHague')
    clock = pygame.time.Clock()


    in_loop = True
    while in_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        screen.fill(GREEN)
        for x, row in enumerate(matrix):
            for y, val in enumerate(row):
                if val == 'W':
                    pygame.draw.rect(screen, BLUE, (3*x, 3*y, 3, 3))
                if val in ['E', 'B', 'M']:
                    pygame.draw.rect(screen, BROWN, (3*x, 3*y, 3, 3))
                if val == 'X':
                    pygame.draw.rect(screen, RED, (3*x, 3*y, 3, 3))

        draw_grid(screen)
        pygame.display.flip()
        clock.tick(10)
