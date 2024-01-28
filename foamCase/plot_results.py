"""
Plot the average number of layers for all cases.
"""

import matplotlib.pyplot as plt
import numpy as np
import csv

labels=[]
layers=[]
with open('results_snappy.txt', newline='\n') as csvfile, \
    open('results_checkmesh_time2.txt', newline='\n') as csvfile2, \
    open('results_checkmesh_time3.txt', newline='\n') as csvfile3:
    reader = csv.reader(csvfile, delimiter=',')
    reader2 = csv.reader(csvfile2, delimiter=',')
    reader3 = csv.reader(csvfile3, delimiter=',')
    for row, row2, row3 in zip(reader, reader2, reader3):
        label = row[0] + ": E2=" + row2[1] + ", E3=" + row3[1] 
        labels.append(label)
        layer_avg = (float(row[1]) + float(row[2]) + float(row[3])) / 3.0
        layers.append(layer_avg)

fig, ax = plt.subplots(figsize=(14,45))
fig.tight_layout()
x = range(len(layers))
width = 0.8
rects1 = ax.barh(x, layers, width, color='r')

ax.set_xlabel('Average number of layers')
ax.set_yticks(x)
ax.set_yticklabels(labels)
plt.subplots_adjust(bottom=0.01, left=0.7, right=0.99, top=0.99)
plt.grid(axis='x')
plt.savefig('results.png')
# plt.show()
