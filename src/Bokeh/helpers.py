import numpy as np


# Creates an base for a custom image
def createArrayOfSize(size):
    heatmap = np.empty((size[1], size[0]), dtype=np.float32)

    for y in range(size[1]):
        for x in range(size[0]):    
            heatmap[y, x] = 0.0

    return (heatmap)


# Get max value from a heatmap
def getMaxValue(array, size):
    currently_highest = 0
    for y in range(size[1]):
        for x in range(size[0]):
            if array[y, x] > currently_highest:
                currently_highest = array[y, x]

    return currently_highest


# Convert hex palette to tuple palette
def hexPaletteToTuplePalette(palette):
    for i in range(len(palette)):
        palette[i] = _hexToDec(palette[i])


# Convert hexadecimal to RGB tuple
def _hexToDec(hex):
    hex_split = hex.strip('#')
    red   = ''.join(hex_split[0:2])
    green = ''.join(hex_split[2:4])
    blue  = ''.join(hex_split[4:6])
    return [int(red, 16), int(green, 16), int(blue,16), 255]