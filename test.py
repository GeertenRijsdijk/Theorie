from algorithms import *
from copy import deepcopy as d
filename = './wijken/wijk_1.csv'
rl = []
gl = []
hl = []

c = 60
n_iteration = 10
layout = load_map(filename)
counts = [int(c * 0.6), int(c * 0.25), int(c * 0.15)]
counts[0] += c - sum(counts)

print('Starting')
for i in range(n_iteration):
    print('ITERATION', i)
    houses *= 0
    _, _, price = random(d(layout), c, d(counts))
    rl.append(price)
    houses *= 0
    _, _, price = greedy(d(layout), c, d(counts))
    gl.append(price)
    houses *= 0
    _, _, price = hillclimb(d(layout), c, d(counts))
    hl.append(price)

print('AVG VALUE WITH RANDOM:     ', np.mean(rl))
print('MAX VALUE WITH RANDOM:     ', np.max(rl))
print('AVG VALUE WITH GREEDY:     ', np.mean(gl))
print('MAX VALUE WITH GREEDY:     ', np.max(gl))
print('AVG VALUE WITH HILLCLIMBER:', np.mean(hl))
print('MAX VALUE WITH HILLCLIMBER:', np.max(hl))
