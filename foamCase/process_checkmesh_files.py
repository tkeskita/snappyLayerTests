"""
Process all generated checkMesh log files to extract number
of errors and export the results as csv for plotting with
plot_results.py
"""

import os
import re
import glob

def parse_logs(time_dir):
    """Parse checkMesh logs for argument time_dir (2 or 3)"""
 
    search_dir = "../logs/log.checkMesh_time" + str(time_dir) + "_*"
    files = list(filter(os.path.isfile, glob.glob(search_dir)))
    # Sort files by file creation date
    files.sort(key=lambda x: os.path.getmtime(x))

    resultfilename="results_checkmesh_time" + str(time_dir) + ".txt"
    if os.path.isfile(resultfilename):
        os.remove(resultfilename)

    pattern1 = re.compile("^\ \ \<\<Writing\ (\d+).*\ to\ set\ (\w+)")

    for file in files:
        filename = os.fsdecode(file)
        testname = filename.split("_time" + str(time_dir) + "_")[1]
        text_short = ""
        text_long = ""
        for line in open(filename):
            for match in re.finditer(pattern1, line):
                shorthand = match.group(2)[0] + ''.join(c for c in match.group(2) if c.isupper())
                text_short += shorthand + match.group(1) + "+"
                text_long += match.group(2) + "=" + match.group(1) + "," 
        text = testname + "," + text_short[0:-1] + "," + text_long[0:-1]
        print("extracted results: " + text)
        with open(resultfilename, "a") as myfile:
            myfile.write(text + "\n")

parse_logs(2)
parse_logs(3)
