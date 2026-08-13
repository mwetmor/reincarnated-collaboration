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
| **Fight cell v2** | gamora | **(arm renamed at L-1/R-PM3-1: BLESSINGS → DEFENSES — Matt bought zero blessings; he built the arena's four defence points: Deathchill / Stormcaller / Inferno Beacons + Vanguard Banner.)** Fold the measured defences (allied entities from decoded contracts; player-facing = the Vanguard Aura's 6 rows, positional within 8 m of the banner); implement kill-throughput movement (CLUSTER policy: seek the live-body density centroid, channel never drops); apply the Lap C DoT corrections (R-PM3-2); run the matrix: **2×2 (movement CAMP/CLUSTER × defences OFF/ON) + leech-OFF diagnostic (RF-2)** — five cells, same seed. **Reference comparator = DEFENSES-ON + CLUSTER. DEFENSES-OFF + CAMP must REPLICATE the PM-2 CAMP baton** (cross-run determinism check; any drift is a finding). Determinism ×2 each; wave-by-wave pacing vs the Lap C reference curve. | fires ONLY after Lap C lands + conductor verifies ✓ FIRED at L-1 |
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

| **L-1** | **LAP C LANDED (legolas, commit `5eec56ca`) — zero improvisations, six cliffs named; and ranking item #1 DISSOLVES as framed.** Deliverables at `legolas/notes/2026-08-12-kc2-pm3-lap-c-blessings-reference-dot/`. **D1:** Matt bought **ZERO blessings** — tribute stepped 145→125 at t=477/484/502/510 buying **Deathchill / Stormcaller / Inferno Beacons + Vanguard Banner** (tier-1, 5 tribute + 10k iron each; the Crucible's Lua declares exactly four defence points — he filled the arena). "Wall/aura/banner things" — **Matt's own words were accurate; "blessings" was conductor genre-gloss** (the L-9 lesson rhymes: his testimony beats my vocabulary). 259 effect rows decoded; **six touch the player** (Vanguard Aura: +80 OA, +4% OA, +100% total damage, +100% retaliation — only within 8 m of the banner, rank EXACT). Beacons = separate allied entities. **The reference run = DEFENSES-ON; the blessings-style buff arm was a counterfactual.** **D2 (Law 4 discharged):** death wave **160** PINNED (persistent HUD counter, template-IoU over 218 frames, 5 unreadable named); fight window 682→868 s = **ten waves in 186 s** (14/17/29 s min/med/max, sharp slowdown on the last two). **Gap re-cut: FOUR waves, not three. And the real kill throughput is ~4–5× the sim's** (186 s/10 waves vs 412 s/5.x waves) — the pre-registered expectation frame for v2. **D3:** R-PM2-1 total-over-duration **RATIFIED by measurement** (GD's own tooltip format); three corrections: (A) `playerDefenseCap=[80,80,80]` — sheet bleed 85 clamps to 80, **bleed taken ×1.333** vs PM-2 fold (closes Lap A G-2); (B) `rotskin` is a **toggled 3.5 m damaging aura**, PM-2 mis-folded it as an initial-slot swing that also displaced the carrier's weapon; (C) DoT duration axis absent from fold (inert here). Stacking has an address but no decodable function → **not modeled, declared** (GL-12). **CL-10 FROM OWN SEAT: PASS** — commit verified; dims exact (260/11/10 rows, ±1 s uncertainty declared per NOTE-9); **death wave 160 eye-verified** (HUD "160" + "You have failed" in evidence frame t880); Vanguard aura rows read from CSV as reported (`banner_offense.dbr` → `banneroffense_aura_buff.dbr`, +80 OA rank-1 EXACT, allies-in-radius). **Conductor rulings (reasoning-boundaries, veto-open, declared on the wire by v2):** **R-PM3-1** matrix arm renamed BLESSINGS→DEFENSES; comparator = DEFENSES-ON+CLUSTER; replication check = DEFENSES-OFF+CAMP ≡ PM-2 CAMP. **R-PM3-2** DoT corrections (A)+(B)+(C) adopted into the v2 fold; stacking declared-unmodeled. **R-PM3-3** defences modeled as allied actors from decoded contracts at Lap C's declared rank (C-2 cliff: rank 26 declared, full arrays shipped — gamora states the rank policy on the wire); NOTE the tension v2 will price: **beacon kills do NOT feed player leech** (ADCtH rides player damage only) — allied defences thin packs and may CUT player sustain while adding CC/damage. **R-PM3-4** placement = the four defence points; the banner's 8 m player-aura tether is positional — in CLUSTER cells leaving the banner radius costs +100% damage (= leech), and the sim prices that tradeoff rather than assuming it away. **FIGHT CELL v2 FIRES.** |

*Charter + ledger opened by gandalf (`RUN-CONDUCTOR`), 2026-08-12.*
