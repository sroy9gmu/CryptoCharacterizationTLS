# data = [[ 15789.47, 34664.27, 5.4, 1.58],
#         [ 11122, 35588, 6.67, 1.31],
#         [ 11043.98, 42559, 6.12, 1.25],
#         [ 6616.34, 27226.12, 3.41, 1.9]]

# columns = ("FFDH-2048", "RSA-PSS-3072", "AES-128-GCM", "SHA-256")
# rows = ['OpenSSL', 'wolfSSL', 'MbedTLS', 'GnuTLS']

# data from https://allisonhorst.github.io/palmerpenguins/
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# algos = ("FFDH-2048", "RSA-PSS-3072", "AES-128-GCM", "SHA-256", "Total")
# times = {
#     'OpenSSL': (1688307, 34664.3, 58, 16.1),
#     'wolfSSL': (38191.5, 35588, 66, 161),
#     'MbedTLS': (94037, 42559, 45, 76),
#     'GnuTLS': (52094, 54453, 86, 167)
# }
# print(matplotlib.__version__)
libs = ('OpenSSL', 'wolfSSL', 'MbedTLS', 'GnuTLS')
# durs = {
#     # 'FFDH-2048': (1688307, 38191.5, 94037, 52094),
#     'Key Exchange': (110000, 38191.5, 94037, 52094),
#     'Signing': (34664.3, 35588, 42559, 54453),
#     'Symmetric Encryption': (58, 66, 45, 86),
#     'Hashing': (16.1, 161, 76, 167)
# }
durs = {
    'Hashing': (16.1, 161, 76, 167),
    'Symmetric Encryption': (58, 66, 45, 86),
    'Signing': (34664.3, 35588, 42559, 54453),
    # 'FFDH-2048': (1688307, 38191.5, 94037, 52094),
    'Key Exchange': (120000, 38191.5, 94037, 52094),   
}

bottom = np.zeros(3)
x = np.arange(len(libs))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots(layout='constrained')
bottom = np.zeros(4)
for boolean, dur in durs.items():
    p = ax.bar(libs, dur, width, label=boolean, bottom=bottom)
    bottom += dur

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Duration (microseconds)')
# ax.set_title('Execution time breadown')
# ax.set_xticks(x + width, libs)
ax.legend(loc=(1, 0.8))
ylim = 0
for index, (key, value) in enumerate(durs.items()):
    ylim += max(durs[key])
ax.set_ylim(0, ylim)
# ax.set_yscale('log')
ax.minorticks_off()
# ax.invert_xaxis() 
ax.grid(axis='y', linestyle='--') # Add horizontal grid lines

# data = []
# row_labels = []
# for index, (key, value) in enumerate(times.items()):
#     tmp = list(value)
#     for i in range(len(tmp)):
#         tmp[i] = "{:,.2f}".format(tmp[i]) # https://queirozf.com/entries/python-number-formatting-examples
#     tmp.append("{:,.2f}".format(sum(value)))
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