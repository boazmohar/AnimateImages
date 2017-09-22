import pytest
import numpy as np
from Animate.Movie import Movie


def test_axis():
    with pytest.raises(ValueError) as ex:
        m = Movie()
        m.add_axis(x_label='x', y_label='y', tight_x='1')
    assert 'tight_x should be a boolean' in str(ex.value)

    m = Movie()
    m.add_axis(x_label='x', y_label='y')
    axis = m.axes[0]
    assert axis['x_label'] == 'x'
    assert axis['y_label'] == 'y'
    assert axis['style'] == 'dark_trace'
    assert axis['running_line'] == {'color': 'white', 'lw': 2}
    assert axis['bottom_left_ticks']
    assert axis['ylim_type'] == 'p_top'
    assert axis['ylim_value'] == 0.1
    assert axis['tight_x']
    assert axis['label_kwargs'] == {'fontsize': 16}
    assert axis['legend_kwargs'] == {'frameon': False}


def test_trace():
    with pytest.raises(RuntimeError) as ex:
        m = Movie()
        m.add_trace(data=[1, 2, 3])
    assert 'Please create axis ' in str(ex.value)

    m = Movie()
    m.add_axis(x_label='x', y_label='y')
    m.add_trace(data=[1, 2, 3], color='blue')
    trace = m.traces[0]
    assert trace['axis'] == 0
    assert np.allclose(trace['data'], [1, 2, 3])
    assert trace['kwargs']['color'] == 'blue'
