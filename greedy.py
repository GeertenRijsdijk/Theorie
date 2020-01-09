from visualize import *
from functions import *

# argument handeling
if len(sys.argv) != 3:
    print('Arguments need to be a path to a file and the amount of houses')
    sys.exit()

# calculate the required amount of the different houses
filename = sys.argv[1]
c = int(sys.argv[2])

# Create the correct distribution for houses
counts = [int(c * 0.6), int(c * 0.25), int(c * 0.15)]
# Add more EENGEZINSWONING if the counts do not sum to c
counts[0] += c - sum(counts)

# Load the map
layout = load_map(filename)
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Greedily place houses
for i in range(c):
    # Choose the type of house to randomly place
    choices = [i for i in range(len(counts)) if counts[i] > 0]
    r = np.random.choice(choices)
    counts[r] -= 1
    type = house_types[i]

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
    print('STARTING', i)
    while current_score < new_score:
        if new_score != float('inf'):
            current_score = new_score
        for move in moves:
            (type, x, y) = house
            new_house = (type, x + move[0],  y + move[1])
            new_score = closest_house(new_house)
            print(house, new_house)
            print(current_score, new_score)
            if new_score > current_score:
                print('UPDATEE')
                house = new_house
                break

    type, x, y = house
    layout = place_house(layout, type, x, y)

free_spots = find_spot(layout, 'EENGEZINSWONING')
print(calculate_price(layout))
visualize_map(layout)
