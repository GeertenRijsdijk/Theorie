'''
visualize_csv.py

Authors:
    - Wisse Bemelman
    - Michael de Jong
    - Geerten Rijsdijk

This file implements the visualisation of the result csvs.
usage:
    python main.py <filename>
example:
    python main.py results/wijk_1_20.csv

While the visualization is open, spacebar can be pressed to save the image
as a png.
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
