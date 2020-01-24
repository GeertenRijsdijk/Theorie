'''
greedy.py

Authors:
- Wisse Bemelman
- Michael de Jong
- Geerten Rijsdijk

This file implements the hillclimber algorithm, which places the houses randomly
and then moves them until a local optimum is reached.

Parameters:
    - grid: the grid object

Returns:
    - price_list: a list containing prices per iteration, which can be plotted.
'''

from .greedy import *

def hillclimb(grid):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Initialize a greedy layout
    greedy(grid)

    # move all houses with moves that maximize the score
    current_total_score = grid.calculate_price()
    price_list = [current_total_score]
    new_total_score = np.inf

    # Keep moving houses as long as this improves the score
    while current_total_score < new_total_score:
        if new_total_score != np.inf:
            current_total_score = new_total_score

        # Try to move each house
        for i in range(len(grid.houses)):
            type, x, y = grid.houses[i]
            current_score = grid.calculate_price()
            new_score = np.inf
            # Move house as long as this improves the score
            while current_score < new_score:
                type, x, y = grid.houses[i]
                if new_score != np.inf:
                    current_score = new_score
                    price_list.append(new_score)
                for move in moves:
                    new_score = \
                        grid.calculate_price_of_move(i, move[0], move[1])

                    # Update house if the move increased the score
                    if new_score > current_score:
                        grid.remove_house(i)
                        grid.place_house(type, x + move[0], y + move[1], i)
                        break

        new_total_score = current_score

    return price_list
