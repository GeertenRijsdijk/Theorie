from visualize import *
from algorithms import *
import csv
import sys
from copy import copy

def probability_function(old_score, new_score):
    return np.exp((old_score - new_score) / old_score)

# NO SWAP
def simann(grid, N):
    # initialize the grid
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    greedy(grid)
    # move all houses with moves that maximize the score
    current_total_score = grid.calculate_price()
    new_total_score = float('inf')
    for i in range(N):
        rnd_index = np.random.randint(0, len(grid.houses))
        house = grid.houses[rnd_index] # random house
        (type, x, y) = house
        current_score = grid.calculate_price()
        new_score = float('inf')
        grid.remove_house(rnd_index)
        free_spots = grid.find_spot(type)
        while current_score < new_score:
            if new_score != float('inf'):
                current_score = new_score
            # random move
            random_move = moves[np.random.randint(0, len(moves))] # random move
            (type, x, y) = house
            newx = x + random_move[0]
            newy = y + random_move[1]
            new_house = (type, newx, newy)
            grid.place_house(type, newx,  newy, rnd_index)
            new_score = grid.calculate_price()
            if new_score > current_score and free_spots[newx,  newy] == '.':
                house = new_house
            elif new_score < current_score:
                p = probability_function(current_score, new_score)
                r = np.random.uniform(0,1)
                if r < p:
                    house = new_house

            type, x, y = house
            grid.place_house(type, x, y, rnd_index)
            new_total_score = grid.calculate_price()
    return grid.layout, grid.calculate_price()
