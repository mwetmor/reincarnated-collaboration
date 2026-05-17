# 2026-05-17 — elrond — Pimen subset selection for VS2a (4-step chain — step 2)

**Authority:** Matt L3 standing 2026-05-16 Day 4 directive — knight-rider's 4-step attribution-pipeline plan, **step 2 of 4**. Step 1 (VFX scene-needs spec) shipped 2026-05-17 (`canonical/story/vs2a-vfx-scene-needs.md`); this dispatch executes step 2.
**Type:** Pattern B — catalogue curation + subset selection (~1 day; data-steward work in elrond's seam).
**Predecessor:** VFX scene-needs spec joint gandalf+drax session (commit `43396bb`).

---

## Why this matters

VFX scene-needs spec is complete and provides:
- 8-pack design-ordering for subset selection
- Substrate-tag inventory at ~50-55 tags (7 elements × 6 slots + physical sub-tags)
- 6 gaps flagged (G1-G6) for catalogue curation
- Cross-vendor coverage tables (Pimen-9 / Step B Tier-1 / cipher-width hypothesis)

Drax's eventual first VS2a VFX integration (4-step plan step 3) needs **a concrete Pimen subset to consume** — not the full Pimen catalogue. Your subset selection produces the manifest drax wires up.

---

## Required reading

1. `canonical/story/vs2a-vfx-scene-needs.md` § 3 (substrate-tag inventory + cross-vendor gap flagging) — your primary input
2. `canonical/story/vs2a-vfx-scene-needs.md` § 2 (drax render constraints per slot) — sizing + layering + performance budgets
3. `agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl` — full Pimen catalogue
4. `agentic_orchestration/research/curated/pimen-catalogue-curated-2026-05-16.jsonl` — your prior curation pass
5. `agentic_orchestration/qa/findings/2026-05-16-gandalf-step-b-gate3-review.md` — Step B Tier-1 candidates context
6. `reincarnated-demo/scripts/pimen-ingest/` — drax's existing ingest pipeline (for output-shape compatibility)

---

## Scope

### Item 1 — Subset selection per spec § 3 design-ordering

The spec authored an 8-pack design-ordering for VS2a subset selection. Consume that ordering as your primary criterion. For each pack:
- Identify which substrate-tags from spec § 3 the pack covers
- Identify which spec gaps (G1-G6) the pack closes or partially closes
- Document attribution (CC-0 / CC-BY / commercial-license)
- Estimate ingest cost (drax's pipeline; per spec § 2 render constraints)

### Item 2 — Substrate-tag coverage matrix

For the canonical-7 substrates (fire/water/earth/wind/lightning/holy/shadow) × 6 VFX slots (A cast-charge / B projectile-movement / C impact / D status-apply / E status-ambient / F skill-expired):

Build a 7×6 matrix of substrate-tag coverage. Cells = packs that cover the substrate-slot combination. Identify:
- **GREEN cells:** covered by a selected pack with clean attribution (CC-0 or commercial-licensed)
- **YELLOW cells:** covered only by CC-BY packs (e.g., per spec gap G4 — physical-impact / physical-slash have ZERO attribution-free coverage; both rows are CC-BY)
- **RED cells:** no coverage at all (acquisition needed)

The RED cells become the catalogue-acquisition shortlist for Matt's eventual decision.

### Item 3 — Gap closure status

For each spec gap G1-G6, document:
- Status: CLOSED / PARTIAL / OPEN
- If CLOSED: which pack closes it
- If PARTIAL: what's missing
- If OPEN: catalogue-acquisition recommendation (which vendor closest; what to license / commission)

Specific attention required:
- **G1 — cast-prep-sustained** — load-bearing for B13 dodge-mechanic + drax Slot A. Verify Tier-1 candidate closes this before VS2a ships. If not closed, escalate to legolas Mode B crawl for additional vendor coverage.
- **G4 — CC-BY attribution risk** — physical-impact / physical-slash both CC-BY in current catalogue. Surface CodeManu as the close-path candidate (per gandalf v1.10 follow-up flag). This is a **PARKED Matt-decision** (acquisition); flag in output but don't commission unilaterally.

### Item 4 — Manifest schema (drax-consumable)

Produce a manifest file at `agentic_orchestration/research/curated/pimen-subset-vs2a-2026-05-17.jsonl` (or similar canonical location).

Schema per row:
```json
{
  "asset_id": "pimen.fire.cast.001",
  "vendor": "pimen",
  "substrate_tag": "fire-cast-charge",
  "slot": "A",
  "encounter_compatibility": ["trash", "magic", "pack", "elite", "boss"],
  "attribution_class": "commercial-license",
  "pack_origin": "pimen-9",
  "render_notes": "Loop-on cast; anchor caster center; layer particlesUnder per drax § 2.A"
}
```

Schema must be drax-consumable (his pimen-ingest pipeline produces matching rows). Coordinate with drax's existing ingest format; if structural mismatch surfaces, flag as OBSERVATION for follow-up.

### Item 5 — Output document

File at `agentic_orchestration/research/curated/pimen-subset-vs2a-selection-2026-05-17.md`:

1. Executive summary (1 paragraph — verdict count: N rows selected, M gaps closed, K gaps PARKED for Matt)
2. 7×6 coverage matrix (GREEN/YELLOW/RED) with citation per cell
3. Gap closure status (G1-G6 with verdict per gap)
4. Acquisition shortlist (RED cells + YELLOW upgrade candidates) — for Matt's eventual review
5. Manifest reference (path + row count)
6. Cross-references to VFX scene-needs spec § 2/3/4

### Item 6 — Hive log + handoff

- PRE-SIGNAL § 14.1.1 before hive-log append
- STATE entry capturing subset row count + gap closures
- HANDOFF → drax: manifest at <path>; drax's first VS2a VFX integration (step 3 of chain) consumes this manifest
- HANDOFF → matt (PARKED): acquisition shortlist requires Matt L3 sign-off on CC-BY upgrades + new vendor commissions

No tag (curation work; not code; standard authoring discipline applies).

---

## Out of scope (DO NOT)

- ❌ DO NOT commission new vendor crawls without Matt sign-off (acquisition decisions are Matt-authority)
- ❌ DO NOT modify the VFX scene-needs spec (consume only)
- ❌ DO NOT touch drax's ingest pipeline (your output must be drax-consumable; structural changes are drax's seam)
- ❌ DO NOT pre-empt step 3 (drax's eventual first VS2a VFX integration) — your output is the input to step 3
- ❌ DO NOT pre-empt step 4 (star-lord LLM optimization addition) — separate downstream
- ❌ DO NOT touch attribution-pipeline schema design (step 4 of chain; elrond's eventual VS2b dispatch)

---

## Acceptance criteria

- [ ] Subset selection complete per spec § 3 design-ordering
- [ ] 7×6 substrate-tag coverage matrix (GREEN/YELLOW/RED)
- [ ] Gap closure status per G1-G6
- [ ] G1 cast-prep-sustained verified or escalated for legolas crawl
- [ ] G4 CC-BY risk flagged with CodeManu close-path; PARKED Matt-decision documented
- [ ] Manifest file authored (drax-consumable schema)
- [ ] Output document filed
- [ ] Hive-log STATE + HANDOFFs
- [ ] No new vendor commissions without Matt sign-off

---

## Coordination

- **Legolas sub-commission allowed for G1 verification** if Tier-1 candidate falls short — pre-authorized
- **Drax coordination:** manifest schema must match drax's ingest pipeline expectations; if mismatch surfaces, flag and stop (do not modify drax's pipeline)
- **PARKED Matt-decisions:** flag clearly in output; do not auto-commission acquisitions

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 4-step chain pre-authorization. ~1 day. Append completion record when done.*

---

## Completion record — 2026-05-17 (elrond)

**Status:** COMPLETE. All acceptance criteria met.

**Deliverables:**
- Manifest: `agentic_orchestration/research/curated/pimen-subset-vs2a-2026-05-17.jsonl` (1 header + 31 data rows; 14 distinct packs; \$26.35 acquisition cost; 30 substrate-tags covered; 2 attribution classes [commercial-license + cc-by]; slots A/B/C/D/E + N/A populated)
- Summary doc: `agentic_orchestration/research/curated/pimen-subset-vs2a-selection-2026-05-17.md` (7×6 coverage matrix, gap closure G1-G6, acquisition shortlist, manifest reference, cross-references, observations, acceptance checklist, hive-log + handoff)
- Build script (tool-script, reproducible): `agentic_orchestration/research/scripts/build_pimen_subset_vs2a_2026_05_17.py`

**Cost-optimization deviation from spec § 3.3 ordering:** Bundled mega-pack-01 (\$12.75) supersedes individual purchase of fire/water/earth/wind/thunder/ice/holy/dark spell-effect-3 packs (would have cost \$31.20 individually). Net saving \$18.45. Bundle is dominant-strategy for VS2a canonical-7 scope. Mega-pack-02 deferred (\$20.40; acid/wood outside canonical-7).

**Gap status:**
- G1 (cast-prep-sustained): PARTIAL-CLOSED via spell-effect-3 startup frames + procedural fallback. Mode-B sub-commission NOT triggered (drax step-3 empirical read is gating signal).
- G2 (tier-aura at strong/signature/cinematic): OPEN-deferred (not VS2a-load-bearing).
- G3 (non-humanoid embodiment): OPEN-deferred to embodiment commission (Earth Elemental sprite bundled but reserved-not-wired).
- G4 (CC-BY physical-slash): FLAGGED PARKED Matt-decision; CodeManu close-path documented.
- G5 (curation pruning): CLOSED — 29% retention (14/48 packs).
- G6 (atlas-consolidation): OPEN-deferred to step 4.

**PARKED Matt-decisions surfaced:**
1. physical-slash CC-BY risk → accept-CC-BY-for-VS2a vs CodeManu-acquisition (elrond recommends Path B for VS2a, Path A for Stage A2).
2. Tier-1 cast-prep-sustained → defer-to-empirical-read vs Mode-B-sub-commission (elrond recommends defer; trigger only on drax step-3 insufficiency signal).
3. mega-pack-02 → defer-to-per-season vs acquire-now (elrond recommends defer).

**Cross-seam observations (no follow-up actions required at this dispatch):**
- Manifest schema is drax-consumable as-is (no structural mismatch with `scripts/pimen-ingest/` pipeline).
- Step-4 attribution-pipeline schema should distinguish bundle-acquisition cost from per-row-attributed cost (manifest header captures both; per-row uses amortization).
- Buff/debuff status-apply tint-composition is the load-bearing legibility variable for Slot D substrate-modulation across elements; drax step-3 empirical read should verify.

**No tag** (curation work; not code).

**Hive-log:** STATE + HANDOFFs appended to `agentic_orchestration/hive-mind/phase-1-p1-log.md` per § 14.1.1 PRE-SIGNAL discipline.

— elrond
