# this reads the colormaps
import numpy as np
import os
from matplotlib.colors import LinearSegmentedColormap

this_dir = os.path.abspath(os.path.dirname(__file__))
colormap_dir = os.path.join(this_dir, "colormaps")


def _get_colormap(cmap_name):
    data_file = os.path.join(colormap_dir, cmap_name + ".txt")
    cm_data = np.loadtxt(data_file)
    return LinearSegmentedColormap.from_list(cmap_name, cm_data)


acton = _get_colormap("acton")
bamako = _get_colormap("bamako")
batlow = _get_colormap("batlow")
berlin = _get_colormap("berlin")
bilbao = _get_colormap("bilbao")
broc = _get_colormap("broc")
buda = _get_colormap("buda")
cork = _get_colormap("cork")
davos = _get_colormap("davos")
devon = _get_colormap("devon")
grayC = _get_colormap("grayC")
hawaii = _get_colormap("hawaii")
imola = _get_colormap("imola")
lajolla = _get_colormap("lajolla")
lapaz = _get_colormap("lapaz")
lisbon = _get_colormap("lisbon")
nuuk = _get_colormap("nuuk")
oleron = _get_colormap("oleron")
oslo = _get_colormap("oslo")
roma = _get_colormap("roma")
tofino = _get_colormap("tofino")
tokyo = _get_colormap("tokyo")
turku = _get_colormap("turku")
vik = _get_colormap("vik")
