import prettyplot as ppl
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(figsize=[10, 4], ncols=2)
ppl.make_ax_dark(ax2)
ax1.set_title("Regular")
ax2.set_title("Dark")