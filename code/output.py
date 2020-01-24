import numpy as np
import csv
import sys
from copy import copy

# Function to add a result to an output file
def write_outputcsv(filename, num_houses, algorithm, revenue):
    with open(filename,'a', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow([num_houses, algorithm, revenue])

# Function to write a grid to csv
def write_csv(grid, filename = 'houses.csv'):
    # open new file
    with open(filename, 'w', newline='') as out:
        csv_out = csv.writer(out)

        # Write the top row
        csv_out.writerow(['num','bottom_left', 'top_right', 'type'])

        # Write the waters
        for i, water in enumerate(grid.waters):
            str1 = str(water[0]) + "," + str(water[1])
            str2 = str(water[2]) + "," + str(water[3])
            csv_out.writerow(['water_' + str(i+1)]+[str1]+[str2]+['WATER'])

        # Initialize counters
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

            # Write house to csv file
            csv_out.writerow(format)
