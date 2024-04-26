"""
Plot solver stability (max(mag(U))) vs. layer coverage for data points
"""

import matplotlib.pyplot as plt
import numpy as np
import csv
import re

pattern1 = re.compile(r"^.*?([\w\.]+)_(.*)$")
maxU = 1000.0  # maximum value for max(mag(U))

def get_data(name):
    """Dig up data points for argument variable name"""

    labels=[]
    stabilities=[]
    coverages=[]
    with open('results_snappy.txt', newline='\n') as csvfile, \
         open('results_labels.txt', newline='\n') as csvfile2, \
         open('results_fieldMinMax.txt', newline='\n') as csvfile3:
        reader = csv.reader(csvfile, delimiter=',')
        reader2 = csv.reader(csvfile2, delimiter=',')
        reader3 = csv.reader(csvfile3, delimiter=',')
        old_varname = ""
        for row, row2, row3 in zip(reader, reader2, reader3):
            long_label = row2[0]
            for match in re.finditer(pattern1, long_label):
                param_name = match.group(1)
                if param_name != name:
                    continue
                layer_avg = (float(row[1]) + float(row[2]) + float(row[3])) / 3.0
                maxMagU = min(maxU, float(row3[2]))
                iters = int(row3[1])
                label = match.group(2)
                labels.append(label)
                if iters < 200:
                    stabilities.append(maxU)
                    coverages.append(0.0)
                else:
                    stabilities.append(maxMagU)
                    coverages.append(layer_avg)
    return labels, coverages, stabilities

def plot_variable(name):
    """Generate a plot for argument variable name)"""

    labels, coverages, stabilities = get_data(name)

    fig, axs = plt.subplots(2, 1, figsize=(10, 6))
    # fig.tight_layout()

    def myplot(ax, minx=None, maxx=None):
        ax.plot(coverages, stabilities)
        for label, x, y in zip(labels, coverages, stabilities):
            ax.annotate(label, xy=(x, y), textcoords="data")
        ax.set_xlabel("mean layer coverage")
        ax.set_ylabel("unstability (max(mag(U)))")
        if minx != None and maxx != None:
            ax.set_xlim([minx, maxx])
            ax.set_ylim([28, 102.0])
        ax.grid()
        ax.plot(1.3233, 33.42066, marker="x", color="red") # hard-coded base value, CHECKME

    fig.suptitle(name)
    myplot(axs[0], 0.0, 4.0)
    myplot(axs[1])
    plt.savefig("results_stability_coverage_for_" + name + ".png")

def get_variables():
    """Generate list of variable names in the dataset"""

    names=[]
    with open('results_labels.txt', newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            long_label = row[0]
            for match in re.finditer(pattern1, long_label):
                param_name = match.group(1)
                if param_name not in names:
                    names.append(param_name)
    return names

names = get_variables()
for name in names:
    print("Generating plot for " + name)
    plot_variable(name)
