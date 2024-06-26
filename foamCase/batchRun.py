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

# Test sweeps
# -----------
layerTests['addLayers'] = ['true']  # Run only base case

# Start of full sweep definitions
# -------------------------------
layerTests['addLayers'] = ['true', 'false']
layerTests['mergePatchFaces'] = ['true', 'false']
layerTests['mergeTolerance'] = [1e-7, 1e-6, 1e-5, 1e-4]

layerTests['meshQualityControls.nSmoothScale']        = [0, 1, 2, 3, 4, 5, 6, 7, 8]
layerTests['meshQualityControls.errorReduction']      = [0, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
layerTests['meshQualityControls.maxNonOrtho']         = [30, 35, 40, 45, 50, 55, 60, 65, 70]
layerTests['meshQualityControls.maxBoundarySkewness'] = [0.5, 0.7, 0.8, 0.9, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 4, 8, 10, 20]
layerTests['meshQualityControls.maxInternalSkewness'] = [0.5, 0.7, 0.8, 0.9, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 4]
layerTests['meshQualityControls.maxConcave']          = [1, 2, 5, 10, 20, 30, 40, 50, 60, 80]
layerTests['meshQualityControls.minVol']              = [1e-15, 1e-9, 1e-8, 3e-8, 5e-8, 8e-8, 1e-7, 2e-7]
layerTests['meshQualityControls.minTetQuality']       = [1e-15, 1e-12, 1e-10, 1e-7, 1e-5, 1e-4, 3e-4, 6e-4, 1e-3]
layerTests['meshQualityControls.minArea']             = [1e-30, 1e-6, 6e-6, 1e-5, 3e-5, 6e-5, 1e-4, 2e-4, 5e-4, 7e-4, 1e-3]
layerTests['meshQualityControls.minTwist']            = [0.001, 0.005, 0.01, 0.05, 0.1, 0.15, 0.2]
layerTests['meshQualityControls.minDeterminant']      = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05]
layerTests['meshQualityControls.minFaceWeight']       = [0.001, 0.005, 0.01, 0.03, 0.05, 0.07, 0.1, 0.15, 0.2]
layerTests['meshQualityControls.minVolRatio']         = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2]
layerTests['meshQualityControls.minTriangleTwist']    = [0.4, 0.5, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]

layerTests['meshQualityControls.relaxed.maxNonOrtho'] = [50, 55, 60, 65, 70, 75, 80, 85]

layerTests['castellatedMeshControls.minRefinementCells']  = [0, 1, 2, 4, 6, 10, 15, 20, 30]
layerTests['castellatedMeshControls.nCellsBetweenLevels'] = [1, 2, 3, 4, 5, 6]
layerTests['castellatedMeshControls.resolveFeatureAngle'] = [0, 10, 20, 30, 40, 50, 60]
layerTests['castellatedMeshControls.planarAngle']         = [0, 10, 20, 30, 40, 50, 60]
layerTests['castellatedMeshControls.useLeakClosure']      = ['true', 'false']
layerTests['castellatedMeshControls.handleSnapProblems']  = ['true', 'false']
layerTests['castellatedMeshControls.useTopologicalSnapDetection'] = ['true', 'false']

layerTests['snapControls.nSmoothPatch']       = [0, 1, 2, 3, 4, 8, 10, 20]
layerTests['snapControls.nSmoothInternal']    = [0, 1, 2, 3, 4]
layerTests['snapControls.tolerance']          = [0.8, 0.9, 1, 1.1, 1.2, 1.5, 2, 2.5, 3, 3.5, 4]
layerTests['snapControls.nSolveIter']         = [0, 1, 2, 3, 4, 5, 6, 8, 10, 20, 30]
layerTests['snapControls.nRelaxIter']         = [0, 1, 2, 3, 4, 5, 6, 8, 10, 20]
layerTests['snapControls.nFeatureSnapIter']   = [0, 1, 2, 3, 4, 5, 6, 8, 10, 20]
layerTests['snapControls.nFaceSplitInterval'] = [-1, 0, 1, 2]
layerTests['snapControls.releasePoints']      = ['true', 'false']
layerTests['snapControls.stringFeatures']     = ['true', 'false']
layerTests['snapControls.avoidDiagonal']      = ['true', 'false']
layerTests['snapControls.strictRegionSnap']   = ['true', 'false']
layerTests['snapControls.concaveAngle']       = [0, 10, 20, 30, 40, 45, 50, 60, 70]
layerTests['snapControls.minAreaRatio']       = [0.1, 0.2, 0.3, 0.4, 0.5]

layerTests['addLayersControls.expansionRatio']            = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6667]
layerTests['addLayersControls.finalLayerThickness']       = [0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
layerTests['addLayersControls.minThickness']              = [0.00001, 0.0001, 0.001, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
layerTests['addLayersControls.nGrow']                     = [-1, 0, 1]
layerTests['addLayersControls.featureAngle']              = [0, 15, 30, 45, 65, 75, 85, 95, 105, 120, 130, 140, 160, 180]
layerTests['addLayersControls.mergePatchFacesAngle']      = [0, 15, 30, 45, 60, 75, 90, 105, 120, 160, 180]
layerTests['addLayersControls.layerTerminationAngle']     = [-180, 0, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
layerTests['addLayersControls.maxFaceThicknessRatio']     = [0.001, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 1]
layerTests['addLayersControls.disableWallEdges']          = ['true', 'false']
layerTests['addLayersControls.nSmoothSurfaceNormals']     = [0, 1, 2, 4, 6, 8, 10, 12, 16, 20, 30]
layerTests['addLayersControls.nSmoothThickness']          = [0, 1, 2, 4, 8, 12, 16, 20, 30]
layerTests['addLayersControls.nSmoothNormals']            = [0, 1, 2, 4, 8]
layerTests['addLayersControls.nSmoothDisplacement']       = [0, 1, 2, 4, 8, 10, 12, 16, 20, 30]
layerTests['addLayersControls.nMedialAxisIter']           = [0, 1, 2, 4, 8, 10, 20, 1000]
layerTests['addLayersControls.minMedialAxisAngle']        = [0, 5, 15, 30, 45, 90, 120, 180]
layerTests['addLayersControls.maxThicknessToMedialRatio'] = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
layerTests['addLayersControls.slipFeatureAngle']          = [0, 15, 30, 90, 120, 160, 180]
layerTests['addLayersControls.nRelaxIter']                = [0, 1, 2, 3, 4, 6, 8, 10, 12, 15, 20]
layerTests['addLayersControls.nBufferCellsNoExtrude']     = [0, 1, 2, 3, 4, 8]
layerTests['addLayersControls.nLayerIter']                = [0, 1, 2, 3, 4, 6, 8, 10, 20]
layerTests['addLayersControls.nRelaxedIter']              = [0, 1, 2, 3, 4]
layerTests['addLayersControls.nOuterIter']                = [0, 1, 2, 1000]

# Test for two parameter combinations. Disabled for now.
# layerTests = {}
var1Tests = {}
# var1Tests['meshQualityControls.errorReduction'] = [0.01, 0.05, 0.15, 0.65, 0.75, 0.85, 0.95, 0.99]
var2Tests = {}
# var2Tests['meshQualityControls.nSmoothScale'] = [1, 2, 4, 8, 16, 32]


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
    os.system(f'cp ../logs/log.checkMesh_layers_important_checks_base ../logs/log.checkMesh_layers_important_checks' + name)
    os.system(f'cp ../logs/log.checkMesh_layers_all_checks_base ../logs/log.checkMesh_layers_all_checks_' + name)
    os.system(f'cp ../logs/log.simpleFoam_base ../logs/log.simpleFoam_' + name)
    os.system(f'cp ../logs/log.fieldMinMax_base ../logs/log.fieldMinMax_' + name)
    os.system(f'cp ../images/slice_base.png ../images/slice_' + name + ".png")
    os.system(f'cp ../images/surface_base.png ../images/surface_' + name + ".png")
    os.system(f'cp ../images/clay_base.png ../images/clay_' + name + ".png")


def store_log_files(name):
    os.system(f'cp log.snappyHexMesh ../logs/log.snappyHexMesh_' + name)
    os.system(f'cp log.checkMesh_snapping ../logs/log.checkMesh_snapping_' + name)
    os.system(f'cp log.checkMesh_layers_important_checks ../logs/log.checkMesh_layers_important_checks_' + name)
    os.system(f'cp log.checkMesh_layers_all_checks ../logs/log.checkMesh_layers_all_checks_' + name)

    # Create empty log files if no files were created, to make postprocessing easy
    if not os.path.isfile("solverCase/log.simpleFoam"):
        open("../logs/log.simpleFoam_" + name, "a").close()
    else:
        os.system(f'cp solverCase/log.simpleFoam ../logs/log.simpleFoam_' + name)
    if not os.path.isfile("solverCase/postProcessing/minMaxMagnitude()/0/fieldMinMax.dat"):
        open("../logs/log.fieldMinMax_" + name, "a").close()
    else:
        os.system(f'cp solverCase/postProcessing/minMaxMagnitude\(\)/0/fieldMinMax.dat ../logs/log.fieldMinMax_' + name)


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
# raise Exception("Stop here when regenerating labels afterwards")

# Run the base case
name = 'base'
print("=====\nStarting to run case %r" % name)
if os.path.isfile(snappyDict):
    os.remove(snappyDict)
os.system(f'cp {snappyTemplate} {snappyDict}')
os.system(f'./mesh {name} dummy_argument')
store_log_files(name)
os.system(f'rm {snappyDict}')
# raise Exception("Stop here when debugging the base case")

# Run single parameter variations
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

# Run two parameter variations
for key1, values1 in var1Tests.items():
    for val1 in values1:
        for key2, values2 in var2Tests.items():
            for val2 in values2:
                name = f'{key1}_{str(val1)}_and_{key2}_{str(val2)}'
                # Add time string to image file name end, unless this is the base case
                date_time_string = datetime.now().strftime("%y%m%d%H%M%S")

                print("=====\nStarting to run case %r" % name)
                os.system(f'cp {snappyTemplate} {snappyDict}')
                time.sleep(1)
                changeSnappySetting(key1, str(val1))
                time.sleep(1)
                changeSnappySetting(key2, str(val2))
                time.sleep(1)
                os.system(f'./mesh {name} {date_time_string}')
                store_log_files(f'{date_time_string}_{name}')
                os.system(f'rm {snappyDict}')

