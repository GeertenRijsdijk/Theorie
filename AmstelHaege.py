import numpy as np
import csv
from copy import copy

house_info = {
    #'name':(width, height, extra space)
    'EENGEZINSWONING':(8,8,2),
    'BUNGALOW':(11,7,3),
    'MAISON':(12, 10,6)
}

def place_house(layout, type, x, y):
    w, h, ex = house_info[type]
    for i in range(ex+1):
        x1, x2 = x-(ex-i), x+w+(ex-i)
        y1, y2 = y-i, y+h+i
        layout[x1:x2, y1:y2] = np.where(layout[x1:x2, y1:y2] != 'W', 'X', 'W')

    layout[x:x+w, y:y+h] = type[0]
    houses.append((type, x, y))

def find_spot(layout, houses, type):
    spots = copy(layout)
    for house in houses:
        pass

with open('./wijken/wijk_1.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, quotechar='"', quoting=csv.QUOTE_ALL,
        skipinitialspace=True)
    T = []
    for row in reader:
        T.append(row)
layout = np.full([160, 180], '.')
houses = []

place_house(layout, 'EENGEZINSWONING', 4, 4)
print(layout[:16, :16])

# struture, bottom_left_xy, top_right_xy, type
# water_1, "0,0", "32,180", WATER
