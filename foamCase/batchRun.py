"""
Main script, used to run through a sweep of snappyHexMesh settings
and save the results.
"""

import os
from datetime import datetime
import time
import subprocess

# Variation test cases
layerTests = {}

# layerTests['addLayers'] = ['true', 'false']

layerTests['meshQualityControls.maxNonOrtho']         = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 90]
layerTests['meshQualityControls.maxBoundarySkewness'] = [-1, 0, 5, 10, 15, 20, 25, 30, 35, 40]
layerTests['meshQualityControls.maxInternalSkewness'] = [-1, 0, 2, 4, 6, 8, 10, 20]
layerTests['meshQualityControls.maxConcave']          = [0, 10, 20, 40, 60, 70, 80, 90, 120, 180]
layerTests['meshQualityControls.minVol']              = [-1e33, 1e-30, 1e-15, 1e-10]
layerTests['meshQualityControls.minTetQuality']       = [-1e-30, 1e-30, 1e-15, 1e-10, 1e-5, 0.01, 0.1, 0.5, 0.9, 0.95]
layerTests['meshQualityControls.minArea']             = [-1, 0, 1e-30, 1e-20, 1e-10, 1e-5, 1e-3, 0.01, 0.1]
layerTests['meshQualityControls.minTwist']            = [-1e30, 0.0001, 0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]
layerTests['meshQualityControls.minDeterminant']      = [-1, 0.001, 0.01, 0.05, 0.1, 0.5, 0.9, 0.95, 0.99]
layerTests['meshQualityControls.minFaceWeight']       = [-1, 0.001, 0.01, 0.05, 0.1, 0.5, 0.9]
layerTests['meshQualityControls.minVolRatio']         = [-1, 0.001, 0.01, 0.05, 0.1, 0.5, 0.9]
layerTests['meshQualityControls.minTriangleTwist']    = [-1, 0.05, 0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]

layerTests['meshQualityControls.relaxed.maxNonOrtho']      = [40, 50, 60, 70, 80, 90, 180]
layerTests['meshQualityControls.relaxed.minTriangleTwist'] = [-1, 0.05, 0.1, 0.2, 0.4, 0.5]
# layerTests['meshQualityControls.relaxed.minTetQuality']    = [-1e-30, 1e-30, 1e-15, 1e-10]

layerTests['meshQualityControls.nSmoothScale']   = [0, 1, 2, 3, 4, 6, 8, 10, 12]
layerTests['meshQualityControls.errorReduction'] = [0, 0.05, 0.1, 0.2, 0.4, 0.6, 0.7, 0.75, 0.8, 0.9, 0.95, 0.99]
layerTests['mergeTolerance']                     = [1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 5e-3, 1e-2]

layerTests['snapControls.nSmoothPatch']       = [0, 1, 2, 3, 4, 5, 6, 8, 10, 20]
layerTests['snapControls.nSmoothInternal']    = [0, 1, 2, 3, 4, 5, 6]
layerTests['snapControls.tolerance']          = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
layerTests['snapControls.nSolveIter']         = [0, 1, 2, 3, 4, 5, 6, 8, 10, 20, 30, 40, 50]
layerTests['snapControls.nRelaxIter']         = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 30]
layerTests['snapControls.nFeatureSnapIter']   = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 30]
layerTests['snapControls.nFaceSplitInterval'] = [-1, 0, 1, 2]

layerTests['addLayersControls.expansionRatio']            = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
layerTests['addLayersControls.finalLayerThickness']       = [0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0]
layerTests['addLayersControls.minThickness']              = [0.00001, 0.0001, 0.001, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
layerTests['addLayersControls.nGrow']                     = [-1, 0, 1]
layerTests['addLayersControls.featureAngle']              = [0, 15, 30, 45, 60, 75, 90, 105, 120, 130, 140, 160, 180]
layerTests['addLayersControls.mergePatchFacesAngle']      = [0, 15, 30, 45, 60, 75, 90, 105, 120, 160, 180]
layerTests['addLayersControls.layerTerminationAngle']     = [-180, -90, 0, 45, 90, 135, 180]
layerTests['addLayersControls.maxFaceThicknessRatio']     = [0.001, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
layerTests['addLayersControls.nSmoothSurfaceNormals']     = [0, 1, 2, 4, 8, 12, 16, 32]
layerTests['addLayersControls.nSmoothThickness']          = [0, 1, 2, 4, 6, 8, 10, 12, 16, 20, 30, 40, 60]
layerTests['addLayersControls.nSmoothNormals']            = [0, 1, 2, 4, 8, 12, 16]
layerTests['addLayersControls.nSmoothDisplacement']       = [0, 1, 2, 4, 8, 10, 12, 16, 20, 30, 40, 50]
layerTests['addLayersControls.minMedialAxisAngle']        = [0, 5, 15, 30, 45, 90, 120, 180]
layerTests['addLayersControls.maxThicknessToMedialRatio'] = [0.001, 0.01, 0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 1.0, 1.5, 2.0]
layerTests['addLayersControls.slipFeatureAngle']          = [0, 5, 15, 30, 45, 90, 120, 160, 180]
layerTests['addLayersControls.nRelaxIter']                = [0, 1, 2, 3, 4, 6, 8, 12, 20]
layerTests['addLayersControls.nBufferCellsNoExtrude']     = [0, 1, 2, 3, 4, 6, 8, 12, 20]
layerTests['addLayersControls.nLayerIter']                = [0, 1, 2, 3, 4, 6, 8, 12, 20, 40, 60]
layerTests['addLayersControls.nRelaxedIter']              = [0, 1, 2, 3, 4]
layerTests['addLayersControls.nOuterIter']                = [0, 1, 2, 3, 4]


def changeSnappySetting(setting, value, dict='./system/snappyHexMeshDict'):
    os.system('foamDictionary -entry ' + setting + ' -set ' + value + ' ' + dict + ' &> /dev/null')


def is_base_case(setting, value):
    base_value = subprocess.check_output('foamDictionary -value -entry ' + setting + ' ./system/snappy.template', shell=True)
    if value == base_value.decode('ascii').strip():
        return True
    return False


def copy_base_case_results(name):
    os.system(f'cp ../logs/log.snappyHexMesh_base ../logs/log.snappyHexMesh_' + name)
    os.system(f'cp ../logs/log.checkMesh_snapping_base ../logs/log.checkMesh_snapping_' + name)
    os.system(f'cp ../logs/log.checkMesh_layers_base ../logs/log.checkMesh_layers_' + name)
    os.system(f'cp ../images/slice_base.png ../images/slice_' + name + ".png")
    os.system(f'cp ../images/surface_base.png ../images/surface_' + name + ".png")


def store_log_files(name):
    os.system(f'cp log.snappyHexMesh ../logs/log.snappyHexMesh_' + name)
    os.system(f'cp log.checkMesh_snapping ../logs/log.checkMesh_snapping_' + name)
    os.system(f'cp log.checkMesh_layers ../logs/log.checkMesh_layers_' + name)


snappyDict = './system/snappyHexMeshDict'
snappyTemplate = './system/snappy.template'

print("=====\nTotal variations=%d, total parameters=%d" % \
      (sum([len(x) for x in layerTests.values()]), len(layerTests.keys())))

# Generate labels to text file
print("Generating labels..")
labels = "base,\n"
for key, value in layerTests.items():
    for val in value:
        name = f'{key}_{str(val)}'
        if is_base_case(key, str(val)):
            labels += f'BASE VALUE {name},\n'
        else:
            labels += f'{name},\n'
with open("results_labels.txt", "w") as myfile:
    myfile.write(labels)
print("Done")

# Run the base case
name = 'base'
print("=====\nStarting to run case %r" % name)
if os.path.isfile(snappyDict):
    os.remove(snappyDict)
os.system(f'cp {snappyTemplate} {snappyDict}')
os.system(f'./mesh {name} dummy_argument')
os.system(f'cp log.snappyHexMesh ../logs/log.snappyHexMesh_' + name)
os.system(f'cp log.checkMesh_snapping ../logs/log.checkMesh_snapping_' + name)
os.system(f'cp log.checkMesh_layers ../logs/log.checkMesh_layers_' + name)
os.system(f'rm {snappyDict}')

# Run variations
for key, value in layerTests.items():
    for val in value:
        name = f'{key}_{str(val)}'
        # Add time string to image file name end, unless this is the base case
        date_time_string = datetime.now().strftime("%y%m%d%H%M%S")

        print("=====\nStarting to run case %r" % name)
        if is_base_case(key, str(val)):
            print("This variation equals the base case, copying results from the base case")
            copy_base_case_results(f'{date_time_string}_{name}')
            time.sleep(1)
            continue

        os.system(f'cp {snappyTemplate} {snappyDict}')
        changeSnappySetting(key, str(val))
        os.system(f'./mesh {name} {date_time_string}')
        store_log_files(f'{date_time_string}_{name}')
        os.system(f'rm {snappyDict}')
