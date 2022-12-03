from matplotlib.projections import register_projection

from .axes_bpl import Axes_bpl
from .colors import *
from .styles import *
from .manage_axes import *
from ._interface import *

register_projection(Axes_bpl)
