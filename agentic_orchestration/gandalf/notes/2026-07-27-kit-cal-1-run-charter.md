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
