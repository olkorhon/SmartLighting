from bokeh.palettes import linear_palette, Plasma256
from bokeh.models.glyphs import Patches
from example_data import generateExampleNetworkData
from shapes import lineToArrow


def drawOnFigure(fig, source, nodes, xs, ys, vs, cs, aS):
    # Load example data
    # TODO use ACTUAL data
    generateExampleNetworkData(source, xs, ys, vs, nodes)
    convertLineDataToArrows(source.data, xs, ys, vs, cs, aS)

    source.data[xs+"_shown"] = []
    source.data[ys+"_shown"] = []
    source.data[vs+"_shown"] = []
    source.data[cs+"_shown"] = []
    source.data[aS+"_shown"] = []

    # Plot patches to figure
    glyph = Patches(xs=xs+"_shown", ys=ys+"_shown", fill_color=cs+"_shown", fill_alpha=aS+"_shown", line_width=0)
    fig.add_glyph(source, glyph)

def convertLineDataToArrows(data, xs, ys, vs, cs, aS):
    palette = linear_palette(Plasma256, 12)

    # Convert lines to arrows
    data[cs] = []
    data[aS] = []
    for i in range(len(data[xs])):
        lineToArrow(data, i, xs, ys, vs)
        data[cs].append(palette[data[vs][i] - 10])
        data[aS].append(0.6)