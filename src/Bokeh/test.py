# -*- coding: cp1252 -*-

from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import Figure, output_file, show

def createBackground(bg_path):
    # Define plot
    print "Initializing plot"
    p = Figure(
        tools=['xpan'],#¤, _createHoverTool()],
        width=1587, height=266,
        x_range=(0,1527), y_range=(0,206),
        min_border=30)

    # Draw image on background
    p.image_url(url=[bg_path], x=0, y=206, w=1527, h=207)

    return p

def createPlot():
    output_file("callback.html")

    x = [(x * 7) for x in range(0, 200)]
    y = x

    source = ColumnDataSource(data=dict(x=x, y=y))

    plot = createBackground('map.png')
    plot.line('x', 'y', source=source, line_width=10, line_alpha=0.6)

    slider = Slider(start=0.1, end=4, value=1, step=0.1, title="power",
                    callback=CustomJS.from_py_func(callback))

    layout = column(slider, plot)
    show(layout)
    
def callback(source=source, window=None):
    data = source.data
    f = cb_obj.value
    x, y = data['x'], data['y']
    for i in range(len(x)):
        y[i] = x[i]**f
    source.trigger('change')

createPlot()
