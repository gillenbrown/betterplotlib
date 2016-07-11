import matplotlib as mpl
from cycler import cycler

from . import colors

def _common_style():
    """
    Set some of the style options used by all styles.
    """

    mpl.rcParams['legend.scatterpoints'] = 1
    mpl.rcParams['savefig.format'] = 'pdf'
    mpl.rcParams['axes.formatter.useoffset'] = False
    # mpl.rcParams['figure.dpi'] = 200
    mpl.rcParams['figure.figsize'] = [10, 7]

    # Font options
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.sans-serif'] = 'Helvetica Neue'
    mpl.rcParams['font.weight'] = 'bold'
    mpl.rcParams['axes.labelweight'] = 'bold'
    mpl.rcParams['axes.titleweight'] = 'bold'

    # I like my own color cycle based on one of the Tableu sets.
    mpl.rcParams['axes.prop_cycle'] = cycler("color", colors.color_cycle)
    # change the colormap while I'm at it.
    mpl.rcParams['image.cmap'] = 'viridis'

def default_style():
    """
    Sets matplotlib parameters to make default plots prettier without effort.

    :return: None
    """
    _common_style()
    
    # Font options
    mpl.rcParams['axes.titlesize'] = 16
    mpl.rcParams['font.size'] = 14
    mpl.rcParams['axes.labelsize'] = 14
    mpl.rcParams['xtick.labelsize'] = 12
    mpl.rcParams['ytick.labelsize'] = 12
    mpl.rcParams['legend.fontsize'] = 13

    # colors
    mpl.rcParams['patch.edgecolor'] = colors.almost_black
    mpl.rcParams['text.color'] = colors.almost_black
    mpl.rcParams['axes.edgecolor'] = colors.almost_black
    mpl.rcParams['axes.labelcolor'] = colors.almost_black
    mpl.rcParams['xtick.color'] = colors.almost_black
    mpl.rcParams['ytick.color'] = colors.almost_black
    mpl.rcParams['grid.color'] = colors.almost_black
    

def presentation_style():
    """
    Same as default_style, but with larger text.

    Useful for powerpoint presentations where large font is nice.

    :return: None
    """

    _common_style()

    mpl.rcParams['axes.titlesize'] = 20
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.labelsize'] = 18
    mpl.rcParams['xtick.labelsize'] = 16
    mpl.rcParams['ytick.labelsize'] = 16
    mpl.rcParams['legend.fontsize'] = 17

    # colors
    mpl.rcParams['patch.edgecolor'] = colors.almost_black
    mpl.rcParams['text.color'] = colors.almost_black
    mpl.rcParams['axes.edgecolor'] = colors.almost_black
    mpl.rcParams['axes.labelcolor'] = colors.almost_black
    mpl.rcParams['xtick.color'] = colors.almost_black
    mpl.rcParams['ytick.color'] = colors.almost_black
    mpl.rcParams['grid.color'] = colors.almost_black


def white_style():
    """
    Sets a style good for presenting on dark backgrounds.

    This was designed to use for creating plots that will be used in
    PowerPoint slides with a dark background. The text is larger to make
    more viewable plots, as well.

    :return: None
    """
    _common_style()

    mpl.rcParams['axes.titlesize'] = 20
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.labelsize'] = 18
    mpl.rcParams['xtick.labelsize'] = 16
    mpl.rcParams['ytick.labelsize'] = 16
    mpl.rcParams['legend.fontsize'] = 17

    # colors
    mpl.rcParams['patch.edgecolor'] = "w"
    mpl.rcParams['text.color'] = "w"
    mpl.rcParams['axes.edgecolor'] = "w"
    mpl.rcParams['axes.labelcolor'] = "w"
    mpl.rcParams['xtick.color'] = "w"
    mpl.rcParams['ytick.color'] = "w"
    mpl.rcParams['grid.color'] = "w"
    # I like my own color cycle based on one of the Tableu sets, but with
    # added colors in front that look better on dark backgrounds
    mpl.rcParams['axes.prop_cycle'] = cycler("color", ["w", "y"] +
                                             colors.color_cycle)