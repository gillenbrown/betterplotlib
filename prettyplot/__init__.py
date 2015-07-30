from palettable.tableau import Tableau_10
import matplotlib as mpl

from .tools import *
from .colors import *


mpl.rcParams['legend.scatterpoints'] = 1
mpl.rcParams['savefig.format'] = 'pdf'
mpl.rcParams['axes.formatter.useoffset'] = False
mpl.rcParams['figure.dpi'] = 300

# Font options
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'Helvetica Neue'
mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['axes.labelweight'] = 'bold'
mpl.rcParams['axes.titleweight'] = 'bold'
mpl.rcParams['axes.titlesize'] = 16
mpl.rcParams['font.size'] = 14
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
mpl.rcParams['legend.fontsize'] = 13

# colors
mpl.rcParams['patch.edgecolor'] = almost_black
mpl.rcParams['text.color'] = almost_black
mpl.rcParams['axes.edgecolor'] = almost_black
mpl.rcParams['axes.labelcolor'] = almost_black
mpl.rcParams['xtick.color'] = almost_black
mpl.rcParams['ytick.color'] = almost_black
mpl.rcParams['grid.color'] = almost_black
# I like my own color cycle based on one of the Tableu sets.
mpl.rcParams['axes.color_cycle'] = [Tableau_10.hex_colors[3],
                                    Tableau_10.hex_colors[0],
                                    Tableau_10.hex_colors[2],
                                    Tableau_10.hex_colors[4],
                                    Tableau_10.hex_colors[1],
                                    Tableau_10.hex_colors[6],
                                    Tableau_10.hex_colors[7],
                                    Tableau_10.hex_colors[9],
                                    Tableau_10.hex_colors[8],
                                    Tableau_10.hex_colors[5]]

# TODO: make errorbar plot where the errorbars look nicer when there are a ton
# of points. Maybe try to make the errorbars themselves transparent slightly,
# or try to make sure they are always behind the actual points.
