from bokeh.layouts import row, column
from bokeh.plotting import output_file, ColumnDataSource, show
from bokeh.models import CustomJS, Slider, CheckboxGroup

from js_callbacks import updateHour, updateDay, updateToggles
import core, heatmap, network

def create(nodes, heatdata):
    print "Data received"
    output_file("visuals.html")

    # Initialize data sources
    state_source = ColumnDataSource(data=dict(hour=[1], day=[25], active=[0]))
    node_source = ColumnDataSource(data=dict(
        x_shown=[], y_shown=[], id_shown=[],
        x=[], y=[], id=[]))
    heat_source = ColumnDataSource(data=dict())
    arrow_source = ColumnDataSource(data=dict(
        x_shown=[], y_shown=[], size_shown=[],
        x=[], y=[], size=[]))

    # Create base for all
    fig = core.createCoreFigure('map.png')

    # Draw Different layers of visualization
    core.drawOnFigure(fig, node_source, nodes)
    heatmap.drawOnFigure(fig, heat_source, heatdata, nodes)
    network.drawOnFigure(fig, arrow_source, nodes, "x", "y", "size", "color", "alpha")
    core.drawNodes(fig, node_source, True)

    # Define user interface
    toggle_callback = CustomJS(args=dict(state=state_source, node_source=node_source, heat_source=heat_source, arrow_source=arrow_source), code=updateToggles)
    toggles = CheckboxGroup(labels=["Nodes", "Heatmap", "Arrows"], active=state_source.data['active'], callback=toggle_callback)

    # Create slider and give it the defined inner function callback
    hour_callback = CustomJS(args=dict(source=heat_source, state=state_source), code=updateHour)
    hour_slider = Slider(start=1, end=24, value=1, step=1, title="hour", callback=hour_callback)

    # Create date slider and give it the defined inner function callback
    day_callback = CustomJS(args=dict(source=heat_source, state=state_source), code=updateDay)
    day_slider = Slider(start=25, end=31, value=25, step=1, title="day", callback=day_callback)

    # Make layout
    layout = column(fig, row(column(hour_slider, day_slider), toggles))

    show(layout)