"""
Main script, used to run through a sweep of snappyHexMesh settings
and save the results.
"""

import os

layerTests = {}

layerTests['snapControls.nSmoothPatch']       = [0, 1, 2, 3, 4, 5, 6, 8, 10, 20]
# nSmoothInternal affects only implicit feature snapping cases
# layerTests['snapControls.nSmoothInternal']    = [0, 1, 2, 3, 4, 5, 6, 8, 10, 20]
layerTests['snapControls.tolerance']          = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
layerTests['snapControls.nSolveIter']         = [0, 1, 2, 3, 4, 5, 6, 8, 10, 20, 30, 40, 50]
layerTests['snapControls.nRelaxIter']         = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 30]
layerTests['snapControls.nFeatureSnapIter']   = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 30]
layerTests['snapControls.nFaceSplitInterval'] = [-1, 0, 1, 2, 3, 4, 5, 6]

layerTests['addLayersControls.expansionRatio']            = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
layerTests['addLayersControls.finalLayerThickness']       = [0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0]
layerTests['addLayersControls.minThickness']              = [0.00001, 0.0001, 0.001, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]
layerTests['addLayersControls.nGrow']                     = [-1, 0, 1]
layerTests['addLayersControls.featureAngle']              = [0, 15, 30, 45, 60, 75, 90, 105, 120, 160, 180]
layerTests['addLayersControls.mergePatchFacesAngle']      = [0, 15, 30, 45, 60, 75, 90, 105, 120, 160, 180]
layerTests['addLayersControls.layerTerminationAngle']     = [-180, -90, 0, 45, 90, 135, 180]
layerTests['addLayersControls.maxFaceThicknessRatio']     = [0.001, 0.01, 0.1, 0.3, 0.5, 0.7, 1.0]
layerTests['addLayersControls.nSmoothSurfaceNormals']     = [0, 1, 2, 4, 8, 12, 16, 32]
layerTests['addLayersControls.nSmoothThickness']          = [0, 1, 2, 4, 8, 12, 16, 32]
layerTests['addLayersControls.nSmoothNormals']            = [0, 1, 2, 4, 8, 12, 16]
layerTests['addLayersControls.nSmoothDisplacement']       = [0, 1, 2, 4, 8, 12, 20, 50, 75, 100]
layerTests['addLayersControls.minMedialAxisAngle']        = [0, 5, 15, 30, 45, 90, 120, 180]
layerTests['addLayersControls.maxThicknessToMedialRatio'] = [0.001, 0.01, 0.1, 0.2, 0.5, 0.7, 1.0, 1.5, 2.0]
layerTests['addLayersControls.slipFeatureAngle']          = [0, 5, 15, 30, 45, 90, 120, 160, 180]
layerTests['addLayersControls.nRelaxIter']                = [0, 1, 2, 3, 4, 8, 12, 20]
layerTests['addLayersControls.nBufferCellsNoExtrude']     = [0, 1, 2, 3, 4, 8, 12, 20]
layerTests['addLayersControls.nLayerIter']                = [0, 1, 2, 3, 4, 8, 20, 50, 75, 100]
layerTests['addLayersControls.nRelaxedIter']              = [0, 1, 2, 3, 4]
layerTests['addLayersControls.nOuterIter']                = [0, 1, 2, 3, 4]

layerTests['meshQualityControls.nSmoothScale']   = [0, 1, 2, 3, 4, 6, 8, 10, 12]
layerTests['meshQualityControls.errorReduction'] = [0, 0.05, 0.1, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
layerTests['mergeTolerance']                     = [1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 5e-3, 1e-2]

def changeSnappySetting(setting, value, dict='./system/snappyHexMeshDict'):
    os.system('foamDictionary -entry ' + setting + ' -set ' + value + ' ' + dict)

snappyDict = './system/snappyHexMeshDict'
snappyTemplate = './system/snappy.template'

if os.path.isfile(snappyDict):
    os.remove(snappyDict)

for key, value in layerTests.items():
    for val in value:
        print("=====\nStarting to run case %r" % (str(key) + "=" + str(val)))
        os.system(f'cp {snappyTemplate} {snappyDict}')
        changeSnappySetting(key, str(val))
        name = f'{key}_{str(val)}'
        os.system(f'./mesh {name}')
        os.system(f'mv log.snappyHexMesh ../logs/log.snappyHexMesh_' + f'{key}_{str(val)}')
        os.system(f'mv log.checkMesh_time2 ../logs/log.checkMesh_time2_' + f'{key}_{str(val)}')
        os.system(f'mv log.checkMesh_time3 ../logs/log.checkMesh_time3_' + f'{key}_{str(val)}')
        os.system(f'rm {snappyDict}')
