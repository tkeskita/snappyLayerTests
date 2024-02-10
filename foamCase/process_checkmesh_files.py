"""
Process all generated checkMesh log files to extract number
of errors and export the results as csv for plotting with
plot_results.py
"""

import os
import re
import glob

def parse_logs(logname):
    """Parse checkMesh logs for argument logname (snapping or layers)"""
 
    search_dir = "../logs/log.checkMesh_" + logname + "_*"
    files = list(filter(os.path.isfile, glob.glob(search_dir)))
    # Sort files by file creation date
    files.sort(key=lambda x: os.path.getmtime(x))

    resultfilename="results_checkmesh_" + logname + ".txt"
    if os.path.isfile(resultfilename):
        os.remove(resultfilename)

    pattern1 = re.compile("^\ \ \<\<Writing\ (\d+).*\ to\ set\ (\w+)")
    pattern2 = re.compile("^\ \ \<\<Writing\ region\ \d+\ with\ \d+\ cells\ to\ cellSet")

    for file in files:
        filename = os.fsdecode(file)
        testname = filename.split("checkMesh_" + logname + "_")[1].lstrip("0123456789_")
        text_short = ""
        text_long = ""
        nRegions = 0
        for line in open(filename):
            for match in re.finditer(pattern1, line):
                shorthand = match.group(2)[0] + ''.join(c for c in match.group(2) if c.isupper())
                text_short += shorthand + match.group(1) + "+"
                text_long += match.group(2) + "=" + match.group(1) + "," 
            for match in re.finditer(pattern2, line):
                nRegions += 1
        # text = testname + "," + text_short[0:-1] + " regions=%d," % nRegions + text_long[0:-1]
        text = testname + "," + text_short[0:-1] + "," + text_long[0:-1]
        print("extracted results: " + text)
        with open(resultfilename, "a") as myfile:
            myfile.write(text + "\n")

parse_logs('snapping')
parse_logs('layers')
