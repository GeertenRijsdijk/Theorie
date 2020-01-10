from visualize import *
from functions import *
from global_vars import *

def random(layout, c, counts):
    # Randomly place houses
    for i in range(c):
        # Choose the type of house to randomly place
        choices = [j for j in range(len(counts)) if counts[j] > 0]
        r = np.random.choice(choices)
        counts[r] -= 1
        type = house_types[r]

        # Find locations where new house can be placed
        free_spots = find_spot(layout, type)
        xcoords, ycoords = np.where(free_spots == '.')
        if len(xcoords) == 0:
            print('NO SPACE LEFT AT', i, 'HOUSES!')
            visualize_map(free_spots)
            break
        # Choose random coordinates for the new house
        r = np.random.randint(0, len(xcoords))
        x, y = xcoords[r], ycoords[r]
        # Place the house at the random coordinates
        layout = place_house(layout, type, x, y)
    return layout

def greedy(layout, c, counts):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Greedily place houses
    for i in range(c):
        # Choose the type of house to randomly place
        choices = [j for j in range(len(counts)) if counts[j] > 0]
        r = np.random.choice(choices)
        counts[r] -= 1
        type = house_types[r]

        # Find locations where new house can be placed
        free_spots = find_spot(layout, type)
        xcoords, ycoords = np.where(free_spots == '.')
        if len(xcoords) == 0:
            print('NO SPACE LEFT AT', i, 'HOUSES!')
            visualize_map(free_spots)
            break
        # Choose random coordinates for the new house
        r = np.random.randint(0, len(xcoords))
        x, y = xcoords[r], ycoords[r]
        house = (type, x, y)
        current_score = closest_house(house)
        new_score = float('inf')
        while current_score < new_score:
            if new_score != float('inf'):
                current_score = new_score
            for move in moves:
                (type, x, y) = house
                new_house = (type, x + move[0],  y + move[1])
                new_score = closest_house(new_house)
                if new_score > current_score and free_spots[x + move[0],  y + move[1]] == '.':
                    house = new_house
                    break

        type, x, y = house
        layout = place_house(layout, type, x, y)
    return layout

def greedy2():
    pass
