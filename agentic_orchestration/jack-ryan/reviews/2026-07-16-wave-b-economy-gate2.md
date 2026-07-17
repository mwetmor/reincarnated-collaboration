# Finding — 2026-07-16 — Wave-B economy (DEV-MODE Gate-2)

**Reviewer:** jack-ryan
**Verdict:** **PASS-WITH-AMENDMENTS** (no BLOCK).
**Target:** rocket `4f2548e`/`33ffc86`/`176f353` (tags `rocket/v2.10-waveb-1..3`) + gamora `1a0e5e4`/`e81f3f9`/`c037c5b`/`41e45f6` (tags `gamora/v1.9-waveb-1..3`), pushed head `cec8f12`. **Push HELD** — gandalf pushes.
**Developers:** rocket (generation seam), gamora (simulation seam).
**Charge:** Gate-2 review of both slices per Wave-A / ailment-Gate-2 precedent; verify Gate-1 amendments 1–10 honored; adjudicate AC-2 delegated ruling 12; ratify delegated rulings 9–12 into decisions-log.
**Principles applied:** Disciplines #1, #2, #3, #8, #11, #12, #13, #18; Review Principles #2, #3, #4, #5; ADR-002 (jack-ryan tier), ADR-004 (MIGRATION), ADR-006 (no push).

---

## Verdict

**PASS-WITH-AMENDMENTS.** Both slices honor Gate-1 amendments 1–10, defend byte-neutrality mechanically (not just empirically), and cite math notes authored BEFORE code (Discipline #1). Regression 391/391 targeted + 24/24 gamora smokes + 64/64 rocket smokes green. Three pre-existing spec-amendment candidates surface — **register as spec ERRATA, not as BLOCKs on this work.** AC-2 adjudicated in favor of DEFERRED-UNBUILT (see item 1). Amendments 11–15 below are ERRATA lines for gandalf/KR to fold into the spec — none blocking, none reversing a slice.

---

## Per-item findings (10 named audit items)

### 1. AC-2 ADJUDICATION — DEFERRED-UNBUILT stands; strike from Wave-B spec, respec at Wave-B.1/C
**(a) Templates:** kit-grain S5 emission does NOT require net-new PC/RS substrate templates. The `charge-stack` slice REUSES `W1_4_CHARGE_STACK` (25 templates, Cycle-12 L3) via the `charge_stack_sub_shape` FIELD on the emitted kit — a per-kit discriminator on the resource_economy dict is the composer's routing surface, not a template family. PC/RS follow the same pattern: the composer entry (`_ECON_BIN_COST_TYPE_MAP`) + `resource_economy` fields + `commitment_bin` widen ARE the emission surface; kit-grain emission composes off THESE, not off a template registry. Template ABSENCE does not block S5. **Not a Wave-B blocker.**
**(b) Bias maps:** grep-confirmed zero engine consumers of an econ-keyed `element_biases` map (`_BIAS` in `generation/` returns zero econ-bias consumers; `element_biases.py` is an ailment/scaling module). rocket correctly declined to land dead code. If element-biased PC/RS composition is INTENDED, it's a `bc_target_composer` sampling-weight change with its own spec section. **Ruling: STRIKE from spec §2.5/§3.5 as drafter speculation; RESPEC at Wave-B.1/C if intended.** Concurs with gandalf DRIFT-CRITIC lean.
**Severity:** INFO. **Action:** amendment 11 (ERRATA line at §2.5/§3.5, gandalf).

### 2. PC cost_type `rage` — VERIFIED
`_ECON_BIN_COST_TYPE_MAP["persistent-condition"] = ["mana", "focus", "rage"]` (`bc_target_composer.py:253`) and `rage` is a resolvable cost_type family (:237/:295 rage-lookup rank=65). Corpus-defensible: D2 Frenzy Barb + D2 Werebear/Werewolf form-states are rage-primary PC kits (spec §2.5 attests barbarian frenzy state). `resolve_cost_type` returns a valid family for all 4 role priorities on this non-empty map (smoke [1] verified). **CONFIRMED.**
**Severity:** INFO.

### 3. RS composed-hybrid 0.25·M floor — DERIVATION SOUND; register as §3.5 ERRATA
Math note §2 derivation: percent alone at `Σpct < 0.90 ⟹ cap_from_pct > 0.10·M`; flat alone at `Σflat ≤ 0.75·M ⟹ cap ≥ 0.25·M`. Under HYBRID at joint maxima (`Σpct→0.90`, `Σflat→0.75·M`), un-floored `cap_after_flat = 0.10·M − 0.75·M = −0.65·M`. The `max(0.25·M, …)` clamp is the tightest single floor that (i) honors both LOCKED per-shape ceilings and (ii) guarantees the pool never zeroes. Belt-and-suspenders architecture is correct. **Derivation validates.** Spec §3.5 states per-shape invariants ONLY; the composed floor is derivable-but-not-stated — register as ERRATA so future readers don't re-derive.
**Severity:** WARN (spec-clarity). **Action:** amendment 12 (ERRATA line at spec §3.5, gandalf: "under HYBRID composition, the effective floor is `max(0.25·M, cap_from_pct − Σflat)`").

### 4. Clamp-vs-block boundary — EMISSION-SIDE Σ NOT ENFORCED
Spec §3.5 says cap-breach = activation BLOCKED (PoE1 semantics); sim CLAMPS (`resource_economy.py:213-220`, sim floor at `spatial_engine.py:283`). Defensible for static-per-fight gauntlet reservations. **BUT:** emission-side `_validate` (`resource_economy.py:113-224`) enforces per-KIT bounds (`reservation_percent≤0.75`, `reservation_flat≤25`) — NOT per-POOL Σ. The line-77 comment says "per-pool Σ invariants gamora-enforced" — this is TRUE for the current sim (single-kit → `Σpct = reservation_percent`, so per-kit ≤ 0.75 satisfies `Σ < 0.90` trivially), but a FUTURE multi-reservation-per-kit case (if it arises) would need a per-pool Σ check at emission OR bind gamora's clamp harder. Current single-value bind means the sim clamp is genuinely belt-and-suspenders (never silently masks an emission breach) — no BLOCK. **Discipline #8 satisfied under single-value bind; note the multi-reservation contingency.**
**Severity:** INFO. **Action:** amendment 13 (spec ERRATA at §3.6 documenting the single-value bind assumption + explicit per-pool Σ owed if multi-reservation lands).

### 5. RS §3.7 CODE-REFUTED — spec ERRATA CONFIRMED
Grep across `simulation/` for `reservation_per_proxy|ECONOMY_RESERVED|regen_cap|reservation_resource|active_count`: ZERO hits pre-slice. Wave-A slice-2 AGENT_STATE (2026-07-13) verbatim: "NO A3 reservation (rocket) ... Next = rocket (... A3 reservation build-true ...)." Spec §3.7 "NO NEW ALGORITHM / extend existing" is code-refuted. gamora's slice-1 IS the first regen-cap-tax consumer, serving BOTH A3 flat-per-proxy (Wave-A backward-compat via `_sum_reserved_per_proxy_rate` + inline `sum(1 for p in self._proxies if p.is_alive)` at `spatial_engine.py:3563`) AND hybrid % fields. Byte-neutral + additive; spec's INTENT faithfully realized. **CONFIRMED.**
**Severity:** WARN (spec accuracy). **Action:** amendment 14 (spec §3.7 ERRATA — "first regen-cap-tax consumer, not an extension; A3 config surface shipped Wave-A but consumer deferred until Wave-B slice-1").

### 6. Charge-stack orthogonality — INTENDED, register as spec CLARIFICATION
Two "charge-stack" concepts kept orthogonal:
- **PRE-EXISTING** `energy_type == "charge-stack"` ROTATION model (`spatial_engine.py:1742-1745` build-and-hold-then-release; :1758-1770 accrual; `CombatantState.per_stack_passive_bonus` :189-190). Pool model — `entity.energy` IS the stack count. Phase-R rotation identity.
- **NEW** `charge_stack_sub_shape` ECON_BIN model (this slice). AM/RC live in NEW SpatialEntity fields (`am_current`, `cycle_charges`, `am_max`, `am_fill_trigger`, `am_fill_amount`, `am_discharge_threshold`, `cycle_max`, `cycle_recharge_seconds`, `cycle_recharge_source`, `cycle_recharge_accum` — `:742-748`).

Smoke C6 verifies energy pool unperturbed by AM kit (`energy=100.000 same as none-shape kit; am_current=12.0>0 orthogonal state`). **Orthogonality is CORRECT semantics** — conflating them would rebuild a shipped payment model mid-wave. Concurs with gandalf DRIFT-CRITIC lean.
**Severity:** INFO. **Action:** amendment 15 (spec §4 CLARIFICATION — name both concepts so future readers don't merge them: "energy_type charge-stack is the ROTATION identity / payment vocabulary; econ_bin charge-stack with sub_shape is a SEPARATE accumulator-or-cycle state machine; a kit MAY carry both").

### 7. Byte-neutrality regression — 391/391 PASS (my re-run, not taking developer word)
Ran targeted battery: `test_w02_bc_target_composer`, `test_spatial_gauntlet_scenarios`, `test_ailment_layer_{gamora,rocket}_slice`, `test_ailment_registry`, `test_cycle13_wave5_gauntlet_sim`, `test_proxy_pairing_layer`, `test_proxy_t4_suite_{eval,strategies}`: **391/391 pass in 1.12s.** rocket smoke `wave_b_economy_emit_smoke_2026_07_16.py` **64/64** (byte-neutrality corner + extra-key guard + runaway-guards + enum widen + 972-lattice-assert intact + template REUSE + no duplicate template_ids). gamora smokes `gamora_waveb_{rs_reservation,pc_persistent_condition,charge_stack}_smoke_2026_07_16.py` **24/24** (R0–R7 + P0–P7 + C0–C6). Inert-default theorem verified: RS `{0,0,0}`→`eff_cap==max_energy`→byte-identical (R1); PC None shape→no ActiveEffect→inert (P1); charge-stack None sub_shape→AM/RC branches skipped→byte-identical (C0). Player-only gating confirmed for mob byte-identity (R7). **CONFIRMED.**
**Severity:** INFO.

### 8. RNG-stream discipline — CONFIRMED, no stream-shift
RS `rs_effective_regen_cap` (`spatial_engine.py:263-283`) is deterministic — no `_resolver_rng`/`_resolver_rng_dmgvar` touch. PC tick-cost drain (`:3576-3586`) — deterministic. AM fill / RC recharge (`:3591-3613`) — deterministic counters. PC establishment (`:2676-2703`) + RC cycle establishment (`:2707-2708`) — BEFORE the RNG tick loop (`while elapsed < max_duration:` starts `:2710`). Hard-before-rng ordering honored (same bar as ailment Gate-2). Proc-loop / AM-discharge route their linked cast through the normal RNG-ordered `_apply_skill_damage` — but ONLY for bin-carrying kits → a non-bin kit sees ZERO extra draws → no stream-shift. **CONFIRMED.**
**Severity:** INFO.

### 9. Emission-validator scope — CORRECT SPLIT, 972-assert intact
Two commitment-enum sites verified:
- `per_skill_emitter._COMMITMENT_BINS` (`:396-406`): **widened** to 5 bins (`snap`, `wind-up`, `channel`, `persistent_toggle`, `persistent_trigger`).
- `bc_target_cell_sampler.COMMITMENT_BINS` (`:391`): **STAYS at 3** (`("snap", "wind-up", "channel")`); `CATALOG_LATTICE_WITH_COMMITMENT = CATALOG_LATTICE_PRE_E4 * 3 = 972` hard-assert intact (`:392`). QD archive cardinality unchanged. Concurs with delegated ruling 12 AC-3: **cell-space stability outranks vocabulary symmetry.** Smoke [5] verifies both (emission validator has 5 bins; lattice sampler unchanged; 972 intact). PC toggle/trigger are PC-kit-ROUTED shapes, not lattice-sampled coordinates. **CONFIRMED.**
**Severity:** INFO.

### 10. Gate-1 amendments 1–10 honored — CHECKLIST COMPLETE
- **#1 (A1) non-empty cost_type maps:** `charge-stack` `[]`→`["mana","focus","stamina-as-resource"]`; `reservation` NEW `["mana","focus"]`; `persistent-condition` NEW `["mana","focus","rage"]` — all resolvable via `resolve_cost_type:274`. HONORED (rocket slice 1, item 2 above).
- **#2 (A2) trigger boundary:** `PROC_TRIGGER_CONDITIONS` = single-trigger primitives ONLY (`resource_economy.py:87-89`, no chain values); PC math note §2.3 confirms terminal single cast, no re-arm. HONORED.
- **#3 (A3) §8 HP-economy corrected:** N/A (spec-doc edit already applied at Gate-1).
- **#4 (A4 TH rider): §8 count 0→3:** N/A (spec-doc edit at Gate-1).
- **#5 (A5 NR ruling):** NR routes to `steady` with `cost_scale≈0` — verified sim-side pool no-op; no rebuild. HONORED.
- **#6 no-`combatant.tick`:** PC/AM/RC consumers wired at `spatial_engine` per-tick loop + `effect_resolver.tick_effects` + `_on_kill_energy_burst` — NOT `combatant.py:tick` (no such method). HONORED across all three gamora slices (`:3552-3568`, `:3570-3586`, `:3588-3613`, `:1801-1806`).
- **#7 `commitment_state_machine` under `spatial_gauntlet/` + enum-widen framing:** commitment_bin enum WIDENED at `per_skill_emitter._COMMITMENT_BINS`; skill_schema doc annotated (`skill_schema.py:222-227`); QD lattice untouched. HONORED (rocket slice 3, item 9 above).
- **#8 W1_4 REUSE:** `substrate_templates.W1_4_CHARGE_STACK` still 25 templates; no charge-stack duplicates; no re-mint. HONORED (rocket smoke [6]).
- **#9 `ActiveEffect.params` not `.category`:** PC state at `params["shape"]`/`params["tick_cost"]`/`params["trigger"]`/`params["stack_count"]`/`params["source_persistent_condition"]` (`spatial_engine.py:2686-2695`); smoke P7 verifies no `.category` attribute created. HONORED.
- **#10 primary-vs-any-occurrence discipline:** counts reconciled at spec §0 to scoreboard; no re-count in implementation. HONORED.

**All 10 amendments HONORED.**

---

## Amendments (spec ERRATA — for gandalf/KR to fold, NOT blocking this work)

- **11** — Strike spec §2.5/§3.5 econ-keyed `element_biases` maps (`PERSISTENT_CONDITION_BIAS`/`RESERVATION_BIAS`) as drafter speculation; RESPEC as own composer sampling-weight section at Wave-B.1/C if intended. AC-2 DEFERRED-UNBUILT ADJUDICATED. Templates STRIKE ("greenfield" language at §2.9/§3.8 not required — kit-grain composes off resource_economy + commitment_bin, not a template registry).
- **12** — Spec §3.5 add composed-floor ERRATA line: under HYBRID composition, the effective floor is `max(0.25·M, cap_from_pct − Σflat)` = math note §2 derivation; sim (`spatial_engine.py:283`) is authoritative.
- **13** — Spec §3.6 note the single-value bind assumption: current sim per-kit `Σpct = reservation_percent` (single-reservation-per-kit); explicit per-pool Σ check owed at emission IF multi-reservation kits land.
- **14** — Spec §3.7 ERRATA — RS is the FIRST regen-cap-tax consumer, not an extension; the A3 config surface shipped Wave-A but the consumer was deferred until this slice.
- **15** — Spec §4 CLARIFICATION — name both charge-stack concepts distinctly: `energy_type=="charge-stack"` = ROTATION identity / payment vocabulary (`entity.energy` pool); `econ_bin=="charge-stack"` with sub_shape = accumulator-or-cycle STATE MACHINE (`am_current`/`cycle_charges` fields). Orthogonal; a kit MAY carry both.

---

## Action

- [x] jack-ryan: Gate-2 verdict PASS-WITH-AMENDMENTS (this file). Auto-commit collab repo.
- [x] jack-ryan: decisions-log entries — delegated rulings 9, 10, 11, 12 + this Gate-2 verdict. Auto-commit engine repo.
- [ ] gandalf: fold ERRATA 11–15 into spec (documentation-only; jack-ryan tier can approve on final read).
- [ ] gandalf: push after verdict-read (both engine + collab). Push HELD per Wave-A / ailment precedent.
- [ ] rocket + gamora: NO further action required; both slices land as tagged.
- [ ] Matt (veto surface, NOT owed a decision): delegated rulings 9–12 remain veto-open; Gate-2 found no engine-contradiction, no BLOCK, no ruling reversal.

---

## References (files reviewed, read-only unless noted)

**Governing spec + Gate-1:**
- `canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` (GATE-1 PASS-WITH-AMENDMENTS)
- `agentic_orchestration/jack-ryan/reviews/2026-07-16-wave-b-economy-gate1.md`

**rocket slices (`rocket/v2.10-waveb-1..3`):**
- `src/reincarnated/generation/bc_target_composer.py` — `_DEFERRED_ECON_BINS:97-101`, `_ECON_BIN_COST_TYPE_MAP:249-260`, `check_infeasibility:322-333`, `resolve_cost_type:260-282`
- `src/reincarnated/generation/resource_economy.py` — `RESOURCE_ECONOMY_KEYS:38-69`, enum vocabularies :74-95, `DEFAULT_RESOURCE_ECONOMY:97-131`, `_validate:188-224`
- `src/reincarnated/generation/per_skill_emitter.py` — `_COMMITMENT_BINS:395-406`
- `src/reincarnated/generation/skill_schema.py` — commitment_bin doc :222-227
- `src/reincarnated/generation/bc_target_cell_sampler.py` — `COMMITMENT_BINS:391-392` (unchanged, 972-assert)
- `src/reincarnated/generation/substrate_templates.py` — `W1_4_CHARGE_STACK:295` (REUSED, 25 templates)
- `src/reincarnated/generation/MIGRATION.md` — Wave-B entry (AC-1/AC-2/AC-3 flags)
- `src/reincarnated/generation/notes/wave_b_economy_emit_smoke_2026_07_16.py` — 64/64
- `src/reincarnated/generation/notes/wave-b-economy-emit-math-2026-07-16.md`

**gamora slices (`gamora/v1.9-waveb-1..3`):**
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` — `rs_effective_regen_cap:263-283`, `_sum_reserved_per_proxy_rate:286-303`, PC helpers :310-325, `SpatialEntity` fields :724-748, charge-stack on-kill hook :1801-1806, PC/RC establishment :2676-2708, regen-tick RS :3552-3568, PC drain :3570-3586, AM/RC per-tick :3588-3613, entity_from_class_dict wire-up :4033-4162
- `src/reincarnated/simulation/math/waveb-rs-reservation-sim-2026-07-16.md`
- `src/reincarnated/simulation/math/waveb-pc-persistent-condition-sim-2026-07-16.md`
- `src/reincarnated/simulation/math/waveb-charge-stack-sim-2026-07-16.md`
- `scripts/gamora_waveb_rs_reservation_smoke_2026_07_16.py` — 8/8
- `scripts/gamora_waveb_pc_persistent_condition_smoke_2026_07_16.py` — 8/8
- `scripts/gamora_waveb_charge_stack_smoke_2026_07_16.py` — 8/8
- `src/reincarnated/simulation/MIGRATION.md:8703-8737` — Wave-B CONSUME entry
- `src/reincarnated/simulation/AGENT_STATE.md` — SESSION 64 checkpoint

**Regression:**
- Targeted: `test_w02_bc_target_composer` + `test_spatial_gauntlet_scenarios` + `test_ailment_layer_{gamora,rocket}_slice` + `test_ailment_registry` + `test_cycle13_wave5_gauntlet_sim` + `test_proxy_pairing_layer` + `test_proxy_t4_suite_{eval,strategies}` = **391/391 pass in 1.12s.**
- Known pre-existing REDS (do NOT attribute to Wave-B): 4 naming-vocab + 12 t4_wireup + 3 d15 + 1 season-gen error in rocket seam + water→ice debt `2ae665b`.
