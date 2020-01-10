from visualize import *
from functions import *
from algorithms import *

# argument handeling
if len(sys.argv) != 4:
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

# run an algorithm
if sys.argv[3] == 'r':
    layout = random(layout, c, counts)
if sys.argv[3] == 'g':
    layout = greedy(layout, c, counts)
if sys.argv[3] == 'h':
    layout = hillclimb(layout, c, counts)
print(calculate_price(layout))
visualize_map(layout)
