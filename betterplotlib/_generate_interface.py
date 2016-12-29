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
    func_args = []
    with open(loc, "r") as original:
        in_axes = False
        in_def = False
        for line in original:
            if in_axes == False and line.strip() == definition:
                in_axes = True
                continue
            if in_axes and line.strip().startswith("def "):
                in_def = True
                this_def = ""
            if in_def:
                if "def" in line:
                    this_def += line.strip().replace("self, ", "") + "\n"
                else:
                    this_def += line[4:]
                    if not line.endswith("\n"):
                        this_def += "\n"
            if in_def and ":" in line:
                in_def = False
                func_args.append(this_def)
                
    return func_args

def strip_defaults(function_def):
    # gets rid of all the default parameters in a function argument so that it
    # can be turned from the definition into a function call

    # first get where the arguments start
    first_paren_idx = function_def.find("(")
    # get the function name and first parenthesis
    def_begin = function_def[4:first_paren_idx + 1]
    # then get the arguments. The -3 at the end takes care of the newline,
    # colon, and closing parenthesis.
    args = function_def[first_paren_idx + 1:-3]
    
    # then we can examine each one in turn, formatiing it properly
    args_list = []
    for arg in args.split(","):
        # find ehere the equals sign indicating a default parameter is
        idx_equals = arg.find("=")
        # if there isn't one, there is no default, so we can just keep the 
        # whole thing
        if idx_equals == -1:
            args_list.append(arg)
        # if there is a default paraemeter, get rid of it. 
        else:
            args_list.append(arg[0:idx_equals])
    
    # then put them back into a comma separated list   
    args_joined = ",".join(args_list)
    # to have things line up properly in the file, we need to add some spaces
    args_joined = args_joined.replace("\n", "\n          ")
    # then join everything together
    return def_begin + args_joined + ")"


axes_definition = "class Axes_bpl(Axes):"
# figure_definition = "class Figure_bpl(Figure):"

axes_functions_args = get_functions(axes_loc, axes_definition)
# figure_functions = get_functions(figure_loc, figure_definition)

for func_args in axes_functions_args:
    func_name = func_args.split()[1].split("(")[0]
    func_args_no_defauts = strip_defaults(func_args)
    interface.write("@_autogen_docstring(bpl.Axes_bpl.{})\n".format(func_name) + \
                    func_args + \
                    "    ax = plt.gca(projection='bpl')\n" + \
                    "    return ax.{}\n\n".format(func_args_no_defauts))

# for func in figure_functions:
#     interface.write("@_autogen_docstring(bpl.Figure_bpl.{})\n".format(func) + \
#                     "def {}(*args, **kwargs):\n".format(func) + \
#                     "    fig = plt.gcf()\n" + \
#                     "    return fig.{}(*args, **kwargs)\n\n".format(func))

interface.close()