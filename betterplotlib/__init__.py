from matplotlib.projections import register_projection
import matplotlib.pyplot as plt

from .axes_bpl import Axes_bpl

from .colors import *
from .styles import *
from ._interface import *

register_projection(Axes_bpl)

def subplots(*args, **kwargs):
    """
    A wrapper to the plt.subplots() function, and is the main way to access the 
    betterplotlib functionality.

    This is exactly the same as the `plt.subplots()` function, only that it
    creates betterplotlib axes objects rather than matplotlib ones.
    The betterplotlib objects are where all the magic happens.
    """

    # use a bpl axes object. This is a stored projection in matplotlib
    # that we can access
    subplot_kwargs = kwargs.setdefault("subplot_kw", dict())
    subplot_kwargs.setdefault("projection", "bpl")

    return plt.subplots(*args, **kwargs)
    