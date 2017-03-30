from numpy import ndarray
from typing import Union

class Animation:
    def __init__(self, base_path: str, name: str, style: Union(tuple, str), dt: float):
        self.dt = 0
        self.trace_list = []
        self.img_list = []
        self.label_list = []
        self.styles = []

    def add_label(self, values: Union(ndarray, list), axis: int, location: tuple, s_format: str, size: int):
        pass

    def add_time_label(self, values: Union(ndarray, list), axis: int, location: tuple, s_format: str, size: int):
        pass

    def add_image_plot(self, data: ndarray, ylim_type: str, ylim_value: Union(float, tuple, list)):
        pass

    def _add_styles(self):
        pass