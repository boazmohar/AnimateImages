from __future__ import print_function
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


class Animation:
    """ Class to make animation of movies with traces
    Default behavior is to add all image animation to the top row of subplots 
    and add all the trace animation plots to the second row

    """

    def __init__(self, base_path, name, style=None, dt=1.0 / 14):
        """
        
        :param base_path: location to save animation 
        :param name: nae of animation
        :param style: same as matplotlib.style.set mainly a dict with rcparams key-value pairs.
        These params will be applied to all subplots
        """
        self.base_path = base_path
        self.name = name
        self.dt = dt
        self.img_list = []
        self.trace_list = []
        self.label_list = []
        self.n_img_plots = 0
        self.n_trace_plots = 0
        if style is not None:
            plt.style.use(style)
        self.styles = copy.deepcopy(plt.style.library)
        self._add_styles()

    def _add_styles(self):
        """ Add 4 new styles to the original matplotlib library: dark and light version for images and traces
        
        """
        styles = dict()
        default = mpl.rcParamsDefault
        dark_background = plt.style.library['dark_background']

        dark_img = copy.deepcopy(dark_background)
        dark_img.update({u'axes.spines.top': False, 'axes.spines.right': False,
                         u'axes.spines.bottom': False, 'axes.spines.left': False,
                         u'axes.facecolor': (1, 1, 1, 0), 'axes.edgecolor': (1, 1, 1, 0),
                         u'xtick.color': (1, 1, 1, 0), 'ytick.color': (1, 1, 1, 0), 'grid.alpha': 0,
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

    def add_label(self, axis=0, location=(0.01, 0.9), s_format='%', size=14):
        self.label_list.append({'axis': axis, 'location': location, 'format': s_format, 'size': size})

    def add_time_label(self, axis=0, location=(0.01, 0.08), s_format='%.2fs', size=14):
        self.add_label(axis, location, s_format, size)

    def add_image_plot(self, data, style='dark_img', c_title=None, ylim_type='p_top', ylim_value=0.1):
        """
        
        :param data: 3d array (n, x, y)
        :param c_title: title to put on the color bar
        :param ylim_type: how to set the y limits. 'p_top' will clip the top ylim_value values in %. \
            'p_bottom' same for bottom % pixels. 'p_both' will clip both ends. 'set' will expect a tuple [min max] \
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

        # get ylim
        if ylim_type == 'set':
            assert len(ylim_value) == 2
            img['ymin'] = ylim_value[0]
            img['ymax'] = ylim_value[1]
        elif ylim_type == 'same':
            assert len(self.img_list) < ylim_value
            img['ymin'] = self.img_list[ylim_value]['ymin']
            img['ymax'] = self.img_list[ylim_value]['ymax']
        elif ylim_type == 'p_top':
            img['ymax'] = np.nanpercentile(data, 100.0 - ylim_value)
            img['ymin'] = np.nanmin(data)
        elif ylim_type == 'p_bottom':
            img['ymax'] = np.nanmax(data)
            img['ymin'] = np.nanpercentile(data, ylim_value)
        elif ylim_type == 'p_both':
            img['ymax'] = np.nanpercentile(data, 100.0 - ylim_value)
            img['ymin'] = np.nanpercentile(data, ylim_value)
        else:
            raise RuntimeError("Expected 'p_top', 'p_top', 'p_top', 'set' or 'same' got: %s" % ylim_type)
        self.img_list.append(img)
