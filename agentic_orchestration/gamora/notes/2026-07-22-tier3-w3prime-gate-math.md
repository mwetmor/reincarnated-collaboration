# Tier-3 W3′ — T3-F4′ Gate: mechanical-execution decisions (math-before-code, Discipline #1)

**Author:** gamora (named leg), 2026-07-22. **Class:** zero-discretion execution of the FROZEN
amendment sheet `2026-07-22-tier3-w3prime-prereg.md` (frozen `904f317c`, clean PASS `c47f6cc8`) +
frozen base `2026-07-22-tier3-w3-prereg.md` (`5ea56bf3`, incorporated by reference). The prereg
sheets ARE the math note; this file records only the *mechanical resolutions* I derived from them so
the runner has zero embedded discretion. Every resolution below cites the governing clause.

## The one thing W3′ changes vs W3: the baseline is COMPOSITION-MATCHED (§2)

W3 baseline = the kit's shared `open_arena` 4-seed mean (3 elite + 37 swarm @ 1.5× MOB_HP_DIFFICULTY,
~19,575 destructible HP). W3 RF-B: that baseline measured HP budget, not geometry — the homogeneous
formation encounters (40 swarm @150 = 6,000 HP; no 1.5× on the fresh scenario_id) had a different HP
pool, so mobs_killed saturated at 40 and damage pinned to formation-HP. §2 fix: **per pair, the
baseline is the open arena's DEFAULT PLACEMENT holding that pair's EXACT encounter mob multiset**
(count + tier + per-mob HP + scalars). Then the ONLY manipulated variable is placement geometry;
fighter AND HP budget both cancel in Δ.

### Resolution M1 — what "matched baseline" is, exactly (§2 + §8.1 + parity invariant)
The encounter mob list (W3 machinery, `build_neutral_mob_dicts` keyed on each spawn's threat_tier)
is homogeneous per COMMON-4 class:
- swarm builder → 40 × `swarm` @ HP 150
- lane builder → 40 × `swarm` @ HP 150
- volley-fan builder → 40 × `magic` @ HP 150
- emplacement builder → 40 × `magic` @ HP 150
(neutral stat-block: HP 150, energy 100, armor 20, `emit_skills_for_threat_tier(tier)`, no elite in
any COMMON-4 layout ⇒ no 2500-HP mob).

The matched baseline uses the **IDENTICAL mob_dicts** (same count, tier multiset, per-mob HP, skills,
armor — byte-identical objects) placed at the **open_arena DEFAULT (x,y) positions**. §2 verbatim:
"the encounter builder's exact mob list … placed WITHOUT formation structure (the arena's default
open placement)." The MULTISET (count+tier+HP+scalars) is the encounter's; only the PLACEMENT (x,y)
is the arena's default. This is forced by the COMPOSITION-PARITY HARD INVARIANT (§2 bullet 3, §8.1):
encounter and baseline multisets must be EQUAL. Using the literal open_arena tier layout (3 elite +
37 swarm) would VIOLATE parity (encounter has 0 elite) — rejected.

### Resolution M2 — the 1.5× MOB_HP_DIFFICULTY must NOT fire on the baseline (parity-critical)
`scenario_id="open_arena"` ∈ `MOB_HP_DIFFICULTY_SCENARIOS`; with default
`apply_mob_hp_difficulty_multiplier=True` the engine multiplies swarm/magic/elite HP ×1.5 at fight
build (`spatial_engine.py` L5561/5604-5609). The encounter (fresh scenario_id `t3w3p_*`) gets NO
1.5×. To hold per-mob HP EQUAL (150 both arms — the parity invariant), the baseline is built with a
**fresh scenario_id `t3w3p_base_*` (NOT `open_arena`) using the open_arena default (x,y) layout**.
Consequence: the 1.5× gate does not fire (scenario_id ∉ set), per-mob HP stays 150, matching the
encounter exactly. Belt-and-suspenders `apply_mob_hp_difficulty_multiplier=False` is ALSO passed on
both arms so the gate is doubly-inert. This is the literal instrument §2 specifies ("same per-mob
stat-blocks/HP"); it is NOT a tuning choice — matching HP is the invariant.

### Resolution M3 — per-mob difficulty scalars = the open-arena default spawn's leash overrides
"Same difficulty scalars" (§2): the baseline spawns carry the open_arena default per-spawn
`leash_distance_override_m` (swarm 35m; the 3 default-elite slots' 25m — but those slots are
RE-TIERED to the encounter's homogeneous tier, see M1, and take the swarm 35m leash since all
encounter mobs are swarm/magic non-elite). The mob stat-block scalars (HP/armor/energy) come from the
encounter mob_dicts (M1). Placement geometry = open-arena default positions. Leash is a placement/
pursuit property of the arena's open layout, held at the arena default — this is the "open placement"
§2 names. Recorded: leash is the arena's, HP/tier/count is the encounter's; that is the exact split
§2 draws between "multiset" (encounter) and "placement" (arena default).

## Resolution S1 — sd_pool′ recomputation (§3 + §8.1 C1)
`sd_pool′(m)` = between-cell stdev over the **32 matched-baseline cells' 4-seed means**, per metric,
WITH heterogeneous compositions in the denominator BY DESIGN (§8.1 C1 option (a) — the standardizer
keeps composition-scale spread; d is CONSERVATIVE on magnitude, neutral on sign; X=0.5 keeps its
base-sheet meaning "half a between-cell sd of the substrate's natural spread"). A within-composition
(seed-noise) standardizer is REJECTED (§8.1). Computed + SEALED before ANY encounter fight (§5 step 5).

## Resolution D1 — degeneracy rule (§4 + §8.3 C3)
Metric m DEGENERATE iff `sd_pool′(m) = 0` OR **≥29 of 32** baseline cells' **4-seed MEANS** sit exactly
at m's hard structural bound. Bounds: mobs_killed = 40; total_aoe_hits + player_damage_total = none.
Test runs over baseline cells' MEANS only — never individual fights, never encounter cells (§8.3 C3(i)).
Determination is one-shot at the seal; the informative-metric count + sign-rule form FREEZE at the seal
and are IMMUTABLE after any encounter fight (§8.3 C3(iii)) — a metric that saturates on encounters but
was informative on baselines stays IN the composite. Renormalized sign rule (§4):
- 3 informative → ≥2-of-3 (unchanged)
- 2 informative → 2-of-2 must agree
- 1 informative → sign alone, record LOW-POWER
- 0 informative → RED-FLAG HALT (no improvised metric swap)

## Resolution G1 — gate legs + verdict (§6 carry-verbatim + §7 + §8.4 C5)
Per pair, per metric: `Δ_m(seed) = m(encounter) − m(matched baseline)`;
`d_m = mean_over_4_seeds(Δ_m) / sd_pool′(m)`. Composite = median of INFORMATIVE d's.
Verdict = showcase median (16 high) ≥ +0.5 ∧ stress median (16 low) ≤ −0.5 ∧ direction ≥ 24/32
sign-correct under the SEALED renormalized sign rule. NO partial pass. If §4 fired (any metric
degenerate): REPORT the recomputed α for the realized informative configuration (§8.4 C5) — the gate
PARAMETER stays the ≥24/32 count (α is descriptive only; the stated ≈0.0035 is exact only under
all-pairs-3-informative). Weights 0.50 verb / 0.30 topo / 0.20 shelf apply to FIT-SELECTION only
(unchanged from base sheet), not to the gate arithmetic.

## Resolution E1 — eligibility redraw (§5 RF-A fix)
Candidate pool = v2 fit rows `scoring_basis=full` AND `family_present ≠ hole`, BOTH sides of the draft.
Empirical check on the pool: full rows are binary present(478)/hole(46); `unresolved` appears only on
`era_only` rows already ineligible by base §5.1. Per-era post-filter counts: I=125, II=111, III=111,
IV=131 — abundant for 4 high + 4 low. Base §5.2-5.7 rules carry VERBATIM (round-robin on the single
ACTIVE sidecar family, courts ≥3, least-extreme swap = smallest |fit − era-deck-median|, ties kit_id
lexicographic asc). The redraw yields a full 32.

### Latent edge recorded (does NOT fire in the realized selection)
`SHAPESHIFT/IV` is `family_present=present` (passes the §5 hole filter) but its only Era-IV formation
is `ss_phase_transform` = strain-4 EXCLUDED ⇒ NO buildable COMMON-4 (5 candidate rows). §5 adds
`≠hole` to the pool but NOT `buildable`; the sheet does not pin a formation for an unbuildable-present
pick. Realized fit: SHAPESHIFT/IV sits at fit 0.5-0.6 (mid-pack; era-IV argmax=1.0, argmin=0.1) — it
is neither drafted high nor low, so the edge is LATENT. The W3 runner's red-flag machinery is retained
UNCHANGED: if round-robin ever surfaced an unbuildable pick it RED-FLAGS (stop the pair, record), it
does not improvise. Zero-discretion posture preserved.

## Invariants carried (§6 base + §8.4 C6 + §7 W3′)
- Engine HEAD stamped at fire; `simulation/spatial_gauntlet/` + `generation/` byte-identical to stamp
  through all ~256 fights else HALT. (Fire stamp = `a3671d4…` — identical to W3 baseline HEAD.)
- Engine imported READ-ONLY; corpus.db read-only, md5 `d091881d…` checked open + close; ZERO engine/
  telemetry writes.
- NO MEMOIZATION (§8.4 C6): every pair's baseline is RUN, even where two pairs share an identical
  multiset — 256 distinct fight records total (128 baseline + 128 encounter).
- Non-passive smoke check first (as W3 did) — 2 non-red-flagged pairs; passive player ⇒ HALT.
- Seed set {20260722, 20260723, 20260724, 20260725}; dmod=1.0; COMMON-4 builders only; strain-4
  excluded; fighter = byte-identical BC→nearest-endgame-cell→PlayerClass mapping from the W3 runner,
  same both arms.
