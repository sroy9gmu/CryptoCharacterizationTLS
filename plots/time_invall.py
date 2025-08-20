# data = [[ 15789.47, 34664.27, 5.4, 1.58],
#         [ 11122, 35588, 6.67, 1.31],
#         [ 11043.98, 42559, 6.12, 1.25],
#         [ 6616.34, 27226.12, 3.41, 1.9]]

# columns = ("FFDH-2048", "RSA-PSS-3072", "AES-128-GCM", "SHA-256")
# rows = ['OpenSSL', 'wolfSSL', 'MbedTLS', 'GnuTLS']

# data from https://allisonhorst.github.io/palmerpenguins/

import matplotlib.pyplot as plt
import numpy as np

# algos = ("FFDH-2048", "RSA-PSS-3072", "AES-128-GCM", "SHA-256")
# times = {
#     'OpenSSL': (15821.53, 34626.81, 5.09,  1.23),
#     'wolfSSL': (11122.21, 35588.00, 6.67, 1.32),
#     'MbedTLS': (11043.98, 42559.00, 6.11, 1.25),
#     'GnuTLS': (6616.34, 27226.12, 3.41, 1.90)
# }

libs = ('OpenSSL', 'wolfSSL', 'MbedTLS', 'GnuTLS')
durs = {
    'Signing': (34626.8, 35588, 42559, 27226.1), 
    'Key Exchange': (15821.5, 11122.2, 11044, 6616.3),   
    'Symmetric Encryption': (5.1, 6.7, 6.1, 3.4), 
    'Hashing': (1.2, 1.3, 1.2, 1.9), 
}

x = np.arange(len(libs))  # the label locations
width = 0.2  # the width of the bars
mul = 0

colors = ['blue', 'purple', 'green','red']
i = 0
fig, ax = plt.subplots(layout='constrained')
for lib, dur in durs.items():
    offset = width * mul
    rects = ax.bar(x + offset, dur, width, label=lib, color=colors[i])
    # ax.bar_label(rects, padding=3)
    mul += 1
    i += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Duration (microseconds)')
# ax.set_title('Execution time of single direct invocation')
ax.set_xticks(x + width, libs)
# ax.legend(loc=(0, 0.8))

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.07), ncol=5)

# ax.set_ylim(0, 100000)
ax.set_yscale('log')
ax.minorticks_off()

ax.grid(axis='y', linestyle='--') # Add horizontal grid lines

# data = []
# row_labels = []
# for index, (key, value) in enumerate(times.items()):
#     tmp = list(value)
#     for i in range(len(tmp)):
#         tmp[i] = "{:,.2f}".format(tmp[i]) # https://queirozf.com/entries/python-number-formatting-examples
#     # tmp.append("{:,.2f}".format(sum(value)))
#     data.append(tmp)    
#     row_labels.append(key)
# col_labels = algos

# fig, ax = plt.subplots()
# ax.axis('off')  # Hide the axes
# table = plt.table(cellText=data, colLabels=col_labels, rowLabels=row_labels, loc='center')
# table.scale(1, 1.5) # Adjust table size

# table.auto_set_font_size(False) # Disable autosizing
# table.set_fontsize(12) # Set font size

plt.show()