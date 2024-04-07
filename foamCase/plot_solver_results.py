"""
Plot maximum velocity from solver test case
"""

import matplotlib.pyplot as plt
import numpy as np
import csv

labels=[]
vals=[]
with open('results_snappy.txt', newline='\n') as csvfile, \
    open('results_labels.txt', newline='\n') as csvfile2, \
    open('results_fieldMinMax.txt', newline='\n') as csvfile3:
    reader = csv.reader(csvfile, delimiter=',')
    reader2 = csv.reader(csvfile2, delimiter=',')
    reader3 = csv.reader(csvfile3, delimiter=',')
    for row, row2, row3 in zip(reader, reader2, reader3):
        layer_avg = (float(row[1]) + float(row[2]) + float(row[3])) / 3.0
        label = row2[0] + " -- maxMagU=%g+-%g" % (float(row3[2]), float(row3[4])) + " -- maxP=%g" % float(row3[3]) + " -- layers=%.3g" % layer_avg + " -- iters=%s" % row3[1]
        labels.append(label)
        val = float(row3[2])  # max(mag(U))
        vals.append(val)

fig, ax = plt.subplots(figsize=(15,15)) # ,65))
fig.tight_layout()
x = range(len(vals))
width = 0.8
rects1 = ax.barh(x, vals, width, color='b')

ax.set_xlabel('maximum velocity magnitude')
ax.set_yticks(x)
ax.set_yticklabels(labels)
ax.set_xlim([0, 105])
plt.subplots_adjust(bottom=0.01, left=0.75, right=0.99, top=0.99)
plt.grid(axis='x')
plt.savefig('results_solver.png')
# plt.show()
