import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy import ndimage
import warnings

# TODO: I need to remake the plt.gca() function to find my Axes_bpl


def _get_ax(**kwargs):
    """
    Get an axis object to plot stuff on.

    This will take the axis from kwargs if the user specified `ax`. If not, it
    will get the current axis, as defined by matplotlib. That may be a
    crapshoot if there are multiple axes, I don't know.

    This function is to be used in the rest of my functions, where we need
    to get an axis.

    :param kwargs: keyword arguments from whatever function call this is used
                   in.
    :return: the axes object. If `ax` is in kwargs, they will be changed
             (since `ax` will be removed), but it is modified in place, and
             any changes will be reflected in the original one too.
    """
    if "ax" in kwargs:
        ax = kwargs.pop("ax")
    else:
        ax = plt.gca(projection="bpl")
    return ax, kwargs


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
    """
    return _freedman_diaconis_core(stats.iqr(data), len(data))


def _freedman_diaconis_core(iqr, n):
    """
    This uses the Freedman Diaconis Algorithm, which is defined by

    .. math:
        h = 2 * IQR * n^{-1/3}

    where IQR is the interquartile range, n is the number of data points, and
    h is the bin size.
    """
    if n <= 0:
        raise ValueError("The number of data points must be positive in "
                         "Freedman Diaconis binning.")
    if iqr <= 0.0:
        raise ValueError("The Freeman-Diaconis binning relies on interquartile"
                         "range, and your data has zero. \nTry passing your"
                         "own bin size.")
    try:
        return 2 * iqr * n ** (-1.0 / 3.0)
    except TypeError:
        raise TypeError("Binning only works for float-like data types.")


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
    # we want to have it choose among the best of certain bins. We first
    # define the bins we want it to be able to choose. We make them all
    # multiples of 10^n, where n is the rounded log of the bin width. This
    # makes them be in the same order of magnitude as the original bin size.
    exponent = np.floor(np.log10(bin_width))
    raise_later = False  # have weird error checking to handle here.
    try:
        if np.isnan(exponent) or np.isinf(exponent):
            # This will raise a Value error if we try it on a list, but we want
            # to raise a value error if these things are true, so we have to
            # raise them outside of the try/except.
            raise_later=True
    except ValueError:
        raise TypeError("Float-like types are needed in this function.")
    if raise_later:
        raise ValueError("Bin width must be positive.")

    possible_bins = [x * 10 ** exponent for x in [1, 2, 5, 10]]
    # include 10 to give the full range from low to high that this bin can go to

    # we then figure out which one is closest to the original
    bin_diffs = [abs(bin_width - pos_width) for pos_width in possible_bins]
    best_idx = np.argmin(bin_diffs)
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
    :type data: list
    :return: Appproximately correct bin size.
    :rtype: float
    """
    return _round_to_nice_width(_freedman_diaconis(data))


def _binning(min, max, bin_size, padding=0):
    """
    Creates smarter bins for the histogram function.

    The default binning often makes bins of very strange size, that don't
    align well with integer values of the x-axis, making interpretation hard.
    This uses the minimum and maximum of the data, along with the specified
    bin size, to create bin boundaries that are integer multiples of the
    bin size away from zero. This makes histogram bins look prettier, and
    it helps when looking at them, especially something that is symmetric
    about zero.

    :param data: List of data that will be placed in the histogram.
    :param bin_size: Width of bins along the x-axis.
    :param padding: How much padding in will be done around the edges
                    of the min and max values. This is not normally needed, but
                    can be useful in smoothed contour plots when the contours
                    should extend past the maximal range of the data.
    :return: numpy array, where each value in the array is a bin boundary.
    """
    try:
        if bin_size <= 0:
            raise ValueError("Bin size must be positive.")
    except TypeError:
        raise TypeError("Bin size must be a numerical value.")
    try:
        if padding < 0:
            raise ValueError("Padding must be non-negative.")
    except TypeError:
        raise TypeError("Padding must be a numerical value.")
    try:
        _ = min > 0  # just for checking if both are not numerical
        if min > max:
            raise ValueError("Min must be smaller than max.")
    except TypeError:
        raise TypeError("Min and max must be numerical values.")


    # first get a rough estimate of the number of bins needed to get to the
    # min and max
    lower_multiples = (min - padding) // bin_size
    upper_multiples = (max + padding) // bin_size + 1
    # we add one to go the next bin (since it's floor divide).

    # we need to move the lower bin down one if the min value lands exactly on
    # a bin edge. We do this to avoid floating point errors that might move
    # our point outside the bin.
    if np.isclose(np.mod((min - padding), bin_size), 0):
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
    :type edges: list
    :return: list of bin centers
    :rtype: list of float
    """
    if isinstance(edges, dict):
        raise TypeError("Edges have to be list-like.")
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
    :type data: list
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
    if bin_size is None:  # need to choose our own
        bin_size = rounded_bin_width(data)

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
            raise ValueError("A iterable must have length two.")
        elif len(item) == 2:
            return [item[0], item[1]]
        elif len(item) == 1:
            return [item[0], item[0]]
    except TypeError:  # will happen if scalar
        return [item, item]


def _make_density_contours(xs, ys, bin_size,
                           padding_x=0, padding_y=0, weights=None,
                           smoothing=0):
    """
    This is the underlying function that is used by the contour plots.

    This smartly makes a 2D histogram, which is what is passed on to the 
    contour functions. The user can specify the number of bins, the specific
    bin edges, or the bin_size. If either the number of bins or bin edges is 
    passed in, the `numpy.histogram2d()` function will use those in the way
    that it normally does. If `bin_size` is specified, then bins with that 
    size will span the entire data range. If nothing is specified, the code
    will use the Freedman Diaconis algorithm to find a roughly optimal bin
    size.

    :param xs: list of x values
    :type xs: list
    :param ys: list of y values
    :type ys: list
    :param bin_size: Size of the bins that will be used to make the 2D
                     histogram. Can either be a scalar, in which case the x and
                     y bin sizes will be the same, or a two element array,
                     where the first is x bin size, and the second is y bin size
    :param padding_x: How much extra space to extend the contours past the min
                      and max values on the x axis. This is useful for smoothed
                      contour plots, when the contours should extend past the
                      minimum and maximum data values.
    :type padding_y: float
    :param padding_y: Same as padding_x, but in the y axis.
    :type padding_y: float
    :param weights: List of weights to go into the underlying histogram
                    function. Should be the same length as xs and ys.
    :type weights: list
    :param smoothing: Optional parameter that will allow the contours to be
                      smoothed. Pass in a nonzero value, which will be the
                      standard deviation of the Gaussian kernel use to smooth
                      the histogram. When using this, often choosing smaller
                      bin sizes is advantageous to make a less grainy plot.
    :type smoothing: float
    :return: list of x center, list of y centers, and the 2d histogram values.
             These can be passed on to the contour functions.
    :rtype: tuple of list, list, np.array
    """
    # First get the bins we need. If the user did not specify any bins
    # this will take care of it.
    bin_size_x, bin_size_y = _two_item_list(bin_size)
    bins = [make_bins(xs, bin_size_x, padding_x),
            make_bins(ys, bin_size_y, padding_y)]

    # We can then use the bins to create the histogram
    hist, x_edges, y_edges = np.histogram2d(xs, ys, bins, weights=weights)

    # turn the bin edges into bin centers, since that's what matters
    x_centers = bin_centers(x_edges)
    y_centers = bin_centers(y_edges)

    # we need to transpose the histogram to get it to line up with the x, y
    hist = hist.transpose()

    if smoothing > 0:
        # TODO: fix this, both the bin size thing and the fact that its the
        # same in both dimensions.
        hist = ndimage.gaussian_filter(hist, smoothing / bin_size_x)

    return x_centers, y_centers, hist

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
    return unique_values * appearances


def _percentile_level_warning_uncertain(percent):
    """
    Create the warning message for when the percentile level is uncertain.

    This should be called whenever this message should be raised.

    :param percent: The percent (from 0 to 1) that is uncertain
    :type percent: float
    :return: None, but raises the warning
    """
    warning_msg = "Location of {:.2f}% is uncertain by more than 1%. \n" \
                  "Consider adding more data."
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
    :param percentages: The percentiles to calculate levels for. If 0.5 is used,
                       one of the values returned will be the level that
                       encloses 50% of the data.
    :return: The level that encloses `percentage` of the data.
    """
    densities = np.array(densities)
    total_mass = np.sum(densities)
    if len(densities.shape) > 1:
        raise ValueError("Density must be one dimensional.")
    if any(densities < 0):
        raise ValueError("Density must be non-negative.")
    # turn percentages into a list
    try:
        rtype = list
        percentages = list(percentages)
    except TypeError:  # happens if a float
        rtype = float
        percentages = list([percentages])
    # check tht percentages are in the right range.
    for p in percentages:
        if not 0.0 <= p <= 1.0:
            raise ValueError("percentages must be between 0 and 1.")

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
