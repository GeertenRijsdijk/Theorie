'''
visualize_csv.py

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
import sys
from code.visualize import *
from code.classes.grid_class import *

# exit if incorrect number of arguments
if len(sys.argv) != 2:
    print('Usage: visualize_csv.py <filepath>')
    quit()

filename = sys.argv[1]
grid = Grid(filename, 0)
visualize_map(grid)
