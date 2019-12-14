import palettable
from matplotlib import colors as mpl_colors

almost_black = '#262626'
light_gray = '#E5E5E5'
light_grey = light_gray
steel_blue = '#3F5D7D'
# I saw the national park road signs and loved the color, so I found it. Here
# is the source if you want (PDF):
# http://www.pc.gc.ca/eng/docs/bib-lib/~/media/docs/bib-lib/pdfs/Exterior_Signage.ashx
# Search for Parks Canada Heritage Green, and you will see that it is the
# color on the signs, and that they give the pantone shade. I found a tool
# online that can convert that to the hex color.
parks_canada_heritage_green = '#284734'
pchg = parks_canada_heritage_green  # alias

color_cycle_map = palettable.cartocolors.qualitative.Pastel_10.hex_colors
color_cycle = [color_cycle_map[5],
               color_cycle_map[4],
               color_cycle_map[6],
               color_cycle_map[2],
               color_cycle_map[3],
               color_cycle_map[1],
               color_cycle_map[0],
               color_cycle_map[8],
               color_cycle_map[9],
               color_cycle_map[7]
              ]

# Some functions to fade and unfade colors, which can be helpful when plotting
# two lines with similar meaning
def fade_color(color):
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
    s = hsv[1] * 3.0 # restore saturation
    # earlier we went 3/4 of the way to full brighness. So to restore it, we
    # need to take this down 3 times the different between the current v and
    # full v
    v = hsv[2] - (3 * (1.0 - hsv[2]))

    return mpl_colors.hsv_to_rgb([h, s, v])
