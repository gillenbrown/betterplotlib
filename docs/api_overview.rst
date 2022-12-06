.. _api_ref:

.. currentmodule:: betterplotlib

API Overview
===========================


Top Level Functions
--------------------

The main function here is the :py:func:`subplots` function, but there is also a style
function available (see the :ref:`styles` page).

.. autosummary::
    subplots
    set_style


Axes
------------------
The :py:class:`Axes_bpl` objects are where the main functionality lies. The easiest
way to create them is by using the :py:func:`subplots` function, which creates both a
`matplotlib Figure` and :py:class:`Axes_bpl` object (typically used as
`fig, ax = bpl.subplots()`). The :py:class:`Axes_bpl` inherits from the
`matplotlib Axes` object, so it has all the same methods. It additionally has
some new ones, and some of the old ones are redefined to make plotting nicer and
easier. The functionality of the :py:class:`Axes_bpl` is broken down into some common
themes below. Each of these has at least one example of the function in use.

Plotting
^^^^^^^^^^^^^^^^^^^
These methods replace or supplement the default matplotlib commands for the main
plotting functionality.

.. autosummary::
    Axes_bpl.plot
    Axes_bpl.scatter
    Axes_bpl.errorbar
    Axes_bpl.hist
    Axes_bpl.density_contour
    Axes_bpl.density_contourf
    Axes_bpl.contour_scatter
    Axes_bpl.shaded_density

Plot Annotations and Format
^^^^^^^^^^^^^^^^^^^^^^^^^^^
These methods control various annotations, like the legend, tick marks, and axes labels.

.. autosummary::
    Axes_bpl.legend
    Axes_bpl.data_ticks
    Axes_bpl.axhline
    Axes_bpl.axvline
    Axes_bpl.add_text
    Axes_bpl.easy_add_text
    Axes_bpl.set_limits
    Axes_bpl.set_ticks
    Axes_bpl.log
    Axes_bpl.add_labels
    Axes_bpl.remove_labels
    Axes_bpl.remove_ticks
    Axes_bpl.remove_spines
    Axes_bpl.equal_scale
    Axes_bpl.twin_axis_simple
    Axes_bpl.twin_axis
    Axes_bpl.make_ax_dark


Non Object-Oriented Interface
-----------------------------

In addition to the interface described above, all the Axes objects are accessible
without directly creating them. This works just like the `plt.whatever()` syntax in
default matplotlib, just with `bpl.whatever()`.

    


