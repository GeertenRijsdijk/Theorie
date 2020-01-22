import numpy as np
import csv
import sys
from copy import copy

def write_outputcsv(filename, num_houses, algorithm, revenue):
    # write to the output file
    with open(filename,'a', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow([num_houses, algorithm, revenue])

def write_csv(grid, filename = 'houses.csv'):
    # open new file
    with open(filename, 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['num','bottom_left', 'top_right', 'type'])

        for i, water in enumerate(grid.waters):
            str1 = str(water[0]) + "," + str(water[1])
            str2 = str(water[2]) + "," + str(water[3])
            csv_out.writerow(['water_' + str(i+1)] + [str1] + [str2] + ['WATER'])

        # initialize counters
        bungalow = 1
        eengezinswoning = 1
        maison = 1

        # rewrite tuple to correct format using a list
        for row in grid.houses:
            format = [0,0,0,0]
            if row[0] == "BUNGALOW":
                bottom_left = str([row[1], row[2] + 7])[1:-1]
                top_right = str([row[1] + 11, row[2]])[1:-1]
                format[0] = "bungalow_" + str(bungalow)
                format[1] = bottom_left
                format[2] = top_right
                format[3] = row[0]
                bungalow += 1
            elif row[0] == "EENGEZINSWONING":
                bottom_left = str([row[1], row[2] + 8])[1:-1]
                top_right = str([row[1] + 8, row[2]])[1:-1]
                format[0] = "eengezinswoning_" + str(eengezinswoning)
                format[1] = bottom_left
                format[2] = top_right
                format[3] = row[0]
                eengezinswoning += 1
            else:
                bottom_left = str([row[1], row[2] + 10])[1:-1]
                top_right = str([row[1] + 12, row[2]])[1:-1]
                format[0] = "maison_1" + str(maison)
                format[1] = bottom_left
                format[2] = top_right
                format[3] = row[0]
                maison += 1

            # write to csv file
            csv_out.writerow(format)

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
    return
