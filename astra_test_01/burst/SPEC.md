# Astra burst lane — T0 SOFTWARE SPEC v1.0 (build-to-spec; Astra builds, gandalf reviews + freezes)

> **STATUS:** BUILD CONTRACT for TOOLING bursts T0-a / T0-b / T0-c (Run C-1). Author: gandalf, 2026-09-11. Charter: `agentic_orchestration/gandalf/notes/2026-09-11-astra-burst-lane-run-charter.md` (§ 2 register card, § 4 burst rules, § 6 rubric — extracted verbatim by T0-a).
> **Constraints binding on every TOOLING burst:** Python 3 stdlib + Pillow + numpy (+ OpenCV **only if already importable**; else numpy fallbacks). No `pip install`. No network. No image generation. Write ONLY under `astra_test_01/burst/`. Read only the paths named here. Every module ships `tests/test_<module>.py` (unittest, stdlib) with **known-bad fixtures**; a test that cannot fail on a bad input is not a test. No PASS/FAIL vocabulary in receipts — results are numbers + booleans consumed by the conductor.

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

**`receipt.schema.json`** (what `--output-schema` enforces):
```json
{"type":"object","required":["task_id","status","images","calls_used","retries","self_report"],
 "properties":{"task_id":{"type":"string"},
 "status":{"enum":["DELIVERED","DELIVERED_WITH_CONCERNS","FAILED"]},
 "images":{"type":"array","items":{"type":"object","required":["name","path","sha256","prompt","references","elapsed_s"],
   "properties":{"name":{"type":"string"},"path":{"type":"string"},"sha256":{"type":"string"},"prompt":{"type":"string"},
   "references":{"type":"array","items":{"type":"object","required":["role","path"],"properties":{"role":{"type":"string"},"path":{"type":"string"}}}},
   "elapsed_s":{"type":"number"}}}},
 "calls_used":{"type":"integer"},"retries":{"type":"array","items":{"type":"object","required":["reason","change"],"properties":{"reason":{"type":"string"},"change":{"type":"string"}}}},
 "self_report":{"type":"object","required":["obeyed_invariants","concerns"],"properties":{"obeyed_invariants":{"type":"boolean"},"concerns":{"type":"array","items":{"type":"string"}}}},
 "files":{"type":"array","items":{"type":"object","required":["path","sha256"],"properties":{"path":{"type":"string"},"sha256":{"type":"string"}}}}}}
```
**Tests (T0-a):** render determinism; dry-run command exactness; audit detects a planted `web__run` line, a planted write outside `out/`, and an image-cap breach from synthetic event files; ledger atomicity; schema_check rejects a receipt with `status:"PASS"`.

## 3. T0-b — gate library (port; regression-locked to run_03)

Port from `astra_test_01/run_02/{guides.py,pipeline.py,registration_preflight.py}` and `astra_test_01/run_03/{turnaround.py,check.py,check_vfx.py,animation.py,package.py,preview_template.html}` — **preserve their measurement definitions exactly**; wrap, don't reinvent. Guides: projection constants become a parameter; the C constants come from `astra_test_01/design/experiments/E01/projection-candidates.json` (read it; if C is not numerically defined there, record `UNEVALUABLE` in the receipt concerns and keep the run_02 constants as the default — do not guess).
- `matte.py` green-plate extraction (particle-safe, run_02 semantics; also expose `remove_chroma_key`-style single-call). `register.py` uniform scale + translation from reviewed contacts; `measured_anchor`.
- `g1_height` ±3 % vs S · `g2_pivot` **two quantities**: root anchor (±4 px literal) and planted-sole contact trajectory (reported) · `g3_light` brightest-5 % centroid in upper-left half · `g5_drift` consecutive MAD < frame0-vs-cast05 · `g6_seam` literal (seam ≤ min internal) **and** `g6b` (seam ≤ median internal), both reported · `g9_alpha` edge mean + dark-fringe check · `drift48.py` 48-px downsample neighbour diff (same comparator as g5) · `silhouette64.py` 64-px BW alpha → Hu moments + aligned IoU vs master; `distance()`.
- `pack.py` sheets/atlas/contacts exactly as run_03 `package.py`; `review/build_review.py` from `preview_template.html`.
- `run_gates.py --frames-dir <run_03 or new> --master <S idle 00> --out checks.json` → list of § 1 results.
**Regression lock:** running the suite on `astra_test_01/run_03/character/frames` must reproduce `run_03/evidence/current_checks.json` numbers (seam/drift/height/pivot) to 1e-3; record the diff in the receipt. **Known-bad tests:** run_02's seven (checkerboard rejection, upscaling rejection, clipped-sole rejection, wrong-side light, measured registration, native-alpha dark interiors, wrong-side/clipping detection) + shifted-mask, repeated-lead, swollen-bag synthetic cases.

## 4. T0-c — parts, motif oracle, comparator, transcription schema

- **`parts/part_masks.py`** — `classify_by_palette(rgba, bins: {part: [(h_lo,h_hi,s_min,v_min)]}) -> {part: mask}` (HSV hue bins, value-insensitive); `from_label_pass(label_rgba, colors: {part: (r,g,b)}, tol) -> {part: mask}`; `alpha_fit(mask, alpha, k_px) -> {"inside_frac": f, "ok": bool}`.
- **`parts/motif_match.py`** — `count_instances(frame_rgb, template_rgb, scales=(0.5..1.5), thresh, allowed_masks: [mask]) -> {"inside": n, "outside": m, "boxes": [...]}`. OpenCV `matchTemplate` (TM_CCOEFF_NORMED) with NMS if `cv2` importable; else a numpy normalized cross-correlation at ≤ 3 scales. Must run on a 1536×1024 image in < 30 s CPU.
- **`parts/part_metrics.py`** — `area(mask)`, `centroid_rel(mask, torso_mask)`, `palette_distance(frame, mask, palette_hex[])`, `hf_energy(frame, mask)` (Laplacian variance), `light_direction(frame, mask) -> degrees` (luminance gradient of the shaded part).
- **`transcribe.schema.json`** — `{frame, parts:[{name,bbox,confidence}], motifs:[{type,bbox,on_part}], straps:[{from_part,to_part,anchored}], materials:[{part,material}], light_dir_deg, notes}`.
- **`bible/schema.json`** — RULE rows: `{id, faction, class: motif|material|construction|silhouette|palette|plain-budget|light|scale|parts, statement, placements:[{where,scale,count}], exclusions:[...], reference_asset, oracle:{id|"JUDGE-only", threshold, inputs}, known_bad, source: matt-ruling|bible-author|oracle-feedback, date}` plus a top-level `parts:[{name, adjacent:[...], rigidity: rigid|cloth|hair, allowed_motifs:[...], palette_bin}]`.
- **`bible/f04-keepers.stub.json`** — parts list for the Keeper (hair, face, shirt, tabard, belt, satchel, pauldron_L, pauldron_R, bracers, trousers, boots, rod, rod_head) and ONE motif rule: `sigil` allowed on `[tabard, rod_head]`, excluded everywhere else, `oracle: motif_match`. Everything else `JUDGE-only` placeholders. Vocabulary rows come later from Matt's rulings — do not invent them.
- **`compare/compare_to_bible.py`** — `compare(bible, gate_results, transcription|None, masks|None) -> [{rule_id, passed|null, value, threshold, diff}]`. For `motif_match` rules: outside-count must be 0.
- **Fixtures:** `fixtures/f04_advanced_crop.png` (crop of `astra_test_01/design/experiments/E07V/art/F04.png`, the advanced figure), `fixtures/sigil_template.png` (crop of the handheld astrolabe head — locate it by viewing the image; record the bbox in `fixtures/manifest.json`), `fixtures/clean_crop.png` (a run_03 mage frame, no astrolabe), run_03 S idle 00 / cast 05 / walk frames as needed.
- **Acceptance (the gate must catch the defect Matt found by eye):** `count_instances(f04_advanced_crop, sigil_template, allowed=[rod_head_bbox]) → outside ≥ 3`; on `clean_crop` → outside == 0; `compare_to_bible` with the stub bible FAILS the F04 crop and PASSES the clean crop. `silhouette64.distance(S idle 00, S idle 00 mirrored)` must be clearly > `distance(S idle 00, S idle 01)`.

## 5. Freeze protocol (conductor, after each T0 burst)

gandalf reviews the receipt + code + test output (DRIFT-CRITIC), runs the tests, then writes `MANIFEST.sha256` over `lane/ gates/ parts/ compare/ review/ *.json *.md`. Any later change = a new TOOLING burst + re-freeze + ledger entry. GENERATE/CHECK/JUDGE bursts read tools by absolute path; the sandbox (workspace-write on a workdir outside the repo) makes the repo read-only to them.
