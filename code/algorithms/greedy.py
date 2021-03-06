'''
greedy.py

Authors:
- Wisse Bemelman
- Michael de Jong
- Geerten Rijsdijk

This file implements the greedy algorithm which places a house randomly onto
the grid, and then moves this as long as the move gives price gain, until
all houses are placed

Parameters:
    - grid: the grid object

Returns:
    - None
'''

import numpy as np

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

        # Print error if there is no space left
        if len(xcoords) == 0:
            print('NO SPACE LEFT AT', i, 'HOUSES!')
            quit()

        # Choose random coordinates for the new house
        r = np.random.randint(0, len(xcoords))
        x, y = xcoords[r], ycoords[r]
        house = (type, x, y)
        grid.place_house(type, x, y)
        current_score = grid.calculate_price()
        new_score = float('inf')

        # Move house as long as this improves the score
        while current_score < new_score:
            if new_score != float('inf'):
                current_score = new_score
            for move in moves:
                (type, x, y) = house
                new_house = (type, x + move[0],  y + move[1])
                new_score = grid.calculate_price_of_move(i, move[0], move[1])
                if new_score > current_score:
                    house = new_house
                    break
                else:
                    grid.remove_house(-1)
                    grid.place_house(type, x, y)

        type, x, y = house
    return
