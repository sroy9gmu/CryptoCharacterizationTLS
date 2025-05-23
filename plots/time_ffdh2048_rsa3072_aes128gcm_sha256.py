# data = [[ 15789.47, 34664.27, 5.4, 1.58],
#         [ 11122, 35588, 6.67, 1.31],
#         [ 11043.98, 42559, 6.12, 1.25],
#         [ 6616.34, 27226.12, 3.41, 1.9]]

# columns = ("FFDH-2048", "RSA-PSS-3072", "AES-128-GCM", "SHA-256")
# rows = ['OpenSSL', 'wolfSSL', 'MbedTLS', 'GnuTLS']

# data from https://allisonhorst.github.io/palmerpenguins/

import matplotlib.pyplot as plt
import numpy as np

algos = ("FFDH-2048", "RSA-PSS-3072", "AES-128-GCM", "SHA-256")
times = {
    'OpenSSL': (15789.47, 34664.27, 5.4, 1.58),
    'wolfSSL': (11122, 35588, 6.67, 1.31),
    'MbedTLS': (11043.98, 42559, 6.12, 1.25),
    'GnuTLS': (6616.34, 27226.12, 3.41, 1.9)
}

x = np.arange(len(algos))  # the label locations
width = 0.2  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='tight')

for attribute, measurement in times.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    # ax.bar_label(rects, label_type='edge')
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Time (microseconds)')
ax.set_title('Execution time by algorithm')
ax.set_xticks(x + width, algos)
# ax.legend(loc='upper left', ncols=3)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.set_yscale('log')

ax.grid(axis='y', linestyle='--') # Add horizontal grid lines

data = []
row_labels = []
for index, (key, value) in enumerate(times.items()):
    tmp = list(value)
    for i in range(len(tmp)):
        tmp[i] = "{:,.2f}".format(tmp[i])
    data.append(tmp)
    row_labels.append(key)
col_labels = algos

fig, ax = plt.subplots()
ax.axis('off')  # Hide the axes
table = plt.table(cellText=data, colLabels=col_labels, rowLabels=row_labels, loc='center')
table.scale(1, 1.5) # Adjust table size

table.auto_set_font_size(False) # Disable autosizing
# table.set_fontsize(12) # Set font size

plt.show()