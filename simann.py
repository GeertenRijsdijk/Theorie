from visualize import *
from algorithms import *
import csv
import sys
from copy import copy

def probability_function(old_score, new_score, T):
    if new_score > old_score:
        return 1
    else:
        return np.exp((new_score - old_score) / T)

# simulated annealing algorithm with NO SWAP
def simann(grid):
    # initialize the grid
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random(grid)
    score = grid.calculate_price()
    # Based on T do random moves that may be accepted
    T = 10000000
    cooling_rate = 0.003
    while T > 1:
        index = np.random.randint(0,len(grid.houses))
        house = grid.houses[index]# random house
        type, x, y = house
        movex, movey = moves[np.random.randint(0,len(moves))] # do a random move
        new_score = grid.calculate_price_of_move(index, movex, movey)
        if new_score != 0:
            p = probability_function(score, new_score, T)
            # accept the score if it's larger than a random value between 0 and 1
            if p > np.random.uniform(0,1):
                score = new_score
                grid.remove_house(index)
                grid.place_house(type, x + movex, y + movey, index)
            T *= 1 - cooling_rate

    return grid.layout, grid.calculate_price()
