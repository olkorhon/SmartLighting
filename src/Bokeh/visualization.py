from calendar import datetime

from bokeh.core.properties import Date, Tuple
from bokeh.layouts import row, column
from bokeh.plotting import output_file, ColumnDataSource, show
from bokeh.models import CustomJS, Slider, CheckboxGroup, DateRangeSlider
from bokeh.palettes import Inferno256

from js_callbacks import updateHour, updateDay, updateToggles
import core, heatmap, network, legend, helpers, energy_save

def create(nodes, heatdata):
    print "Data received"
    output_file("visuals.html")

    # Initialize data sources
    print 'Define data sources'
    state_source = ColumnDataSource(data=dict(hour=[1], day=[25], active=[0]))
    node_source = ColumnDataSource()
    heat_source = ColumnDataSource(data=dict())
    arrow_source = ColumnDataSource()
    energy_source = ColumnDataSource(data=dict())

    # Create base for all
    fig = core.createCoreFigure('map.png')

    # Define used palette
    palette = Inferno256
    helpers.hexPaletteToTuplePalette(palette)

    # Gradientify palette
    for i in range(len(palette)):
        palette[i][3] = (float(i) / len(palette)) * 255

    # Draw Different layers of visualization
    print 'Draw different map visualization layers'
    print '  Core...'
    core.drawOnFigure(fig, node_source, nodes)
    print '  Heatmap...'
    heatmap.drawOnFigure(fig, heat_source, heatdata, nodes, palette)
    print '  Network...'
    network.drawOnFigure(fig, arrow_source, nodes, "x", "y", "size", "color", "alpha")
    print '  Nodes...'
    core.drawNodes(fig, node_source, True)

    print '\nDraw Energy save graph'
    energy_fig = energy_save.createEnergySaveGraph(300, 240)
    energy_save.setData(energy_fig, energy_source, 'hours', 'savings')

    # Define user interface
    toggle_callback = CustomJS(args=dict(state=state_source, node_source=node_source, heat_source=heat_source, arrow_source=arrow_source), code=updateToggles)
    toggles = CheckboxGroup(labels=["Nodes", "Heatmap", "Arrows"], active=state_source.data['active'], callback=toggle_callback)

    # Create slider and give it the defined inner function callback
    hour_callback = CustomJS(args=dict(heat_source=heat_source, energy_source=energy_source, arrow_source=arrow_source, state=state_source), code=updateHour)
    hour_slider = Slider(start=1, end=24, value=1, step=1, title="hour", callback=hour_callback)

    # Create date slider and give it the defined inner function callback
    day_callback = CustomJS(args=dict(heat_source=heat_source, energy_source=energy_source, arrow_source=arrow_source, state=state_source), code=updateDay)
    day_slider = Slider(start=25, end=31, value=25, step=1, title="Date 2017 : 2 ", callback=day_callback, value_labels='hide')
    #date_picker = DateRangeSlider(
    #  step={},
    #  bounds=(Tuple(Date(datetime.date(year=2017, month=9, day=25)), Date(datetime.date(year=2017, month=9, day=30)))),
    #  value=Date(datetime.date(2017, 9, 25)),
    #  wheel_mode=None)

    # Make layout
    addons_below = row(column(hour_slider, day_slider), toggles, energy_fig)
    legend_widget = legend.createLegend(palette, 80, 270)

    layout = row(column(fig, addons_below), legend_widget)
    show(layout)