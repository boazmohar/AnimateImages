from types import Union, List

from matplotlib.animation import TimedAnimation
from matplotlib.axis import Axis
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib.lines import Line2D
from matplotlib.text import Text
from numpy import ndarray

from Animate import Prepare


class Animation(TimedAnimation):
    """

    """
    def __init__(self, prepare: Prepare):
        self.x_data: Union(None, ndarray)= None
        self.prepare: Prepare = prepare
        self.n_images: int = 0
        self.n_axes: int = 0
        self.fig: Figure = None
        self.img_axes: List(Axis) = []
        self.images: List(AxesImage) = []
        self.trace_axes: List(Axis) = []
        self.traces: List(Line2D) = []
        self.running_lines: List(Line2D) = []
        self.labels: List(Text) = []


    def init_labels(self):
        pass

    def init_annotations(self):
        pass

    def init_traces(self):
        pass

    def init_images(self):
        pass

    def make_x_data(self):
        pass

    def _draw_frame(self, frame):
        pass

    def new_frame_seq(self):
        pass

    def _init_draw(self):
        pass
