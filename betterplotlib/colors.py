import palettable

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
