from algorithms import *
from copy import deepcopy as d
filename = './wijken/wijk_1.csv'
rl = []
gl = []
hl = []

c = 20
layout = load_map(filename)
counts = [int(c * 0.6), int(c * 0.25), int(c * 0.15)]
counts[0] += c - sum(counts)

print('Starting')
for i in range(20):
    print('ITERATION', i)
    houses *= 0
    rl.append(calculate_price(random(d(layout), c, d(counts))))
    houses *= 0
    gl.append(calculate_price(greedy(d(layout), c, d(counts))))
    houses *= 0
    hl.append(calculate_price(hillclimb(d(layout), c, d(counts))))

print('AVG VALUE WITH RANDOM:     ', np.mean(rl))
print('AVG VALUE WITH GREEDY:     ', np.mean(gl))
print('AVG VALUE WITH HILLCLIMBER:', np.mean(hl))
