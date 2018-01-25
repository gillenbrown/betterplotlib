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

    try:
        matched = image_similarity(new_img, baseline_img)
    except OSError:
        raise IOError("Baseline image does not exist.")
    if matched:
        os.remove(new_img)
    return matched


# ------------------------------------------------------------------------------
#
# set up some random data
#
# ------------------------------------------------------------------------------
xs_normal_10000 = np.random.normal(0, scale=1, size=10000)
ys_normal_10000 = np.random.normal(0, scale=1, size=10000)

xs_uniform_10 = np.random.uniform(0, 1, 10)
ys_uniform_10 = np.random.uniform(0, 1, 10)

xs_normal_500 = np.random.normal(0, scale=1, size=500)
ys_normal_500 = np.random.normal(0, scale=1, size=500)


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
                        "contours for some reason. Try other data, or smooth."

levels_contour_err_msg = "The levels parameter is set by this function. " \
                         "Do not pass it in. "

# ------------------------------------------------------------------------------
#
# Testing make ax dark
#
# ------------------------------------------------------------------------------
def test_ax_dark_image():
    fig, [ax0, ax1, ax2] = bpl.subplots(ncols=3)
    ax0.make_ax_dark(minor_ticks=False)
    ax1.make_ax_dark(minor_ticks=True)
    ax2.make_ax_dark()
    assert image_similarity_full(fig, "make_ax_dark.png")


# ------------------------------------------------------------------------------
#
# Testing remove ticks
#
# ------------------------------------------------------------------------------
def test_remove_ticks_example_image():
    fig, (ax0, ax1) = bpl.subplots(ncols=2, figsize=[10, 5])

    ax0.plot([0, 1, 2], [0, 1, 2])
    ax1.plot([0, 1, 2], [0, 1, 2])

    ax0.remove_ticks(["top", "right"])
    ax1.remove_ticks(["all"])

    ax0.set_title("removed top/right ticks")
    ax1.set_title("removed all ticks")

    assert image_similarity_full(fig, "remove_ticks_example.png")


# def test_remove_ticks_wrong_values():
#     fig, ax = bpl.subplots()
#     with pytest.raises(ValueError):
#         ax.remove_ticks("sdfs")
#     with pytest.raises(ValueError):
#         ax.remove_ticks(["sdfs", "top", "bottom"])
#     with pytest.raises(ValueError):
#         ax.remove_ticks("left", "sdfs", "top", "bottom")
#
#
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
#     assert image_similarity_full(fig, "remove_ticks_multiple_no_list.png")


# ------------------------------------------------------------------------------
#
# Testing remove spines
#
# ------------------------------------------------------------------------------
def test_remove_spines_example_image():
    fig, (ax0, ax1) = bpl.subplots(ncols=2, figsize=[10, 5])

    ax0.plot([0, 1, 2], [0, 1, 2])
    ax1.plot([0, 1, 2], [0, 1, 2])

    ax0.remove_spines(["top", "right"])
    ax1.remove_spines(["all"])

    ax0.set_title("removed top/right spines")
    ax1.set_title("removed all spines")

    assert image_similarity_full(fig, "remove_spines_example.png")


# ------------------------------------------------------------------------------
#
# Testing scatter
#
# ------------------------------------------------------------------------------
def test_scatter_simple_example_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10)
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "scatter_simple_example.png")


def test_scatter_multiple_datasets_example_image():
    fig, ax = bpl.subplots()

    ax.scatter(xs_normal_500,     ys_normal_500)
    ax.scatter(xs_normal_500 + 1, ys_normal_500 + 0.5)
    ax.scatter(xs_normal_500 + 1, ys_normal_500 + 1)
    ax.equal_scale()

    assert image_similarity_full(fig, "scatter_multiple_datasets_example.png")


# ------------------------------------------------------------------------------
#
# Testing hist
#
# ------------------------------------------------------------------------------
def test_hist_basic_first_example_image():
    fig, ax = bpl.subplots()

    ax.hist(xs_normal_10000)
    assert image_similarity_full(fig, "hist_simple.png")


def test_hist_few_options_example_image():
    fig, ax = bpl.subplots()
    data1 = xs_normal_10000 - 6
    data2 = xs_normal_10000 - 2
    data3 = xs_normal_10000 + 2
    data4 = xs_normal_10000 + 6
    bin_size = 0.5
    ax.hist(data1, rel_freq=True, bin_size=bin_size)
    ax.hist(data2, rel_freq=True, bin_size=bin_size, histtype="step",
             linewidth=5)
    ax.hist(data3, rel_freq=True, bin_size=bin_size,
             histtype="stepfilled", hatch="o", alpha=0.8)
    ax.hist(data4, rel_freq=True, bin_size=bin_size, histtype="step",
             hatch="x", linewidth=4)

    ax.add_labels(y_label="Relative Frequency")

    assert image_similarity_full(fig, "hist_few_options.png")

# ------------------------------------------------------------------------------
#
# Testing add labels
#
# ------------------------------------------------------------------------------
def test_add_labels_example_image():
    xs = np.arange(0, 10, 0.1)
    ys = xs ** 2

    fig, ax = bpl.subplots()
    ax.plot(xs, ys)
    ax.add_labels("X value", "Y value", "Title")

    assert image_similarity_full(fig, "add_labels_example.png")


# ------------------------------------------------------------------------------
#
# Testing set limits
#
# ------------------------------------------------------------------------------
def test_set_limits_example_image():
    xs = np.arange(0, 10, 0.01)
    ys = np.cos(xs)

    fig, [ax1, ax2] = bpl.subplots(ncols=2)

    ax1.plot(xs, ys)

    ax2.plot(xs, ys)
    ax2.set_limits(0, 2 * np.pi, -1.01, 1.01)

    assert image_similarity_full(fig, "set_limits_example.png")


# ------------------------------------------------------------------------------
#
# Testing add_text
#
# ------------------------------------------------------------------------------
def test_add_text_example_image():
    xs = np.arange(0, 7, 0.1)
    ys = xs ** 2

    fig, ax = bpl.subplots()

    ax.plot(xs, ys)
    ax.add_text(2, 30, "(2, 30) data", ha="center", va="center")
    ax.add_text(0.6, 0.2, "60% across, 20% up", "axes")

    assert image_similarity_full(fig, "add_text_example.png")


# ------------------------------------------------------------------------------
#
# Testing remove labels
#
# ------------------------------------------------------------------------------
def test_remove_labels_example_image():
    xs = np.arange(0, 5, 0.1)
    ys = xs ** 2

    fig, ax = bpl.subplots()

    ax.plot(xs, ys)

    ax.remove_labels("y")
    ax.remove_ticks(["top"])
    ax.add_labels("Conceptual plot", "Axes labels still work")

    assert image_similarity_full(fig, "remove_labels_example.png")


# ------------------------------------------------------------------------------
#
# Testing legend
#
# ------------------------------------------------------------------------------
def test_legend_example_image():
    x = np.arange(0, 5, 0.1)

    fig, ax = bpl.subplots()

    ax.plot(x, x, label="x")
    ax.plot(x, 2 * x, label="2x")
    ax.plot(x, 3 * x, label="3x")
    ax.legend(loc=2)

    assert image_similarity_full(fig, "legend_example_image.png")


def test_legend_example_with_kwargs_image():
    x = np.arange(0, 5, 0.1)

    fig, ax = bpl.subplots()

    ax.plot(x, x, label="x")
    ax.plot(x, 2 * x, label="2x")
    ax.plot(x, 3 * x, label="3x")
    ax.legend(fontsize=20, loc=6, title="Title")

    assert image_similarity_full(fig, "legend_example_with_kwargs.png")


# ------------------------------------------------------------------------------
#
# Testing equal scale
#
# ------------------------------------------------------------------------------
def test_equal_scale_example_one_image():
    xs = xs_normal_500
    ys = ys_normal_500 * 2

    fig, [ax1, ax2] = bpl.subplots(figsize=[12, 5], ncols=2)

    ax1.scatter(xs, ys)
    ax2.scatter(xs, ys)

    ax2.equal_scale()

    ax1.add_labels(title="Looks symmetric")
    ax2.add_labels(title="Shows true shape")

    assert image_similarity_full(fig, "equal_scale_example_one.png")


def test_equal_scale_shape_example_image():
    xs = xs_normal_500
    ys = ys_normal_500 * 2

    fig, [ax1, ax2] = bpl.subplots(figsize=[12, 5], ncols=2)

    ax1.scatter(xs, ys)
    ax2.scatter(xs, ys)

    ax1.equal_scale()
    ax2.equal_scale()

    ax1.set_limits(-10, 10, -4, 4)
    ax2.set_limits(-5, 5, -10, 10)

    assert image_similarity_full(fig, "equal_scale_shape_example.png")


# ------------------------------------------------------------------------------
#
# Testing easy add text
#
# ------------------------------------------------------------------------------
def test_easy_add_text_example_numbers_image():
    fig, ax = bpl.subplots()

    ax.easy_add_text("1", 1)
    ax.easy_add_text("2", 2)
    ax.easy_add_text("3", 3)
    ax.easy_add_text("4", 4)
    ax.easy_add_text("5", 5)
    ax.easy_add_text("6", 6)
    ax.easy_add_text("7", 7)
    ax.easy_add_text("8", 8)
    ax.easy_add_text("9", 9)

    assert image_similarity_full(fig, "easy_add_text_example_numbers.png")


def test_easy_add_text_example_words_image():
    fig, ax = bpl.subplots()

    ax.easy_add_text("upper left", "upper left")
    ax.easy_add_text("upper center", "upper center")
    ax.easy_add_text("upper right", "upper right")
    ax.easy_add_text("center left", "center left")
    ax.easy_add_text("center", "center")
    ax.easy_add_text("center right", "center right")
    ax.easy_add_text("lower left", "lower left")
    ax.easy_add_text("lower center", "lower center")
    ax.easy_add_text("lower right", "lower right")

    assert image_similarity_full(fig, "easy_add_text_example_words.png")


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

def test_density_contour_error_checking_data_not_all_same_smoothing_works():
    xs = [1, 1, 1, 1]
    ys = [4, 4, 4, 4]
    fig, ax = bpl.subplots()
    ax.density_contour(xs, ys, bin_size=0.1, percent_levels=0.5,
                           smoothing=1.0)
    # no error

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


def test_density_contour_percent_level_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=5, c="orange")
    ax.density_contour(xs_uniform_10, ys_uniform_10,
                       bin_size=0.01, percent_levels=[0.4, 0.9], smoothing=0.1)
    ax.equal_scale()
    ax.set_limits(-0.25, 1.25, -0.25, 1.25)
    assert image_similarity_full(fig, "density_contour_percent_level.png")


def test_density_contour_diff_smoothing_bins_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=5, c="orange")
    ax.density_contour(xs_uniform_10, ys_uniform_10,
                       bin_size=0.01,
                       percent_levels=[0.4, 0.95],
                       smoothing=[0.05, 0.2],
                       labels=False)
    ax.equal_scale()
    ax.set_limits(-0.25, 1.25, -0.25, 1.25)
    assert image_similarity_full(fig, "density_contour_diff_smoothing_bins.png")


def test_density_contour_weights_image():
    fig, ax = bpl.subplots()
    xs = [1, 2, 3, 4]
    ys = xs
    weights = xs
    ax.density_contour(xs, ys, weights=weights,
                       bin_size=0.01,
                       percent_levels=[0.4, 0.95],
                       smoothing=0.3,
                       labels=True,
                       cmap="ocean")
    ax.equal_scale()
    assert image_similarity_full(fig, "density_contour_weights.png")


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


def test_density_contourf_percent_level_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=5, c="white")
    ax.density_contourf(xs_uniform_10, ys_uniform_10,
                        bin_size=0.01, percent_levels=[0.4, 0.9], smoothing=0.1,
                        zorder=0)
    ax.equal_scale()
    ax.set_limits(-0.25, 1.25, -0.25, 1.25)
    assert image_similarity_full(fig, "density_contourf_percent_level.png")


def test_density_contourf_diff_smooth_bins_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=5, c="white")
    ax.density_contourf(xs_uniform_10, ys_uniform_10,
                        bin_size=0.01,
                        percent_levels=[0.4, 0.95],
                        smoothing=[0.05, 0.2],
                        zorder=0)
    ax.equal_scale()
    ax.set_limits(-0.25, 1.25, -0.25, 1.25)
    assert image_similarity_full(fig, "density_contourf_diff_smooth_bins.png")


def test_density_contourf_weights_image():
    fig, ax = bpl.subplots()
    xs = [1, 2, 3, 4]
    ys = xs
    weights = xs
    ax.density_contourf(xs, ys, weights=weights,
                        bin_size=0.01,
                        percent_levels=[0.4, 0.95],
                        smoothing=0.3,
                        cmap="ocean")
    ax.equal_scale()
    assert image_similarity_full(fig, "density_contourf_weights.png")


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


def test_contour_scatter_scatter_outside_contours_image():
    xs = np.concatenate([xs_normal_10000, xs_normal_10000 + 5])
    ys = np.concatenate([ys_normal_10000, ys_normal_10000 + 5])

    fig, ax = bpl.subplots()
    ax.scatter(xs, ys, c=bpl.color_cycle[1], s=2, alpha=1, zorder=4)
    ax.contour_scatter(xs, ys, bin_size=0.01, smoothing=0.2,
                       scatter_kwargs={"s":20, "zorder":3})
    ax.equal_scale()
    assert image_similarity_full(fig, "contour_scatter_outside_contours.png")


def test_contour_scatter_mult_holes_example_image():
    # set the seed specifically for this test, so that I can keep this data
    # created in this function.
    np.random.seed(10)
    rad1 = np.random.normal(10, 0.75, 10000)
    theta1 = np.random.uniform(0, 2 * np.pi, 10000)
    x1 = [r * np.cos(t) for r, t in zip(rad1, theta1)]
    y1 = [r * np.sin(t) for r, t in zip(rad1, theta1)]

    rad2 = np.random.normal(20, 0.75, 20000)
    theta2 = np.random.uniform(0, 2 * np.pi, 20000)
    x2 = [r * np.cos(t) for r, t in zip(rad2, theta2)]
    y2 = [r * np.sin(t) for r, t in zip(rad2, theta2)]

    rad3 = np.random.normal(12, 0.75, 12000)
    theta3 = np.random.uniform(0, 2 * np.pi, 12000)
    x3 = [r * np.cos(t) + 10 for r, t in zip(rad3, theta3)]
    y3 = [r * np.sin(t) + 10 for r, t in zip(rad3, theta3)]

    x4 = np.random.uniform(-20, 20, 3500)
    y4 = x4 + np.random.normal(0, 0.5, 3500)

    y5 = y4 * (-1)

    xs = np.concatenate([x1, x2, x3, x4, x4])
    ys = np.concatenate([y1, y2, y3, y4, y5])

    fig, ax = bpl.subplots()

    ax.contour_scatter(xs, ys, smoothing=0.5, bin_size=0.5)
    ax.equal_scale()

    assert image_similarity_full(fig, "contour_scatter_mult_holes_example.png")


def test_contour_scatter_mult_kwargs_example_image():
    xs = np.concatenate([xs_normal_10000,
                         xs_normal_10000 + 3,
                         xs_normal_10000])
    ys = np.concatenate([ys_normal_10000,
                         ys_normal_10000 + 3,
                         ys_normal_10000 + 3])

    fig, axs = bpl.subplots(nrows=2, ncols=2)
    [ax1, ax2], [ax3, ax4] = axs

    percent_levels = [0.99, 0.7, 0.3]
    smoothing = 0.2
    bin_size = 0.1

    ax1.contour_scatter(xs, ys,
                        bin_size=bin_size,
                        percent_levels=percent_levels,
                        smoothing=smoothing,
                        fill_cmap="background_grey",
                        contour_kwargs={"cmap": "magma"},
                        scatter_kwargs={"s": 10,
                                        "c": bpl.almost_black})
    ax1.make_ax_dark()

    # or we can choose our own `fill_cmap`
    ax2.contour_scatter(xs, ys,
                        bin_size=bin_size,
                        smoothing=smoothing,
                        fill_cmap="viridis",
                        percent_levels=percent_levels,
                        contour_kwargs={"linewidths": 1,
                                        "colors":     "white"},
                        scatter_kwargs={"s":     50,
                                        "c":     bpl.color_cycle[3],
                                        "alpha": 0.3})

    # There are also my colormaps that work with the dark axes
    ax3.contour_scatter(xs, ys,
                        bin_size=bin_size,
                        smoothing=smoothing,
                        fill_cmap="modified_greys",
                        percent_levels=percent_levels,
                        scatter_kwargs={"c": bpl.color_cycle[0]},
                        contour_kwargs={"linewidths": [2, 0, 0, 0, 0, 0, 0],
                                        "colors":     bpl.almost_black})
    ax3.make_ax_dark()

    # the default `fill_cmap` is white.
    new_linestyles = ["solid", "dashed", "dashed", "dashed"]
    ax4.contour_scatter(xs, ys,
                        bin_size=bin_size,
                        smoothing=smoothing,
                        percent_levels=percent_levels,
                        scatter_kwargs={"marker":    "^",
                                        "linewidth": 0.2,
                                        "c":         bpl.color_cycle[1],
                                        "s":         20},
                        contour_kwargs={"linestyles": new_linestyles,
                                        "colors":     bpl.almost_black})

    assert image_similarity_full(fig, "contour_scatter_mult_kwargs_example.png")


def test_contour_scatter_lab_smooth_example_image():
    xs = [1, 2, 3, 4]
    ys = [1, 2, 3, 4]
    weights = [1, 2, 3, 4]
    fig, ax = bpl.subplots()
    ax.contour_scatter(xs, ys,
                       weights=weights,
                       bin_size=0.01,
                       smoothing=[0.8, 0.3],
                       fill_cmap="Blues",
                       labels=True,
                       contour_kwargs={"colors": "k"})
    ax.equal_scale()

    assert image_similarity_full(fig, "contour_scatter_lab_smooth_example.png")


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


def test_shaded_density_basic_image():
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
    assert image_similarity_full(fig, "shaded_density_points_are_inside.png")


def test_shaded_density_with_smoothing_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
    ax.shaded_density(xs_uniform_10, ys_uniform_10, bin_size=0.01,
                      smoothing=0.1, cmap="viridis")
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_with_smoothing.png")


def test_shaded_density_bin_size_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
    ax.shaded_density(xs_uniform_10, ys_uniform_10, bin_size=[0.2, 0.25])
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_bin_size.png")


def test_shaded_density_smoothing_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
    ax.shaded_density(xs_uniform_10, ys_uniform_10, bin_size=0.01,
                      smoothing=[0.5, 0.05])
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_smoothing.png")


def test_shaded_density_weights_image():
    xs = [0.2, 0.4, 0.6, 0.8]
    ys = [0.2, 0.4, 0.6, 0.8]
    weights = [1, 2, 3, 4]

    fig, ax = bpl.subplots()
    ax.shaded_density(xs, ys, weights=weights, bin_size=0.01,
                      smoothing=[0.05, 0.2], cmap="ocean")
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_weights.png")
