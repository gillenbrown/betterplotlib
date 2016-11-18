from matplotlib.figure import Figure

class Figure_bpl(Figure):
    def savefig(self, name, *args, **kwargs):
        """
        Saves the figure with some sugar to make it better.

        Automatically saves as pdf if not specified. If it is specified to save
        as anything other than a pdf, it is saved with high dpi.

        :param kwargs: additional parameters that will be passed on to the
                       fig.savefig() function.
        :return: None, but saves the plot.
        """

        # check for the file format to use
        if len(name.split(".")) > 1:
            kwargs.setdefault("format", name.split(".")[-1])
        else:
            kwargs.setdefault("format", "pdf")
        # If we aren't saving a pdf, we need to set the dpi high
        if kwargs["format"] != "pdf":
            kwargs.setdefault("dpi", 500)

        super().savefig(name, *args, **kwargs)
