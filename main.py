# python -m cProfile -o output main.py wijken/wijk_1.csv 60 h

# import pstats
# p = pstats.Stats('output')
# p.sort_stats('cumulative').print_stats(50)

from visualize import *
from grid_class import *

# exit if incorrect number of arguments
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
   sys.exit

if sys.argv[3] == 'r':
    grid = Grid(filename, c)
    print(random(grid))
if sys.argv[3] == 'g':
    grid = Grid(filename, c)
    print(greedy(grid))
if sys.argv[3] == 'h':
    grid = Grid(filename, c)
    print(hillclimb(grid))
