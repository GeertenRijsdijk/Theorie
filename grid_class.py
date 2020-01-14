# python -m cProfile -o output main.py wijken/wijk_1.csv 60 h

# import pstats
# p = pstats.Stats('output')
# p.sort_stats('cumulative').print_stats(50)

from visualize import *
from algorithms import *

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
        self.layout = self.layout_orig

    def reset(self):
        self.houses = []
        self.layout = self.layout_orig
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

        for house in self.houses:
            type, x, y = house
            w2, h2, ex2, _, _ = self.house_info[type]
            ex = max(ex1, ex2) + 1
            for i in range(ex):
                x1, x2 = x - w + 1 - i, x + w2 + i
                y1, y2 = y - h - (ex - i), y + h2 + (ex-i)
                x1 = min(layout_w, max(x1, 0))
                x2 = min(layout_w, max(x2, 0))
                y1 = min(layout_h, max(y1, 0))
                y2 = min(layout_h, max(y2, 0))
                spots[x1:x2, y1:y2] = np.where(spots[x1:x2, y1:y2] == '.', 'X', spots[x1:x2, y1:y2])

        for water in self.waters:
            wx1, wy1, wx2, wy2 = water
            wx1 = min(layout_w, max(wx1 - w, 0))
            wy1 = min(layout_h, max(wy1 - h, 0))
            spots[wx1:wx2, wy1:wy2] = \
                np.where(spots[wx1:wx2, wy1:wy2] == '.', 'X', spots[wx1:wx2, wy1:wy2])
        return spots

    def closest_house(self, house):
        type, x, y = house
        w, h, f, _, _ = self.house_info[type]

        centers = self.house_cwh[:, :2]
        wh = self.house_cwh[:, 2:]

        if len(self.houses) == 0:
            return float("inf")
        house_center = np.array([x + w/2, y + h/2])
        dists_xy = np.abs(centers - house_center) - wh - np.array([w/2, h/2])
        dists_xy = np.where(dists_xy < 0, 0, dists_xy)
        dists = dists_xy[:,0] + dists_xy[:,1]
        top2 = np.partition(dists, 1)[0:2]
        best = top2[0] if top2[0] > 0 else top2[1]
        return best - f

    def calculate_price(self):
        totalprice = 0
        for house in self.houses: # (type,x,y)
            baseprice = self.house_info[house[0]][3]
            multiplier = 1 + self.closest_house(house) * self.house_info[house[0]][4]
            totalprice += baseprice * multiplier
        return totalprice

    def write_csv(self):
        # open new file
        with open('houses.csv','w', newline='') as out:
            csv_out = csv.writer(out)
            csv_out.writerow(['num','bottom_left', 'top_right', 'type'])

            # initialize counters
            bungalow = 1
            eengezinswoning = 1
            maison = 1

            # rewrite tuple to correct format using a list
            for row in self.houses:
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
