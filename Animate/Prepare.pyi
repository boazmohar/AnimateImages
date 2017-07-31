from numpy import ndarray
from typing import Union, List

class Prepare:
    def __init__(self, base_path: str, name: str, style: Union(tuple, str), dt: float,
                 fig_kwargs:Union(None, dict)={'figsize': (10, 10)}):
        self.traces: List(dict) = []
        self.images: List(dict) = []
        self.annotations: List(ndarray) = []
        self.labels: List(dict) = []
        self.styles: list = []
        self.axes: List(dict) = []
        self.dt = dt
        self.fig_kwargs = fig_kwargs

    def add_label(self, values: Union(ndarray, list), axis: int, location: tuple, s_format: str, size: int, kwargs: dict):
        pass

    def add_time_label(self, values: Union(ndarray, list), axis: int, location: tuple, s_format: str, size: int):
        pass

    def add_behavior_label(self, values: Union(ndarray, list), axis: int, location: tuple, s_format: str, size: int,
                           kwargs: dict):
        pass

    def add_line_annotation(self, axis: int, x: int, y: int, kwargs: dict):
        pass

    def add_text_annotation(self, axis: int, x: int, y: int, text: str, kwargs: dict):
        pass

    def add_scale_bar(self, axis: int=0, pixel_width:int =40, um_width: str='20'):
        pass
    def add_image(self, data: ndarray, ylim_type: str='p_top', ylim_value: Union(float, tuple, list)=0.1):
        pass

    def _add_styles(self):
        pass
    def add_trace(self, data: ndarray, axis: int=0, name: Union(None, str)=None, ylim_type: str='p_top',
                  ylim_value: Union(float, tuple, list)=0.1):
        pass
    def add_axis(self, x_label: str, y_label: str, style: Union(tuple, str)='dark_trace', running_line: bool=True):
        pass
