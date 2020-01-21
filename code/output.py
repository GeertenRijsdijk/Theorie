import numpy as np
import csv
import sys
from copy import copy

def write_outputcsv(filename, num_houses, algorithm, revenue):
    # write to the output file
    with open(filename,'a', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow([num_houses, algorithm, revenue])

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

def random2(grid):
    # Randomly place houses
    for i in range(grid.c):
        # Place more valuable houses first
        if grid.counts[2] != 0:
            type = grid.house_types[2]
            grid.counts[2] -= 1
        elif grid.counts[1] != 0:
            type = grid.house_types[1]
            grid.counts[1] -= 1
        elif grid.counts[0] != 0:
            type = grid.house_types[0]

        # Find locations where new house can be placed
        free_spots = grid.find_spot(type)

        xcoords, ycoords = np.where(free_spots == '.')
        if len(xcoords) == 0:
            print('NO SPACE LEFT AT', i, 'HOUSES!')
            #visualize_map(free_spots)
            break
        # Choose random coordinates for the new house
        r = np.random.randint(0, len(xcoords))
        x, y = xcoords[r], ycoords[r]
        # Place the house at the random coordinates
        grid.place_house(type, x, y)
    return grid.layout, grid.calculate_price()

def greedy2(grid):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Greedily place houses
    for i in range(grid.c):
        # Place more valuable houses first
        if grid.counts[2] != 0:
            type = grid.house_types[2]
            grid.counts[2] -= 1
        elif grid.counts[1] != 0:
            type = grid.house_types[1]
            grid.counts[1] -= 1
        elif grid.counts[0] != 0:
            type = grid.house_types[0]

        # Find locations where new house can be placed
        free_spots = grid.find_spot(type)
        xcoords, ycoords = np.where(free_spots == '.')
        if len(xcoords) == 0:
            print('NO SPACE LEFT AT', i, 'HOUSES!')
            #visualize_map(free_spots)
            break
        # Choose random coordinates for the new house
        r = np.random.randint(0, len(xcoords))
        x, y = xcoords[r], ycoords[r]
        house = (type, x, y)
        current_score = grid.closest_house(house)
        new_score = float('inf')
        while current_score < new_score:
            if new_score != float('inf'):
                current_score = new_score
            for move in moves:
                (type, x, y) = house
                new_house = (type, x + move[0],  y + move[1])
                new_score = grid.closest_house(new_house)
                if new_score > current_score and free_spots[x + move[0],  y + move[1]] == '.':
                    house = new_house
                    break

        type, x, y = house
        grid.place_house(type, x, y)
    return grid.layout, grid.calculate_price()

def hillclimb2(grid):
    # initialize the grid
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    greedy2(grid)
    # move all houses with moves that maximize the score
    current_total_score = grid.calculate_price()
    new_total_score = float('inf')
    while current_total_score < new_total_score:
        if new_total_score != float('inf'):
            current_total_score = new_total_score
        for i in range(len(grid.houses)):
            house = grid.houses[i]
            (type, x, y) = house
            current_score = grid.closest_house(house)
            new_score = float('inf')
            grid.remove_house(i)
            free_spots = grid.find_spot(type)
            while current_score < new_score:
                if new_score != float('inf'):
                    current_score = new_score
                for move in moves:
                    (type, x, y) = house
                    new_house = (type, x + move[0],  y + move[1])
                    new_score = grid.closest_house(new_house)
                    if new_score > current_score and free_spots[x + move[0],  y + move[1]] == '.':
                        house = new_house
                        break

            type, x, y = house
            new_total_score = grid.calculate_price()
            grid.place_house(type, x, y, i)
    return grid.layout, grid.calculate_price()

def steep_hillclimb(grid):
    # initialize the grid
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    greedy(grid)
    # move all houses with moves that maximize the score
    current_total_score = grid.calculate_price()
    new_total_score = float('inf')
    while current_total_score < new_total_score:
        if new_total_score != float('inf'):
            current_total_score = new_total_score
        for i in range(len(grid.houses)):
            house = grid.houses[i]
            (type, x, y) = house
            current_score = grid.calculate_price()
            new_score = float('inf')
            grid.remove_house(i)
            free_spots = grid.find_spot(type)
            while current_score < new_score:
                if new_score != float('inf'):
                    current_score = new_score
                # consider all options, pick the best
                for move in moves:
                    (type, x, y) = house
                    new_house = (type, x + move[0],  y + move[1])
                    new_score = grid.calculate_price()
                    if new_score > current_score and free_spots[x + move[0],  y + move[1]] == '.':
                        current_score = new_score
                        house = new_house

            type, x, y = house
            new_total_score = grid.calculate_price()
            grid.place_house(type, x, y, i)
    return grid.layout, grid.calculate_price()

#move deze naar grid_class.py anders werkt hij niet
def validate_swap(self, type1, type2):
    # get info two random houses
    h1_type, h1_y, h1_x = type1[0], type1[1], type1[2]
    h2_type, h2_y, h2_x = type2[0], type2[1], type2[2]
    h1_w, h1_h, h1_ex1, _, _ = self.house_info[h1_type]
    h2_w, h2_h, h2_ex1, _, _= self.house_info[h2_type]
    print(h1_type, h2_type)

    # make matrix with required space
    required_space = self.layout[h2_y - h1_ex1:h2_y + h1_h + h1_ex1, h2_x - h1_ex1:h2_x + h1_w + h1_ex1].transpose()
    required_space_w = self.layout[h2_y:h2_y + h1_h , h2_x:h2_x + h1_w]
    print(required_space)
    required_space[h1_ex1: h1_ex1 + h2_h,h1_ex1: h1_ex1 + h2_w] = '.'

    # house will be in the water
    if 'W' in required_space_w:
        print("in water")
        return False
    # other house too close
    if 'M' in required_space or 'B' in required_space or 'E' in required_space:
        print("house to close")
        return False

    # return true can be placed
    print("can be swapped")
    return True

def swap(grid):
    # initialize the grid
    greedy2(grid)
    # swap houses if improves score
    current_total_score = grid.calculate_price()
    new_total_score = float('inf')
    while current_total_score < new_total_score:
        if new_total_score != float('inf'):
            current_total_score = new_total_score
        for i in range(10):
            # select two random houses of different kind
            while grid.validate_swap(random_house1, random_house2) == False:
                random_house1 = ["type", "x", "y"]
                random_house2 = ["type", "x", "y"]
                    # repeat if they are of the same type
                while random_house1[0] == random_house2[0]:
                    random_house1 = random.choice(grid.houses)
                    random_house2 = random.choice(grid.houses)

            ## hieronder nog niks veranderd
            print("SUCCES")
            house = grid.houses[i]
            current_score = grid.calculate_price()
            new_score = float('inf')
            grid.remove_house(i)

            while current_score < new_score:
                if new_score != float('inf'):
                    current_score = new_score
                # consider all options, pick the best
                for move in moves:
                    (type, x, y) = house
                    new_house = (type, x + move[0],  y + move[1])
                    new_score = grid.calculate_price()
                    if new_score > current_score and free_spots[x + move[0],  y + move[1]] == '.':
                        current_score = new_score
                        house = new_house

            type, x, y = house
            new_total_score = grid.calculate_price()
            grid.place_house(type, x, y, i)
