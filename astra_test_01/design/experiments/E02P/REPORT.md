# E02P — Phaser 4 foundation result

Phaser 4.2.1 joins Godot 4.6.3 and Pixi 8.20.1 for the selected projection C. It passed the bounded placement/attachment/UI foundation. Carry all three into the painted-chamber composition test; no renderer winner is established.

Open [the labelled browser comparison](review.html). It works directly from disk and includes nine positions, two camera policies, native 720×405 images and 3× enlargements of the same rendered pixels. Matt reports Canvas links open as code, so standalone browser HTML is the primary review delivery. [Live Phaser](index.html) needs the local server below.

## Evidence and scope

[Batch 02 validation](evidence/batch-02/validation.json): 140/140 checks passed, including dependency hashes, 18 independent projection comparisons, 18 engine attachment checks, 18 root/socket planted-fault cases, 18 scale/bad-scale cases, 18 native captures, completeness/error checks and five actual UI behaviors. Maximum Phaser-vs-independent-Python root/top discrepancy: **0.0000128861px**, below the frozen 0.5px threshold. Actual root/socket transforms come from Phaser Containers. The scale instrument rejects the 25% oversized control; root and socket instruments reject actual 8px hierarchy mutations. Translation changes coordinates and pause stops them; it is a frozen-pose diagnostic, never a walking claim.

[Runtime metadata](evidence/batch-02/runtime.json): Phaser **4.2.1**, Chrome **152.0.7977.83**, **WebGL 1.0**, ANGLE Metal / Apple M2. E02 Pixi used WebGL 2.0; this result qualifies the observed configurations, not backend parity. No frame-time/performance ranking was attempted. Same source PNG/projection/layout are referenced and hashed in [INPUTS.json](INPUTS.json), not regenerated. E02's Godot/Pixi captures are preserved, not rerun against an exhausted budget.

[Saved review verification](evidence/batch-03-review/review-check.json): all 18 position/camera combinations load all six images directly from disk; no page errors; detail toggle works. Browser screenshots: [center](evidence/batch-03-review/center.png), [right](evidence/batch-03-review/right.png). Agent visually inspected the comparison at center/right and Phaser far/near native output. Placement and source scale agree visually; Godot grid strokes are smoother/thicker in these captures, while Phaser/Pixi thin lines and tiny labels show different rasterization. The same small historical character does not reveal an evidence-backed artistic winner.

**Still unproved:** C-conditioned painted floor/character agreement, persistent-layer motion, modular gear, masks/depth/occlusion, VFX transfer, collision/state interactions, combat JSON ingestion and full G2. Legacy art's depicted camera is uncalibrated. E02's cuboid approximation finding remains valid within its geometric scope; it is not an anatomical failure of this painting. No original ASTRA failures or E01 gaps are closed by this experiment.

## Preserved failure and correction

Batch 01: 122/140 checks passed; all 18 capture-size checks failed. Playwright's element screenshot rounded a fractional CSS position to **720×406**. Runtime math and controls passed. [Failed validation](evidence/batch-01/validation.json), raw captures and exact capture/probe scripts remain in that directory. Batch 02 captures the rendered canvas buffer using `toDataURL`, giving exactly **720×405** without crop/resize/art edits. UI labels also now synchronize after programmatic test resets. No acceptance threshold changed. Batch 03 was saved-review verification; all three registered capture batches are consumed.

This experiment took no generation or paid-service calls. Runtime code builds a new scene on each diagnostic redraw; this is a composition probe, not a production allocation/performance design. The historical E02 ARTIFACTS manifest describes its commit snapshot, including then-current live handoff docs; changes to those handoff docs do not invalidate unchanged E02 evidence. E02P separately rechecks only the immutable dependencies it uses.

## Reproduce and continue

From this repository root:

```sh
python3 astra_test_01/design/experiments/E02/fetch_tools.py
python3 -m http.server 8769 --bind 127.0.0.1 --directory astra_test_01/design/experiments
```

Then open `http://127.0.0.1:8769/E02P/` for the live probe. The saved comparison is `astra_test_01/design/experiments/E02P/review.html` and works without a server. Stop the server after review. Phaser and MIT license are vendored; browser automation uses the pinned E02 Playwright bootstrap. Validate saved evidence without rendering with `python3 astra_test_01/design/experiments/E02P/validate.py batch-02`.

The three-batch limit is exhausted: do not invoke capture scripts again without a separately registered extension. Next action is **E03**: register C-conditioned painted floor/prop and actor-view controls with frozen alpha/art-data/generation limits, then compose identical accepted assets in all three adapters. Use [the shared benchmark](../E02/RENDERER_BENCHMARK.md) and [architecture](../../ARCHITECTURE_PLAN.md). Build chamber state, collision, occlusion and interactions from layout data; paintings must visibly agree. Seek Matt's style/projection judgment only with concrete painted comparisons. No unanswered choice is approval.

## Primary sources

Phaser version was verified against its [official Phaser 4 release listing](https://phaser.io/download/phaser4) and the downloaded runtime's `Phaser.VERSION`. The [official Container documentation](https://docs.phaser.io/phaser/concepts/gameobjects/container) guided hierarchy/world-transform instrumentation; actual downloaded v4 behavior was exercised locally. [Pinned distribution](https://cdn.jsdelivr.net/npm/phaser@4.2.1/dist/phaser.min.js), version/hash/license and automation dependency are recorded in [DEPENDENCIES.json](DEPENDENCIES.json). Other alternatives remain researched only in [E02's renderer research](../E02/RENDERER_RESEARCH.md).
