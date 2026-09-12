# Astra burst lane — T0 SOFTWARE SPEC v1.0 (build-to-spec; Astra builds, gandalf reviews + freezes)

> **STATUS:** BUILD CONTRACT for TOOLING bursts T0-a / T0-b / T0-c (Run C-1). Author: gandalf, 2026-09-11. Charter: `agentic_orchestration/gandalf/notes/2026-09-11-astra-burst-lane-run-charter.md` (§ 2 register card, § 4 burst rules, § 6 rubric — extracted verbatim by T0-a).
> **Constraints binding on every TOOLING burst:** Python 3 stdlib + Pillow 10.3 + numpy 2.4 + **scipy 1.17 + scikit-learn 1.8** (all present in system `python3`, first-hand probe, legolas R8 § 0.7). **`cv2`, `skimage`, `torch`, `onnxruntime` are ABSENT — do not import them; do not `pip install`.** `scipy.signal.fftconvolve` = normalised cross-correlation; `scipy.ndimage` = labelling, morphology, sobel; `sklearn.cluster.KMeans` = palette work. No network. No image generation. Write ONLY under `astra_test_01/burst/`. Read only the paths named here. Every module ships `tests/test_<module>.py` (unittest, stdlib) with **known-bad fixtures**; a test that cannot fail on a bad input is not a test. No PASS/FAIL vocabulary in receipts — results are numbers + booleans consumed by the conductor.

## 0. Layout (all paths relative to `astra_test_01/burst/`)

```
SPEC.md  REGISTER_CARD.md  BURST_RULES.md  JUDGE_RUBRIC.md      # T0-a extracts the three from the charter, verbatim
receipt.schema.json  transcribe.schema.json  bible/schema.json  bible/f04-keepers.stub.json
lane/{render_brief.py, run_burst.py, audit.py, ledger.py, schema_check.py}     # T0-a
gates/{common.py, matte.py, register.py, g1_height.py, g2_pivot.py, g3_light.py, g5_drift.py,
       g6_seam.py, g9_alpha.py, drift48.py, silhouette64.py, pack.py, run_gates.py}          # T0-b
parts/{part_masks.py, motif_match.py, part_metrics.py}   compare/compare_to_bible.py      # T0-c
review/build_review.py  tests/  fixtures/  runs/C-1/ledger.json  MANIFEST.sha256 (conductor)
```

## 1. Shared result schema (every gate / metric returns this; `run_gates.py` writes a list of them)

```json
{"id":"g6_seam","subject":"idle/S","passed":true,"value":0.661,"threshold":0.717,"op":"<=",
 "unit":"rgb_mad","evidence":["evidence/idle_S_seam.png"],"notes":"literal brief gate; see g6b"}
```
`passed` may be `null` (UNEVALUABLE) with a `notes` reason — never silently `true`.

## 2. T0-a — lane runtime

**`lane/render_brief.py`** — `render(task: dict, type: str) -> str`. Concatenates, in order: `REGISTER_CARD.md` · the type-specific section of `BURST_RULES.md` · `TASK` (task.text, output names, caps) · `REFERENCES` (one line per image: `Image N: <role> — <filename>`) · `RETURN` (the receipt schema, inlined). Deterministic: same task → byte-identical brief; the brief's sha256 goes in the ledger.

**`lane/run_burst.py`** — CLI: `--run C-1 --burst-id <id> --type <TOOLING|GENERATE|CHECK|JUDGE|TRANSCRIBE|LABEL|ANNOTATE|PACK> --task task.json [--dry-run]`.
`task.json`: `{"text": str, "references": [{"path": str, "role": str}], "image_cap": int, "minutes_cap": int, "tool_call_cap": int, "outputs": [str], "effort": "medium|high", "add_dirs": [str]}`.
Behaviour: (1) create workdir `~/astra-burst/runs/<run>/<burst-id>/` with `in/` (references copied, sha256 recorded) and `out/`; (2) snapshot the workdir tree + hashes; (3) invoke
`codex exec --ignore-user-config -p astra-burst -C <workdir> -s workspace-write --ephemeral --skip-git-repo-check -c model_reasoning_effort="<effort>" [-i in/<ref> …] [--add-dir <d> …] --output-schema <receipt.schema.json> -o out/receipt.json --json "<brief>" </dev/null > events.jsonl 2> stderr.txt`
with a hard wall timeout of `minutes_cap` (kill the process group on expiry; record `TIMEOUT`); (4) run `audit.py`; (5) validate `out/receipt.json` with `schema_check.py`; (6) verify every receipt-listed file exists in `out/` with matching sha256; (7) harvest `out/` → `runs/<run>/artifacts/<burst-id>/`; (8) `ledger.append(...)`; (9) exit code: 0 DELIVERED · 2 VOID (audit/receipt/hash violation) · 3 FAILED (codex error/timeout). `--dry-run` renders the brief and the exact command without invoking.

**`lane/audit.py`** — `audit(events_path, workdir, snapshot, caps, type) -> {"violations": [...], "image_calls": int, "tool_calls": int, "tools_seen": {...}, "writes_outside_out": [...]}`. Parses the `--json` event stream (`item.completed` items: classify by item type and, for command executions, by command text). Detect image calls (item type containing `image` OR command text containing `image_gen`); forbidden tools (`web`, `collaboration`, `spawn`); writes outside `out/` by **filesystem diff against the pre-burst snapshot** (new/modified files anywhere in the workdir except `out/`, plus any path under the repo except the declared `add_dirs`); caps (image_cap, tool_call_cap). X1 calibrates the image-call detector (exactly 2 generated → count == 2).

**`lane/ledger.py`** — `append(run, entry)` to `runs/<run>/ledger.json`: `{"bursts":[{"id","type","experiment","brief_sha256","started","ended","minutes","image_calls","tool_calls","audit","receipt_sha256","artifacts":[{"name","sha256"}],"exit"}],"images_used":n,"images_cap":250,"experiments":{},"milestones":[],"halts":[],"rulings":[]}`. Atomic write (tmp + rename). Never edited by a burst.

**`receipt.schema.json`** (what `--output-schema` enforces). **STRICT FORM is mandatory** — the Responses API rejects any schema whose objects lack `additionalProperties:false` or whose `required` omits a property (T0-a attempt 1 failed on exactly this, `invalid_json_schema`). Same rule for `transcribe.schema.json` and any `--output-schema` you ever pass:
```json
{
 "type": "object",
 "properties": {
  "task_id": {
   "type": "string"
  },
  "status": {
   "type": "string",
   "enum": [
    "DELIVERED",
    "DELIVERED_WITH_CONCERNS",
    "FAILED"
   ]
  },
  "images": {
   "type": "array",
   "items": {
    "type": "object",
    "properties": {
     "name": {
      "type": "string"
     },
     "path": {
      "type": "string"
     },
     "sha256": {
      "type": "string"
     },
     "prompt": {
      "type": "string"
     },
     "references": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "role": {
         "type": "string"
        },
        "path": {
         "type": "string"
        }
       },
       "required": [
        "role",
        "path"
       ],
       "additionalProperties": false
      }
     },
     "elapsed_s": {
      "type": "number"
     }
    },
    "required": [
     "name",
     "path",
     "sha256",
     "prompt",
     "references",
     "elapsed_s"
    ],
    "additionalProperties": false
   }
  },
  "calls_used": {
   "type": "integer"
  },
  "retries": {
   "type": "array",
   "items": {
    "type": "object",
    "properties": {
     "reason": {
      "type": "string"
     },
     "change": {
      "type": "string"
     }
    },
    "required": [
     "reason",
     "change"
    ],
    "additionalProperties": false
   }
  },
  "self_report": {
   "type": "object",
   "properties": {
    "obeyed_invariants": {
     "type": "boolean"
    },
    "concerns": {
     "type": "array",
     "items": {
      "type": "string"
     }
    }
   },
   "required": [
    "obeyed_invariants",
    "concerns"
   ],
   "additionalProperties": false
  },
  "files": {
   "type": "array",
   "items": {
    "type": "object",
    "properties": {
     "path": {
      "type": "string"
     },
     "sha256": {
      "type": "string"
     }
    },
    "required": [
     "path",
     "sha256"
    ],
    "additionalProperties": false
   }
  }
 },
 "required": [
  "task_id",
  "status",
  "images",
  "calls_used",
  "retries",
  "self_report",
  "files"
 ],
 "additionalProperties": false
}
```
**Tests (T0-a):** render determinism; dry-run command exactness; audit detects a planted `web__run` line, a planted write outside `out/`, and an image-cap breach from synthetic event files; ledger atomicity; schema_check rejects a receipt with `status:"PASS"`.

## 3. T0-b — gate library (port; regression-locked to run_03)

Port from `astra_test_01/run_02/{guides.py,pipeline.py,registration_preflight.py}` and `astra_test_01/run_03/{turnaround.py,check.py,check_vfx.py,animation.py,package.py,preview_template.html}` — **preserve their measurement definitions exactly**; wrap, don't reinvent. Guides: projection constants become a parameter; the C constants come from `astra_test_01/design/experiments/E01/projection-candidates.json` (read it; if C is not numerically defined there, record `UNEVALUABLE` in the receipt concerns and keep the run_02 constants as the default — do not guess).
- `matte.py` green-plate extraction (particle-safe, run_02 semantics; also expose `remove_chroma_key`-style single-call). `register.py` uniform scale + translation from reviewed contacts; `measured_anchor`.
- `g1_height` ±3 % vs S · `g2_pivot` **two quantities**: root anchor (±4 px literal) and planted-sole contact trajectory (reported) · `g3_light` brightest-5 % centroid in upper-left half · `g5_drift` consecutive MAD < frame0-vs-cast05 · `g6_seam` literal (seam ≤ min internal) **and** `g6b` (seam ≤ median internal), both reported · `g9_alpha` edge mean + dark-fringe check · `drift48.py` 48-px downsample neighbour diff (same comparator as g5) · `silhouette64.py` 64-px BW alpha → Hu moments + aligned IoU vs master; `distance()`.
- `pack.py` sheets/atlas/contacts exactly as run_03 `package.py`; `review/build_review.py` from `preview_template.html`.
- `run_gates.py --frames-dir <run_03 or new> --master <S idle 00> --out checks.json` → list of § 1 results.
**Regression lock:** running the suite on `astra_test_01/run_03/character/frames` must reproduce `run_03/evidence/current_checks.json` numbers (seam/drift/height/pivot) to 1e-3; record the diff in the receipt. **Known-bad tests:** run_02's seven (checkerboard rejection, upscaling rejection, clipped-sole rejection, wrong-side light, measured registration, native-alpha dark interiors, wrong-side/clipping detection) + shifted-mask, repeated-lead, swollen-bag synthetic cases.

## 4. T0-c — oracles O1–O9, part masks, comparator, transcription contract (v1.1 — revised 2026-09-11 from legolas R6–R8: `agentic_orchestration/legolas/research/2026-09-11-ai-tells-bibles-oracles/findings.md` § 2.4, § 3.2–3.9)

**Every oracle returns the § 1 result schema; every threshold is a parameter with a documented calibration set (never a magic number). `passed: null` + reason when inputs are unclassifiable.**

| id | Module / function | Method (closed-form) | Bible inputs | Masks? |
|---|---|---|---|---|
| **O1** | `oracles/palette.py: adherence(rgba, swatches_hex, dE_tol)` → % off-palette + off-palette cluster centroids | CIELAB nearest-swatch; KMeans on off-palette pixels | `PALETTE.swatches[]` per scope | N |
| **O2** | `oracles/figure_ground.py: separation(rgba, background_rgb)` → mean/spread luminance inside alpha vs outside; sign + delta | luminance stats | `PALETTE.relation_rules[]` | N (alpha) |
| **O3** | `oracles/motif.py: count_instances(rgb, template_rgb, scales, rotations_deg, thresh, allowed_masks)` → {inside, outside, peaks[]} | NCC via `fftconvolve` over a scale pyramid × rotation bank; peak NMS; partition by allowed masks | motif crop; `placements[]`; `exclusions[]`; `scope` | Y to scope; N for raw count |
| **O4** | `oracles/plain_budget.py: plain_fraction(rgb, alpha, mask=None, edge_thresh)` | local edge-energy (`ndimage.sobel`) below threshold ÷ area | `plain-budget` target; `PARTS[].plain` | Y per part |
| **O5** | `oracles/silhouette64.py: descriptor(alpha)`, `distance(a,b)` → aligned IoU (primary), contour distance (secondary), Hu moments (screen only) | binarise at 64 px, centroid+scale align | frame set; **threshold + its calibration set** | Y (silhouette) |
| **O6** | `parts/part_masks.py: classify_by_bins(rgba, bins)` → {part: mask, unclassified_frac}; `part_metrics.py: area, centroid_rel(torso), palette_distance, mirror_symmetry(mask_a, mask_b)` | classify in CIELAB a*b* (luminance de-weighted); **erode 1–2 px** before measuring; report unclassified fraction as a health metric — above threshold ⇒ `passed: null` (VOID), not FAIL | `PARTS[] {palette_bin, attachment_to, adjacency, mirror_of, plain}` | **produces them** |
| **O7** | `oracles/keylight.py: azimuth(rgb, alpha, mask=None)` → circular mean + dispersion of luminance-weighted gradient azimuth | `ndimage.sobel` | `LIGHT.key_azimuth_deg`, tolerance | optional |
| **O8** | `oracles/grain.py: band_energy(rgb, alpha, source_px)` → radial spectral profile normalised to SOURCE pixels; distance to anchor profile | numpy FFT | `SCALE {canvas_px, feature_size_px}`; anchor asset | N |
| **O9** | `transcribe/` — `questions.py: from_bible(bible, scope)` → atomic, unique, dependency-ordered questions (DSG-shaped) over a **closed part list**; `transcribe.schema.json` (strict form; **presence/absence + per-part counts ONLY — never coordinates, never open vocabulary**); `compare/compare_to_bible.py` scores answers vs declarations | model-backed by an Astra TRANSCRIBE burst; the comparator is closed-form; **every question set includes ≥ 1 declared-absent control part**; counts are cross-checked against O3 where a template exists (VLM count = hypothesis, template count = measurement) | `PARTS[]` closed list; `placements[]`; `exclusions[]`; control list | N |
| ~~O10~~ | cross-frame identity (DINO-I) — **NOT T0** (`torch` absent); dependency decision recorded | | | |

**Bible schema v0.1 (`bible/schema.json`) — adopts legolas § 2.4; extensions marked ours:**
```
RULE { id, faction, scope: character|prop|environment|vfx|ui, class: motif|material|construction|silhouette|palette|plain-budget|light|scale,
       statement, placements[] {where, scale_px, count}, exclusions[] (stated POSITIVELY where possible — "all other surfaces plain"),
       parts_ref[], reference_asset, known_bad, oracle {id|"JUDGE-only", threshold, inputs, needs_part_masks},
       source: matt-ruling|bible-author|oracle-feedback, date, status }
PILLARS[2..3] { name, filter_statement }                                   (D4 precedent)
PALETTE       { scope, swatches[hex], relation_rules[] {figure_vs_ground, sign, min_delta} }
PARTS[]       { name, adjacency[], rigidity: rigid|soft|cloth|hair, attachment_to, palette_bin, allowed_motifs[], plain: bool, mirror_of }   (ours — ID-map precedent)
CONSTRUCTION[] { part, terminates_at | closes, statement }                  (ours — "every strap declares an endpoint; every fastener declares what it closes")
LIGHT         { key_azimuth_deg, key_elevation, fill_ratio, source_count }
SCALE         { canvas_px, feature_size_px: {class: px} }
```
`bible/f04-keepers.stub.json`: PARTS list for the Keeper (hair, face, shirt, tabard, belt, satchel, pauldron_L, pauldron_R, bracers, trousers, boots, rod, rod_head), ONE motif rule (`sigil` on `[tabard, rod_head]` only, `scope: character`, oracle O3), PALETTE with swatch placeholders, LIGHT key azimuth = upper-left (135° screen convention documented in the file), SCALE canvas 512. Everything else `JUDGE-only` placeholders. **Do not invent vocabulary; Matt rules it.**

**Fixtures + acceptance (unchanged in spirit; the gate must catch the defect Matt found by eye):** `fixtures/f04_advanced_crop.png`, `fixtures/sigil_template.png` (crop the handheld astrolabe head; record its bbox in `fixtures/manifest.json`), `fixtures/clean_crop.png` (a run_03 mage frame), run_03 S idle 00 / cast 05 / walk frames.
- O3 on the F04 crop with `allowed=[rod_head bbox]` → `outside ≥ 3`; on `clean_crop` → `outside == 0`. `compare_to_bible` with the stub FAILS the F04 crop and PASSES the clean crop.
- O5: `distance(S idle 00, mirrored S idle 00)` clearly > `distance(S idle 00, S idle 01)`.
- O6: on a synthetic 3-part sprite with disjoint bins + anti-aliased borders, per-part IoU vs ground truth ≥ 0.95 after 1-px erosion; unclassified border fraction reported.
- O1: a swatch-shifted copy of a frame reports off-palette % > the original by a margin.
- O9: `questions.from_bible(stub)` yields ≥ 1 declared-absent control; the comparator flags a synthetic answer set that claims the absent part present.

**Explicitly NOT built (legolas contraindication):** any "is it AI at all" detector.

## 5. Freeze protocol (conductor, after each T0 burst)

gandalf reviews the receipt + code + test output (DRIFT-CRITIC), runs the tests, then writes `MANIFEST.sha256` over `lane/ gates/ parts/ compare/ review/ *.json *.md`. Any later change = a new TOOLING burst + re-freeze + ledger entry. GENERATE/CHECK/JUDGE bursts read tools by absolute path; the sandbox (workspace-write on a workdir outside the repo) makes the repo read-only to them.

## 6. T1–T5 tooling roadmap (NOT YET CONTRACTED — recorded 2026-09-11 at Matt's question; each becomes a TOOLING burst before the experiment it instruments; "instrument before candidate")

| Burst | Instruments (closed-form unless marked) | Needs from bible / manifest | Before |
|---|---|---|---|
| **T1 sheet + gait** | `edit_canvas.py` (seed in slot 0; `seed_persistence` MAD slot-0 vs seed) · `visibility_table.py` (per-part expected visibility per direction from part *side*; catches a satchel switching hips) · `identity_vector.py` (model-free: per-part palette hist + silhouette + area vector; distance to master; loop trajectory) · `gait_oracle.py` (sole trajectories per boot from masks; planted = at ground line moving backward at walk speed in an in-place cycle; swing = above line moving forward; alternating leads; contacts at frames 1/5; no moonwalk; closure) · `pose_guide.py` (numbered-foot silhouette guides, 8 phases × direction, from a gait template) · `flow_smoothness.py` (optical-flow magnitude continuity; cv2 Farneback else block-match) | parts[] with `side`; ground line; gait template | X2, X4 |
| **T2 gear** | `gear_overlay.py` (variant − base diff → dilated mask → **gear layer RGBA per slot** — the modular asset; `base_preservation ≥ 99 %`, `overlay_containment` in allowed part regions) · `fit_check.py` (coverage of the underlying part; spill band) · `helmet_toggle.py` (hair preserved when off; helmet covers hair mask ≥ 95 % when on) · `set_consistency.py` (layer palette/area across 8 dirs × frames) · `manifest.py` + validator (engine-neutral JSON per E04/NEUTRAL_CONTRACT: frames, fps, pivot, direction, **layer stack + slot**, hitbox, emissive) · `godot_import.py` (SpriteFrames `.tres` + layer scenes — the port, written now) | parts[] → slot→region map; palette bins | X5 |
| **T3 scene** | `edge_sockets.py` (exit centres in bands; edge-strip profile similarity for plate joins) · `doorway_side.py` (declared interior/exterior + threshold band; aperture mask containment; exterior-imagery-only-on-exterior-side via annotation + brightness prior; JUDGE residue) · `plate_assembler.py` (room graph → plates → seam preview → walkable-mask union → HTML/Pixi-viewer with y-sorted Keeper vs props) · `nav_from_masks.py` (grid + BFS reachability of exits; Godot side = AStarGrid2D) · `plate_light.py` (key direction from wall shading gradients must match the sprite key — "room lit from the wrong side") · `normal_from_height.py` (Sobel normal map for Godot `CanvasTexture` — the F03 floor/wall glow as runtime 2D light) | plate socket conventions; part list for props | X6 |
| **T4 VFX** | `vfx_lifecycle.py` (cast 8 @ 20 fps · travel 6 loop + top/bottom mirror-diff · impact 10 unimodal energy curve + last frame fully transparent) · `attachment.py` (flare centroid vs staff-tip socket ± tol) · `element_hue.py` (dominant emissive hue within the element's band: frost / fire / physical) · `archetype_validator.py` (the sealed 24-archetype binding spec as data: required modules, timing, attachment rule, layer; every bundle validated) · `material_matrix.py` (material × damage-type → impact module coverage; blood-decal atlas builder + preview) · composite timing port of run_03 `test_preview.cjs` | archetype table (from `gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md` — sealed); sockets from manifest | X8 |
| **T5 light** | `rim_check.py` (key-facing silhouette arc brighter than the far arc) · `spell_only.py` (saturation outside the spell radius on cast frames ≤ non-cast level) · `value_range.py` (no pure-black shadows; histogram distance to F04/F03 anchors) · `no_floor_shadow.py` (alpha/dark blob below the sole line ≈ 0 — sprites carry **no** baked shadow; runtime shadows are the engine's) · `light_direction` per part (T0-c) | anchors; sole line | X2 (sprite), X6 (plate) |
| **cross-cutting** | `known_bad_factory.py` (mirror, shift, swell, repeated-lead, palette shift, overlay shift — every JUDGE/TRANSCRIBE batch draws a control here) · `transcribe_validator.py` (reader vs deterministic masks where both exist — calibrates the reader) · `bible_renderer.py` (bible JSON → REGISTER_CARD sections + per-part sentences + TELL-CONTROL block: **prompts become generated artifacts**) | the bible | X1+ |

Model-backed options deferred to R8's return: identity embeddings (CLIP/DINO), SAM-class part segmentation. Everything above is Pillow/numpy(/cv2) and costs zero image calls.
