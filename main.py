#from visualize import *
from functions import *
from algorithms import *

# argument handeling
if len(sys.argv) != 4:
    print("Arguments need to be a path to a file, the amount of houses and the algorithm")
    sys.exit()

# exit if not correct algorithm entered
if sys.argv[3] not in ['r', 'g', 'h']:
    print("Please enter valid algorith: Random = r, Greedy = g, Hillclimb = h")
    sys.exit()

# calculate the required amount of the different houses
filename = sys.argv[1]
c = int(sys.argv[2])

# exit if non valid number of houses is entered
if c <= 0:
   print("Please enter non-negative number of houses")
   sys.exit()

# Create the correct distribution for houses
counts = [int(c * 0.6), int(c * 0.25), int(c * 0.15)]

# Add more EENGEZINSWONING if the counts do not sum to c
counts[0] += c - sum(counts)

# Load the map
layout = load_map(filename)

# run an algorithm
if sys.argv[3] == 'r':
    layout, house_cwh, price = random(layout, c, counts)
if sys.argv[3] == 'g':
    layout, house_cwh, price = greedy(layout, c, counts)
if sys.argv[3] == 'h':
    layout, house_cwh, price = hillclimb(layout, c, counts)
print(price)
