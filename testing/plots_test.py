import imageio
import numpy as np
import os
import pytest
from matplotlib.ticker import MultipleLocator

import betterplotlib as bpl
bpl.default_style()

this_dir = os.path.realpath(os.path.split(__file__)[0])
baseline_im_dir = this_dir + os.sep + "baseline_images" + os.sep
new_im_dir = this_dir + os.sep + "temporary_images" + os.sep

def image_similarity(im_1_path, im_2_path):
    """
    Compare two images to see if they are identical.

    :param im_1_path: Path of the first image. Should be a png.
    :type im_1_path: str
    :param im_2_path: Path of the second image. Should be a png.
    :type im_2_path: str
    :return: True if the images are identical, false if they are not.
    :rtype bool:
    """
    im_1 = imageio.imread(im_1_path)
    im_2 = imageio.imread(im_2_path)

    return abs(np.sum(im_1 - im_2)) < 1

def image_similarity_full(fig, image_name):
    new_img = new_im_dir + image_name
    baseline_img = baseline_im_dir + image_name

    fig.savefig(new_im_dir + image_name)

    return image_similarity(new_img, baseline_img)

# ------------------------------------------------------------------------------
#
# Testing make ax dark
#
# ------------------------------------------------------------------------------
def test_ax_dark():
    fig, [ax0, ax1, ax2] = bpl.subplots(ncols=3)
    ax0.make_ax_dark(minor_ticks=False)
    ax1.make_ax_dark(minor_ticks=True)
    ax2.make_ax_dark()
    assert image_similarity_full(fig, "dark.png")


# ------------------------------------------------------------------------------
#
# Testing make ax dark
#
# ------------------------------------------------------------------------------
def test_remove_ticks_wrong_values():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError):
        ax.remove_ticks("sdfs")
    with pytest.raises(ValueError):
        ax.remove_ticks(["sdfs", "top", "bottom"])

def test_remove_ticks_single_image():
    fig, [ax0, ax1, ax2, ax3, ax4] = bpl.subplots(ncols=5)
    ax0.remove_ticks("top")
    ax1.remove_ticks("bottom")
    ax2.remove_ticks("left")
    ax3.remove_ticks("right")
    ax4.remove_ticks("all")
    assert image_similarity_full(fig, "remove_ticks_single.png")


def test_remove_ticks_multiple_images():
    fig, [ax0, ax1, ax2, ax3] = bpl.subplots(ncols=4)
    ax0.remove_ticks("top", "bottom", "left")
    ax1.remove_ticks(["bottom", "top", "left"])
    ax2.remove_ticks("all")
    ax3.remove_ticks(["all"])
    assert image_similarity_full(fig, "remove_ticks_multiple.png")
