from bokeh.plotting import figure, output_file, ColumnDataSource, show
from bokeh.models import HoverTool
from bokeh.charts import HeatMap

import numpy as np

def makeHeatmap(nodes):
    output_file('heatmap.html')

    # Format node positions to plottable format
    node_ids = []
    x_coords = []
    y_coords = []
    for node in nodes:
        node_ids.append(node)
        x_coords.append(nodes[node].pos_x)
        y_coords.append(206 - nodes[node].pos_y)

    source = ColumnDataSource(data=dict(
        x=x_coords,
        y=y_coords,
        node=node_ids))

    # Load events
    events = []
    for node in nodes:
        n_events = nodes[node].all_readings['20160201':'20160230']
        for event in n_events:
            print event

    # Define plot
    p = figure(
        tools=['xpan', createHoverTool()],
        width=1638, height=626,
        x_range=(0,618), y_range=(0,206))

    # Draw image on background
    p.image_url(url=['map.png'], x=0, y=207, w=1527, h=207)

    # Draw circles where nodes are
    p.circle('x', 'y', source=source, size=25, color='red')

    # Define sizes
    brush_size = 21
    base_size = (150, 20)

    # Initialize maps
    base, base_view = createHeatmapBase(150, 20)
    brush, brush_view = createBrushMesh(21)

    applyBrush(base_view, brush_view, base_size, brush_size, (0, 0))
    applyBrush(base_view, brush_view, base_size, brush_size, (0, 19))

    # Stuffzies
    p.image_rgba(image=[base], x=0, y=0, dw=1527, dh=207)

    # Set borders
    p.min_border = 60

    show(p)

def applyBrush(base, brush, base_size, brush_size, offset):
    brush_half = (brush_size - 1) / 2
    offset = (offset[0] - brush_half, offset[1] - brush_half)
    
    for x in range(brush_size):
        for y in range(brush_size):
            # Skip coordinates that are outside the map
            if (x + offset[0] < 0 or x + offset[0] >= base_size[0] or
                y + offset[1] < 0 or y + offset[1] >= base_size[1]):
                continue

            # Append color
            base[y + offset[1], x + offset[0], 0] += brush[y, x, 0]
            base[y + offset[1], x + offset[0], 1] += brush[y, x, 1]
            base[y + offset[1], x + offset[0], 2] += brush[y, x, 2]

def createHeatmapBase(size_w, size_h):
    heatmap = np.empty((size_h, size_w), dtype=np.uint32)
    heatmap_view = heatmap.view(dtype=np.uint8).reshape((size_h, size_w, 4))

    for x in range(size_w):
        for y in range(size_h):
            heatmap_view[y, x, 0] = 0
            heatmap_view[y, x, 1] = 0
            heatmap_view[y, x, 2] = 0
            heatmap_view[y, x, 3] = 192

    return (heatmap, heatmap_view)

def createBrushMesh(size):
    brush = np.empty((size, size), dtype=np.uint32)
    brush_view = brush.view(dtype=np.uint8).reshape((size, size, 4))

    half = (size - 1) / 2.0
    half2 = half**2
    for x in range(size):
        for y in range(size):
            # Calculate distance
            dist = 1.0 - (((x - half)**2 + (y - half)**2)) / half2
            if dist < 0:
                dist = 0

            # Set brush
            brush_view[x, y, 0] = dist * 64
            brush_view[x, y, 1] = dist * 64
            brush_view[x, y, 2] = dist * 64
            brush_view[x, y, 3] = 0

    return (brush, brush_view)
            
def createHoverTool():
    return HoverTool(tooltips=[
        ('node', '@node'),
        ('location', '(@x, @y)')
        ])
