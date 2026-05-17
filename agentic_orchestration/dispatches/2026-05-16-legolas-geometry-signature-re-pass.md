# Dispatch — 2026-05-16 — legolas — Geometry-signature re-pass (all 9 Tier-1 vendors; per gandalf geometry-coverage commission Tracks 1+2)

**From:** knight-rider (authored per gandalf 2026-05-16 geometry-VFX-coverage-investigation commission `agentic_orchestration/gandalf/requests/2026-05-16-geometry-vfx-coverage-investigation-b11-gating.md` Tracks 1+2 consolidated; Drift-11 noted)
**To:** legolas (Mode B; focused re-pass)
**Approved by:** Matt at 2026-05-16 Day 4 explicit batch directive ("author geometry dispatches")
**Status:** PENDING — ACTIVE
**Estimated effort:** ~1-2 Mode B sessions (~3-6h); focused geometry-signature classification pass against the 9 already-crawled Tier-1 vendor catalogues (Pimen + 8 from Step B). Per gandalf: marginal effort vs re-crawling later.
**Acceptance:** Per-vendor sidecar files at `agentic_orchestration/research/catalogue/<vendor-slug>/geometry-signatures-2026-05-XX.jsonl` (keyed by `asset_id`) covering all 9 Tier-1 vendors. Each row contains `geometry_signatures: [...]` array per pack's animations. Per-vendor coverage report capturing geometry-classification confidence + any `geometry_uncertain` flags.

---

## Context — what gandalf caught

Per gandalf's 2026-05-16 geometry-VFX-coverage-investigation commission + Drift-11 entry just filed in `canonical/story/drift-audit.md`:

The Step B Tier-1 crawl (completed 2026-05-16; 9 vendors / 54 packs / 28 substrate rows / 17 novel substrate tags) **did not extract geometry signatures** — only element / mechanic / register / etc. Per gandalf's catch, the **geometry × element coverage** is a load-bearing dimension for B11 (Geometry palette expansion 16 → 25 active types) demo integration. Without geometry-signature data per pack, the elrond rubric (Track 3 — separate dispatch) cannot build the geometry × element coverage matrix that gandalf's gap-severity assessment (Track 4) depends on.

**Drift-11 pattern:** scoped-work-missed-a-load-bearing-dimension. Two instances today (movement-speed catch earlier; geometry-VFX catch now). Filed for future scope-authoring discipline.

**Critical path:** this re-pass + Track 3 elrond rubric + Track 4 gandalf assessment fits within current 3-4 week B11 window if started immediately. B11 engine + sim phases (rocket + gamora) can proceed in parallel; B11 drax demo integration is HELD pending Track 4 gap-severity assessment.

**Why consolidate Tracks 1+2 into a single dispatch:** Track 1 (Step B amendment for geometry_signatures extraction) and Track 2 (Pimen re-crawl) per gandalf's commission framing are both geometry-signature extraction work. Step B already shipped; the "amendment + re-crawl" framing collapses to "focused re-pass over the already-crawled 9 vendors." Single dispatch is cleaner than 9 separate per-vendor passes.

## What this dispatch produces

A per-vendor sidecar at `agentic_orchestration/research/catalogue/<vendor-slug>/geometry-signatures-2026-05-16.jsonl` for each of the 9 Tier-1 vendors:

| Vendor | Existing catalogue | New sidecar |
|---|---|---|
| Pimen | `pimen/full-2026-05-16.jsonl` (47 packs) | `pimen/geometry-signatures-2026-05-16.jsonl` |
| ansimuz | `ansimuz/full-2026-05-16.jsonl` (6 packs) | `ansimuz/geometry-signatures-2026-05-16.jsonl` |
| Brackeys VFX Bundle | `brackeys/full-2026-05-16.jsonl` (1 pack) | `brackeys/geometry-signatures-2026-05-16.jsonl` |
| CraftPix | `craftpix/full-2026-05-16.jsonl` (7 packs) | `craftpix/geometry-signatures-2026-05-16.jsonl` |
| CreativeKind | `creativekind/full-2026-05-16.jsonl` (8 packs) | `creativekind/geometry-signatures-2026-05-16.jsonl` |
| Frostwindz | `frostwindz/full-2026-05-16.jsonl` (15 packs) | `frostwindz/geometry-signatures-2026-05-16.jsonl` |
| Pixogen | `pixogen/full-2026-05-16.jsonl` (2 packs) | `pixogen/geometry-signatures-2026-05-16.jsonl` |
| CodeManu | `codemanu/full-2026-05-16.jsonl` (3 packs) | `codemanu/geometry-signatures-2026-05-16.jsonl` |
| Fellor | `fellor/full-2026-05-16.jsonl` (7 packs) | `fellor/geometry-signatures-2026-05-16.jsonl` |
| Pipoya | `pipoya/full-2026-05-16.jsonl` (5 packs) | `pipoya/geometry-signatures-2026-05-16.jsonl` |

**Existing JSONL files stay unchanged** — sidecar pattern preserves Step B output integrity per read-only discipline.

## Geometry-signature vocabulary (per gandalf commission line 69)

For each animation in each pack, classify against the 30-target vocabulary (current 16 + B11's 9 + B13's 5 per `canonical/09-geometry-palette-discussion.md`):

**Current 16 (per canonical/09-geometry-palette-discussion.md baseline):**
- `impact_burst`, `projectile_straight`, `projectile_arcing`, `projectile_homing`
- `beam_channel`, `cone`, `ground_slam_circular`, `ground_slam_directional`
- `aura_radial`, `aura_directional`, `nova_radial`, `nova_wave`
- `chain`, `ring`, `whirlwind`, `dash_attack`

**B11's 9 additions** (per roadmap §VS2a B11 16→25 active types expansion):
- `leap_strike`, `vortex_pull`, `summon`, `buff_self`, `debuff_target`
- `melee_strike`, `melee_arc`, `melee_thrust`, `melee_cleave` (or per the specific 9 in canonical/09)

**B13's 5 additions** (per roadmap §VS2a B13 active mobility extension):
- `dodge_roll`, `blink_teleport`, `parry_active`, `block_active`, `iframe_dash` (or per the specific 5 in canonical/09)

**Per pack:** the `geometry_signatures` array lists all geometry-classifications evident in the pack's animations.

**For uncertain classifications:** tag `geometry_uncertain` with brief notes explaining the ambiguity. Don't force a classification when the animation doesn't cleanly fit.

## Per-vendor methodology

For each of the 9 vendor catalogues:

### Step 1 — Pack-by-pack geometry-signature classification

For each pack in the vendor's existing JSONL:
1. Read pack metadata (animation list, file format, register, etc.)
2. For each named animation in the pack, classify against the 30-target vocabulary
3. Build the `geometry_signatures` array as the union of unique classifications across the pack's animations
4. If any animation classification is uncertain, tag `geometry_uncertain` with notes

### Step 2 — Per-vendor coverage report

Surface in a brief `findings-summary-geometry-2026-05-16.md` (or append to the existing per-vendor findings file):
- Per-geometry-type coverage count for this vendor
- Per-vendor geometry-specialty observation (e.g., "CodeManu is kinetic-VFX specialist; high coverage on melee_strike + impact_burst + dash_attack")
- Any `geometry_uncertain` patterns warranting elrond rubric attention

### Step 3 — Sidecar JSONL output

File at `agentic_orchestration/research/catalogue/<vendor-slug>/geometry-signatures-2026-05-16.jsonl`.

Schema per row:
```json
{
  "asset_id": "<pack-id>",
  "vendor": "<vendor-slug>",
  "geometry_signatures": ["impact_burst", "projectile_straight", "aura_radial"],
  "geometry_uncertain": [],
  "notes": "<optional brief observation>"
}
```

## Pimen-specific note

Pimen is the most-covered vendor (47 packs); allocate proportionally more time to Pimen's pass (~2-3h vs ~30-60min for smaller vendors). Pimen's geometry breadth is foundational — gandalf's gap-severity assessment will reference Pimen as the baseline.

## Cross-seam considerations

- **Gandalf:** primary downstream consumer of the per-vendor coverage reports. Gandalf's Track 4 gap-severity assessment operates on elrond's Track 3 rubric output (which consumes YOUR sidecar files).
- **Elrond:** primary downstream consumer of the sidecar JSONL files. Elrond's Track 3 rubric dispatch (separately authored at `dispatches/2026-05-16-elrond-geometry-element-coverage-rubric.md`) builds the geometry × element coverage matrix against your output.
- **Knight-rider:** notify at completion. Once both this dispatch AND elrond's rubric dispatch complete, gandalf's Track 4 gap-severity assessment can fire.
- **Rocket / gamora:** READ-ONLY at this layer; their B11 engine + sim phases proceed in parallel without dependency on this dispatch.
- **Drax:** their B11 demo integration is HELD pending gandalf's Track 4 gap-severity assessment (which depends on this dispatch + elrond's rubric).

## Out of scope (explicit)

- **NO new vendor crawls.** Only re-pass against existing 9 Tier-1 vendor catalogues from Step B.
- **NO modifications to existing per-vendor JSONL files.** Read-only; sidecar pattern preserves Step B output integrity.
- **NO geometry-coverage matrix construction.** That's elrond's Track 3 dispatch.
- **NO gap-severity assessment.** That's gandalf's Track 4.
- **NO B11 dispatch authoring or roadmap-amendment work.** Knight-rider coordinates per-Track completion routing.
- **NO geometry-vocabulary extension beyond gandalf's 30-target list.** If you observe geometry types that don't fit the 30 targets, tag `geometry_uncertain` with notes; do NOT introduce new vocabulary terms.

## Required reading

- `agentic_orchestration/gandalf/requests/2026-05-16-geometry-vfx-coverage-investigation-b11-gating.md` (the commission; Tracks 1+2 your scope)
- `canonical/09-geometry-palette-discussion.md` (geometry vocabulary source-of-truth)
- `canonical/story/drift-audit.md` Drift-11 entry (gandalf filed; pattern context)
- 9 vendor catalogues at `agentic_orchestration/research/catalogue/<vendor>/full-2026-05-16.jsonl` (your inputs)
- `agentic_orchestration/qa/findings/2026-05-16-gandalf-step-b-gate3-review.md` (gate-3 review context; per-vendor verdicts)
- `agentic_orchestration/research/curated/post-step-b-cleanup-2026-05-16.md` (elrond's catalogue cleanup; 4 flag adjudications applied)
- `agentic_orchestration/AGENTS.md` § Legolas Mode B (crawl methodology)

## Acceptance criteria

- [ ] All 9 vendor sidecar JSONL files created at `research/catalogue/<vendor>/geometry-signatures-2026-05-16.jsonl`
- [ ] Per-vendor coverage reports filed
- [ ] Geometry classifications use only the 30-target vocabulary from `canonical/09-geometry-palette-discussion.md`
- [ ] Uncertain classifications tagged `geometry_uncertain` with notes
- [ ] Pimen given proportionally more time (47 packs; foundational baseline)
- [ ] No modifications to existing per-vendor JSONL files (sidecar pattern only)
- [ ] Knight-rider notified at completion; elrond rubric dispatch unblocks

## Tag policy

No tag (analytical/research output; not a code change).

---

## Completion record

(To be filled in by legolas on completion)

**Completed:**
**Total assets classified:**
**Per-vendor sidecar paths:**
**Geometry-uncertain count:**
**Notable per-vendor geometry-specialties:**
**Notes for knight-rider:**
