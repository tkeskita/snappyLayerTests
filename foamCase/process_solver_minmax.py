"""
Process all generated fieldMinMax files to exctract number of
solver iterations, maximum velocity and maximum pressure for plotting with
plot_results.py
"""

import os
import re
import glob
import statistics

pattern1 = re.compile("^(\d+)\s*([\w\(\)]+).*\(.*\).*\s([\d\.e\+\-]+)\s+\(.*\)")

search_dir = "../logs"
files = list(filter(os.path.isfile, glob.glob(search_dir + "/log.fieldMinMax_*")))
# Sort files by file creation date
files.sort(key=lambda x: os.path.getmtime(x))

resultfilename="results_fieldMinMax.txt"
if os.path.isfile(resultfilename):
    os.remove(resultfilename)

for file in files:
    filename = os.fsdecode(file)
    testname = filename.split("fieldMinMax_")[1].lstrip("0123456789_")
    text = testname + ","

    Uvals = []
    maxMagU = 0.0
    maxP = 0.0
    iter = 0
    for line in open(filename):
        for match in re.finditer(pattern1, line):
            iter = int(match.group(1))
            varname = match.group(2)
            value = float(match.group(3))
            if iter < 10:
                continue
            if varname == "mag(U)":
                Uvals.append(value)
                if value > maxMagU:
                    maxMagU = value
            elif varname == "p" and value > maxP:
                maxP = value

    if iter > 10:
        stdev_val = statistics.stdev(Uvals)
    else:
        stdev_val = 0.0

    text += str(iter) + "," + str(maxMagU) + "," + str(maxP) + "," + str(stdev_val)

    print("extracted results: " + text)
    with open(resultfilename, "a") as myfile:
        myfile.write(text + "\n")
