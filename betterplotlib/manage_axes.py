import matplotlib.pyplot as plt


def subplots(*args, **kwargs):
    """
    A wrapper to the plt.subplots() function, and is the main way to access the
    betterplotlib functionality.

    This is exactly the same as the `plt.subplots()` function, only that it
    creates betterplotlib axes objects rather than matplotlib ones.
    The betterplotlib objects are where all the magic happens.
    """

    # use a bpl axes object. This is a stored projection in matplotlib
    # that we can access
    subplot_kwargs = kwargs.setdefault("subplot_kw", dict())
    subplot_kwargs.setdefault("projection", "bpl")
    kwargs.setdefault("tight_layout", True)

    return plt.subplots(*args, **kwargs)


def get_axis():
    """
    Get a currently active betterplotlib axis object
    """
    if plt.get_fignums() == []:
        fig, ax = subplots()
        return ax
    fig = plt.gcf()
    if len(fig.axes) != 0:
        # go through and find a bpl axis
        for ax in fig.axes:
            if ax.name == "bpl":
                return ax
    # if we got here, there is no bpl axis available on this figure
    # if there is already an axis on this, raise an error
    if len(fig.axes) > 0:
        raise ValueError("no axis available")
    # no axis availabe, so add one
    ax = fig.add_subplot(projection="bpl")
    return ax
