from __future__ import print_function, division

import copy

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from .Animation import Animation


class Movie:
    """ Class to movie animation of movies with traces
        Adds all image animation to a top row of subplots
        and adds all the trace animation plots to rows 2, 3, ...

        Dynamic componants (will update every cycle):
        images: a list of images to display on the top row
        labels: a list of labels that change ever frame (time / behavior)

        Static componants:
        axes: a list of axis to display on 2nd row
        traces: a list of traces to display on one of the axis from the above list
        annotations: a list of annotations

    """

    def __init__(self, style=None, dt=1.0 / 14, fig_kwargs={'figsize': (10, 10)}, fig_color='black',
                 height_ratio=2):
        """

        :param style: same as matplotlib.style.set mainly a dict with rcparams key-value pairs.
        These params will be applied to all subplots
        :param dt:
        :param fig_kwargs:
        :param fig_color:
        :param height_ratio: 1 will make height rations (1, 1), (2, 1, 1), (3, 1, 1, 1)
        2 will make height rations (2, 1), (4, 1, 1), (6, 1, 1, 1)
        """
        self.dt = dt
        self.fig_color = fig_color
        self.height_ratio = height_ratio
        self.fig_kwargs = fig_kwargs
        self.images = []
        self.traces = []
        self.labels = []
        self.annotations = []
        self.axes = []
        self.styles = copy.deepcopy(plt.style.library)  # type: dict
        self._add_styles()
        if style is not None:
            plt.style.use(style)

    def _add_styles(self):
        """ Add 4 new styles to the original matplotlib library: dark and light versions for images and traces

        """
        styles = dict()
        default = mpl.rcParamsDefault  # for light backgrounds
        dark_background = plt.style.library['dark_background']

        dark_img = copy.deepcopy(dark_background)
        dark_img.update({u'axes.spines.top': False, u'axes.spines.right': False,
                         u'axes.spines.bottom': False, u'axes.spines.left': False,
                         u'axes.facecolor': (1, 1, 1, 0), u'axes.edgecolor': (1, 1, 1, 0),
                         u'xtick.color': (1, 1, 1, 0), u'ytick.color': (1, 1, 1, 0), u'grid.alpha': 0,
                         u'image.interpolation': 'None', u'image.cmap': 'viridis'})
        styles[u'dark_img'] = dark_img

        light_img = copy.deepcopy(default)
        light_img.update({u'axes.spines.top': False, u'axes.spines.right': False,
                          u'axes.spines.bottom': False, u'axes.spines.left': False,
                          u'axes.facecolor': (1, 1, 1, 0), u'axes.edgecolor': (1, 1, 1, 0),
                          u'xtick.color': (1, 1, 1, 0), u'ytick.color': (1, 1, 1, 0), u'grid.alpha': 0,
                          u'image.interpolation': 'None'})
        styles[u'light_img'] = light_img

        dark_trace = copy.deepcopy(dark_background)
        dark_trace.update({u'axes.spines.top': False, u'axes.spines.right': False, u'axes.labelsize': u'x-large',
                           u'axes.titlesize': u'x-large'})
        styles[u'dark_trace'] = dark_trace

        light_trace = copy.deepcopy(default)
        light_trace.update({u'axes.spines.top': False, u'axes.spines.right': False,u'axes.labelsize': u'x-large',
                            u'axes.titlesize': u'x-large'})
        styles[u'light_trace'] = light_trace

        self.styles.update(styles)
        plt.style.library.update(styles)

    def add_label(self, x, y, values, axis=0, s_format='%s', size=14, **kwargs):
        """

        :param x: location in x
        :param y: location in y
        :param values: list of values
        :param axis: axis number to add the label to
        :param s_format: string format to use on the values
        :param size: font size
        :param kwargs: to be sent to the plt.text function
        :return:
        """
        local_vars = locals()
        del local_vars['self']
        self.labels.append(local_vars)

    def add_time_label(self, x=0.01, y=0.08, values=None, axis=0, s_format='%.2fs', size=14, **kwargs):
        if values is None:
            if len(self.images) == 0:
                if len(self.traces) == 0:
                    raise RuntimeError('Can not add time labels when no values are given and no data was added')
                else:
                    values = np.arange(self.traces[0]['data'].shape[0]) * self.dt
            else:
                values = np.arange(self.images[0]['data'].shape[0]) * self.dt
        self.add_label(x, y, values, axis, s_format, size, **kwargs)

    def add_behavior_label(self, x=0.9, y=0.08, values=None, axis=0, s_format='%s', size=14, **kwargs):
        self.add_label(x=x, y=y, values=values, axis=axis, s_format=s_format, size=size, kwargs=kwargs)

    def add_annotation(self, axis, xy, xy_text, text, **kwargs):
        self.annotations.append({'type': 'annotation', 'axis': axis, 'text': text, 'xy': xy, 'xy_text': xy_text,
                                 'kwargs': kwargs})

    def add_line_annotation(self, axis, x, y, **kwargs):
        """

        :param axis: axis number of the images
        :param x: x locations
        :param y: y locations
        :param kwargs: kwargs to be passed to Line2D
        :return:
        """
        self.annotations.append({'type': 'line', 'axis': axis, 'x': x, 'y': y, 'kwargs': kwargs})

    def add_text_annotation(self, axis, x, y, text, **kwargs):
        """

        :param axis: axis number of the images
        :param x: x location
        :param y: y location
        :param text: text to write
        :param kwargs: kwargs to be passed to plt.text
        :return:
        """
        self.annotations.append({'type': 'text', 'axis': axis, 'x': x, 'y': y, 'text': text, 'kwargs': kwargs})

    def add_circle_annotation(self, axis, x, y, radius, **kwargs):
        self.annotations.append({'type': 'circle', 'axis': axis, 'x': x, 'y': y, 'radius': radius, 'kwargs': kwargs})

    def add_scale_bar(self, axis=0, pixel_width=40, um_width='20', y=2, text_offset=1):
        """

        :param axis: which axis
        :param pixel_width: width of line in pixels
        :param um_width: text to write
        :param y: y position
        :param text_offset: offset of text in relation to the line
        :return:
        """
        self.add_line_annotation(axis=axis, x=(0, pixel_width), y=(y, y), color='white', lw=3)
        mid = int(pixel_width / 2)
        self.add_text_annotation(axis=axis, x=mid, y=y - text_offset, text=um_width + 'um', ha='center', fontsize=14,
                                 color='white')

    def get_ylim(self, ylim_type, ylim_value, data):
        """

        :param ylim_type: str:
        'set': expects y_lim_value to be (min, max) tuple
        'same': ylim_value is a trace or image reference number (according to 'same_type')
        'p_top': clip to the ylim_value percentile from the top
        'p_bottom': clip to the ylim_value percentile from the bottom
        'p_both': clip to the ylim_value percentile from the bottom and top
        :param ylim_value: according to 'ylim_type'
        :param data: image or trace to work on
        :return: tuple of min and max
        """
        if ylim_type == 'set':
            if hasattr(ylim_value, '__len__') and len(ylim_value) == 2:
                return ylim_value[0], ylim_value[1]
            else:
                raise RuntimeError('ylim type set to set but len of ylim_value is not len 2')
        elif ylim_type == 'same':
            if len(self.images) > ylim_value:
                return self.images[ylim_value]['ymin'], self.images[ylim_value]['ymax']
            else:
                raise RuntimeError('Tried to have same y limits as %d but # of images is %d' % (ylim_value,
                                                                                                len(self.images)))
        elif ylim_type == 'p_top':
            return np.nanmin(data), np.nanpercentile(data, 100.0 - ylim_value)
        elif ylim_type == 'p_bottom':
            return np.nanpercentile(data, ylim_value), np.nanmax(data)
        elif ylim_type == 'p_both':
            return np.nanpercentile(data, ylim_value), np.nanpercentile(data, 100.0 - ylim_value)
        else:
            raise RuntimeError("Expected 'p_top', 'p_bottom', 'p_both', 'set' or 'same' got: %s" % ylim_type)

    def add_image(self, data, style='dark_img', c_title=None, c_style='dark_background', ylim_type='p_top',
                  ylim_value=0.1):
        """

        :param data: 3d array (n, x, y)
        :param name: axis name to be referenced by other objects such as labels
        :param c_title: title to put on the color bar
        :param ylim_type: how to set the y limits. 'p_top' will clip the top ylim_value values in %.
        'p_bottom' same for bottom % pixels. 'p_both' will clip both ends. 'set' will expect a tuple [min max]
        in ylim_value. 'same' will expect a index in ylim_value for the axis number to take from.
        :param ylim_value: see ylim_type
        :param style: see matplotlib.style.set_. ability to compose styles. example: base style is dark for images
        .. _matplotlib.style.set: http://matplotlib.org/api/style_api.html?highlight=style#matplotlib.style.use
         but with a different color map:
        >>> style=['dark_img', {'image.cmap': 'magma'}]
        :return: Adds an image animation
        """
        if len(data.shape) != 3:
            raise ValueError('Expected 3d numpy array as image got: %s', data.shape)
        img = dict()
        img['data'] = data
        img['style'] = style
        img['c_title'] = c_title
        img['c_style'] = c_style
        img['ymin'], img['ymax'] = self.get_ylim(ylim_type, ylim_value, data)
        self.images.append(img)

    def add_trace(self, data, axis=0, **kwargs):
        if len(self.axes) <= axis:
            raise RuntimeError('Please create axis %d before adding traces' % axis)
        local_vars = locals()
        del local_vars['self']
        self.traces.append(local_vars)

    def add_axis(self, x_label, y_label, style='dark_trace', running_line={'color': 'white', 'lw': 2},
                 bottom_left_ticks=True, ylim_type='p_top', ylim_value=0.1, tight_x=True,
                 label_kwargs={'fontsize': 16}, legend_kwargs={'frameon': False}, **kwargs):
        """

        :param x_label: x label
        :param y_label: y label
        :param style: see matplotlib.styles
        :param ylim_type: how to set the y limits. 'p_top' will clip the top ylim_value values in %.
        'p_bottom' same for bottom % pixels. 'p_both' will clip both ends. 'set' will expect a tuple [min max]
        in ylim_value. 'same' will expect a index in ylim_value for the axis number to take from.
        :param ylim_value: see ylim_type
        :param running_line: if not None will display a line with the properties provided example:
         running_line = {'color': 'white', 'lw': 3}
         :param bottom_left_ticks: if True will only show the bottom left ticks of the axis
        :return:
        """
        local_vars = locals()
        del local_vars['self']
        self.axes.append(local_vars)

    def save(self, path, fps=14, codec='h264'):
        """

        :param path: full path to save animation
        :param fps: frames oer second to save movie
        :param codec: codec to use (h264 was tested to be good for power point on mac and windows)
        :return:
        """
        animation = Animation(self)
        animation.save(path, codec=codec, fps=fps, savefig_kwargs={'facecolor': self.fig_color})
