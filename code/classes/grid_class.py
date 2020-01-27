'''
grid_class.py

Authors:
- Wisse Bemelman
- Michael de Jong
- Geerten Rijsdijk

This file implements a class which represents the entire problem. The class
contains representations of the state of the problem as well as functions to
place/remove houses, calculate the price of the grid, swap houses and more.
'''
from copy import copy, deepcopy
import numpy as np
import csv

class Grid():
    def __init__(self, filename, c):
        """
        Function to initialize attributes of the class
        """
        self.filename = filename

        self.house_info = {
            #'name':(width, height, extra space)
            'EENGEZINSWONING':(8,8,2,285000,0.03),
            'BUNGALOW':(11,7,3,399000,0.04),
            'MAISON':(12,10,6,610000,0.06)
        }

        self.house_types = ['EENGEZINSWONING', 'BUNGALOW', 'MAISON']
        self.houses = []
        self.waters = []

        # Set number of houses. If None, reads c in from filename.
        if c:
            self.c = c
        else:
            self.c = self.count_houses(filename)

        # Create the correct distribution for houses
        self.counts = [int(self.c*0.6), int(self.c*0.25), int(self.c*0.15)]

        # Add more EENGEZINSWONING if the counts do not sum to c
        self.counts[0] += self.c - sum(self.counts)

        self.house_cwh = np.zeros((self.c,4))
        self.house_cwh[:, :2] = np.inf

        self.layout_orig = self.load_map(self.filename)
        self.layout = deepcopy(self.layout_orig)

    def reset(self):
        """
        Function to reset the grid
        """
        self.houses = []
        self.layout = deepcopy(self.layout_orig)
        self.house_cwh = np.zeros((self.c,4))
        self.house_cwh[:, :2] = np.inf

        # Create the correct distribution for houses
        self.counts = [int(self.c*0.6), int(self.c*0.25), int(self.c*0.15)]

        # Add more EENGEZINSWONING if the counts do not sum to c
        self.counts[0] += self.c - sum(self.counts)

    def count_houses(self, filename):
        """
        Function to count the houses, returns the number of houses
        """
        n_houses = 0
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, quotechar='"', quoting=csv.QUOTE_ALL,
                skipinitialspace=True)
            for obj in reader:
                if obj[-1] in self.house_types:
                    n_houses += 1
        return n_houses

    def load_map(self, filename):
        """
        Function to load the map
        """
        # Initialize the grid
        self.layout = np.full([160,180],'.')
        # Read the input csv file
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, quotechar='"', quoting=csv.QUOTE_ALL,
                skipinitialspace=True)
            # Add all water objects to the neighbourhood
            for obj in reader:
                if obj[-1] == 'WATER':
                    xy1 = str.split(obj[1],',')
                    xy2 = str.split(obj[2],',')
                    x1, y1 = int(xy1[0]), int(xy1[1])
                    x2, y2 = int(xy2[0]), int(xy2[1])
                    self.waters.append((x1, y1, x2, y2))
                    self.layout[x1:x2,y1:y2].fill('W')
                elif obj[-1] in self.house_types:
                    xy1 = str.split(obj[1],',')
                    xy2 = str.split(obj[2],',')
                    x, y = int(xy1[0]), int(xy2[1])
                    self.place_house(obj[-1], x, y)

        return self.layout

    def place_house(self, type, x, y, i = None):
        """
        Function to place existing or new house
        """
        # Place the house on the grid
        w, h, ex = self.house_info[type][0:3]
        self.layout[x:x+w, y:y+h] = type[0]
        # Add new house to house list and centers matrix
        if i == None:
            self.houses.append((type, x, y))
            self.house_cwh[len(self.houses)-1] = [x + w/2, y+h/2, w/2, h/2]
        # Insert existing house to house list and centers matrix
        else:
            self.houses.insert(i, (type, x, y))
            self.house_cwh[i] = [x + w/2, y+h/2, w/2, h/2]

    def remove_house(self, index):
        """
        Function to remove a house from the grid
        """
        # Get house info
        type, x, y = self.houses[index]
        w, h, _, _, _ = self.house_info[type]

        # Adjust grid, remove from house list and centers matrix
        self.layout[x:x+w, y:y+h] = '.'
        self.house_cwh[index] = [np.inf, np.inf, 0, 0]
        return self.houses.pop(index)

    def find_spot(self, type):
        """
        Function that returns the possible spots a certain house type can be
        placed
        """
        spots = copy(self.layout)
        layout_w, layout_h = self.layout.shape
        w, h, ex1, _, _ = self.house_info[type]

        # Ensure house not to close to borders of the map
        spots[0:layout_w, 0:ex1] = np.where(spots[0:layout_w, 0:ex1] == '.',\
         'X', spots[0:layout_w, 0:ex1])
        spots[0:ex1, 0:layout_h] = np.where(spots[0:ex1, 0:layout_h] == '.',\
         'X', spots[0:ex1, 0:layout_h])
        spots[0:layout_w, layout_h-h-ex1:layout_h] = \
            np.where(spots[0:layout_w, layout_h-h-ex1:layout_h] == '.', 'X',\
             spots[0:layout_w, layout_h-h-ex1:layout_h])
        spots[layout_w - w - ex1:layout_w, 0:layout_h] = \
            np.where(spots[layout_w - w - ex1:layout_w, 0:layout_h] == '.', \
            'X', spots[layout_w - w - ex1:layout_w, 0:layout_h])

        # Find spot considering other houses
        for i, house in enumerate(self.houses):
            type, x, y = house
            w2, h2, ex2, _, _ = self.house_info[type]
            ex = max(ex1, ex2) + 1
            for i in range(ex):
                y1, y2 = y - h - (ex - i), y + h2 + (ex-i)
                y1 = min(layout_h, max(y1, 0))
                y2 = min(layout_h, max(y2, 0))
                if i == 0:
                    x1, x2 = x - w + 1 - i, x + w2 + i
                    x1 = min(layout_w, max(x1, 0))
                    x2 = min(layout_w, max(x2, 0))
                    spots[x1:x2, y1:y2] = np.where(spots[x1:x2, y1:y2] == '.',\
                     'X', spots[x1:x2, y1:y2])
                else:
                    x1, x2 = x - w + 1 - i, x + w2 + i - 1
                    x1 = min(layout_w-1, max(x1, 0))
                    x2 = min(layout_w-1, max(x2, 0))
                    spots[x1, y1:y2] = np.where(spots[x1, y1:y2] == '.', \
                    'X', spots[x1, y1:y2])
                    spots[x2, y1:y2] = np.where(spots[x2, y1:y2] == '.', \
                    'X', spots[x2, y1:y2])

        # Find spot considering waters
        for water in self.waters:
            wx1, wy1, wx2, wy2 = water
            wx1 = min(layout_w, max(wx1 - w, 0))
            wy1 = min(layout_h, max(wy1 - h, 0))
            spots[wx1:wx2, wy1:wy2] = \
                np.where(spots[wx1:wx2, wy1:wy2] == '.', 'X', spots[wx1:wx2, wy1:wy2])
        return spots

    def closest_house(self, house):
        """
        Function that calculates the distance to the closest house
        """
        # Return if no houses placed yet
        if len(self.houses) == 0:
            return float("inf")

        # Get info on the house
        type, x, y = house
        w, h, f, _, _ = self.house_info[type]

        centers = self.house_cwh[:, :2]
        wh = self.house_cwh[:, 2:]

        # Calculate distance to closest center other house
        house_center = np.array([x + w/2, y + h/2])
        dists_xy = np.abs(centers - house_center) - wh - np.array([w/2, h/2])
        dists_xy = np.where(dists_xy < 0, 0, dists_xy)
        dists = dists_xy[:,0] + dists_xy[:,1]
        top2 = np.partition(dists, 1)[0:2]
        best = top2[0] if top2[0] > 0 else top2[1]

        # Return the actual distance between the houses
        return best - f

    def calculate_price(self):
        """
        Function that calculates the revenue the current layout generates
        """
        # Return if no houses placed yet
        n = len(self.houses)
        if n == 0:
            return 0
        # Create n x n matrices for X, Y, W, H
        X = np.tile(self.house_cwh[:n, 0], (n, 1))
        Y = np.tile(self.house_cwh[:n, 1], (n, 1))
        W = np.tile(self.house_cwh[:n, 2], (n, 1))
        H = np.tile(self.house_cwh[:n, 3], (n, 1))

        # Create n x n matrix of required space for houses
        f_list = [self.house_info[type][2] for type, _, _ in self.houses]
        F = np.tile(np.array(f_list), (n, 1))
        # Each row represents the distances for one house
        F = np.transpose(F)

        # Calculate distances in X and Y direction
        X = np.abs(X - np.transpose(X)) - W - np.transpose(W)
        Y = np.abs(Y - np.transpose(Y)) - H - np.transpose(H)

        # Set distances smaller than 0 to 0.
        X = np.where(X < 0, 0, X)
        Y = np.where(Y < 0, 0, Y)

        # Calculate distances between houses
        dists = X + Y - F
        # Ignore distances between house and itself
        np.fill_diagonal(dists, np.inf)
        min_dists = dists.min(1)

        # Calculate prices
        base_prices = np.array([self.house_info[t][3] \
            for t, _, _ in self.houses])
        price_incs = np.array([self.house_info[t][4] \
            for t, _, _ in self.houses])
        prices = base_prices + base_prices * price_incs * min_dists

        return np.sum(prices)

    def calculate_price_of_move(self, i, xmove, ymove):
        """
        Function that calculates the price of the layout, given that house i
        is moved a certain distance
        """
        # Get house info
        type, x, y = self.houses[i]
        centerx, centery = self.house_cwh[i, 0:2]
        self.house_cwh[i, 0:2] = np.array([np.inf, np.inf])

        # Return 0 if house can not be placed
        if not self.can_place_house(type, x + xmove, y + ymove):
            self.house_cwh[i, 0:2] = np.array([centerx, centery])
            return 0

        # Calculate new price after move
        self.houses[i] = (type, x + xmove, y + ymove)
        self.house_cwh[i, 0:2] = np.array([centerx + xmove, centery + ymove])
        price = self.calculate_price()

        # Reset
        self.houses[i] = (type, x, y)
        self.house_cwh[i, 0:2] -= np.array([xmove, ymove])
        return price

    def can_place_house(self, type, x, y):
        """
        Function that determines whether a house can be placed at a certain
        position
        """
        # Get house info
        w, h, f, _, _ = self.house_info[type]
        x2, y2 = x + w, y + h

        # Return false if too close to the border of the grid
        if x - f < 0 or x2 + f > 160:
            return False
        if y - f < 0 or y2 + f > 180:
            return False

        # Return false if in water
        for water in self.waters:
            wx, wy, wx2, wy2 = water
            if x < wx2 and x2 > wx and y < wy2 and y2 > wy:
                return False

        # Return true if no other houses placed yet
        if len(self.houses) == 0:
            return True

        # Return false if too close to other house, else return true
        centers = self.house_cwh[:, :2]
        wh = self.house_cwh[:, 2:]
        house_center = np.array([x + w/2, y + h/2])
        dists_xy = np.abs(centers - house_center) - wh - np.array([w/2, h/2])
        dists_xy = np.where(dists_xy < 0, 0, dists_xy)
        dists = dists_xy[:,0] + dists_xy[:,1]
        best = np.min(dists)
        best_index = np.argmin(dists)
        f2= self.house_info[self.houses[best_index][0]][2]
        if best - max(f, f2) < 0:
            return False
        return True

    def swap(self, house1, house2):
        """
        Function to swap the houses
        """
        # Get info
        index_h1 = self.houses.index(house1)
        index_h2 = self.houses.index(house2)
        type_1, x_1, y_1 = self.houses[index_h1]
        type_2, x_2, y_2 = self.houses[index_h2]

        # Swap the houses
        self.remove_house(index_h1)
        self.place_house(type_2, x_1 , y_1, index_h1)
        self.remove_house(index_h2)
        self.place_house(type_1, x_2 , y_2, index_h2)

        return

    def price_after_swap(self, house1, house2):
        """
        Function that calculates the price of the layout after the houses
        have swapped
        """
        # Swap houses in the houses list with tuples
        temp_list = copy(self.houses)
        houses_list = [list(elem) for elem in self.houses]
        index_h1 = self.houses.index(house1)
        index_h2 = self.houses.index(house2)
        houses_list[index_h1][1] = house2[1]
        houses_list[index_h1][2] = house2[2]
        houses_list[index_h2][1] = house1[1]
        houses_list[index_h2][2] = house1[2]
        self.houses = [tuple(l) for l in houses_list]

        temp_matrix = copy(self.house_cwh)

        # Swap the houses in the centers matrix
        h1x = houses_list[index_h1][1] + self.house_info[house1[0]][0]/2
        h1y = houses_list[index_h1][2] + self.house_info[house1[0]][1]/2
        h2x = houses_list[index_h2][1] + self.house_info[house2[0]][0]/2
        h2y = houses_list[index_h2][2] + self.house_info[house2[0]][1]/2
        self.house_cwh[index_h1, :2] = np.array([h1x, h1y])
        self.house_cwh[index_h2, :2] = np.array([h2x, h2y])

        ### CHECK WHETHER SWAP IS LEGAL

        # Get info two houses
        h1_type, h1_x, h1_y = house1
        h2_type, h2_x, h2_y = house2
        h1_w, h1_h, h1_ex1, _, _ = self.house_info[h1_type]
        h2_w, h2_h, h2_ex1, _, _= self.house_info[h2_type]

        # Calculate new_score
        new_score = self.calculate_price()

        # Check if enough vrijstand
        if self.closest_house(self.houses[index_h1]) < h1_ex1 or \
         self.closest_house(self.houses[index_h2]) < h2_ex1:
            new_score = 0

        # Check if required space is in the grid
        if h2_x - h1_ex1 < 0 or h2_y - h1_ex1 < 0 or h2_x + h1_w + h1_ex1 > 160\
            or h2_y + h1_h + h1_ex1 > 180:
            new_score = 0
        if h1_x - h2_ex1 < 0 or h1_y - h2_ex1 < 0 or h1_x + h2_w + h2_ex1 > 160\
            or h1_y + h2_h + h2_ex1 > 180:
            new_score = 0

        # Check if house will be in the water
        required_space_w = copy(self.layout)
        required_space_w = required_space_w[h2_x:h2_x + h1_w, h2_y:h2_y + h1_h]
        if 'W' in required_space_w:
            new_score = 0
        required_space_w = copy(self.layout)
        required_space_w = required_space_w[h1_x:h1_x + h2_w, h1_y:h1_y + h2_h]
        if 'W' in required_space_w:
            new_score = 0

        # Reset settings
        self.houses = temp_list
        self.house_cwh = temp_matrix

        return new_score
