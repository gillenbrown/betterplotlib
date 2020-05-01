import urllib
import os

from matplotlib import rcParams
from matplotlib import font_manager
from cycler import cycler

from . import colors

def set_style(style="default", font="Lato"):
    """
    Same as default_style, but with larger text.

    Useful for powerpoint presentations where large font is nice.

    :return: None
    """

    _common_style()

    if style == "default":
        _set_font_settings(font)
    elif style == "white":
        _set_font_settings(font)
        # override some of the colors
        rcParams['patch.edgecolor'] = "w"
        rcParams['text.color'] = "w"
        rcParams['axes.edgecolor'] = "w"
        rcParams['axes.labelcolor'] = "w"
        rcParams['xtick.color'] = "w"
        rcParams['ytick.color'] = "w"
        rcParams['grid.color'] = "w"
        # I like my own color cycle based on one of the Tableu sets, but with
        # added colors in front that look better on dark backgrounds
        rcParams['axes.prop_cycle'] = cycler("color", ["w", "y"] +
                                             colors.color_cycle)
    elif style == "latex":
        # here font is ignored
        # change everything to LaTeX
        rcParams['font.family'] = 'serif'
        rcParams['font.sans-serif'] = 'Computer Modern Roman'
        rcParams['font.serif'] = 'Computer Modern Roman'
        rcParams['text.usetex'] = True

def _common_style():
    """
    Set some of the style options used by all styles.
    """
    rcParams['legend.scatterpoints'] = 1
    rcParams['legend.numpoints'] = 1
    # ^ these two needed for matplotlib 1.x
    rcParams['savefig.format'] = 'pdf'
    rcParams['axes.formatter.useoffset'] = False
    rcParams['figure.dpi'] = 100
    rcParams['savefig.dpi'] = 300
    rcParams['figure.figsize'] = [10, 7]

    rcParams['xtick.major.size'] = 5.0
    rcParams['xtick.minor.size'] = 2.5
    rcParams['ytick.major.size'] = 5.0
    rcParams['ytick.minor.size'] = 2.5

    rcParams['axes.titlesize'] = 22
    rcParams['font.size'] = 20
    rcParams['axes.labelsize'] = 20
    rcParams['xtick.labelsize'] = 16
    rcParams['ytick.labelsize'] = 16
    rcParams['legend.fontsize'] = 18

    rcParams['patch.edgecolor'] = colors.almost_black
    rcParams['text.color'] = colors.almost_black
    rcParams['axes.edgecolor'] = colors.almost_black
    rcParams['axes.labelcolor'] = colors.almost_black
    rcParams['xtick.color'] = colors.almost_black
    rcParams['ytick.color'] = colors.almost_black
    rcParams['grid.color'] = colors.almost_black

    # I like my own color cycle
    rcParams['axes.prop_cycle'] = cycler("color", colors.color_cycle)
    # change the colormap while I'm at it.
    rcParams['image.cmap'] = 'viridis'


def _set_font_settings(font):
    """
    Sets the Helvetica Neue font settings, used by most styles.

    :return: None
    """
    # Some good font options: Lato, Nunito, Open Sans,

    # The font doesn't actually have to be sans-serif, we're just setting that
    # as a default since we currently don't know what family the requested
    # font is. And for our purposes it doesn't matter, since it works fine if
    # we tell matplotlib it's a sans-serif font, even if it's not.
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = font

    # change math font too
    rcParams['mathtext.fontset'] = 'custom'
    rcParams['mathtext.default'] = 'regular'

    # set the rest of the default parameters
    rcParams['font.weight'] = 'medium'
    rcParams['axes.labelweight'] = 'medium'
    rcParams['axes.titleweight'] = 'medium'

    # The user might request a font that's not downloaded. To check this, we'll
    # see if the found font is the default. If so, we'll download the font
    fm = font_manager.FontManager()
    default_font = fm.defaultFont["ttf"]
    found_font = fm.findfont(font)

    if default_font == found_font:
        print("- Downloading font: {}".format(font))
        print("- You may need to rerun this script or restart this jupyter")
        print("  notebook for these changes to take effect.")
        print("- This only needs to be done once.")
        font_dir = os.path.join(rcParams["datapath"], "fonts/ttf/")
        download_font(font, font_dir)

        # then rebuild the font cache
        font_manager._rebuild()


def _download_file(url, local_dir):
    filename = url.split("/")[-1]
    local_filename = os.path.join(local_dir, filename)
    try:
        urllib.request.urlretrieve(url, filename=local_filename)
    except urllib.error.HTTPError:
        raise ValueError("File was not found (404): {}".format(url))



def download_font(fontname, dir):
    # format the font as it is in the github repo
    fontname = fontname.lower()
    fontname = fontname.replace(" ", "")

    base_url = "https://raw.githubusercontent.com/google/fonts/master/"
    # we don't know what license the font uses, so we need to search for it
    licenses = ["apache", "ofl", "ufl"]
    found = False
    for l in licenses:
        font_dir_url = os.path.join(base_url, l, fontname)

        # try to get the metadata file
        metadata_url = os.path.join(font_dir_url, "METADATA.pb")
        # this will throw an error if it's not found
        try:
            _download_file(metadata_url, ".")
            found = True
            break
        except ValueError:
            continue

    if not found:
        raise ValueError("Font not found!")

    # then get the filenames from the metadata file
    ttf_names = []
    with open("./METADATA.pb", "r") as metadata:
        for line in metadata:
            strip_line = line.strip()
            if strip_line.startswith("filename:"):
                filename = strip_line.split()[-1]
                # this will have quotes, remove them
                filename = filename.replace('"', '')
                ttf_names.append(filename)

    # then download all those individual files
    for ttf_file in ttf_names:
        ttf_url = os.path.join(font_dir_url, ttf_file)
        _download_file(ttf_url, dir)