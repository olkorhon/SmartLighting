from bokeh.models import FixedTicker
from bokeh.plotting import figure, show
from example_data import generateSavingData
from helpers import ensureDictionaryHasHolders

def createEnergySaveGraph(width, height):
    # Define base figure for energy savings
    fig = figure(width=width, height=height, x_range=(6,18), y_range=(0, 100), toolbar_location=None, tools=[])
    fig.xaxis[0].ticker=FixedTicker(ticks=range(25))#[0, 3, 6, 9, 12, 15, 18, 21, 24])
    fig.xgrid.grid_line_color = None

    # Set axis labels
    fig.xaxis.axis_label = 'Hour'
    fig.yaxis.axis_label = 'Energy save percentage'

    return fig

def setExampleData(fig, source, xs, ys, days):
    # Initialize data
    times = []
    for i in range(24):
        times.append(i+0.5)

    # Construct data
    data = {xs:times, ys:range(24)}

    # Generate BS data
    for date in range(*days): #TODO No hardcoding!
        for h in range(24):
            postfix = '_' + str(h) + str(date)
            data[ys+postfix] = generateSavingData()

    # Set data to default
    data[ys+'_shown'] = data[ys]

    source.data = data

    # Setup line data
    #fig.line(
    #    x=xs,
    #    y=ys + '_shown',
    #    source=source,
    #    color="#2b8cbe")

    fig.vbar(
        x=xs,
        width=0.8,
        bottom = 0,
        top=ys + '_shown',
        source=source,
        color="#2b8cbe")

def setData(fig, source, raw_data, xs, ys, days, start_h):
    parsed_data = {}

    for date, elem_list in raw_data.iteritems():
        if elem_list == None:
            print 'Hyvin varoitettu Eero, Noneha se oli'
            continue

        postfix = '_' + str(date.day)
        x_path = xs + postfix
        y_path = ys + postfix

        ensureDictionaryHasHolders(parsed_data, x_path, y_path)

        for i in range(len(elem_list)):
            elem = elem_list[i]

            # Skip empty elements
            if elem == None:
                print 'Syyta Eeroa, elementti oli tyhja saatana'
                continue

            parsed_data[x_path].append(i + start_h + 0.5)
            parsed_data[y_path].append(elem)

    # Get random data
    for key, elem in parsed_data.iteritems():
        rand_elem = elem
        break

    # Set data to default
    parsed_data[xs + '_shown'] = []
    parsed_data[ys + '_shown'] = []

    first_stamp = '_' + str(start_h) + str(days[0])
    if xs+first_stamp in parsed_data and ys+first_stamp in parsed_data:
        parsed_data[xs + '_shown'] = parsed_data[xs + first_stamp]
        parsed_data[ys + '_shown'] = parsed_data[ys + first_stamp]

    # Set data for source
    source.data = parsed_data

    fig.vbar(
        x=xs + '_shown',
        width=0.8,
        bottom=0,
        top=ys + '_shown',
        source=source,
        color="#2b8cbe")



def setDivider(fig, source):
    data = {}
    if source.data != None:
        data = source.data

    data['div_x'] = [0.5]
    data['top'] = [100]

    fig.vbar(
        x='div_x',
        bottom=0, top='top',
        width=1,
        source=source,
        color="#a6bddb")

def setDailyAverage(fig, source):
    data = {}
    if source.data != None:
        data = source.data

    data['avg_x'] = [-200, 200]
    data['avg_y'] = [0, 0]

    fig.line(x='avg_x',
             y='avg_y',
             source=source,
             color="#feb24c",
             line_width=1)

if __name__ == '__main__':
    show(createEnergySaveGraph(300, 240))