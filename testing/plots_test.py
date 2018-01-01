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
xs_normal_10000 = np.random.normal(0, 1, 10000)
ys_normal_10000 = np.random.normal(0, 1, 10000)

xs_uniform_10 = np.random.uniform(0, 1, 10)
ys_uniform_10 = np.random.uniform(0, 1, 10)


# ------------------------------------------------------------------------------
#
# define some common error messages to check against
#
# ------------------------------------------------------------------------------
no_iqr_msg = "The Freeman-Diaconis default binning relies on " \
             "inter-quartile range, and your data has zero.\n" \
             "Try passing your own bin size."

empty_data_msg = "Empty list is not valid for data."
xy_length_msg = "x and y data must be the same length."

bin_size_positive_msg = "Bin size must be positive."
bin_size_typing_msg = "Bin_size must be either a scalar or " \
                      "two element numeric list."

smoothing_nonnegative_msg = "Smoothing must be nonnegative."
smoothing_typing_msg = "Smoothing must be either a scalar or " \
                       "two element numeric list."

weights_nonnegative_msg = "Weights must be non-negative."
weights_wrong_length = "Weights and data need to have the same length."
weights_typing_msg = "Weights must be a numerical array."

percent_levels_typing_msg = "Percent_levels needs to be a numeric list."
percent_levels_duplicates_msg = "The percent levels chosen lead to duplicate " \
                                "levels.\nContour levels must be increasing."
percent_levels_range_msg = "Percentages must be between 0 and 1."

colormap_msg_part = "is not recognized. Possible values are: Accent"

data_not_all_same_msg = "All points are identical. This breaks matplotlib " \
                        "contours for some reason. Try other data."

levels_contour_err_msg = "The levels parameter is set by this function. " \
                         "Do not pass it in. "

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
def test_density_contour_error_checking_data_length_nonzero():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contour([], [], bin_size=0.1, percent_levels=0.5)
    assert str(err_msg.value) == empty_data_msg


def test_density_contour_error_checking_data_not_all_same():
    xs = [1, 1, 1, 1]
    ys = [4, 4, 4, 4]
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contour(xs, ys, bin_size=0.1, percent_levels=0.5)
    assert str(err_msg.value) == data_not_all_same_msg


def test_density_contour_error_checking_data_no_variation_needs_bin_size():
    xs = [1, 2, 2, 2, 2, 2, 2, 3]
    ys = [1, 2, 2, 2, 2, 2, 2, 3]
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contour(xs, ys, percent_levels=0.5)
    assert str(err_msg.value) == no_iqr_msg
    ax.density_contour(xs, ys, bin_size=0.1, percent_levels=0.5)


def test_density_contour_error_checking_data_length_needs_same():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contour([1, 2, 3], [1, 2])
    assert str(err_msg.value) == xy_length_msg


@pytest.mark.parametrize("bin_size,err,msg", [
    (-1,         ValueError, bin_size_positive_msg),
    ([-1, 5],    ValueError, bin_size_positive_msg),
    ([1, -5],    ValueError, bin_size_positive_msg),
    ([0, 5],     ValueError, bin_size_positive_msg),
    ([1, 5, 3],  ValueError, bin_size_typing_msg),
    ([],         ValueError, bin_size_typing_msg),
    (["a", "b"], TypeError,  bin_size_typing_msg)
])
def test_density_contour_error_checking_bin_size(bin_size, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.density_contour(xs_uniform_10, ys_uniform_10, bin_size)
    assert str(err_msg.value) == msg


@pytest.mark.parametrize("smoothing,err,msg", [
    (-1,         ValueError, smoothing_nonnegative_msg),
    ([-1, 5],    ValueError, smoothing_nonnegative_msg),
    ([1, -5],    ValueError, smoothing_nonnegative_msg),
    ([1, 5, 3],  ValueError, smoothing_typing_msg),
    ([],         ValueError, smoothing_typing_msg),
    (["a", "b"], TypeError,  smoothing_typing_msg)
])
def test_density_contour_error_checking_smoothing(smoothing, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.density_contour(xs_uniform_10, ys_uniform_10, smoothing=smoothing)
    assert str(err_msg.value) == msg


def test_density_contour_error_checking_colormap():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contour(xs_uniform_10, ys_uniform_10, cmap="sdfsd",
                           percent_levels=0.5)
    assert colormap_msg_part in str(err_msg.value)


@pytest.mark.parametrize("weights,err,msg", [
    (-1 * xs_uniform_10, ValueError, weights_nonnegative_msg),
    ([1, 5, 3],          ValueError, weights_wrong_length),
    (["a", "b"],         TypeError,  weights_typing_msg)
])
def test_density_contour_error_checking_weights(weights, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.density_contour(xs_uniform_10, ys_uniform_10, weights=weights)
    assert str(err_msg.value) == msg


@pytest.mark.parametrize("percents,err,msg", [
    (["a"],       TypeError,  percent_levels_typing_msg),
    ([0.45, 0.451],  ValueError, percent_levels_duplicates_msg),
    ([-0.4, 0.5], ValueError, percent_levels_range_msg),
    ([0.4, 1.01], ValueError, percent_levels_range_msg)
])
def test_density_contour_error_checking_percent_levels(percents, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.density_contour(xs_uniform_10, ys_uniform_10,
                           percent_levels=percents)
    assert str(err_msg.value) == msg


def test_density_contour_levels_not_in_kwargs():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contour(xs_uniform_10, ys_uniform_10, levels=[1])
    assert str(err_msg.value) == levels_contour_err_msg


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
def test_density_contourf_error_checking_data_length_nonzero():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contourf([], [], bin_size=0.1, percent_levels=0.5)
    assert str(err_msg.value) == empty_data_msg


def test_density_contourf_error_checking_data_not_all_same():
    xs = [1, 1, 1, 1]
    ys = [4, 4, 4, 4]
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contourf(xs, ys, bin_size=0.1, percent_levels=0.5)
    assert str(err_msg.value) == data_not_all_same_msg


def test_density_contourf_error_checking_data_no_variation_needs_bin_size():
    xs = [1, 2, 2, 2, 2, 2, 2, 3]
    ys = [1, 2, 2, 2, 2, 2, 2, 3]
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contourf(xs, ys, percent_levels=0.5)
    assert str(err_msg.value) == no_iqr_msg
    ax.density_contourf(xs, ys, bin_size=0.1, percent_levels=0.5)


def test_density_contourf_error_checking_data_length_needs_same():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contourf([1, 2, 3], [1, 2])
    assert str(err_msg.value) == xy_length_msg


@pytest.mark.parametrize("bin_size,err,msg", [
    (-1,         ValueError, bin_size_positive_msg),
    ([-1, 5],    ValueError, bin_size_positive_msg),
    ([1, -5],    ValueError, bin_size_positive_msg),
    ([0, 5],     ValueError, bin_size_positive_msg),
    ([1, 5, 3],  ValueError, bin_size_typing_msg),
    ([],         ValueError, bin_size_typing_msg),
    (["a", "b"], TypeError,  bin_size_typing_msg)
])
def test_density_contourf_error_checking_bin_size(bin_size, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.density_contourf(xs_uniform_10, ys_uniform_10, bin_size)
    assert str(err_msg.value) == msg


@pytest.mark.parametrize("smoothing,err,msg", [
    (-1,         ValueError, smoothing_nonnegative_msg),
    ([-1, 5],    ValueError, smoothing_nonnegative_msg),
    ([1, -5],    ValueError, smoothing_nonnegative_msg),
    ([1, 5, 3],  ValueError, smoothing_typing_msg),
    ([],         ValueError, smoothing_typing_msg),
    (["a", "b"], TypeError,  smoothing_typing_msg)
])
def test_density_contourf_error_checking_smoothing(smoothing, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.density_contourf(xs_uniform_10, ys_uniform_10, smoothing=smoothing)
    assert str(err_msg.value) == msg


def test_density_contourf_error_checking_colormap():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contourf(xs_uniform_10, ys_uniform_10, cmap="sdfsd",
                           percent_levels=0.5)
    assert colormap_msg_part in str(err_msg.value)


@pytest.mark.parametrize("weights,err,msg", [
    (-1 * xs_uniform_10, ValueError, weights_nonnegative_msg),
    ([1, 5, 3],          ValueError, weights_wrong_length),
    (["a", "b"],         TypeError,  weights_typing_msg)
])
def test_density_contourf_error_checking_weights(weights, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.density_contourf(xs_uniform_10, ys_uniform_10, weights=weights)
    assert str(err_msg.value) == msg


@pytest.mark.parametrize("percents,err,msg", [
    (["a"],       TypeError,  percent_levels_typing_msg),
    ([0.45, 0.451],  ValueError, percent_levels_duplicates_msg),
    ([-0.4, 0.5], ValueError, percent_levels_range_msg),
    ([0.4, 1.01], ValueError, percent_levels_range_msg)
])
def test_density_contourf_error_checking_percent_levels(percents, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.density_contourf(xs_uniform_10, ys_uniform_10,
                           percent_levels=percents)
    assert str(err_msg.value) == msg


def test_density_contourf_levels_not_in_kwargs():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contourf(xs_uniform_10, ys_uniform_10, levels=[1])
    assert str(err_msg.value) == levels_contour_err_msg


def test_density_contourf_no_labels():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contourf(xs_uniform_10, ys_uniform_10, labels=True)
    assert str(err_msg.value) == "Filled contours cannot have labels."


# ------------------------------------------------------------------------------
#
# Testing contour_scatter
#
# ------------------------------------------------------------------------------
def test_contour_scatter_error_checking_data_length_nonzero():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.contour_scatter([], [], bin_size=0.1, percent_levels=0.5)
    assert str(err_msg.value) == empty_data_msg


def test_contour_scatter_error_checking_data_not_all_same():
    xs = [1, 1, 1, 1]
    ys = [4, 4, 4, 4]
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.contour_scatter(xs, ys, bin_size=0.1, percent_levels=0.5)
    assert str(err_msg.value) == data_not_all_same_msg


def test_contour_scatter_error_checking_data_no_variation_needs_bin_size():
    xs = [1, 2, 2, 2, 2, 2, 2, 3]
    ys = [1, 2, 2, 2, 2, 2, 2, 3]
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.contour_scatter(xs, ys, percent_levels=0.5)
    assert str(err_msg.value) == no_iqr_msg
    ax.contour_scatter(xs, ys, bin_size=0.1, percent_levels=0.5)


def test_contour_scatter_error_checking_data_length_needs_same():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.contour_scatter([1, 2, 3], [1, 2])
    assert str(err_msg.value) == xy_length_msg


@pytest.mark.parametrize("bin_size,err,msg", [
    (-1,         ValueError, bin_size_positive_msg),
    ([-1, 5],    ValueError, bin_size_positive_msg),
    ([1, -5],    ValueError, bin_size_positive_msg),
    ([0, 5],     ValueError, bin_size_positive_msg),
    ([1, 5, 3],  ValueError, bin_size_typing_msg),
    ([],         ValueError, bin_size_typing_msg),
    (["a", "b"], TypeError,  bin_size_typing_msg)
])
def test_contour_scatter_error_checking_bin_size(bin_size, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.contour_scatter(xs_normal_10000, ys_normal_10000, bin_size)
    assert str(err_msg.value) == msg


@pytest.mark.parametrize("smoothing,err,msg", [
    (-1,         ValueError, smoothing_nonnegative_msg),
    ([-1, 5],    ValueError, smoothing_nonnegative_msg),
    ([1, -5],    ValueError, smoothing_nonnegative_msg),
    ([1, 5, 3],  ValueError, smoothing_typing_msg),
    ([],         ValueError, smoothing_typing_msg),
    (["a", "b"], TypeError,  smoothing_typing_msg)
])
def test_contour_scatter_error_checking_smoothing(smoothing, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.contour_scatter(xs_normal_10000, ys_normal_10000, smoothing=smoothing)
    assert str(err_msg.value) == msg


def test_contour_scatter_error_checking_colormap():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.contour_scatter(xs_normal_10000, ys_normal_10000, fill_cmap="sdfsd")
    assert colormap_msg_part in str(err_msg.value)


@pytest.mark.parametrize("weights,err,msg", [
    (xs_normal_10000, ValueError, weights_nonnegative_msg),
    ([1, 5, 3],       ValueError, weights_wrong_length),
    (["a", "b"],      TypeError,  weights_typing_msg)
])
def test_contour_scatter_error_checking_weights(weights, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.contour_scatter(xs_normal_10000, ys_normal_10000, weights=weights)
    assert str(err_msg.value) == msg


@pytest.mark.parametrize("percents,err,msg", [
    (["a"],       TypeError,  percent_levels_typing_msg),
    ([0.45, 0.451],  ValueError, percent_levels_duplicates_msg),
    ([-0.4, 0.5], ValueError, percent_levels_range_msg),
    ([0.4, 1.01], ValueError, percent_levels_range_msg)
])
def test_contour_scatter_error_checking_percent_levels(percents, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.contour_scatter(xs_normal_10000, ys_normal_10000,
                           percent_levels=percents)
    assert str(err_msg.value) == msg


def test_contour_scatter_error_checking_no_labels_contourf():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.contour_scatter(xs_normal_10000, ys_normal_10000,
                           contourf_kwargs={"labels": True})
    assert str(err_msg.value) == "Filled contours cannot have labels."


def test_contour_scatter_error_checking_no_levels_contour():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.contour_scatter(xs_normal_10000, ys_normal_10000,
                           contour_kwargs={"levels": [1]})
    assert str(err_msg.value) == levels_contour_err_msg


def test_contour_scatter_error_checking_no_levels_contourf():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.contour_scatter(xs_normal_10000, ys_normal_10000,
                           contourf_kwargs={"levels": [1]})
    assert str(err_msg.value) == levels_contour_err_msg


# def test_contour_scatter_scatter_outside_contours():
#     xs = np.concatenate([xs_normal_10000, xs_normal_10000 + 5])
#     ys = np.concatenate([ys_normal_10000, ys_normal_10000 + 5])
#
#     fig, ax = bpl.subplots()
#     ax.scatter(xs, ys, c=bpl.color_cycle[1], s=2, alpha=1, zorder=4)
#     ax.contour_scatter(xs, ys, bin_size=0.01, smoothing=0.2,
#                        scatter_kwargs={"s":20, "zorder":3})
#     ax.equal_scale()
#     assert image_similarity_full(fig, "contour_scatter_outside_contours.png")


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
    assert str(err_msg.value) == empty_data_msg


def test_shaded_density_error_checking_data_length_one_needs_bin_size():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.shaded_density([1], [1])
    assert str(err_msg.value) == no_iqr_msg
    ax.shaded_density([1], [1], bin_size=0.1)  # no error


def test_shaded_density_error_checking_data_no_variation_needs_bin_size():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.shaded_density([1, 1, 1, 1], [1, 1, 1, 1])
    assert str(err_msg.value) == no_iqr_msg
    ax.shaded_density([1, 1, 1, 1], [1, 1, 1, 1], bin_size=0.1)  # no error


def test_shaded_density_error_checking_data_length_needs_same():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.shaded_density([1, 2, 3], [1, 2])
    assert str(err_msg.value) == xy_length_msg


@pytest.mark.parametrize("bin_size,err,msg", [
    (-1,         ValueError, bin_size_positive_msg),
    ([-1, 5],    ValueError, bin_size_positive_msg),
    ([1, -5],    ValueError, bin_size_positive_msg),
    ([0, 5],     ValueError, bin_size_positive_msg),
    ([1, 5, 3],  ValueError, bin_size_typing_msg),
    ([],         ValueError, bin_size_typing_msg),
    (["a", "b"], TypeError,  bin_size_typing_msg)
])
def test_shaded_density_error_checking_bin_size(bin_size, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.shaded_density(xs_uniform_10, ys_uniform_10, bin_size)
    assert str(err_msg.value) == msg


@pytest.mark.parametrize("smoothing,err,msg", [
    (-1,         ValueError, smoothing_nonnegative_msg),
    ([-1, 5],    ValueError, smoothing_nonnegative_msg),
    ([1, -5],    ValueError, smoothing_nonnegative_msg),
    ([1, 5, 3],  ValueError, smoothing_typing_msg),
    ([],         ValueError, smoothing_typing_msg),
    (["a", "b"], TypeError,  smoothing_typing_msg)
])
def test_shaded_density_error_checking_smoothing(smoothing, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.shaded_density(xs_uniform_10, ys_uniform_10, smoothing=smoothing)
    assert str(err_msg.value) == msg


def test_shaded_density_error_checking_colormap():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.shaded_density(xs_uniform_10, ys_uniform_10, cmap="sdfsd")
    assert colormap_msg_part in str(err_msg.value)


@pytest.mark.parametrize("weights,err,msg", [
    (-1 * xs_uniform_10, ValueError, weights_nonnegative_msg),
    ([1, 5, 3],          ValueError, weights_wrong_length),
    (["a", "b"],         TypeError,  weights_typing_msg)
])
def test_shaded_density_error_checking_weights(weights, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.shaded_density(xs_uniform_10, ys_uniform_10, weights=weights)
    assert str(err_msg.value) == msg


# def test_shaded_density_no_parameters_image():
#     fig, ax = bpl.subplots()
#     ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
#     ax.shaded_density(xs_uniform_10, ys_uniform_10)
#     ax.equal_scale()
#     ax.set_limits(0, 1, 0, 1)
#     assert image_similarity_full(fig, "shaded_density_basic.png")
#
#
# def test_shaded_density_points_are_inside_image():
#     """Test that the scatter points to indeed lie in the regions they should."""
#     fig, ax = bpl.subplots()
#     ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
#     ax.shaded_density(xs_uniform_10, ys_uniform_10, bin_size=0.01,
#                       smoothing=0, cmap="Greens")
#     for x in xs_uniform_10:
#         ax.axvline(x, lw=0.01)
#     for y in ys_uniform_10:
#         ax.axhline(y, lw=0.01)
#     ax.equal_scale()
#     ax.set_limits(0, 1, 0, 1)
#     assert image_similarity_full(fig, "shaded_density_with_scatter.png")
#
#
# def test_shaded_density_points_with_smoothing_image():
#     fig, ax = bpl.subplots()
#     ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
#     ax.shaded_density(xs_uniform_10, ys_uniform_10, bin_size=0.01,
#                       smoothing=0.1, cmap="viridis")
#     ax.equal_scale()
#     ax.set_limits(0, 1, 0, 1)
#     assert image_similarity_full(fig, "shaded_density_with_smoothing.png")
#
#
# def test_shaded_density_points_specify_bin_size_image():
#     fig, ax = bpl.subplots()
#     ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
#     ax.shaded_density(xs_uniform_10, ys_uniform_10, bin_size=[0.2, 0.25])
#     ax.equal_scale()
#     ax.set_limits(0, 1, 0, 1)
#     assert image_similarity_full(fig, "shaded_density_bin_size.png")
#
#
# def test_shaded_density_points_variable_bin_size_image():
#     fig, ax = bpl.subplots()
#     ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
#     ax.shaded_density(xs_uniform_10, ys_uniform_10, bin_size=0.01,
#                       smoothing=[0.5, 0.05])
#     ax.equal_scale()
#     ax.set_limits(0, 1, 0, 1)
#     assert image_similarity_full(fig, "shaded_density_smoothing.png")
#
#
# def test_shaded_density_with_weights_image():
#     xs = [0.2, 0.4, 0.6, 0.8]
#     ys = [0.2, 0.4, 0.6, 0.8]
#     weights = [1, 2, 3, 4]
#
#     fig, ax = bpl.subplots()
#     ax.shaded_density(xs, ys, weights=weights, bin_size=0.01,
#                       smoothing=[0.05, 0.2], cmap="ocean")
#     ax.equal_scale()
#     ax.set_limits(0, 1, 0, 1)
#     assert image_similarity_full(fig, "shaded_density_weights.png")
