# Normalization Pass — Delta Summary (2026-06-12)

**Author:** gandalf
**Authorization:** Matt, 2026-06-12 ("Go ahead with the normalization pass.")
**Source punch list:** `gandalf/notes/2026-06-12-five-session-cascade-legibility-verdict.md` (N1–N8)
**Measuring stick:** `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3 (locked BC axis vocabulary)

One-page record of what changed across the five session specs + the gamora kernel-handoff dispatch. Design INTENT in all six documents is unchanged; the pass re-pointed vocabulary, corrected kernel premises against verified code, and added two flagged design questions.

---

## 1. Cross-cutting conventions established (applied to all docs)

1. **Generation-time vs measurement-time.** Eligibility gates, priors, and generation rules bind to STRUCTURAL properties (declared `energy_type`, CC tags, skill geometry) or PREDICTED bins. BC bins are MEASURED downstream of simulation; a generation rule never reads a measured bin it hasn't produced yet. The one intentional measurement-time table: Session 2 § 6.3 companion-archetype modifiers (companion kits are BC-measured by modifier-derivation time).
2. **Three geometry layers.** Rich 24-type (`VALID_GEOMETRY_TYPES`, incl. `beam_channel`) → spatial 6-type (circle/cone/line/point/mixed/none via `_RICH_TO_SPATIAL`) → Axis 2 damage-geometry bins. Invented terms "AoE_burst"/"DoT_stack" belong to NONE of the three layers and were removed everywhere; DoT-stacking is Layer 2 `stackability`.
3. **Energy types ≠ Axis 5 bins.** mana/rage/focus/charge-stack are structural inputs; Axis 5 bins (HP-economy / damage-taken-converts / charge-stack / starved / overflow / generator-spender / steady) are measured behavior. The drafted energy_type→Axis-5 identity table was removed (Session 3 § 2.3).
4. **`front_load_profile` (NEW metric, telemetry-only).** front-loaded (≥50% damage in first 3s) / even (≤25% AND dps CV ≤0.30) / mixed. Legitimate home for the drifted "Axis 3A burst/sustained" usage. Promotion to a BC axis is Session 5 territory (Q3).
5. **Cell math.** 68,040 = 6×5×3×3×3×3×4×7 ALREADY includes 7-bin Axis 5; the drafted 81,648 figure was retracted (Session 3 § 2.3).

## 2. Per-file deltas

| File | Key edits |
|---|---|
| **Session 1 (T4 architecture)** | Six gate re-points: GEOMETRY_COLLAPSE (≥60% predicted damage share in one Axis 2 bin); MOMENTUM_CASCADE (Axis 2 ∈ AOE/chain/multi-spawn; vacuous "burst OR sustained" clause dropped); SACRIFICE_ASCENDANCY (HP-cost structural + predicted Axis 5 = HP-economy, Axis 4 ≠ glass); GEOMETRY_INVERSION (dominant-bin gate; Instant Actualization via Layer 2 `stackability = stacking`); TEMPORAL_CHARGE (declared `energy_type` = charge-stack + Q9 flag; geometry upgrades in rich/spatial terms); NETWORK_AMPLIFIER (Axis 2B ∈ {mixed, control-pure}; ≥3 CC types from locked closed enum). |
| **Session 2 (proxy + companion)** | § 3.4: kernel is SYMMETRIC (`simulate_fight(combatant_a, combatant_b, ...)` verified at fight_engine.py:107); extension is keyword-only `proxies_a`/`proxies_b`. § 4.2/5.2 weight tables re-pointed to locked bins + structural energy_type rows. § 9.1/9.2 prior keys re-pointed (`axis2b_control_pure`, `axis4_mitigator`, etc.). Axis 2A deferral RETIREMENT recorded (at Session 2 ratification — not a lock amendment). Q10 added (faction coverage gap). |
| **Session 3 (core combat mechanics)** | § 2.3 rewritten (identity table removed; cell-math retraction; Q9). § 3.1 three-layer geometry table + build status (`beam_channel` EXISTS; terrain GREENFIELD — only ChokeZone movement clamping at arena.py:104). § 3.2 symmetric signature + `terrain_type` kwarg; terrain-reactive as skill TAG. § 4.2/4.3 locked Axis 2B thresholds (20%/60%, effect-budget weighted); count-ratio formula repurposed as generation-time PREDICTOR with divergence telemetry. § 4.5 CC enum: counting vs non-counting (knockback/pull/taunt) split. § 5.1/5.2 locked Axis 3A (event-rate 2/6 per s) + Axis 3B (per-event CV 0.3/0.7); `damage_event_log` gamora addition. New Q6 (displacement effects). |
| **Session 4 (kit identity + generation)** | § 1.4 opener = direct-hit delivery; cross-chain control gate = predicted Axis 2B control-pure. § 2.2 all 18 labels re-expressed in locked bins + structural tags (e.g., Earthshaper via `terrain_reactive`; Stormbringer via `beam_channel`). § 2.3 16-rule assignment function re-pointed + reachability-verification note (vestigial-ontology discipline: labels NAME-ONLY, post-generation). § 4.5/§ 5.2 register + investment tables re-pointed (mitigator/glass; Axis 3B spiky). |
| **Session 5 (validation architecture)** | § 2.1/2.2 winner profiles + Test 2 criteria in locked vocabulary (front-loaded vs even; mitigator/tank vs glass). Test 3 CIRCULARITY FIX: behavioral-divergence tests only where test metric ≠ bin definition (Axes 1/2/2B/4); population-COVERAGE tests for telemetry-defined axes (3A/3B all bins ≥5%; Axis 5 ≥5 of 7 bins ≥3%; charge-stack reachability gated on Q9). NEW § 6: validation outputs → pattern-cell mapping (6-row table) + occupancy discipline (400 in-band kits ≈ 0.6% of 68,040 cells — the grid is a COORDINATE SYSTEM, not a fill target). |
| **Gamora dispatch (kernel handoff)** | STATUS: READY TO FIRE (Items 1, 2, 3, 5) on Session 2 § 3 ratification; **Item 4 ON HOLD pending Q9 Matt ruling**. § 2 verified symmetric signature + proxies_a/proxies_b. § 3 six modifier types; application point de-asymmetrized (player-side Combatant adjustment before `simulate_fight`). § 4 actual `_ENERGY_CONFIGS` shape `dict[str, tuple[float, bool, float]]`; on-HIT accumulation is NEW (combo precedent is on-USE, fight_engine.py:750); spend-all cost model is NEW; provisional charge-stack spec `(10.0, False, 0.0)`. § 5 terrain GREENFIELD premise corrected + assessment questions rewritten. § 7 Gate-2 self-verify kwargs corrected. |

## 3. New open questions surfaced by the pass

- **Q9 — hold-vs-spend (charge-stack).** A spend-all sawtooth NEVER measures as Axis 5 charge-stack bin (mean ≥0.75, var <0.20 = build-then-HOLD). Recommended fix (verdict § 6.1): spend-all + passive per-stack bonus while held; rocket varies magnitudes so the optimal-rotation solver yields BOTH hold-optimal and spend-optimal kits. Zero lock amendment. Routes to Session 1 dialogue; gates dispatch Item 4 + Test 3 charge-stack coverage criterion.
- **Q10 — faction coverage gap.** Mesoamerican / sub-Saharan African / South-SE Asian lineages (of Session 4's 14) are homeless among the 8 drafted factions. Options: add factions / intentional absorption / substrate-derived factions. Routes to Session 1 dialogue.

## 4. Kernel-premise corrections (code-verified)

| Drafted claim | Verified reality |
|---|---|
| Asymmetric player-vs-monster `simulate_fight` | Symmetric `(combatant_a, combatant_b, ...)` — fight_engine.py:107 |
| `_ENERGY_CONFIGS` dict-of-dicts with regen/decay fields | `dict[str, tuple[float, bool, float]]` = (pool_max, start_full, regen_per_s) — combatant.py:322 |
| On-hit stack accumulation exists (combo precedent) | Combo accumulates on-USE; on-HIT is NEW behavior |
| Terrain zones already exist | GREENFIELD — only ChokeZone movement clamping (arena.py:104) |
| Beam geometry NOT BUILT | `beam_channel` EXISTS in rich layer → spatial `line` |

---

*Sign-off: gandalf, 2026-06-12. Anchors: qd-engine-bc-axes-lock-2026-05-20.md § 3; five-session-cascade-legibility-verdict.md (incl. § 6 kernel-accuracy addendum); fight_engine.py / combatant.py / arena.py code verification.*
