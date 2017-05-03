from bokeh.palettes import viridis

from helpers import *
from example_data import generateEventsForNode

def drawOnFigure(fig, source, nodes):
    # Initialize properties
    BRUSH_SIZE = 25
    HEATMAP_RESOLUTION = (150, 20)

    # Create palette
    print "Creating palette"
    palette = viridis(64)
    hexPaletteToTuplePalette(palette)

    # Initialize maps
    print "Creating template for heatmap"
    template_base = createArrayOfSize(HEATMAP_RESOLUTION)
    brush = createBrushMesh(BRUSH_SIZE)

    # Add empty image
    empty_image = np.copy(template_base)
    reformatHeatmap(empty_image, HEATMAP_RESOLUTION, palette, 0)
    source.data["image_empty"] = [empty_image]

    # Default image is empty
    source.data["image"] = source.data['image_empty']

    # Populate source with data
    print "Populating image source with instances of template_base"
    populateImageSource(source, nodes, template_base, brush, BRUSH_SIZE, HEATMAP_RESOLUTION, palette)

    # Draw the heatmap
    print "Drawing heatmap"
    fig.image_rgba(image="image", x=0, y=0, dw=1527, dh=207, source=source)


def populateImageSource(source, nodes, template_base, brush, brush_size, heatmap_resolution, palette):
    # Load events to source
    print "Loading node events"
    for d in range(7):
        for h in range(24):
            image_path = "image_" + str(h + 1) + str(d + 1)
            source.data[image_path] = createHeatmap(template_base, nodes, heatmap_resolution, brush, brush_size, palette)


def createHeatmap(template_base, nodes, heatmap_resolution, brush, brush_size, palette):
    heatmap = np.copy(template_base)

    for node in nodes:
        count = generateEventsForNode()  # nodes[node].get_measurement_count_by_time_window("2016-01-10 16:00:00","2016-01-10 23:59:59")
        if count > 0:
            brush_offset = (int(nodes[node].pos_x / 1527.0 * heatmap_resolution[0]),
                            int((207 - nodes[node].pos_y) / 207.0 * heatmap_resolution[1]))
            applyBrush(heatmap, brush, heatmap_resolution, brush_size, brush_offset, count)

    # Reformat data
    reformatHeatmap(heatmap, heatmap_resolution, palette)
    return [heatmap]


# Change heatmap data from float32 to [uint8]
def reformatHeatmap(array, size, palette, alpha=223):
    # Get highest value in the heatmap
    max_value = getMaxValue(array, size)
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
            color = palette[int(array[y, x] * scaling_value)]
            view[y, x, 0] = color[0]
            view[y, x, 1] = color[1]
            view[y, x, 2] = color[2]
            view[y, x, 3] = alpha


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
                dist = dist ** 3  # Unlinear falloff, sharper edges

            # Set brush
            brush[x, y] = dist * 6.0

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
            if (base[y + offset[1], x + offset[0]] + brush[y, x] * multiplier >= 1024):
                base[y + offset[1], x + offset[0]] = 255
            else:
                base[y + offset[1], x + offset[0]] += brush[y, x] * multiplier