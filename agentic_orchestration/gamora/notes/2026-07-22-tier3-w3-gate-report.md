# Tier-3 W3 — T3-F4 GATE — REPORT

# VERDICT: **FAIL** (all three legs miss; no partial pass per §6)

**WAVE W3 of the Tier-3 Encounter-Geometry Run** · conductor gandalf `RUN-CONDUCTOR` · gamora leg
**Author:** named-gamora sub-agent · 2026-07-22
**Execution:** ZERO-DISCRETION mechanical execution of the FROZEN prereg sheet
(`agentic_orchestration/gandalf/notes/2026-07-22-tier3-w3-prereg.md`, freeze commit `5ea56bf3`).
Where the sheet pinned a rule I followed it exactly; where the sheet did not decide I STOPPED that
pair / recorded a red-flag and continued — never improvised a rule (RF-A ×4 pairs + RF-B wave-level).

**Header stamps:** substrate corpus.db md5 `d091881d` (READ-ONLY, verified) · sidecar commit `6dd43161`
· engine HEAD open `a3671d4` / close `a3671d4` — **HEAD-state invariant OK** (subtree delta
`a3671d4..HEAD` on `simulation/spatial_gauntlet/` + `generation/` = EMPTY, byte-identical) · seeds
{20260722–25} · dmod=1.0 · frozen X=0.5, Y=75% (≥24/32). **Zero engine-repo writes; zero telemetry
writes** (ADR-006; harness invoked by path).

**Artifacts (all in `agentic_orchestration/gamora/notes/`):**
- `2026-07-22-tier3-w3-gate.py` — the executable (selection + formation-fit + fights + gate)
- `2026-07-22-tier3-w3-gate-output.json` — census + subscores + 128 fight records + per-pair d + legs + verdict
- this report

---

## The three legs (§6) — numbers

| Leg | Metric | Value | Threshold | Pass |
|---|---|---|---|---|
| **LEG 1 showcase** | median composite d over 16 high-fit pairs | **0.0** | ≥ +0.5 | **NO** |
| **LEG 2 stress** | median composite d over 16 low-fit pairs | **+0.507** | ≤ −0.5 | **NO** (wrong sign) |
| **LEG 3 direction** | pairs sign-correct (≥2 of 3 metric d's) | **7 / 28** | ≥ 24 / 32 | **NO** |

PASS requires all three; **FAIL** on all three. LEG 2 lands POSITIVE (+0.507) — the exact inverse of
the ≤ −0.5 the stress leg demands; low-fit pairs did BETTER than neutral, not worse (mechanism below).

---

## Selection census (§5) — deterministic, clean

Full-basis rows only (524 candidates, 131/era). 4 high (argmax) + 4 low (argmin) per era under the
kit-side family round-robin (§5.2–3, draft-family = the kit's single ACTIVE sidecar row). **All four
eras passed the courts check with n=5 courts and ZERO swaps** (≥3 required):

| Era | Families drafted (8 kits) | Courts (n) | Swaps |
|---|---|---|---|
| I | AURA · CHANNELED-BEAM · DOT-AILMENT · MPV · TOTEM-SENTRY · TRAP-MINE | chaos-poison, cold, fire, lightning, physical (5) | 0 |
| II | + MELEE-STRIKE · WHIRLWIND (7 fams) | same 5 courts | 0 |
| III | 7 fams | same 5 courts | 0 |
| IV | 7 fams | same 5 courts | 0 |

Round-robin verified deterministic (fit_score primary, kit_id lexicographic-asc tiebreak). Sampled-pair
`membership_tier` mix (28 scored pairs): **RATIFIED 11 · PROPAGATED 5 · DOCKET 12** — travels per L-13(c).

## Formation assignment (§5.4 · STEP 2)

Per-formation fit sub-scores COMPUTED with the frozen component logic (0.50·verb + 0.30·topo + 0.20·shelf;
verb+shelf constant per (kit,era), only topo varies per formation via the v2 `TOPO_AFFINITY`/`TOPO_CLASS`
tables — reused, not re-derived). Strain-4 EXCLUDED (`cbn_corridor_arc`, `cb_crossfire`,
`ts_environmental_nest`, `ss_phase_transform`). formation_id→COMMON-4-builder mapping transcribed from the
W2 `FORMATION_SCENARIO_MAP.formation_class` column. Argmax formation (high) / argmin (low) per pair; the
chosen formation_id + class + sub-score recorded per pair in the JSON. Formation class distribution across
the 28 scored pairs: swarm / volley-fan / lane / emplacement all exercised (emplacement dominates the
anchor/aura/totem/trap families; volley-fan the MPV/ranged; swarm the melee/whirlwind; lane the
corridor/wedge/beam).

## Fights (§2 · STEP 3)

28 pairs × 4 seeds = **112 fights ran** (16 high + 12 low; 4 low pairs red-flagged, not fought — RF-A).
Formation builders at HEAD (`build_{swarm,volley_fan,lane,emplacement}_formation`, arena.py), **MOB-COUNT
PARITY 40 TOTAL hard** — all four builders held exactly 40 (swarm 10×4, volley-fan count=40, lane count=40,
emplacement 8×5), all in-bounds in a 44×44 neutral arena; **zero builder parity red-flags**. Fighter =
each kit's BC→nearest-endgame-cell→real fighting PlayerClass, **byte-identical to the baseline** (baseline
mapping + idx-assignment + neutral per-tier mob stat-block reused verbatim; 16 cells, 0.3s build). dmod=1.0,
same 4 seeds. **Discipline #11 smoke passed BEFORE the full run**: 2 pairs, player NON-PASSIVE (d2-bowazon
volley-fan mk=40/pd=6000; d2-fire-sorc emplacement mk=20/pd=3000) — no passive-player pathology.

---

## Full decomposition

**Per-era legs (descriptive; n=8/era binomially weak alone, per §4):**

| Era | high median composite d | low median composite d | sign-correct |
|---|---|---|---|
| I | −0.234 | +0.507 | 1/7 |
| II | +0.244 | +0.702 | 3/7 |
| III | 0.0 | +0.254 | 1/6 |
| IV | +0.351 | +0.351 | 2/8 |

**Per-metric medians (the confound is visible here):**

| Metric | high median d | low median d |
|---|---|---|
| mobs_killed | **0.0** (ceiling-pinned) | +0.507 |
| total_aoe_hits | **0.0** (ceiling-coupled) | +0.585 |
| player_damage_total | −0.727 | −0.065 |

**Per-family mean composite d (working labels):** TRAP-MINE +0.804 · MPV +0.715 · AURA +0.611 ·
TOTEM-SENTRY +0.211 · WHIRLWIND 0.0 · MELEE-STRIKE 0.0 · DOT-AILMENT −0.234.

---

## Red-flags (situations the FROZEN sheet did not decide — recorded, NOT improvised)

### RF-A — hole-cell formation-assignment gap (4 pairs; per-pair)

§5's round-robin legitimately drafts **hole-cell families** as low-side argmin (they ARE the lowest-fit:
`family_present=hole`, `fit_score=0.15`, `meso=[]`, `topo_reason=no_formation_dealt`). But §5.4
encounter-construction gives **NO COMMON-4 formation for a hole cell** (the family deals zero formation in
that era's deck). The sheet does not pin a formation for hole cells → I STOPPED those 4 pairs, recorded
them, did not improvise:

- **I / low `gd-aar-spellbinder`** — CHANNELED-BEAM is a genre HOLE in Era I (§3.3 "CHANNELED-BEAM absent Age I").
- **II / low `d2-avenger`** — MELEE-STRIKE is the famous PoE1 melee HOLE in Era II (§3.3, load-bearing).
- **III / low `d2-auradin`** — AURA is a true genre HOLE in Era III (§3.3).
- **III / low `poe1-frost-blades`** — MPV is a HOLE in Era III (GD ranged is single-shot, not fan-volley).

Consequence: the low side scored 12/16, not 16/16. Per §6 (no partial pass) an incomplete 32-sample cannot
certify a PASS regardless — moot here since the gate FAILS on the scored pairs anyway, but recorded so the
conductor owns whether §5's selection should exclude hole cells or §5.4 should pin a hole-cell formation.

### RF-B — HP-budget composition confound (wave-level measurement artifact)

§2 pins mob-count parity **"40 total" ("formation shapes geometry, NOT budget")** but does **not** pin the
encounter's per-mob HP or elite/swarm split. The baseline is `open_arena` = 40 mobs (**3 elite + 37 swarm**)
WITH the engine's 1.5× `MOB_HP_DIFFICULTY` (elite eff 3,750 · swarm eff 225 → **total destructible HP ≈
19,575**, matching the observed baseline `player_damage_total` ceiling of 19,575). The COMMON-4 formations
are **HOMOGENEOUS** (all swarm-tier, or all magic-tier) at the neutral per-tier stat-block, and with a fresh
`scenario_id` the 1.5× does not fire (geometry, not tuning — §5.4). Net total-destructible-HP mismatch
(e.g. swarm formation 40 × 150 = **6,000** vs baseline **19,575**) makes:

- **`mobs_killed` SATURATE at the 40 ceiling** — the player clears the weaker homogeneous formation to
  40/40 on nearly every seed (evidenced: many low pairs go baseline mk≈22 → encounter mk=40 → d=+1.40, a
  HP-budget artifact, NOT fit); high-side already-ceiling baselines give d=0.0 (40 vs 40).
- **`player_damage_total` PIN at the formation total-HP** (6,000 for a full swarm clear), regardless of fit.

So **2 of the 3 gate metrics are HP-budget-dominated, not geometry-dominated**, and `total_aoe_hits` is
ceiling-coupled to `mobs_killed` here. This is why LEG 2 inverts to positive: low-fit pairs kill MORE (more,
weaker mobs) than in the elite-heavy baseline. **The confound is INHERENT to the frozen instrument**
(elite-heavy 1.5×-scaled `open_arena` baseline vs homogeneous unscaled 40-mob formation, both "40 total") —
matching per-mob HP would NOT dissolve it, because the elite/swarm split is unpinned by "40 total." I did
**not** rescale HP to compensate: rescaling is an un-pinned rule that would move the verdict, forbidden by
zero-discretion mechanical execution. Recorded for the conductor's W4 fold.

**Robustness note:** the FAIL is robust to any HP choice within the sheet's pins — LEG 1 showcase median is
0.0 (against ≥+0.5) and LEG 3 is 7/28 (against ≥24/32); no per-mob-HP normalization the sheet leaves open
could lift a 0.0 showcase median to +0.5 or flip 21 sign-incorrect pairs.

---

## Where the FAIL routes (§6 honorable fallback)

RD-1 does NOT fire. The failure decomposition routes to the W4 review book + lane queues:
1. **RF-B (instrument):** the baseline↔encounter HP-budget mismatch — the gate as frozen measures HP-budget
   on 2 of 3 metrics. A re-instrument would either (a) match the encounter's 40-mob elite/swarm split +
   effective HP to the baseline's, or (b) re-baseline each formation against its OWN neutral open-arena at
   the same composition. Either is a conductor/Matt commitment-class call, not gamora's to pin.
2. **RF-A (selection×construction seam):** §5 selection vs §5.4 construction disagree on hole cells — pin
   one (exclude hole cells from the draft, OR define a hole-cell formation).
3. **Signal that DID survive:** even HP-confounded, the emplacement formation shows genuine positive fit
   response for anchor/aura/totem/trap high picks (d2-frenzy-barb +1.05, le-explosive-trap-falconer +1.19,
   poe1-armageddon-brand +0.70) — the geometry signal exists but is drowned by the budget confound on the
   ceiling-bound metrics. `player_damage_total`, if freed from the composition pin, is the metric to lean on.

---

## Discipline compliance

- **#1 math-before-code:** the FROZEN prereg IS the math note (execution-plan header in the .py, no
  re-derivation); all weights/tables/thresholds transcribed verbatim from the frozen sheet + v2 fit script.
- **#2 smoke-scale:** 112 fights, 5.2s wall — this IS the smoke-scale gate (128-pair budget).
- **#3 no parallel same-seed:** single sequential process, one shared 4-seed set.
- **#11 empirical inspection:** non-passive smoke ran on 2 pairs BEFORE the full run; the HP-budget confound
  (RF-B) was CAUGHT by inspecting baseline-vs-encounter raw values, not assumed.
- **#12 semantic-shift:** N/A to a change (no existing behavior reinterpreted); RF-B is a reported
  instrument property, framed explicitly, not buried.
- **HEAD-state invariant (§2):** armed at open, re-checked at close — HEAD `a3671d4` unmoved, both subtrees
  byte-identical. No HALT.
- **ADR-006:** corpus.db READ-ONLY (md5 `d091881d`, `mode=ro`); zero telemetry writes; zero engine-repo
  writes (harness by path).
- **Zero design discretion:** every pinned rule followed exactly; every un-pinned situation red-flagged
  (RF-A×4 + RF-B), never improvised.
