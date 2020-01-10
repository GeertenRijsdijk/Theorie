import numpy as np
import pygame
import random
from copy import copy

# Variables for the grid and colors
GRID_W, GRID_H = 3, 3

WIDTH, HEIGHT = (GRID_W*160, GRID_H*180)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (50, 50, 50)
BLUE = (0, 0, 255)
GREEN = (20, 255, 20)
BROWN = (160, 80, 20)
RED = (255,0,0)
MARBLE = (230, 230, 200)

# draws a grid on the pygame window
def draw_grid(screen):
    for x in range(0, WIDTH, GRID_W):
        pygame.draw.line(screen, GREY, (x,0), (x,HEIGHT))
    for y in range(0, HEIGHT, GRID_H):
        pygame.draw.line(screen, GREY, (0,y), (WIDTH,y))

        # Fonts

pygame.init()

# uses the matrix to print all water and houses on the screen
def visualize_map(matrix):
    real_screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
    screen = pygame.Surface((WIDTH, HEIGHT))
    pygame.display.set_caption('AmstelHague')
    clock = pygame.time.Clock()

    # main game loop for pygame
    in_loop = True
    while in_loop:
        pygame.event.pump()
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            in_loop = False
        elif event.type == pygame.VIDEORESIZE:
            real_screen = pygame.display.set_mode(event.dict['size'], pygame.DOUBLEBUF|pygame.RESIZABLE)
            draw_grid(screen)
            real_screen.blit(pygame.transform.scale(screen, event.dict['size']), (0, 0))
            pygame.display.flip()

        screen.fill(GREEN)
        for x, row in enumerate(matrix):
            for y, val in enumerate(row):
                if val == 'W':
                    pygame.draw.rect(screen, BLUE, (GRID_W*x, GRID_H*y, GRID_W, GRID_H))
                if val == 'E':
                    pygame.draw.rect(screen, BROWN, (GRID_W*x, GRID_H*y, GRID_W, GRID_H))
                if val == 'B':
                    pygame.draw.rect(screen, BLACK, (GRID_W*x, GRID_H*y, GRID_W, GRID_H))
                if val in 'M':
                    pygame.draw.rect(screen, MARBLE, (GRID_W*x, GRID_H*y, GRID_W, GRID_H))
                if val == 'X':
                    pygame.draw.rect(screen, RED, (GRID_W*x, GRID_H*y, GRID_W, GRID_H))
