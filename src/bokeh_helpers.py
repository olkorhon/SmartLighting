import numpy as np

# Append array to another array with an offset
def applyBrush(base, brush, base_size, brush_size, offset):
    # Shift offset by half brush so it points to the center
    brush_half = (brush_size - 1) / 2
    offset = (offset[0] - brush_half, offset[1] - brush_half)

    # Append brush to image
    for x in range(brush_size):
        for y in range(brush_size):
            # Skip coordinates that are outside the map
            if (x + offset[0] < 0 or x + offset[0] >= base_size[0] or
                y + offset[1] < 0 or y + offset[1] >= base_size[1]):
                continue

            # Append color
            if (base[y + offset[1], x + offset[0]] + brush[y, x] >= 1024):
                base[y + offset[1], x + offset[0]] = 255
            else:
                base[y + offset[1], x + offset[0]] += brush[y, x]

# Creates an base for a custom image
def createHeatmapBase(size):
    heatmap = np.empty((size[1], size[0]), dtype=np.float32)

    for y in range(size[1]):
        for x in range(size[0]):    
            heatmap[y, x] = 0.0

    return (heatmap)

# Creates a template for events
def createBrushMesh(size):
    brush = np.empty((size, size), dtype=np.float32)

    half = (size - 1) / 2.0
    half2 = half**2
    for y in range(size):
        for x in range(size):
            # Calculate distance to center, normalized between 0 and 1
            dist = 1.0 - (((x - half)**2 + (y - half)**2)) / half2
            
            # Parse distance, drop negative ones
            if dist < 0:
                dist = 0
            else:
                dist = dist**3 # Unlinear falloff, sharper edges

            # Set brush
            brush[x, y] = dist * 6.0

    return (brush)

# Change heatmap data from float32 to uint8
def reformatHeatmap(array, size, palette):
    # Get highest value in the heatmap
    max_value = _getMaxValue(array, size)
    # NOTE! All heatmap values will be scaled to uint8, palette should be the same size
    if max_value <= 0:
        scaling_value = 1.0
    else:
        scaling_value = 255.0 / max_value  

    # Reformat heatmap data to an image format
    view = array.view(dtype=np.uint8).reshape((size[1], size[0], 4))
    for y in range(size[1]):
        for x in range(size[0]):
            color = palette[int(array[y, x] * scaling_value)]
            view[y, x, 0] = color[0]
            view[y, x, 1] = color[1]
            view[y, x, 2] = color[2]
            view[y, x, 3] = 223

# Get max value from a heatmap
def _getMaxValue(array, size):
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
    return (int(red, 16), int(green, 16), int(blue,16))
