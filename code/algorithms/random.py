import numpy as np
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
    return
