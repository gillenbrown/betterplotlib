import pytest
from pytest import approx
import numpy as np
from betterplotlib import tools

random_x = np.random.normal(0, 1, 1000)

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
    assert 0 < tools._alpha(10 ** 2) <= 1.0
    assert 0 < tools._alpha(10 ** 4) <= 1.0
    assert 0 < tools._alpha(10 ** 10) <= 1.0


# ------------------------------------------------------------------------------
#
# Freedman Diaconis core bin size testing
#
# ------------------------------------------------------------------------------
def test_freedman_diaconis_core_zero_data():
    """Length of zero or negative doesn't work in FD."""
    with pytest.raises(ValueError):
        tools._freedman_diaconis_core(10, 0)
    with pytest.raises(ValueError):
        tools._freedman_diaconis_core(10, -5)


def test_freedman_diaconis_core_zero_iqr():
    """zero iqr gives zero bin size, which is meaningless"""
    with pytest.raises(ValueError):
        tools._freedman_diaconis_core(0, 10)
    with pytest.raises(ValueError):
        tools._freedman_diaconis_core(-5, 10)


def test_freedman_diaconis_core_data_types_string():
    with pytest.raises(TypeError):
        tools._freedman_diaconis_core("t", 5)
    with pytest.raises(TypeError):
        tools._freedman_diaconis_core(5, "s")


def test_freedman_diaconis_core_data_types_list():
    with pytest.raises(TypeError):
        tools._freedman_diaconis_core([1, 2], 5)
    with pytest.raises(TypeError):
        tools._freedman_diaconis_core(5, [4, 5])


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
    with pytest.raises(ValueError):
        tools._freedman_diaconis([])


def test_freedman_diaconis_zero_range_a():
    """No range produces bad bins."""
    with pytest.raises(ValueError):
        tools._freedman_diaconis([1])


def test_freedman_diaconis_zero_range_b():
    """zero interquartile range doesn't work."""
    with pytest.raises(ValueError):
        tools._freedman_diaconis([1, 2, 2, 2, 2, 2, 3])


def test_freedman_diaconis_example_a():
    """Have an example here that will result in easy to calculate values"""
    data = np.linspace(0, 100, num=1000)
    # here iqr = 50, n^{1/3} = 10, so 2 * iqr / n^{1/3} = 10
    real_bin_size = 10.0
    test_bin_size = tools._freedman_diaconis(data)
    assert real_bin_size == approx(test_bin_size)


def test_freedman_diaconis_example_b():
    """Another example I can calculate easily."""
    data = [1, 1,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            4]
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
    assert tools._round_to_nice_width(1.2E-7) == approx(1E-7)


def test_round_to_nice_width_with_exp_large():
    assert tools._round_to_nice_width(8.6E7) == approx(1E8)


def test_round_to_nice_width_with_exp_general():
    """Want either 1, 2, 5, or 10 bins per 10 units. So we either round the
    bin to 10, 5, 2, or 1, respectively. """
    for exp in np.arange(-10.0, 10.0):
        factor = 10**exp
        assert np.isclose(tools._round_to_nice_width(1.0 * factor),
                          1.0 * factor)
        assert np.isclose(tools._round_to_nice_width(1.49999 * factor),
                          1.0 * factor)
        assert np.isclose(tools._round_to_nice_width(1.50001 * factor),
                          2.0 * factor)
        assert np.isclose(tools._round_to_nice_width(2.0 * factor),
                          2.0 * factor)
        assert np.isclose(tools._round_to_nice_width(3.49999 * factor),
                          2.0 * factor)
        assert np.isclose(tools._round_to_nice_width(3.50001 * factor),
                          5.0 * factor)
        assert np.isclose(tools._round_to_nice_width(5.0 * factor),
                          5.0 * factor)
        assert np.isclose(tools._round_to_nice_width(7.49999 * factor),
                          5.0 * factor)
        assert np.isclose(tools._round_to_nice_width(7.50001 * factor),
                          10.0 * factor)
        assert np.isclose(tools._round_to_nice_width(10.0 * factor),
                          10.0 * factor)
        assert np.isclose(tools._round_to_nice_width(14.9999 * factor),
                          10.0 * factor)
        assert np.isclose(tools._round_to_nice_width(15.0001 * factor),
                          20.0 * factor)


def test_round_to_nice_width_error_checking_positive():
    """can't have a bin size that is negative or zero"""
    with pytest.raises(ValueError):
        tools._round_to_nice_width(0)
    with pytest.raises(ValueError):
        tools._round_to_nice_width(-1)


def test_round_to_nice_width_error_checking_types_string():
    """can't pass in anything other th"""
    with pytest.raises(TypeError):
        tools._round_to_nice_width("1.2")


def test_round_to_nice_width_error_checking_types_list():
    """can't pass in a list"""
    with pytest.raises(TypeError):
        tools._round_to_nice_width([1, 3])
    # or an array
    with pytest.raises(TypeError):
        tools._round_to_nice_width(np.array([5, 3]))


# ------------------------------------------------------------------------------
#
# binning
#
# ------------------------------------------------------------------------------
def test_binning_bin_size_error_checking_zero():
    with pytest.raises(ValueError):
        tools._binning(min=1, max=2, bin_size=0)


def test_binning_bin_size_error_checking_negative():
    with pytest.raises(ValueError):
        tools._binning(min=1, max=2, bin_size=-1)


def test_binning_padding_error_checking():
    with pytest.raises(ValueError):
        tools._binning(min=1, max=2, bin_size=1, padding=-1)


def test_binning_min_max_checking_not_ordered():
    with pytest.raises(ValueError):
        tools._binning(min=1, max=0, bin_size=1)


def test_binning_wrong_type_min():
    with pytest.raises(TypeError):
        tools._binning(min="a", max=0, bin_size=1)


def test_binning_wrong_type_max():
    with pytest.raises(TypeError):
        tools._binning(min=1, max="a", bin_size=1)


def test_binning_wrong_type_min_max():
    with pytest.raises(TypeError):
        tools._binning(min="a", max="b", bin_size=1)


def test_binning_wrong_type_bin_size():
    with pytest.raises(TypeError):
        tools._binning(min=0, max=1, bin_size="a")


def test_binning_wrong_type_padding():
    with pytest.raises(TypeError):
        tools._binning(min=-1, max=0, bin_size=1, padding="a")


def test_binning_wrong_type_min_list():
    with pytest.raises(TypeError):
        tools._binning(min=[-1, -2], max=2, bin_size=1, padding=0)


def test_binning_wrong_type_max_list():
    with pytest.raises(TypeError):
        tools._binning(min=-1, max=[0, 1], bin_size=1, padding=0)


def test_binning_wrong_type_bin_size_list():
    with pytest.raises(TypeError):
        tools._binning(min=-1, max=0, bin_size=[1, 2], padding=0)


def test_binning_wrong_type_padding_list():
    with pytest.raises(TypeError):
        tools._binning(min=-1, max=0, bin_size=1, padding=[0, 1])


def test_binning_positive_bin_aligned():
    test_bins = tools._binning(min=1.0, max=2.0, bin_size=0.5)
    real_bins = [0.5, 1.0, 1.5, 2.0, 2.5]
    assert real_bins == approx(test_bins)


def test_binning_negative_bin_aligned():
    test_bins = tools._binning(min=-2.0, max=-1.0, bin_size=0.5)
    real_bins = [-2.5, -2, -1.5, -1, -0.5]
    assert real_bins == approx(test_bins)


def test_binning_zero_to_pos_bin_aligned():
    test_bins = tools._binning(min=0, max=1, bin_size=0.5)
    real_bins = [-0.5, 0, 0.5, 1.0, 1.5]
    assert real_bins == approx(test_bins)


def test_binning_neg_to_zero_bin_aligned():
    test_bins = tools._binning(min=-1, max=0, bin_size=0.5)
    real_bins = [-1.5, -1, -0.5, 0, 0.5]
    assert real_bins == approx(test_bins)


def test_binning_zero_to_pos_bin_aligned_b():
    test_bins = tools._binning(min=0.5, max=1, bin_size=0.5)
    real_bins = [0, 0.5, 1.0, 1.5]
    assert real_bins == approx(test_bins)


def test_binning_neg_to_zero_bin_aligned_b():
    test_bins = tools._binning(min=-1, max=-0.5, bin_size=0.5)
    real_bins = [-1.5, -1, -0.5, 0]
    assert real_bins == approx(test_bins)


def test_binning_across_zero_bin_aligned():
    test_bins = tools._binning(min=-0.5, max=1, bin_size=0.5)
    real_bins = [-1, -0.5, 0, 0.5, 1.0, 1.5]
    assert real_bins == approx(test_bins)


def test_binning_across_zero_not_aligned():
    test_bins = tools._binning(min=-0.25, max=0.25, bin_size=0.5)
    real_bins = [-0.5, 0, 0.5]
    assert real_bins == approx(test_bins)


def test_binning_neg_to_zero_not_aligned():
    test_bins = tools._binning(min=-0.75, max=-0.25, bin_size=0.5)
    real_bins = [-1, -0.5, 0]
    assert real_bins == approx(test_bins)


def test_binning_zero_to_pos_not_aligned():
    test_bins = tools._binning(min=0.25, max=0.75, bin_size=0.5)
    real_bins = [0, 0.5, 1]
    assert real_bins == approx(test_bins)


def test_binning_positive_not_aligned():
    test_bins = tools._binning(min=0.75, max=1.25, bin_size=0.5)
    real_bins = [0.5, 1, 1.5]
    assert real_bins == approx(test_bins)


def test_binning_negative_not_aligned():
    test_bins = tools._binning(min=-1.25, max=-0.75, bin_size=0.5)
    real_bins = [-1.5, -1, -0.5]
    assert real_bins == approx(test_bins)


def test_binning_across_zero_many_bins_not_aligned():
    test_bins = tools._binning(min=-0.51, max=0.61, bin_size=0.1)
    real_bins = [-0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0,
                 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    assert real_bins == approx(test_bins)


def test_binning_positive_many_bins_not_aligned():
    test_bins = tools._binning(min=0.51, max=1.11, bin_size=0.1)
    real_bins = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    assert real_bins == approx(test_bins)


def test_binning_negative_many_bins_not_aligned():
    test_bins = tools._binning(min=-1.31, max=-0.49, bin_size=0.1)
    real_bins = [-1.4, -1.3, -1.2, -1.1, -1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4]
    assert real_bins == approx(test_bins)


def test_binning_zero_to_pos_many_bins_not_aligned():
    test_bins = tools._binning(min=0.01, max=0.51, bin_size=0.1)
    real_bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    assert real_bins == approx(test_bins)


def test_binning_neg_to_zero_many_bins_not_aligned():
    test_bins = tools._binning(min=-0.51, max=-0.01, bin_size=0.1)
    real_bins = [-0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0]
    assert real_bins == approx(test_bins)


def test_binning_padding_positive_aligned():
    test_bins = tools._binning(min=5, max=10, bin_size=1, padding=2)
    real_bins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    assert real_bins == approx(test_bins)


def test_binning_padding_negative_aligned():
    test_bins = tools._binning(min=-1.0, max=-0.5, bin_size=0.1, padding=0.2)
    real_bins = [-1.3, -1.2, -1.1, -1, -0.9, -0.8, -0.7,
                 -0.6, -0.5, -0.4, -0.3, -0.2]
    assert real_bins == approx(test_bins)


def test_binning_padding_positive_not_aligned():
    test_bins = tools._binning(min=0.5, max=1.1, bin_size=0.2, padding=0.2)
    real_bins = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4]
    assert real_bins == approx(test_bins)


def test_binning_padding_negative_not_aligned():
    test_bins = tools._binning(min=-11, max=-5, bin_size=2, padding=2)
    real_bins = [-14, -12, -10, -8, -6, -4, -2]
    assert real_bins == approx(test_bins)


def test_binning_range_smaller_than_bin_aligned():
    test_bins = tools._binning(min=0.0, max=2.0, bin_size=10.0)
    real_bins = [-10, 0, 10]
    assert real_bins == approx(test_bins)


def test_binning_range_smaller_than_bin_not_aligned():
    test_bins = tools._binning(min=-5.0, max=-3.0, bin_size=10.0)
    real_bins = [-10, 0]
    assert real_bins == approx(test_bins)


def test_binning_min_equal_max():
    test_bins = tools._binning(min=1, max=1, bin_size=0.5)
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
    with pytest.raises(TypeError):
        tools.bin_centers("hello")
    with pytest.raises(TypeError):
        tools.bin_centers(100)


def test_centers_wrong_type_wrong_iterable():
    test_dict = {0: 0, 1: 1}
    with pytest.raises(TypeError):
        tools.bin_centers(test_dict)


def test_centers_zero_length_edges():
    with pytest.raises(ValueError):
        tools.bin_centers([])


def test_centers_one_length_edges():
    with pytest.raises(ValueError):
        tools.bin_centers([1])


def test_centers_two_length():
    assert tools.bin_centers([1, 2]) == approx(1.5)


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


#-------------------------------------------------------------------------------

# Testing the parsing of the bin size. This doesn't have a lot.

#-------------------------------------------------------------------------------
def test_two_element_list_more_elt_array():
    with pytest.raises(ValueError):
        tools._two_item_list([0.4, 0.3, 0.1])


def test_two_element_list_zero_elt_array():
    with pytest.raises(ValueError):
        tools._two_item_list([])


def test_two_element_list_scalar():
    assert tools._two_item_list(0.1) == [0.1, 0.1]


def test_two_element_list_two_elt_array():
    assert tools._two_item_list([0.1, 0.3]) == [0.1, 0.3]


def test_two_element_list_one_elt_array():
    assert tools._two_item_list([0.4]) == [0.4, 0.4]


def test_two_element_list_strings_too_long():
    with pytest.raises(ValueError):
        tools._two_item_list("hello")


def test_two_element_list_strings_too_short():
    with pytest.raises(ValueError):
        tools._two_item_list("")


def test_two_element_list_two_item_string():
    assert tools._two_item_list("ab") == ["a", "b"]


def test_two_element_list_one_item_string():
    assert tools._two_item_list("a") == ["a", "a"]


def test_two_element_list_set():
    assert tools._two_item_list("a") == ["a", "a"]

#-------------------------------------------------------------------------------

# Testing the parsing of the bin options. This relies heavily on the _binning
# function, so a lot of the more detailed testing is taken care of there.

#-------------------------------------------------------------------------------
def test_make_bins_error_checking_data_type():
    with pytest.raises(TypeError):
        tools.make_bins("hello")


def test_make_bins_error_checking_bin_size_type():
    with pytest.raises(TypeError):
        tools.make_bins([1, 2 , 3], "hello")


def test_make_bins_error_checking_padding_type():
    with pytest.raises(TypeError):
        tools.make_bins([1, 2, 3], 1, "hello")


def test_make_bins_error_checking_data_type_not_list():
    with pytest.raises(TypeError):
        tools.make_bins(1)


def test_make_bins_error_checking_bin_size_type_list():
    with pytest.raises(TypeError):
        tools.make_bins([1, 2, 3], [1, 2])


def test_make_bins_error_checking_padding_type_list():
    with pytest.raises(TypeError):
        tools.make_bins([1, 2, 3], 1, [4, 5])


def test_make_bins_error_checking_need_data_no_bin_size():
    with pytest.raises(ValueError):
        tools.make_bins([])


def test_make_bins_error_checking_need_data_with_bin_size():
    with pytest.raises(ValueError):
        tools.make_bins([], bin_size=1.0)


def test_make_bins_error_checking_length_of_data_too_small_bad():
    """If we don't pass in much data, we need to specify our bin size."""
    with pytest.raises(ValueError):
        tools.make_bins([1])


def test_make_bins_error_checking_length_of_data_too_small_good():
    """If we don't pass in much data, we need to specify our bin size."""
    test_bins = tools.make_bins([1], bin_size=0.5)
    true_bins = [0.5, 1, 1.5]
    assert true_bins == approx(test_bins)


def test_make_bins_error_checking_bin_size_positive():
    with pytest.raises(ValueError):
        tools.make_bins([1, 2, 3], 0)
    with pytest.raises(ValueError):
        tools.make_bins([1, 2, 3], -1)


def test_make_bins_error_checking_padding_nonnegative():
    with pytest.raises(ValueError):
        tools.make_bins([1, 2, 3], 1, padding=-1)


def test_make_bins_too_small_iqr_bad():
    """If the IQR of the data is too small, we have to pass in the bin size"""
    with pytest.raises(ValueError):
        tools.make_bins([1, 2, 2, 2, 2, 2, 2, 3])


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
    assert approx(0.0) in bins


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
    data = np.random.uniform(1E-4, 5E-4, 1000)
    bins = tools.make_bins(data)
    bin_size = bins[1] - bins[0]
    assert 1E-6 < bin_size < 5E-4


def test_make_bins_order_of_magnitude_of_chosen_bins_large():
    data = np.random.uniform(1E4, 5E4, 1000)
    bins = tools.make_bins(data)
    bin_size = bins[1] - bins[0]
    assert 1E3 < bin_size < 5E4


@pytest.mark.parametrize("bin_size", [1, None])
def test_make_bins_all_same_size(bin_size):
    data = np.random.uniform(0, 1, 1000)
    bins = tools.make_bins(data, bin_size=bin_size)
    real_bin_size = bins[1] - bins[0]
    for idx in range(len(bins) - 1):
        assert bins[idx+1] - bins[idx] == approx(real_bin_size)


#-------------------------------------------------------------------------------

# Testing the unique_total

#-------------------------------------------------------------------------------
def test_unique_total_error_checking_types_string():
    with pytest.raises(TypeError):
        tools._unique_total_sorted("hello")


def test_unique_total_error_checking_types_string_array():
    with pytest.raises(TypeError):
        tools._unique_total_sorted([1, 2, 3, "b"])


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


#-------------------------------------------------------------------------------

# Testing the level that contains certain percentages

#-------------------------------------------------------------------------------
def test_percentile_level_error_checking_positive_density():
    with pytest.raises(ValueError):
        tools.percentile_level([-1, 0, 1, 2, 3], 0.5)


def test_percentile_level_error_checking_no_negative_percentile():
    with pytest.raises(ValueError):
        tools.percentile_level([1, 2, 3], [-1, 0, 0.5])


def test_percentile_level_error_checking_no_greater_percent_than_one():
    with pytest.raises(ValueError):
        tools.percentile_level([1, 2, 3], [0, 0.35, 0.7, 1.002])


def test_percentile_level_error_checking_non_iterable_density():
    with pytest.raises(TypeError):
        tools.percentile_level(1, 0.5)


def test_percentile_level_error_checking_empty_list():
    with pytest.raises(ValueError):
        tools.percentile_level([], 0.3)


def test_percentile_level_error_checking_no_multi_dimension_density():
    density = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        tools.percentile_level(density, 0.5)


def test_percentile_level_list_vs_scalar_percentile():
    """A single item list should be treated the same as a scaler for percent"""
    densities = np.random.uniform(0, 10, 100)
    level = 0.6
    scalar_value = tools.percentile_level(densities, level)
    list_value   = tools.percentile_level(densities, [level])
    assert approx(scalar_value) == approx(list_value)


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
    percentiles = [1, 24.0/25.0, 22.0/25.0, 19.0/25.0, 15.0/25.0, 10.0/25.0, 0]
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
    percentiles = [24.0/25.0, 22.0/25.0, 19.0/25.0, 15.0/25.0, 10.0/25.0, 0]
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
    percentages = np.arange(0.1, 1.0, 0.01) # 1 to 99 percent
    # the levels can be computed analytically, since this is a uniform
    # distribution. The level should be computed such that the integral of x
    # from l to 1 is some percentage of the total. This gives P = 1 - l^2
    real_levels = sorted(np.sqrt(1 - percentages))
    test_levels = tools.percentile_level(densities, percentages)
    assert real_levels == approx(test_levels, abs=1E-3)
    # need larger tolerance to account for the fact that our points are only
    # spaced 1E-3 apart.


def test_percentile_level_big_data_warnings(recwarn):
    # get a ton of data
    densities = np.linspace(0, 1, 1000)
    percentages = np.arange(0.1, 1.0, 0.01) # 1 to 99 percent
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
    have floating point errors. """
    data = [1, 1, 1, 1, 1, 1, 1, 1, 1,  # 9 total
            3, 3, 3,                    # 9 total
            9]                          # 9 total
    # here the 50th percentile (if cumulatively summing) is right in the middle
    # of the 3s. To get past 50 we do have to go below the threes
    assert 1.0 < tools.percentile_level(data, 0.5) < 3.0


def test_percentile_level_in_middle_of_constants_warning():
    """What happens when the correct level is hard to define, since there are
    a bunch of ones like it. When there is a big gap between what we have
    and what we want we raise an error also. """
    data = [1, 1, 1, 1, 1, 1, 1, 1, 1,  # 9 total
            3, 3, 3,                    # 9 total
            9]                          # 9 total
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


def percentile_level_not_aligned():
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
    percentiles = [0.45000, 0.45000001, 0.45000002, 0.45000003,
                   0.86000, 0.86000001, 0.86000002, 0.86000003]
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

