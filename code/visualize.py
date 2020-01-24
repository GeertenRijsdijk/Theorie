'''
visualize.py

Authors:
- Wisse Bemelman
- Michael de Jong
- Geerten Rijsdijk

This file contains a function to visualize the layout of the grid and the price,
as well as two functions that creates a histograms of results in a csv file.
'''

import numpy as np
import pygame
from copy import copy
import csv
import matplotlib.pyplot as plt
from collections import Counter

# Variables for the grid and colors
GRID_W, GRID_H = 3, 3

WIDTH, HEIGHT = (GRID_W*160, GRID_H*180)
WIDTH_PLUS = WIDTH + 200
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (50, 50, 50)
BLUE = (0, 0, 255)
GREEN = (20, 255, 20)
BROWN = (160, 80, 20)
RED = (255,0,0)
MARBLE = (230, 230, 200)


# Function displays text on screen
def draw_text(surf, text, fontsize, x, y, pos = "left", color = BLACK):
    font = pygame.font.SysFont('Monospace', fontsize)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if pos == "left":
        text_rect.topleft = (x,y)
    elif pos == "right":
        text_rect.topright = (x,y)
    elif pos == "center":
        text_rect.center = (x,y)
    else:
        text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)
    return (text_rect.x, text_rect.y, text_rect.width, text_rect.height)

# draws a grid on the pygame window
def draw_grid(screen):
    for x in range(0, WIDTH, GRID_W):
        pygame.draw.line(screen, GREY, (x,0), (x,HEIGHT))
    for y in range(0, HEIGHT, GRID_H):
        pygame.draw.line(screen, GREY, (0,y), (WIDTH,y))

pygame.init()

# uses the matrix to print all water and houses on the screen
def visualize_map(grid):
    if isinstance(grid, np.ndarray):
        matrix = grid
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    else:
        matrix = grid.layout
        screen = pygame.display.set_mode((WIDTH_PLUS, HEIGHT))
    pygame.display.set_caption('AmstelHague')
    clock = pygame.time.Clock()

    # draw the houses on the screen
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (0,0,WIDTH,HEIGHT))
    pygame.draw.rect(screen, BLACK, (WIDTH, 0, WIDTH_PLUS - WIDTH, HEIGHT), 1)
    for x, row in enumerate(matrix):
        for y, val in enumerate(row):
            if val == 'W':
                pygame.draw.rect(screen, BLUE,
                    (GRID_W*x, GRID_H*y, GRID_W, GRID_H))
            if val == 'E':
                pygame.draw.rect(screen, BROWN,
                    (GRID_W*x, GRID_H*y, GRID_W, GRID_H))
            if val == 'B':
                pygame.draw.rect(screen, BLACK,
                    (GRID_W*x, GRID_H*y, GRID_W, GRID_H))
            if val in 'M':
                pygame.draw.rect(screen, MARBLE,
                    (GRID_W*x, GRID_H*y, GRID_W, GRID_H))
            if val == 'X':
                pygame.draw.rect(screen, RED,
                    (GRID_W*x, GRID_H*y, GRID_W, GRID_H))

    draw_grid(screen)

    # make the sidebar with information
    if not isinstance(grid, np.ndarray):
        draw_text(screen, 'FILENAME:', 18, WIDTH + 10, 10)
        draw_text(screen, grid.filename, 12, WIDTH + 30, 30)

        draw_text(screen, 'NUMBER OF HOUSES:', 18, WIDTH + 10, 70)
        draw_text(screen, str(len(grid.houses)), 18, WIDTH + 30, 90)

        draw_text(screen, 'PRICE:', 18, WIDTH + 10, 130)
        draw_text(screen, str(grid.calculate_price()), 18, WIDTH + 30, 150)

    pygame.display.flip()

    # main game loop for pygame
    in_loop = True
    while in_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                return
            # make a screenshot when you press the spacebar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    location = grid.filename
                    location = location.strip('.csv')
                    location = location.replace('/data','/results')
                    pygame.image.save(screen, '.' + location + '.png')

        clock.tick(60)

# plots a histogram with the values of the csv output files
def make_histogram(filename, n_houses, algorithm, ran = None):

    # read in the result csv files
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, quotechar='"', quoting=csv.QUOTE_ALL,
            skipinitialspace=True)
        val_list = []
        for obj in reader:
            if int(obj[0]) == n_houses and obj[1] == algorithm:
                val_list.append(float(obj[-1]))

        if val_list == []:
            return

        print(len(val_list), 'instances')
        print('MEAN:', np.mean(val_list))
        print('MAX:', np.max(val_list))

        # round the price values
        for i, v in enumerate(val_list):
            val = round(v, -5)/1000000
            val_list[i] = val

        print('MEAN2:', np.mean(val_list))
        print('MAX2:', np.max(val_list))

        # put the price values into bins and add them to the plot
        if ran:
            bins = [round(ran[0] + 0.1*i, 1)
                for i in range(int(10*(ran[1]-ran[0]+0.001))+1)]
            plt.hist(val_list, bins = bins, edgecolor = 'black',
                rwidth = 0.8, align = 'right')
        else:
            min_val = min(val_list)
            max_val = max(val_list)
            bins = [round(min_val + 0.1*i, 1)
                for i in range(int(10*(max_val-min_val+0.001))+1)]
            plt.hist(val_list, bins = bins, edgecolor = 'black',
                rwidth = 0.8, align = 'right')
        plt.xlabel('waarde van wijk')
        plt.ylabel('aantal keer')
        plt.show()

        return val_list

# As make_histogram but for multiple files.
def make_histogram2(filenames, n_houses, algorithms):
    ran = (23,31)
    val_lists = []
    if len(filenames) != len(algorithms):
        return
    for i in range(len(filenames)):
        # read in the result csv files
        with open(filenames[i], newline='') as csvfile:
            reader = csv.reader(csvfile, quotechar='"',
                quoting=csv.QUOTE_ALL, skipinitialspace=True)
            val_list = []
            for obj in reader:
                if int(obj[0]) == n_houses and obj[1] == algorithms[i]:
                    val_list.append(float(obj[-1]))

            if val_list == []:
                return

            print(len(val_list), 'instances')
            print('MEAN:', np.mean(val_list))
            print('MAX:', np.max(val_list))

            # round the price values
            for i, v in enumerate(val_list):
                val = round(v, -5)/1000000
                val_list[i] = val

            print('MEAN2:', np.mean(val_list))
            print('MAX2:', np.max(val_list))

            # put the price values into bins and add them to the plot
            bins = [round(ran[0] + 0.1*i, 1)
                for i in range(int(10*(ran[1]-ran[0]+0.001))+1)]
            plt.hist(val_list, bins = bins, edgecolor = 'black',
                rwidth = 0.8, align = 'right')

            val_lists.append(val_list)
    plt.xlabel('waarde van wijk')
    plt.ylabel('aantal keer')
    plt.show()
