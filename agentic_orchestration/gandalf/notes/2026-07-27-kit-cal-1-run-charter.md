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
