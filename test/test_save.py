import pytest
import os
import numpy as np
from Animate.Movie import Movie
from matplotlib.animation import writers
import matplotlib.pyplot as plt


@pytest.yield_fixture(autouse=True, scope='module')
def set_ffmpeg_path_travis():
    print(plt.rcParams['animation.ffmpeg_path'])
    if os.environ.get('TRAVIS_PYTHON_VERSION') is not None:
        plt.rcParams['animation.ffmpeg_path'] = u'/opt/ffmpeg/bin/ffmpeg'


@pytest.mark.skipif('imagemagick' not in writers.avail, reason='No imagemagick to save with')
def test_imagemagick(tmpdir):
    path = tmpdir.join('test').relto('')
    m = Movie(dt=1.0/14, height_ratio=2)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.save(path, writer_name='imagemagick')
    assert os.path.isfile(path + '.gif')


@pytest.mark.skipif('ffmpeg' not in writers.avail, reason='No ffmpeg to save with')
def test_ffmpeg(tmpdir):
    path = tmpdir.join('test2').relto('')
    m = Movie(dt=1.0/14, height_ratio=2)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.save(path)
    assert os.path.isfile(path + '.mp4')


def test_save_fail(tmpdir):
    path = tmpdir.join('test').relto('')
    writers.avail = []
    m = Movie(dt=1.0 / 14, height_ratio=2)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    with pytest.raises(ValueError) as ex:
        m.save(path)
    assert 'Could not find' in str(ex.value)
