# Dispatch — Rocket: Generation Handoff (Sessions 3 + 4)

**STATUS:** READY TO FIRE (Items 1–9) — Item 10 (charge-stack kit generation) ON HOLD pending Q9 Matt ruling; faction-lookup completeness for 3 lineages flagged on Q10 (gandalf, 2026-06-12; authored post-normalization-pass per legibility verdict § 7.4)
**Authored by:** gandalf (Session 3 + 4 spec author; KR auto-commits per standing pattern)
**Target agent:** rocket
**Seam:** generation/, element/, anchor/, foundation/ (+ engine internal canonical library)
**Does NOT touch:** simulation/ (gamora — incl. ProxyCombatant + kernel), telemetry/export/llm (star-lord), demo, loadout

---

> **VOCABULARY AUTHORITY:** the locked BC axis vocabulary at `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3 is the ONLY bin vocabulary. Both source specs were normalized against it 2026-06-12 (delta summary: `gandalf/notes/2026-06-12-normalization-pass-delta-summary.md`). If any instruction below appears to conflict with the lock doc, the lock doc wins and you flag the conflict to gandalf — do not re-derive bins from memory.

> **GENERATION-TIME vs MEASUREMENT-TIME (load-bearing convention):** your generation rules bind to STRUCTURAL properties (declared `energy_type`, CC tags, skill geometry, Layer 2 fields) or PREDICTED bins you compute yourself. MEASURED BC bins come from the BC pipeline downstream of simulation. Two items in this dispatch (investment profile, vestigial-class labels) intentionally run at kit finalization AFTER BC measurement — they are flagged as such. Everything else is pre-simulation.

## 0. Context

Sessions 3 + 4 of the 5-session architecture cascade are Matt-authorized and spec'd:

- `gandalf/notes/2026-06-12-session-3-core-combat-mechanics-spec.md` (Layer 2 dimensions; Axis 2B predictor; cognitive load; charge-stack generation rules)
- `gandalf/notes/2026-06-12-session-4-kit-identity-generation-spec.md` (kit architecture; vestigial-class labels; coupling depth; lineage × period × register; investment profile; faction verification)

Per the session-close handoff, all Session 3 + 4 rocket-seam work is unlocked NOW — it does not wait on Session 1 ratification (Q1–Q8). Two exceptions hold (Item 10 / Q9; faction-table gap / Q10), and one open question is worked with a placeholder (Q2 chain count — see § 11).

**Vestigial-ontology constraint (applies to every item):** archetype/class labels are NAME-ONLY, derived AFTER generation from substrate observations, never branched on in any generation or kernel path. Per `2026-06-12-vestigial-ontology-discipline-candidate.md` + register.

---

## 1. Layer 2 mechanism-structural dimensions (BLOCKING — everything downstream composes on this)

**Scope:** implement the four Layer 2 skill properties assigned at generation time: `magnitude_pattern × stackability × trigger × scaling_pattern`. Full value enums + behavior definitions at Session 3 § 1.1–1.4.

**Key decisions:**
- 6 magnitude_patterns (flat / scaling / burst_spike / decay / escalating / threshold_burst)
- 5 stackability values — `stacking_unlimited` is gamora-reserved, NOT a rocket generation value
- 8 triggers (on_use / on_hit / on_kill / on_take_damage / periodic / threshold_stack / threshold_hp / sequence)
- 6 scaling_patterns (player_level / gear_tier / resource_current / stack_count / enemy_hp_remaining / elapsed_time)

**Assignment rules (Session 3 § 1.5 — implementation contract):** per-skill-type constraint sets for CC skills, DoT skills, Burst AOE skills (spatial geometry ∈ {circle, cone, line}; predicted Axis 2 ∈ {small-AOE, large-AOE}), plus the T4-capstone assignment table (MOMENTUM_CASCADE → `stacking_capped_10` + `threshold_burst`; TEMPORAL_CHARGE → `stacking_capped_5` + `escalating` + `stack_count`; etc. — implement the § 1.5 table verbatim).

**Pass/fail:**
- Every generated skill carries all four fields with values from the closed enums
- Per-skill-type constraint validation: zero CC skills with periodic/sequence triggers; zero DoT openers; zero rocket-generated `stacking_unlimited`
- T4 capstone skills match the § 1.5 table per assigned strategy

## 2. Axis 2B generation-time predictor + CC closed enum

**Scope:** Session 3 §§ 4.1, 4.3, 4.5.

- CC-skill definition: non-null `cc_effect` from the closed enum AND applies to enemy AND duration > 0.5s
- Closed enum (locked Axis 2B inclusion list): stun, root, slow, freeze, fear, silence, blind, chill (counts only at ≥30% slow magnitude), mind_control/charm. **knockback / pull / taunt are valid `cc_effect` values that do NOT count toward control share** (Q6 — Session 1 dialogue may amend)
- Predictor: `predicted_control_share = cc_skill_count / total_skill_count`, mapped through the LOCKED thresholds (<20% damage-pure / 20–60% mixed / ≥60% control-pure) → `predicted_axis2b_bin`
- Store both `predicted_control_share` and `predicted_axis2b_bin` in kit record. The MEASURED bin (effect-budget weighted, BC pipeline) is the QD coordinate; your predictor serves eligibility gates (NETWORK_AMPLIFIER) and priors only. Predictor-vs-measured divergence is telemetry — do not "fix" divergence by changing the predictor without a gandalf consult.

## 3. Cognitive load metric

**Scope:** Session 3 § 6. Compute at kit finalization (after T4 assignment): `skill_count×1.0 + sequence_depth×2.0 + state_conditions×1.5 + timing_windows×2.5`; bins LOW <8 / MEDIUM 8–14 / HIGH ≥14. Store `cognitive_load_score: float` + `cognitive_load_bin: str`. Gates RESONANCE_LOOP (medium/high required) + TEMPORAL_CHARGE floor. Calibrate against the § 6.4 example table — those six examples are acceptance fixtures.

**Open dependency (Q4, Session 3 § 7):** whether chains themselves contribute `sequence_depth` or only T4 strategies. Implement T4-only for now; chain contribution is a one-line amendment when Matt rules.

## 4. Kit architecture — single / hybrid-2-element / physical-hybrid

**Scope:** Session 4 § 1.

- Architecture types + T4 eligibility alignment (§ 1.1); hybrid ratios (`primary_element_ratio` 0.60–0.70; physical 0.30–0.50) (§ 1.2)
- Sub-element compatibility matrix (§ 1.3) — incompatible pairs excluded by default; Matt-explicit override path only (Q1 may relax)
- Skill composition (§ 1.4): opener = direct-hit delivery, NO stacking-DoT opener; closer = highest-magnitude hit or CC; ≤1 CC per chain UNLESS `predicted_axis2b_bin = control-pure` (then 1 per chain distributed); ≥1 AoE skill per kit except explicit proxy-delegation

**Pass/fail:** generation validation rejects kits violating ratio bounds, incompatible sub-element pairs, DoT openers, or the AoE floor.

## 5. Coupling depth (Layer 1.5)

**Scope:** Session 4 § 3. `prerequisite_skill` field; coupling_depth = max prerequisite-link chain; enforce per-T4-family max depth table (§ 3.2 — e.g., RESONANCE_LOOP 4, proxy-family 2, monster kits 1) by removing the deepest link when exceeded. Store `coupling_depth: int`; feeds cognitive_load `sequence_depth`.

## 6. Identity sampling — cultural lineage × historical period × register + faction derivation

**Scope:** Session 4 § 4.

- 14-lineage catalog, 7-period catalog, 9-register catalog (§§ 4.2–4.4) — closed enums
- Sampling order: lineage (uniform unless priors skew) → period (lineage-affinity weighted, § 4.5 table) → register (element × predicted Axis 4 / predicted Axis 3B weighted, § 4.5 table — PREDICTED bins, generation-time)
- Faction = `FACTION_LOOKUP_TABLE[(lineage, period, register)]` with nearest-match fallback (register > lineage > period) and Void Covenant override (§ 4.6). Table is a DATA FILE loaded at generation time — elrond maintains; you implement the loader + lookup, you do NOT hardcode the table

**Q10 FLAG (do not self-resolve):** mesoamerican, sub_saharan_african, and south_southeast_asian lineages currently have no home among the 8 drafted factions. Implement the lookup + nearest-match mechanism regardless; the table CONTENT for those lineages lands after Matt rules Q10 (add factions / intentional absorption / substrate-derived). Until then, nearest-match will route them — log every nearest-match firing so the Q10 ruling has data.

## 7. Investment profile (POST-BC-MEASUREMENT item)

**Scope:** Session 4 § 5. Assigned at kit finalization AFTER BC measurement (the assignment table reads MEASURED Axis 4 / Axis 3B bins — this is one of the two intentional measurement-time items). First-match precedence per § 5.2 table (glass → HIGH; spiky + TEMPORAL_CHARGE → HIGH; proxy-primary → LOW player / HIGH proxy; mitigator/tank → SCALING; default SCALING). Store `investment_profile: str`.

## 8. Vestigial-class labels (POST-GENERATION, NAME-ONLY)

**Scope:** Session 4 § 2. 18 primary labels + 6 secondary modifiers; 16-rule first-match assignment function (§ 2.3) reading MEASURED BC bins + structural properties.

**Non-negotiables:**
- Labels are NAME-ONLY freight: UX + telemetry only; NEVER read by fight_engine, damage_resolver, or any generation branching path
- Per the § 2.3 rule-order note: verify per-label reachability at implementation. **Labels that never fire are substrate evidence, not bugs** — report unreachable labels to gandalf; do NOT reorder rules to force reachability

**Pass/fail:** assignment function is total (every kit gets exactly one primary label; rule 16 default catches the remainder); reachability report produced over the Season 001010 corpus.

## 9. Faction-kit completeness verification

**Scope:** Session 4 § 6. Post-generation + QD: verify ≥10 in-band player kits per faction; ≥20 NPC kits per faction; ≥40 monster kits per binding category; no faction >30% of in-band corpus. Log distribution (phase7 summary extension or separate faction report); floors unmet → flag to gandalf/knight-rider for weight adjustment — do NOT self-adjust sampling weights. (Floor values may move per Session 4 Q4; implement as config, not constants.)

## 10. Charge-stack kit generation rules — ON HOLD (Q9)

**Scope when it fires:** Session 3 § 2 — exactly 1 `trigger=threshold_stack` spend skill per chain; threshold 5–10 assigned at generation; spend-all model; T4 compatibility table (§ 2.2; DEFENSIVE_TRADEOFF excluded — requires `energy_type == mana` per vestigial-ontology register).

**Why held:** the locked Axis 5 charge-stack bin detects build-then-HOLD (mean ≥0.75, var <0.20); a pure spend-all rotation measures as starved/generator-spender. Recommended resolution (verdict § 6.1, Session 3 § 2.3): spend-all + passive per-stack bonus while held; YOU vary passive-vs-burst magnitudes per kit so the rotation solver yields both hold-optimal and spend-optimal kits. **Do not implement until Matt rules Q9** — this item is paired with gamora kernel handoff Item 4 (also held); both fire together on the same ruling.

---

## 11. Open-question dependencies (work-with-placeholder vs hold)

| Q | Item affected | Disposition |
|---|---|---|
| Q2 (chain count: generation parameter vs derived) | Items 1, 4 | **Placeholder OK** — implement with current chain-count rules; ruling is a parameter change |
| Q4-S3 (chain sequence_depth) | Item 3 | **Placeholder OK** — T4-only contribution for now |
| Q6 (displacement CC counting) | Item 2 | **Implement as spec'd** (uncounted); amendment is enum-flag flip |
| Q9 (hold-vs-spend) | Item 10 | **HOLD** |
| Q10 (faction coverage gap) | Item 6 | **Implement mechanism; table content for 3 lineages held**; log nearest-match firings |
| Q1/Q6-S4 (sub-element edge pairs; cosmic_horror gating) | Items 4, 6 | **Implement as spec'd**; default-exclusion stands until Matt rules |

## 12. Sequencing + process

1. **Item 1 first** (Layer 2 dimensions) — Items 2–5 compose on it
2. Items 2–6 in any order after Item 1; Item 9 after Item 6
3. Items 7–8 require the BC pipeline pass — sequence after a measurement run exists for the generated corpus
4. Item 10 waits on Q9
5. **Regression discipline:** smoke-test before full-regen per engineering-disciplines; no parallel regens of the same seed; tag intermediate states
6. **MIGRATION.md:** new section documenting kit-record schema additions (`predicted_control_share`, `predicted_axis2b_bin`, `cognitive_load_score/bin`, `coupling_depth`, `cultural_lineage/historical_period/register`, `faction`, `investment_profile`, label fields) — star-lord + elrond consume this schema; vestigial-ontology charge applies (no ontology-named fields with behavioral weight)
7. **Gate-2:** jack-ryan gates implementation commits per seam protocol; the spec docs themselves are gandalf-authored design artifacts (no Gate-2)
8. **Cross-seam boundary:** anything touching `simulation/` routes to gamora (e.g., `damage_event_log` is gamora's, per Session 3 § 5.2); FACTION_LOOKUP_TABLE content is elrond's

---

**Author:** gandalf, 2026-06-12. Authored post-normalization per legibility verdict § 7.4 ("rocket dispatch is authored AFTER normalization — never before"). Anchors: Session 3 + Session 4 specs (normalized); qd-engine-bc-axes-lock § 3; normalization-pass delta summary; vestigial-ontology register.
