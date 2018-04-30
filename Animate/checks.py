from numbers import Number
import numpy as np

try:
    basestring
except NameError:
    basestring = str


def check_axis(axis):
    if not isinstance(axis, int):
        raise ValueError('Axis must be an integer got: %s' % type(axis))
    if axis < 0:
        raise ValueError('Axis must be positive got: %d' % axis)


def check_location(location, name):
    if not hasattr(location, '__iter__') or len(location) != 2:
        raise ValueError('%s should be an iterable of length 2 got type: %s, len %d' %
                         (name, type(location), len(location)))


def check_axis_type(axis_type):
    if axis_type != 'image' and axis_type != 'trace':
        raise ValueError('axis_type should be image or trace got %s' % axis_type)


def check_number(number, name):
    if not isinstance(number, Number):
        raise ValueError('%s should be a number got: %s' % (name, type(number)))


def check_locations(locations, name):
    if not isinstance(locations, (list, tuple, np.ndarray)):
        raise ValueError('%s should be an iterable of locations got: %s' % (name, type(locations)))


def check_text(text, name):
    if not isinstance(text, basestring):
        raise ValueError('%s should be a string: %s' % (name, type(text)))


def check_dict(d, name):
    if not isinstance(d, dict):
        raise ValueError('%s should be a dictionary: %s' % (name, type(d)))


def check_bool(b, name):
    if not isinstance(b, bool):
        raise ValueError('%s should be a boolean: %s' % (name, type(b)))


def check_length(a, length, name):
    if len(a) != length:
        raise ValueError('%s should be length: %d got %d' % (name, length, len(a)))
