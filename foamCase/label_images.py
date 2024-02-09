"""
Add text label to all image files in ../images.
"""

import os
import glob
import cv2  # from opencv Python package
import re

search_dir = "../images"
files = list(filter(os.path.isfile, glob.glob(search_dir + "/*.png")))
for file in files:
    filepath = os.fsdecode(file)
    print("Processing %r" % filepath)
    # Skip the base case images
    if "base" in filepath:
        continue

    # Get case name from file path name like
    # ../images/surface_123456789012_addLayersControls.nOuterIter_1.png
    # --> "addLayersControls.nOuterIter_1"
    filename = re.search(".*_\d+_(.*)\.png", filepath).group(1)

    # Find label
    pattern1 = re.compile("(.*" + re.escape(filename) + "),")
    label = ""
    for line in open("results_labels.txt"):
        for match in re.finditer(pattern1, line):
            label = match.group(1)
    if not label:
        raise Exception("No label found for " + filename)

    color = (0, 0, 0)
    if "slice" in str(filepath):
        color = (255, 255, 255)
    if "BASE" in label:
        color = (0, 0, 255)
    print("Labeling " + filename + " : " + label)

    # Add the label to the image
    img = cv2.imread(file)
    cv2.putText(
        img = img, 
        text = label,
        org = (50, 80),
        fontFace = cv2.FONT_HERSHEY_SIMPLEX,
        fontScale = 2,
        color = color,
        thickness = 4,
    )
    cv2.imwrite(filepath, img)
