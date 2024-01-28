"""
Process all generated snappyHexMesh log files to extract final
number of layers and export the results as csv for plotting with
plot_results.py
"""

import os
import re
import glob

pattern1 = re.compile("^walls_manifold\s.*\d+\s+\d+\s+([\d\.]+)\s+[\d\.]+\s+([\d\.]+)")
pattern2 = re.compile("^walls_nonmanifold\s.*\d+\s+\d+\s+([\d\.]+)\s+[\d\.]+\s+([\d\.]+)")
pattern3 = re.compile("^walls_nonmanifold_slave\s.*\d+\s+\d+\s+([\d\.]+)\s+[\d\.]+\s+([\d\.]+)")

search_dir = "../logs"
files = list(filter(os.path.isfile, glob.glob(search_dir + "/log.snappyHexMesh_*")))
# Sort files by file creation date
files.sort(key=lambda x: os.path.getmtime(x))

resultfilename="results_snappy.txt"
if os.path.isfile(resultfilename):
    os.remove(resultfilename)

for file in files:
    filename = os.fsdecode(file)
    testname = filename.split("snappyHexMesh_")[1]
    text = testname + ","

    w1 = "0.0,"
    w2 = "0.0,"
    w3 = "0.0,"
    for line in open(filename):
        for match in re.finditer(pattern1, line):
            w1 = match.group(1) + ","
        for match in re.finditer(pattern2, line):
            w2 = match.group(1) + ","
        for match in re.finditer(pattern3, line):
            w3 = match.group(1) + ","
    text += w1 + w2 + w3

    print("extracted results: " + text)
    with open(resultfilename, "a") as myfile:
        myfile.write(text + "\n")
