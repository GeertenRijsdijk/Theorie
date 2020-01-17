from greedy import *

def hillclimb(grid):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random(grid)
    # move all houses with moves that maximize the score
    current_total_score = grid.calculate_price()
    new_total_score = np.inf
    while current_total_score < new_total_score:
        if new_total_score != np.inf:
            current_total_score = new_total_score
        for i in range(len(grid.houses)):
            type, x, y = grid.houses[i]
            oldhouse = copy(grid.houses[i])
            current_score = current_total_score
            new_score = np.inf
            while current_score < new_score:
                type, x, y = grid.houses[i]
                if new_score != np.inf:
                    current_score = new_score
                for move in moves:
                    new_score = grid.calculate_price_of_move(i, move[0], move[1])
                    if new_score > current_score:
                        grid.remove_house(i)
                        grid.place_house(type, x + move[0], y + move[1], i)
                        break

            new_total_score = grid.calculate_price()
    return grid.layout, grid.calculate_price()
