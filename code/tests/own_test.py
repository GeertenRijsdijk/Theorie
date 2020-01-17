from algorithms import *
from grid_class import *
from visualize import *
from code.algorithms import simann
filename = './wijken/empty.csv'
c=20
grid = Grid(filename, c)
counts = [int(c * 0.6), int(c * 0.25), int(c * 0.15)]
counts[0] += c - sum(counts)

_, price = randomi(grid)
print(price)
print(grid.houses)
visualize_map(grid.layout)
