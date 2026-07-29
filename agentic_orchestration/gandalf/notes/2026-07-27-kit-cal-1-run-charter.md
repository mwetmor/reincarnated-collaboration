# CHARTER — KIT-CAL-1 — the first calibration kit run

**Run ID:** `KC1-2026-07-27`
**Conductor:** gandalf (`RUN-CONDUCTOR`; charter author conducts — intent residency per desirable-run-pattern §2 Element 3)
**Pattern:** desirable-run pattern (`operating-procedures/desirable-run-pattern.md`) — §3 fit test: F1 ✓ F2 ✓ F3 ✓ F4 ✓
**Authorization chain:** Matt ruled GD = primary join key (R-1, this cycle); Matt approved the iconic-build/calibration-kit split contingent on this ultra-think; Matt's "go" authorized this charter. Launch requires the §4 grill answered + L-gates green.
**Status:** DRAFTED — awaiting launch gates (§6).

---

## §0 — Intent sentence (the rubric-law anchor)

> **Prove the RDR battle sim can be held accountable to a measured external fixture:** map the
> play-test-v1 werewolf build into a sim-abstract kit from GD source data, run it in gamora's
> harness, and land inside pre-registered acceptance bands against the R2 fixture — **or fail
> honorably with the miss decomposed** into source-mapping error vs sim-mechanics error vs
> fixture-measurement error.

Per pattern §6.3 (rubric law): every exit predicate in §2 was diffed against this sentence at
drafting. What fell out, named out loud: **this run does not certify "the sim feels like GD"** —
it certifies agreement on the accountability targets ratified at grill item 2, nothing wider.
It also does not select the iconic build (KIT-1) — that is a parallel commission (grill item 5).

## §1 — Bounded substrate (frozen at launch; the substrate votes)

| # | Substrate | Location | Count/pin |
|---|---|---|---|
| S-1 | T-A telemetry ledger (run `GP-gd-2026-07-26-s1`) | `/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/` (+ Matt's copy `matt_notes_handoff_docs/GD-tests/play-test-v1/`, git-ignored) | 13,633 samples @0.5s; endpoints 882/74/54/358/175/12468.06 |
| S-2 | G-1 T-B intake output (in flight) | galadriel captures dir, path fixed when G-1 reports | ~19,305 frames over 106 engagement windows |
| S-3 | GD Edition-II source data | `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` (`.arz` + `Text_EN.arc`) | Edition-I frozen sibling retained for diff |
| S-4 | corpus.db GD rows | canon_corpus 41 gd kits · kit_numeric 26 gd rows | as-is at launch |
| S-5 | Verdict + verification docs | `gandalf/notes/2026-07-26-gd-playtest-v1-efficacy-verdict.md`, `…-artifact-verification.md` | regime boundaries 358/1134/6052/7094 |

**The fixture** (default naming, grill item 1): **R2** — 647 kills / 77 engagements, `play_time`
1134–6052, two-skill werewolf, potions 0/0, no devotion proc, level ~5–11. **R3** (190/16,
poison-DoT regime) is the secondary fixture with its own error bars. **R1 is report-only** —
13 engagements is an anecdote, not a distribution (verdict §3).

Discoveries beyond this substrate are findings for the next lap, never silent scope growth.

## §2 — Decidable target-state (exit predicates)

The run is DONE when all of:

- **T-1** — G-2b causal-decomposition artifact filed: pack-size vs dash-chaining vs AoE-proficiency
  signatures separated from the S-1 CSV (engagement-duration trend, intra-engagement kill-gap
  structure, charge-per-engagement, multi-kill fraction per regime), with the verdict's
  "engages larger packs" causal claim and the "R3 packs ~3.6× R1" claim re-graded against it.
- **T-2** — Onslaught-attribution check resolved empirically from S-1 (did the `onslaught`
  counter increment anywhere in R2?) and the grill-item-3 decision rule applied.
- **T-3** — G-3 ingestion landed (elrond): fixture in the substrate DB, **regime-partitioned**
  (a pooled table is a trap — verdict §7), `life_healed` 3.1% rejection rate riding as a column.
- **T-4** — G-4 kit spec authored (named `gandalf` sub-agent): the werewolf build as a
  sim-abstract kit, every numeric traced to an S-3 `.arz` record or explicitly graded
  ATTESTED/DERIVED with the gap named.
- **T-5** — G-5 harness comparison executed (gamora): **coverage gate FIRST** (pattern §6.1 —
  which fixture series the sim reproduces *at all*: TTK shape, intake, kills/engagement),
  **then** band accuracy on the ratified accountability targets against pre-registered bands.
  Result is PASS **or** an honorable-fail decomposition per §0. Either terminates the run.

"Done" is checkable in-run; the two judgment points are converted to Matt HALTs (§5), not left
as quality feelings.

## §3 — Run body (sequenced; seams execute, conductor writes no production code)

| Phase | Work | Seam | Notes |
|---|---|---|---|
| P-0 | G-2b causal decomposition + T-2 onslaught check | **galadriel** (CSV analysis rides the G-1 lane) | fires the moment G-1 reports; feeds HALT H-1 |
| P-1 | G-3 fixture ingestion | **elrond** | regime-partitioned; schema his call within verdict §7 constraints |
| P-2 | G-4 kit spec | **named `gandalf` sub-agent** | conductor-seam piece → named agent per §2.1 corollary; onslaught rule applied; Matt owner-eye checkpoint here (§5) |
| P-3 | G-5 harness + coverage gate + band comparison | **gamora** | jack-ryan Gate-2 untouched; bands ratified at H-2 before execution |

Parallel, **non-gating** (ride alongside, do not block exit): grill-item-4 `.gdc` save probe
(legolas); grill-item-5 iconic shortlist (legolas); R-2 D2 annex harvest + R-3 `source_edition`
flag (elrond/legolas, riding the join-key ruling); drax werewolf-asset queue items.

## §4 — Launch grill (ELICIT, don't IMPOSE — leans stated, Matt rules)

Five lines to answer:

1. **Fixture + kit identity.** Lean: fixture `GD-R2-werewolf` (pinned to run
   `GP-gd-2026-07-26-s1`, regime R2); kit id `gd-werewolf-kitcal-1`. Your naming governs canon.
2. **Accountability-target set.** Lean: **primary = engagement-level TTK shape + damage-intake
   distribution** (the two §1-protocol quantities); **kills/engagement = provisional** until
   G-2b decomposes the proficiency confound you identified; R1/R3 report-only. Alternative:
   promote kills/engagement to primary anyway and let the bands absorb the confound (I
   recommend against — it bands a measurement artifact).
3. **Onslaught disposition rule** (pre-pinned decision rule; run applies it at T-2):
   **(a)** counter incremented in R2 → 3-active kit; **(b)** counter frozen → adopt
   transform-remap hypothesis, model Onslaught presses as claws-attributed events, grade the
   third active ATTESTED-by-your-testimony; **(c)** neither resolvable → 2-active spec with a
   named sensitivity note. Lean: ratify (a)/(b)/(c) as the rule now so the run never halts on it.
4. **G-7 `.gdc` save-file probe** — parse your save to recover exact devotion/attribute/gear
   state (upgrades build identity toward MEASURED; would also settle the devotion-points
   UNVERIFIED claim from verdict §9). Yes/no. Lean: **yes** — bounded, cheap, non-gating.
5. **Iconic-build shortlist commission** (legolas: 5–8 candidates, canon-fame × RDR archetype
   need × v2-recordability, GD Stash noted as endgame-construction path). Yes/no. Lean: **yes**,
   parallel — it names the v2 recording target and KIT-1 without touching this run.

## §5 — Matt interface + HALTs (declared pre-launch; veto-open ruling ledger runs throughout)

- **HALT H-1 (commitment):** when G-2b evidence is on the table — **F-1 engagement-grain ruling**
  (gap>5s vs alternative segmentation) is made by you WITH the decomposition in hand, before
  bands are drafted. The grain choice defines what "an engagement" means in canon; that is
  yours, not mine.
- **HALT H-2 (commitment):** **acceptance-band ratification** before the first G-5 comparison
  executes. I draft the bands with G-2b + intake evidence; you pin them; only then does the
  comparison run. Preregistration discipline: the run cannot move its own goalposts.
- **Owner-eye checkpoint (pattern §6.2):** G-4 kit spec goes past your eyes at P-2 — you played
  this build; your testimony already caught two things the instruments graded wrong (Onslaught,
  the pack-size causal claim). Your eye is an instrument of record here, not a briefing recipient.
- Red-flag pings anytime; review book at run end; every in-run ruling logged veto-open.
- **Red-main tripwire (pattern §6.4):** N/A — no CI/deploy surface in this run. Stated so the
  omission is deliberate.

## §6 — Launch gates

- **L-1** — G-1 T-B intake pass reports with coverage adequate to stand as the intake fixture
  (converts the play-test verdict CONDITIONAL PASS → PASS). If G-1 coverage fails, launch is a
  fresh Matt call (TTK-only run vs re-pass), not a silent narrowing.
- **L-2** — §4 grill answered (five lines).
- **L-3** — this charter is the ARCHITECT open-questions gate: every decision the run will hit
  is RESOLVED here or GATED at H-1/H-2 with its empirical criterion named. Gate is clean at
  drafting; it re-checks trivially at launch.

## §7 — Honorable fallback

A band miss at T-5 is a **processable finding, not a terminal event** (pattern §2 Element 4).
The run terminates at a filed decomposition: which target missed, which regime, by how much,
and the suspected locus — (i) source-data mapping error in G-4, (ii) sim-mechanics divergence
in the RDR engine, (iii) fixture-measurement error upstream. Locus (ii) is the *valuable*
outcome — it is the first externally-anchored defect report the sim has ever received. A miss
decomposed is a run succeeded.

**Signed:** gandalf, 2026-07-27.

---

## §8 — LAUNCH RECORD + RULING LEDGER (2026-07-28)

**All launch gates green:** L-1 — G-1 reported (19,348 frames / 88.8% coverage; verdict converted
CONDITIONAL PASS → PASS, R3 travels with its declared hole — see verdict addendum 2026-07-28).
L-2 — Matt ratified all five grill leans verbatim ("Agreed on all five leans, launch when G-1
reports"). L-3 — ARCHITECT gate clean. **RUN `KC1-2026-07-27` IS LIVE.**

**Ruling ledger (veto-open):**

| # | Ruling | Source |
|---|---|---|
| R-KC1-1 | Fixture `GD-R2-werewolf` (pinned to `GP-gd-2026-07-26-s1`, regime R2); kit `gd-werewolf-kitcal-1` | Matt ratified lean |
| R-KC1-2 | Accountability targets: **TTK shape + damage-intake primary**; kills/engagement **provisional** pending G-2b; R1/R3 report-only | Matt ratified lean |
| R-KC1-3 | Onslaught disposition rule (a)/(b)/(c) ratified as pre-pinned; run applies the branch the CSV proves | Matt ratified lean |
| R-KC1-4 | `.gdc` save probe: **YES** — legolas fired at launch | Matt ratified lean |
| R-KC1-5 | Iconic-build shortlist commission: **YES** — legolas fired at launch, parallel, non-gating | Matt ratified lean |

**Testimony amendments recorded at launch (Matt, 2026-07-28):**

1. **Onslaught UI-masking is CERTAIN:** "Onslaught skill use is hidden by the game because I was
   in werewolf form; the skill that impacted the enemies was the werewolf claw." This pre-confirms
   the frozen-counter reading as UI behavior, not player behavior. The **open sub-question he
   names**: did Onslaught function as a claws-damage *augment* while transformed, or was the press
   *replaced* by a claw swing? → new **G-4 source-data task**: read the Fangs-of-Asterkarn
   werewolf-transform records in the Edition-II `.arz` for skill-exclusion / skill-conversion
   behavior (GD's transmuter/exclusion-skill machinery). T-2's empirical check (does the counter
   ever increment in R2/R3) still runs — testimony and series must agree or the disagreement is
   a finding.
2. **Devotion-zero upgrades to ATTESTED:** "I definitely did not utilize any devotion points."
   Verdict §9's stronger claim (zero devotion *assigned*, previously UNVERIFIED) is now
   player-attested; the R-KC1-4 `.gdc` probe upgrades it to MEASURED if the save is reachable.

**Fired at launch:** P-0 G-2b (galadriel, in flight since L-1); P-1 G-3 ingestion (elrond);
R-KC1-4 `.gdc` probe (legolas); R-KC1-5 iconic shortlist (legolas). **Held:** P-2 G-4 awaits the
G-2b onslaught answer + carries testimony amendment 1; P-3 G-5 awaits HALT H-2 band ratification.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-28.

---

## §9 — IN-RUN FINDING F-KC1-1 — the R2/R3 boundary is a COMPOUND event (2026-07-28)

**Trigger:** Matt testimony, in-run — *"the weapon, shield and amulet I equipped at level 12 added
HUGE health boosts."* Checked immediately against the T-B rollup. **Confirmed, and larger than the
testimony implies.**

| Regime | max-HP range (observed) | largest single-frame drop (RAW HP) | median drop | drops ≥10% EHP |
|---|---|---|---|---|
| R1 | 250 → 314 | 14 | 5.0 | 0 |
| R2 | 366 → **759** | **541** | 5.0 | **27** (46.8% of intake) |
| R3 | **1600 → 1600 (flat)** | **136** | **1.0** | 0 |

**The finding.** Max HP steps **759 → 1600 (2.11×) at the R2/R3 boundary and is then FLAT for all
of R3.** The verdict located that boundary by *gear-equip bracketing off the poison DoT*
(`play_time` 6052–6282, correction C-1). The max-HP series is a **far sharper instrument** for the
same boundary and it corroborates the placement independently.

**⚠ SWITCH: (claim-relayer) → DRIFT-CRITIC — correcting a claim I endorsed one turn earlier.**
The T-B headline — *"hazard inverts; the player got safer by out-scaling the size of what lands"* —
was relayed by me as a build/world fact. It is substantially a **gear fact**. R3's flat 1600 EHP
and its collapsed drop magnitudes (median 5.0 → **1.0** raw HP; max 541 → 136) are what a
weapon+shield+amulet step *does*: more pool, and — since these are post-mitigation reads — more
armor/block eating the incoming hits. The **inversion survives in raw HP** (541 → 136 is not a
denominator artifact; the fixture's largest hit fell 4× in absolute terms), so the *shape* finding
stands. Its **attribution** does not.

> **R3 is not "R2 plus a poison DoT." It is a different character on both sides of the ledger** —
> offense (DoT) *and* defense (2.11× pool + mitigation) stepped together at one gear event. Every
> R3 figure must travel with **"post-gear-step"** as a condition, alongside its existing
> coverage-hole condition.

**Ripples, ruled in-run (veto-open):**

1. **A fourth causal channel enters G-2b: SURVIVABILITY.** The kills/engagement climb into R3
   (11.9) now has four candidate causes, not three — pack size, dash-chaining segmentation-merge,
   AoE proficiency, **and a tankier character able to hold pack centers.** G-2b is in flight with
   the first three; the fourth rides a **G-2c follow-up** rather than killing the running pass.
2. **R2's own EHP is not constant either** (366 → 759, 2.07× across the regime). G-2c must check
   whether the 27 ≥10%-EHP hits cluster early (low-denominator artifact) or late. The 72.4% hit
   sits at EHP 747 — late-regime, near-max pool — so at least the extreme is a genuine huge hit.
3. **The `.gdc` probe (R-KC1-4) is upgraded from convenience to load-bearing.** Identifying those
   three items is now required for G-4 to model R3 at all. Gear identity was already in its scope.
4. **Accountability-target consequence:** this strengthens R-KC1-2. Intake bands must be fit
   per-regime against per-window EHP (galadriel already did this — `max_hp_range` is instrumented,
   not assumed), and **R2 remains the fixture** precisely because it is the longest stretch without
   a compound step.

**Also banked:** Matt's Onslaught refinement — masking is CERTAIN (werewolf form hides it; claws
were the visible effect); the OPEN question is *augment vs replacement*, which the Edition-II
`.arz` transform records should settle outright (G-4 task, §8 amendment 1).

**Signed:** gandalf (`RUN-CONDUCTOR` / DRIFT-CRITIC), 2026-07-28.
*(Amended by §11 — the block-mitigation half of this finding is falsified; the pool half stands.)*

---

## §10 — G-2b RETURNED · T-2 RESOLVED · HALT H-1 package (2026-07-28)

Source: `galadriel/notes/2026-07-28-gd-playtest-v1-g2b-causal-decomposition.md` + captures
`2026-07-28-gd-playtest-v1-g2b/`. Gate 0 reproduced the 106-window derivation field-identical
before anything downstream fired.

### 10.1 — The headline: the climb is a STEP, not a ramp

Within R2, **build held constant, 4,338 game-seconds, levels 3 → 11**: kills/engagement
7.90 / 8.16 / 8.90 / 8.68 by quartile — **Spearman ρ = 0.075, p = 0.52.** Charge-per-engagement
drifts *down* (1.78 → 1.58). Bursts ρ = −0.115. Simultaneity ρ = 0.091.

> **A proficiency ramp would show there. A zone-depth pack ramp would show there. Neither does.**
> The entire established climb is the **2.54× jump across the 335-second build-swap intermission**
> (`play_time` 1135 → 1470). Permutation tests, engagement unit, 50k: R1→R2 **p = 0.00054**;
> R1→R3 p = 0.00026; **R2→R3 p = 0.129 — NOT established.**

R1's purity is a world-fact, not an instrument artifact: **43 kills in 43 separate half-seconds,
zero multi-kills**, P(0 of 43 | R2's rate) = **7.0e-11**, and the same 0.5 s instrument resolved
373 multi-kills afterwards. The four-skill build **never once killed two things at the same time.**
The werewolf did so immediately (R2's first four engagements read 1.33 / 1.80 / 1.00 / 1.40).

**Matt's contested attribution adjudicated:** the *mechanism* he named is real and measured —
charge predicts burst count at ρ = 0.665 (R2, p = 7.5e-11) and ρ = 0.772 (R3); R3's long
engagements carry **31.6%** travel-band gaps against 4.3% in its short ones. But chaining **cannot
be the cause of the climb**: it survives re-segmentation to one sample of separation (R3/R1 = 2.91
at gap>1.0 s vs 3.59 at gap>5 s; merge share **+16.2% [−32%, +40%]**, ≤ +4.5% at 2.0 s), and the
merge channel is flat-to-falling across regimes (2.46 → 2.20 → 2.13). **Half-right, and not the
half he expected** — his mechanism exists, his causal role for it does not.

**Verdict §3's "R3 packs ~3.6× R1" — FINAL GRADE: NOT SUPPORTED as a pack-size claim.** 3.590
decomposes A ×1.900 · B ×2.188 · C ×0.863, and **no instrument in this artifact measures pack size
at all.** R1 is also the wrong denominator (different build, skills, level, zone, gear). My claim,
struck.

### 10.2 — T-2 RESOLVED, and a correction to the pass that resolved it

**The ledger answer is airtight: ZERO Onslaught increments after `play_time` 1145.** 10,065
consecutive samples read exactly 54; zero non-monotone reads; the series terminates on the
human-read total 54; the reader stayed live on Soldier rows to `play_time` 6780. Refusals cannot
hide an increment in a monotone series terminating on its own endpoint.

**⚠ SWITCH: (receiver) → DRIFT-CRITIC — one G-2b conclusion is contradicted by G-2b's own data.**
The pass ruled transform-remap *"ruled out by timing — the freeze at 1145 precedes the first
`werewolf1` read at 1469 by 324 s."* **That argument does not hold.** Direct ledger read of
`play_time` 1145 → 1470:

| | |
|---|---|
| kills | **45 → 45. Zero.** |
| span | 325 game-seconds / 342 wallclock-seconds |
| only moving counter | `life_healed` (out-of-combat regen at pt 1335/1344/1345) |

**There is no combat in that window** — it is the respec/traversal intermission. Onslaught had
**zero opportunity** to increment. Its last use is the last press of the last pre-swap fight; the
next fight is the first fight of the werewolf era. The freeze does not precede the transform in any
*behavioral* sense, only in wallclock. **Transform-suppression is NOT ruled out — it is back to
being the leading hypothesis, and it matches Matt's testimony.**

What survives from the pass and is decisive: **the panel carries exactly six skill signatures**,
built from the final-frame native screenshot, and GD's panel is cumulative — **there is no seventh
row the presses could have gone to.** (Set aside the claws-rate comparison: it measured Onslaught's
*in-combat* rate against claws' *run-wide* rate; not apples-to-apples, and not load-bearing.)

> **RULING R-KC1-6 (veto-open): T-2 resolves to branch (b) of R-KC1-3.** Counter frozen →
> transform-suppression adopted; the third active is graded **ATTESTED** on Matt's testimony.
> **Augment-vs-replacement is NOT answerable from any telemetry instrument** and routes wholly to
> **G-4's Edition-II `.arz` read** of the Fangs werewolf-transform record (skill-exclusion /
> conversion machinery). A skill-use counter cannot see a press that never fired.
> **New v2 requirement:** player-intent attribution needs an input log or keybind-visible HUD.

### 10.3 — HALT H-1: the F-1 grain question, and why it partly dissolves

The decomposition supplies an identity that is exact by construction:

> **kills/engagement = A (kills per kill-event) × B (kill-events per burst) × C (bursts per
> engagement)**, burst = maximal run with internal gaps ≤ b.

That identity reframes F-1. The three factors are **three different kinds of quantity**:

| Factor | What it measures | Whose behaviour is it? |
|---|---|---|
| **A** — simultaneity | AoE breadth / how many die at once | **the kit's** — sim must reproduce |
| **B** — kill-events per burst | sustained pressure, DoT tail | **the kit's** — sim must reproduce |
| **C** — bursts per engagement | dash-chaining, routing, travel | **the player's + the level's** — the sim should NOT be accountable to it |

R3's entire (unestablished) lift sits in **B** (2.27 → 2.94) with A and C unchanged — the
mechanical signature of a damage-over-time tail, exactly as the gear event predicts.

**gandalf lean — R-KC1-2 amendment, for Matt's ruling:** **retire kills/engagement as an
accountability target** rather than de-provisionalise it. It is a composite of two kit quantities
and one player quantity, and G-2b shows it behaves as a **step function of build identity**, not a
continuous measurable. Replace it with **A and B as the accountability targets**, and treat **C as
a declared non-target** (a routing artifact the sim is not asked to match). This makes the grain
choice nearly moot for accountability — A is grain-invariant by construction, B is defined on the
burst, and only C depends on the engagement boundary.

**Residual grain decision, still Matt's:** what the canonical "engagement" is *for reporting*.
- **Option A — keep gap > 5 s** (verdict-compatible, 106 units, largest sample, reads as "a fight").
- **Option B — tighten to gap > 2.5–3.0 s** (closer to a single pack; note the climb ratio gets
  *bigger*, 4.03–4.23, so this does not flatter the prior claim).
- **Option C — dual grain (gandalf lean):** keep **gap > 5 s = "encounter"** as the reporting and
  TTK/intake unit (it is what the intake pass already measured, so nothing is re-derived), and
  adopt **burst (gaps ≤ 1.5 s) = "pack-proxy"** as the unit for A and B. Two names, two jobs, no
  conflation — and it is what the decomposition already used.

### 10.4 — The one gap nothing above closes

**No enemy-count instrument exists in this artifact.** The split *inside* A — "the player centred
an AoE on a pair" vs "a pair happened to be standing there" — is unmeasurable from counters.
Galadriel names a **T-C frame-level enemy census over the 106 windows** as the highest-value next
pass, and I concur: it is the only thing that measures pack size at all, and pack size is a
quantity RDR needs independently for encounter geometry. **Surfaced to Matt as a decision, not
fired** — it is a substantial new CV pass on the same footage.

**Signed:** gandalf (`RUN-CONDUCTOR` / DRIFT-CRITIC), 2026-07-28.

---

## §11 — G-3 LANDED · two corrections and one boundary upgrade (2026-07-28)

Fixture ingested: `research/curated/fixtures.db`, schema `fixtures-v0.5` — series as the
measurement, regimes/engagements/rollup/fixture as *named replaceable partitions of it*. Regime
partition is enforced structurally (no `ALL` row exists to point at; a pooled insert fails), coverage
is unrepresentable-if-NULL via triggers, and `kills_per_engagement` is banked
`tier='provisional'` / `semantics_status='contested'` so it cannot be read as a headline. Verdict §3
reproduced cell-for-cell from banked rows. MIGRATION: `research/curated/MIGRATION-fixtures.md` (M8).

### 11.1 — Elrond's flag belongs IN the H-1 package: the grain had selection pressure

`C-SEG-GRAIN-UNRULED`, banked UNVERIFIED: **gap > 5 s is simultaneously the most permissive
defensible threshold AND the only one that reaches §1's 100–250 engagement target band** (>8 s → 75,
>10 s → 67). That is a researcher-degrees-of-freedom hazard stated out loud, and it is a fact Matt
should hold while ruling F-1. **It strengthens the §10.3 dual-grain lean**: separating the reporting
unit (which hit a band) from the pack-proxy unit (which carries A and B) is precisely what removes
the pressure from the quantities the sim is accountable to.

### 11.2 — CORRECTION to F-KC1-1 (§9): block is NOT the mitigation mechanism

`shield_block_chance` is a T-A column, and it **changes exactly once in the entire run: 15.0 → 18.0
at `play_time` 3256** — mid-R2, nowhere near the boundary. Matt was **already wearing a shield long
before level 12**; the level-12 shield did not introduce blocking.

**§9 speculated "armor/block eating the incoming." The block half is FALSIFIED.** What stands: the
**2.11× max-HP pool step** (759 → 1600, then flat) is measured and real; armour remains an
uninstrumented candidate for the residual magnitude collapse (median drop 5.0 → 1.0 raw HP). The
hazard-shape finding survives on raw HP either way; only my proposed mechanism narrows.

### 11.3 — BOUNDARY UPGRADE: the R2/R3 placement is *non-identifying*, not merely DERIVED

Elrond graded the boundary DERIVED because it collapses a 230 s gear bracket (6052–6282) to its
lower edge. The ledger says something stronger:

| | |
|---|---|
| last kill before the boundary | `play_time` **5808** (engagement 89, 1 kill, max HP 759) |
| next kill after the boundary | `play_time` **6475** (engagement 90) |
| `dps` series | falls to 0 at 5814, does not resume until **6282** |

> **There is no combat between `play_time` 5808 and 6475 — a 667-game-second gap.** Every candidate
> boundary in that interval, including 6052 and 6282, **partitions the engagement data identically.**
> The placement is therefore **non-identifying** for every engagement-level quantity, not merely
> derived-and-uncertain. Recommend `boundary_grade` carry that distinction (DERIVED-NONIDENTIFYING),
> since "DERIVED" invites a precision worry that does not exist here.

The max-HP step is bracketed to the same dead interval (last confirmed 759 at engagement 89; first
confirmed 1600 at engagement 94 — engagements 90–93 are the zero-coverage hole, so the globe series
cannot narrow it either). Consistent, and immaterial for the same reason.

### 11.4 — Two further items carried

- **Elrond's coverage-gate disagreement with galadriel is material and unresolved-by-design:** frame
  coverage vs delta coverage moves **R3 mean intake 163.3 → 188.4** (n 9 → 10). Both quantities are
  real; the store holds both. **The figure I relayed to Matt (163.3) is the delta-gated one.** R3
  intake must never travel as a bare number.
- **`life_healed`'s 3.1% rejection hides a 5× regime skew: R1 0.20% · R2 1.26% · R3 15.15%** —
  concentrated in the same thin regime that carries the coverage hole. R3 is fragile on every axis.
- **Admission carried:** intake re-derivation after a grain change needs a galadriel `tb_rollup.py`
  re-run (adjacency/bridging/spike rules live in Python, not the store). Frames are banked, so it is
  cheap — but the DB cannot re-cut the intake half by itself. This is a real cost of Option B in
  §10.3 and a reason the dual grain (Option C) is cheaper: it re-derives nothing.

**Signed:** gandalf (`RUN-CONDUCTOR` / DRIFT-CRITIC), 2026-07-28.

---

## §12 — ELICITATION OUTCOME · RULINGS R-KC1-7…12 RATIFIED · HALT H-1 RELEASED (2026-07-28)

Matt requested the launch-grill's descendants be answered rather than merely elicited ("ultra
think through your own questions … let me know … what your recommendations are"), then ran two
further ultra-think rounds that reshaped the slate — the **instrument-canonical** resolution of
Fork α, and the **authority-asymmetry / capability-gate** recognition. All six rows ratified
verbatim: **"Ratified on all six rows, cascade."**

### 12.1 — The ratified ledger extension (veto-open, as all rulings)

| # | Ruling |
|---|---|
| **R-KC1-7** | **Two join layers, both required.** *Identity* join = `.arz` record path (community build ↔ corpus ↔ `.gdc` save ↔ sim kit spec). *Measurement* join = common ledger schema + `harness_version`. Neither substitutes for the other. |
| **R-KC1-8** | **The engagement grain is INSTRUMENT-CANONICAL** — neither fixture-local nor RDR design ontology. It is a versioned property of the shared measurement harness (`harness-v1` = §10.3 Option C: encounter gap > 5 s for reporting/TTK/intake; burst ≤ 1.5 s as pack-proxy carrying A and B). Applied identically to any ledger: GD-OCR, sim-adapter, Godot-OCR. Comparisons join on `harness_version` (structural like-for-like). Declared instrument limits of harness-v1 on this fixture: **19.2% of combat-state time (240 s of 1,250 s where dps > 0) falls outside padded windows (27 stretches)**; death-counter increments at pt **2837** (outside windows AND dps spans — invisible to every instrument on the table) and pt **5152** (inside both). The dps-span/E family defers to **harness-v2**, informed empirically by the Godot calibration leg; death attribution closes only at v2 capture (input log / death-moment capture — added to the v2 recording requirements). |
| **R-KC1-9** | **R-KC1-2 amended: STRUCTURAL fidelity is the primary claim.** Targets: (i) the **A-step** (multi-kill emergence at the build swap — R1: 43 kills in 43 separate half-seconds, p = 7.0e-11; R2/R3 multi-kill routinely), (ii) the **B DoT-tail** (R3 lift confined to kill-events-per-burst), (iii) the **gear-step survivability regime change** (2.11× pool step flipping hazard shape). TTK-shape + intake-tail numeric bands are **secondary corroboration** with wide honest bands. **kills/engagement RETIRED as an accountability target** (already banked `provisional/contested`); **C declared a non-target** (player + level routing). Rationale triple-reinforced: structure is what identity-bears about a build; structural quantities are grain-robust; structure cannot be faked without the producing mechanism class. |
| **R-KC1-10** | **T-C enemy census CANCELLED.** Replaced by (a) a G-4 `.arz` task — claws AoE radius + spawn/proxy density priors (rides the same corpus pass as the transform-record read), and (b) a G-5 **density sweep** — the sim must reproduce the A-step at `.arz`-plausible densities; needing implausible density = miscalibration finding. Strictly stronger than measuring GD's density from pixels. |
| **R-KC1-11** | **Measurement architecture.** *Findings* (calibration targets) flow into sim mechanics; *parameters* (grain, sampling, gating) flow into harness + adapter, **never** into sim mechanics (the D3 Greater-Rift-timer Goodhart guard). The sim never sees pixels: a **sim-side export adapter + degradation model** (star-lord/gamora seam; spec via G-4 addendum) renders native telemetry into the common ledger schema at OCR-like conditions for fair comparison, with the exact ledger retained for diagnosis. The **Godot OCR leg** (future run, drax + galadriel) is BOTH the reverse test and the **instrument-calibration rig**: OCR-vs-known-truth yields the pipeline's error model, applied backward to tighten this fixture's error bars. |
| **R-KC1-12** | **Authority asymmetry + capability gate.** GD = genre-canon authority (100% genre-canonical); fixture = lossy evidence of it; RDR sim = **unvalidated hypothesis**; Godot = downstream presentation. Default miss attribution, after instrument error is excluded: **the sim is wrong.** G-4 carries a **mechanism-requirements manifest** — per structural signature, the mechanism classes required to express it, each marked **genre-obligatory** (absence = gap) vs **GD-specific** (absence = fine; RDR identity governs — spirit-swap, form-library, elements are design divergence, not error). G-5 grades each signature **PRESENT-CALIBRATABLE / PRESENT-MISCALIBRATED / ABSENT** *before* any numeric comparison; ABSENT routes to the build queue as a design finding. §7's honorable fallback gains its fourth miss category: **mechanism-class absence.** KC1's primary deliverable restated: **genre-gap map first, tuning target second.** Two prior collisions now read as instances of this gate firing ad hoc: retaliation (absent from simulation code → shortlist exclusion) and melee geometry (2026-05-08 finding: none exists — a live risk to A-step expressibility). Fixture portfolio consequence: iconic builds are **genome samples** — chosen to maximize mechanism-class coverage (validates the C2+C6 hedge; governs picks three+). |

### 12.2 — Consequential updates

- **HALT H-1 is RELEASED.** F-1 ruled via R-KC1-8. §11.1's selection-pressure flag
  (`C-SEG-GRAIN-UNRULED`) is discharged for the accountability targets — A is grain-invariant, B
  lives on the burst — and the reporting-unit pressure is a documented property of harness-v1.
- **HALT H-2 lightens but stands:** bands are now secondary corroboration; Matt still pins them
  before G-5 executes (preregistration discipline unchanged).
- **§7 honorable fallback amended** per R-KC1-12 (fourth category: mechanism-class absence →
  build queue).
- **Homebrew/GD-install contradiction RESOLVED on disk:** `/opt/homebrew/bin/depotdownloader`
  exists; `~/depots/` holds 45 files / 190 MB of `.arz` + `Text_EN.arc` + manifests (depots 219991,
  2699230/2699231, 897670/897671 …); Steam.app is present but `steamapps/common/` has **no Grim
  Dawn**. Matt's recollection is accurate — GD *data* was fetched via the homebrew-installed
  DepotDownloader with his credentials — and the `.gdc` probe's finding stands: a depot fetch
  contains no save; the character was played on the GD PC. **T11 unchanged.**
- **New routed work items:** (a) galadriel — `tb_rollup.py` refactor to a **source-agnostic,
  versioned harness** (home of harness-v1; discharges §11.4's rules-live-in-Python admission);
  (b) star-lord/gamora — adapter + degradation model, spec first via G-4 addendum;
  (c) Godot OCR leg — chartered later as its own desirable-pattern run, NOT a KC1 phase;
  (d) elrond — fixtures.db semantic amendments (kills_per_engagement retirement note,
  `harness_version` column convention, `DERIVED-NONIDENTIFYING` boundary grade per §11.3).

### 12.3 — Cascade fired

**G-2c** (galadriel): survivability fourth-channel + ≥10%-EHP-hit clustering within R2 (§9 ripples
1–2), with the T-C cancellation communicated. **G-4** (named `gandalf` sub-agent per §2.1
corollary): kit spec + mechanism-requirements manifest + enlarged `.arz` task list (transform
record, claws AoE radius, density priors) + adapter-spec addendum + secondary-band draft for H-2.
**Elrond amendment pass** fired non-gating. **G-5 remains held on H-2.**

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-28.

---

## §12a — POST-§13 MATT RULINGS (2026-07-28; recorded here to keep §13's run-state authoritative)

*(Sectioned out of order to avoid renumbering §13's cross-references; chronology: after §13.)*

- **R-KC1-13:** **KIT-1 = C2, Eye of Reckoning Warlord** — Matt ratified the shortlist lean.
  Names the play-test-v2 recording target; C6 Cadence remains the hedge, unruled.
- **Owner-eye item 1 RESOLVED:** Matt attests **no points in `werewolf2`/`werewolf3`/`werewolf1b`**
  ("no I didn't"). Spec §7.1 item 4 upgrades inference → ATTESTED. Matt further discloses he
  **screenshotted all of his skills** — the 313 stills at
  `/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots/` should contain
  skill-window frames. → **G-6 fired (galadriel):** locate + read skill-window shots; upgrades
  skill ranks (incl. Onslaught's exact rank, previously T11-gated) and werewolf-line absence to
  **MEASURED-by-screenshot**. Consequence for H-2: G-4 §6.5 said exact claws rank re-centres the
  A band — G-6 may deliver that **without waiting on T11**. T11 keeps its distinct payload (gear
  identity, devotion conjunctive test, potions counters, `save_identity` uid).
- **Onslaught mechanism confirmed to Matt in plain terms:** the transform swapped the active skill
  *set*; his mouse bindings kept working but drove the form's set-1 skills (claws/charge); his
  Onslaught presses fired nothing (set 0 excluded). Both set-0 counters froze at the same instant.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-28.

---

## §13 — G-4 + G-2c LANDED · T-2 FULLY CLOSED · four corrections banked (2026-07-28)

All three cascade agents returned. Elrond's M9: `fixtures-v0.6` (harness_version as a *table*
carrying harness-v1's meaning + limits; retirement on a new axis preserving `contested`;
`DERIVED-NONIDENTIFYING` adopted; A/B values flagged `C-AB-NOT-INGESTED`, queued M10).

### 13.1 — G-4: augment-vs-replacement is REPLACEMENT, MEASURED (R-KC1-6 closes fully)

Spec: `gandalf/notes/2026-07-28-kitcal1-g4-kit-spec.md`. GD partitions skills into numbered
**skill sets**; `werewolf1.dbr` selects `activeSkillSet=1`; claws + charge carry `skillSet=1`;
`onslaught1.dbr` carries no `skillSet` field → set 0 → **excluded while transformed.** Corpus-wide:
`skillSet` non-zero on exactly 18 records, all transform-granted. Fourth corroborating line, novel:
**`defaultweaponattack` froze at 74 at the same instant** — set-partition exclusion predicts both
set-0 skills freezing; augment predicts neither. **The werewolf kit is 2-active (claws + charge);
Onslaught leaves the spec's active set entirely.** Matt's testimony sub-question: answered.

**Mechanism manifest (R-KC1-12's genre-gap map):** A-step 3 PRESENT-CALIBRATABLE ·
1 PRESENT-MISCALIBRATED (**BQ-2**: cone fixed at 90°/5.0 m as module globals — not per-skill,
not per-rank) · 1 ABSENT (**BQ-1**: no `skillTargetNumber` target cap — the *only* genre-obligatory
absence). B DoT-tail **6/6 present** (incl. lethal DoT ticks + independent poison stacking).
Gear-step **6/6 present.** **The 2026-05-08 "no melee geometry" prior is SUPERSEDED** — 1D kernel
deleted 2026-06-16; the 2D spatial engine is the sole sim; grading on the stale prior would have
wrongly failed every A-step row. Trap flagged: deprecated `pack_proxy_size` path multiplies AoE
damage by aggregate pack size — under it the A-step is structurally inexpressible; **G-5 pre-flight
must assert `pack_proxy_size == 0` and fail loud.** Retaliation confirmed absent-and-out-of-scope.
Claws footprint is an **arc with a cap, not a radius**; density priors extracted for the G-5 sweep.
Bands drafted (§6 of the spec) with the structure-primary preamble; R2's A ≈ 1.74 is derived —
**G-5 re-centres A/B from `fixtures.db` (M10), not from the spec's arithmetic.**

### 13.2 — G-2c: the survivability channel is CLOSED (null), and the tail is real but terminal

Artifact: `galadriel/notes/2026-07-28-gd-playtest-v1-g2c-survivability.md`. **Q1 null at the
premise:** within-R2 EHP is a monotone nine-step function of the clock (ρ=+0.985) — zero residual
variance, so EHP-vs-behaviour is **structurally undecidable** from this fixture; all four
instruments null (|ρ|≤0.28, wrong-signed where near-significant). Raw hazard rises with EHP but
dies when EHP-normalised: **the 2.07× pool bought no net safety.** Cross-regime, R2-tail→R3 moves
**B alone** (×1.39) — the DoT signature again. The fourth causal channel is retired; R-KC1-9's
structural triad is now corroborated from every direction the substrate allows. **Q2: LATE,
decisively** (≥40 HP hits ×4.70 exposure-matched, p=9.3e-6; lowest-denominator plateaus carry
zero) — the R2 intake tail is genuine, **but** above ~75 HP it is carried by the terminal 8
engagements: **5.8% of covered time holds 43% of intake.** H-2 bands must carry that concentration
qualifier or R2's tail band will be mis-read as stationary.

### 13.3 — ⚠ SWITCH: RUN-CONDUCTOR → DRIFT-CRITIC — four corrections, two against my own §12

- **C-1 (corrects §9 and §12):** the 72.4%-EHP anchor hit **is death 1** — 541→0, 0.067 s before
  the counter increment; **floor-censored** (true damage ≥541) and not like-for-like against R3's
  max 136 (R3 has no death). My §12/R-KC1-8 claim that death 1 was *"invisible to every
  instrument"* is **WRONG**: the fatal hit is IN the banked intake series; what lies outside the
  windows is the lagged *counter increment* (respawn), which I had also measured in the wrong
  timebase —
- **C-3 (corrects §12):** the death timestamps I banked (pt 2837 / 5152) are **`pts_s`**, not
  `play_time`; true `play_time` values **3156 / 5453**. Harness-v1's declared-limits text (here and
  in elrond's `harness_version` table) must be restated: *the 19.2%/240 s combat-time non-overlap
  stands (internally consistent timebase); the death-visibility clause is corrected to "death
  events are visible as terminal intake drops (floor-censored); death-counter increments are
  lagged respawn markers and must never be used as death timestamps."* → **M10 rider for elrond.**
- **C-2 (corrects §9 ripple 4):** R2 is **not** "the longest stretch without a compound step" —
  it contains three gear events, one compound (~`play_time` 3256: +36.9% pool AND the run's only
  block change). R2 remains the fixture on sample size, not purity; the rationale is amended.
- **C-4:** globe OCR coverage degrades exactly where Q2's mass lands (ρ=−0.432) — the terminal-
  concentration figure carries a coverage caveat of its own.

### 13.4 — Run state after §13

**T-1 ✓ T-2 ✓ (fully) T-3 ✓ T-4 ✓.** Only **T-5 (G-5)** remains, held on **HALT H-2**. Build-queue
findings **BQ-1** (target-count cap) + **BQ-2** (per-skill/per-rank cone params) route to
knight-rider for sequencing — they are design findings, exactly the outcome R-KC1-12 predicted,
and pleasingly small: *one* absent class, *one* miscalibration, everything else present.
**M10 (elrond):** A/B ingestion + harness-v1 limits restatement per C-1/C-3.

**Owner-eye items pending Matt (charter §5 checkpoint):** (1) the spec's **largest sensitivity —
`werewolf2`**: if allocated, claws carries a second bleed DoT + life-leech the spec does not model;
answerable from memory (ATTESTED) or definitively by the T11 save (MEASURED). (2) **H-2 timing
fork** (G-4 §6.5): pin the drafted bands now and fire G-5, or hold for T11 — which upgrades gear
identity AND answers werewolf2 — and redraft once, then fire. (3) The ATTESTED-grade list in the
spec's closing section.

**Signed:** gandalf (`RUN-CONDUCTOR` / DRIFT-CRITIC), 2026-07-28.

---

## §14 — Matt's attested-claims round + T11 executed by SSH (2026-07-28)

### 14.1 — The five attested claims, banked verbatim (owner-eye round, charter §5 checkpoint)

Matt's answers to the spec's ATTESTED list, recorded before G-6/G-7 return so that the
independent instruments confront testimony rather than inherit it:

1. **Devotion = 0.** (Stands; G-7's conjunctive three-part test will upgrade to MEASURED.)
2. **Onslaught = pressed-but-inert** — mechanism now source-proven (G-4 skillSet partition).
3. **Gear — TESTIMONY CORRECTED.** *"They were actually 4 total items, all green (rare), with two
   major items and two minor items. Major items were in the slots of weapon and amulet while the
   minor items were in the slots of Armor and Belt."*
   - **Weapon** = *Poisoned Pusquill's Tail of Corrosion* (Screenshot 323) — major
   - **Amulet** = *Menacing Putrid Necklace of Protection* (Screenshot 328) — major
   - **Armor** = *Mystic Salvaged Armor of Menhir's Wall* — minor
   - **Belt** = *Mystic Woven Cord of Soulwarding* — minor
   This **corrects §9 / F-KC1-1's "weapon, shield and amulet"**: FOUR items, **no shield** in the
   level-12 event. The correction *harmonizes* with §11.2's own falsification (block stats showed
   the shield was worn long before level 12) — testimony and telemetry now agree. "Poisoned …
   of Corrosion" on the weapon is the poison-DoT carrier the B-signature predicted. Screenshots
   (323) and (328) confirmed present on the share (numbering range 40–352).
4. **Werewolf line unallocated** (werewolf2/3/1b = 0) — resolves G-4 §7.3's largest sensitivity
   at ATTESTED grade; G-7 upgrades to MEASURED.
5. **Potions used = 0** — G-7's `healthPotionsUsed`/`manaPotionsUsed` upgrades to MEASURED.

**Grade note:** all five remain ATTESTED until G-7 lands. Any G-6/G-7 contradiction with this
section is a **loud finding**, not a silent overwrite.

### 14.2 — T11 EXECUTED (Matt directive: "please SSH into the PC"; character name supplied)

Matt authorized direct SSH and supplied the character name **"Fresh Character 01"**. Executed via
the retired PC-team target (`mhwet@192.168.1.133`, recovered from pre-teardown CLAUDE.md in git).
**Finding en route:** the save lives in **`save\user\`** (custom-game campaign directory), not
`save\main\` — the play test ran on a custom campaign, which is why the to-do's two candidate
paths both missed. Whole folder copied (tar-pipe) to
`/Volumes/reincarnated/matt-notes-from-pc/gd-save/_Fresh Character 01/`; `player.gdc` 15,473 B,
SHA-256 `0be3a99f…d5ee91`, source mtime **2026-07-26 5:57 PM — play-test day, untouched since**:
the end-of-run state survives intact. No `Backup/` subfolder exists in the cloud-save layout.
**G-7 fired** (legolas, `.gdc` parse per the probe map): devotion conjunctive test, every skill
rank incl. Onslaught's hidden rank, gear record paths joined against the four §14.1 names,
`playTime` drift vs ≈7094, `uid` for the `save_identity` join key. To-do doc marked DONE.

### 14.3 — R-KC1-14: G-5 remains the run's finale — the run-vs-program distinction (Matt challenge, ruled veto-open)

Matt: *"how could this be the finale of the run? We just decided that making a random werewolf
character early on would have little to no value versus making the end game character (C2 Eye of
Reckoning Warlord) as first run kit."*

Ruling: **both stand, at different scopes.** R-KC1-13 (KIT-1 = C2 EoR Warlord) governs the
*program* — which build the accountability pipeline serves first at production grade. G-5 governs
*this run* — KC1 is the **commissioning lap**, and the werewolf fixture is **the only build in
existence with measured GD gameplay**. C2 has no fixture until play-test v2 is played; a C2-first
G-5 would compare the sim against nothing. G-5's product is not "werewolf balance data" — it is
**proof the whole pipeline closes**: kit-spec → sim run → common-ledger export → structural triad
comparison → capability-gate grading, exercised end-to-end on a fixture that cost nothing further
to obtain, *before* Matt spends an expensive v2 session generating the C2 fixture. Commissioning
on the cheap fixture protects the expensive one. The C2 lap is the **next run**, reusing every
piece G-5 proves. Skipping G-5 abandons the werewolf fixture at peak value — precisely as G-6/G-7
upgrade it from attested to measured identity. **Veto-open:** if Matt rules the commissioning lap
itself expendable, T-5 strikes cleanly and the run closes at §13's state.

### 14.4 — C-5 correction + Matt's opposition-comparability gate (H-3) — G-5a/G-5b fired

- **C-5 (Matt, corrects §14.2 and the T11 doc's framing):** `save\user\` is NOT a custom
  campaign. It is *"a blank folder that opens the game in full production mode, but with the
  console capability."* The play test ran **shipping Act-1 campaign tuning** — the fixture's
  opposition is production-canonical, which *strengthens* its authority as ground truth.
- **H-3 (Matt gate, verbatim):** *"Before I agree to any value in G-5, I need to know how our
  current RDR battle sim's monsters compare to GD level 12 monsters. Otherwise, what is the
  point? We build it so that the werewolf loses to high level monsters?"* — G-5 is now
  additionally held on an **opposition-comparability audit**. This is R-KC1-12's authority
  asymmetry applied to the monster side: with untuned opposition, a G-5 miss is unattributable
  (kit-model failure vs opposition mistuning are confounded). Resolution frame: **measure GD's
  level-12 opposition from `.arz` source and PIN the sim's opposition to those values** — the
  kit becomes the only free variable. Two read-only passes fired in parallel:
  - **G-5a (legolas):** GD level-12 opposition ledger from the Edition-II corpus — scaling
    mechanism, Act-1 proto values at level 12 Normal (HP / damage-per-hit / cadence), pack
    priors, and the dimensionless ratios vs the fixture's measured player pools (759/1600).
  - **G-5b (gamora, read-only census):** the sim's monster stat model; the **injection
    question** (can a harness supply bespoke monster + player stats without code change —
    YES / NO / YES-WITH-CHANGE); today's generated ranges at an early-game tier for the
    side-by-side; `pack_proxy_size` reachability.
  **Decision rule:** G-5a × G-5b compose into a comparability verdict Matt reads *before*
  ruling on G-5. If injection = NO and the change is non-trivial, that is itself a build-queue
  finding (the sim cannot currently be pointed at external ground truth — a capability absence
  senior to BQ-1/BQ-2).

### 14.5 — G-7 save parse landed + Matt reconciles testimony to the measured record

The G-7 parse completed (artifacts at `legolas/scratch/2026-07-28-gdc-parse-g7/`; findings note
in flight after the first agent died post-parse on a stream timeout). **Fixture identity
proven:** `playTime` 7096 vs run's ≈7094 (2 s), deaths 2 (exact telemetry match), kills 882.
Measured record: devotion conjunctive test **PASSES** (3 earned / 3 unspent / 0 reclaimed / all
`devotionLevel` 0); **Onslaught rank 13**; **werewolf1 rank 16** (claws/charge mirror at 16,
`enabled=0` while untransformed — second-source confirmation of the G-4 skillSet partition);
**werewolf1b rank 1**; potions 0/0 MEASURED; attributes 122/74/50; level **13** (bio; play_stats
`maxLevel` lags at 12); greatest kill `tagSlithBossB02` level 13, 15,822 life+mana; `uid` all
zeros → `save_identity` falls back to SHA-256 (flags artifact-verification §505). Gear: all four
attested items match structurally (rare blunt weapon + rare necklace + Menhir's-Wall-class torso
suffix + Soulwarding-class belt suffix); shield IS equipped (rare base) — consistent with §11.2's
"worn long before level 12", not with the level-12 event. English-name verification in flight.

**Matt reconciliation (verbatim, supersedes §14.1 rows 4 and the level attestation):** *"I did
level to 13, you're right. I mis-quoted my level at 12. I did level the two werewolf nodes, and
if I indicated otherwise, I must not have understood your question in context."* → Level = 13
MEASURED+CONFIRMED; werewolf1 (16) + werewolf1b (1) allocation MEASURED+CONFIRMED; the §14.1
"werewolf line unallocated" attestation is retired as a question-framing artifact, not a memory
dispute. **werewolf2 (bleed+leech, the spec's largest sensitivity) remains measured-absent** —
the save lists no allocation. **Process note:** this is the attested→measured discipline doing
its exact job — two testimony errors caught by instruments within hours of banking, zero drama,
because grades were carried instead of trust. Kit-spec + H-2 bands now redraft on measured
identity (level 13, claws 16, Onslaught 13, four greens + shield) per G-4 §6.5.

### 14.6 — H-3 comparability verdict: G-5a × G-5b × G-7-note synthesis (decision package to Matt)

All three passes landed (legolas `9838449d` G-5a ledger; gamora `4b972902` G-5b census; legolas
`d311ec1b` G-7 findings note — all pushed).

**G-7 note headlines:** gear names **4/4 EXACT** character-for-character against Matt's testimony
— hard verification of the whole `.gdc`→`.arz`→`.arc` chain. Ranks proven **base hard points**
(budget closes 37 = 36-from-levels + 1 quest; +skills sources empty). Level 13 proven twice from
`.arz` arithmetic (XP thresholds; attribute bytes). "All four green" refines to: weapon+amulet
Rare **bases**, armor+belt Common bases with Rare-class **suffixes** — Matt's major/minor split
partitions exactly along that boundary. **`werewolf1b` = "Blight of Ch'thon"** (`GDX3.arz`,
transmuter, max 1): its whole effect is **100% Pierce→Chaos conversion** + blighted mesh. **The
kit's pierce output is chaos-typed.** Resolution: conversion is static/total, so it compiles into
the kit spec as retyped damage — no sim conversion mechanism needed (degradation-model note).
Follow-on **U-1**: extract rank-16 array values for werewolf1/claws/charge + the four items'
rolled stats (reader exists in scratch).

**Comparability verdict (H-3):** GD level-12 Normal/1P opposition (28 protos, 16 spawn pools):
monster HP 181→35,198 (200× span — HP is the differentiation axis) while per-hit damage sits in
a **33–67 band ≈ 2.5% of the 1600 post-gear pool**; concurrent melee capped by
`numAttackSlots=4` (~10% pool/round). Sim today: player 14,555 (floor 10k), hits 625–2,500
(4–17% pool), cadence 1.4 s. **Absolute scales ~10× apart — but moot under pinning**, which
G-5b proved possible for monsters with zero engine change. Two genuine gaps: (1) **BQ-3** —
player `max_hp` floor + hardcoded-zero defence path block the fixture's 759→1600 pools (~9
default-inert lines, gamora + Gate-2); (2) **attack-slot arbitration likely ABSENT in sim** —
with GD pack sizes injected and no 4-slot cap, concurrent pressure overstates ~2.5×; harness
compensation (cap effective attackers) or manifest row. G-5a's one DERIVED risk — the
`monsterAttributePak` multiplicative reading — is validatable **against the fixture itself**
(predicted 33–67 band vs the measured intake distribution; `hitsReceived=500`), no live client
needed.

**Proposed R-KC1-15 (HALT — H-3 is Matt's commitment-boundary):** (a) BQ-3 lines via gamora,
Gate-2 reviewed; (b) U-1 rank/item-value extraction; (c) pak validation via fixture-intake join;
(d) harness pins monsters from the G-5a ledger (spawn pools + 4-slot compensation) and player
from the measured kit, pre-flight asserts armed (`pack_proxy_size==0`, ×1.5 HP multiplier off,
0.6 damage scale accounted, no skill-less mobs); (e) chaos retype at spec-compile; (f) **then
G-5 fires.** Awaiting Matt's ruling.

### 14.7 — G-6 lands (galadriel `3425c062`): triangulation complete, and the pixels carry history the save cannot

All chartered instruments have now reported. G-6 ran **blind** to T11/G-7 (they landed mid-pass)
and **independently agrees on every shared claim** — testimony, save bytes, and pixels now
triangulate. What only the pixels know (37 skill-window frames, dated on `play_time` via the
panel reader; ledger endpoints read exactly at f352):

- **Ranks are DATED, and R2 is NOT A-stationary:** claws' target cap grew **2→3→4→5** and its
  arc **90°→150°**, capping at `play_time` 2918; transform maxed (16) at 3619; Onslaught sat at
  rank 1 until level 9 with its counter frozen at 54. H-2's A-step band must segment R2 or draw
  from the post-2918 window — v2 fork.
- **Two allocated skills the v1 spec missed, both switching on mid-R2:** **Battle Surge** r1
  (crit-gated self-heal, 8% max-HP/s × 3 s on 6 s recharge — unmodelled sustain channel) and a
  **cold aura** r1 (+16 Armor / +20 DA).
- **U-1 substantially delivered from tooltips:** the 759→1600 step is **87.6% itemised** (+737
  of +841 from four flat +Health affixes); ~109+ Armor accounted; weapon poison DoT **50 dmg /
  5 s**; the kit runs **six damage channels and two conversions** vs the v1 spec's two channels.
- **Fifth independent line for the G-4 skillSet ruling, in GD's own words:** the transform
  tooltip reads *"cannot trigger weapon pool skills."*
- BQ-1/BQ-2 sharpened: GD's target cap is a *rank-scaling* mechanic (2→5) and claws' end-state
  arc is **150°**, not the sim's fixed global 90°.
- Devotion tab visible in all 37 frames, never selected — no devotion frames exist; the save's
  MEASURED zero stands as the sole (and sufficient) source.

**Consequence fired (pre-authorized by G-4 §6.5):** kit-spec **v2** redraft dispatched to the
named gandalf sub-agent — full measured identity (level 13, chaos retype, Battle Surge + cold
aura, dated A-step, six channels), normalized-units bands per G-5b §7.3, ending in the **H-2
pin-sheet** for Matt. R-KC1-15 remains HALTed to Matt; the redraft is robust to any line-strike.

### 14.8 — R-KC1-15 RATIFIED AS AMENDED (Matt) — the path to G-5 is live

Matt ratified all six lines with three amendments:

1. **BQ-3 + CONTAINMENT MANDATE (verbatim):** *"I agree, but ultra-think and implement whatever
   is needed to ensure these lines/values are NEVER used in the sim/pipeline. We need to build
   out real mechanisms and fit them to the kits in the future."* — The overrides are a
   calibration-harness-only door, structurally sealed against production leakage (namespaced
   `_calibration_overrides` block, NOT the existing `defense` key; explicit opt-in flag default
   False; negative asserts at production boundaries; output stamping; byte-identity regression
   test). Gamora implements + Gate-2. **Design significance:** the mandate also states the
   forward obligation — the real player-defence/HP mechanisms remain OWED and must be built and
   fit to kits later; the override must never dull that pressure.
2. **U-1 EXPANDED:** *"use all of the item's rolled stats"* — all 12 equipped slots, not just
   the four greens. Plus rank-16 arrays (claws/charge/transform), Blight r1, Battle Surge +
   cold aura confirmation, Onslaught r13 marked INERT.
3. Pak validation vs fixture intake — ratified; galadriel joins predicted 33–67 band against the
   measured per-regime intake distribution (mitigation-aware, alias/DoT/censoring-aware).
4. Harness pins ratified; **Matt's addition ACCEPTED — tiered scenarios:** *"should we also
   represent one rare/elite/boss fights as well using GD rare+ monsters tuned to level 13ish?"*
   → YES: (a) trash-pack scenarios (spawn-pool pinned, A-step target), (b) champion/hero mixed
   pack, (c) **boss single-target pinned to `tagSlithBossB02` at charLevel 13 — the fixture's
   own greatest kill (15,822 life+mana measured)**, giving a measured single-target/DoT-tail
   endpoint the pack scenarios can't. U-1 resolves its record; the 15,822 cross-check doubles
   as a live-client validation of the whole G-5a resolution chain.
5. Chaos retype at spec-compile — ratified.
6. G-5 fires when (1)–(5) + the H-2 pin land.

**Fired in parallel:** gamora (BQ-3 + containment), legolas (U-1 expanded + Slith/champion/hero
resolution), galadriel (pak validation). Kit-spec v2 redraft still in flight; its pin-sheet is
the remaining Matt gate (H-2) before G-5.

### 14.9 — Kit-spec v2 lands (`19ddb998`): six channels, W-c window, the 8-pin H-2 sheet, and C-6

Spec: `gandalf/notes/2026-07-28-kitcal1-g4-kit-spec-v2.md`. Headlines:

- **Six damage channels compiled** (v1 had two): physical (weapon 14–40), acid (weapon base +
  18% phys→acid affix conversion), chaos (claws 237 + charge 375 flat, Blight retype), poison
  DoT 50/5s (weapon affix roll — falsifies v1's `componentName` hypothesis), bleed DoT (charge,
  810 over 3 s, present R2 *and* R3), cold (Amatok's Pact; Onslaught's cold cannot fire). Plus
  the near-missed seventh contributor: **charge's 295% off-hand reads LARGER than main-hand**
  (the shield) — single-weapon compile would understate ~2× (pin P-7).
- **A-step window: W-c, `play_time ≥ 3619`** (49 engagements, 421 kills) — kit-exactness binds,
  not A-stationarity: A's pre/post-2918 CIs overlap, but **B moves ×1.347 across the
  composition event** (Blight+Battle Surge+Amatok, bracketed to (2918, 3619]) with no DoT added
  at that boundary. Whole-R2 would contaminate B by a lift the size of S-2's own signal.
  Segmenting to W-c *hardens* the S-2 target: v1 ×1.30 → **×1.218**. Costs 5 engagements.
- **Pin-sheet (8):** P-1 window choice (lean W-c) · P-2 ratify S-1/S-2/S-3 structural bands ·
  P-3 ratify N-1..N-12 numeric bands · P-4 N-12 grain (accept R2-whole vs galadriel re-cut) ·
  P-5 coverage gate (a ≥0.80 gate would EXCLUDE the fixture's worst hazard event) · P-6 gamora
  D1 check (attacker-targeted `on_crit` consequence expressible? else Battle Surge → BQ-4) ·
  P-7 off-hand compile · P-8 pak-validation-first (already in flight, §14.8). **P-1/P-2/P-3
  gate G-5.**
- **C-6 (⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC, against my own §13.3):** the 72.4% anchor is
  death **2** (`play_time` 5453, e082), not death 1 — C-1's numbering was made in the pre-C-3
  timebase. R-KC1-8's death-visibility clause **stands as originally written**. M10 rider
  amended accordingly (elrond gets C-6 with C-1/C-3).

### 14.10 — P-8 returns: the pak's multiplicative reading is FALSIFIED — the fixture corrects the ledger (galadriel `5d6c004e`)

**Verdict: FAIL as stated — the fixture confirms the ADDITIVE pak stage** (LR 96:1 in the
cleanest window, 733:1 in the second; hard integer-feasibility closes it — the multiplicative
floor of 6.46 sits above five measured level-1 drops of 4–5). The composite-drop aliasing rate
independently re-derives `numAttackSlots=4`. Reframing finding: the fixture has ~35 s of
level-12 combat — the 759 pool is **level 11**; the level-12 band is DERIVED-by-extrapolation.

**Consequences for the G-5a ledger (corrections owed):**
- Trash damage rows rescale **×0.74** — charLevel-12 tier-01 becomes **27–33**, not 36.6–45.1.
  §14.6's "33–67 band" headline was an artifact of the falsified operator.
- **Champion/hero/boss damage rows fall into an unmeasured clamp regime → UNRESOLVED, not
  DERIVED** — they must NOT enter G-5 pinning until the clamp is resolved. This holds the
  champion-pack and Slith-boss scenario tiers (§14.8 item 4) on their *damage* side; the
  boss's 15,822 life+mana cross-check (HP-side) is unaffected. U-1 (in flight) resolves Slith
  under the old operator — its damage rows re-grade on landing.
- G-5a's falsification-of-additive was itself thinner than stated (Warden's `+4` adjuster not
  carried); the operator question is now settled the other way by measurement.

**Hardening options for the clamp (route after U-1 lands, not before):** (a) legolas source
pass on the `armorbase03–06` clamp behavior; (b) galadriel's cheapest-hardening proposal — **60
seconds of level-1–2 GD capture with nameplate OCR** (a micro-ask for Matt, C4-calibrated
reader ready). **Process note:** this is P-8 doing precisely what Matt ratified it for — a
wrong operator caught by pre-registered validation *before* it entered the harness, at the cost
of one read-only pass. The pin-sheet itself is unaffected (bands are fixture-side; opposition
numbers feed the harness).

### 14.11 — U-1 lands (legolas `156229b2`): kit values closed to source; the Slith check FAILS clean and corrects the ledger's HP side too

- **Claws @16 fully pinned, five-for-five against G-6's tooltip frame:** 150% weapon dmg, flat
  237 pierce→chaos, **target cap 5, arc 150°**, mana 5, no cooldown. Cap+arc **saturate at rank
  13** — the whole W-c window sits post-saturation. Kit carries **no skill-native physical**
  (spec-v2 channel-1 reconciliation item: physical exists only as weapon-carried, post the 18%
  acid conversion).
- **The transform grants ZERO stats at any rank** (`werewolf1.dbr` has no `characterLife`
  arrays) — G-7 §7's parked transform-HP hypothesis is dead; the gear-step is gear, full stop.
- **+Health cross-check PASS** — nominal 700, window [627,773], G-6's +737 at the 52nd
  percentile; the boots' affix is a **5% modifier** whose resolution (76.2 vs pixel-read +75)
  *independently corroborates the 1600 endpoint*. Gear step now **≈96.6% itemised**. Residuals:
  weapon flat 220 vs pixel 242; armour 337-base/≈380-resolved vs G-6's "109+" needs a re-crop
  before `mitigation_delta` (N-band) is pinned — galadriel item.
- **Slith cross-check: FAIL by +22%** (chain 19,294 vs measured 15,822) — and the miss is a
  *finding*: only charLevel 13 yields integrality, requiring a net life-modifier pool of
  exactly −36.00% where the chain composes −21%. The client's number over-determines the level
  and indicts the HP composition rule by a flat 15 points. **Every G-5a HP figure is 16–19%
  high** (trash ×0.837, boss ×0.810; Warden 61,353 → 49,706). Damage side untouched (that
  correction came independently from §14.10).
- **The symmetry worth naming:** the fixture carried exactly two live-client numbers — the
  intake distribution and one boss HP triple — and each falsified a *different* half of the
  derived opposition ledger (damage operator; HP composition). Co-pinning discipline, vindicated
  twice in one evening. **Closure path:** one more `greatestMonsterKilledLifeAndMana` triple
  from ANY other GD save pins the composition rule → ask Matt whether other character saves
  exist on the PC (SSH re-check is a one-line dir listing; new-scope, so Matt-gated).

### 14.12 — BQ-3 lands (gamora, tag `gamora/v-bq3-calibration-door-1` @ engine `c067bbd`): the calibration door built under Matt's NEVER-used mandate; Gate-2 filed

Matt's amendment to ruling 1 (§14.8, verbatim): *"ultra-think and implement whatever is needed
to ensure these lines/values are NEVER used in the sim/pipeline."* Gamora's implementation
honours the mandate **structurally, not conventionally** — six layers:

- **L1 — namespaced key.** Overrides ride ONLY under `class_dict["_calibration_overrides"]`.
  **Gamora overruled her own G-5b census §5.3 here**, and the overrule is the best call in the
  work: the census proposed soft-reading the existing `defense` key ("it already exists"), but
  the kit compiler emits `defense` on *every* compiled kit — so the day the REAL defence
  mechanism (the one Matt's amendment says is still owed) starts emitting `defense.armor`, the
  census design would have **silently activated the calibration door** on every production
  fight. The trap was armed by the future roadmap itself.
- **L2 — keyword-only `allow_calibration_overrides=False`** at all three player-building
  entries (`entity_from_class_dict`, `combatant_projection_from_class_dict`,
  `run_spatial_fight`).
- **L3 — the teeth: present-but-not-allowed RAISES.** A dict carrying the key cannot be
  simulated *at all* by a non-opted-in path. Not "production must remember not to pass the
  flag" — a structural crash, which is what NEVER means.
- **L4 — unconditional asserts** (no opt-in parameter even exists) at the four production
  entrypoints: `run_slot`, `run_slot_smoke`, `_run_kit_slot_worker`, `_w4g_run_fight_batch`.
- **L5 — AST sweep** (not grep — docstrings quote the flag name) for `=True` call-sites;
  allow-list currently empty.
- **L6 — provenance stamp** on `SpatialFightResult` + MIGRATION entry.

Deliberately NOT built: env var, global flag, registry — all forms of process state a run can
inherit by accident. **Evidence:** production-path digest `25c212eb…` captured on the
pre-change commit, byte-identical post-merge AND with the door present but no overrides;
39/39 new tests; 1,578-test regression with 55 pre-existing failures **diff-empty** vs a
stash baseline; KF-4 smoke 36 GREEN. Forward obligation restated per Matt's ruling: this door
is scaffolding — *real* defence + HP mechanisms fitted to kits are owed, and L1's namespacing
is what keeps that future work from colliding with this one.

**Gate-2:** `agentic_orchestration/qa/pending/2026-07-28-gamora-bq3-calibration-override-door.md`
(meta `11a441f9`) — §1 asks jack-ryan to rule *explicitly* on the census departure rather than
letting it pass as implementation detail. Both repos + tag pushed per the cycle push-pattern;
the Gate-2 file's "committed never pushed" line is superseded by this landing record.

**Run-state after §14.12:** every chartered instrument and every R-KC1-15 work item except the
harness itself has returned. G-5 now waits on exactly four things: (1) Matt's pin rulings
(P-1/P-2/P-3 gate; P-4/P-5/P-7 shape), (2) jack-ryan Gate-2 on BQ-3, (3) the P-6 gamora check
(attacker-targeted `on_crit` consequence for Battle Surge, else BQ-4), (4) clamp/HP-composition
closure for the champion/hero/boss tiers (§14.10–§14.11 corrections applied; other-saves ask
open with Matt).

### 14.13 — R-KC1-16: the pin-sheet RATIFIED as leaned; the death-2 killer named; frame 281 turns out to carry the client's own scoreboard

**R-KC1-16 (Matt, verbatim: "Ratify all as leaned"):** the full H-2 pin-sheet lands on the
conductor's stated leans — **P-1** window = W-c (`play_time ≥ 3619`, post-saturation, 49
engagements / 421 kills) · **P-2** structural triad S-1/S-2/S-3 ratified (S-2 at the W-c-hardened
×1.218) · **P-3** normalized units N-1..N-12 ratified · **P-4** N-12 at R2-whole grain (no
galadriel re-cut) · **P-5** coverage gate ≥0.80 WITH the named exception for the worst hazard
event (D3 Goodhart discipline) · **P-7** dual-hand compile (charge's 295% off-hand reads) ·
P-6/P-8 were process pins (P-8 already executed §14.10). **The G-5 gate set by R-KC1-15 is now
pin-complete.** Remaining before G-5 fires: jack-ryan Gate-2 on BQ-3, the P-6 check (in
flight), boss/champ-tier clamp + HP-composition closure.

**Matt's second attestation of the message — the death-2 killer has a name:** *"it looks like I
did screenshot my death number two (screenshot 281) from the Primordian, The Forgotten One
(Beastkin) enemy monster."* Conductor read of the full-res frame
(`/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots/Screenshot (281).png`)
finds far more than the killer's nameplate — **the console Play-Statistics overlay is OPEN at
the death instant** (provisional naked-eye reads, all pending galadriel C4 calibration, G-8):

- Play Time **90 min 53 s = 5453 s** — the frame self-dates to C-6's death-2 anchor (e082)
  exactly. Deaths **2**, kills **~655** (vs 882 final), potions **0/0**.
- **"Damage per second: 743.22"** — the client's OWN lifetime-DPS figure. First measured
  damage-output scalar for the fixture; a direct external check on the kit-spec's compiled
  output and on S-1/S-2 once windowing semantics are established (lifetime-average vs W-c).
- **"Life healed: ~5649"** — measured lifetime healing. Battle Surge's mechanism (P-6/BQ-4)
  now has a fixture total waiting for it, whichever way the expressibility check lands.
- **Skills Used table with per-record USE COUNTS** (claws ~245, charge ~125, weaponattack ~74,
  defaultbioattack ~13, …) — the measured **skill-mix channel** for the G-5 harness driver.
  Nobody chartered this instrument; the fixture volunteered it.
- **One collision flagged, not smoothed:** the left orb may read `0/747` at death — inside R3,
  where the banked gear-step timeline says max HP is 1600. G-8 is tasked to verify or refute
  LOUDLY before anything re-opens.
- The named-exception loop closes on itself: P-5's excluded worst-hazard event is a fight
  against the monster whose **guaranteed drop is the fixture's amulet** — Matt died to
  Primordian at 5453, then killed it and wore its necklace through the rest of the run.

**Lanes fired (all read-only):** **G-8** galadriel — calibrated OCR of frame 281 + the
270–295 neighborhood + a corpus-wide sweep for any monster-HP numeric (a second HP triple pins
the §14.11-corrected composition rule). **P-6** gamora — on_crit attacker-targeted consequence
expressibility, file:line evidence, verdict EXPRESSIBLE-NOW / WITH-GLUE / BQ-4. **Primordian
proto** legolas — raw fields from the Edition-II corpus (damage rows raw, NOT composed through
the held champion/hero/boss regime; HP fields staged for when the composition rule pins);
Primordian is the natural hero/boss-tier scenario candidate alongside Slith.

**Open to Matt (from his own question, held as Q-KC1-1):** whether the P-6/BQ-4 outcome should
expand into building the REAL mechanisms behind gamora's 9 inert lines now. Conductor
recommendation delivered in-session: yes, but as the **next wave, with G-5's output as its
acceptance fixture** — not coupled to G-5 (full argument in the session record; the door was
built precisely so calibration need not wait for mechanisms, and mechanisms built pre-G-5
would be fitted to theorycraft instead of measurement). Awaiting Matt's ruling.

### 14.14 — P-6 resolves (gamora `c3907354`): NOT-EXPRESSIBLE → **BQ-4**. Battle Surge exits the kit spec's live surface

Verdict with file:line evidence (note:
`agentic_orchestration/gamora/notes/2026-07-28-kitcal1-p6-oncrit-expressibility.md`). Three
legs, one healthy:

- **on_crit trigger — produced, then dropped.** `"on-crit"` is legal spec vocabulary
  (`resource_economy.py:126-134`) and the damage resolver emits crit events
  (`damage_resolver.py:1349`), but NO call site logs them into the Wave-C event stream — the
  five live triggers are on-hit / on-kill / on-defender-death / on-block-successful /
  on-damage-taken (`spatial_engine.py:4545-4731`). The player attack path never sets
  `return_events=True`; only mob→player does. A vocabulary naming bridge (`on_crit` vs
  `on-crit`) is also absent.
- **Attacker-targeted consequence — EXISTS** (`_wave_c_dispatch_consequence` resolves
  `resource-fill` onto the attacker, `spatial_engine.py:3759-3761`) — **but no heal payload**:
  `CONSEQUENCE_TYPES` has no heal member.
- **3s HoT + 6s ICD — NO on both.** The deepest find: `heal_over_time` exists
  (`effect_resolver.py:121-130`) but **its recovery lands on scratch state and never reaches
  spatial HP** (`spatial_engine.py:5163/5186` — only the DoT side syncs). No per-proc ICD
  primitive at all.

Gamora correctly declined to glue: the HoT→spatial-HP bridge is a Discipline #12 semantic
shift, and trigger-vocabulary extension crosses into rocket's seam. **Consequences for the
run:** Battle Surge r1 moves from PRESENT-CALIBRATABLE-candidate to **ABSENT (BQ-4)** under
the R-KC1-9 capability taxonomy — the kit spec carries it as a named inert entry with its
fixture number attached (client-measured "Life healed: ~5649" over 5453 s, G-8-pending). G-5
proceeds without self-heal; the fixture's death-2 hazard event is *conservative* in the sim's
favor is NOT claimable (healing helped Matt survive R3 — its absence biases the sim werewolf
FRAGILE, which is the honest direction to miss in, and it is now quantified, not vibes).
**BQ-4 joins the Q-KC1-1 defensive-mechanics wave** (max-HP derivation, armor/mitigation,
on_crit self-heal, HoT spatial bridge) — three of its four members now have measured fixture
targets. BQ-1/BQ-2/BQ-4 route to knight-rider for sequencing after Matt rules Q-KC1-1.

### 14.15 — Matt REJECTS the sustain-free framing (C-7); Primordian lands and IS the Slith boss; the save yields four unregistered fields; sustain fork opened (proposed R-KC1-17)

**C-7 — Matt (verbatim):** *"No, this is not possible. The 5,649 self heal loss is too large of
a deficit, unless some of this comes with natural Health Regen and that makes it into the
sim."* ⚠ SWITCH: RUN-CONDUCTOR → DRIFT-CRITIC on my own §14.14: the "conservative miss / honest
direction" line is **withdrawn**. G-5's verdict is FIDELITY — a sim werewolf that dies where the
player lived fails calibration exactly as badly as the reverse. Conservative bias is still
bias; §14.14's closing claim does not survive its own run-intent (rubric law, desirable-pattern
amendment 3: the owner's question is twin-fidelity, not survival-with-handicap).

**Four play_stats fields surfaced from the G-7 parse, previously unregistered:**
`hitsReceived = 500` (one hit per ~11 s lifetime average — intake is sparse),
`criticalHitsInflicted = 66` (→ Battle Surge is BOUNDED: ≤66 procs all run),
`criticalHitsReceived = 0`, `greatestDamageReceived = 260.498` (hardest single hit of the whole
run — a measured POST-mitigation bound the held §14.10 boss damage regime must respect; third
live-client number). One contradiction flagged: `lastHitBy = 273.704 > greatestDamageReceived`
— same-scale numbers can't do that; semantics probe assigned. Rate framing: 5,649 over 5,453 s
≈ **1.04 HP/s lifetime** — trivial per trash engagement (~20 HP per 20 s vs a 1600 pool),
decisive only where it concentrates: long boss fights. **The deficit is a boss-tier problem,
not a global one — but boss-tier is S-3's home, so Matt's challenge stands where it bites.**

**Primordian proto lands (legolas `c714174c`) — three reshaping finds:**
1. **`tagSlithBossB02` IS Primordian.** One entity — the measured 15,822 triple belongs to the
   monster that dealt death 2. §14.11's "Slith cross-check" was already a Primordian check;
   §14.13's "hero-tier candidate ALONGSIDE Slith" is corrected: the run has ONE measured boss.
2. **The 15,822 carries a ≈+300 stochastic gear term** (`chanceToEquipMisc2 = 100` — it wears
   a rolled rare necklace every spawn; the fixture amulet's own base, before it dropped). The
   §14.11 closure criterion TIGHTENS: the next triple must come from a monster with zero
   `chanceToEquip*` slots. Also: charLevel 13-vs-16 ambiguity (`+3` remapper on `lv6_hero`) —
   cl 13, cl 17-multiplicative, and cl 11+gear all land within 1–2% of measured; one number
   cannot separate them.
3. **The death-2 encounter is a mandatory TRIO** (`slitha_melee_b01` + `slitha_shaman_c01`,
   both `alwaysSpawn`) with an ~85%-cold kit: 16-projectile 360° freeze ring
   (`projectileUsesAllDamage`), 8 s blizzard field, ice-armor phases (25% absorption, 12s-on/
   32s-off), `NeverFlee`, 75 m pursuit. Burst-heavy — which is exactly the profile that
   punishes cheap sustain approximations. Boss-tier scenario = the trio, or the simplification
   named. Classification `Quest`, `numAttackSlots 8`, no weapon / no `damagebonus_*` (better
   clamp fixture than Warden Krieg).

**Lanes fired (read-only):** legolas — sustain decomposition ("Life healed" inclusion
semantics: constitution / passive regen / leech / skill heals / overheal; passive regen/s
computed from save+corpus incl. Menhir's Wall + Soulwarding suffix resolution; Battle Surge
band under the 66-crit bound; the lastHitBy contradiction). gamora — passive-regen census
(does ANY per-tick HP regen reach spatial HP; minimal door-gated tick estimate; EHP fold-in
distortion verdict against Primordian's burst profile). G-8 galadriel still in flight (char-
sheet regen frame added to its follow-up scope on completion — no SendMessage surface).

**Proposed R-KC1-17 (held for Matt, decision-shaped):** boss/champion-tier scenarios carry
measured sustain via one of — **O-a** pin native sim regen (if it exists) · **O-b** minimal
flat-HP/s tick gated behind the BQ-3 door (small gamora build, dies when the real wave ships) ·
**O-c** EHP fold-in via existing door (zero code; burst-ordering distortion under assessment).
NOT on the table: sustain-free boss scenarios (C-7), or blocking G-5 on full BQ-4. Conductor
lean: O-a if native, else O-b — a measured tick is honest where EHP is convenient, and
Primordian's nova punishes convenience. Trash tier proceeds sustain-free with an insensitivity
assertion either way. Ruling lands after the two probes return.

### 14.16 — The sustain question RESOLVES by measurement (gamora `72976462`, legolas `e2f3e3fe`): the pivot is LIFE LEECH, and the kernel already knows how

**Regen census (gamora):** O-a DEAD — no passive HP regen reaches spatial HP anywhere (the
energy twin ticks at `spatial_engine.py:5057`; the HP side of the same loop simply does not
exist; upstream `regen_per_sec` dies three breaks before a fight — the same corpse as the BQ-4
HoT bridge). O-c DEAD for boss tier — EHP fold-in vs a 16-projectile nova is an
**outcome-flip** error, not magnitude (the engine's own `bc_measurement.py:199-205` already
demotes fold-in to fallback). O-b sized at ~16 lines but see below — the measured rate makes
it moot.

**Sustain decomposition (legolas) — the premise reshapes:**
- **"Life healed" is CLAMPED** — no overheal, no respawn refill. It measures *damage absorbed
  and recovered from*. Cleanest proof: 5,649 ÷ 500 hitsReceived = **24.94 HP/hit — landing
  exactly on the G-5a post-mitigation trash ledger** (the fourth independent client-side
  validation of the corrected damage operator).
- **~52% is Constitution** (out-of-fight; live in this edition, `acceleratedLifeRegenPercent
  = 25.0`, measured ceiling 26.4% maxHP/s) — **free by harness construction**.
- **~48% in-fight (~2,712)**, split: **ADCTH leech ~1,200 · Battle Surge point ~1,500**
  (ceiling 2,883 — bounded by the clamp, not the 66 crits: 69.1% of in-combat frames sit at
  FULL health).
- **Passive regen = 1.10 HP/s total** (base 1.0 × one +10% helm affix — the ONLY regen source
  in twelve slots; **Menhir's Wall and Soulwarding grant NO regen** — genre memory would have
  been wrong; C-8-class correction to §14.15's candidate framing). O-b at 1.10 HP/s moves no
  outcome (~66 HP/min) → **dropped as not load-bearing**. UNRESOLVED flag carried honestly:
  the measured in-fight floor 1.61 HP/s exceeds computed 1.10.
- **The kit HAS LIFE LEECH:** *Vampiric* ring, `offensiveLifeLeechMin = 5.0` (jitter band
  3.25–6.75% ADCTH) over 1,606 hits — capacity exceeds the run's entire realised healing.
- **lastHitBy contradiction DISSOLVED:** `lastHit`/`lastHitBy` are the last target's **DA /
  last attacker's OA**, not damage (Plague Walker ledger OA 274 vs 273.704 — two M-grade
  opposition values validating G-5a derivations to <0.5%). And **`greatestDamageReceived =
  260.50` is confirmed post-mitigation**: across boss + 3 heroes + 7 champions, no single
  event exceeded it; both deaths were compounding (death-2 `drop_max` 541 over 3 s), not
  one-shots — a ceiling the held §14.10 boss damage regime must respect.

**Conductor reconnaissance (evidence-only, this session):** the kernel ALREADY RESOLVES
lifesteal — `damage_resolver.py:1253-1263`: secondary effect, `stolen = min(total_damage ×
pct, max_hp − hp)`, attacker-healed, `on_lifesteal` evented. The spatial adapter **discards it
by documented design** — `spatial_resolver_adapter.py:342-344`: side effects "mutate the
attacker scratch state and are … not carried back (parity with the simplified model's
information content; math note § 6)". The gap is ONE carry-back seam, not a missing mechanism.

**R-KC1-17 proposal REVISED (held for Matt):**
1. **O-d — leech carry-back behind the BQ-3 door** (supersedes O-a/O-b/O-c): gamora build,
   Gate-2, carrying the kernel's already-correct lifesteal heal back to the spatial attacker
   entity, active ONLY through `_calibration_overrides`, pinned at the Vampiric ring's rolled
   percent (U-1 all-rolled-stats per Matt's amendment). Discipline-#12 surface named: math
   note §6's parity decision is being deliberately relaxed inside the door.
2. Battle Surge stays **named-absent (BQ-4)**, quantified: ~1,500 of run-wide healing the sim
   werewolf goes without, concentrated where crits concentrate.
3. Passive regen 1.10 HP/s: declared negligible, no build. 4. Constitution: free by
   construction. 5. Trash tier sustain-free + insensitivity assertion. 6. The 1.61-vs-1.10
   floor UNRESOLVED flag rides to G-8/char-sheet confirmation, non-blocking.

### 14.17 — G-8 lands (galadriel `1e9d41f3`): the client rendered monster HP numerals — the composition rule PINS without another save; the orb "collision" resolves AGAINST the charter

**The headline: §14.11's closure path is CLOSED, from inside the corpus we already held.** The
client renders monster health as numerals; galadriel found **ten readouts across seven
frames**. Frame 281 itself carries Primordian at **13,571 / 14,812**:
- **14,812 max pins the net life modifier at −36.000% ± 0.004 pp** — measured independently,
  landing EXACTLY on the value §14.11 said integrality demanded (−36.00%). The composition
  rule is no longer inferred from one over-determined triple; it is read off the screen.
- The 15,822-vs-14,812 residual = **1,010 ≈ bio mana 1,009.74** — confirming the
  `LifeAndMana` split as a byproduct.
- **Second tier measured:** champion Thundersnout ~ Thundering, L10, **max 4,702** (Δ0.28 pp
  vs bar). **Six trash maxima:** 58, 326×2, 434, 649, 813, 1,820. Three tiers of the HP table
  now carry client-measured anchors. (The other-saves ask to Matt drops from *required* to
  *redundancy-nice-to-have*.)

**The orb collision (§14.13 flag) dissolves — and the charter was the wrong party.** Death 2
reads **HP 0/747, mana 239/349**; `play_time` 5453 sits in **R2** (ratified 1134–6052), and
747 is the banked ladder level for (4987, 5648]. §14.13's "inside R3, where max is 1600" was a
conductor regime-assignment error, now corrected: the 759→1600 gear step lands AFTER death 2.
Galadriel reproduced the whole orb ladder still-side: 250→366→451→672→707→**747**→759→1600→
**1607** — terminal max is **1607, not 1600** (small G-6 §7.1 correction; kit-spec N-band
endpoints re-check at harness compile).

**Two provisional conductor reads corrected (C-9):** Onslaught was used **54** times (not ~5 —
it was a live rotation piece, consistent with its INERT-stat-but-cast status); and **"Damage
per second" is a rolling ~5 s meter, NOT lifetime** (14.0 … 743.22 … 1492.47 across frames —
743.22 is the death-window value; G-5 must window any comparison, never treat it as a run
average). Skills-Used counts all M-OCR ≥0.957: kick 13 · weapon 74 · onslaught 54 · transform
7 · claws 243 · charge 125. Death-window rate (f280→f281, 81 s): +59 kills, +19 claws, +9
charge, 0 everything else — **a pure claws:charge 2.11:1 window** (harness driver's boss-tier
mix, measured at the actual death). Primordian's nameplate level **13** over-determined
against save + `lv6_hero` remap — the §14.15 charLevel ambiguity collapses.

**Lane fired:** legolas — fold the ten HP readouts + −36.000% modifier into a corrected
opposition-ledger HP table (trash/champion/boss re-graded, §14.11's ×0.837/×0.810 replaced by
the measured rule), and grade the six trash maxima against the G-5a pool predictions.

### 14.18 — R-KC1-17 RATIFIED (O-d) · Q-KC1-1 RATIFIED · Matt's compensation question → proposed R-KC1-18 (A/B arms); O-d build fired

**R-KC1-17 — RATIFIED (Matt: "Ratify O-d").** Leech carry-back behind the BQ-3 door, pinned
per-scenario as a door VALUE. Build fired to gamora same turn: extends the door with a new
namespaced field under the full six-layer containment; the Discipline-#12 surface (math note
§6's parity decision, relaxed inside the door only) named in the commission; the clamp must be
applied against the SPATIAL entity's live hp/max (the kernel's own clamp computes against
scratch max_hp=1.0 in this path — a wrong-state trap the commission calls out). Target tag
`gamora/v-od-leech-carryback-1`; Gate-2 consolidated with BQ-3 as one door review.

**Q-KC1-1 — RATIFIED as recommended.** The defensive-mechanics wave (max-HP derivation,
armor/mitigation, on_crit self-heal + HoT spatial bridge [BQ-4], PERMANENT leech carry-back
replacing the door version, target-cap rank-scaling [BQ-1], per-skill cone [BQ-2]) is the
NEXT wave, spec-frozen against the kit spec + G-5 output as acceptance fixture, knight-rider
sequenced. Hand-off note to KR owed at run wind-down. Measured targets already banked for the
wave: leech ~1,200 / Battle Surge ~1,500 / regen 1.10 HP/s / "Life healed" 5,649-clamped.

**Matt's question (verbatim): "would it make sense to increase life steal by roughly half of
the in-battle-heal amount that the missing battle-surge procs would have healed for?"**
Conductor answer: not folded into the canonical kit — the kit spec's build identity is
MEASURED and a synthetic uplift would smear calibration attribution (survival no longer
traceable to measured kit vs compensation). Instead, **proposed R-KC1-18: run boss-tier as an
A/B pair through the same door, zero code delta** —
- **Arm A:** leech at the ring's measured rolled percent. Canonical candidate; Battle Surge
  absent-and-named.
- **Arm B (Matt's proposal):** leech uplifted by half the Battle-Surge point estimate
  (~750 HP over the run's hit budget ≈ ring roll × ~1.6).
- **Decision rule, pre-registered:** outcome FLIPS between arms → Battle Surge is load-bearing
  → BQ-4 promoted in the Q-KC1-1 wave with evidence. No flip → the absence is PROVEN
  non-load-bearing → Arm A canonical. Either way Matt's compensation instinct becomes an
  instrument instead of a contaminant (same key as P-8: pre-registered arms beat post-hoc
  fudges). Distortion honestly stated: uplifted leech smooths Battle Surge's lumpy transfer
  function (3 s proc bursts → continuous drip) — second-order for a calibration lap, unlike
  the rejected EHP fold-in's outcome-flip ordering error.

**R-KC1-18 — RATIFIED (Matt: "agreed on A/B pair").** Boss-tier G-5 runs both arms through the
door; the flip rule above is the pre-registered gate. The ruling ledger for this run is now
**closed on the sustain question end-to-end**: C-7 challenge → decomposition → O-d ratified →
A/B arms ratified, every step measured. **In flight:** O-d build (gamora), HP re-grade
(legolas). **Unchanged:** Gate-2 with jack-ryan (BQ-3 + O-d consolidated). **G-5 preconditions
remaining:** Gate-2 · O-d lands · re-graded HP table · harness assembly.

### 14.19 — HP re-grade lands (legolas `73e986b1`): §14.11's provisional factors WITHDRAWN both ways — trash/champion stand verbatim, boss takes one −15 pp rule, heroes carry a measured anomaly

- **Trash + champion: NO correction.** Frame 287's four numerals reproduce EXACTLY under the
  unmodified G-5a chain at charLevel 11 (Eastmire Warrior 813.28→813, Deepmire Vanguard
  649.75→649, Eastmire Herder 326.39→326 ×2 — creature, level and HP landing together off one
  nameplate). The provisional ×0.837 is **falsified**; those tables stand as first derived.
- **Boss/quest: additive −15.000 pp on the life-modifier pool**, not a ratio:
  23,145.108 × (1 + (−71+35)/100) = 14,812.869 → the measured 14,812. §14.11's two
  provisional factors (×0.837 / ×0.810) were **one rule wearing two hats** (−15 pp restated
  per-tier). The `armorbase03–06` clamp gate is KILLED (Eastmire Warrior, Champion at −71,
  validates at +50); surviving gates are classification-based. Additive-15pp vs
  multiplicative-×0.81013 separate by 1.4% at charLevel ≥20 — the named discriminator for any
  future higher-level fixture. **The §14.10 clamp-hardening asks (armorbase source pass /
  60 s level-1–2 capture) are RETIRED — closed from inside the existing corpus.**
- **Necklace residual EXACTLY zero** — monster equipped-gear life is not applied to HP; the
  proto note's stochastic-contamination warning retires. **Nameplate = charLevel** proven on
  two remappers → Primordian closes at 13; the cl-17 and cl-11+gear candidates are dead.
- **Warden Krieg re-graded: 21,189 / 28,514** (49,703 combined; §14.11's rough 49,706 was
  1.00006 off — the direction of honest error).
- **Two flags, not smoothed:** Thundersnout is a **Hero** (`hero/boar_h07`, GDX3 — "~ Affix"
  is archetype, not tier), and its measured 4,702 is **unreachable by ANY record × charLevel ×
  operator in the corpus** (exhaustive negative, 8 hypotheses) — 2.49× ABOVE model, the
  opposite direction from every prior correction. 434 and 1,820 fail the same frame-176
  window. **Ruling (conductor, reasoning-boundary): heroes are NOT re-graded downward; the
  mixed-pack scenario uses the MEASURED 4,702 for its hero slot** (instrument-canonical grain:
  measured beats derived where derivation fails), and the unmodeled hero-HP source is a named
  finding for the Q-KC1-1 wave's ledger — likely GDX3 hero scaling the chain doesn't model.
- **Damage rows stay HELD** — with teeth now: 260.50 post-mitigation **falsifies any clamp
  flooring boss-tier TDM at or above ≈−42%**.

**Harness-ready state:** all three scenario tiers now carry client-anchored HP (trash verbatim
/ champion verbatim / Primordian 14,812 + trio protos pending / hero slot at measured 4,702).
Remaining before G-5: O-d lands · Gate-2 · harness assembly.

---

## §14.20 — O-d LANDS: there was nothing to carry back · a production-wide dormant-lifesteal finding · R-KC1-18 semantics corrected · the replay-trace rider accepted (R-KC1-19)

**Banked 2026-07-28, post-compaction turn (charter-freshness gate executed from disk before
processing). Engine pushed `c067bbd..67d165b` + tag `gamora/v-od-leech-carryback-1`; meta pushed
`1a6ee7ae..00e720ca`.**

### The build — operator REPRODUCED, not carried (C-8-class correction, stated not smuggled)

Gamora's diagnosis inverted the ratified framing: **kernel lifesteal has never fired in a spatial
fight.** The kernel's `stolen = min(dmg × pct, max_hp − hp)` clamps against the projection
attacker's *scratch* `max_hp = 1.0` (`spatial_resolver_adapter.py:233`), so the operand is ≤ 0 in
every reachable state — three resync regimes probed, heal 0.000 in all three, `on_lifesteal`
never emitted. Counterfactual with the real pool: 254.585. **The operator is right; the clamp's
operand is wrong.** So O-d is the kernel operator *reproduced* at
`spatial_engine._apply_skill_damage` (adapter untouched; `resolve_spatial_hit` signature +
return shape literally unchanged; its parity docstring amended, not left to mislead) — behind
the BQ-3 door, leech percent as per-scenario door VALUE per R-KC1-17. Gamora stated this as a
C-8-class correction in math note §0 rather than quietly shipping something other than what was
ratified. The commission's pre-flag of the scratch-max_hp trap is what enabled the diagnosis.

- **Clamp placement:** against the SPATIAL entity, re-evaluated per hit inside the target loop
  (AOE headroom can't go stale). Sentinel test `OD-6d` fails if it had stayed put.
- **Named deviation:** heal base is `delivered` damage, not the raw roll — crediting healing for
  damage never dealt inflates hardest where the fixture has the most samples (trash, 1,606 hits).

### Dormant production lifesteal — the finding nobody ordered

The "obvious repair" (fixing scratch `max_hp`) was REFUSED: it would wake execute,
freeze-shatter, and the heal cap simultaneously, and would make production kits' existing
`lifesteal` effects **start healing in every season** — a balance change in a bug-fix costume.
Pinned dormant by test `OD-10`. **The wake-up is owed to the Q-KC1-1 defensive-mechanics wave**
(joins BQ-1 / BQ-2 / BQ-4 / permanent leech / hero-scaling on that wave's ledger). Every spatial
season ever run has had lifesteal silently dead; whatever balance was tuned, was tuned around it.

### R-KC1-18 semantics CORRECTED — arms are DISTRIBUTIONAL, not paired

Gamora's suite falsified her own §2.3 claim: the A/B arms do **not** share per-seed RNG streams.
The flip-rule comparison is **distribution-vs-distribution**, not per-seed paired deltas. The
pre-registered flip rule survives unchanged in intent — "outcome flips" is evaluated on the
arms' outcome distributions — but any per-seed delta table would have been an instrument error.
Recorded in MIGRATION §7. Baseline honesty: the regression baseline ran in a `git worktree`
whose pass counts are not comparable to main-tree counts; it supports **"zero new failure
names"** and nothing more — which is exactly what was claimed.

**Evidence bundle:** 33 new tests; 72/72 across both door suites; pre-registered digest
`25c212eb…` UNCHANGED; KF-4 smoke 36 GREEN / 0 RED; digest exclusion growth made structural by
`OD-1c`. Consolidated Gate-2 (BQ-3 + O-d, one door review) queued at
`agentic_orchestration/qa/pending/2026-07-28-gamora-bq3-calibration-override-door.md`.

### Out-of-seam flag — routed, not committed

A test run rewrote `src/reincarnated/output/leg3_pilot_section8a1_band_measurement.json`
(star-lord's seam). Gamora left it UNCOMMITTED, deliberately. **Routed to star-lord via KR at
wind-down: inspect, then restore or adopt — the conductor does not commit into another's seam.**

### R-KC1-19 — the G-5 replay-trace rider: ACCEPTED (conductor ruling, reasoning-boundary)

The unexplained meta commit `00e720ca` resolved: a **rider request from the TCP
suite-architecture session** (gandalf, same date), delivered by Matt — the only legitimate
channel into a running conduction — at
`agentic_orchestration/gandalf/notes/2026-07-28-g5-replay-trace-rider-request.md`. Ask: before
harness assembly freezes, the harness writes a **replay-grade trace** per scenario run
(non-gating side artifact; header / per-tick entity state / timestamped events; raw series
only), so the TCP program's Godot REPLAY capstone can render the werewolf battle without
re-running G-5.

**RULING: ACCEPTED, riding harness assembly.** Rationale: (1) it arrives at exactly the phase
boundary it names — harness assembly has NOT fired, so this is one commission line, not a
retrofit; (2) non-gating is verifiable — no exit predicate, band, or verdict dependency changes;
(3) the pre-registered §4 fallback (post-verdict re-run of only the canonical arm, same seeds)
makes a mid-assembly drop bounded and honorable; (4) the alternative — re-running a chartered
calibration finale for presentation reasons — is exactly the epistemically-ugly path the rider
itself names. **One premise correction, material to the writer:** the rider assumes "the O-d
door already receives the kernel's `on_lifesteal` event." Per this section, that event has NEVER
been emitted in spatial — O-d *reproduces* the operator at the spatial seam. The trace's
leech-heal events therefore come from **the door's own heal application site** in
`spatial_engine._apply_skill_damage`, not from a kernel event stream. Format within the rider's
§3 constraints is gamora's call; if she prefers star-lord's export seam to own the writer, that
is her recommendation to make at assembly. **If the rider threatens G-5 timing, the §4 fallback
fires without further ruling — pre-authorized here.**

**Board after this section:** Gate-2 (jack-ryan, consolidated) → harness assembly (gamora, now
carrying the trace writer + the terminal-max 1607 re-check) → G-5 fires both arms (A measured
ring roll / B roll ×1.6), trash + champion sustain-free with insensitivity assertion, scenario
HP per §14.19.

---

## §14.21 — R-KC1-20 + R-KC1-21 RATIFIED: the scratch-max_hp fix pulls forward, pre-G-5 — and Matt's argument beat the conductor's

**Banked 2026-07-28. Gamora commissioned (background, seam write-work, tag target
`gamora/v-scratch-maxhp-wake-1`); harness assembly queues directly behind her.**

**The reversal, honestly recorded.** §14.20 held the dormancy line ("balance change in a
bug-fix costume; wake-up owed to the Q-KC1-1 wave"). Matt challenged it twice and won on the
second pass: *"we don't have a validated RDR battle sim… we are LITERALLY making the first
validated emitted kit/monster production."* The conductor's D3-1.0.3 comparability argument
FAILS here — Diablo had a live economy load-bearing on its bug; we have zero shipped seasons
and zero players. Every telemetry baseline the dormancy protected is pre-validation output of
an engine with a dead mechanic. And the deeper point is the substrate discipline itself:
**validating a state you already know is wrong is backwards** — if G-5 stamps engine-state N
and the wave immediately produces N+1, the verdict attaches to a corpse. The verdict must
attach to the state we keep. Conductor lean withdrawn; Matt's ruling governs.

- **R-KC1-20 (RATIFIED):** fix `spatial_resolver_adapter.py:233` scratch `max_hp = 1.0` → real
  attacker pool, PRE-G-5, under a **blast-radius battery** (before/after distributional: KF-4 +
  season-telemetry smoke; every awakened mechanic's delta enumerated — execute, freeze-shatter,
  heal cap, production lifesteal; anomalies are findings, not silent patches). Plus a
  **no-stack assertion**: the O-d door (leech as per-scenario VALUE, R-KC1-17) and the awakened
  kernel path must contribute zero double-healing for the fixture kit — tested, not assumed.
  OD-10 flips semantics (pins-dormant → pins-awake-with-measured-deltas); digest re-registered
  as a RULED change, not a smuggled one.
- **R-KC1-21 (RATIFIED, class umbrella per Matt's "if so, I ratify the others"):** the clamp is
  one member of a family — *kernel operators the spatial seam silently kills via scratch-clamp
  or sync-omission*. Census bounded to the mapped sites (adapter scratch construction, the
  math-note §6 discard list, sync sites ~`:5163/:5186`). Named additional candidate: the **HoT
  bridge** (HoTs land on scratch and evaporate — if sync-list-omission class, it fixes now).
  **Class line, one sentence: known-wrong operands get fixed before validation; not-yet-built
  mechanics get built in their wave.** Explicitly HELD in the Q-KC1-1 wave regardless: BQ-4
  Battle Surge, BQ-1, BQ-2, regen HP-tick (build-class by ruling; measured 1.10 HP/s is
  undetectable by G-5 — magnitude, not caution, keeps it out).
- **A/B arms SURVIVE the fix** (Matt probed this): the arms test the quantified-absent Battle
  Surge proc (~1,500 HP in-fight), which no operand fix resurrects. R-KC1-18 stands, in its
  §14.20 distributional form.

**Board:** gamora fix+census+battery → consolidated Gate-2 (now THREE items, one review:
BQ-3 + O-d + wake) → harness assembly (trace writer per R-KC1-19; terminal-max 1607 re-check)
→ G-5 both arms on the POST-FIX engine.

---

## §14.22 — THE WAKE LANDS: five operands fixed, zero outcomes moved — the census draws the fix/build line at 19 members, and two conductor framings take corrections

**Banked 2026-07-28. Engine pushed `67d165b..9218238` + tag `gamora/v-scratch-maxhp-wake-1`;
meta pushed `94d2704c..0c645ee0` (ride-along: two parallel-session gandalf commits —
PROVISION-CAL §5/§6 rulings and the canon supersession — pushed under the cycle pattern, owned
by their sessions). Findings note:
`agentic_orchestration/gamora/notes/2026-07-28-kitcal1-scratch-maxhp-wake.md`; math note
`src/reincarnated/simulation/math/scratch-maxhp-wake-2026-07-28.md`.**

### Census verdict (R-KC1-21) — 19 members

**FIXED (operand class, 5):** S1 kernel lifesteal clamp (0→42 fires) · S2 heal cap (same
operand) · S3 HoT tick cap (0→51 heals) · S4 freeze-shatter (fixed, still 0 — **corpus-dormant,
not structurally dormant**: nothing in generation emits `freeze`, 0/4,772 class + 0/2,332 mob)
· S5 execute threshold (fixed, still 0 — shim lacks the field AND 0/5,021 corpus).
**BUILD-class findings for the Q-KC1-1 wave (F-1..F-7):** spatial-vs-kernel max_hp divergence
with gear (F-1); **HoT healing (F-2) — the named candidate RULED BUILD**, and the reason is
solid: `tick_effects` returns one scalar and the only zero-signature carrier `heals_received`
conflates lifesteal/heal/HoT, so a delta-read would double-count against the O-d door; direct
heal (F-3); kernel-lifesteal out-carry (F-4 — would stack with the door); thorns (F-5);
offense-site events (F-6); attacker scratch hp not re-synced at offense site (F-7 — the one
HALT: in-sync without out-carry is more truthful but still discarded).
**Docstring debt repaid:** Y6–Y9 (shield/buffs/silence/kill-element) were NEVER dropped — the
§6 discard list was over-broad and is corrected.

### Battery — all quiet, and the quiet is EXPLAINED, not lucky

Before/after on both arms (PROD season path + PROJ), 6 fights: **all three digests UNCHANGED**
(`25c212eb…` did not move), `mean_mobs_killed` 3.5→3.5, anomalies NONE. Awakened on PROJ:
`on_lifesteal` 0→42, HoT scratch heals 0→51 (max 432 HP), nonzero scratch heals 0→84 — and
every one **evaporates** (no carrier reaches spatial HP or an emitted field; the carriers ARE
the wave's F-findings). **Gamora declined the commissioned digest re-registration** because the
digest didn't move — a note claiming a golden-master reset that never happened is worse than
none. Right call; the commission's prediction was wrong, hers governs.

### No-stack (R-KC1-20's assertion) — three-legged, not vacuous

NS-1 compiled pilot kits carry no skill-borne lifesteal (SKIP-guarded, non-vacuous) · NS-2 door
`healed` equals its formula even with a kernel-lifesteal skill firing · NS-3 spatial HP gain ==
door `healed` exactly. Tests 76/76 door suites (+OD-6d2, NS-1/2/3); OD-10 and OD-6d rewritten
with inverted semantics (OD-6d now perturbs the scratch across three regimes — proof-by-
magnitude had stopped discriminating); KF-4 36 GREEN / 0 RED, four pilot fights numerically
identical; regression 1,587 vs 1,585 same-tree stash baseline, 55 failure names diff-empty.

### Two corrections to the conductor's §14.20/§14.21 framing (C-10, C-11)

- **C-10:** "make production kits' lifesteal start healing in every season" was structurally
  impossible either way — **season generation never takes the projection path.** No season
  could move; the safety was reachability, not restraint. Both the original dormancy caution
  AND the ratified wake's season-risk framing overstated the blast radius.
- **C-11:** "kernel lifesteal never fired in spatial" (§14.20) needs sharpening: the
  **production-path** kernel lifesteal was never dormant — it fires (55× in battery) and its
  heal is **thrown away** for want of an out-carry (F-4). The projection-path clamp death and
  the production-path discard are two different deaths; §14.20 named only the first.

### What G-5's harness now assumes (gamora's flags, adopted)

1. **The fixture's max_hp override reaches the kernel state too — one body, not two.** Before
   the fix, the kernel saw a 1-HP attacker while the entity saw 1,600. This is the wake's one
   material G-5 improvement, and it is exactly the fixture-truthfulness Matt's ruling bought.
2. **The O-d door remains the ONLY leech reaching spatial HP** (NS-3 proves it).
3. **Freeze-shatter and execute are corpus-dormant, not structurally dormant** — the day
   generation emits `freeze`, player-side shatter goes live at 20% max-HP per proc. Named
   hazard for any future kit that compiles freeze effects.

**Board:** consolidated Gate-2 (THREE items, one review: BQ-3 + O-d + wake) → harness assembly
(trace writer per R-KC1-19; terminal-max 1607 re-check; the three assumptions above) → G-5
both arms. `leg3_pilot_section8a1_band_measurement.json` still flagged, still uncommitted,
still star-lord's.

### R-KC1-19a — trace-writer amendment (Matt query 2026-07-28: "will this run also ship the AI state?")

**Ruling:** the replay trace ships **no live AI** — in the REPLAY capstone Godot renders, it
does not think; the sim is the mind, the trace carries every AI decision's *outcomes* (per-tick
kinematics + timestamped events). But the rider's own "facing if the spatial layer holds it"
rule extends by the same logic: **per-tick current-target id and any behavior/intent fields the
spatial layer ACTUALLY HOLDS ship raw; nothing is fabricated.** A synthetic behavior enum the
engine doesn't have would be derived data wearing a raw costume — the consumer computes those
honestly (idle/engaged from engagement boundaries; anim states from kinematics + events). The
explicit target id matters most for the charge path (the L6∩L7 trail case — "who is that
monster charging at" should not require detective work on movement vectors). **Delivery path:**
no mid-flight channel into the running assembly exists this session; the amendment applies at
the harness landing — trace schema inspected, missing raw-if-held fields added in a small
follow-up BEFORE G-5 fires (zero timing cost: G-5 already gates on Gate-2 + conductor go).

---

## §14.23 — GATE-2 LANDS: NO BLOCK, G-5 CLEARED — with two harness flags that bite, five doc conditions, and every judgment call upheld

**Banked 2026-07-28. Verdict:
`agentic_orchestration/qa/findings/2026-07-28-gate2-gamora-bq3-od-scratch-maxhp-wake.md`
(jack-ryan `93db6a8a`, pushed `2a531b33..58f7bed9` — ride-alongs: legolas PC-W1-B Q46 null-diff
+ gandalf PROVISION-CAL §8, owned by their sessions/lanes).**

**Verdicts:** BQ-3 **PASS** · O-d **PASS** (1 doc condition) · wake **CONDITIONAL PASS** (4 doc
+ 2 harness conditions). **No BLOCK.** Verified-not-accepted highlights: 76/76 with **zero
skips** (NS-1 executed — cannot have passed vacuously); digest `25c212eb…` holds; battery
digests byte-identical while PROJ counters moved in the same run; the two-path premise (C-10)
confirmed in code at `spatial_engine.py:5813-5828`; Y6/Y8 spot-checks hold; the wake regression
**reproduces exactly** (34F/1,587P/21E). Every contested judgment upheld: the census `defense`
overrule (correct — the key would open the door prematurely), reproduce-not-carry (gamora's to
make, and right), the declined digest re-registration (upheld with the sharpest phrasing of the
day: *"a reset note for a reset that didn't happen is a false evidentiary artifact"*). Two
offered/invited BLOCKs — same-day dormancy reversal, HoT/F-2 — both declined on the merits.

**Harness flags (ADOPTED as landing checks — no channel into the running assembly, so both
apply the moment gamora reports, before G-5 fires):**

- **H-1 (bites the boss scenario):** freeze-shatter's dormancy is **corpus**-scoped, and G-5's
  hand-authored GD mob dicts are OUTSIDE the corpus. `_resolver_skill_from_dict` copies effects
  verbatim; `freeze` is a live ailment; post-wake, one freeze expiry below 25% HP costs **320
  HP against the fixture's 1,600 pool**. And the Primordian's kit is ~85% cold with a
  16-projectile freeze nova — this flag aims straight at our boss dict. **Conductor lean
  (fidelity law):** GD freeze is CC — it has NO shatter-on-expiry burst; RDR's shatter is an
  RDR mechanic. The boss dict must NOT carry RDR `freeze` (assert it); the nova compiles as
  cold damage, and the un-modeled freeze-CC joins the named-gap ledger ADJACENT to the evasion
  finding (§ pending Matt's R-KC1-22 ruling) — both are "the nova's danger was more than its
  damage" gaps, on the same side of the ledger.
- **H-2:** the L5 AST sweep root is `src/reincarnated/` only — a harness placed outside keeps
  T-8 green while hollowing BQ-3's deletion inventory. Landing check: harness path must sit
  inside the sweep root.

**Doc conditions C-1..C-5 (no re-tag):** owed by gamora in the same follow-up that closes the
harness landing checks — notably C-5 (stale comment at `spatial_engine.py:2570-2596` asserting
kernel dormancy at the exact site no-stack must hold) and C-3 (42-not-45, including a
production docstring). `leg3_pilot…json`: confirmed no landed test depends on it; residual
risk named (tracked-dirty file in a shared tree) — still star-lord's.

**Gate state:** G-5 is cleared by Gate-2. Remaining before fire: harness lands → landing checks
(H-1 freeze assert · H-2 path · R-KC1-19a trace fields · C-1..C-5 docs · terminal-1607) →
Matt's evasion-anchor ruling (proposed R-KC1-22: boss-tier interpretation anchors to the
death-2 no-evasion trajectory; dodge-on-tell logged as build-class inexpressible) → conductor
go.

---

## §14.24 — R-KC1-22 RATIFIED: the boss verdict anchors to death 2 — and Matt discloses the observer effect that makes the anchor MORE honest

**Banked 2026-07-28. Matt (verbatim core): "We can ratify (a) as R-KC1-22, but I should also
note that the first time I died [to the Primordian], I was standing still for a couple of
seconds soaking up damage while I attempted to take a screenshot. Still worth the A/B."**

- **R-KC1-22 (RATIFIED, option a):** boss-tier G-5 interpretation anchors to the **death-2
  no-evasion trajectory**, not the win. The win required **sustain AND evasion**; dodge-on-tell
  is a build-class inexpressible (no tell modeling, no dodge policy — new AI architecture, not
  an operand) and joins the Q-KC1-1 wave ledger beside BQ-4 and the H-1-adjacent freeze-CC gap.
  The A/B flip rule is UNTOUCHED: it compares Arm A vs Arm B *within the sim's no-evasion
  behavior space* — Matt explicitly reaffirmed the arms' worth. **Matt's winning attempt is
  banked as the future acceptance fixture for the evasion mechanic** — the measured proof that
  dodge-on-tell converts this exact loss into a win.
- **Disclosed observer-effect artifact (fixture caveat, ledgered not smoothed):** during the
  first Primordian attempt (death 2), Matt stood still ~2 s soaking damage while taking the
  screenshot. **Grading implication runs in the anchor's FAVOR:** standing still under fire is
  the sim player's native behavior for the whole fight — the contamination pushes the human
  sample TOWARD the sim's behavior space. Honest treatment regardless: the anchor is a
  **trajectory BAND, not a punctual match**, and tolerance on the screenshot window widens for
  the disclosed pause. The sample is more sim-like AND less clean; both facts recorded.
- **Design-DNA note carried with the ruling:** "slow, readable tells" is the telegraph contract
  (dangerous = visible = dodgeable) — the Primordian fight was winnable through skill, not
  stat-checking. The replay trace already carries monster skill-activation events, so tell
  windows render in Godot for free when the REPLAY capstone consumes it.

---

## §14.25 — HARNESS LANDS, CHECKS PASS, **G-5 FIRES** — and the smoke catches a contract with no writer (REPLICA-1's gap)

**Banked 2026-07-28. Engine pushed `9218238..bef1f55` + tag `gamora/v-g5-harness-1`; meta
pushed `996b6c54..d1f5a033` (ride-alongs: PROVISION-CAL §8 + drax PC-T12, owned by their
lanes). Assembly notes: `src/reincarnated/simulation/math/g5-harness-assembly-2026-07-28.md` +
`agentic_orchestration/gamora/notes/2026-07-28-kitcal1-g5-harness-assembly.md`. Harness:
`spatial_gauntlet/kitcal_g5_{scenarios,trace,harness}.py`.**

**Landing checklist (Matt's go pre-authorized on pass — ALL PASS):**
- **H-1 ✓** `A-FRZ-1`: no `freeze` on kit or any mob — the shatter hazard cannot reach the
  boss fight. **H-2 ✓** harness inside the AST sweep root. **Terminal-1607 ✓ — both halves:**
  W-c *is* R2b, so the canonical pool is **759**; 1607 belongs to the R3 arm alone. A harness
  that merely "corrected 1600→1607" would have been precisely wrong; gamora caught the
  conductor's half-framed re-check. **R-KC1-19a ✓ satisfied by the BASE schema** — conductor
  verification found `replica-frame/v1` already ships per-frame `heading_rad`, a `decision`
  event streaming `(tick, chosen_target_id, intent)` (the aim-line), and `telegraph` events
  with damage amounts — the §14.24 tell-rendering channel EXISTS. Raw-if-held was already the
  schema's law; nothing added. **C-1..C-5** doc-only, don't gate execution (Gate-2 cleared the
  fire); owed in the wind-down follow-up.
- **Pin enforcement (assembly note §10 map):** trash/champion HP verbatim (champion = the
  frame-287 roster — the one tier whose whole opposition HP vector is measured); Primordian
  14,812 **+ the trio built** (protos were available, cold identity all three, nothing
  invented); hero slot MEASURED 4,702 with `A-HP-3` failing on any re-derivation; arms
  boss-only (`A-ARM-1`), leech as door VALUE never compiled (`A-ARM-2`), distributional with
  **no paired-delta surface existing** (`A-ARM-3`); one-body (`A-HP-2`); trash/champion
  sustain-free with `INS-1` non-vacuous (86.9/91.1 HP of heal ignored, fights bit-identical).
- **Dry-run smoke PASS:** 8/8 static pins, 4 tiers, both arms, 5 traces. 18/18 new tests;
  76/76 door suites (digest unmoved); KF-4 36 GREEN; regression +18 = exactly the new tests,
  failure names diff-empty.

**THE SMOKE FINDING — a documented contract with no writer (REPLICA-1's gap, not this run's):**
intake read 0.00% on every tier while boss arms healed 721 HP — impossible, since leech only
fills headroom. `ReplicaFrameSink.on_hit` has carried documented received-side semantics since
KF-5 and **the mob→player branch never called it**. Consequences, named: every replica trace
ever emitted shows a player taking no damage; G-5's N-7..N-11 and the **entire S-3
hazard-shape signature** would have read identically zero — *a comparison reported but never
run*, the same class jack-ryan BLOCKed in Wave 0. Repaired + tested in assembly; filed in
MIGRATION as REPLICA-1's gap. **Downstream routing: drax's Godot lane is the other consumer of
replica frames — the repair reaches him via the wind-down hand-off.** The instrument-first
discipline paid for itself an hour before the finale: G-5 without this repair would have
produced a defensive verdict on a channel that was silently all-zeros.

**HALTs carried into interpretation (right calls, all three):** boss damage rows HELD — swept
at 33/50/67 with the 260.50 post-mitigation ceiling as falsification gate; `primordian_
frigidring` **named-absent** (biases the sim boss LESS bursty — named as bias per C-7's law,
not smoothed); crit is out of the trace (P-6's un-glued seam — BQ-4 territory). Star-lord's
`leg3_pilot…json` was rewritten AGAIN despite test deselection — still uncommitted, still
routed; the rewrite trigger is now itself a named item for the wind-down.

**FIRE RECORD:** all checks green + Matt's pre-authorized go →
`python3 -m reincarnated.simulation.spatial_gauntlet.kitcal_g5_harness --run --seeds 30`
launched in background, 2026-07-28. Both arms, four tiers, 30 seeds. The run's verdict
processes under R-KC1-18 (distributional flip rule) + R-KC1-22 (death-2 band anchor) + the
sweep/named-absent qualifications above.

---

## §14.26 — G-5 EXECUTES CLEAN: NO FLIP → **ARM A CANONICAL** — and the boss fight's whole drama turns out to live in the two inexpressibles

**Banked 2026-07-28. Exit 0; 150 fights (30 seeds × [trash + champion + mixed_pack + boss×2]);
engine hash `bef1f55`; report
`src/reincarnated/simulation/output/kitcal_g5/g5/kitcal_g5_g5_report.json`; 150 replay traces
(`g5-replay-trace/v1`) alongside. All 8 static assertions passed in-run, incl. A-HP-1 pool
{759, 1607} with "1600 superseded" recorded in the assertion string itself.**

**Results:** player wins **30/30 on every tier and both arms.** Trash 4.2–4.3 s / champion
4.4–4.5 s / mixed pack 10.1–11.5 s, all sustain-free (leech 0, INS-probe confirms ~87 HP of
would-be healing ignored with bit-identical fights). Boss: 27.3–30.3 s, intake **156.3% of the
759 pool**, worst single drop **7.8%**, leech healed 698–748 (Arm A @ 5%) vs 979–1043 (Arm B @
8%).

**R-KC1-18 RESOLVES — NO FLIP → ARM A CANONICAL** (pre-registered rule applies itself): both
arms 30/30, indistinguishable elapsed/intake distributions; Arm B's extra ~290 HP absorbed by
capacity clamping without touching any outcome. **Within the sim's behavior space, the missing
Battle Surge proc is NOT load-bearing.** Named deviation, visible in the report and named
here: `arm_a_jitter=false` (flat 5.0%, not the 3.25–6.75% measured jitter) — immaterial to
the flip verdict since 5% vs 8% produced zero outcome difference, but it is a deviation from
R-KC1-18's arm spec as written, recorded not smoothed.

**R-KC1-22 anchor reading (DRIFT-CRITIC):** the sim does NOT reproduce the death-2 trajectory
— it wins where the no-evasion human died. **Processed as the named-absent ledger's predicted
consequence, not as calibration failure and not smoothed into one:** the sim boss deals
chip-only damage (worst drop 7.8% ≈ 59 HP; Matt's nova was a burst killer), because
`primordian_frigidring` is named-absent (HALT-2 — its compile is forbidden by the §14.23 H-1
freeze ruling and its magnitude sits inside the HELD damage clamp). Robustness: at the
declared sweep ceiling (67 DPH) the worst drop scales to ~10% — still chip; **no value inside
the swept range kills the werewolf without the burst mechanic.**

**The symmetry finding (the section's keeper):** Matt's WIN required evasion — inexpressible
(R-KC1-22). Matt's DEATH required the frigidring nova — also inexpressible (HALT-2 + H-1).
**Both outcomes of the real boss fight lived in mechanics the sim cannot yet express; what the
sim CAN express — the sustain economy — it resolved decisively (no flip).** The boss-tier join
is therefore thin by construction until the Q-KC1-1 wave builds telegraph/burst + dodge; the
tiers where opposition is MEASURED (trash/champion verbatim HP) are where fidelity claims
attach. This is C-7's law honored in both directions: no survival-with-handicap framing, and
no victory-parade framing either.

**What the finale still owes (the verdict-processing lap):** the N-band JOIN — sim-side
series (intake shape, A/B/C, kill-times, R2b-grain windows) against the fixture's measured
endpoints per the kit spec — producing the run's efficacy-verdict document. N-12 carries its
non-stationarity caveat (R2-whole grain both sides); coverage note carried like-for-like.
Then wind-down: C-1..C-5 doc closures · REPLICA-1 hand-off to drax · star-lord json rewrite
trigger · Q-KC1-1 wave hand-off to knight-rider (BQ-1/BQ-2/BQ-4 + leech carriers F-1..F-7 +
hero-scaling + dodge-on-tell + frigidring/telegraph modeling — with Matt's win banked as the
evasion acceptance fixture and this G-5 dataset as the before-baseline).

**Signed:** gandalf (`RUN-CONDUCTOR` / `DRIFT-CRITIC` reading), 2026-07-28.

---

## §14.27 — T-5 VERDICT LANDS: **HONORABLE FAIL — DECOMPOSED** · and the largest miss is the CONDUCTOR'S OWN FIRE COMMAND · repair lap fired same hour

**Banked 2026-07-28.** The T-5 verdict lap (named gandalf sub-agent, DRIFT-CRITIC, doc
`2026-07-28-kitcal1-g5-efficacy-verdict.md`, commit `ed26723e`) returned before band arithmetic
even mattered: **the coverage gate — run FIRST per pattern §6.1, exactly as T-5 orders — found
`r3_arm: false` and `player_pool: 759.0` on all 150 fights.** The kit spec's §6.0 sentence 1
("a band hit with a signature absent is a FAIL") therefore governs: **S-2 (DoT-tail lift) and
S-3 (gear-step hazard inversion) were never executed, and S-1 ran only its arc leg** (single-
target control unrun). Five of six primary signature legs missing → the battery-as-run cannot
reach PASS regardless of bands. Band table on the surface it CAN see: **1 weighting-robust PASS
(N-2) · 7 weighting-robust MISS (N-5, N-7…N-12) · 3 CUT-DEPENDENT (N-1/N-3/N-4 — a §6.3
defect owned in the verdict: no tier-weighting rule was pre-registered; both legitimate cuts
graded, the flattering one named and rejected) · 1 NOT SCORED (N-6).**

**Conductor verification + ownership (⚠ SWITCH: RUN-CONDUCTOR → DRIFT-CRITIC on my own fire
command).** Trust-but-verify confirmed every load-bearing claim byte-level: `r3_arm: False` in
the report, single pool 759, §6.0 sentence verbatim at spec line 540–541. And the decomposition
lands on ME: **gamora's harness SHIPPED `--r3-arm` (pool 1607 + poison DoT, built precisely to
serve S-2/S-3, assembly note §"CLI") and `--arm-a-jitter` — both default-OFF per assembly §3.2
— and the conductor's fire command took the defaults.** One deviation (jitter) I named at fire
time in §14.26; the other I did not even see. The verdict lap caught it. This is the desirable-
run pattern's coverage-before-accuracy observation (§6.1, the KIT-FIDELITY lesson) doing its
job against its own author.

**Consequence for §6.0's application — argued, not asserted:** "a band hit with a signature
absent is a FAIL" presumes the signature was TESTED and absent in result. A signature leg
*unrun because of a fire-command omission* is a coverage gap, not a sim inadequacy — grading
the sim FAILED on legs it was never asked to run would convert a conductor error into a
calibration verdict. **The verdict document stands as the verdict on the battery-as-run** (no
goalposts move); the honest repair is to RUN the missing legs under the same pre-registered
predicates and seeds, then amend.

**R-KC1-23 (conductor ruling, veto-open): repair lap fired immediately.**
- **R3-arm supplement: FIRED and LANDED** — same fire shape (`--run --r3-arm --seeds 30
  --seed-base 74000800`), separate out-dir `output/kitcal_g5/g5_r3arm/` (canonical report
  untouched). 150 fights, pool **1607.0** all fights, `r3_arm: true` in the report, engine
  `f54c547` (delta from `bef1f55` is gamora's Gate-2 C-1..C-5 comments-only pass — digest
  `25c212eb…` unchanged, so the batteries are metric-comparable; named, not assumed). The
  W-c→R3 like-for-like that S-2/S-3 pre-registered now exists on both sides at matched seeds.
- **S-1 control arm: COMMISSIONED** (gamora, in flight) — the one leg with NO harness support:
  `--s1-control`, arc skill swapped for a single-target basic attack, conservative-reading
  rule if ambiguous, predicate A ∈ [0.98, 1.05]. Tag `gamora/v-g5-s1control-1` on landing.
- **Amendment lap queued:** when the control lands, one verdict-amendment pass reads S-1
  (both legs) / S-2 / S-3 against their ratified predicates and re-applies §6.0 to a COMPLETE
  signature set. Until then the run's status line is: **honorable fail on the battery-as-run;
  signature verdict PENDING on the completed batteries.**
- Jitter stays OFF and stays a named deviation: the flip rule already resolved with a
  281–345 HP inter-arm gap; intra-arm jitter cannot reach it. Re-running for jitter would be
  motion, not information.

**The verdict's three keepers, banked before amendment (they survive it):** (1) the W-c hazard
distribution is **collapsed to its middle** — sim zero-intake 0.00 vs fixture 0.378, median
drop 3.8× too high, max 9.5× too low: *the quiet is gone for want of evasion, the violence for
want of burst* — the §14.26 symmetry finding now measured as a distribution shape. (2) The
A/B multi-kill statistics **invert** (sim A 2.25 vs fixture 1.76; sim B 1.12 vs fixture 2.41)
at identical grain — the one genuine category-(ii) sim-mechanics delta on the table (note:
A/B/C here are the kit-spec kill-structure statistics, NOT the leech arms). (3) The S-1
breadth diagnostic reads **1.36 hits/press vs the fixture's 2.36** — the sim's arc is
*narrower* than the fixture's, so the intuitive BQ-1/BQ-2 fix ("tighten the target cap")
would have moved the sim BACKWARDS. **N-11 graded MISS, not NOT-EVALUABLE** (sub-agent's
argument adopted: R-KC1-22 pre-committed to the death-2 anchor before results; un-grading it
after seeing the miss is goalpost movement), attributed wholly to category-(iv) mechanism-class
absence (frigidring) — **a MISS the build-class cannot close and which must never be cited as
a calibration error.** Carried to Matt veto-open, as is this whole section.

**Parallel landings this window:** Gate-2 doc conditions **C-1..C-5 CLOSED** (gamora: C-1
corrected at 4 sites not 2; C-2 citation fixed + `TestTwoPathReachability` added, 78 tests
green; C-3 45→42 at 3 sites; C-4 §7.0 names ARM PROJ `94236eb0…` as the discriminating
instrument; C-5 rewritten + 2 uncited sites of identical dormancy drift found and fixed;
engine `f54c547`, meta `5123cabd`). Hand-off queue filed and pushed
(`2026-07-28-kit-cal-1-handoff-queue.md`, `6a050059`): HQ-1 REPLICA-1→drax, HQ-2
self-rewriting `leg3_pilot…json`→star-lord (sequences first — active hazard), HQ-3 Q-KC1-1
wave inputs→knight-rider.

**Signed:** gandalf (`RUN-CONDUCTOR`; R-KC1-23 veto-open), 2026-07-28.

---

## §14.28 — S-1 CONTROL LANDS (gamora `ee5930a`): the control FAILS its band — and thereby exposes a COINCIDENCE FLOOR in the A statistic · plus a contradiction sent to Gate-2

**Banked 2026-07-28. Engine `ee5930a`, tag `gamora/v-g5-s1control-1`, pushed. Gamora flagged
"Gate 2 REQUIRED, not self-cleared" — Gate-2 FIRED (jack-ryan, in flight). The amendment lap
HOLDS until his verdict; this section records the landing, not conclusions.**

**Design choice (hers, conservative):** neutralize BOTH multi-target geometries — claws
cone→single_target AND charge line→single_target — at otherwise-EXACT canonical values,
because a weaker control drives A→1 by spacing kills out, which would make A≈1 stop meaning
"the arc was the mechanism." Hardest control to pass. Pins A-S1C-1/A-S1C-2 injection-proved;
27/27 harness tests; canonical `g5/`, conductor-fired `g5_r3arm/`, and `g5_s1control/`
outputs all banked in-repo (the canonical battery output had been sitting untracked — her
catch).

**Result: the control returns A = 2.667 / 1.333 / 1.200 (trash/champion/mixed) — OUTSIDE
[0.98, 1.05] at every pack tier; boss 1.000 passes.** And the pre-registered §1.1p second
instrument says why: the control reads **exactly 1.0000 hits/press, every tier, every seed**
— no press ever hit two bodies — so the excess A is **bin coincidence**: claws compile at
`cooldown_seconds = 0.0` (no player attack-speed model), sequential single kills land in the
same 0.5 s bin, and **A carries a coincidence floor above 1 at every pack tier.** Canonical A
must be read against that floor, not against 1. She did NOT repair it — the floor is a
property of the pinned canonical kit; changing it is a balance change in a control's costume.
Named, routed (attack-speed model → Q-KC1-1 wave input).

**CONTRADICTION → Gate-2 item 3:** verdict keeper (3) computed canonical breadth **1.36
hits/press** vs fixture 2.36 ("arc NARROWER; tightening the cap would move the sim
backwards"); gamora's landing computes **2.5816** vs 2.362 (within 9% — arc looks RIGHT).
Both cannot hold under one §1.1p definition. Jack-ryan adjudicates byte-level; whichever
number dies takes its conclusion with it. The amendment lap inherits the ruling.

**Also carried:** MIGRATION.md updated — the control/r3-arm artifact-shape changes are ones
**drax's REPLICA lane must widen for** (compounds HQ-1). `leg3_pilot…json` did NOT re-fire
during her test run (mtime unmoved; still dirty from the prior session) — one data point for
HQ-2's diagnosis: the trigger is not the harness tests per se.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-28.

---

## §14.29 — GATE-2 SPLITS: control landing CONDITIONAL PASS · **BLOCK on `g5_r3arm/` — the poison DoT NEVER TICKED** · S-2 was a null instrument, not a miss · R-KC1-24 fires the repair

**Banked 2026-07-28. Jack-ryan findings `b2267f6d`
(`qa/findings/2026-07-28-gate2-gamora-g5-s1control.md`), pushed.**

**What PASSED (conditional):** the control arm itself — independent leaf diff confirms exactly
7 differing leaves, all geometry; flag threading cannot masquerade; pins non-vacuous by
injection. **The coincidence floor is TRUE, reproduced at event level** — one kill per 0.1 s
tick, eight kills into three bins; `compute_abc` is not buggy; no alternative explanation
survives.

**The 1.36-vs-2.58 contradiction: RESOLVED — aggregation scope, no computational error on
either side.** The verdict doc pooled three tiers ex-boss (1374/1009 = 1.3617); gamora quoted
trash alone (253/98 = 2.5816); both reproduce to 4 dp; **neither is a valid §1.1p comparator**
(the pool is 75% mixed_pack; adding boss's 2,082 presses swings it to 1.1485). **Keeper (3)
SURVIVES on better evidence than it was born with:** `max_targets` is read NOWHERE in the
engine — the cap never binds (max observed hits/press anywhere = 4 vs cap 5) — and
`CONE_HALF_ANGLE_RAD = π/4` puts the A2 premise at the source. "Don't tighten the cap"
stands, restated density-conditional.

**The BLOCK (and jack-ryan's escalation to Matt):** across all 300 r3-arm fights, **zero DoT
events**. Live probe: 27.8 s boss fight, 95 hits, `DOT_TICKS=0` both arms; A/B/C bit-identical
W-c vs R3. Root cause: **`resolve_spatial_hit` discards the kernel's DoT into scratch — the
`_tick_effects` gate never opens.** So S-2's lever was never connected: **B lift 1.000 is a
NULL INSTRUMENT, not a MISS** — the third instrument-validity catch of this run (REPLICA-1's
zero-intake, the A coincidence floor, now this). Escalation scope, jack-ryan verbatim: *"the
projection-seam discard voids `dot` on every kit the spatial engine has run."* The canonical
claws kit carries **bleed** — if bleed routes through the same discarded path, the canonical
battery's offense side was wrong too.

**R-KC1-24 (conductor ruling, veto-open): the DoT discard IS the R-KC1-21 operand class** —
a kernel operator killed at the projection seam, sibling of the S1–S5 census fixes and C-11's
thrown-away kernel lifesteal. Fix pre-ratified by the ratified class line ("known-wrong
operands get fixed before validation"). **Gamora commissioned (in flight): blast-radius census
FIRST** (which effect types route through the discard; which of the three batteries carried
one; historical scope measured not speculated), then math note → minimal single-sourced fix →
re-run of every affected battery at matched seeds into `_fix` out-dirs (BLOCKed + banked
artifacts preserved as evidence), plus the undisclosed control-boss-loss asymmetry (10/60 vs
0/60) disclosed properly. Gate-2 re-reviews; the BLOCK is not self-cleared. **The amendment
lap now holds for the post-fix batteries** — the terminal signature verdict reads S-1 (settled
above) + S-2/S-3 from instruments that are actually connected.

**Signed:** gandalf (`RUN-CONDUCTOR`; R-KC1-24 veto-open), 2026-07-28.

> **R-KC1-24 RATIFIED by Matt, 2026-07-28** ("agreed on R-KC1-24") — the ruling closes from
> veto-open to RATIFIED. Fourth application of the operand-class line (S1–S5 wake · O-d ·
> now the DoT discard), all under the same principle: validation attaches to the state we
> keep. The historical-scope question (what re-validation the census's blast radius triggers
> OUTSIDE this run) remains Matt's, pending gamora's measurement.

---

## §14.30 — THE REPAIR LANDS (gamora `9f6805a`+`7483a21`) and OVERTURNS THE ESCALATION'S PREMISE: production is CLEAN, the "discard" was a SPELLING, and under the first null instrument sat a SECOND

**Banked 2026-07-28. Engine pushed through `7483a21`, tag `gamora/v-g5-dotfix-1`. Gate-2
re-review FIRED (jack-ryan, in flight; BLOCK not self-cleared). Re-run batteries at
`output/kitcal_g5_fix/`; BLOCKed + banked artifacts untouched, as evidence.**

**Root cause CORRECTED — jack-ryan's observation stood, his mechanism did not.**
`resolve_spatial_hit` discards nothing: `defender_state` IS `target.combatant_state`, the
object `_tick_effects` reads — proven by a measured falsifier (registry-spelled DoT through
the exact call: 8 poison stacks off 30 hits). The real site: **`resolve_skill`'s effect loop
handles exactly 26 names (10 literals + 16 registry ailments) with NO `else`** — the G-5 kit
dicts spelled `{"name":"dot"}`, which is in none of them, and it fell through in silence.
Voided class = the `dot` spelling, **2 sites, both in `kitcal_g5_scenarios.py`.**

**The census DEFUSES the escalation: production is CLEAN — 0 of 3,462 effect instances
across 632 season files fall outside the handled set; `git log -S` bounds the spelling's
entire history to `bef1f55` — today. Zero prior batteries.** Matt's reserved historical-scope
ruling dissolves if Gate-2 upholds the census (spot-verification commissioned). But **all
three G-5 batteries carried it** — the charge bleed was spelled the same way — so canonical
offense was wrong too; all three re-ran.

**Fix shape:** re-spell to `bleed`/`poison`, `tick_damage = magnitude/duration`, byte-neutral
`apply_chance` door; exactly one writer + one ticker on the path — a carry-back at the adapter
would have been a second writer, i.e. the O-d hazard, and was refused. **Residual hazard
NAMED, not fixed:** the no-`else` silent fall-through remains — Discipline #8 material, routed
to Gate-2 disposition. Tests 39 pass; 251 kernel-adjacent regression tests unchanged.

**The lever woke — and exposed a SECOND null instrument.** DoT ticks 0→60/0→180/0→3,150;
R3 boss elapsed 28.45→26.48 s. Yet **S-2's B lift is STILL 1.0000, structurally:**
`A×B×C ≡ kills/encounter`, which is CONSTANT in designed batteries (every tier always
clears) — **B is a residual of A and C, not an independent measurement; it returns 1.000 for
ANY DoT magnitude.** Two null instruments were stacked: first the lever was disconnected,
then the gauge it should have moved turns out to read a tautology in this frame. This is a
defect in the kit spec's OWN §6.2 S-2 predicate (conductor's spec — owned as such): B was a
live quantity in the fixture's telemetry, where encounter composition varied; in a designed
battery it degenerates. **The amendment lap must rule what S-2 evidence is valid** (DoT
damage share; kill-time delta R3-vs-W-c — 28.45→26.48 s IS a real S-2-shaped signal) —
and must re-read keeper (2)'s "B inverts" against the same degeneracy.

**Boss-loss disclosure (owed from §14.29):** control 50/60 → 56/60 post-fix (the control
overkills less, so its bleed lands 3× more often); canonical 60/60 both. Narrowed, not
closed; rides into the amendment. Jack-ryan's §3 keeper survives on corrected grounds: in
canonical the charge one-shots its targets and the liveness gate correctly refuses
corpse-DoT.

**NEW FINDING → MATT (decision-shaped, not part of the BLOCK): DoT delivery is tick-rate
dependent.** `sum(0.1×10) = 0.9999999999999999` — at `TICK_SIZE=0.1` **every DoT the engine
has ever ticked delivered 90% of its declared damage** (0.25/0.5/1.0 tick sizes → 100%).
Pre-existing, production-wide, floating-point accumulation. Decision teed in-session; if
unruled at session end, files to `canonical/matt_decision_needed/`.

**`leg3_pilot…json`:** shows modified but hash `b73ec83…` IDENTICAL at session start and end,
mtime pre-session — HQ-2 data point: the mutation event is real but not reproduced by any
harness/test session today.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-28.

---

## §14.31 — GATE-2 RE-REVIEW: **BLOCK LIFTED** · census verified 5.7× broader · S-2's B proven UNSATISFIABLE BY CONSTRUCTION · and the tick-rate finding CORRECTED UPWARD: the run's own bleed delivers **66.7%**

**Banked 2026-07-28. Jack-ryan addendum
`qa/findings/2026-07-28-gate2-gamora-g5-dotfix-addendum.md` (`ead08351`).**

- **BLOCK LIFTED on the post-fix artifact.** Pre-fix `g5_r3arm/` permanently quarantined as
  evidence; the two must never be pooled (his SS-1). Root-cause correction ACCEPTED and filed
  at his §0, with the Discipline #10 failure owned by name (mechanism inferred from a
  docstring whose enumerated list was attacker-side only). All DoT-wake tick counts
  re-derived exactly; boss-loss disclosure verified.
- **Census VERIFIED on a broader base than gamora's:** 5,110 JSON walked, **19,642 effect
  instances, 0 unhandled** (5.7× her sample) + AST pass over every `.py` (only unhandled
  literal left is her own injection test). His words: *"my escalation's scope claim is
  falsified — Matt's historical ruling is now trivial: no historical scope, no re-run owed."*
  **Matt's reserved historical-scope question CLOSES as moot.**
- **No-`else` hazard: wave-routed, not conditioned** (zero live exposure; kernel-level;
  recommended shape — derived frozenset + strict-raise behind a flag — in his §3). →
  Q-KC1-1 input.
- **S-2's B: not just degenerate — UNSATISFIABLE BY CONSTRUCTION.** His sweep (which gamora
  didn't run): DoT magnitude across six orders — **B flat at 1.0000 on three of four tiers**,
  including at a magnitude that cuts boss kill-time 4.2×; on the fourth it moves *against*
  the lever. The identity `A·B·C ≡ kills` holds at 0 violations / 450 fights, kills pinned
  by design. His recommendation to the amendment lap: re-express S-2 on **boss kill-time
  delta** (measured 0.93 s, sd 0.63) + **DoT damage share** (0.732% → 4.062%). Grading call
  stays with the amendment lap, as chartered.
- **Tick-rate finding NOT verified — CORRECTED, and the defect ENLARGES.** The "90% at
  TICK_SIZE=0.1" was an artifact of gamora's fixed-wall-clock probe (`sum([0.1]*10)` is
  exactly 1.0 in his derivation; the drift is CULL-driven, not accumulation-driven — both
  accumulators drift identically and the race buys a 101st sub-tick → 100% at 10.0 s).
  **At shipped durations the defect is worse: the 3.0 s charge bleed delivers 540/810 =
  66.7% of declared** — confirmed in the artifact at 90/90 applications, zero exceptions.
  **Short DoTs are hit hardest** — inverting the risk shape the 90% number implied. The
  post-fix batteries' bleed numbers are ~33% light. **The Matt decision teed in §14.30
  stands with corrected numbers** — (a) fix-now + one more battery re-run vs (b) named
  deviation — and the (a) lean strengthens: the terminal verdict would otherwise sit on
  batteries whose newest-woken mechanic delivers two-thirds of its declared damage.

**Run state:** the amendment lap (terminal signature verdict: S-1 settled · S-2 on the
re-expressed instruments · S-3 from `_fix`) now waits on exactly ONE input — Matt's
tick-rate ruling, which decides which batteries it reads.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-28.

> **R-KC1-25 RATIFIED by Matt, 2026-07-28** (verbatim: *"Agree - (a) Fix now under the
> R-KC1-21 principle and re-run the _fix batteries once more, so the terminal verdict sits
> on a fully-repaired stack."*) — the cull-driven DoT under-delivery (66.7% at 3.0 s per
> Gate-2's corrected derivation) gets fixed at the kernel ticker NOW; all three batteries
> re-run into `_fix2`; the terminal verdict reads the fully-repaired stack. Fifth
> application of the operand-class principle, and the first to touch the production-shared
> kernel path — Gate-2 review is therefore MANDATORY on the fix before the amendment lap
> reads its output. Gamora commissioned.

---

## §14.32 — R-KC1-25 EXECUTED: kernel delivery ledger lands (`3aa4a55`) · `_fix2` batteries are the terminal stack · mandatory Gate-2 fired · and the KIT-CAL-2 capture protocol ships to Matt

**Banked 2026-07-28, post-kernel-fix landing.**

**1 — Gamora's fix lap confirmed jack-ryan's correction AND extended past it.** The cull-race
derivation was verified — and then rooted one level deeper: the defect is **a continuous
declaration paid in indivisible 1.0 s pulse lumps**. Her falsifier: at `ts=0.25` (exact
binary, zero float drift) a 1.5 s DoT still delivers 66.7% — so the race is a symptom, the
lump quantization is the disease. Her 52-cell duration×tick-size matrix spans **0%–200% of
declared** (both under- and over-delivery), and non-integral durations are *ordinary*, not
edge-case: `control_duration_bonus` affixes add 0.5–2.0 s continuously. Smoke (`ts=0.5`)
and full (`ts=0.1`) batteries had been silently measuring DIFFERENT DoT totals — a
validation-integrity defect, not just a balance one. Extension routed to Gate-2 for
adjudication alongside the fix itself.

**2 — The fix: an integer delivery ledger** (engine `3aa4a55`, tag `gamora/v-dot-delivery-1`).
`n_pulses = max(1, round(D / 1.0))`; `per_pulse = tick_damage · D / n_pulses`; pulse *k*
fires at the first sub-tick where `e·n_pulses ≥ k·n_subticks` — total delivered ≡ declared,
by construction, at any tick size. 3 sites, +134/−7. **Scope fence held:** DoT + HoT only;
the control-ailment layer is byte-identical under an 8-name pin; refresh carries intra-pulse
phase. Evidence: 393 invariant tests (212 fail on the pre-fix kernel — non-vacuous), 251/251
regression unchanged, exactly ONE pinned expectation moved (DW-5 900→1000 — the fixed-clock
probe now measuring a correct kernel).

**3 — `_fix2` is the terminal-verdict stack** (`output/kitcal_g5/kitcal_g5_fix2/`, all three
batteries re-run per R-KC1-25). Deltas from `_fix`: boss R3/W-c kill-time delta
0.9309 → **0.9160 s**; DoT damage share R3 4.770 → **6.215%**; **no tier outcome changed**;
S-3 11/12 unmoved. The re-expressed S-2 instruments (boss kill-time delta + DoT share)
both survive the repair with signal intact. W-c boss elapsed unmoved — the canonical bleed
remains corpse-refused by the G-4 liveness gate (S-2's lever is overkill-gated, as found).

**4 — Mandatory Gate-2 fired** (jack-ryan, in flight) per R-KC1-25's first-production-kernel
condition. The amendment lap (terminal signature verdict on `_fix2`) holds until his verdict.

**5 — KIT-CAL-2 substrate capture: the EoR Warlord play-test protocol is authored and on
Matt's share.** `gandalf/notes/2026-07-28-eor-warlord-playtest-directions.md`, byte-identical
copy at `/Volumes/reincarnated/matt-notes-from-pc/eor-warlord-playtest/DIRECTIONS.md`.
Design: **same arena, new fighter** — same campaign, path, and Primordian endpoint as the
werewolf fixture, so the measured opposition side is held constant and every fixture delta
is the kit. Every KIT-CAL-1 capture cost is encoded as a rule: name pre-chosen (`EoR
Warlord 01`), devotion-zero as rule not attestation, no mid-combat screenshots, mic
narration of load-bearing moments, batched gear steps, three screenshot ceremonies, the
**10-hold channel probe** (closes the shortlist's `skill_use_count` activation-vs-tick
unknown), deaths-are-data, save-flush + don't-play-after-end (T11 SSH copy). **FORK-1 open:**
EoR earliest-online timing — legolas extracting the measured answer from the `.arz` (in
flight); the share copy gets amended **§7-RESOLVED** when it lands; the doc's §5.1
two-window rule makes the run right either way.

**Run state:** two in-flight inputs — jack-ryan's Gate-2 on `3aa4a55` (gates the amendment
lap) and legolas's EoR unlock extraction (gates the §7-RESOLVED amendment; does NOT gate
Matt starting play, per the two-window rule). Nothing else is owed before the terminal lap.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-28, §14.32.

---

## §14.33 — GATE-2 ON THE KERNEL FIX: **BLOCK** — single-application repair verified perfect; the refresh phase-carry is an opposite-signed regression on the dominant production path · repair lap commissioned

**Banked 2026-07-28. Jack-ryan finding
`qa/findings/2026-07-28-gate2-gamora-dot-tick-delivery-r-kc1-25.md` (`edf6d3fb`, pushed).**

- **Root cause: hers supersedes his, conceded without hedging.** His float-race derivation
  explained integral-duration cells only; her 1.0 s-lump (M-1) + over-delivery (M-3) mechanisms
  reproduced on his independent harness cell-for-cell, including a cell her matrix missed
  (D=0.3, ts=1.0 → **333%**). Symmetric honesty across two laps: he corrected her 90%, she
  rooted past his 66.7%, he ratified her supersession.
- **Single-application repair: NOTHING FAULTED.** Full 12×4 matrix 100.0% every cell,
  adversarials, degenerates, determinism, cadence, 13-name control byte-neutrality, HoT
  conservation — all independently reproduced. The ledger design stands (his §8).
- **The BLOCK (his §3): refresh phase-carry under-credits by a factor of `n_pulses`.**
  Time-to-next-pulse after refresh = `ceil((N+phase)/P′) − phase` → credits `phase/P′`,
  forfeits `phase·(P′−1)/P′` per refresh; at `P′=1` the credit is exactly zero (total
  starvation under continued re-application; worst measured reachable-by-future-content cell
  0.182). Sustained 120 s grids: post-fix **0.55–1.00** where pre-fix read a uniform
  **0.992** — worse in 34/54 cells. Gamora's own math note §3.4 names the approximation in a
  parenthesis, then concludes "non-starving" — *the parenthesis is the bug.* Production
  reachability: `primary_attack` cooldown 0.0–1.5 s × ailment_chance 0.25 — the refresh band
  is the dominant DoT mode, not the exotic one.
- **Double structural blindness, one layer down:** the guard test scores **8 pre-fix and 8
  post-fix** (non-discriminating), and `_fix2` exercises refresh **zero times** (W-c bleed
  rows `{3:30}` — one application per fight; R3 poison never re-binds). The fixture chosen to
  validate the repair is the one fixture that cannot exercise the repaired path — gamora's
  own smoke-gate diagnosis, recursed.
- **`_fix2` headline numbers: every one reproduces exactly** on his independent recomputation
  (his §4 table) — but **`_fix2` is NOT final** (C-3). Two evidence-integrity defects: `_fix2`
  stamped with pre-fix hash `7483a21` (C-4); quarantined `kitcal_g5/smoke/` WAS overwritten
  despite the commit's "UNTOUCHED" claim (C-5) — recoverable from git, but the declared
  meaning was violated.
- **Leech question asked-and-answered:** NO leech on the DoT tick path at all (O-d is per-hit
  in `_apply_skill_damage`). But `delivered` is HP-pinned, so the DoT gain is exactly offset
  by direct-hit loss → `leech_capacity_total` falls by `Δ_DoT × door_pct`: **non-poolable
  across fix generations**, to be named in SS-1 (C-6). SS-2 understates the HoT
  overheal-clamp interaction (magnitude, not just timing).
- **Conditions:** C-1 (phase credit to FIRST post-refresh interval only — his §3.2 / her own
  parenthesis) · C-2 (discriminating ≥120 s refresh sweep, non-vacuity by stash) · C-3
  (`_fix3` batteries; his prediction — verify, don't assume — headlines invariant) all BLOCK;
  C-4/C-5/C-6 WARN; C-7 INFO (banker's-rounding cadence note).
- **Routing (ADR-002):** within-seam; gamora implements, jack-ryan re-reviews; **Matt
  escalation only if** (a) gamora disputes / argues ship-as-named-shift, or (b) C-1 moves the
  G-5 headlines — either makes `_fix2` non-final in substance.
- **Repair lap COMMISSIONED** (named gamora sub-agent, background) with C-1..C-7 verbatim +
  both HALT triggers; commit-not-push; target tag `gamora/v-dot-delivery-2`; batteries into
  `kitcal_g5_fix3/` on matched seeds/flags, sequential.

**Run state:** the terminal-verdict stack moves `_fix2` → **`_fix3`** (pending repair +
re-review). Amendment lap holds on the re-review PASS. Sixth consecutive instance of the run
finding its own instruments disconnected — and the fifth operand-class fix now audits its own
first draft. FORK-1 (legolas, EoR unlock) still in flight, independent.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-28, §14.33.

---

## §14.34 — FORK-1 RESOLVED: EoR castable at level 10, main attack ~20, and the channel's energy cost is charged PER TICK — play-test directions amended §7-RESOLVED on both copies

**Banked 2026-07-28. Legolas findings `legolas/notes/2026-07-28-eor-unlock-timing.md`
(committed by legolas; pushed by conductor).**

- **Earliest castable: character level 10** — two independent gates land on the same level
  (tier-6 gate = Oathkeeper bar 25, whose 27-point minimum equals level 10's income exactly;
  and `masteryIncrementLevel = [1,10]` first legalises the second mastery there). Level 12
  (werewolf band) reachable with 6 points spare.
- **The trap, banked:** `skillMasteryLevelRequired` reads 0 on EVERY Oathkeeper skill — the
  real gate is `skillTier` against `gameengine.dbr :: skillMasteryTierLevel =
  [1,5,10,15,20,25,32,40,50]`, found only by brute-force scan of all **93,190 records**
  across the four archives. Base-game record; no expansion overrides it.
- **The sharp finding: `skillManaCost` on channels is per TICK, not per second** (dev text:
  0.16 s ticks at 100% attack speed; `timeBetweenAttacks × 0.8` reproduces it on EoR, FoI,
  AAR alike). EoR r1 = **25 energy/s** vs ~575 pool @ 1.0/s regen → **≈24 s of continuous
  channel**; r16 → ~8.5 s. Fixture consequence declared in the directions: broken channel
  segments are energy-attributed data, not piloting error. This lands directly on the
  KIT-CAL-2 gap family (sustained channel) — the sustain *constraint* is now a measured
  input to the kit spec, not something to be reverse-engineered from pixels.
- **Realistic main-attack band ~15–21 (~20 honest)** — point-budget + sustain argument, NOT
  a DPS crossover (flagged; crossover is a tractable follow-up if wanted). EoR's own
  modifier line (`eyeofreckoning2.dbr`) is tier 8 = bar 40 ≈ level 28 minimum — a "complete"
  kit is a materially later character than a "castable" one.
- **Directions amended:** §7 → **§7-RESOLVED** on the meta-repo record AND the share copy
  (byte-verified identical). Headline change to Matt's plan: the §5.1 two-window path is now
  the EXPECTED path — Primordian in the Righteous-Fervor window (werewolf-comparable), then
  continue to the EoR era (~15–20) + 10-hold probe + one boss-grade fight.
- **Open residue (his §7, one-directional):** quest skill-point rewards unenumerated (can
  only LOWER the floor, by ≤1 level); Spirit→regen conversion engine-side (1.0/s is a
  floor); `masteryMilestoneValueMax = 56` recorded as an oddity. None gates play.

**Run state:** FORK-1 closed. Outstanding: gamora's C-1..C-7 repair lap → jack-ryan
re-review → amendment lap on `_fix3`. Matt may start the KIT-CAL-2 capture whenever he
likes — the directions are final.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-28, §14.34.

---

## §14.35 — SIDE PROBE (Matt question, not a chartered lap): Primordian endgame availability — two corrections + one fixture opportunity

**Banked 2026-07-28. Legolas `legolas/notes/2026-07-28-primordian-endgame-availability.md`
(`0c8d54f4`, pushed). Legolas-measured; conductor spot-verification deferred — nothing here
gates the run.**

- **Correction 1 (naming, mine to own):** Primordian is a **base-game Act-1 (Wightmire)
  boss**, not a Fangs-of-Asterkarn one — gdx3 contains no Primordian data at all. Earlier
  conductor messages calling him an Asterkarn boss were wrong; the play-test directions are
  unaffected (they name him only as the werewolf run's target).
- **Correction 2 (scaling premise inverted):** the Crucible **overrides the boss life
  equation** (`((charLevel·25)^1.5)+100` vs campaign `((charLevel·51)^1.53)+2400`) —
  campaign-Ultimate Primordian (≈4.3–8.0M life at L100) is **6–8× more durable** than
  Crucible-Gladiator's (≈647K–1.05M at wave ~132). "Endgame Crucible" is the *easier*
  Primordian.
- **Availability:** Crucible YES (tier09/w06 guaranteed ≈ wave 86; tier14/w02 50/50 vs
  Viloth ≈ wave 132; data in-corpus — Crucible ships as a mod, so the depot fetch already
  holds it). Campaign all difficulties YES (no level gate). Shattered Realm NO in practice
  (absent from all 16 `proxy_bossall*` variants; selection-rule residue flagged U).
- **KIT-CAL input (routed, not banked):** the Crucible's own Primordian record has
  `dropItems=False` and ALL equip slots zeroed → a **gear-uncontaminated HP-closure
  fixture** candidate for the held HP-operator question (§14.10 lineage). Filed as an input
  to the Q-KC1-1 wave / HP-closure lane, pending conductor verification if ever load-bearing.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-28, §14.35.

---

## §14.36 — C-1..C-7 REPAIR LANDS (`67e7ccb` + `2be600f`, tag `gamora/v-dot-delivery-2`, pushed): gamora REJECTS C-1's letter by measurement, ships an absolute-time carry · C-3 verdict "nothing moved" — 450 traces byte-identical · Gate-2 re-review fired

**Banked 2026-07-28, post-repair-lap. Conductor verified commits/tag/`_fix3` arms/tree state
before pushing; substance verification is the re-review's (in flight).**

- **C-1 — the letter rejected, the intent shipped.** She derived, prototyped, and MEASURED
  jack-ryan's prescription (phase credit to first interval only): still 0.964 at Δ=0.1 /
  **0.708 at Δ=0.5** (D=6.37) — restarting at k=0 traverses only the systematically-longest
  interval: the blocked defect class plus smoke/full divergence, one order down. Shipped
  instead: **phase carried in absolute time** — `sched_carry_us` accrues µs, debited
  `round(1e6·D/P)` per pulse; microseconds are the only re-bind-invariant unit, so refresh
  converts nothing and loses nothing; `_add_or_refresh` collapses to one line; a
  final-settlement clause keeps INV-1 exact; **new INV-4** (delivery rate independent of Δ,
  cadence, and duration to 1 µs). *Whether the substitute stands is the re-review's call —
  a developer measuring her reviewer's prescribed fix failing is the discipline working,
  not defiance.*
- **C-2 — discriminating at last:** 44/50 fail on the pre-C-1 kernel (survivors exactly the
  `reapply=1.0` column, the one lattice-aligned cadence). Reproduces jack-ryan's §3.1 grid
  cell-for-cell through the production writer. **And a correction back at the reviewer:**
  his §3.2 prose transposes his own formula's credit/forfeit split (her §10.1) — teed for
  his ruling.
- **Post-repair grid: 48/48 at 1.000000** (single exception 0.999736 = one settlement pulse
  in flight at the 120 s window edge — rate-correct); rows constant across cadence AND
  identical between Δ=0.1/Δ=0.5; the `P=1` total-starvation cell reads 1.000000, was 0.000.
- **C-3 — THE ESCALATION TRIGGER READS ZERO:** 33 headline cells, 0 moved; invariant blocks
  byte-identical; **all 450 trace files byte-identical with header hash stripped** (a check
  nobody asked for — the strongest possible form of the invariance claim). `_fix2` final in
  substance; **`_fix3` supersedes in provenance only.** No Matt escalation on either trigger
  (no dispute — she out-measured the prescription rather than disputing the block; no
  headline movement).
- **C-4/C-5/C-6/C-7:** `-dirty` hash suffix (root cause was a dirty tree); ordering now
  code-commit → clean-tree battery → outputs-commit (`_fix3` stamps `67e7ccb`);
  `output/kitcal_g5/` restored byte-identical + writer now REFUSES cross-hash overwrite;
  SS-1/SS-2 extended, SS-5/SS-6 added; banker's-rounding note in. Tests: **442 / 263 / 904,
  0 failed.**
- **HQ-2 root cause found in passing:** her session-82 claim that
  `leg3_pilot_section8a1_band_measurement.json` doesn't mutate is **false — the batteries
  write it.** Restored, left unstaged as the live reproduction. Handoff queue HQ-2 updated:
  star-lord's search space collapses from "unknown import-time trigger" to "the battery
  writer path."

**Run state:** Gate-2 re-review in flight (jack-ryan; adjudicates the C-1 substitute, his
own §3.2 transposition, and the C-3 zero). On PASS → amendment lap reads **`_fix3`** and
the run terminates. Matt interface: nothing owed; both escalation triggers read clean.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-28, §14.36.
