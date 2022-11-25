from matplotlib import colors as mpl_colors

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

        color = "#9bcfb3"
        fig, ax = bpl.subplots()
        ax.axhline(1, c=color, label="Original")
        ax.axhline(0, c=bpl.fade_color(color), label="Faded")
    """
    rgb = mpl_colors.to_rgb(color)
    hsv = mpl_colors.rgb_to_hsv(rgb)
    h = hsv[0]
    s = hsv[1] / 3.0  # remove saturation
    # make things lighter - 3/4 of the way to full brightness. In combination
    # with the reduction in saturation, it basically fades things whiter
    v = hsv[2] + (1.0 - hsv[2]) * 0.75

    return mpl_colors.hsv_to_rgb([h, s, v])


def unfade_color(color):
    rgb = mpl_colors.to_rgb(color)
    hsv = mpl_colors.rgb_to_hsv(rgb)
    h = hsv[0]
    s = hsv[1] * 3.0  # restore saturation
    # earlier we went 3/4 of the way to full brighness. So to restore it, we
    # need to take this down 3 times the different between the current v and
    # full v
    v = hsv[2] - (3 * (1.0 - hsv[2]))

    return mpl_colors.hsv_to_rgb([h, s, v])
