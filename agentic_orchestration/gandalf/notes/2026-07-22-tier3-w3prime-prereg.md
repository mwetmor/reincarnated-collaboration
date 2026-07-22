# Tier-3 W3′ Pre-Registration — T3-F4′ Gate Instrument (AMENDMENT SHEET)

**Author:** gandalf `RUN-CONDUCTOR` (SPEC-AUTHOR beat), 2026-07-22 — ruling **L-16** under Matt's verbatim authorization *"W3′ go!"* (charter-amendment class, Matt-ruled; PING-1 fork (ii)).
**Status:** DRAFT → freezes on jack-ryan prereg check. After freeze, NO parameter changes through W3′; a violated invariant is a red-flag, not a silent adjust.
**Relationship to W3:** **T3-F4′ is a NEW gate. The W3 FAIL stands on the record as W3's verdict** — this sheet does not revise it. The RD-1 conditional (T3-V6) TRANSFERS to the W3′ verdict per L-15(c)(ii) + Matt's go.
**Base sheet:** `2026-07-22-tier3-w3-prereg.md` (frozen `5ea56bf3`) — **incorporated by reference; every parameter not explicitly re-pinned below carries VERBATIM.**

---

## §1 — What W3 proved defective (the two pins this sheet replaces)

1. **RF-B:** base §2 pinned mob-COUNT parity ("40 total") believing count pinned budget. It did not: baseline `open_arena` = 3-elite+37-swarm at 1.5× (~19,575 eff HP) vs homogeneous unscaled formations (~6,000). Two of three gate metrics measured HP budget, not geometry (mobs_killed ceiling; damage pinned to formation HP; LEG-2 sign inversion mechanically explained).
2. **RF-A:** base §5.1 candidate pool admits hole cells (`family_present=hole`, fit 0.15, `meso=[]`) that base §5.4 construction cannot build — 4 low pairs stopped; a complete 32-sample was impossible.

## §2 — Re-pin A: COMPOSITION-MATCHED BASELINE (the instrument fix)

For each sampled pair, the baseline is **no longer the shared `open_arena` fight.** New instrument:

- **Baseline fight = open arena, IDENTICAL MOB MULTISET to that pair's encounter** — the encounter builder's exact mob list (count=40, same tier composition, same per-mob stat-blocks/HP, same difficulty scalars, fresh `scenario_id` semantics identical to the encounter's) placed WITHOUT formation structure (the arena's default open placement). Same 4 seeds.
- `Δ_m(seed) = m(encounter fight, seed) − m(matched baseline fight, seed)`; per-pair `d_m = mean_over_4_seeds(Δ_m) / sd_pool′(m)` (§3).
- **COMPOSITION-PARITY HARD INVARIANT:** encounter and baseline mob multisets must be equal (count + tier + HP + scalars). Any mismatch → per-pair red-flag; do not normalize silently.

**What now cancels in the contrast:** the fighter (carried from base §2 — byte-identical BC→cell→PlayerClass both sides) AND the HP budget (new). The manipulated variable is **placement geometry alone** — the isolation the base sheet claimed and did not deliver.

## §3 — Re-pin B: sd_pool′ recomputation (mechanical, stamped pre-gate)

`sd_pool′(m)` = between-cell stdev of the **32 matched-baseline cells'** 4-seed means, per metric — computed and stamped in the output BEFORE any encounter fight is scored. The **X=0.5 standardized rule carries verbatim**; only the standardizer's numbers recompute on the new pool (the old pool sd was a property of the retired elite-heavy baseline set).

## §4 — Re-pin C: metric-degeneracy rule (pre-pinned; declared before data)

The matched instrument may saturate a metric in BOTH arms (e.g., the fighter clears 40/40 in open arena AND formation → mobs_killed carries no contrast). Pinned NOW so no post-hoc judgment exists:

- Metric m is **DEGENERATE** iff `sd_pool′(m) = 0` OR ≥90% of matched-baseline cells sit at m's hard structural bound (mobs_killed bound = 40; the other two have none).
- Degenerate metrics are excluded from BOTH the per-pair composite (median of informative d's) and the sign rule, which renormalizes: 3 informative → ≥2-of-3 (unchanged) · 2 → 2-of-2 must agree · 1 → its sign alone, gate record flagged LOW-POWER · **0 → red-flag HALT** (honorable; no improvised metric swap).
- `elapsed_s` + flanking metrics stay **descriptive-only** regardless — promotion of an unmeasured metric into a gate is new-instrument risk this sheet refuses.

## §5 — Re-pin D: eligibility (the RF-A fix)

Base §5.1 candidate pool adds: **`family_present ≠ hole`, both sides of the draft.** A hole cell means the era's deck deals that family NO formation — there is no geometry to test, and constructing one would fabricate substrate (substrate-led discipline). The low-side draft redraws to next-best argmin candidates under the UNCHANGED round-robin + courts + tiebreak rules (base §5.2–5.7 verbatim) → **full 32 pairs restored.**

## §6 — Carried VERBATIM from the frozen base sheet (completeness list)

Weights `0.50·verb + 0.30·topology + 0.20·shelf` (frozen; adjust-once remains DECLINED) · **X = 0.5** standardized (§3 pool) · **Y = 75% pooled over 32 pairs**, binomial basis P(≥24/32|p=0.5)≈0.0035 · seeds {20260722–25} · dmod=1.0 · mob-count 40 hard (now subsumed by §2 composition parity) · COMMON-4 formations only, strain-4 excluded · formation assignment argmax/argmin per base §5.4 with v2 TOPO tables · fighter mapping byte-identical both arms · primary metric triple mobs_killed / total_aoe_hits / player_damage_total (subject to §4) · gate verdict = showcase median ≥ +0.5 ∧ stress median ≤ −0.5 ∧ direction ≥75% of 32 (≥2-of-3 or §4-renormalized) · **no partial pass** · honorable fallback (FAIL ⇒ RD-1 does not fire; findings route to W4) · corpus.db read-only md5-checked · zero engine/telemetry writes.

**HEAD-state invariant (re-stamped):** W3′ stamps engine HEAD at ITS fire; all ~256 fights (32×4 baseline + 32×4 encounter) execute with `simulation/spatial_gauntlet/` + `generation/` byte-identical to that stamp, else **HALT** (Lane-1's active writes are export/output/tests — non-colliding; #9 audit confirmed no other engine writer).

## §7 — Execution + verdict

Single named-gamora leg: eligibility redraw + census → 32 matched-baseline compositions built + parity-verified → sd_pool′ stamp → 256 fights → §4 degeneracy determination → gate legs → verdict. **PASS ⇒ RD-1 fires** (transferred conditional — first act-structured run-object as emission-congruent JSON; Lane-1's acceptance fixture). **FAIL ⇒ honorable fallback:** RD-1 does not fire; both instrument-generations' findings (W3 RF-A/RF-B + W3′ decomposition) route to the W4 review book.

On jack-ryan check PASS this sheet freezes verbatim; conductor judges results as DRIFT-CRITIC against THIS sheet.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-22 — L-16, veto-open (T3-V1).
