
==============
Animate Images
==============

|Build Status| |PyPI version| |Updates| |Python3| |Cover|

Helper functions to make animations of images with corresponding traces and labels using matplotlib

------------
Example use:
------------

.. code-block:: python

    from Animate.Movie import Movie
    import numpy as np
    m = Movie(dt=1.0 / 14, height_ratio=1.5)
    img = np.random.randint(10, size=(40, 5, 5))
    m.add_image(img, style='dark_img')
    m.add_axis(x_label='time (s)', y_label='value')
    m.add_trace(img.mean(axis=(1, 2)))
    m.save('path/to/file/with_name', fps=1)


.. image:: resources/example.gif


-------
Testing
-------

.. code-block:: bash

    pytest --pep8 --cov=Animate --cov-report html


---------
Deploying
---------

.. code-block:: bash

    bumpversion patch
    python setup.py sdist
    twine upload \dist\...

.. |Updates| image:: https://pyup.io/repos/github/boazmohar/AnimateImages/shield.svg
   :target: https://pyup.io/repos/github/boazmohar/AnimateImages/
.. |Python3| image:: https://pyup.io/repos/github/boazmohar/AnimateImages/python-3-shield.svg
   :target: https://pyup.io/repos/github/boazmohar/AnimateImages/
.. |Build Status| image:: https://travis-ci.org/boazmohar/AnimateImages.svg?branch=master
   :target: https://travis-ci.org/boazmohar/AnimateImages
.. |PyPI version| image:: https://badge.fury.io/py/animateimages.svg
   :target: https://badge.fury.io/py/animateimages
.. |Cover| image:: https://coveralls.io/repos/github/boazmohar/AnimateImages/badge.svg?branch=master
   :target: https://coveralls.io/github/boazmohar/AnimateImages?branch=master
