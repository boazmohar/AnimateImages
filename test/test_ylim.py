import pytest
import numpy as np
from Animate.Movie import Movie
from Animate.Animation import Animation


def test_set_ylim_image():
    m = Movie(dt=1.0/14)
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img, style='dark_img', ylim_type='p_top', ylim_value=50)
    m_img = m.images[-1]
    assert m_img['ymin'] == 0
    assert np.isclose(m_img['ymax'], 49.5)

    m.add_image(img, style='dark_img', ylim_type='p_bottom', ylim_value=50)
    m_img = m.images[-1]
    assert np.isclose(m_img['ymin'], 49.5)
    assert m_img['ymax'] == 99

    m.add_image(img, style='dark_img', ylim_type='p_both', ylim_value=10)
    m_img = m.images[-1]
    assert np.isclose(m_img['ymin'], 9.9)
    assert np.isclose(m_img['ymax'], 89.1)

    m.add_image(img, style='dark_img', ylim_type='set', ylim_value=(2, 10))
    m_img = m.images[-1]
    assert m_img['ymin'] == 2
    assert m_img['ymax'] == 10

    with pytest.raises(RuntimeError) as ex:
        m.add_image(img, style='dark_img', ylim_type='set', ylim_value=10)
    assert 'ylim type set to set but len of ylim_value is not len 2' in str(ex.value)

    m.add_image(img, style='dark_img', ylim_type='same', ylim_value=len(m.images)-1)
    m_img = m.images[-1]
    assert m_img['ymin'] == 2
    assert m_img['ymax'] == 10

    with pytest.raises(RuntimeError) as ex:
        m.add_image(img, style='dark_img', ylim_type='same', ylim_value=len(m.images))
    assert 'Tried to have same y' in str(ex.value)

    with pytest.raises(RuntimeError) as ex:
        m.add_image(img, style='dark_img', ylim_type='error', ylim_value=len(m.images))
    assert "Expected 'p_top'" in str(ex.value)


def test_set_ylim_axis_top():
    m = Movie(dt=1.0 / 14)
    img = np.arange(250).reshape(10, 5, 5)
    m.add_image(img, style='dark_img')
    data = np.arange(10)
    m.add_axis('test', 'test', ylim_type='p_top', ylim_value=50)
    m.add_trace(data)
    a = Animation(m)
    a._init_draw()
    ax = a.trace_axes[-1]
    y_min, y_max = ax.get_ylim()
    assert np.isclose(y_min, 0)
    assert np.isclose(y_max, 4.5)


def test_set_ylim_axis_bottom():
    m = Movie(dt=1.0 / 14)
    img = np.arange(250).reshape(10, 5, 5)
    m.add_image(img, style='dark_img')
    data = np.arange(10)
    m.add_axis('test', 'test', ylim_type='p_bottom', ylim_value=50)
    m.add_trace(data)
    a = Animation(m)
    a._init_draw()
    ax = a.trace_axes[-1]
    y_min, y_max = ax.get_ylim()
    assert np.isclose(y_min, 4.5)
    assert np.isclose(y_max, 9)


def test_set_ylim_axis_both():
    m = Movie(dt=1.0 / 14)
    img = np.arange(250).reshape(10, 5, 5)
    m.add_image(img, style='dark_img')
    data = np.arange(10)
    m.add_axis('test', 'test', ylim_type='p_both', ylim_value=10)
    m.add_trace(data)
    a = Animation(m)
    a._init_draw()
    ax = a.trace_axes[-1]
    y_min, y_max = ax.get_ylim()
    assert np.isclose(y_min, 0.9)
    assert np.isclose(y_max, 8.1)


def test_set_ylim_axis_set_fail():
    m = Movie(dt=1.0 / 14)
    img = np.arange(250).reshape(10, 5, 5)
    m.add_image(img, style='dark_img')
    data = np.arange(10)
    with pytest.raises(RuntimeError) as ex:
        m.add_axis('test', 'test', ylim_type='set', ylim_value=10)
        m.add_trace(data)
        a = Animation(m)
        a._init_draw()
    assert 'ylim type set to set but len of ylim_value is not len 2' in str(ex.value)


def test_set_ylim_axis_set():
    m = Movie(dt=1.0 / 14)
    img = np.arange(250).reshape(10, 5, 5)
    m.add_image(img, style='dark_img')
    data = np.arange(10)
    m.add_axis('test', 'test', ylim_type='set', ylim_value=(2, 10))
    m.add_trace(data)
    a = Animation(m)
    a._init_draw()
    ax = a.trace_axes[-1]
    y_min, y_max = ax.get_ylim()
    assert np.isclose(y_min, 2)
    assert np.isclose(y_max, 10)


def test_set_ylim_axis_same_fail():
    m = Movie(dt=1.0 / 14)
    img = np.arange(250).reshape(10, 5, 5)
    m.add_image(img, style='dark_img')
    with pytest.raises(RuntimeError) as ex:
        m.add_axis('test', 'test', ylim_type='same', ylim_value=1)
        m.add_trace(np.arange(10))
        a = Animation(m)
        a._init_draw()
    assert 'Tried to have same y limits ' in str(ex.value)


def test_set_ylim_axis_same():
    m = Movie(dt=1.0 / 14)
    img = np.arange(250).reshape(10, 5, 5)
    m.add_image(img, style='dark_img')
    data = np.arange(10)
    m.add_axis('test', 'test', ylim_type='set', ylim_value=(2, 10))
    m.add_trace(data)
    m.add_axis('test', 'test', ylim_type='same', ylim_value=0)
    m.add_trace(data)
    m.add_trace(data, axis=1)
    a = Animation(m)
    a._init_draw()
    ax = a.trace_axes[-1]
    y_min, y_max = ax.get_ylim()
    assert np.isclose(y_min, 2)
    assert np.isclose(y_max, 10)


def test_set_ylim_axis_two():
    m = Movie(dt=1.0 / 14)
    img = np.arange(250).reshape(10, 5, 5)
    m.add_image(img, style='dark_img')
    data = np.arange(10)
    m.add_axis('test', 'test', ylim_type='p_top', ylim_value=10)
    m.add_trace(data)
    m.add_trace(np.arange(10, 20))
    a = Animation(m)
    a._init_draw()
    ax = a.trace_axes[-1]
    y_min, y_max = ax.get_ylim()
    assert np.isclose(y_min, 0)
    assert np.isclose(y_max, 17.1)
