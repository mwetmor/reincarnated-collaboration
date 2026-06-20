# Dispatch — 2026-06-20 — gamora — DoT/ailment activation + mitigation-symmetry, 3-arm lever/confound MEASUREMENT run

**From:** knight-rider
**To:** gamora (simulation seam)
**Approved by:** Matt 2026-06-20 — *"we should fix DoT/Ailment for both caster and physical (with the extra STR/DEX scaling for physical) … and now the armor/resist asymmetry — write a KR prompt for a run to fix these and then test."* AMENDS the gandalf brief `gandalf/requests/2026-06-20-dot-ailment-activation-and-physical-scaling-fix-run-brief.md` (commit `f42915f`): the fix sections of that brief stand; gandalf's armor/resist verification adds a third fix (F4) and restructures the test into 3 arms (A/B/C).
**Estimated effort:** multi-hour, Pattern B (own session memory). Math-note-first → implement F1/F2/F3/F4 (production combat changes) → fix the seed-stride overflow → run Arms B & C of the reused `str_9pass_floor_all18` harness → aggregate A/B/C deltas → emit results + math note.
**Acceptance:** clean per-arm JSON + gandalf-consumable A/B/C comparison table answering Q1–Q4 (below), with each cell band-fit-classified against the **CURRENT untouched bands**; math note confirms the fix mechanics + verify-gates BEFORE any number is read; both semantic-shift boundaries declared; band-refit dependency recorded; seed-stride fix verified. jack-ryan Gate-2 PASS.

> **ADDENDUM (post-Gate-1; gandalf pre-registration committed `df1023b`) — F4 is a MEASUREMENT INSTRUMENT, not a shipping resistance design.** The math note MUST explicitly mark F4's uniform symmetric resistance (`armor/(armor+3000)` applied flat across all elements) as the correct instrument *for this confound-isolation run only* — it is NOT a production boss-resistance design. The genre-correct shipping pattern is per-element resistance *profiles* (PoE per-element, D2 immunities, Grim Dawn spreads) that reward damage-type build-crafting. **Uniform-for-measurement now; profiled-for-shipping is a separate downstream design step** — do NOT let the uniform resistance silently harden into the shipping boss. State this framing in the math note so the band-refit step does not inherit uniform-resist as a design commitment. (gandalf design-fit: F2 source-attr routing ships as-is, genre-correct; F4 flagged instrument-only as above.)

> **RE-SCOPE ADDENDUM (Matt-authorized 2026-06-20, post gamora math-note-first stop) — Path 1: Arm B only; Arm C deferred.** gamora's anchor-confirmation pass discovered the run's premise does not survive contact with the population: **0 of 66 season-001 faithful-power configs carry ANY ailment effect; STR carries zero `tick_damage` on any skill** — the substrate-assigned bleed lever is *absent from generation*, not merely inert in the sim. Matt confirmed **STR was DESIGNED to carry bleed** → this is a **generation bug at the rocket seam**, not a design gap. Consequences:
> - **Arm C (F1+F2 DoT lever) is structurally NULL for this population** (≡ Arm B byte-for-byte; the "DoT ticks in Arm C" smoke assertion cannot pass without a DoT source). **DEFERRED** until rocket restores STR's designed bleed emission + the population is regenerated. gandalf's pre-registration (`df1023b`) stands and binds to that deferred re-fire.
> - **Arm B (F4 mitigation symmetry) runs NOW** — fully measurable; answers Q2, Q3, and the **armor-confound half of Q1**. F1/F2/F4 still implemented as correct faithful production fixes (recompose-first); both semantic shifts declared; band-refit dependency recorded. Arm C documented as null-for-this-population pending the rocket fix.
> - **`rotating_elements` = the full 7-substrate registered set** `{fire, water, earth, wind, lightning, holy, shadow}` (gamora confirmed int casts `{earth,fire,lightning,shadow,water}`, wis casts `{earth,holy,shadow,wind}` via per-effect element overrides — a partial set silently under-covers). **`ARMOR_MITIGATION_K` is at `foundation/math_model.py:34`** (not `simulation/`). Q4 tick-bypass CONFIRMED (`effect_resolver.py:68-69`).
> - Parallel: a rocket dispatch diagnoses + fixes the generation bug (STR's designed bleed never emitted). Arm C re-fires after that lands.

---

## 0. Why this run exists (read the gandalf brief `f42915f` fully — this is the short version + the amendment)

The gandalf brief activated DoT and re-scaled physical-DoT so STR's substrate-assigned **bleed** could function as the focus-fire **lever** for its anchor-gap (boss/mini_boss/elite_pack). **gandalf's armor/resist verification then surfaced a confound that must be tested BEFORE the lever:**

> The synthetic endgame mob carries **nonzero armor** but **`elemental_resistances={}`**. Physical attacks eat **8/36/66/90/93%** mitigation across the tiers (swarm → boss); elemental attacks eat **0%**. STR's elite+boss failure maps *exactly* onto this physical-mitigation gradient (boss control: str 0.00 / dex 0.79 / int 0.99 / wis 0.99). **STR's allocation disposition is therefore CONFOUNDED** — we cannot tell how much of STR's gap is a real allocation problem versus an artifact of physical-only mitigation. The run must test the **premise (fair mitigation)** before crediting the **solution (bleed lever)**.

So the run decomposes into three arms and four questions. It is the first empirical probe of Matt's (A)-vs-(B) single-target-skill question, now with the mitigation confound controlled out.

## 1. THE FIX (gamora — math-note-first per Discipline #1; **re-confirm ALL anchors first-hand — they have DRIFTED since the brief was written; KR-observed current lines below**)

> **Anchor-drift notice (KR verified on disk 2026-06-20, Discipline #11/#1.2).** The brief's line citations are stale. Current observed lines — **re-confirm each first-hand before citing in your math note; do not trust these on report, but do not re-walk the brief's stale numbers either:**
> - `_synthetic_mob_dict_for_spatial` → **t4_sim_cycling.py:992** (brief said :1007/:1248). The Pydantic-monster builder with `elemental_resistances={}` is at **:967**; the spatial-dict builder is **:992**; the call site is **:1056**. Confirm WHICH builder feeds the spatial sim path your harness drives.
> - tick-scaling `eff_attr` / `tick_scale` → **damage_resolver.py:987-988** (jack-ryan Gate-1 corrected; brief said :987-988 too — the dispatch draft's :988-989 was off-by-one): `:987` `eff_attr = attacker.attribute_values.get("intelligence",0) or ...get("wisdom",0)`, `:988` `tick_scale = 1.0 + eff_attr*0.003`, `:989` is the `params["tick_damage"]` apply. The DIRECT-damage scaling-attr precedent to mirror is **damage_resolver.py:312** (`scaling_stat = attacker.attribute_values.get(_sa_norm, 0)`).
> - `ARMOR_MITIGATION_K = 3000.0` → **math_model.py:34**.
> - DoT tick loop → **effect_resolver.py ~:62-71** (brief said :69): tick applies `combatant.hp -= tick_dmg` after only `absorb_with_shield(tick_dmg)` — **no `elemental_resistances`/armor lookup on ticks** (this IS the Q4 bypass, jack-ryan-confirmed Gate-1; confirm it holds).
> - **F4 DEFENDER flow (jack-ryan Gate-1 disambiguation):** the spatial-dict builder `_synthetic_mob_dict_for_spatial` (:992, return dict ~:1007 — no `elemental_resistances` key today) flows through `spatial_resolver_adapter.py:228` (`monster_dict.get("elemental_resistances", {})`) into the **DEFENDER**. That `:228` get IS the F4 path — add the resist key to the `:992` builder's return dict. NOTE: the `:967` `elemental_resistances={}` is the Pydantic-monster builder (NOT the spatial path), and `spatial_resolver_adapter.py:196` `elemental_resistances={}` is the **ATTACKER** projection (attacker resist is not read for mitigation — do NOT edit :196). The DEFENDER elemental-resist lookup at resolve time is `damage_resolver.py:470`.
> - F1 scratch-HP-discard locus → `spatial_resolver_adapter.resolve_spatial_hit` (the spatial path discards the DoT scratch-HP mutation; persist it).

- **F1 — activate DoT ticking in the spatial sim (regime-wide; burn + bleed + drain together).** Today a DoT `ActiveEffect` is appended to the defender but never advanced in the spatial path: `spatial_engine.py` has no `tick_effects`/DoT advance, and `spatial_resolver_adapter.resolve_spatial_hit` discards the scratch-HP mutation. The tick MATH already exists and is correct in `effect_resolver.py` (~:62-71) — the spatial path simply never calls it / never persists its mutation. Wire DoT ticking into the spatial engine so burn/bleed/drain deal over-time damage in the shipping regime. Activation is regime-level — you cannot selectively activate one ailment; all three DoT primitives begin ticking together.
- **F2 — route physical-DoT tick-scaling through the ORIGINATING skill's scaling attribute.** At `damage_resolver.py:988-989`, `eff_attr` reads int-or-wis only, so a physical bleed scales on a STR kit's near-zero int/wis. Re-route so the tick scales on the **source skill's** scaling attribute — **martial source → str/dex, caster source → int/wis** — mirroring the direct-damage path at `damage_resolver.py:312`. Caster burn is UNCHANGED (it already reads int/wis); the fix only corrects the physical case.
- **F4 (NEW — the confound control) — mitigation symmetry.** In `_synthetic_mob_dict_for_spatial` (t4_sim_cycling.py:992), add an elemental-resistance key to the return dict (~:1007) so it flows through `spatial_resolver_adapter.py:228` into the DEFENDER, matching the physical-mitigation curve the armor already imposes:
  `"elemental_resistances": {e: r for e in rotating_elements}` where `r = mob_armor / (mob_armor + ARMOR_MITIGATION_K)` (ARMOR_MITIGATION_K = 3000.0, math_model.py:34).
  Casters then eat **exactly what physical eats** at each tier, via the DEFENDER lookup `damage_resolver.py:470` (`res = defender.elemental_resistances.get(element, 0.0)`).
  **CRITICAL (jack-ryan Gate-1 Fold A) — `rotating_elements` coverage is an arm-isolation integrity risk, not a doc nicety.** The resolver looks up resist by the **ATTACKER's skill element**, not the mob's `dominant_element`. If `rotating_elements` does not cover every element the int/wis caster cohorts actually attack with, the uncovered elements silently resolve to `0.0` resist — and the A→B caster drop (Q2) is partial, which CONFOUNDS Q2 and dirties the otherwise-clean A→B isolation. Make `rotating_elements ⊇ {elements the season-001 caster cohorts cast}` and ENFORCE it as a smoke assertion (see §7) — Arm B caster KPM must drop for int AND wis, not just one.
- **F3 — correct the math-note §1.1 "DoT folds into the per-hit float" doc error.** It becomes genuinely misleading once DoT is non-zero. Fix it as part of this work.

**DISCIPLINE — recompose-first; NO magnitude re-tune AND NO armor-level re-tune this pass (Discipline: recompose-first; #20-adjacent faithful-implement).** Implement all four faithfully with the EXISTING coefficients (`0.003` tick coefficient; the existing `mob_armor` values; the existing `ARMOR_MITIGATION_K = 3000.0`). The run's PURPOSE is to MEASURE the deltas so the tuning call is made on data, not guessed. Magnitude tuning AND armor-level tuning are BOTH downstream + data-driven.

> **These are PRODUCTION COMBAT CHANGES, not harness-only.** Unlike the prior `str_9pass` run (read-only diagnostic), F1/F2/F4 change the SHIPPING combat-resolution path. The production SHIP GATE (bands, `gauntlet_pass`, floor) stays UNTOUCHED — but production combat OUTPUT changes, which means the bands are now **stale and must be refit downstream**. This is a deliberate, declared intermediate state. See §4 Cautions + the jack-ryan band-refit-dependency record.

## 2. THE TEST (gamora harness — MEASUREMENT-ONLY; 3 arms)

Reuse the proven `str_9pass_floor_all18` harness (jack-ryan Gate-2 PASS, commit `612c1a8`): tier_1-bypassed (drive tier_2 directly on all 18 shells), faithful power (max-profile investment, flip #3 default ON), all 18 `ENDGAME_ENCOUNTER_CATALOG` shells × 4 cohorts × the 66-config season-001 faithful-power population.

**FIX the intra-run seed-stride overflow jack-ryan flagged (math-note §11.1): adopt the production `*10_000` / `*1_000` / `+enc_idx` seed layout** before re-use, and use a **fresh seed base disjoint from `[700000,766703]` AND `[619000,684303]`** (Discipline #3 — no parallel regens of the same seed namespace).

The harness must gate the three fixes by **arm** so the change-sets are cleanly separable (this is a single-lever-per-transition decomposition — Discipline #24 isolation; each transition toggles exactly ONE mechanism):

| Arm | DoT (F1+F2) | Mitigation symmetry (F4) | Source | Run? |
|---|---|---|---|---|
| **A** | inert | asymmetric (physical-only) | = the existing baseline | **Reference — do NOT re-run.** Pull STR/dex/int/wis cells from the `612c1a8` `str_9pass_floor_all18` artifact. |
| **B** | inert | **SYMMETRIC (F4 only)** | this run | **RUN** |
| **C** | **active (F1+F2)** | SYMMETRIC (F4) | this run | **RUN** |

- **A→B** isolates the mitigation confound (F4 only). **B→C** isolates the bleed lever (F1+F2 on top of symmetric mitigation).
- **Subjects:** STR (the lever/confound test) + dex / int / wis (controls + caster-impact measure).
- **Bands UNTOUCHED** — classify every A/B/C cell against the **CURRENT** `ENCOUNTER_COHORT_KPM_BAND` so every shift is *visible against the bands you know*. Do NOT re-fit, do NOT touch the gate (V6 holds for the GATE; the COMBAT ENGINE is the intended change).

## 3. THE QUESTIONS the run answers

- **Q1 — decompose STR's gap (A→B→C).** How much of STR's elite/boss failure is **armor-confound** (the A→B shift once casters eat what physical eats), how much is **residual allocation** (what STR still fails at B, mitigation-fair but bleed-inert), and how much is **closed by the bleed lever** (the B→C shift)? This is the headline decomposition.
- **Q2 — caster impact (A→B).** How far do int/wis KPMs DROP once they eat resistance symmetrically? (This tells us how much caster dominance was a free-mitigation artifact; sizes the downstream refit.)
- **Q3 — boss absolute difficulty (B).** Under symmetric ~90–93% mitigation at the boss tier, is boss survive+kill viable for ANY attribute? If NO → Matt's armor-nerf for the boss is warranted (downstream, data-driven — **NOT this run**).
- **Q4 — DoT symmetry (C).** Does physical bleed contribute comparably to caster burn, each on its OWN attribute? Confirm ticks BYPASS mitigation as expected (effect_resolver.py ~:62-71 — tick applies `hp -= tick_dmg` with only `absorb_with_shield`, no armor/resist).

## 4. CAUTIONS (load-bearing)

- **TWO band-shift events now** — DoT activation (F1+F2) AND mitigation symmetry (F4). This run MEASURES the combined shift against the current bands; it does **NOT** refit bands or touch the gate. The band refit is a SEPARATE downstream step (gamora sim + jack-ryan Gate-2) once magnitude + armor-level decisions are made on this run's data.
- **Production combat changes land on main while bands are stale.** F1/F2/F4 auto-commit as in-scope cycle work (team commit discipline). That means production combat OUTPUT changes before the bands are refit — a known, declared intermediate state. jack-ryan records the **band-refit dependency** at Gate-2 so the gate is not trusted until refit. The fix is committed; the gate-trust is explicitly suspended pending refit.
- **Semantic-shift declaration (jack-ryan, Discipline #12) — TWO boundaries.** DoT-live AND resist-live each change every KPM/DPS number. Declare the boundary on every affected combat-output telemetry field (as the DPS field was declared). Two declarations, not one.
- **Magnitude AND armor-level tuning are downstream + data-driven.** Measure first. No re-tune this pass.
- **Out of scope:** the DEFERRED control-ailment damage-signatures proposal (wind cut+bleed, earth thorny-root, water cold-burn). This run fixes the EXISTING DoT ailments only — do NOT pull that in.

## 5. Cross-seam contract change? (Principle 6 gate — KR completes at authoring time)

Does this dispatch add/modify/rename/remove any field on a telemetry schema table, fight_log dict key, loadout dict key, export packet, or inter-seam fixture?

**NO schema change — Round-trip: not applicable.** F1/F2/F4 change combat-resolution NUMBERS and the synthetic-mob `elemental_resistances` VALUE; they do not add/rename/remove any telemetry SCHEMA field, fight_log key, or export-packet field. No MIGRATION.md required for a schema contract. **HOWEVER** — the meaning of every combat-output field shifts across this boundary, so the **semantic-shift declaration (Discipline #12) IS required** (two boundaries, §4) and is recorded by jack-ryan at Gate-2. (Distinguish clearly: no MIGRATION.md schema change; semantic-shift declaration mandatory.)

## 6. Math-before-code — Discipline #1 (THE GATE; FIRST, before any fix or harness code)

Author a math note (`simulation/math/dot-ailment-mitigation-symmetry-run-2026-06-20.md`) that, BEFORE any number is trusted:

1. **Estimates the expected DoT contribution** (per-tick and full-fight, per tier) with the existing `0.003` coefficient, so the F1+F2 power injection is sanity-checked against the bands BEFORE wiring (math-note-first; the injection must not silently dwarf or vanish against the bands).
2. **Estimates the symmetric-mitigation reduction per tier** — compute `r = mob_armor/(mob_armor+3000)` at each of the 4 tiers from the actual `mob_armor` values, confirm the 8/36/66/90/93% physical curve gandalf cited, and project the caster KPM drop A→B (Q2 pre-estimate).
3. **Confirms the fix mechanics with first-hand line citations (drifted anchors re-confirmed):** F1 spatial-tick wiring locus + that effect_resolver tick math is reused (not re-derived); F2 source-attr routing mirrors `damage_resolver.py:312`; F4 resolver elemental-resist path (`damage_resolver.py:470`) is the one the spatial path traverses; F3 doc fix.
4. **Confirms the verify-gates** (carry forward the `str_9pass` V1–V6, re-scoped to 3 arms):
   - **V1 (tier_2 ran on all 18 in EACH run arm; no defaulted-0.0 masquerading as a measured miss)** — LOAD-BEARING, the generalized trap. Assert every cell's KPM came from an executed batch (`batch.n_fights == expected_n`; `n_fights==0` = FAIL, fail loud, no table emitted).
   - **V2 (faithful power)** — max-profile investment default chain, not the stripped floor.
   - **V3 (proxy-inclusive KPM)** — `mobs_killed`/min, attribution-agnostic (DoT/proxy kills count regardless of final-blow source — newly relevant now that bleed kills exist in Arm C).
   - **V4 (clear-shell win condition)** — clear shells resolve on `all_mobs_killed`; clear-shell integrity check `Σ termination_counts == n_fights`; boss-shell V1 self-consistency (`b_dead == wins == winner_player`) retained for the 4 boss shells.
   - **V5 (single regime)** — current spatial sim + current mobs/min + faithful power; NO old-scale KPM mixed in; fingerprint the regime AND the arm (DoT on/off, mitigation sym/asym) in output metadata.
   - **V6 (measurement-only — GATE scope)** — production SHIP GATE untouched: no edits to the bands, `gauntlet_pass`/`eligible_encounters_passed`, the floor, or the tier_1 routing. **NOTE the scope boundary explicitly: V6 protects the GATE; the COMBAT ENGINE (F1/F2/F4) is the intended production change — call this distinction out in the note so Gate-2 reads it correctly.**
   - **(new) Arm-isolation gate** — confirm A→B toggles ONLY F4 and B→C toggles ONLY F1+F2 (Discipline #24 single-lever isolation); no other variable moves between arms (same seeds-by-construction, same population, same shells, same bands).
5. **Seed layout** — document the production `*10_000`/`*1_000`/`+enc_idx` stride fix and the fresh disjoint seed base (§11.1 overflow corrected; Discipline #3).

## 7. Scope
- [ ] Math note FIRST (`simulation/math/dot-ailment-mitigation-symmetry-run-2026-06-20.md`) — DoT-contribution estimate; symmetric-mitigation per-tier reduction estimate (confirm the 8/36/66/90/93% curve); fix-mechanic citations (drifted anchors re-confirmed first-hand, subdir-correct paths); V1–V6 + arm-isolation gate; seed-stride fix + fresh disjoint base; F3 doc-error correction noted.
- [ ] Implement **F1** (activate DoT ticking in the spatial path — reuse effect_resolver tick math; persist the scratch-HP mutation in `resolve_spatial_hit`).
- [ ] Implement **F2** (route physical-DoT tick-scaling through the source skill's scaling attr — martial→str/dex, caster→int/wis — mirroring `damage_resolver.py:312`; caster burn unchanged).
- [ ] Implement **F4** (mitigation symmetry in `_synthetic_mob_dict_for_spatial`: `elemental_resistances={e: mob_armor/(mob_armor+ARMOR_MITIGATION_K) for e in rotating_elements}`).
- [ ] **F3** doc-error correction (math-note §1.1 "DoT folds into per-hit float").
- [ ] Seed-stride overflow fix (production `*10_000`/`*1_000`/`+enc_idx`; fresh base disjoint from `[700000,766703]` & `[619000,684303]`).
- [ ] Arm-gating in the harness: A = reference (pulled from `612c1a8`, NOT re-run); B = F4 only; C = F1+F2+F4. Single-lever-per-transition verified.
- [ ] Smoke-test (Disc #2 + #2.1): tiny n_fights dry-run on ONE kit × one-of-each clear type + one boss × one cohort, for **both run arms B and C**, confirming: tier_2 fires on clear shells (the trap), DoT actually ticks in Arm C (non-zero `dot_damage`), Arm B mitigation is symmetric, band-fit classification populates, integrity checks pass. **`rotating_elements`-coverage assertion (Fold A): Arm B caster KPM must drop vs Arm A for BOTH int AND wis cohorts** — if either does not drop, the resist dict under-covers that cohort's attack elements; FAIL loud, do not proceed to the full run. Resource-scaling sanity: peak memory of the full 2-arm × 18×4×66 run bounded vs host RAM (project the 2× scaling vs the single-arm `str_9pass` run).
- [ ] Run Arms B & C at full tier_2 `n_fights` across STR + dex/int/wis; aggregate per arm; compute A→B, B→C, A→C deltas per cohort × clear-type × boss.
- [ ] Band-fit classification (below-floor / in-band / above-ceiling, record the SIDE) per cell per arm against the CURRENT untouched bands.
- [ ] Clean per-arm JSON + gandalf-consumable A/B/C comparison table → `agentic_orchestration/cycle-14-wave-5-season-001/` (suggested `dot-mitigation-symmetry-3arm-2026-06-20.json` + `.txt`).
- [ ] MIGRATION.md: not applicable (no schema contract change; note explicitly). **Semantic-shift declaration: REQUIRED — two boundaries (DoT-live, resist-live); coordinate with jack-ryan at Gate-2.**
- [ ] AGENT_STATE.md updated at session end.
- [ ] AUTO-COMMIT the F1/F2/F3/F4 engine changes + harness + math note + output (in-scope cycle work, team commit discipline). **DO NOT PUSH** — record the unpushed commit list in the completion record.

## 8. Acceptance criteria
- [ ] Math note confirms V1–V6 + arm-isolation gate WITH first-hand line citations (subdir-correct) BEFORE the table is read as data. V1 especially (no defaulted-0.0 cells in either run arm).
- [ ] **If V1 fails (any clear-shell cell carries a KPM not from an executed batch): STOP, do not emit, report.**
- [ ] DoT demonstrably TICKS in Arm C (smoke shows non-zero `dot_damage`); physical bleed scales on str/dex in Arm C (F2 verified — a STR kit's bleed is non-trivial, not near-zero).
- [ ] Mitigation is symmetric in Arms B & C (smoke/full shows caster elemental damage now eats the same per-tier mitigation as physical; F4 verified at `damage_resolver.py:470`). **`rotating_elements` covers both int AND wis cohort attack elements — both caster KPMs drop A→B (Fold A); if either fails to drop, the resist dict is under-covered → STOP.**
- [ ] Arm isolation holds: A→B differs ONLY by F4; B→C differs ONLY by F1+F2 (same seeds/population/shells/bands).
- [ ] Q1–Q4 answerable from the artifact (STR gap decomposed A→B→C; caster A→B drop; boss-B viability for any attribute; physical-vs-caster DoT symmetry + tick-bypass confirmed).
- [ ] Band-fit recorded per cell per arm with the failure SIDE, against the CURRENT untouched bands (V6 GATE scope).
- [ ] Production SHIP GATE untouched (bands / `gauntlet_pass` / floor / tier_1 routing) — V6 GATE scope (combat-engine change is intended + declared).
- [ ] Two semantic-shift declarations recorded; band-refit dependency recorded (jack-ryan Gate-2).
- [ ] n per attribute cell ≥ the `str_9pass` cell sizes (not underpowered).
- [ ] Round-trip smoke: not applicable — no cross-seam schema contract change.

## 9. Out of scope (explicit non-goals)
- **DO NOT re-tune DoT magnitude** (keep the `0.003` coefficient). Measure first.
- **DO NOT re-tune armor levels or `ARMOR_MITIGATION_K`** (keep `3000.0` and the existing `mob_armor`). The armor-nerf question (Q3) is a downstream, data-driven call — NOT this run.
- **DO NOT re-fit or re-touch the KPM bands or the ship gate** (V6 GATE scope). Measure against current bands.
- **DO NOT pull in the DEFERRED control-ailment damage-signatures proposal.** Existing DoT ailments only.
- **DO NOT re-run Arm A** — pull it from the `612c1a8` `str_9pass_floor_all18` artifact as the reference baseline.
- **DO NOT rewrite the harness from scratch** — extend/reuse the Gate-2-blessed `str_9pass_floor_all18` harness (same bypass, population, V1 assertion); add only arm-gating + the seed-stride fix + A/B/C aggregation.
- **DO NOT push to remote.**

## 10. Open questions for the agent to resolve (document the decision in the math note)
- **Arm-gating mechanism.** How do you toggle F1+F2 and F4 independently per arm — env/flag, a config dict threaded into the synthetic-mob builder + the spatial tick path, or a parameterized harness driver? Whatever you choose, the production DEFAULT once committed must be F1+F2+F4 ALL ON (that is the shipping fix); the arm-gating is a harness-level override for the B-vs-C measurement, not a production toggle. State which and why.
- **`rotating_elements` set for F4 (ELEVATED to integrity-critical per jack-ryan Gate-1 Fold A — NOT merely "document it").** The resolver looks up resist by the ATTACKER's skill element, not the mob's `dominant_element`. Determine the full set of elements the season-001 int/wis caster cohorts actually attack with, and make `rotating_elements` a superset of it. Under-coverage → uncovered elements resolve to 0.0 resist → partial A→B caster drop → Q2 confounded + A→B isolation dirtied. The §7 smoke assertion (both int AND wis KPMs drop A→B) is the enforcement; document the element set you confirmed and why it is complete.
- **Tick mitigation-bypass confirmation (Q4).** Confirm first-hand that DoT ticks do NOT route through the elemental-resist/armor mitigation (effect_resolver applies `hp -= tick_dmg` after only `absorb_with_shield`). If they DO get mitigated anywhere, flag it loudly — it changes the Q4 symmetry interpretation.
- **Arm-A baseline provenance.** Confirm the `612c1a8` `str_9pass_floor_all18` artifact's cells are directly comparable (same population, same faithful-power, same bands) so A→B deltas are apples-to-apples; if any drift, note it.

## 11. Hand-back (what KR returns to gandalf + jack-ryan)
On completion, append a completion record with:
- **THE DECOMPOSITION (Q1):** STR's elite/boss gap split into armor-confound (A→B) vs residual allocation (B) vs bleed-lever-closed (B→C), per cohort × clear-type × boss.
- **Q2:** int/wis KPM drop A→B (the caster free-mitigation artifact, sized).
- **Q3:** boss-tier (Arm B) survive+kill viability for any attribute under symmetric ~90–93% mitigation — the input to Matt's armor-nerf decision (downstream).
- **Q4:** physical-bleed vs caster-burn contribution each on its own attribute (Arm C); tick mitigation-bypass confirmed.
- The dex/int/wis CONTROL pass counts (corroboration the harness is sound — if a control craters unexpectedly, the harness is suspect, not the result).
- V1–V6 + arm-isolation verify status (each PASS/FAIL with the line cited).
- The two semantic-shift declarations + the band-refit dependency record.
- The output artifact path + the unpushed commit list (engine F1/F2/F3/F4 + harness + math note + output).
- Any surprise vs gandalf's pre-registered A/B/C interpretation.

This feeds: gandalf's **lever/confound disposition** — (1) how much of STR's gap was measurement-artifact (armor-confound) vs real allocation; (2) does the bleed lever close the residual gap; (3) revised STR ship characterization (ships-via-floor with a *working* lever?); (4) recommendation on Matt's armor-nerf for the boss — and onward into the (A)-vs-(B) skill investigation.

## 12. References
- The brief this AMENDS: `agentic_orchestration/gandalf/requests/2026-06-20-dot-ailment-activation-and-physical-scaling-fix-run-brief.md` (commit `f42915f`)
- Composes with: `gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md` §5a (STR ships-via-floor with a focus-fire lever); `gandalf/findings/2026-06-19-ailment-system-design-debt-and-dps-mechanism-correction.md` (Findings 1 & 2)
- The harness to reuse (Gate-2 PASS `612c1a8`): `str_9pass_floor_all18` + its dispatch `agentic_orchestration/dispatches/2026-06-19-gamora-str-9pass-floor-all18-clearroom-harness.md`
- Engine anchors (RE-CONFIRM first-hand — drifted): `_synthetic_mob_dict_for_spatial` t4_sim_cycling.py:992 (return dict ~:1007; call site :1056; Pydantic builder :967 — NOT the spatial path); tick-scaling damage_resolver.py:987-988 (:989 = apply); direct-damage scaling precedent damage_resolver.py:312; DEFENDER elemental-resist lookup damage_resolver.py:470; F4 defender-flow `spatial_resolver_adapter.py:228` (`monster_dict.get("elemental_resistances", {})`) — NOT the :196 attacker projection; `ARMOR_MITIGATION_K=3000.0` math_model.py:34; DoT tick loop effect_resolver.py ~:62-71 (bypasses resist/armor); F1 scratch-HP locus spatial_resolver_adapter.resolve_spatial_hit
- The clear-room bands (CURRENT, untouched): `gauntlet_sim.py:316-322` (`ENCOUNTER_COHORT_KPM_BAND`, cohort-invariant); floor `gauntlet_sim.py:158` (`=9`)
- Disciplines: #1/#1.2 (math-before-code, code-citation), #2/#2.1 (smoke + resource-scaling), #3 (distinct seeds), #11 (citation-correction), #12 (semantic-shift), #24 (single-lever isolation)

---

## Completion record (gamora, 2026-06-20 — Path 1: Arm B live, Arm C deferred)

**Status:** COMPLETE. F1/F2/F3/F4 production combat fixes implemented (recompose-first, existing coefficients, no magnitude/armor re-tune); Arm B mitigation-symmetry run executed to completion (4752 cells × 20 fights, exited clean; 67.3 MB peak RSS, 1324.9s wall). Math-note-first per Discipline #1. Committed (NOT pushed). Returns to gandalf + jack-ryan Gate-2 via KR.

### THE DECOMPOSITION (Q1) — STR's elite/boss gap, armor-confound half (A→B)
- **STR moves almost nothing A→B** (open_arena −0.3%, chokepoint −0.3%, magic −0.5%, elite +0.9%, boss 0.0%, mini_boss 0.0%). STR is **94% physical** (136/144 attacks) so it ALREADY ate the armor curve in Arm A; F4 only re-touches its 6% elemental tail. **Interpretation: STR's elite/boss gap is NOT an armor-confound artifact** — making mitigation fair to casters does not move STR, because STR was already paying the physical curve. The residual STR gap at Arm B is therefore **real allocation / kit-shape**, not a free-mitigation asymmetry. (The bleed-lever-closes half — B→C — is the DEFERRED Arm C, structurally null for this population: 0/66 carry a DoT source.)

### Q2 — caster A→B drop (the free-mitigation artifact, sized)
Mean observed_kpm A→B drop (F4 = only lever), per tier:
| tier | INT Δ% | WIS Δ% |
|---|---|---|
| open_arena (swarm) | −8.6% | −8.4% |
| chokepoint_corridor | −8.3% | −7.7% |
| magic_pack | −30.8% | −32.0% |
| elite_pack | −76.5% | −79.2% |
| boss_with_adds | −93.4% | −94.3% |
| mini_boss | −100.0% | −99.6% |
The caster free-mitigation advantage was **enormous and tier-escalating** — casters got ~76-94% of their elite/boss KPM for free because elemental ate 0% while physical ate 66-93%. This sizes the downstream band refit: the elite/boss KPM bands are badly stale for elemental attackers.

### Q3 — boss-tier (Arm B) survive+kill viability under symmetric ~90-93% mitigation
**survive+kill = 0.000 for ALL FOUR attributes** (str/dex/int/wis), **100% timeout**, n = 3840/3840/3840/9600 fights. Under symmetric boss mitigation NO attribute can survive+kill in the time cap. **This is the input to Matt's boss armor-nerf decision** (downstream, data-driven — NOT this run). The boss is currently unkillable-in-time once casters stop getting free mitigation.

### Q4 — physical-bleed vs caster-burn DoT symmetry + tick mitigation-bypass
**Tick mitigation-bypass CONFIRMED first-hand** (`effect_resolver.tick_effects:62-72`: `hp -= tick_dmg` after only `absorb_with_shield`; no armor/resist lookup). The physical-bleed-vs-caster-burn symmetry contribution is **not measurable for this population** (Arm C deferred — 0/66 DoT source). By construction F2 makes each scale on its own attribute and both bypass mitigation → symmetric; measured when rocket's bleed lands.

### Control read (dex/int/wis corroboration)
- **DEX A→B drop is EXPECTED, not a harness fault.** DEX is **83% elemental** (120/144: fire/earth/shadow/water) → eats the new symmetric resist like a caster (elite −72.8%, boss −93.1%, mini_boss −92.8%). The **STR-vs-DEX asymmetry corroborates F4** mitigates by skill ELEMENT (`damage_resolver.py:470`) not attribute label: mostly-elemental DEX moves with casters; mostly-physical STR does not. Do NOT read DEX's drop as STR-gap evidence.
- int/wis behave as the caster Q2 read; cohort-agreement spread = 0 within each attribute (harness sound).

### Verify-gates (V1–V6 + arm-isolation) — JSON-confirmed
- **V1 PASS** (no defaulted-0.0 masquerading): `metadata.v1_integrity_all_pass = True`; every clear-shell KPM from an executed batch (`harness :586-593`).
- **V2 PASS** (faithful power): max-profile flip #3 ON (`combatant_from_player_class:136`).
- **V3 PASS** (proxy-inclusive KPM): `mobs_killed/min` attribution-agnostic (relevant only at Arm C re-fire).
- **V4 PASS**: `metadata.v4_integrity_all_pass = True`; Σ termination_counts == n_fights.
- **V5 PASS** (single regime): fingerprint `spatial_current_mobs_per_min_faithful_DoT-on_mitigation-symmetric`.
- **V6 PASS** (measurement-only — GATE scope): production SHIP GATE untouched (`production_gate_modified=False`); COMBAT ENGINE changed by intent (`production_combat_engine_modified=True`).
- **Arm-isolation PASS**: A→B toggles ONLY F4 (F1/F2 inert: 0 DoT source, proven §0). Authoritative isolation = INTERNAL matched-seed Fold-A (`paired_seed:true`): int drops=True (Δ−2.894), wis drops=True (Δ−4.7466), both_drop=True.

### Semantic-shift declarations (2) + band-refit dependency
1. **DoT-live (F1)** — combat-output fields carry over-time damage when a DoT source exists (null for this population; field semantic changes regardless). Declared on all combat-output telemetry fields.
2. **resist-live (F4)** — every elemental-attacker KPM/DPS DROPS under symmetric resist (the live measured shift). Declared on all combat-output telemetry fields.
- **Band-refit dependency RECORDED:** F1/F2/F4 shift production combat OUTPUT while `ENCOUNTER_COHORT_KPM_BAND` is UNTOUCHED → bands STALE → must be refit downstream (gamora sim + jack-ryan Gate-2) once magnitude + armor-level decisions are made. Until refit: gate committed, gate-TRUST SUSPENDED. **No MIGRATION** (no schema/key contract change).

### GATE-2 FLAG (authoritative-comparison framing) — math note §5.1
The **EXTERNAL A→B table** (this run's Arm B vs the `612c1a8` Arm A artifact) carries **cross-artifact seed/sampling noise** (different seed namespaces) — at SMOKE n it showed WIS **+24% on open_arena** (wrong-signed) that washed out at full n. The **rigorous lever-isolation is the INTERNAL `fold_a_caster_drop_check` matched-seed f4_off/f4_on Fold-A** (`paired_seed:true`). Gate-2: credit the INTERNAL Fold-A for "F4 moves the lever"; treat the external table's swarm/magic-tier deltas as noise-bounded (corroborative-only). Documented in math note §5.1 as authoritative.

### Arm C — documented deferred-null
Arm C (F1+F2 DoT lever) is **structurally NULL for this population** (0/66 configs carry any ailment effect or nonzero `tick_damage` — STR's designed bleed is ABSENT FROM GENERATION = rocket-seam bug, not design gap; Matt-confirmed). Byte-for-byte ≡ Arm B; the "Arm C ticks DoT" smoke assertion cannot pass without a DoT source. **DEFERRED** to post-rocket-fix re-fire; gandalf pre-registration `df1023b` binds to that re-fire.

### Artifact paths + UNPUSHED COMMIT LIST (NOT pushed — Matt-gated)
- **Engine repo (`reincarnated-engine`)** — commit `e537b29` "gamora: F1/F2/F4 DoT+mitigation-symmetry production combat fixes + Arm B measurement (math-note-first)": `damage_resolver.py` (F2), `spatial_gauntlet/spatial_engine.py` (F1), `t4_sim_cycling.py` (F4), `math/dot-ailment-mitigation-symmetry-run-2026-06-20.md`, `dot_mitigation_symmetry_armb_harness_2026_06_20.py`, `AGENT_STATE.md`.
- **Collaboration repo (`reincarnated-collaboration`)** — commit (this completion record + artifacts; hash recorded at commit): `cycle-14-wave-5-season-001/dot-mitigation-symmetry-armB-2026-06-20.{json,txt}` (6.4 MB full) + `-smoke.{json,txt}` + this dispatch completion record.

### Surprise vs gandalf's pre-registered interpretation
The headline surprise is **STR does NOT move A→B** (−0.3% to 0.0%): the armor-confound hypothesis (that STR's gap is partly a physical-only-mitigation artifact) is **NOT supported** — STR was already paying the physical curve, so fairness-to-casters leaves it unmoved. The confound was a CASTER over-credit (Q2: 76-94% free elite/boss KPM), not a STR under-credit. STR's residual gap is real allocation, awaiting the bleed lever (deferred Arm C) to test whether the lever closes it.
