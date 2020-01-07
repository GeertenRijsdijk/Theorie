import numpy as np
import csv
import sys
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

layout = np.full([160,180],'.')
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

houses = []

place_house(layout, 'EENGEZINSWONING', 4, 4)
print(layout[:16, :16])

# struture, bottom_left_xy, top_right_xy, type
# water_1, "0,0", "32,180", WATER
