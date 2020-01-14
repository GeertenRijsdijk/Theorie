import numpy as np
import csv
import sys
from copy import copy
from global_vars import *

# read the input csv file
def load_map(filename):
    # initialize the grid
    layout = np.full([160,180],'.')
    with open(filename, newline='') as csvfile:
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

def place_house(layout, house_cwh, type, x, y, i = None):
    w, h, ex = house_info[type][0:3]
    layout[x:x+w, y:y+h] = type[0]
    if i == None:
        houses.append((type, x, y))
        house_cwh[len(houses)-1] = [x + w/2, y+h/2, w/2, h/2]
    else:
        houses.insert(i, (type, x, y))
        house_cwh[i] = [x + w/2, y+h/2, w/2, h/2]

    return layout, house_cwh

def remove_house(layout, index):
    type, x, y = houses[index]
    w, h, _, _, _ = house_info[type]
    layout[x:x+w, y:y+h] = '.'
    return layout, houses.pop(index)

def find_spot(layout, type):
    spots = copy(layout)
    layout_w, layout_h = layout.shape
    w, h, ex1, _, _ = house_info[type]

    spots[0:layout_w, 0:ex1] = np.where(spots[0:layout_w, 0:ex1] == '.', 'X', spots[0:layout_w, 0:ex1])
    spots[0:ex1, 0:layout_h] = np.where(spots[0:ex1, 0:layout_h] == '.', 'X', spots[0:ex1, 0:layout_h])
    spots[0:layout_w, layout_h-h-ex1:layout_h] = \
        np.where(spots[0:layout_w, layout_h-h-ex1:layout_h] == '.', 'X', spots[0:layout_w, layout_h-h-ex1:layout_h])
    spots[layout_w - w - ex1:layout_w, 0:layout_h] = \
        np.where(spots[layout_w - w - ex1:layout_w, 0:layout_h] == '.', 'X', spots[layout_w - w - ex1:layout_w, 0:layout_h])

    for house in houses:
        type, x, y = house
        w2, h2, ex2, _, _ = house_info[type]
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
        wx1, wy1, wx2, wy2 = water
        wx1 = min(layout_w, max(wx1 - w, 0))
        wy1 = min(layout_h, max(wy1 - h, 0))
        spots[wx1:wx2, wy1:wy2] = \
            np.where(spots[wx1:wx2, wy1:wy2] == '.', 'X', spots[wx1:wx2, wy1:wy2])
    return spots

def closest_house(house, house_cwh):
    type, x, y = house
    w, h, f, _, _ = house_info[type]

    centers = house_cwh[:, :2]
    wh = house_cwh[:, 2:]

    if len(houses) == 0:
        return float("inf")
    house_center = np.array([x + w/2, y + h/2])
    dists_xy = np.abs(centers - house_center) - wh - np.array([w/2, h/2])
    dists_xy = np.where(dists_xy < 0, 0, dists_xy)
    dists = dists_xy[:,0] + dists_xy[:,1]
    top2 = np.partition(dists, 1)[0:2]
    best = top2[0] if top2[0] > 0 else top2[1]
    return best - f

def calculate_price(layout, house_cwh):
    totalprice = 0
    for house in houses: # (type,x,y)
        baseprice = house_info[house[0]][3]
        multiplier = 1 + closest_house(house, house_cwh) * house_info[house[0]][4]
        totalprice += baseprice * multiplier
    return totalprice

def write_csv(houses):
    # open new file
    with open('houses.csv','w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['num','bottom_left', 'top_right', 'type'])

        # initialize counters
        bungalow = 1
        eengezinswoning = 1
        maison = 1

        # rewrite tuple to correct format using a list
        for row in houses:
            format = [0,0,0,0]
            if row[0] == "BUNGALOW":
                bottom_left = str([row[1], row[2] - 7])[1:-1]
                top_right = str([row[1] + 11, row[2]])[1:-1]
                format[0] = "bungalow_" + str(bungalow)
                format[1] = bottom_left
                format[2] = top_right
                format[3] = row[0]
                bungalow += 1
            elif row[0] == "EENGEZINSWONING":
                bottom_left = str([row[1], row[2] - 8])[1:-1]
                top_right = str([row[1] + 8, row[2]])[1:-1]
                format[0] = "eengezinswoning_" + str(eengezinswoning)
                format[1] = bottom_left
                format[2] = top_right
                format[3] = row[0]
                eengezinswoning += 1
            else:
                bottom_left = str([row[1], row[2] - 10])[1:-1]
                top_right = str([row[1] + 12, row[2]])[1:-1]
                format[0] = "maison_1" + str(maison)
                format[1] = bottom_left
                format[2] = top_right
                format[3] = row[0]
                maison += 1

            # write to csv file
            csv_out.writerow(format)
