from __future__ import print_function, division, unicode_literals

import copy

from matplotlib.animation import writers
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from .Animation import Animation
from .checks import *


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
        dark_trace.update({u'axes.spines.top': False, u'axes.spines.right': False, u'axes.labelsize': u'xx-large',
                           u'axes.titlesize': u'xx-large', u'xtick.labelsize': 14, u'ytick.labelsize': 14})
        styles[u'dark_trace'] = dark_trace

        light_trace = copy.deepcopy(default)
        light_trace.update({u'axes.spines.top': False, u'axes.spines.right': False, u'axes.labelsize': u'xx-large',
                            u'axes.titlesize': u'xx-large', u'xtick.labelsize': 14, u'ytick.labelsize': 14})
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

    def add_annotation(self, axis, xy, xy_text, text, axis_type='image', **kwargs):
        """ add annotation using axis.annotate

        :param axis: axis number starting at 0
        :param xy: position of the arrow
        :param xy_text: position of the text box
        :param text: string to write
        :param axis_type: 'image' for images, 'trace' for traces
        :param kwargs: will be forwarded to annotate
        :return:
        """
        check_axis(axis)
        check_location(xy, name='xy')
        check_location(xy_text, name='xy_text')
        check_axis_type(axis_type)
        self.annotations.append({'type': 'annotation', 'axis': axis, 'text': text, 'xy': xy, 'xy_text': xy_text,
                                 'axis_type': axis_type, 'kwargs': kwargs})

    def add_variable_annotation(self, axis, xy_array, xy_text_array, text_array, axis_type='image', **kwargs):
        """ add annotation using axis.annotate

        :param axis: axis number starting at 0
        :param xy_array: position of the arrow (array length of data)
        :param xy_text_array: position of the text box (array length of data)
        :param text_array: string to write (array length of data)
        :param axis_type: 'image' for images, 'trace' for traces
        :param kwargs: will be forwarded to annotate
        :return:
        """
        check_axis(axis)
        check_location(xy_array[0], name='xy')
        check_location(xy_text_array[0], name='xy_text')
        check_axis_type(axis_type)
        if len(self.images) == 0:
            if len(self.traces) == 0:
                raise RuntimeError('Can not add time labels when no values are given and no data was added')
            else:
                length = self.traces[0]['data'].shape[0]
        else:
            length = self.images[0]['data'].shape[0]
        check_length(xy_array, length, 'xy_array')
        check_length(xy_text_array, length, 'xy_text_array')
        check_length(text_array, length, 'text_array')
        self.annotations.append({'type': 'var_annotation', 'axis': axis, 'text_array': text_array, 'xy_array': xy_array,
                                 'xy_text_array': xy_text_array, 'axis_type': axis_type, 'kwargs': kwargs})

    def add_rectangle_annotation(self, axis, xy, width, height, angle, axis_type='image', **kwargs):
        """ add annotation using patches.Rectangle. Draw a rectangle with lower left at xy = (x, y)
        with specified width, height and rotation angle.

        :param axis: axis number starting at 0
        :param xy: lower left corner
        :param width: width
        :param height:height
        :param angle: angle
        :param axis_type: 'image' for images, 'trace' for traces
        :param kwargs: will be forwarded to patches.Rectangle
        :return:
        """
        check_axis(axis)
        check_location(xy, name='xy')
        check_number(width, name='width')
        check_number(height, name='height')
        check_number(angle, name='angle')
        check_axis_type(axis_type)
        self.annotations.append({'type': 'rectangle', 'axis': axis, 'axis_type': axis_type, 'xy': xy, 'width': width,
                                 'height': height, 'angle': angle, 'kwargs': kwargs})

    def add_line_annotation(self, axis, x, y, axis_type='image', **kwargs):
        """

        :param axis: axis number of the images
        :param x: x locations
        :param y: y locations
        :param axis_type: 'image' for images, 'trace' for traces
        :param kwargs: kwargs to be passed to Line2D
        :return:
        """
        check_axis(axis)
        check_locations(x, 'x')
        check_locations(y, 'y')
        check_axis_type(axis_type)
        self.annotations.append({'type': 'line', 'axis': axis, 'x': x, 'y': y, 'axis_type': axis_type,
                                 'kwargs': kwargs})

    def add_text_annotation(self, axis, x, y, text, axis_type='image', **kwargs):
        """

        :param axis: axis number of the images
        :param x: x location
        :param y: y location
        :param text: text to write
        :param axis_type: 'image' for images, 'trace' for traces
        :param kwargs: kwargs to be passed to plt.text
        :return:
        """
        check_axis(axis)
        check_number(x, name='x')
        check_number(y, name='y')
        check_text(text, name='text')
        check_axis_type(axis_type)
        self.annotations.append({'type': 'text', 'axis': axis, 'x': x, 'y': y, 'text': text, 'axis_type': axis_type,
                                 'kwargs': kwargs})

    def add_circle_annotation(self, axis, x, y, radius, axis_type='image', **kwargs):
        """

        :param axis: axis number of the images
        :param x: x location
        :param y: y location
        :param radius: radius of circle
        :param axis_type: 'image' for images, 'trace' for traces
        :param kwargs: kwargs to be passed to plt.text
        :return:
        """
        check_axis(axis)
        check_number(x, name='x')
        check_number(y, name='y')
        check_number(radius, name='radius')
        check_axis_type(axis_type)
        self.annotations.append({'type': 'circle', 'axis': axis, 'x': x, 'y': y, 'radius': radius,
                                 'axis_type': axis_type, 'kwargs': kwargs})

    def add_scale_bar(self, axis=0, x_offset=0, pixel_width=40, um_width='20', y=2, text_offset=1, line_kwargs=None,
                      text_kwargs=None):
        """

        :param axis: which axis
        :param x_offset: x start position
        :param pixel_width: width of line in pixels
        :param um_width: text to write
        :param y: y position
        :param text_offset: offset of text in relation to the line in y
        :return:
        """
        check_axis(axis)
        check_number(x_offset, name='x_offset')
        check_number(pixel_width, name='pixel_width')
        check_text(um_width, name='um_width')
        check_number(y, name='y')
        check_number(text_offset, name='text_offset')
        stop = x_offset + pixel_width
        if line_kwargs is None:
            self.add_line_annotation(axis=axis, x=(x_offset, stop), y=(y, y), color='white', lw=3)
        else:
            check_dict(line_kwargs, name='line_kwargs')
            self.add_line_annotation(axis=axis, x=(x_offset, stop), y=(y, y), **line_kwargs)
        mid = int(pixel_width / 2 + x_offset)
        if text_kwargs is None:
            self.add_text_annotation(axis=axis, x=mid, y=y - text_offset, text=um_width + 'um', ha='center',
                                     fontsize=14, color='white')
        else:
            check_dict(text_kwargs, name='text_kwargs')
            self.add_text_annotation(axis=axis, x=mid, y=y - text_offset, text=um_width + 'um', **text_kwargs)

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

    def add_image(self, data, animation_type='movie', style='dark_img', c_title=None, c_style='dark_background',
                  ylim_type='p_top', ylim_value=0.1, window_size=29, window_step=1, is_rgb=False):
        """

        :param data: 3d array (n, x, y) if type is movie or (x, y) if type is window
        :param animation_type: type of movie animation. 'movie' assume a 3d movie. 'window' does a sliding window with
         window_size and window_step of a 2d array.
        :param c_title: title to put on the color bar
        :param c_style
        :param ylim_type: how to set the y limits. 'p_top' will clip the top ylim_value values in %.
        'p_bottom' same for bottom % pixels. 'p_both' will clip both ends. 'set' will expect a tuple [min max]
        in ylim_value. 'same' will expect a index in ylim_value for the axis number to take from.
        :param ylim_value: see ylim_type
        :param style: see matplotlib.style.set_. ability to compose styles. example: base style is dark for images
        .. _matplotlib.style.set: http://matplotlib.org/api/style_api.html?highlight=style#matplotlib.style.use
         but with a different color map:
        >>> style=['dark_img', {'image.cmap': 'magma'}]
        :param window_size: size of window of the x axis of the movie to display
        :param window_step: step to advance in each frame of the animation
        :return: Adds an image animation
        """
        if animation_type != 'movie' and animation_type != 'window':
            raise ValueError('animation type should be movie or window got: %s' % animation_type)
        if len(data.shape) != 3 and animation_type == 'movie':
            raise ValueError('Expected 3d numpy array when animation type is movie got: %s', data.shape)
        if len(data.shape) != 2 and animation_type == 'window' and not is_rgb:
            raise ValueError('Expected 2d numpy array when animation type is window got: %s', data.shape)
        if animation_type == 'window' and is_rgb:
            if len(data.shape) != 3 or (len(data.shape) == 3 and data.shape[2] != 3):
                raise ValueError('Expected 3d numpy array when animation type is window and is_rgb is True got: %s',
                                 data.shape)

        if (window_size & 1) != 1:
            raise ValueError('Window size must be odd got: %d' % window_size)
        img = dict()
        img['ymin'], img['ymax'] = self.get_ylim(ylim_type, ylim_value, data)
        local_vars = locals()
        del local_vars['self']
        del local_vars['img']
        del local_vars['ylim_type']
        del local_vars['ylim_value']
        img.update(local_vars)
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
        check_text(x_label, 'x_label')
        check_text(y_label, 'y_label')
        check_dict(running_line, 'running_line')
        check_bool(bottom_left_ticks, 'bottom_left_ticks')
        check_text(ylim_type, 'ylim_type')
        check_bool(tight_x, 'tight_x')
        check_dict(label_kwargs, 'label_kwargs')
        check_dict(legend_kwargs, 'legend_kwargs')
        local_vars = locals()
        del local_vars['self']
        self.axes.append(local_vars)

    def save(self, path, writer_name='ffmpeg', fps=14, codec='h264'):
        """

        :param path: full path to save animation (path and filename without extension)
        :param writer_name: could be 'ffmpeg' or 'imagemagick' for now
        :param fps: frames oer second to save movie
        :param codec: codec to use (h264 was tested to be good for power point on mac and windows)
        :return:
        """
        animation = Animation(self, fps=fps)
        if writer_name in writers.avail:
            if 'ffmpeg' in writer_name:
                path += '.mp4'
            elif 'imagemagick' in writer_name:
                path += '.gif'
            else:
                raise ValueError('writer_name not "ffmpeg" or "imagemagick" got: %s' % writer_name)
            writer = writers[writer_name](fps=fps, codec=codec)
            animation.save(path, writer=writer, savefig_kwargs={'facecolor': self.fig_color})
        else:
            raise ValueError('Could not find %s in writers: %s' % (writer_name, writers.avail))
