import matplotlib.pyplot as plt


def make_ax_dark(ax):
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

    ax.set_axis_bgcolor("#E5E5E5")
    ax.grid(which="major", color="w", linestyle="-", linewidth=0.5)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=0.5)
    ax.set_axisbelow(True)  # moves gridlines below the points

    # remove all outer splines
    remove_spines(ax, ["left", "right", "top", "bottom"])

    return ax

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
