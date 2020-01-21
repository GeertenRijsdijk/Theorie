import numpy as np

def water_intersects(grid,x1,y1,x2,y2):
    if 'W' in grid.layout[x1:x2,y1:y2]:
        return True
    return False

def random_water(grid):
    waters = np.random.randint(1,5) # between 1 and 4 waters
    for water in range(waters):
        w, h = grid.layout.shape
        amount = int((0.2/waters)*w*h)
        width = np.random.randint((0.25*amount)**0.5, ((4*amount)**0.5)+1)
        height = int(amount / width)
        x = np.random.randint(0, w - width+1)
        y = np.random.randint(0, h - height+1)
        # add random fitting water
        while water_intersects(grid, x, y, x+width, y+height) == True:
            x = np.random.randint(0, w - width+1)
            y = np.random.randint(0, h - height+1)
        grid.waters.append((x, y, x+width, y+height))
        grid.layout[x:x+width, y:y+height].fill('W')
