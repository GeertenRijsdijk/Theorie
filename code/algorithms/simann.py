'''
simann.py

Authors:
- Wisse Bemelman
- Michael de Jong
- Geerten Rijsdijk

This file implements the simulated annealing algorithm. The function contains
parameters for the temperature, cooling rate, stop temperature and swap
probability. The function returns a list of prices per iteration, which can
be plotted.
'''

from .random import *

def probability_function(old_score, new_score, T):
    if new_score > old_score:
        return 1
    else:
        return np.exp((new_score - old_score) / T)

# simulated annealing algorithm with NO SWAP
def simann(grid, T = 10000000, cooling_rate = 0.003, stopT=0.1, swap_prob = 0.1):
    # initialize the grid
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random(grid)
    score = grid.calculate_price()
    price_list = [score]
    # Based on T do random moves that may be accepted
    while T > stopT:
        index = np.random.randint(0,len(grid.houses))
        house = grid.houses[index]# random house
        type, x, y = house

        if swap_prob > np.random.uniform(0,1):
            #grid.price_after_swap(house1, house2):
            ind = np.random.randint(0, len(grid.houses))
            house_1 = grid.houses[ind]
            rest_houses = [h for h in grid.houses if h[0] != house_1[0]]
            ind2 = np.random.randint(0, len(rest_houses))
            house_2 = rest_houses[ind2]

            new_score = grid.price_after_swap(house_1, house_2)
            if new_score > 0:
                p = probability_function(score, new_score, T)
                if p > np.random.uniform(0,1):
                    score = new_score
                    price_list.append(score)
                    grid.swap(house_1, house_2)
        else:
            movex, movey = moves[np.random.randint(0,len(moves))] # do a random move
            new_score = grid.calculate_price_of_move(index, movex, movey)
            if new_score != 0:
                p = probability_function(score, new_score, T)
                # accept the score if it's larger than a random value between 0 and 1
                if p > np.random.uniform(0,1):
                    score = new_score
                    price_list.append(score)
                    grid.remove_house(index)
                    grid.place_house(type, x + movex, y + movey, index)
        T *= 1 - cooling_rate

    return price_list
