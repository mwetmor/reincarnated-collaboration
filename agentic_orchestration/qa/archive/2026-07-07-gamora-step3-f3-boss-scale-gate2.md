# Gate-2 submission — 2026-07-07 — gamora Step-3 COMPLETION: F3 tier-independent boss_damage_scale + full-pop F2 re-lock + genre-sane boss HP

**To:** jack-ryan (Gate-2, BLOCK authority)
**From:** gamora (simulation seam)
**Engine tag:** `gamora/v-batch2-step3-f3-boss-scale-1` (HEAD `61a7faf`; push HELD — Matt-gated)
**Dispatch:** `dispatches/2026-07-07-gamora-step3-f3-boss-scale-completion.md` (Matt's 4-decision ruling — executes (1)+(4); (2)+(3) are your decisions-log lane)
**Predecessor Gate-2:** `qa/findings/2026-07-07-gamora-step3-lived-channel-repilot-gate2.md` (`9ecccff`) — determination (4): "there is no two-knob path; the decoupled `boss_damage_scale` is the minimum-rank addition." This submission implements exactly that.
**Why Gate-2:** new certification-path knob (`boss_damage_scale`) + F2 full-pop re-lock + Rider-3 disposition semantics.

## What landed (2 commits on `main`)
- `59dc832` — math-before-code note (Disc #1+#24+#11+#12), committed BEFORE any tuning: `simulation/math/step3-f3-boss-damage-scale-2026-07-07.md`. This is the plan-of-record; everything below executes it verbatim.
- `61a7faf` — the tier-scoped knob + full-pop re-lock + genre-sane HP + Rider-3 dispositions + cosmetic INFO fix + AGENT_STATE + sidecar JSON.

## The rank-deficiency, resolved (your determination (4) endorsed the path)
- **The STOP was a rank-deficiency** (2 knobs, 3 independent targets: F2-WR, F3-TTK, F3-WR). One monolithic `mob_damage_scale` multiplies boss (dm 5.0) AND swarm (dm 0.85) together, so the F2-lock 0.03 defangs the F3 boss to dm 0.15 → F3 WR pinned at 1.0. The minimum-rank fix is a boss-tier-independent damage lever.
- **(1) The tier-scoped knob — DONE.** `_mob_skills_for_tier(..., boss_damage_scale=1.0)` applies a SECOND multiplicative factor AFTER `mob_damage_scale`, gated to `is_boss_tier = tier in {boss, mini-boss, miniboss}` ONLY — NOT elite, NOT swarm/magic. Post-change per-tier dm: swarm/magic/elite UNCHANGED (`native·mds`); boss/mini-boss = `native·mds·bds`. At `bds=1.0` every tier's dm is byte-identical to pre-change (strict extension).
- **Strictly-positive guard (your Gate-2 (1) COERCION FINDING carried):** `_mob_skills_for_tier` raises `ValueError` on `bds <= 0.0` — a computed dm of 0.0 is falsy → `_resolver_skill_from_dict` coerces `0.0 → 1.0` (`spatial_resolver_adapter.py:118`), aliasing native lethality, the opposite of "off." The "off" reference is `bds=1.0` (the defanged 0.15 boss that produced the STOP), never 0.0.

## NO-LEAKAGE PROOF (measured, not asserted — Disc #11)
- **Structural:** the two knobs attach at DISJOINT tier sets. `boss_damage_scale` multiplies only `{boss, mini-boss}`; the F2 competency tiers (swarm + magic + elite) are in `mob_damage_scale`'s set and NOT in `boss_damage_scale`'s. F1/F2/F4 rooms carry NO boss/mini-boss tier → the boss knob is a no-op there.
- **Empirical witness (in the sweep):** F2 full-pop wheel-avg WR at `bds ∈ {1.0, 5.0}` on the re-locked `mds` = **IDENTICAL (0.9446 == 0.9446)**, per-kit vectors byte-equal. If they had differed, leakage existed. They do not. The F2 lock is provably untouched by the boss knob.

## #24 sweep result (re-lock F2 on full pop FIRST, then sweep bds for F3; HP FIXED)
- **(4) F2 full-pop re-lock: `mob_damage_scale = 0.03`** (IN_BAND). Full-pop wheel-avg WR **0.9446**, inside [0.85,0.95] at the band-ceiling edge. The steep cliff resolves on the 40-kit population: 0.025→0.998, 0.03→0.945, 0.035→0.707 (< 0.85 floor). 0.03 is the sole in-band member near the 0.90 midpoint — the beat-locked value HOLDS on full pop.
- **F3 boss knob lock: `boss_damage_scale = 48.0`** (WR_IN_BAND). With `mds` fixed and HP fixed, boss dm = 5.0·0.03·48.0 = 7.2. F3 full-pop wheel-avg WR **0.7018** ∈ [0.60,0.80]. Clean monotone descent across the cliff (bds 35→0.857, 40→0.818, 46→0.761, 48→0.702, 50→0.639) — single-parameter #24 isolation, clean grip.
- **Genre-sane boss HP = 9000 = 60× trash (150); ARPG 40–100× band.** NOT swept to force TTK (Matt (3)). `_HP_BY_TIER` now carries `boss: 9000, mini-boss: 9000` (the mini-boss key was missing — fell to the 150 default; correctness fix for the F3 `mini_boss` member).
- **F3 TTK = 5.036 s → STANDING population-wide OVERPOWERED FLAG.** Kit-DPS-bound (~5s vs 9000 HP; the ~11–13s engage floor + ~90k kit DPS are the binding terms, not boss HP — your Gate-2 (3) TTK-DPS-bound determination stands). Recorded per-kit + aggregate (38 kits flagged), routed to balance review. NOT auto-fail, NOT a reason to inflate HP. This is the chassis-evidence-#1 TTK-DPS mismatch surfacing as a flag.

## Full four-family re-pilot (one seed stream; Rider-3 dispositions; `pilot_policy=scripted-rotation-v1`)
| Family | Martial cert/n (Rider-3) | Caster cert/n | Rider-3 disp (martial: PASS / FLAG_PASS / FAIL) |
|---|---|---|---|
| F1 | 25/40 | 2/2 | 10 / 15 / 15 |
| F2 | 36/40 | 2/2 | 8 / 28 / 4 |
| F3 | **28/40 (CERTIFIES — was the STOP)** | 2/2 | 0 / 28 / 12 |
| F4 | 5/40 | 2/2 | 5 / 0 / 35 |

- **F3 NOW CERTIFIES** (WR med 0.8214; the boss threatens). Casters get REAL F3 numbers (WR 1.0, margin +0.40 above the 0.60 floor) — last run F3 was the defanged 1.0 STOP.
- **F2 WR-over-band = FLAG-PASS per Rider 3 / Matt (4):** 28/40 martial kits ride the WR ceiling (>0.95) and dispose as `FLAG_PASS_OVERPOWERED` (certified + flagged), NOT auto-fail. 4 genuine under-floor FAILs remain. n_certified 36/40.
- **F4-martial KPM: MEASURE ONLY** = 23.7 med < 60 floor (35 FAIL). Kit response GATED on the pilot-attribution probe (Matt) — NOT fired. Out of scope per dispatch.
- **Caster margins re-confirmed on the new scale + F3:** F1 +0.05, F3 +0.40, F4 +0.20, all pass.
- **F-b closing read: PARITY HOLDS** on F1/F2/F4 (diagnostic; F-b retirement is your closed decisions-log lane).

## Rider-3 disposition schema + SEMANTIC SHIFT (Disc #12 — framed, not buried)
- `_bar_disposition` → `_rider3_disposition`: under-floor → **FAIL** (hard cert line); over-ceiling / over-band → **FLAG_PASS_OVERPOWERED** (certified-but-flagged → balance review); in-band → **PASS**. F3 TTK<15s → standing flag. Floor beats ceiling (an under-floor sub-metric dominates).
- **SHIFT 1 (calibration model):** mob-damage calibration is now DECOUPLED — F3 boss lethality was coupled to the swarm chip via the monolithic scalar; it is now an independent tier-gated lever.
- **SHIFT 2 (disposition):** an over-CEILING reading was previously folded into `passes_bar=False` (an auto-fail); it now disposes as FLAG_PASS_OVERPOWERED. `passes_bar` KEEPS its strict-in-band meaning unchanged (your Gate-2 confirmed it is computed correctly); `n_certified` = PASS + FLAG_PASS is the new Rider-3 cert count.
- Both shifts are the same discipline's honest-scope framing. Please route to the decisions-log.

## Cosmetic INFO fix (your Gate-2)
`_bar_disposition` kpm_band branch now writes `disp["wr"] = wr`. Before: `_miss_taxonomy`'s `disp.get("wr", disp.get("win_rate"))` resolved `None` → `side` ternary fell to `"under"` → F2 WR=1.0 (over the 0.95 ceiling) mislabeled `wr_under_band`. **VERIFIED in the report:** the over-band F2 kit now labels `wr_over_band` with `disp["wr"]=1.0` and disposition `FLAG_PASS_OVERPOWERED`. Reporting-clarity only; NO verdict change (`passes_bar`/`wr_in_band` computed independently).

## Guard / provenance
- **NO kit-side chassis constants** (BASE_PHYSICAL/SPELL_DAMAGE_L50, 2.3384× fossil FROZEN). **NO bar/band moved** (bars are FIXED INPUTS; the knob tunes the F3 ROOM to the F3 WR BAR).
- **NO boss-HP inflation to force TTK** (genre-sane 9000 + standing flag). **NO F-b / F4-martial / Leg-C work. NO tier scalar beyond boss/mini-boss.**
- Sim-internal room-side constants + sidecar JSON (`step3-lived-calibration-sweep-v2-boss-damage-scale`, `step3-lived-channel-repilot-v2-boss-damage-scale`) — NO cross-seam persisted field → **NO MIGRATION.md** (math note §8).
- **pilot_policy stamp:** re-pilot report stamped `pilot_policy=scripted-rotation-v1` (read from your decisions-log `8607840`, not invented).
- **Regression:** `test_cycle13_wave5_gauntlet_sim` 50/50; sweep beat + full-pop + full re-pilot PASS.

## Asks for Gate-2 + escalation
1. **Verify the tier-scoped attachment + no-leakage** (boss knob a no-op on F1/F2/F4; the empirical IDENTICAL witness) + the strictly-positive guard.
2. **Ratify the Rider-3 disposition semantic shift** (over-band = FLAG_PASS_OVERPOWERED, not auto-fail; the `n_certified` cert count) and route both shifts to the decisions-log.
3. **Register the F3 TTK-under-15s standing flag** as the chassis-evidence-#1 surface (parallel to your (2)/(3) lane) — recorded, NOT tuned to, NOT HP-inflated.
4. **Escalate to Matt (deferred rulings):** none new from my scope — (2) F-b retirement and (3) chassis-evidence-#1 registration are your lane; the F4-martial pilot-attribution probe remains Matt-gated.
