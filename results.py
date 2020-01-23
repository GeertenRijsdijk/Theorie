from code.visualize import *
from code.classes.grid_class import *
from code.algorithms.random import *
from code.algorithms.greedy import *
from code.algorithms.hillclimber import *
from code.algorithms.simann import *
from code.output import *
import sys

# python -m cProfile -o output main.py

# import pstats
# p = pstats.Stats('output')
# p.sort_stats('cumulative').print_stats(10)

filename = './data/wijk_1.csv'
grid = Grid(filename, 40)

max_score = 0
for i in range(10):
    grid.reset()
    print('ITERATION', i)
    simann(grid,10000000,0.0001,0.01,0.3)
    price = grid.calculate_price()
    price > max_score
        max_score = price
        write_csv(grid, filename = 'wijk_1_40.csv')
    #write_outputcsv('strips_simann.csv', 60, 'simann_swap', grid.calculate_price())
