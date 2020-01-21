from copy import copy, deepcopy
import numpy as np
import csv

class Grid():
    def __init__(self, filename, c):
        self.filename = filename
        self.c = c
        # Create the correct distribution for houses
        self.counts = [int(self.c * 0.6), int(self.c * 0.25), int(self.c * 0.15)]

        # Add more EENGEZINSWONING if the counts do not sum to c
        self.counts[0] += self.c - sum(self.counts)

        self.houses = []
        self.house_types = ['EENGEZINSWONING', 'BUNGALOW', 'MAISON']
        self.waters = []

        self.house_info = {
            #'name':(width, height, extra space)
            'EENGEZINSWONING':(8,8,2,285000,0.03),
            'BUNGALOW':(11,7,3,399000,0.04),
            'MAISON':(12,10,6,610000,0.06)
        }

        self.house_cwh = np.zeros((self.c,4))
        self.house_cwh[:, :2] = np.inf

        self.layout_orig = self.load_map(self.filename)
        self.layout = deepcopy(self.layout_orig)

    def reset(self):
        self.houses = []
        self.layout = deepcopy(self.layout_orig)
        self.house_cwh = np.zeros((self.c,4))
        self.house_cwh[:, :2] = np.inf
        # Create the correct distribution for houses
        self.counts = [int(self.c * 0.6), int(self.c * 0.25), int(self.c * 0.15)]

        # Add more EENGEZINSWONING if the counts do not sum to c
        self.counts[0] += self.c - sum(self.counts)

    # read the input csv file
    def load_map(self, filename):
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
                    self.waters.append((x1, y1, x2, y2))
                    layout[x1:x2,y1:y2].fill('W')
        return layout

    def place_house(self, type, x, y, i = None):
        w, h, ex = self.house_info[type][0:3]
        self.layout[x:x+w, y:y+h] = type[0]
        if i == None:
            self.houses.append((type, x, y))
            self.house_cwh[len(self.houses)-1] = [x + w/2, y+h/2, w/2, h/2]
        else:
            self.houses.insert(i, (type, x, y))
            self.house_cwh[i] = [x + w/2, y+h/2, w/2, h/2]

    def remove_house(self, index):
        type, x, y = self.houses[index]
        w, h, _, _, _ = self.house_info[type]
        self.layout[x:x+w, y:y+h] = '.'
        self.house_cwh[index] = [np.inf, np.inf, 0, 0]
        return self.houses.pop(index)

    def find_spot(self, type):
        spots = copy(self.layout)
        layout_w, layout_h = self.layout.shape
        w, h, ex1, _, _ = self.house_info[type]

        spots[0:layout_w, 0:ex1] = np.where(spots[0:layout_w, 0:ex1] == '.', 'X', spots[0:layout_w, 0:ex1])
        spots[0:ex1, 0:layout_h] = np.where(spots[0:ex1, 0:layout_h] == '.', 'X', spots[0:ex1, 0:layout_h])
        spots[0:layout_w, layout_h-h-ex1:layout_h] = \
            np.where(spots[0:layout_w, layout_h-h-ex1:layout_h] == '.', 'X', spots[0:layout_w, layout_h-h-ex1:layout_h])
        spots[layout_w - w - ex1:layout_w, 0:layout_h] = \
            np.where(spots[layout_w - w - ex1:layout_w, 0:layout_h] == '.', 'X', spots[layout_w - w - ex1:layout_w, 0:layout_h])

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
                    spots[x1:x2, y1:y2] = np.where(spots[x1:x2, y1:y2] == '.', 'X', spots[x1:x2, y1:y2])
                else:
                    x1, x2 = x - w + 1 - i, x + w2 + i - 1
                    x1 = min(layout_w-1, max(x1, 0))
                    x2 = min(layout_w-1, max(x2, 0))
                    spots[x1, y1:y2] = np.where(spots[x1, y1:y2] == '.', 'X', spots[x1, y1:y2])
                    spots[x2, y1:y2] = np.where(spots[x2, y1:y2] == '.', 'X', spots[x2, y1:y2])

        for water in self.waters:
            wx1, wy1, wx2, wy2 = water
            wx1 = min(layout_w, max(wx1 - w, 0))
            wy1 = min(layout_h, max(wy1 - h, 0))
            spots[wx1:wx2, wy1:wy2] = \
                np.where(spots[wx1:wx2, wy1:wy2] == '.', 'X', spots[wx1:wx2, wy1:wy2])
        return spots

    def closest_house(self, house):
        if len(self.houses) == 0:
            return float("inf")

        type, x, y = house
        w, h, f, _, _ = self.house_info[type]

        centers = self.house_cwh[:, :2]
        wh = self.house_cwh[:, 2:]

        house_center = np.array([x + w/2, y + h/2])
        dists_xy = np.abs(centers - house_center) - wh - np.array([w/2, h/2])
        dists_xy = np.where(dists_xy < 0, 0, dists_xy)
        dists = dists_xy[:,0] + dists_xy[:,1]
        top2 = np.partition(dists, 1)[0:2]
        best = top2[0] if top2[0] > 0 else top2[1]
        return best - f

    # def calculate_price_2(self):
    #     totalprice = 0
    #     for house in self.houses:
    #         bp = self.house_info[house[0]][3]
    #         mp = 1 + self.closest_house(house) * self.house_info[house[0]][4]
    #         totalprice += bp * mp
    #     return totalprice

    def calculate_price(self):
        n = len(self.houses)
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
        base_prices = np.array([self.house_info[t][3] for t, _, _ in self.houses])
        price_incs = np.array([self.house_info[t][4] for t, _, _ in self.houses])
        prices = base_prices + base_prices * price_incs * min_dists

        return np.sum(prices)

    # Calculates the price of the layout, given that house i is moved a certain
    # distance
    def calculate_price_of_move(self, i, xmove, ymove):
        type, x, y = self.houses[i]

        centerx, centery = self.house_cwh[i, 0:2]
        self.house_cwh[i, 0:2] = np.array([np.inf, np.inf])

        if not self.can_place_house(type, x + xmove, y + ymove):
            self.house_cwh[i, 0:2] = np.array([centerx, centery])
            return 0

        self.houses[i] = (type, x + xmove, y + ymove)
        self.house_cwh[i, 0:2] = np.array([centerx + xmove, centery + ymove])

        price = self.calculate_price()

        self.houses[i] = (type, x, y)
        self.house_cwh[i, 0:2] -= np.array([xmove, ymove])
        return price

    def can_place_house(self, type, x, y):
        w, h, f, _, _ = self.house_info[type]
        x2, y2 = x + w, y + h

        if x - f < 0 or x2 + f > 160:
            return False
        if y - f < 0 or y2 + f > 180:
            return False

        for water in self.waters:
            wx, wy, wx2, wy2 = water
            if x < wx2 and x2 > wx and y < wy2 and y2 > wy:
                return False

        if len(self.houses) == 0:
            return True

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

    def validate_swap(self, type1, type2):
        # get info two random houses
        h1_type, h1_y, h1_x = type1[0], type1[1], type1[2]
        h2_type, h2_y, h2_x = type2[0], type2[1], type2[2]
        h1_w, h1_h, h1_ex1, _, _ = self.house_info[h1_type]
        h2_w, h2_h, h2_ex1, _, _= self.house_info[h2_type]
        print(h1_type, h1_w, h1_h, h2_type, h2_w, h2_h)

        # make matrix with required space
        required_space = copy(self.layout)
        required_space = required_space[h2_y - h1_ex1:h2_y + h1_w + h1_ex1, h2_x - h1_ex1:h2_x + h1_h + h1_ex1]
        required_space_w = copy(self.layout)
        required_space_w = required_space_w[h2_y:h2_y + h1_w, h2_x:h2_x + h1_h]
        required_space[h1_ex1: h1_ex1 + h2_h,h1_ex1: h1_ex1 + h2_w ] = '.'

        # house will be in the water
        if 'W' in required_space_w:
            return False
        # other house too close
        if 'M' in required_space or 'B' in required_space or 'E' in required_space:
            return False

        # check swap other direction
        required_space = copy(self.layout)
        required_space = required_space[h1_y - h2_ex1:h1_y + h2_w + h2_ex1, h1_x - h2_ex1:h1_x + h2_h + h2_ex1]
        required_space_w = copy(self.layout)
        required_space_w = required_space_w[h1_y:h1_y + h2_w, h1_x:h1_x + h2_h]
        required_space[h2_ex1: h2_ex1 + h1_h,h2_ex1: h2_ex1 + h1_w ] = '.'

        if 'W' in required_space_w:
            return False
        if 'M' in required_space or 'B' in required_space or 'E' in required_space:
            return False

        return True

    def swap(grid, house1, house2):
        # get info
        index_h1 = grid.houses.index(house1)
        index_h2 = grid.houses.index(house2)
        type_1, x_1, y_1 = grid.houses[index_h1]
        type_2, x_2, y_2 = grid.houses[index_h2]

        # swap the houses
        grid.remove_house(index_h1)
        grid.place_house(type_2, x_1 , y_1, index_h1)
        grid.remove_house(index_h2)
        grid.place_house(type_1, x_2 , y_2, index_h2)

    return grid.layout, grid.calculate_price()

    def swap_profitable(grid, house1, house2):
        # swap houses in the houses list with tuples
        temp_list = copy(grid.houses)
        houses_list = [list(elem) for elem in grid.houses]
        index_h1 = grid.houses.index(house1)
        index_h2 = grid.houses.index(house2)
        houses_list[index_h1][1] = house2[1]
        houses_list[index_h1][2] = house2[2]
        houses_list[index_h2][1] = house1[1]
        houses_list[index_h2][2] = house1[2]
        grid.houses = [tuple(l) for l in houses_list]

        # swap the houses in the centers matrix
        temp_matrix = copy(grid.house_cwh)
        grid.house_cwh[index_h1] = temp_matrix[index_h2]
        grid.house_cwh[index_h2] = temp_matrix[index_h1]

        # calculate new_score
        new_score = grid.calculate_price()

        # reset settings
        grid.houses = temp_list
        grid.house_cwh = temp_matrix

        return new_score
