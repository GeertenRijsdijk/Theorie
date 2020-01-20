import numpy as np
import pygame
from copy import copy
import csv
import matplotlib.pyplot as plt
from collections import Counter

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
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('AmstelHague')
    clock = pygame.time.Clock()

    # main game loop for pygame
    in_loop = True
    while in_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                return

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

        draw_grid(screen)
        pygame.display.flip()
        clock.tick(60)

def make_histogram(filename, n_houses, algorithm):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, quotechar='"', quoting=csv.QUOTE_ALL,
            skipinitialspace=True)
        val_list = []
        for obj in reader:
            if int(obj[0]) == n_houses and obj[1] == algorithm:
                v = round(float(obj[-1]), -5)/1000000
                val_list.append(v)

        if val_list == []:
            return

        min_val = min(val_list)
        max_val = max(val_list)
        print(min_val, max_val)
        bins = [round(min_val + 0.1*i, 1) for i in range(int(10*(max_val-min_val))+2)]
        print(bins)
        plt.hist(val_list, bins = bins, rwidth = 0.008, histtype = 'stepfilled')
        plt.show()

        return val_list
