from bokeh.models import LabelSet, HoverTool
from bokeh.plotting import figure
import constants

def createCoreFigure(bg_path):
    border = 20

    fig = figure(
        tools=[],#"xpan", _createHoverTool()],
        width=constants.MAP_RESOLUTION[0] + 2 * border, height=constants.MAP_RESOLUTION[1] + 2 * border,
        x_range=(0, constants.MAP_RESOLUTION[0]), y_range=(0, constants.MAP_RESOLUTION[1]),
        min_border=border, toolbar_location=None)
    fig.axis.visible = False
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None

    # Draw image on background
    fig.image_url(url=[bg_path], x=0, y=constants.MAP_RESOLUTION[1], w=constants.MAP_RESOLUTION[0], h=constants.MAP_RESOLUTION[1] + 1)
    return fig


def drawOnFigure(fig, source, nodes):
    populateNodeSource(source, nodes, constants.MAP_RESOLUTION[1])
    drawNodes(fig, source, True)


def populateNodeSource(source, nodes, y_invert_factor=-1):
    data = dict(
        x_shown=[], y_shown=[], id_shown=[],
        x=[], y=[], id=[])

    # Format node positions to plottable format
    if y_invert_factor >= 0:
        for node_id in nodes:
            if (nodes[node_id].pos_x != None):
                data["id"].append(node_id)
                data["x"].append(nodes[node_id].pos_x)
                data["y"].append(y_invert_factor - nodes[node_id].pos_y)
    else:
        for node_id in nodes:
            if (nodes[node_id].pos_x != None):
                data["id"].append(node_id)
                data["x"].append(nodes[node_id].pos_x)
                data["y"].append(nodes[node_id].pos_y)

    # Nodes are visible by default
    data["x_shown"] = data["x"]
    data["y_shown"] = data["y"]
    data["id_shown"] = data["id"]

    source.data = data

def drawNodes(fig, source, draw_labels):
    # Draw circles to indicate nodes
    fig.circle("x_shown", "y_shown", source=source, size=11, color="black")

    # Draw labels
    if draw_labels:
        labels = LabelSet(x='x_shown', y='y_shown', text='id_shown', level='glyph',
                          x_offset=0, y_offset=5, source=source, render_mode='canvas',
                          text_font_style="bold", text_color="black", text_font_size='10pt',
                          background_fill_color="White", background_fill_alpha=0.5)
        fig.add_layout(labels)