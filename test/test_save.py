import pytest
import subprocess
import os.path
import numpy as np
from Animate.Movie import Movie
from matplotlib.animation import writers
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = u'/opt/ffmpeg/bin/ffmpeg'


@pytest.mark.skipif(len(writers.avail) == 0, reason='No writers to save with')
def test_imagemagick(tmpdir):
    path = tmpdir.join('test').relto('')
    m = Movie(dt=1.0/14, height_ratio=2)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    if 'ffmpeg' in writers.avail:
        del writers.avail['ffmpeg']
    m.save(path)
    assert os.path.isfile(path + '.gif')


def test_save_fail(tmpdir):
    path = tmpdir.join('test').relto('')
    writers.avail = []
    m = Movie(dt=1.0 / 14, height_ratio=2)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    with pytest.raises(ValueError) as ex:
        m.save(path)
    assert 'Could not find "ffmpeg" and "imagemagick"' in str(ex.value)


@pytest.mark.skipif('ffmpeg' not in writers.avail, reason='No ffmpeg to save with')
def test_ffmpeg(tmpdir):
    path = tmpdir.join('test2').relto('')
    m = Movie(dt=1.0/14, height_ratio=2)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.save(path)
    assert os.path.isfile(path + '.mp4')
