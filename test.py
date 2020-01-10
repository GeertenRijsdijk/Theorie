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
    houses = []
    visualize_map(layout)
    rl.append(calculate_price(random(d(layout), c, d(counts))))
    visualize_map(layout)
    houses = []
    gl.append(calculate_price(greedy(d(layout), c, d(counts))))
    visualize_map(layout)
    houses = []
    hl.append(calculate_price(hillclimb(d(layout), c, d(counts))))
    print(len(houses))

print('ded')
print(np.mean(rl),np.mean(gl),np.mean(hl))
