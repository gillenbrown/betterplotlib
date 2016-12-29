from matplotlib import docstring
from matplotlib.pyplot import _autogen_docstring
import matplotlib.pyplot as plt

import betterplotlib as bpl

@_autogen_docstring(bpl.Axes_bpl.make_ax_dark)
def make_ax_dark(minor_ticks=False):
    ax = plt.gca(projection='bpl')
    return ax.make_ax_dark(minor_ticks)

@_autogen_docstring(bpl.Axes_bpl.remove_ticks)
def remove_ticks(ticks_to_remove):
    ax = plt.gca(projection='bpl')
    return ax.remove_ticks(ticks_to_remove)

@_autogen_docstring(bpl.Axes_bpl.remove_spines)
def remove_spines(spines_to_remove):
    ax = plt.gca(projection='bpl')
    return ax.remove_spines(spines_to_remove)

@_autogen_docstring(bpl.Axes_bpl.scatter)
def scatter(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.scatter(*args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.hist)
def hist(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.hist(*args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.add_labels)
def add_labels(x_label=None, y_label=None, title=None,
               *args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.add_labels(x_label, y_label, title,
                         *args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.set_limits)
def set_limits(x_min=None, x_max=None, y_min=None, y_max=None,
               **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.set_limits(x_min, x_max, y_min, y_max,
                         **kwargs)

@_autogen_docstring(bpl.Axes_bpl.add_text)
def add_text(x, y, text, coords="data", **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.add_text(x, y, text, coords, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.remove_labels)
def remove_labels(labels_to_remove):
    ax = plt.gca(projection='bpl')
    return ax.remove_labels(labels_to_remove)

@_autogen_docstring(bpl.Axes_bpl.legend)
def legend(facecolor="None", *args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.legend(facecolor, *args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.equal_scale)
def equal_scale(self):
    ax = plt.gca(projection='bpl')
    return ax.equal_scale(self)

@_autogen_docstring(bpl.Axes_bpl.easy_add_text)
def easy_add_text(text, location, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.easy_add_text(text, location, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.contour_scatter)
def contour_scatter(xs, ys, fill_cmap="white", bin_size=None,
                    min_level=5, num_contours=7, scatter_kwargs=dict(), 
                    contour_kwargs=dict()):
    ax = plt.gca(projection='bpl')
    return ax.contour_scatter(xs, ys, fill_cmap, bin_size,
                              min_level, num_contours, scatter_kwargs, 
                              contour_kwargs)

@_autogen_docstring(bpl.Axes_bpl.data_ticks)
def data_ticks(x_data, y_data, extent=0.015, *args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.data_ticks(x_data, y_data, extent, *args, **kwargs)

