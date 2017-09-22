import pytest
import numpy as np
from Animate.Movie import Movie


def test_fail_axis():
    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_annotation(axis='1', xy=(0, 1), xy_text=(2, 3), text='')
    assert 'Axis must be an integer got' in str(ex.value)

    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_annotation(axis=-1, xy=(0, 1), xy_text=(2, 3), text='')
    assert 'Axis must be positive got' in str(ex.value)


def test_fail_positions():
    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_annotation(axis=0, xy=(0,), xy_text=(2, 3), text='')
    assert 'xy should be an iterable' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_annotation(axis=0, xy='12', xy_text=(2, 3), text='')
    assert 'xy should be an iterable' in str(ex.value)

    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_annotation(axis=0, xy=(0, 1), xy_text=(2,), text='')
    assert 'xy_text should be an iterable' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_annotation(axis=0, xy=(0, 1), xy_text='12', text='')
    assert 'xy_text should be an iterable' in str(ex.value)


def test_fail_axis_type():
    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_annotation(axis=0, xy=(0, 1), xy_text=(2, 3), text='', axis_type='fail')
    assert 'axis_type should be image or trace' in str(ex.value)


def test_defaults():
    m = Movie()
    m.add_annotation(axis=0, xy=(0, 1), xy_text=(2, 3), text='4', color='blue')
    a = m.annotations[0]
    assert a['type'] == 'annotation'
    assert a['axis'] == 0
    assert a['text'] == '4'
    assert a['xy'] == (0, 1)
    assert a['xy_text'] == (2, 3)
    assert a['axis_type'] == 'image'
    kwargs = a['kwargs']
    assert kwargs['color'] == 'blue'


def test_rectangle():
    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_rectangle_annotation(axis=0, xy=(0, 1), width='1', height=2, angle=0)
    assert 'width should be a number' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_rectangle_annotation(axis=0, xy=(0, 1), width=1, height='2', angle=0)
    assert 'height should be a number' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_rectangle_annotation(axis=0, xy=(0, 1), width=1, height=2, angle='0')
    assert 'angle should be a number' in str(ex.value)
    m = Movie()
    m.add_rectangle_annotation(axis=0, xy=(0, 1), width=1, height=2, angle=0, color='blue')
    a = m.annotations[0]
    assert a['type'] == 'rectangle'
    assert a['axis'] == 0
    assert a['xy'] == (0, 1)
    assert a['width'] == 1
    assert a['height'] == 2
    assert a['angle'] == 0
    assert a['axis_type'] == 'image'
    kwargs = a['kwargs']
    assert kwargs['color'] == 'blue'


def test_line():
    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_line_annotation(axis=0, x='1', y=[0, 1])
    assert 'x should be an iterable of locations' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_line_annotation(axis=0, x=(1, 2), y={'1': 2})
    assert 'y should be an iterable of locations' in str(ex.value)
    m = Movie()
    m.add_line_annotation(axis=0, x=(1, 2), y=np.array([2, 3]), color='blue')
    a = m.annotations[0]
    assert a['type'] == 'line'
    assert a['axis'] == 0
    assert a['x'] == (1, 2)
    assert np.allclose(a['y'], np.array([2, 3]))
    assert a['axis_type'] == 'image'
    kwargs = a['kwargs']
    assert kwargs['color'] == 'blue'


def test_text():
    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_text_annotation(axis=0, x=0, y=1, text=3)
    assert 'text should be a string' in str(ex.value)

    m = Movie()
    m.add_text_annotation(axis=0, x=0, y=1, text='3', color='blue')
    a = m.annotations[0]
    assert a['type'] == 'text'
    assert a['axis'] == 0
    assert a['x'] == 0
    assert a['y'] == 1
    assert a['text'] == '3'
    assert a['axis_type'] == 'image'
    kwargs = a['kwargs']
    assert kwargs['color'] == 'blue'


def test_circle():
    m = Movie()
    m.add_circle_annotation(axis=0, x=0, y=1, radius=3, color='blue')
    a = m.annotations[0]
    assert a['type'] == 'circle'
    assert a['axis'] == 0
    assert a['x'] == 0
    assert a['y'] == 1
    assert a['radius'] == 3
    assert a['axis_type'] == 'image'
    kwargs = a['kwargs']
    assert kwargs['color'] == 'blue'


def test_scale_bar_fail():
    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_scale_bar(axis=0, pixel_width=40, um_width='20', y=2, text_offset=1, line_kwargs=(1,),
                        text_kwargs=None)
    assert 'line_kwargs should be a dictionary' in str(ex.value)
    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_scale_bar(axis=0, pixel_width=40, um_width='20', y=2, text_offset=1, line_kwargs={'color': 'blue'},
                        text_kwargs=[2])
    assert 'text_kwargs should be a dictionary' in str(ex.value)


def test_scale_bar_default():
    m = Movie()
    m.add_scale_bar()
    line = m.annotations[0]
    assert line['axis'] == 0
    assert line['x'] == (0, 40)
    assert line['y'] == (2, 2)
    line_kwargs = line['kwargs']
    assert line_kwargs['color'] == 'white'
    assert line_kwargs['lw'] == 3

    text = m.annotations[1]
    assert text['axis'] == 0
    assert text['x'] == 20
    assert text['y'] == 1
    assert text['text'] == '20um'
    text_kwargs = text['kwargs']
    assert text_kwargs['ha'] == 'center'
    assert text_kwargs['fontsize'] == 14
    assert text_kwargs['color'] == 'white'


def test_scale_bar_kwargs():
    m = Movie()
    m.add_scale_bar(text_kwargs={'color': 'blue'}, line_kwargs={'color': 'blue'})
    line = m.annotations[0]
    assert line['axis'] == 0
    assert line['x'] == (0, 40)
    assert line['y'] == (2, 2)
    line_kwargs = line['kwargs']
    assert line_kwargs['color'] == 'blue'

    text = m.annotations[1]
    assert text['axis'] == 0
    assert text['x'] == 20
    assert text['y'] == 1
    assert text['text'] == '20um'
    text_kwargs = text['kwargs']
    assert text_kwargs['color'] == 'blue'
