from palettable.tableau import Tableau_10
import matplotlib as mpl

from .tools import *
from .colors import *


mpl.rcParams['axes.color_cycle'] = Tableau_10.hex_colors
mpl.rcParams['legend.scatterpoints'] = 1
mpl.rcParams['savefig.format'] = 'pdf'
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'Helvetica'
mpl.rcParams['patch.edgecolor'] = almost_black
mpl.rcParams['text.color'] = almost_black
mpl.rcParams['axes.edgecolor'] = almost_black
mpl.rcParams['axes.labelcolor'] = almost_black
mpl.rcParams['xtick.color'] = almost_black
mpl.rcParams['ytick.color'] = almost_black
mpl.rcParams['grid.color'] = almost_black