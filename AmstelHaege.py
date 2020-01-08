import numpy as np
import csv
import sys
from copy import copy
from visualize import *

house_info = {
    #'name':(width, height, extra space)
    'EENGEZINSWONING':(8,8,2),
    'BUNGALOW':(11,7,3),
    'MAISON':(12,10,6)
}

def place_house(layout, type, x, y):
    w, h, ex = house_info[type]

    layout[x:x+w, y:y+h] = type[0]
    houses.append((type, x, y))

def find_spot(layout, houses, type):
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
            x1 = max(x1, 0)
            x2 = max(x2, 0)
            y1 = max(y1, 0)
            y2 = max(y2, 0)
            spots[x1:x2, y1:y2] = np.where(spots[x1:x2, y1:y2] == '.', 'X', spots[x1:x2, y1:y2])

    return spots

layout = np.full([160,180],'.')
print('Argument List:', str(sys.argv))
with open('./wijken/wijk_3.csv', newline='') as csvfile:
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
houses = []

for i in range(60):
    free_spots = find_spot(layout, houses, 'EENGEZINSWONING')
    xcoords, ycoords = np.where(free_spots == '.')
    if len(xcoords) == 0:
        print('NO SPACE LEFT AT', i, 'HOUSES!')
        visualize_map(free_spots)
        break
    r = np.random.randint(0, len(xcoords))
    x, y = xcoords[r], ycoords[r]
    place_house(layout, 'EENGEZINSWONING', x, y)

free_spots = find_spot(layout, houses, 'EENGEZINSWONING')
visualize_map(free_spots)



# struture, bottom_left_xy, top_right_xy, type
# water_1, "0,0", "32,180", WATER
