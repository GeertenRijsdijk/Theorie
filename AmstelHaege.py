from visualize import *
from functions import *

# argument handeling
if len(sys.argv) != 3:
    print('Arguments need to be a path to a file and the amount of houses')
    sys.exit()

# calculate the required amount of the different houses
filename = sys.argv[1]
c = int(sys.argv[2])
counts = [int(c * 0.6), int(c * 0.25), int(c * 0.15)]

layout = load_map(filename)

for i in range(c):
    choices = [i for i in range(len(counts)) if counts[i] > 0]
    i = np.random.choice(choices)
    counts[i] -= 1
    type = house_types[i]

    free_spots = find_spot(layout, type)
    xcoords, ycoords = np.where(free_spots == '.')
    if len(xcoords) == 0:
        print('NO SPACE LEFT AT', i, 'HOUSES!')
        visualize_map(free_spots)
        break
    r = np.random.randint(0, len(xcoords))
    x, y = xcoords[r], ycoords[r]
    layout = place_house(layout, type, x, y)

free_spots = find_spot(layout, 'EENGEZINSWONING')
print(calculate_price(layout))
visualize_map(layout)
