# KR prompt — DoT/ailment activation + physical-DoT scaling fix, with lever-test measurement

**Type:** gandalf-authored brief → **knight-rider to sequence** (gamora implement + run; jack-ryan Gate-2; gandalf design-fit + pre-reg + disposition). Matt-authorized 2026-06-20: *"we should fix DoT/Ailment for both caster and physical (with the extra STR/DEX scaling we need to fix for physical as well)… write a KR prompt for a run to fix these and then test."*
**Author:** gandalf
**Composes with:** the STR disposition (`gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md` §5a — STR ships via the floor with the anchor+adds gap as class texture, shippable only with a focus-fire LEVER); the ailment design-debt findings (`gandalf/findings/2026-06-19-ailment-system-design-debt-and-dps-mechanism-correction.md` — Findings 1 & 2 are exactly this fix).

---

## 0. Why this run (the lever connection)

STR ships, but its one structurally-coherent gap is the **focus-fire-amid-adds** encounter (boss, mini_boss, elite_pack). The design ruling: that gap is shippable *as texture* only if STR has a **lever** — a way to choose to damage the high-HP anchor while the adds swarm. STR's substrate-assigned single-target tool already exists: **bleed DoT**. It just doesn't work — it is INERT in the spatial sim (Finding 1) and mis-scaled to int/wis (Finding 2). This run **activates + correctly-scales DoT** (recompose-first: make the substrate's existing intent *function* — do not invent a new mechanic) and then **MEASURES** whether that closes STR's anchor-gap. It is simultaneously the first empirical probe of Matt's (A)-vs-(B) question: *if the existing tool, once working, suffices → the tools existed (A-leaning); if STR is still below-floor on elite_pack even with bleed live → we need more skills/weapon-effects (B-leaning).*

## 1. The FIX (gamora — math-note-first per Discipline #1; re-confirm all anchors, they may have drifted since 2026-06-19)

- **Finding 1 — activate DoT in the spatial sim (regime-wide; affects caster burn AND physical bleed AND drain together).** Today a DoT `ActiveEffect` is appended to the defender but never advanced: `spatial_engine.py` has no `tick_effects`/DoT advance, and `spatial_resolver_adapter.resolve_spatial_hit` discards the scratch HP mutation. Wire DoT ticking into the spatial engine so burn/bleed/drain actually deal over-time damage in the shipping regime. (Activation is regime-level — you cannot selectively activate one ailment; all three DoT primitives begin ticking together.)
- **Finding 2 — route physical-DoT tick-scaling through the ORIGINATING skill's scaling attribute.** Today `damage_resolver.py:987-988`: `eff_attr = int-or-wis only`; `tick_scale = 1.0 + eff_attr*0.003`. A physical bleed therefore scales on a STR kit's near-zero int/wis. Re-route so the tick scales on the source skill's scaling attribute — **martial source → str/dex, caster source → int/wis** — mirroring the DIRECT-damage path already at `damage_resolver.py:312` (`scaling_stat = attacker.attribute_values.get(_sa_norm, 0)`). This is the "extra str/dex scaling for physical." Caster burn is UNCHANGED by this (it already reads int/wis); the fix only corrects the physical case.

**Discipline — recompose-first, NO magnitude re-tune this pass.** Implement the mechanism faithfully with the EXISTING `0.003` coefficient. Do **not** re-tune DoT magnitude in this run. The run's PURPOSE is to measure the delta so the tuning call is made on data, not guessed. Math-note-first: gamora estimates the expected per-tick and full-fight DoT contribution BEFORE wiring, so the power-injection size is sanity-checked against the bands.

## 2. The TEST (gamora harness — MEASUREMENT-ONLY)

- Reuse the proven `str_9pass_floor_all18` harness (jack-ryan Gate-2 PASS, `612c1a8`) with **DoT ACTIVE**. tier_1-bypassed (same trap-avoidance — drive tier_2 on all shells). Faithful power. Fix the **intra-run seed-stride overflow** jack-ryan flagged (§11.1: adopt the production `*10_000`/`*1_000`/`+enc_idx` layout) before re-use, and use a fresh seed base disjoint from `[700000,766703]` and `[619000,684303]` (Discipline #3).
- **Subjects:** STR (the lever test) + dex/int/wis (controls + caster-burn-impact measure).
- **MEASUREMENT-ONLY:** do **NOT** touch `ENCOUNTER_COHORT_KPM_BAND` or the production gate. Bands stay as-is so the shift is visible *against the current bands*.

## 3. The three questions the run answers

1. **Lever test (STR anchor-gap).** Does STR's **elite_pack** KPM rise from below-floor (current max-cell 3.40 vs 5.65 floor) into band? Does STR's **boss** survive+kill rise from 0.000 (boss timeout drop)? → does bleed-as-lever close the gap STR's allocation problem opens?
2. **Band-shift magnitude (re-fit dependency).** How much does EVERY cohort's clear-room KPM rise with DoT live? This is the power-injection Finding 1 flagged — it sizes the downstream band re-fit. (Casters already sit near/above some clear ceilings; activating burn pushes them further above — expect worse above-ceiling clipping, which is a band-fit artifact to re-fit, not real over-performance.)
3. **Physical-vs-caster symmetry.** With the scaling fix, does physical bleed contribute comparably to caster burn (each on its own attribute)? The fairness check that the substrate's bleed→physical assignment now actually funds martial kits.

## 4. CAUTIONS (load-bearing)

- **Power injection = a band RE-FIT event, and that is NOT this run.** Activating DoT shifts every band. This run MEASURES the shift; it does **not** re-fit bands or re-touch the gate. The band re-fit is a SEPARATE downstream step (gamora sim + jack-ryan Gate-2) once DoT magnitude is decided. Do not conflate mechanism-fix with band-re-fit.
- **Semantic-shift declaration (jack-ryan).** DoT going live changes every KPM/DPS number; any telemetry field capturing combat output shifts meaning across this boundary — declare it (as the DPS field was).
- **Magnitude-tuning is downstream + data-driven.** Measure first.
- **Out of scope:** the DEFERRED control-ailment-damage-signatures proposal (wind cut+bleed, earth thorny-root, water cold-burn). This run fixes the EXISTING DoT ailments only — do not pull that in.
- **Finding 3** (math-note §1.1 "DoT folds into the per-hit float" doc error) becomes genuinely misleading once DoT is non-zero — correct it as part of this work.

## 5. Seam routing (knight-rider sequences)

- **gamora:** math note (expected DoT contribution) → implement Findings 1 & 2 → seed-stride fix → run the DoT-active harness → results + math note. (Engine simulation seam: `spatial_engine.py`, `damage_resolver.py`, `spatial_resolver_adapter`.)
- **gandalf:** design-fit on the source-attribute routing (martial→str/dex, caster→int/wis mapping correctness); **pre-register** the interpretation of all three measured outcomes BEFORE data lands; rule the lever disposition.
- **jack-ryan:** Gate-2 — mechanism correctness, V-gates, NO production-gate regression, semantic-shift declaration, band-re-fit dependency recorded, seed-stride fix verified.

## 6. Hand-back

gamora → DoT-active harness results (STR anchor-shell delta; all-cohort band-shift magnitude; physical-vs-caster symmetry) + math note. jack-ryan Gate-2. gandalf → **lever disposition**: does the DoT lever close STR's anchor-gap? is magnitude tuning needed? does STR still ship-via-floor, now with a *working* lever? → feeds directly into the (A)-vs-(B) skill investigation (this run is its first probe).

---

**Signed:** gandalf, 2026-06-20. Activate the tool the substrate already gave STR, scale it on the attribute STR actually has, and measure whether that turns the anchor-gap from a wall into a choice — without touching the bands until we know how far they moved.
