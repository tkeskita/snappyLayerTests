'''
Paraview python script
'''
#paraview.compatibility.major 5
#paraview.compatibility.major 9

import os
import sys
from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

name = sys.argv[1]
date_time_string = str(sys.argv[2])

screenshotDir = '../images'
if not os.path.exists(screenshotDir):
    os.makedirs(screenshotDir)

# Add time string to image file name end, unless this is the base case
if name == 'base':
    file_name_end = 'base'
else:
    file_name_end = date_time_string + "_" + name


###########################
##      Functions        ##
###########################

# create a new 'OpenFOAMReader'
def loadFoam(dotFoamFile: str, path: str):
    casefoam = OpenFOAMReader(registrationName=dotFoamFile, FileName=path)
    casefoam.SkipZeroTime = 0
    casefoam.CaseType = 'Reconstructed Case'
    casefoam.MeshRegions = ['internalMesh', 'walls_manifold', 'walls_nonmanifold_slave']
    casefoam.CellArrays = ['nSurfaceLayers', 'thickness', 'thicknessFraction']
    casefoam.Decomposepolyhedra = 0

    # return the casefoam object
    return casefoam

def displayDefaults(displayObj,variable: str):
    return displayObj

def meshSlice(casefoam):
    # extract just the internalField
    extractBlock1 = ExtractBlock(registrationName='ExtractBlock1', Input=casefoam)
    extractBlock1.BlockIndices = [1]

    # create a new 'Slice'
    slice1 = Slice(registrationName='Slice1', Input=extractBlock1)
    slice1.SliceType = 'Plane'
    slice1.SliceOffsetValues = [0.0]
    slice1.SliceType.Origin = [0, 0.0125, 0]
    slice1.SliceType.Normal = [0.0, 1.0, 0.0]
    slice1.Triangulatetheslice = 0
    return slice1

def setOverheadCam(camera):
    camera.SetPosition([0.75, -4, 0.75])
    camera.SetFocalPoint([0.75, 0, 0.75])
    camera.SetViewUp([0, 0, 1])
    camera.SetParallelScale(0.8)
    return camera

def setPerspectiveCam(camera):
    camera.SetPosition([-1.4, -3, 2.5])
    camera.SetFocalPoint([0.75, 0, 0.75])
    camera.SetViewUp([0, 0, 1])
    camera.SetParallelScale(0.9)
    return camera

def meshSurface(casefoam):
    extractBlock2 = ExtractBlock(registrationName='ExtractBlock2', Input=casefoam)
    extractBlock2.BlockIndices = [2]
    return extractBlock2

###########################
## Start the main script ##
###########################

renderView0 = GetActiveViewOrCreate('RenderView')

## check if a file exists in the directory called case.foam, if not, create it using touch
if not os.path.exists('./case.foam'):
    os.system('touch ./case.foam')

# create a new 'OpenFOAMReader'
casefoam = loadFoam('case.foam', f'./')
animationScene1 = GetAnimationScene()
animationScene1.GoToLast()

## Make a new render view, swap to it and set the camera
SetActiveView(None)
layout1 = CreateLayout(name='Layout #1')
renderView1 = CreateView('RenderView')
renderView1.CameraParallelProjection = 1
renderView1.OrientationAxesVisibility = 0
renderView1.Background = [1.0, 1.0, 1.0]
AssignViewToLayout(view=renderView1, layout=layout1, hint=0)
camera = GetActiveCamera()
setOverheadCam(camera)

# Create a slice to display the mesh cross section
slice1 = meshSlice(casefoam)
slice1Display = GetDisplayProperties(slice1, view=renderView1)
slice1Display.SetRepresentationType('Surface With Edges')
ColorBy(slice1Display, ('CELLS', 'nSurfaceLayers'))
slice1Display.ScaleFactor = 50
LUT = GetColorTransferFunction('nSurfaceLayers')
LUT.RescaleTransferFunction(0.0, 4.0)

# text1 = Text(registrationName=name)
# text1.Text = name
# text1Display = Show(text1, renderView1, 'TextSourceRepresentation')
# if name == 'base':
#     text1Display.Color = [1.0, 0.0, 0.0]
# else:
#     text1Display.Color = [1.0, 1.0, 1.0]
# text1Display.FontSize = 50

SaveScreenshot(f'{screenshotDir}/slice_{file_name_end}.png',renderView1,ImageResolution=[2400,1600])

## Make a new render view, swap to it and set the camera
SetActiveView(None)
layout2 = CreateLayout(name='Layout #2')
renderView2 = CreateView('RenderView')
renderView2.OrientationAxesVisibility = 0
renderView2.Background = [1.0, 1.0, 1.0]
AssignViewToLayout(view=renderView2, layout=layout2, hint=0)
camera = GetActiveCamera()
setPerspectiveCam(camera)

extractBlock2 = meshSurface(casefoam)

# text2Display = Show(text1, renderView2, 'TextSourceRepresentation')
# if name == 'base':
#     text2Display.Color = [1.0, 0.0, 0.0]
# else:
#     text2Display.Color = [0.0, 0.0, 0.0]
# text2Display.FontSize = 50

extractBlock2Display = Show(extractBlock2, renderView2, 'GeometryRepresentation')
extractBlock2Display.AmbientColor = [1.0, 1.0, 1.0]
extractBlock2Display.DiffuseColor = [1.0, 1.0, 1.0]

# Only surfaces with white color to see surface smoothness
SaveScreenshot(f'{screenshotDir}/clay_{file_name_end}.png',renderView2,ImageResolution=[2400,2400])

# Color by surface layers
ColorBy(extractBlock2Display, ('CELLS', 'nSurfaceLayers'))
extractBlock2Display.SetRepresentationType('Surface With Edges')
LUT = GetColorTransferFunction('nSurfaceLayers')
LUT.RescaleTransferFunction(0.0, 4.0)

SaveScreenshot(f'{screenshotDir}/surface_{file_name_end}.png',renderView2,ImageResolution=[2400,2400])
