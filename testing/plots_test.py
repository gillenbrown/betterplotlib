import imageio
import numpy as np
import os
import pytest

import betterplotlib as bpl

bpl.default_style()
np.random.seed(314159)

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
# set up some random data
#
# ------------------------------------------------------------------------------
xs_normal = np.random.normal(0, 1, 10)
ys_normal = np.random.normal(0, 1, 10)

xs_uniform_10 = np.random.uniform(0, 1, 10)
ys_uniform_10 = np.random.uniform(0, 1, 10)


# ------------------------------------------------------------------------------
#
# Testing make ax dark
#
# ------------------------------------------------------------------------------
# def test_ax_dark():
#     fig, [ax0, ax1, ax2] = bpl.subplots(ncols=3)
#     ax0.make_ax_dark(minor_ticks=False)
#     ax1.make_ax_dark(minor_ticks=True)
#     ax2.make_ax_dark()
#     assert image_similarity_full(fig, "dark.png")


# ------------------------------------------------------------------------------
#
# Testing remove ticks
#
# ------------------------------------------------------------------------------
# def test_remove_ticks_wrong_values():
#     fig, ax = bpl.subplots()
#     with pytest.raises(ValueError):
#         ax.remove_ticks("sdfs")
#     with pytest.raises(ValueError):
#         ax.remove_ticks(["sdfs", "top", "bottom"])
#     with pytest.raises(ValueError):
#         ax.remove_ticks("left", "sdfs", "top", "bottom")


# def test_remove_ticks_single_image():
#     fig, [ax0, ax1, ax2, ax3, ax4] = bpl.subplots(ncols=5)
#     ax0.remove_ticks("top")
#     ax0.add_labels(title="top")
#     ax1.remove_ticks("bottom")
#     ax1.add_labels(title="bottom")
#     ax2.remove_ticks("left")
#     ax2.add_labels(title="left")
#     ax3.remove_ticks("right")
#     ax3.add_labels(title="right")
#     ax4.remove_ticks("all")
#     ax4.add_labels(title="all")
#     assert image_similarity_full(fig, "remove_ticks_single.png")
#
#
# def test_remove_ticks_multiple_images():
#     fig, [ax0, ax1, ax2, ax3] = bpl.subplots(ncols=4)
#     ax0.remove_ticks("top", "bottom", "left")
#     ax0.add_labels(title="top, bottom, left")
#     ax1.remove_ticks(["bottom", "top", "left"])
#     ax1.add_labels(title="top, bottom, left")
#     ax2.remove_ticks("all")
#     ax1.add_labels(title="all")
#     ax3.remove_ticks(["all"])
#     ax1.add_labels(title="all")
#     assert image_similarity_full(fig, "remove_ticks_multiple.png")


# ------------------------------------------------------------------------------
#
# Testing remove spines
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing scatter
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing hist
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing add labels
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing set limits
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing add_text
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing remove labels
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing legend
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing equal scale
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing easy add text
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing density contour
#
# ------------------------------------------------------------------------------
# def test_contour_percent_level_scalar_percentile():
#     fig, ax = bpl.subplots()
#     ax.scatter(xs_normal, ys_normal, s=5)
#     ax.density_contour(xs_normal, ys_normal, bin_size=0.1, percent_levels=0.4,
#                        smoothing=0.5)
#     ax.equal_scale()
#     ax.set_limits(-20, 20, -20, 20)
#     assert image_similarity_full(fig, "simple_density_contour.png")


# def test_contour_percent_level_list_percentile():
#     fig, ax = bpl.subplots()
#     ax.scatter(xs_normal, ys_normal, s=5)
#     ax.density_contour(xs_normal, ys_normal, bin_size=0.1,
#                        percent_levels=[0.4], smoothing=0.5)
#     ax.equal_scale()
#     ax.set_limits(-20, 20, -20, 20)
#     assert image_similarity_full(fig, "simple_density_contour.png")


# ------------------------------------------------------------------------------
#
# Testing density filled contour
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing contour_scatter
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing data ticks
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing plot
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing axvline
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing axhline
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing errorbar
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing twin axis simple
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing twin axis
#
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#
# Testing shaded density
#
# ------------------------------------------------------------------------------
def test_shaded_density_error_checking_data_length_nonzero():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.shaded_density([], [])
    assert str(err_msg.value) == "Empty lists are not valid data to plot."


def test_shaded_density_error_checking_data_length_one_needs_bin_size():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.shaded_density([1], [1])
    desired_msg = "The Freeman-Diaconis default binning relies on " \
                  "inter-quartile range, and your data has zero.\n" \
                  "Try passing your own bin size."
    assert str(err_msg.value) == desired_msg
    ax.shaded_density([1], [1], bin_size=0.1)  # no error


def test_shaded_density_error_checking_data_no_variation_needs_bin_size():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.shaded_density([1, 1, 1, 1], [1, 1, 1, 1])
    desired_msg = "The Freeman-Diaconis default binning relies on " \
                  "inter-quartile range, and your data has zero.\n" \
                  "Try passing your own bin size."
    assert str(err_msg.value) == desired_msg
    ax.shaded_density([1, 1, 1, 1], [1, 1, 1, 1], bin_size=0.1)  # no error


def test_shaded_density_error_checking_data_length_needs_same():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.shaded_density([1, 2, 3], [1, 2])
    desired_msg = "The length of the x and y data needs to be the same."
    assert str(err_msg.value) == desired_msg


def test_shaded_density_no_parameters_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
    ax.shaded_density(xs_uniform_10, ys_uniform_10)
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_basic.png")


def test_shaded_density_points_are_inside_image():
    """Test that the scatter points to indeed lie in the regions they should."""
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
    ax.shaded_density(xs_uniform_10, ys_uniform_10, bin_size=0.01,
                      smoothing=0, cmap="Greens")
    for x in xs_uniform_10:
        ax.axvline(x, lw=0.01)
    for y in ys_uniform_10:
        ax.axhline(y, lw=0.01)
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_with_scatter.png")


def test_shaded_density_points_with_smoothing_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
    ax.shaded_density(xs_uniform_10, ys_uniform_10, bin_size=0.01,
                      smoothing=0.1, cmap="viridis")
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_with_smoothing.png")


def test_shaded_density_points_specify_bin_size_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
    ax.shaded_density(xs_uniform_10, ys_uniform_10, bin_size=[0.2, 0.25])
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_bin_size.png")


def test_shaded_density_points_variable_bin_size_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
    ax.shaded_density(xs_uniform_10, ys_uniform_10, bin_size=0.01,
                      smoothing=[0.5, 0.05])
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_smoothing.png")


def test_shaded_density_with_weights_image():
    xs = [0.2, 0.4, 0.6, 0.8]
    ys = [0.2, 0.4, 0.6, 0.8]
    weights = [1, 2, 3, 4]

    fig, ax = bpl.subplots()
    ax.shaded_density(xs, ys, weights=weights, bin_size=0.01,
                      smoothing=[0.05, 0.2], cmap="ocean")
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_weights.png")
