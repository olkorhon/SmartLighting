from bokeh.plotting import figure, output_file, ColumnDataSource, show
from bokeh.palettes import linear_palette, Plasma256
from bokeh.models import HoverTool

import numpy as np

def makeNetwork(nodes):
    print "Data received"
    output_file('arrow.html')

    # Create figure with nodes 
    p = createBackground(nodes)

    # Load example data
    data = generateExampleData(nodes)

    palette = linear_palette(Plasma256, 12)
    

    # Convert lines to arrows
    alphas = []
    colors = []
    sizes = [10, 11, 12, 13, 14, 15, 16, 17]
    sizes.extend(sizes)
    for i in range(len(data['x'])):
        transformToAnArrow(data, i, sizes[i])
        alphas.append(0.9)
        colors.append(palette[sizes[i] - 10])
   
    p.patches(data['x'], data['y'], line_width=0,
              color=colors, alpha=alphas)

    show(p)

# Size should be normalized
def transformToAnArrow(data, i, size):
    delta_x = data['x'][i][1] - data['x'][i][0]
    delta_y = data['y'][i][1] - data['y'][i][0]

    length = (delta_x ** 2 + delta_y ** 2) ** 0.5

    delta_x = delta_x * size / length
    delta_y = delta_y * size / length

    tangent_x = delta_y
    tangent_y = -delta_x

    # Add extra points
    data['x'][i].append(data['x'][i][1] - tangent_x - delta_x * 2)
    data['x'][i].append(data['x'][i][1] + tangent_x / 2 + delta_x * 1.5 - delta_x * 2)
    data['x'][i].append(data['x'][i][1] + tangent_x * 2 - delta_x * 2)
    data['x'][i].append(data['x'][i][1] + tangent_x - delta_x * 2)
    data['x'][i].append(data['x'][i][0] + tangent_x + delta_x / size * 40)
    data['x'][i][1] -= delta_x * 2
    data['x'][i][0] += delta_x / size * 40

    data['y'][i].append(data['y'][i][1] - tangent_y - delta_y * 2)
    data['y'][i].append(data['y'][i][1] + tangent_y / 2 + delta_y * 1.5 - delta_y * 2)
    data['y'][i].append(data['y'][i][1] + tangent_y * 2 - delta_y * 2)
    data['y'][i].append(data['y'][i][1] + tangent_y - delta_y * 2)
    data['y'][i].append(data['y'][i][0] + tangent_y + delta_y / size * 40)
    data['y'][i][1] -= delta_y * 2
    data['y'][i][0] += delta_y / size * 40
    
def createBackground(nodes):
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

    # Draw circles where nodes are
    p.circle('x', 'y', source=source, size=15, color='red')

    # Set borders
    p.min_border = 30

    return p

# Generate an example path that includes all the nodes
def generateExampleData(nodes):
    # Define path with node_ids
    example_path = [259, 254, 256, 251, 252, 258, 253, 250, 257]
    reverse_path = example_path[::-1]
    
     # Make example lines
    x = []
    y = []
    last = None
    for node in example_path:
        if last != None:
            points_x = []
            points_y = []
            points_x.append(nodes[last].pos_x)
            points_x.append(nodes[node].pos_x)
            points_y.append(207 - nodes[last].pos_y)
            points_y.append(207 - nodes[node].pos_y)
            x.append(points_x)
            y.append(points_y)
        last = node

    # Reverse list
    last = None
    for node in reverse_path:
        if last != None:
            points_x = []
            points_y = []
            points_x.append(nodes[last].pos_x)
            points_x.append(nodes[node].pos_x)
            points_y.append(207 - nodes[last].pos_y)
            points_y.append(207 - nodes[node].pos_y)
            x.append(points_x)
            y.append(points_y)
        last = node

    example_path = [259, 254, 256, 251, 252, 258, 253, 250, 257]
    reverse_path = example_path[::-1]

    return {'x':x, 'y':y}

# Returns a hovertool for nodes  
def _createHoverTool():
    return HoverTool(tooltips=[
        ('node', '@node'),
        ('location', '(@x, @y)')])
