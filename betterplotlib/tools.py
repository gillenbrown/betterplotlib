import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler
import numpy as np

from . import colors


def default_style():
    """
    Sets matplotlib parameters to make default plots prettier without effort.

    :return: None
    """

    mpl.rcParams['legend.scatterpoints'] = 1
    mpl.rcParams['savefig.format'] = 'pdf'
    mpl.rcParams['axes.formatter.useoffset'] = False
    # mpl.rcParams['figure.dpi'] = 200
    mpl.rcParams['figure.figsize'] = [10, 7]

    # Font options
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.sans-serif'] = 'Helvetica Neue'
    mpl.rcParams['font.weight'] = 'bold'
    mpl.rcParams['axes.labelweight'] = 'bold'
    mpl.rcParams['axes.titleweight'] = 'bold'
    mpl.rcParams['axes.titlesize'] = 16
    mpl.rcParams['font.size'] = 14
    mpl.rcParams['axes.labelsize'] = 14
    mpl.rcParams['xtick.labelsize'] = 12
    mpl.rcParams['ytick.labelsize'] = 12
    mpl.rcParams['legend.fontsize'] = 13

    # colors
    mpl.rcParams['patch.edgecolor'] = colors.almost_black
    mpl.rcParams['text.color'] = colors.almost_black
    mpl.rcParams['axes.edgecolor'] = colors.almost_black
    mpl.rcParams['axes.labelcolor'] = colors.almost_black
    mpl.rcParams['xtick.color'] = colors.almost_black
    mpl.rcParams['ytick.color'] = colors.almost_black
    mpl.rcParams['grid.color'] = colors.almost_black
    # I like my own color cycle based on one of the Tableu sets.
    mpl.rcParams['axes.prop_cycle'] = cycler("color", colors.color_cycle)

def presentation_style():
    """
    Same as default_style, but with larger text.

    Useful for powerpoint presentations where large font is nice.

    :return: None
    """

    mpl.rcParams['legend.scatterpoints'] = 1
    mpl.rcParams['savefig.format'] = 'pdf'
    mpl.rcParams['axes.formatter.useoffset'] = False
    # mpl.rcParams['figure.dpi'] = 200
    mpl.rcParams['figure.figsize'] = [10, 7]

    # Font options
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.sans-serif'] = 'Helvetica Neue'
    mpl.rcParams['font.weight'] = 'bold'
    mpl.rcParams['axes.labelweight'] = 'bold'
    mpl.rcParams['axes.titleweight'] = 'bold'
    mpl.rcParams['axes.titlesize'] = 20
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.labelsize'] = 18
    mpl.rcParams['xtick.labelsize'] = 16
    mpl.rcParams['ytick.labelsize'] = 16
    mpl.rcParams['legend.fontsize'] = 17

    # colors
    mpl.rcParams['patch.edgecolor'] = colors.almost_black
    mpl.rcParams['text.color'] = colors.almost_black
    mpl.rcParams['axes.edgecolor'] = colors.almost_black
    mpl.rcParams['axes.labelcolor'] = colors.almost_black
    mpl.rcParams['xtick.color'] = colors.almost_black
    mpl.rcParams['ytick.color'] = colors.almost_black
    mpl.rcParams['grid.color'] = colors.almost_black
    # I like my own color cycle based on one of the Tableu sets.
    mpl.rcParams['axes.prop_cycle'] = cycler("color", colors.color_cycle)


def white_style():
    """
    Sets a style good for presenting on dark backgrounds.

    This was designed to use for creating plots that will be used in
    PowerPoint slides with a dark background. The text is larger to make
    more viewable plots, as well.

    :return: None
    """

    mpl.rcParams['legend.scatterpoints'] = 1
    mpl.rcParams['savefig.format'] = 'pdf'
    mpl.rcParams['axes.formatter.useoffset'] = False
    # mpl.rcParams['figure.dpi'] = 200
    mpl.rcParams['figure.figsize'] = [10, 7]

    # Font options
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.sans-serif'] = 'Helvetica Neue'
    mpl.rcParams['font.weight'] = 'bold'
    mpl.rcParams['axes.labelweight'] = 'bold'
    mpl.rcParams['axes.titleweight'] = 'bold'
    mpl.rcParams['axes.titlesize'] = 20
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.labelsize'] = 18
    mpl.rcParams['xtick.labelsize'] = 16
    mpl.rcParams['ytick.labelsize'] = 16
    mpl.rcParams['legend.fontsize'] = 17

    # colors
    mpl.rcParams['patch.edgecolor'] = "w"
    mpl.rcParams['text.color'] = "w"
    mpl.rcParams['axes.edgecolor'] = "w"
    mpl.rcParams['axes.labelcolor'] = "w"
    mpl.rcParams['xtick.color'] = "w"
    mpl.rcParams['ytick.color'] = "w"
    mpl.rcParams['grid.color'] = "w"
    # I like my own color cycle based on one of the Tableu sets, but with
    # added colors in front that look better on dark backgrounds
    mpl.rcParams['axes.prop_cycle'] = cycler("color", ["w", "y"] +
                                             colors.color_cycle)


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
        ax = plt.gca()
    return ax, kwargs


def make_ax_dark(ax=None, minor_ticks=False):
    """Turns an axis into one with a dark background with white gridlines.

    When you pass any axis, it will turn it into one with a slightly light
    gray background, and with solid white gridlines. All the axes spines are
    removed (so there isn't any outline), and the ticks are removed too.

    This returns the same axis object back, but since it is modified in the
    function it isn't necessary. Just calling the function will turn it dark,
    you don't need to reassign the variable.

    :param ax: Axes object that will be made dark. This isn't necessary, as
               matplotlib can find the currectly active axis.
    :type ax: matplotlib.axes
    :param minor_ticks: Whether or not to add minor ticks. They will be
                        drawn as dotted lines, rather than solid lines in the
                        axes space.
    :type minor_ticks: bool
    :return: same axis object after being modified.

    Example:

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import matplotlib.pyplot as plt

        bpl.default_style()

        fig, (ax0, ax1) = plt.subplots(figsize=[12, 5], ncols=2)
        bpl.make_ax_dark(ax1)
        ax0.set_title("Regular")
        ax1.set_title("Dark")


    """
    if ax is None:
        ax, kwargs = _get_ax()

    ax.set_axis_bgcolor(colors.light_gray)
    ax.grid(which="major", color="w", linestyle="-", linewidth=0.5)
    if minor_ticks:
        ax.minorticks_on()
        ax.grid(which="minor", color="w", linestyle=":", linewidth=0.5)

    ax.set_axisbelow(True)  # moves gridlines below the points

    # remove all outer splines
    remove_spines(["left", "right", "top", "bottom"], ax)

    return ax

def _alpha(n, scale=2000):
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
    :param scale: Parameter in the function that determines the alpha value.
                  Defaults to 2000. The larger the value, the more opaque 
                  points will be for a given n.
    :type scale: float
    :return: Guess at an alpha value for a scatterplot.
    :rtype: float

    """

    return 0.99 / (1.0 + (n / float(scale)))  # turn scale into a float to make
                                              # sure it still works in Python 2


def scatter(*args, **kwargs):
    """
    Makes a scatter plot that looks nicer than the matplotlib default.

    The call works just like a call to plt.scatter. It will set a few default
    parameters, but anything you pass in will override the default parameters.
    This function also uses the color cycle, unlike the default scatter.

    It also automatically determines a guess at the proper alpha (transparency)
    of the points in the plot.

    NOTE: the `c` parameter tells just the facecolor of the points, while
    `color` specifies the whole color of the point, including the edge line
    color. This follows the default matplotlib scatter implementation.


    :param args: non-keyword arguments that will be passed on to the
                 plt.scatter function. These will typically be the x and y
                 lists.
    :keyword ax: Axes object to plot on.
    :type ax: matplotlib.axes
    :param kwargs: keyword arguments that will be passed on to plt.scatter.
    :return: the output of the plt.scatter call is returned directly.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np

        bpl.default_style()

        x1 = np.random.normal(0, scale=0.5, size=500)
        y1 = np.random.normal(0, scale=0.5, size=500)
        x2 = np.random.normal(0.5, scale=0.5, size=500)
        y2 = np.random.normal(0.5, scale=0.5, size=500)
        x3 = np.random.normal(1, scale=0.5, size=500)
        y3 = np.random.normal(1, scale=0.5, size=500)

        bpl.scatter(x1, y1)
        bpl.scatter(x2, y2)
        bpl.scatter(x3, y3)
    """

    ax, kwargs = _get_ax(**kwargs)

    # get the color, if it hasn't already been set.
    if 'color' not in kwargs and 'c' not in kwargs:
        # get the default color cycle, and get the next color.
        kwargs['c'] = ax._get_lines.prop_cycler.next()['color']

    # set other parameters, if they haven't been set already
    # I use setdefault to do that, which puts the values in if they don't
    # already exist, but won't overwrite anything.
    kwargs.setdefault('linewidth', 0.25)
    # use the function we defined above to get the proper alpha value.
    kwargs.setdefault('alpha', _alpha(len(args[0])))

    # edgecolor is a weird case, since it shouldn't be set if the user
    # specifies 'color', since that refers to the whole point, not just the
    # color of the point. It includes the edge color.
    if 'color' not in kwargs:
        kwargs.setdefault('edgecolor', colors.almost_black)

    return ax.scatter(*args, **kwargs)


def _bin_width(data):
    """
    Gets a reasonable bin size, rounded so that it lines up with plot ticks.

    This stats by using the Freedman Diaconis Algorithm, which is defined by

    .. math:
        h = 2 * IQR * n^{-1/3}

    where IQR is the interquartile range, n is the number of data poings, and
    h is the bin size.

    This bin size is then rounded to the one closest to it among the 
    possibilites, which are of the format [1, 2, 4, 5, 10] * 10^n, where n 
    is some integer. This has the effect of making the bin edges line up with
    the ticks that are automatically added to matplotlib plots. This makes 
    the resulting histograms looks nicer, and still have reasonable bin sizes.

    :param data: Raw data that will be used to create the histogram.
    :type data: list
    :return: Appproximately correct bin size.
    :rtype: float
    """

    # To use the Freedman Diaconis rule, we need to calculate the inter 
    # quartile range, which is the distance between the 25th and 75th 
    # percentiles.
    iqr = np.percentile(data, 75) - np.percentile(data, 25)
    # then we can use the rule.
    fd_bin_width = 2 * iqr * len(data) **(-1.0/3.0)

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


def hist(*args, **kwargs):
    """
    A better histogram function. Also supports relative frequency plots, bin
    size, and hatching better than the default matplotlib implementation.

    Everything is the same as the default matplotlib implementation, with the
    exception a few keyword parameters. `rel_freq` makes the histogram a
    relative frequency plot, `hatch` controls the hatching of the
    bars, and `bin_size` controls the width of each bin.

    :param args: non-keyword arguments that will be passed on to the
                 plt.hist() function. These will typically be the list of
                 values.
    :keyword rel_freq: Whether or not to plot the histogram as a relative
                       frequency histogram. Note that this plots the
                       relative frequency of each bin compared to the whole
                       sample. Even if your range excludes some of the data,
                       it will still be included in the relative frequency
                       calculation.
    :type rel_freq: bool
    :keyword hatch: Controls the hatch style of the bars. Must be one of the
                    following: '-', '|', '+', '/', '\\', 'x', '.', 'o', 'O',
                    '*'. You can also repeat a symbol as many times as you
                    want to get a denser pattern. The backslashes need twice
                    as many, since Python uses those as escapes. If you
                    don't include this keyword, the bars will not have
                    hatching.
    :type hatch: str
    :keyword bin_size: The width of the bins in the histogram. The bin
                       boundaries will start at zero, and will be integer
                       multiples of bin_size from there. Specify either this,
                       or bins, but not both.
    :type bin_size: float
    :keyword kwargs: additional controls that will be passed on through to the
                     plt.hist() function.
    :return: same output as plt.hist()

    Examples:

    The basic histogram should look nicer than the default histogram.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import matplotlib.pyplot as plt
        import numpy as np

        bpl.default_style()

        data = np.random.normal(0, 2, 10000)

        bpl.hist(data)

    There are also plenty of options that make other histograms look nice too.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import matplotlib.pyplot as plt
        import numpy as np

        bpl.default_style()

        data1 = np.random.normal(-6, 1, size=10000)
        data2 = np.random.normal(-2, 1, size=10000)
        data3 = np.random.normal(2, 1, size=10000)
        data4 = np.random.normal(6, 1, size=10000)
        bin_size = 0.5
        bpl.hist(data1, rel_freq=True, bin_size=bin_size)
        bpl.hist(data2, rel_freq=True, bin_size=bin_size, histtype="step", linewidth=5)
        bpl.hist(data3, rel_freq=True, bin_size=bin_size, histtype="stepfilled", hatch="o", alpha=0.8)
        bpl.hist(data4, rel_freq=True, bin_size=bin_size, histtype="step", hatch="x", linewidth=4)

        bpl.add_labels(y_label="Relative Frequency")

    Here is a demo of all the hatch styles. Repeat each symbol more for a
    denser pattern. I would only use hatching when using `histtype` as either
    `step` or `stepfilled`, since the bar borders on the regular histogram
    mess with the hatching.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import matplotlib.pyplot as plt
        import numpy as np

        bpl.default_style()

        data = np.random.uniform(0, 0.9, 10000)

        for hatch in ['-', '|', '+', '/', '\\\\', 'x', '.', 'o', 'O', '*']:
            bins = [min(data), max(data)]
            bpl.hist(data, histtype="stepfilled", hatch=hatch, bins=bins)
            data += 1

    If you specify histtype="step", the hatching is the same color as the
    rest of the bar.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import matplotlib.pyplot as plt
        import numpy as np

        bpl.default_style()

        data = np.random.uniform(0, 0.9, 10000)

        for hatch in ['-', '|', '+', '/', '\\\\', 'x', '.', 'o', 'O', '*']:
            bins = [min(data), max(data)]
            bpl.hist(data, histtype="step", hatch=hatch, bins=bins)
            data += 1
    """

    # TODO: Add documentatino for examples of bin_size
    ax, kwargs = _get_ax(**kwargs)

    # I like white as an edgecolor if we use bars.
    if "histtype" not in kwargs or kwargs["histtype"] != "step":
        kwargs.setdefault('edgecolor', 'white')

    # do the relative frequency business if we need to
    if kwargs.pop("rel_freq", False):
        # check that they didn't set weights, since that's what I'll change
        if "weights" in kwargs:
            raise ValueError("The `weights` keyword can't be used with "
                             "`rel_freq`, since `rel_freq` works by "
                             "modifying the weights.")
        # normed doesn't work either.
        if "normed" in kwargs and kwargs["normed"] is True:
            raise ValueError("Normed does not work properly with rel_freq.")

        # the data will be the first arg.
        data = args[0]
        # we weight each item by 1/total items.
        kwargs["weights"] = [1.0 / len(data)] * len(data)

    # get the hatch before passing the kwargs on
    hatch = kwargs.pop("hatch", None)

    # if they didn't specify the binning, use our binning
    if "bin_size" in kwargs and "bins" in kwargs:
        raise ValueError("The `bins` and `bin_size` keywords cannot be "
                         "used together. Use `bins` if you want to "
                         "pass your own bins, or use `bin_size` to "
                         "have the code determine its own bins. ")
    kwargs.setdefault("bin_size", _bin_width(args[0]))
    kwargs.setdefault("bins", _binning(args[0], kwargs.pop("bin_size")))

    # plot the histogram, and keep the results
    hist_results = ax.hist(*args, **kwargs)

    # set the hatch on the patch objects, which are the last thing in the
    # output of plt.hist()
    if hatch is not None:
        for patch in hist_results[2]:
            patch.set_hatch(hatch)

    return hist_results


def remove_spines(spines_to_remove, ax=None):
    """Remove spines from the axis.

    Spines are the lines on the side of the axes. In many situations, these
    are not needed, and are just junk. Calling this function will remove
    the specified spines from an axes object. Note that it does not remove
    the tick labels if they are visible for that axis.

    The axis will be modified in place, so there isn't a need to return the
    axis object, but you can keep it if you want.

    Note that this function can mess up if you call this function multiple
    times with the same axes object, due to the way matplotlib works under
    the hood. I haven't really tested it extensively (since I have never once
    wanted to call it more than once), but I think the last function call
    is the one that counts. Calling this multiple times on the same axes
    would be weird, though, since you can specify multiple axes in one call.
    If you really need to call it multiple times and it is breaking, let me
    know and I can try to fix it.

    :param spines_to_remove: List of the desired spines to remove. Can choose
                             from "all", "top", "bottom", "left", or "right".
    :type spines_to_remove: list
    :param ax: Axes object to remove the spines from. This isn't necessary, and
               can be left blank if you are willing to let matplotlib find
               the axis for you.
    :type ax: matplotlib.axes
    :return: the same axis object.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import matplotlib.pyplot as plt

        bpl.default_style()

        fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=[10, 5])

        ax0.plot([0, 1, 2], [0, 1, 2])
        ax1.plot([0, 1, 2], [0, 1, 2])

        bpl.remove_spines(["top", "right"], ax=ax0)
        bpl.remove_spines(["all"], ax=ax1)

        ax0.set_title("removed top/right spines")
        ax1.set_title("removed all spines")

    """
    # If they want to remove all spines, turn that into workable infomation
    if ax is None:
        ax, kwargs = _get_ax()

    spines_to_remove = set(spines_to_remove)  # to remove duplicates
    if "all" in spines_to_remove:
        spines_to_remove.remove("all")
        for spine in ["left", "right", "top", "bottom"]:
            spines_to_remove.add(spine)

    # remove the spines
    for spine in spines_to_remove:
        ax.spines[spine].set_visible(False)

    # remove the ticks that correspond the the splines removed
    remove_ticks(list(spines_to_remove), ax)

    return ax


def remove_ticks(ticks_to_remove, ax=None):
    """Removes ticks from the given locations.

    In some situations, ticks aren't needed or wanted. Note that this doesn't
    remove the spine itself, or the labels on that axis.

    Like most of these function, the axis is modified in place when the ticks
    are removed, so the axis object doesn't really need to be returned.

    :param ticks_to_remove: locations where ticks need to be removed from.
                            Pass in a list, and choose from: "all, "top",
                            "bottom", "left", or "right".
    :type ticks_to_remove: list
    :param ax: Axes object to remove ticks from. This can be ignored.
    :type ax: matplotlib.axes
    :return: axis object with the ticks removed.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import matplotlib.pyplot as plt

        bpl.default_style()

        fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=[10, 5])

        ax0.plot([0, 1, 2], [0, 1, 2])
        ax1.plot([0, 1, 2], [0, 1, 2])

        bpl.remove_ticks(["top", "right"], ax=ax0)
        bpl.remove_ticks(["all"], ax=ax1)

        ax0.set_title("removed top/right ticks")
        ax1.set_title("removed all ticks")
    """
    # TODO: doesn't work if they pass in a string, rather than a list
    if ax is None:
        ax, kwargs = _get_ax()

    # If they want to remove all spines, turn that into workable infomation
    ticks_to_remove = set(ticks_to_remove)  # to remove duplicates
    if "all" in ticks_to_remove:
        # have to do weirdness since its a set
        ticks_to_remove.remove("all")
        for tick in ["left", "right", "top", "bottom"]:
            ticks_to_remove.add(tick)

    # matplotlib only allows setting which axes the ticks are on, so figure
    # that out and set the ticks to only be on the desired axes.
    if "left" in ticks_to_remove and "right" in ticks_to_remove:
        ax.yaxis.set_ticks_position("none")
    elif "left" in ticks_to_remove:
        ax.yaxis.set_ticks_position("right")
    elif "right" in ticks_to_remove:
        ax.yaxis.set_ticks_position("left")

    if "top" in ticks_to_remove and "bottom" in ticks_to_remove:
        ax.xaxis.set_ticks_position("none")
    elif "top" in ticks_to_remove:
        ax.xaxis.set_ticks_position("bottom")
    elif "bottom" in ticks_to_remove:
        ax.xaxis.set_ticks_position("top")

    return ax


def remove_labels(labels_to_remove, ax=None):
    """
    Removes the laels and tick marks from an axis border.

    This is useful for making conceptual plots where the numbers on the axis
    don't matter.

    :param labels_to_remove: location of labels to remove. Pass in a list,
                             and choose from: "all, "top", 'bottom",
                             "left", or "right".
    :type labels_to_remove: list
    :param ax: Axes object to remove ticks from. This can be ignored.
    :type ax: matplotlib.axes
    :return: axis object with the labels removed.
    """

    # TODO: create example
    if ax is None:
        ax, kwargs = _get_ax()

    # If they want to remove all labels, turn that into workable infomation
    labels_to_remove = set(labels_to_remove)  # to remove duplicates
    if "all" in labels_to_remove:
        # have to do weirdness since its a set
        labels_to_remove.remove("all")
        for tick in ["left", "right", "top", "bottom"]:
            labels_to_remove.add(tick)

    # create a dictionary to record all the places the labels should be
    places = {"top": True,
              "bottom": True,
              "left": True,
              "right": True}

    for label in labels_to_remove:
        try:
            places[label] = False
        except KeyError:
            raise ValueError("You can only remove the `top`, `bottom`, "
                             "`left`, and `right` labels. ")

    ax.tick_params(labeltop=places["top"], labelbottom=places["bottom"],
                   labelleft=places["left"], labelright=places["right"])

    return ax


def legend(facecolor="None", *args, **kwargs):
    """Create a nice looking legend.

    Works by calling the ax.legend() function with the given args and kwargs.
    If some are not specified, they will be filled with values that make the
    legend look nice.

    :param facecolor: color of the background of the legend. There are two
                      default options: "light" and "dark". Light will be white,
                      and dark will be the same color as the dark ax. If any
                      other color is passed in, then that color will be the one
                      used. If nothing is passed in, the legend will be
                      transparent.
    :type facecolor: str
    :param args: non-keyword arguments passed on to the ax.legend() fuction.
    :keyword ax: Axes object to plot on.
    :type ax: matplotlib.axes
    :param kwargs: keyword arguments that will be passed on to the ax.legend()
                   function. This will be things like loc, and title, etc.
    :return: legend object returned by the ax.legend() function.

    The default legend is a transparent background with no border, like so.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import matplotlib.pyplot as plt
        import numpy as np

        bpl.default_style()

        x = np.arange(0, 5, 0.1)

        plt.plot(x, x, label="x")
        plt.plot(x, 2*x, label="2x")
        plt.plot(x, 3*x, label="3x")
        bpl.legend()

    The dark legend is designed for the dark axes in mind.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import matplotlib.pyplot as plt
        import numpy as np

        bpl.default_style()

        x = np.arange(0, 5, 0.1)

        plt.plot(x, x, label="x")
        plt.plot(x, 2*x, label="2x")
        plt.plot(x, 3*x, label="3x")
        bpl.make_ax_dark()
        bpl.legend("dark")

    That said, the other combinations look good too. I especially like the
    light legend on the dark background.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import matplotlib.pyplot as plt
        import numpy as np

        bpl.default_style()

        x = np.arange(0, 5, 0.1)

        fig, axs = plt.subplots(ncols=2, figsize=[10, 5])

        for ax in axs:
            ax.plot(x, x, label="x")
            ax.plot(x, 2*x, label="2x")
            ax.plot(x, 3*x, label="3x")

        ax0, ax1 = axs

        bpl.legend("dark", ax=ax0)
        bpl.make_ax_dark(ax1)
        bpl.legend("light", ax=ax1)


    You can still pass in any kwargs to the legend function you want.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import matplotlib.pyplot as plt
        import numpy as np

        bpl.default_style()

        x = np.arange(0, 5, 0.1)

        plt.plot(x, x, label="x")
        plt.plot(x, 2*x, label="2x")
        plt.plot(x, 3*x, label="3x")
        bpl.legend(fontsize=20, loc=6, title="Title")
    """

    ax, kwargs = _get_ax(**kwargs)

    kwargs.setdefault('loc', 0)
    if facecolor == "light":
        facecolor = "#FFFFFF"
    elif facecolor == "dark":
        facecolor = '#E5E5E5'
    # otherwise, make facecolor transparent
    else:
        facecolor = "None"

    # push the legend a little farther away from the edge.
    kwargs.setdefault('borderaxespad', 0.75)

    leg = ax.legend(*args, **kwargs)

    # TODO: set the fontsize of the title properly. The best way to do it is
    # probably to get the font from one of the other text objects, then
    # increment that slightly, then set the title's fontsize to be that.
    # the fontsize param doesn't change the title, so do that manually
    # title = legend.get_title()
    # title.set_fontsize(kwargs['fontsize'])

    # turn the background into whatever color it needs to be
    frame = leg.get_frame()
    frame.set_facecolor(facecolor)
    frame.set_linewidth(0)

    return leg


def equal_scale(ax=None):
    """ Makes the x and y axes have the same scale.

    Useful for plotting things like ra and dec, something with the same
    quantity on both axes, or anytime the x and y axis have the same scale.

    It's really one one command, but it's one I have a hard time remembering.

    :param ax: Axis to make equal scale.
    :type ax: matplotlib.axes
    :return: axis that was passed in. It is modified in place, though, so even
             if its result is not assigned to anything it will still work.
    """
    if ax is None:
        ax, kwargs = _get_ax()
    ax.set_aspect("equal", adjustable="box")
    return ax


def add_labels(x_label=None, y_label=None, title=None, *args, **kwargs):
    """
    Adds labels to the x and y axis, plus a title.

    Addition properties will be passed the all single label creations,
    so any properties will be applied to all. If you want the title to be
    different, for example, don't include it here.

    The axis can be passed in as a kwarg if desired.

    :param x_label: label for the x axis
    :type x_label: str
    :param y_label: label for the y axis
    :type y_label: str
    :param title: title for the given axis
    :type title: str
    :param args: additional properties that will be passed on to all the labels
                 you asked for.
    :keyword ax: Axes object to plot on.
    :type ax: matplotlib.axes
    :param kwargs: additional keyword arguments that will be passed on to
                   all the labels you make.
    :return: None
    """
    ax, kwargs = _get_ax(**kwargs)
    if x_label is not None:
        ax.set_xlabel(x_label, *args, **kwargs)
    if y_label is not None:
        ax.set_ylabel(y_label, *args, **kwargs)
    if title is not None:
        ax.set_title(title, *args, **kwargs)


def set_limits(x_min=None, x_max=None, y_min=None, y_max=None, **kwargs):
    """
    Set axes limits for both x and y axis at once.

    The ax can be passed in as a kwarg. Any additional kwargs will be passed
    on to the matplotlib functions that set the limits, so refer to that
    documentation to find the allowed parameters.

    :param x_min: minimum x value to be plotted
    :type x_min: int, float
    :param x_max: maximum x value to be plotted
    :type x_max: int, float
    :param y_min: minimum y value to be plotted
    :type y_min: int, float
    :param y_max: maximum y value to be plotted
    :type y_max: int, float
    :keyword ax: Axes object to plot on.
    :type ax: matplotlib.axes
    :param kwargs: Kwargs for the set_limits() functions. Can also include
                   the axis, with the ax keyword.
    :return: none.
    """

    ax, kwargs = _get_ax(**kwargs)
    # Any None values won't change the plot any.
    ax.set_xlim([x_min, x_max], **kwargs)
    ax.set_ylim([y_min, y_max], **kwargs)


def add_text(x, y, text, coords="data", **kwargs):
    """
    Adds text to the specified location. Allows for easy specification of
    the type of coordinates you are specifying.

    Matplotlib allows the text to be in data or axes coordinates, but it's
    hard to remember the command for that. This fixes that. The param
    `coords` takes care of that.

    The x and y locations can be specified in either data or axes coords.
    If data coords are used, the text is placed at that data point. If axes
    coords are used, the text is placed relative to the axes. (0,0) is the
    bottom left, (1,1) is the top right. Remember to use the
    horizontalalignment and verticalalignment parameters if it isn't quite in
    the spot you expect.

    Also consider using easy_add_text, which gives 9 possible location to
    add text with minimal consternation.

    :param x: x location of the text to be added.
    :type x: int, float
    :param y: y location of the text to be added.
    :type y: int, float
    :param text: text to be added
    :type text: str
    :param coords: type of coordinates. This parameter can be either 'data' or
                   'axes'. 'data' puts the text at that data point. 'axes' puts
                   the text in that location relative the axes. See above.
    :type coords: str
    :keyword ax: Axes to put the text on.
    :type ax: matplotlib.axes
    :param kwargs: any additional keyword arguments to pass on the text
                   function. Pass things you would pass to plt.text()
    :return: Same as output of plt.text().
    """

    # this function takes care of the transform keyword already, so don't
    # allow the user to specify it.
    if "transform" in kwargs:
        raise ValueError("add_text takes care of the transform for you when "
                         "you specify coords. \n"
                         "Don't specify transform in this function.")

    ax, kwargs = _get_ax(**kwargs)

    # set the proper coordinate transformation
    if coords == "data":
        transform = ax.transData
    elif coords == "axes":
        transform = ax.transAxes
    else:
        raise ValueError("`coords` must be either 'data' or 'axes'")
    # putting it in kwargs makes it easier to pass on.
    kwargs["transform"] = transform

    # add the text
    return ax.text(x, y, text, **kwargs)


def easy_add_text(text, location, **kwargs):
    """
    Adds text in common spots easily.

    This was inspired by the plt.legend() function and its loc parameter,
    which allows for easy placement of legends. This does a similar thing,
    but just for text.

    VERY IMPORTANT NOTE: Although this works similar to plt.legend()'s loc
    parameter, the numbering is NOT the same. My numbering is based on the
    keypad. 1 is in the bottom left, 5 in the center, and 9 in the top right.
    You can also specify words that tell the location.

    :param text: Text to add to the axes.
    :type text: str
    :param location: Location to add the text. This can be specified two
                     in two possible ways. You can pass an integer, which
                     puts the text at the location corresponding to that
                     number's location on a standard keyboard numpad.
                     You can also pass a string that describe the location.
                     'upper', 'center', and 'lower' describe the vertical
                     location, and 'left', 'center', and 'right' describe the
                     horizontal location. You need to specify vertical, then
                     horizontal, like 'upper right'. Note that 'center' is
                     the code for the center, not 'center center'.
    :type location: str, int
    :keyword ax: Axes object to put the text on.
    :type ax: matplotlib.axes
    :param kwargs: additional text parameters that will be passed on to the
                   plt.text() function. Note that this function controls the
                   x and y location, as well as the horizonatl and vertical
                   alignment, so do not pass those parameters.
    :return: Same as output of plt.text()

    Example:

    There are two ways to specify the location, and we will demo both.

    .. plot::
        :include-source:

        import matplotlib.pyplot as plt
        import betterplotlib as bpl

        bpl.default_style()

        bpl.easy_add_text("1", 1)
        bpl.easy_add_text("2", 2)
        bpl.easy_add_text("3", 3)
        bpl.easy_add_text("4", 4)
        bpl.easy_add_text("5", 5)
        bpl.easy_add_text("6", 6)
        bpl.easy_add_text("7", 7)
        bpl.easy_add_text("8", 8)
        bpl.easy_add_text("9", 9)

    .. plot::
        :include-source:

        import matplotlib.pyplot as plt
        import betterplotlib as bpl

        bpl.default_style()

        bpl.easy_add_text("upper left", "upper left")
        bpl.easy_add_text("upper center", "upper center")
        bpl.easy_add_text("upper right", "upper right")
        bpl.easy_add_text("center left", "center left")
        bpl.easy_add_text("center", "center")
        bpl.easy_add_text("center right", "center right")
        bpl.easy_add_text("lower left", "lower left")
        bpl.easy_add_text("lower center", "lower center")
        bpl.easy_add_text("lower right", "lower right")


    """
    # check that the user didn't specify parameters I want to control.
    if 'ha' in kwargs or 'va' in kwargs or 'horizontalalignment' in kwargs \
            or 'verticalalignment' in kwargs:
        raise ValueError("This function controls the alignment. Do not"
                         "pass it in.")

    # then check each different case, and set the parameters we want to use.
    if location == 1 or location == "lower left":
        x_value = 0.04
        y_value = 0.04
        kwargs['horizontalalignment'] = "left"
        kwargs['verticalalignment'] = "bottom"
    elif location == 2 or location == "lower center":
        x_value = 0.5
        y_value = 0.04
        kwargs['horizontalalignment'] = "center"
        kwargs['verticalalignment'] = "bottom"
    elif location == 3 or location == "lower right":
        x_value = 0.96
        y_value = 0.04
        kwargs['horizontalalignment'] = "right"
        kwargs['verticalalignment'] = "bottom"
    elif location == 4 or location == "center left":
        x_value = 0.04
        y_value = 0.5
        kwargs['horizontalalignment'] = "left"
        kwargs['verticalalignment'] = "center"
    elif location == 5 or location == "center":
        x_value = 0.5
        y_value = 0.5
        kwargs['horizontalalignment'] = "center"
        kwargs['verticalalignment'] = "center"
    elif location == 6 or location == "center right":
        x_value = 0.96
        y_value = 0.5
        kwargs['horizontalalignment'] = "right"
        kwargs['verticalalignment'] = "center"
    elif location == 7 or location == "upper left":
        x_value = 0.04
        y_value = 0.96
        kwargs['horizontalalignment'] = "left"
        kwargs['verticalalignment'] = "top"
    elif location == 8 or location == "upper center":
        x_value = 0.5
        y_value = 0.96
        kwargs['horizontalalignment'] = "center"
        kwargs['verticalalignment'] = "top"
    elif location == 9 or location == "upper right":
        x_value = 0.96
        y_value = 0.96
        kwargs['horizontalalignment'] = "right"
        kwargs['verticalalignment'] = "top"
    else:
        raise ValueError("loc was not specified properly.")

    # then add the text.
    return add_text(x_value, y_value, text, coords="axes", **kwargs)


def savefig(fig, *args, **kwargs):
    """
    Saves the figure with some sugar to make it better.

    Automatically saves as pdf if not specified. If it is specified to save
    as anything other than a pdf, it is saved with high dpi.

    :param fig: Figure to save
    :param kwargs: additional parameters that will be passed on to the
                   fig.savefig() function.
    :return: None, but saves the plot.
    """

    kwargs.setdefault("format", "pdf")
    if "format" in kwargs and kwargs["format"] != "pdf":
        kwargs.setdefault("dpi", 300)

    fig.savefig(*args, **kwargs)


