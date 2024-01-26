"""
Plot the average number of layers for all cases.
"""

import matplotlib.pyplot as plt
import numpy as np
import csv

labels=[]
layers=[]
with open('results.txt', newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        labels.append(str(row[0]))
        layer_avg = (float(row[1]) + float(row[2]) + float(row[3])) / 3.0
        layers.append(layer_avg)

fig, ax = plt.subplots(figsize=(7,45))
fig.tight_layout()
x = range(len(layers))
width = 0.8
rects1 = ax.barh(x, layers, width, color='r')

ax.set_xlabel('Average number of layers')
ax.set_yticks(x)
ax.set_yticklabels(labels)
plt.subplots_adjust(bottom=0.01, left=0.6, right=0.99, top=0.99)
plt.grid(axis='x')
plt.savefig('results.png')
# plt.show()
