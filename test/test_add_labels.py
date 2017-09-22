import pytest
import numpy as np
from Animate.Movie import Movie
from Animate.Animation import Animation


def test_label():
    m = Movie(dt=1.0/14, height_ratio=2)
    m.add_label(1, 2, [1, 2], color='blue')
    assert m.labels[0]['x'] == 1
    assert m.labels[0]['y'] == 2
    assert m.labels[0]['values'] == [1, 2]
    assert m.labels[0]['axis'] == 0
    assert m.labels[0]['s_format'] == '%s'
    assert m.labels[0]['size'] == 14
    kwargs = m.labels[0]['kwargs']
    assert kwargs['color'] == 'blue'


def test_time_label_fail():
    m = Movie(dt=1.0 / 14, height_ratio=2)
    with pytest.raises(RuntimeError) as ex:
        m.add_time_label()
    assert 'Can not add time labels' in str(ex.value)


def test_time_label_image():
    m = Movie(dt=1.0 / 14, height_ratio=2)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.add_time_label(color='blue')
    assert m.labels[0]['x'] == 0.01
    assert m.labels[0]['y'] == 0.08
    assert np.allclose(m.labels[0]['values'], np.arange(4) / 14.0)
    assert m.labels[0]['axis'] == 0
    assert m.labels[0]['s_format'] == '%.2fs'
    assert m.labels[0]['size'] == 14
    kwargs = m.labels[0]['kwargs']
    assert kwargs['color'] == 'blue'


def test_time_label_axis():
    m = Movie(dt=1.0 / 14, height_ratio=2)
    m.add_axis(x_label='x', y_label='y')
    m.add_trace(data=np.arange(10))
    m.add_time_label(color='blue')
    assert m.labels[0]['x'] == 0.01
    assert m.labels[0]['y'] == 0.08
    assert np.allclose(m.labels[0]['values'], np.arange(10) / 14.0)
    assert m.labels[0]['axis'] == 0
    assert m.labels[0]['s_format'] == '%.2fs'
    assert m.labels[0]['size'] == 14
    kwargs = m.labels[0]['kwargs']
    assert kwargs['color'] == 'blue'
