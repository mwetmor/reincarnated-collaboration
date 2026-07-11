# Dispatch — 2026-07-11 — gamora — F5 cost-TYPE math note (notes-only)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-07-11 (F5 forks all RULED same-day; build CLEAR with the math note FIRST)
**Estimated effort:** notes-only pass — **$0, NO sim code, NO runs, NO fights.** Math-before-code (Discipline #1) documentation only.
**Acceptance:** the four §8 open questions from the design note are PINNED to line-level truth in a math note under `simulation/math/`, ready for the rocket + star-lord co-sign and the downstream build.

## Context

Matt ruled the F5 cost-TYPE pass on 2026-07-11 — one pass, three R-4 reserved Axis-5 bins (HP-economy / damage-taken-converts / charge-stack). All three forks are ruled same-day:

- **F5-Q1 → (a) floor-guarded** — cast REFUSED when HP can't cover the cost (mirrors the `combatant.py:409` mana gate exactly).
- **F5-Q2 → BOTH seats** — **K26** Blood Mage/Martyr at the **WIS base seat** (the doc-48 un-defer) **+ K29** Necromantic Blood Mage at **INT** via the existing **T4 RESOURCE_CONVERSION door** (`t4_cost_resource: HP`; K13→K12 folded-kit precedent; no doc-48 INT-row amendment).
- **F5-Q3 → (a)** — K-sequential IDs; bench rows retire on promotion. Roster K26–K29; denominator 31 → **35**.

The design note (gandalf, SPEC-AUTHOR) is the build authority. **The build is CLEAR** — this math note is the FIRST step (math-before-code). The design grain lives in the note; **line-level truth lands here.** Precedent shape: the E4 commitment-axis note → gamora math note; and the proxy-calibration-note (cost-model semantics are class-fantasy surface → critique pair on the landed note).

## Required reading before starting

1. **This dispatch** — especially the serialization law (§ below) and the four pins.
2. `agentic_orchestration/gandalf/notes/2026-07-11-f5-cost-type-axis-design-note.md` — the P-1a build authority. **Header + §7 roster + §8 (the four open questions) + §9 (the forks, all ruled) carry the rulings.** Also §1 (what-IS survey — the code cites are verified against source 2026-07-11), §2 (two-mechanism / three-bin decomposition), §3 (Mechanism A: resource target), §4 (Mechanism B: builder source), §5 (invariants), §6 (measurement half).
3. Engine cites to verify against source (the note already did; re-confirm at math-note grain):
   - `combatant.py:409` `can_use_skill` mana gate (the mirror for the HP floor).
   - `combatant.py:286-293/:794` `t4_cost_resource` RESOURCE_CONVERSION HP deduction branch (Cycle 12 W5) — the SHARED consumer both doors inherit.
   - `combatant.py` `_ENERGY_CONFIGS` (~:427) — existing charge (10, start-empty, no regen), rage (100/empty/0), combo (5/empty/0), focus, stamina configs.
   - `per_skill_emitter.py:772` — the per-chain ailment hardwiring (the v1 direct-write mirror precedent for `on_damage_taken` accumulation).
   - `effect_resolver.py:tick_effects` (~:70) — where the E4 PHASE-2 tick work will also land (name the migration seam; do NOT build against it here).
4. Your own SESSION 62 AGENT_STATE — the attribution-spine writes (`damage_resolver.py:470/513`, `effect_resolver.py:~70`) are adjacent surfaces; note but do not disturb.

## The four pins (the §8 open questions — pin each to line-level truth)

**(1) HP-floor semantics at `_take_action` (fork F5-Q1(a) — floor-guarded).**
- Cast is REFUSED when HP cannot cover the cost, mirroring the `combatant.py:409` mana gate exactly. Pin: WHERE the gate lives, WHAT it returns/branches to on insufficient HP, and how it composes with the existing spend path.
- **ONE deduction branch that BOTH doors inherit** — K26 (base-native `resource_target: hp`) and K29 (T4-expressed `t4_cost_resource: HP`) share the same fight-engine HP deduction branch and the same floor gate. Pin the shared-consumer contract: the T4 RESOURCE_CONVERSION strategy SETS the same field the base door sets; the floor gate is downstream of both. No second deduction path.
- Self-KO-tail semantics: floor-guard keeps self-caused death out of gauntlet KPIs (which certify opponent-caused outcomes). Note that option (b) suicide-legal stays revisitable as T4 texture — out of scope for v1, pin the floor as the v1 law.

**(2) damage-taken event grain for the `on_damage_taken` builder (K27).**
- Pin the accumulation grain: per-hit **count** vs damage **magnitude**; **pre- vs post-mitigation**. Genre prior is flat-per-event (D3/D4 thorns), which also resists degenerate scaling against many-weak-hits encounters — state the ruling and the rationale.
- Pin the v1 accumulation mechanism: **direct resolver writes** (mirror of the per-chain ailment hardwiring at `per_skill_emitter.py:772`) with a **NAMED migration** — when the hook layer lands (E4-PHASE-2 adjacency), `on_damage_taken` becomes a hook-vocabulary trigger and the direct writes migrate. Name it now so the shortcut is a lineage entry, not drift.

**(3) charge-pool arity + the active-spender law (K27/K28).**
- Pin charge-pool arity for K27/K28 vs the existing `(10, start-empty, no regen)` config — same config or new? State the numbers and the rationale.
- **Active-spender law (anti-Invoker, STRUCTURAL not tuned):** charges must be SPENT by an action, never passively drained. No spender cast → no output → stand-there turret play is inexpressible **by construction**. Pin this as a structural invariant of Mechanism B, not a balance dial. Player-feel target: D4 Flay-thorns (getting hit BANKS, the cast is the payoff). D3 Invoker is the named anti-pattern.

**(4) byte-guard scope — existing-population byte-identity.**
- Pin the guard: every existing kit's fight outcomes must be **byte-identical** when no F5 field is present (default `resource_target: pool`, no `on_damage_taken`). This is the **third wearing** of the guard pattern (rocket's mono guard → gamora's attribution purity → F5's flat-resource guard).
- Pin the harness shape (the A/B reproduction pattern from SESSION 62's attribution purity harness is the model) — but this is the math note's SPECIFICATION of the guard, not the build. Name the field-absence → byte-identity contract and how the harness will prove it.

## Math-before-code

This entire dispatch IS the math-before-code step (Discipline #1). Deliverable is the math note; no implementation. Math-note code-citation discipline (#1.2): every claim cites its line-level source in the engine.

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)

**Round-trip: not applicable — no cross-seam contract change in THIS dispatch.** This is a notes-only math-note authoring pass; it emits NO code, NO schema, NO fields. The BUILD commit that follows carries the cross-seam contract (schema enum gain, `cost_model` fields, star-lord economy fingerprint columns + MIGRATION.md per ADR-004, doc-48 assigner amendment) — those are OUT OF SCOPE here and are the downstream build's obligations, pinned by this note.

## Scope

- [ ] Author `simulation/math/f5-cost-type-2026-07-11.md` (or seam-conventional name) pinning the four items above to line-level truth.
- [ ] Every claim cites engine source (Discipline #1.2).
- [ ] rocket + star-lord co-sign the math note (they are downstream consumers — doc-48 assigner / packet-enum for rocket; economy columns / MIGRATION for star-lord).
- [ ] AGENT_STATE.md updated at session end.
- [ ] Auto-commit per CLAUDE.md team discipline. Tag optional for a notes-only pass (seam-prefix if tagged).

## Acceptance criteria

- [ ] All four §8 open questions PINNED with a stated ruling + rationale + code cite.
- [ ] The shared-deduction-branch contract (K26 base + K29 T4 inherit ONE branch + ONE floor gate) is explicit.
- [ ] The active-spender law is stated as a STRUCTURAL invariant, not a dial.
- [ ] The byte-guard contract (field-absence → byte-identity) is specified with a harness shape.
- [ ] The `on_damage_taken` NAMED migration (direct-write v1 → hook-vocabulary at E4-PHASE-2 adjacency) is recorded.
- [ ] rocket + star-lord co-signs appended.
- [ ] Round-trip: not applicable — no cross-seam contract change in this dispatch (notes only).

## Out of scope (explicit non-goals)

- **ANY sim code, config change, or fight run.** Notes-only. $0. No runs.
- The BUILD itself (mechanisms, configs, gates in `simulation/`) — the downstream build after this note + co-sign + critique pair.
- rocket's generation half (doc-48 assigner amendment, schema/enum, packet emission, grammar cost branches) — co-sign only here.
- star-lord's economy fingerprint columns + MIGRATION.md — co-sign only here.
- The Axis-5 structural detector (measurement half §6) — downstream build.
- The §11 F5 re-derivation event — fires AFTER the build's baseline gauntlet output exists (Discipline #18 refinement).
- The doc-48 "Skirmisher DEFER" gap — explicitly OUT of F5 scope (design note §1); logged in the tracker, not this note's concern.
- Option (b) suicide-legal HP semantics — v1 is floor-guarded; (b) is revisitable T4 texture, not built or specified here.
- **E4 PHASE-2 files / cast-state machine / `effect_resolver.py` tick restructure** — serialization law (below). Name the migration seam, do NOT touch it.

## Serialization law (READ — the slot call)

**One gamora unit in flight at a time; the gamora SEAM is the serialization point.** Per Matt's slot call (relayed via KR): **E4 PHASE-2 sim build occupies the gamora slot FIRST.** This F5 math note fires ONLY when the gamora slot is free — i.e., after E4 PHASE-2 lands (or reaches a serialization-safe hand-off). Do NOT fire this dispatch concurrent with an in-flight E4 PHASE-2 gamora session. KR owns the slot sequencing; this dispatch is QUEUED-BEHIND-E4-PHASE-2 until KR clears it.

## On landing (KR-owned, do not self-invoke)

When the math note lands, KR runs the **Gate-1 critique pair (jack-ryan + gandalf)** on the landed note — cost-model semantics are class-fantasy surface (proxy-calibration-note precedent). THEN the F5 build sequencing returns to KR.

## References

- `agentic_orchestration/gandalf/notes/2026-07-11-f5-cost-type-axis-design-note.md` (P-1a build authority; forks §9 all ruled).
- `agentic_orchestration/gandalf/notes/2026-07-10-e4-commitment-axis-design-note.md` (precedent shape: design note → math note).
- `2026-07-10-gamora-commitment-axis-E4.md` (the E4 dispatch this serializes behind; PHASE-2 half fires first).
- engineering-disciplines.md #1 (math-before-code), #1.2 (math-note code-citation), #18 (re-derivation / registry-honesty timing).
- SESSION 62 AGENT_STATE (attribution purity harness — the byte-guard A/B model).

**Sign-off:** knight-rider, 2026-07-11 — FIRE-READY, QUEUED-BEHIND-E4-PHASE-2. Design fully ruled (all three forks); this is locked-decision math-before-code execution. Critique pair runs on the LANDED note, not pre-fire.
