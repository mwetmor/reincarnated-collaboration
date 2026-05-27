# Dispatch — 2026-05-26 — legolas — Cycle 13 SC-4 ARPG Modifier Partitioning Landscape Research (Mode A)

**From:** knight-rider
**To:** legolas
**Approved by:** Matt 2026-05-26 (via Cycle 13 framing brief Q4 ratification + KR kicker authorization)
**Estimated effort:** 4-8 hrs research + synthesis
**Acceptance:** research note synthesizing modifier-partitioning landscape across 4 reference ARPGs; feeds Wave 1 partition design cycle inputs

## Context

Cycle 13 Wave 1 = stat-sheet partition design cycle (early Cycle 13 milestone per framing brief § 3). The partition cycle is a math hotspot per Discipline #18 — gandalf design intent + gamora methodology consultation + rocket implementation + jack-ryan critique converge on operationalizing doc 40 § 3 spec-driven gear gen + § 3.6 7-item partition scope (modifier surface enumeration / per-slot partition / per-slot probability / node-count + chain-distribution math / weapon damage spec / non-weapon baseline stats / main_weapon routing cleanup).

Per Discipline #18 (methodology-before-execution at math hotspots), this dispatch fires BEFORE Wave 1 specialist execution. Goal: ground the partition design in proven ARPG modifier-partitioning patterns. NOT to copy-paste; to inform design space.

This is Mode A analytical research (read-only literature/community/wiki sources). NOT Mode B catalogue crawl. NOT engine-side modifications.

## Required reading before starting

1. `canonical/00-ground-state.md` — current epoch (Epoch 4 + Cycle 13 architectural foundation)
2. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` §§ 3 + 3.6 + 5 (spec-driven gear gen + partition cycle 7-item scope + capability toolkit)
3. `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 0.5 (content lifecycle dependency chain — sim CONSUMES, doesn't generate)
4. `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-framing-brief.md` § 3 Wave 1 + § 5 SC-4 (this dispatch's authority basis)
5. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #18 (methodology-before-execution) + #20 (robots.txt compliance)

## Math-before-code (Mode A research; no code)

NOT applicable — research synthesis only. No engine modifications.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** Output is a research note consumed at design time by gandalf + gamora + rocket + jack-ryan; no schema / fixture / boundary change.

## Scope

For each of the 4 reference ARPGs below, document modifier-partitioning architecture across these dimensions:

### Reference ARPGs (priority order)

1. **Path of Exile 2** (current state of art for modifier-pool-driven gear generation)
2. **Last Epoch** (idol affix system + tiered affix progression; closest architectural cousin to doc 40 spec-driven gen)
3. **Diablo 4** (sacred/ancestral/uber-unique tier escalation; aspect+affix architecture)
4. **Grim Dawn** (prefix/suffix + component augment system)

### Per-ARPG dimensions to document

For each ARPG:

- [ ] **Modifier surface enumeration**: full taxonomy of modifier types the system supports (damage mods / defense mods / resource mods / on-trigger mods / stat mods / proc mods / etc.). Count + categories.
- [ ] **Per-slot partition design**: which gear slots roll which modifier types. Slot-restriction logic. Mod-pool definitions per slot.
- [ ] **Per-slot probability distribution**: how mod weighting works (item-level requirements, tier weighting, mod-tag-based filtering). How probability changes with item rarity / item level / influence / etc.
- [ ] **Rarity escalation pattern**: how rarity (magic/rare/legendary etc.) affects modifier surface — does rarity unlock new mod types, or only roll more affixes from existing pool?
- [ ] **Legendary / unique architecture**: how special items are designed differently from random rolls (handcrafted vs procedural; fixed mod pool vs unique mod surface; tier system within legendaries)
- [ ] **Set item architecture** (where applicable): set bonus structure (2pc/4pc/6pc), set affinity mechanics, set-specific affix pools
- [ ] **Triggered / proc modifier surface**: how "X on hit / X on crit / X on kill" type modifiers are partitioned (separate pool vs integrated)
- [ ] **Skill-modifying modifier surface**: how modifiers that grant or alter skills are partitioned (e.g., "+1 to lightning skills"; "added cold damage to attacks")
- [ ] **Crafting / modification surface**: how player-side modifier manipulation works (orbs, fragments, idols, etc.) — informs spec-driven gen by showing the "modifier alphabet"
- [ ] **Notable architectural lessons**: what works / what fails per ARPG (community-known pain points; design lessons that informed sequels)

### Synthesis dimensions (cross-ARPG)

- [ ] **Modifier-surface size**: how many distinct modifier TYPES does each ARPG expose? (Diablo 4 vs PoE2 vs Last Epoch vs Grim Dawn — order of magnitude)
- [ ] **Per-slot mod-pool size**: typical mod-pool size per slot (5? 20? 100?)
- [ ] **Rarity-escalation pattern taxonomy**: across the 4 ARPGs, how many distinct escalation patterns exist? (rarity-unlocks-new-types vs rarity-rolls-more-affixes vs rarity-affects-magnitude-only)
- [ ] **Legendary architecture taxonomy**: how many distinct legendary architectures exist? (fixed-roll vs constrained-random vs unique-affix-pool)
- [ ] **Probability-distribution archetypes**: weighting mechanisms (flat vs item-level-weighted vs tag-based vs tier-cascaded)
- [ ] **Capability-toolkit precedents**: what existing ARPG modifier surfaces map to doc 40 capability toolkit categories (multiplicative / mechanic-adjusting / spatial-adjusting / axis-adjusting / added-skill)?

### Discipline #18 compliance

- [ ] Identify which dimensions the partition cycle MUST decide vs MAY defer to first-cycle calibration. Be explicit: "PoE2 mod-tag-based weighting requires upfront tag schema; can't be deferred"; "magnitude calibration can iterate empirically."
- [ ] Flag any partition decisions where a single methodology choice has multi-week downstream cost (these need explicit Wave 1 design lock before partition fires).

## Acceptance criteria

- [ ] Research note authored at `agentic_orchestration/research/cycle-13/2026-05-26-arpg-modifier-partitioning-landscape.md`
- [ ] All 4 ARPGs covered across all 10 per-ARPG dimensions (Mode A read-only sources: official wikis, community references, design retrospectives by developers, well-cited theorycrafting docs)
- [ ] Synthesis section completes 6 cross-ARPG dimensions
- [ ] Discipline #18 compliance section flags methodology choice gates explicitly
- [ ] Source citations per dimension (URL or doc-title + author); robots.txt compliance per Discipline #20
- [ ] **NO Mode B catalogue crawl** — analytical research only
- [ ] Round-trip: not applicable — no cross-seam contract change

## Out of scope (explicit non-goals)

- Mode B catalogue crawl (no scraping; no data extraction at scale)
- Engine code modifications
- Substrate database modifications
- Catalogue DB modifications
- Recommendations for which ARPG pattern to adopt (recommend only IF research surfaces a clear pareto-dominant choice; otherwise present landscape neutrally — design decisions land in Wave 1 partition cycle)
- Coverage beyond 4 reference ARPGs (Diablo 2 / PoE 1 / Wolcen / Torchlight / etc. mentioned only IF informative for a specific dimension)

## Open questions for the agent to resolve

- Best-source-per-dimension: which sources are authoritative for each dimension? (e.g., PoE2 official wiki vs path-of-building reference vs developer blog post)
- Source-stability: any source citations that may rot (community wikis can change); flag in note
- Coverage-completeness vs depth tradeoff: prioritize covering all 4 ARPGs at sufficient depth over exhaustive coverage of any single ARPG

## References

- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 3 (spec-driven gear gen) + § 3.6 (7-item partition scope)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 0.5 (content lifecycle dependency chain)
- `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-framing-brief.md` § 3 Wave 1 + § 5 SC-4
- `agentic_orchestration/operating-procedures/legolas.md` (Mode A research protocol)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #18 + #20

---

**Cycle:** 13
**Wave:** 0 / Sidecar
**Gates:** Wave 1 partition cycle (must land before Wave 1 design lock)
**Priority:** P1 — fire first

---

## Completion record

**Completed:** 2026-05-27
**Output:** `agentic_orchestration/research/cycle-13/2026-05-27-arpg-modifier-partitioning-landscape.md`
**robots.txt compliance (Discipline #20):** All four game wikis (poewiki.net, lastepoch.wiki.gg, diablo4.wiki.gg, grimdawn.wiki.gg) block ClaudeBot. Research routed to official game sites (pathofexile.com, lastepoch.com, grimdawn.com — all permitted) and secondary sources verified individually.
**Round-trip:** Not applicable — research note only; no cross-seam contract change.
**Notes for Wave 1 partition design:**
- All 4 ARPGs covered across all 10 per-ARPG dimensions.
- Synthesis section covers all 6 cross-ARPG dimensions.
- Discipline #18 compliance section explicitly flags 5 MUST-DECIDE gates + MAY-DEFER items.
- Key finding: mechanic-adjusting, spatial-adjusting, and axis-adjusting modifiers are exclusively legendary/unique surfaces in ALL 4 reference ARPGs — never in the random rare pool. This directly grounds doc 40 capability-toolkit placement decisions.
- Key finding: prefix/suffix binary is load-bearing schema decision that must precede individual modifier assignments.
- Key finding: proc/trigger routing decision (gear pool vs separate system vs support gem) is the highest-leverage partition gate — determines whether gear slot pools are simple or complex.
