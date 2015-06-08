import colors


def make_ax_dark(ax, minor_ticks=False):
    """Turns an axis into one with a dark background with white gridlines.

    When you pass any axis, it will turn it into one with a slightly light
    gray background, and with solid white gridlines. All the axes spines are
    removed (so there isn't any outline), and the ticks are removed too.

    This returns the same axis object back, but since it is modified in the
    function it isn't necessary. Just calling the function will turn it dark,
    you don't need to reassign the variable.

    :param ax: axis object to be changed
    :return: same axis object after being modified.
    """

    ax.set_axis_bgcolor(colors.light_gray)
    ax.grid(which="major", color="w", linestyle="-", linewidth=0.5)
    if minor_ticks:
        ax.minorticks_on()
        ax.grid(which="minor", color="w", linestyle=":", linewidth=0.5)

    ax.set_axisbelow(True)  # moves gridlines below the points

    # remove all outer splines
    remove_spines(ax, ["left", "right", "top", "bottom"])

    return ax

def scatter(ax, *args, **kwargs):
    """
    Makes a scatter plot that looks nicer than the matplotlib default.

    The call works just like a call to plt.scatter, except that the first
    parameter needs to be the axis that this stuff will be plotted on. All
    other parameters will be passed on to the plt.scatter function.

    NOTE: the `c` parameter tells just the facecolor of the points, while
    `color` specifies the whole color of the point, including the edge line
    color. This follows the default matplotlib scatter implementation.

    :param ax: axis object the scatter points will be plotted on.
    :param args: non-keyword arguments that will be passed on to the
                 plt.scatter function. These will typically be the x and y
                 lists.
    :param kwargs: keyword arguments that will be passed on to plt.scatter.
    :return: the output of the plt.scatter call is returned directly.
    """

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

def remove_spines(ax, spines_to_remove):
    """Remove the desired spines from the axis, as well as the corresponding
    ticks.

    The axis will be modified in place, so there isn't a need to return the
    axis object, but you can keep it if you want.

    :param ax: axis object to remove the spines from.
    :param spines_to_remove: List of the desired spines to remove. Can choose
                             from "all", "top", "bottom", "left", or "right".
    :return: the same axis object.
    """
    # If they want to remove all spines, turn that into workable infomation
    spines_to_remove = set(spines_to_remove) # to remove duplicates
    if "all" in spines_to_remove:
        spines_to_remove.remove("all")
        for spine in ["left", "right", "top", "bottom"]:
            spines_to_remove.add(spine)

    # remove the spines
    for spine in spines_to_remove:
        ax.spines[spine].set_visible(False)

    # remove the ticks that correspond the the splines removed
    remove_ticks(ax, spines_to_remove)

    return ax

def remove_ticks(ax, ticks_to_remove):
    """Removes ticks from the given locations.

    Like most of these function, the axis is modified in place when the ticks
    are removed, so the axis object doesn't really need to be returned.

    :param ax: axes to remove ticks from.
    :param ticks_to_remove: locations where ticks need to be removed from.
                            Pass in a list, and choose from: "all, "top",
                            "bottom", "left", or "right".
    :return: axis object with the ticks removed.
    """
    # TODO: doesn't work if they pass in a string, rather than a list

    # If they want to remove all spines, turn that into workable infomation
    ticks_to_remove = set(ticks_to_remove) # to remove duplicates
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

def legend(ax, facecolor, *args, **kwargs):
    """Create a nice looking legend.

    Works by calling the ax.legend() function with the given args and kwargs.
    If some are not specified, they will be filled with values that make the
    legend look nice.

    :param ax: axis object the legend will be put on.
    :param facecolor: color of the background of the legend. There are two
                      default options: "light" and "dark". Light will be white,
                      and dark will be the same color as the dark ax. If any
                      other color is passed in, then that color will be the one
                      used.
    :param args: non-keyword arguments passed on to the ax.legend() fuction.
    :param kwargs: keyword arguments that will be passed on to the ax.legend()
                   function. This will be things like loc, and title, etc.
    :return: legend object returned by the ax.legend() function.
    """
    kwargs.setdefault('loc', 0)
    if facecolor == "light":
        facecolor = "#FFFFFF"
    elif facecolor == "dark":
        facecolor = '#E5E5E5'
    # otherwise, leave facecolor alone

    # push the legend a little farther away from the edge.
    kwargs.setdefault('borderaxespad', 0.75)

    legend = ax.legend(*args, **kwargs)

    # TODO: set the fontsize of the title properly. The best way to do it is
    # probably to get the font from one of the other text objects, then
    # increment that slightly, then set the title's fontsize to be that.
    # the fontsize param doesn't change the title, so do that manually
    # title = legend.get_title()
    # title.set_fontsize(kwargs['fontsize'])

    # turn the background into whatever color it needs to be
    frame = legend.get_frame()
    frame.set_facecolor(facecolor)
    frame.set_linewidth(0)

    return legend

def equal_scale(ax):
    """ Makes the x and y axes have the same scale

    Useful for plotting things like ra and dec, something with the same
    quantity on both axes, or anytime the x and y axis have the same scale.

    It's really one one command, but it's one I have a hard time remembering.

    :param ax: Axis to make equal scale.
    :return: axis that was passed in. It is modified in place, though, so even
             if its result is not assigned to anything it will still work.
    """
    ax.set_aspect("equal", adjustable="box")
    return ax
