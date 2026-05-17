# Dispatch — 2026-05-16 — gandalf + drax (joint) — VFX scene-needs spec (VS2a attribution-pipeline upstream input)

**From:** knight-rider (authored per Matt's 2026-05-16 Day 4 directive; sequencing the upcoming attribution-pipeline work)
**To:** **gandalf** (primary — design framing + style register + per-encounter VFX-slot enumeration) AND **drax** (secondary — pipeline/render constraints + per-slot consumption requirements)
**Approved by:** Matt L3 2026-05-17 (~19:30 EDT) — all 3 micro-decisions resolved; dispatch ACTIVATED for joint gandalf+drax authoring session.
**Status:** 🟢 **ACTIVE — execute now.** All 3 placeholders hard-locked per § "Micro-decision placeholders (RESOLVED)" below.
**Estimated effort:** 1 joint session (~3-5 hours); design + render-constraint analysis. NOT a long sequence.
**Acceptance:** A VS2a-targeted VFX scene-needs spec document filed at `canonical/story/vs2a-vfx-scene-needs.md` (or equivalent) capturing per-encounter-type VFX slot enumeration at substrate-level (gandalf design framing + drax render constraints). Spec serves as the primary input to elrond's eventual VS2b attribution-pipeline schema dispatch.

---

## Context — why this dispatch exists

Per knight-rider's 4-step attribution-pipeline plan (orchestration log answer 2026-05-16 Day 4) AND Matt's commission of this question:

**Step 1 of 4 = THIS DISPATCH.** Commission the VFX scene-needs spec FIRST so that:
- Elrond can do Pimen subset selection (currently blocked on knowing which VFX slots VS2a actually needs)
- Drax's eventual first VFX integration (VS2a critical path) has a clear target asset list
- Gaps surface early ("we need a Plasma effect but Pimen has fire + lightning separately; do we crawl another vendor or commission?")
- The eventual VS2b attribution-pipeline schema has empirical scope to design against

Per the form-bias 5-entry batch (committed `5d51b5a`) + ailment-deferral entry (committed `680a3f1`) + the cadence Option II lock + the strategic-axis lock, **the spec can be authored at substrate level WITHOUT waiting on cipher-width / Foundation-layer / D1 / per-season-vocabulary sub-locks** (all four are downstream-independent at substrate granularity).

But three micro-decisions tighten the spec's VS2a-substrate scope and benefit from gandalf input. Those decisions live in the open-thread referenced above. Once they converge, this dispatch activates; placeholders below flip to hard locks.

## Micro-decision placeholders (RESOLVED 2026-05-17)

**Sub-decision A (element vocabulary at player-facing surface): LOCKED — HYBRID a3.**

Per gandalf v1.10 advisory (`gandalf/v1.10-vfx-sub-decision-a-consult-1 @ 20e1adc`):
- **Canonical-7 substrate vocabulary** at combat-text surface (damage numbers, status effects, hotbar tooltips, combat log, stats block) — fire/water/earth/wind/lightning/holy/shadow (canonical-7 shipped 2026-05-17 via Phase-1 P1 D20)
- **Per-season vocabulary** at flavor-text / lore / NPC dialog / quest-description surfaces only
- **BINDING AUTHORING RULE — REGISTER-FENCE PER UI SURFACE BLOCK:**
  > Within any single UI surface block, exactly one vocabulary register appears. Stats block = canonical-7 only. Flavor-text block = per-season vocabulary only (NEVER the canonical-7 substrate words). Item-label block = season-authored derived label (may echo per-season theme, never mixes canonical-7 substrate words). Skill-name block = canonical-7-derived for VS2a; per-season-derived deferred to Stage 3 (VS2b).

The register-fence rule is **load-bearing for ALL VS2a+ content regardless of cipher migration timing** and should be lifted into the spec itself as a top-level authoring discipline (not just buried in this Sub-A resolution).

**Sub-decision B (embodiment scope): LOCKED — mix-mode (humanoid fixed + non-humanoid allowed at generation; curation selects).**

Per Matt L3 2026-05-17:
- Engine generation infrastructure supports both humanoid AND non-humanoid embodiments at season creation
- ~75% expected generative-season failure rate (Matt-locked design constant; jack-ryan decisions-log entry queued)
- Curation step selects which generated seasons ship to playtest
- Frame: "this IS a feature of the design, NOT a bug/failure" — non-humanoid generation that doesn't ship is *expected*, not waste

**Implication for spec scope:** Section 1 (encounter-type inventory) covers BOTH humanoid and non-humanoid embodiments per encounter type. Section 4 (per-embodiment narrative-skin rendering, if applicable) covers expected non-humanoid embodiments (Slime / Spider / Dragon-Hatchling subset at minimum) as forward-looking content.

**Sub-decision C (spec deliverable scope): LOCKED — Option II (VS2a + VS2b forward-looking).**

Per Matt L3 2026-05-17, justified by:
- 7-substrate scope (canonical-7 shipped today + per-season vocabulary at flavor)
- Non-humanoid embodiment generation enabled (Sub-B mix-mode)
- Spec authoring must anticipate cipher-width-expanded substrate + per-embodiment narrative-skin renaming hooks + Stage 4 amendment-trigger placeholders

**Spec output target:** ~80-120 lines per scene type with both VS2a-locked + VS2b-forward-looking content. Section 4 (per-encounter scene-walkthroughs) is INCLUDED per Option II.

## Strategic-axis context (load-bearing — applies regardless of micro-decisions)

Per the 2026-05-16 form-bias 5-entry batch + the cadence Option II lock:

- **Sub-lock (a) ARPG-canon-primary at substrate-mechanical layer.** The VFX scene-needs spec preserves the existing engine substrate (skill mechanics, encounter content-types, attribute-math). VFX choices honor ARPG-canon at the substrate level — fire-spell-effect for fire-elemental skill; physical-impact-burst for kinetic-skill; etc.
- **Sub-lock (b) Isekai-canon-primary at narrative-skin and convergence layers.** The VFX scene-needs spec's display-layer renderings (per-embodiment narrative-skin) feed into drax's Stage 4 form-bias work. For VS2a specifically: PLACEHOLDER A + B determine how much of sub-lock (b) lands at VS2a vs is deferred to VS2b.

**Three-layer model (Entry 2 of the form-bias batch):**
- **Substrate** (engine-internal; Pimen-9 elements at current state; cipher-width-expanded outcome at post-Step-B): the spec operates at THIS layer.
- **Grouping** (per-season opposition structure): the spec is grouping-agnostic; VS2a uses whatever grouping the season-001005 generation produced.
- **Vocabulary** (per-season LLM names; player-facing): the spec REFERENCES this layer via PLACEHOLDER A.

## What this dispatch produces

A single document: `canonical/story/vs2a-vfx-scene-needs.md` (or `agentic_orchestration/research/vs2a-vfx-scene-needs.md` — gandalf+drax pick the location; canonical/story is preferred for design-doc visibility).

### Section 1 — Encounter-type inventory (gandalf design framing)

Per the gauntlet structure (per `canonical/29-design-overview.md` + the engine's content-type slots), enumerate the per-encounter-type VFX presence:

| Encounter type | Combatant scope (per PLACEHOLDER B) | VFX presence per skill-cast | VFX presence per impact | VFX presence per status/ambient |
|---|---|---|---|---|
| Trash | (resolve via spec session) | (resolve) | (resolve) | (resolve) |
| Magic | (resolve) | (resolve) | (resolve) | (resolve) |
| Pack | (resolve) | (resolve) | (resolve) | (resolve) |
| Elite | (resolve) | (resolve) | (resolve) | (resolve) |
| Mini-boss | (resolve) | (resolve) | (resolve) | (resolve) |
| Boss | (resolve) | (resolve) | (resolve) | (resolve) |
| Trial | (resolve) | (resolve) | (resolve) | (resolve) |

Gandalf authors the per-encounter design framing: what VFX moments are diegetic-load-bearing per encounter type? What's the difference between a "magic" encounter's VFX expectation vs a "boss" encounter's? Use `canonical/story/court-of-forms.md` + `canonical/story/style-register.md` + `canonical/story/enemy-visual-legibility.md` as design-anchor docs.

### Section 2 — Per-skill VFX slot enumeration (drax render-constraint framing)

For each skill archetype the engine generates (mage / controller / warrior / hunter / etc. per `b6_archetype_templates.py`), enumerate the VFX slots a skill-cast needs:

| Slot | What it is | Drax render constraints | Catalogue mapping target |
|---|---|---|---|
| **Cast-charge** | Pre-cast visual (LLM "Cyclone Slash" preparation moment) | (drax: timing constraints; layering; sprite-vs-particle) | (substrate-tag: e.g., "wind-cast-charge") |
| **Projectile / movement** | Cast-in-flight visual (where applicable) | (drax) | (substrate-tag) |
| **Impact** | Hit-resolution visual on target | (drax) | (substrate-tag) |
| **Status-application** | Status-effect-attaches-to-target visual | (drax) | (substrate-tag) |
| **Status-ambient** | Status-effect-persists-on-target visual (DoT, slow, root, etc.) | (drax) | (substrate-tag) |
| **(other)** | (gandalf surfaces additional slots based on design judgment) | (drax) | (substrate-tag) |

The slot enumeration is per-archetype-AGGREGATE, not per-individual-skill. The spec captures the SHAPE of skill VFX needs, not enumerating every concrete season-generated skill.

### Section 3 — Substrate-tag inventory needed (cross-vendor evidence target)

Aggregate the substrate-tags the spec surfaces. Compare against:
- **Pimen-9 baseline** (`research/catalogue/pimen/full-2026-05-16.jsonl`) — what's covered today
- **Frostwindz / Pixogen / CodeManu / Fellor / Pipoya** (Step B candidates; per `qa/findings/2026-05-16-gandalf-step-b-gate3-review.md`) — what's coming
- **Cipher-width-expanded substrate** (per PLACEHOLDER C if II chosen) — what's hypothesized for VS2b

Flag substrate-tag-gaps:
- Tags the spec needs that aren't covered by Pimen + Step B candidates → catalogue follow-on work needed
- Tags the spec doesn't need that vendors over-cover → curation pruning opportunity

This section feeds the eventual elrond Pimen subset selection dispatch + elrond's VS2b attribution-pipeline schema dispatch.

### Section 4 — Per-encounter scene-walkthroughs (Optional per PLACEHOLDER C)

If PLACEHOLDER C = (II), add per-encounter scene-walkthroughs for VS2b forward-looking:
- What does a "magic encounter with cipher-width-expanded substrate" look like in display?
- What does "per-embodiment-narrative-skin rendering" mean concretely per encounter type?
- What amendment-triggers would the spec need to absorb when post-Step-B sub-locks resolve?

If PLACEHOLDER C = (I), this section is SKIPPED — the spec stays VS2a-substrate-locked and future amendment lands as a separate dispatch.

### Section 5 — Open questions surfaced by the spec (gandalf+drax convergence checkpoint)

Things the spec authoring session SHOULDN'T resolve unilaterally — surface for Matt + future dispatches:

- Pimen subset selection: which 5-10 packs from the curated catalogue (`research/curated/pimen-catalogue-curated-2026-05-16.jsonl`) do VS2a's slots actually need? (Elrond's downstream dispatch consumes this.)
- VFX-attribution-pipeline schema: what does the manifest schema look like? (Elrond's VS2b dispatch consumes this.)
- Per-embodiment rendering decisions (PLACEHOLDER B (b2) only): which embodiments ship at VS2a, in what scenes, with what asset support?
- Cipher-width amendment-trigger conditions (PLACEHOLDER C (II) only): when does the spec need updating per post-Step-B sub-lock resolutions?

## Cross-seam considerations

- **Elrond:** primary downstream consumer. The spec drives elrond's Pimen subset selection (VS2a) + the VS2b attribution-pipeline schema dispatch (post-VS2a friction findings). No coordination required during this dispatch.
- **Drax (in their secondary role):** provides render-constraint framing per slot (Section 2). Drax doesn't author the SPEC; gandalf does. Drax provides the bounds within which gandalf's slot enumerations are renderable.
- **Star-lord:** out of seam for this dispatch. The eventual LLM-optimization addition (knight-rider plan step 4) lives in star-lord's seam; not commissioned here.
- **Rocket:** out of seam — generation produces what it produces; the spec doesn't ask rocket for changes.
- **Knight-rider:** notify at completion. The spec output triggers the next dispatch in the chain (elrond Pimen subset selection).

## Tag policy

No tag required (design-doc spec; not a code change). Standard authoring discipline applies (filed in collaboration repo; pushed to origin; cross-referenced in skill_handoff log + CHANGELOG).

## Required reading

- `agentic_orchestration/gandalf/open-threads/2026-05-16-vfx-scene-needs-spec-micro-decisions.md` (the open-thread holding the 3 micro-decisions this dispatch's placeholders resolve to)
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) + ailment-deferral (committed `680a3f1`) — strategic-axis lock + cadence Option II + the design-state context
- `canonical/story/form-bias-cadence-strategy.md` § 5 + § 6 + § 7 (strategic-axis + three-layer model + cadence Option II)
- `canonical/16-project-roadmap.md` §VS2a + §VS2b (workstream framing)
- `canonical/story/style-register.md` (locked HD-2D-pixel register; binding design constraint)
- `canonical/story/court-of-forms.md` (encounter framing; gandalf design anchor)
- `canonical/story/enemy-visual-legibility.md` (encounter visual rules; gandalf design anchor)
- `canonical/story/embodiment-narrative-layer.md` (per-embodiment narrative-skin source; relevant if PLACEHOLDER B = b2)
- `agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl` (Pimen substrate baseline)
- `agentic_orchestration/qa/findings/2026-05-16-gandalf-step-b-gate3-review.md` (Step B Tier-1 candidates + Pimen-9 + cipher-width framework)
- `agentic_orchestration/research/curated/pimen-catalogue-curated-2026-05-16.jsonl` (curated catalogue; drax render-target reference)
- `agentic_orchestration/research/curated/catalogue-structural-pre-inventory-2026-05-16.md` (elrond pre-inventory; substrate-tag inventory baseline)
- `reincarnated-demo/scripts/pimen-ingest/` (drax pimen ingest pipeline; render-constraint source for Section 2)

## Acceptance criteria

- [ ] Spec document filed at `canonical/story/vs2a-vfx-scene-needs.md` (or equivalent location gandalf+drax pick)
- [ ] Section 1 (encounter-type inventory) complete per gandalf design framing
- [ ] Section 2 (per-skill VFX slot enumeration) complete per drax render-constraint framing
- [ ] Section 3 (substrate-tag inventory + cross-vendor gap flagging) complete
- [ ] Section 4 (per-encounter scene-walkthroughs) complete IF PLACEHOLDER C = II; else SKIPPED with explanation
- [ ] Section 5 (open questions parking) complete with explicit dependency flags
- [ ] Knight-rider notified at completion; substrate-tag inventory feeds elrond Pimen subset selection dispatch authoring task

## Out of scope (explicit)

- **NO Pimen subset selection.** This is a SPEC; selection is elrond's downstream dispatch.
- **NO VS2b attribution-pipeline schema authoring.** Same — separate downstream dispatch.
- **NO per-pack asset evaluation.** Drax's ingest pipeline already handles per-pack consumption; the spec operates at slot level.
- **NO design changes to canonical-story docs.** The spec REFERENCES style-register.md / court-of-forms.md / enemy-visual-legibility.md but doesn't amend them.
- **NO engine generation changes.** Substrate-tags the spec needs are what the engine emits at current state; no engine-side ask.
- **NO commitment to PLACEHOLDER C = II content unless explicitly resolved that way.** Default deferral to Option I-scope unless the open-thread converges otherwise.

## Sequencing — how this dispatch fits

```
Open-thread micro-decisions (gandalf + Matt) ─→ Knight-rider activates THIS dispatch ─→ Joint gandalf+drax session ─→ Spec landed
                                                                                                                          │
                                                                                                                          ▼
                                                                                                                  Elrond Pimen subset selection dispatch (next)
                                                                                                                          │
                                                                                                                          ▼
                                                                                                                  VS2a first VFX integration (drax — ad-hoc per knight-rider plan step 2)
                                                                                                                          │
                                                                                                                          ▼
                                                                                                                  VS2b attribution-pipeline schema dispatch (elrond primary; per knight-rider plan step 3)
                                                                                                                          │
                                                                                                                          ▼
                                                                                                                  Optional star-lord LLM-optimization addition (per knight-rider plan step 4)
```

---

## Completion record

(To be filled in by gandalf + drax jointly on completion)

**Completed:**
**Spec path:**
**Encounter types enumerated:**
**VFX slots enumerated:**
**Substrate-tag inventory size:**
**Gaps flagged (count):**
**Section 4 (VS2b forward-looking) status:** included / skipped (per PLACEHOLDER C resolution)
**Open questions parked (count):**
**Notes for knight-rider:**
