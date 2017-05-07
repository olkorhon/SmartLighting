from bokeh.palettes import linear_palette, Inferno256
from bokeh.models.glyphs import Patches
from example_data import generateExampleNetworkData
from shapes import lineToArrow


def drawOnFigure(fig, source, nodes, xs, ys, vs, cs, aS):
    # Load example data
    data = { } # TODO use ACTUAL data

    for date in range(25, 32): #TODO No hardcoding!
        for h in range(24):
            postfix = '_' + str(h + 1) + str(date)

            x_key = xs + postfix
            y_key = ys + postfix
            value_key = vs + postfix
            generateExampleNetworkData(x_key, y_key, value_key, nodes, data)

            color_key = cs + postfix
            alpha_key = aS + postfix
            convertLineDataToArrows(data, x_key, y_key, value_key, color_key, alpha_key)

    data[xs + '_shown'] = []
    data[ys + '_shown'] = []
    data[vs + '_shown'] = []
    data[cs + '_shown'] = []
    data[aS + '_shown'] = []

    source.data = data

    # Plot patches to figure
    glyph = Patches(xs=xs+"_shown", ys=ys+"_shown", fill_color=cs+"_shown", fill_alpha=aS+"_shown", line_width=0)
    fig.add_glyph(source, glyph)

def convertLineDataToArrows(data, xs, ys, vs, cs, aS, palette=linear_palette(Inferno256, 11)):
    # Convert lines to arrows
    if cs not in data:
        data[cs] = []

    if aS not in data:
        data[aS] = []

    for i in range(len(data[xs])):
        lineToArrow(data, i, xs, ys, vs)
        data[cs].append(palette[data[vs][i] - 10])
        data[aS].append(0.6)