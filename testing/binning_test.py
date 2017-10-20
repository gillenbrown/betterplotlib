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

def test_round_to_nice_number_with_exp():
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

