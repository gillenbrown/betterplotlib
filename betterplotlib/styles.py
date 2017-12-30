import matplotlib as mpl
from matplotlib import font_manager
from cycler import cycler
import warnings

from . import colors


def _common_style():
    """
    Set some of the style options used by all styles.
    """
    mpl.rcParams['legend.scatterpoints'] = 1
    mpl.rcParams['legend.numpoints'] = 1
    # ^ these two needed for matplotlib 1.x
    mpl.rcParams['savefig.format'] = 'pdf'
    mpl.rcParams['axes.formatter.useoffset'] = False
    mpl.rcParams['figure.dpi'] = 100
    mpl.rcParams['savefig.dpi'] = 300
    mpl.rcParams['figure.figsize'] = [10, 7]

    mpl.rcParams['xtick.major.size'] = 5.0
    mpl.rcParams['xtick.minor.size'] = 2.5
    mpl.rcParams['ytick.major.size'] = 5.0
    mpl.rcParams['ytick.minor.size'] = 2.5

    # the matplotlib 2.0 colors are fine, but the old ones aren't.
    if mpl.__version__[0] == "1":
        # I like my own color cycle based on one of the Tableu sets.
        mpl.rcParams['axes.prop_cycle'] = cycler("color", colors.color_cycle)
        # change the colormap while I'm at it.
        mpl.rcParams['image.cmap'] = 'viridis'


def _set_font_settings(font="Avenir"):
    """
    Sets the Helvetica Neue font settings, used by most styles.

    :return: None
    """
    mpl.rcParams['font.family'] = 'sans-serif'

    # We have to be more suble when setting the font. We want to check that the
    # use has the font we want.
    backup_font = "Arial"

    # Matplotlib will issue a warning if it can't find the font, so we will
    # try to find the font, and see if the warning was issued
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        # line that will throw a warning
        font_manager.fontManager.findfont(font)

        if len(w) == 0:  # if no warnings
            mpl.rcParams['font.sans-serif'] = font
        else:  # there were warnings, so the font wasn't found
            mpl.rcParams['font.sans-serif'] = backup_font
            url = "https://github.com/olgabot/sciencemeetproductivity.tumblr." \
                  "com/blob/master/posts/2012/11/how-to-set-helvetica-as-" \
                  "the-default-sans-serif-font-in.md"
            # this_file = os.path.abspath(__file__)
            print("Betterplotlib could not find the font {}.\n"
                  "For directions on how to install it, check {}\n"
                  "You don't need to do step 4 on that page.\n\n"
                  "You can also change the font to something you'd prefer."
                  "".format(font, url))

    # change math font too
    mpl.rcParams['mathtext.fontset'] = 'custom'
    mpl.rcParams['mathtext.default'] = 'regular'

    # set the rest of the default parameters
    mpl.rcParams['font.weight'] = 'bold'
    mpl.rcParams['axes.labelweight'] = 'bold'
    mpl.rcParams['axes.titleweight'] = 'bold'


def default_style(font="Avenir"):
    """
    Sets matplotlib parameters to make default plots prettier without effort.

    :return: None
    """
    _common_style()
    _set_font_settings(font)
    
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
    

def presentation_style(font="Avenir"):
    """
    Same as default_style, but with larger text.

    Useful for powerpoint presentations where large font is nice.

    :return: None
    """

    _common_style()
    _set_font_settings(font)

    mpl.rcParams['axes.titlesize'] = 22
    mpl.rcParams['font.size'] = 20
    mpl.rcParams['axes.labelsize'] = 20
    mpl.rcParams['xtick.labelsize'] = 16
    mpl.rcParams['ytick.labelsize'] = 16
    mpl.rcParams['legend.fontsize'] = 18

    # colors
    mpl.rcParams['patch.edgecolor'] = colors.almost_black
    mpl.rcParams['text.color'] = colors.almost_black
    mpl.rcParams['axes.edgecolor'] = colors.almost_black
    mpl.rcParams['axes.labelcolor'] = colors.almost_black
    mpl.rcParams['xtick.color'] = colors.almost_black
    mpl.rcParams['ytick.color'] = colors.almost_black
    mpl.rcParams['grid.color'] = colors.almost_black


def white_style(font="Avenir"):
    """
    Sets a style good for presenting on dark backgrounds.

    This was designed to use for creating plots that will be used in
    PowerPoint slides with a dark background. The text is larger to make
    more viewable plots, as well.

    :return: None
    """
    _common_style()
    _set_font_settings(font)

    mpl.rcParams['axes.titlesize'] = 22
    mpl.rcParams['font.size'] = 20
    mpl.rcParams['axes.labelsize'] = 20
    mpl.rcParams['xtick.labelsize'] = 16
    mpl.rcParams['ytick.labelsize'] = 16
    mpl.rcParams['legend.fontsize'] = 20

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


def paper_style():
    """
    Uses LaTeX font rendering to make plots look good in publications where
    LaTeX is used.

    :return: None
    """
    _common_style()

    mpl.rcParams['figure.figsize'] = [10, 8]
    # change everything to LaTeX
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams['font.sans-serif'] = 'Computer Modern Roman'
    mpl.rcParams['text.usetex'] = True

    # font sizes
    mpl.rcParams['axes.titlesize'] = 26
    mpl.rcParams['font.size'] = 28
    mpl.rcParams['axes.labelsize'] = 28
    mpl.rcParams['xtick.labelsize'] = 24
    mpl.rcParams['ytick.labelsize'] = 24
    mpl.rcParams['legend.fontsize'] = 18
