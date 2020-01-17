import numpy as np
from copy import copy, deepcopy
import csv
from code.visualize import *
from code.classes.grid_class import *
from code.algorithms.random import *
from code.algorithms.greedy import *
from code.algorithms.hillclimber import *
from code.algorithms.simann import *
import sys
filename = './data/empty.csv'
c=20
grid = Grid(filename, c)
counts = [int(c * 0.6), int(c * 0.25), int(c * 0.15)]
counts[0] += c - sum(counts)

_, price = random(grid)
print(price)
visualize_map(grid.layout)
