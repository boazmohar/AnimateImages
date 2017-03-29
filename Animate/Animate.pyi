from numpy import ndarray

class Animation:
    def __init__(self, base_path: str, name: str, style: tuple, dt: float):
        pass
    def add_label(self, axis: int, location: tuple, s_format: str, size: int):
        pass

    def add_time_label(self, axis: int, location: tuple, s_format: str, size: int):
        pass

    def add_image_plot(self, data: ndarray, ylim_type: str):
        pass