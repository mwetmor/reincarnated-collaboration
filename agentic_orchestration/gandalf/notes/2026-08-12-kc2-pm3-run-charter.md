# RUN KC2-PM3 — charter + ledger: make the sim player fight like Matt fought

> **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Chartered:** 2026-08-12 on Matt's word at the PM-2 HALT:
> **"Push the engine commits and charter PM-3 with your re-based ranking."**
> **Lineage:** PM-2 charter + ledger (`2026-08-12-kc2-pm2-run-charter.md`, L-0..L-10) · gamora landing
> note (`gamora/notes/2026-08-12-kc2-pm2-fight-landing.md`) · PM-1 ledger E-1.
> **Desirable-run fit (§3 test):** bounded substrate (the .arz corpus + the reference video + the PM-2
> baton set, all frozen) · decidable target-state (below) · forks pre-drained (ranking Matt-adopted;
> residuals declared with veto-open leans) · authority-resident (this charter's author conducts).

## Why PM-3 exists (the founding testimony)

PM-2 proved the sim is a fight and the player dies — but of the modeled player, not of Matt. At the
HALT, Matt corrected the reference truth (died wave 159–160, NOT survived; ledger L-9) and testified
(L-10): he **felt the leech starvation** and countered it by **kiting multiple packs into a single
area to max leech/tick**; he **dashed a lot**, ran the **full build-guide skill kit**, carried the
**4 purchased wall/aura/banner blessings**, and died to a **poison/DoT on his last wave** — the same
threat family the sim ranked #1–2 incoming (`livingplant_venomousseed`, `aetherialcorruption_rotskin`).

**PM-3's question: with the measured blessings folded in and a kill-throughput-aware movement policy,
does the modeled player reach the wave 159–160 band where the real player died?** The gap to close is
3–4 waves (sim: dies wave 156 / cleared 5 · Matt: died 159–160 / cleared 8–9).

## The re-based ranking (Matt-adopted at charter)

1. **Crucible tribute blessings + banner** — decode + fold. The largest un-modeled term; measurable
   from the .arz tribute tables; WHICH four Matt bought is measured from the video's opening minutes,
   not assumed (GL-12).
2. **Kill-throughput-aware movement** — the human-validated survival policy (L-10(i)): seek toward
   the live-body **density centroid** (kite-to-cluster), not the nearest pack. Maximize
   bodies-in-disc = maximize leech/tick.
3. **DoT semantics audit** — DoTs are #1–2 incoming despite 85 bleed / 80 vitality / 80 acid res on
   the measured sheet; decode stacking/duration/resist-application semantics before trusting the fold.
4. *(diagnostic)* **leech-OFF cell** — the PM-2 cell's own § 14.1 ask; separates "tanky" from
   "sustained" definitively.
5. *(deferred unless Lap C decode makes them cheap)* pet reuse gates (51 silent specials) ·
   player control-state (286 named-not-carried rows).

## Laws (binding; carried + amended)

1. **FROZEN substrate:** the two PM-1/baseline batons + the four PM-2 siblings (digests at PM-2 L-7)
   — read-only, digest-verified before load (GL-6). Lap B's `tg2_*` CSV set + Lap A's measured player
   sheet are pinned inputs.
2. **Determinism ×2** per cell, masked digest EXACT (FG-10; mask = emitter's own
   `PROVENANCE_VOLATILE_KEYS`, imported not restated).
3. **NO balance tuning.** Survival curves are FINDINGS. Reaching or missing the 159–160 band is a
   measurement either way; nothing is nudged toward it.
4. **⚑ NEW — MEASURED REFERENCE TRUTH (the L-9 law).** Every reference-truth quantity this run
   compares against must be **measured from substrate, not remembered or inferred** — the PM-2
   headline shipped against a conductor-remembered "Matt survived" that the reference himself
   falsified. Lap C pins the exact death wave + per-wave timeline from the video before the fight
   cell's findings are cut. `survivalWaveTier`-class unlock-state fields are NOT outcomes.
5. **Seams:** gamora writes ALL engine code; export deltas minimal + MIGRATION-filed + star-lord
   flagged; legolas laps read-only, filed to `legolas/notes/`; conductor writes no production code;
   CL-10 from own seat at every landing. `/Volumes/reincarnated/` capture dirs are FIRST-CLASS
   substrate (PM-2 Law 6 carried).
6. **GL-12 unchanged:** decode, never estimate. A blessing whose contract can't be decoded is
   declared-absent with the gap named, not approximated from a wiki.
7. **Basis discipline (NOTE-9):** every quantity asserts its population — including the conductor's
   own verification probes (PM-2 L-7's two conductor basis errors are the precedent).

## Residual forks (conductor leans, all VETO-OPEN — none block Lap C)

| fork | conductor lean | status |
|---|---|---|
| **RF-1 dodge** | **DROP dodge from the PM-3 matrix.** PM-2 measured its effect at ≤0.02% of time-of-death and the 33.3% geometric ceiling stands; matrix slots spend better on blessings × movement. Matt's ~50% directive re-aim stays PARKED as a Matt-interface item, not a PM-3 input. | lean declared |
| **RF-2 leech-OFF diagnostic** | **INCLUDE as a 5th cell** (cheap; same seed; definitively separates tanky/sustained). | lean declared |
| **RF-3 `threat_tier` summon member** | star-lord seam; interim pets-ride-`waves[].pets` pattern carries PM-3 unchanged. Ruling can land any time without re-run. | parked |

## Cell sequence

| cell | seat | scope | gate |
|---|---|---|---|
| **Lap C — blessing decode + reference pin + DoT audit** | legolas | (1) From the video's opening minutes, identify WHICH four tribute purchases Matt made (wall/aura/banner things — measured, not assumed); decode their full stat contracts from the .arz tribute/blessing tables (reuse the Lap B instrument stack, `research/scripts/pm2b_*`); deliver a measured blessing sheet (gamora's fold input). (2) Scan the video's wave banners → pin the EXACT death wave + per-wave start timeline (the reference pacing curve, Law 4). (3) DoT semantics: stacking / duration / resist-application for the top incoming DoT families vs the measured sheet's resists; flag any semantics the PM-2 fold got wrong. | fires NOW (background) |
| **Fight cell v2** | gamora | Fold the measured blessings; implement kill-throughput movement (CLUSTER policy: seek the live-body density centroid, channel never drops); apply any Lap C DoT-semantics corrections; run the matrix: **2×2 (movement CAMP/CLUSTER × blessings OFF/ON) + leech-OFF diagnostic (RF-2)** — five cells, same seed. **UNBLESSED+CAMP must REPLICATE the PM-2 CAMP baton** (cross-run determinism check; any drift is a finding). Determinism ×2 each; wave-by-wave pacing vs the Lap C reference curve. | fires ONLY after Lap C lands + conductor verifies |
| **Landing** | conductor | CL-10 from own seat; findings vs the MEASURED reference truth; HALT to Matt with the numbers. Scene-side consumption stays uncommissioned. | — |

## Target-state (decidable)

Five sibling batons + digest ×2 EXACT per cell + UNBLESSED+CAMP replication verdict vs the PM-2 CAMP
baton + survival depth per cell reported against the **video-measured** death wave + wave-by-wave
pacing curve comparison + ledger updated → **HALT to Matt with the numbers.** The headline question —
*does BLESSED+CLUSTER reach the 159–160 band?* — is answered yes/no with the mechanism named.

## Matt interface

Commitment-boundaries: any tuning temptation (Law 3) · scene-side consumption · the parked ~50%
dodge-directive re-aim · RF-3 schema ruling. Everything else = reasoning-boundaries, veto-open,
ledgered.

---

## Ledger

| row | content |
|---|---|
| **L-0** | Charter authored on Matt's word ("Push the engine commits and charter PM-3 with your re-based ranking"). **Engine pushed first: `6c4a7472..c75af8da` (6 commits), porcelain 2,789 = FG-17 baseline** — the four PM-2 batons are in-tree + on remote. Lap C fired (legolas, background). |

*Charter + ledger opened by gandalf (`RUN-CONDUCTOR`), 2026-08-12.*
