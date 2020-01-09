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

free_spots = find_spot(layout, 'EENGEZINSWONING')
print(calculate_price(layout))
visualize_map(layout)
