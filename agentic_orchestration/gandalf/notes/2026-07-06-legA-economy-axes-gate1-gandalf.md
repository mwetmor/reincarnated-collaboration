# Gate-1 (design) — Leg A economy-axes math note

> **▶ ROLE: DRIFT-CRITIC — judging a build against a spec, and this is MY spec being operationalized.**
> **Verdict: RATIFY-WITH-CONDITIONS.**
> Reviewer: gandalf (design / player-experience / thematic dimension). Peer: jack-ryan (process / contract, parallel).
> Target: `reincarnated-engine/src/reincarnated/generation/notes/legA-economy-axes-math-2026-07-06.md` (rocket, 2026-07-06).
> Governing spec (mine): `canonical/reap-die-rise-engine/batch2-build-spec-2026-07-06.md` §2 Q1(a) / §3 caster-feel read / §5 provenance.
> Date: 2026-07-06.

---

## Frame — what I am checking

I authored the batch-2 spec. Q1(a) is a substrate-led ruling: *don't tune the caster — let the population
vote on what a viable mana economy is.* Leg A honors that ruling only if (a) the axes carve a space of
caster fantasies **worth having**, (b) the ranges let the population genuinely vote rather than smuggling my
bias in through range shape, (c) the Leg-B read is informative on GO **and** HALT, and (d) no viable region
is mechanically-valid-but-thematically-hollow. I judge all four PASS **with two binding conditions** — one of
which is load-bearing on substrate integrity, not just flavor.

---

## Charge 1 — Do the five identity regions map to caster fantasies worth having? PARTIALLY. Two of three STRUCTURAL economies are UNREACHABLE.

The five named regions (note §3) are real, legible caster fantasies and I endorse them as authored:

- **cheap-sustained** = the machine-gun mage (D3 Wizard channeled Disintegrate; PoE early cast-while-attacking
  spam). Real fantasy. Real pole.
- **builder/spender** = cast cheap primaries → land the expensive finisher, kills refund (D4 Sorc conjuration
  loops; the "kill feeds the next nuke" tempo). Real, and thematically the richest of the five.
- **flat-cost/attrition** = the baseline chassis, the known-failing center. Correctly the negative anchor.
- **warm-up/channeler** = slow-start-ramps-into-power. Real (Archon-windup feel; PoE Righteous Fire warmup).
- **glass-economy** = burns bright, burns out. Correct as a designed negative anchor.

**The problem is not what's IN the five — it's what the axes structurally CANNOT reach.** Resource economy is
not a free-form design space here; it is **BC Axis 5, a LOCKED substrate axis with seven bins**
(`qd-engine-bc-axes-lock-2026-05-20.md §3.8`). The batch-2 population Leg C emits is *the population the
faction library is derived from* (my spec §5 provenance law), and the faction library clusters on the eight
BC axes. So the economy axes must be legible **in Axis-5 bin space**, not merely in emitted-quantity space.
Mapping rocket's five regions onto the seven locked bins:

| Axis-5 bin (locked) | Detection | Reachable by rocket's axes? |
|---|---|---|
| **overflow** | mean ≥0.85 / no-cost | ✓ cheap-sustained |
| **generator-spender** | variance ≥0.20 (on-kill folds here) | ✓ builder/spender |
| **steady** | mid mean, low var | ✓ flat-cost/attrition |
| **starved** | mean ≤0.30 | ✓ glass-economy |
| **HP-economy** | >50% skill cost paid in HP (STRUCTURAL) | ✗ **unreachable** |
| **damage-taken-converts** | resource gained from incoming damage (STRUCTURAL) | ✗ **unreachable** |
| **charge-stack** | build-then-hold stack-cap mechanic (STRUCTURAL) | ✗ **unreachable** |

rocket's continuous levers (cost `c`, regen `r`, cadence `k`) span the **four STATISTICAL bins** cleanly —
those are exactly the bins detected by mean/variance, and a multiplier triple moves a kit's mean-resource-
fraction and variance around, so the population CAN vote across overflow / steady / generator-spender /
starved. That is genuinely good coverage of the statistical half of the axis.

But the **three STRUCTURAL bins are detected by cost-TYPE and mechanic, not by magnitude** — HP-as-cost,
damage→resource conversion, charge-cap-hold. No multiplier on a mana table can produce them. They are
different economies in KIND, not degree. This is not rocket's error — the dispatch scoped Leg A to *INT-band
mana kits*, and these three bins are (arguably) not INT-caster-native. **But it must be named as a bounded
claim, or the substrate reads a lie:** if Leg C emits only the four statistical economies and the faction
clustering later runs on all seven Axis-5 bins, three bins sit *empty for the entire caster population* — and
the clustering forms factions around economy-*absence* in exactly the way my spec §5 warns about ("a mixed
population forms clusters around axis-absence"). The caster half of the faction library would be
structurally incapable of ever producing a blood-mage, a rage-caster, or a charge-conjurer identity — not
because Matt ruled them out, but because the axis geometry silently foreclosed them.

**This is Condition 1.** It does not block Leg A. It requires the note (and the Leg-B read to Matt) to state
explicitly: *the economy axes cover the four statistical Axis-5 bins for INT-band kits; the three structural
bins (HP-economy, damage-taken-converts, charge-stack) are OUT OF SCOPE for batch-2 casters by construction,
and the caster region of the faction library will therefore be empty in those three bins — a scoped decision,
not a substrate finding.* Matt should see that foreclosure as a decision he's implicitly making, not discover
it as an emergent hole after the faction cut.

---

## Charge 2 — Q1(a) fidelity: does the population vote, or is bias smuggled through range SHAPE? PASS, with one asymmetry to flag.

The no-pre-bias invariant (§1.4) is genuinely honored and I want to be emphatic: **the default corner
reproduces the byte-verified known-failing chassis** (`c=1.0, s=flat, r=flat, RAMP=0, k=1.0` → identical
emitted tables), and the ranges span *outward from a failing center*. That is the correct structural-honesty
posture — the same discipline the calibration note earned my ratification for. The built-in refutation check
(§7 rule 4: any Leg-B run MUST reproduce 0.0 KPM at the default corner or the binding is wrong) is exactly
the right regression anchor. rocket did not bake a clear into the ranges. I checked for it and it isn't there.

**One asymmetry worth naming (not a bias, but a legibility caveat for the read):** the ranges are symmetric
in the *lever* (`c ∈ [0.60, 1.60]` symmetric-in-log about 1.0; `g_flat ∈ [0.60, 1.80]`), but they are NOT
symmetric in *KPM outcome*, because cost and regen act non-linearly on a bounded pool. rocket's own worked
numbers show this: at low `c` a T1 skill casts ~53× on the pool; at high `c` a T3 casts ~6.7×. The *viable*
region is likely to sit off-center toward the cheap/regen-rich corner, because that's where the pool stops
binding. That is not smuggled bias — it is the physics of the economy, and it is the RIGHT thing for the map
to reveal. But the Leg-B read must not report "the viable region is skewed toward cheap-sustained" as if it
were a discovered *preference*; it is partly a geometric consequence of a bounded pool. **Condition 2 (light):
the Leg-B report should present viable-region location in Axis-5 bin terms (which economy IDENTITY cleared),
not only in raw lever-coordinates (c, k, regen-mag), so Matt reads "generator-spender cleared, starved did
not" rather than "the clear lives near c=0.7" — the former is a caster-feel finding; the latter is a number.**

---

## Charge 3 — Is the caster-feel read informative on GO *and* HALT? YES, this is the note's strongest structural property.

My spec §3 requires the economy-identity read reported to Matt "either way." The note delivers this well:

- **On GO:** §3's region table + §6's LHS-within-6-strata scheme means the map surfaces WHICH identity region
  cleared, with marginal-axis gradients readable (Discipline #24, §4 confounded-pair audit = NONE). Matt
  learns not just "casters can be viable" but "casters are viable AS a builder/spender / as a machine-gun
  mage." That is a caster-feel finding, not a pass/fail bit.
- **On HALT:** §1.4 makes HALT genuinely informative — if no composition of the economy cube clears, the
  finding is "caster viability is blocked BELOW the economy layer" (cast mechanics / damage-vs-trash scaling),
  which is precisely gamora's Leg-4 warning promoted to a proven result. A HALT here is a *diagnosis*, not a
  dead end. That is the correct shape for my spec §3's HALT clause.

The LHS-over-grid choice (§6) is correct and I endorse it: a 384-cell grid at ~25/cell budget is infeasible
AND wastes samples in the glass-economy corner the region analysis already predicts is dead. LHS keeps
regen-shape in the search (rejecting the "hold regen flat" alternative), which is right — on_kill regen IS the
builder-spender hypothesis, and holding it flat would blind the pilot to the most interesting fantasy. Good.

**One condition on the read (Condition 3):** the six strata are `s(2) × r(3)`, with ~4 continuous-LHS points
each. At ~4 points/stratum the categorical shapes (escalating slope, on_kill, ramping) are thinly sampled. If
the pilot GOs, the caster-feel finding on WHICH shape cleared is a **low-confidence** read — the note
acknowledges this ("thin, but the pilot's job is coverage"). That's acceptable for a GO/HALT gate, but the
Leg-B report to Matt must **stamp the shape-finding as pilot-confidence, not established** — otherwise a
thinly-sampled "on_kill cleared" becomes a load-bearing caster-identity claim on 4 samples. The identity
finding is directional at pilot scale; densification is Leg C's job. Say so in the report.

---

## Charge 4 — Provenance / thematic coherence: does economy-as-axis fracture caster identity? Can a viable region be mechanically-valid-but-thematically-hollow? MOSTLY NO, one real risk.

**Economy-as-axis does NOT fracture caster identity — it CONSTITUTES it.** Resource economy is the caster's
combat verb. A machine-gun mage and a builder/spender are not the same class wearing different numbers; they
*play* differently at the hands. Making economy an axis the population votes on is the correct expression of
"let the substrate discover caster identities," and it composes cleanly with Leg-1's tree-content axes
(§4: disjoint emitted fields, no confound) and with the G4 proxy knob (§7 rule 3: proxy has no mana pool,
economy ⊥ G4). The provenance law (§5) is honored — only the Leg-C population votes; the pilot kits are
fixture bank. No integrity objection.

**The one real hollowness risk: the `ramping` / warm-up-channeler region.** `ramping` is NOT a distinct
Axis-5 bin — it is a within-fight regen *trajectory*, and at the fight's end it resolves into steady (if the
ramp paid off) or reads as starved-early-then-fine. A warm-up caster that clears the 240s window by
back-loading its KPM may be **mechanically valid (it clears) but thematically hollow at the substrate layer**:
it will bin as "steady" or "generator-spender" like everything else, so the *ramping fantasy* — the thing
that made it feel distinct at the hands — is invisible to the clustering. The player feels a warm-up caster;
the faction library sees a steady caster. This is the mirror of the calibration note's floor-reads-as-fantasy
problem: a mechanic that's legible in PLAY but illegible in the SUBSTRATE VECTOR. It's not a reason to cut
`ramping` from the axes — the *play feel* is real and worth searching — but the Leg-B read should note that
`ramping`'s identity does not survive into the Axis-5 bin, so if a warm-up caster clears, its faction-library
representation will not carry the warm-up signature. **This folds into Condition 1** (name what the substrate
can and cannot see about caster economy identity).

I checked the inverse — is any of the five regions mechanically-valid-but-thematically-EMPTY (clears but no
one wants to play it)? No. All five are fantasies with genre precedent. Even glass-economy, the expected
negative anchor, is a legible fantasy (players DO build glass cannons); its expected failure is a *balance*
result, not a fantasy void. Clean on that axis.

---

## Verdict: RATIFY-WITH-CONDITIONS

The math is honest, the no-pre-bias invariant holds, the HALT is genuinely informative, the sweep-isolation
is clean, and economy-as-axis is the correct expression of the Q1(a) substrate-led ruling. I ratify the axes
as authored. The conditions attach to the **Leg-B read and the note's scope statement**, not to the axis math
itself — none blocks Leg A from proceeding to jack-ryan's process gate and Matt's run authorization.

On the §5 cross-seam FINDING (the `resource_economy` loadout field, Route A vs B): that is jack-ryan's
process/contract lane, not mine. From the design chair I note only that **Route B (single `resource_economy`
dict) is also the design-correct choice** — it keeps the economy identity in ONE inspectable place, which is
what makes the Leg-B per-cohort read legible as caster-feel rather than reverse-engineered out of per-skill
cost values. Design and process concur on Route B; the contract mechanics are jack-ryan's to ratify.

### Design conditions (numbered)

1. **State the Axis-5 coverage boundary explicitly (binding on the note + the Leg-B report).** The economy
   axes reach the four STATISTICAL Axis-5 bins (overflow / steady / generator-spender / starved) for INT-band
   kits. The three STRUCTURAL bins (HP-economy, damage-taken-converts, charge-stack) are UNREACHABLE by a
   mana-multiplier triple and are OUT OF SCOPE for batch-2 casters by construction. The caster region of the
   faction library will therefore be EMPTY in those three bins. This must be named as a *scoped decision Matt
   is making*, not discovered as an emergent hole after the faction cut. Also name that `ramping`'s warm-up
   identity does not survive into the Axis-5 bin (Charge 4) — the substrate sees steady/generator-spender, not
   "warm-up caster."

2. **Report the viable region in Axis-5 IDENTITY terms, not only lever-coordinates (binding on the Leg-B
   report).** "Generator-spender cleared; starved did not" is a caster-feel finding; "the clear lives near
   c=0.7" is a number. Present the former. And flag that viable-region skew toward the cheap/regen-rich corner
   is partly bounded-pool physics, not a discovered player preference (Charge 2).

3. **Stamp the shape-finding as pilot-confidence (binding on the Leg-B report).** At ~4 continuous-LHS points
   per `s×r` stratum, the finding on WHICH categorical economy shape cleared is directional, not established.
   Do not let a thinly-sampled "on_kill cleared" become a load-bearing caster-identity claim; densification is
   Leg C's job (Charge 3).

## What I explicitly ENDORSE (not just permit)

- The no-pre-bias invariant (§1.4) + the default-corner refutation anchor (§7 rule 4). Structurally honest;
  the HALT stays a genuine outcome. This is the note's spine and it's sound.
- LHS-within-6-strata over a grid (§6), keeping regen-shape in the search. Correct sampling choice; it
  protects the builder/spender fantasy from being sampled out.
- Economy-as-axis as the constitution (not fracture) of caster identity. Making the population vote on the
  combat verb is the right reading of Q1(a).
- Route B as design-correct (concurring with rocket's recommendation; contract call is jack-ryan's).

**Signed:** gandalf, 2026-07-06 (Gate-1 design dimension; RATIFY-WITH-CONDITIONS; to critique pair alongside
jack-ryan process review). Build the axes honestly — but name the two of seven Axis-5 economies the casters
will never reach, so Matt rules the hole rather than inherits it.
