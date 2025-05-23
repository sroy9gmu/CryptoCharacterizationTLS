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
    'OpenSSL': (1688307.0, 34664.27, 58.0, 16.156222),
    'wolfSSL': (38191.548417, 35588.0, 66.0, 161.0),
    'MbedTLS': (94037.0, 42559.0, 45.0, 76.0),
    'GnuTLS': (52094.0, 54453.0, 86.0, 167.0)
}

libs = ('OpenSSL', 'wolfSSL', 'MbedTLS', 'GnuTLS')
durs = {
    'FFDH-2048': (1688307.0, 38191.548417, 94037.0, 52094.0),
    'RSA-PSS-3072': (34664.27, 35588.0, 42559.0, 54453.0),
    'AES-128-GCM': (58.0, 66.0, 45.0, 86.0),
    'SHA-256': (16.156222, 161.0, 76.0, 167.0)
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
ax.set_ylabel('Duration (microseconds)')
ax.set_title('Execution time breadown')
# ax.set_xticks(x + width, libs)
ax.legend(loc='lower center', ncols=4)
# ax.set_ylim(0, 100000)
ax.set_yscale('log')
ax.minorticks_off()

ax.grid(axis='y', linestyle='--') # Add horizontal grid lines

data = []
row_labels = []
for index, (key, value) in enumerate(times.items()):
    tmp = list(value)
    for i in range(len(tmp)):
        tmp[i] = "{:,.2f}".format(tmp[i]) # https://queirozf.com/entries/python-number-formatting-examples
    tmp.append("{:,.2f}".format(sum(value)))
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