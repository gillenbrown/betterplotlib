# this reads the colormaps
import numpy as np
import os
from matplotlib.colors import LinearSegmentedColormap

colormap_dir = os.path.dirname(__file__) + "/colormaps/"

def get_colormap(cmap_name):
    data_file = colormap_dir + cmap_name + ".txt"
    cm_data = np.loadtxt(data_file)
    return LinearSegmentedColormap.from_list(cmap_name, cm_data)

acton = get_colormap("acton")
bamako = get_colormap("bamako")
batlow = get_colormap("batlow")
berlin = get_colormap("berlin")
bilbao = get_colormap("bilbao")
broc = get_colormap("broc")
buda = get_colormap("buda")
cork = get_colormap("cork")
davos = get_colormap("davos")
devon = get_colormap("devon")
grayC = get_colormap("grayC")
hawaii = get_colormap("hawaii")
imola = get_colormap("imola")
lajolla = get_colormap("lajolla")
lapaz = get_colormap("lapaz")
lisbon = get_colormap("lisbon")
nuuk = get_colormap("nuuk")
oleron = get_colormap("oleron")
oslo = get_colormap("oslo")
roma = get_colormap("roma")
tofino = get_colormap("tofino")
tokyo = get_colormap("tokyo")
turku = get_colormap("turku")
vik = get_colormap("vik")
