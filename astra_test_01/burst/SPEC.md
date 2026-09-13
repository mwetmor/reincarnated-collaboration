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
`task.json`: `{"text": str, "references": [{"path": str, "role": str}], "image_cap": int, "minutes_cap": int, "tool_call_cap": int, "outputs": [str], "effort": "high" (Matt 2026-09-11: ALWAYS high; T0-d makes validate_task reject any other value), "add_dirs": [str]}`.
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

**C-2 amendment (ledger R-28 / R-30, 2026-09-12) — the freeze DOMAIN, stated once:** `lane/ gates/ oracle/ oracles/ parts/ compare/ transcribe/ review/ bible/ fixtures/ tests/` plus the six root contracts (`BURST_RULES.md JUDGE_RUBRIC.md REGISTER_CARD.md SPEC.md receipt.schema.json transcribe.schema.json`). **Excluded:** `__pycache__/`, `*.pyc`, `tests/tmp/`, and the suite's own volatile outputs `tests/t0c_suite_output.txt` + `tests/t0c_summary.json` — pinning those made pre-conditions P1 (run the suite) and P2 (the freeze verifies) contradict each other. `oracle/` (the T1 instruments **and the pre-registered band files**) sat outside the T1 freeze (`9146d9811620`); from the C-2 freeze on it is pinned, so a committed band cannot move silently. A data edit ruled by Matt (bible, bands) is a conductor edit + re-hash + ledger line; a TOOL edit is still a TOOLING burst + re-freeze + ledger entry.

## 6. T1–T5 tooling roadmap (NOT YET CONTRACTED — recorded 2026-09-11 at Matt's question; each becomes a TOOLING burst before the experiment it instruments; "instrument before candidate")

| Burst | Instruments (closed-form unless marked) | Needs from bible / manifest | Before |
|---|---|---|---|
| **T1 sheet + gait** | `edit_canvas.py` (seed in slot 0; `seed_persistence` MAD slot-0 vs seed) · `visibility_table.py` (per-part expected visibility per direction from part *side*; catches a satchel switching hips) · `identity_vector.py` (model-free: per-part palette hist + silhouette + area vector; distance to master; loop trajectory) · `gait_oracle.py` (sole trajectories per boot from masks; planted = at ground line moving backward at walk speed in an in-place cycle; swing = above line moving forward; alternating leads; contacts at frames 1/5; no moonwalk; closure) · `pose_guide.py` (numbered-foot silhouette guides, 8 phases × direction, from a gait template) · `flow_smoothness.py` (optical-flow magnitude continuity; cv2 Farneback else block-match) | parts[] with `side`; ground line; gait template | X2, X4 |
| **T2 gear** | `gear_overlay.py` (variant − base diff → dilated mask → **gear layer RGBA per slot** — the modular asset; `base_preservation ≥ 99 %`, `overlay_containment` in allowed part regions) · `fit_check.py` (coverage of the underlying part; spill band) · `helmet_toggle.py` (hair preserved when off; helmet covers hair mask ≥ 95 % when on) · `set_consistency.py` (layer palette/area across 8 dirs × frames) · `manifest.py` + validator (engine-neutral JSON per E04/NEUTRAL_CONTRACT: frames, fps, pivot, direction, **layer stack + slot**, hitbox, emissive) · `godot_import.py` (SpriteFrames `.tres` + layer scenes — the port, written now) | parts[] → slot→region map; palette bins | X5 |
| **T3 scene** | `edge_sockets.py` (exit centres in bands; edge-strip profile similarity for plate joins) · `doorway_side.py` (declared interior/exterior + threshold band; aperture mask containment; exterior-imagery-only-on-exterior-side via annotation + brightness prior; JUDGE residue) · `plate_assembler.py` (room graph → plates → seam preview → walkable-mask union → HTML/Pixi-viewer with y-sorted Keeper vs props) · `nav_from_masks.py` (grid + BFS reachability of exits; Godot side = AStarGrid2D) · `plate_light.py` (key direction from wall shading gradients must match the sprite key — "room lit from the wrong side") · `normal_from_height.py` (Sobel normal map for Godot `CanvasTexture` — the F03 floor/wall glow as runtime 2D light) | plate socket conventions; part list for props | X6 |
| **T4 VFX** | `vfx_lifecycle.py` (cast 8 @ 20 fps · travel 6 loop + top/bottom mirror-diff · impact 10 unimodal energy curve + last frame fully transparent) · `attachment.py` (flare centroid vs staff-tip socket ± tol) · `element_hue.py` (dominant emissive hue within the element's band: frost / fire / physical) · `archetype_validator.py` (the sealed 24-archetype binding spec as data: required modules, timing, attachment rule, layer; every bundle validated) · `material_matrix.py` (material × damage-type → impact module coverage; blood-decal atlas builder + preview) · composite timing port of run_03 `test_preview.cjs` | archetype table (from `gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md` — sealed); sockets from manifest | X8 |
| **T5 light** | `rim_check.py` (key-facing silhouette arc brighter than the far arc) · `spell_only.py` (saturation outside the spell radius on cast frames ≤ non-cast level) · `value_range.py` (no pure-black shadows; histogram distance to F04/F03 anchors) · `no_floor_shadow.py` (alpha/dark blob below the sole line ≈ 0 — sprites carry **no** baked shadow; runtime shadows are the engine's) · `light_direction` per part (T0-c) | anchors; sole line | X2 (sprite), X6 (plate) |
| **cross-cutting** | `known_bad_factory.py` (mirror, shift, swell, repeated-lead, palette shift, overlay shift — every JUDGE/TRANSCRIBE batch draws a control here) · `transcribe_validator.py` (reader vs deterministic masks where both exist — calibrates the reader) · `bible_renderer.py` (bible JSON → REGISTER_CARD sections + per-part sentences + TELL-CONTROL block: **prompts become generated artifacts**) | the bible | X1+ |

| **T0-d lane extensions (R9, C-1-or-never) — PLUS the T0-c review fixes, FIRST:** (a) `lane/audit.py`: the forbidden-tool regex applies to item `type`/`tool`/`name`/`server` ONLY — never to command text (the repo path `reincarnated-collaboration` matched `collaboration` seven times in T0-c); (b) `lane/run_burst.py` + `audit.py`: for TOOLING bursts, writes and receipt-listed files under declared `add_dirs` are PERMITTED — hash-verified in place, recorded in the ledger as `artifacts_in_place[]`, not harvested; (c) **O3b** `oracles/motif.py`: add a *primitive-family* mode — a radial-symmetry / ring detector (Loy–Zelinsky fast radial symmetry, or gradient-vote circular Hough, numpy/scipy) counting ring/radial features ≥ a size floor, partitioned by allowed masks — because the F04 bleed instances are family members, not copies (T0-c: template mode found inside=1, outside=0); keep template mode for copy detection; acceptance unchanged (F04 crop outside ≥ 3; clean crop 0); (d) `lane/run_burst.py`: `effort` must be `high` (reject otherwise) and the resolved model + effort are recorded per burst in the ledger (from the exec header or config); (e) `transcribe/questions.py`: declared-absent controls must be absent anatomical PARTS (helmet, cape, shield, second_belt), not merely absent sigils — **and a PART-inventory question set beside the motif set** (the T0-c generator counts the motif ON each part; the charter's X0-T calibrates the transcriber on the anatomical part inventory): `parts_questions(parts, controls)` / `parts_schema(parts, controls)` (lower-level forms so an F03 calibration list needs no F03 bible; controls appended to the closed list, expected absent/0), `bible.controls.declared_absent_parts`, `compare_answers` accepting either set, and **`compare/calibrate_transcriber.py`** scoring N inventories against the conductor's hand inventory — presence precision/recall, counts within ±1, control catch-rate, with the charter X0-T thresholds (P/R ≥ 0.9; ±1 on ≥ 80 % of parts; controls 100 %) as named parameters; **(f) the X1 review fixes (ledger R-2, 2026-09-11):** **F-1** the `--json` event stream does NOT surface `image_gen` calls (X1: only a `cat …/skills/.system/imagegen/SKILL.md` and a `cp` from `generated_images/` appear) — the image-call truth source is a before/after listing of `$CODEX_HOME/generated_images/` (env `CODEX_HOME`, else `~/.codex`; restrict to the burst's `thread_id` from `thread.started` when present): `image_calls` = new image files, each recorded (`path`, `sha256`) as `generated_images_new[]`; the old event heuristic is kept only as `image_calls_events` (reported, never authoritative); `receipt.calls_used != image_calls` ⇒ violation `image count mismatch`; **F-2** snapshot roots = the workdir + the declared `add_dirs` ONLY (never the whole repo); `.git/`, `__pycache__/`, `*.pyc` and the wrapper's own `out/.wrapper-*` logs are excluded from the diff; non-TOOLING tasks must declare `add_dirs: []` (validate_task rejects otherwise); **F-4** (doc, conductor) reads of Codex's own system skills under `$CODEX_HOME/skills/.system/` are permitted and expected — BURST_RULES + charter § 4 twin-edited; **F-5** `gates/plate_uniformity.py` (fraction of non-subject pixels within ±8/channel of #00ff00 + plate sd; calibration set = X1's two props: 100 % / 38 %, both sd < 1.1) and an `alpha_floor` parameter for character/prop mattes (residual alpha < 40/255 → 0; VFX/particle mode unchanged) so G9's border-clipping metric reads 0 on X1's props. **Split (conductor ruling R-3, HITL step 0 — 'instrument before candidate' applied to the instrument itself; charter § 7 T0 row allows 1–2 TOOLING bursts):** **T0-d1** = (a) (b) (d) (f: F-1, F-2) + `lane/check_sync.py` + tests — runs under the OLD wrapper, whose VOID on (a)/(b) is expected and recorded; the ledger entry also gains `model` (resolved from the profile — the stream does not echo it), `effort`, `codex_version`, `profile_sha256`, `artifacts_in_place[]`; **T0-d2** = (c) (e) (f: F-5) + the R9 extensions below, through the T0-d1-fixed wrapper; **T0-d3** (owed by ledger R-5, 2026-09-12) = **O3b annulus discrimination** — `count_family` counts FILLED DISCS as ring-family (the clean crop's only peak is the mage's boot toe at (286,407) r=8; on the F04 crop the face, a fist and both boot toes sit among the 14 outside peaks beside the genuine ring-sigils): add a hollow-centre / inner-edge test as a NAMED parameter with a calibration note — a ring shows an inner edge at 0.4–0.85 r whose gradient sign opposes the outer edge (or: the centre disc within 0.5 r is closer in Lab to the surround than to the ring band); a filled disc shows neither; the synthetic calibration set gains filled discs at the three ring radii on flat and textured backgrounds (must count 0) beside the rings (must count) and a half-arc control; acceptance UNCHANGED (F04 crop outside ≥ 3; clean crop 0) — report the new F04 count and which peaks dropped; nothing tuned to the real crops; comparator + tests updated; full suite green. THEN: `lane/check_sync.py` (00-system § 7 SYNC hashes vs `shasum`; non-zero on drift) · `lane/provenance_capture.py` (read C2PA / XMP issuer, model, generated_at from every generated PNG **at ingest, before matting**; store beside the receipt) · `lane/ref_provenance.py` (every `references[]` entry must resolve to a first-party content-addressed asset in `runs/<run>/artifacts/` or `astra_test_01/run_0*/`; third-party images refuse) · `oracles/model_drift_probe.py` (a frozen probe set — N prompts + refs hashed into the bible — re-generated at K1 and at every burst-day boundary; O5/O1/O8 distance to the approved set; alarm threshold) · `oracles/pse_check.py` (XAG-118 photosensitivity on VFX/cast sequences: general flash = ≥10 % luminance change, fail at >3 flashes/s over ≥20 % of a 1280×720-equivalent area; red-flash rule `R/(R+G+B) ≥ 0.8` and `(R−G−B)×320 > 20`; spatial-pattern rule) · `gates/matte_quality.py` (green-plate matte health: spill fraction, edge halo, particle loss — **model-coupled**, re-validated on every drift alarm) · `oracles/sheet_consistency.py` (sheet-level statistic beside pairwise identity_vector — pairwise is reported insufficient) · **ledger-entry** fields (not the receipt — strict-mode receipts require every property, and a burst cannot know a probe distance or a retirement date; refined at T0-d2 authoring): `generator {observed_fingerprint, probe_set_sha256}`, `regeneratable_until`, written null by the wrapper and filled by the conductor after the probe runs; bible: `never_generated[]`, `content_flags{blood, skeletal, religious_iconography}` per asset, `asset_id` (slot-stable) distinct from `content_hash`; `deps_ledger.py` keys on `asset_id` | bible probe set; first-party asset index; element_palette carries XAG-118 thresholds | after X1 (zero images; next session acceptable) |
| **T0-e mask composite (X3 / X5; charter § 5 named `mask_composite.py` as a T0 build — omitted from the T0-b contract, a conductor gap found at K3 2026-09-12)** | `gates/mask_composite.py`: `composite(base_rgba, variant_rgba, region_box, thresh, dilate_px) -> (out_rgba, mask, metrics)` — |variant − base| (max over RGB, alpha-aware) thresholded + dilated by `dilate_px`, restricted to the declared `region_box` (x0,y0,x1,y1 on the 512 canvas); the generated pixels are pasted ONLY inside the mask; **base pixels outside the mask are byte-identical**; metrics: mask area fraction, base_preserved_fraction (outside-mask pixels identical / all outside-mask pixels), changed-inside fraction · **G12** `evaluate(base, out, mask, subject)` → result envelope: `base_preserved_fraction ≥ 0.99` literal (pre-registered, charter § 7 X3), `passed` null if the mask covers > 60 % of the figure (composite meaningless) · `compose_loop(base, variants[], region_boxes[])` helper for a frame set · tests with known-bad inputs: a variant that differs everywhere (mask blows up → null), a shifted variant (region box catches the shift), a byte-identical variant (mask empty, preserved 1.0), a planted out-of-box change (must be dropped and reported) | region boxes declared per animation (idle: torso/shoulders/staff-tip band; walk: legs + arms) | before X3 / K3 composite (fires serially at the first quiet lane) |
| **T1a-idle — idle oracle instrument (memo `2026-09-12-oracle-derived-testing-suite-spec.md` § 11; Matt R-21 intent-first, R-24 GO)** | `oracle/__init__.py` · `oracle/motion_map.py`: `load_frames(dir) -> list[np.uint8 HxWx3]` (numbered PNGs, RGB; RGBA/green-keyed frames are matted first via `gates.matte.remove_chroma_key` and composited on the median colour so the same code path serves reference clips and our 512-canvas frames); `camera_shift(frames) -> px per frame` (phase correlation on downscaled luminance; any |shift| > 1 px marks that frame VOID); `motion_energy(frames, box, tau) -> dict` — median background over the clip, per-pixel |frame − median| (max over RGB), thresholded at `tau`, restricted to the figure `box` (x0,y0,x1,y1 XYXY exclusive) with height H = y1−y0; regions as bands of H: head 0–18 %, shoulders_chest 18–45 %, hips 45–60 %, legs 60–85 %, feet 85–100 %, plus arms_left/arms_right = the outer 22 % columns of the box between 18–60 %; per frame per region: energy = changed pixels / region pixels; `head_dy` = vertical centroid of changed pixels in the head band (px and /H); `chest_dw` = width of the changed-pixel column extent in shoulders_chest (/H); `weapon_tip` = topmost changed row outside the box within 0.5 H above it (/H, null if none) · `oracle/idle_curves.py`: `period(signal, fps) -> (frames, seconds, confidence)` by autocorrelation (null if confidence < 0.3 or signal flat); `amplitude(signal)` = (p95 − p5); `classify_regions(energy_by_region, eps, floor) -> {LOCK: [...], MOTION: [...], moving_count}`; `curves(frames_dir, box, fps, tau, eps, floor) -> dict` with every series and the summary · `oracle/idle_bands.py`: CLI `python3 -m oracle.idle_bands --ref DIR --box x0,y0,x1,y1 --fps 12 --label relaxed|combat --out oracle/bands_idle.json [--plot_dir DIR]` — merges a row per label: `{breath_amplitude_H, breath_period_s, head_sway_H, lock_regions, motion_regions, moving_count, provenance:{source_note, frames, fps, box, tau, eps, floor}}` with `floor = 0.6 × value`, `target = value`, `ceiling = 1.5 × value` for every amplitude; `--ours DIR --label X` measures our frames the same way (box derived from the alpha/keyed mask bounding box) and writes `runs/C-1/oracle/<label>_ours.json`; `--plot_dir` writes `<label>_curves.png` (series overlaid, bands shaded) and `<label>_box_check.png` (frame 1 with the box + region bands drawn) — **plots go ONLY to the given plot_dir (outside the repo when the input is a class-E reference); numbers only in the repo** · tests `tests/test_oracle_idle.py`: synthetic idle (a static figure of blocks; a 'chest' block whose width breathes sinusoidally with period 24 f, amplitude 6 % H; a 'head' block bobbing 2 % H at the same period; feet + legs static; 96 frames) → period recovered ± 1 frame, breath amplitude within ± 15 % of truth, head sway within ± 15 %, feet/legs/hips classified LOCK, shoulders_chest + head MOTION, moving_count 2; a static clip → all LOCK, period null, moving_count 0; the synthetic idle with a 3-px/frame pan → every frame VOID (camera_shift), summary `passed: null`; a green-keyed 512 RGBA-style copy of the synthetic → identical curves (same code path) · stdlib + Pillow + numpy + scipy only; result envelopes follow `gates/common.py` | Hades clean cycles (class E, Desktop, read-only) as `--ref`; our K3-reg-02 idle frames as `--ours` | T1a-idle: first serial TOOLING burst of Phase 1 (R-24); Matt checkpoint on the curves before any band is committed |
| **T1a-walk — walk oracle instrument on Muybridge (memo §§ 1–4; legolas R10 § 5.4 W-1…W-6; R-21 12-frame walk; R-22 plates 2 + 13)** | `oracle/walk_landmarks.py`: `figure_mask(frame_rgb) -> bool HxW` for a Muybridge collotype cell (luminance Otsu after a median filter that suppresses the printed grid; largest connected component; morphological close) and for our 512-canvas RGBA/green frames (alpha ≥ 128 via `gates.matte`); `landmarks(mask) -> dict`: `head_top_y` (topmost mask row; plus `head_top_thin` flag when the top 5 % of the figure is < 3 px wide — the dark-hair-on-dark-backdrop case — and a `head_ref_y` fallback = topmost row of the widest run in the upper 20 %), `sole_line_y` (bottommost row), `H`, `head_cx` (centroid x of the top 12 %H), `foot_L_x/foot_R_x` (the two lowest components below 0.75 H, left/right by x with temporal continuity), `planted` per foot (sole within 2 px of the ground line), `wrist_ext_L/R` (mask extent beyond the torso column at 0.45 H per side), `torso_cx`; all in px and ÷ H · `oracle/walk_curves.py`: `phase_table(landmarks_seq) -> list` assigning CONTACT / DOWN / PASSING / UP per frame from the planted-foot events (12-frame cycle: two contacts); `bob(series)` → W-1 peak-to-peak head-top y / H, W-2 frame index of min/max mapped to phase, W-4 count of minima; `head_path(cx, cy)` → W-3a PCA minor/major ratio, W-3b signed area ÷ (A_vert × A_lat), W-3c sign changes of x over the closed cycle; `arm_swing` → W-5 peak-to-peak wrist extent / H per side, W-6 fraction of frames where the arm opposes the same-side leg; `sole_scroll` → planted-sole x per frame and slip (px / frame deviation from the mean scroll) · `oracle/walk_bands.py`: CLI `python3 -m oracle.walk_bands --ref DIR --pattern '*.png' --fps 8.33 --label plate2_lateral|plate13_lateral|plate13_front|plate13_rear --out oracle/bands_walk.json [--plot_dir DIR]` — per label a row with the measured Muybridge value as `floor` for W-1 / W-5 / sole scroll, `target = floor × k` with named parameters `k_vert = 2.0` (animators amplify the vertical — Williams; Legolas § 1.4) and `k_lat = 0.5` (suppress the lateral), `ceiling` from Legolas § 5.4 (W-1 7 %H; W-3a ≤ 0.35; W-3c 2–3; W-4 = 2; W-5 free arm 8–20 %H, weapon arm ≥ 3 %H; W-6 ≥ 6/8 → for 12 frames ≥ 9/12), the 12-frame phase table, and provenance (plate, row, fps, mask params); `--ours DIR` measures our registered frames the same way → `runs/C-1/oracle/<label>_ours.json`; plots: `<label>_curves.png` (head y, head x, per-foot sole x, wrist extents over phase; bands shaded), `<label>_mask_check.png` (frame 1 mask + landmarks drawn) — Muybridge is public domain, so plots may live under `runs/C-1/oracle/plots/` · tests `tests/test_oracle_walk.py`: a synthetic 12-frame walker (block torso + head bobbing 3 %H at period 6 with minima on DOWN, two feet alternating with one planted and scrolling, arms opposing legs) on (i) a plain backdrop and (ii) a printed-grid backdrop → identical landmarks within 1 px; W-1 within ± 15 %, W-2 min on DOWN, W-4 = 2, W-3c = 2, W-6 ≥ 11/12, planted foot detected on every frame; a 'floating' walker (no bob) → W-1 below floor reported, `passed` false; a 'pigeon' walker (head on a circle) → W-3a > 0.35 · stdlib + Pillow + numpy + scipy only; envelopes per `gates/common.py` | Muybridge plate 2 lateral (`05 …/_frames/NN.png`, 322×520) and plate 13 lateral / front / rear (`05b …/_frames/<row>_NN.png`, 395×773), public domain; our K3 walk frames if registered | T1a-walk: second serial TOOLING burst (after T1a-idle review) |
| **T1a-idle-2 — idle instrument FIX (conductor ruling R-25: the T1a-idle formulas measure changed-pixel extent, not displacement)** | (1) **Geometric displacement estimators** in `oracle/motion_map.py`: `band_shift_y(frames, box, band)` → per-frame vertical displacement (px, /H) of the band's content relative to the clip median, and `band_edges_x(frames, box, band)` → per-frame left/right silhouette-edge positions and their width (/H) — estimator is the builder's choice (residual row/column-profile cross-correlation against the median-frame profile; or edge tracking of the changed region's outer boundary; or a background-subtracted figure mask with hysteresis) but it MUST recover the synthetic truth: breath (chest width p95−p5) 6 %H ± 15 % and head bob 2 %H ± 15 % on the T1a-idle synthetic — these two existing red tests become the acceptance and must go green with the truth values unchanged; `head_dy` and `chest_dw` in the summary now come from these estimators (keep the old extent series under `_extent` for lineage) · (2) **Control box**: `motion_energy` takes an optional `control_box` (same size as the figure box, background only, default = the figure box translated by 1.2 × box width to whichever side lies inside the frame) and reports `control_energy` per region-equivalent band and `contamination = median(control energy) / median(figure energy)`; summary `passed: null` with reason `background_motion` when contamination > 0.5 · (3) **Noise-floor calibration (Legolas I-1)**: `eps` defaults to the p95 of the FEET band energy of the clip being measured (feet are locked by definition in a standing idle), `floor = 3 × eps`; both still overridable; report the derived values · (4) `--ours` mode: camera_shift is NOT applied (our registered frames are figure-registered; residual translation is G11's business) — report it as `figure_drift_px` instead, never VOID · (5) `--ref` for the combat idle uses RAW fixed-camera frames with an explicit `--box` (no tracking crop); the relaxed House clip is measured with its control box and the contamination number reported · tests: the two amplitude cases go green; a contaminated synthetic (moving background stripes behind a static figure) → contamination > 0.5, passed null, reason background_motion; a clean synthetic with a noisy feet band → eps derived ≥ that noise, feet LOCK | Hades combat RAW fixed-camera frames (class E, Desktop, read-only), Hades relaxed CLEAN_CYCLE frames (class E), our K3-reg-02 idle frames | T1a-idle-2: serial, immediately after T1a-idle; Matt checkpoint after it |
| **T1a-walk-2 — walk instrument METHOD CHANGE (conductor ruling R-26 after T1a-walk FAILED)** | (1) `figure_mask_row(frames)` in `oracle/walk_landmarks.py`: register the 12 cells of a row on the printed grid by phase correlation of a high-pass (grid-only) image, build the MEDIAN backdrop over the registered cells (the figure is at a different x in every cell, so the median is the empty backdrop), figure = |cell − median| (max over RGB) > tau after a white top-hat that removes lines thinner than 5 px; largest component; close; hole-fill; report per-frame mask area / H and a `grid_leak` score (fraction of mask pixels lying on the detected grid lines) · (2) `track_head(frames, masks)`: pick the template frame as the one whose upper 20 % has the widest run; head patch = the top 12 %H of the mask's bbox; per frame normalized cross-correlation within ± 25 %H of the previous position → `head_cx, head_cy` (template-tracked), with `head_top_y` = template top row + the tracked offset; the mask-top series stays as `head_top_mask_y` for lineage · (3) `planted` = a foot component whose sole centroid x moves ≤ 2 px between consecutive frames (camera fixed → planted foot stationary on the plate) AND whose sole is within 3 px of the ground line; CONTACT = the first planted frame of each foot's stance; expect exactly two contacts per 12-frame row; W-2/W-4 from the tracked head; sole scroll = the SWING foot's x-velocity (the planted one is by definition still) · (4) synthetic test: the grid-backdrop walker must yield landmarks within 2 px of the plain-backdrop walker (currently 5 px on head_ref_y); two contacts detected; W-4 = 2 · (5) run rows plate13_lateral (primary), plate13_front, plate13_rear, plate2_lateral (secondary); report W-1 lateral and flag if outside 1–5 %H (Legolas veridical sanity band) — a value outside it means the head track failed, not that Muybridge bobbed that much | Muybridge plates (public domain) | T1a-walk-2: serial, immediately after T1a-walk |
| **T1a-walk-3 — walk instrument: ANNOTATED-LANDMARK path + mask-stability selector (conductor ruling R-27 after two segmentation failures)** | (1) `oracle/walk_bands.py --landmarks JSON --label L --fps 8.33 --out oracle/bands_walk.json [--plot_dir]`: reads an ANNOTATE burst's `annotation.json` (per frame: head_top, chin, hip, near_sole, far_sole, near_wrist, far_wrist, ground_y, planted_near/far, confidence; subject_height_px; stride_notes) and computes the SAME W-quantities as the mask path from those points: H = ground_y − head_top.y (per frame, and the mean); W-1 = p2p(head_top.y)/H; W-2 = frames of head-y min/max mapped onto the phase table; W-3a/b/c from (head_top.x, head_top.y); W-4 = minima count; W-5 per arm = p2p(wrist.x − hip.x)/H (near = the arm nearer the camera); W-6 = fraction of frames where sign(wrist.x − hip.x) opposes sign(same-side sole.x − hip.x); phase table from planted flags (CONTACT = first planted frame of a stance; PASSING = the frame where |near_sole.x − far_sole.x| is minimal; DOWN/UP between) — expect two contacts; swing-foot scroll = Δx of the non-planted sole; every quantity carries `source: 'annotation'` and the mean confidence · (2) mask path kept: `figure_mask_row` reverts to METHOD A (Otsu + median filter + morphology, the T1a-walk version) as default; add `mask_stability` = coefficient of variation of mask area over the 12 frames and `mask_H_cv` likewise; the mask estimate is REPORTED only when both CV < 0.25, else `mask_estimate: null, reason: unstable_segmentation` · (3) `--landmarks` + `--ref` together → an AGREEMENT block per quantity (annotation vs mask; |Δ| and whether within 20 % of the annotation value); the band row's `value` = the annotation value, `mask_agrees` boolean · (4) `--ours DIR` unchanged (alpha masks) · tests: a synthetic annotation JSON generated from the synthetic walker's true landmarks → W-1/W-4/W-3c/W-6/phase table recovered exactly; a JSON with one planted flag flipped → phase table reports `expected two contact events; observed N` rather than fabricating | `runs/C-1/artifacts/T1a-ann-13L/annotation.json` (Muybridge plate 13 lateral; PD) ; Muybridge fixtures under `fixtures/muybridge/` | T1a-walk-3: serial TOOLING after T1a-ann-13L |
| **T1b — intent gates + dope sheets + pose guides (memo §§ 5–6; R-21 intent-first; consumes T1a bands)** | `gates/idle_intent.py`: `evaluate(frames_dir, bands_idle_row, label)` → result envelope: MINIMUM-amplitude gate (breath %H and head bob %H measured by `oracle.idle_bands --ours` must be ≥ the band floor; report value/floor/target/ceiling), MAXIMUM gate (≤ ceiling → 'panting'), region classification by per-band DISPLACEMENT (not energy): a region is LOCK if its band_shift p2p ≤ lock_eps (default 0.4 %H), MOTION otherwise; I-1 feet LOCK is mandatory (any sole displacement > 0.25 %H fails); the expected LOCK/MOTION lists come from the band row; `passed` null when the band row is `committed: false` (report-only until Matt commits) · `gates/gait_intent.py`: `evaluate(frames_dir, bands_walk_row, phase_table)` on OUR alpha-masked frames via `oracle.walk_landmarks` (mask path — clean masks) → W-1 (floor/target/ceiling from the row), W-2 phase check against the row's phase table, W-3a/c, W-4, W-5 per arm (weapon arm ≥ 3 %H, free arm 8–20 %H), W-6 (≥ 9/12), planted-sole slip; envelope per gate; `passed` null while the row is uncommitted · `oracle/dope_sheet.py`: `idle_sheet(bands_idle_row, n_frames, fps)` → per-frame targets: head Δy and chest Δw on a sine at the band period (or n_frames/fps if period null), the LOCK list as assertions, the MOTION list with amplitudes; renders `prompt_text` (one sentence per frame + the lock/motion sentences) and a JSON table; `walk_sheet(bands_walk_row, n_frames=12)` → per-frame phase (CONTACT/DOWN/PASSING/UP from the row's 12-frame table), head height above ground (target amplitude = floor × k_vert, phase from W-2), planted foot + swing-foot x, arm opposition; `prompt_text` per frame ('frame 3 — PASSING: …') · `oracle/pose_guide.py`: `render_walk_guide(walk_sheet, H_px, canvas=512)` → 12 numbered line-art PNGs (ground line, two sole outlines at the sheet's x/y, a head circle at the sheet's height, phase label) — drawn from the TABLE, no reference pixels; `render_idle_guide(idle_sheet, base_rgba)` → overlay of the breath extremes as two outlines · `gates/g6_seam.py` amend: add `G6c` (seam frame-pair difference vs the half-cycle homologue pair; PASS ≤ 1.25×; walks only; idles fall back to G6b) as a function beside the existing G6/G6b, tests with a synthetic loop where the seam equals the homologue (ratio ≈ 1) and one with a broken seam (ratio > 1.25) · tests: idle_intent on our K3-reg-02 idle-S against the (uncommitted) combat row → reports below-floor with passed null; a synthetic breathing loop at the target → within band; gait_intent on the synthetic 12-frame alpha walker → all W gates evaluated, W-4 = 2, W-6 ≥ 9/12; dope_sheet round-trip: sheets generated from the synthetic bands reproduce the synthetic's per-frame targets; pose_guide renders 12 PNGs with the right sole positions (assert pixel positions) · stdlib + Pillow + numpy + scipy | `oracle/bands_idle.json`, `oracle/bands_walk.json` (+ annotation row), our K3-reg-02 frames | T1b: serial TOOLING after T1a-walk-3 |
| **T1c — judge questions from the dope sheet + X0-M motion-transcriber calibration (memo § 7; JUDGE/TRANSCRIBE families; Muybridge PD as calibration frames)** | `transcribe/motion_questions.py`: `questions_from_walk_sheet(sheet)` → DSG-shaped YES/NO questions per frame and per pair (planted foot per frame; lead alternation between contacts; head higher at PASSING than at CONTACT; arm opposes leg; frame 12→1 continuity) and `questions_from_idle_sheet(sheet)` (do the feet move? does the chest rise and fall? does the head drift? does the staff tip drift? is frame N→1 continuous?) with a closed answer schema and one DECLARED-ABSENT control per set (a question whose truth is known false for the sheet) · `compare/calibrate_motion_transcriber.py`: given a transcriber's answers on the 12 Muybridge plate-13 frames (ground truth = the T1a-ann-13L annotation → derived truth table) scores presence P/R on the closed set, per-question accuracy, control pass rate; pre-registered bar: accuracy ≥ 0.85, controls 100 %; writes `runs/C-1/x0m/calibration_summary.json` · `briefs` are NOT written by this burst; it writes the QUESTION SET files `runs/C-1/x0m/questions_plate13.json` + `truth_plate13.json` so the conductor can fire the X0-M TRANSCRIBE bursts · tests: question generation from the synthetic walk/idle sheets (counts, control present, schema valid); calibration scorer on a perfect answer set → 1.0 and on the control-failed set → controls < 100 % | dope sheets from T1b; T1a-ann-13L annotation | T1c: serial TOOLING after T1b; then X0-M TRANSCRIBE bursts (non-TOOLING, parallel) |
| **T4 VFX (amend)** | + `pse_check.py` runs on every cast/travel/impact sequence and every composite preview | | X8 |
| **T5 light / resolution (amend)** | tell oracles (O1–O8) run at **display size** (the locked resolution table's on-screen hero height), not only at the 627-px native cell; the resolution table is an **unrepeatable mint-time lock** (D2R rebuilt its renderer rather than re-mint sprites — GDC 2022) with the Steam Deck **9 px minimum glyph height at 1280×800** written in | resolution table (Matt, HITL) | before K2 |
| **budgets (amend)** | memory constant = **4 bytes/px RGBA8, lossless** (Godot 2D: VRAM compression avoided); add a **fill-rate** budget beside memory | | C-2 |

Model-backed options deferred to R8's return: identity embeddings (CLIP/DINO), SAM-class part segmentation. Everything above is Pillow/numpy(/cv2) and costs zero image calls.
