'''
results.py

Authors:
    - Wisse Bemelman
    - Michael de Jong
    - Geerten Rijsdijk

This file is used to test multiple iterations of an algorithm.
It saves the all the results to a csv file, and the best layout to a different
csv file.
usage:
    python results.py <datafile> <amount of houses> <algorithm> <n_iterations>
example:
    python results.py ./data/wijk_2.csv 60 r 100
The algorithm choices are located in the readme.
'''

from code.visualize import *
from code.classes.grid_class import *
from code.algorithms.random import *
from code.algorithms.greedy import *
from code.algorithms.hillclimber import *
from code.algorithms.simann import *
from code.output import *
import sys

# Exit if incorrect number of arguments
if len(sys.argv) != 5:
    print("Arguments need to be a path to a file, the amount of houses, \
        the algorithm and the number of iterations")
    sys.exit()
# Exit if not correct algorithm entered
if sys.argv[3] not in ['r', 'g', 'h','s']:
    print("Please enter valid algorith: Random = r, Greedy = g, Hillclimb = h \
        Simann = s")
    sys.exit()
# Calculate the required amount of the different houses
filename = sys.argv[1]
c = int(sys.argv[2])
n_iterations = int(sys.argv[4])

# Exit if non valid number of houses is entered
if c <= 0:
   print("Please enter non-negative number of houses")
   sys.exit

if n_iterations <= 1:
 print("Please enter a number of iterations larger than 1")
 sys.exit

algorithm = sys.argv[3]
grid = Grid(filename, c)

# Make the filename for the output file
fn = filename.replace('.csv', '') + '_' + str(c) + '_' + sys.argv[3]
fn = fn.replace('data', 'results')
print(fn)

try:
    g = Grid(fn + '_best.csv', c = None)
    max_score = g.calculate_price()
except:
    max_score = 0

for i in range(n_iterations):
    grid.reset()
    print('ITERATION', i)
    # Run correct algorithm
    if algorithm == 'r':
        random(grid)
    if algorithm == 'g':
        greedy(grid)
    if algorithm == 'h':
        hillclimb(grid)
    if algorithm == 's':
        simann(grid,10000000,0.0001,0.01,0.3)
    price = grid.calculate_price()
    if price > max_score:
        max_score = price
        write_csv(grid, fn + '_best.csv')
    write_outputcsv(fn + '.csv', c, algorithm, price)
    grid.reset()

g2 = Grid(fn + '_best.csv', c = None)
visualize_map(g2)
