from matplotlib.axes import Axes
from matplotlib import colors as mpl_colors
from matplotlib import path
from scipy import optimize
from astropy import convolution
import numpy as np
import sys

from . import colors
from . import tools
from . import type_checking


class Axes_bpl(Axes):

    name = "bpl"

    def make_ax_dark(self, grid=True, minor_ticks=False):
        """
        Turns an axis into one with a dark background with white gridlines.

        This will turn an axis into one with a slightly light gray background,
        and with solid white gridlines. All the axes spines are removed (so
        there isn't any outline), and the ticks are removed too.

        :param grid: Whether or not to draw the grid. Defaults to True.
        :type grid: bool
        :param minor_ticks: Whether or not to add minor ticks. They will be
                            drawn as dotted lines, rather than solid lines in
                            the axes space. If `grid` is False then this
                            parameter does not matter.
        :type minor_ticks: bool
        :return: None

        .. plot::
            :include-source:

            import betterplotlib as bpl
            bpl.set_style()

            fig, (ax0, ax1) = bpl.subplots(figsize=[12, 5], ncols=2)
            ax1.make_ax_dark()
            ax0.set_title("Regular")
            ax1.set_title("Dark")


        """
        self.set_facecolor(colors.light_gray)
        if grid:
            self.grid(which="major", color="w", linestyle="-", linewidth=0.5)
            if minor_ticks:
                self.minorticks_on()
                self.grid(which="minor", color="w", linestyle=":", linewidth=0.5)

        self.set_axisbelow(True)  # moves gridlines below the points

        # remove all outer splines
        self.remove_spines("all")

    def remove_ticks(self, *ticks_to_remove):
        """
        Removes ticks from the given locations.

        In some situations, ticks aren't needed or wanted. Note that this
        doesn't remove the spine itself, or the labels on that axis.

        Note that this can break when used with the various `remove_*()`
        functions. Order matters with these calls, presumably due to something
        with the way matplotlib works under the hood. Mess around with it if
        you're having trouble.

        :param ticks_to_remove: locations where ticks need to be removed from. Choose
                                from: "all, "top", "bottom", "left", or "right",
                                and pass in as many as you'd like
        :return: None

        .. plot::
            :include-source:

            import betterplotlib as bpl
            bpl.set_style()

            fig, (ax0, ax1) = bpl.subplots(ncols=2, figsize=[10, 5])

            ax0.plot([0, 1, 2], [0, 1, 2])
            ax1.plot([0, 1, 2], [0, 1, 2])

            ax0.remove_ticks("top", "right")
            ax1.remove_ticks("all")

            ax0.set_title("removed top/right ticks")
            ax1.set_title("removed all ticks")
        """
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
            self.yaxis.set_ticks_position("none")
        elif "left" in ticks_to_remove:
            self.yaxis.set_ticks_position("right")
        elif "right" in ticks_to_remove:
            self.yaxis.set_ticks_position("left")

        if "top" in ticks_to_remove and "bottom" in ticks_to_remove:
            self.xaxis.set_ticks_position("none")
        elif "top" in ticks_to_remove:
            self.xaxis.set_ticks_position("bottom")
        elif "bottom" in ticks_to_remove:
            self.xaxis.set_ticks_position("top")

    def remove_spines(self, *spines_to_remove):
        """
        Remove spines from the axis.

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

        :param spines_to_remove: The desired spines to remove. Can
                                 choose from "all", "top", "bottom", "left",
                                 or "right".
        :return: None

        .. plot::
            :include-source:

            import betterplotlib as bpl
            bpl.set_style()

            fig, (ax0, ax1) = bpl.subplots(ncols=2, figsize=[10, 5])

            ax0.plot([0, 1, 2], [0, 1, 2])
            ax1.plot([0, 1, 2], [0, 1, 2])

            ax0.remove_spines("top", "right")
            ax1.remove_spines("all")

            ax0.set_title("removed top/right spines")
            ax1.set_title("removed all spines")

        """
        # If they want to remove all spines, turn that into workable infomation
        spines_to_remove = set(spines_to_remove)  # to remove duplicates
        if "all" in spines_to_remove:
            spines_to_remove.remove("all")
            for spine in ["left", "right", "top", "bottom"]:
                spines_to_remove.add(spine)

        # remove the spines
        for spine in spines_to_remove:
            self.spines[spine].set_visible(False)

        # remove the ticks that correspond the the splines removed
        self.remove_ticks(*spines_to_remove)

    def scatter(self, *args, **kwargs):
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
            import numpy as np
            bpl.set_style()

            x = np.random.normal(0, scale=0.5, size=500)
            y = np.random.normal(0, scale=0.5, size=500)

            for dx in [0, 0.5, 1]:
                bpl.scatter(x + dx, y + dx)
            bpl.equal_scale()

        """
        # put x and y in args if they're not already there
        if len(args) == 0:
            args = kwargs.pop("x"), kwargs.pop("y")
        # get the color, if it hasn't already been set. I don't need to do this
        # in mpl 2.0 technically, but I do it anyway so I can use this color
        # for the invisible label below.
        if "color" not in kwargs and "c" not in kwargs:
            # get the default color cycle, and get the next color.
            kwargs["c"] = next(self._get_lines.prop_cycler)["color"]

        # set other parameters, if they haven't been set already
        # I use setdefault to do that, which puts the values in if they don't
        # already exist, but won't overwrite anything.
        # use the function we defined to get the proper alpha value.
        kwargs.setdefault("alpha", tools._alpha(len(args[0])))

        # we want to make the points in the legend opaque always. To do this
        # we plot nans with all the same parameters, but with alpha of one.
        if "label" in kwargs:
            # we don't want to plot any data here, so exclude the data if
            # it exists. We'll exclude the "x" and "y" kwargs below, too
            if len(args) >= 2:
                label_args = args[2:]
            # we need to process the kwargs a little before plotting the fake
            # data, so make a copy of them
            label_kwargs = kwargs.copy()
            # exclude any plotted data, if it is in a kwarg
            label_kwargs.pop("x", None)
            label_kwargs.pop("y", None)
            # set the alpha to one, which is the whole point
            label_kwargs["alpha"] = 1.0
            # we can then plot the fake data. Due to weirdness in matplotlib, we
            # have to plot a two element NaN list.
            super(Axes_bpl, self).scatter(
                [np.nan, np.nan], [np.nan, np.nan], *label_args, **label_kwargs
            )
            # in the main plotting we don't want to have a label, so we pop it.
            kwargs.pop("label")

        # we then plot the main data
        return super(Axes_bpl, self).scatter(*args, **kwargs)

    def hist(self, *args, **kwargs):
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

            bpl.set_style()

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
            bpl.set_style()

            data1 = np.random.normal(-6, 1, size=10000)
            data2 = np.random.normal(-2, 1, size=10000)
            data3 = np.random.normal(2, 1, size=10000)
            data4 = np.random.normal(6, 1, size=10000)
            bin_size = 0.5
            bpl.hist(
                data1,
                rel_freq=True,
                bin_size=bin_size,
            )
            bpl.hist(
                data2,
                rel_freq=True,
                bin_size=bin_size,
                histtype="step",
                linewidth=5,
            )
            bpl.hist(
                data3,
                rel_freq=True,
                bin_size=bin_size,
                histtype="stepfilled",
                hatch="o",
                alpha=0.8,
            )
            bpl.hist(
                data4,
                rel_freq=True,
                bin_size=bin_size,
                histtype="step",
                hatch="x",
                linewidth=4,
            )

            bpl.add_labels(y_label="Relative Frequency")

        """
        # I like white as an edgecolor if we use bars.
        if "histtype" not in kwargs or kwargs["histtype"] != "step":
            kwargs.setdefault("edgecolor", "white")

        # do the relative frequency business if we need to
        if kwargs.pop("rel_freq", False):
            # check that they didn't set weights, since that's what I'll change
            if "weights" in kwargs:
                raise ValueError(
                    "The `weights` keyword can't be used with "
                    "`rel_freq`, since `rel_freq` works by "
                    "modifying the weights."
                )
            if "density" in kwargs:
                raise ValueError("The `weights` keyword can't be used with `density`")

            # the data will be the first arg.
            data = args[0]
            # we weight each item by 1/total items.
            kwargs["weights"] = [1.0 / len(data)] * len(data)

        # if they didn't specify the binning, use our binning
        if "bin_size" in kwargs and "bins" in kwargs:
            raise ValueError(
                "The `bins` and `bin_size` keywords cannot be "
                "used together. Use `bins` if you want to "
                "pass your own bins, or use `bin_size` to "
                "have the code determine its own bins. "
            )
        # the setdefault function calls the second argument no matter what
        # This is a problem if the user's data has no IQR, since the
        # rounded bin width function will raise an error. We'll do the check
        # in a less elegant way
        if "bins" not in kwargs:
            if "bin_size" not in kwargs:
                kwargs["bin_size"] = tools.rounded_bin_width(args[0])
            kwargs["bins"] = tools._binning(
                min(args[0]), max(args[0]), kwargs.pop("bin_size")
            )

        # plot the histogram, and keep the results
        return super(Axes_bpl, self).hist(*args, **kwargs)

    def add_labels(self, x_label=None, y_label=None, title=None, *args, **kwargs):
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
            bpl.set_style()

            xs = np.arange(0, 10, 0.1)
            ys = xs**2

            fig, ax = bpl.subplots()
            ax.plot(xs, ys)
            ax.add_labels("X value", "Y value", "Title")
        """
        if x_label is not None:
            self.set_xlabel(x_label, *args, **kwargs)
        if y_label is not None:
            self.set_ylabel(y_label, *args, **kwargs)
        if title is not None:
            self.set_title(title, *args, **kwargs)

    def set_limits(self, x_min=None, x_max=None, y_min=None, y_max=None, **kwargs):
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
            bpl.set_style()

            xs = np.arange(0, 10, 0.01)
            ys = np.cos(xs)

            fig, [ax1, ax2] = bpl.subplots(ncols=2)

            ax1.plot(xs, ys)

            ax2.plot(xs, ys)
            ax2.set_limits(0, 2*np.pi, -1.1, 1.1)
        """
        # Any None values won't change the plot any.
        self.set_xlim([x_min, x_max], **kwargs)
        self.set_ylim([y_min, y_max], **kwargs)

    def add_text(self, x, y, text, coords="data", **kwargs):
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
            bpl.set_style()

            xs = np.arange(0, 7, 0.1)
            ys = xs**2

            bpl.plot(xs, ys)
            bpl.add_text(2, 30, "(2, 30) data", ha="center", va="center")
            bpl.add_text(0.6, 0.2, "60% across, 20% up", "axes")
        """

        # this function takes care of the transform keyword already, so don't
        # allow the user to specify it.
        if "transform" in kwargs:
            raise ValueError(
                "add_text takes care of the transform for you when"
                " you specify coords. \n"
                "Don't specify transform in this function."
            )

        # set the proper coordinate transformation
        if coords == "data":
            transform = self.transData
        elif coords == "axes":
            transform = self.transAxes
        else:
            raise ValueError("`coords` must be either 'data' or 'axes'")
        # putting it in kwargs makes it easier to pass on.
        kwargs["transform"] = transform

        # add the text
        return self.text(x, y, text, **kwargs)

    def remove_labels(self, labels_to_remove):
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
            bpl.set_style()

            xs = np.arange(0, 5, 0.1)
            ys = xs**2

            fig, ax = bpl.subplots()

            ax.plot(xs, ys)

            ax.remove_labels("y")
            ax.remove_ticks("top")
            ax.add_labels("Conceptual plot", "Axes labels still work")

        """
        # validate their input
        if labels_to_remove not in ["both", "x", "y"]:
            raise ValueError('Please pass in either "x", "y", or "both".')

        # then set the tick parameters.
        self.tick_params(
            axis=labels_to_remove,
            bottom=False,
            top=False,
            left=False,
            right=False,
            labelbottom=False,
            labeltop=False,
            labelleft=False,
            labelright=False,
        )

    def legend(self, linewidth=0, *args, **kwargs):
        """
        Create a nicer looking legend.

        Works by calling the ax.legend() function with the given args and
        kwargs. If some are not specified, they will be filled with values that
        make the legend look nice.

        :param linewidth: linewidth of the border of the legend. Defaults to
                          zero.
        :type linewidth: float
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
            bpl.set_style()

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

            bpl.set_style()

            x = np.arange(0, 5, 0.1)

            bpl.plot(x, x, label="x")
            bpl.plot(x, 2*x, label="2x")
            bpl.plot(x, 3*x, label="3x")
            bpl.legend(fontsize=20, loc=6, title="Title")
        """

        # push the legend a little farther away from the edge.
        kwargs.setdefault("borderaxespad", 0.75)

        leg = super(Axes_bpl, self).legend(*args, **kwargs)

        # TODO: set the fontsize of the title properly. The best way to do it is
        # probably to get the font from one of the other text objects, then
        # increment that slightly, then set the title's fontsize to be that.
        # the fontsize param doesn't change the title, so do that manually
        # title = legend.get_title()
        # title.set_fontsize(kwargs['fontsize'])

        if leg is not None:
            # turn the background into whatever color it needs to be
            frame = leg.get_frame()
            frame.set_linewidth(linewidth)

        return leg

    def equal_scale(self):
        """
        Makes the x and y axes have the same scale.

        Useful for plotting things like ra and dec, something with the same
        quantity on both axes, or anytime the x and y axis have the same scale. It also
        works when both axes are in log (making one dex the same on both axes) or when
        only one axis is in log (one dex = one unit in linear space).

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

            bpl.set_style()

            # make a Gaussian with more spread in y direction
            xs = np.random.normal(0, 1, 1000)
            ys = np.random.normal(0, 2, 1000)

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

            bpl.set_style()

            # make a Gaussian with more spread in y direction
            xs = np.random.normal(0, 1, 1000)
            ys = np.random.normal(0, 2, 1000)

            fig, [ax1, ax2] = bpl.subplots(figsize=[12, 5], ncols=2)

            ax1.scatter(xs, ys)
            ax2.scatter(xs, ys)

            ax1.equal_scale()
            ax2.equal_scale()

            ax1.set_limits(-10, 10, -4, 4)
            ax2.set_limits(-5, 5, -10, 10)

        And here's a demonstration of using this with log scaled axes

        .. plot::
            :include-source:

            import betterplotlib as bpl
            import numpy as np

            bpl.set_style()

            xs = np.random.normal(0, 1, 1000)
            ys = 10 ** np.random.normal(0, 0.5, 1000)

            fig, ax = bpl.subplots()

            ax.scatter(xs, ys)
            ax.set_yscale("log")
            ax.set_limits(-3, 3, 10**-3, 10**3)
            ax.equal_scale()

        """
        self.set_aspect("equal", adjustable="box")

    def easy_add_text(self, text, location, **kwargs):
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
            bpl.set_style()

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
            bpl.set_style()

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
        if (
            "ha" in kwargs
            or "va" in kwargs
            or "horizontalalignment" in kwargs
            or "verticalalignment" in kwargs
        ):
            raise ValueError("This function controls the alignment. Do not pass it in.")

        # then check each different case, and set the parameters we want to use.
        if location == 1 or location == "lower left":
            x_value = 0.04
            y_value = 0.04
            kwargs["horizontalalignment"] = "left"
            kwargs["verticalalignment"] = "bottom"
        elif location == 2 or location == "lower center":
            x_value = 0.5
            y_value = 0.04
            kwargs["horizontalalignment"] = "center"
            kwargs["verticalalignment"] = "bottom"
        elif location == 3 or location == "lower right":
            x_value = 0.96
            y_value = 0.04
            kwargs["horizontalalignment"] = "right"
            kwargs["verticalalignment"] = "bottom"
        elif location == 4 or location == "center left":
            x_value = 0.04
            y_value = 0.5
            kwargs["horizontalalignment"] = "left"
            kwargs["verticalalignment"] = "center"
        elif location == 5 or location == "center":
            x_value = 0.5
            y_value = 0.5
            kwargs["horizontalalignment"] = "center"
            kwargs["verticalalignment"] = "center"
        elif location == 6 or location == "center right":
            x_value = 0.96
            y_value = 0.5
            kwargs["horizontalalignment"] = "right"
            kwargs["verticalalignment"] = "center"
        elif location == 7 or location == "upper left":
            x_value = 0.04
            y_value = 0.96
            kwargs["horizontalalignment"] = "left"
            kwargs["verticalalignment"] = "top"
        elif location == 8 or location == "upper center":
            x_value = 0.5
            y_value = 0.96
            kwargs["horizontalalignment"] = "center"
            kwargs["verticalalignment"] = "top"
        elif location == 9 or location == "upper right":
            x_value = 0.96
            y_value = 0.96
            kwargs["horizontalalignment"] = "right"
            kwargs["verticalalignment"] = "top"
        else:
            raise ValueError("loc was not specified properly.")

        # then add the text.
        return self.add_text(x_value, y_value, text, coords="axes", **kwargs)

    def _density_contour_core(
        self,
        xs,
        ys,
        bin_size=None,
        percent_levels=None,
        smoothing=0,
        weights=None,
        log=False,
        labels=False,
        filled=False,
        **kwargs
    ):
        """
        The underlying function to do both filled and unfilled contours. Call
        `density_contour` or `density_contourf` instead of this.

        :param xs: List of x values
        :type xs: list, np.ndarray
        :param ys: List of y values
        :type ys: list, np.ndarray
        :param bin_size: Bin size to use for the underlying 2D histogram. This
                         can either be a scalar, in which case the bin size will
                         be the same in both the x dimensions, or else a two
                         element list, where the first element will be the
                         bin size in the x dimension, and the second will be
                         the bin size in the y dimension.
        :type bin_size: int, float, list
        :param percent_levels: A list describing the levels of the contours that
                               will be drawn. Each value in this list contains
                               a float between zero and 1 (inclusive) that
                               describes how much of that data will be enclosed
                               by a contour. So if you pass [0.25, 0.5, 0.75],
                               there will be three contours drawn, that enclose
                               25%, 50%, and 75% of the data. If this is not
                               passed in, the default is
                               [0.25, 0.5, 0.75, 0.95].
        :type percent_levels: float, list
        :param smoothing: Optional parameter that will allow the contours to be
                          smoothed. Pass in a nonzero value, which will be the
                          standard deviation of the Gaussian kernel use to smooth
                          the histogram. When using this, often choosing smaller
                          bin sizes is advantageous to make a less grainy plot.
                          Has the same format as padding and bin_size, so different
                          smoothing kernels are possible in the x and y directions.
        :type smoothing: int, float, list
        :param weights: A list containing weights for each data point. If these
                        are not passed, all data points will be weighted
                        equally.
        :type weights: list, np.ndarray
        :param log: Whether or not to do the smoothing and bin creation in log
                    space. This should be used if the plot will be done on
                    log-scaled axes.Can either be a single bool, in which case the
                    x and y scales will both be log (or not), or a two element
                    array, where the first is whether the x axis is log, and the
                    second is y. If this is used, the bin_size and smoothing
                    parameters will be interpreted as dex, rather than raw values.
        :type log: bool, list
        :param labels: Whether or not to label the individual contour lines
                       with their percentage level.
        :type labels: bool
        :param filled: True will use filled contours, or False to use hollow ones.
        :type filled: bool
        :param kwargs: Additional keyword arguments to pass on to the original
                       matplotlib contour function.
        :return: output of the matplotlib.contour function.
        """
        # error check weird error matplotlib has when all x and y data are same.
        if len(set(xs)) == len(set(ys)) == 1 and smoothing == 0:
            raise ValueError(
                "All points are identical. This breaks matplotlib "
                "contours for some reason. "
                "Try other data, or smooth."
            )
        # levels is set by this function, so it can't be in there
        if "levels" in kwargs:
            raise ValueError(
                "The levels parameter is set by this function. " "Do not pass it in. "
            )
        # if smoothing is not specified, we still want some padding on the
        # outside so the contours aren't cut off.
        if smoothing == 0:
            try:
                padding = [
                    2 * tools._freedman_diaconis(xs),
                    2 * tools._freedman_diaconis(ys),
                ]
            except ValueError:  # data length too short, will handle in 2d hist
                padding = 0
        else:
            padding = tools._padding_from_smoothing(smoothing)
        hist, x_e, y_e = tools.smart_hist_2d(
            xs,
            ys,
            bin_size,
            padding=padding,
            weights=weights,
            smoothing=smoothing,
            log=log,
        )
        x_cen = tools.bin_centers(x_e)
        y_cen = tools.bin_centers(y_e)

        # then get the levels of the contours
        if percent_levels is None:
            percent_levels = [0, 0.25, 0.5, 0.75, 0.95]
        else:
            not_list_msg = "Percent_levels needs to be a numeric list."
            percent_levels = type_checking.numeric_list_1d(percent_levels, not_list_msg)
            # add zero level to have center region full
            percent_levels = np.insert(percent_levels, 0, 0)

        levels = tools.percentile_level(hist.flatten(), percent_levels)
        # then check that the levels are increasing and without duplicates
        if len(set(levels)) < len(levels):
            raise ValueError(
                "The percent levels chosen lead to duplicate "
                "levels.\nContour levels must be increasing."
            )
        kwargs["levels"] = levels

        # set the normalization to ignore the central dummy level. But I don't want
        # either level to be at the edge of the colormap, since those are often white
        # or black
        vmin = levels[0]
        vmax = levels[-2]
        vmin -= 0.1 * (vmax - vmin)
        vmax += 0.1 * (vmax - vmin)
        kwargs["norm"] = mpl_colors.Normalize(vmin=vmin, vmax=vmax)

        if not filled:
            kwargs.setdefault("zorder", 3)
            kwargs.setdefault("linewidths", 2)
            contours = super(Axes_bpl, self).contour(x_cen, y_cen, hist, **kwargs)
        else:
            kwargs.setdefault("zorder", 2)
            contours = super(Axes_bpl, self).contourf(x_cen, y_cen, hist, **kwargs)

        if labels:
            # need to order the percent_levels properly (from high to low)
            percent_levels = sorted(percent_levels)[::-1]
            label_percents = percent_levels + [0]
            # needed since there is one hidden coutour at the very center.
            label_dict = {
                l: "{:.1f}%".format(percent * 100)
                for l, percent in zip(levels, label_percents)
            }

            self.clabel(contours, fmt=label_dict, fontsize=16)

        return contours

    def density_contour(
        self,
        xs,
        ys,
        bin_size=None,
        percent_levels=None,
        smoothing=0,
        weights=None,
        log=False,
        labels=False,
        **kwargs
    ):
        """
        Creates contours over a 2D histogram of data density.

        Here you pass in the location and weights of all data points, then
        this will calculate the 2D histogram with smartly chosen bin size,
        and put contours over the top of that histogram.

        These contours are just lines, not filled regions. Check out
        `density_contourf()` for that.

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
        :param percent_levels: A list describing the levels of the contours that
                               will be drawn. Each value in this list contains
                               a float between zero and 1 (inclusive) that
                               describes how much of that data will be enclosed
                               by a contour. So if you pass [0.25, 0.5, 0.75],
                               there will be three contours drawn, that enclose
                               25%, 50%, and 75% of the data. If this is not
                               passed in, the default is
                               [0.25, 0.5, 0.75, 0.95].
        :type percent_levels: float, list
        :param smoothing: Optional parameter that will allow the contours to be
                          smoothed. Pass in a nonzero value, which will be the
                          standard deviation of the Gaussian kernel use to smooth
                          the histogram. When using this, often choosing smaller
                          bin sizes is advantageous to make a less grainy plot.
                          Has the same format as padding and bin_size, so different
                          smoothing kernels are possible in the x and y directions.
        :type smoothing: int, float, list
        :param weights: A list containing weights for each data point. If these
                        are not passed, all data points will be weighted
                        equally.
        :type weights: list, np.ndarray
        :param log: Whether or not to do the smoothing and bin creation in log
                    space. This should be used if the plot will be done on
                    log-scaled axes.Can either be a single bool, in which case the
                    x and y scales will both be log (or not), or a two element
                    array, where the first is whether the x axis is log, and the
                    second is y. If this is used, the bin_size and smoothing
                    parameters will be interpreted as dex, rather than raw values.
        :type log: bool, list
        :param labels: Whether or not to label the individual contour lines
                       with their percentage level.
        :type labels: bool
        :param kwargs: Additional keyword arguments to pass on to the original
                       matplotlib contour function.
        :return: output of the matplotlib.contour function.

        .. plot::
            :include-source:

            import betterplotlib as bpl
            import numpy as np

            bpl.set_style()

            xs = np.concatenate(
                [
                    np.random.normal(3, 2, 1000),
                    np.random.normal(7, 2, 1000),
                ]
            )
            ys = np.concatenate(
                [
                    np.random.normal(7, 2, 1000),
                    np.random.normal(3, 2, 1000),
                ]
            )

            bpl.density_contour(xs, ys, bin_size=0.01, smoothing=0.5, cmap="inferno")
            bpl.set_limits(0, 10, 0, 10)
            bpl.equal_scale()

        .. plot::
            :include-source:

            import betterplotlib as bpl
            import numpy as np

            bpl.set_style()

            xs = np.concatenate(
                [
                    np.random.normal(3, 2, 1000),
                    np.random.normal(7, 2, 1000),
                ]
            )
            ys = 10 ** np.concatenate(
                [
                    np.random.normal(7, 2, 1000),
                    np.random.normal(3, 2, 1000),
                ]
            )

            fig, ax = bpl.subplots()
            ax.density_contour(
                xs, ys, bin_size=0.01, smoothing=0.5, log=[False, True], cmap="inferno"
            )
            ax.set_yscale("log")
            ax.set_limits(0, 10, 1, 1e10)
            bpl.equal_scale()
        """
        return self._density_contour_core(
            xs,
            ys,
            bin_size=bin_size,
            percent_levels=percent_levels,
            smoothing=smoothing,
            weights=weights,
            log=log,
            labels=labels,
            filled=False,
            **kwargs
        )

    def density_contourf(
        self,
        xs,
        ys,
        bin_size=None,
        percent_levels=None,
        smoothing=0,
        weights=None,
        log=False,
        **kwargs
    ):
        """
        Creates filled contours over a 2D histogram of data density.

        Here you pass in the location and weights of all data points, then
        this will calculate the 2D histogram with smartly chosen bin size,
        and put contours over the top of that histogram.

        These contours are just filled regions with no lines. Check out
        `density_contour()` for that.

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
        :param percent_levels: A list describing the levels of the contours that
                               will be drawn. Each value in this list contains
                               a float between zero and 1 (inclusive) that
                               describes how much of that data will be enclosed
                               by a contour. So if you pass [0.25, 0.5, 0.75],
                               there will be three contours drawn, that enclose
                               25%, 50%, and 75% of the data. If this is not
                               passed in, the default is
                               [0.25, 0.5, 0.75, 0.95].
        :type percent_levels: float, list
        :param smoothing: Optional parameter that will allow the contours to be
                          smoothed. Pass in a nonzero value, which will be the
                          standard deviation of the Gaussian kernel use to smooth
                          the histogram. When using this, often choosing smaller
                          bin sizes is advantageous to make a less grainy plot.
                          Has the same format as padding and bin_size, so different
                          smoothing kernels are possible in the x and y directions.
        :type smoothing: int, float, list
        :param weights: A list containing weights for each data point. If these
                        are not passed, all data points will be weighted
                        equally.
        :type weights: list, np.ndarray
        :param log: Whether or not to do the smoothing and bin creation in log
                    space. This should be used if the plot will be done on
                    log-scaled axes.Can either be a single bool, in which case the
                    x and y scales will both be log (or not), or a two element
                    array, where the first is whether the x axis is log, and the
                    second is y. If this is used, the bin_size and smoothing
                    parameters will be interpreted as dex, rather than raw values.
        :type log: bool, list
        :param kwargs: Additional keyword arguments to pass on to the original
                       matplotlib contour function.
        :return: output of the matplotlib.contourf function.

        .. plot::
            :include-source:

            import betterplotlib as bpl
            import numpy as np

            bpl.set_style()

            xs = np.concatenate(
                [
                    np.random.normal(3, 2, 1000),
                    np.random.normal(7, 2, 1000),
                ]
            )
            ys = np.concatenate(
                [
                    np.random.normal(7, 2, 1000),
                    np.random.normal(3, 2, 1000),
                ]
            )

            bpl.density_contourf(xs, ys, bin_size=0.01, smoothing=0.5, cmap="inferno")
            bpl.set_limits(0, 10, 0, 10)
            bpl.equal_scale()

        .. plot::
            :include-source:

            import betterplotlib as bpl
            import numpy as np

            bpl.set_style()

            xs = 10 ** np.concatenate(
                [
                    np.random.normal(3, 2, 1000),
                    np.random.normal(7, 2, 1000),
                ]
            )
            ys = np.concatenate(
                [
                    np.random.normal(7, 2, 1000),
                    np.random.normal(3, 2, 1000),
                ]
            )

            fig, ax = bpl.subplots()
            ax.density_contourf(
                xs, ys, bin_size=0.01, smoothing=0.5, log=[True, False], cmap="inferno"
            )
            ax.set_xscale("log")
            ax.set_limits(1, 1e10, 0, 10)
            bpl.equal_scale()
        """
        # don't let user use the labels param here like they can in contour
        if "labels" in kwargs:
            raise ValueError("Filled contours cannot have labels.")
        return self._density_contour_core(
            xs,
            ys,
            bin_size=bin_size,
            percent_levels=percent_levels,
            smoothing=smoothing,
            weights=weights,
            log=log,
            labels=False,
            filled=True,
            **kwargs
        )

    def contour_scatter(
        self,
        xs,
        ys,
        bin_size=None,
        percent_levels=None,
        smoothing=0,
        weights=None,
        labels=False,
        fill_cmap="white",
        scatter_kwargs=None,
        contour_kwargs=None,
        contourf_kwargs=None,
    ):
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
        :param percent_levels: A list describing the levels of the contours that
                               will be drawn. Each value in this list contains
                               a float between zero and 1 (inclusive) that
                               describes how much of that data will be enclosed
                               by a contour. So if you pass [0.25, 0.5, 0.75],
                               there will be three contours drawn, that enclose
                               25%, 50%, and 75% of the data. If this is not
                               passed in, the default is
                               [0.25, 0.5, 0.75, 0.95].
        :type percent_levels: float, list
        :param smoothing: Optional parameter that will allow the contours to be
                          smoothed. Pass in a nonzero value, which will be the
                          standard deviation of the Gaussian kernel use to smooth
                          the histogram. When using this, often choosing smaller
                          bin sizes is advantageous to make a less grainy plot.
                          Has the same format as padding and bin_size, so different
                          smoothing kernels are possible in the x and y directions.
        :type smoothing: int, float, list
        :param weights: A list containing weights for each data point. If these
                        are not passed, all data points will be weighted
                        equally.
        :type weights: list, np.ndarray
        :param labels: Whether or not to label the individual contour lines
                       with their percentage level.
        :type labels: bool
        :param fill_cmap: The colormap used for the filled regions. Can be
                          a strong with any named matplotlib colormap or a
                          colormap object. In addition, there are some special
                          strings that can be used. "white", which is just a
                          solid white fill, is the default.  "background_grey"
                          gives a solid fill that is the same color as the
                          make_ax_dark() background. "modified_greys" is a
                          colormap that starts at the "background_grey" color,
                          then transitions to black.
        :type fill_cmap: str, matplotlib.colors.LinearSegmentedColormap
        :param scatter_kwargs: Dictionary of additional parameters that will be
                               passed to the underlying matplotlib scatter
                               function used for points in the outer regions.
        :type scatter_kwargs: dict
        :param contour_kwargs: Dictionary of additional parameters that will be
                               passed to the underlying matplotlib contour
                               function.
        :type contour_kwargs: dict
        :param contourf_kwargs: Dictionary of additional parameters that will be
                                passed to the underlying matplotlib contourf
                                function.
        :type contourf_kwargs: dict

        Examples

        First, we'll show why this plot is useful. This won't use any of the
        fancy settings, other than `bin_size`, which is used to make the
        contours look nicer.

        .. plot::
            :include-source:

            import numpy as np
            import betterplotlib as bpl

            bpl.set_style()

            xs = np.concatenate(
                [
                    np.random.normal(0, 1, 100000),
                    np.random.normal(3, 1, 100000),
                    np.random.normal(0, 1, 100000),
                ]
            )
            ys = np.concatenate(
                [
                    np.random.normal(0, 1, 100000),
                    np.random.normal(3, 1, 100000),
                    np.random.normal(3, 1, 100000),
                ]
            )

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

            bpl.set_style()

            xs = np.concatenate(
                [
                    np.random.normal(0, 1, 10000),
                    np.random.normal(3, 1, 10000),
                    np.random.normal(0, 1, 10000),
                ]
            )
            ys = np.concatenate(
                [
                    np.random.normal(0, 1, 10000),
                    np.random.normal(3, 1, 10000),
                    np.random.normal(3, 1, 10000),
                ]
            )

            fig, (ax1, ax2, ax3) = bpl.subplots(ncols=3, figsize=[15, 5])

            ax1.contour_scatter(xs, ys, bin_size=0.2)
            ax2.contour_scatter(xs, ys, bin_size=0.3)
            ax3.contour_scatter(xs, ys, bin_size=0.5)

        You can see how small values of `bin_size` lead to more noisy contours.
        The code will attempt to choose its own value of `bin_size` if nothing
        is specified, but it's normally not a very good choice.

        Adjusting the smoothing is often the better way to control the
        noise.

        .. plot::
            :include-source:

            import numpy as np
            import betterplotlib as bpl

            bpl.set_style()

            xs = np.concatenate(
                [
                    np.random.normal(0, 1, 10000),
                    np.random.normal(3, 1, 10000),
                    np.random.normal(0, 1, 10000),
                ]
            )
            ys = np.concatenate(
                [
                    np.random.normal(0, 1, 10000),
                    np.random.normal(3, 1, 10000),
                    np.random.normal(3, 1, 10000),
                ]
            )

            fig, (ax1, ax2, ax3) = bpl.subplots(ncols=3, figsize=[15, 5])

            ax1.contour_scatter(xs, ys, bin_size=0.1, smoothing=0.1)
            ax2.contour_scatter(xs, ys, bin_size=0.1, smoothing=0.2)
            ax3.contour_scatter(xs, ys, bin_size=0.1, smoothing=0.3)

        The weights behave exactly the same as they do in the other density
        contour functions. Here we just have 4 points, but with different
        weights. We also show the different smoothing for different axes, and
        the labels.

        .. plot::
            :include-source:

            import betterplotlib as bpl

            bpl.set_style()

            xs = [1, 2, 3, 4]
            ys = [1, 2, 3, 4]
            weights = [1, 2, 3, 4]
            bpl.contour_scatter(
                xs,
                ys,
                weights=weights,
                bin_size=0.01,
                smoothing=[0.8, 0.3],
                fill_cmap="Blues",
                labels=True,
                contour_kwargs={"colors": "k"},
            )
            bpl.equal_scale()

        Now we can mess with the fun stuff, which is the `fill_cmap` param and
        the kwargs that get passed to the `scatter`, `contour`, and `contourf`
        function calls. There is a lot of stuff going on here, just for
        demonstration purposes. Note that the code has some default parameters
        that it will choose if you don't specify anything.

        .. plot::
            :include-source:

            import numpy as np
            import betterplotlib as bpl

            bpl.set_style()

            xs = np.concatenate(
                [
                    np.random.normal(0, 1, 10000),
                    np.random.normal(3, 1, 10000),
                    np.random.normal(0, 1, 10000),
                ]
            )
            ys = np.concatenate(
                [
                    np.random.normal(0, 1, 10000),
                    np.random.normal(3, 1, 10000),
                    np.random.normal(3, 1, 10000),
                ]
            )

            fig, axs = bpl.subplots(nrows=2, ncols=2)
            [ax1, ax2], [ax3, ax4] = axs

            percent_levels = [0.99, 0.7, 0.3]
            smoothing = 0.2
            bin_size = 0.1

            ax1.contour_scatter(
                xs,
                ys,
                bin_size=bin_size,
                percent_levels=percent_levels,
                smoothing=smoothing,
                fill_cmap="background_grey",
                contour_kwargs={"cmap": "magma"},
                scatter_kwargs={"s": 10, "c": bpl.almost_black},
            )
            ax1.make_ax_dark()

            # or we can choose our own `fill_cmap`
            ax2.contour_scatter(
                xs,
                ys,
                bin_size=bin_size,
                smoothing=smoothing,
                fill_cmap="viridis",
                percent_levels=percent_levels,
                contour_kwargs={"linewidths": 1, "colors": "white"},
                scatter_kwargs={"s": 50, "c": bpl.color_cycle[3], "alpha": 0.3},
            )

            # There are also my colormaps that work with the dark axes
            ax3.contour_scatter(
                xs,
                ys,
                bin_size=bin_size,
                smoothing=smoothing,
                fill_cmap="modified_greys",
                percent_levels=percent_levels,
                scatter_kwargs={"c": bpl.color_cycle[0]},
                contour_kwargs={
                    "linewidths": [2, 0, 0, 0, 0, 0, 0],
                    "colors": bpl.almost_black,
                },
            )
            ax3.make_ax_dark()

            # the default `fill_cmap` is white.
            new_linestyles = ["solid", "dashed", "dashed", "dashed"]
            ax4.contour_scatter(
                xs,
                ys,
                bin_size=bin_size,
                smoothing=smoothing,
                percent_levels=percent_levels,
                scatter_kwargs={
                    "marker": "^",
                    "linewidth": 0.2,
                    "c": bpl.color_cycle[1],
                    "s": 20,
                },
                contour_kwargs={
                    "linestyles": new_linestyles,
                    "colors": bpl.almost_black,
                },
            )

        Note that the contours will work appropriately for datasets with
        "holes", as demonstrated here.

        .. plot::
            :include-source:

            import numpy as np
            import betterplotlib as bpl
            bpl.set_style()

            rad1 = np.random.normal(10, 0.75, 10000)
            theta1 = np.random.uniform(0, 2 * np.pi, 10000)
            x1 = [r * np.cos(t) for r, t in zip(rad1, theta1)]
            y1 = [r * np.sin(t) for r, t in zip(rad1, theta1)]

            rad2 = np.random.normal(20, 0.75, 20000)
            theta2 = np.random.uniform(0, 2 * np.pi, 20000)
            x2 = [r * np.cos(t) for r, t in zip(rad2, theta2)]
            y2 = [r * np.sin(t) for r, t in zip(rad2, theta2)]

            rad3 = np.random.normal(12, 0.75, 12000)
            theta3 = np.random.uniform(0, 2 * np.pi, 12000)
            x3 = [r * np.cos(t) + 10 for r, t in zip(rad3, theta3)]
            y3 = [r * np.sin(t) + 10 for r, t in zip(rad3, theta3)]

            x4 = np.random.uniform(-20, 20, 3500)
            y4 = x4 + np.random.normal(0, 0.5, 3500)

            y5 = y4 * (-1)

            xs = np.concatenate([x1, x2, x3, x4, x4])
            ys = np.concatenate([y1, y2, y3, y4, y5])

            fig, ax = bpl.subplots()

            ax.contour_scatter(xs, ys, smoothing=0.5, bin_size=0.5)
            ax.equal_scale()
        """

        if scatter_kwargs is None:
            scatter_kwargs = dict()
        if contour_kwargs is None:
            contour_kwargs = dict()
        if contourf_kwargs is None:
            contourf_kwargs = dict()

        # determine what our colormap for the fill will be
        if fill_cmap == "white":
            # colormap with one color: white
            fill_cmap = mpl_colors.ListedColormap(colors="white", N=1)
        elif fill_cmap == "background_grey":
            # colormap with one color: the light grey used in backgrounds
            fill_cmap = mpl_colors.ListedColormap(colors=colors.light_gray, N=1)
        elif fill_cmap == "modified_greys":
            # make one that transitions from light grey to black
            new_colors = [colors.light_gray, "black"]
            fill_cmap = mpl_colors.LinearSegmentedColormap.from_list(
                "mod_gray", new_colors
            )

        # then we can set a bunch of default parameters for the contours
        contour_kwargs.setdefault("linewidths", 2)
        contour_kwargs.setdefault("zorder", 3)
        if "colors" not in contour_kwargs:
            contour_kwargs.setdefault("cmap", "viridis")

        # we can then go ahead and plot the filled contours, then the contour lines
        if fill_cmap is not None:
            self.density_contourf(
                xs,
                ys,
                bin_size=bin_size,
                percent_levels=percent_levels,
                smoothing=smoothing,
                weights=weights,
                cmap=fill_cmap,
                **contourf_kwargs
            )
        contours = self.density_contour(
            xs,
            ys,
            bin_size=bin_size,
            percent_levels=percent_levels,
            smoothing=smoothing,
            weights=weights,
            labels=labels,
            **contour_kwargs
        )

        # we saved the output from the contour, since it has information about the
        # shape of the contours we can use to figure out which points are outside
        # and therefore need to be plotted. There may be multiple outside contours,
        # especially if the shape is complicated, so we test to see how many
        # each point is inside. We only do this if the user actually wants to
        # plot these points
        if scatter_kwargs.get("s") != 0:
            shapes_in = np.zeros(len(xs))
            for line in contours.allsegs[0]:  # zero index is lowest level
                # make a closed shape with the line
                polygon = path.Path(line, closed=True)
                shapes_in += polygon.contains_points(list(zip(xs, ys)))

            # the ones that need to be hidden are inside an odd number of
            # shapes. This shounds weird, but actually works. If we have a ring
            # of points, the outliers in the middle will be inside the outermost
            # and innermost contours, so they are inside two shapes. We want to
            # plot these. So we plot the ones that are divisible by two.
            plot_idx = np.where(shapes_in % 2 == 0)

            # We then get these elements. The multiple indexing is only supported for
            # numpy arrays, not Python lists, so convert our values to that first.
            outside_xs = np.array(xs)[plot_idx]
            outside_ys = np.array(ys)[plot_idx]

            # now we can do our scatterplot.
            scatter_kwargs.setdefault("alpha", 1.0)
            scatter_kwargs.setdefault("s", 10)
            if "c" not in scatter_kwargs:
                scatter_kwargs.setdefault("color", colors.almost_black)
            scatter_kwargs.setdefault("zorder", 1)
            self.scatter(outside_xs, outside_ys, **scatter_kwargs)

        return contours

    def data_ticks(self, x_data, y_data, extent=0.015, *args, **kwargs):
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
            bpl.set_style()

            xs = np.random.normal(0, 1, 100)
            ys = np.random.normal(0, 1, 100)

            bpl.scatter(xs, ys)
            bpl.data_ticks(xs, ys)
        """
        kwargs.setdefault("color", colors.almost_black)
        kwargs.setdefault("linewidth", 0.5)

        for x in x_data:
            self.axvline(x, ymin=0, ymax=extent, *args, **kwargs)

        # Since the matplotlib command to ax(h/v)line uses an extent based on
        # percentage of the way to the end, to get the same physical size for
        # both axes, we have to scale based on the size of the axes
        h_extent = (self.bbox.height / self.bbox.width) * extent
        for y in y_data:
            self.axhline(y, xmin=0, xmax=h_extent, *args, **kwargs)

    def plot(self, *args, **kwargs):
        """
        A slightly improved plot function.

        This is best used for plotting lines, while the `scatter()` function
        is best used for plotting points.

        Currently all this does is make the lines thicker, which looks better.
        There isn't any added functionality.

        The parameters here are the exact same as they are for the regular
        `plt.plot()` or `ax.plot()` functions.

        :param args: Additional arguments to pass to the `plot` function
        :param kwargs: Additional keyword arguments to pass to the `plot` function

        .. plot::
            :include-source:

            import numpy as np
            import betterplotlib as bpl
            import matplotlib.pyplot as plt
            bpl.set_style()

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
        # set the linewidth to a thicker value. There are two keys here, though,
        # so we have to be careful.
        if not ("lw" in kwargs or "linewidth" in kwargs):
            kwargs.setdefault("lw", 3)

        return super(Axes_bpl, self).plot(*args, **kwargs)

    def axvline(self, x=0, *args, **kwargs):
        """
        Place a vertical line at some point on the axes.

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
            bpl.set_style()

            left_xs = np.arange(-20, 1, 0.01)
            right_xs = np.arange(1.001, 20, 0.01)
            left_ys = left_xs / (left_xs - 1)
            right_ys = right_xs / (right_xs - 1)

            bpl.make_ax_dark()
            bpl.plot(left_xs, left_ys, c=bpl.color_cycle[2])
            bpl.plot(right_xs, right_ys, c=bpl.color_cycle[2])
            bpl.axvline(1.0, linestyle="--")
            bpl.axhline(1.0, linestyle="--")
            bpl.set_limits(-10, 10, -10, 10)

        """

        # set the color to be almost black. Matplotlib has two keywords for
        # color, so we need to check both here.
        if not ("c" in kwargs or "color" in kwargs):
            kwargs.setdefault("c", colors.almost_black)

        return super(Axes_bpl, self).axvline(x, *args, **kwargs)

    def axhline(self, y=0, *args, **kwargs):
        """
        Place a horizontal line at some point on the axes.

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
            bpl.set_style()

            left_xs = np.arange(-20, 1, 0.01)
            right_xs = np.arange(1.001, 20, 0.01)
            left_ys = left_xs / (left_xs - 1)
            right_ys = right_xs / (right_xs - 1)

            bpl.make_ax_dark()
            bpl.plot(left_xs, left_ys, c=bpl.color_cycle[2])
            bpl.plot(right_xs, right_ys, c=bpl.color_cycle[2])
            bpl.axvline(1.0, linestyle="--")
            bpl.axhline(1.0, linestyle="--")
            bpl.set_limits(-10, 10, -10, 10)

        """

        # set the color to be almost black. Matplotlib has two keywords for
        # color, so we need to check both here.
        if not ("c" in kwargs or "color" in kwargs):
            kwargs.setdefault("c", colors.almost_black)

        return super(Axes_bpl, self).axhline(y, *args, **kwargs)

    def errorbar(self, *args, **kwargs):
        """
        Wrapper for the plt.errorbar() function.

        Style changes: capsize is automatically zero, and the format is
        automatically a scatter plot, rather than the connected lines that
        are used by default otherwise. It also adds a black marker edge to
        distinguish the markers when there are lots of data poitns. Otherwise
        everything blends together.

        :param args: Additional arguments to pass to the `errorbar` function
        :param kwargs: Additional keyword arguments to pass to the `errorbar` function

        .. plot::
            :include-source:

            import numpy as np
            import betterplotlib as bpl
            import matplotlib.pyplot as plt
            bpl.set_style()

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

        kwargs.setdefault("capsize", 0)
        kwargs.setdefault("fmt", "o")
        kwargs.setdefault("markeredgewidth", 0.25)
        kwargs.setdefault("markeredgecolor", colors.almost_black)

        return super(Axes_bpl, self).errorbar(*args, **kwargs)

    def twin_axis_simple(self, axis, lower_lim, upper_lim, label="", log=False):
        """
        Creates a differently scaled axis on either the top or the left.

        Note that this only does simple scalings of the new axes, which will
        still only be linear or log scaled axes. If you want a function that
        smartly places labels based on a function that takes one set of axes
        values to another (in a potentially nonlinear way), the other function
        I haven't made will do that.

        :param axis: Where the new scaled axis will be placed. Must
                     either be "x" or "y".
        :type axis: str
        :param lower_lim: Value to be put on the left/bottom of the newly
                          created axis.
        :type lower_lim: float
        :param upper_lim: Value to be put on the right/top of the newly
                          created axis.
        :type upper_lim: float
        :param label: The label to put on this new axis.
        :type label: str
        :param log: Whether or not to log scale this axis.
        :type log: bool
        :returns: the new axes

        .. plot::
            :include-source:

            import betterplotlib as bpl
            bpl.set_style()

            bpl.set_limits(0, 10, 0, 5)
            bpl.add_labels("x", "y")
            bpl.twin_axis_simple("x", 0, 100, "$10 x$")
            bpl.twin_axis_simple("y", 1, 10**5, "$10^y$", log=True)

        Note that for a slightly more complicated version of this plot, say if
        we wanted the top x axis to be x^2 rather than 10x, the limits would
        still be the same, but since the new axis will always be a linear or log
        scale the new axis won't represent the true relationship between the
        variables on the twin axes. See `twin_axis` for that.


        """

        if axis == "x":
            new_ax = super(Axes_bpl, self).twiny()
            new_ax.set_xlim(lower_lim, upper_lim)
            if log:
                new_ax.set_xscale("log")
            new_ax.set_xlabel(label)
        elif axis == "y":
            new_ax = super(Axes_bpl, self).twinx()
            new_ax.set_ylim(lower_lim, upper_lim)
            if log:
                new_ax.set_yscale("log")
            new_ax.set_ylabel(label)
        else:
            raise ValueError("Axis must be either 'x' or 'y'. ")

        return new_ax

    def twin_axis(
        self, axis, new_ticks, label, old_to_new_func=None, new_to_old_func=None
    ):
        """
        Create a twin axis, where the new axis values are an arbitrary function
        of the old values.

        This is used when you want to put two related quantities on the axis,
        for example distance/redshift in astronomy, where one isn't a simple
        scaling of the other. If you want a simple linear or log scale, use the
        `twin_axis_simple` function. This one will create a new axis that is
        an arbitrary scale.

        :param axis: Whether the new axis labels will be on the "x" or "y" axis.
                     If "x" is chosen this will place the markers on the top
                     botder of the plot, while "y" will place the values on the
                     left border of the plot. "x" and "y" are the only
                     allowed values.
        :type axis: str
        :param new_ticks: List of of locations (in the new data values) to place
                          ticks. Any values outside the range of the plot
                          will be ignored.
        :type new_ticks: list, np.ndarray
        :param label: The label given to the newly created axis.
        :type label: str
        :param old_to_new_func: Function that takes values on the original axis
                                and transforms them to corresponding values
                                on the soon-to-be created axis. Either this
                                parameter or `new_to_old_func` can be used, but
                                not both.
        :param new_to_old_func: Function that takes values on the
                                soon-to-be-created axis and transforms them to
                                corresponding values on the original axis.
                                Either this parameter or `old_to_new_func` can
                                be used, but not both.
        :return: New axis object that was created, containing the newly
                 created labels.

        .. plot::
            :include-source:

            import betterplotlib as bpl
            bpl.set_style()

            def square(x):
                return x**2

            def cubed(x):
                return x**3

            fig, ax = bpl.subplots(figsize=[5, 5], tight_layout=True)
            ax.set_limits(0, 10, 0, 10.0001)  # to avoid floating point errors
            ax.add_labels("x", "y")
            ax.twin_axis("y", [0, 10, 30, 60, 100], "$y^2$", square)
            ax.twin_axis("x", [0, 10, 100, 400, 1000], "$x^3$", cubed)

        Note that we had to be careful with floating point errors when one of
        the markers we want is exactly on the edge. Make the borders slightly
        larger to ensure that all labels fit on the plot.

        There are two ways to give the funtion that transforms the values from
        one axis to the other. The parameter `old_to_new_func` (used as the
        last parameter in the plot above) takes values on the original axis and
        transforms them to values on the newly created axis. However, the
        parameter `new_to_old_func` does the inverse, taking values on the
        new axis and transforming them to the currently existing one. Only one
        of these two parameters can be provided. Identical plots can be created
        with either function, but due to specifics of the implementation, using
        the `new_to_old_func` parameter is slightly more computationally
        efficient. Here's an example of an identical plot to the first created
        with `new_to_old_func` instead.


        .. plot::
            :include-source:

            import numpy as np
            import betterplotlib as bpl

            bpl.set_style()

            def cube_root(x):
                return x ** (1.0 / 3.0)

            fig, ax = bpl.subplots(figsize=[5, 5], tight_layout=True)
            ax.set_limits(0, 10, 0, 10.0001)  # to avoid floating point errors
            ax.add_labels("x", "y")
            ax.twin_axis("y", [0, 10, 30, 60, 100], "$y^2$", new_to_old_func=np.sqrt)
            ax.twin_axis(
                "x", [0, 10, 100, 400, 1000], "$x^3$", new_to_old_func=cube_root
            )

        This function will ignore values for the ticks that are outside the
        limits of the plot. The following plot isn't the most useful, since
        it could be done with the `axis_twin_simple`, but it gets the idea
        across.

        .. plot::
            :include-source:

            import betterplotlib as bpl
            import numpy as np
            bpl.set_style()

            xs = np.logspace(0, 3, 100)

            fig, ax = bpl.subplots(figsize=[5, 5], tight_layout=True)
            ax.plot(xs, xs)
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.add_labels("x", "y")
            # extraneous values are ignored.
            ax.twin_axis("x", [-1, 0, 1, 2, 3, 4, 5], "log(x)", np.log10)
            ax.twin_axis("y", [-1, 0, 1, 2, 3, 4, 5], "log(y)", np.log10)

        """

        # support for automatically adding new ticks is not yet supported. You
        # have to pass your own in.
        #     if new_ticks is None:
        #         if axis == "x":
        #             new_ticks = create_new_bins(func, ax.get_xticks())
        #         elif axis == "y":
        #             new_ticks = create_new_bins(func, ax.get_yticks())

        # implementation details: The data values for the old axes will be used
        # as the data values for the new scaled axis. This ensures that they
        # will line up with each other. However, we will set the label text
        # to be the values the user passes in.

        if old_to_new_func is None and new_to_old_func is None:
            raise ValueError(
                "Either `old_to_new_func` or `new_to_old_func` " "must be provided."
            )
        if old_to_new_func is not None and new_to_old_func is not None:
            raise ValueError(
                "Don't provide both `old_to_new_func` and "
                "`new_to_old_func`.\nUsing `new_to_old_func` is "
                "more efficient, so provide only that."
            )

        # depending on which axis the user wants to use, we have to get
        # different things.
        if axis == "y":
            new_ax = self.twinx()  # shares y axis
            old_min, old_max = self.get_ylim()
            lim_func = new_ax.set_ylim  # function to set limits
            new_axis = new_ax.yaxis
            new_ax.set_ylabel(label)
            # the new axis needs to share the same scaling as the old
            if self.get_yscale() == "log":
                new_ax.set_yscale("log")
                # if we have log in old, we don't want minor ticks on the new
                new_axis.set_tick_params(which="minor", length=0)
            new_ax.set_ylabel(label)
        elif axis == "x":
            new_ax = self.twiny()  # shares x axis
            old_min, old_max = self.get_xlim()
            lim_func = new_ax.set_xlim  # function to set limits
            new_axis = new_ax.xaxis
            new_ax.set_xlabel(label)
            # the new axis needs to share the same scaling as the old
            if self.get_xscale() == "log":
                new_ax.set_xscale("log")
                # if we have log in old, we don't want minor ticks on the new
                new_axis.set_tick_params(which="minor", length=0)
        else:
            raise ValueError("`axis` must either be 'x' or 'y'. ")

        # set the limits using the function we got earlier. We use the values
        # of the old axies for the underlying data
        lim_func(old_min, old_max)

        # then determine the locations to put the new ticks, in terms of the
        # old values
        tick_locs_in_old = []
        new_ticks_good = []
        if new_to_old_func is not None:
            for new_value in new_ticks:
                # we can directly use the function to go from the new ticks to
                # the values on the old axis that correspond
                old_data_loc = new_to_old_func(new_value)
                # then check if it's within the original axis range
                if old_min <= old_data_loc <= old_max:
                    tick_locs_in_old.append(old_data_loc)
                    new_ticks_good.append(new_value)
        else:
            for new_value in new_ticks:
                # determine the value on the original axis corresponding to
                # each tick. Since we have the function transforming the old
                # ticks to the new ones, we have to invert it
                # define a function to minimize so scipy can work.
                def minimize(x):
                    return abs(old_to_new_func(x) - new_value)

                # ignore numpy warnings here, everything is fine.
                with np.errstate(all="ignore"):
                    old_data_loc = optimize.minimize_scalar(minimize).x
                    # then check if it's within the original axis range
                    if old_min <= old_data_loc <= old_max:
                        tick_locs_in_old.append(old_data_loc)
                        new_ticks_good.append(new_value)

        # then put the ticks at the locations of the old data, but label them
        # with the value of the transformed data.
        new_axis.set_ticks(tick_locs_in_old)
        new_axis.set_ticklabels(new_ticks_good)

        return new_ax

    def shaded_density(
        self,
        xs,
        ys,
        bin_size=None,
        smoothing=0,
        cmap="Greys",
        weights=None,
        log_xy=False,
        log_hist=False,
    ):
        """
        Creates shaded regions showing the density.

        Is essentially a 2D histogram, but supports smoothing. Under the hood,
        this uses the  pcolormesh function in matplotlib.

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
        :param smoothing: Optional parameter that will smooth the shaded density.
                          Pass in a nonzero value, which will be the
                          standard deviation of the Gaussian kernel use to smooth
                          the histogram. When using this, often choosing smaller
                          bin sizes is advantageous to make a less grainy plot.
                          Has the same format as padding and bin_size, so different
                          smoothing kernels are possible in the x and y directions.
        :type smoothing: int, float, list
        :param cmap: The colormap to use for the shading
        :type cmap: str
        :param weights: A list containing weights for each data point. If these
                        are not passed, all data points will be weighted
                        equally.
        :type weights: list, np.ndarray
        :param log_xy: Whether or not to do the smoothing and bin creation in log
                       space. This should be used if the plot will be done on
                       log-scaled axes.Can either be a single bool, in which case the
                       x and y scales will both be log (or not), or a two element
                       array, where the first is whether the x axis is log, and the
                       second is y. If this is used, the bin_size and smoothing
                       parameters will be interpreted as dex, rather than raw values.
        :type log: bool, list
        :param log_hist: Whether or not to use the log of the histogram values to
                         compute the shading, or just the values of the histogram.
        :type log_hist: bool
        :return: output of the pcolormesh function call.

        .. plot::
            :include-source:

            import betterplotlib as bpl
            import numpy as np
            bpl.set_style()

            xs = np.concatenate(
                [np.random.normal(3, 2, 1000), np.random.normal(7, 2, 1000)]
            )
            ys = np.concatenate(
                [np.random.normal(7, 2, 1000), np.random.normal(3, 2, 1000)]
            )

            bpl.shaded_density(xs, ys, bin_size=0.01, smoothing=0.5, cmap="inferno")
            bpl.set_limits(0, 10, 0, 10)
            bpl.equal_scale()

        .. plot::
            :include-source:

            import betterplotlib as bpl
            import numpy as np

            bpl.set_style()

            xs = np.concatenate(
                [np.random.normal(3, 2, 1000), np.random.normal(7, 2, 1000)]
            )
            ys = 10 ** np.concatenate(
                [np.random.normal(7, 2, 1000), np.random.normal(3, 2, 1000)]
            )

            fig, ax = bpl.subplots()
            bpl.shaded_density(
                xs,
                ys,
                bin_size=0.01,
                smoothing=0.5,
                cmap="inferno",
                log_xy=[False, True],
            )
            ax.set_yscale("log")
            bpl.set_limits(0, 10, 1, 1e10)
            bpl.equal_scale()

        """
        padding = tools._padding_from_smoothing(smoothing)
        # first get the underlying density histogram
        hist, x_edges, y_edges = tools.smart_hist_2d(
            xs,
            ys,
            bin_size,
            padding=padding,
            smoothing=smoothing,
            weights=weights,
            log=log_xy,
        )

        vmax = np.max(hist)
        vmin = np.percentile(hist[hist >= 0], 1)

        if log_hist:
            vmin_linear = np.percentile(hist[hist > 0], 1)
            hist = np.log10(hist)
            vmax = np.log10(vmax)
            vmin = max(np.log10(vmin_linear), vmax - 3)

        return super(Axes_bpl, self).pcolormesh(
            x_edges, y_edges, hist, cmap=cmap, vmax=vmax, vmin=vmin
        )
