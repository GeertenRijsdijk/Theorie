# python -m cProfile -o output main.py wijken/wijk_1.csv 60 h

# import pstats
# p = pstats.Stats('output')
# p.sort_stats('cumulative').print_stats(50)

from code.visualize import *
from code.classes.grid_class import *
from code.algorithms.random import *
from code.algorithms.greedy import *
from code.algorithms.hillclimber import *
from code.algorithms.simann import *
import sys
import matplotlib.pyplot as plt

# exit if incorrect number of arguments
if len(sys.argv) != 4:
    print("Arguments need to be a path to a file, the amount of houses and the algorithm")
    sys.exit()
# exit if not correct algorithm entered
if sys.argv[3] not in ['r', 'g', 'h','s']:
    print("Please enter valid algorith: Random = r, Greedy = g, Hillclimb = h, Simann = s")
    sys.exit()
# calculate the required amount of the different houses
filename = sys.argv[1]
c = int(sys.argv[2])

# exit if non valid number of houses is entered
if c <= 0:
   print("Please enter non-negative number of houses")
   sys.exit

grid = Grid(filename, c)
if sys.argv[3] == 'r':
    random(grid)
if sys.argv[3] == 'g':
    greedy(grid)
if sys.argv[3] == 'h':
    price_list = hillclimb(grid)
    plt.plot(price_list)
    plt.ylabel('iteration')
    plt.ylabel('value')
    plt.show()
if sys.argv[3] == 's':
    price_list = simann(grid)
    plt.plot(price_list)
    plt.ylabel('iteration')
    plt.ylabel('value')
    plt.show()
print(grid.calculate_price())
#visualize_map(grid.layout)
