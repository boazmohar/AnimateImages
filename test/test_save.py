import pytest
import os.path
import numpy as np
from Animate.Movie import Movie
from matplotlib.animation import writers


@pytest.mark.skipif(len(writers.avail) == 0, 'No writers to save with')
def test_save(tmpdir):
    path = tmpdir.join('test').relto('')
    m = Movie(dt=1.0/14, height_ratio=2)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.save(path)
    assert os.path.isfile(path + '.mp4') or os.path.isfile(path + '.gif')
