# 2026-05-17 — gamora — D11 hybrid_mage tuning math note (QUEUED — auto-fires on gandalf advisory completion)

**Authority:** Matt L3 2026-05-17 evening — D11 sprint authorized; gandalf advisory determines tuning direction; gamora translates to engine-side math.
**Type:** Pattern B — gen-math + balance-loop math note; ~1 day.
**Predecessor (gates auto-fire):** gandalf D11 ARPG-balance advisory (`agentic_orchestration/dispatches/2026-05-17-gandalf-d11-arpg-balance-advisory.md`).
**Status:** 🟡 **QUEUED — DO NOT EXECUTE until gandalf advisory ships completion record.** Knight-rider activates when gandalf-D11 lands.

---

## Why this matters

D10 hit 37.1% convergence (vs >50% target). Residual is hybrid_mage structural over-generation. Gandalf's D11 advisory recommends the tuning DIRECTION (retain / retire / reshape; trade-off lever; thematic framing). Your math note translates that into:

1. **Engine-side gen-math rules** (rocket implements) — what does the generator do differently for hybrid_mage going forward
2. **Balance-loop / modifier behavior** (your seam) — does anything change in `balance_loop.py` to support hybrid trade-offs (e.g., the `floor_over_band` flag from D10 may need an `element_breadth_penalty` companion)
3. **Salvage strategy for 002011-015 hybrid_mage classes** — post-process the existing D10-curated outputs to apply D11 rules, or accept current state and require regen for D11 effects (likely post-process; preserves LLM cost discipline)

---

## Required reading (when activated)

1. **Gandalf D11 advisory** — `canonical/story/d11-hybrid-mage-tuning-advisory-2026-05-17.md` (your authoritative input; consume design direction)
2. **Rocket D10 completion record** — diagnostic anchor for hybrid_mage residual
3. **Your own D10 math note** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/D10-substrate-coherent-gen-math-note-2026-05-17.md` (pattern + style anchor for D11 note)
4. **Hybrid_mage sample classes** from 002011-015 D10-curated (your v1.5 convergence-analysis output exemplars are the over-band hybrid_mage cases)
5. **`reincarnated-engine/src/reincarnated/simulation/balance_loop.py`** — your seam; understand current modifier convergence behavior + where `floor_over_band` flag is emitted
6. **`reincarnated-engine/src/reincarnated/generation/d10_kit_constraints.py`** — rocket's D10 module; identify where D11 rules attach
7. **`reincarnated-engine/src/reincarnated/generation/geometry_derivation.py`** — derivation cascade; understand if hybrid_mage geometry signals need adjustment

---

## Scope — three deliverables

### Deliverable 1 — D11 hybrid_mage tuning math note

Author at: `reincarnated-engine/output/standard-demo-regen-2026-05-17/D11-hybrid-mage-tuning-math-note-2026-05-17.md`

Structure (mirror D10 math note pattern):
1. **§ 1 — Gandalf advisory translation** — restate the design direction in math-spec terms
2. **§ 2 — Inputs to D11 rules** — what fields, class object structures, class-level constants are consumed
3. **§ 3 — Tuning lever specification** — the concrete math (e.g., if "element-coverage damage tax", what's the formula; if "lower skill ceiling", what's the new ceiling per archetype variant)
4. **§ 4 — Generation-time rules** (rocket implements) — what changes in `generation/` to produce D11-coherent hybrid_mage
5. **§ 5 — Balance-loop / modifier rules** (your seam) — any new modifier_flag_tier emissions, convergence-helper signals
6. **§ 6 — Salvage strategy for 002011-015** — post-process plan; what gets re-pruned / re-balanced
7. **§ 7 — Expected convergence impact** — your projection of post-D11 convergence rate (target >50%; what's the realistic delta)
8. **§ 8 — Cross-seam impact + R11(b) round-trip clause** — if any new output paths or contract changes, declare them
9. **§ 9 — Acceptance criteria for rocket D11 implementation** — what rocket must hit
10. **§ 10 — Out of scope** — what D11 does NOT cover (D12+ flags; non-hybrid_mage archetypes unless gandalf scope-extended)

### Deliverable 2 — `MIGRATION.md v1.8` entry (if needed)

If D11 introduces a new modifier_flag_tier emission or a new balance-loop field on `ClassBalanceResult`, append a v1.8 entry to `src/reincarnated/simulation/MIGRATION.md` BEFORE your D11 code tag (jack-ryan pre-flag pattern; sets up rocket).

### Deliverable 3 — Hive log + tag

- PRE-SIGNAL § 14.1.1 before hive-log append
- STATE entry summarizing tuning direction + projected convergence delta
- HANDOFF → rocket (D11 implementation; auto-fires on your completion record)
- HANDOFF → jack-ryan (Gate 1 review of D11 math note before rocket fires)
- Tag `gamora/v1.6-d11-hybrid-mage-tuning-math-note-1` (math note authoring; per gamora pattern)

---

## Out of scope (DO NOT)

- ❌ DO NOT pre-empt gandalf advisory — wait for completion record; consume only
- ❌ DO NOT implement in code (rocket's job; you author math note + balance-loop changes if any)
- ❌ DO NOT modify `generation/` modules (rocket's seam; you specify the rule, rocket implements)
- ❌ DO NOT extend beyond D11 scope without explicit Matt authorization
- ❌ DO NOT push tag without Matt authorization (ADR-006)

---

## Acceptance criteria (when activated)

- [ ] D11 math note authored (10 sections per structure above)
- [ ] Inputs / outputs / formulas / acceptance criteria specified concretely enough for rocket to implement
- [ ] R11(b) round-trip clause present (either smoke-spec or "not applicable because <reason>")
- [ ] MIGRATION.md v1.8 entry (if cross-seam contract changes)
- [ ] Convergence projection grounded in v1.5 sample analysis + D10 empirical baseline
- [ ] HANDOFF → rocket + HANDOFF → jack-ryan (Gate 1) appended
- [ ] Hive-log STATE entry
- [ ] Tag `gamora/v1.6-d11-hybrid-mage-tuning-math-note-1` (local)

---

## Coordination

- **AUTO-FIRE TRIGGER:** gandalf D11 advisory ships completion record. Knight-rider monitors and spawns gamora agent at that time.
- **Parallel-safe with** drax v1.11 SEASON_IDS flip (different seam) + any post-VS2a work
- **PRE-SIGNAL § 14.1.1** before hive-log appends
- **Gate 1 BEFORE rocket fires** — your math note goes through jack-ryan Gate 1 advisory (D10 pattern; pre-flags surfaced before rocket implements)

---

*Dispatched (queued) 2026-05-17 by knight-rider per Matt L3 D11 sprint authorization. ~1 day when activated. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Author:** gamora
**Tag:** `gamora/v1.6-d11-hybrid-mage-tuning-math-note-1` (local; push gated per ADR-006)

### Deliverables shipped

**Deliverable 1 — D11 math note**
Path: `reincarnated-engine/output/standard-demo-regen-2026-05-17/D11-hybrid-mage-tuning-math-note-2026-05-17.md`
Sections: 10 + § 0 TL;DR. Structure matches dispatch spec (§§ 1-10 per acceptance criteria).

**Deliverable 2 — MIGRATION.md v1.10 entry**
Path: `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`
Entry: v1.10 — D11 element-coverage damage tax: new ClassBalanceResult fields + balance_metadata provenance.
Star-lord action required: YES (3 new columns on `class_balance_results`; non-blocking).

**Deliverable 3 — Hive log + AGENT_STATE + tag**
PRE-SIGNAL § 14.1.1 filed. STATE + HANDOFF entries appended to `agentic_orchestration/hive-mind/phase-1-p1-log.md`.
AGENT_STATE.md updated at `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`.
Tag `gamora/v1.6-d11-hybrid-mage-tuning-math-note-1` cut (local only; push gated per ADR-006).

### Acceptance criteria check

- [x] D11 math note authored (10 sections per structure)
- [x] Inputs / outputs / formulas / acceptance criteria specified concretely enough for rocket to implement
- [x] R11(b) round-trip clause present (§ 8.2 — clean; no new output paths)
- [x] MIGRATION.md v1.10 entry (cross-seam contract for 3 new ClassBalanceResult fields)
- [x] Convergence projection grounded in v1.5 Class C sample + D10 empirical baseline (§ 7)
- [x] HANDOFF → rocket + HANDOFF → jack-ryan (Gate 1) appended
- [x] Hive-log STATE entry
- [x] Tag `gamora/v1.6-d11-hybrid-mage-tuning-math-note-1` (local)

### Key decisions made in this math note (beyond advisory)

1. **Application site: Site A** (kit finalization, not balance-loop modifier) — per gandalf recommendation and D10 pre-eval gate correctness argument (§ 3.2)
2. **Config location for α** — `config/substrate_identities/_tax_config.yaml` (Phase-1 P2 forward compat; Discipline #13) (§ 3.4)
3. **DAMAGE_CONTRIBUTING_EFFECTS vocabulary** — excludes heal/lifesteal (player-side benefit); includes shock/consecrate (new substrate ailments) (§ 2.4)
4. **Pure defensive/CC/mobility skills are NOT taxed** — tax is on outbound damage, not utility effectiveness (§ 3.3)
5. **Salvage is hybrid_mage-only** — 17 instances; ~5-8 min sim time; $0 LLM (§ 6)

### α-recalibration flag

Matt-parked. α=0.07 is the starting point. Rocket smoke must confirm 3-element hybrid_mage converges above MODIFIER_FLOOR + FLOOR_EPSILON (0.055). If still pinning at floor → push α to 0.08-0.09. If over-correcting → reduce to 0.05-0.06. Surface finding to Matt before any code change on α.

### Gate before rocket fires

jack-ryan Gate 1 review is required before rocket D11 implementation begins. This is the D10 pattern. Gate 1 can run parallel with rocket planning, but rocket must not commit D11 code until Gate 1 verdict (ENDORSE or CONDITIONAL ENDORSE) is received.

---

## Jack-ryan Gate-1 advisory — D11 math note

**Reviewer:** jack-ryan
**Date:** 2026-05-17
**Tag:** `jack-ryan/v1.5-d11-math-note-gate1-review-1`
**Verdict:** CONDITIONAL ENDORSE — rocket may fire; pre-flags below must be addressed at code-time.

### Pre-flags (rocket addresses at code-time)

**WARN-1 — `skill_effects()` helper undefined in spec**

`_is_damage_bearing()` in § 3.3 calls `skill_effects(skill)` but that function is not defined anywhere in the math note or in `d10_kit_constraints.py` (confirmed by inspection — no such helper exists in the generation module). The empirical JSON structure shows skills as plain dicts with a top-level `"effects"` list. Rocket must replace the `skill_effects()` call with the concrete dict-access pattern already established in `d10_kit_constraints.py`:

```python
effect_names = {e["name"] for e in skill.get("effects", [])}
```

This avoids importing a non-existent helper and is consistent with the existing effect-access pattern in the same file (lines 123, 297 of d10_kit_constraints.py).
Cite: Discipline #11 (empirical inspection over assumption).

**WARN-2 — `schema_version` bump target is wrong**

§ 6.3 Step 6 directs rocket to bump `schema_version` to `v1.8` on post-processed class JSONs. Empirical inspection of the season_002012 classes.json confirms: `schema_version` is NOT a per-class-object field — it lives on the season `manifest.json` only (currently `v1.7`). The per-class top-level keys are: `id`, `name`, `archetype_tag`, `skills`, `carried_gear`, `balance_metadata`, `post_process_d10`, `d10_pruning_log`, etc. — no `schema_version`. Rocket must either: (a) add the schema bump to `manifest.json` only (not individual class entries), or (b) confirm the `v1.8` bump is a new per-class provenance field being introduced by D11 (in which case add it explicitly as a new key alongside `d11_post_process`). Either path is acceptable; the current instruction as written would silently add a field that no consumer reads on the wrong level. Bump target must be `manifest.json` → `v1.8` or a new explicit `d11_schema_version` field on each class.
Cite: Discipline #12 (semantic shift — don't assume field location).

**WARN-3 — Salvage § 6 does not explicitly confirm `carried_gear` preservation**

Matt hit a `carried_gear` bug at D10 (per dispatch). The D11 salvage steps (§§ 6.3 Steps 1-6) modify `damage_multiplier` values on skills and add provenance fields, but § 6.3 Step 6 does not explicitly state that `carried_gear` is preserved read-through and not cleared or rebuilt. Empirical inspection confirms `carried_gear` is a top-level dict on each class object (populated at D10 canonical-loadout selection). Rocket must add an explicit assertion in the salvage post-process: `carried_gear` is read-only during D11 post-process — the salvage rewrites `skills[*].damage_multiplier` and adds `d11_post_process` / `element_coverage_tax_multiplier` provenance fields; it does not touch `carried_gear`. Recommend adding a smoke assertion: `assert class_obj["carried_gear"] == pre_salvage_carried_gear` after salvage completes for each class.
Cite: Discipline #11 (empirical inspection); D10 bug pattern (carried_gear regression).

**INFO-1 — Convergence projection at § 7.2 uses compounded rough estimates**

The § 7.2 projection ("post-D10 WR 0.94–0.97" for the v1.5 Class C kit after D10 constraints) is an estimate-on-estimate. The actual post-D10+D11 WR for Class C is unknown without running the sim. The projection is flagged as approximate in the note itself (appropriately — "rough estimate"), and the α-recalibration flag in § 0 correctly handles the uncertainty. No action required at code-time; this is an observability note. Rocket's smoke run will produce the actual number.
Cite: Discipline #7 (capture decision telemetry; smoke anchors the projection).

**INFO-2 — Tax application note does not address `damage_multiplier = 0.0` edge case**

The tax is applied as `damage_multiplier *= tax_multiplier`. If any skill has `damage_multiplier = 0.0` (e.g., a pure-CC skill that carries a nominal zero on the field), the tax application is a no-op (0.0 × 0.93 = 0.0) — which is the correct behavior. However, the damage-bearing check `_is_damage_bearing()` may still return True for skills with `damage` in their effects but `damage_multiplier = 0.0`. Recommend rocket add a guard: if `damage_multiplier == 0.0` after tax, emit a warning log entry. This surfaces potential malformed skills that escaped D10 constraints.
Cite: Discipline #11 (empirical inspection over assumption).

**INFO-3 — MIGRATION.md v1.10 references "v2.4 (current)" for star-lord telemetry migrations.py**

The v1.10 entry states "Next available slot in `telemetry/migrations.py` after v2.4 (current)." This migration version was accurate at gamora write-time but may have advanced if drax v1.12 hotfix or rocket v1.12.1 also touched telemetry. Star-lord should verify `migrations.py` current version before appending. Non-blocking for D11 implementation; star-lord action only.
Cite: ADR-004 (cross-seam contract accuracy).

### Notes for rocket (carry-forward pre-flags)

1. Replace `skill_effects(skill)` call in `_is_damage_bearing()` with `skill.get("effects", [])` pattern (WARN-1).
2. Clarify `schema_version` bump target: manifest.json only OR explicit new per-class field (WARN-2).
3. Add explicit `carried_gear` preservation assertion to salvage post-process code (WARN-3).
4. Smoke must include `element_coverage_tax_applied == False` assertion on physical_warrior and fire_controller (§ 9.2 already specifies; WARN-3 adds `carried_gear` preservation check).

### R11(b) round-trip verdict

Clean per § 8.2 reasoning. Export path reads taxed `damage_multiplier` values directly (Site A application). Demo/loadout render correctly without modification. No new output paths or contract changes for drax/demo.

### Tax formula consistency verdict

Consistent. `1.0 - 0.07 × max(0, n_elements - 2)²` is stated identically in: § 0 TL;DR, § 3.1 formula, § 3.1 calibration table, § 6.3 Step 4 inline recalculation, and MIGRATION.md v1.10. No α drift detected across sections.

### Tax application point verdict

Unambiguous. Site A (kit finalization) is stated in § 3.2 with rationale for pre-eval gate correctness and export-path truth. §§ 5.1, 5.2, 8.2 all consistently reference Site A. No Site B ambiguity exists in the note.

### Ceiling 4→3 + ceremonial deferral verdict

Clear. § 4.1 states the single-line change with a "D12+ ceremonial only" comment. § 10 explicitly lists "4-element ceremonial path" as out of scope. Rocket cannot misread this as in-scope.

### MIGRATION.md v1.10 contract verdict

All three ClassBalanceResult fields are fully specified: name, type, default value, population method (via `getattr` defensive pattern), and column type for telemetry. Star-lord action is flagged as required + non-blocking. Contract is complete for star-lord to act on independently of D11 code execution.
