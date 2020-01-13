#from visualize import *
from functions import *
from global_vars import *

def random(layout, c, counts):
    house_cwh = np.zeros((c,4))
    house_cwh[:, :2] = np.inf
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
            #visualize_map(free_spots)
            break
        # Choose random coordinates for the new house
        r = np.random.randint(0, len(xcoords))
        x, y = xcoords[r], ycoords[r]
        # Place the house at the random coordinates
        layout, house_cwh = place_house(layout, house_cwh, type, x, y)
    return layout, house_cwh, calculate_price(layout, house_cwh)

def greedy(layout, c, counts):
    house_cwh = np.zeros((c,4))
    house_cwh[:, :2] = np.inf

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
            #visualize_map(free_spots)
            break
        # Choose random coordinates for the new house
        r = np.random.randint(0, len(xcoords))
        x, y = xcoords[r], ycoords[r]
        house = (type, x, y)
        current_score = closest_house(house, house_cwh)
        new_score = float('inf')
        while current_score < new_score:
            if new_score != float('inf'):
                current_score = new_score
            for move in moves:
                (type, x, y) = house
                new_house = (type, x + move[0],  y + move[1])
                new_score = closest_house(new_house, house_cwh)
                if new_score > current_score and free_spots[x + move[0],  y + move[1]] == '.':
                    house = new_house
                    break

        type, x, y = house
        layout, house_cwh = place_house(layout, house_cwh, type, x, y)
    return layout, house_cwh, calculate_price(layout, house_cwh)

def hillclimb(layout, c, counts):
    # initialize the grid
    layout, house_cwh, _ = greedy(layout, c, counts)

    # move all houses with moves that maximize the score
    current_total_score = calculate_price(layout, house_cwh)
    new_total_score = float('inf')
    while current_total_score < new_total_score:
        if new_total_score != float('inf'):
            current_total_score = new_total_score
        for i in range(len(houses)):
            house = houses[i]
            (type, x, y) = house
            current_score = closest_house(house, house_cwh)
            new_score = float('inf')
            layout, house = remove_house(layout, i)
            free_spots = find_spot(layout, type)
            while current_score < new_score:
                if new_score != float('inf'):
                    current_score = new_score
                for move in moves:
                    (type, x, y) = house
                    new_house = (type, x + move[0],  y + move[1])
                    new_score = closest_house(new_house, house_cwh)
                    if new_score > current_score and free_spots[x + move[0],  y + move[1]] == '.':
                        house = new_house
                        break
            type, x, y = house
            new_total_score = calculate_price(layout, house_cwh)
            layout, house_cwh = place_house(layout, house_cwh, type, x, y, i)
    return layout, house_cwh, new_total_score
