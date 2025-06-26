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
    'OpenSSL': (15821.53, 34626.81, 5.09,  1.23),
    'wolfSSL': (11122.21, 35588.00, 6.67, 1.32),
    'MbedTLS': (11043.98, 42559.00, 6.11, 1.25),
    'GnuTLS': (6616.34, 27226.12, 3.41, 1.90)
}

libs = ('OpenSSL', 'wolfSSL', 'MbedTLS', 'GnuTLS')
durs = {
    'FFDH-2048': (15821.53, 11122.21, 11043.98, 6616.34),
    'RSA-PSS-3072': (34626.81, 35588.00, 42559.00, 27226.12),
    'AES-128-GCM': (5.09, 6.67, 6.11, 3.41),
    'SHA-256': (1.23, 1.32, 1.25, 1.90)
}

x = np.arange(len(libs))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots(layout='tight')
bottom = np.zeros(4)
for boolean, dur in durs.items():
    p = ax.bar(libs, dur, width, label=boolean, bottom=bottom)
    bottom += dur

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Duration (microseconds)')
ax.set_title('Execution time of single direct invocation')
# ax.set_xticks(x + width, libs)
ax.legend(loc='lower center', ncols=4)
# ax.set_ylim(0, 100000)
# ax.set_yscale('log')
ax.minorticks_off()

ax.grid(axis='y', linestyle='--') # Add horizontal grid lines

data = []
row_labels = []
for index, (key, value) in enumerate(times.items()):
    tmp = list(value)
    for i in range(len(tmp)):
        tmp[i] = "{:,.2f}".format(tmp[i]) # https://queirozf.com/entries/python-number-formatting-examples
    # tmp.append("{:,.2f}".format(sum(value)))
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