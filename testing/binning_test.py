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