# Analysis of SnappyLayerTests results

Last updated: 2024-02-17

## Disclaimer

This is my subjective analysis of the SnappyHexMesh meshing results on
a modified motorBike geometry. Conclusions are not universally
applicable.

## Data

[Background, boundary conditions and code to run the tests](./README.md)

Latest results from snappyHexMesh with `nFeatureSnapIter 0` (and
snap `tolerance 1.0`). These results show relatively low level of
noise (visual variance in number of layers):

* [result summary image](http://tkeskita.kapsi.fi/OF/snappyLayerTests_results_run8.png) shows the summary of parameter sweep results
* [slice video](https://vimeo.com/913973776) colored by 0<=nSurfaceLayers<=4
* [surface video](https://vimeo.com/913973744) colored by 0<=nSurfaceLayers<=4

Here are earlier results with `nFeatureSnapIter 3` (and snap
`tolerance 2.0`). These results show relatively high level of noise
(visual variance in number of layers):

* [result summary image](http://tkeskita.kapsi.fi/OF/snappyLayerTests_results_run6.png) shows the summary of parameter sweep results
* [slice video](https://vimeo.com/906686016) colored by 0<=nSurfaceLayers<=4
* [surface video](https://vimeo.com/906685981) colored by 0<=nSurfaceLayers<=4

## General observations

* SnappyHexMesh has >40 parameters that can be varied. Many
  parameters affect the same mesh characteristics, like face
  non-orthogonality, which makes it very hard to control parameter
  values to reach a specific result in non-trivial cases.

* Feature edge snapping (`nFeatureSnapIter > 0`) is often desirable as
  it snaps patches to sharp edges. However, it can also create twisted
  surfaces which can compromise subsequent layer addition. If feature
  edge snapping feature is used, it is best to visually inspect the
  the extracted feature edges
  (`constant/extendedFeatureEdgeMesh/*_edgeMesh.obj` files) and to
  ensure that feature edge snapping is limited only to necessary
  edges.

* Results with `nFeatureSnapIter 3` are noisy: Minor change in almost
  any parameter value affects layer coverage and mesh errors in
  a seemingly chaotic way. Parameter sweeps seem to be necessary to get
  overall trends. With `nFeatureSnapIter 0` the noise level decreases,
  so it is easier to gauge the effect of single parameters on the end
  result.

* Mesh error count (as reported by checkMesh) can be improved by two methods:

  * Tightening a mesh quality criteria (e.g. `minTriangleTwist`) at
    the cost of lowered quality in snapping and layer coverage.

  * increasing `nSmoothScale` value >10 at the cost of increased meshing
    time.

* Good layer coverage seems to require sufficient mesh refinement.  It
  is not possible to achieve good layer coverage with a coarse mesh
  (refinement level 1 in this test).

* Layers seem to be typically removed (collapsed) in regions of high
  surface curvature and large enough change in surface mesh face size.

* OpenFOAM.com option `nOuterIter` value set to target number of
  layers gave highest coverage, at the cost of increased meshing time.

* Cross-correlations are not revealed in these tests. Due to the noise
  in the results, identification of cross-correlations would likely
  require a lot of test points -> would be heavy calculation.
  Nonetheless, some cross-correlations might be worthwhile to
  study, e.g. `nSmoothScale` vs. `errorReduction`.


## Parameter specific observations

Links to latest versions of [snappyHexMeshDict template](./foamCase/system/snappy.template) and [meshQualityDict](./foamCase/system/meshQualityDict)

### meshQualityControls (including mergeTolerance)

* **nSmoothScale<=4** decreases layer coverage. Increase in nSmoothScale to values around 10-20 seems to remove mesh errors, but increases simulation time.
* **0.2<=errorReduction<=0.9** seems best, smaller or larger values decrease layer coverage slightly.
* **mergeTolerance>=1e-6** seems good, and does not seem to affect much.
* **maxNonOrtho<=25** causes mesh errors. maxNonOrtho=5 or 10 increases layer coverage but snapping is bad.
* **10<=maxBoundarySkewness<=50** seems good, and does not seem to affect anything.
* **2<=maxInternalSkewness<=4** seems good. Larger values create skew faces. maxInternalSkewness=4 gave best layer coverage.
* **maxConcave>=60** seems good, and does not seem to affect anything.
* **minVol<=1e-10** seems good. Larger values decrease layer coverage.
* **minTetQuality<=1e-15** seems good. Larger values decrease layer coverage.
* **minArea<=1e-5** seems good. Larger values decrease layer coverage.
* **minTwist<=0.1** seems good. Larger values decrease layer coverage.
* **minDeterminant<=0.01** seems good. Larger values decrease layer coverage.
* **minFaceWeight<=0.05** seems good. Larger values decrease layer coverage.
* **minVolRatio<=0.01** seems good. Larger values decrease layer coverage.
* **minTriangleTwist<=0.2** creates non-orthogonal faces. minTriangleTwist>=0.8 creates bad snapping. Layer coverage increases mildly with minTriangleTwist, and is very high at 90<=minTriangleTwist<=95.
* **relaxed.maxNonOrto > maxNonOrtho(35)** increases layer coverage up to value 70 or 80. Relaxed maxNonOrtho 70 seems good.
* **relaxed.minTriangleTwist < minTriangleTwist(0.6)** does not increase layer coverage.

### snapControls

* **nSmoothPatch=2 is** good, larger values create skewed faces (and visualization shows missing cells in the mesh?).
* **nSmoothInternal=1** or 2 is good, larger values does not affect anything.
* **1.5<=tolerance<=3.0** looks good, no clear effect on layer coverage or mesh errors.
* **2<=nSolveIter<=6** seems enough to relax the mesh on visual inspection, otherwise only minor effects.
* **2<=nRelaxIter<=10** seems enough to relax the mesh on visual inspection, otherwise only minor effects.
* **nFeatureSnapIter=3** seems enough to snap to feature edges on visual inspection. nFeatureSnapIter>=5 seems to create mesh errors and decreases layer coverage. nFeatureSnapIter=0 allows better layer addition in spots where snapping to feature edges creates twists, like in the wind shield.
* **nFaceSplitInterval=-1=0** is good. Values >0 increase layer coverage slightly, but create some skewed faces and more non-manifold points.

### addLayersControls

* **expansionRatio>=1.3** leads to decrease in layer coverage.
* **0.2<=finalLayerThickness<=0.6** gives best layer coverage (for expansionRatio 1.2). finalLayerThickness>=0.6 creates squished mesh where two layer extrusion fronts tend to meet.
* **minThickness>0.1** decreases layer coverage.
* **nGrow>0** deteriorates layer addition.
* **45<=nFeatureAngle<=160** seems good. Slightly increased layer coverage near 90.
* **30<=mergePatchFacesAngle<=90** seems good. mergePatchFacesAngle>90 does not seem to affect anything.
* **-90<=layerTerminationAngle<=90** deteriorates layer coverage, otherwise not much effect.
* **0.3<=maxFaceThicknessRatio<=1.0** seems good.
* **nSmoothSurfaceNormals>=0** seems good. nSmoothSurfaceNormals=8 or 12 seems good enough on visual inspection for relaxing the mesh. nSmoothSurfaceNormals>2 decreases layer coverage slightly and about linearly.
* **nSmoothThickness=2** seems good. nSmoothThickness>2 start to decrease layer coverage slightly and about linearly.
* **nSmoothNormals>0** does not seem to affect anything much.
* **nSmoothDisplacement>2** seems good on visual inspection. With more iterations the layer coverage increases linearly on average, but the effect is very minor.
* **minMedialAxisAngle=90** seems good. Layer coverage increases with increasing minMedialAxisAngle, but minMedialAxisAngle>90 seems to create twists on the background mesh on visual inspection.
* **0.2<=maxThicknessToMedialRatio<=0.7** seems good, but maxThicknessToMedialRatio>0.7 seems to cause mesh squishing in visual inspection.
* **slipFeatureAngle** has no effect in this case.
* **2<=nRelaxIter<=12** seems good. nRelaxIter=1 creates numerous mesh errors. Increasing nRelaxIter increases meshing time.
* **nBufferCellsNoExtrude>0** decreases layer coverage.
* **4<=nLayerIter<=12** seems good. nLayerIter>12 does not seem to change anything. nLayerIter=1 creates the best layer coverage and the worst amount of mesh errors.
* **nRelaxedIter>0** decreases layer coverage radically.
* **nOuterIter=4** (=target number of layers) generates best layer coverage with a smooth nSurfaceLayers transitions, but is computationally heavy.


## Feedback

[Link to discussion thread on CFD-Online](https://www.cfd-online.com/Forums/openfoam-meshing/254447-snappyhexmesh-parametric-sweep-study.html)