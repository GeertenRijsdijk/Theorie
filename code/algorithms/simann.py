'''
simann.py

Authors:
- Wisse Bemelman
- Michael de Jong
- Geerten Rijsdijk

This file implements the simulated annealing algorithm.

Parameters:
    - grid: the grid object
    - T: initial temperature
    - cooling_rate: amount the temperature decreases each iteration
    - stopT: the temperature at which the algorithm stops, if T is below it
    - swap_prob: the probability of swapping houses at an iteration

Returns:
    - price_list: a list containing prices per iteration, which can be plotted.
'''

from .random import *

# Function that swaps two houses
def swap(grid, index, score, T, price_list, type, x, y):
    # Find random swap
    ind = np.random.randint(0, len(grid.houses))
    house_1 = grid.houses[ind]
    rest_houses = [h for h in grid.houses if h[0] != house_1[0]]
    ind2 = np.random.randint(0, len(rest_houses))
    house_2 = rest_houses[ind2]

    new_score = grid.price_after_swap(house_1, house_2)

    # Continue only if the move is legal
    if new_score > 0:
        # Calculate probability of swapping
        p = probability_function(score, new_score, T)
        if p > np.random.uniform(0,1):
            # Swap the houses
            #score = new_score
            price_list.append(score)
            grid.swap(house_1, house_2)
            return new_score
    return score

# Function that moves a house
def move(grid, index, score, T, price_list, type, x, y):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Choose a random move
    movex, movey = moves[np.random.randint(0,len(moves))]
    new_score = grid.calculate_price_of_move(index, movex, movey)

    # Continue only if the move is legal
    if new_score != 0:
        # Calculate probability of moving
        p = probability_function(score, new_score, T)
        if p > np.random.uniform(0,1):
            # Move the house
            # score = new_score
            price_list.append(score)
            grid.remove_house(index)
            grid.place_house(type, x + movex, y + movey, index)
            return new_score
    return score

# Function that calculates the probability of moving to a new state
def probability_function(old_score, new_score, T):
    if new_score > old_score:
        return 1
    else:
        return np.exp((new_score - old_score) / T)

# Simulated annealing algorithm with a chance to swap houses
# instead of moving them
def simann(grid, T=10000000, cooling_rate=0.003, stopT=0.1, swap_prob=0.1):

    # initialize a random start state
    random(grid)
    score = grid.calculate_price()
    price_list = [score]

    # Based on T do random moves that may be accepted
    while T > stopT:
        # Choose a random house
        index = np.random.randint(0,len(grid.houses))
        house = grid.houses[index]
        type, x, y = house

        # Choose whether to move or swap based on swap_prob
        if swap_prob > np.random.uniform(0,1):
            score = swap(grid, index, score, T, price_list, type, x, y)
        else:
            score = move(grid, index, score, T, price_list, type, x, y)

        # Cooling rate update
        T *= 1 - cooling_rate

    return price_list
