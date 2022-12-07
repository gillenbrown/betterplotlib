from matplotlib import colors as mpl_colors
from matplotlib import cm

almost_black = "#262626"
light_gray = "#E5E5E5"
light_grey = light_gray
steel_blue = "#3F5D7D"
# I saw the national park road signs and loved the color, so I found it. Here
# is the source if you want (PDF):
# http://www.pc.gc.ca/eng/docs/bib-lib/~/media/docs/bib-lib/pdfs/Exterior_Signage.ashx
# Search for Parks Canada Heritage Green, and you will see that it is the
# color on the signs, and that they give the pantone shade. I found a tool
# online that can convert that to the hex color.
parks_canada_heritage_green = "#284734"
pchg = parks_canada_heritage_green  # alias

# see the notebook in the docs folder for a description of why these colors
# were chosen
color_cycle = [
    "#4b5387",
    "#9bcfb3",
    "#919191",
    "#ac4649",
    "#d5b130",
    "#5b8070",
    "#ce9269",
    "#8b77a5",
]

# Some functions to fade and unfade colors, which can be helpful when plotting
# two lines with similar meaning
def fade_color(color):
    """
    Create a faded version of a different color

    :param color: the original color. Can be in any format
    :return: the hex color of the faded version
    :rtype: str

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np
        bpl.set_style()

        c = "#ac4649"
        fig, ax = bpl.subplots()

        ax.axhline(2, lw=20, c=c)
        ax.axhline(1, lw=20, c=bpl.fade_color(c))
        ax.axhline(0, lw=20, c=bpl.unfade_color(bpl.fade_color(c)))

        ax.add_text(0.5, 2.1, "Original", va="bottom", ha="center")
        ax.add_text(0.5, 1.1, "Faded", va="bottom", ha="center")
        ax.add_text(0.5, 0.1, "Faded then Unfaded", va="bottom", ha="center")

        ax.set_limits(0, 1, -1, 3)
        ax.remove_labels("both")
    """
    rgb = mpl_colors.to_rgb(color)
    hsv = mpl_colors.rgb_to_hsv(rgb)
    h = hsv[0]
    s = hsv[1] / 3.0  # remove saturation
    # make things lighter - 3/4 of the way to full brightness. In combination
    # with the reduction in saturation, it basically fades things whiter
    v = hsv[2] + (1.0 - hsv[2]) * 0.75

    return mpl_colors.rgb2hex(mpl_colors.hsv_to_rgb([h, s, v]))


def unfade_color(color):
    """
    Undo the fading applied by `fade_color`

    :param color: the faded color. Can be in any format. This color must have a low
                  enough saturation to be unfaded. A ValueError will be raised if this
                  color is too saturated to be unfaded.
    :return: the hex color of the unfaded version
    :rtype: str

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np
        bpl.set_style()

        c = "#ac4649"
        fig, ax = bpl.subplots()

        ax.axhline(2, lw=20, c=c)
        ax.axhline(1, lw=20, c=bpl.fade_color(c))
        ax.axhline(0, lw=20, c=bpl.unfade_color(bpl.fade_color(c)))

        ax.add_text(0.5, 2.1, "Original", va="bottom", ha="center")
        ax.add_text(0.5, 1.1, "Faded", va="bottom", ha="center")
        ax.add_text(0.5, 0.1, "Faded then Unfaded", va="bottom", ha="center")

        ax.set_limits(0, 1, -1, 3)
        ax.remove_labels("both")
    """
    rgb = mpl_colors.to_rgb(color)
    hsv = mpl_colors.rgb_to_hsv(rgb)
    h = hsv[0]

    # can't unfade colors that are already too saturated
    if hsv[1] > 1 / 3:
        raise ValueError("This color is too saturated to be unfaded")
    s = hsv[1] * 3.0  # restore saturation
    # earlier we went 3/4 of the way to full brighness. So to restore it, we
    # need to take this down 3 times the different between the current v and
    # full v
    v = hsv[2] - (3 * (1.0 - hsv[2]))

    return mpl_colors.rgb2hex(mpl_colors.hsv_to_rgb([h, s, v]))


def create_mappable(vmin, vmax, cmap, log=False):
    """
    Create a ScalarMappable, which is used to get colors from a colorbar

    This is also often used to seed a colorbar.

    :param vmin: Value corresponding to the minimum value of the colormap
    :type vmin: float
    :param vmax: Value corresponding to the maximum value of the colormap
    :type vmax: float
    :param cmap: The colormap to use. Can be a string with the colormap name
                 or a colormap object
    :param log: Whether or not to use log scaling on the normalization between
                vmin and vmax
    :type log: bool
    :returns: The ScalarMappable object
    :rtype: matplotlib.cm.ScalarMappable

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np

        bpl.set_style()

        mappable = bpl.create_mappable(0, 1, "Blues")
        fig, ax = bpl.subplots()
        for i in np.arange(0, 1.01, 0.1):
            ax.plot([0, 1], [i, i], c=mappable.to_rgba(i))
        ax.set_limits(0, 1, -0.05, 1.05)
        fig.colorbar(mappable)

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np

        bpl.set_style()

        mappable = bpl.create_mappable(1, 100, "Blues", log=True)
        fig, ax = bpl.subplots()
        for i in np.logspace(0, 2, 10):
            ax.plot([0, 1], [i, i], c=mappable.to_rgba(i))
        ax.log("y")
        ax.set_limits(0, 1, 0.9, 110)
        fig.colorbar(mappable)
    """
    if log:
        norm = mpl_colors.LogNorm(vmin=vmin, vmax=vmax)
    else:
        norm = mpl_colors.Normalize(vmin=vmin, vmax=vmax)
    return cm.ScalarMappable(norm=norm, cmap=cmap)
