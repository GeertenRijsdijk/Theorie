import numpy as np
import csv

from code.visualize import *
from code.classes.grid_class import *
from code.algorithms.random import *
from code.algorithms.greedy import *
from code.algorithms.hillclimber import *
from code.algorithms.simann import *
from output import *
import sys
import random

def swap(grid):
    # initialize the grid
    greedy2(grid)
    # swap houses if improves score
    current_total_score = grid.calculate_price()
    new_total_score = float('inf')
    while current_total_score < new_total_score:
        if new_total_score != float('inf'):
            current_total_score = new_total_score
        for i in range(1000):
            # select two random houses of different kind
            random_house1 = ["type", "x", "y"]
            random_house2 = ["type", "x", "y"]
            # repeat if they are of the same type
            while random_house1[0] == random_house2[0]:
                random_house1 = random.choice(grid.houses)
                random_house2 = random.choice(grid.houses)

            # try new random houses if cannot be swapped
            while grid.validate_swap(random_house1, random_house2) == False:
                random_house1 = ["type", "x", "y"]
                random_house2 = ["type", "x", "y"]
                while random_house1[0] == random_house2[0]:
                    random_house1 = random.choice(grid.houses)
                    random_house2 = random.choice(grid.houses)

            # calculate score current grid
            current_score = grid.calculate_price()

            # swap houses in the houses list with tuples
            temp_list = copy(grid.houses)
            houses_list = [list(elem) for elem in grid.houses]
            index_h1 = grid.houses.index(random_house1)
            index_h2 = grid.houses.index(random_house2)
            houses_list[index_h1][1] = random_house2[1]
            houses_list[index_h1][2] = random_house2[2]
            houses_list[index_h2][1] = random_house1[1]
            houses_list[index_h2][2] = random_house1[2]
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

            # if score not better reset, else swap houses
            if new_score <= current_score:
                print("dont swap")
            else:
                new_total_score = new_score

                type_1, x_1, y_1 = grid.houses[index_h1]
                type_2, x_2, y_2 = grid.houses[index_h2]

                # swap the houses
                grid.remove_house(index_h1)
                grid.place_house(type_2, x_1 , y_1, index_h1)
                grid.remove_house(index_h2)
                grid.place_house(type_1, x_2 , y_2, index_h2)

        return grid.layout, grid.calculate_price()

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
        print("in water")
        return False
    # other house too close
    if 'M' in required_space or 'B' in required_space or 'E' in required_space:
        print("house to close")
        return False

    # check swap other direction
    required_space = copy(self.layout)
    required_space = required_space[h1_y - h2_ex1:h1_y + h2_w + h2_ex1, h1_x - h2_ex1:h1_x + h2_h + h2_ex1]
    required_space_w = copy(self.layout)
    required_space_w = required_space_w[h1_y:h1_y + h2_w, h1_x:h1_x + h2_h]
    required_space[h2_ex1: h2_ex1 + h1_h,h2_ex1: h2_ex1 + h1_w ] = '.'

    if 'W' in required_space_w:
        print("in water")
        return False
    if 'M' in required_space or 'B' in required_space or 'E' in required_space:
        print("house to close")
        return False

    print("can be swapped")
    return True
