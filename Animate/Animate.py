from __future__ import print_function, division

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import TimedAnimation
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D


class Animation(TimedAnimation):
    """

    """

    def __init__(self, movie):
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
        TimedAnimation.__init__(self, self.fig, interval=70, blit=True)

    def _init_labels(self):
        for label in self.movie.labels:
            ax = self.img_axes[label['axis']]
            l = ax.text(label['x'], label['y'], label['s_format'] % label['values'][0], size=label['size'],
                        transform=ax.transAxes, **label['kwargs'])
            self.labels.append(l)

    def _init_annotations(self):
        for annotation in self.movie.annotations:
            ax = self.img_axes[annotation['axis']]
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
            else:
                raise RuntimeError('Annotation type is wrong: %s' % annotation['type'])

    def _init_traces(self):
        gs = GridSpec(1 + self.n_axes, self.n_images, height_ratios=self.movie.height_ratios)
        trace_axis = np.array(map(lambda x: x['axis'], self.movie.traces))

        # for each axis
        for i, axis in enumerate(self.movie.axes):
            # set correct style
            with plt.style.context(axis['style'], after_reset=True):

                # get the color cycle
                colors = plt.style.library[axis['style']].get('axes.prop_cycle')
                colors = map(lambda x: x['color'], list(colors))
                ax = self.fig.add_subplot(gs[i + 1, :])
                self.trace_axes.append(ax)

                ax.set_xlabel(axis['x_label'])
                ax.set_ylabel(axis['y_label'])
                if axis['bottom_left_ticks']:
                    ax.yaxis.set_ticks_position('left')
                    ax.xaxis.set_ticks_position('bottom')
                # running line
                if axis['running_line'] is not None:
                    run_line = Line2D([], [], **axis['running_line'])
                    ax.add_line(run_line)
                    self.running_lines.append(run_line)

                # find the traces that belong to this axis
                trace_index = np.where(trace_axis == i)[0]
                for j, index in enumerate(trace_index):
                    trace = self.movie.traces[index]
                    if 'color' in trace['kwargs']:
                        line = Line2D(self.x_data, trace['data'], **trace['kwargs'])
                    else:
                        # use the default from the color cycle
                        line = Line2D(self.x_data, trace['data'], color=colors[j], **trace_axis['kwargs'])
                    ax.add_line(line)
                    self.traces.append(line)

                    if j == 0:
                        ax.set_ylim(trace['ymin'], trace['ymax'])
                        ax.set_xlim(0, self.x_data.max())
                    else:
                        y_min, y_max = ax.get_ylim()
                        ax.set_ylim(min([trace['ymin'], y_min]), max([trace['ymax'], y_max]))

    def _init_images(self):
        gs = GridSpec(1 + self.n_axes, self.n_images, height_ratios=self.movie.height_ratios)
        for i, image in enumerate(self.movie.images):
            with plt.style.context(image['style'], after_reset=True):
                ax = self.fig.add_subplot(gs[0, i])
                self.img_axes.append(ax)
                im = ax.imshow(image['data'][0, :, :], animated=True, vmin=image['ymin'],
                               vmax=image['ymax'])
                self.images.append(im)
                if image['c_title'] is not None:
                    with plt.style.context(image['c_style'], after_reset=True):
                        plt.colorbar(im, ax=ax, label=image['c_title'])

    def _make_x_data(self):
        img = self.movie.images[0]['data']
        length = img.shape[0]
        self.x_data = np.arange(length) * self.movie.dt

    def _draw_frame(self, frame):
        drawn_artist = []
        # images
        for im, image in zip(self.images, self.movie.images):
            im.set_array(image['data'][frame, :, :])
            drawn_artist.append(im)
        # labels
        for label, data in zip(self.labels, self.movie.labels):
            label.set_text(data['s_format'] % data['values'][frame])
            drawn_artist.append(label)
        # running lines
        for line in self.running_lines:
            y_limits = line.axes.get_ylim()
            line.set_data([self.x_data[frame], self.x_data[frame]], [y_limits[0], y_limits[1]])
            drawn_artist.append(line)
        self._drawn_artists = drawn_artist

    def new_frame_seq(self):
        return iter(range(self.movie.images[0]['data'].shape[0]))

    def _init_draw(self):
        pass
