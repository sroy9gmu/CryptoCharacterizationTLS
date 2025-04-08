"""
=============================
Grouped bar chart with labels
=============================

This example shows a how to create a grouped bar chart and how to annotate
bars with labels.
"""

# data from https://allisonhorst.github.io/palmerpenguins/

import matplotlib.pyplot as plt
import numpy as np

devs = ("Zero W", "3B+", "4B", "x86_64")
libs = {
    'OpenSSL': (0, 0, 163.32, 63.43),
    'wolfSSL': (0, 0, 1852.45, 482.87),
    'GnuTLS': (0, 0, 728.78, 213.89),
    'MbedTLS': (0, 0, 2416.00, 927.07),
}

x = np.arange(len(devs))  # the label locations
width = 0.2  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='tight')

for attribute, measurement in libs.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, label_type='edge')
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel(r'Execution Time ($microsec$s)')
# ax.set_title('Penguin attributes by species')
ax.set_xticks(x + width, devs)
# ax.legend(loc='upper right', ncols=3)
# ax.set_ylim(0, 10)
ax.set_yscale('log')
ax.minorticks_off()

# fig.set_figwidth(4) 
fig.set_figheight(3) 

# # Shrink current axis by 20%
# box = ax.get_position()
# ax.set_position([box.x0, box.y0, box.width * 0.9, box.height * 0.5])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()

# %%
#
# .. admonition:: References
#
#    The use of the following functions, methods, classes and modules is shown
#    in this example:
#
#    - `matplotlib.axes.Axes.bar` / `matplotlib.pyplot.bar`
#    - `matplotlib.axes.Axes.bar_label` / `matplotlib.pyplot.bar_label`
