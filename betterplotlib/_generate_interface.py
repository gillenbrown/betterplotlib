# auto generates _interface.py
import os

this_dir = os.path.realpath(os.path.split(__file__)[0])
interface_loc = this_dir + os.sep + "_interface.py"
axes_loc = this_dir + os.sep + "axes_bpl.py"
figure_loc = this_dir + os.sep + "figure_bpl.py"

interface = open(interface_loc, "w")

# write a header
interface.write("from matplotlib import docstring\n" +  
                "from matplotlib.pyplot import _autogen_docstring\n" +
                "import matplotlib.pyplot as plt\n\n"
                "import betterplotlib as bpl\n\n")

def get_functions(loc, definition):    
    functions = []
    with open(loc, "r") as original:
        in_axes = 0
        for line in original:
            if in_axes != 1 and line.strip() == definition:
                in_axes = 1
            if in_axes and line.strip().startswith("def "):
                func_name_with_parens = line.split()[1]
                func_name = func_name_with_parens.split("(")[0]
                functions.append(func_name)
                
    return functions


axes_definition = "class Axes_bpl(Axes):"
figure_definition = "class Figure_bpl(Figure):"

axes_functions = get_functions(axes_loc, axes_definition)
figure_functions = get_functions(figure_loc, figure_definition)

for func in axes_functions:
    interface.write("@_autogen_docstring(bpl.Axes_bpl.{})\n".format(func) + \
                    "def {}(*args, **kwargs):\n".format(func) + \
                    "    ax = plt.gca(projection='bpl')\n" + \
                    "    return ax.{}(*args, **kwargs)\n\n".format(func))

for func in figure_functions:
    interface.write("@_autogen_docstring(bpl.Figure_bpl.{})\n".format(func) + \
                    "def {}(*args, **kwargs):\n".format(func) + \
                    "    fig = plt.gcf()\n" + \
                    "    return fig.{}(*args, **kwargs)\n\n".format(func))

interface.close()