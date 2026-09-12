All verdict thresholds are explicit parameters. No parameter was fitted to the F04 acceptance result. `fixtures/manifest.json` freezes the initial O3 bank and threshold before measurement; these remain provisional. NCC tests use transformed copies, a constant template negative, and independent mage negatives. This matcher detects visual similarity, not semantic equivalence of sigils.

O1 uses caller-supplied dE76 tolerance and off-palette budget; tests use solid swatches and a shifted mage. O2 uses supplied sign and luminance delta; tests reverse contrast. O4 uses supplied Sobel edge threshold and plain fraction budget; tests compare constant and striped planes. O5 reuses the gate implementation unchanged, with caller-supplied distance threshold; tests use idle neighbors and mirroring. O6 bins and maximum unclassified fraction require reviewed label-sheet calibration; tests use disjoint Lab bins, antialiased borders, overlapping bins and unknown colors. Erosion is explicitly 1–2 display pixels. O7 compares the gradient direction to a caller-supplied azimuth/tolerance; tests use linear planes and reversed light. It is a shading proxy, not a causal light-source estimator. O8 compares spectral profiles only when a compatible anchor is supplied; tests use known sinusoid periods and source-normalized downsampling.

`display_scale` means uniform analytical downsampling in (0,1]. This does not register or modify delivered frames. O3's template bank interpolation is analysis, not generated-art upscaling. Masks use nearest sampling. Gate silhouette measurement retains its existing analytical 64px normalization.

Bible v0.1 uses `RULE` as an array and the literal fields listed in SPEC. Null palette bins, empty swatches, unknown geometry and uncalibrated thresholds are placeholders, not approvals. LIGHT screen convention is x-right/y-up: upper-left = 135°. The stub's rigidity and mirror labels are provisional placeholders; Matt owns declarations. Placement counts are maximum allowed motif counts, consistent with accepting a clean, undecorated frame. The transcription's presence/count fields refer to the sigil on each closed part. Plain excluded parts provide absent-sigil controls; they do not assert absence of the anatomical part. A distinct absent-anatomical-part control is not supplied by this stub.

`compare_to_bible` evaluates its named O3/O9 coverage only. A zero violated-rule count does not certify unimplemented or JUDGE-only criteria. It requires reviewed allowed regions and does not infer anatomical locations from a RGB crop.

## T0-d2: O3b primitive-family calibration (2026-09-11)

The legacy paragraphs above describe the T0-c baseline. Bible v0.2 now adds a
separate anatomical PART inventory and helmet/cape/shield/second_belt controls;
`from_bible` remains the unchanged motif-on-part question generator. No new
anatomical vocabulary was introduced. `compare_answers(question_set='parts')`
requires the entire PART-plus-control inventory. Auto mode identifies the PART
set by its control keys; explicit mode is available for malformed inventories.
X0-T thresholds are named constants in `compare/calibrate_transcriber.py`:
presence precision/recall >=0.9, count error <=1 on >=0.8 of closed parts, and
control catch rate 1.0. Controls must be answered absent AND zero. Aggregate
presence scores are micro-averaged over bursts/parts; count and control rates
use all corresponding observations. N=0 never produces a boolean verdict.

O3b is a gradient-vote circular Hough instrument beside unchanged NCC copy
matching. It searches native radii 8..30 pixels; the floor excludes features
smaller than an 8px radius. Native coordinates and the exact center-based
allowed-mask partition are retained. Each Sobel gradient above 0.02 votes in
both directions; Gaussian sigma=max(1,0.08r). The vote score normalises the
accumulator by circumference and Gaussian peak, not by an image-dependent
maximum. It is not a probability. One concentric family center is retained by
NMS with center distance <0.8 times the larger radius.

`tests/motif_calibration.py` builds the fixed calibration set: flat and seeded
textured backgrounds with rings at (40,48,r8), (108,48,r14), (185,70,r22), plus a
rectangular no-ring sprite. The initial 0.25 exploratory cutoff exposed unwanted
synthetic peaks up to 0.3999017884; true ring scores were >=2.1807297163.
**vote_thresh=0.50 was selected from those synthetic observations BEFORE any
F04/clean family measurement**, and has not changed. Initial held-out counts
were F04 inside=2/outside=64 and clean outside=5. This diagnosed arc/corner
responses and triggered the single retry: a signed radial-gradient support
check, >=75% of 48 angular samples, alignment cosine >=0.9, in a radius band
+/-max(2px,0.15r). A synthetic half-arc negative was added to the same set.
No real-crop counts were used to alter the vote threshold.

Final synthetic counts: flat 3, textured 3 (each known center within 2px and
radius within 2px, no extra peaks), no-ring sprite 0, half-arcs 0. Final real
counts: **F04 inside=1, outside=14; clean inside=0, outside=1**, at clean center
(286,407), radius 8, score 0.7741343318. The clean-zero acceptance is UNMET.
The comparator in `both` mode therefore rejects the clean crop as well as F04;
these remain active assertions. No second detector retry or threshold rescue
was attempted. This is a geometric radial-feature screen, not semantic sigil
recognition; precision on ornamental/non-ornamental circular forms is not
established. All peaks and parameters are in `tests/o3b_calibration.json`.

Acceptance copied verbatim from SPEC §4 (unchanged):
- O3 on the F04 crop with `allowed=[rod_head bbox]` → `outside ≥ 3`; on `clean_crop` → `outside == 0`. `compare_to_bible` with the stub FAILS the F04 crop and PASSES the clean crop.

## T0-d2: F-5 and model-coupled matte health

F-5 `tol=8` is the registered per-channel key-color tolerance. `min_fraction`
has **no default threshold**; X1 is an observational calibration set, not a
source for inventing a shipping bar. With supplied matted alpha, non-subject
means alpha<128, the existing opaque-core convention; all such pixels are
sampled, including the exterior antialias band, rather than border-only samples.
This support definition explains why results need not equal the ledger's
100%/38% or sd<1.1; the ledger numbers were NOT used for tuning.

- X1 satchel: fraction 0.9951550008737277 (99.5155000874%); plate mean RGB
  [3.5858515174,249.5110987344,3.8822837564], sd
  [0.9222366909,2.2387386663,0.9332130756], n=1253251.
- X1 staff head: fraction 0.2233263715097009 (22.3326371510%); mean RGB
  [6.4743078939,249.0838767818,9.2130608953], sd
  [1.1746059839,1.7064204064,1.3473317913], n=1478061.

`alpha_floor=40` is a caller option in 0..255 alpha units, not a new default.
It zeros residual alpha below 40 outside the main alpha>=128 component. On
these X1 source props with preserve_particles=True: border clipping 34→0 and
39→0. Without a floor every synthetic particle remains; with the floor an
isolated alpha30 speck is removed and alpha200 and alpha100 particles remain.
The legacy default matte/gate definitions are otherwise unchanged. Detailed
measurements are in `tests/f5_calibration.json`.

`gates/matte_quality.py` is explicitly MODEL-COUPLED, revalidated on every drift
alarm. Against the supplied (pre-floor) X1 RGBA counterparts, both props have
spill fraction=0, edge halo=0, particle-loss proxy=0. Source partial-alpha mass:
11920991 (satchel), 22387111 (staff). This proxy includes plate residuals and
antialias edges: it cannot identify true VFX particles without annotations.
Thresholds remain undeclared; exact envelopes are in
`tests/matte_quality_calibration.json`.

## T0-d2: R9 descriptive calibrations and deferred thresholds

- Sheet consistency: run_03 idle S mean/max centroid distances
  0.1657680432/0.2089352467. Mirroring frame 0 raises them to
  0.1847703103/0.2944569574, with frame 0 farthest. Palette uses 8 bins per Lab
  dimension; histogram and aligned O5 mask blocks have unit L2 norm, alpha
  mass is a canvas-area fraction. These are analytical representations, not
  per-frame art registration. Threshold remains null.
- Model drift: harness and strict probe-set schema only. Conductor supplies
  production prompts at HITL. freeze hashes exact manifest bytes after checking
  referenced bytes. O5/O1/O8 identical synthetic pairs measure zero; mirror and
  palette shifts increase their corresponding distances. No alarm threshold
  before K1. Constant foreground has a defined zero spectral descriptor.
- PSE: named XAG-118 temporal thresholds are in `oracles/pse_check.py` with the
  citation. A flash counts opposing transitions, not individual edges; a
  sliding (t-1,t] window is used. Synthetic 4Hz white and saturated-red scenes
  exceed the 3/s bar; 1Hz and exactly 3Hz do not. The spatial-pattern instrument
  is explicitly report-only/null: robust >=5-pair spatial analysis is not
  implemented, as permitted by the task. Temporal results do not certify full
  XAG-118 compliance.
- PNG provenance: text/XMP field extraction and C2PA manifest presence do not
  constitute signature verification. Opaque C2PA/JUMBF fields remain null when
  not exposed as readable metadata; raw keys and text are retained at ingest.
