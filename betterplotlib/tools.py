import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy import ndimage
import warnings
import numbers

from . import type_checking


def _alpha(n, threshold=30, scale=2000):
    """
    Calculate a rough guess for the best alpha value for a default scatterplot.

    This is calculated with the equation

    .. math::
        \\alpha = \\frac{0.99}{1 + \\frac{n}{\\text{scale}}}

    This is done so that is ranges from nearly 1 for small values of n to 0.01
    for very large datasets. Note that very large datasets should probably use
    a contour plot, but this is avaiable.

    :param n: Length of the dataset that will be plotted in the scatterplot.
    :type n: int
    :param threshold: For the size of the dataset below this, the points will
                      be 100% opaque.
    :param scale: Parameter in the function that determines the alpha value.
                  Defaults to 2000. The larger the value, the more opaque
                  points will be for a given n.
    :type scale: float
    :return: Guess at an alpha value for a scatterplot.
    :rtype: float

    """
    # error checking
    err_msg = "{} must be a numeric scalar."
    n = type_checking.numeric_scalar(n, err_msg.format("n"))
    threshold = type_checking.numeric_scalar(threshold, err_msg.format("threshold"))
    scale = type_checking.numeric_scalar(scale, err_msg.format("scale"))
    if n < threshold:
        return 1.0
    # turn scale into a float to make sure it still works in Python 2
    return 0.99 / (1.0 + (n / float(scale)))


# ------------------------------------------------------------------------------
#
# Bin sizing things
#
# ------------------------------------------------------------------------------
def _freedman_diaconis(data):
    """This uses the Freedman Diaconis Algorithm, which is defined by

    .. math:
        h = 2 * IQR * n^{-1/3}

    where IQR is the interquartile range, n is the number of data points, and
    h is the bin size.

    :param data: The list of data to calculate the bin size for
    :type data: list, ndarray
    :returns: the proper bin size
    :rtype: float
    """
    return _freedman_diaconis_core(stats.iqr(data), len(data))


def _freedman_diaconis_core(iqr, n):
    """
    This uses the Freedman Diaconis Algorithm, which is defined by

    .. math:
        h = 2 * IQR * n^{-1/3}

    where IQR is the interquartile range, n is the number of data points, and
    h is the bin size.

    :param iqr: the interquartile range of the data
    :type iqr: float
    :param n: the size of the dataset
    :type n: float:
    :return: the proper bin size
    :rtype: float
    """
    n = type_checking.numeric_scalar(n, "n must be a numeric scalar.")
    iqr = type_checking.numeric_scalar(iqr, "iqr must be a numeric scalar.")

    if n <= 0:
        raise ValueError(
            "The number of data points must be positive in "
            "Freedman Diaconis binning."
        )
    if iqr <= 0.0:
        raise ValueError(
            "The Freeman-Diaconis default binning relies on "
            "inter-quartile range, and your data has zero."
            "\nTry passing your own bin size."
        )
    return 2 * iqr * n ** (-1.0 / 3.0)


def _round_to_nice_width(bin_width):
    """
    Take a bin width and round it to something nice.

    This will round a bin width to be a factor of 10 times one of the following:
    1, 2, 5, or 10. These are roughly a factor of two apart from each other,
    and will result in the bins lining up evenly on the ticks marks of typical
    axes, since they divide evenly into ticks that a power of 10.

    Some examples:
    10 -> 10
    9 -> 10
    11 -> 10
    0.004 -> 0.005
    0.8 -> 1.0

    :param bin_width: Width of bin that will be rounded.
    :type bin_width: float
    :return: Rounded bin width, as described above.
    :rtype: float
    """
    bin_width = type_checking.numeric_scalar(
        bin_width, "Bin width must be a " "numeric scalar."
    )
    if bin_width <= 0:
        raise ValueError("Bin width must be positive.")
    # we want to have it choose among the best of certain bins. We first
    # define the bins we want it to be able to choose. We make them all
    # multiples of 10^n, where n is the rounded log of the bin width. This
    # makes them be in the same order of magnitude as the original bin size.
    exponent = np.floor(np.log10(bin_width))
    possible_bins = [x * 10**exponent for x in [1, 2, 5, 10]]
    # include 10 to give the full range from low to high that this bin can go to

    # we then figure out which one is closest to the original
    bin_diffs = [abs(bin_width - pos_width) for pos_width in possible_bins]
    best_idx = int(np.argmin(bin_diffs))
    # the indices are the same between the diffs and originals, so we know
    # which index to get.
    return possible_bins[best_idx]


def rounded_bin_width(data):
    """
    Gets a reasonable bin size, rounded so that it lines up with plot ticks.

    This starts by getting the bin size recommended by the Freedman Diaconis
    algorithm. This bin size is then rounded to the one closest to it among the
    possibilites, which are of the format [1, 2, 5, 10] * 10^n, where n
    is some integer. This has the effect of making the bin edges line up with
    the ticks that are automatically added to matplotlib plots. This makes
    the resulting histograms looks nicer, and still have reasonable bin sizes.

    :param data: Raw data that will be used to create the histogram.
    :type data: list, ndarray
    :return: Appproximately correct bin size.
    :rtype: float
    """
    data = type_checking.numeric_list_1d(
        data, "data must be a list of numeric" "values in `rounded_bin_width`."
    )
    return _round_to_nice_width(_freedman_diaconis(data))


def _binning(min_, max_, bin_size, padding=0):
    """
    Creates smarter bins for the histogram function.

    The default binning often makes bins of very strange size, that don't
    align well with integer values of the x-axis, making interpretation hard.
    This uses the minimum and maximum of the data, along with the specified
    bin size, to create bin boundaries that are integer multiples of the
    bin size away from zero. This makes histogram bins look prettier, and
    it helps when looking at them, especially something that is symmetric
    about zero.

    :param min_: Minimum value of the dataset.
    :type min_: float
    :param max_: Maximum value of the dataset.
    :type max_: float
    :param bin_size: Width of bins along the x-axis.
    :type bin_size: float
    :param padding: How much padding in will be done around the edges
                    of the min and max values. This is not normally needed, but
                    can be useful in smoothed contour plots when the contours
                    should extend past the maximal range of the data.
    :type padding: float
    :return: numpy array, where each value in the array is a bin boundary.
    :rtype: np.ndarray
    """
    msg = "{} must be a numerical value in `_binning`."
    min_ = type_checking.numeric_scalar(min_, msg.format("min"))
    max_ = type_checking.numeric_scalar(max_, msg.format("max"))
    bin_size = type_checking.numeric_scalar(bin_size, msg.format("bin_size"))
    padding = type_checking.numeric_scalar(padding, msg.format("padding"))
    if bin_size <= 0:
        raise ValueError("Bin size must be positive.")
    if padding < 0:
        raise ValueError("Padding must be non-negative.")
    if min_ > max_:
        raise ValueError("Min must be smaller than max.")

    # first get a rough estimate of the number of bins needed to get to the
    # min and max
    lower_multiples = (min_ - padding) // bin_size
    upper_multiples = (max_ + padding) // bin_size + 1
    # we add one to go the next bin (since it's floor divide).

    # we need to move the lower bin down one if the min value lands exactly on
    # a bin edge. We do this to avoid floating point errors that might move
    # our point outside the bin.
    if np.isclose(np.mod((min_ - padding), bin_size), 0):
        lower_multiples -= 1

    # then turn these bin numbers into actual data limits for the lower and
    # upper edges of the bins
    lower_lim = lower_multiples * bin_size
    upper_lim = upper_multiples * bin_size + (bin_size / 2.0)
    # extra term to account for open interval in arange (next line)
    return np.arange(lower_lim, upper_lim, bin_size)


def bin_centers(edges):
    """
    This takes histogram edges and calculates the centers of each bin.

    All this does is take the average of each pair of edges.

    :param edges: List of edges of the bins of the histogram.
    :type edges: list, ndarray
    :return: list of bin centers
    :rtype: list of float
    """
    err_msg = "Edges have to be numeric list-like."
    if isinstance(edges, numbers.Real):
        raise TypeError(err_msg)
    try:
        edges = type_checking.numeric_list_1d(edges, err_msg)
    except TypeError:
        raise TypeError(err_msg)
    if len(edges) < 2:
        raise ValueError("Need at least two edges to calculate centers.")

    centers = []
    for left_edge_idx in range(len(edges) - 1):
        # average the left and right edges
        centers.append((edges[left_edge_idx] + edges[left_edge_idx + 1]) / 2.0)
    return centers


def make_bins(data, bin_size=None, padding=0):
    """
    Takes the user options and creates bins out of them.

    :param data: List of data values that will be binned.
    :type data: list, ndarray
    :param bin_size: Size of bins. If not passed in one will be chosen. We will
                     use the Freedman-Diaconis bin width, but round it so that
                     the edges line up with ticks
    :type bin_size: float
    :param padding: How much space to give on each side of the min and max. See
                    the `_binning()` function for more info.
    :type padding: float
    :return: List of bin edges.
    :rtype: np.ndarray
    """
    msg = "{} must be a {} in `make_bins`."
    data = type_checking.numeric_list_1d(data, msg.format("data", "list"))
    if len(data) == 0:
        raise ValueError("Empty list is not valid for data.")
    if bin_size is None:  # need to choose our own
        bin_size = rounded_bin_width(data)
    bin_size = type_checking.numeric_scalar(bin_size, msg.format("bin_size", "scalar"))
    padding = type_checking.numeric_scalar(padding, msg.format("padding", "scalar"))

    return _binning(min(data), max(data), bin_size, padding)


def _two_item_list(item):
    """
    Will return a two element list from either a scalar or two element list.

    If a scalar is passed in, it will be duplicated, and both items of the
    returned list will be this value. If an iterable is passed in, it must have
    one or two elements. A one element list will be treated like a scalar, while
    a two item list will be returned without modification.

    :param item: Either a scalar or list, as described above.
    :return: Two item list as described above.
    :rtype: list
    """
    try:
        if len(item) > 2 or len(item) == 0:
            raise ValueError("An iterable must have length two.")
        elif len(item) == 2:
            return [item[0], item[1]]
        elif len(item) == 1:
            return [item[0], item[0]]
    except TypeError:  # will happen if scalar
        return [item, item]


def _smart_hist_2d_error_checking(xs, ys, log, bin_size, padding, weights, smoothing):
    """
    Does the error checking for the _smart_hist_2d function.

    All parameters the same as for that function.
    """
    msg = "{} must be a numerical array."
    xs = type_checking.numeric_list_1d(xs, msg.format("x"))
    ys = type_checking.numeric_list_1d(ys, msg.format("y"))
    if len(xs) != len(ys):
        raise ValueError("x and y data must be the same length.")

    if weights is not None:
        weights = type_checking.numeric_list_1d(weights, msg.format("Weights"))
        if len(weights) != len(xs):
            raise ValueError("Weights and data need to have the same length.")
        if not all(weights >= 0):
            raise ValueError("Weights must be non-negative.")

    # parse the bin size options, then error check them.
    two_elt_msg = "{} must be either a scalar or two element numeric list."
    try:
        bin_size_x, bin_size_y = _two_item_list(bin_size)
    except ValueError:
        raise ValueError(two_elt_msg.format("Bin_size"))
    if bin_size is not None:
        type_checking.numeric_scalar(bin_size_x, two_elt_msg.format("Bin_size"))
        type_checking.numeric_scalar(bin_size_y, two_elt_msg.format("Bin_size"))

    # parse the log options
    try:
        log_x, log_y = _two_item_list(log)
    except ValueError:
        raise ValueError(two_elt_msg.format("log"))
    if log_x not in [True, False] or log_y not in [True, False]:
        raise TypeError("log must be True or False")

    # then do the same with the padding
    try:
        padding_x, padding_y = _two_item_list(padding)
    except ValueError:
        raise ValueError(two_elt_msg.format("Padding"))
    type_checking.numeric_scalar(padding_x, two_elt_msg.format("Padding"))
    type_checking.numeric_scalar(padding_y, two_elt_msg.format("Padding"))

    # and lastly with smoothing
    try:
        smoothing_x, smoothing_y = _two_item_list(smoothing)
    except ValueError:
        raise ValueError(two_elt_msg.format("Smoothing"))
    type_checking.numeric_scalar(smoothing_x, two_elt_msg.format("Smoothing"))
    type_checking.numeric_scalar(smoothing_y, two_elt_msg.format("Smoothing"))
    # smoothing must be positive, too
    if smoothing_x < 0 or smoothing_y < 0:
        raise ValueError("Smoothing must be nonnegative.")

    return (
        xs,
        ys,
        log_x,
        log_y,
        bin_size_x,
        bin_size_y,
        padding_x,
        padding_y,
        weights,
        smoothing_x,
        smoothing_y,
    )


def smart_hist_2d(
    xs, ys, bin_size=None, padding=0, weights=None, smoothing=0, log=False
):
    """
    Makes a 2D histogram, with smart choices made if nothing is passed in.

    Can also do smoothing of the underlying histogram data.

    :param xs: list of x values
    :type xs: list, ndarray
    :param ys: list of y values
    :type ys: list, ndarray
    :param bin_size: Bin size to use for the underlying 2D histogram. This
                     can either be a scalar, in which case the bin size will
                     be the same in both the x dimensions, or else a two
                     element list, where the first element will be the
                     bin size in the x dimension, and the second will be
                     the bin size in the y dimension.
    :type bin_size: int, float, list
    :param padding: How much extra space to extend the contours past the min
                    and max values on the x axis. This is useful for smoothed
                    contour plots, when the contours should extend past the
                    minimum and maximum data values. This has the same format
                    as bin_size.
    :type padding: int, float, list
    :param weights: A list containing weights for each data point. If these
                    are not passed, all data points will be weighted
                    equally.
    :type weights: list, np.ndarray
    :param smoothing: Optional parameter that will allow the contours to be
                      smoothed. Pass in a nonzero value, which will be the
                      standard deviation of the Gaussian kernel use to smooth
                      the histogram. When using this, often choosing smaller
                      bin sizes is advantageous to make a less grainy plot.
                      Has the same format as padding and bin_size, so different
                      smoothing kernels are possible in the x and y directions.
    :type smoothing: int, float, list
    :param log: Whether or not to do the smoothing and bin creation in log
                space. Can either be a single bool, in which case the x and y scales
                will be the same, or a two element array, where the first is whether
                the x axis is log, and the second is y. This should be used if the
                plot will be done on log-scaled axes. If this is used, the bin_size
                and smoothing parameters will be interpreted as dex, rather than
                raw values.
    :type log: bool, list
    :return: the 2d histogram values, list of x bin edges, list of y bin edges.
             These can be passed on to the contour functions after turning bin
             edges into bin centers. The first index into this array sets the
             y value, then the second index sets the x value. So it is row then
             column.
    :rtype: tuple of np.array, list, list
    """
    # error checking and data wrangling.
    validated_params = _smart_hist_2d_error_checking(
        xs, ys, log, bin_size, padding, weights, smoothing
    )
    xs, ys = validated_params[0:2]
    log_x, log_y = validated_params[2:4]
    bin_size_x, bin_size_y = validated_params[4:6]
    padding_x, padding_y = validated_params[6:8]
    weights = validated_params[8]
    smoothing_x, smoothing_y = validated_params[9:]

    # if the user wants log, do that
    if log_x:
        xs = np.log10(xs)
    if log_y:
        ys = np.log10(ys)

    # then we can go ahead and make the bin edges using this data
    bin_edges = [
        make_bins(xs, bin_size_x, padding_x),
        make_bins(ys, bin_size_y, padding_y),
    ]

    # get the actual bin size used
    bin_size_x = bin_edges[0][1] - bin_edges[0][0]
    bin_size_y = bin_edges[1][1] - bin_edges[1][0]

    # We can then use the bins to create the histogram
    hist, x_edges, y_edges = np.histogram2d(xs, ys, bin_edges, weights=weights)

    # if the user wants to smooth, do that.
    if smoothing_x > 0 or smoothing_y > 0:
        kernel_x = smoothing_x / bin_size_x
        kernel_y = smoothing_y / bin_size_y
        hist = ndimage.gaussian_filter(hist, [kernel_x, kernel_y])

    # we need to transpose the histogram to get it to line up with the x, y
    # used in other plotting functions.
    hist = hist.transpose()

    # if we have something in log, we need to turn it back into regular space
    if log_x:
        x_edges = 10**x_edges
    if log_y:
        y_edges = 10**y_edges

    return hist, x_edges, y_edges


def _unique_total_sorted(values):
    """
    Returns a list of the unique values in a list, weighted by the number of
    times they appear in the original list. This is basically the "mass" held
    at this value.

    Some examples will be the best way to explain it. Each value in the return
    list contains the sum of all the duplicates of that item. So if there are
    3 7s in the array, one item will be 21. The list will be sorted in order
    of the unique values.
    [1] -> [1]
    [1, 1] -> [2]  # two ones
    [1, 2, 3] -> [1, 2, 3]
    [1, 1, 2, 3] -> [2, 2, 3]  # two ones
    [1, 1, 1, 2, 2, 3] -> [3, 4, 3]  # three ones, two twos, one three
    [3, 2, 3, 1] -> [1, 2, 3]  # sorted, with two threes

    :param values: List of values to sort and find uniques of. Scalars and
                   empty lists are allowed, but only lists that contain
                   numerical data otherwise.
    :return: Sorted list of unique values in the list, weighted by the number
             of time that it appears in the array.
    :rtype: np.ndarray
    """
    unique_values, appearances = np.unique(values, return_counts=True)
    try:
        return unique_values * appearances
    except TypeError:
        raise TypeError("Need an array in `unique_total_sorted`.")


def _percentile_level_warning_uncertain(percent):
    """
    Create the warning message for when the percentile level is uncertain.

    This should be called whenever this message should be raised.

    :param percent: The percent (from 0 to 1) that is uncertain
    :type percent: float
    :return: None, but raises the warning
    """
    warning_msg = (
        "Location of {:.2f}% is uncertain by more than 1%. \n"
        "Consider adding more data, smoothing, or "
        "increasing the bin size."
    )
    warnings.warn(warning_msg.format(percent * 100), RuntimeWarning)


def _percentile_level_duplicate_checking(results_dict):
    """
    Check if there are any percentages that correspond to the same level.

    :param results_dict: Dictionary from the percentile_level function,
                         containing keys that are the percentages, and values
                         that are the corresponding level.
    :return: None, but raises warnings if there are duplicate levels.
    """
    unique_values = set(results_dict.values())
    # see if any of these values have more than one key with them.
    for val in unique_values:
        duplicate_keys = []
        for key in results_dict:
            if results_dict[key] == val:
                duplicate_keys.append(key)
        # there will be always one key that matches a value, but we care when
        # there are more than one.
        warn_message = "The percentiles {} all have the same level."
        if len(duplicate_keys) > 1:
            warnings.warn(warn_message.format(duplicate_keys), RuntimeWarning)


def percentile_level(densities, percentages):
    """
    Calculates the level of density that encloses X percent of the data.

    More specifically, this calculates the value of density at which X
    percent of the "mass" is held in cells with a density of this level or
    higher. More simply, this is used to find the levels that enclose 50% of
    the data points when they are put into a density plot.

    Note that there will be a range of values that satisfy the condition
    that the sum of the densities above this value is the given percentage of
    the total. The allowable rangs is the range between the next value of
    density on either side, since going past that range would enclose a
    different set of cells and give a different enclosed density. Therefore
    you can only trust these results to that level.

    This will raise warnings if this range is more than 1% of the "mass", or
    if two or more of your percentages end up with the same levels. This can
    happen if you have a small number of data points and closely spaced
    percentages.

    :param densities: List of densities. This can be each cell in a 2D
                      histogram (most typically) or each bin in a 1D histogram.
                      This needs to be flattened, though, so it's just one
                      dimension.
    :type densities: list, ndarray
    :param percentages: The percentiles to calculate levels for. If 0.5 is used,
                       one of the values returned will be the level that
                       encloses 50% of the data.
    :type percentages: list, ndarray
    :return: The level that encloses `percentage` of the data.
    :rtype: float
    """
    msg = "{} in percentile_level must be array like."
    densities = type_checking.numeric_list_1d(densities, msg.format("densities"))
    if len(densities) == 0:
        raise ValueError("Empty density array not allowed")

    total_mass = np.sum(densities)
    if any(densities < 0):
        raise ValueError("Density must be non-negative.")
    # turn percentages into a list
    try:
        rtype = list
        percentages = list(percentages)
    except TypeError:  # happens if a float
        rtype = float
    percentages = type_checking.numeric_list_1d(percentages, msg.format("percentages"))

    # check tht percentages are in the right range.
    for p in percentages:
        if not 0.0 <= p <= 1.0:
            raise ValueError("Percentages must be between 0 and 1.")

    # the accumulated mass is the cumulative sum (starting from the highest
    # density point). We will get the array of values at each point first.
    densities_high_to_low = np.unique(densities)[::-1]
    densities_to_accumulate = _unique_total_sorted(densities)[::-1]
    accumulated_mass = np.cumsum(densities_to_accumulate)
    # then get the fraction of the mass that represents
    mass_fractions = accumulated_mass / total_mass

    return_values = dict()
    for percent in percentages:
        # check for percent of 0 and 100, which needs to be handled specially
        if percent == 0:
            return_values[percent] = 1.02 * densities_high_to_low[0]
            continue
        elif percent == 1:
            return_values[percent] = 0.98 * densities_high_to_low[-1]
            continue
        # find the index where we are closest to the desired percentage while
        # getting at least to the desired value.
        best_idx = np.argmax((mass_fractions - percent) >= 0)
        # this works because argmax will find the first value that has the
        # condition being true, which will be the first one over the threshold.

        # see if we need to raise a warning for uncertain levels.
        best_mass_frac = mass_fractions[best_idx]
        # don't raise a warning if we found the level exactly
        if not np.isclose(best_mass_frac, percent):
            if best_idx == 0:  # the first value went past our defined density
                # since the first value went past our threshold, we have no
                # idea where along this it happened, so we are uncertain
                _percentile_level_warning_uncertain(percent)
            else:  # not the first value
                # The criteris here will be that the gap between this level and
                # the one before it (which did not pass the threshold) is more
                # than 1%. This is a large region where the threshold could
                # have been passes
                next_mass_frac = mass_fractions[best_idx - 1]
                if best_mass_frac - next_mass_frac > 0.01:
                    _percentile_level_warning_uncertain(percent)

        # Get the return value. This is a bit subjective. It only has to be
        # higher then the level that encloses the correct percentage, since
        # we want to make sure that level is included. It also has to be
        # below the next density so we don't include too much. I'll take the
        # mean of the best value and the next lowest density, which satisfies
        # these conditions.
        value = densities_high_to_low[best_idx]
        # have to be careful when we have the last value, since there is no
        # next value to average with.
        if best_idx == len(densities_high_to_low) - 1:  # last value
            return_values[percent] = value * 0.99
            # just below the lowest density.
            continue
        next_value = densities_high_to_low[best_idx + 1]
        return_values[percent] = np.mean([value, next_value])

    # if the user pased in a float, then return a float only.
    if len(return_values) == 1 and rtype is float:
        return list(return_values.values())[0]  # complex, but just gets the val

    # check for duplicates
    _percentile_level_duplicate_checking(return_values)

    # else, want them sorted from low to high for ease of plotting in contours
    return sorted(list(return_values.values()))


def _padding_from_smoothing(smoothing):
    """
    If smoothing is desirec but padding is not specified, create the padding.

    This is useful because the smoothing will go past the edges of the original
    dataset, so we want to be able to see it. The default here is that the
    padding 5 times the smoothing kernel in each dimension. This might be a
    little big in some situations, but will ensure that the kernel dies off
    before we stop calculating it.

    :param smoothing: What the user passed in for the smoothing parameter in
                      one of the main functions. Will be either a scalar, one
                      element list, or two element list.
    :type smoothing: int, float, list
    :return: Two element list with the padding to be used for the 2D histogram.
    :rtype: list
    """
    # see if what they passed in is the proper shape
    msg = "Smoothing must be either a scalar or two element numeric list."
    try:
        smoothing_x, smoothing_y = _two_item_list(smoothing)
    except ValueError:
        raise ValueError(msg)

    # try convert to float. There is where we do the 5 times the smoothing.
    try:
        return [5 * float(smoothing_x), 5 * float(smoothing_y)]
    except ValueError:
        raise TypeError(msg)


def _outer_contours(paths):
    """
    Find outer polygons among a collection of them.

    :param paths: List of matplotlib path objects that come from contours. These
                  are assumed to be closed and not overlapping. These will not
                  be checked, so know what you are pasing in here.
    :type paths: list of matplotlib.path.Path
    :return: The outermost contours. There can be multiple of these if they are
             distinct regions.
    :rtype: list of matplotlib.path.Path
    """
    outer_polygons = []
    for potential_outer in paths:
        ever_contained = False
        # see if any other shapes contain this one.
        for other_polygon in paths:
            if other_polygon.contains_path(potential_outer):
                ever_contained = True
        # if none other ones contain it, then it's an outer one.
        if not ever_contained:
            outer_polygons.append(potential_outer)
    return outer_polygons
