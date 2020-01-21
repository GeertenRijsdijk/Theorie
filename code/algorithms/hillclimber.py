from .random import *
from .greedy import *

def hillclimb(grid):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    greedy(grid)

    # move all houses with moves that maximize the score
    current_total_score = grid.calculate_price()
    price_list = [current_total_score]
    new_total_score = np.inf
    while current_total_score < new_total_score:
        if new_total_score != np.inf:
            current_total_score = new_total_score
        for i in range(len(grid.houses)):
            type, x, y = grid.houses[i]
            current_score = grid.calculate_price()
            new_score = np.inf
            while current_score < new_score:
                type, x, y = grid.houses[i]
                if new_score != np.inf:
                    current_score = new_score
                    price_list.append(new_score)
                    #print(new_score)
                for move in moves:
                    new_score = grid.calculate_price_of_move(i, move[0], move[1])
                    if new_score > current_score:
                        grid.remove_house(i)
                        grid.place_house(type, x + move[0], y + move[1], i)
                        break

        new_total_score = current_score

    return price_list
