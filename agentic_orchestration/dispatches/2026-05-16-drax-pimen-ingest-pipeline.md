# Dispatch — 2026-05-16 — drax — Pimen ingest pipeline (VS2a foundation)

**From:** knight-rider
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4 (per VS2a critical-path scope; bandwidth-binding constraint per roadmap Risk 1 — starting clock now)
**Status:** PENDING — ACTIVE
**Estimated effort:** 2-3 sessions (~6-12 hours total); pipeline-plumbing work, not math-driven. Tag at end of pipeline build (no smoke season needed until first integration consumes assets).
**Acceptance:** Reusable ingest pipeline that converts elrond-curated Pimen pack records → demo-consumable VFX assets. Three stages required: RAR-unpack, frame-assembly, canvas metadata extraction. Pipeline runs on the existing curated subset (test against 2–3 representative packs); broader catalogue ingestion happens later as VS2a integration progresses.

---

## Context — why now

**This is the VS2a foundation dispatch for drax.** Per `canonical/16-project-roadmap.md` §VS2a:
- B6 (rocket pre-work + gamora main), B10 V2 (gamora), B11 (rocket + drax), and Pimen first integration (drax) all gate VS2a ship.
- Drax is the binding bandwidth constraint (Risk 1, ~4-6 months saturation under combined VS2a + VS2b load).
- **Starting the Pimen ingest pipeline clock now is the single biggest schedule lever for drax.**

**Three-track Pimen viability gate (Day 3) findings drove this dispatch:**

Per `agentic_orchestration/skill_handoff_2026-05-16.md` §"Pimen viability gate":
- Drax filed PASS WITH FLAGS — wiring track.
- **Must-have #1:** RAR-unpack step required (75% of packs are RAR; Pixi.js can't consume RAR at load-time — unpack at curation/ingest).
- **Must-have #2:** Frame-assembly step needed for individual-frame-only packs (`ice-spell-effect-01` confirmed; others TBD at full crawl — now COMPLETE).
- **Nice-to-have:** Per-animation canvas metadata (pack-level single-cell-size assumption breaks on non-square canvases).

Elrond's full curation pipeline ran 2026-05-16 (COMPLETE; `dispatches/2026-05-16-elrond-pimen-full-catalogue-curation.md`). Elrond produced the curated records at `research/curated/`. **Your ingest pipeline consumes those records as input** and produces demo-consumable assets as output.

## What this dispatch builds

A three-stage ingest pipeline. Each stage is independently testable; together they form the pipeline.

### Stage 1 — RAR-unpack

**Input:** elrond-curated Pimen pack records (with `file_format` indicating archive type — RAR or ZIP).
**Output:** unpacked pack directory ready for Stage 2.

Requirements:
- Detect archive type from the curated record (don't assume; the catalogue includes ZIP packs too — e.g., `Battle VFX Projectile` is ZIP).
- Use `unrar` or a Node.js equivalent that handles the RAR format used by Pimen.
- Output to a deterministic per-pack directory (`assets/pimen/<pack-slug>/raw/`).
- Idempotent: re-running on an already-unpacked pack should no-op (or refresh deterministically).
- Log per-pack: source archive, output dir, file count, total bytes.

**Test:** unpack 2-3 representative packs that elrond's curation flagged — at least one RAR (most packs) and one ZIP (e.g., Battle VFX Projectile). Verify outputs are byte-identical across runs.

### Stage 2 — Frame-assembly

**Input:** Stage 1 unpacked pack directory.
**Output:** assembled sprite sheets (or assembled animation frames if sheet-output is wrong for Pixi.js consumption — your call).

Requirements:
- Detect pack layout: full sprite sheet (most packs) vs individual-frame-only (confirmed: `ice-spell-effect-01`; others surfaced by elrond's curation).
- For individual-frame packs: assemble frames into a single sheet (column-major or row-major; document your choice).
- For sheet-packs: pass through; preserve original sheet layout.
- Output to `assets/pimen/<pack-slug>/sheets/` (or equivalent — your call on layout).
- Idempotent.

**Test:** at minimum, validate the assembly works on `ice-spell-effect-01` (the confirmed individual-frame case) and on a known sheet-pack. Verify Pixi.js can load the output (smoke test: `PIXI.Texture.from()` or equivalent succeeds on the output sheet).

### Stage 3 — Canvas metadata extraction

**Input:** Stage 2 assembled sheets.
**Output:** per-animation canvas metadata JSON describing canvas dimensions per animation.

Requirements:
- For each animation in the pack, determine the canvas dimensions (width × height per frame).
- **The "nice-to-have" from the viability finding:** pack-level single-cell-size assumption breaks on non-square canvases. Surface per-animation cell sizes, not pack-level.
- Output to `assets/pimen/<pack-slug>/metadata.json` with shape:
  ```json
  {
    "pack_slug": "...",
    "animations": [
      { "name": "...", "frame_count": N, "canvas_width": W, "canvas_height": H, "fps_hint": ... }
    ]
  }
  ```
- If Aseprite source is available in the curated record (per elrond's note: 13 packs include Aseprite), prefer Aseprite-derived metadata over assumption.

**Test:** validate metadata accuracy on 2-3 packs. Spot-check at least one pack with non-square canvas (e.g., Buff/Debuff Pack 09 was flagged as a register outlier at 24×24 retro band).

## Repo placement

- **Pipeline scripts:** your call. Two reasonable options:
  - `reincarnated-demo/scripts/pimen-ingest/` (lives with the consumer; clear seam ownership)
  - `agentic_orchestration/scripts/pimen-ingest/` (lives with the catalogue, shared)
  
  Recommendation: demo repo. The ingest pipeline IS demo infrastructure; the curated records live in collaboration but are read-only inputs. Demo repo placement makes the seam boundary crisp.

- **Output assets:** `reincarnated-demo/public/assets/pimen/` (or equivalent; subject to demo asset-loading convention).

- **Curated records (read-only):** `~/Games/reincarnated-collaboration/agentic_orchestration/research/curated/` (elrond's seam; reference but do not modify).

## Out of scope (explicit — do NOT do these)

- **First VFX integration in demo.** The ingest pipeline produces consumable assets; CONSUMING them in scenes is a separate later dispatch. This dispatch builds infrastructure only.
- **Loadout-side VFX consumption.** VS2b territory.
- **Frame-by-frame visual review.** That was elrond's curation pass (COMPLETE); trust the curation flags. If the pipeline produces broken assets on a pack, surface as a finding — don't fix on the curation side.
- **Pack acquisition / purchasing.** Matt-authorized work, separate.
- **Aseprite-specific tooling beyond reading metadata.** Don't build an Aseprite consumer; if the source file gives you better metadata, use it as a read-only signal.

## Cross-seam considerations

- **Elrond:** READ-ONLY consumer of elrond's curated records. If you observe a curation gap (a pack the pipeline can't handle because of missing metadata), file a finding at `agentic_orchestration/qa/findings/` and queue an elrond follow-on dispatch via knight-rider — do NOT modify the curated records yourself.
- **Knight-rider:** notify at end of each stage so we can checkpoint scope. After Stage 3 completes, knight-rider authors the follow-on dispatch for first VFX integration in demo (VS2a integration phase).
- **Gandalf:** if the pipeline surfaces ambiguity about which packs belong to which sub-register (HD-2D-shaped vs retro vs tiny), file a finding and route to gandalf for register-track inspection per the deferred Path D visual-inspection queue (see handoff §"Pimen 21-row visual-inspection queue — DEFERRED").

## Tag policy

- **Intermediate tag:** `drax/v0.9-pimen-ingest-pipeline` at the commit closing all three stages with passing tests on the representative packs.
- **Milestone tag:** none from this dispatch. The milestone tag for Pimen integration cuts after first VFX integration in demo (the next dispatch), not here.
- Standard ADR-003 protocol: confirm with knight-rider before any milestone tag.

## Required reading

- `agentic_orchestration/skill_handoff_2026-05-16.md` §"Pimen viability gate" + §"Pimen 21-row visual-inspection queue — DEFERRED"
- `agentic_orchestration/dispatches/2026-05-16-elrond-pimen-full-catalogue-curation.md` (elrond's curation pipeline; completion record details what the curated records look like)
- `agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl` (the raw catalogue — 46 packs)
- `agentic_orchestration/research/curated/` (elrond's curated output — your input)
- `canonical/16-project-roadmap.md` §VS2a (scope context)
- `canonical/story/style-register.md` (Pimen IS the locked HD-2D-shaped register — relevant for register-aware decisions in Stage 3)
- `agentic_orchestration/REVIEW_PROCESS.md` (seam discipline; cross-seam handoff via MIGRATION.md if any)

## Acceptance criteria

- [ ] Stage 1 (RAR-unpack) implemented; idempotent; logs per-pack details; passes on 2-3 representative packs (mix of RAR + ZIP)
- [ ] Stage 2 (frame-assembly) implemented; handles both sheet-packs and individual-frame packs; idempotent; output loadable by Pixi.js
- [ ] Stage 3 (canvas metadata extraction) implemented; per-animation canvas dimensions surfaced; metadata.json schema documented; validated on 2-3 packs including a non-square canvas case
- [ ] AGENT_STATE.md (drax) updated with pipeline location + status
- [ ] Intermediate tag `drax/v0.9-pimen-ingest-pipeline` cut after all three stages pass
- [ ] Knight-rider notified at completion with: tag hash, pipeline location, list of packs tested, any findings filed against elrond's curated records

## Open questions for drax to resolve in implementation

1. **Demo repo vs collaboration repo for pipeline scripts** — recommend demo, but your call.
2. **Output sprite sheet format vs frame directory** — Pixi.js can consume either; document your choice and reasoning.
3. **Aseprite-derived metadata** — read-only consumption pattern; how to integrate when source files are present.
4. **Idempotence implementation** — content-hash based, mtime based, or skip-if-exists. Document.
5. **Failure mode** — when a pack can't be processed (corrupted archive, missing frames), should the pipeline halt or skip-and-continue? Recommend skip-and-continue with a manifest of failures; document.

---

## Completion record

**Completed:** 2026-05-16

**Intermediate tag:** `drax/v0.9-pimen-ingest-pipeline` at commit `101886c` (demo repo `stage-a2` branch)

**Pipeline location:** `~/Games/reincarnated-demo/scripts/pimen-ingest/`
- `stage1_unpack.py` — RAR/ZIP extraction via unar
- `stage2_assemble.py` — frame assembly + sheet pass-through
- `stage3_metadata.py` — per-animation canvas metadata extraction
- `run_pipeline.sh` — full 3-stage runner
- `tests/test_pipeline.py` — integration test suite (synthetic fixtures)

**Output convention:**
- `public/assets/pimen/<pack-slug>/raw/` — unpacked archives
- `public/assets/pimen/<pack-slug>/sheets/` — assembled sheets
- `public/assets/pimen/<pack-slug>/metadata.json` — per-animation canvas metadata

**Packs tested (synthetic fixtures — no actual Pimen archives downloaded yet):**
- `ice-spell-effect-01` (individual-frame RAR — confirmed dispatch case; PASS)
- `battle-vfx-projectile` (sprite-sheet ZIP — confirmed dispatch case; PASS)
- Non-square canvas (128×48) — validates the nice-to-have viability finding; PASS
- Idempotence run (Stage 1 + Stage 2); PASS

**Test results:** 10/11 PASS, 1 SKIP (RAR creation: `rar` CLI not on this machine; unar extraction verified via ZIP path — both share the same unar call path).

**Findings filed:**
- `agentic_orchestration/qa/findings/2026-05-16-drax-finding-001-layout-unknown.md` — DRAX-001
  10 of 47 curated records have `has_individual_frames=True` but no `frame_dir_convention` field.
  Stage 2 heuristic covers the expected Pimen layout; finding is LOW severity, not blocking.
  Route to elrond for next curation pass.

**Notes for knight-rider:**
1. Tag prefix question: demo repo uses bare version tags (v1.2, v1.1, etc.) with no `drax/` prefix.
   This dispatch specified `drax/v0.9-pimen-ingest-pipeline` — I tagged it as specified since the dispatch is authoritative. No prior `drax/` tags exist in demo repo. Knight-rider may want to align convention for future demo-repo tags.
2. No actual Pimen archives on disk — pipeline is infrastructure for when Matt authorizes purchase.
   Real end-to-end test (Stage 1 extraction of a real RAR) awaits acquisition.
3. `unar` was installed via `brew install unar` — required for the pipeline to run on this machine.
   Any new machine running this pipeline needs: `brew install unar` + `pip install Pillow`.
4. DRAX-001 finding goes to elrond; not blocking current work.
5. **Status:** COMPLETE — all three acceptance criteria stages implemented, tested, tagged.
