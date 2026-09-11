# E02 — C perspective in Godot and Pixi.js

**Outcome: both renderer foundation probes run; continue with C.** No production
renderer is selected. H01's final painted compatibility remains INDETERMINATE;
G2 is partial, not PASS. [Visual comparison](review.html),
[renderer alternatives](RENDERER_RESEARCH.md), [shared benchmark](RENDERER_BENCHMARK.md),
[receipt](RECEIPT.json), [validation](evidence/validation.json).

## User decisions carried forward

Matt chose **C** to test whether perspective creates a real visual problem. That
supersedes the agent's B-first recommendation for test priority; it does not imply
a final art target approval. Matt then required Godot and Pixi.js versions plus
research into other composition tools. The goal is agent scene/character/VFX
assembly capability around shared combat JSON. Combat engine breadth is not a
ranking criterion. The existing sibling demo JSON loader was inspected read-only;
no pipeline schema was replaced or newly integrated by this probe.

Matt also clarified that Grim Dawn offers camera zoom/angle controls. Treat the
varied source framing as settings-dependent; E01 screenshots still have unknown
capture settings. This is recorded user context, not a recovered camera measurement.
E01's native-motion gaps remain open, and its source packet remains unchanged.

## Executed probe

Both adapters load byte-identical snapshots of E01's projection/layout and one
existing painted mage frame. Geometry and shader sampling are rendered locally,
not simulated by a static illustration. Nine camera-ground positions cover center,
near/far, left/right and diagonals, under fixed and exactly following cameras.
An affine B view is retained as a control beside selected C inside each engine's
raw capture. The review page compares **C against C** across engines.

Godot 4.6.3 used Sprite2D/ImageTexture, a child Marker2D attachment and SubViewport
capture on Apple M2. Pixi.js 8.20.1 used Container/Sprite hierarchy, masking,
RenderTexture and WebGL2 through ANGLE Metal on Apple M2. A fresh isolated Chrome
process exercised its actual camera, position and bad-scale UI. No existing user
browser profile was accessed. [Godot record](evidence/runtime-fixed-v2.json),
[Pixi record](evidence/runtime-pixi-v2.json).

The source is a frozen historical S idle pose; translation is **not walking**.
The floor and footprints are diagnostic geometry. No art-generation call was made.
The historical depicted camera is not qualified for C, so center-view art agreement
is a confound. This controls positional reuse of one source; it cannot establish
that a correctly C-authored actor or complete painted chamber will pass or fail.

## Measurements and interpretation

**95/95 component checks PASS.** Independent projection references agree with
both runtime adapters to at most **0.0000198891 px**. Root/socket tests pass the
0.5 px limit. Runtime-shifted root/socket controls are rejected; the wrong-scale
and frozen-ground-circle controls are detected. PNG source hashes and capture
dimensions/nonempty images pass. This is a scoped component result, not 95 art tests.

In the fixed camera, the selected 2m vertical-axis projection varies from **35.85
to 39.98 px** across the declared samples. A known 0.6×0.4×2m cuboid, treated as a
center image translated and uniformly scaled, differs from its true C projection
by up to **6.93 px** at lateral positions. Six off-center samples exceed the
preregistered 2px geometric review flag. This quantity measures a known cuboid
approximation, not hidden mage anatomy, source-pixel drift or a perceptual failure.
[All sample measurements](evidence/analysis.json).

The guide poles reveal the cause: projected world verticals lean toward a vanishing
point off center, while this simple screen-upright sprite stays upright. In inspected
right-side captures, that distinction is clearer beside the poles and at 3× than
in the small painted body alone. Near/far body/view differences are less decisive
in these frames. This is provisional agent visual judgment, not an independent
human acceptance result. The actual sampled mid-body viewing direction spans
roughly 46–58° elevation; the legacy painting has no calibrated matching volume.

The exact following camera removes the centered actor's position-dependent viewing
change by keeping its camera-relative position constant. That result is scoped to
the followed actor and policy. Other creatures/props, camera lag, edge clamps,
zoom/angle changes and elevated terrain still need explicit tests.

**Decision: the current evidence does not justify abandoning C.** It identifies
an approximation worth testing with C-conditioned art and painted vertical props.
Do not automatically reject C using the cuboid metric, or call the small existing
sprite a proof that perspective never matters.

## Visual inspection and preparation failures

Inspected source: `inputs/legacy-idle-S.png`. Inspected initial Godot fixed right,
near/far and following-right captures; Pixi initial right; final Godot right and
bad-scale; final Pixi right and center. Inspection covered root appearance, side
guides, relative size, alpha on the diagnostic floor and review-view fairness.
Other retained sample images have automated validation but are not individually
claimed as visually inspected. No uncut native-source gameplay or qualified gait
was inspected in E02.

Two review defects are retained: the first Godot lower enlargement was clipped by
a 940px window (native upper scenes were complete); initial Pixi lower views redrew
source art at 3× while Godot enlarged a 720px viewport. The latter could create a
false sharpness preference. **Use v2 captures for comparison.** Both now enlarge
native render textures. Line rasterization/font/filter differences remain visible;
no pixel-identical rendering claim is made. The Godot bad-control title overlaps
the position caption, but its 25% size change is visible; no metric depends on text.

The first npm install timed out. Direct Python HTTPS downloads then failed local
certificate-chain validation. Verified-system curl obtained the pinned public
artifacts without disabling TLS checks. The final runtime uses a locally retained
Pixi distribution and license; the test-only Playwright package is reproducibly
fetchable and excluded from git. Browser connector discovery was empty; local
standalone Chrome succeeded under the documented fallback. No paid account was used.

## Renderer research result

Keep **Godot and Pixi.js** as the required comparators; **Phaser 4** is the most
informative third test. Defold/Cocos remain reserves and Three.js a conditional
painted-plane/depth experiment. These research recommendations are evidence-linked
in [RENDERER_RESEARCH.md](RENDERER_RESEARCH.md). Alternate-engine composition ability
is untested. No aggregate quality, productivity or performance winner is inferred.
Godot-first implementation and Pixi contract reuse make effort comparisons order-biased.

## Run and continue

Open [review.html](review.html) directly for all retained comparisons; no server
is needed. The Canvas companion embeds a selection of unchanged captures and
supports camera/position selection; its host compilation is not independently verified.

Run Godot interactively:

```sh
/Applications/Godot.app/Contents/MacOS/Godot --path /Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E02/runtime
```

Run the local Pixi probe (then open `http://127.0.0.1:8768/pixi/`):

```sh
python3 -m http.server 8768 --bind 127.0.0.1 --directory /Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E02
```

Revalidate saved evidence without rerendering:

```sh
python3 astra_test_01/design/experiments/E02/validate.py
```

**Exact next action:** register E03's shared C-conditioned painted floor/prop and
actor-view control, freeze generation/alpha/art-data tolerances, then feed the same
accepted assets into Godot and Pixi. Add the Phaser foundation adapter under its
own recorded limits. [Benchmark sequence](RENDERER_BENCHMARK.md).
G1 motion recovery stays a separate changed-acquisition-method task; no exhausted
searches or old ASTRA repairs should resume automatically.
