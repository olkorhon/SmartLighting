from bokeh.models import FixedTicker
from bokeh.plotting import figure, show
from example_data import generateSavingData

def createEnergySaveGraph(width, height):
    # Draw scale
    fig = figure(width=width, height=height, x_range=(0, 23), y_range=(0, 100), toolbar_location=None, tools=[])
    fig.xaxis[0].ticker=FixedTicker(ticks=[0, 3, 6, 9, 12, 15, 18, 21, 24])
    fig.xgrid.grid_line_color = None
    #fig.axis.visible = False
    #fig.xgrid.grid_line_color = None
    #fig.ygrid.grid_line_color = None

    fig.xaxis.axis_label = 'Hour'
    fig.yaxis.axis_label = 'Energy save percentage'

    #fig.line(x=[0, 24], y=[0, 0], line_width=2, color='black')

    return fig

def setData(fig, source, xs, ys):
    # Hours
    default_savings = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    # Initialize data
    times = []
    for i in range(24):
        times.append(i)

    # Construct data
    data = {xs:times, ys:range(24)}



    # Set currently visible data
    #source.data[xs+'_shown'] = source.data[xs]

    for date in range(25, 32): #TODO No hardcoding!
        for h in range(24):
            postfix = '_' + str(h) + str(date)
            data[ys+postfix] = generateSavingData()

    # Set data to default
    data[ys+'_shown'] = data[ys]

    source.data = data

    # Setup line data
    fig.line(
        x=xs,
        y=ys + '_shown',
        source=source,
        color="navy")


def setDivider(fig, source):
    data = {}
    data['div_x'] = [0, 0]
    data['div_y'] = [-20, 100]

    source.data = data

    fig.line(
        x='div_x',
        y='div_y',
        source=source,
        color="yellow",
        line_width=2)



if __name__ == '__main__':
    show(createEnergySaveGraph(300, 240))