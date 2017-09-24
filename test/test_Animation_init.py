import pytest
import numpy as np
from Animate.Movie import Movie
from Animate.Animation import Animation
import matplotlib as mpl


def test_ratio_2():
    m = Movie(dt=1.0/14, height_ratio=2)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    a = Animation(m)
    a._init_draw()
    assert a.gs.get_geometry() == (1, 1)
    assert a.gs.get_height_ratios() is None

    m = Movie(dt=1.0/14, height_ratio=2)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.add_axis('x', 'y')
    m.add_trace(np.arange(4))
    a = Animation(m)
    a._init_draw()
    assert a.gs.get_geometry() == (2, 1)
    assert a.gs.get_height_ratios() == (2, 1)

    m = Movie(dt=1.0 / 14, height_ratio=2)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.add_axis('x', 'y')
    m.add_trace(np.arange(4))
    m.add_axis('x', 'y')
    m.add_trace(np.arange(4), axis=1)
    a = Animation(m)
    a._init_draw()
    assert a.gs.get_geometry() == (3, 1)
    assert a.gs.get_height_ratios() == (4, 1, 1)


def test_ratio_1():
    m = Movie(dt=1.0 / 14, height_ratio=1)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    a = Animation(m)
    a._init_draw()
    assert a.gs.get_geometry() == (1, 1)
    assert a.gs.get_height_ratios() is None

    m = Movie(dt=1.0 / 14, height_ratio=1)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.add_axis('x', 'y')
    m.add_trace(np.arange(4))
    a = Animation(m)
    a._init_draw()
    assert a.gs.get_geometry() == (2, 1)
    assert a.gs.get_height_ratios() == (1, 1)

    m = Movie(dt=1.0 / 14, height_ratio=1)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.add_axis('x', 'y')
    m.add_trace(np.arange(4))
    m.add_axis('x', 'y')
    m.add_trace(np.arange(4), axis=1)
    a = Animation(m)
    a._init_draw()
    assert a.gs.get_geometry() == (3, 1)
    assert a.gs.get_height_ratios() == (2, 1, 1)


def test_ratio_1p5():
    m = Movie(dt=1.0 / 14, height_ratio=1.5)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    a = Animation(m)
    a._init_draw()
    assert a.gs.get_geometry() == (1, 1)
    assert a.gs.get_height_ratios() is None

    m = Movie(dt=1.0 / 14, height_ratio=1.5)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.add_axis('x', 'y')
    m.add_trace(np.arange(4))
    a = Animation(m)
    a._init_draw()
    assert a.gs.get_geometry() == (2, 1)
    assert a.gs.get_height_ratios() == (1.5, 1)

    m = Movie(dt=1.0 / 14, height_ratio=1.5)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.add_axis('x', 'y')
    m.add_trace(np.arange(4))
    m.add_axis('x', 'y')
    m.add_trace(np.arange(4), axis=1)
    a = Animation(m)
    a._init_draw()
    assert a.gs.get_geometry() == (3, 1)
    assert a.gs.get_height_ratios() == (3, 1, 1)


def test_n_axis():
    with pytest.raises(RuntimeError) as ex:
        m = Movie(dt=1.0 / 14, height_ratio=1.5)
        _ = Animation(m)
    assert 'At least one image is needed' in str(ex.value)

    m = Movie(dt=1.0 / 14, height_ratio=1.5)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    a = Animation(m)
    a._init_draw()
    assert a.n_axes == 0
    assert a.n_images == 1

    m = Movie(dt=1.0 / 14, height_ratio=1.5)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.add_image(img, style='dark_img')
    a = Animation(m)
    a._init_draw()
    assert a.n_axes == 0
    assert a.n_images == 2

    m = Movie(dt=1.0 / 14, height_ratio=1.5)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.add_axis('x', 'y')
    with pytest.raises(RuntimeError) as ex:
        a = Animation(m)
        a._init_draw()
    assert 'Axis 0 with no traces' in str(ex.value)

    m = Movie(dt=1.0 / 14, height_ratio=1.5)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    m.add_axis('x', 'y')
    m.add_trace(np.arange(4))
    a = Animation(m)
    a._init_draw()
    assert a.n_axes == 1
    assert a.n_images == 1


def test_x_data():
    m = Movie(dt=1.0 / 14, height_ratio=1.5)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img')
    a = Animation(m)
    assert np.allclose(a.x_data, np.arange(4) * 1.0 / 14)

    m = Movie(dt=0.5, height_ratio=1.5)
    img = np.arange(1000).reshape(40, 5, 5)
    m.add_image(img, style='dark_img')
    a = Animation(m)
    assert np.allclose(a.x_data, np.arange(40) * 0.5)

    m = Movie(dt=1)
    img = np.arange(100).reshape(5, 20)
    m.add_image(img, animation_type='window', window_size=5)
    m.add_axis('x', 'y')
    m.add_trace(np.arange(20))
    a = Animation(m)
    assert np.allclose(a.x_data, np.arange(20) - 5 // 2)

    m = Movie(dt=1)
    img = np.arange(100).reshape(5, 20)
    m.add_image(img, animation_type='window', window_size=7, window_step=2)
    m.add_axis('x', 'y')
    m.add_trace(np.arange(20))
    a = Animation(m)
    assert np.allclose(a.x_data, np.arange(20) - 7 // 2)


def test_style():
    _ = Movie(style='default')
    assert mpl.rcParams['figure.facecolor'] == 'w'
    _ = Movie(style='dark_background')
    assert mpl.rcParams['figure.facecolor'] == 'black'
