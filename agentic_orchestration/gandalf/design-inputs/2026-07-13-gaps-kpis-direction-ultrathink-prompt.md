# gandalf ultra-think — gaps, negative-kit learnings, functional KPIs, and a direction re-assessment

**This document IS the session prompt.** Paste it (or point a fresh gandalf session at this path).
It is self-contained: it assumes no memory of the conversation that produced it. It is the *sequel*
to the family-definition ultra-think — read that output first (§0.2), build on it, do not re-derive it.

---

## 0. Who you are + bootstrap reading

### 0.1 Role
You are **gandalf**, the Reincarnated project's story/design/architect/elicitation steward. Adopt the
role: read your operating procedure (`agentic_orchestration/operating-procedures/gandalf.md`) and role
definition, then the artifacts below, then execute this as a **Pattern-B sustained design analysis**.

Lead every cognition with a role tag (`▶ ROLE: SPEC-AUTHOR / ARCHITECT / DRIFT-CRITIC / ELICITOR /
CANON-STEWARD`). Ground every non-trivial claim in a corpus query, a code read, or a file read
(**Discipline #11 — re-read at *assertion* time, not just investigation time; do not assert what you
can check**). **No sleep/rest/"fresh eyes" recommendations. No time-of-day / timezone framing —
workstream-relative only.** Anchor every recommendation to a concrete **player consequence**. Cite
genre by name *and decision* (Diablo I–IV + Immortal, PoE 1/2, Last Epoch, Grim Dawn, Titan Quest,
Torchlight, Vampire Survivors, isekai works). **Ultra-think: reason deeply before you answer, and do
not merely ratify the framings below — the value of this session is independent derivation. Break what
deserves breaking.**

### 0.2 Read, in order
1. `agentic_orchestration/gandalf/design-inputs/2026-07-13-family-definition-analysis.md` — **the
   primary input.** The settled result you build on: *a family is a fiber of the behavior map B*
   (member-count-free); the invariance/irreducibility/maximality conditions; identity/texture is
   per-region and behavioral; the structure is a lattice not a partition; lift is demoted to a triage
   annotation; gaps = fibers with zero samples = Mendeleev predictions; coherence = domain-membership
   of B, not corpus co-occurrence; and the §7 honest-cost list (ε replaces minsup; sim-as-oracle risk;
   coherence ≠ fun).
2. `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` — the 13 Class-A coordinates,
   §6/§6.1 the strict-13 cell key, the never-demote-core vs demotable-with-evidence split.
3. `agentic_orchestration/gamora/analyses/2026-07-13-cell-key-dedup-v1/collapse-structure-report.md`
   — the 470→457 dedup + near-twin adjacency aggregate.
4. `agentic_orchestration/gandalf/design-inputs/family-discovery-poc-rerank.py` — the FCA + lift PoC.
   **Re-run it** (`python3 …`) to reproduce the fibers you will treat as proxy-confirmed families.
5. **The simulation seam** (for Charge B — you cannot theorize B's KPIs without reading what the sim
   actually computes): `reincarnated-engine/src/reincarnated/simulation/` (fight engine, damage
   resolver, batch runner, balance loop) and `spirit_guide/`; and `reincarnated-engine/src/
   reincarnated/telemetry/` for what is already measured/logged. Note known telemetry gaps
   (engine_version unknown, termination_reason missing) surfaced in prior analyses.
6. **For the direction re-assessment (Charge D):** `canonical/00-ground-state.md`, then the three
   spec homes' indices — `canonical/reap-die-rise-story/00-index.md`,
   `canonical/reap-die-rise-engine/00-index.md`, `canonical/reap-die-rise-game/00-index.md` — plus
   `canonical/current-to-end-state/` (build-vs-spec deltas). This is where "breadth is the pitch" and
   the One Realm MVP live; you must know the direction to re-assess it.

### 0.3 Corpus access (read-only)
`agentic_orchestration/research/curated/corpus.db`. Always `PRAGMA query_only=ON`. Two tables matter:
- **`canon_engine_key`** — the keyed **470** combat-kits (filter `row_class='combat-kit' AND cell_key
  IS NOT NULL`). 14-slot `cell_key` pipe order (positions 1–14):
  `movement | delivery | amp | geometry | treatment | function | defense | economy | proxy | range |
  tempo | commit | activation | dependency`. `unknown`/`blank` are literal values, some are
  missing-data-in-disguise (an economy backfill is owed).
- **`canon_corpus`** — the fuller **524**-kit record, with a **`negative` INTEGER** column. `negative=1`
  marks the **38 filtered-out kits** (Charge A). Each carries `lattice_coord` (a compact 6-char coord,
  NOT the 14-slot key), raw coord columns (`geo_raw, ctrl_raw, def_raw, econ_raw, mob_raw`), a design
  postmortem in `mech_note`, and a filter reason in `mobile_blocking_mechanics`. **37 of the 38 are not
  in `canon_engine_key`** — they were filtered before keying.

---

## 1. The frame — two altitudes, bottom-up

Matt's charge has a concrete floor and a meta ceiling, and the floor *feeds* the ceiling:

- **Floor (Charges A–C):** mine the **38 filtered-out kits** (`canon_corpus.negative=1` — the genre's
  labeled trap-skills and dead branches) for learnings, derive *functional KPIs* that operationalize
  the behavior map B, and *enumerate the gaps* (the predicted archetypes). The filtered kits are the
  key that unlocks the others: they label which empty cells are *tried-and-rejected* graveyards vs
  *unclaimed* virgin territory, and they are labeled bad-KPI points for deriving the KPIs.
- **Ceiling (Charge D):** ultra-think through the whole current project, **re-assess whether we are
  moving in the right direction, and steelman the alternatives** — using the floor findings as
  evidence. If failure-pattern mining shows the coordinate model is broken, or that many cells died for
  want of an economy home (the *setless-orphan* pattern), or KPI feasibility shows the sim cannot be
  the oracle, those are *ammunition* for the re-assessment. Do the floor first; let it inform the
  ceiling.

---

## 2. What is settled — build on it, do not re-derive
From the family-definition analysis (§0.2 item 1):
- **Definition:** a family = maximal axis-aligned region on which fight-sim behavior B is invariant to
  its free coords (a fiber of B). Member count = sampling density, never definition.
- **Identity/texture partition:** per-region, behavioral (perturb a coord — does B move > ε?).
  Structural signal is a candidate-generator only; design-semantic is the mandatory cross-check and
  final authority on feel.
- **Three-way split:** Definition (fiber) / Validation (cross-*source* recurrence) / Prioritization
  (population + market salience). Lift is a triage annotation, never a definition.
- **Structure is a lattice/cover, not a partition** (Fork B). "The table" is a projection/view.
- **Reproduced fibers** (treat as proxy-confirmed families until the sim pipeline exists): Whirlwind
  (lift 2120), Trap/Mine (1426), Aura-damage (1230), Minion/Turret (622), Channeled-Beam (233),
  Totem/Sentry (224). The lift-1.1 mush (`126 kits · treatment=damage · function=none · …
  everything varies`) is the null family.

The one thing the family analysis deliberately left abstract: **what B actually measures.** That is
Charge B, and it is load-bearing for everything downstream.

---

## 3. Charge A — learnings from the *filtered-out* kits (the genre's labeled negative design space)

**What the negatives actually are (verified this session).** `canon_corpus` holds 524 kits; the
`negative` column flags **38** that were filtered OUT of the keyed 470 — and they are not junk. They
are the genre's canonical **trap-skills and dead branches**, each with a design postmortem in
`mech_note`. Examples: `d4-incinerate` ("rooted, short-ranged, out-damaged by everything mobile —
tier-list bottom for D4's whole run"); `d2-golemancer` ("golem-as-primary-damage never worked across
two decades"); `d2-blaze-sorc` ("movement-paints-damage inversion that never produced a viable loop");
`d3-firebomb` ("no set, legendary, or meta ever wanted"). **These are the empty cells someone already
tried** — the genre's own record of what fails. Matt's insight: they teach us about the gaps.

**Access.** `SELECT kit_id, folk_name, corpus_bucket, lattice_coord, mech_note, mobile_blocking_
mechanics, geo_raw, ctrl_raw, def_raw, econ_raw, mob_raw FROM canon_corpus WHERE negative=1`
(query_only). To *place* a negative near a cell you must re-key it (map `lattice_coord`/raw → the
13-coord register); 37 of 38 are unkeyed. Flag that re-keying cost — it may be a task for elrond/rocket.

**Step 1 — separate the two axes of "negative" (verified split 33/5; do not conflate):**
- **Genre-negative (33)** — the design *failed in its source game* (`mech_note` is a postmortem).
  THIS is the graveyard signal you are mining.
- **Pipeline-negative (5)** — our engine *could not classify it* (`mobile_blocking_mechanics LIKE
  '%no rule matched%'`). A curation TODO (→ elrond/rocket to add rules), **NOT a design failure.**
  Keep it out of the graveyard analysis — an unprocessed kit is not a failed one.

**Step 2 — cluster the genre-negatives into FAILURE PATTERNS.** The postmortems already rhyme; make it
rigorous. Candidate patterns visible in the data (verify, refine, add): *channel-flame-rooted*
(d2-inferno, d4-incinerate — rooted+channel+short-range, out-damaged by mobile); *movement-verb-
miscast-as-damage* (d2-leap-attack, d2-blaze, d4-blade-shift, d4-kick, d3-wave-of-force — "the
movement verb was the value, the damage was the pretense"); *single-target-trap-on-cooldown*
(gd-blade-trap, d2-impale); *fused-hybrid-that-scales-neither-half* (gd-reap-spirit, d2-golemancer);
*setless-orphan* (d3-firebomb, d3-wave-of-force, d4-wind-shear — mechanically fine but no
itemization/economy home ever wanted it); *degenerate/broken* (hot-blood-catcher — hundred-billion-
damage bug). Each pattern is a **known-bad REGION** of coordinate-space.

**Step 3 — cross-source NEGATIVE recurrence is a first-class signal.** A failure pattern that recurs
across independent franchises (channel-flame-rooted died in *both* D2 and D4) is the negative twin of
the validation layer: as much as six studios converging on Whirlwind proves a *good* natural kind, two
studios independently killing the channel-flame-rooted cell proves a *bad* one. Count the source-
diversity of each failure pattern; a mono-source failure may be one studio's tuning miss, not a law.

**Step 4 — negative-positive collisions (Matt's signal; a distinct, high-value diagnostic).** When a
genre-negative, once re-keyed, lands in the *same cell* as a surviving canon positive, that collision
means one of two **opposite** things — disambiguate each case using the `mech_note` postmortem:
- **Intrinsic → the register is blind.** The two kits genuinely play differently (one viable, one a
  trap) but the 13 coords cannot see the difference → a **missing coordinate** in exactly that region.
  This is the sharpest register-completeness signal we have: the negatives point precisely at where the
  model fails to separate viable from trap. (E.g., if `d4-incinerate` collides with a *working* channel
  kit, the separating coord — movement-tax? damage-per-cast vs uptime? range-band? — is missing.)
- **Extrinsic → the cell is fine; the *game* differs.** The same mechanical signature works in game A
  and fails in game B because of surrounding systems — itemization economy (the setless-orphan
  pattern), mobility baseline, breakpoint/tuning, monster density. The cell is well-defined; viability
  is game-context-dependent (a Class-B/context property, not Class-A identity).

The two readings drive **opposite** actions: intrinsic → *fix the register*; extrinsic → the cell is
viable-conditional-on-systems, and **our** systems may be the antidote — a genre-graveyard our economy
could revive is an **opportunity**, not a warning (arguably the most exciting output of the whole
charge). Report every collision with its reading and its consequence.

**What each feeds (why the charge matters):**
- **→ Charge C (gaps).** An empty cell adjacent to a genre-negative is a **GRAVEYARD** (tried-and-
  rejected), not virgin territory. This makes the three-way split of empty cells *data-backed*:
  **unclaimed** (green — up-rank), **tried-and-rejected** (red — down-rank / redesign-required),
  **forbidden/incoherent** (void). This is the single most important use of the negatives.
- **→ Charge B (KPIs).** The negatives are **labeled bad-KPI-region points.** "rooted + short-range +
  out-damaged-by-mobile" is a *functional* failure signature. Known-bad (negatives) + known-good
  (confirmed fibers) together are supervised labels to *derive and validate* the KPI set that separates
  viable from trap — the closest thing to ground truth for the fun/coherence question the sim cannot
  yet answer directly.
- **→ register + curation.** The 5 pipeline-negatives (and any misplaced negatives) route to
  elrond/rocket as a curation-completeness signal, kept separate from the design signal. Note whether
  any failure pattern also implies the *coordinate model* is blind or overfit (DRIFT-CRITIC): if the
  register cannot even express *why* a trap-skill is a trap, it is missing a coordinate.

**Deliverable for A:** the negatives split into genre vs pipeline; the genre set clustered into named
failure-patterns with cross-source counts; and, per pattern, (a) the coordinate-region it condemns (for
Charge C graveyard-labeling), (b) its KPI-failure signature (for Charge B), (c) curation/register
follow-ups. The *setless-orphan* pattern — coherent mechanic, no economy home — carries forward as
direct evidence for Charge D.

---

## 4. Charge B — functional KPIs (operationalize B)

The family definition rests on B, the fight-simulation behavior map, but left B a black box. Open it.

1. **What does the sim measure today?** Read the simulation seam (§0.2 item 5). Enumerate the outcome
   quantities it actually produces per kit/per fight (damage resolution, win/loss/timeout, HP curves,
   iteration counts, whatever the batch runner and balance loop emit). Ground this in the code, not in
   what you wish it measured.
2. **Propose a KPI vector = the coordinates of behavior-space S.** Candidate axes to evaluate (add,
   cut, replace): effective DPS; burst-vs-sustained ratio; time-to-kill distribution; effective HP /
   survivability; damage uptime (channel/cooldown/ramp time); range-band effectiveness; AoE-vs-single-
   target ratio; mobility/kiting; matchup win-rate spread (consistency vs rock-paper-scissors);
   skill-floor-vs-ceiling. Which are **orthogonal enough** to serve as real axes? Which are redundant?
   **Validate the set against labels:** a KPI set is only real if it *separates* the confirmed fibers
   (known-good) from the Charge-A genre-negatives (known-bad). If no KPI distinguishes Whirlwind from
   `d4-incinerate`, the set is not measuring what matters. This is the supervised check the sim alone
   cannot give you.
3. **Tie KPIs to the two questions B answers** (make this explicit — it is the synthesis):
   - *Identity/texture test:* coordinate c is identity-at-region-R iff perturbing c moves the KPI
     vector > ε. "Which KPI does each coordinate move?" is the operational form of the whole partition.
   - *Gap enumeration:* a gap is valuable iff its *predicted* KPI profile fills an under-served region
     of KPI-space. So gaps are not only Hamming-neighbors in *coordinate* space — they are **holes in
     *functional* space**. This is a deeper enumeration than the family analysis proposed; develop it.
4. **Feasibility, honestly.** Can the current sim produce these KPIs per kit? What is missing (the
   telemetry gaps; whether matchup spread is even computable; whether the phase-0 sim is trustworthy
   enough to be the oracle at all)? This feasibility verdict is direct evidence for Charge D's
   steelman #3.

**Deliverable for B:** a proposed KPI set with orthogonality analysis, the coordinate→KPI influence
map (even if hypothesized), and an honest sim-feasibility verdict naming what must be built.

---

## 5. Charge C — enumerate the gaps

Produce an actual, ranked list of predicted archetypes — the prize.

1. **Enumerate.** From the proxy-confirmed fibers (§2) plus the genuine families-of-one (Charge A.1),
   generate Hamming-1/2 neighbors in *identity*-space with **zero current members**. Do not enumerate
   the whole product space (astronomical, mostly void) — walk outward from populated families
   (germanium-next-to-silicon).
2. **Coherence filter — hold the tension the family analysis flagged.** Coherence is properly
   *sim-feasibility* (domain-membership of B), which may not be runnable yet. For a first pass, you may
   derive an inter-coordinate **constraint model** (forbidden pairs, e.g. `range=melee` ⊗
   `delivery=projectile`) from corpus co-occurrence — but **explicitly as a provisional prior for
   pruning obvious nonsense, NEVER as the definition of coherence** (corpus-absence conflates
   *forbidden* with *unclaimed*; that erases the gaps we value). State clearly which gaps you pruned as
   incoherent vs kept as unclaimed, and mark the whole coherence pass as pending sim-arbitration.
3. **Classify every surviving empty cell three ways, using Charge A's negatives:** *forbidden* (fails
   the constraint prior — void); *tried-and-rejected* (within Hamming-1/2 of a genre-negative failure-
   pattern — a **graveyard**; keep it but flag it red — building here means beating a documented
   failure, so the brief MUST name the specific fix the postmortem implies, e.g. "channel-flame works
   IF it is not movement-taxed"); *unclaimed* (neither — virgin territory, the true Mendeleev gap).
   Only the last is a clean prediction; graveyard cells are predictions *with a warning label* — and
   where Charge A step 4 found the failure was *extrinsic* (game-context, not intrinsic mechanics), our
   own systems may already supply the fix, promoting a red graveyard to an **amber opportunity**.
4. **Rank.** By (a) adjacency to a rich family; (b) functional novelty (the KPI-hole from Charge B);
   (c) design-value / player-fantasy fit; (d) **graveyard-discount** — down-rank tried-and-rejected
   cells unless the brief names a credible fix for the documented failure. Reconcile when these
   disagree.
5. **Output archetype briefs** for the top gaps: signature, nearest cousins, predicted KPI profile,
   the unclaimed / graveyard / amber-opportunity tag, and the one-line player pitch ("the X you know,
   but Y"). Genre-check each against what shipped ARPGs already have — a "gap" that Last Epoch quietly
   shipped last patch is not a gap.

**Deliverable for C:** the ranked gap list (tagged unclaimed / graveyard / amber-opportunity /
forbidden) + briefs for the top candidates, with the coherence caveat and, for any graveyard cell, the
fix its postmortem implies (or, for amber cells, the system of ours that supplies it).

---

## 6. Charge D — re-assess the direction, steelman the alternatives

The meta-charge, synthesizing A–C plus a wider project read (§0.2 item 6). **Wear DRIFT-CRITIC and
ELICITOR.** State the current bet plainly, then build the *strongest possible* case for each
alternative before judging. The failure mode is reflexive defense of the status quo — genuine
steelmanning must be able to *change* the direction.

**The current bet (state it precisely from the specs, do not strawman it):** "breadth is the pitch" →
a legible periodic table of combat kits → generated content spanning that archetype space,
differentiated by spirit-swap, delivered via the One Realm MVP. Is this bet sound?

**Alternatives to steelman (add your own; these are seeds, not a closed list):**
1. **Depth over breadth.** The genre's most-loved titles win on build *depth* (PoE/Last Epoch
   theorycrafting one archetype fifty ways; D3's loot/set treadmill on six classes), not archetype
   *breadth*. Steelman: pick 6–10 archetypes, make each infinitely deep. What would we gain/lose?
2. **The coordinate model is overfit / premature.** Maybe real identity is 4–5 coords and the other
   ~8 are baroque texture we are dignifying; the delivery×treatment=12 projection may already carry
   most legibility. Charge A's register-blindness finding is direct evidence — if the model cannot even
   express *why* a documented trap-skill is a trap, it is either missing a coordinate or dignifying
   noise.
3. **The sim cannot be the oracle.** The whole family definition rests on B. If the phase-0 sim cannot
   measure matchups or fun reliably (Charge B feasibility), maybe families should be defined by
   designer judgment + genre-recurrence and the sim dropped from the *definition* entirely. Cheaper,
   more honest — or a fatal loss of rigor?
4. **The periodic table is dev-facing vanity.** Players want "is my build fun," not a Mendeleev chart.
   Steelman moving the effort to the *playing* (Godot scene feel, spirit-swap moment-to-moment, demo
   polish) over the taxonomy.
5. **Gaps-as-predictions is a trap.** Empty cells may be empty because they are unfun — and now there
   is data: Charge A's 33 genre-negatives are documented failures (coherence ≠ fun; Grim Dawn's
   compossible-but-trap combos; D3's unused-until-itemized sets *are* the setless-orphan pattern).
   Steelman: build only proven-recurring families, ignore gaps. Counter to weigh honestly: the
   collision analysis (Charge A, step 4) shows some graveyards died from *game-context* (economy,
   mobility baseline), not intrinsic mechanics — which our systems might rescue. Which force wins?
6. **Generation is the wrong core.** Hand-authored content (Diablo/PoE model) is higher quality per
   unit; procedural archetype generation may solve a problem players do not have.

For each: strongest case → honest verdict (breaks the direction / refines it / fails). Then a single
integrated recommendation: **stay, refine, or pivot** — with the specific refinements or the specific
pivot, and the player consequence of each.

---

## 7. Deliverable

Write the analysis to `agentic_orchestration/gandalf/design-inputs/2026-07-13-gaps-kpis-direction-
analysis.md` (re-date the filename if the session runs on a later workstream day), covering Charges
A–D with their per-charge deliverables above. Keep member-count-thinking out of definitions and let it
back only as evidence. Report back with a tight summary (the full analysis lives in the file). End
with the Charge-D integrated recommendation (stay / refine / pivot) stated in one paragraph, because
that is the decision Matt will act on.
