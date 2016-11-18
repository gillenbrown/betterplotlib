from matplotlib.projections import register_projection
import matplotlib.pyplot as plt

from .axes_bpl import Axes_bpl
from .figure_bpl import Figure_bpl

from .colors import *
from .styles import *
from ._interface import *

register_projection(Axes_bpl)

def subplots(*args, **kwargs):
    """
    Acts as a wrapper to the plt.subplots() function.

    This is exactly the same as the `plt.subplots()` function, only that it
    creates betterplotlib axes and figure objects rather than matplotlib ones.
    The betterplotlib objects are where all the magic happens.
    """
    # use a bpl figure
    kwargs.setdefault("FigureClass", Figure_bpl)

    # use a bpl axes object. This is a stored projection in matplotlib
    # that we can access
    subplot_kwargs = kwargs.setdefault("subplot_kw", dict())
    subplot_kwargs.setdefault("projection", "bpl")

    return plt.subplots(*args, **kwargs)
    