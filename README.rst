
==============
Animate Images
==============

Helper functions to make animations of images with corresponding traces and labels using matplotlib

------------
Example use:
------------

.. code-block:: python
    from Animate import Animation

    prepare = Prepare('a', 'b', None)
    data = np.random.rand(10, 40, 20)
    prepare.add_image(data, c_title='try1')
    data = np.random.rand(10, 40, 20)
    prepare.add_image(data, c_title='try2')
    prepare.add_scale_bar(pixel_width=4)
    prepare.add_scale_bar(pixel_width=8, axis=1)
    prepare.add_time_label()
    prepare.add_annotation(0, (3, 3), (7, 9), '123', size=13, ha='right', va='center',
                           arrowprops=dict(arrowstyle="->", color='b'), color='g')
    prepare.add_circle_annotation(1, 3, 7, 3, color='b', lw=0.5, fill=False)
    prepare.add_axis('Time (s)', '$\Delta$F/F')
    prepare.add_trace(np.random.rand(10), 0, 'try1')
    prepare.add_trace(np.random.rand(10) + 2, 0, 'try2')
    prepare.add_axis('Time (s)', '$\Delta$F/F')
    prepare.add_trace(np.random.rand(10), 1, 'try1')
    prepare.add_trace(np.random.rand(10) + 2, 1, 'try2')
    animation = Animation(prepare)
    animation.save('test_sub.mp4', codec='h264')

