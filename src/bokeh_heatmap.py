from bokeh.layouts import column
from bokeh.plotting import figure, output_file, ColumnDataSource, show
from bokeh.models import HoverTool, CustomJS, Slider
from bokeh.palettes import magma

import numpy as np
from bokeh_helpers import *

def makeHeatmap(nodes):
    print "Data received"

    output_file('heatmap.html')

    # Format node positions to plottable format
    node_ids = []
    x_coords = []
    y_coords = []
    for node in nodes:
        node_ids.append(node)
        x_coords.append(nodes[node].pos_x)
        y_coords.append(206 - nodes[node].pos_y)

    # Extracting source info
    print "Extracting node info"
    source = ColumnDataSource(data=dict(
        x=x_coords,
        y=y_coords,
        node=node_ids))

    # Define plot
    print "Initializing plot"
    p = figure(
        tools=['xpan', _createHoverTool()],
        width=1587, height=266,
        x_range=(0,1527), y_range=(0,206))

    # Draw image on background
    p.image_url(url=['map.png'], x=0, y=206, w=1527, h=207)

    # Define sizes
    brush_size = 151
    base_size = (600, 80)

    # Initialize maps
    global base
    base = createHeatmapBase(base_size)
    brush = createBrushMesh(brush_size)

    # Load events
    print "Loading node events"
    for node in nodes:
        count = nodes[node].get_measurement_count_by_time_window('2016-01-10 16:00:00','2016-01-10 23:59:59')
        if count > 0:
            for i in range(count):
                offset = ( int(nodes[node].pos_x / 1527.0 * 600.0),
                           int((207 - nodes[node].pos_y) / 207.0 * 80.0))
                applyBrush(base, brush, base_size, brush_size, offset)

    # Create palette
    palette = magma(256)
    hexPaletteToTuplePalette(palette)

    # Reformat data
    reformatHeatmap(base, base_size, palette)

    # Stuffzies
    print "Drawing heatmap"
    p.image_rgba(image=[base], x=0, y=0, dw=1527, dh=207)

     # Draw circles where nodes are
    p.circle('x', 'y', source=source, size=15, color='red')

    # Set borders
    p.min_border = 30

    # Define slider
    slider = Slider(start=1, end=29, value=1, step=1, title="Date",
                    callback=CustomJS.from_py_func(sliderCallback))

    # Make layout
    layout = column(p, slider)

    show(layout)

def sliderCallback(source, window=None):
    global base
    for j in range(10):
        for i in range(10):
            base[j, i, 0] = 0
            base[j, i, 1] = 0
            base[j, i, 2] = 0

# Returns a hovertool for nodes  
def _createHoverTool():
    return HoverTool(tooltips=[
        ('node', '@node'),
        ('location', '(@x, @y)')])
