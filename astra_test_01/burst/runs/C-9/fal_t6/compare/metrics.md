# C-9 T6 -- 3D generator bake-off, measurements

Matt R-C9-66. Six pipelines per subject: the Meshy baseline plus five fal endpoints, all
built from the SAME approved four-view painted plates. Renders at orthographic
52.95354112560294 deg elevation per Matt R-C9-68; the IoU pass is at 0 deg because the
painted plates are flat and an IoU against them has to be measured in their own projection.

Counts are AFTER an exact-position weld (glTF splits vertices at UV seams; the delivered
numbers are in `metrics.json` as `*_as_delivered`). `frag` = islands under 1% of surface
area, with their combined area share. IoU = silhouette agreement with the painted plate,
height-normalised.

## KNIGHT

| generator | tris | verts | textures | GLB MB | islands | frag <1% | largest detached piece | non-manifold edges | watertight | gen s | $/gen | IoU front | IoU right | IoU back | IoU left | IoU mean | IoU mean ex-back |
|---|---:|---:|---|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Meshy (baseline) | 115,567 | 58,198 | 2048x2048 | 7.5 | 20 | 19 (0.04%) | 0.01% internal | 333 | no | 211 | $0.60* | 0.770 | 0.707 | 0.786 | 0.716 | **0.745** | 0.731 |
| Hunyuan3D 3.1 Pro | 500,000 | 249,992 | 4096x4096 | 35.0 | 1 | 0 (0.00%) | - | 0 | yes | 160 | $0.525 | 0.858 | 0.726 | 0.849 | 0.746 | **0.794** | 0.776 |
| Rodin v2.5 | 500,000 | 249,996 | 2048x2048 | 23.3 | 1 | 0 (0.00%) | - | 0 | yes | 187 | $0.4 | 0.845 | 0.856 | 0.896 | 0.856 | **0.863** | 0.852 |
| Tripo H3.1 multiview | 1,447,702 | 723,853 | 4096x4096 | 44.8 | 1 | 0 (0.00%) | - | 0 | yes | 158 | $0.4 | 0.859 | 0.881 | 0.902 | 0.880 | **0.881** | 0.874 |
| TRELLIS 2 | 491,940 | 243,948 | 2048x2048 x2 | 18.1 | 3 | 2 (0.03%) | 0.03% internal | 1,685 | no | 41 | $0.3 | 0.834 | 0.736 | 0.896 | 0.736 | **0.800** | 0.768 |
| Hi3D v3.0 | 2,000,000 | 999,924 | 8192x8192 x2 | 49.9 | 1 | 0 (0.00%) | - | 0 | yes | 549 | $2.1 | 0.841 | 0.802 | 0.889 | 0.796 | **0.832** | 0.813 |

## MANTICORE

| generator | tris | verts | textures | GLB MB | islands | frag <1% | largest detached piece | non-manifold edges | watertight | gen s | $/gen | IoU front | IoU right | IoU back | IoU left | IoU mean | IoU mean ex-back |
|---|---:|---:|---|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Meshy (baseline) | 71,577 | 35,809 | 2048x2048 | 5.2 | 4 | 3 (0.00%) | 0.00% internal | 12 | no | 278 | $0.60* | 0.442 | 0.417 | 0.288 | 0.678 | **0.456** | 0.512 |
| Hunyuan3D 3.1 Pro | 498,420 | 249,212 | 4096x4096 | 37.4 | 3 | 1 (0.92%) | 1.82% **off-body** | 0 | yes | 159 | $0.525 | 0.355 | 0.388 | 0.225 | 0.637 | **0.401** | 0.460 |
| Rodin v2.5 | 500,000 | 250,002 | 2048x2048 | 22.4 | 1 | 0 (0.00%) | - | 0 | yes | 137 | $0.4 | 0.434 | 0.339 | 0.276 | 0.596 | **0.411** | 0.456 |
| Tripo H3.1 multiview | 1,455,660 | 727,834 | 4096x4096 | 45.7 | 2 | 0 (0.00%) | 1.87% **off-body** | 0 | yes | 161 | $0.4 | 0.402 | 0.345 | 0.255 | 0.832 | **0.459** | 0.527 |
| TRELLIS 2 | 498,469 | 237,861 | 2048x2048 x2 | 22.6 | 140 | 139 (1.06%) | 0.26% internal | 6,344 | no | 134 | $0.3 | 0.454 | 0.443 | 0.306 | 0.530 | **0.433** | 0.476 |
| Hi3D v3.0 | 2,000,000 | 1,000,002 | 8192x8192 x2 | 50.0 | 1 | 0 (0.00%) | - | 0 | yes | 451 | $2.1 | 0.502 | 0.691 | 0.256 | 0.363 | **0.453** | 0.519 |

\* Meshy: 30 credits. Meshy publishes no dollars-per-credit rate; $0.60 is DERIVED as
Pro plan $20 / 1,000 credits per month, and holds only at full monthly utilisation
($0.40 on Premium, $0.375 on Ultra). fal prices are marginal per-request prices; this is not.

## Knight rig probe (no Meshy rigging call, no credits spent)

| generator | tris | decimate to reach 300k | one humanoid island | floating frags | arm/torso gap rows | arms clear |
|---|---:|---:|---|---:|---:|---|
| Meshy (baseline) | 115,567 | x1.000 | yes (0.9996) | 19 | 121 | yes |
| Hunyuan3D 3.1 Pro | 500,000 | x0.600 | yes (1.0000) | 0 | 107 | yes |
| Rodin v2.5 | 500,000 | x0.600 | yes (1.0000) | 0 | 108 | yes |
| Tripo H3.1 multiview | 1,447,702 | x0.207 | yes (1.0000) | 0 | 107 | yes |
| TRELLIS 2 | 491,940 | x0.610 | yes (0.9997) | 2 | 118 | yes |
| Hi3D v3.0 | 2,000,000 | x0.150 | yes (1.0000) | 0 | 119 | yes |

## Orientation applied (measured, not assumed)

| model | yaw applied | yaw margin (IoU) | mirror argmax | mirror margin | mirrored? |
|---|---:|---:|---|---:|---|
| knight/Meshy (baseline) | 180° | 0.038 | False | 0.0239 | no |
| knight/Hunyuan3D 3.1 Pro | 180° | 0.031 | False | 0.0045 | no |
| knight/Rodin v2.5 | 180° | 0.123 | False | 0.0113 | no |
| knight/Tripo H3.1 multiview | 90° | 0.144 | False | 0.3767 | no |
| knight/TRELLIS 2 | 180° | 0.038 | False | 0.0144 | no |
| knight/Hi3D v3.0 | 180° | 0.099 | False | 0.0217 | no |
| manticore/Meshy (baseline) | 180° | 0.168 | True | 0.0048 | no |
| manticore/Hunyuan3D 3.1 Pro | 180° | 0.147 | True | 0.0021 | no |
| manticore/Rodin v2.5 | 180° | 0.142 | True | 0.0061 | no |
| manticore/Tripo H3.1 multiview | 90° | 0.191 | False | 0.3895 | no |
| manticore/TRELLIS 2 | 180° | 0.113 | True | 0.0021 | no |
| manticore/Hi3D v3.0 | 180° | 0.145 | False | 0.0368 | no |

No model was mirrored. A flip is applied only on a margin >= 0.05 and nothing cleared it:
both Tripo models reject a flip decisively (~0.38), every 180 deg model is within ~0.006
either way, which is noise on a bilaterally symmetric subject.

## Caveats

- MANTICORE back-view IoU (0.225-0.306 for all six) measures the PLATE, not the model: the painted back plate draws the tail as a vertical spike above the skull, so its height box is roughly twice the creature’s. No generator reproduces that. Read the manticore on front/right/left (mean_ex_back).
- Silhouette scale and alignment come from the largest blob; the full mask including detached fragments is what is scored. Without the largest-blob guard a 200-pixel flake set the scale for a million-triangle mesh and the orientation fit chose the wrong yaw on an IoU of 0.22.
- Triangle and vertex counts are AFTER an exact-position weld. glTF splits vertices at UV seams, so the delivered index buffer reports every seam as a hole; delivered counts are kept alongside as *_as_delivered.
- Rodin v2.5 with material="Shaded" delivers a BLACK base colour and routes its map into Emission at strength 1: its "texture" is a LIGHTING BAKE, not an albedo. The unlit pass reads that socket so Rodin is visible at all, but Rodin’s row is not an apples-to-apples base-colour comparison -- it already contains shading that will fight any light you later put on it.
- Meshy’s price is derived from plan price / included credits because Meshy publishes no per-credit dollar rate. It is a subscription amortisation, not a marginal per-request price like fal’s.
