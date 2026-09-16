T4h-r1 — burst_v2 stretch-and-erode

The eighth kit is registered beside v1. The masks and delivered schema are preserved; small islands appear only in the intact hold. Core membership is measured against the largest inscribed circle and takes precedence over the tongue band heuristic. Each radial transform is Axis Node2D -> Stretch Sprite2D -> original-mask Sprite2D with counter-rotation and root offset. Roots never translate.

Whole-body erosion textures use the original peak alpha centroid, sampled in the pieces’ original full-canvas UVs. The stationary original masks beneath the extending body retain core/root coverage; a v2-only upper-distance clip bounds that residue while the T4a erode and band-step dissolve remove coverage. The shared shader, v1 script, and seven existing exports remain unchanged. A final pre/post comparison found all 488 existing export files byte-identical.

Rendered acceptance is UNEVALUABLE. Both 768-square, scale-1.0 Movie Maker launches aborted (-6/SIGABRT), with no PNGs. Godot headless import exited 0, the two independently run v2 traces are byte-identical, and the clock records hold 2, stretch 15 ticks, residue 36 ticks, release at age 76. Headless traces are not bake determinism evidence.

CPU geometry reports a connected silhouette (minimum largest-component fraction 0.999778) and a stationary 21.0102% residue, but only 1.4244x extent, below 1.8x. Even a generous bound allowing 2x stretch, all permitted rotations and full root drift reaches only 1.6542x for these masks. This is a reported limitation, not a relaxed gate or a shipping verdict. The 311-pixel CPU source extent uses alpha>0, including faint source islands; the conductor’s 306-pixel rendered body is a different support measurement.

Full suite: 595 tests, 580 successful tests, successful=false. All fifteen red results are named in acceptance.json and full_suite.json: five standing oracle reds and ten Godot sandbox/environment reds. Focused v1/v2 tests: 17 successful; final v2 checks: 3 successful. Test path routing is archived as sitecustomize.py; no assertions or errors were suppressed.

Evidence archive

Extract evidence.tar.gz into this directory to recover the fixture project, original baseline export, actual traces, command/process reports, logs, and reproduction drivers. Import project/ headlessly with Godot using an explicit writable --log-file, then repeat the recorded run.json commands with fresh output paths. The archived run_bakes.py records the original orchestration and requires fresh output directories. That driver deliberately leaves original v1 kit data untouched and uses only the fixture copy’s phase_scale=1.0. The Movie Maker commands, including --write-movie and --fixed-fps 60, are recorded in bake_v1/run.json and bake_v2/run.json.

The 512 default remains unchanged; crop validation additionally accepts exactly 768x768. out/files.json inventories surviving deliverables; the receipt records the manifest’s own hash to avoid a self-referential checksum.
