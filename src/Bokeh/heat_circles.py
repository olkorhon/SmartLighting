from math import pi
from bokeh.palettes import Inferno256, linear_palette

from helpers import ensureDictionaryHasHolders
import constants

def drawOnFigure(fig, source, heatdata, nodes, data_format, palette=Inferno256):
    data = parseRawData(heatdata, nodes, data_format, linear_palette(palette, constants.HEATMAP_CUTOFF + 1))

    # Create holder for currently shown circles
    data[data_format['xs'] + '_shown'] = []
    data[data_format['ys'] + '_shown'] = []
    data[data_format['ss'] + '_shown'] = []
    data[data_format['cs'] + '_shown'] = []

    source.data = data

    fig.scatter(
        x=data_format['xs'] + '_shown', y=data_format['ys'] + '_shown',
        radius=data_format['ss'] + '_shown', fill_color=data_format['cs'] + '_shown',
        fill_alpha=0.8, source=source, angle=pi/3, line_color=None)


def parseRawData(raw_data, nodes, data_format, palette):
    edited_data = {}

    print "    Painting data to heatmaps"
    for node in raw_data:
        pos_x = float(nodes[node].pos_x)
        pos_y = float(nodes[node].pos_y)
        for date, elem_list in raw_data[node].iteritems():
            # Elem is a tuple
            for elem in elem_list:
                # Skip if no events
                if elem[1] == 0:
                    continue

                # Determine date coded keys for arrays
                postfix = '_' + str(elem[0]) + str(date.day)
                x_path = data_format['xs'] + postfix
                y_path = data_format['ys'] + postfix
                s_path = data_format['ss'] + postfix
                c_path = data_format['cs'] + postfix

                ensureDictionaryHasHolders(edited_data, x_path, y_path, s_path, c_path)

                size = elem[1]
                if size > constants.HEATMAP_BRUSH_MAXSIZE:
                    size = constants.HEATMAP_BRUSH_MAXSIZE
                if size < constants.HEATMAP_BRUSH_MINSIZE:
                    size = constants.HEATMAP_BRUSH_MINSIZE

                color = elem[1]
                if color > constants.HEATMAP_CUTOFF:
                    color = constants.HEATMAP_CUTOFF

                edited_data[x_path].append(pos_x)
                edited_data[y_path].append(constants.MAP_RESOLUTION[1] - pos_y)
                edited_data[s_path].append(size)
                edited_data[c_path].append(palette[color])

    return edited_data