from visualize import *
import csv
import sys
from copy import copy

def random(grid):

    # Randomly place houses
    for i in range(grid.c):
        # Choose the type of house to randomly place
        choices = [j for j in range(len(grid.counts)) if grid.counts[j] > 0]
        r = np.random.choice(choices)
        grid.counts[r] -= 1
        type = grid.house_types[r]

        # Find locations where new house can be placed
        free_spots = grid.find_spot(type)

        xcoords, ycoords = np.where(free_spots == '.')
        if len(xcoords) == 0:
            print('NO SPACE LEFT AT', i, 'HOUSES!')
            #visualize_map(free_spots)
            break
        # Choose random coordinates for the new house
        r = np.random.randint(0, len(xcoords))
        x, y = xcoords[r], ycoords[r]
        # Place the house at the random coordinates
        grid.place_house(type, x, y)
    return grid.layout, grid.calculate_price()

def greedy(grid):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Greedily place houses
    for i in range(grid.c):
        # Choose the type of house to randomly place
        choices = [j for j in range(len(grid.counts)) if grid.counts[j] > 0]
        r = np.random.choice(choices)
        grid.counts[r] -= 1
        type = grid.house_types[r]

        # Find locations where new house can be placed
        free_spots = grid.find_spot(type)
        xcoords, ycoords = np.where(free_spots == '.')
        if len(xcoords) == 0:
            print('NO SPACE LEFT AT', i, 'HOUSES!')
            #visualize_map(free_spots)
            break
        # Choose random coordinates for the new house
        r = np.random.randint(0, len(xcoords))
        x, y = xcoords[r], ycoords[r]
        house = (type, x, y)
        current_score = grid.closest_house(house)
        new_score = float('inf')
        while current_score < new_score:
            if new_score != float('inf'):
                current_score = new_score
            for move in moves:
                (type, x, y) = house
                new_house = (type, x + move[0],  y + move[1])
                new_score = grid.closest_house(new_house)
                if new_score > current_score and free_spots[x + move[0],  y + move[1]] == '.':
                    house = new_house
                    break

        type, x, y = house
        grid.place_house(type, x, y)
    return grid.layout, grid.calculate_price()

def hillclimb(grid):
    # initialize the grid
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    greedy(grid)
    # move all houses with moves that maximize the score
    current_total_score = grid.calculate_price()
    new_total_score = float('inf')
    while current_total_score < new_total_score:
        if new_total_score != float('inf'):
            current_total_score = new_total_score
        for i in range(len(grid.houses)):
            house = grid.houses[i]
            (type, x, y) = house
            current_score = grid.closest_house(house)
            new_score = float('inf')
            grid.remove_house(i)
            free_spots = grid.find_spot(type)
            while current_score < new_score:
                if new_score != float('inf'):
                    current_score = new_score
                for move in moves:
                    (type, x, y) = house
                    new_house = (type, x + move[0],  y + move[1])
                    new_score = grid.closest_house(new_house)
                    if new_score > current_score and free_spots[x + move[0],  y + move[1]] == '.':
                        house = new_house
                        break

            type, x, y = house
            new_total_score = grid.calculate_price()
            grid.place_house(type, x, y, i)
    return grid.layout, grid.calculate_price()
