# Dispatch — 2026-05-30 — drax — Cycle 14 v1.1 W4 UI wiring: skills × chain × tier + Primary T4 + Layer 2 T4

**From:** knight-rider (per gandalf consolidated follow-on routing 2026-05-30; Stage 2)
**To:** drax
**Authority:** Matt 2026-05-30 follow-on verbatim "wire in T4 nodes... emit the hidden secondary T4" — captured via gandalf session
**Hive-state:** ACTIVE — v1.1 mini-cycle W4 (last wave before wind-down)
**Status:** PENDING (gated on W3 close)
**Auto-commit:** YES per CLAUDE.md addendum 2026-05-25
**Auto-push:** YES per established cycle pattern; INCLUDES Vercel Production deploy

---

## Blocking dependency

GATED on:
- `agentic_orchestration/dispatches/2026-05-30-star-lord-cycle-14-v1-1-w3-chain-t4-emit-extension.md`

W3 emits: chain_composition + class_chain_count + t4_candidates + t4_scope + primary_t4 fields per kit; tag `star-lord/v1.69-cycle-14-chain-t4-emit-extension-1`.

---

## Required reading

1. `~/Games/reincarnated-collaboration/canonical/49-loadout-sample-player-surface-design-2026-05-27.md` § 1.1 (Loadout sandbox + T4 unlock semantics) + § 1.1.1 (Rank-0 amendment) + § 1.2 (Sample immutable spec)
2. `~/Games/reincarnated-collaboration/canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6 + § 4.6.4 (two-layer T4; universal-guarantee)
3. `~/Games/reincarnated-collaboration/canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3.1 (D66 one-T4-active sharpened)
4. `~/Games/reincarnated-collaboration/canonical/51-investment-scaling-6-pattern-architecture.md` § 10.7.8, § 10.8.5 (Primary T4 EXEMPT from strip-and-ship per universal-guarantee), § 10.8.9
5. `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` §v1.69 (W3-authored)
6. Spot-check 1 emitted class JSON in `~/Games/reincarnated-loadout/data/cycle-14-wave-5-season-001/classes/` for `chain_composition` + `t4_candidates` + `primary_t4` shape **before** committing render path (Disc #11 — parallel to W2 catch)

---

## Scope

### Work-item 1 — Skill display component (chain × tier grouping)

Render 12 skills per kit grouped by **chain** (chain_A/B/C per `skills[].chain_id`) × **tier** (1-4) on BOTH Loadout + Sample pages.

**Per-skill metadata to surface:** name, role (primary_attack/secondary_attack/control/support), scaling_attribute, canonical_element, energy_cost, cooldown_seconds, geometry, damage_multiplier, effects[]. T4 capstones (tier=4) **visually distinct** from tier 1-3.

**investment_points display:** value displayed as rank indicator. 0 = uninvested rank-0 per doc 49 § 1.1.1 amendment. (Cycle 14 wave-5 all skills emit investment_points=0; rank-0 nodes everywhere.)

### Work-item 2 — Chain composition display (kit-level structural)

Kit-level structural element showing `class_chain_count` + `chain_composition` (`t4_chains` vs `supporting_chains` vs `total_chains`). Both pages display this; it's the kit's structural identity.

### Work-item 3 — Primary T4 slot (fixed universal; non-toggleable)

Both Loadout + Sample pages render **Primary T4 as a FIXED slot** — cannot be toggled off; not selectable; universal-guarantee shape per doc 47 § 4.6.4.

Visually distinct from Layer 2 to communicate architectural distinction (Primary = universal; Layer 2 = cycling).

**Player-facing text:** e.g., "Primary T4: Direct Damage Amplification · 1.75× preferred-encounter-type · universal" — exact wording is drax in-scope per doc 49 player-surface vocabulary discretion.

### Work-item 4 — Sample tab Layer 2 T4 rendering (ACTIVE selection)

Show the **ACTIVE Layer 2 T4 candidate** (`t4_candidates[is_active=True]`) as the "AS-gauntlet-passed Layer 2 T4 selection."

**Real substrate-honest data, NOT placeholder.** Display: `t4_scope` + `category_a_strategy` + `category_bc_strategy` + `secondary_element` + `magnitude_tier` as canonical description of the gauntlet-passed Layer 2 T4 effect.

Sample tab scope boundary per doc 49 § 1.2 — Sample is the immutable AS-gauntlet-passed view; Layer 2 T4 is real because the gauntlet sim ran with that one specific Layer 2 active.

### Work-item 5 — Loadout tab Layer 2 T4 unlocks (toggleable; radio-button)

Show ALL `t4_candidates` as **toggleable unlockables** per doc 49 § 1.1 sandbox theorycraft semantics.

**Per doc 40 § 8.3.1 D66 sharpened:** player selects ONE Layer 2 T4 active at a time.

**Visual:** radio-button semantics — each candidate listed with its description (t4_scope + category_a_strategy + category_bc_strategy + secondary_element + magnitude_tier); selected one highlighted; clicking another deselects current and selects new.

### Work-item 5b — CHAIN_WIDE_OWN empty-Layer-2-T4 handling (KR amendment 2026-05-30 post-W3-routing)

**17 ACCEPT kits across 3 seasons** have `t4_scope=CHAIN_WIDE_OWN` and `t4_candidates=[]` per engine canonical state `CHAIN_WIDE_OWN_NO_T4` (`unified_calibration_loop.py:693`). Per doc 47 § 4.6.4 universal-guarantee proof, these kits satisfy Target 4 via Primary T4 universal alone — Layer 2 T4 list is canonically empty, NOT missing.

**Per-season ACCEPT breakdown** (star-lord W3 verification):
- season-001: 8 / 54 ACCEPT kits
- season-002: 3 / 53 ACCEPT kits
- season-003: 6 / 51 ACCEPT kits

**Render path (drax UX call within doc 47 § 4.6.4 anchor):**
- Loadout tab Layer 2 T4 panel: render empty-state for these kits with explanatory copy. Suggested copy: "This kit has no Layer 2 T4 unlocks — its T4 capability is provided by the Primary T4 universal guarantee alone (canonical per doc 47 § 4.6.4)." Drax adjusts wording per player-surface vocabulary discretion.
- Sample tab Layer 2 T4 surface: same empty-state pattern — there is no "AS-gauntlet-passed Layer 2 T4 selection" because none exists. Display the Primary T4 universal as the kit's sole T4 commitment.

**Anti-pattern guard:** do NOT render a placeholder "coming soon" or "Cycle 15+ pending" — these kits are canonically complete at v1.1; the empty state IS the substrate-honest design output.

### Work-item 6 — Gear display (no change)

`Cycle14GearDisplay` (W2-built) continues working. No changes needed.

### Work-item 7 — Vercel deploy

Push pattern is established this cycle. Trigger Vercel Production deploy (not preview only). Aliased to `https://reincarnated-loadout.vercel.app`. Spot-check 1 Cycle 14 season URL to confirm render.

---

## Quality criterion

**Game-quality goal this dispatch serves:** /loadout and /sample pages render the kit's full architectural identity at the player surface — skill structure organized by chain × tier (NOT a flat list), Primary T4 universal commitment, Layer 2 T4 cycling (active on Sample, toggleable on Loadout). This is the substrate-led player-facing surface doc 49 was designed for. Composes upward: Engine (W3 emission landed) > Game (player reads architectural identity at v1.1 surface; theorycrafts on Loadout, sees AS-gauntlet-passed identity on Sample) > Phase (this dispatch closes v1.1 mini-cycle player surface).

**Refutation conditions** (drax sub-agent surfaces if any apply BEFORE executing):
- W3 emitted shape contradicts dispatch's expected schema (Disc #11 spot-check 1 emitted JSON first — parallel to W2 catch)
- doc 49 § 1.1.1 Rank-0 amendment reading conflicts with the proposed render (e.g., investment_points=0 nodes should render as grey-disabled vs grey-enabled — drax design call)
- doc 47 § 4.6.4 universal-guarantee reading creates ambiguity about Primary T4 visual treatment (e.g., is "universal" rendered as a tag, a section header, a separate panel?)
- doc 40 § 8.3.1 D66 sharpened reading creates ambiguity about radio-button vs other selection semantic (drax UX call)
- Sample tab scope boundary (doc 49 § 1.2 immutable AS-gauntlet-passed) is violated by any of the renderings — e.g., if Layer 2 T4 toggle UI accidentally appears on Sample
- Dispatch introduces a pre-authored taxonomy without justification (#41) — player-facing T4 vocabulary MUST cite doc 49 anchor; drax wording discretion lives within doc 49 vocabulary frame
- Dispatch introduces a scaffold value not flagged as pending-decision (#40) — none expected

**Sub-agent action if refutation triggers:** halt before render-pass execution; return triage finding to KR. KR routes to gandalf Pattern A-light for canonical-anchor verification.

---

## Acceptance criteria

- [ ] Skill display renders 12 skills grouped by chain × tier on both /loadout + /sample
- [ ] T4 capstones (tier=4) visually distinct from tier 1-3
- [ ] Chain composition kit-level structural display (t4_chains / supporting_chains / total_chains)
- [ ] Primary T4 fixed slot rendered on both pages — non-toggleable, universal scope shape per § 4.6.4
- [ ] Sample tab shows ACTIVE Layer 2 T4 candidate as real AS-gauntlet-passed selection
- [ ] Loadout tab shows all Layer 2 T4 candidates as toggleable unlockables; ONE active at a time (radio-button per D66)
- [ ] CHAIN_WIDE_OWN kits (17 ACCEPT across 3 seasons) render empty Layer 2 T4 panel with canonically-grounded empty-state copy per doc 47 § 4.6.4 (Primary T4 universal-guarantee satisfies Target 4 alone)
- [ ] investment_points = 0 displayed as uninvested rank-0 nodes per doc 49 § 1.1.1
- [ ] Cycle14GearDisplay (W2) continues working — no regression
- [ ] No regression on /analytics, /encounters
- [ ] Build clean; loadout tests pass; Vercel Production deploy Ready
- [ ] Tag: `drax/v1.X-cycle-14-v1-1-w4-ui-wiring-1` (you choose version)

---

## Out of scope (explicit guard)

- Investment commit values per skill (Cycle 15+; investment_points stays 0)
- AS-gauntlet-passed skill-investment data on Sample (Cycle 15+; only Primary T4 + Layer 2 T4 active available now)
- Stat_distribution rendering changes (Cycle 15+ bundled-design-call queue)
- Color_palette / seasonal_cipher / t4_substrate_binding rendering (Cycle 15+)
- Live stat calculator on Loadout (Cycle 15+ post-investment-commit)

---

## Cross-seam impact

- **star-lord (W3 upstream):** consumed via §v1.69 emit. If any field-shape ambiguity surfaces, drax surfaces back to KR for star-lord clarification.
- **gamora:** no impact

---

## Completion record (to be appended on close)

**Status:** PENDING (gated on W3 close)
**Authored:** 2026-05-30 by knight-rider per gandalf consolidated follow-on Stage 2
