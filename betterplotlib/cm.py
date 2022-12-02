# this reads the colormaps
from pathlib import Path
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import register_cmap

colormap_dir = Path(__file__).parent / "colormaps"

for cmap_file in colormap_dir.iterdir():
    if not cmap_file.suffix == ".txt":
        continue
    cmap_name = cmap_file.stem
    cm_data = np.loadtxt(cmap_file)
    cmap = LinearSegmentedColormap.from_list(cmap_name, cm_data)
    register_cmap(cmap_name, cmap)
