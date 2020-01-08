import numpy as np
import csv
import sys
from copy import copy
from global_vars import *

# read the input csv file
def load_map(filename):
    # initialize the grid
    layout = np.full([160,180],'.')
    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.reader(csvfile, quotechar='"', quoting=csv.QUOTE_ALL,
            skipinitialspace=True)
        # add all water objects to the neighbourhood
        for obj in reader:
            if obj[-1] == 'WATER':
                xy1 = str.split(obj[1],',')
                xy2 = str.split(obj[2],',')
                x1, y1 = int(xy1[0]), int(xy1[1])
                x2, y2 = int(xy2[0]), int(xy2[1])
                waters.append((x1, y1, x2, y2))
                layout[x1:x2,y1:y2].fill('W')
    return layout

def place_house(layout, type, x, y):
    w, h, ex = house_info[type]

    layout[x:x+w, y:y+h] = type[0]
    houses.append((type, x, y))
    return layout

def find_spot(layout, type):
    spots = copy(layout)
    layout_w, layout_h = layout.shape
    w, h, ex1 = house_info[type]

    spots[0:layout_w, 0:ex1] = np.where(spots[0:layout_w, 0:ex1] == '.', 'X', spots[0:layout_w, 0:ex1])
    spots[0:ex1, 0:layout_h] = np.where(spots[0:ex1, 0:layout_h] == '.', 'X', spots[0:ex1, 0:layout_h])
    spots[0:layout_w, layout_h-h-ex1:layout_h] = \
        np.where(spots[0:layout_w, layout_h-h-ex1:layout_h] == '.', 'X', spots[0:layout_w, layout_h-h-ex1:layout_h])
    spots[layout_w - w - ex1:layout_w, 0:layout_h] = \
        np.where(spots[layout_w - w - ex1:layout_w, 0:layout_h] == '.', 'X',spots[layout_w - w - ex1:layout_w, 0:layout_h])

    for house in houses:
        type, x, y = house
        w2, h2, ex2 = house_info[type]
        ex = max(ex1, ex2) + 1
        for i in range(ex):
            x1, x2 = x - w + 1 - i, x + w2 + i
            y1, y2 = y - h - (ex - i), y + h2 + (ex-i)
            x1 = min(layout_w, max(x1, 0))
            x2 = min(layout_w, max(x2, 0))
            y1 = min(layout_h, max(y1, 0))
            y2 = min(layout_h, max(y2, 0))
            spots[x1:x2, y1:y2] = np.where(spots[x1:x2, y1:y2] == '.', 'X', spots[x1:x2, y1:y2])

    for water in waters:
        print(water)
        wx1, wy1, wx2, wy2 = water
        wx1 = min(layout_w, max(wx1 - w, 0))
        wy1 = min(layout_h, max(wy1 - h, 0))
        spots[wx1:wx2, wy1:wy2] = \
            np.where(spots[wx1:wx2, wy1:wy2] == '.', 'X', spots[wx1:wx2, wy1:wy2])

    return spots
