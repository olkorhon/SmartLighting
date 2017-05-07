# -*- coding: utf-8 -*-
import numpy as np

from bokeh.models import LabelSet
from bokeh.palettes import Inferno256
from bokeh.plotting import figure, show, ColumnDataSource

from helpers import hexPaletteToTuplePalette
import constants

def createLegend(palette, width, height):
    # Draw scale
    fig = figure(width=width, height=height, x_range=(0, 80), y_range=(0, 400), toolbar_location=None, tools=[])
    fig.axis.visible = False
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None

    scale = np.empty((len(palette), 1), dtype=np.float32)
    reformatArray(scale, palette)

    fig.image_rgba(image=[scale], x=5, y=10, dw=30, dh=380)

    # Draw label
    label_count = 5
    label_data = {'x': [], 'y': [], 'value': []}

    for i in range(label_count):
        label_data['x'].append(40)
        label_data['y'].append((float(i) / (label_count - 1)) * 360 + 10)
        label_data['value'].append((float(i) / (label_count - 1)) * constants.HEATMAP_CUTOFF)

    source = ColumnDataSource(data=label_data)
    labels = LabelSet(x='x', y='y', text='value', level='glyph',
                      x_offset=0, y_offset=5, source=source, render_mode='canvas',
                      text_font_style="bold", text_color="black", text_font_size='10pt',
                      background_fill_color="White", background_fill_alpha=0.5,
                      text_align='left', text_baseline='middle')
    fig.add_layout(labels)
    return fig

# Change heatmap data from float32 to [uint8]
def reformatArray(array, palette):
    # Reformat heatmap data to an image format
    view = array.view(dtype=np.uint8).reshape(len(palette), 1, 4)
    for y in range(len(palette)):
        color = palette[y]
        view[y, 0, 0] = color[0]
        view[y, 0, 1] = color[1]
        view[y, 0, 2] = color[2]
        view[y, 0, 3] = 255


if __name__ == "__main__":
    show(createLegend(hexPaletteToTuplePalette(Inferno256), 80, 400))