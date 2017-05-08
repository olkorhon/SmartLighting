from calendar import datetime

from bokeh.core.properties import Date, Tuple
from bokeh.layouts import row, column
from bokeh.plotting import output_file, ColumnDataSource, show
from bokeh.models import CustomJS, Slider, CheckboxGroup, DateRangeSlider
from bokeh.palettes import Inferno256

from js_callbacks import updateHour, updateDay, updateToggles
import core, heatmap, network, legend, helpers, energy_save, heat_circles

def create(nodes, heatdata, traffic_data, hourly_savings_per_day):
    print "Data received"
    output_file("visuals.html")

    # Initialize data sources
    print 'Define data sources'
    state_source = ColumnDataSource(data=dict(hour=[1], day=[25], active=[0]))
    node_source = ColumnDataSource()
    heat_source = ColumnDataSource(data=dict())
    arrow_source = ColumnDataSource()
    energy_source = ColumnDataSource(data=dict())
    divider_source = ColumnDataSource(data=dict())
    average_source = ColumnDataSource(data=dict())

    sources = dict(state=state_source,
                   node_source=node_source,
                   heat_source=heat_source,
                   arrow_source=arrow_source,
                   energy_source=energy_source,
                   divider_source=divider_source,
                   average_source=average_source)

    # Create base for all
    fig = core.createCoreFigure('map.png')

    # Define used palette
    palette = Inferno256

    # Set day range
    days = (25, 32)

    # Draw Different layers of visualization
    print 'Draw different map visualization layers'
    print '  Core...'
    core.drawOnFigure(fig, node_source, nodes)
    print '  Heatmap...'
    #heatmap.drawOnFigure(fig, heat_source, heatdata, nodes, days, palette)
    heat_circles.drawOnFigure(fig, heat_source, heatdata, nodes, {'xs':'x', 'ys':'y', 'ss':'size', 'cs':'color', 'as':'alpha'}, palette)
    print '  Network...'
    network.drawOnFigure(fig, arrow_source, traffic_data, nodes,
        {'xs':'x', 'ys':'y', 'vs':'size', 'cs':'color', 'as':'alpha'})
    print '  Nodes...'
    core.drawNodes(fig, node_source, True)

    print '\nDraw Energy save graph'
    energy_fig = energy_save.createEnergySaveGraph(600, 240)
    energy_save.setDivider(energy_fig, divider_source)
    energy_save.setData(energy_fig, energy_source, hourly_savings_per_day, 'hour', 'saving', days, 6)
    energy_save.setDailyAverage(energy_fig, average_source)

    # Define user interface
    toggle_callback = CustomJS(args=sources, code=updateToggles)
    toggles = CheckboxGroup(labels=["Nodes", "Heatmap", "Arrows"], active=state_source.data['active'], callback=toggle_callback)

    # Create slider and give it the defined inner function callback
    hour_callback = CustomJS(args=sources, code=updateHour)
    hour_slider = Slider(start=0, end=23, value=1, step=1, title="hour", callback=hour_callback)

    # Create date slider and give it the defined inner function callback
    day_callback = CustomJS(args=sources, code=updateDay)
    day_slider = Slider(start=25, end=31, value=25, step=1, title="Date 2017 : 2 ", callback=day_callback)

    # Modify palette for legend
    helpers.hexPaletteToTuplePalette(palette)
    for i in range(len(palette)):
        palette[i][3] = 200
    palette[0][3] = 0

    # Make layout
    addons_below = row(column(hour_slider, day_slider), toggles, energy_fig)
    legend_widget = legend.createLegend(palette, 80, 270)

    layout = row(column(fig, addons_below), legend_widget)
    show(layout)