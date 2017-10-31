import pytest
import numpy as np
from betterplotlib import _tools

random_x = np.random.normal(0, 1, 1000)


# Freedman Diaconis bin size testing
def test_freedman_diaconis_zero_data():
    """Length of zero doesn't work in FD."""
    with pytest.raises(ValueError):
        _tools._freedman_diaconis_core(10, 0)


def test_freedman_diaconis_simple():
    """Some easy test cases for FD"""
    assert _tools._freedman_diaconis_core(1.0, 1.0) == 2.0
    assert _tools._freedman_diaconis_core(10.0, 1.0) == 20.0
    assert _tools._freedman_diaconis_core(1.0, 8.0) == 1.0
    assert _tools._freedman_diaconis_core(5.0, 8.0) == 5.0
    assert _tools._freedman_diaconis_core(6.0, 27.0) == 4.0


def test_round_to_nice_width_simple():
    assert np.isclose(_tools._round_to_nice_width(0.5), 0.5)
    assert np.isclose(_tools._round_to_nice_width(4), 5)
    assert np.isclose(_tools._round_to_nice_width(78), 100)


def test_round_to_nice_width_with_exp():
    """Want either 1, 2, 5, or 10 bins per 10 units. So we either round the
    bin to 10, 5, 2, or 1, respectively. """
    for exp in np.arange(-10.0, 10.0):
        factor = 10**exp
        assert np.isclose(_tools._round_to_nice_width(1.0 * factor),
                          1.0 * factor)
        assert np.isclose(_tools._round_to_nice_width(1.49999 * factor),
                          1.0 * factor)
        assert np.isclose(_tools._round_to_nice_width(1.50001 * factor),
                          2.0 * factor)
        assert np.isclose(_tools._round_to_nice_width(2.0 * factor),
                          2.0 * factor)
        assert np.isclose(_tools._round_to_nice_width(3.49999 * factor),
                          2.0 * factor)
        assert np.isclose(_tools._round_to_nice_width(3.50001 * factor),
                          5.0 * factor)
        assert np.isclose(_tools._round_to_nice_width(5.0 * factor),
                          5.0 * factor)
        assert np.isclose(_tools._round_to_nice_width(7.49999 * factor),
                          5.0 * factor)
        assert np.isclose(_tools._round_to_nice_width(7.50001 * factor),
                          10.0 * factor)
        assert np.isclose(_tools._round_to_nice_width(10.0 * factor),
                          10.0 * factor)
        assert np.isclose(_tools._round_to_nice_width(14.9999 * factor),
                          10.0 * factor)
        assert np.isclose(_tools._round_to_nice_width(15.0001 * factor),
                          20.0 * factor)


def test_binning_bin_size_error_checking_zero():
    with pytest.raises(ValueError):
        _tools._binning(1, 2, 0)


def test_binning_bin_size_error_checking_negative():
    with pytest.raises(ValueError):
        _tools._binning(1, 2, -1)


def test_binning_padding_error_checking():
    with pytest.raises(ValueError):
        _tools._binning(1, 2, 1, -1)


def test_binning_min_max_checking_not_ordered():
    with pytest.raises(ValueError):
        _tools._binning(1, 0, 1)


def test_binning_wrong_type_min():
    with pytest.raises(TypeError):
        _tools._binning("a", 0, 1)


def test_binning_wrong_type_max():
    with pytest.raises(TypeError):
        _tools._binning(1, "a", 1)


def test_binning_wrong_type_min_max():
    with pytest.raises(TypeError):
        _tools._binning("a", "b", 1)


def test_binning_wrong_type_bin_size():
    with pytest.raises(TypeError):
        _tools._binning(0, 1, "a")


def test_binning_wrong_type_padding():
    with pytest.raises(TypeError):
        _tools._binning(-1, 0, 1, "a")


def test_binning_positive_bin_aligned():
    assert np.allclose(_tools._binning(1.0, 2.0, 0.5),
                       [0.5, 1.0, 1.5, 2.0, 2.5])


def test_binning_negative_bin_aligned():
    assert np.allclose(_tools._binning(-2.0, -1.0, 0.5),
                       [-2.5, -2, -1.5, -1, -0.5])


def test_binning_zero_to_pos_bin_aligned():
    assert np.allclose(_tools._binning(0, 1, 0.5),
                       [-0.5, 0, 0.5, 1.0, 1.5])


def test_binning_neg_to_zero_bin_aligned():
    assert np.allclose(_tools._binning(-1, 0, 0.5),
                       [-1.5, -1, -0.5, 0, 0.5])


def test_binning_zero_to_pos_bin_aligned_b():
    assert np.allclose(_tools._binning(0.5, 1, 0.5),
                       [0, 0.5, 1.0, 1.5])


def test_binning_neg_to_zero_bin_aligned_b():
    assert np.allclose(_tools._binning(-1, -0.5, 0.5),
                       [-1.5, -1, -0.5, 0])


def test_binning_across_zero_bin_aligned():
    assert np.allclose(_tools._binning(-0.5, 1, 0.5),
                       [-1, -0.5, 0, 0.5, 1.0, 1.5])


def test_binning_across_zero_not_aligned():
    assert np.allclose(_tools._binning(-0.25, 0.25, 0.5),
                       [-0.5, 0, 0.5])


def test_binning_neg_to_zero_not_aligned():
    assert np.allclose(_tools._binning(-0.75, -0.25, 0.5),
                       [-1, -0.5, 0])


def test_binning_zero_to_pos_not_aligned():
    assert np.allclose(_tools._binning(0.25, 0.75, 0.5),
                       [0, 0.5, 1])


def test_binning_positive_not_aligned():
    assert np.allclose(_tools._binning(0.75, 1.25, 0.5),
                       [0.5, 1, 1.5])


def test_binning_negative_not_aligned():
    assert np.allclose(_tools._binning(-1.25, -0.75, 0.5),
                       [-1.5, -1, -0.5])


def test_binning_across_zero_many_bins_not_aligned():
    assert np.allclose(_tools._binning(-0.51, 0.61, 0.1),
                       [-0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3,
                        0.4, 0.5, 0.6, 0.7])


def test_binning_positive_many_bins_not_aligned():
    assert np.allclose(_tools._binning(0.51, 1.11, 0.1),
                       [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2])


def test_binning_negative_many_bins_not_aligned():
    assert np.allclose(_tools._binning(-1.31, -0.49, 0.1),
                       [-1.4, -1.3, -1.2, -1.1, -1, -0.9, -0.8, -0.7, -0.6,
                        -0.5, -0.4])


def test_binning_zero_to_pos_many_bins_not_aligned():
    assert np.allclose(_tools._binning(0.01, 0.51, 0.1),
                       [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])


def test_binning_neg_to_zero_many_bins_not_aligned():
    assert np.allclose(_tools._binning(-0.51, -0.01, 0.1),
                       [-0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0])


def test_binning_padding_positive_aligned():
    assert np.allclose(_tools._binning(5, 10, 1, 2),
                       [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])


def test_binning_padding_negative_aligned():
    assert np.allclose(_tools._binning(-1.0, -0.5, 0.1, 0.2),
                       [-1.3, -1.2, -1.1, -1, -0.9, -0.8, -0.7, -0.6, -0.5,
                        -0.4, -0.3, -0.2])


def test_binning_padding_positive_not_aligned():
    assert np.allclose(_tools._binning(0.5, 1.1, 0.2, 0.2),
                       [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4])


def test_binning_padding_negative_not_aligned():
    assert np.allclose(_tools._binning(-11, -5, 2, 2),
                       [-14, -12, -10, -8, -6, -4, -2])


def test_min_equal_max():
    assert np.allclose(_tools._binning(1, 1, 0.5),
                       [0.5, 1, 1.5])


def test_centers_simple_equal_spacing():
    assert np.allclose(_tools._centers([1, 2, 3, 4]),
                       [1.5, 2.5, 3.5])


def test_centers_not_equal_spacing():
    assert np.allclose(_tools._centers([1, 2, 3, 4, 6, 8, 10]),
                       [1.5, 2.5, 3.5, 5, 7, 9])


def test_centers_length():
    xs = np.arange(np.random.randint(10, 100, 1))
    assert len(xs) == len(_tools._centers(xs)) + 1

#-------------------------------------------------------------------------------

# Testing the parsing of the binning.
# We don't need to od a whole lot here, since most if it is taken care of by
# the binning function, which has been thoroughly tested above.

#-------------------------------------------------------------------------------

def test_parse_bin_size_scalar():
    assert _tools._parse_bin_size(0.1) == [0.1, 0.1]

def test_parse_bin_size_two_elt_array():
    assert _tools._parse_bin_size([0.1, 0.3]) == [0.1, 0.3]

def test_parse_bin_size_one_elt_array():
    assert _tools._parse_bin_size([0.4]) == [0.4, 0.4]

def test_parse_bin_size_more_elt_array():
    with pytest.raises(ValueError):
        _tools._parse_bin_size([0.4, 0.3, 0.1])

def test_parse_bin_size_zero_elt_array():
    with pytest.raises(ValueError):
        _tools._parse_bin_size([])

def test_parse_binning_options_core_all_specified():
    data = [1, 2]
    assert np.allclose(_tools._parse_binning_options(data, 0.5, 0),
                       [0.5, 1.0, 1.5, 2.0, 2.5])

def test_parse_binning_options_core_no_padding_specified():
    data = [1, 2]
    assert np.allclose(_tools._parse_binning_options(data, 0.5),
                       [0.5, 1.0, 1.5, 2.0, 2.5])

def test_parse_binning_options_core_no_bins_centering():
    data = [-2, -1, 0, 1, 2]
    bins = _tools._parse_binning_options(data)
    assert 0 in bins  # shows that we did indeed use the binning that centers
                      # around zero

def test_parse_binning_options_core_no_bins_rounding():
    data = [-2, -1, 0, 1, 2]
    bins = _tools._parse_binning_options(data)
    # make sure the bin size is rounded like we want.
    assert bins[1] - bins[0] in [0.1, 0.2, 0.5, 1.0, 2.0]

#-------------------------------------------------------------------------------

# Testing the level that contains certain percentages

#-------------------------------------------------------------------------------

def test_percentile_level_core_simple_a():
    densities = [1, 1, 2]
    assert 1 < _tools._percentile_level_core(densities, 0.5) < 2

def test_percentile_level_core_simple_b():
    densities = [1, 1, 2, 4]
    assert 2 < _tools._percentile_level_core(densities, 0.5) < 4

def test_percentile_level_core_simple_c():
    densities = [1, 1, 3, 3]
    assert 1 < _tools._percentile_level_core(densities, 0.75) < 3

def test_percentile_level_core_simple_d():
    densities = [1, 2, 3, 4, 5, 10]
    assert 1 < _tools._percentile_level_core(densities, 24.0/25.0) < 2
    assert 2 < _tools._percentile_level_core(densities, 22.0/25.0) < 3
    assert 3 < _tools._percentile_level_core(densities, 19.0/25.0) < 4
    assert 4 < _tools._percentile_level_core(densities, 15.0/25.0) < 5
    assert 5 < _tools._percentile_level_core(densities, 10.0/25.0) < 10

def test_percentile_level_values():
    densities = [1, 2, 3, 4, 5, 10]
    percentiles = [24.0/25.0, 22.0/25.0, 19.0/25.0, 15.0/25.0, 10.0/25.0]
    for _ in range(10):
        np.random.shuffle(percentiles)  # order of percentiles won't matter
        levels = _tools._percentile_level(densities, percentiles)
        assert 1 < levels[0] < 2
        assert 2 < levels[1] < 3
        assert 3 < levels[2] < 4
        assert 4 < levels[3] < 5
        assert 5 < levels[4] < 10
        assert 10 < levels[5]

def test_percentile_level_big_data():
    # get a ton of data
    densities = np.linspace(0, 1, 1000)
    percentages = np.arange(0.90, -0.01, -0.1) # 0 to 90 percent
    # the levels can be computed analytically, since this is a uniform
    # distribution. The level should be computer such that the integral of x
    # from l to 1 is some percentage of the total. This gives P = 1 - l^2
    levels = sorted(np.sqrt(1 - percentages))
    assert np.allclose(_tools._percentile_level(densities, percentages),
                       np.concatenate([levels, [1.0]]), atol=0.02)
    # need larger tolerance for random, need to add extra for center point