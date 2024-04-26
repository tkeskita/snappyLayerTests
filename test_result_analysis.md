# Analysis of SnappyLayerTests results

Last updated: 2024-04-26

## Disclaimer

This is my subjective analysis of the SnappyHexMesh meshing results on
a modified motorBike geometry. Conclusions are not universally
applicable.

## Data

[Background, boundary conditions and code to run the tests](./README.md)

Results with simpleFoam solver (un)stability testing, using maximum of
max(mag(U)) from iterations 30-200 as a measure of unstability. This
case applied values `layerTerminationAngle 20`, `maxInternalSkewness
1.5`, `maxBoundarySkewness 2.0`. A key change was to decrease under
relaxation of `U` (from 0.9 to 0.8) for simpleFoam. This increased the
stability of the solution significantly (using `consistent yes` for
`SIMPLE`).

* [unstability vs. mean layer coverage plots of variables](http://tkeskita.kapsi.fi/OF/snappyLayerTests_results_montage_run46.png)
* [mean layer coverage result plot](http://tkeskita.kapsi.fi/OF/snappyLayerTests_results_run46.png)
* [stability result plot](http://tkeskita.kapsi.fi/OF/snappyLayerTests_results_solver_run46.png)
* [slice video](https://vimeo.com/939556131) colored by 0<=nSurfaceLayers<=4
* [surface video](https://vimeo.com/939556168) colored by 0<=nSurfaceLayers<=4
* [clay video](https://vimeo.com/939556098) white surfaces to visualize snapping

---

Results with simpleFoam solver (un)stability testing, using
maximum of max(mag(U)) from iterations 10-200 as a measure of
unstability.  In this case, the value of `maxInternalSkewness` was
lowered from 4 to 1.5, as it seemed to provide fairly stable results
(although there is still some noise). Layer coverage seems to be good
and consistent in smooth surface areas, and collapsed in high
curvature areas.

* [unstability vs. mean layer coverage plots of variables](http://tkeskita.kapsi.fi/OF/snappyLayerTests_results_montage_run31.png)
* [mean layer coverage result plot](http://tkeskita.kapsi.fi/OF/snappyLayerTests_results_run31.png)
* [stability result plot](http://tkeskita.kapsi.fi/OF/snappyLayerTests_results_solver_run31.png)
* [slice video](https://vimeo.com/934492878) colored by 0<=nSurfaceLayers<=4
* [surface video](https://vimeo.com/934492908) colored by 0<=nSurfaceLayers<=4
* [clay video](https://vimeo.com/934492863) white surfaces to visualize snapping

---

Below are the previous results from snappyHexMesh with `mergePatchFaces false` and
`nFeatureSnapIter 0`, including also some less common snappyHexMesh
parameters in the variations:

* [result summary image](http://tkeskita.kapsi.fi/OF/snappyLayerTests_results_run13.png) shows the summary of parameter sweep results
* [slice video](https://vimeo.com/916759473) colored by 0<=nSurfaceLayers<=4
* [surface video](https://vimeo.com/916759534) colored by 0<=nSurfaceLayers<=4
* [clay video](https://vimeo.com/916759617) white surfaces to visualize snapping

---

Below are the previous results with `nFeatureSnapIter 0` (and
snap `tolerance 1.0`). These results show relatively low level of
noise (visual variance in number of layers):

* [result summary image](http://tkeskita.kapsi.fi/OF/snappyLayerTests_results_run8.png) shows the summary of parameter sweep results
* [slice video](https://vimeo.com/913973776) colored by 0<=nSurfaceLayers<=4
* [surface video](https://vimeo.com/913973744) colored by 0<=nSurfaceLayers<=4
* [clay video](https://vimeo.com/914195069) white surfaces to visualize snapping

---

Here are earlier results with `nFeatureSnapIter 3` (and snap
`tolerance 2.0`). These results show relatively high level of noise
(visual variance in number of layers):

* [result summary image](http://tkeskita.kapsi.fi/OF/snappyLayerTests_results_run6.png) shows the summary of parameter sweep results
* [slice video](https://vimeo.com/906686016) colored by 0<=nSurfaceLayers<=4
* [surface video](https://vimeo.com/906685981) colored by 0<=nSurfaceLayers<=4

## General observations

* SnappyHexMesh has >40 parameters that can be varied (>50 if you
  count the less often used as well). Many parameters affect the same
  mesh characteristics, like face non-orthogonality, which makes it
  very hard to control parameter values to reach a specific result in
  non-trivial cases.

* Feature edge snapping (`nFeatureSnapIter > 0`) is often desirable as
  it snaps patch edges to sharp edges in the geometry. However, it can
  also create twisted surfaces which can compromise subsequent layer
  addition. If feature edge snapping feature is used, it is best to
  visually inspect the the extracted feature edges
  (`constant/extendedFeatureEdgeMesh/*_edgeMesh.obj` files) and to
  ensure that feature edge snapping is limited only to the necessary
  edges.

* Results with `nFeatureSnapIter > 0` are very noisy: Minor change in
  almost any parameter value affects layer coverage and mesh errors in
  a seemingly chaotic or random way. Parameter sweeps seem to be
  necessary to get overall trends. With `nFeatureSnapIter 0` the noise
  level decreases for many parameters, so it is easier to gauge the
  effect of single parameters on the end result.

* Mesh error count (as reported by checkMesh) can be improved by two methods:

  * Increasing the value of a mesh quality criteria
    (e.g. minTetQuality, minTwist, minDeterminant, minFaceWeight,
    minVolRatio, or minTriangleTwist). The cost is lowered quality in
    snapping and decrease in layer coverage. For example, the extreme
    setting of `minTriangleTwist 0.9` removed all but non-manifold
    point errors, but the quality of snapping and layer coverage were
    clearly decreased.

  * `nSmoothScale > 10` seems to slighly decrease mesh errors on
    average, but variance is large. Meshing time is increased
    significantly with increase in nSmoothScale.

* Good layer coverage seems to require sufficient mesh refinement. It
  is not possible to achieve good layer coverage with a coarse mesh
  (refinement level 1 in this test).

* Layers seem to be typically removed (collapsed) in regions of high
  surface curvature and large enough change in surface mesh face size.

* Surface curvature (angle between adjacent surface mesh faces) is
  critical for layers: Flat surface gives consistently high layer
  coverage, and bending surfaces loses layers consistently. On medium
  curvature it's a gamble: Changing almost any parameter can either
  grow layers or collapse layers randomly, and the effect seems to be
  chaotic.

* OpenFOAM.com option `nOuterIter` value set to target number of
  layers (or a very large value like 1000) gave highest coverage, at
  the cost of increased meshing time.

* Some outlier parameter values (value out of normal or typical range)
  can result in significantly improved layer coverage
  (e.g. `nLayerIter 1`), but the resulting mesh contains severe
  errors.

* Cross-correlations are not revealed in single parameter sweep
  tests. Due to the noise in the results, identification of
  cross-correlations would likely require a lot of test points ->
  would be heavy calculation.  Nonetheless, some cross-correlations
  might be worthwhile to study, e.g. `nSmoothScale`
  vs. `errorReduction`.

* A low of `layerTerminationAngle`, `maxInternalSkewness`, and
  `maxBoundarySkewness` seem to be highly correlated with simpleFoam
  solver stability. Current best values which seem to provide stable
  solution are `layerTerminationAngle 20`, `maxInternalSkewness 1.5`
  and `maxBoundarySkewness 2.0`.


## Parameter specific observations

Links to latest versions of [snappyHexMeshDict template](./foamCase/system/snappy.template) and [meshQualityDict](./foamCase/system/meshQualityDict)

### top level parameters

* **mergePatchFaces false** increases layer coverage a bit, possibly because surface mesh cells are flatter and face size differences are small.
* **mergeTolerance>=1e-6** seems good, and does not seem to affect much.

### meshQualityControls

* **nSmoothScale<=4** decreases layer coverage. nSmoothScale>10 seems to decrease mesh errors (decrease is mild and chaotic), but it also increases simulation time significantly.
* **0.2<=errorReduction<=0.9** seems best, smaller or larger values decrease layer coverage slightly.
* **30<=maxNonOrtho<=70** seems good. **maxNonOrtho<=25** causes mesh errors.
* **2<=maxBoundarySkewness<=50** seems good. Low values seem to increase simpleFoam stability.
* **0.8<=maxInternalSkewness<=4** seems good. Low values seem to increase simpleFoam stability. Larger values create skew faces. maxInternalSkewness=4 gave best layer coverage, and maxInternalSkewness<=2 improves simpleFoam stability (decreases max(mag(U)).
* **20<=maxConcave<=80** seems good, and does not seem to affect anything much. **maxConcave<=20** decreases coverage.
* **1e-30<=minVol<=1e-10** seems good. Larger values decrease layer coverage and create mesh errors.
* **1e-30<=minTetQuality<=1e-10** seems good. Larger values decrease layer coverage and then start to create mesh errors.
* **1e-30<=minArea<=1e-5** seems good. Larger values decrease layer coverage.
* **minTwist<=0.1** seems good. Larger values decrease layer coverage.
* **minDeterminant<=0.01** seems good. Larger values decrease layer coverage.
* **minFaceWeight<=0.05** seems good. Larger values decrease layer coverage and increase unstability of simpleFoam solution.
* **minVolRatio<=0.01** seems good. Larger values decrease layer coverage.
* **minTriangleTwist<=0.8** seems good. Larger values decrease layer coverage.
* **relaxed.maxNonOrto > maxNonOrtho(35)** increases layer coverage up to relaxed.maxNonOrtho=70 or 80.
* **relaxed.minTriangleTwist < minTriangleTwist(0.6)** does not increase layer coverage.

### snapControls

* **nSmoothPatch=2 is** good, larger values create skewed faces (and visualization shows missing cells in the mesh?).
* **nSmoothInternal=1** or 2 is good, larger values does not affect anything.
* **1.0<=tolerance<=3.0** looks good, no clear effect on layer coverage or mesh errors.
* **2<=nSolveIter<=6** seems enough to relax the mesh on visual inspection, otherwise only minor effects.
* **2<=nRelaxIter<=10** seems enough to relax the mesh on visual inspection, otherwise only minor effects.
* **nFeatureSnapIter=3** seems enough to snap to feature edges on visual inspection. nFeatureSnapIter>=5 seems to create mesh errors and decreases layer coverage. nFeatureSnapIter=0 allows better layer addition in spots where snapping to feature edges creates twists, like in the wind shield.
* **nFaceSplitInterval=-1=0** seems good. Values >0 may increase layer coverage slightly, and create some skewed faces and more non-manifold points.

### addLayersControls

* **expansionRatio>=1.3** may lead to decrease in layer coverage.
* **0.2<=finalLayerThickness<=0.6** gives best layer coverage (for expansionRatio 1.2). finalLayerThickness>=0.6 creates squished mesh where two layer extrusion fronts tend to meet.
* **minThickness>0.1** decreases layer coverage.
* **nGrow>0** deteriorates layer addition.
* **45<=nFeatureAngle<=160** seems good. Slightly increased layer coverage near 90.
* **30<=mergePatchFacesAngle<=90** seems good. mergePatchFacesAngle>90 does not seem to affect anything.
* **-90<=layerTerminationAngle<=90** deteriorates layer coverage, otherwise not much effect.
* **0.5<=maxFaceThicknessRatio<=1.0** seems good.
* **nSmoothSurfaceNormals>=0** seems good. nSmoothSurfaceNormals=8 seems good enough on visual inspection for relaxing the mesh. nSmoothSurfaceNormals>2 decreases layer coverage slightly and about linearly.
* **nSmoothThickness=2** seems good. nSmoothThickness>2 start to decrease layer coverage slightly and about linearly. Mesh errors increase as well.
* **nSmoothNormals>0** does not seem to affect anything much.
* **nSmoothDisplacement>2** seems good on visual inspection. With more iterations the layer coverage increases linearly on average, but the effect is very minor.
* **minMedialAxisAngle=90** seems good. Layer coverage increases with increasing minMedialAxisAngle, but minMedialAxisAngle>90 seems to create twists on the background mesh on visual inspection.
* **0.2<=maxThicknessToMedialRatio<=0.7** seems good, but maxThicknessToMedialRatio>0.7 seems to cause mesh squishing in visual inspection.
* **slipFeatureAngle** has no effect in this case.
* **3<=nRelaxIter<=12** seems good. Lower values create numerous mesh errors. Higher values tend to increase layer coverage slightly. Increasing nRelaxIter increases meshing time.
* **nBufferCellsNoExtrude>0** decreases layer coverage.
* **4<=nLayerIter<=12** seems good. nLayerIter>12 does not seem to change anything. nLayerIter=1 creates the best layer coverage and the worst amount of mesh errors.
* **nRelaxedIter>0** decreases layer coverage radically.
* **nOuterIter=4** (=target number of layers) generates best layer coverage with a smooth nSurfaceLayers transitions, but is computationally heavy.


## Feedback

[Link to discussion thread on CFD-Online](https://www.cfd-online.com/Forums/openfoam-meshing/254447-snappyhexmesh-parametric-sweep-study.html)
