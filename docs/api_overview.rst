.. _api_ref:

.. currentmodule:: betterplotlib

API Overview
===========================

Here are all the functions in the module, hopefully organized in a way that makes them easy to understand.

Top Level Functions
--------------------

Betterplotlib has some top level functions, involving either styles or object handling.

Object Handling
^^^^^^^^^^^^^^^^^
.. autosummary::
    subplots

Styles
^^^^^^^^^^^
.. autosummary::
    default_style
    presentation_style
    white_style


Axes
------------------
The :py:class:`Axes_bpl` objects are where the main functionality lies. The easiest way to create them is by using the :py:func:`subplots` function, which creates both a `matplotlib Figure` and :py:class:`Axes_bpl` object. The :py:class:`Axes_bpl` inherits from the `matplotlib Axes` object, so it has all the same methods. It additionally has some new ones, and some of the old ones are redefined to make plotting nicer and easier. The functionality of the :py:class:`Axes_bpl` is broken down into some common themes below.

Plotting
^^^^^^^^^^^^^^^^^^^
These methods replace or supplement the default matplotlib commands for the main plotting functionality.

.. autosummary::
    Axes_bpl.plot
    Axes_bpl.scatter
    Axes_bpl.hist
    Axes_bpl.contour_scatter

Plot Annotations
^^^^^^^^^^^^^^^^^^
These methods control various annotations, like the legend, tick marks, and axes labels.

.. autosummary::
    Axes_bpl.legend
    Axes_bpl.set_limits
    Axes_bpl.data_ticks
    Axes_bpl.axhline
    Axes_bpl.axvline
    Axes_bpl.add_text
    Axes_bpl.easy_add_text
    Axes_bpl.add_labels
    Axes_bpl.remove_labels
    Axes_bpl.remove_ticks
    Axes_bpl.remove_spines

Plot Format
^^^^^^^^^^^^
These methods control the format of the axes itself.

.. autosummary::
    Axes_bpl.make_ax_dark
    Axes_bpl.equal_scale


Non Object-Oriented Interface
-----------------------------

In addition to the interface described above, all the Axes objects are accessible without directly creating them. This works just like the `plt.whatever()` syntax in default matplotlib. See the examples page for some examples. Note that I designed everything with the object oriented syntax in mind, and haven't tested the non-OO interface as much, so it might not always work as intended. Let me know if you find any bugs.

    


