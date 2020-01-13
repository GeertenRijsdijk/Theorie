import numpy as np
import sys
houses = []
house_types = ['EENGEZINSWONING', 'BUNGALOW', 'MAISON']
waters = []
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

house_info = {
    #'name':(width, height, extra space)
    'EENGEZINSWONING':(8,8,2,285000,0.03),
    'BUNGALOW':(11,7,3,399000,0.04),
    'MAISON':(12,10,6,610000,0.06)
}
