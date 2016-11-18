from matplotlib import docstring
from matplotlib.pyplot import _autogen_docstring
import matplotlib.pyplot as plt

import betterplotlib as bpl

@_autogen_docstring(bpl.Axes_bpl.make_ax_dark)
def make_ax_dark(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.make_ax_dark(*args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.remove_ticks)
def remove_ticks(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.remove_ticks(*args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.remove_spines)
def remove_spines(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.remove_spines(*args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.scatter)
def scatter(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.scatter(*args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.hist)
def hist(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.hist(*args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.add_labels)
def add_labels(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.add_labels(*args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.set_limits)
def set_limits(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.set_limits(*args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.add_text)
def add_text(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.add_text(*args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.remove_labels)
def remove_labels(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.remove_labels(*args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.legend)
def legend(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.legend(*args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.equal_scale)
def equal_scale(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.equal_scale(*args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.easy_add_text)
def easy_add_text(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.easy_add_text(*args, **kwargs)

@_autogen_docstring(bpl.Axes_bpl.contour_scatter)
def contour_scatter(*args, **kwargs):
    ax = plt.gca(projection='bpl')
    return ax.contour_scatter(*args, **kwargs)

@_autogen_docstring(bpl.Figure_bpl.savefig)
def savefig(*args, **kwargs):
    fig = plt.gcf()
    return fig.savefig(*args, **kwargs)

