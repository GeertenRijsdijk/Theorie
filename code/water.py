'''
water.py

Authors:
- Wisse Bemelman
- Michael de Jong
- Geerten Rijsdijk

This file contains a function to add random water to a grid from the grid class.
It places between 1 and 4 water blocks of a random size.
'''
import numpy as np

# Checks if the water blocks intersect
def water_intersects(grid,x1,y1,x2,y2):
    if 'W' in grid.layout[x1:x2,y1:y2]:
        return True
    return False

# Places random amount of water that is 20% of the total surface
def random_water(grid):
    # Between 1 and 4 waters
    waters = np.random.randint(1,5)
    for water in range(waters):
        w, h = grid.layout.shape
        amount = int((0.2/waters)*w*h)
        # Check if width / height ratio is correct
        width = np.random.randint((0.25*amount)**0.5, ((4*amount)**0.5)+1)
        height = int(amount / width)
        x = np.random.randint(0, w - width+1)
        y = np.random.randint(0, h - height+1)
        # Add random fitting water
        while water_intersects(grid, x, y, x+width, y+height) == True:
            x = np.random.randint(0, w - width+1)
            y = np.random.randint(0, h - height+1)
        grid.waters.append((x, y, x+width, y+height))
        grid.layout[x:x+width, y:y+height].fill('W')
