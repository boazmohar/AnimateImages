import pytest
import subprocess
import os.path
import numpy as np
from Animate.Movie import Movie
from matplotlib.animation import writers


@pytest.mark.skipif(len(writers.avail) == 0, reason='No writers to save with')
def test_save(tmpdir):
    path = tmpdir.join('test').relto('')
    m = Movie(dt=1.0/14, height_ratio=2)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.save(path)
    assert os.path.isfile(path + '.mp4') or os.path.isfile(path + '.gif')


def test_save_fail(tmpdir):
    path = tmpdir.join('test').relto('')
    writers.avail = []
    m = Movie(dt=1.0 / 14, height_ratio=2)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    with pytest.raises(ValueError) as ex:
        m.save(path)
    assert 'Could not find "ffmpeg" and "imagemagick"' in str(ex.value)
    

def test_ffmpeg():
    path = subprocess.check_output("locate ffmpeg", shell=True)
    print(path)
    assert path == ''
