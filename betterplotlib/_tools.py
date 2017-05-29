import matplotlib.pyplot as plt
import numpy as np
import sys

from . import colors

#TODO: I need to remake the plt.gca() function to find my Axes_bpl

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
    return 0.99 / (1.0 + (n / float(scale)))  # turn scale into a float to make
                                              # sure it still works in Python 2


def _freedman_diaconis(data):
    """
    This stats by using the Freedman Diaconis Algorithm, which is defined by

    .. math:
        h = 2 * IQR * n^{-1/3}

    where IQR is the interquartile range, n is the number of data poings, and
    h is the bin size.
    """
    # To use the Freedman Diaconis rule, we need to calculate the inter 
    # quartile range, which is the distance between the 25th and 75th 
    # percentiles.
    iqr = np.percentile(data, 75) - np.percentile(data, 25)
    # then we can use the rule.
    return 2 * iqr * len(data) **(-1.0/3.0)


def _rounded_bin_width(data):
    """
    Gets a reasonable bin size, rounded so that it lines up with plot ticks.

    This starts by getting the bin size recommended by the Freedman Diaconis 
    algorithm. This bin size is then rounded to the one closest to it among the 
    possibilites, which are of the format [1, 2, 4, 5, 10] * 10^n, where n 
    is some integer. This has the effect of making the bin edges line up with
    the ticks that are automatically added to matplotlib plots. This makes 
    the resulting histograms looks nicer, and still have reasonable bin sizes.

    :param data: Raw data that will be used to create the histogram.
    :type data: list
    :return: Appproximately correct bin size.
    :rtype: float
    """
    fd_bin_width = _freedman_diaconis(data)

    # we then want to have it choose among the best of certain bins. We first
    # define the bins we want it to be able to choose. We make them all 
    # multiples of 10^n, where n is the rounded log of the bin width. This 
    # makes them be in the same order of magnitude as the original bin size.
    exponent = np.floor(np.log10(fd_bin_width))
    possible_bins = [x * 10**exponent for x in [1, 2, 4, 5, 10]]

    # we then figure out which one is closest to the original
    bin_diffs = [abs(fd_bin_width - pos_width) for pos_width in possible_bins]
    best_idx = bin_diffs.index(min(bin_diffs))
    # the indices are the same between the diffs and originals, so we know 
    # which index to get.
    return possible_bins[best_idx]


def _binning(data, bin_size):
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
    :return: numpy array, where each value in the array is a bin boundary.
    """

    lower_multiples = min(data) // bin_size
    upper_multiples = max(data) // bin_size

    upper_multiples += 1  # to round up, rather than down

    lower_lim = lower_multiples * bin_size
    upper_lim = upper_multiples * bin_size + (bin_size / 2.0)
    # to account for open interval

    return np.arange(lower_lim, upper_lim, bin_size)


def _centers(edges):
    """
    This takes histogram edges and calculates the centers of each bin.

    All this does is take the average of each pair of edges.

    :param edges: List of edges of the bins of the histogram.
    :type edges: list
    :return: list of bin centers
    :rtype: list of float
    """
    centers = []
    for left_edge_idx in range(len(edges) - 1):
        # average the left and right edges
        centers.append((edges[left_edge_idx] + edges[left_edge_idx + 1]) / 2.0)
    return centers


def _make_density_contours(xs, ys, bin_size=None, bins=None):
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
    :param bins: Same as for `np.histogram2d()`. Can either be a number, a 
                 tuple of two numbers, a single list, or a tuple with two lists.
                 If it one or two numbers, this will be the number of bins.
                 Lists of numbers will be the bin edges. If only one number
                 or list is passed in, it will be used for both x and y. If a 
                 tuple of two lists or numbers is passed in, the first will be 
                 used for x, the second for y.
    :param bin_size: Size of the bins that will be used to make the 2D 
                     histogram. Can be either a number or a two element list, 
                     with bin sizes for x and y. 
    :type bin_size: float
    :return: list of x center, list of y centers, and the 2d histogram values.
             These can be passed on to the contour functions.
    :rtype: tuple of list, list, np.array
    """
    if bins is not None and bin_size is not None:
        raise ValueError("The `bins` and `bin_size` keywords cannot be "
                         "used together. Use `bins` if you want to "
                         "pass your own bins, or use `bin_size` to "
                         "have the code determine its own bins. ")
    elif (bin_size is not None) or (bin_size is None and bins is None):
        # if we got here, we need to make our own bins. If we don't know the 
        # bin size, find an "optimal" one.
        if bin_size is None:
            x_bin_size = _freedman_diaconis(xs)
            y_bin_size = _freedman_diaconis(ys)
        else:  # use the bin_size the user provided.
            # if we have a multiple element bin_size, then we can use that for
            # x and y
            try:
                x_bin_size = bin_size[0]
                if len(bin_size) != 2:
                    raise ValueError("bin_size needs to be either a scalar\n"
                                     "or a two element list.")
                y_bin_size = bin_size[1]
            except TypeError:
                # we only have a scalar, so use that for both x and y
                x_bin_size = bin_size
                y_bin_size = bin_size
        # then use that bin size to make the actual bins
        x_bins = _binning(xs, x_bin_size)
        y_bins = _binning(ys, y_bin_size)
        bins = [x_bins, y_bins]

        # we can use this directly in the 2D histogram function.
        hist, x_edges, y_edges = np.histogram2d(xs, ys, bins) 
    elif bins is not None:
        # the user gave us bins, so let numpy figure it out
        hist, x_edges, y_edges = np.histogram2d(xs, ys, bins)

    # turn the bin edges into bin centers, since that's what matters
    x_centers = _centers(x_edges)
    y_centers = _centers(y_edges)
    
    return x_centers, y_centers, hist.transpose()

# ==============================================================================

# Density Contour removed for now, but I didn't want to delete it.


# def density_contour(xs, ys, bin_size=None, ax=None, **kwargs):
#     """
#     Make a contour plot where the levels are based on the density of the points.

#     When a dataset is large, plotting a scatterplot often doesn't look good. 
#     This function makes a contour plot of the density of points, rather than
#     plotting the points themselves. 

#     Under the hood, this uses the `np.histogram2d()` function to create a 2D
#     histogram, which is then used to create the contours. 

#     You may be interested in the `contour_scatter()` function, too.

#     :param xs: list of x values
#     :type xs: list
#     :param ys: list of y values
#     :type ys: list
#     :param bin_size: Size of the bins used in the 2D histogram. This is kind
#                      of an arbitrary parameter. The code will guess a value for
#                      this if none is passed in, but this value isn't always 
#                      good. A smaller value gives noisier contours. A value that
#                      is too large will lead to "chunky" contours. Adjust this
#                      until your contours look good to your eye. That's the best
#                      way to pick a value for this parameter.
#     :type bin_size: float
#     :param ax: Axes object to plot on.
#     :param kwargs: Additional keyword arguments that will be passed on to the
#                    contour function.
#     :return: output of the `plt.contour()` function.

#     Future: ADD EXAMPLES!!!
#     """

#     if ax is None:
#         ax, _ = _get_ax()
    
#     # the other function does the hard work
#     x_centers, y_centers, hist = _make_density_contours(xs, ys, bin_size)
    
#     # then set some default parameters
#     kwargs.setdefault("linewidths", 2)
#     if "colors" not in kwargs:
#         kwargs.setdefault("cmap", "viridis")
    
#     # then we can plot
#     return ax.contour(x_centers, y_centers, hist, **kwargs)

# ==============================================================================
    
