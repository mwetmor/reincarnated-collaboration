# Dispatch — 2026-05-25 — drax — engine generation run loadout amendments (bundled fast-follow)

**From:** knight-rider (orchestrator)
**To:** drax (loadout app implementation seam)
**Approved by:** Matt 2026-05-25 (parallel-fire with rocket engine generation run; supports T4 post-mortem session 1 review with engine-layer field visibility)
**Estimated effort:** ~0.75-1.5 day combined (bundled: amendments 1+2 ~0.5-0.75d + M1/M2/M5 verify ~0.1d + optional Tier 3 ~0.25d)
**Acceptance:** design-mode toggle + cultural/period/quality-tier badges + § 8 strategy badge (optional) live in loadout Vercel preview; M2 gate-flip decision made + documented; jack-ryan Gate-2 PASSes output

---

## Context (parallel fast-follow to engine generation run)

The engine generation run is firing in parallel (rocket dispatch `2026-05-25-rocket-engine-generation-run-v1-narrow.md`; ~30-60 min wall-clock; produces ~30-40 forms via new engine v2.0). These loadout amendments land **as fast-follow** to support T4 post-mortem session 1 review — design-mode toggle in particular makes engine-internal fields visible for Matt + gandalf post-mortem evaluation without requiring CLI/notebook tooling.

**Per gandalf parked-amendments artifact** (`agentic_orchestration/gandalf/notes/2026-05-25-parked-loadout-amendments-post-v1-narrow.md`), Matt has signaled fire NOW (cycle pause is here; engine generation run lands forms but Matt + gandalf post-mortem review benefits from design-mode visibility before the design call).

This dispatch bundles **four scope items**:

1. **Amendment 1 — Design-mode toggle** (amendment artifact § Amendment 1)
2. **Amendment 2 — Cultural / period / quality-tier badges** (amendment artifact § Amendment 2)
3. **M1 + M2 + M5 ship verification** (knight-rider empirical-inspection finding: all three shipped per `drax/v0.1-cycle-11-m1-m2-m5-loadout-display-2026-05-25` commit `f22a61f`; M2 UI-staging gate `SHOW_OFF_HAND_SLOT = false` per intentional Cycle 11 design decision — **drax judges whether to flip at this milestone**)
4. **Optional Tier 3** — § 8 strategy distribution badge per form (at-a-glance "which keystone fired" view; ~0.25 day; drax discretion on inclusion vs deferral)

No contention with rocket engine generation run: different repos (`reincarnated-loadout` vs `reincarnated-engine`); cross-seam interface is the exported `classes.json` consumed by loadout (post-rocket-completion).

---

## Required reading before starting

**Primary (load-bearing):**
- `agentic_orchestration/gandalf/notes/2026-05-25-parked-loadout-amendments-post-v1-narrow.md` — amendments 1 + 2 scope verbatim (gandalf-authored, Matt-ratified)
- `agentic_orchestration/dispatches/2026-05-25-rocket-engine-generation-run-v1-narrow.md` — rocket dispatch context (what fields are about to land in `classes.json` via export pipeline)
- `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-run-framing-brief.md` § 1.4 — definitive list of "Forms WILL have" fields that design-mode surfaces
- `reincarnated-loadout/AGENT_STATE.md` — most recent drax state (Cycle 12 Wave 5 Spirit Guide narration L6 enrichment COMPLETE)

**M-item context (verify ship status + design continuity):**
- `agentic_orchestration/dispatches/2026-05-25-drax-cycle-11-m1-m2-m5-loadout-display.md` § Completion record — M1+M2+M5 ship state + M2 UI-staging gate rationale ("At v1.0 production launch, flip to `true` and remove the TODO comment")
- Empirical file inspection (knight-rider verified prior to dispatch):
  - `reincarnated-loadout/src/components/WeaponSlot/WeaponSlot.tsx` (M1)
  - `reincarnated-loadout/src/components/WeaponSlot/OffHandSlot.tsx` (M2 — note `SHOW_OFF_HAND_SLOT` constant gate)
  - `reincarnated-loadout/src/components/ui/ProvenanceBadge.tsx` (M5)

**Companion (consult as needed):**
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` §§ v1.4-layer-2 through v1.5 — full PlayerClassV2 + ExportAlterationOutput contract that loadout consumes
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — composition policy v1 (cultural / period / quality_tier semantics)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` — 8-phase workflow (provides context for "Intent Metadata" framing per existing M6 Tier 2 treatment)

---

## Math-before-code

**Not applicable** — UI-affordance dispatch with no math hotspot. Smoke-test discipline (#2) load-bearing: amendments must degrade cleanly when fields absent on pre-Cycle-12 classes (just as M3/M6/M5/M2 do per prior null-safe patterns).

---

## Cross-seam contract change? (Principle 6 gate)

**NO** — this dispatch does NOT add, modify, rename, or remove any cross-seam field. It consumes EXISTING engine-emitted fields:
- `named_bearer` / `named_mythological_match` — populated by rocket Layer 2/3 for Sketch F anchors
- `mechanical_substrate_triple` — populated by rocket Layer 6 (L9)
- `source_library` — already consumed by M5 ProvenanceBadge
- `bc_target_cell` — populated by rocket Layer 2
- `converged_modifier` — populated by rocket Layer 4
- `t4_alteration_output` (raw struct) — already consumed by M6 T4ComparisonPanel
- `cultural_lineage_canonical` / `historical_period_canonical` / `quality_tier` — populated on weapon records per Sidecar B + Stage 4 substrate
- For § 8 strategy badge: `t4_alteration_output.strategy_type` (already typed as T4StrategyType union in `types.ts`)

**Round-trip:** not applicable — no cross-seam contract change in this dispatch. The cross-seam round-trip validation happened at star-lord Wave 5 (off-hand contract export round-trip 42/42 PASS) + rocket Layer 6 (round-trip JSON smoke PASS). This dispatch consumes already-validated upstream fields.

---

## Scope

### Item 1 — Design-mode toggle (amendment 1)

- [ ] Add toggle component to loadout form-display panel — Player-mode (default; current M1-M6 surface) vs Design-mode (exposes engine-layer fields)
- [ ] Toggle UI placement + styling — drax design judgment (likely top-of-page or per-form-card; small switch / button group; not intrusive)
- [ ] Toggle state — drax judgment whether per-session (in-memory) or persisted (localStorage); default = Player-mode regardless
- [ ] Design-mode field surfacing (per parked amendment § Amendment 1):
  - [ ] `named_bearer` / `named_mythological_match` (engine-layer identity; surface as labeled field on form card)
  - [ ] `mechanical_substrate_triple` (per L9 BDI math substrate tuple; surface as labeled field or expanded chip)
  - [ ] `source_library` (provenance: generator_v2 / engine_authored_gap_fill_v1 / legacy; **may overlap with existing M5 ProvenanceBadge** — drax judgment whether to surface as additional design-mode-only treatment or rely on existing badge)
  - [ ] `bc_target_cell` (5-tuple identity; surface as labeled field; consider compact representation)
  - [ ] `converged_modifier` (Layer 4 output; surface as labeled field — likely numeric / object representation)
  - [ ] Optional: `t4_alteration_output` raw struct (alongside spirit-guide narration; collapsed/expandable; drax judgment)
- [ ] Null-safe throughout (pre-v2.0 classes lack these fields; design-mode degrades cleanly to "—" or omitted-field treatment)
- [ ] Component placement: drax judgment per existing loadout panel architecture (likely woven into existing form-card or new design-mode-only section)

### Item 2 — Cultural / period / quality-tier badges (amendment 2)

- [ ] Add badges to loadout form-display per main weapon + off-hand item (per parked amendment § Amendment 2):
  - [ ] **Cultural tag badge** — from weapon's `cultural_lineage_canonical` (european / east_asian / mesoamerican / etc.)
  - [ ] **Period tag badge** — from weapon's `historical_period_canonical` (classical / medieval / contemporary / mythological / etc.)
  - [ ] **Quality-tier badge** — from weapon's `quality_tier` (S / A / B / C); INFORMATIONAL rarity for v1 viewing (Tier S forms feel legendary; Tier B forms feel common); NOT player-game ARPG drop rarity (v1.1+ territory — DO NOT confuse with M5 provenance treatment)
  - [ ] **Substrate provenance** — if quality_tier is engine-authored gap-fill (per M5 existing badge), **preserve current M5 treatment** (no overlap; M5 = library provenance; quality_tier = quality grade)
- [ ] Badge styling — drax design judgment (likely small chips below/beside weapon name; visually distinct from existing M5 ProvenanceBadge; use Tailwind utility classes consistent with existing badge patterns)
- [ ] Display modes:
  - [ ] **Always visible** in Player-mode (per amendment 2 scope — these are weapon-display enrichments, not engine-layer-only)
  - [ ] **Also visible** in Design-mode (no special treatment beyond Player-mode visibility)
- [ ] Null-safe (pre-Cycle-10 weapons may lack `cultural_lineage_canonical` / `historical_period_canonical` / `quality_tier`; badges hide when field absent)

### Item 3 — M1 + M2 + M5 ship verification + M2 gate-flip decision

- [ ] Inspect `src/components/WeaponSlot/WeaponSlot.tsx` (M1) — verify shipped + consumed correctly by Loadout page
- [ ] Inspect `src/components/WeaponSlot/OffHandSlot.tsx` (M2) — verify shipped + UI-staging gate state (`SHOW_OFF_HAND_SLOT` constant)
- [ ] Inspect `src/components/ui/ProvenanceBadge.tsx` (M5) — verify shipped + consumed by class-level + weapon-level treatments
- [ ] **M2 gate-flip decision (drax authority per seam ownership):**
  - **Context:** Cycle 11 dispatch deferred gate-flip until "v1.0 production launch". Cycle 12 closed (`v1.0-new-engine-ready` tag) + engine generation run lands ~30-40 forms with populated `off_hand_contract` via Wave 5 (`c0be301`). Off-hand data is now production-shape.
  - **Drax decision:** flip `SHOW_OFF_HAND_SLOT = true` OR keep gated for further validation. Document rationale.
  - **If flip:** verify off_hand consumption is null-safe across pre-Cycle-12 classes (which lack off_hand data); confirm visual treatment matches Cycle 11 intent.
  - **If hold:** document specific empirical-evidence criterion that gates re-engagement of the flip (e.g., "post-rocket-completion verify off_hand contract shape on ≥3 forms before flip").

### Item 4 — Optional Tier 3: § 8 strategy distribution badge per form

- [ ] **Drax discretion:** include in this dispatch OR defer as separate fast-follow
- [ ] **Scope (if included):**
  - [ ] Surface § 8 strategy as compact badge on form card — "RESOURCE_CONVERSION" / "TRADE_OFF" / "ELEMENT_CONVERSION" / "DEFENSIVE_CONVERSION" / "GEOMETRY_COLLAPSE" / "DEFENSIVE_TRADEOFF"
  - [ ] Source: `t4_alteration_output.strategy_type` (already typed as T4StrategyType in `types.ts` per Cycle 11 M3 work)
  - [ ] At-a-glance "which keystone fired" view — supports T4 post-mortem strategy distribution review
  - [ ] Color-coding optional (drax judgment per visual design consistency)
  - [ ] Display in both Player-mode AND Design-mode (this is a player-relevant intent affordance per Tier 2 framing — same treatment as existing M6 Intent Metadata)
- [ ] **If deferred:** document deferral rationale in completion record; create deferred-item entry for next drax dispatch

### Operational scope (all items)

- [ ] Smoke-test passes (`npm run build` clean; `npm run dev` launches; null-case + populated-case smoke per existing drax discipline)
- [ ] No regression on M1/M2/M3/M4/M5/M6 (verify per existing smoke fixtures + ~114 classes in 11 real seasons)
- [ ] Round-trip smoke: not applicable — no cross-seam contract change in this dispatch (consuming existing emitted fields per Principle 6 gate above)
- [ ] **Vercel preview-only** (Q5 RATIFIED from Cycle 11; production promotion remains separate Matt-touch — DO NOT promote)
- [ ] MIGRATION.md: drax seam-internal MIGRATION update if needed for design-mode component architecture (drax judgment)
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `drax/v0.1-engine-generation-run-loadout-amendments-2026-05-25`
- [ ] Sub-tags per item per drax discretion (per-item allows incremental verification; aligns with Cycle 11 M1/M2/M5 per-item pattern)

## Acceptance criteria

- [ ] Amendments 1 + 2 deliverables shipped per parked amendment artifact scope verbatim
- [ ] M1/M2/M5 verification documented in completion record; M2 gate-flip decision made + rationale captured
- [ ] Optional Tier 3 inclusion-vs-deferral decision made + rationale captured
- [ ] Build clean (0 TypeScript errors); dev server launches; null-case + populated-case smoke PASS
- [ ] No regression on existing M-items or pre-Cycle-12 classes
- [ ] Vercel preview URL provided in completion record (Q5 preview-only; no production promotion)
- [ ] Round-trip smoke: not applicable because no cross-seam contract change in this dispatch
- [ ] Tag `drax/v0.1-engine-generation-run-loadout-amendments-2026-05-25` shipped; AGENT_STATE.md updated
- [ ] jack-ryan Gate-2 fires post-tag (KR routes — gate validates output)

## Out of scope (explicit non-goals)

- **Production Vercel promotion** — Q5 RATIFIED preview-only; production promotion is separate Matt-touch
- **Player-facing ARPG rarity mechanics** (common / uncommon / rare / epic / legendary) — v1.1+ design territory; quality_tier badge is INFORMATIONAL only at v1 narrow
- **Faction membership display** — deferred per roadmap § 3.4
- **Per-fight spatial telemetry display** — v1.1+ multi-seam work
- **M7+ items** — out of scope per gandalf parked amendments artifact "What this note does NOT touch"
- **New cross-seam contract changes** — Principle 6 BLOCK if amendment scope creeps to require engine-side field additions; STOP and escalate to knight-rider
- **Engine-side bugs surfaced during display** — if loadout reveals a bug in engine-emitted data (e.g., malformed `mechanical_substrate_triple`), STOP design-mode work + escalate; do NOT amend engine data inline (that's rocket scope post-T4-post-mortem)

## Open questions for drax to resolve

- **Design-mode toggle placement:** top-of-page global toggle vs per-form-card toggle vs nav-bar setting — drax design judgment
- **Design-mode toggle persistence:** in-memory session-only vs localStorage — drax design judgment (default OFF either way)
- **`source_library` design-mode treatment:** drax judgment whether to add design-mode-specific surfacing OR rely on existing M5 ProvenanceBadge as sufficient design-mode-visible affordance
- **`mechanical_substrate_triple` visual representation:** raw object dump vs structured labeled triple vs collapsed/expandable — drax design judgment
- **Quality-tier badge visual distinction from M5 ProvenanceBadge:** drax judgment per visual design consistency (these are distinct concepts; visual treatment must not confuse)
- **M2 gate-flip decision:** drax seam authority per Cycle 11 dispatch deferral framing; document rationale either way
- **Tier 3 inclusion-vs-deferral:** drax discretion per workstream budget
- **Sub-tag granularity:** drax discretion (per-item sub-tags vs single combined tag)

## Cross-seam coordination (informational)

- **Rocket engine generation run is firing in parallel** (`agentic_orchestration/dispatches/2026-05-25-rocket-engine-generation-run-v1-narrow.md`) — no contention (different repos); but **timing observation:** drax amendments are most valuable AFTER rocket lands ~30-40 forms because design-mode toggle becomes load-bearing for T4 post-mortem. Drax may:
  - Start work IN PARALLEL (rocket's classes.json export happens at end of rocket run)
  - Verify amendments against incoming rocket-produced classes.json when it lands (loadout already consumes whatever season files exist in `data/`)
  - Use existing 11 real seasons + sample-season as smoke fixtures during build (pre-rocket-completion)
- **No fresh rocket / star-lord / elrond dispatch needed for this drax work** — all consumed fields are already emitted upstream per Wave 5 completion

## Handoff trigger (post-completion)

When this dispatch completes:

1. **jack-ryan Gate-2 fires** — knight-rider routes Gate-2 on the drax tag post-completion (standard Gate-2 protocol per critique-pair gate skill)
2. **T4 post-mortem session 1 readiness amplified** — design-mode toggle + cultural/period/quality-tier badges + § 8 strategy badge (if included) all support Matt + gandalf post-mortem review with engine-layer field visibility

## References

- `agentic_orchestration/gandalf/notes/2026-05-25-parked-loadout-amendments-post-v1-narrow.md` (load-bearing — Matt-ratified)
- `agentic_orchestration/dispatches/2026-05-25-rocket-engine-generation-run-v1-narrow.md` (parallel-fire context)
- `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-run-framing-brief.md` § 1.4
- `agentic_orchestration/dispatches/2026-05-25-drax-cycle-11-m1-m2-m5-loadout-display.md` § Completion record (M2 gate state + rationale)
- `agentic_orchestration/cycle-12-wind-down-summary-2026-05-25.md` (Cycle 12 closure record)
- `reincarnated-loadout/AGENT_STATE.md` (most recent drax state — Cycle 12 Wave 5 Spirit Guide narration L6 enrichment COMPLETE)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (cultural / period / quality_tier semantics)

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 — parallel-fire drax dispatch with rocket engine generation run; scope-doc autonomy + skip-confirmation re-auth for Cycle 13 transition state; gandalf parked amendments fire NOW
**Status:** FIRE — parallel-track to rocket engine generation run; no contention; lands fast-follow to support T4 post-mortem session 1 review with engine-layer field visibility

---
