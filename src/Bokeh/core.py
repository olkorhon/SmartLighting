from bokeh.models import LabelSet, HoverTool
from bokeh.plotting import figure


def createCoreFigure(bg_path):
    fig = figure(
        tools=[],#"xpan", _createHoverTool()],
        width=1527 + 40, height=206 + 40,
        x_range=(0, 1527), y_range=(0, 206),
        min_border=20, toolbar_location=None)
    fig.axis.visible = False
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None

    # Draw image on background
    fig.image_url(url=[bg_path], x=0, y=206, w=1527, h=207)
    return fig


def drawOnFigure(fig, source, nodes):
    populateNodeSource(source, nodes, 206)
    drawNodes(fig, source, True)


def populateNodeSource(source, nodes, y_invert_factor=-1):
    data = dict(
        x_shown=[], y_shown=[], id_shown=[],
        x=[], y=[], id=[])

    # Format node positions to plottable format
    if y_invert_factor >= 0:
        for node_id in nodes:
            data["id"].append(node_id)
            data["x"].append(nodes[node_id].pos_x)
            data["y"].append(y_invert_factor - nodes[node_id].pos_y)
    else:
        for node_id in nodes:
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


# Returns a hovertool for nodes
#def _createHoverTool():
#    return HoverTool(tooltips=[
#        ("node", "@id"),
#        ("location", "(@x, @y)")])
