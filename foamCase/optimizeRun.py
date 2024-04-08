"""
SnappyHexMesh parameter optimization routine. Tries to find
parameter values which maximize simpleFoam stability and layer
coverage.
"""

import numpy as np
from scipy.optimize import minimize, OptimizeResult
import subprocess
import os
import re
import statistics

# Names of parameters which are to be included in optimization
param_names=[
    # "meshQualityControls.maxNonOrtho",
    "meshQualityControls.maxBoundarySkewness",
    "meshQualityControls.maxInternalSkewness",
    # "meshQualityControls.minVol",
    # "meshQualityControls.minTetQuality",
    # "meshQualityControls.minArea",
    "meshQualityControls.maxConcave",
    "meshQualityControls.minTwist",
    "meshQualityControls.minDeterminant",
    "meshQualityControls.minFaceWeight",
    "meshQualityControls.minVolRatio",
    # "meshQualityControls.minTriangleTwist",
]

def parse_results():
    """Parse the wanted quantities out of result files"""

    # Parse fieldMinMax.dat to find max(mag(U))
    pattern1 = re.compile("^(\d+)\s*([\w\(\)]+).*\(.*\).*\s([\d\.e\+\-]+)\s+\(.*\)")
    maxMagU = 0.0
    maxiter = 200  # CHECKME
    iter = 0
    filename = "./solverCase/postProcessing/minMaxMagnitude()/0/fieldMinMax.dat"
    for line in open(filename):
        for match in re.finditer(pattern1, line):
            iter = int(match.group(1))
            varname = match.group(2)
            value = float(match.group(3))
            if iter < 10:
                continue
            if varname == "mag(U)":
                if value > maxMagU:
                    maxMagU = value

    # Parse log.snappyHexMesh to find number of layers
    pattern1 = re.compile("^walls_manifold\s.*\d+\s+(\d+)\s+([\d\.]+)\s+[\d\.]+\s+([\d\.]+)")
    pattern2 = re.compile("^walls_nonmanifold\s.*\d+\s+(\d+)\s+([\d\.]+)\s+[\d\.]+\s+([\d\.]+)")
    pattern3 = re.compile("^walls_nonmanifold_slave\s.*\d+\s+(\d+)\s+([\d\.]+)\s+[\d\.]+\s+([\d\.]+)")
    max_ll = 4.0  # Cost for failing to produce any layers
    ll1 = max_ll
    ll2 = max_ll
    ll3 = max_ll
    filename = "./log.snappyHexMesh"
    for line in open(filename):
        for match in re.finditer(pattern1, line):
            ll1 = float(match.group(1)) - float(match.group(2))  # target minus actual layers
        for match in re.finditer(pattern2, line):
            ll2 = float(match.group(1)) - float(match.group(2)) 
        for match in re.finditer(pattern3, line):
            ll3 = float(match.group(1)) - float(match.group(2))
    n_lacking_layers = (ll1 + ll2 + ll3) / 3.0

    lacking_iters = float(maxiter - iter)

    return maxMagU, n_lacking_layers, lacking_iters


def f(x):
    """The function to be minimized to get optimal parameters"""

    snappyDict = './system/snappyHexMeshDict'
    snappyTemplate = './system/snappy.template'
    os.system(f'rm {snappyDict}')
    os.system(f'cp {snappyTemplate} {snappyDict}')
    set_x0(param_names, x)
    os.system(f'./mesh optimizer optimized')
    maxMagU, n_layers_lacking, n_iters_lacking = parse_results()    
    n_layers_lacking *= 50.0  # Increase cost of lacking layers
    err = maxMagU + n_layers_lacking + n_iters_lacking
    err2 = err * err
    printout = "params=" + str(list(x)) + " err2=%g" % err2 + " costs=" + str(maxMagU) + ", " + str(n_layers_lacking) + ", " + str(n_iters_lacking)
    print(printout)
    with open("optimizer_output.txt", "a") as outfile:
        outfile.write(printout + "\n")
    return err2


def get_x0(param_names):
    """Dig up the initial parameter values for given parameter names in
    the dictionary files
    """

    values=[]
    for setting in param_names:
        value = subprocess.check_output('foamDictionary -value -entry ' + setting + ' ./system/snappy.template' + ' &> /dev/null', shell=True)
        values.append(float(value.decode('ascii').strip()))
    return values

def set_x0(param_names, values, dict='./system/snappyHexMeshDict'):
    """Set dictionary values for each parameter in param_names"""

    for setting, value in zip(param_names, values):
        subprocess.check_output('foamDictionary -entry ' + setting + ' -set ' + str(value) + ' ' + dict + ' &> /dev/null', shell=True)

# Main program
os.system('surfaceFeatureExtract > log.surfaceFeatureExtract')
x0 = get_x0(param_names)
res = minimize(f, x0, method='nelder-mead', \
               options={'xatol': 1e-8, 'disp': True})
