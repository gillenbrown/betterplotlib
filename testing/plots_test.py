import imageio.v2 as imageio
import numpy as np
import matplotlib.pyplot as plt  # for some tests
from pathlib import Path
import pytest
from tools_test import clear_all_open_figures

import betterplotlib as bpl

bpl.set_style()
np.random.seed(314159)

this_dir = Path(__file__).parent
baseline_im_dir = this_dir / "baseline_images"
new_im_dir = this_dir / "temporary_images"


# ------------------------------------------------------------------------------
#
# iamge comparison tests
#
# ------------------------------------------------------------------------------
# I do some image comparison tests. However, these are very difficult to do well. There
# are slight differences in font rendering or general plot rendering on different
# machines. Therefore, an exact compariosn does not work. Also, I don't like doing
# similarity within a given threshold, since often we're interested in checking some
# small differences (i.e. ticks). The threshold needed to cover system differences is
# often enough to allow substantive differences to still pass. I tried matplotlib's
# testing framework, where you can remove text, but still found differences. In short,
# I could not find a way to make the tests fail for only substantive differences with
# no false negatives or false positives. So what I do is make the tests pass on my
# local machine, but not on GitHub actions where the tests run on multiple python
# versions. I use decorators to enforce that the tests pass locally, but mark that
# they're expected to fail on the remote
if str(Path.home()) == "/Users/gillenbrown":  # pragma: no cover
    pass_local_fail_remote = lambda x: x
else:  # pragma: no cover
    pass_local_fail_remote = pytest.mark.xfail


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
    new_img = new_im_dir / image_name
    baseline_img = baseline_im_dir / image_name

    fig.savefig(new_img)

    # clear open figures to prepare for next text
    clear_all_open_figures()

    try:
        matched = image_similarity(new_img, baseline_img)
    except OSError:  # pragma: no cover
        raise IOError(f"Baseline image {image_name} does not exist.")
    if matched:  # pragma: no cover
        new_img.unlink()
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
no_iqr_msg = (
    "The Freeman-Diaconis default binning relies on "
    "inter-quartile range, and your data has zero.\n"
    "Try passing your own bin size."
)

empty_data_msg = "Empty list is not valid for data."
xy_length_msg = "x and y data must be the same length."

bin_size_positive_msg = "Bin size must be positive."
bin_size_typing_msg = "Bin_size must be either a scalar or two element numeric list."

smoothing_nonnegative_msg = "Smoothing must be nonnegative."
smoothing_typing_msg = "Smoothing must be either a scalar or two element numeric list."

weights_nonnegative_msg = "Weights must be non-negative."
weights_wrong_length = "Weights and data need to have the same length."
weights_typing_msg = "Weights must be a numerical array."

percent_levels_typing_msg = "Percent_levels needs to be a numeric list."
percent_levels_duplicates_msg = (
    "The percent levels chosen lead to duplicate levels.\n"
    "Contour levels must be increasing."
)
percent_levels_range_msg = "Percentages must be between 0 and 1."

data_not_all_same_msg = (
    "All points are identical. This breaks matplotlib "
    "contours for some reason. Try other data, or smooth."
)

levels_contour_err_msg = (
    "The levels parameter is set by this function. Do not pass it in. "
)

# ------------------------------------------------------------------------------
#
# test the examples used in the documentation
#
# ------------------------------------------------------------------------------
# Here I parse the axes_bpl.docstrings to get all the code examples, then make the plots
# contained there to test against.


def check_examples(file_name, func_name, idx):
    """
    Test the examples for a given function

    :param file_name: The name of the file where the function is defined. Do not include
                      the ".py" suffix
    :type file_name: str
    :param func_name: the function to get the examples from
    :type func_name: str
    :param idx: index into the list of examples to check
    :type idx: int
    :return: result of the comparison
    :rtype: bool
    """
    code = get_examples(file_name, func_name)[idx]

    # then run the figures and check the image similarity
    # I need to make some changes behind the scenes, to make random numbers work
    # correctly. I'll create a random rng object, then use that instead of the
    # common np.random.whatever
    code = code.replace("np.random", "rng")
    code = "rng = np.random.default_rng(314159)\n" + code
    exec(code)
    # the `fig` variable will be defined in this code. For some reason I can't
    # figure out how to just call `fig` to get that, so instead I have to get it
    # from the locals dictionary. If it's not there, get it
    try:
        fig = locals()["fig"]
    except KeyError:
        fig = plt.gcf()
    return image_similarity_full(locals()["fig"], f"{func_name}_example_{idx}.png")


def get_examples(file_name, func_name):
    """
    Get all the code used to make the example plots, which can then be directly tested

    :param file_name: The name of the file where the function is defined. Do not include
                      the ".py" suffix
    :type file_name: str
    :param func_name: The function name that we want to grab plotting code from
    :type func_name: str
    :return: tuple of strings with the code to execute to create a given plot
    :rtype: tuple(str)
    """
    bpl_file = Path(__file__).parent.parent / "betterplotlib" / f"{file_name}.py"
    docstring = ""
    in_func = False
    in_docstring = False
    with open(bpl_file, "r") as in_file:
        for line in in_file:
            if line.strip().startswith(f"def {func_name}("):
                in_func = True
                continue
            if in_func and not in_docstring and line.strip() == '"""':
                in_docstring = True
                continue
            if in_docstring:
                if line.strip() == '"""':
                    break
                docstring += line

    # then parse the docstring to get the plot information. Detecting this depends on
    # the amount of whitespace in front. I use spaces, not tabs.
    # first detect the indented spacing
    for line in docstring.split("\n"):
        if line.strip().startswith(":include-source"):
            indent_spaces = len(line) - len(line.lstrip())

    # then go through and find all the code blocks
    code_blocks = []
    this_code_block = ""
    in_code_block = False
    for line in docstring.split("\n"):
        if line.strip().startswith(":include-source"):
            in_code_block = True
            continue
        if in_code_block:
            # see if we're not in a code block anymore
            if len(line.strip()) != 0 and not line.startswith(" " * indent_spaces):
                in_code_block = False
                code_blocks.append(this_code_block)
                this_code_block = ""
                continue
            # this is a normal line. Ignore comments, imports, blank lines
            # don't ignore setting style, since that I use that in some tests
            line_deindent = line.replace(" " * indent_spaces, "", 1)
            if (
                line_deindent.strip() == ""
                or line_deindent.startswith("#")
                or line_deindent.startswith("import")
            ):
                continue
            # this is something to add
            this_code_block += line_deindent + "\n"
    # if we got to the end of the docstring, add what's left
    if this_code_block != "":
        code_blocks.append(this_code_block)

    return code_blocks


# and test these functions
def test_get_examples_single():
    code = get_examples("axes_bpl", "make_ax_dark")
    assert len(code) == 1
    assert code[0] == (
        "bpl.set_style()\n"
        "fig, (ax0, ax1) = bpl.subplots(figsize=[12, 5], ncols=2)\n"
        "ax1.make_ax_dark()\n"
        'ax0.set_title("Regular")\n'
        'ax1.set_title("Dark")\n'
    )


def test_get_examples_multiple():
    code = get_examples("axes_bpl", "equal_scale")
    assert len(code) == 3
    assert code[0] == (
        "bpl.set_style()\n"
        "xs = np.random.normal(0, 1, 1000)\n"
        "ys = np.random.normal(0, 2, 1000)\n"
        "fig, [ax1, ax2] = bpl.subplots(figsize=[12, 5], ncols=2)\n"
        "ax1.scatter(xs, ys)\n"
        "ax2.scatter(xs, ys)\n"
        "ax2.equal_scale()\n"
        'ax1.add_labels(title="Looks symmetric")\n'
        'ax2.add_labels(title="Shows true shape")\n'
    )
    assert code[1] == (
        "bpl.set_style()\n"
        "xs = np.random.normal(0, 1, 1000)\n"
        "ys = np.random.normal(0, 2, 1000)\n"
        "fig, [ax1, ax2] = bpl.subplots(figsize=[12, 5], ncols=2)\n"
        "ax1.scatter(xs, ys)\n"
        "ax2.scatter(xs, ys)\n"
        "ax1.equal_scale()\n"
        "ax2.equal_scale()\n"
        "ax1.set_limits(-10, 10, -4, 4)\n"
        "ax2.set_limits(-5, 5, -10, 10)\n"
    )
    assert code[2] == (
        "bpl.set_style()\n"
        "xs = np.random.normal(0, 1, 1000)\n"
        "ys = 10 ** np.random.normal(0, 0.5, 1000)\n"
        "fig, ax = bpl.subplots()\n"
        "ax.scatter(xs, ys)\n"
        'ax.log("y")\n'
        "ax.set_limits(-3, 3, 10**-3, 10**3)\n"
        "ax.equal_scale()\n"
    )


def test_get_example_loop():
    code = get_examples("axes_bpl", "scatter")
    assert len(code) == 1
    assert code[0] == (
        "bpl.set_style()\n"
        "x = np.random.normal(0, scale=0.5, size=500)\n"
        "y = np.random.normal(0, scale=0.5, size=500)\n"
        "for dx in [0, 0.5, 1]:\n"
        "    bpl.scatter(x + dx, y + dx)\n"
        "bpl.equal_scale()\n"
    )


def test_get_example_different_file():
    code = get_examples("colors", "fade_color")
    assert len(code) == 1
    assert code[0] == (
        "bpl.set_style()\n"
        'c = "#ac4649"\n'
        "fig, ax = bpl.subplots()\n"
        "ax.axhline(2, lw=20, c=c)\n"
        "ax.axhline(1, lw=20, c=bpl.fade_color(c))\n"
        "ax.axhline(0, lw=20, c=bpl.unfade_color(bpl.fade_color(c)))\n"
        'ax.add_text(0.5, 2.1, "Original", va="bottom", ha="center")\n'
        'ax.add_text(0.5, 1.1, "Faded", va="bottom", ha="center")\n'
        'ax.add_text(0.5, 0.1, "Faded then Unfaded", va="bottom", ha="center")\n'
        "ax.set_limits(0, 1, -1, 3)\n"
        'ax.remove_labels("both")\n'
    )


# ------------------------------------------------------------------------------
#
# Actually make the tests for example images
#
# ------------------------------------------------------------------------------
functions = [
    ("styles", "set_style"),
    ("colors", "fade_color"),
    ("colors", "unfade_color"),
    ("axes_bpl", "make_ax_dark"),
    ("axes_bpl", "remove_ticks"),
    ("axes_bpl", "remove_spines"),
    ("axes_bpl", "scatter"),
    ("axes_bpl", "hist"),
    ("axes_bpl", "add_labels"),
    ("axes_bpl", "set_limits"),
    ("axes_bpl", "add_text"),
    ("axes_bpl", "remove_labels"),
    ("axes_bpl", "legend"),
    ("axes_bpl", "equal_scale"),
    ("axes_bpl", "easy_add_text"),
    ("axes_bpl", "density_contour"),
    ("axes_bpl", "density_contourf"),
    ("axes_bpl", "contour_scatter"),
    ("axes_bpl", "data_ticks"),
    ("axes_bpl", "plot"),
    ("axes_bpl", "axvline"),
    ("axes_bpl", "axhline"),
    ("axes_bpl", "errorbar"),
    ("axes_bpl", "twin_axis_simple"),
    ("axes_bpl", "twin_axis"),
    ("axes_bpl", "shaded_density"),
    ("axes_bpl", "log"),
    ("axes_bpl", "set_ticks"),
]

# then create the list of tests to run
params = []
for f_file, f_name in functions:
    for i in range(len(get_examples(f_file, f_name))):
        params.append((f_file, f_name, i))


@pass_local_fail_remote
@pytest.mark.parametrize(
    "file,name,number",
    params,
)
def test_all_examples(file, name, number):
    assert check_examples(file, name, number)


# ------------------------------------------------------------------------------
#
# Testing styles
#
# ------------------------------------------------------------------------------
def test_invalid_style():
    with pytest.raises(ValueError):
        bpl.set_style("bad_style_name")


# ------------------------------------------------------------------------------
#
# Testing make ax dark
#
# ------------------------------------------------------------------------------
@pass_local_fail_remote
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
@pass_local_fail_remote
def test_remove_ticks_all_sides():
    fig, axs = bpl.subplots(ncols=5, figsize=[20, 5])
    # set ticks on all axes before we remove them
    for ax in axs:
        ax.xaxis.set_ticks_position("both")
        ax.yaxis.set_ticks_position("both")

    # then remove the ticks we want to check
    for ax, to_remove in zip(axs, ["top", "bottom", "left", "right", "all"]):
        ax.remove_ticks(to_remove)
        ax.add_labels("x_label", "y_label", to_remove)

    assert image_similarity_full(fig, "remove_ticks_all_sides.png")


@pass_local_fail_remote
def test_remove_ticks_imperative():
    bpl.scatter(xs_uniform_10, ys_uniform_10)
    bpl.remove_ticks("left", "right")
    assert image_similarity_full(plt.gcf(), "remove_ticks_imperative.png")


# ------------------------------------------------------------------------------
#
# Testing remove spines
#
# ------------------------------------------------------------------------------
@pass_local_fail_remote
def test_remove_spines_imperative():
    bpl.scatter(xs_uniform_10, ys_uniform_10)
    bpl.remove_spines("left", "right")
    assert image_similarity_full(plt.gcf(), "remove_spines_imperative.png")


# ------------------------------------------------------------------------------
#
# Testing scatter
#
# ------------------------------------------------------------------------------
@pass_local_fail_remote
def test_scatter_use_kwargs():
    fig, ax = bpl.subplots()
    ax.scatter(x=xs_uniform_10, y=ys_uniform_10)
    assert image_similarity_full(fig, "scatter_kwargs.png")


@pass_local_fail_remote
def test_scatter_legend_alpha():
    fig, ax = bpl.subplots()
    ax.scatter(x=xs_normal_10000, y=ys_normal_10000, alpha=0.1, label="Test")
    ax.legend()
    assert image_similarity_full(fig, "scatter_legend_alpha.png")


# ------------------------------------------------------------------------------
#
# Testing hist
#
# ------------------------------------------------------------------------------
def test_hist_not_relfreq_and_weights():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError):
        ax.hist(xs_normal_500, rel_freq=True, weights=xs_normal_500)


def test_hist_not_relfreq_and_density():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError):
        ax.hist(xs_normal_500, rel_freq=True, density=False)


def test_hist_not_binsize_and_bins():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError):
        ax.hist(xs_normal_500, bin_size=1, bins=np.arange(-10, 10, 0.5))


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
def test_add_text_cant_use_transform():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError):
        ax.add_text(0, 0, "text", transform=None)


def test_add_text_bad_coords():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError):
        ax.add_text(0, 0, "text", coords="lklkj")


# ------------------------------------------------------------------------------
#
# Testing remove labels
#
# ------------------------------------------------------------------------------
def test_remove_labels_validate_labels_passed_in():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError):
        ax.remove_labels("lkjlk")


@pass_local_fail_remote
def test_remove_labels_imperative():
    bpl.scatter(xs_uniform_10, ys_uniform_10)
    bpl.remove_labels("both")
    assert image_similarity_full(plt.gcf(), "remove_labels_imperative.png")


# ------------------------------------------------------------------------------
#
# Testing legend
#
# ------------------------------------------------------------------------------
@pass_local_fail_remote
def test_legend_title_fontsize():
    fig, ax = bpl.subplots()
    ax.scatter([], [], label="test")
    ax.legend(title="Test Title", fontsize=25)
    assert image_similarity_full(fig, "legend_fontsize.png")


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
def test_easy_add_text_cant_control_alignment():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError):
        ax.easy_add_text("text", "upper left", ha="left")
    with pytest.raises(ValueError):
        ax.easy_add_text("text", "upper left", va="bottom")
    with pytest.raises(ValueError):
        ax.easy_add_text("text", "upper left", horizontalalignment="left")
    with pytest.raises(ValueError):
        ax.easy_add_text("text", "upper left", verticalalignment="bottom")


def test_easy_add_text_validate_location():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError):
        ax.easy_add_text("text", "upper left wrong")
    with pytest.raises(ValueError):
        ax.easy_add_text("text", 10)


# ------------------------------------------------------------------------------
#
# Testing underlying density contour
#
# ------------------------------------------------------------------------------
def test_density_contour_error_checking_data_length_nonzero():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax._density_contour_core([], [], bin_size=0.1, percent_levels=0.5)
    assert str(err_msg.value) == empty_data_msg


def test_density_contour_error_checking_data_not_all_same():
    xs = [1, 1, 1, 1]
    ys = [4, 4, 4, 4]
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax._density_contour_core(xs, ys, bin_size=0.1, percent_levels=0.5)
    assert str(err_msg.value) == data_not_all_same_msg


def test_density_contour_error_checking_data_not_all_same_smoothing_works():
    xs = [1, 1, 1, 1]
    ys = [4, 4, 4, 4]
    fig, ax = bpl.subplots()
    ax._density_contour_core(xs, ys, bin_size=0.1, percent_levels=0.5, smoothing=1.0)
    # no error


def test_density_contour_error_checking_data_no_variation_needs_bin_size():
    xs = [1, 2, 2, 2, 2, 2, 2, 3]
    ys = [1, 2, 2, 2, 2, 2, 2, 3]
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax._density_contour_core(xs, ys, percent_levels=0.5)
    assert str(err_msg.value) == no_iqr_msg
    ax._density_contour_core(xs, ys, bin_size=0.1, percent_levels=0.5)


def test_density_contour_error_checking_data_length_needs_same():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax._density_contour_core([1, 2, 3], [1, 2])
    assert str(err_msg.value) == xy_length_msg


@pytest.mark.parametrize(
    "bin_size,err,msg",
    [
        (-1, ValueError, bin_size_positive_msg),
        ([-1, 5], ValueError, bin_size_positive_msg),
        ([1, -5], ValueError, bin_size_positive_msg),
        ([0, 5], ValueError, bin_size_positive_msg),
        ([1, 5, 3], ValueError, bin_size_typing_msg),
        ([], ValueError, bin_size_typing_msg),
        (["a", "b"], TypeError, bin_size_typing_msg),
    ],
)
def test_density_contour_error_checking_bin_size(bin_size, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax._density_contour_core(xs_uniform_10, ys_uniform_10, bin_size)
    assert str(err_msg.value) == msg


@pytest.mark.parametrize(
    "smoothing,err,msg",
    [
        (-1, ValueError, smoothing_nonnegative_msg),
        ([-1, 5], ValueError, smoothing_nonnegative_msg),
        ([1, -5], ValueError, smoothing_nonnegative_msg),
        ([1, 5, 3], ValueError, smoothing_typing_msg),
        ([], ValueError, smoothing_typing_msg),
        (["a", "b"], TypeError, smoothing_typing_msg),
    ],
)
def test_density_contour_error_checking_smoothing(smoothing, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax._density_contour_core(xs_uniform_10, ys_uniform_10, smoothing=smoothing)
    assert str(err_msg.value) == msg


@pytest.mark.parametrize(
    "weights,err,msg",
    [
        (-1 * xs_uniform_10, ValueError, weights_nonnegative_msg),
        ([1, 5, 3], ValueError, weights_wrong_length),
        (["a", "b"], TypeError, weights_typing_msg),
    ],
)
def test_density_contour_error_checking_weights(weights, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax._density_contour_core(xs_uniform_10, ys_uniform_10, weights=weights)
    assert str(err_msg.value) == msg


@pytest.mark.parametrize(
    "percents,err,msg",
    [
        (["a"], TypeError, percent_levels_typing_msg),
        ([0.45, 0.451], ValueError, percent_levels_duplicates_msg),
        ([-0.4, 0.5], ValueError, percent_levels_range_msg),
        ([0.4, 1.01], ValueError, percent_levels_range_msg),
    ],
)
def test_density_contour_error_checking_percent_levels(percents, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax._density_contour_core(xs_uniform_10, ys_uniform_10, percent_levels=percents)
    assert str(err_msg.value) == msg


def test_density_contour_levels_not_in_kwargs():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax._density_contour_core(xs_uniform_10, ys_uniform_10, levels=[1])
    assert str(err_msg.value) == levels_contour_err_msg


def test_density_log_is_right_length():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError):
        ax._density_contour_core(xs_uniform_10, ys_uniform_10, log=[True, True, False])


def test_density_log_is_right_type():
    fig, ax = bpl.subplots()
    with pytest.raises(TypeError):
        ax._density_contour_core(xs_uniform_10, ys_uniform_10, log=["yes", "no"])


def test_density_contour_can_specify_smoothing_but_not_bin_size():
    # just test that this avoids an error
    fig, ax = bpl.subplots()
    ax._density_contour_core(xs_uniform_10, ys_uniform_10, smoothing=0.1)


# ------------------------------------------------------------------------------
#
# Testing density contour
#
# ------------------------------------------------------------------------------
@pass_local_fail_remote
def test_density_contour_percent_level_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=5, c="orange")
    ax.density_contour(
        xs_uniform_10,
        ys_uniform_10,
        bin_size=0.01,
        percent_levels=[0.4, 0.9],
        smoothing=0.1,
    )
    ax.equal_scale()
    ax.set_limits(-0.25, 1.25, -0.25, 1.25)
    assert image_similarity_full(fig, "density_contour_percent_level.png")


@pass_local_fail_remote
def test_density_contour_diff_smoothing_bins_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=5, c="orange")
    ax.density_contour(
        xs_uniform_10,
        ys_uniform_10,
        bin_size=0.01,
        percent_levels=[0.4, 0.95],
        smoothing=[0.05, 0.2],
        labels=False,
    )
    ax.equal_scale()
    ax.set_limits(-0.25, 1.25, -0.25, 1.25)
    assert image_similarity_full(fig, "density_contour_diff_smoothing_bins.png")


@pass_local_fail_remote
def test_density_contour_weights_image():
    fig, ax = bpl.subplots()
    xs = [1, 2, 3, 4]
    ys = xs
    weights = xs
    ax.density_contour(
        xs,
        ys,
        weights=weights,
        bin_size=0.01,
        percent_levels=[0.4, 0.95],
        smoothing=0.3,
        labels=True,
        cmap="ocean",
    )
    ax.equal_scale()
    assert image_similarity_full(fig, "density_contour_weights.png")


# ------------------------------------------------------------------------------
#
# Testing density filled contour
#
# ------------------------------------------------------------------------------
def test_density_contourf_no_labels():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contourf(xs_uniform_10, ys_uniform_10, labels=True)
    assert str(err_msg.value) == "Filled contours cannot have labels."


@pass_local_fail_remote
def test_density_contourf_percent_level_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=5, c="white")
    ax.density_contourf(
        xs_uniform_10,
        ys_uniform_10,
        bin_size=0.01,
        percent_levels=[0.4, 0.9],
        smoothing=0.1,
        zorder=0,
    )
    ax.equal_scale()
    ax.set_limits(-0.25, 1.25, -0.25, 1.25)
    assert image_similarity_full(fig, "density_contourf_percent_level.png")


@pass_local_fail_remote
def test_density_contourf_diff_smooth_bins_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=5, c="white")
    ax.density_contourf(
        xs_uniform_10,
        ys_uniform_10,
        bin_size=0.01,
        percent_levels=[0.4, 0.95],
        smoothing=[0.05, 0.2],
        zorder=0,
    )
    ax.equal_scale()
    ax.set_limits(-0.25, 1.25, -0.25, 1.25)
    assert image_similarity_full(fig, "density_contourf_diff_smooth_bins.png")


@pass_local_fail_remote
def test_density_contourf_weights_image():
    fig, ax = bpl.subplots()
    xs = [1, 2, 3, 4]
    ys = xs
    weights = xs
    ax.density_contourf(
        xs,
        ys,
        weights=weights,
        bin_size=0.01,
        percent_levels=[0.4, 0.95],
        smoothing=0.3,
        cmap="cividis",
    )
    ax.equal_scale()
    assert image_similarity_full(fig, "density_contourf_weights.png")


# ------------------------------------------------------------------------------
#
# Testing contour_scatter
#
# ------------------------------------------------------------------------------
@pass_local_fail_remote
def test_contour_scatter_scatter_outside_contours_image():
    xs = np.concatenate([xs_normal_10000, xs_normal_10000 + 5])
    ys = np.concatenate([ys_normal_10000, ys_normal_10000 + 5])

    fig, ax = bpl.subplots()
    ax.scatter(xs, ys, c=bpl.color_cycle[1], s=2, alpha=1, zorder=4)
    ax.contour_scatter(
        xs, ys, bin_size=0.01, smoothing=0.2, scatter_kwargs={"s": 20, "zorder": 3}
    )
    ax.equal_scale()
    assert image_similarity_full(fig, "contour_scatter_outside_contours.png")


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
@pass_local_fail_remote
def test_errorbar_imperative():
    bpl.errorbar(
        x=xs_uniform_10, y=ys_uniform_10, xerr=xs_uniform_10, yerr=ys_uniform_10
    )
    assert image_similarity_full(plt.gcf(), "errorbar_imperative.png")


# ------------------------------------------------------------------------------
#
# Testing twin axis simple
#
# ------------------------------------------------------------------------------
@pass_local_fail_remote
def test_twin_axis_simple_opposite_of_example():
    # have the log on different axis to get full coverage
    fig, ax = bpl.subplots(tight_layout=True)
    ax.set_limits(0, 5, 0, 10)
    ax.add_labels("x", "y")
    ax.twin_axis_simple("x", 1, 10**5, "$10^x$", log=True)
    ax.twin_axis_simple("y", 0, 100, "$10 y$")
    assert image_similarity_full(fig, "twin_axis_simple_example_0_opp.png")


def test_twin_axis_simple_axis_error_checking():
    # have the log on different axis to get full coverage
    fig, ax = bpl.subplots(tight_layout=True)
    with pytest.raises(ValueError):
        ax.twin_axis_simple("z", 1, 10**5, "$10^x$", log=True)


# ------------------------------------------------------------------------------
#
# Testing twin axis
#
# ------------------------------------------------------------------------------
def test_twin_axis_no_func_error_checking():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError):
        ax.twin_axis("x", [-1, 0, 1, 2, 3, 4, 5], "log(x)")


def test_twin_axis_double_func_error_checking():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError):
        ax.twin_axis("x", [-1, 0, 1, 2, 3, 4, 5], "log(x)", np.log10, np.log10)


def test_twin_axis_axis_error_checking():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError):
        ax.twin_axis("z", [-1, 0, 1, 2, 3, 4, 5], "log(x)", np.log10)


@pass_local_fail_remote
def test_twin_axis_imperative():
    bpl.set_limits(0, 3, 0, 3)
    bpl.twin_axis("x", [1, 10, 100, 1000], "label", lambda x: 10**x)
    assert image_similarity_full(plt.gcf(), "twin_axis_imperative.png")


# ------------------------------------------------------------------------------
#
# Testing shaded density
#
# ------------------------------------------------------------------------------
@pass_local_fail_remote
def test_shaded_density_basic_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
    ax.shaded_density(xs_uniform_10, ys_uniform_10)
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_basic.png")


@pass_local_fail_remote
def test_shaded_density_points_are_inside_image():
    """Test that the scatter points to indeed lie in the regions they should."""
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
    ax.shaded_density(
        xs_uniform_10, ys_uniform_10, bin_size=0.01, smoothing=0, cmap="Greens"
    )
    for x in xs_uniform_10:
        ax.axvline(x, lw=0.01)
    for y in ys_uniform_10:
        ax.axhline(y, lw=0.01)
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_points_are_inside.png")


@pass_local_fail_remote
def test_shaded_density_with_smoothing_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
    ax.shaded_density(
        xs_uniform_10, ys_uniform_10, bin_size=0.01, smoothing=0.1, cmap="viridis"
    )
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_with_smoothing.png")


@pass_local_fail_remote
def test_shaded_density_bin_size_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
    ax.shaded_density(xs_uniform_10, ys_uniform_10, bin_size=[0.2, 0.25])
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_bin_size.png")


@pass_local_fail_remote
def test_shaded_density_smoothing_image():
    fig, ax = bpl.subplots()
    ax.scatter(xs_uniform_10, ys_uniform_10, s=1, c="yellow", zorder=10)
    ax.shaded_density(
        xs_uniform_10, ys_uniform_10, bin_size=0.01, smoothing=[0.5, 0.05]
    )
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_smoothing.png")


@pass_local_fail_remote
def test_shaded_density_weights_image():
    xs = [0.2, 0.4, 0.6, 0.8]
    ys = [0.2, 0.4, 0.6, 0.8]
    weights = [1, 2, 3, 4]

    fig, ax = bpl.subplots()
    ax.shaded_density(
        xs, ys, weights=weights, bin_size=0.01, smoothing=[0.05, 0.2], cmap="ocean"
    )
    ax.equal_scale()
    ax.set_limits(0, 1, 0, 1)
    assert image_similarity_full(fig, "shaded_density_weights.png")


@pass_local_fail_remote
def test_shaded_density_log_hist():
    fig, axs = bpl.subplots(ncols=2)
    axs[0].shaded_density(
        xs_normal_10000, ys_normal_10000, bin_size=0.1, smoothing=0.5, log_hist=True
    )
    axs[1].shaded_density(
        xs_normal_10000, ys_normal_10000, bin_size=0.1, smoothing=0.5, log_hist=False
    )
    for ax in axs:
        ax.equal_scale()
        ax.set_limits(-2, 2, -2, 2)
    assert image_similarity_full(fig, "shaded_density_log.png")


@pass_local_fail_remote
def test_shaded_density_different_xy():
    # just test that this avoids an error
    fig, ax = bpl.subplots()
    ax.shaded_density(xs_normal_500, xs_normal_500, bin_size=[0.5, 1], smoothing=[5, 1])
    ax.set_limits(-6, 6, -6, 6)
    ax.equal_scale()
    assert image_similarity_full(fig, "shaded_density_different_xy.png")


# ------------------------------------------------------------------------------
#
# Testing log axis
#
# ------------------------------------------------------------------------------
def test_log_axis_error_checking():
    with pytest.raises(ValueError):
        bpl.log("lkjlkj")


def test_log_axis_minor_ticks():
    bpl.log("both")
    bpl.set_limits(0.1, 1, 0.1, 1)
    bpl.equal_scale()
    assert image_similarity_full(plt.gcf(), "log_axis_minor_ticks.png")


# ------------------------------------------------------------------------------
#
# Testing set_ticks
#
# ------------------------------------------------------------------------------
def test_set_ticks_axis_name_check():
    with pytest.raises(ValueError):
        bpl.set_ticks("z", [1, 2])


# ------------------------------------------------------------------------------
#
# Testing color
#
# ------------------------------------------------------------------------------
def test_cant_unfade_something_too_saturated():
    bpl.unfade_color("#FFF1AB")  # works fine
    with pytest.raises(ValueError):
        bpl.unfade_color("#FFF1A8")  # slightly more saturated
