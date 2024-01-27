# SnappyLayerTests

## Summary

This repository contains program code for running automated
[SnappyHexMesh](https://www.openfoam.com/documentation/guides/latest/doc/guide-meshing-snappyhexmesh.html)
parameter variation sweeps.
I used the testing framework from the inspiring repository
https://github.com/Ben-Malin/snappyLayerTests as a basis.
Aim was to evaluate how different SnappyHexMesh parameter values
affect the resulting mesh when only one parameter value was changed at
a time.

## Setup

* x64 Ubuntu Linux 20.04.6
* Python 3.8
* OpenFOAM.com v2312
* Paraview 5.9.1

## Test case

* Modified OpenFOAM motorBike.obj geometry (minor mesh editing,
  clean-up and separated manifold and non-manifold surfaces to
  separate STL files). This tutorial geometry is highly complex and
  thereby a good test for automatic mesh generation software.
* Using constant cubic block mesh size (50 mm side length) as a
  background mesh, with one surface refinement level around the motor
  bike surfaces (25 mm side length). That made the computational
  effort tolerable for a home PC. However, the downside is that layer
  addition is only partial at this mesh resolution.
* Target of four layers only (because of computational effort).
* Using only explicit feature in snapping phase (`explicitFeatureSnap true`).
  Surface feature extraction applied feature angle value 150.
* For SnappyHexMesh base setup I used the settings produced by the
  [SnappyHexMesh GUI Blender add-on](https://github.com/tkeskita/snappyhexmesh_gui)
  (version at the time was 1.5) as a basis (set nFaceSplitInterval to -1).

## How to run tests

Edit `foamCase/mesh` file (last line) to point to pvpython of Paraview 5.9.1,
then run following commands in terminal:

```
cd foamCase
. /usr/lib/openfoam/openfoam2312/etc/bashrc
./remove_results
surfaceFeatureExtract
python3 batchRun.py
python3 process_logfiles.py
python3 plot_results.py
```

Zero result for average number of layers means that either no layers
were added, or SnappyHexMesh run failed. The run logs are saved to
the `logs` folder, and mesh pictures in the `images` folder.
