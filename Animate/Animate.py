from __future__ import print_function, division
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


class Animation:
    """ Class to make animation of movies with traces
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

    def __init__(self, base_path, name, style=None, dt=1.0 / 14):
        """

        :param base_path: location to save animation 
        :param name: name of animation
        :param style: same as matplotlib.style.set mainly a dict with rcparams key-value pairs.
        These params will be applied to all subplots
        """
        self.base_path = base_path
        self.name = name
        self.dt = dt
        self.images = []
        self.traces = []
        self.labels = []
        self.annotations = []
        self.axes = []
        if style is not None:
            plt.style.use(style)
        self.styles = copy.deepcopy(plt.style.library)  # type: dict
        self._add_styles()

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
                         u'image.interpolation': 'None'})
        styles[u'dark_img'] = dark_img

        light_img = copy.deepcopy(default)
        light_img.update({u'axes.spines.top': False, u'axes.spines.right': False,
                          u'axes.spines.bottom': False, u'axes.spines.left': False,
                          u'axes.facecolor': (1, 1, 1, 0), u'axes.edgecolor': (1, 1, 1, 0),
                          u'xtick.color': (1, 1, 1, 0), u'ytick.color': (1, 1, 1, 0), u'grid.alpha': 0,
                          u'image.interpolation': 'None'})
        styles[u'light_img'] = light_img

        dark_trace = copy.deepcopy(dark_background)
        dark_trace.update({u'axes.spines.top': False, u'axes.spines.right': False,
                           u'axes.spines.bottom': False, u'axes.spines.left': False,
                           u'axes.facecolor': (1, 1, 1, 0), u'axes.edgecolor': (1, 1, 1, 0),
                           u'xtick.color': (1, 1, 1, 0), u'ytick.color': (1, 1, 1, 0), u'grid.alpha': 0,
                           u'image.interpolation': 'None'})
        styles[u'dark_trace'] = dark_trace

        light_trace = copy.deepcopy(default)
        light_trace.update({u'axes.spines.top': False, u'axes.spines.right': False,
                            u'axes.spines.bottom': False, u'axes.spines.left': False,
                            u'axes.facecolor': (1, 1, 1, 0), u'axes.edgecolor': (1, 1, 1, 0),
                            u'xtick.color': (1, 1, 1, 0), u'ytick.color': (1, 1, 1, 0), u'grid.alpha': 0,
                            u'image.interpolation': 'None'})
        styles[u'light_trace'] = light_trace

        self.styles.update(styles)

    def add_label(self, values, axis=0, location=(0.01, 0.9), s_format='%', size=14, **kwargs):
        """
        
        :param values: list of values
        :param axis: axis number to add the label to
        :param location: where to add the label in axis coordinates
        :param s_format: string format to use on the values
        :param size: font size
        :param kwargs: to be sent to the plt.text function
        :return: 
        """
        local_vars = locals()
        del local_vars['self']
        self.labels.append(local_vars)

    def add_time_label(self, values=None, axis=0, location=(0.01, 0.08), s_format='%.2fs', size=14, **kwargs):
        if values is None:
            if len(self.images) == 0:
                if len(self.traces) == 0:
                    raise RuntimeError('Can not add time labels when no values are given and no data was added')
                else:
                    values = np.arange(self.traces[0]['data'].shape[0]) * self.dt
            else:
                values = np.arange(self.images[0]['data'].shape[0]) * self.dt
        self.add_label(values, axis, location, s_format, size, kwargs)

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

    def add_scale_bar(self, axis=0, pixel_width=40, um_width='20'):
        """

        :param axis:
        :param pixel_width:
        :param um_width:
        :return:
        """
        self.add_line_annotation(axis=axis, x=(0, pixel_width), y=(2, 2), color='white', lw=3)
        mid = int(pixel_width / 2)
        self.add_text_annotation(axis=axis, x=mid, y=mid, text=um_width + 'um', ha='center', fontsize=14, color='white')

    def _get_ylim(self, ylim_type, ylim_value, data):
        """

        :param ylim_type: 
        :param ylim_value: 
        :param data: 
        :return: 
        """
        if ylim_type == 'set':
            assert len(ylim_value) == 2
            return ylim_value[0], ylim_value[1]
        elif ylim_type == 'same':
            assert len(self.img_list) < ylim_value
            return self.img_list[ylim_value]['ymin'], self.img_list[ylim_value]['ymax']
        elif ylim_type == 'p_top':
            return np.nanpercentile(data, 100.0 - ylim_value), np.nanmin(data)
        elif ylim_type == 'p_bottom':
            return np.nanmax(data), np.nanpercentile(data, ylim_value)
        elif ylim_type == 'p_both':
            return np.nanpercentile(data, 100.0 - ylim_value), np.nanpercentile(data, ylim_value)
        else:
            raise RuntimeError("Expected 'p_top', 'p_bottom', 'p_both', 'set' or 'same' got: %s" % ylim_type)

    def add_image(self, data, name, style='dark_img', c_title=None, ylim_type='p_top', ylim_value=0.1):
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
        img = dict()
        img['data'] = data
        img['style'] = style
        img['c_title'] = c_title
        img['ymax'], img['ymin'] = self._get_ylim(ylim_type, ylim_value, data)
        self.images.append(img)

    def add_trace(self, data, axis=0, name=None, ylim_type='p_top', ylim_value=0.1):
        if len(self.axes) <= axis:
            raise RuntimeError('Please create axis %d before adding traces' % axis)
        trace = dict()
        trace['data'] = data
        trace['name'] = name
        trace['axis'] = axis
        trace['ymax'], trace['ymin'] = self._get_ylim(ylim_type, ylim_value, data)
        self.traces.append(trace)

    def add_axis(self, x_label, y_label, style='dark_trace', running_line=True):
        """

        :param x_label:
        :param y_label:
        :param style:
        :param running_line:
        :return:
        """
        local_vars = locals()
        del local_vars['self']
        print(local_vars.keys())
        self.axes.append(local_vars)

    def add_traces(self):
        pass


a = Animation('a', 'b', None)
a.add_axis('time','dff')
a.add_trace([1,2,3,4,5,6,7,], 0, 'try1')