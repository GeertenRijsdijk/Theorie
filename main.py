'''
main.py

Authors:
    - Wisse Bemelman
    - Michael de Jong
    - Geerten Rijsdijk

This file implements the front end for the algorithms and visualisation.
usage:
    python main.py <datafile> <amount of houses> <algorithm>
example:
    python main.py ./data/wijk_2.csv 60 r
The algorithm choices are located in the readme.
'''
from code.visualize import *
from code.classes.grid_class import *
from code.algorithms.random import *
from code.algorithms.greedy import *
from code.algorithms.hillclimber import *
from code.algorithms.simann import *
import sys
import matplotlib.pyplot as plt

# Exit if incorrect number of arguments
if len(sys.argv) != 4:
    print("Arguments need to be a path to a file, the amount "
     "of houses and the algorithm")
    sys.exit()
# Exit if not correct algorithm entered
if sys.argv[3] not in ['r', 'g', 'h','s']:
    print("Please enter valid algorith: Random = r, Greedy = g, Hillclimb = h, "
        "Simann = s")
    sys.exit()

# Let user enter parameters for simulated annealing
if sys.argv[3] == 's':
    temperature = input("Please enter temperature (for standard testing "
        "values: 10000000, press enter): ")
    cooling_rate = input("Please enter cooling rate (for standard testing "
        "values: 0.0001, press enter): ")
    stopT = input("Please enter stop temperature (for standard testing "
        "values: 0.01, press enter): ")
    swap_prob = input("Please enter swap probability (for standard testing "
        "values: 0.3, press enter): ")

    # Insert standard testing values if user presses enter, else str to int
    if temperature == '':
        temperature = 10000000
    else:
        temperature = int(temperature)
    if cooling_rate == '':
        cooling_rate = 0.0001
    else:
        cooling_rate = int(cooling_rate)
    if stopT == '':
        stopT = 0.01
    else:
        stopT = int(stopT)
    if swap_prob == '':
        swap_prob = 0.3
    else:
        swap_prob = int(swap_prob)

# Calculate the required amount of the different houses
filename = sys.argv[1]
c = int(sys.argv[2])

# Exit if non valid number of houses is entered
if c <= 0:
   print("Please enter non-negative number of houses")
   sys.exit

# Run correct algorithm
grid = Grid(filename, c)
if sys.argv[3] == 'r':
    random(grid)
if sys.argv[3] == 'g':
    greedy(grid)
if sys.argv[3] == 'h':
    price_list = hillclimb(grid)
if sys.argv[3] == 's':
    price_list = simann(grid,temperature, cooling_rate, stopT, swap_prob)

print(grid.calculate_price())

if sys.argv[3] in ['h', 's']:
    plt.plot(price_list)
    plt.ylabel('iteration')
    plt.ylabel('value')
    plt.show()
visualize_map(grid)
