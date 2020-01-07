import numpy as np
import csv

with open('./wijken/wijk_1.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, quotechar='"', quoting=csv.QUOTE_ALL,
        skipinitialspace=True)
    T = []
    for row in reader:
        T.append(row)
A = np.zeros([160,180])
print(T)
# structure, bottom_left_xy, top_right_xy, type
# water_1, "0,0", "32,180", WATER
