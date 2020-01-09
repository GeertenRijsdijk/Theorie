import numpy as np
import pygame
import random

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

def draw_grid(screen):
    for x in range(0, WIDTH, GRID_W):
        pygame.draw.line(screen, GREY, (x,0), (x,HEIGHT))
    for y in range(0, HEIGHT, GRID_H):
        pygame.draw.line(screen, GREY, (0,y), (WIDTH,y))

pygame.init()

def visualize_map(matrix):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
                    pygame.draw.rect(screen, BLUE, (GRID_W*x, GRID_H*y, GRID_W, GRID_H))
                if val in ['E', 'B']:
                    pygame.draw.rect(screen, BROWN, (GRID_W*x, GRID_H*y, GRID_W, GRID_H))
                if val in 'M':
                    pygame.draw.rect(screen, MARBLE, (GRID_W*x, GRID_H*y, GRID_W, GRID_H))
                if val == 'X':
                    pygame.draw.rect(screen, RED, (GRID_W*x, GRID_H*y, GRID_W, GRID_H))

        draw_grid(screen)
        pygame.display.flip()
        clock.tick(10)
