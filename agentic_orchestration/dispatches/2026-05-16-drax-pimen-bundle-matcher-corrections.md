# Dispatch — 2026-05-16 — drax — Pimen bundle-pipeline matcher corrections (post-elrond bundle follow-up)

**From:** knight-rider (authored per elrond bundle-follow-up findings + Matt 2026-05-16 Day 4 directive: "fire drax bundle matcher fix")
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4
**Status:** PENDING — HOLD-on-prior. Do NOT execute until your in-flight B11 demo integration dispatch (`drax/v0.15-b11-demo-integration` work) completes; drax can only run one dispatch per session (per-seam AGENT_STATE.md sharing).
**Estimated effort:** 1-2 sessions (~3-5h); surgical matcher fixes + tests + idempotency re-run.
**Acceptance:** Two matcher-pattern fixes landed in `scripts/pimen-ingest/stage1_unpack.py`; re-run on Matt's existing mega-pack archives shows correct sub-pack identification (no false-out-of-band on explosion-effect; no slug-collision skip on Earth Spell 03); MIGRATION.md / completion notes updated; tag.

---

## Context — what elrond's bundle follow-up surfaced

Per elrond bundle-follow-up dispatch completion 2026-05-16 (tag `elrond/v1.1-bundle-follow-up-and-register-mixed-flag`; findings at `agentic_orchestration/research/curated/pimen-bundle-follow-up-2026-05-16.md`):

Your prior bundle-extension dispatch (`drax/v0.13-pimen-pipeline-bundle-archive-support @ 04ef825`) made **two correct surfaces** that turned out to be matcher misidentifications when elrond cross-verified against catalogue:

### Misidentification 1 — "30 out-of-band explosion VFX packs"

Your matcher reported: 30 numbered `Explosion VFX N/` folders inside `Explosion VFX.rar` are out-of-band (no curated slug match).

**Elrond verification**: those 30 folders ARE the **30 constituent animations** of the already-curated `explosion-effect` pack. Cross-verified: catalogue `animations_count=30` matches; frame-count-notes enumerate VFX1-30 with matching canvas sizes; `lsar` listing matches frame-by-frame.

**Pattern**: `subpack-organization-style: per-animation-subfolders` — some Pimen packs ship as a single archive with per-animation subfolders inside. The matcher needs to recognize this pattern: if archive's inner folders count matches a curated pack's animations_count + animation names match, treat the archive AS the pack (not as a bundle).

### Misidentification 2 — Slug collision (Earth Spell 03 vs Earth Effect 03)

Your matcher reported: `Earth Spell 03` and `Earth Effect 03` both fuzzy-match `earth-spell-effect-03`; first wins (Earth Effect 03), second skipped (Earth Spell 03 = `skip_slug_collision`).

**Elrond verification**: both folders are the SAME pack delivered in two formats inside the bundle:
- `Earth Spell 03` = full content (frames + spritesheets; canonical)
- `Earth Effect 03` = compact spritesheet-only variant

**Resolution**: elrond amended the curated rows with `bundle_folder_hint` overlay (priority-ordered list `["Earth Spell 03", "Earth Effect 03"]`) + queryable `bundle-folder-hint:*` tags. Your matcher should consume the new `bundle_folder_hint` field to prefer the canonical folder (Earth Spell 03) when both are present.

## What this dispatch does

### Step 1 — Per-animation-subfolders detection

In `~/Games/reincarnated-demo/scripts/pimen-ingest/stage1_unpack.py`:

Add a detection step BEFORE bundle-folder iteration:
1. Read curated catalogue for the target archive (if any pack's `bundle_folder_hint` references this archive)
2. Compare archive's inner-folder count to the curated pack's `animations_count`
3. If counts match AND inner folder names match `animation_names` pattern (e.g., `Explosion VFX 1`, `Explosion VFX 2`, ..., `Explosion VFX 30`), treat the archive AS THE PACK (not as a bundle of sub-packs)
4. Unpack as single-pack to `<pack-slug>/raw/` (existing single-pack path)

### Step 2 — bundle_folder_hint consumption

Update `match_folder_to_slug()` (or equivalent matcher):
1. NEW Priority 0 (highest): if a curated record has `bundle_folder_hint` set and the bundle inner folder matches one of the hinted names, route to that curated slug
2. Within `bundle_folder_hint` list: priority is left-to-right (first hint preferred)
3. Existing Priority 1-4 logic preserved as fallback

### Step 3 — Re-run on Matt's existing mega-pack archives

After matcher updates:
1. Re-run `./run_pipeline.sh --archive-dir ~/Games/reincarnated-demo/public/assets/pimen/`
2. Verify:
   - `Explosion VFX.rar` now unpacks correctly as `explosion-effect` single-pack (NOT 30 out-of-band)
   - `Earth Spell 03` (canonical) preferred over `Earth Effect 03` (variant) per bundle_folder_hint
   - All other prior matches preserved (idempotent re-run)
3. metadata.json files for explosion-effect now real Stage 3 output (replacing whatever stub state exists; previously 5/5 sub-packs were UNPACKED but listed as out-of-band)

### Step 4 — Tests + smoke

- Update `tests/test_pipeline.py` for the new matcher logic (per-animation-subfolders detection; bundle_folder_hint Priority 0)
- Existing 17/18 + 7 bundle tests still pass
- Smoke verify on Matt's existing archives

### Step 5 — Findings + completion

- Update `~/Games/reincarnated-demo/scripts/pimen-ingest/PIMEN_BUNDLE_MATCHER_NOTES.md` (or equivalent) documenting the two pattern fixes
- Tag `drax/v0.16-pimen-bundle-matcher-corrections`
- AGENT_STATE.md updated
- Completion report to knight-rider

## Cross-seam considerations

- **Elrond** (READ-ONLY upstream): elrond's `bundle_folder_hint` overlay + matcher-correction tags are your input substrate; do NOT modify elrond catalogue files
- **Knight-rider**: notify at completion; closes the bundle-pipeline misidentification loop from prior Day 4 work

## Out of scope (explicit)

- **NO new ELEMENT_SLOT_MAP changes** — your v0.14 mapping landed; this dispatch is matcher only
- **NO new Pimen pack curation** — elrond's job; if matcher reveals new out-of-band candidates, file finding
- **NO bundle-folder-hint or subpack-organization-style as first-class fields** — that's elrond's MIGRATION.md v1.4 open follow-on #2 (separate elrond dispatch later)
- **NO room/hallway changes**
- **NO new VFX integration work beyond verifying explosion-effect now serves real assets**
- **NO B11 demo integration changes** — separate prior dispatch (`drax/v0.15-b11-demo-integration` in flight)
- **NO character-track ingest pipeline** — separate future dispatch

## Required reading

- `agentic_orchestration/research/curated/pimen-bundle-follow-up-2026-05-16.md` (elrond findings; PRIMARY source)
- `agentic_orchestration/research/curated/pimen-catalogue-curated-2026-05-16.jsonl` (amended rows with bundle_folder_hint + matcher-correction tags)
- Your prior bundle-extension dispatch + completion record (`drax/v0.13-pimen-pipeline-bundle-archive-support @ 04ef825`)
- Your prior ELEMENT_SLOT_MAP fix dispatch + completion record (`drax/v0.14-pimen-element-slot-map-real-mapping @ 7fba617`) — explosion-effect rendering may need ELEMENT_SLOT_MAP entry if not already present
- `~/Games/reincarnated-demo/scripts/pimen-ingest/stage1_unpack.py` (target file for matcher updates)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #2 (smoke); #10 (empirical inspection over assumption — this dispatch IS the empirical correction)

## Acceptance criteria

- [ ] Per-animation-subfolders detection implemented (Stage 1)
- [ ] `bundle_folder_hint` consumption in matcher (Priority 0)
- [ ] Re-run on Matt's existing archives shows correct identification
- [ ] explosion-effect unpacks as single-pack (NOT 30 out-of-band)
- [ ] Earth Spell 03 preferred over Earth Effect 03 per bundle_folder_hint
- [ ] All other prior matches preserved
- [ ] Existing tests pass + new matcher tests pass
- [ ] PIMEN_BUNDLE_MATCHER_NOTES.md updated
- [ ] Intermediate tag `drax/v0.16-pimen-bundle-matcher-corrections` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

## Tag policy

- **Intermediate tag:** `drax/v0.16-pimen-bundle-matcher-corrections` at the commit closing matcher fixes + smoke pass.

---

## Completion record

**Completed:** 2026-05-16
**Intermediate tag:** `drax/v0.16-pimen-bundle-matcher-corrections` @ `447e11d`
**Commits:** `447e11d` (matcher corrections + tests + PIMEN_BUNDLE_MATCHER_NOTES.md + pipeline re-run output), `1483eaf` (AGENT_STATE.md)

**Per-animation-subfolders pattern handling:**
- Added `detect_per_animation_subfolders()` in `stage1_unpack.py` — checks elrond-curated tag
  `subpack-organization-style:per-animation-subfolders` + `animations_count` match before
  sub-pack iteration loop.
- Added helpers: `get_animations_count()`, `has_per_animation_subfolders_tag()`.
- When detected: archive is unpacked as a single pack to `<slug>/raw/` (standard single-pack path).
  Idempotence uses archive SHA256 directly (not composite hash).
- Verification on Explosion VFX.rar: "Per-animation-subfolders detected: 30 folders match
  animations_count=30 for curated slug 'explosion-effect'". 86 files, 360KB unpacked correctly.
  Second run: `skip_idempotent` (correct).

**bundle_folder_hint consumption:**
- Added `get_bundle_folder_hints()` helper to extract `bundle_folder_hint` list from
  `_amendment_2026_05_16_bundle_folder_hint` overlay.
- `match_folder_to_slug()` Priority 0: scans all records for hints, returns slug for first
  hint-normalised match (canonical-first per hint list index).
- `process_bundle_archive()` collision resolution updated to be hint-aware: added
  `_hint_index_for_folder()` inner function; lower hint_index wins over first-seen ordering.
- Verification on Elemental Effects.rar: "bundle_folder_hint prefers 'Earth Spell 03'
  (hint_index=0) over 'Earth Effect 03' (hint_index=1); skipping 'Earth Effect 03'".
  `earth-spell-effect-03/raw/` re-extracted from canonical "Earth Spell 03" folder (16 files, 61KB).

**Re-run verification:**
- `Explosion VFX.rar`: explosion-effect single-pack (86 files). No out-of-band sub-packs.
- `Elemental Effects.rar`: Earth Spell 03 canonical; Earth Effect 03 skip_slug_collision
  "(resolved via bundle_folder_hint)". Fire/water/wind/thunder: skip_idempotent. Icons: skip_idempotent.
- All other prior matches preserved.
- Stage 2+3 re-ran on earth-spell-effect-03 (re-extracted from canonical folder).
- Test results: 23/24 PASS, 1 SKIP, 0 FAIL. 6 new v0.16 matcher tests added.

**Note on Earth Spell 03 format (spritesheet-only vs full-content):**
Elrond finding: "Earth Spell 03" is spritesheet-only; "Earth Effect 03" has frames + spritesheets.
The hint canonical is "Earth Spell 03" per product page naming. The Separated Frames are now
absent from `earth-spell-effect-03/raw/`. The ELEMENT_SLOT_MAP animName "Earth Hit Effect 1 (32x32)"
exists as a spritesheet in both formats — no pimenVfx.ts changes needed.

**PIMEN_BUNDLE_MATCHER_NOTES.md:** Created at `scripts/pimen-ingest/PIMEN_BUNDLE_MATCHER_NOTES.md`
documenting both pattern fixes, matching priority table, log interpretation guide, and forward-queued items.

**Notes for knight-rider:**
- Both misidentifications from drax/v0.13 are now corrected. Bundle pipeline is stable.
- explosion-effect/raw/ now populated with real Pimen content (86 files). Subset selection for
  first VFX integration is a consumption-time decision (drax picks animations from the 30 available).
- earth-spell-effect-03/raw/ now uses canonical "Earth Spell 03" spritesheet-only format.
  The full-content "Earth Effect 03" folder (with Separated Frames) is the fallback — available
  if frame-by-frame inspection is needed in a future dispatch.
- earth-spell-effect-03::enemy-elemental: enemy character content at `Extra - Earth Elemental/`
  within the canonical folder; accessible via elrond's `earth_elemental_subpath` field when needed.
- mega-pack-elemental-icons: 10 icon PNGs now extracted (from prior pipeline run). Available for
  VS2a/VS2b UI element-affinity display when needed.
- Open forward item: `bundle_folder_hint` and `subpack_organization_style` as first-class
  curation-time fields (MIGRATION.md v1.4 open follow-on #2) — elrond item, not drax.
