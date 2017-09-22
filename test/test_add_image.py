import pytest
import numpy as np
from Animate.Movie import Movie
from Animate.Animation import Animation
import matplotlib as mpl


def test_fail_type():
    with pytest.raises(ValueError) as ex:
        m = Movie()
        img = np.arange(100).reshape(4, 5, 5)
        m.add_image(img, animation_type='fail')
    assert 'animation type should be movie or window' in str(ex.value)


def test_fail_movie_size():
    with pytest.raises(ValueError) as ex:
        m = Movie()
        img = np.arange(100).reshape(20, 5)
        m.add_image(img, animation_type='movie')
    assert 'Expected 3d numpy array when animation type is movie' in str(ex.value)


def test_fail_window_size():
    with pytest.raises(ValueError) as ex:
        m = Movie()
        img = np.arange(100).reshape(4, 5, 5)
        m.add_image(img, animation_type='window')
    assert 'Expected 2d numpy array when animation type is window' in str(ex.value)


def test_fail_window_size_rgb():
    with pytest.raises(ValueError) as ex:
        m = Movie()
        img = np.arange(100).reshape(4, 5, 5)
        m.add_image(img, animation_type='window', is_rgb=True)
    assert 'Expected 3d numpy array when animation type is window and is_rgb is True' in str(ex.value)


def test_default_values():
    m = Movie()
    img = np.arange(100).reshape(4, 5, 5)
    m.add_image(img)
    m_img = m.images[0]
    assert np.allclose(m_img['data'], img)
    assert m_img['animation_type'] == 'movie'
    assert m_img['style'] == 'dark_img'
    assert m_img['c_title'] is None
    assert m_img['c_style'] == 'dark_background'
    assert np.isclose(m_img['ymin'], 0)
    assert np.isclose(m_img['ymax'], 98.901)
    assert m_img['window_size'] == 60
    assert m_img['window_step'] == 3
    assert m_img['is_rgb'] is False
