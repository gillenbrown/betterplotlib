import imageio.v2 as imageio
import numpy as np
import matplotlib.pyplot as plt  # for some tests
from pathlib import Path
import pytest

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

    try:
        matched = image_similarity(new_img, baseline_img)
    except OSError:  # pragma: no cover
        raise IOError(f"Baseline image {image_name} does not exist.")
    if matched:
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


def check_examples(func_name, idx):
    """
    Test the examples for a given function

    :param func_name: the function to get the examples from
    :type func_name: str
    :param idx: index into the list of examples to check
    :type idx: int
    :return: result of the comparison
    :rtype: bool
    """
    code = get_examples(func_name)[idx]

    # then run the figures and check the image similarity
    # I need to make some changes behind the scenes, to make random numbers work
    # correctly. I'll create a random rng object, then use that instead of the
    # common np.random.whatever
    code = code.replace("np.random", "rng")
    code = "rng = np.random.default_rng(314159)\n" + code
    exec(code)
    # the `fig` variable will be defined in this code. For some reason I can't
    # figure out how to just call `fig` to get that, so instead I have to get it
    # from the locals dictionary
    return image_similarity_full(locals()["fig"], f"{func_name}_example_{idx + 1}.png")


def get_examples(func_name):
    """
    Get all the code used to make the example plots, which can then be directly tested

    :param func_name: The function name that we want to grab plotting code from
    :type func_name: str
    :return: tuple of strings with the code to execute to create a given plot
    :rtype: tuple(str)
    """
    bpl_file = Path(__file__).parent.parent / "betterplotlib" / "axes_bpl.py"
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
            # this is a normal line. Ignore comments, imports, style set, blank lines
            line_deindent = line.replace(" " * indent_spaces, "", 1)
            if (
                line_deindent.strip() == ""
                or line_deindent.startswith("#")
                or line_deindent.startswith("import")
                or line_deindent == "bpl.set_style()"
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
    code = get_examples("make_ax_dark")
    assert len(code) == 1
    assert code[0] == (
        "fig, (ax0, ax1) = bpl.subplots(figsize=[12, 5], ncols=2)\n"
        "ax1.make_ax_dark()\n"
        'ax0.set_title("Regular")\n'
        'ax1.set_title("Dark")\n'
    )


def test_get_examples_multiple():
    code = get_examples("equal_scale")
    assert len(code) == 2
    assert code[0] == (
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


def test_get_example_loop():
    code = get_examples("scatter")
    assert len(code) == 1
    assert code[0] == (
        "x = np.random.normal(0, scale=0.5, size=500)\n"
        "y = np.random.normal(0, scale=0.5, size=500)\n"
        "fig = plt.figure(figsize=[15, 7])\n"
        "ax1 = fig.add_subplot(121)\n"
        'ax2 = fig.add_subplot(122, projection="bpl")\n'
        "for ax in [ax1, ax2]:\n"
        "    ax.scatter(x,       y)\n"
        "    ax.scatter(x + 0.5, y + 0.5)\n"
        "    ax.scatter(x + 1,   y + 1)\n"
        'ax1.set_title("matplotlib")\n'
        'ax2.add_labels(title="betterplotlib")\n'
    )


# ------------------------------------------------------------------------------
#
# Actually make the tests for example images
#
# ------------------------------------------------------------------------------
functions = [
    "make_ax_dark",
    "remove_ticks",
    "remove_spines",
    "scatter",
    "hist",
    "add_labels",
    "set_limits",
    "add_text",
    "remove_labels",
    "legend",
    "equal_scale",
    "easy_add_text",
    "density_contour",
    "density_contourf",
    "contour_scatter",
    "contour_all",
    "data_ticks",
    "plot",
    "axvline",
    "axhline",
    "errorbar",
    "twin_axis_simple",
    "twin_axis",
    "shaded_density",
    "format_labels",
]

# then create the list of tests to run
params = []
for f in functions:
    for i in range(len(get_examples(f))):
        params.append((f, i))


@pass_local_fail_remote
@pytest.mark.parametrize(
    "name,number",
    params,
)
def test_all_examples(name, number):
    assert check_examples(name, number)


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


def test_density_contour_error_checking_data_not_all_same_smoothing_works():
    xs = [1, 1, 1, 1]
    ys = [4, 4, 4, 4]
    fig, ax = bpl.subplots()
    ax.density_contour(xs, ys, bin_size=0.1, percent_levels=0.5, smoothing=1.0)
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
        ax.density_contour(xs_uniform_10, ys_uniform_10, bin_size)
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
        ax.density_contour(xs_uniform_10, ys_uniform_10, smoothing=smoothing)
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
        ax.density_contour(xs_uniform_10, ys_uniform_10, weights=weights)
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
        ax.density_contour(xs_uniform_10, ys_uniform_10, percent_levels=percents)
    assert str(err_msg.value) == msg


def test_density_contour_levels_not_in_kwargs():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.density_contour(xs_uniform_10, ys_uniform_10, levels=[1])
    assert str(err_msg.value) == levels_contour_err_msg


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
def test_density_contourf_error_checking_bin_size(bin_size, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.density_contourf(xs_uniform_10, ys_uniform_10, bin_size)
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
def test_density_contourf_error_checking_smoothing(smoothing, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.density_contourf(xs_uniform_10, ys_uniform_10, smoothing=smoothing)
    assert str(err_msg.value) == msg


@pytest.mark.parametrize(
    "weights,err,msg",
    [
        (-1 * xs_uniform_10, ValueError, weights_nonnegative_msg),
        ([1, 5, 3], ValueError, weights_wrong_length),
        (["a", "b"], TypeError, weights_typing_msg),
    ],
)
def test_density_contourf_error_checking_weights(weights, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.density_contourf(xs_uniform_10, ys_uniform_10, weights=weights)
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
def test_density_contourf_error_checking_percent_levels(percents, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.density_contourf(xs_uniform_10, ys_uniform_10, percent_levels=percents)
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
def test_contour_scatter_error_checking_bin_size(bin_size, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.contour_scatter(xs_normal_10000, ys_normal_10000, bin_size)
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
def test_contour_scatter_error_checking_smoothing(smoothing, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.contour_scatter(xs_normal_10000, ys_normal_10000, smoothing=smoothing)
    assert str(err_msg.value) == msg


@pytest.mark.parametrize(
    "weights,err,msg",
    [
        (xs_normal_10000, ValueError, weights_nonnegative_msg),
        ([1, 5, 3], ValueError, weights_wrong_length),
        (["a", "b"], TypeError, weights_typing_msg),
    ],
)
def test_contour_scatter_error_checking_weights(weights, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.contour_scatter(xs_normal_10000, ys_normal_10000, weights=weights)
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
def test_contour_scatter_error_checking_percent_levels(percents, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.contour_scatter(xs_normal_10000, ys_normal_10000, percent_levels=percents)
    assert str(err_msg.value) == msg


def test_contour_scatter_error_checking_no_labels_contourf():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.contour_scatter(
            xs_normal_10000, ys_normal_10000, contourf_kwargs={"labels": True}
        )
    assert str(err_msg.value) == "Filled contours cannot have labels."


def test_contour_scatter_error_checking_no_levels_contour():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.contour_scatter(
            xs_normal_10000, ys_normal_10000, contour_kwargs={"levels": [1]}
        )
    assert str(err_msg.value) == levels_contour_err_msg


def test_contour_scatter_error_checking_no_levels_contourf():
    fig, ax = bpl.subplots()
    with pytest.raises(ValueError) as err_msg:
        ax.contour_scatter(
            xs_normal_10000, ys_normal_10000, contourf_kwargs={"levels": [1]}
        )
    assert str(err_msg.value) == levels_contour_err_msg


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
def test_shaded_density_error_checking_bin_size(bin_size, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.shaded_density(xs_uniform_10, ys_uniform_10, bin_size)
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
def test_shaded_density_error_checking_smoothing(smoothing, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.shaded_density(xs_uniform_10, ys_uniform_10, smoothing=smoothing)
    assert str(err_msg.value) == msg


@pytest.mark.parametrize(
    "weights,err,msg",
    [
        (-1 * xs_uniform_10, ValueError, weights_nonnegative_msg),
        ([1, 5, 3], ValueError, weights_wrong_length),
        (["a", "b"], TypeError, weights_typing_msg),
    ],
)
def test_shaded_density_error_checking_weights(weights, err, msg):
    fig, ax = bpl.subplots()
    with pytest.raises(err) as err_msg:
        ax.shaded_density(xs_uniform_10, ys_uniform_10, weights=weights)
    assert str(err_msg.value) == msg


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
