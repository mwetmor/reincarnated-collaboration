# RUN KC2-PM4 — charter + ledger: replicate waves 150–160 faithfully (iterative convergence run)

> **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Chartered:** 2026-08-13 on Matt's word at the PM-3 HALT:
> **"Can you please proceed autonomously from here on until the waves 150-160 are replicated
> faithfully? There was no reason to ask me this question. Push as you go as well."**
> **Lineage:** PM-2 charter (L-0..L-10) · PM-3 charter (L-0..L-3) · gamora landing notes (PM-2 fight,
> PM-3 v2) · legolas Laps A/B/C.

## Two standing authority amendments (Matt verbatim, banked)

1. **Substrate completion via MEASURED decode = a reasoning-boundary.** The PM-3 HALT asked Matt
   whether decoding the missing eHP was permitted; his answer: *"This is obvious… There was no
   reason to ask me this question."* Going forward the conductor fires measured-decode substrate
   completion on own authority. Law 3 (no tuning) is UNCHANGED — the line is *measured decode of
   what the real fight had* (allowed, conductor authority) vs *fitting constants toward an outcome*
   (still barred, still a Matt commitment if ever tempted).
2. **Push-as-you-go** — engine + meta push after each landing, no per-push word (per-workstream push
   pattern, CLAUDE.md commit discipline).

## Target-state (decidable, pre-registered BEFORE iteration 1)

The **reference configuration cell** (DEFENSES-ON + CLUSTER — what Matt actually played) replicates
the measured reference truth (Lap C `measured-reference-truth.csv`, Law 4 lineage):

- **T1 — survival depth:** player death on **wave 160** (band {159–161} = near-miss, reported;
  exact 160 = met).
- **T2 — fight duration:** time-of-death within **±15%** of the measured **186 s** (682→868 s).
- **T3 — pacing shape:** per-wave clear times correlate with the measured curve (14/17/29 s
  min/med/max; slowdown on the final two waves reproduced in direction).
- **T4 — mechanism:** death consistent with the reference testimony (DoT-involved terminal wave;
  sustain-through-throughput while alive).

All four bands pre-registered HERE, before any iteration ran. **NO constant is ever fitted toward
them** — iterations close *named, measured* gaps only; if all measurable limbs fold and the sim
still sits outside the bands, the residual is the finding and the run HALTs with it.

## Method — the iteration loop

Each iteration: (1) name the current largest measured divergence + the substrate/model limb that
carries it; (2) legolas decodes the limb (MEASURED only, GL-12); (3) conductor verifies (CL-10);
(4) gamora folds + re-runs the standing matrix; (5) conductor verifies, banks the ledger row,
**pushes engine + meta**; (6) re-measure vs target-state → converged? HALT with numbers : next
iteration. Determinism ×2 per cell every iteration; replication cell (corrections-off CAMP vs the
PM-2 CAMP digest) retired after PM-3 proved it EXACT — each iteration instead pins its predecessor's
reference-cell digest as the comparison baseline.

**Standing matrix (lean):** CLUSTER/DEF-ON (reference cell) · CAMP/DEF-OFF (control) ·
CLUSTER/DEF-OFF (defence isolation). Leech-OFF retired (settled at PM-3). Cells may be added by
conductor ruling when a limb demands isolation.

## Pre-registered iteration queue (re-orderable by measurement, not by preference)

| # | limb | why queued | evidence |
|---|---|---|---|
| **I-1** | **band-B eHP — give the monsters their bodies back** | 182/188 bodies enter `hp_max=0`; THE proven largest term (PM-3 § 5) | band-A table proves the corpus carries life MEASURED (`t22_band_a_monster_stats.csv` life_equation + wave scaling) |
| **I-2** | **player kill throughput on a covered board** | with real eHP the player's damage model binds for the first time; the sim models the EoR channel only — Matt ran the full build-guide kit + dashes | Lap A parsed 318/318 skills from the gdc; build-guide doc in `/Volumes/reincarnated/agent-prompts/` |
| **I-3** | **potion / circuit-breaker recovery layer** | Matt played with potions; absent from F-3; matters once damage-bound waves lengthen exposure | decodable from .arz consumable records + gdc quickbar |
| **I-4** | **pet special reuse gates** | 51 slots silent (declared under-read, PM-2 § 9) | needs a measured reuse-gate decode |
| **I-5** | **player control-state** | 286 control/debuff rows named-not-carried (PM-2 § 10) | stun/freeze/fumble semantics in corpus |
| **I-6** | **DoT stacking** | declared-unmodeled (Lap C C-4: address, no decodable function) | may stay declared; revisit only if T-bands demand it |

After each iteration the queue re-orders by the measured divergence, not this table's order.

## Laws (binding; carried)

Frozen inputs digest-verified before load (GL-6) — note the eHP limb is now VERSIONED substrate, not
frozen: each iteration's substrate set is pinned + digested in its ledger row · determinism ×2
masked-EXACT (FG-10) · **NO tuning** (Law 3 as amended above) · GL-12 decode-never-estimate ·
NOTE-9 basis discipline · gamora writes all engine code; legolas laps read-only; conductor writes no
production code; CL-10 from own seat at every landing · math-note-before-code with pre-registered
predictions per fold (Discipline #1; the PM-2/PM-3 falsification record is the working standard) ·
explicit-path commits · `/Volumes/reincarnated/` capture dirs first-class substrate.

## Matt interface

Matt reads the ledger + pushed commits as the run proceeds; the conductor HALTs to him only at:
**convergence** (target-state met — final numbers + the full iteration lineage) · **exhaustion**
(all measurable limbs folded, sim still outside bands — the residual is the finding) · **any genuine
tuning temptation** · **scene-side consumption** (still uncommissioned). Parked, unchanged: dodge
re-aim · RF-3 `threat_tier`.

---

## Ledger

| row | content |
|---|---|
| **L-0** | Charter authored; authority amendments banked; PM-3's three engine commits PUSHED (`c75af8da..301807b4`). Target-state bands T1–T4 pre-registered above BEFORE iteration 1 fired. **I-1 Lap D fired** (legolas, background): decode life equations + per-level eHP + wave `life_modifier_pct` fold for the FULL E-s09-cp150 roster (all 344-actor records, waves 151–170 — covers the 188 band-B bodies and future-proofs the band), extending the band-A instrument. |
| **L-1** | **Lap D LANDED + CL-10 PASS from conductor's own seat** (legolas push `52c231be..41059e86`). Coverage 6/188 → **188/188** (791-record closure; ONE named zero-magnitude gap `krieg_aethertrap.dbr`); grades 790 MEASURED. Conductor re-verified: SHA-256 all four CSVs EXACT (`3e82e72b`/`8fa5279a`/`adfec980`/`9d276ddb`); baton join 114/114 at own wave; all five agreement integers located (Steward mid-level 2,345,066 in `life_by_level` @ charLevel 107, per-wave limbs bracket it); Σ w160 = **15,967,220** reproduced (HI limb; LO 15,760,198, −1.3%); G endpoints 306@151/344@170 ⇒ G(150)=304 corroborated from the table, not adopted. Structural: 0 monotone / 0 negative / 0 limb-order violations, 200/200 floor spot-check. **The headline that re-orders nothing but explains everything:** at run-of-record limb the covered board costs **185.0 s of pure disc contact vs the measured 186 s** — PM-3's "throughput was never the constraint" was read off a 96.8%-empty board. Waves 151–160 Σ eHP 18.9M → **117.2M (×6.2)**. **Rulings:** **R-PM4-1** (resolves ⚑D-1): fold consumes eHP per `(record, wave)` — each body enters at its OWN wave's G via `pm4d_band_b_ehp_by_wave.csv`; the single-`board160`-dict pattern retired (F-2-class regression, per-wave emission exists precisely to close it). **R-PM4-2** (resolves ⚑D-2): run-of-record limb = **LO by explicit column selection** (carries the declared LO-limb ruling; never row-order); HI carried as sensitivity in the landing note. **R-PM4-3**: Lap D measured levels (663 MEASURED-SET + 128 DERIVED-INHERITED) supersede the `_BAND_B_MODAL_LEVEL=109` fallback — closes `DIV-LEVEL-COVERAGE` (93/169 records rode a level outside their derived set). **Parked by ruling:** C-D1 pet-life two-folds-one-board (pets keep Lap-B values UNCHANGED this iteration; cliff named, lands with I-4) · C-D2 G(171)=420 discontinuity (outside the 151–160 band) · C-D3 the named gap (if rolled, enters declared `hp_max=0` + GAP basis, counted + reported) · C-D4 damage out of scope. **gamora I-1 fold fired** (background): eHP-ONLY fold + standing-matrix re-run, math-note-first with pre-registered predictions, determinism ×2, PM-3 cluster-defon digest pinned as baseline, measure vs T1–T4. |

| **L-2** | **I-1 LANDED + CL-10 PASS from conductor's own seat** (gamora engine `301807b4..e6f3b2c6`, meta `b7d5c9d3..2c09217b`, both pushed; batons `dec60040`/`cd367066`/`59da5739`; 395 tests pass; Law 3 witness `moved: {}`). **T-band scorecard (conductor-corrected):** T1 **MET-mechanism-divergent** (wave 160 all three cells — but via approach-window burst, not attrition) · T2 **MET** (190.61 s = +2.5% of 186 s; conductor re-read t_s=190.6122 from wire) · T3 **NEAR** (median ratio 1.121; holding out pre-existing travel-outlier wave 154: 1.017, r=0.796; 158→159 slowdown reproduced ×2.21 vs ref ×1.86 — conductor EXACT) · T4 **SPLIT, conductor overrules gamora's MET** — sustain limb holds (95.6% mean HP, ADCtH 27.97M offered) but the terminal clause FAILS: reference = DoT-major 29 s fought wave; sim = 7.02 s / 86 ticks, 20,903 intake (=1.045× HP bar, decomposition verified EXACT: devastationshard 9,923 + arcanemissilenova 8,343 + sappingorbs 2,444 + teleport 194), ZERO player damage rows, DoT 4.9%. **CL-10 resolutions:** killer "w160_pet0011" vs wire "w160_a001" = NOTE-9 basis split on ONE row (source_id=owner wendigo, damage_source_tag=its summoned wraith) — both true, bases now asserted; "pets 12,366" = tag-basis (9,923+2,444). **⚑ Conductor-found instrument gap: `waves[].pets` DROPPED from the PM-4 baton** (present in PM-2/PM-3) — pet lifecycle rides only 625 tag strings; 596 pet kills + 35-live-at-death are driver-internal, not wire-reproducible. **Banked defects:** PROVENANCE_VOLATILE_KEYS misses `sim_pin.tree_state_untracked_entries_excluded` (flagged star-lord, countersigned, non-blocking) · PM-3 CAMP 326.5 s wave corrected: 314 s two-pet TTL stall, not roster time · Lap D's "185.0 s" flagged as over-read pre-run (uncapped multi-target disc, N_eff=2.99). Falsification record 4/9 confirmed banked (G.1 sustain-priced-exposure-missed is the run's teaching). **⚑ QUEUE RE-ORDERED BY MEASUREMENT — Iteration 2 = C-D1 pet life:** 596/779 = 76.5% of reference-cell kills are pet bodies still on Lap-B granted-passives-only life (median ×4.22 soft); every T-band number stands on this mis-measured limb; PM-3 § 10's "pets are the only bodies with real HP" has fully inverted. I-2 (kit/dash) + I-3 (potion) now NAMED WITH A MEASUREMENT (no answer during approach; Matt had all three) and queue next. **Lap E fired** (legolas, background): decode whether monster-summoned pets receive the Ultimate (+580%) and wave-G life folds + pet level source — MEASURED or DECLARED-undecidable, never estimated; Iteration-2 gamora fold will also restore pet wire observability. |

*Charter + ledger opened by gandalf (`RUN-CONDUCTOR`), 2026-08-13.*
