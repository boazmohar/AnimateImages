from numpy import ndarray
from typing import Union, List

class Movie:
    def __init__(self, base_path: str, name: str, style: Union(tuple, str), dt: float,
                 fig_kwargs:Union(None, dict)={'figsize': (10, 10)}, fig_color: string='black',
                 height_ratio: float=2):
        self.base_path: str
        self.name: str
        self.dt : float = dt
        self.fig_color: str
        self.height_ratio: float
        self.fig_kwargs: dict
        self.traces: List(dict) = []
        self.images: List(dict) = []
        self.annotations: List(ndarray) = []
        self.labels: List(dict) = []
        self.styles: list = []
        self.axes: List(dict) = []


    def _add_styles(self):
        pass

    def add_label(self, x: float, y: float, values: Union(ndarray, list), axis: int, s_format: str, size: int, kwargs: dict):
        pass

    def add_time_label(self, x: float, y: float, values: Union(ndarray, list), axis: int, s_format: str, size: int,
                       kwargs: dict):
        pass

    def add_behavior_label(self, x: float, y: float, values: Union(ndarray, list), axis: int, s_format: str, size: int,
                           kwargs: dict):
        pass

    def add_annotation(self, axis: int, xy: tuple, xy_text: tuple, text: str, kwargs: dict):
        pass

    def add_line_annotation(self, axis: int, x: int, y: int, kwargs: dict):
        pass

    def add_text_annotation(self, axis: int, x: int, y: int, text: str, kwargs: dict):
        pass

    def add_circle_annotation(self, axis: int, x: int, y: int, radius: int, **kwargs):
        pass

    def add_scale_bar(self, axis: int=0, pixel_width:int =40, um_width: str='20'):
        pass

    def get_ylim(self, ylim_type: str, ylim_value: Union(tuple, float), data: ndarray):
        pass

    def add_image(self, data: ndarray, style:Union(str, list), c_title: Union(None, str)=None,
                  c_style: Union(list, str)='dark_background', ylim_type: str='p_top',
                  ylim_value: Union(float, tuple, list)=0.1):
        pass

    def add_trace(self, data: ndarray, axis: int=0, name: Union(None, str)=None):
        pass

    def add_axis(self, x_label: str, y_label: str, style: Union(tuple, str)='dark_trace',
                 running_line: dict={'color': 'white', 'lw': 2}, bottom_left_ticks: bool=True, ylim_type: str='p_top',
                 ylim_value: Union(float, tuple, list)=0.1):
        pass
