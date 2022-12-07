import matplotlib.pyplot as plt
import pytest
from pytest import approx
import numpy as np
from scipy import integrate
from matplotlib import path
from betterplotlib import tools, get_axis, subplots

np.random.seed(19680801)
random_x = np.random.normal(0, 1, 1000)

# ------------------------------------------------------------------------------
#
# test get axis
#
# ------------------------------------------------------------------------------
def clear_all_open_figures():
    # needed to make sure things are fresh before starting
    for i in plt.get_fignums():
        plt.close(i)


def test_get_axis_nothing_previously_set():
    clear_all_open_figures()
    ax = get_axis()
    assert ax is not None


def test_get_axis_figure_only_set():
    clear_all_open_figures()
    fig = plt.figure()
    ax = get_axis()
    assert fig == ax.figure


def test_get_axis_fig_and_ax_already_set():
    clear_all_open_figures()
    fig, ax = subplots()
    ax2 = get_axis()
    assert ax2 == ax
    assert ax2.figure == fig


def test_get_axis_non_bpl_axis_only():
    clear_all_open_figures()
    fig = plt.figure()
    fig.add_subplot(projection="polar")
    with pytest.raises(ValueError):
        get_axis()


# ------------------------------------------------------------------------------
#
# testing alpha. I don't test a lot here, since the actual values are just
# aesthetics
#
# ------------------------------------------------------------------------------
def test_alpha_small_values():
    """Test that small values are given totally opaque."""
    assert tools._alpha(10, threshold=30) == approx(1.0)
    assert tools._alpha(29, threshold=30) == approx(1.0)
    assert tools._alpha(30, threshold=30) != approx(1.0)


def test_alpha_large_values():
    """Test that alpha values never go to zero."""
    assert 0 < tools._alpha(10**2) <= 1.0
    assert 0 < tools._alpha(10**4) <= 1.0
    assert 0 < tools._alpha(10**10) <= 1.0


# ------------------------------------------------------------------------------
#
# Freedman Diaconis core bin size testing
#
# ------------------------------------------------------------------------------
def test_freedman_diaconis_core_zero_data():
    """Length of zero or negative doesn't work in FD."""
    with pytest.raises(ValueError) as err_msg:
        tools._freedman_diaconis_core(10, 0)
    desired_msg = (
        "The number of data points must be positive in " "Freedman Diaconis binning."
    )
    assert str(err_msg.value) == desired_msg

    with pytest.raises(ValueError) as err_msg:
        tools._freedman_diaconis_core(10, -5)
    assert str(err_msg.value) == desired_msg


def test_freedman_diaconis_core_zero_iqr():
    """zero iqr gives zero bin size, which is meaningless"""
    with pytest.raises(ValueError) as err_msg:
        tools._freedman_diaconis_core(0, 10)
    desired_msg = (
        "The Freeman-Diaconis default binning relies on "
        "inter-quartile range, and your data has zero.\n"
        "Try passing your own bin size."
    )
    assert str(err_msg.value) == desired_msg

    with pytest.raises(ValueError) as err_msg:
        tools._freedman_diaconis_core(-5, 10)
    assert str(err_msg.value) == desired_msg


def test_freedman_diaconis_core_data_types_string():
    with pytest.raises(TypeError) as err_msg:
        tools._freedman_diaconis_core("t", 5)
    assert str(err_msg.value) == "iqr must be a numeric scalar."

    with pytest.raises(TypeError) as err_msg:
        tools._freedman_diaconis_core(5, "s")
    assert str(err_msg.value) == "n must be a numeric scalar."


def test_freedman_diaconis_core_data_types_list():
    with pytest.raises(TypeError) as err_msg:
        tools._freedman_diaconis_core([1, 2], 5)
    assert str(err_msg.value) == "iqr must be a numeric scalar."

    with pytest.raises(TypeError) as err_msg:
        tools._freedman_diaconis_core(5, [4, 5])
    assert str(err_msg.value) == "n must be a numeric scalar."


def test_freedman_diaconis_core_simple():
    """Some easy test cases for FD"""
    assert tools._freedman_diaconis_core(1.0, 1.0) == 2.0
    assert tools._freedman_diaconis_core(10.0, 1.0) == 20.0
    assert tools._freedman_diaconis_core(1.0, 8.0) == 1.0
    assert tools._freedman_diaconis_core(5.0, 8.0) == 5.0
    assert tools._freedman_diaconis_core(6.0, 27.0) == 4.0


# ------------------------------------------------------------------------------
#
# Actual testing of FD binning. There will only be a few examples here, since
# it's tedious to calculate this a lot.
#
# ------------------------------------------------------------------------------
def test_freedman_diaconis_zero_data():
    """Zero data doesn't produce any bins."""
    with pytest.raises(ValueError) as err_msg:
        tools._freedman_diaconis([])
    desired_msg = (
        "The number of data points must be positive in " "Freedman Diaconis binning."
    )
    assert str(err_msg.value) == desired_msg


def test_freedman_diaconis_zero_range_a():
    """No range produces bad bins."""
    with pytest.raises(ValueError) as err_msg:
        tools._freedman_diaconis([1])
    desired_msg = (
        "The Freeman-Diaconis default binning relies on "
        "inter-quartile range, and your data has zero.\n"
        "Try passing your own bin size."
    )
    assert str(err_msg.value) == desired_msg


def test_freedman_diaconis_zero_range_b():
    """zero interquartile range doesn't work."""
    with pytest.raises(ValueError) as err_msg:
        tools._freedman_diaconis([1, 2, 2, 2, 2, 2, 3])
    desired_msg = (
        "The Freeman-Diaconis default binning relies on "
        "inter-quartile range, and your data has zero.\n"
        "Try passing your own bin size."
    )
    assert str(err_msg.value) == desired_msg


def test_freedman_diaconis_example_a():
    """Have an example here that will result in easy to calculate values"""
    data = np.linspace(0, 100, num=1000)
    # here iqr = 50, n^{1/3} = 10, so 2 * iqr / n^{1/3} = 10
    real_bin_size = 10.0
    test_bin_size = tools._freedman_diaconis(data)
    assert real_bin_size == approx(test_bin_size)


def test_freedman_diaconis_example_b():
    """Another example I can calculate easily."""
    data = [
        1,
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        4,
    ]
    # here iqr = 1, n=27
    real_bin_size = 2.0 / 3.0
    test_bin_size = tools._freedman_diaconis(data)
    assert real_bin_size == approx(test_bin_size)


# ------------------------------------------------------------------------------
#
# testing for the rounding of the bin sizes.
#
# ------------------------------------------------------------------------------
def test_round_to_nice_width_simple():
    assert tools._round_to_nice_width(0.5) == approx(0.5)
    assert tools._round_to_nice_width(4) == approx(5)
    assert tools._round_to_nice_width(78) == approx(100)


def test_round_to_nice_width_with_exp_small():
    assert tools._round_to_nice_width(1.2e-7) == approx(1e-7)


def test_round_to_nice_width_with_exp_large():
    assert tools._round_to_nice_width(8.6e7) == approx(1e8)


def test_round_to_nice_width_with_exp_general():
    """Want either 1, 2, 5, or 10 bins per 10 units. So we either round the
    bin to 10, 5, 2, or 1, respectively."""
    for exp in np.arange(-10.0, 10.0):
        factor = 10**exp
        assert np.isclose(tools._round_to_nice_width(1.0 * factor), 1.0 * factor)
        assert np.isclose(tools._round_to_nice_width(1.49999 * factor), 1.0 * factor)
        assert np.isclose(tools._round_to_nice_width(1.50001 * factor), 2.0 * factor)
        assert np.isclose(tools._round_to_nice_width(2.0 * factor), 2.0 * factor)
        assert np.isclose(tools._round_to_nice_width(3.49999 * factor), 2.0 * factor)
        assert np.isclose(tools._round_to_nice_width(3.50001 * factor), 5.0 * factor)
        assert np.isclose(tools._round_to_nice_width(5.0 * factor), 5.0 * factor)
        assert np.isclose(tools._round_to_nice_width(7.49999 * factor), 5.0 * factor)
        assert np.isclose(tools._round_to_nice_width(7.50001 * factor), 10.0 * factor)
        assert np.isclose(tools._round_to_nice_width(10.0 * factor), 10.0 * factor)
        assert np.isclose(tools._round_to_nice_width(14.9999 * factor), 10.0 * factor)
        assert np.isclose(tools._round_to_nice_width(15.0001 * factor), 20.0 * factor)


def test_round_to_nice_width_error_checking_positive():
    """can't have a bin size that is negative or zero"""
    with pytest.raises(ValueError) as err_msg:
        tools._round_to_nice_width(0)
    assert str(err_msg.value) == "Bin width must be positive."

    with pytest.raises(ValueError) as err_msg:
        tools._round_to_nice_width(-1)
    assert str(err_msg.value) == "Bin width must be positive."


def test_round_to_nice_width_error_checking_types_list():
    """can't pass in a list"""
    with pytest.raises(TypeError) as err_msg:
        tools._round_to_nice_width([1, 3])
    assert str(err_msg.value) == "Bin width must be a numeric scalar."
    # or an array
    with pytest.raises(TypeError) as err_msg:
        tools._round_to_nice_width(np.array([5, 3]))
    assert str(err_msg.value) == "Bin width must be a numeric scalar."


# ------------------------------------------------------------------------------
#
# binning
#
# ------------------------------------------------------------------------------
def test_binning_bin_size_error_checking_zero():
    with pytest.raises(ValueError) as err_msg:
        tools._binning(min_=1, max_=2, bin_size=0)
    assert str(err_msg.value) == "Bin size must be positive."


def test_binning_bin_size_error_checking_negative():
    with pytest.raises(ValueError) as err_msg:
        tools._binning(min_=1, max_=2, bin_size=-1)
    assert str(err_msg.value) == "Bin size must be positive."


def test_binning_padding_error_checking():
    with pytest.raises(ValueError) as err_msg:
        tools._binning(min_=1, max_=2, bin_size=1, padding=-1)
    assert str(err_msg.value) == "Padding must be non-negative."


def test_binning_min_max_checking_not_ordered():
    with pytest.raises(ValueError) as err_msg:
        tools._binning(min_=1, max_=0, bin_size=1)
    assert str(err_msg.value) == "Min must be smaller than max."


def test_binning_wrong_type_min():
    with pytest.raises(TypeError) as err_msg:
        tools._binning(min_="a", max_=0, bin_size=1)
    assert str(err_msg.value) == "min must be a numerical value in `_binning`."


def test_binning_wrong_type_max():
    with pytest.raises(TypeError) as err_msg:
        tools._binning(min_=1, max_="a", bin_size=1)
    assert str(err_msg.value) == "max must be a numerical value in `_binning`."


def test_binning_wrong_type_min_max():
    with pytest.raises(TypeError) as err_msg:
        tools._binning(min_="a", max_="b", bin_size=1)
    assert str(err_msg.value) == "min must be a numerical value in `_binning`."


def test_binning_wrong_type_bin_size():
    with pytest.raises(TypeError) as err_msg:
        tools._binning(min_=0, max_=1, bin_size="a")
    desired_msg = "bin_size must be a numerical value in `_binning`."
    assert str(err_msg.value) == desired_msg


def test_binning_wrong_type_padding():
    with pytest.raises(TypeError) as err_msg:
        tools._binning(min_=-1, max_=0, bin_size=1, padding="a")
    desired_msg = "padding must be a numerical value in `_binning`."
    assert str(err_msg.value) == desired_msg


def test_binning_wrong_type_min_list():
    with pytest.raises(TypeError) as err_msg:
        tools._binning(min_=[-1, -2], max_=2, bin_size=1, padding=0)
    assert str(err_msg.value) == "min must be a numerical value in `_binning`."


def test_binning_wrong_type_max_list():
    with pytest.raises(TypeError) as err_msg:
        tools._binning(min_=-1, max_=[0, 1], bin_size=1, padding=0)
    assert str(err_msg.value) == "max must be a numerical value in `_binning`."


def test_binning_wrong_type_bin_size_list():
    with pytest.raises(TypeError) as err_msg:
        tools._binning(min_=-1, max_=0, bin_size=[1, 2], padding=0)
    desired_msg = "bin_size must be a numerical value in `_binning`."
    assert str(err_msg.value) == desired_msg


def test_binning_wrong_type_padding_list():
    with pytest.raises(TypeError) as err_msg:
        tools._binning(min_=-1, max_=0, bin_size=1, padding=[0, 1])
    desired_msg = "padding must be a numerical value in `_binning`."
    assert str(err_msg.value) == desired_msg


def test_binning_positive_bin_aligned():
    test_bins = tools._binning(min_=1.0, max_=2.0, bin_size=0.5)
    real_bins = [0.5, 1.0, 1.5, 2.0, 2.5]
    assert real_bins == approx(test_bins)


def test_binning_negative_bin_aligned():
    test_bins = tools._binning(min_=-2.0, max_=-1.0, bin_size=0.5)
    real_bins = [-2.5, -2, -1.5, -1, -0.5]
    assert real_bins == approx(test_bins)


def test_binning_zero_to_pos_bin_aligned():
    test_bins = tools._binning(min_=0, max_=1, bin_size=0.5)
    real_bins = [-0.5, 0, 0.5, 1.0, 1.5]
    assert real_bins == approx(test_bins)


def test_binning_neg_to_zero_bin_aligned():
    test_bins = tools._binning(min_=-1, max_=0, bin_size=0.5)
    real_bins = [-1.5, -1, -0.5, 0, 0.5]
    assert real_bins == approx(test_bins)


def test_binning_zero_to_pos_bin_aligned_b():
    test_bins = tools._binning(min_=0.5, max_=1, bin_size=0.5)
    real_bins = [0, 0.5, 1.0, 1.5]
    assert real_bins == approx(test_bins)


def test_binning_neg_to_zero_bin_aligned_b():
    test_bins = tools._binning(min_=-1, max_=-0.5, bin_size=0.5)
    real_bins = [-1.5, -1, -0.5, 0]
    assert real_bins == approx(test_bins)


def test_binning_across_zero_bin_aligned():
    test_bins = tools._binning(min_=-0.5, max_=1, bin_size=0.5)
    real_bins = [-1, -0.5, 0, 0.5, 1.0, 1.5]
    assert real_bins == approx(test_bins)


def test_binning_across_zero_not_aligned():
    test_bins = tools._binning(min_=-0.25, max_=0.25, bin_size=0.5)
    real_bins = [-0.5, 0, 0.5]
    assert real_bins == approx(test_bins)


def test_binning_neg_to_zero_not_aligned():
    test_bins = tools._binning(min_=-0.75, max_=-0.25, bin_size=0.5)
    real_bins = [-1, -0.5, 0]
    assert real_bins == approx(test_bins)


def test_binning_zero_to_pos_not_aligned():
    test_bins = tools._binning(min_=0.25, max_=0.75, bin_size=0.5)
    real_bins = [0, 0.5, 1]
    assert real_bins == approx(test_bins)


def test_binning_positive_not_aligned():
    test_bins = tools._binning(min_=0.75, max_=1.25, bin_size=0.5)
    real_bins = [0.5, 1, 1.5]
    assert real_bins == approx(test_bins)


def test_binning_negative_not_aligned():
    test_bins = tools._binning(min_=-1.25, max_=-0.75, bin_size=0.5)
    real_bins = [-1.5, -1, -0.5]
    assert real_bins == approx(test_bins)


def test_binning_across_zero_many_bins_not_aligned():
    test_bins = tools._binning(min_=-0.51, max_=0.61, bin_size=0.1)
    real_bins = [
        -0.6,
        -0.5,
        -0.4,
        -0.3,
        -0.2,
        -0.1,
        0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
    ]
    assert real_bins == approx(test_bins)


def test_binning_positive_many_bins_not_aligned():
    test_bins = tools._binning(min_=0.51, max_=1.11, bin_size=0.1)
    real_bins = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    assert real_bins == approx(test_bins)


def test_binning_negative_many_bins_not_aligned():
    test_bins = tools._binning(min_=-1.31, max_=-0.49, bin_size=0.1)
    real_bins = [-1.4, -1.3, -1.2, -1.1, -1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4]
    assert real_bins == approx(test_bins)


def test_binning_zero_to_pos_many_bins_not_aligned():
    test_bins = tools._binning(min_=0.01, max_=0.51, bin_size=0.1)
    real_bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    assert real_bins == approx(test_bins)


def test_binning_neg_to_zero_many_bins_not_aligned():
    test_bins = tools._binning(min_=-0.51, max_=-0.01, bin_size=0.1)
    real_bins = [-0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0]
    assert real_bins == approx(test_bins)


def test_binning_padding_positive_aligned():
    test_bins = tools._binning(min_=5, max_=10, bin_size=1, padding=2)
    real_bins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    assert real_bins == approx(test_bins)


def test_binning_padding_negative_aligned():
    test_bins = tools._binning(min_=-1.0, max_=-0.5, bin_size=0.1, padding=0.2)
    real_bins = [-1.3, -1.2, -1.1, -1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2]
    assert real_bins == approx(test_bins)


def test_binning_padding_positive_not_aligned():
    test_bins = tools._binning(min_=0.5, max_=1.1, bin_size=0.2, padding=0.2)
    real_bins = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4]
    assert real_bins == approx(test_bins)


def test_binning_padding_negative_not_aligned():
    test_bins = tools._binning(min_=-11, max_=-5, bin_size=2, padding=2)
    real_bins = [-14, -12, -10, -8, -6, -4, -2]
    assert real_bins == approx(test_bins)


def test_binning_range_smaller_than_bin_aligned():
    test_bins = tools._binning(min_=0.0, max_=2.0, bin_size=10.0)
    real_bins = [-10, 0, 10]
    assert real_bins == approx(test_bins)


def test_binning_range_smaller_than_bin_not_aligned():
    test_bins = tools._binning(min_=-5.0, max_=-3.0, bin_size=10.0)
    real_bins = [-10, 0]
    assert real_bins == approx(test_bins)


def test_binning_min_equal_max():
    test_bins = tools._binning(min_=1, max_=1, bin_size=0.5)
    real_bins = [0.5, 1, 1.5]
    assert real_bins == approx(test_bins)


def test_binning_all_bins_same_size():
    desired_bin_size = 0.25
    bins = tools._binning(0, 10, desired_bin_size, padding=2.34)
    for idx in range(len(bins) - 1):
        this_bin_size = bins[idx + 1] - bins[idx]
        assert this_bin_size == approx(desired_bin_size)


# ------------------------------------------------------------------------------
#
# bin centers
#
# ------------------------------------------------------------------------------
def test_centers_wrong_type_noniterable():
    with pytest.raises(TypeError) as err_msg:
        tools.bin_centers("hello")
    assert str(err_msg.value) == "Edges have to be numeric list-like."

    with pytest.raises(TypeError) as err_msg:
        tools.bin_centers(100)
    assert str(err_msg.value) == "Edges have to be numeric list-like."


def test_centers_wrong_type_wrong_iterable():
    test_dict = {0: 0, 1: 1}
    with pytest.raises(TypeError) as err_msg:
        tools.bin_centers(test_dict)
    assert str(err_msg.value) == "Edges have to be numeric list-like."


def test_centers_zero_length_edges():
    with pytest.raises(ValueError) as err_msg:
        tools.bin_centers([])
    assert str(err_msg.value) == "Need at least two edges to calculate centers."


def test_centers_one_length_edges():
    with pytest.raises(ValueError) as err_msg:
        tools.bin_centers([1])
    assert str(err_msg.value) == "Need at least two edges to calculate centers."


def test_centers_two_length():
    assert tools.bin_centers([1, 2]) == approx([1.5])


def test_centers_simple_equal_spacing():
    test_centers = tools.bin_centers([1, 2, 3, 4])
    real_centers = [1.5, 2.5, 3.5]
    assert test_centers == approx(real_centers)


def test_centers_not_equal_spacing():
    test_centers = tools.bin_centers([1, 2, 3, 4, 6, 8, 10])
    real_centers = [1.5, 2.5, 3.5, 5, 7, 9]
    assert test_centers == approx(real_centers)


def test_centers_length():
    xs = np.arange(np.random.randint(10, 100, 1))
    assert len(xs) == len(tools.bin_centers(xs)) + 1


# ------------------------------------------------------------------------------

# Testing the parsing of the bin size. This doesn't have a lot.

# ------------------------------------------------------------------------------
def test_two_element_list_more_elt_array():
    with pytest.raises(ValueError) as err_msg:
        tools._two_item_list([0.4, 0.3, 0.1])
    assert str(err_msg.value) == "An iterable must have length two."


def test_two_element_list_zero_elt_array():
    with pytest.raises(ValueError) as err_msg:
        tools._two_item_list([])
    assert str(err_msg.value) == "An iterable must have length two."


def test_two_element_list_scalar():
    assert tools._two_item_list(0.1) == [0.1, 0.1]


def test_two_element_list_two_elt_array():
    assert tools._two_item_list([0.1, 0.3]) == [0.1, 0.3]


def test_two_element_list_one_elt_array():
    assert tools._two_item_list([0.4]) == [0.4, 0.4]


def test_two_element_list_two_item_string():
    assert tools._two_item_list("ab") == ["a", "b"]


def test_two_element_list_one_item_string():
    assert tools._two_item_list("a") == ["a", "a"]


def test_two_element_list_strings_too_long():
    with pytest.raises(ValueError) as err_msg:
        tools._two_item_list("hello")
    assert str(err_msg.value) == "An iterable must have length two."


def test_two_element_list_strings_too_short():
    with pytest.raises(ValueError) as err_msg:
        tools._two_item_list("")
    assert str(err_msg.value) == "An iterable must have length two."


def test_two_element_list_strings_list_numeric_multiple():
    assert tools._two_item_list(["0.4", "0.5"]) == ["0.4", "0.5"]


def test_two_element_list_strings_list_numeric_single():
    assert tools._two_item_list(["0.4"]) == ["0.4", "0.4"]


# ------------------------------------------------------------------------------

# Testing the parsing of the bin options. This relies heavily on the _binning
# function, so a lot of the more detailed testing is taken care of there.

# ------------------------------------------------------------------------------
def test_make_bins_error_checking_data_type():
    with pytest.raises(TypeError) as err_msg:
        tools.make_bins("hello")
    assert str(err_msg.value) == "data must be a list in `make_bins`."


def test_make_bins_error_checking_bin_size_type():
    with pytest.raises(TypeError) as err_msg:
        tools.make_bins([1, 2, 3], "hello")
    assert str(err_msg.value) == "bin_size must be a scalar in `make_bins`."


def test_make_bins_error_checking_padding_type():
    with pytest.raises(TypeError) as err_msg:
        tools.make_bins([1, 2, 3], 1, "hello")
    assert str(err_msg.value) == "padding must be a scalar in `make_bins`."


def test_make_bins_error_checking_bin_size_type_list():
    with pytest.raises(TypeError) as err_msg:
        tools.make_bins([1, 2, 3], [1, 2])
    assert str(err_msg.value) == "bin_size must be a scalar in `make_bins`."


def test_make_bins_error_checking_padding_type_list():
    with pytest.raises(TypeError) as err_msg:
        tools.make_bins([1, 2, 3], 1, [4, 5])
    assert str(err_msg.value) == "padding must be a scalar in `make_bins`."


def test_make_bins_error_checking_need_data_no_bin_size():
    with pytest.raises(ValueError) as err_msg:
        tools.make_bins([])
    assert str(err_msg.value) == "Empty list is not valid for data."


def test_make_bins_error_checking_need_data_with_bin_size():
    with pytest.raises(ValueError) as err_msg:
        tools.make_bins([], bin_size=1.0)
    assert str(err_msg.value) == "Empty list is not valid for data."


def test_make_bins_error_checking_length_of_data_too_small_bad():
    """If we don't pass in much data, we need to specify our bin size."""
    with pytest.raises(ValueError) as err_msg:
        tools.make_bins([1])
    desired_msg = (
        "The Freeman-Diaconis default binning relies on "
        "inter-quartile range, and your data has zero.\n"
        "Try passing your own bin size."
    )
    assert str(err_msg.value) == desired_msg


def test_make_bins_error_checking_length_of_data_too_small_good():
    """If we don't pass in much data, we need to specify our bin size."""
    test_bins = tools.make_bins([1], bin_size=0.5)
    true_bins = [0.5, 1, 1.5]
    assert true_bins == approx(test_bins)


def test_make_bins_error_checking_bin_size_positive():
    with pytest.raises(ValueError) as err_msg:
        tools.make_bins([1, 2, 3], 0)
    assert str(err_msg.value) == "Bin size must be positive."

    with pytest.raises(ValueError) as err_msg:
        tools.make_bins([1, 2, 3], -1)
    assert str(err_msg.value) == "Bin size must be positive."


def test_make_bins_error_checking_padding_nonnegative():
    with pytest.raises(ValueError) as err_msg:
        tools.make_bins([1, 2, 3], 1, padding=-1)
    assert str(err_msg.value) == "Padding must be non-negative."


def test_make_bins_too_small_iqr_bad():
    """If the IQR of the data is too small, we have to pass in the bin size"""
    with pytest.raises(ValueError) as err_msg:
        tools.make_bins([1, 2, 2, 2, 2, 2, 2, 3])
    desired_msg = (
        "The Freeman-Diaconis default binning relies on "
        "inter-quartile range, and your data has zero.\n"
        "Try passing your own bin size."
    )
    assert str(err_msg.value) == desired_msg


def test_make_bins_too_small_iqr_good():
    """If the IQR of the data is too small, we have to pass in the bin size"""
    test_bins = tools.make_bins([1, 2, 2, 2, 2, 2, 2, 3], bin_size=0.5)
    true_bins = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
    assert true_bins == approx(test_bins)


def test_make_bins_sorted():
    """The bins should be sorted."""
    data = np.random.normal(0, 1, 1000)
    bins = tools.make_bins(data)
    assert np.array_equal(sorted(bins), bins)


def test_make_bins_everything_specified():
    test_bins = tools.make_bins([1, 2], 0.5, 0)
    true_bins = [0.5, 1.0, 1.5, 2.0, 2.5]
    assert true_bins == approx(test_bins)


def test_make_bins_no_padding_specified():
    test_bins = tools.make_bins([1, 2], 0.5, 0)
    true_bins = [0.5, 1.0, 1.5, 2.0, 2.5]
    assert true_bins == approx(test_bins)


def test_make_bins_with_bin_size_centering_zero_included():
    """Make sure that if we did not pass in bin size, we did center on zero."""
    bins = tools.make_bins([-2, -1, 0, 1, 2], bin_size=0.25)
    assert 0 in bins


def test_make_bins_no_bin_size_centering_zero_included():
    """Make sure that if we did not pass in bin size, we did center on zero."""
    bins = tools.make_bins([-2, -1, 0, 1, 2])
    assert 0 in bins


def test_make_bins_bin_size_correct():
    """Test that the bin size we passed in is indeed what was used."""
    bin_size = 0.32382039482
    bins = tools.make_bins([-2, -1, 0, 1, 2], bin_size=bin_size)
    assert bins[1] - bins[0] == approx(bin_size)


def test_make_bins_no_bins_rounding():
    data = [-2, -1, 0, 1, 2]
    bins = tools.make_bins(data)
    # make sure the bin size is rounded like we want.
    assert bins[1] - bins[0] in [0.1, 0.2, 0.5, 1.0, 2.0]


def test_make_bins_min_no_bins():
    bins = tools.make_bins([1, 2, 3, 4])
    assert bins[0] < 1.0


def test_make_bins_min_with_bins():
    bins = tools.make_bins([1, 2, 3, 4], bin_size=0.34)
    assert bins[0] < 1.0


def test_make_bins_max_no_bins():
    bins = tools.make_bins([1, 2, 3, 4])
    assert bins[-1] > 4.0


def test_make_bins_max_with_bins():
    bins = tools.make_bins([1, 2, 3, 4], bin_size=0.34)
    assert bins[-1] > 4.0


def test_make_bins_min_no_bins_padding():
    bins = tools.make_bins([1, 2, 3, 4], padding=2.5)
    assert bins[0] < -1.5


def test_make_bins_min_with_bins_padding():
    bins = tools.make_bins([1, 2, 3, 4], bin_size=0.34, padding=2.5)
    assert bins[0] < -1.5


def test_make_bins_max_no_bins_padding():
    bins = tools.make_bins([1, 2, 3, 4], padding=1.4)
    assert bins[-1] > 5.4


def test_make_bins_max_with_bins_padding():
    bins = tools.make_bins([1, 2, 3, 4], bin_size=0.34, padding=8.54)
    assert bins[-1] > 12.54


@pytest.mark.parametrize("bin_size", [1, None])
def test_make_bins_larger_dataset_min(bin_size):
    data = np.random.normal(0, 1, 1000)
    bins = tools.make_bins(data, bin_size=bin_size)
    assert bins[0] < min(data)


@pytest.mark.parametrize("bin_size", [1, None])
def test_make_bins_larger_dataset_max(bin_size):
    data = np.random.normal(0, 1, 1000)
    bins = tools.make_bins(data, bin_size=bin_size)
    assert bins[-1] > max(data)


@pytest.mark.parametrize("bin_size", [1, None])
def test_make_bins_larger_dataset_zero_in_bins(bin_size):
    data = np.random.normal(0, 1, 1000)
    bins = tools.make_bins(data, bin_size=bin_size)
    # want to check that zero is in the list, but we can't do that with the
    # approx syntax nicely. We instead check if any item is close.
    in_bins = False
    for item in bins:
        if approx(0.0) == item:
            in_bins = True
    assert in_bins  # true if zero is in, false otherwise


@pytest.mark.parametrize("padding", [0, 23.4])
def test_make_bins_larger_dataset_min_padding(padding):
    data = np.random.normal(0, 1, 1000)
    bins = tools.make_bins(data, padding=padding)
    assert bins[0] < min(data) - padding


@pytest.mark.parametrize("padding", [0, 2.9])
def test_make_bins_larger_dataset_max_padding(padding):
    data = np.random.normal(0, 1, 1000)
    bins = tools.make_bins(data, padding=padding)
    assert bins[-1] > max(data) + padding


def test_make_bins_order_of_magnitude_of_chosen_bins_small():
    data = np.random.uniform(1e-4, 5e-4, 1000)
    bins = tools.make_bins(data)
    bin_size = bins[1] - bins[0]
    assert 1e-6 < bin_size < 5e-4


def test_make_bins_order_of_magnitude_of_chosen_bins_large():
    data = np.random.uniform(1e4, 5e4, 1000)
    bins = tools.make_bins(data)
    bin_size = bins[1] - bins[0]
    assert 1e3 < bin_size < 5e4


@pytest.mark.parametrize("bin_size", [1, None])
def test_make_bins_all_same_size(bin_size):
    data = np.random.uniform(0, 1, 1000)
    bins = tools.make_bins(data, bin_size=bin_size)
    real_bin_size = bins[1] - bins[0]
    for idx in range(len(bins) - 1):
        assert bins[idx + 1] - bins[idx] == approx(real_bin_size)


# ------------------------------------------------------------------------------

# Testing the unique_total

# ------------------------------------------------------------------------------
def test_unique_total_error_checking_types_string():
    with pytest.raises(TypeError) as err_msg:
        tools._unique_total_sorted("hello")
    assert str(err_msg.value) == "Need an array in `unique_total_sorted`."


def test_unique_total_error_checking_types_string_array():
    with pytest.raises(TypeError) as err_msg:
        tools._unique_total_sorted([1, 2, 3, "b"])
    assert str(err_msg.value) == "Need an array in `unique_total_sorted`."


def test_unique_total_no_duplicates():
    """should return the original array"""
    data = np.arange(0, 100, 0.5)
    new_data = tools._unique_total_sorted(data)
    assert approx(data) == new_data


def test_unique_total_one_duplicate():
    data = [1, 2, 2, 3, 4, 5, 6]
    new_data = tools._unique_total_sorted(data)
    assert approx(new_data) == [1, 4, 3, 4, 5, 6]


def test_unique_total_multiple_dups():
    data = [0.1, 0.2, 0.3, 0.3, 0.4, 0.4, 0.4, 0.5]
    new_data = tools._unique_total_sorted(data)
    assert approx(new_data) == [0.1, 0.2, 0.6, 1.2, 0.5]


def test_unique_total_not_originally_sorted():
    data = [0.1, 0.2, 0.3, 0.3, 0.4, 0.4, 0.4, 0.5]
    data = np.random.permutation(data)  # randomizes the order
    new_data = tools._unique_total_sorted(data)
    assert approx(new_data) == [0.1, 0.2, 0.6, 1.2, 0.5]


def test_unique_total_is_finally_sorted():
    data = np.random.normal(0, 1, 1000)  # unordered
    new_data = tools._unique_total_sorted(data)
    assert sorted(new_data) == approx(new_data)


# ------------------------------------------------------------------------------

# Testing the level that contains certain percentages

# ------------------------------------------------------------------------------
def test_percentile_level_error_checking_positive_density():
    with pytest.raises(ValueError) as err_msg:
        tools.percentile_level([-1, 0, 1, 2, 3], 0.5)
    assert str(err_msg.value) == "Density must be non-negative."


def test_percentile_level_error_checking_no_negative_percentile():
    with pytest.raises(ValueError) as err_msg:
        tools.percentile_level([1, 2, 3], [-1, 0, 0.5])
    assert str(err_msg.value) == "Percentages must be between 0 and 1."


def test_percentile_level_error_checking_no_greater_percent_than_one():
    with pytest.raises(ValueError) as err_msg:
        tools.percentile_level([1, 2, 3], [0, 0.35, 0.7, 1.002])
    assert str(err_msg.value) == "Percentages must be between 0 and 1."


def test_percentile_level_error_checking_empty_list():
    with pytest.raises(ValueError) as err_msg:
        tools.percentile_level([], 0.3)
    assert str(err_msg.value) == "Empty density array not allowed"


def test_percentile_level_error_checking_no_multi_dimension_density():
    density = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError) as err_msg:
        tools.percentile_level(density, 0.5)
    desired_msg = "densities in percentile_level must be array like."
    assert str(err_msg.value) == desired_msg


def test_percentile_level_list_vs_scalar_percentile():
    """A single item list should be treated the same as a scaler for percent"""
    densities = np.random.uniform(0, 10, 100)
    level = 0.6
    scalar_value = tools.percentile_level(densities, level)
    list_value = tools.percentile_level(densities, [level])
    assert [scalar_value] == approx(list_value)


def test_percentile_level_zero_percentile():
    densities = np.random.uniform(0, 10, 1000)
    assert tools.percentile_level(densities, 1.0) < min(densities)


def test_percentile_level_one_percentile():
    densities = np.random.uniform(0, 10, 1000)
    assert tools.percentile_level(densities, 0.0) > max(densities)


def test_percentile_level_type_of_return_scalar():
    assert isinstance(tools.percentile_level([1, 2, 3], 0.2), float)


def test_percentile_level_type_of_return_list():
    assert isinstance(tools.percentile_level([1, 2, 3], [0.2]), list)


def test_percentile_level_length_of_list_return():
    num = np.random.randint(1, 100, size=10)
    for n in num:
        percentiles = np.random.uniform(0, 1, size=n)
        densities = np.random.uniform(0, 10, 1000)
        levels = tools.percentile_level(densities, percentiles)
        assert len(levels) == n


def test_percentile_level_simple_a():
    densities = [1, 1, 2]
    assert 1 < tools.percentile_level(densities, 0.5) < 2


def test_percentile_level_core_simple_b():
    densities = [1, 1, 2, 4]
    assert 2 < tools.percentile_level(densities, 0.5) < 4


def test_percentile_level_core_simple_c():
    densities = [1, 1, 3, 3]
    assert 1 < tools.percentile_level(densities, 0.75) < 3


def test_percentile_level_core_simple_d():
    densities = [1, 2, 3, 4, 5, 10]
    assert tools.percentile_level(densities, 1.0) < 1
    assert 1 < tools.percentile_level(densities, 24.0 / 25.0) < 2
    assert 2 < tools.percentile_level(densities, 22.0 / 25.0) < 3
    assert 3 < tools.percentile_level(densities, 19.0 / 25.0) < 4
    assert 4 < tools.percentile_level(densities, 15.0 / 25.0) < 5
    assert 5 < tools.percentile_level(densities, 10.0 / 25.0) < 10
    assert 10 < tools.percentile_level(densities, 0)


def test_percentile_level_values_multiple():
    densities = [1, 2, 3, 4, 5, 10]
    percentiles = [
        1,
        24.0 / 25.0,
        22.0 / 25.0,
        19.0 / 25.0,
        15.0 / 25.0,
        10.0 / 25.0,
        0,
    ]
    levels = tools.percentile_level(densities, percentiles)
    assert 0 < levels[0] < 1
    assert 1 < levels[1] < 2
    assert 2 < levels[2] < 3
    assert 3 < levels[3] < 4
    assert 4 < levels[4] < 5
    assert 5 < levels[5] < 10
    assert 10 < levels[6]


def test_percentile_level_values_order_not_matter():
    densities = [1, 2, 3, 4, 5, 10]
    percentiles = [24.0 / 25.0, 22.0 / 25.0, 19.0 / 25.0, 15.0 / 25.0, 10.0 / 25.0, 0]
    for _ in range(10):
        np.random.shuffle(percentiles)  # order of percentiles won't matter
        np.random.shuffle(densities)
        levels = tools.percentile_level(densities, percentiles)
        assert 1 < levels[0] < 2
        assert 2 < levels[1] < 3
        assert 3 < levels[2] < 4
        assert 4 < levels[3] < 5
        assert 5 < levels[4] < 10
        assert 10 < levels[5]


def test_percentile_level_big_data():
    # get a ton of data
    densities = np.linspace(0, 1, 1000)
    percentages = np.arange(0.1, 1.0, 0.01)  # 1 to 99 percent
    # the levels can be computed analytically, since this is a uniform
    # distribution. The level should be computed such that the integral of x
    # from l to 1 is some percentage of the total. This gives P = 1 - l^2
    real_levels = sorted(np.sqrt(1 - percentages))
    test_levels = tools.percentile_level(densities, percentages)
    assert real_levels == approx(test_levels, abs=1e-3)
    # need larger tolerance to account for the fact that our points are only
    # spaced 1E-3 apart.


def test_percentile_level_big_data_warnings(recwarn):
    # get a ton of data
    densities = np.linspace(0, 1, 1000)
    percentages = np.arange(0.1, 1.0, 0.01)  # 1 to 99 percent
    # there is enough data here that the levels should be well determined
    tools.percentile_level(densities, percentages)
    assert len(recwarn) == 0


def test_percentile_level_points_very_close():
    """IF two points are very close together, make sure we get in between
    if needed."""
    data = [1, 1, 1, 2.0000, 2.0000001, 3]
    this_level = tools.percentile_level(data, 0.5)
    assert 2.0000 < this_level < 2.0000001


def test_percentile_level_in_middle_of_constants_result():
    """What happens when the correct level is hard to define, since there are
    a bunch of ones like it. This won't matter in most cases since we will
    have floating point errors."""
    data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 9]  # 9 total  # 9 total  # 9 total
    # here the 50th percentile (if cumulatively summing) is right in the middle
    # of the 3s. To get past 50 we do have to go below the threes
    assert 1.0 < tools.percentile_level(data, 0.5) < 3.0


def test_percentile_level_in_middle_of_constants_warning():
    """What happens when the correct level is hard to define, since there are
    a bunch of ones like it. When there is a big gap between what we have
    and what we want we raise an error also."""
    data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 9]  # 9 total  # 9 total  # 9 total
    with pytest.warns(RuntimeWarning):
        tools.percentile_level(data, 0.5)


def test_percentile_level_not_well_constrained_warnings_raise(recwarn):
    """Raise warnings when the things are not well constrained"""
    densities = [5, 4, 3, 2, 1]  # total 15
    # give some percentiles that are not well constrained by the data. They all
    # have to be on different sides of the different densities so that we don't
    # get errors for having duplicate percentages
    percentiles = [0.2, 0.5, 0.7, 0.9, 0.95]
    tools.percentile_level(densities, percentiles)
    assert len(recwarn) == len(percentiles)


def test_percentile_level_not_well_constrained_order():
    """Check results for when things aren't aligned with the data"""
    densities = [5, 4, 1]
    # give some percentiles that are not well constrained by the data
    percentiles = [0.01, 0.2, 0.49, 0.51, 0.7, 0.89, 0.91, 0.95, 0.99]
    results = tools.percentile_level(densities, percentiles)
    assert 4 < results[8] < 5
    assert 4 < results[7] < 5
    assert 4 < results[6] < 5
    assert 1 < results[5] < 4
    assert 1 < results[4] < 4
    assert 1 < results[3] < 4
    assert results[2] < 1
    assert results[1] < 1
    assert results[0] < 1


def test_percentile_level_order():
    """Results should be from low to high levels."""
    densities = np.random.uniform(0, 10, 1000)
    percentages = np.random.uniform(0, 1, 100)  # random order
    levels = tools.percentile_level(densities, percentages)
    for idx in range(len(levels) - 1):
        assert levels[idx] <= levels[idx + 1]


def test_percentile_level_not_aligned():
    """Test what happens when percentages are not aligned well with data."""
    densities = [1, 2, 3]
    assert 2 < tools.percentile_level(densities, 0.01) < 3
    assert 2 < tools.percentile_level(densities, 0.45) < 3
    assert 1 < tools.percentile_level(densities, 0.55) < 2
    assert 1 < tools.percentile_level(densities, 0.75) < 2
    assert tools.percentile_level(densities, 0.90) < 1
    assert tools.percentile_level(densities, 0.99) < 1


def test_percentile_level_warnings_no_raise_if_exact(recwarn):
    """Check ones that are exactly aligned with data, should not warn"""
    densities = [4, 3, 2, 1]
    percentiles = [0.4, 0.7, 0.9]
    tools.percentile_level(densities, percentiles)
    assert len(recwarn) == 0


def test_percentile_level_warnings_no_raise_if_zero(recwarn):
    densities = np.random.uniform(2, 9, 100)
    tools.percentile_level(densities, 0)
    assert len(recwarn) == 0


def test_percentile_level_warnings_no_raise_if_one(recwarn):
    densities = np.random.uniform(2, 9, 100)
    tools.percentile_level(densities, 1.0)
    assert len(recwarn) == 0


def test_percentile_level_warnings_no_raise_if_close(recwarn):
    densities = [1, 1.00000001]
    tools.percentile_level(densities, 0.5)
    assert len(recwarn) == 0


def test_percentile_level_duplicate_warning(recwarn):
    densities = np.linspace(0, 100, 1000)
    percentiles = [0.45000, 0.45000001]
    tools.percentile_level(densities, percentiles)
    assert len(recwarn) == 1


def test_percentile_level_dup_warn_once_for_multiple_dup_one_level(recwarn):
    densities = np.linspace(0, 100, 1000)
    percentiles = [0.45000, 0.45000001, 0.45000002, 0.45000003]
    tools.percentile_level(densities, percentiles)
    assert len(recwarn) == 1


def test_percentile_level_dup_warn_for_multiple_levels_with_dups(recwarn):
    densities = np.linspace(0, 100, 1000)
    percentiles = [
        0.45000,
        0.45000001,
        0.45000002,
        0.45000003,
        0.86000,
        0.86000001,
        0.86000002,
        0.86000003,
    ]
    tools.percentile_level(densities, percentiles)
    assert len(recwarn) == 2


def test_percentile_level_duplicate_warning_with_imprecise(recwarn):
    """If two percentages results in the same level, raise a warning."""
    data = [1.0, 2.0]
    percentiles = [0.7, 0.75]
    tools.percentile_level(data, percentiles)
    assert len(recwarn) == 3  # two from imprecise level, one from duplicate


def test_percentile_level_duplicate_warning_with_imprecise_multiples(recwarn):
    """If two percentages results in the same level, raise a warning."""
    data = [1.0, 2.0]
    percentiles = [0.45, 0.5, 0.55, 0.7, 0.75]
    tools.percentile_level(data, percentiles)
    assert len(recwarn) == 7  # four from imprecise level, two from duplicate


# ------------------------------------------------------------------------------

# Testing the density contours function

# ------------------------------------------------------------------------------
def test_hist_2d_error_checking_types_no_strings():
    """Proxy for non-numerical data of any kind."""
    with pytest.raises(TypeError) as err_msg:
        tools.smart_hist_2d("a", [1, 2])
    assert str(err_msg.value) == "x must be a numerical array."

    with pytest.raises(TypeError) as err_msg:
        tools.smart_hist_2d([1, 2], "a")
    assert str(err_msg.value) == "y must be a numerical array."


def test_hist_2d_error_x_and_y_same_length():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 2], [1, 2, 3])
    desired_msg = "x and y data must be the same length."
    assert str(err_msg.value) == desired_msg


def test_hist_2d_bin_size_typing_string():
    with pytest.raises(TypeError) as err_msg:
        tools.smart_hist_2d([1], [2], bin_size="he")
    desired_msg = "Bin_size must be either a scalar or " "two element numeric list."
    assert str(err_msg.value) == desired_msg


def test_hist_2d_bin_size_typing_empty_list():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1], [2], bin_size=[])
    desired_msg = "Bin_size must be either a scalar or " "two element numeric list."
    assert str(err_msg.value) == desired_msg


def test_hist_2d_bin_size_typing_too_long():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1], [2], bin_size=[1, 2, 3])
    desired_msg = "Bin_size must be either a scalar or " "two element numeric list."
    assert str(err_msg.value) == desired_msg


def test_hist_2d_bin_size_positive_scalar():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1], [2], bin_size=0)
    assert str(err_msg.value) == "Bin size must be positive."

    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1], [2], bin_size=-4)
    assert str(err_msg.value) == "Bin size must be positive."


def test_hist_2d_bin_size_positive_single_element_list():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1], [2], bin_size=[0])
    assert str(err_msg.value) == "Bin size must be positive."

    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1], [2], bin_size=[-4])
    assert str(err_msg.value) == "Bin size must be positive."


def test_hist_2d_bin_size_positive_two_element_list():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1], [2], bin_size=[0, 2])
    assert str(err_msg.value) == "Bin size must be positive."

    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1], [2], bin_size=[2, 0])
    assert str(err_msg.value) == "Bin size must be positive."

    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1], [2], bin_size=[0, 0])
    assert str(err_msg.value) == "Bin size must be positive."


def test_hist_2d_padding_typing_string():
    with pytest.raises(TypeError) as err_msg:
        tools.smart_hist_2d([1, 2], [2, 3], padding="he")
    desired_msg = "Padding must be either a scalar or two element numeric list."
    assert str(err_msg.value) == desired_msg


def test_hist_2d_padding_typing_empty_list():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 3], [2, 3], padding=[])
    desired_msg = "Padding must be either a scalar or two element numeric list."
    assert str(err_msg.value) == desired_msg


def test_hist_2d_padding_typing_too_long_list():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 3], [2, 3], padding=[1, 2, 3])
    desired_msg = "Padding must be either a scalar or two element numeric list."
    assert str(err_msg.value) == desired_msg


def test_hist_2d_padding_nonnegative_scalar():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 3], [2, 3], padding=-4)
    assert str(err_msg.value) == "Padding must be non-negative."


def test_hist_2d_padding_nonnegative_single_element_list():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 3], [2, 3], padding=[-4])
    assert str(err_msg.value) == "Padding must be non-negative."


def test_hist_2d_padding_nonnegative_two_element_list():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 3], [2, 3], padding=[-1, 2])
    assert str(err_msg.value) == "Padding must be non-negative."

    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 3], [2, 3], padding=[2, -2])
    assert str(err_msg.value) == "Padding must be non-negative."

    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 3], [2, 3], padding=[-1, -1])
    assert str(err_msg.value) == "Padding must be non-negative."


def test_hist_2d_error_checking_types_no_list_weights():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 3], [1, 2], weights=1)
    desired_msg = "Weights and data need to have the same length."
    assert str(err_msg.value) == desired_msg


def test_hist_2d_error_checking_types_no_strings_weights():
    """Proxy for non-numerical data of any kind."""
    with pytest.raises(TypeError) as err_msg:
        tools.smart_hist_2d([1, 2], [1, 2], "ab")
    desired_msg = "Bin_size must be either a scalar or " "two element numeric list."
    assert str(err_msg.value) == desired_msg


def test_hist_2d_error_x_y_weights_same_length():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 2], [1, 2], weights=[1, 2, 3])
    desired_msg = "Weights and data need to have the same length."
    assert str(err_msg.value) == desired_msg


def test_hist_2d_error_checking_weights_positive():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 2, 3], [1, 2, 3], weights=[1, -2, 3])
    assert str(err_msg.value) == "Weights must be non-negative."

    # zero is acceptable
    tools.smart_hist_2d([1, 2, 3], [1, 2, 3], weights=[1, 0, 3])  # no error


def test_hist_2d_error_checking_smoothing_typing_string():
    with pytest.raises(TypeError) as err_msg:
        tools.smart_hist_2d([1, 3], [2, 3], smoothing="he")
    des_msg = "Smoothing must be either a scalar or two element numeric list."
    assert str(err_msg.value) == des_msg


def test_hist_2d_error_checking_smoothing_typing_empty_list():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 2], [2, 3], smoothing=[])
    des_msg = "Smoothing must be either a scalar or two element numeric list."
    assert str(err_msg.value) == des_msg


def test_hist_2d_error_checking_smoothing_typing_too_long_list():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 2], [2, 3], smoothing=[1, 2, 3])
    des_msg = "Smoothing must be either a scalar or two element numeric list."
    assert str(err_msg.value) == des_msg


def test_hist_2d_error_checking_smoothing_nonnegative_scalar():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 2], [2, 3], smoothing=-4)
    assert str(err_msg.value) == "Smoothing must be nonnegative."


def test_hist_2d_error_checking_smoothing_nonnegative_single_element_list():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 2], [2, 3], smoothing=[-4])
    assert str(err_msg.value) == "Smoothing must be nonnegative."


def test_hist_2d_error_checking_smoothing_nonnegative_two_element_list():
    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 2], [2, 3], smoothing=[-1, 2])
    assert str(err_msg.value) == "Smoothing must be nonnegative."

    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 2], [2, 3], smoothing=[2, -2])
    assert str(err_msg.value) == "Smoothing must be nonnegative."

    with pytest.raises(ValueError) as err_msg:
        tools.smart_hist_2d([1, 3], [2, 3], smoothing=[-1, -1])
    assert str(err_msg.value) == "Smoothing must be nonnegative."


# done with error checking. Now test output
def test_hist_2d_length_of_output():
    output = tools.smart_hist_2d([1, 2], [2, 3])
    assert len(output) == 3


@pytest.fixture
def random_data():
    xs = np.random.normal(0, 10, 1000)
    ys = np.random.normal(0, 10, 1000)
    return xs, ys


def test_hist_2d_bin_size_scalar(random_data):
    xs, ys = random_data
    bin_size = 2.345
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys, bin_size)
    empirical_x_bin = x_edges[1] - x_edges[0]
    empirical_y_bin = y_edges[1] - y_edges[0]
    assert approx(empirical_x_bin) == bin_size
    assert approx(empirical_y_bin) == bin_size


def test_hist_2d_bin_size_single_item_list(random_data):
    xs, ys = random_data
    bin_size = 2.345
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys, bin_size=[bin_size])
    empirical_x_bin = x_edges[1] - x_edges[0]
    empirical_y_bin = y_edges[1] - y_edges[0]
    assert approx(bin_size) == empirical_x_bin
    assert approx(bin_size) == empirical_y_bin


def test_hist_2d_bin_size_separate_x_y(random_data):
    xs, ys = random_data
    x_bin_size = 2.345
    y_bin_size = 7.347
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys, [x_bin_size, y_bin_size])
    empirical_x_bin = x_edges[1] - x_edges[0]
    empirical_y_bin = y_edges[1] - y_edges[0]
    assert approx(x_bin_size) == empirical_x_bin
    assert approx(y_bin_size) == empirical_y_bin


def test_hist_2d_bin_size_all_same_single_bin(random_data):
    xs, ys = random_data
    bin_size = 2.345
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys, bin_size)
    for x_idx in range(len(x_edges) - 1):
        empirical_x_bin = x_edges[x_idx + 1] - x_edges[x_idx]
        assert empirical_x_bin == approx(bin_size)
    for y_idx in range(len(y_edges) - 1):
        empirical_y_bin = y_edges[y_idx + 1] - y_edges[y_idx]
        assert empirical_y_bin == approx(bin_size)


def test_hist_2d_bin_size_all_same_separate_xy(random_data):
    xs, ys = random_data
    x_bin_size = 2.345
    y_bin_size = 7.347
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys, [x_bin_size, y_bin_size])
    for x_idx in range(len(x_edges) - 1):
        empirical_x_bin = x_edges[x_idx + 1] - x_edges[x_idx]
        assert empirical_x_bin == approx(x_bin_size)
    for y_idx in range(len(y_edges) - 1):
        empirical_y_bin = y_edges[y_idx + 1] - y_edges[y_idx]
        assert empirical_y_bin == approx(y_bin_size)


def test_hist_edges_contain_data_no_bins(random_data):
    xs, ys = random_data
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys)

    assert x_edges[+0] < min(xs)
    assert x_edges[-1] > max(xs)
    assert y_edges[+0] < min(ys)
    assert y_edges[-1] > max(ys)


def test_hist_edges_contain_data_single_bin_size_scalar(random_data):
    xs, ys = random_data

    bin_size = 1.0
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys, bin_size=bin_size)

    assert x_edges[+0] < min(xs)
    assert x_edges[-1] > max(xs)
    assert y_edges[+0] < min(ys)
    assert y_edges[-1] > max(ys)


def test_hist_edges_contain_data_two_bin_size(random_data):
    xs, ys = random_data

    x_bin_size = 0.56
    y_bin_size = 0.892
    _, x_edges, y_edges = tools.smart_hist_2d(xs, ys, bin_size=[x_bin_size, y_bin_size])

    assert x_edges[+0] < min(xs)
    assert x_edges[-1] > max(xs)
    assert y_edges[+0] < min(ys)
    assert y_edges[-1] > max(ys)


def test_hist_edges_contain_data_single_bin_size_scalar_padding(random_data):
    xs, ys = random_data

    bin_size = 1.0
    padding = 3.45
    hist, x_edges, y_edges = tools.smart_hist_2d(
        xs, ys, bin_size=bin_size, padding=padding
    )

    assert x_edges[+0] < (min(xs) - padding)
    assert x_edges[-1] > (max(xs) + padding)
    assert y_edges[+0] < (min(ys) - padding)
    assert y_edges[-1] > (max(ys) + padding)


def test_hist_edges_contain_data_two_bin_size_two_padding(random_data):
    xs, ys = random_data

    x_bin_size = 0.56
    y_bin_size = 0.892
    x_padding = 3.46
    y_padding = 1.34
    _, x_edges, y_edges = tools.smart_hist_2d(
        xs, ys, bin_size=[x_bin_size, y_bin_size], padding=[x_padding, y_padding]
    )

    assert x_edges[+0] < (min(xs) - x_padding)
    assert x_edges[-1] > (max(xs) + x_padding)
    assert y_edges[+0] < (min(ys) - y_padding)
    assert y_edges[-1] > (max(ys) + y_padding)


def test_hist_2d_results_in_right_number_cells_one_point():
    xs = [1]
    ys = [1]
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys, bin_size=0.5)
    hist = hist.flatten()
    assert len(hist.nonzero()) == 1


def test_hist_2d_results_in_right_number_cells_many_points():
    xs = [1, 2, 3, 3]
    ys = [1, 1, 1, 2]
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys, bin_size=0.5)
    hist = hist.flatten()
    assert len(hist.nonzero()[0]) == 4


def test_hist_2d_results_in_right_number_cells_many_points_with_dups():
    xs = [1, 2, 3, 4, 4]  # two in same cell
    ys = [1, 1, 1, 1, 1]
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys, bin_size=0.5)
    hist = hist.flatten()
    assert len(hist.nonzero()[0]) == 4


def test_hist_2d_results_right_height_no_weights_no_dups():
    xs = [1, 2, 3, 3]
    ys = [1, 1, 1, 2]
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys, bin_size=0.5)
    hist = hist.flatten()
    assert np.max(hist) == 1


def test_hist_2d_results_right_height_no_weights_with_dups():
    xs = [1, 2, 3, 4, 4]  # two in same cell
    ys = [1, 1, 1, 1, 1]
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys, bin_size=0.5)
    hist = hist.flatten()
    assert np.max(hist) == 2


def test_hist_2d_results_right_height_with_weights_no_dups():
    xs = [1, 2, 3, 3]
    ys = [1, 1, 1, 2]
    weights = [4, 3, 2, 1]
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys, bin_size=0.5, weights=weights)
    hist = hist.flatten()
    assert np.max(hist) == 4


def test_hist_2d_results_right_height_with_weights_with_dups():
    xs = [1, 2, 3, 4, 4]  # two in same cell
    ys = [1, 1, 1, 1, 1]
    weights = [1.3, 2.3, 3.5, 2, 3]
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys, bin_size=0.5, weights=weights)
    hist = hist.flatten()
    assert np.max(hist) == 5


def test_hist_2d_results_orientation():
    xs = [0.75, 0.75, 1.25]
    ys = [0.75, 1.25, 1.25]
    hist, x_edges, y_edges = tools.smart_hist_2d(xs, ys, bin_size=0.5)

    # find the location of the indices of all three locations, according to bins
    x_idxs = [None, None, None]
    y_idxs = [None, None, None]
    for x_edge_idx in range(len(x_edges) - 1):
        for x_idx, x in enumerate(xs):
            if x_edges[x_edge_idx] < x < x_edges[x_edge_idx + 1]:
                x_idxs[x_idx] = x_edge_idx
    for y_edge_idx in range(len(y_edges) - 1):
        for y_idx, y in enumerate(ys):
            if y_edges[y_edge_idx] < y < y_edges[y_edge_idx + 1]:
                y_idxs[y_idx] = y_edge_idx

    # then check that there are points where they should be. Rows go first in
    # all the actual matplotlib applications, so that's what we'll use.
    for x_idx, y_idx in zip(x_idxs, y_idxs):
        assert hist[y_idx][x_idx] > 0


def test_hist_2d_smoothing_scalar_all_cells_nonzero():
    xs = [1]
    ys = [1]
    hist, _, _ = tools.smart_hist_2d(xs, ys, bin_size=0.01, smoothing=1)
    assert np.all(hist > 0)


def test_hist_2d_smoothing_different_scale_all_cells_nonzero():
    xs = [1]
    ys = [1]
    hist, _, _ = tools.smart_hist_2d(xs, ys, bin_size=0.01, smoothing=[1, 2])
    assert np.all(hist > 0)


def test_hist_2d_smoothing_different_scale_different_results():
    xs = [0]
    ys = [0]
    hist, _, _ = tools.smart_hist_2d(xs, ys, bin_size=0.1, padding=10, smoothing=[5, 1])
    # more smoothed in x than in y. So you need to go farther in x than y to
    # get the same decrease
    center_idx_x = int(hist.shape[0] / 2.0)
    center_idx_y = int(hist.shape[1] / 2.0)

    central_dens = hist[center_idx_y][center_idx_x]
    off_in_x = hist[center_idx_y][center_idx_x + 20]
    off_in_y = hist[center_idx_y + 20][center_idx_x]
    assert central_dens > off_in_x
    assert central_dens > off_in_y
    assert off_in_x > off_in_y  # since at a given distance, x lowers less.


# ------------------------------------------------------------------------------

# Testing the padding from smoothing. Full error checking won't be done, since
# that will be done in the 2D hist function.

# ------------------------------------------------------------------------------
def test_padding_from_smoothing_error_empty_list():
    with pytest.raises(ValueError) as err_msg:
        tools._padding_from_smoothing([])
    desired_msg = "Smoothing must be either a scalar or two element " "numeric list."
    assert str(err_msg.value) == desired_msg


def test_padding_from_smoothing_error_list_too_long():
    with pytest.raises(ValueError) as err_msg:
        tools._padding_from_smoothing([1, 2, 3])
    desired_msg = "Smoothing must be either a scalar or two " "element numeric list."
    assert str(err_msg.value) == desired_msg


def test_padding_from_smoothing_error_string():
    with pytest.raises(TypeError) as err_msg:
        tools._padding_from_smoothing("ab")
    desired_msg = "Smoothing must be either a scalar or " "two element numeric list."
    assert str(err_msg.value) == desired_msg


def test_padding_from_smoothing_error_string_array():
    with pytest.raises(TypeError) as err_msg:
        tools._padding_from_smoothing(["a", "b"])
    desired_msg = "Smoothing must be either a scalar or " "two element numeric list."
    assert str(err_msg.value) == desired_msg


def test_padding_from_smoothing_scalar():
    smoothing = 4
    padding = tools._padding_from_smoothing(smoothing)
    assert padding == approx([20, 20])


def test_padding_from_smoothing_single_list():
    smoothing = [4.0]
    padding = tools._padding_from_smoothing(smoothing)
    assert padding == approx([20, 20])


def test_padding_from_smoothing_multiple_list():
    smoothing = [3.33, 9.33]
    true_padding = [16.65, 46.65]
    test_padding = tools._padding_from_smoothing(smoothing)
    assert true_padding == approx(test_padding)


def test_padding_from_smoothing_error_string_correct():
    padding = tools._padding_from_smoothing("12")
    assert padding == approx([5, 10])


def test_padding_from_smoothing_error_string_array_correct():
    padding = tools._padding_from_smoothing(["1", "2"])
    assert padding == approx([5, 10])


# ------------------------------------------------------------------------------

# Testing the outer contour level function.

# ------------------------------------------------------------------------------
def test_outer_contour_single_value():
    circle = path.Path.circle((0, 0), 1)
    assert tools._outer_contours([circle]) == [circle]


def test_outer_contour_concentric_circles_two():
    circle_inner = path.Path.circle((0, 0), 1)
    circle_outer = path.Path.circle((0, 0), 2)
    circles = [circle_inner, circle_outer]
    assert tools._outer_contours(circles) == [circle_outer]


def test_outer_contour_concentric_circles_many():
    circle_1 = path.Path.circle((0, 0), 1)
    circle_2 = path.Path.circle((0, 0), 2)
    circle_3 = path.Path.circle((0, 0), 3)
    circle_4 = path.Path.circle((0, 0), 4)
    circles = [circle_3, circle_4, circle_2, circle_1]
    assert tools._outer_contours(circles) == [circle_4]


def test_outer_contour_few_offset():
    circle_1 = path.Path.circle((0, 0), 1)
    circle_2 = path.Path.circle((0, 0), 2)
    circle_3 = path.Path.circle((7, 0), 3)
    circle_4 = path.Path.circle((0, 10), 4)
    circles = [circle_3, circle_4, circle_2, circle_1]

    test_results = tools._outer_contours(circles)
    true_results = [circle_4, circle_3, circle_2]
    # can't directly test equality, since order doesn't matter.
    for circle in true_results:
        assert circle in test_results
    assert len(true_results) == len(test_results)


# ------------------------------------------------------------------------------

# Testing the Gaussian

# ------------------------------------------------------------------------------
def test_gaussian_peak_is_at_mean():
    mean = 3
    xs = np.arange(0, 10, 0.01)
    values = tools.gaussian(xs, mean, 1)
    max_x = xs[np.argmax(values)]
    assert max_x == 3


def test_gaussian_proper_peak_normalization():
    sigma = 1.5
    value = tools.gaussian(0, 0, sigma)
    assert np.isclose(value, (1.0 / (sigma * np.sqrt(2 * np.pi))), rtol=0, atol=0.0001)


def test_gaussian_integration_over_infinity():
    def integrand(x):
        return tools.gaussian(x, -3, 2)

    result = integrate.quad(integrand, -23, 17)[0]
    assert np.isclose(result, 1, rtol=0, atol=0.00001)


def test_gaussian_integration_over_one_sigma():
    def integrand(x):
        return tools.gaussian(x, 5, 3)

    result = integrate.quad(integrand, 2, 8)[0]
    assert np.isclose(result, 0.68268, rtol=0, atol=0.00001)


def test_gaussian_integration_over_three_sigma():
    def integrand(x):
        return tools.gaussian(x, 1, 1)

    result = integrate.quad(integrand, -2, 4)[0]
    assert np.isclose(result, 0.9973, rtol=0, atol=0.00001)
