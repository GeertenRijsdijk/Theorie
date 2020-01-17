from algorithms import *
from grid_class import *
from simann import *
filename = './wijken/wijk_2.csv'
rl = []
gl = []
hl = []
sl = []

c = 40
n_iteration = 100
grid = Grid(filename, c)
counts = [int(c * 0.6), int(c * 0.25), int(c * 0.15)]
counts[0] += c - sum(counts)

print('Starting')
for i in range(n_iteration):
    print('ITERATION', i, c, 'HOUSES')
    _, price = random(grid)
    grid.reset()
    rl.append(price)
    _, price = greedy(grid)
    grid.reset()
    gl.append(price)
    _, price = hillclimb(grid)
    grid.reset()
    hl.append(price)
    _, price = simann(grid)
    grid.reset()
    sl.append(price)

print('AVG VALUE WITH RANDOM:     ', np.mean(rl))
print('MAX VALUE WITH RANDOM:     ', np.max(rl))
print('AVG VALUE WITH GREEDY:     ', np.mean(gl))
print('MAX VALUE WITH GREEDY:     ', np.max(gl))
print('AVG VALUE WITH HILLCLIMBER:', np.mean(hl))
print('MAX VALUE WITH HILLCLIMBER:', np.max(hl))
print('AVG VALUE WITH SIMANN:     ', np.mean(sl))
print('MAX VALUE WITH SIMANN:     ', np.max(sl))
