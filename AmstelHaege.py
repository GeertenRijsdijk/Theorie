import numpy as np
import csv
import sys

layout = np.full([160,180],'')
print('Argument List:', str(sys.argv))
with open('./wijken/wijk_1.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, quotechar='"', quoting=csv.QUOTE_ALL,
        skipinitialspace=True)
    T = [] # add all water objects to the neighbourhood
    for obj in reader:
        if obj[-1] == 'WATER':
            xy1 = str.split(obj[1],',')
            xy2 = str.split(obj[2],',')
            x1, y1 = int(xy1[0]), int(xy1[1])
            x2, y2 = int(xy2[0]), int(xy2[1])
            layout[x1:x2,y1:y2].fill('W')
        T.append(obj)
print(layout)
# structure, bottom_left_xy, top_right_xy, type
# water_1, "0,0", "32,180", WATER
