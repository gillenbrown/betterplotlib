import urllib
import os
from pathlib import Path

import matplotlib
from matplotlib import rcParams
from matplotlib import font_manager
from cycler import cycler

from . import colors


def set_style(style="default", font="Lato", fontweight="semibold"):
    """
    Set style settings that will apply to all plots after this function call.

    :param style: I have three predefined styles: "default", "white"", and "latex".
                  On the whole, they're all pretty similar. The default style is
                  appropriate for presentations and paper figures. "white" takes the
                  default style and turns the axes white, so that it can be used in
                  a presentation with a dark slide background. When using the "white"
                  style, you'll probably want to save the figure with the
                  "transparent=True" keyword so that the slide background shows through.
                  Finally, the "latex" style uses LaTeX to render all text. Note that
                  all styles can fully render LaTeX equations in axis labels and other
                  text, but the "latex"theme uses the Computer Modern LaTeX font.
    :type style: str
    :param font: For the default and white styles, the font to use. Must be the name
                 of a font available through Google fonts. The font will be
                 automatically downloaded if not currently present on your system.
    :type font: str
    :param fontweight: The weight of the font
    :type fontweight: str
    :return: None

    .. plot::
        :include-source:

        import betterplotlib as bpl
        bpl.set_style() # default

        fig, ax = bpl.subplots()
        for i in range(3):
            ax.scatter(np.random.normal(i, 1, 100), np.random.normal(i, 1, 100))
        ax.add_labels("X Label", "Y Label", "Title")

    .. plot::
        :include-source:

        import betterplotlib as bpl
        bpl.set_style(font="DejaVu Sans")

        fig, ax = bpl.subplots()
        for i in range(3):
            ax.scatter(np.random.normal(i, 1, 100), np.random.normal(i, 1, 100))
        ax.add_labels("X Label", "Y Label", "Title")

    .. plot::
        :include-source:

        import betterplotlib as bpl
        bpl.set_style("white")

        fig, ax = bpl.subplots()
        for i in range(3):
            ax.scatter(np.random.normal(i, 1, 100), np.random.normal(i, 1, 100))
        ax.add_labels("X Label", "Y Label", "Title")

    If you download this previous image you can see that the background is transparent
    and the axes are white.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        bpl.set_style("latex")

        fig, ax = bpl.subplots()
        for i in range(3):
            ax.scatter(np.random.normal(i, 1, 100), np.random.normal(i, 1, 100))
        ax.add_labels("X Label", "Y Label", "Title")
    """
    _common_style()

    if style == "default":
        _set_font_settings(font, fontweight)
    elif style == "white":
        _set_font_settings(font, fontweight)
        # override some of the colors
        rcParams["savefig.transparent"] = True
        rcParams["patch.edgecolor"] = "w"
        rcParams["text.color"] = "w"
        rcParams["axes.edgecolor"] = "w"
        rcParams["axes.labelcolor"] = "w"
        rcParams["xtick.color"] = "w"
        rcParams["ytick.color"] = "w"
        rcParams["grid.color"] = "w"
        # I like my own color cycle based on one of the Tableu sets, but with
        # added colors in front that look better on dark backgrounds
        rcParams["axes.prop_cycle"] = cycler("color", ["w", "y"] + colors.color_cycle)
    elif style == "latex":
        # here font is ignored
        # change everything to LaTeX
        rcParams["font.family"] = "serif"
        rcParams["font.sans-serif"] = "Computer Modern Roman"
        rcParams["font.serif"] = "Computer Modern Roman"
        rcParams["text.usetex"] = True
    else:
        raise ValueError("style not recognized")


def _common_style():
    """
    Set some of the style options used by all styles.
    """
    rcParams["legend.scatterpoints"] = 1
    rcParams["legend.numpoints"] = 1
    # ^ these two needed for matplotlib 1.x
    rcParams["savefig.format"] = "pdf"
    rcParams["savefig.transparent"] = False
    rcParams["savefig.dpi"] = 300
    rcParams["savefig.facecolor"] = "w"
    rcParams["axes.formatter.useoffset"] = False
    rcParams["figure.dpi"] = 100
    rcParams["figure.figsize"] = [10, 7]

    rcParams["xtick.major.size"] = 5.0
    rcParams["xtick.minor.size"] = 2.5
    rcParams["ytick.major.size"] = 5.0
    rcParams["ytick.minor.size"] = 2.5

    rcParams["axes.titlesize"] = 22
    rcParams["font.size"] = 20
    rcParams["axes.labelsize"] = 20
    rcParams["xtick.labelsize"] = 16
    rcParams["ytick.labelsize"] = 16
    rcParams["legend.fontsize"] = 18

    rcParams["patch.edgecolor"] = colors.almost_black
    rcParams["text.color"] = colors.almost_black
    rcParams["axes.edgecolor"] = colors.almost_black
    rcParams["axes.labelcolor"] = colors.almost_black
    rcParams["xtick.color"] = colors.almost_black
    rcParams["ytick.color"] = colors.almost_black
    rcParams["grid.color"] = colors.almost_black

    # I like my own color cycle
    rcParams["axes.prop_cycle"] = cycler("color", colors.color_cycle)
    # change the colormap while I'm at it.
    rcParams["image.cmap"] = "viridis"


def _set_font_settings(font, fontweight):
    """
    Sets the font settings, used by most styles.

    :return: None
    """
    # Some good sans-serif font options: Lato, Nunito, Nunito Sans, Open Sans,
    # Jost, Cabin, Tajawal, Muli, Rubik, Assistant, Alata
    # serif: PT Serif
    # fun: Lobster

    # The font doesn't actually have to be sans-serif, we're just setting that
    # as a default since we currently don't know what family the requested
    # font is. And for our purposes it doesn't matter, since it works fine if
    # we tell matplotlib it's a sans-serif font, even if it's not.

    rcParams["font.family"] = "sans-serif"
    rcParams["font.sans-serif"] = font
    rcParams["text.usetex"] = False

    # change math font too
    rcParams["mathtext.fontset"] = "custom"
    rcParams["mathtext.default"] = "regular"

    # set the rest of the default parameters
    rcParams["font.weight"] = fontweight
    rcParams["axes.labelweight"] = fontweight
    rcParams["axes.titleweight"] = fontweight

    # The user might request a font that's not downloaded. To check this, we'll
    # see if the found font is the default. If so, we'll download the font
    fm = font_manager.FontManager()
    default_font = fm.defaultFont["ttf"]
    found_font = fm.findfont(font, rebuild_if_missing=True)

    # download the font if we need to. We need to if we got the default font instead of
    # what we wanted (although we check if the default font is in fact what we wanted)
    if default_font == found_font and not font.lower().startswith("dejavu"):
        print("- Downloading font: {}".format(font))
        print("- You may need to rerun this script or restart this jupyter")
        print("  notebook for these changes to take effect.")
        print("- This only needs to be done once.")
        font_dir = Path(matplotlib.get_data_path()) / "fonts/ttf/"
        download_font(font, font_dir)

        # remove the font cache
        cache_dir = Path(matplotlib.get_cachedir())
        for item in cache_dir.iterdir():
            if item.name.startswith("font"):
                item.unlink()

        # make sure it worked
        fm = font_manager.FontManager()
        assert fm.findfont(font, rebuild_if_missing=True) != fm.defaultFont["ttf"]


def _download_file(url, local_dir):
    filename = url.split("/")[-1]
    local_filename = local_dir / filename
    try:
        urllib.request.urlretrieve(url, filename=local_filename)
    except urllib.error.HTTPError:
        raise ValueError("File was not found (404): {}".format(url))


def download_font(fontname, dir):
    # https://github.com/google/fonts
    # format the font as it is in the github repo
    fontname = fontname.lower().replace(" ", "")

    base_url = "https://raw.githubusercontent.com/google/fonts/master/"
    # we don't know what license the font uses, so we need to search for it
    licenses = ["apache", "ofl", "ufl"]
    found = False
    for l in licenses:
        font_dir_url = os.path.join(base_url, l, fontname)

        # try to get the metadata file
        metadata_url = os.path.join(font_dir_url, "METADATA.pb")
        # the download will throw an error if it's not found
        try:
            _download_file(metadata_url, dir)
            found = True
            break  # needed so we keep the right license and therefore URL
        except ValueError:
            continue

    if not found:
        raise ValueError("Font not found!")

    # then get the filenames from the metadata file. We do need to watch out
    # for variable fonts.
    metadata_path = dir / "METADATA.pb"
    with open(metadata_path, "r") as metadata_file:
        metadata = [line.strip() for line in metadata_file]

    # remove the metadata file
    metadata_path.unlink()

    # see if we have a variable font. This particular line will note one of the
    # variable font axes
    variable = "axes {" in metadata

    if not variable:
        # In non-variable fonts, the filenames are all listed in the metadata
        for line in metadata:
            if line.startswith("filename:"):
                filename = line.split()[-1]
                # this will have quotes, remove them
                filename = filename.replace('"', "")
                # then we can just download it
                ttf_url = os.path.join(font_dir_url, filename)
                _download_file(ttf_url, dir)
                print("  - Downloading {}".format(filename))

    else:  # we do have a variable font
        # the metadata file does not list all the files, as they may be in the
        # "static" subdirectory. We have to manually find those files. But not every
        # font has the static subdirectory. So we'll look for static, but if we don't
        # find it just download the variable font files.
        # first get the name of the font as it will appear in the file
        for md in metadata:
            if md.startswith("filename:"):
                full_name = md.split()[-1]
                # only get the part before the bracket
                idx = full_name.find("[")
                # there is a " at the beginning we ignore
                file_base_name = full_name[1:idx]
                break

        # we then iterate through all possible font names. Thankfully the names
        # follow a regular pattern: FontName-WeightItalics.ttf. We'll iterate
        # through all options and grab the ones that exist
        weights = [
            "Thin",
            "ExtraLight",
            "Light",
            "Regular",
            "Medium",
            "SemiBold",
            "Bold",
            "ExtraBold",
            "Black",
            "",
        ]
        found_any = False
        for weight in weights:
            for italic in ["Italic", ""]:
                ttf_name = "{}-{}{}.ttf".format(file_base_name, weight, italic)

                ttf_url = os.path.join(font_dir_url, "static", ttf_name)

                # some of these will not exist, which is fine. Grab what exists
                try:
                    _download_file(ttf_url, dir)
                    print("  - Downloading {}".format(ttf_name))
                    found_any = True
                except ValueError:
                    pass

        # if we couldn't find any static files, just download the variable files
        if not found_any:
            # get all the filenames
            for md in metadata:
                if md.startswith("filename:"):
                    filename = md.split()[-1]
                    # this will have quotes, remove them
                    filename = filename.replace('"', "")
                    # then we can just download it
                    ttf_url = os.path.join(font_dir_url, filename)
                    _download_file(ttf_url, dir)
                    print("  - Downloading {}".format(filename))
