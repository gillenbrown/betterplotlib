import matplotlib.pyplot as plt


def make_ax_dark(minor_ticks=False):
    """Turns an axis into one with a dark background with white gridlines.

    This will turn an axis into one with a slightly light gray background, 
    and with solid white gridlines. All the axes spines are removed (so 
    there isn't any outline), and the ticks are removed too.

    :param minor_ticks: Whether or not to add minor ticks. They will be
                drawn as dotted lines, rather than solid lines in 
                the axes space.
    :type minor_ticks: bool
    :return: None

    Example:

    .. plot::
        :include-source:

        import betterplotlib as bpl
        bpl.default_style()

        fig, (ax0, ax1) = bpl.subplots(figsize=[12, 5], ncols=2)
        ax1.make_ax_dark()
        ax0.set_title("Regular")
        ax1.set_title("Dark")


    """
    ax = plt.gca(projection='bpl')
    return ax.make_ax_dark(minor_ticks)


def remove_ticks(ticks_to_remove):
    """Removes ticks from the given locations.

    In some situations, ticks aren't needed or wanted. Note that this 
    doesn't remove the spine itself, or the labels on that axis.

    Note that this can break when used with the various `remove_*()` 
    functions. Order matters with these calls, presumably due to something 
    with the way matplotlib works under the hood. Mess around with it if 
    you're having trouble. 

    :param ticks_to_remove: locations where ticks need to be removed from.
                Pass in a list, and choose from: "all, "top",
                "bottom", "left", or "right".
    :type ticks_to_remove: list
    :return: None

    .. plot::
        :include-source:

        import betterplotlib as bpl
        bpl.default_style()

        fig, (ax0, ax1) = bpl.subplots(ncols=2, figsize=[10, 5])

        ax0.plot([0, 1, 2], [0, 1, 2])
        ax1.plot([0, 1, 2], [0, 1, 2])

        ax0.remove_ticks(["top", "right"])
        ax1.remove_ticks(["all"])

        ax0.set_title("removed top/right ticks")
        ax1.set_title("removed all ticks")
    """
    ax = plt.gca(projection='bpl')
    return ax.remove_ticks(ticks_to_remove)


def remove_spines(spines_to_remove):
    """Remove spines from the axis.

    Spines are the lines on the side of the axes. In many situations, these
    are not needed, and are just junk. Calling this function will remove
    the specified spines from an axes object. Note that it does not remove
    the tick labels if they are visible for that axis.

    Note that this function can mess up if you call this function multiple
    times with the same axes object, due to the way matplotlib works under
    the hood. I haven't really tested it extensively (since I have never 
    wanted to call it more than once), but I think the last function call
    is the one that counts. Calling this multiple times on the same axes
    would be pointless, though, since you can specify multiple axes in one 
    call. If you really need to call it multiple times and it is breaking, 
    let me know and I can try to fix it. This also can break when used with 
    the  various `remove_*()` functions. Order matters with these calls, 
    for some reason. 

    :param spines_to_remove: List of the desired spines to remove. Can 
                 choose from "all", "top", "bottom", "left", 
                 or "right".
    :type spines_to_remove: list
    :return: None

    .. plot::
        :include-source:

        import betterplotlib as bpl
        bpl.default_style()

        fig, (ax0, ax1) = bpl.subplots(ncols=2, figsize=[10, 5])

        ax0.plot([0, 1, 2], [0, 1, 2])
        ax1.plot([0, 1, 2], [0, 1, 2])

        ax0.remove_spines(["top", "right"])
        ax1.remove_spines(["all"])

        ax0.set_title("removed top/right spines")
        ax1.set_title("removed all spines")

    """
    ax = plt.gca(projection='bpl')
    return ax.remove_spines(spines_to_remove)


def scatter(*args, **kwargs):
    """
    Makes a scatter plot that looks nicer than the matplotlib default.

    The call works just like a call to plt.scatter. It will set a few 
    default parameters, but anything you pass in will override the default 
    parameters. This function also uses the color cycle, unlike the default 
    scatter.

    It also automatically determines a guess at the proper alpha 
    (transparency) of the points in the plot.

    NOTE: the `c` parameter tells just the facecolor of the points, while
    `color` specifies the whole color of the point, including the edge line
    color. This follows the default matplotlib scatter implementation.

    :param args: non-keyword arguments that will be passed on to the
             plt.scatter function. These will typically be the x and y
             lists.
    :param kwargs: keyword arguments that will be passed on to plt.scatter.
    :return: the output of the plt.scatter call is returned directly.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import matplotlib.pyplot as plt
        import numpy as np
        bpl.default_style()

        x = np.random.normal(0, scale=0.5, size=500)
        y = np.random.normal(0, scale=0.5, size=500)
        
        fig = plt.figure(figsize=[15, 7])
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122, projection="bpl")
        
        for ax in [ax1, ax2]:
        ax.scatter(x,     y)
        ax.scatter(x+0.5, y+0.5)
        ax.scatter(x+1,   y+1)
        
        ax1.set_title("matplotlib")
        ax2.add_labels(title="betterplotlib")

    """
    ax = plt.gca(projection='bpl')
    return ax.scatter(*args, **kwargs)


def hist(*args, **kwargs):
    """
    A better histogram function. Also supports relative frequency plots, bin
    size, and hatching better than the default matplotlib implementation.

    Everything is the same as the default matplotlib implementation, with 
    the exception a few keyword parameters. `rel_freq` makes the histogram a
    relative frequency plot and `bin_size` controls the width of each bin.

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
    :keyword bin_size: The width of the bins in the histogram. The bin
               boundaries will start at zero, and will be integer
               multiples of bin_size from there. Specify either 
               this, or bins, but not both.
    :type bin_size: float
    :keyword kwargs: additional controls that will be passed on through to 
             the plt.hist() function.
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

        fig = plt.figure(figsize=[15, 7])
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122, projection="bpl")
        
        ax1.hist(data)
        ax2.hist(data)
        
        ax1.set_title("matplotlib")
        ax2.add_labels(title="betterplotlib")

    There are also plenty of options that make other histograms look nice 
    too.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np
        bpl.default_style()

        data1 = np.random.normal(-6, 1, size=10000)
        data2 = np.random.normal(-2, 1, size=10000)
        data3 = np.random.normal(2, 1, size=10000)
        data4 = np.random.normal(6, 1, size=10000)
        bin_size = 0.5
        bpl.hist(data1, rel_freq=True, bin_size=bin_size)
        bpl.hist(data2, rel_freq=True, bin_size=bin_size, histtype="step", 
             linewidth=5)
        bpl.hist(data3, rel_freq=True, bin_size=bin_size, 
             histtype="stepfilled", hatch="o", alpha=0.8)
        bpl.hist(data4, rel_freq=True, bin_size=bin_size, histtype="step", 
             hatch="x", linewidth=4)

        bpl.add_labels(y_label="Relative Frequency")

    """
    ax = plt.gca(projection='bpl')
    return ax.hist(*args, **kwargs)


def add_labels(x_label=None, y_label=None, title=None,
               *args, **kwargs):
    """
    Adds labels to the x and y axis, plus a title.

    Addition properties will be passed the all single label creations,
    so any properties will be applied to all. If you want the title to be
    different, for example, don't include it here.

    :param x_label: label for the x axis
    :type x_label: str
    :param y_label: label for the y axis
    :type y_label: str
    :param title: title for the given axis
    :type title: str
    :param args: additional properties that will be passed on to all the 
             labels you asked for.
    :param kwargs: additional keyword arguments that will be passed on to
               all the labels you make.
    :return: None

    Example:

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np
        bpl.default_style()

        xs = np.arange(0, 10, 0.1)
        ys = xs**2

        bpl.plot(xs, ys)
        bpl.add_labels("X value", "Y value", "Title")
    """
    ax = plt.gca(projection='bpl')
    return ax.add_labels(x_label, y_label, title,
                         *args, **kwargs)


def set_limits(x_min=None, x_max=None, y_min=None, y_max=None,
               **kwargs):
    """
    Set axes limits for both x and y axis at once.

    Any additional kwargs will be passed on to the matplotlib functions 
    that set the limits, so refer to that documentation to find the 
    allowed parameters.

    :param x_min: minimum x value to be plotted
    :type x_min: int, float
    :param x_max: maximum x value to be plotted
    :type x_max: int, float
    :param y_min: minimum y value to be plotted
    :type y_min: int, float
    :param y_max: maximum y value to be plotted
    :type y_max: int, float
    :param kwargs: Kwargs for the set_limits() functions.
    :return: none.

    Example:

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np
        bpl.default_style()

        xs = np.arange(0, 10, 0.01)
        ys = np.cos(xs)

        fig, [ax1, ax2] = bpl.subplots(ncols=2)

        ax1.plot(xs, ys)

        ax2.plot(xs, ys)
        ax2.set_limits(0, 2*np.pi, -1.1, 1.1)    
    """
    ax = plt.gca(projection='bpl')
    return ax.set_limits(x_min, x_max, y_min, y_max,
                         **kwargs)


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
    horizontalalignment and verticalalignment parameters if it isn't quite 
    in the spot you expect.

    Also consider using easy_add_text, which gives 9 possible location to
    add text with minimal consternation.

    :param x: x location of the text to be added.
    :type x: int, float
    :param y: y location of the text to be added.
    :type y: int, float
    :param text: text to be added
    :type text: str
    :param coords: type of coordinates. This parameter can be either 'data' 
    or 'axes'. 'data' puts the text at that data point. 'axes' puts the 
    text in that location relative the axes. See above.
    :type coords: str
    :param kwargs: any additional keyword arguments to pass on the text
               function. Pass things you would pass to plt.text()
    :return: Same as output of plt.text().

    Example:

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np
        bpl.default_style()

        xs = np.arange(0, 7, 0.1)
        ys = xs**2

        fig, ax = bpl.subplots()

        ax.plot(xs, ys)
        ax.add_text(2, 30, "(2, 30) data", ha="center", va="center")
        ax.add_text(0.6, 0.2, "60% across, 20% up", "axes")
    """
    ax = plt.gca(projection='bpl')
    return ax.add_text(x, y, text, coords, **kwargs)


def remove_labels(labels_to_remove):
    """
    Removes the labels and tick marks from an axis border.

    This is useful for making conceptual plots where the numbers on the axis
    don't matter. Axes labels still work, also.

    Note that this can break when used with the various `remove_*()` 
    functions. Order matters with these calls, presumably due to something 
    with the way matplotlib works under the hood. Mess around with it if 
    you're having trouble. 

    :param labels_to_remove: location of labels to remove. Choose from: 
                 "both", "x", or "y".
    :type labels_to_remove: str
    :return: None

    Example:

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np
        bpl.default_style()

        xs = np.arange(0, 5, 0.1)
        ys = xs**2

        fig, ax = bpl.subplots()

        ax.plot(xs, ys)

        ax.remove_labels("y")
        ax.remove_ticks(["top"])
        ax.add_labels("Conceptual plot", "Axes labels still work")

    """
    ax = plt.gca(projection='bpl')
    return ax.remove_labels(labels_to_remove)


def legend(linewidth=0, *args, **kwargs):
    """Create a nice looking legend.

    Works by calling the ax.legend() function with the given args and 
    kwargs. If some are not specified, they will be filled with values that 
    make the legend look nice.

    :param linewidth: linewidth of the border of the legend. Defaults to
              zero. 
    :param args: non-keyword arguments passed on to the ax.legend() fuction.
    :param kwargs: keyword arguments that will be passed on to the 
               ax.legend() function. This will be things like loc, 
               and title, etc.
    :return: legend object returned by the ax.legend() function.
    
    The default legend is a transparent background with no border, like so.

    .. plot::
        :include-source:

        import numpy as np
        import betterplotlib as bpl
        import matplotlib.pyplot as plt
        bpl.default_style()

        x = np.arange(0, 5, 0.1)

        fig = plt.figure(figsize=[15, 7])
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122, projection="bpl")  # bpl subplot.
        
        for ax in [ax1, ax2]:
        ax.plot(x, x, label="x")
        ax.plot(x, 2*x, label="2x")
        ax.plot(x, 3*x, label="3x")
        ax.legend(loc=2)
        
        ax1.set_title("matplotlib")
        ax2.set_title("betterplotlib")

    You can still pass in any kwargs to the legend function you want.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np

        bpl.default_style()

        x = np.arange(0, 5, 0.1)

        fig, ax = bpl.subplots()

        ax.plot(x, x, label="x")
        ax.plot(x, 2*x, label="2x")
        ax.plot(x, 3*x, label="3x")
        ax.legend(fontsize=20, loc=6, title="Title")
    """
    ax = plt.gca(projection='bpl')
    return ax.legend(linewidth, *args, **kwargs)


def equal_scale(self):
    """ Makes the x and y axes have the same scale.

    Useful for plotting things like ra and dec, something with the same
    quantity on both axes, or anytime the x and y axis have the same scale.

    It's really one one command, but it's one I have a hard time 
    remembering.

    Note that this keeps the range the same from the plot as before, so you
    may want to adjust the limits to make the plot look better. It will 
    keep the axes adjusted the same, though, no matter how you change the 
    limits afterward. 

    :return: None

    Examples:

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np

        bpl.default_style()

        # make a Gaussian with more spread in y direction
        xs = np.random.normal(0, 1, 10000)
        ys = np.random.normal(0, 2, 10000)

        fig, [ax1, ax2] = bpl.subplots(figsize=[12, 5], ncols=2)

        ax1.scatter(xs, ys)
        ax2.scatter(xs, ys)

        ax2.equal_scale()

        ax1.add_labels(title="Looks symmetric")
        ax2.add_labels(title="Shows true shape")

    Here is proof that changing the limits don't change the scaling between
    the axes. 

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np

        bpl.default_style()

        # make a Gaussian with more spread in y direction
        xs = np.random.normal(0, 1, 10000)
        ys = np.random.normal(0, 2, 10000)

        fig, [ax1, ax2] = bpl.subplots(figsize=[12, 5], ncols=2)

        ax1.scatter(xs, ys)
        ax2.scatter(xs, ys)

        ax1.equal_scale()
        ax2.equal_scale()

        ax1.set_limits(-10, 10, -4, 4)
        ax2.set_limits(-5, 5, -10, 10)

    """
    ax = plt.gca(projection='bpl')
    return ax.equal_scale(self)


def easy_add_text(text, location, **kwargs):
    """
    Adds text in common spots easily.

    This was inspired by the plt.legend() function and its loc parameter,
    which allows for easy placement of legends. This does a similar thing,
    but just for text.

    VERY IMPORTANT NOTE: Although this works similar to plt.legend()'s loc
    parameter, the numbering is NOT the same. My numbering is based on the
    keypad. 1 is in the bottom left, 5 in the center, and 9 in the top 
    right. You can also specify words that tell the location.

    :param text: Text to add to the axes.
    :type text: str
    :param location: Location to add the text. This can be specified two
             in two possible ways. You can pass an integer, which
             puts the text at the location corresponding to that
             number's location on a standard keyboard numpad.
             You can also pass a string that describe the location.
             'upper', 'center', and 'lower' describe the vertical
             location, and 'left', 'center', and 'right' describe 
             the horizontal location. You need to specify vertical,
             then horizontal, like 'upper right'. Note that 
             'center' is the code for the center, not 
             'center center'.
    :type location: str, int
    :param kwargs: additional text parameters that will be passed on to the
               plt.text() function. Note that this function controls the
               x and y location, as well as the horizonatl and vertical
               alignment, so do not pass those parameters.
    :return: Same as output of plt.text()

    Example:

    There are two ways to specify the location, and we will demo both.

    .. plot::
        :include-source:

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
    ax = plt.gca(projection='bpl')
    return ax.easy_add_text(text, location, **kwargs)


def density_contour(xs, ys, bin_size=None, percent_levels=None,
                    smoothing=0, weights=None, labels=False, **kwargs):
    """ """
    ax = plt.gca(projection='bpl')
    return ax.density_contour(xs, ys, bin_size, percent_levels,
                              smoothing, weights, labels, **kwargs)


def density_contourf(xs, ys, bin_size=None, percent_levels=None,
                     smoothing=0, weights=None, **kwargs):
    """ """
    ax = plt.gca(projection='bpl')
    return ax.density_contourf(xs, ys, bin_size, percent_levels,
                               smoothing, weights, **kwargs)


def contour_scatter(xs, ys, fill_cmap="white", bin_size=None,
                    min_level=5, num_contours=7, scatter_kwargs=None,
                    contour_kwargs=None, smoothing=None,
                    percent_levels=None, weights=None, labels=None):
    """
    Create a contour plot with scatter points in the sparse regions.

    When a dataset is large, plotting a scatterplot is often really hard to 
    understand, due to many points overlapping and the high density of 
    points overall. A contour or hexbin plot solves many of these problems, 
    but these still have the disadvantage of making outliers less obvious. 
    A simple solution is to plot contours in the dense regions, while 
    plotting individual points where the density is low. That is what 
    this function does.

    Here's how this works under the hood. Skip this paragraph if you don't 
    care; it won't affect how you use this. This function uses the numpy 
    2D histogram function to create an array representing the density in 
    each region. If no binning info is specified by the user, the 
    Freedman-Diaconis algorithm is used in both dimensions to find the 
    ideal bin size for the data. First, an opaque filled contour is 
    plotted, then the contour lines are put on top. Then the outermost 
    contour is made into a matplotlib path object, which lets us 
    check which of the points are outside of this contour. Only the points 
    that are outside are plotted.

    The parameters of this function are more complicated than others in 
    betterplotlib and are somewhat arbitrary, so please read the info below 
    carefully. The examples should make things more clear also.

    :param xs: list of x values of your data
    :type xs: list
    :param ys: list of y values of your data
    :type ys: list
    :param fill_cmap: Colormap that will fill the opaque contours. Defaults 
              to "white", which is just a solid white fill. You can 
              pass any name of a matplotlib colormap, as well as 
              some options I have created. "background_grey" gives 
              a solid fill that is the same color as the 
              make_ax_dark() background. "modified_greys" is a 
              colormap that starts at the "background_grey" color, 
              then transitions to black. 
    :type fill_cmap: str
    :param bin_size: Size of the bins used in the 2D histogram. This is kind
             of an arbitraty parameter. The code will guess a 
             value for this if none is passed in, but this value 
             isn't always good. A smaller value gives noisier 
             contours. A value that is too large will lead to 
             "chunky" contours. Adjust this until your contours 
             look good to your eye. That's the best
             way to pick a value for this parameter. It can be
             either a scalar, in which case that will be used for 
             both x and y. It could also be a two element list, in
             which case it will be the bin size for x and y. 
    :type bin_size: float or list
    :param min_level: This is another arbitrary parameter that determines 
              how high the density of points needs to be before 
              the outer contour is drawn. The higher the value, 
              the more points will be outside the last contour. 
              Again, adjust this until it looks good to your eye. 
              The default parameter choice will generally be okay, 
              though. Also note that if you want to specify the 
              levels yourself, use the `levels` keyword.
    :type min_level: int
    :param num_contours: Number of contour lines to be drawn between the 
                 lowest and highest density regions. Adjust this 
                 until the plot looks good to your eye. Also note 
                 that if you want to specify the levels yourself, 
                 use the `levels` keyword.
    :type num_contours: int
    :param scatter_kwargs: This is a dictionary of keywords that will be 
                   passed on to the `bpl.scatter()` function. Note 
                   that this doesn't work like normal kwargs. You 
                   need to pass in a dictionary. This is because we 
                   have to separate the kwargs that go to the 
                   scatter function from the ones that go to the 
                   ontour function. 
    :type scatter_kwargs: dict
    :param contour_kwargs: This is a dictionary of keywords that will be 
                   passed on to the `plt.contour()` function. Note 
                   that this doesn't work like normal kwargs. You 
                   need to pass in a dictionary. This is because we 
                   have to separate the kwargs that go to the 
                   scatter function from the ones that go to the 
                   contour function. 
    :type contour_kwargs: dict
    :return: The output of the `contour` call will be returned. This doesn't 
         need to be saved, you can use it if you want. 

    Examples

    First, we'll show why this plot is useful. This won't use any of the 
    fancy settings, other than `bin_size`, which is used to make the 
    contours look nicer. 

    .. plot::
        :include-source:

        import numpy as np
        import betterplotlib as bpl
        bpl.default_style()

        xs = np.concatenate([np.random.normal(0, 1, 100000),
                 np.random.normal(3, 1, 100000),
                 np.random.normal(0, 1, 100000)])
        ys = np.concatenate([np.random.normal(0, 1, 100000),
                 np.random.normal(3, 1, 100000),
                 np.random.normal(3, 1, 100000)])

        fig, (ax1, ax2) = bpl.subplots(ncols=2, figsize=[10, 5])

        ax1.scatter(xs, ys)
        ax2.contour_scatter(xs, ys, bin_size=0.3)

    The scatter plot is okay, but the contour makes things easier to see. 

    We'll now mess with some of the other parameters. This plot shows how 
    the  `bin_size` parameter changes things. 

    .. plot::
        :include-source:

        import numpy as np
        import betterplotlib as bpl
        bpl.default_style()

        xs = np.concatenate([np.random.normal(0, 1, 100000),
                 np.random.normal(3, 1, 100000),
                 np.random.normal(0, 1, 100000)])
        ys = np.concatenate([np.random.normal(0, 1, 100000),
                 np.random.normal(3, 1, 100000),
                 np.random.normal(3, 1, 100000)])

        fig, (ax1, ax2, ax3) = bpl.subplots(ncols=3, figsize=[15, 5])

        ax1.contour_scatter(xs, ys, bin_size=0.1)
        ax2.contour_scatter(xs, ys, bin_size=0.2)
        ax3.contour_scatter(xs, ys, bin_size=0.5)

    You can see how small values of `bin_size` lead to more noisy contours. 
    The code will attempt to choose its own value of `bin_size` if nothing 
    is specified, but it's normally not a very good choice.

    For a given value of `bin_size`, changing `min_level` adjusts the height 
    at which the first contours are drawn.

    .. plot::
        :include-source:

        import numpy as np
        import betterplotlib as bpl
        bpl.default_style()

        xs = np.concatenate([np.random.normal(0, 1, 100000),
                 np.random.normal(3, 1, 100000),
                 np.random.normal(0, 1, 100000)])
        ys = np.concatenate([np.random.normal(0, 1, 100000),
                 np.random.normal(3, 1, 100000),
                 np.random.normal(3, 1, 100000)])

        fig, (ax1, ax2, ax3) = bpl.subplots(ncols=3, figsize=[15, 5])

        ax1.contour_scatter(xs, ys, bin_size=0.3, min_level=2)
        ax2.contour_scatter(xs, ys, bin_size=0.3, min_level=15)
        ax3.contour_scatter(xs, ys, bin_size=0.3, min_level=50)

    The code sets `min_level = 5` if you don't set it.

    As expected, `num_contours` adjusts the number of contors drawn. 

    .. plot::
        :include-source:

        import numpy as np
        import betterplotlib as bpl
        bpl.default_style()

        xs = np.concatenate([np.random.normal(0, 1, 100000),
                 np.random.normal(3, 1, 100000),
                 np.random.normal(0, 1, 100000)])
        ys = np.concatenate([np.random.normal(0, 1, 100000),
                 np.random.normal(3, 1, 100000),
                 np.random.normal(3, 1, 100000)])

        fig, (ax1, ax2, ax3) = bpl.subplots(ncols=3, figsize=[15, 5])

        ax1.contour_scatter(xs, ys, bin_size=0.3, num_contours=2)
        ax2.contour_scatter(xs, ys, bin_size=0.3, num_contours=5)
        ax3.contour_scatter(xs, ys, bin_size=0.3, num_contours=10)

    Now we can mess with the fun stuff, which is the `fill_cmap` param and 
    the kwargs that get passed to the `scatter` and `contour` function 
    calls. There is a lot of stuff going on here, just for demonstration 
    purposes. Note that the code has some default parameters that it will 
    choose if you don't specify anything.

    .. plot::
        :include-source:

        import numpy as np
        import betterplotlib as bpl
        bpl.default_style()

        xs = np.concatenate([np.random.normal(0, 1, 100000),
                 np.random.normal(3, 1, 100000),
                 np.random.normal(0, 1, 100000)])
        ys = np.concatenate([np.random.normal(0, 1, 100000),
                 np.random.normal(3, 1, 100000),
                 np.random.normal(3, 1, 100000)])

        fig, axs = bpl.subplots(nrows=2, ncols=2)
        [ax1, ax2], [ax3, ax4] = axs

        ax1.contour_scatter(xs, ys, bin_size=0.3,
                fill_cmap="background_grey",
                contour_kwargs={"cmap":"magma"},
                scatter_kwargs={"s":10, "c":bpl.almost_black})
        ax1.make_ax_dark()

        # or we can choose our own `fill_cmap`
        ax2.contour_scatter(xs, ys, bin_size=0.3, fill_cmap="viridis",
                contour_kwargs={"linewidths":1, 
                        "colors":"white"},
                scatter_kwargs={"s":50, "c":bpl.color_cycle[3], 
                        "alpha":0.3})

        # There are also my colormaps that work with the dark axes
        ax3.contour_scatter(xs, ys, bin_size=0.3, fill_cmap="modified_greys",
                num_contours=7,
                scatter_kwargs={"c": bpl.color_cycle[0]},
                contour_kwargs={"linewidths":[2,0,0,0,0,0,0],
                        "colors":bpl.almost_black})
        ax3.make_ax_dark(ax3)

        # the default `fill_cmap` is white.
        ax4.contour_scatter(xs, ys, bin_size=0.3, num_contours=3,
                scatter_kwargs={"marker":"^", "linewidth":0.2,
                        "c":bpl.color_cycle[1], "s":20},
                contour_kwargs={"linestyles":["solid", "dashed", 
                                  "dashed", "dashed"],
                        "colors":bpl.almost_black})

    Note that the contours will work appropriately for datasets with 
    "holes", as demonstrated here.
    
    .. plot::
        :include-source:

        import numpy as np
        import betterplotlib as bpl
        bpl.default_style()

        rad1 = np.random.normal(10, 0.75, 100000)
        theta1 = np.random.uniform(0, 2 * np.pi, 100000)
        x1 = [r * np.cos(t) for r, t in zip(rad1, theta1)]
        y1 = [r * np.sin(t) for r, t in zip(rad1, theta1)]

        rad2 = np.random.normal(20, 0.75, 200000)
        theta2 = np.random.uniform(0, 2 * np.pi, 200000)
        x2 = [r * np.cos(t) for r, t in zip(rad2, theta2)]
        y2 = [r * np.sin(t) for r, t in zip(rad2, theta2)]

        rad3 = np.random.normal(12, 0.75, 120000)
        theta3 = np.random.uniform(0, 2 * np.pi, 120000)
        x3 = [r * np.cos(t) + 10 for r, t in zip(rad3, theta3)]
        y3 = [r * np.sin(t) + 10 for r, t in zip(rad3, theta3)]

        x4 = np.random.uniform(-20, 20, 35000)
        y4 = x4 + np.random.normal(0, 0.5, 35000)

        y5 = y4 * (-1)

        xs = np.concatenate([x1, x2, x3, x4, x4])
        ys = np.concatenate([y1, y2, y3, y4, y5])

        fig, ax = bpl.subplots()

        ax.contour_scatter(xs, ys)
        ax.equal_scale()
    """
    ax = plt.gca(projection='bpl')
    return ax.contour_scatter(xs, ys, fill_cmap, bin_size,
                              min_level, num_contours, scatter_kwargs,
                              contour_kwargs, smoothing,
                              percent_levels, weights, labels)


def data_ticks(x_data, y_data, extent=0.015, *args, **kwargs):
    """
    Puts tiny ticks on the axis borders making the location of each point.

    :param x_data: list of values to mark on the x-axis.
    :type x_data: list
    :param y_data: list of values to mark on the y-axis. This doesn't have
               to be the same length as `x-data`, necessarily.
    :type y_data: list
    :param extent: How far the ticks go up from the x-axis. The default is
               0.02, meaning the ticks go 2% of the way to the top of 
               the plot. Note that the ticks created by this function
               will have the same physical size on both axes. Since in
               general the x and y axes aren't the same physical size, 
               the ticks on the y-axis will be scaled to match the 
               physical size of the x ticks. This means that in the 
               default case, the y ticks won't cover 2% of the axis, but
               again will be the same physical size as the x ticks. 
    :type extent: float
    :param args: Additional arguments to pass to the `axvline` and `axhline`
             functions, which is what is used to make each tick.
    :param kwargs: Additional keyword arguments to pass to the `axvline` and
               `axhline` functions. `color` is an important one here, 
               and it defaults to `almost_black` here.


    Example
    
    .. plot::
        :include-source:

        import numpy as np
        import betterplotlib as bpl
        bpl.default_style()

        xs = np.random.normal(0, 1, 100)
        ys = np.random.normal(0, 1, 100)

        fig, ax = bpl.subplots()
        ax.scatter(xs, ys)
        ax.data_ticks(xs, ys)       
    """
    ax = plt.gca(projection='bpl')
    return ax.data_ticks(x_data, y_data, extent, *args, **kwargs)


def plot(*args, **kwargs):
    """A slightly improved plot function.

    This is best used for plotting lines, while the `scatter()` function
    is best used for plotting points.

    Currently all this does is make the lines thicker, which looks better.
    There isn't any added functionality.

    The parameters here are the exact same as they are for the regular
    `plt.plot()` or `ax.plot()` functions, so I don't think any 
    documentation would be helpful.

    .. plot::
        :include-source:

        import numpy as np
        import betterplotlib as bpl
        import matplotlib.pyplot as plt
        bpl.default_style()

        xs = np.arange(0, 1, 0.01)
        ys_1 = xs
        ys_2 = xs**2

        fig = plt.figure(figsize=[15, 7])
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122, projection="bpl")  # bpl subplot.
        
        ax1.plot(xs, ys_1) 
        ax1.plot(xs, ys_2) 
        
        ax2.plot(xs, ys_1) 
        ax2.plot(xs, ys_2) 
        
        ax1.set_title("matplotlib")
        ax2.set_title("betterplotlib")

    """
    ax = plt.gca(projection='bpl')
    return ax.plot(*args, **kwargs)


def axvline(x=0, *args, **kwargs):
    """ Place a vertical line at some point on the axes.

    :param x: Data value on the x-axis to place the line.
    :type x: float
    :param args: Additional parameters that will be passed on the the 
             regular `plt.axvline` function. See it's documentation 
             for details.
    :param kwargs: Similarly, additional keyword arguments that will be 
               passed on to the regular `plt.axvline` function.

    .. plot::
        :include-source:

        import numpy as np
        import betterplotlib as bpl
        bpl.default_style()

        left_xs = np.arange(-20, 1, 0.01)
        right_xs = np.arange(1.001, 20, 0.01)
        left_ys = left_xs / (left_xs - 1)
        right_ys = right_xs / (right_xs - 1)

        fig, ax = bpl.subplots()
        ax.make_ax_dark()
        ax.plot(left_xs, left_ys, c=bpl.color_cycle[2])
        ax.plot(right_xs, right_ys, c=bpl.color_cycle[2])
        ax.axvline(1.0, linestyle="--")
        ax.axhline(1.0, linestyle="--")
        ax.set_limits(-10, 10, -10, 10)

    """
    ax = plt.gca(projection='bpl')
    return ax.axvline(x, *args, **kwargs)


def axhline(y=0, *args, **kwargs):
    """ Place a horizontal line at some point on the axes.

    :param y: Data value on the y-axis to place the line.
    :type y: float
    :param args: Additional parameters that will be passed on the the 
             regular `plt.axhline` function. See it's documentation 
             for details.
    :param kwargs: Similarly, additional keyword arguments that will be 
               passed on to the regular `plt.axhline` function.
    
    .. plot::
        :include-source:

        import numpy as np
        import betterplotlib as bpl
        bpl.default_style()

        left_xs = np.arange(-20, 1, 0.01)
        right_xs = np.arange(1.001, 20, 0.01)
        left_ys = left_xs / (left_xs - 1)
        right_ys = right_xs / (right_xs - 1)

        fig, ax = bpl.subplots()
        ax.make_ax_dark()
        ax.plot(left_xs, left_ys, c=bpl.color_cycle[2])
        ax.plot(right_xs, right_ys, c=bpl.color_cycle[2])
        ax.axvline(1.0, linestyle="--")
        ax.axhline(1.0, linestyle="--")
        ax.set_limits(-10, 10, -10, 10)
        
    """
    ax = plt.gca(projection='bpl')
    return ax.axhline(y, *args, **kwargs)


def errorbar(*args, **kwargs):
    """Wrapper for the plt.errorbar() function.
    
    Style changes: capsize is automatically zero, and the format is 
    automatically a scatter plot, rather than the connected lines that
    are used by default otherwise. It also adds a black marker edge to
    distinguish the markers when there are lots of data poitns. Otherwise
    everything blends together.
    
    .. plot::
        :include-source:

        import numpy as np
        import betterplotlib as bpl
        import matplotlib.pyplot as plt
        bpl.default_style()
        
        xs = np.random.normal(0, 1, 100)
        ys = np.random.normal(0, 1, 100)
        yerr = np.random.uniform(0.3, 0.8, 100)
        xerr = np.random.uniform(0.3, 0.8, 100)
        
        fig = plt.figure(figsize=[15, 7])
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122, projection="bpl")  # bpl subplot.
        
        for ax in [ax1, ax2]:
        ax.errorbar(xs,   ys,   xerr=xerr, yerr=yerr, label="set 1")
        ax.errorbar(xs+1, ys+1, xerr=xerr, yerr=yerr, label="set 2")
        ax.legend()
        ax1.set_title("matplotlib")
        ax2.set_title("betterplotlib")
        
        """
    ax = plt.gca(projection='bpl')
    return ax.errorbar(*args, **kwargs)


def twin_axis_simple(axis, lower_lim, upper_lim, label="", log=False):
    """Creates a differently scaled axis on either the top or the left.
    
    This can be used to put multiple scales on one plot for easier 
    comparison. Some examples might be distance/time, redshift/age, or
    any two related quantities.
    
    Note that this only does simple scalings of the new axes, which will 
    still only be linear or log scaled axes. If you want a function that
    smartly places labels based on a function that takes one set of axes
    values to another (in a potentially nonlinear way), the other function 
    I haven't made will do that. 
    
    :param axis: Where the new scaled axis will be placed. Must
             either be "x" or "y". 
    :param lower_lim: Value to be put on the left/bottom of the newly
              created axis.
    :param upper_lim: Value to be put on the right/top of the newly 
              created axis. 
    :param label: The label to put on this new axis. 
    :param log: Whether or not to log scale this axis.
    :returns: the new axes
    
    .. plot::
        :include-source:
        
        import betterplotlib as bpl
        bpl.presentation_style()
        
        fig, ax = bpl.subplots(tight_layout=True)
        ax.set_limits(0, 10, 0, 5)
        ax.add_labels("x", "y")
        ax.twin_axis_simple("x", 0, 100, r"$10 x$")
        ax.twin_axis_simple("y", 1, 10**5, r"$10^y$", log=True)
        
    Note that for a slightly more complicated version of this plot, say if
    we wanted the top x axis to be x^2 rather than 10x, the limits would
    still be the same, but since the new axis will always be a linear or log
    scale the new axis won't represent the true relationship between the
    variables on the twin axes. See the other function for that. 
        
        
    """
    ax = plt.gca(projection='bpl')
    return ax.twin_axis_simple(axis, lower_lim, upper_lim, label, log)


def twin_axis(func, axis, new_ticks, label=None):
    """
    Create a twin axis, where the new axis values are an arbitrary function
    of the old values.

    This is used when you want to put two related quantities on the axis,
    for example distance/redshift in astronomy, where one isn't a simple
    scaling of the other. If you want a simple linear or log scale, use the
    `twin_axis_simple` function. This one will create a new axis that is
    an arbitrary scale.

    Here is a way this can be used.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        bpl.presentation_style()

        def square(x):
        return x**2

        def cubed(x):
        return x**3

        fig, ax = bpl.subplots(figsize=[5, 5], tight_layout=True)
        ax.set_limits(0, 10, 0, 10.0001)  # to avoid floating point errors
        ax.add_labels("x", "y")
        ax.twin_axis(square, "y", [0, 10, 30, 60, 100], r"$y^2$")
        ax.twin_axis(cubed,"x", [0, 10, 100, 400, 1000], r"$x^3$")

    Note that we had to be careful with floating point errors when one of
    the markers we want is exactly on the edge. Make the borders slightly
    larger to ensure that all labels fit on the plot.

    This function will ignore values for the ticks that are outside the
    limits of the plot. The following plot isn't the most useful, since
    it could be done with the `axis_twin_simple`, but it gets the idea
    across.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np
        bpl.presentation_style()

        xs = np.logspace(0, 3, 100)

        fig, ax = bpl.subplots(figsize=[5, 5], tight_layout=True)
        ax.plot(xs, xs)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.add_labels("x", "y")
        # extraneous values are ignored.
        ax.twin_axis(np.log10, "x", [-1, 0, 1, 2, 3, 4, 5], "log(x)")
        ax.twin_axis(np.log10, "y", [-1, 0, 1, 2, 3, 4, 5], "log(y)")

    :param func: Function that transforms values from the original axis
             into values that will be marked on the axis that will
             be created here.
    :param axis: Whether the new axis labels will be on the "x" or "y" axis.
             If "x" is chosen this will place the markers on the top
             botder of the plot, while "y" will place the values on the
             left border of the plot. "x" and "y" are the only
             allowed values.
    :param new_ticks: List of of locations (in the new data values) to place
              ticks. Any values outside the range of the plot
              will be ignored.
    :return: New axis object that was created, containing the newly
         created labels.
    """
    ax = plt.gca(projection='bpl')
    return ax.twin_axis(func, axis, new_ticks, label)


def shaded_density(xs, ys, bin_size=None, smoothing=0,
                   cmap="Greys", weights=None):
    """
    Creates shaded regions showing the density.

    Is essentially a 2D histogram, but supports smoothing. Under the hood,
    this uses the pcolormesh function in matplotlib.

    .. plot::
        :include-source:

        import betterplotlib as bpl
        import numpy as np
        bpl.presentation_style()

        xs = np.random.uniform(0, 10, 100)
        ys = np.random.uniform(0, 10, 100)

        fig, ax = bpl.subplots()
        ax.shaded_density(xs, ys, bin_size=0.01, smoothing=0.5,
                  cmap="inferno")
        ax.set_limits(0, 10, 0, 10)
        ax.equal_scale()

    :param xs: list of x values
    :param ys: list of y values
    :param bin_size: bin size for the 2D histogram. If not passed in, an
             appropriate bin size will be automatically found.
             If you are using smoothing, a smaller bin size is
             often useful as it can make for a better looking plot.
    :param smoothing: The size of the Gaussian smoothing kernel for the
              data. Currently is the same in both dimensions.
              Pass None for no smoothing.
    :param cmap: colormap used for the density.
    :return: output of the pcolormesh function call.
    """
    ax = plt.gca(projection='bpl')
    return ax.shaded_density(xs, ys, bin_size, smoothing,
                             cmap, weights)
