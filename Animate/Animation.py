from __future__ import print_function, division, unicode_literals

import copy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import TimedAnimation
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
import matplotlib.patches as patches


class Animation(TimedAnimation):
    """

    """

    def __init__(self, movie, fps=1):
        """

        :param movie:
        """
        self.x_data = None
        self.movie = movie
        self.n_images = len(movie.images)
        if self.n_images == 0:
            raise RuntimeError('At least one image is needed')
        self.n_axes = len(movie.axes)
        self._make_x_data()
        # figure
        if movie.fig_kwargs is not None:
            self.fig = plt.figure(**movie.fig_kwargs)
        else:
            self.fig = plt.figure()
        rect = self.fig.patch
        rect.set_facecolor(self.movie.fig_color)
        TimedAnimation.__init__(self, self.fig, interval=1.0 / fps * 1000, blit=True)

    def _init_labels(self):
        for label in self.movie.labels:
            ax = self.img_axes[label['axis']]
            l = ax.text(label['x'], label['y'], '', size=label['size'],
                        transform=ax.transAxes, **label['kwargs'])
            self.labels.append(l)

    def _init_annotations(self):
        for annotation in self.movie.annotations:
            if annotation['axis_type'] == 'image':
                ax = self.img_axes[annotation['axis']]
            elif annotation['axis_type'] == 'trace':
                ax = self.trace_axes[annotation['axis']]
            else:
                raise ValueError('annotation axis_type is not "image" or "trace": %s' % annotation['axis_type'])
            if annotation['type'] == 'text':
                ax.text(annotation['x'], annotation['y'], annotation['text'], **annotation['kwargs'])
            elif annotation['type'] == 'line':
                line = Line2D(annotation['x'], annotation['y'], **annotation['kwargs'])
                ax.add_line(line)
            elif annotation['type'] == 'circle':
                c = plt.Circle((annotation['x'], annotation['y']), annotation['radius'], axes=ax,
                               **annotation['kwargs'])
                ax.add_patch(c)
            elif annotation['type'] == 'annotation':
                ax.annotate(annotation['text'], xy=annotation['xy'], xytext=annotation['xy_text'],
                            **annotation['kwargs'])
            elif annotation['type'] == 'rectangle':
                r = patches.Rectangle(xy=annotation['xy'], width=annotation['width'], height=annotation['height'],
                                      angle=annotation['angle'], **annotation['kwargs'])
                ax.add_patch(r)
            else:
                raise ValueError('Annotation type is wrong: %s' % annotation['type'])

    def _init_traces(self):
        trace_axis = np.array(list(map(lambda x: x['axis'], self.movie.traces)))
        # for each axis
        for i, axis in enumerate(self.movie.axes):
            axis['legend_handles'] = []
            # set correct style
            with plt.style.context(axis['style'], after_reset=True):

                # get the color cycle
                colors = plt.style.library[axis['style']].get('axes.prop_cycle')
                colors = list(map(lambda x: x['color'], list(colors)))
                ax = self.fig.add_subplot(self.gs[i + 1, :], **axis['kwargs'])
                self.trace_axes.append(ax)

                ax.set_xlabel(axis['x_label'], **axis['label_kwargs'])
                ax.set_ylabel(axis['y_label'], **axis['label_kwargs'])
                if axis['bottom_left_ticks']:
                    ax.yaxis.set_ticks_position('left')
                    ax.xaxis.set_ticks_position('bottom')

                # find the traces that belong to this axis
                trace_index = np.where(trace_axis == i)[0]
                if len(trace_index) == 0:
                    raise RuntimeError('Axis %d with no traces' % i)
                all_data = []
                for j, index in enumerate(trace_index):
                    trace = self.movie.traces[index]
                    if 'color' in trace['kwargs']:
                        line = Line2D(self.x_data, trace['data'], **trace['kwargs'])
                    else:
                        # use the default from the color cycle
                        line = Line2D(self.x_data, trace['data'], color=colors[j], **trace['kwargs'])
                    if 'label' in trace['kwargs']:
                        axis['legend_handles'].append(line)
                    ax.add_line(line)
                    all_data.append(copy.deepcopy(trace['data']))
                    self.traces.append(line)
                if len(all_data) > 1:
                    all_data = np.concatenate(all_data)
                else:
                    all_data = all_data[0]
                if axis['ylim_type'] == 'same':
                    if axis['ylim_value'] >= self.n_axes:
                        raise RuntimeError('Tried to have same y limits as %d but # of axes is %d' %
                                           (axis['ylim_value'], len(self.images)))
                    else:
                        y_min, y_max = self.trace_axes[axis['ylim_value']].get_ylim()
                else:
                    y_min, y_max = self.movie.get_ylim(axis['ylim_type'], axis['ylim_value'], all_data)
                ax.set_ylim(y_min, y_max)
                if axis['tight_x']:
                    ax.set_xlim([min(self.x_data), max(self.x_data)])
                if len(axis['legend_handles']) > 0:
                    ax.legend(handles=axis['legend_handles'], **axis['legend_kwargs'])
                # running line
                if axis['running_line'] is not None:
                    movie = self.movie.images[0]
                    if movie['animation_type'] == 'movie':
                        run_line = Line2D([], [], **axis['running_line'])
                        ax.add_line(run_line)
                        self.running_lines.append(run_line)
                    else:
                        patch_x = (movie['window_size'] // 2 * -1 - 1) * self.movie.dt
                        r = patches.Rectangle(xy=(patch_x, y_min), width=movie['window_size'] * self.movie.dt,
                                              height=y_max - y_min, angle=0, **axis['running_line'])
                        ax.add_patch(r)
                        self.running_lines.append(r)

    def _init_images(self):
        for i, image in enumerate(self.movie.images):
            with plt.style.context(image['style'], after_reset=True):
                ax = self.fig.add_subplot(self.gs[0, i])
                self.img_axes.append(ax)
                if image['animation_type'] == 'movie':
                    im = ax.imshow(image['data'][0, :, :], animated=True, vmin=image['ymin'],
                                   vmax=image['ymax'])
                elif image['animation_type'] == 'window':
                    if image['is_rgb']:
                        im = ax.imshow(image['data'][:, :image['window_size'], :], animated=True, vmin=image['ymin'],
                                       vmax=image['ymax'])
                    else:
                        im = ax.imshow(image['data'][:, :image['window_size']], animated=True, vmin=image['ymin'],
                                       vmax=image['ymax'])
                    ax.set_aspect('auto')
                self.images.append(im)
                if image['c_title'] is not None:
                    with plt.style.context(image['c_style'], after_reset=True):
                        plt.colorbar(im, ax=ax, label=image['c_title'])

    def _make_x_data(self):
        # for now we assume that either all animation types are 'movie' or 'window'
        movie = self.movie.images[0]
        img = movie['data']

        if movie['animation_type'] == 'movie':
            for m in self.movie.images:
                if m['animation_type'] != 'movie':
                    raise NotImplementedError('All animation types should be the same as the first -- "movie"')
            length = img.shape[0]
            self.x_data = np.arange(length) * self.movie.dt
        elif movie['animation_type'] == 'window':
            for m in self.movie.images:
                if m['animation_type'] != 'window':
                    raise NotImplementedError('All animation types should be the same as the first -- "movie"')
            length = img.shape[1]
            window_length = movie['window_size']
            self.x_data = (np.arange(length) - window_length // 2) * self.movie.dt

    def _draw_frame(self, frame):
        print(frame, end=', ')
        drawn_artist = []
        # images
        for im, image in zip(self.images, self.movie.images):
            if image['animation_type'] == 'movie':
                im.set_array(image['data'][frame, :, :])
            elif image['animation_type'] == 'window':
                start = frame
                stop = frame + image['window_size']
                if image['is_rgb']:
                    im.set_array(image['data'][:, start:stop, :])
                else:
                    im.set_array(image['data'][:, start:stop])
            drawn_artist.append(im)
        # labels
        for label, data in zip(self.labels, self.movie.labels):
            label.set_text(data['s_format'] % data['values'][frame])
            drawn_artist.append(label)
        # running lines
        if self.n_axes > 0:
            for line in self.running_lines:
                y_limits = line.axes.get_ylim()
                if self.movie.images[0]['animation_type'] == 'movie':
                    line.set_data([self.x_data[frame], self.x_data[frame]], [y_limits[0], y_limits[1]])
                else:
                    x, y = line.xy
                    x += self.movie.images[0]['window_step'] * self.movie.dt
                    line.xy = (x, y)
                    # x_loc = self.x_data[frame] + self.movie.images[0]['window_size'] // 2
                    # line.set_data([x_loc, x_loc], [y_limits[0], y_limits[1]])
                drawn_artist.append(line)
        self._drawn_artists = drawn_artist

    def new_frame_seq(self):
        if self.movie.images[0]['animation_type'] == 'movie':
            return iter(range(self.movie.images[0]['data'].shape[0]))
        elif self.movie.images[0]['animation_type'] == 'window':
            img = self.movie.images[0]
            length = img['data'].shape[1] - img['window_size']
            return iter(range(0, length, img['window_step']))

    def _init_draw(self):
        if self.n_axes > 0:
            height_ratios = (self.n_axes * self.movie.height_ratio,) + (1,) * self.n_axes
            self.gs = GridSpec(1 + self.n_axes, self.n_images, height_ratios=height_ratios)
        else:
            self.gs = GridSpec(1, self.n_images)
            # images
        self.img_axes = []
        self.images = []
        self._init_images()
        # traces
        if self.n_axes > 0:
            self.trace_axes = []
            self.traces = []
            self.running_lines = []
            self._init_traces()
        # annotations
        self._init_annotations()
        # labels
        self.labels = []
        self._init_labels()
