from bokeh.palettes import linear_palette, Inferno256
from bokeh.models.glyphs import Patches
from example_data import generateExampleNetworkData
from shapes import lineToArrow


def drawOnFigure(fig, source, raw_data, nodes, xs, ys, vs, cs, aS):
    # Load example data
    data = readData(raw_data, nodes, xs, ys, vs, cs, aS)

    data[xs + '_shown'] = []
    data[ys + '_shown'] = []
    data[vs + '_shown'] = []
    data[cs + '_shown'] = []
    data[aS + '_shown'] = []

    source.data = data

    # Plot patches to figure
    glyph = Patches(xs=xs+"_shown", ys=ys+"_shown", fill_color=cs+"_shown", fill_alpha=aS+"_shown", line_width=0)
    fig.add_glyph(source, glyph)

def readData(raw_data, nodes, xs, ys, vs, cs, aS, palette=linear_palette(Inferno256, 12)):
    edited_data = {}

    for key in raw_data:
        link = raw_data[key]
        start = nodes[link['from_node_id']]
        end = nodes[link['to_node_id']]

        for date in link['events']:
            for value_pair in link['events'][date]:
                # Skip if this is not a value
                if value_pair[1] == 0:
                    continue

                # Determine date coded keys for arrays
                postfix = '_' + str(value_pair[0]) + str(date.day)
                x_path = xs + postfix
                y_path = ys + postfix
                v_path = vs + postfix
                c_path = cs + postfix
                a_path = aS + postfix

                # Make sure a holder with this date exists
                if x_path not in edited_data:
                    edited_data[x_path] = []
                if y_path not in edited_data:
                    edited_data[y_path] = []
                if v_path not in edited_data:
                    edited_data[v_path] = []
                if c_path not in edited_data:
                    edited_data[c_path] = []
                if a_path not in edited_data:
                    edited_data[a_path] = []

                size = value_pair[1]
                if size < 5:
                    size = 5

                # Finally convert to arrow
                points_x, points_y = lineToArrow((start.pos_x, end.pos_x), (207 - start.pos_y, 207 - end.pos_y), size)
                edited_data[x_path].append(points_x)
                edited_data[y_path].append(points_y)
                edited_data[a_path].append(0.8)
                # Color could easily overflow, cap at 12
                if (size > 12):  # TODO do not use magick numbers as ceilings
                    edited_data[c_path].append(palette[11])
                else:
                    edited_data[c_path].append(palette[value_pair[1] - 1])

    return edited_data