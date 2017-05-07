from bokeh.palettes import Inferno256

from helpers import *
from example_data import generateEventsForNode

def drawOnFigure(fig, source, heatdata, nodes, palette=hexPaletteToTuplePalette(Inferno256)):
    # Initialize properties
    BRUSH_SIZE = 25
    HEATMAP_RESOLUTION = (150, 20)

    # Initialize maps
    print "    Creating template for heatmap"
    template_base = createArrayOfSize(HEATMAP_RESOLUTION)
    brush = createBrushMesh(BRUSH_SIZE)

    image_data = {}

    # Populate source with data
    print "    Populating image source with instances of template_base"
    populateImagesSourceWithData(image_data, nodes, heatdata, template_base, brush, BRUSH_SIZE, HEATMAP_RESOLUTION)

    # Reformat data to image format
    for key in image_data:
        reformatHeatmap(image_data[key], HEATMAP_RESOLUTION, palette, 256.0)
        image_data[key] = [image_data[key]]

    image_data["image_empty"] = np.copy(template_base)
    reformatHeatmap(image_data["image_empty"], HEATMAP_RESOLUTION, palette, 256.0, 0)
    image_data["image_empty"] = [image_data["image_empty"]]

    # Default image is empty
    image_data["image"] = image_data['image_empty']
    source.data = image_data

    # Draw the heatmap
    fig.image_rgba(image="image", x=0, y=0, dw=1527, dh=207, source=source)


def populateImagesSourceWithData(image_data, nodes, data, template_base, brush, brush_size, heatmap_resolution):
    # Create holders for heatmaps
    print "    Reserving memory for heatmaps"
    for date in range(25, 32): #TODO No hardcoding!
        for h in range(24):
            image_path = "image_" + str(h + 1) + str(date)
            image_data[image_path] = np.copy(template_base)

    # Paint data to heatmaps
    print "    Painting data to heatmaps"
    for node in data:
        pos_x = nodes[node].pos_x
        pos_y = nodes[node].pos_y
        for date in data[node]:
            # Elem is a tuple
            for elem in data[node][date]:
                image_path = "image_" + str(elem[0]) + str(date.day)
                brush_offset = (int(pos_x / 1527.0 * heatmap_resolution[0]),
                                int((207 - pos_y) / 207.0 * heatmap_resolution[1]))
                applyBrush(image_data[image_path], brush, heatmap_resolution, brush_size, brush_offset, elem[1])


# Change heatmap data from float32 to [uint8]
def reformatHeatmap(array, size, palette, max_value, alpha=223):
    # Get highest value in the heatmap
    palette_size = len(palette)

    # NOTE! All heatmap values will be scaled down to palette size
    if max_value <= 0:
        scaling_value = 1.0
    else:
        scaling_value = (palette_size - 1) / max_value

    # Reformat heatmap data to an image format
    view = array.view(dtype=np.uint8).reshape((size[1], size[0], 4))
    for y in range(size[1]):
        for x in range(size[0]):
            color_index = array[y, x] * scaling_value
            color = palette[int(color_index)]
            view[y, x, 0] = color[0]
            view[y, x, 1] = color[1]
            view[y, x, 2] = color[2]
            view[y, x, 3] = color[3]


# Creates a template for events
def createBrushMesh(size):
    brush = np.empty((size, size), dtype=np.float32)

    half = (size - 1) / 2.0
    half2 = half ** 2
    for y in range(size):
        for x in range(size):
            # Calculate distance to center, normalized between 0 and 1
            dist = 1.0 - (((x - half) ** 2 + (y - half) ** 2)) / half2

            # Parse distance, drop negative ones
            if dist < 0:
                dist = 0
            else:
                dist = dist # Unlinear falloff, sharper edges

            # Set brush
            brush[x, y] = dist

    return (brush)


# Append array to another array with an offset
def applyBrush(base, brush, base_size, brush_size, offset, multiplier):
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
            if (base[y + offset[1], x + offset[0]] + brush[y, x] * multiplier > 256):
                base[y + offset[1], x + offset[0]] = 256
            else:
                base[y + offset[1], x + offset[0]] += brush[y, x] * multiplier