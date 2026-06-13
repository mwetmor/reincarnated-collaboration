# Dispatch — Rocket: Generation Handoff (Sessions 3 + 4)

**STATUS:** **FIRED 2026-06-12 (Matt-authorized, same session as gamora kernel handoff).** All items 1–11 authorized. **Session 1 RATIFIED same-day (Matt, 2026-06-12): Item 10 UN-HELD (Q9 ruled); Q2 ruled (chain count = generation parameter from {2,3}); Q10 ruled (faction redraw — see Item 6 note); Item 11 (Flag 4 cognitive-load prior) ADDED.** Ruling record: `gandalf/notes/2026-06-12-session-1-rulings-q1-q10-t4-catalog-expansion.md`. (gandalf, 2026-06-12; authored post-normalization-pass per legibility verdict § 7.4)

> **DESIGN LATITUDE GRANT (Matt, 2026-06-12 — mirrors the gamora dispatch grant):** significant implementation-design latitude is granted on HOW wherever this dispatch marks rocket-owned judgment: Layer 2 assignment-machinery architecture; sampling/weighting implementation; predictor implementation; kit-record schema field layout (within the MIGRATION.md discipline); rejection-pipeline design; config-vs-constant choices; threshold/magnitude PLUMBING (all T4 magnitudes from ruling record § 2 are PROVISIONAL — implement as config so balance passes tune without code changes). **Latitude covers HOW, not WHAT:** closed enums, locked BC thresholds, eligibility gates, the Session 3 § 1.5 capstone table verbatim (incl. the five Session-1 rows), vestigial-ontology (labels NAME-ONLY, never branched on), the do-not-self-adjust-weights rules (Items 9 + 11), generation-time vs measurement-time convention, and the Session 4 § 1.1 do-not-generate-proxy-primary guard are not negotiable. Where a latitude call would change design INTENT or a ratified surface, surface to gandalf before implementing — otherwise exercise judgment and record the call in the Gate-2 handoff.
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

Per the session-close handoff, all Session 3 + 4 rocket-seam work is unlocked NOW. ~~Two exceptions hold (Item 10 / Q9; faction-table gap / Q10), and one open question is worked with a placeholder (Q2 chain count)~~ **SESSION 1 RATIFIED same-day (2026-06-12):** Q9 ruled → Item 10 UN-HELD; Q2 ruled → chain count is a generation parameter from {2, 3} (placeholder replaced by the ruling — see Item 1 + § 12); Q10 ruled → faction redraw in flight (Item 6 mechanism unblocked; table content lands from elrond post-redraw). Catalog is now **25 strategies** (4 Session-1 additions: GEOMETRY_PROPAGATION `_cascade`/`_overkill`, RETRIBUTION_ENGINE, PERSISTENCE_ENGINE `_uptime`/`_saturation`, PHASE_MOMENTUM — Layer 2 capstone rows at Session 3 § 1.5; spec blocks at ruling record § 2). **NEW Item 11 added** (Flag 4 cognitive-load generation prior).

**Vestigial-ontology constraint (applies to every item):** archetype/class labels are NAME-ONLY, derived AFTER generation from substrate observations, never branched on in any generation or kernel path. Per `2026-06-12-vestigial-ontology-discipline-candidate.md` + register.

---

## 1. Layer 2 mechanism-structural dimensions (BLOCKING — everything downstream composes on this)

**Scope:** implement the four Layer 2 skill properties assigned at generation time: `magnitude_pattern × stackability × trigger × scaling_pattern`. Full value enums + behavior definitions at Session 3 § 1.1–1.4.

**Key decisions:**
- 6 magnitude_patterns (flat / scaling / burst_spike / decay / escalating / threshold_burst)
- 5 stackability values — `stacking_unlimited` is gamora-reserved, NOT a rocket generation value
- 8 triggers (on_use / on_hit / on_kill / on_take_damage / periodic / threshold_stack / threshold_hp / sequence)
- 6 scaling_patterns (player_level / gear_tier / resource_current / stack_count / enemy_hp_remaining / elapsed_time)

**Assignment rules (Session 3 § 1.5 — implementation contract):** per-skill-type constraint sets for CC skills, DoT skills, Burst AOE skills (spatial geometry ∈ {circle, cone, line}; predicted Axis 2 ∈ {small-AOE, large-AOE}), plus the T4-capstone assignment table (MOMENTUM_CASCADE → `stacking_capped_10` + `threshold_burst`; TEMPORAL_CHARGE → `stacking_capped_5` + `escalating` + `stack_count`; etc. — implement the § 1.5 table verbatim, **including the five Session-1-ratified rows added 2026-06-12:** GEOMETRY_PROPAGATION cascade/overkill, RETRIBUTION_ENGINE, PERSISTENCE_ENGINE, PHASE_MOMENTUM).

**Chain count (Q2 RULED 2026-06-12):** chain count is a **generation parameter sampled from {2, 3}** (2 chains → 1 T4 slot; 3 chains → 2 T4 slots from different families). The 4-chain row in Session 1 § 2.1 is architecture headroom — do NOT generate 4-chain kits in the 4,000-seed run.

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

**Q10 RULED (2026-06-12, ruling record § 1 Q10):** the 8 factions are being **redrawn so all 14 lineages have a faction home** (ONE composite ninth faction added only if the redraw can't absorb mesoamerican / sub_saharan_african / south_southeast_asian cleanly). Implement the lookup + nearest-match mechanism now; the redrawn table CONTENT lands from elrond. Keep the nearest-match logging — it remains the empirical check that no lineage routes through fallback systematically post-redraw.

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

## 10. Charge-stack kit generation rules — UN-HELD (Q9 RULED 2026-06-12)

**Scope:** Session 3 § 2 — exactly 1 `trigger=threshold_stack` spend skill per chain; threshold 5–10 assigned at generation; spend-all model; T4 compatibility table (§ 2.2; DEFENSIVE_TRADEOFF excluded — requires `energy_type == mana` per vestigial-ontology register).

**Q9 ruling (Matt-ratified, ruling record § 1 Q9):** **spend-all PLUS a passive per-stack bonus while stacks are held.** YOU vary passive-vs-burst magnitudes per kit — supply `per_stack_passive_bonus` + threshold-burst magnitude in kit data — so the optimal-rotation solver yields hold-optimal kits (→ Axis 5 charge-stack bin) AND spend-optimal kits (→ generator-spender bin). The kernel reads your magnitudes, never chooses (gamora kernel handoff Item 4 — un-held same ruling; both items fire together, gamora's after Items 1+2 smoke).

## 11. Cognitive-load generation prior (Flag 4 — RATIFIED 2026-06-12, ruling record § 3)

**Scope (NEW item):** generation prior on the cognitive-load distribution of the in-band corpus:
- HIGH cognitive-load bin (score ≥14) ≥ ~8% of in-band corpus
- ≤ 50% of the HIGH bin carries RESONANCE_LOOP — force the stacked-state route to HIGH (e.g., TEMPORAL_CHARGE + NETWORK_AMPLIFIER + SACRIFICE_ASCENDANCY = 19.5, no Resonance)

**Why:** Test 5 (Session 5) was amended to a three-way comparison (HIGH-with-Resonance / HIGH-without / LOW) to de-confound complexity penalty from single-strategy tuning; this prior guarantees the HIGH-without-Resonance group is populated. Implement as a generation-target check (like faction floors, Item 9): floors unmet → flag, do NOT self-adjust T4 selection weights.

---

## 12. Open-question dependencies (updated post-Session-1 ratification 2026-06-12)

| Q | Item affected | Disposition |
|---|---|---|
| Q2 (chain count) | Items 1, 4 | **RULED** — generation parameter from {2, 3}; placeholder retired (see Item 1) |
| Q4-S3 (chain sequence_depth) | Item 3 | **Placeholder OK** — T4-only contribution for now |
| Q6 (displacement CC counting) | Item 2 | **Implement as spec'd** (uncounted); amendment is enum-flag flip |
| Q9 (hold-vs-spend) | Item 10 | **RULED** — un-held; spend-all + passive per-stack held bonus (see Item 10) |
| Q10 (faction coverage gap) | Item 6 | **RULED** — faction redraw in flight; implement mechanism now; redrawn table content from elrond; keep nearest-match logging |
| Q1/Q6-S4 (sub-element edge pairs; cosmic_horror gating) | Items 4, 6 | **Implement as spec'd**; default-exclusion stands until Matt rules |

## 13. Sequencing + process

1. **Item 1 first** (Layer 2 dimensions) — Items 2–5 compose on it
2. Items 2–6 in any order after Item 1; Item 9 after Item 6; Item 11 alongside Item 9 (both are distribution-floor checks)
3. Items 7–8 require the BC pipeline pass — sequence after a measurement run exists for the generated corpus
4. Item 10 fires with gamora kernel handoff Item 4 (post gamora Items 1+2 smoke)
5. **Regression discipline:** smoke-test before full-regen per engineering-disciplines; no parallel regens of the same seed; tag intermediate states
6. **MIGRATION.md:** new section documenting kit-record schema additions (`predicted_control_share`, `predicted_axis2b_bin`, `cognitive_load_score/bin`, `coupling_depth`, `cultural_lineage/historical_period/register`, `faction`, `investment_profile`, label fields) — star-lord + elrond consume this schema; vestigial-ontology charge applies (no ontology-named fields with behavioral weight)
7. **Gate-2:** jack-ryan gates implementation commits per seam protocol; the spec docs themselves are gandalf-authored design artifacts (no Gate-2)
8. **Cross-seam boundary:** anything touching `simulation/` routes to gamora (e.g., `damage_event_log` is gamora's, per Session 3 § 5.2); FACTION_LOOKUP_TABLE content is elrond's

---

**Author:** gandalf, 2026-06-12. Authored post-normalization per legibility verdict § 7.4 ("rocket dispatch is authored AFTER normalization — never before"). Anchors: Session 3 + Session 4 specs (normalized); qd-engine-bc-axes-lock § 3; normalization-pass delta summary; vestigial-ontology register.

---

## Completion record (rocket, 2026-06-12)

**Status:** Items 1–11 + **Item 10 Part B** LANDED; Items 7/8 pipeline-RUN + Part B measured-split RUN
HELD (empirical-criterion gated); Item 12 (MIGRATION + Gate-2 handoff) complete. Full Session 3/4 rocket
suite **180 passed** (167 + 13 Part B). Item 10 Part B + cascade pushed to engine main.

| Item | Module | Status |
|---|---|---|
| 1 | `layer2_dimensions` | landed |
| 2, 3, 5 | `kit_finalization` | landed |
| 4 | `kit_architecture` | landed |
| 6 | `identity_sampling` (+ faction stub data file) | landed |
| 7 | `investment_profile` | function landed; RUN held (BC measurement) |
| 8 | `vestigial_labels` | function landed; RUN held; Berserker/Conduit structurally unreachable (reported, not reordered) |
| 9, 11 | `corpus_floor_verification` | landed (flag-only) |
| 10 | `charge_stack_generation` | Part A landed; **Part B landed** (UN-HELD after gamora kernel Item 4) |
| 12 | MIGRATION.md + AGENT_STATE + Gate-2 handoff | landed |

**Math-before-code:** 9 math notes in `generation/math/` precede the modules (incl. Part B α(T) crossover).
**Commits (engine main):** 807022f, 52ca2b4, 6c9daf3, 8647004, 18820d0, 3a122d3, 3dcfff1, **452ca29** (Part B) (+ Item 1).
**Gate-2:** `agentic_orchestration/rocket/notes/2026-06-12-session-3-4-generation-cascade-gate-2-handoff.md` — PENDING jack-ryan (now covers Parts A+B). No milestone tag pending verdict.
**Flags (4, `rocket/notes/`):** cogload §6.4 fixture discrepancy; identity §4.5 affinity excerpt + faction-table-pending (elrond); Items 7+8 reachability + kit_kind-gate + modifier-precedence.
**Held criteria:** Items 7/8 RUN + Part B measured-split RUN → BC-measurement pass over the generated corpus (reachability report over Season 001010); Part B kit→CombatantState live wiring → gamora follow-on once a charge-stack kit exists in a generated season.

### Item 10 Part B addendum (2026-06-12 — UN-HELD by Matt: "gamora finished item four. Proceed to item 10 and push")

Part B landed + **pushed** to engine main (`452ca29`; `d2ea435..452ca29`). gamora's kernel Item 4
(`dae0349`) supplied the charge-stack economics; Part B's first-order crossover model anchors to it.

- **Model:** HOLD-optimal ⟺ `cbps/psb < α(T)`, `α(T) = S − (T−2)(T−1)/(2T)`, S=10. Per-kit psb
  (`per_stack_passive_bonus`, hold reward) + cbps (`threshold_burst_magnitude`, spend burst rate) drawn
  with a margin off α(T) so each kit is unambiguously hold or spend. PROVISIONAL config bands (psb
  [0.03,0.07]; cbps clamp [0.10,0.90]; f_hold=0.50) — **do-not-self-adjust** (config not constants;
  measured-split deviation FLAGGED, never auto-tuned). gamora smoke defaults verified spend-optimal. ✔
- **PREDICTED vs MEASURED (Disc #11):** rocket emits the PREDICTED Axis-5 bin; the MEASURED hold/spend
  split is a downstream BC-pipeline RUN (same posture as Items 7/8 RUN).
- **Smoke:** charge-stack 26 passed (13 A + 13 B); full Session 3/4 suite **180 passed**.
- **Cross-seam (flagged to KR):** rocket `threshold_burst_magnitude` ⟷ kernel `charge_burst_per_stack`
  (same per-stack rate). gamora **action:** wire the kit→CombatantState lift when a generated season
  carries a charge-stack kit. See `rocket/notes/2026-06-12-item-10-part-b-landed-and-cross-seam-flag.md`.

### Items 7 + 8 RUN addendum (2026-06-13 — held criterion CLEARED)

gamora's BC-measurement pass is COMPLETE (`bc_measured_bins.json`, season `kse_20260613_002`, 96
kits, engine commit `edec4c6`). The two POST-BC-MEASUREMENT items RAN. Functions UNCHANGED (landed
2026-06-12); this is the RUN. Math note RUN addendum § 5 precedes; 40 unit tests green. Per the
vestigial-ontology constraint + § 2.3, the collapse/inversion is REPORTED as substrate evidence — no
rule reorder, no generation re-tune.

- **Join (FK, not bare tuple):** `simulatable_corpus.id_map` (96, 1:1, zero FK collisions). Harness
  `scripts/run_items_7_8_measured.py`.
- **Item 7:** investment_profile CLUSTERED → **high 95 / scaling 1** (glass collapse drives § 5.2
  rule 1). Proxy LOW-player/HIGH-proxy split masked on 6 proxy kits. →
  `output/season_001010_representative_20260613/item7_investment_profile_measured.json`.
- **Item 8 reachability:** reachable = {Arcanist 68, Pact-holder 12, Stormbringer 8, Invoker 6,
  Threshold 1, Sentinel 1}; **structurally unreachable = {Berserker, Conduit}**; empirically unfired
  = {Earthshaper, Phantom, Ranger, Ravager, Reaver, Shadowcaller, Striker, Templar, Warden,
  Windrunner}. → `item8_vestigial_labels_measured.json` + `measured_vs_predicted_divergence.json`.
- **Inversion root cause (gandalf Gate 1 input):** `defensive_vitality_scale` has ZERO generation
  consumers — never wired to the `vitality` stat, which follows energy/element priors instead. The
  collapse + inversion is one root cause: the defensive-target → stat bridge is absent. Reported,
  not patched (truth-to-design-around vs fix is gandalf + Matt's call).
- **Commit:** engine main (NOT pushed — Matt keystone-close gate).
