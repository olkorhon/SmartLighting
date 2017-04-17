from bokeh.plotting import figure, output_file, show
from bokeh.charts import HeatMap

import numpy as np

def makeHeatmap(nodes):
    output_file('heatmap.html')

    # Format node positions to plottable format
    x_coords = []
    y_coords = []
    for node in nodes:
        x_coords.append(nodes[node].pos_x)
        y_coords.append(206 - nodes[node].pos_y)

    # Define plot
    p = figure(
        tools='xpan',
        width=1638, height=626,
        x_range=(0,618), y_range=(0,206))

    # Draw image on background
    p.image_url(url=['map.png'], x=0, y=207, w=1527, h=207)

    #N = 10
    #x = np.linspace(0, 20, N)
    #y = np.linspace(0, 20, N)
    #xx, yy = np.meshgrid(x, y)
    #d = np.sin(xx)*np.cos(yy)
    #img_dat = [[0,1,2,3], [4,5,6,7], [8,9,10,11], [12,13,14,15]]
    #p.image(image=[img_dat], x=0, y=0, dw=200, dh=200, palette="Spectral11")

    # Draw circles where nodes are
    p.circle(x=x_coords, y=y_coords, size=30, color='red')

    # Set borders
    p.min_border = 60

    show(p)
