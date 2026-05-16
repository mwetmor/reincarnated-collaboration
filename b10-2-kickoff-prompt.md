# B10.2 kickoff — pack-proxy (Model C) + native swarm composition

You're a fresh Claude CLI session in ~/Games/reincarnated-engine/.
B10.1 closed last night (tag v1.3-b10-1-structure). B10.2 is the
next sub-block of B10 work.

## Read these first (in order)

1. `canonical/16-project-roadmap.md` — find the B10.2 row marked
   ACTIVE; gives top-line scope and estimate
2. `canonical/28-engine-arpg-rebalance-design.md` § B10 — V1 vs V2
   distinction, tier table, A3 gauntlet composition that just shipped
3. `design/b10-gauntlet-analysis.md` — full math analysis, especially
   § 11 (four learnings from B10.1 closure) which has a B10.2 action
   item: strengthen the loose `len(tiers_present) >= 2` assertion in
   test_gauntlet_is_tier_diverse
4. `design/decisions/decisions-log.md` — search for "B10" entries;
   D0–D5 sign-offs and the B10.1 closure entry are the decision trail
5. `design/working-agreement/engineering-disciplines.md` — all 12
   disciplines. Note: numbering shifted in B10.1 closeout (new #9 =
   test assertions from spec sources; old #9–11 → #10–12)

## B10.2 scope

Two sub-deliverables that ship together (one tag, one milestone):

**A. Pack-proxy (Model C) semantics**

Single-entity simulation approximation for swarm encounters. Instead
of simulating N individual swarm-tier monsters in a pack, simulate
one synthetic pack-proxy entity with:
- HP scaled by pack size N (linear or sub-linear — math-before-code)
- Damage output scaled by N (with possible crowding discount)
- Critical: AOE skills do proportional damage to the pack; single-
  target skills chip through pack HP one "unit" at a time

This is the partial-AOE signal V1 was chartered to deliver. The full
multi-actor simulation comes in V2 (sequential rooms with HP carryover).

**B. Native swarm composition rules**

Composition logic for what monsters appear in a pack. Decisions to
make (math-before-code):
- Pack size N (proposed range: 6-10 monsters per pack — verify
  against D2/PoE/Diablo IV genre conventions)
- Homogeneity (proposed: same element + same archetype within a
  pack, varying across packs)
- How many pack encounters appear in the gauntlet (replace some
  swarm slots? Add additional encounters?)

## Pre-implementation work (Discipline #1: math-before-code)

Before any code changes:

1. Pack size N: pick a number with rationale. Single-target classes
   should chew through a pack in ~N × single-target-time. AOE classes
   should clear in ~1-2 AOE pulses. Verify the differential is
   meaningful (>20% time delta between AOE and single-target).

2. HP scaling factor: linear (N × swarm-HP) is simplest. Sub-linear
   (sqrt(N) × swarm-HP) is more forgiving. Pick one with justification.

3. AOE multiplier: how does an AOE skill see a pack? Options:
   - Full damage to each pack-member (pack takes N × AOE damage)
   - AOE pulse damage applied N times to pack-proxy HP
   - Discount for "spillover" (AOE skills designed for groups get full
     value; AOE skills with small radius get partial)
   The right choice depends on what V1 should signal. Discuss before
   implementing.

4. Cost projection: does pack-proxy change simulation cost? Single
   entity per pack is cheaper than N entities, but if pack encounters
   are added on top of existing 12-monster gauntlet, total fights goes
   up. Update b10-gauntlet-analysis.md cost projection.

5. Tag intermediate state before implementation: v1.3-b10-2-pre-impl

## Queued micro-fix to fold in

From B10.1 closure learnings: `len(tiers_present) >= 2` in
`test_gauntlet_is_tier_diverse` is too loose. Strengthen for the
size==12 path specifically:
- Assert ≥4 distinct tiers present (matches A3 composition: trash,
  magic, elite, mini-boss, boss — boss is optional in small variants)
- Or assert specific per-tier counts (6 trash, 2 magic, 2 elite,
  1 mini-boss, 1 boss)
- Keep the loose assertion for the size!=12 fallback path

Land this either as the first commit in B10.2 or as a separate B10.1.1
micro-tag before B10.2 proper begins. Your call.

## Closing protocol

1. Tag `v1.3-b10-2-pack-proxy` once pack-proxy + swarm composition
   are in and tests pass
2. Update canonical/28 § B10 status from "V1 partial closure (B10.1)"
   to "V1 partial closure (B10.1 + B10.2)" with new section describing
   pack-proxy semantics
3. Update canonical/16 — B10.2 ✅ COMPLETE, B10.3 (if defined) or
   B10.4 (cost verification) → ACTIVE
4. Append to b10-gauntlet-analysis.md § 11 — what B10.2 surfaced
   (any unexpected findings worth queuing)
5. Update decisions-log.md with B10.2 closure entry
6. Push everything to origin/stage-a2
7. Report final state

## Engineering disciplines to apply (don't skip)

- #1 Math-before-code: pack size, HP scaling, AOE multiplier all
  decided before implementation
- #2 Smoke-test vs full regen: iterate on smoke (~2-3 min) until
  pack-proxy behaves; full regen at B10.4 only
- #4 Right tool: pack-proxy validation is a math + small-test
  question, not a full-season validation
- #5 Triage: blocking issues stop work; downstream-fixable goes to
  queue; known-issues get noted
- #9 (new) Test assertions from spec sources: the
  test_gauntlet_is_tier_diverse strengthening exemplifies this
- #10 Attribution clarity: any test changes co-locate with
  implementation changes
- #11 Empirical inspection over assumption: pack-proxy math is
  theoretical; verify empirically with small-scale tests
- #12 Semantic-shifting fixes need explicit framing: if pack-proxy
  changes how existing skills behave (e.g., AOE radius interpretation),
  call it out

## B10.4 reminder

When you get to B10.4 (cost verification — separate sub-block),
measure both full-regen wall time vs the 29-34 min B10.1 estimate
AND smoke-mode wall time vs the 2-3 min target. If smoke scaled
2.4× too, that's a knob worth knowing about.

## Out of scope

- B10 V2 (sequential rooms with HP carryover) — deferred per
  decisions-log
- Trial boss restructure — separate work block
- Gear in simulation — post-MVP, not part of B10
