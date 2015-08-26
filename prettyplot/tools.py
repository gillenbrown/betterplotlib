import matplotlib as mpl
import matplotlib.pyplot as plt

import colors


def set_style():

    mpl.rcParams['legend.scatterpoints'] = 1
    mpl.rcParams['savefig.format'] = 'pdf'
    mpl.rcParams['axes.formatter.useoffset'] = False
    mpl.rcParams['figure.dpi'] = 300
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
    mpl.rcParams['axes.color_cycle'] = colors.color_cycle



def _get_ax(**kwargs):
    """
    Get an axis object to plot stuff on.

    This will take the axis from kwargs if the user specified `ax`. If not, it
    will get the current axis, as defined by matplotlib. That may be a
    crapshoot if there are multiple axes, I don't know.

    This function is to be used in the rest of my functions, where we need
    to get an axis.

    :param kwargs: keyword arguments from whatever function call this is used
                   if.
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
    :param minor_ticks: Whether or not to add minor ticks. They will be
                        drawn as dotted lines, rather than solid lines in the
                        axes space.
    :return: same axis object after being modified.

    Example:

    .. plot::
        :include-source:

        import prettyplot as ppl
        import matplotlib.pyplot as plt

        ppl.set_style()

        fig, (ax1, ax2) = plt.subplots(figsize=[12, 5], ncols=2)
        ppl.make_ax_dark(ax2)
        ax1.set_title("Regular")
        ax2.set_title("Dark")


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


def scatter(*args, **kwargs):
    """
    Makes a scatter plot that looks nicer than the matplotlib default.

    The call works just like a call to plt.scatter. It will set a few default
    parameters, but anything you pass in will override the default parameters.
    This function also uses the color cycle, unlike the default scatter.

    NOTE: the `c` parameter tells just the facecolor of the points, while
    `color` specifies the whole color of the point, including the edge line
    color. This follows the default matplotlib scatter implementation.


    :param args: non-keyword arguments that will be passed on to the
                 plt.scatter function. These will typically be the x and y
                 lists.
    :keyword ax: Axes object to plot on.
    :param kwargs: keyword arguments that will be passed on to plt.scatter.
    :return: the output of the plt.scatter call is returned directly.

    .. plot::
        :include-source:

        import prettyplot as ppl
        import numpy as np

        ppl.set_style()

        x1 = np.random.normal(0, scale=0.5, size=500)
        y1 = np.random.normal(0, scale=0.5, size=500)
        x2 = np.random.normal(0.5, scale=0.5, size=500)
        y2 = np.random.normal(0.5, scale=0.5, size=500)
        x3 = np.random.normal(1, scale=0.5, size=500)
        y3 = np.random.normal(1, scale=0.5, size=500)

        ppl.scatter(x1, y1)
        ppl.scatter(x2, y2)
        ppl.scatter(x3, y3)
    """

    ax, kwargs = _get_ax(**kwargs)

    # get the color, if it hasn't already been set.
    if 'color' not in kwargs and 'c' not in kwargs:
        # get the default color cycle, and get the next color.
        color_cycle = ax._get_lines.color_cycle
        kwargs['c'] = next(color_cycle)

    # set other parameters, if they haven't been set already
    # I use setdefault to do that, which puts the values in if they don't
    # already exist, but won't overwrite anything.
    kwargs.setdefault('linewidth', 0.25)
    kwargs.setdefault('alpha', 0.5)
    # edgecolor is a weird case, since it shouldn't be set if the user
    # specifies 'color', since that refers to the whole point, not just the
    # color of the point. It includes the edge color.
    if 'color' not in kwargs:
        kwargs.setdefault('edgecolor', colors.almost_black)

    return ax.scatter(*args, **kwargs)


def hist(*args, **kwargs):
    """
    A better histogram function. Also supports relative frequency plots and
    hatching better than the default matplotlib implementation.

    Everything is the same as the default matplotlib implementation, with the
    exception a few keyword parameters. `rel_freq` makes the histogram a
    relative frequency plot, and `hatch` controls the hatching of the
    bars.

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
    :keyword kwargs: additional controls that will be passed on through to the
                     plt.hist() function.
    :return: same output as plt.hist()

    Examples:

    The basic histogram should look nicer than the default histogram.

    .. plot::
        :include-source:

        import prettyplot as ppl
        import matplotlib.pyplot as plt
        import numpy as np

        ppl.set_style()

        data = np.random.normal(0, 2, 10000)

        ppl.hist(data)

    There are also plenty of options that make other histograms look nice too.

    .. plot::
        :include-source:

        import prettyplot as ppl
        import matplotlib.pyplot as plt
        import numpy as np

        ppl.set_style()

        data1 = np.random.normal(-6, 1, size=10000)
        data2 = np.random.normal(-2, 1, size=10000)
        data3 = np.random.normal(2, 1, size=10000)
        data4 = np.random.normal(6, 1, size=10000)
        ppl.hist(data1, rel_freq=True)
        ppl.hist(data2, rel_freq=True, histtype="step", linewidth=5)
        ppl.hist(data3, rel_freq=True, histtype="stepfilled", hatch="o", alpha=0.8)
        ppl.hist(data4, rel_freq=True, histtype="step", hatch="x", linewidth=4)

        ppl.add_labels(y_label="Relative Frequency")

    Here is a demo of all the hatch styles. Repeat each symbol more for a
    denser pattern. I would only use hatching when using `histtype` as either
    `step` or `stepfilled`, since the bar borders on the regular histogram
    mess with the hatching.

    .. plot::
        :include-source:

        import prettyplot as ppl
        import matplotlib.pyplot as plt
        import numpy as np

        ppl.set_style()

        data = np.random.uniform(0, 0.9, 10000)

        for hatch in ['-', '|', '+', '/', '\\\\', 'x', '.', 'o', 'O', '*']:
            ppl.hist(data, histtype="stepfilled", hatch=hatch,
                     bins=[min(data), max(data)])
            data += 1

    If you specify histtype="step", the hatching is the same color as the
    rest of the bar.

    .. plot::
        :include-source:

        import prettyplot as ppl
        import matplotlib.pyplot as plt
        import numpy as np

        ppl.set_style()

        data = np.random.uniform(0, 0.9, 10000)

        for hatch in ['-', '|', '+', '/', '\\\\', 'x', '.', 'o', 'O', '*']:
            ppl.hist(data, histtype="step", hatch=hatch,
                     bins=[min(data), max(data)])
            data += 1
    """

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

    # plot the histogram, and keep the results
    hist_results = ax.hist(*args, **kwargs)

    # set the hatch on the patch objects, which are the last thing in the
    # output of plt.hist()
    if hatch is not None:
        for patch in hist_results[2]:
            patch.set_hatch(hatch)

    return hist_results


def remove_spines(spines_to_remove, ax=None):
    """Remove the desired spines from the axis, as well as the corresponding
    ticks.

    The axis will be modified in place, so there isn't a need to return the
    axis object, but you can keep it if you want.

    :param spines_to_remove: List of the desired spines to remove. Can choose
                             from "all", "top", "bottom", "left", or "right".
    :param ax: Axes object to remove the spines from. This isn't necessary, and
               can be left blank if you are willing to let matplotlib find
               the axis for you.
    :return: the same axis object.
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
    remove_ticks(spines_to_remove, ax)

    return ax


def remove_ticks(ticks_to_remove, ax=None):
    """Removes ticks from the given locations.

    Like most of these function, the axis is modified in place when the ticks
    are removed, so the axis object doesn't really need to be returned.


    :param ticks_to_remove: locations where ticks need to be removed from.
                            Pass in a list, and choose from: "all, "top",
                            "bottom", "left", or "right".
    :param ax: Axes object to remove ticks from. This can be ignored.
    :return: axis object with the ticks removed.
    """
    # TODO: doesn't work if they pass in a string, rather than a list
    if ax is None:
        ax, kwargs = _get_ax()

    # If they want to remove all spines, turn that into workable infomation
    ticks_to_remove = set(ticks_to_remove)  # to remove duplicates
    if "all" in ticks_to_remove:
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


def legend(facecolor, *args, **kwargs):
    """Create a nice looking legend.

    Works by calling the ax.legend() function with the given args and kwargs.
    If some are not specified, they will be filled with values that make the
    legend look nice.

    :param facecolor: color of the background of the legend. There are two
                      default options: "light" and "dark". Light will be white,
                      and dark will be the same color as the dark ax. If any
                      other color is passed in, then that color will be the one
                      used.
    :param args: non-keyword arguments passed on to the ax.legend() fuction.
    :keyword ax: Axes object to plot on.
    :param kwargs: keyword arguments that will be passed on to the ax.legend()
                   function. This will be things like loc, and title, etc.
    :return: legend object returned by the ax.legend() function.
    """

    ax, kwargs = _get_ax(**kwargs)

    kwargs.setdefault('loc', 0)
    if facecolor == "light":
        facecolor = "#FFFFFF"
    elif facecolor == "dark":
        facecolor = '#E5E5E5'
    # otherwise, leave facecolor alone

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
    """ Makes the x and y axes have the same scale

    Useful for plotting things like ra and dec, something with the same
    quantity on both axes, or anytime the x and y axis have the same scale.

    It's really one one command, but it's one I have a hard time remembering.

    :param ax: Axis to make equal scale.
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
    :param x_max: maximum x value to be plotted
    :param y_min: minimum y value to be plotted
    :param y_max: maximum y value to be plotted
    :keyword ax: Axes object to plot on.
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
    :param y: y location of the text to be added.
    :param text: text to be added
    :param coords: type of coordinates. This parameter can be either 'data' or
                   'axes'. 'data' puts the text at that data point. 'axes' puts
                   the text in that location relative the axes. See above.
    :keyword ax: Axes to put the text on.
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
    :keyword ax: Axes object to put the text on.
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
        import prettyplot as ppl

        ppl.set_style()

        ppl.easy_add_text("1", 1)
        ppl.easy_add_text("2", 2)
        ppl.easy_add_text("3", 3)
        ppl.easy_add_text("4", 4)
        ppl.easy_add_text("5", 5)
        ppl.easy_add_text("6", 6)
        ppl.easy_add_text("7", 7)
        ppl.easy_add_text("8", 8)
        ppl.easy_add_text("9", 9)

    .. plot::
        :include-source:

        import matplotlib.pyplot as plt
        import prettyplot as ppl

        ppl.set_style()

        ppl.easy_add_text("upper left", "upper left")
        ppl.easy_add_text("upper center", "upper center")
        ppl.easy_add_text("upper right", "upper right")
        ppl.easy_add_text("center left", "center left")
        ppl.easy_add_text("center", "center")
        ppl.easy_add_text("center right", "center right")
        ppl.easy_add_text("lower left", "lower left")
        ppl.easy_add_text("lower center", "lower center")
        ppl.easy_add_text("lower right", "lower right")


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
