from bokeh.palettes import linear_palette, RdBu
from bokeh.models.glyphs import Patches
from shapes import lineToArrow

from helpers import ensureDictionaryHasHolders
import constants


def drawOnFigure(fig, source, raw_data, nodes, data_format):
    # Load example data
    data = readData(raw_data, nodes, data_format)

    data[data_format['xs'] + '_shown'] = []
    data[data_format['ys'] + '_shown'] = []
    data[data_format['vs'] + '_shown'] = []
    data[data_format['cs'] + '_shown'] = []
    data[data_format['as'] + '_shown'] = []

    source.data = data

    # Plot patches to figure
    glyph = Patches(
        xs=data_format['xs'] + "_shown",
        ys=data_format['ys'] + "_shown",
        fill_color=data_format['cs'] + "_shown",
        fill_alpha=data_format['as'] + "_shown",
        line_width=0,
        line_color=None)

    # Add patch glyph to figure
    fig.add_glyph(source, glyph)


def readData(raw_data, nodes, data_format, palette=RdBu[11]):
    edited_data = {}

    for key, link in raw_data.iteritems():
        start = nodes[link['from_node_id']]
        end = nodes[link['to_node_id']]

        for date, event_collection in link['events'].iteritems():
            for value_pair in event_collection:
                # Skip if this is not a value
                if value_pair[1] == 0:
                    continue

                # Determine date coded keys for arrays
                postfix = '_' + str(value_pair[0]) + str(date.day)
                x_path = data_format['xs'] + postfix
                y_path = data_format['ys'] + postfix
                v_path = data_format['vs'] + postfix
                c_path = data_format['cs'] + postfix
                a_path = data_format['as'] + postfix

                # Make sure a holder with this date exists
                ensureDictionaryHasHolders(edited_data, x_path, y_path, v_path, c_path, a_path)

                # Scale arrow size
                size = value_pair[1] * constants.ARROW_SIZE_SCALE_FACTOR
                if size < constants.ARROW_MIN_SIZE:
                    size = constants.ARROW_MIN_SIZE
                if size > constants.ARROW_MAX_SIZE:
                    size = constants.ARROW_MAX_SIZE

                # Finally convert to arrow
                points_x, points_y = lineToArrow(
                    (start.pos_x, end.pos_x),
                    (constants.MAP_RESOLUTION[1] - start.pos_y, constants.MAP_RESOLUTION[1] - end.pos_y),
                    size)
                edited_data[x_path].append(points_x)
                edited_data[y_path].append(points_y)
                edited_data[a_path].append(0.8)

                # Color could easily overflow, cap at 12
                if (value_pair[1] > constants.ARROW_MAX_COLOR):  # TODO do not use magick numbers as ceilings
                    edited_data[c_path].append(palette[constants.ARROW_MAX_COLOR - 1])
                else:
                    edited_data[c_path].append(palette[value_pair[1] - 1])

    return edited_data