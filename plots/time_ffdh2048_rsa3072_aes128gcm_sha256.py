# data = [[ 15789.47, 34664.27, 5.4, 1.58],
#         [ 11122, 35588, 6.67, 1.31],
#         [ 11043.98, 42559, 6.12, 1.25],
#         [ 6616.34, 27226.12, 3.41, 1.9]]

# columns = ("FFDH-2048", "RSA-PSS-3072", "AES-128-GCM", "SHA-256")
# rows = ['OpenSSL', 'wolfSSL', 'MbedTLS', 'GnuTLS']

# data from https://allisonhorst.github.io/palmerpenguins/

import matplotlib.pyplot as plt
import numpy as np

algos = ("FFDH-2048", "RSA-PSS-3072", "AES-128-GCM", "SHA-256", "Total")
times = {
    'OpenSSL': (15789.47, 34664.27, 5.4, 1.58),
    'wolfSSL': (11122, 35588, 6.67, 1.31),
    'MbedTLS': (11043.98, 42559, 6.12, 1.25),
    'GnuTLS': (6616.34, 27226.12, 3.41, 1.9)
}

libs = ('OpenSSL', 'wolfSSL', 'MbedTLS', 'GnuTLS')
durs = {
    'FFDH-2048': (15789.47, 11122, 11043.98, 6616.34),
    'RSA-PSS-3072': (34664.27, 35588, 42559, 27226.12),
    'AES-128-GCM': (5.4, 6.67, 6.12, 3.41),
    'SHA-256': (1.58, 1.31, 1.25, 1.9)
}

bottom = np.zeros(3)
x = np.arange(len(libs))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots(layout='tight')
bottom = np.zeros(4)
for boolean, dur in durs.items():
    p = ax.bar(libs, dur, width, label=boolean, bottom=bottom)
    bottom += dur

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Time (microseconds)')
ax.set_title('Execution time')
# ax.set_xticks(x + width, libs)
ax.legend(loc='lower center', ncols=4)
# ax.set_ylim(0, 100000)

ax.grid(axis='y', linestyle='--') # Add horizontal grid lines

data = []
row_labels = []
for index, (key, value) in enumerate(times.items()):
    tmp = list(value)
    for i in range(len(tmp)):
        tmp[i] = "{:,.2f}".format(tmp[i])
    tmp.append("{:,.2f}".format(sum(value)))
    data.append(tmp)    
    row_labels.append(key)
col_labels = algos

fig, ax = plt.subplots()
ax.axis('off')  # Hide the axes
table = plt.table(cellText=data, colLabels=col_labels, rowLabels=row_labels, loc='center')
table.scale(1, 2) # Adjust table size

table.auto_set_font_size(False) # Disable autosizing
# table.set_fontsize(12) # Set font size

plt.show()