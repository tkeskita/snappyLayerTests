"""
Plot the average number of layers for all cases.
"""

import matplotlib.pyplot as plt
import numpy as np
import csv

labels=[]
layers=[]
with open('results_snappy.txt', newline='\n') as csvfile, \
    open('results_checkmesh_snapping.txt', newline='\n') as csvfile2, \
    open('results_checkmesh_layers_important_checks.txt', newline='\n') as csvfile3, \
    open('results_labels.txt', newline='\n') as csvfile4:
    reader = csv.reader(csvfile, delimiter=',')
    reader2 = csv.reader(csvfile2, delimiter=',')
    reader3 = csv.reader(csvfile3, delimiter=',')
    reader4 = csv.reader(csvfile4, delimiter=',')
    for row, row2, row3, row4 in zip(reader, reader2, reader3, reader4):
        label = row4[0] + " -- snap_errors=" + row2[1] + " -- layer_errors=" + row3[1]
        label += " -- meshing_time=%s" % row[4]
        labels.append(label)
        layer_avg = (float(row[1]) + float(row[2]) + float(row[3])) / 3.0
        layers.append(layer_avg)

fig, ax = plt.subplots(figsize=(15, 85))
fig.tight_layout()
x = range(len(layers))
width = 0.8
rects1 = ax.barh(x, layers, width, color='r')

ax.set_xlabel('Average number of layers')
ax.set_yticks(x)
ax.set_yticklabels(labels)
plt.subplots_adjust(bottom=0.01, left=0.75, right=0.99, top=0.99)
plt.grid(axis='x')
plt.savefig('results.png')
# plt.show()
