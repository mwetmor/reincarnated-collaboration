# Dispatch — 2026-05-27 — legolas — Cycle 13 SC-4 Expansion (9-Category Surface Verification + Synergy Taxonomy + Degenerate-Pattern Catalog Research)

**From:** knight-rider
**To:** legolas
**Approved by:** Matt 2026-05-27 — Cycle 13 handoff doc § 4.1.4 (SC-4 expansion) + framing brief § 4.1 KR autonomous (sidecar dispatching) + Matt verbatim "Resume Wave 0 → Wave 1 dispatch sequencing"
**Estimated effort:** 6-12 hrs Mode A analytical research + synthesis
**Acceptance:** research note synthesizing 3 expansion topics; feeds Wave 1 partition intent verification (gandalf canonical doc 42) + Wave 2 T4 algorithm compositional synergy scan implementation (rocket) + Wave 4 sim degenerate-state detection methodology (gamora)

## Context

Original SC-4 (dispatched 2026-05-26; landed 2026-05-27 at `research/cycle-13/2026-05-27-arpg-modifier-partitioning-landscape.md`; 77KB) covered modifier-partitioning landscape across PoE2 / Last Epoch / Diablo 4 / Grim Dawn. Closeout § 10 SC-4 EXPANDED scope to ADD three new Mode A research dimensions surfaced by Pattern-B session 2026-05-27:

1. **9-category char sheet surface verification** — closeout § 3.1 LOCKED 9-category architecture (Damage / Defense / Resource / Crit / Speed / Resistance-Penetration / On-trigger / Build-identity / Utility-Meta-progression). Research: how do reference ARPGs (POST-training-data state — query latest patches/seasons) actually structure their stat sheet categorizations? Does the 9-category framework match real-world player-facing taxonomy OR amend?

2. **Synergy taxonomy** (per closeout § 2.5 compositional synergy scan) — research PoE/D4/LE community analysis on synergy keystones (PoE Awakened gem support gems, D4 Aspects + Tempering, LE Idol synergies). Specifically: how does the community categorize "good synergies" vs "degenerate synergies" vs "trap synergies"? What patterns surface for "tension-resolution" vs "theme-compound" vs "cross-chain composition" vs "element-gap fill" per closeout § 2.5 synergy opportunity patterns?

3. **Degenerate-pattern catalog research** (per closeout § 5.2 GAP 3) — closeout LOCKED 8-pattern v1 catalog (stunlock / zero-damage void / mandatory-skill-lock / permanent-CC / resource-starvation / degenerate-tank / bounce-CC / resource-overflow). Research: how do reference ARPGs detect + mitigate these patterns? What additional patterns surface in their literature/community analysis that v1 catalog may have missed?

This is Mode A analytical research (read-only literature/community/wiki sources). NO Mode B catalogue crawl. NO engine modifications.

## Required reading before starting

1. `agentic_orchestration/research/cycle-13/2026-05-27-arpg-modifier-partitioning-landscape.md` (YOUR prior SC-4 research; 77KB; baseline for this expansion; reuse sources)
2. `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 3 + § 5 (9-category char sheet lock + 8-pattern degenerate catalog source)
3. `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 2.5 (compositional synergy scan source)
4. `canonical/41-progression-framework-2026-05-27.md` (L50 hybrid framework context for stat sheet categorization)
5. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 3 + § 8 (capability toolkit + T4 algorithm context for synergy + degenerate-state context)
6. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #18 (methodology-before-execution) + #20 (robots.txt compliance) + #26 (Playability) + #30 (sim methodology naming)
7. `agentic_orchestration/operating-procedures/legolas.md` (Mode A research protocol)

## Math-before-code (Mode A research; no code)

NOT applicable — research synthesis only.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** Research note is design-input artifact; no schema / fixture / boundary mutation.

## Scope

For each of the 3 expansion topics:

### Topic 1 — 9-category char sheet surface verification

For PoE2 + Last Epoch + Diablo 4 + Grim Dawn:

- [ ] **Current stat sheet categorization** — what categories does each ARPG's stat sheet expose to players? (e.g., PoE2's "Offense / Defense / Misc"; D4's "Offense / Defense / Utility"; LE's "Offense / Defense / Resource / Other"; GD's "General / Combat Defense / Resists")
- [ ] **Category granularity comparison** — fewer than 9 vs 9 vs more than 9 categories per ARPG; what's the relationship between player-facing categorization vs underlying mechanic categorization?
- [ ] **Cross-ARPG comparison** — overlapping vs divergent categories; what's universal? what's variant?
- [ ] **Verification against 9-category lock** — does the 9-category framework (Damage / Defense / Resource / Crit / Speed / Resistance-Penetration / On-trigger / Build-identity / Utility-Meta-progression) match real-world player-facing taxonomy? Specifically:
  - Is splitting Damage from Crit standard practice? (or do most ARPGs fold Crit into Damage?)
  - Is Build-identity a distinct category in any ARPG, or is it folded into Utility / Misc?
  - Is Utility-Meta-progression (magic find / xp boost / currency drop) standard category? Where do ARPGs place these?
  - Is Resistance-Penetration distinct from Damage, or fold-in?
- [ ] **Recommendation** — does the 9-category lock match consensus practice, OR are there patterns from reference ARPGs that suggest amendment? Present neutrally; final decision is gandalf at doc 42 authoring.

### Topic 2 — Synergy taxonomy

For PoE2 + Last Epoch + Diablo 4 + Grim Dawn:

- [ ] **Community synergy categorization** — how does each ARPG's theorycrafting community categorize synergies? (e.g., PoE's "keystone synergies" vs "support gem chains"; D4 community's "Aspect synergies" + "Tempering bonus targeting"; LE's "Idol stacking patterns"; GD's "component + augment combos")
- [ ] **Synergy keystone exemplars** — list 5-10 examples per ARPG of widely-discussed "good synergies" (player-favorite designs)
- [ ] **"Degenerate synergy" exemplars** — list 3-5 examples per ARPG of synergies the community/devs identified as degenerate (overpowered, dominant, encouraged stale play patterns); how were they balanced?
- [ ] **"Trap synergy" exemplars** — list 3-5 examples per ARPG of synergies that LOOK powerful but underperform; what makes them traps?
- [ ] **Cross-ARPG taxonomy synthesis** — patterns that surface across all 4 ARPGs:
  - Tension-resolution synergies (one mechanic solves another's problem)
  - Theme-compound synergies (kit theme amplification)
  - Cross-chain composition synergies (parallel mechanic combination)
  - Element-gap fill synergies (coverage gap completion)
  - Any patterns NOT in closeout § 2.5 four-category framework?
- [ ] **"First-do-no-harm" pattern detection literature** — does any ARPG community analyze downstream-tension-creation (per closeout § 2.5 Pass 2 preserve)? Examples where a synergy resolved one tension but created another?
- [ ] **Recommendation** — does closeout 4-category synergy framework hold against real-world synergy taxonomy, OR are there additional patterns worth incorporating?

### Topic 3 — Degenerate-pattern catalog research

For PoE2 + Last Epoch + Diablo 4 + Grim Dawn:

- [ ] **Known degenerate patterns per ARPG** — list documented degenerate patterns each ARPG has historically dealt with (per dev blog posts, patch notes, community analysis); examples: PoE flicker strike pre-nerf; D4 trap rogue pre-3 sphere-of-pain; LE harmonic mages pre-tuning; GD blood knight broken combos
- [ ] **Detection methodology per ARPG** — how do developers detect degenerate patterns? (telemetry-driven? community-feedback-driven? sim-driven? play-testing?)
- [ ] **Mitigation pattern per ARPG** — what mechanisms are deployed to mitigate? (nerf the source mechanic; nerf the synergy; add counterplay mechanic; reshape the encounter)
- [ ] **Cross-ARPG pattern verification** — does the closeout 8-pattern v1 catalog cover the major patterns each ARPG has dealt with?
  1. Infinite stunlock (PoE freezing? D4 stunlock builds?)
  2. Zero-damage void (any ARPG analog?)
  3. Mandatory-skill-lock (PoE single-skill builds? LE single-archetype dominance?)
  4. Permanent-CC (D4 CC-heavy builds pre-balance?)
  5. Resource-starvation (any ARPG analog?)
  6. Degenerate-tank (LE tank builds with no damage? D4 indestructible tank?)
  7. Bounce-CC (any ARPG analog?)
  8. Resource-overflow (any ARPG analog?)
- [ ] **Additional patterns surfaced** — any degenerate patterns from reference ARPGs that v1 catalog may have missed? (e.g., dot-stack degenerate; movement-spam degenerate; etc.)
- [ ] **Recommendation** — does the 8-pattern catalog suffice for Cycle 13 v1, OR are there additions worth incorporating?

### Discipline #18 compliance + #20 robots.txt

- [ ] All sources verified for robots.txt permission per Discipline #20 (game wikis blocked ClaudeBot per prior SC-4; reuse permitted sources + verify new sources individually)
- [ ] Source citations per dimension (URL + access verification)
- [ ] Per Discipline #18: identify which findings inform PRE-Wave-1 decisions (gandalf doc 42 authoring) vs POST-Wave-1 decisions (rocket implementation; gamora SC-7 consultation). Flag both timing buckets explicitly.

## Acceptance criteria

- [ ] Research note authored at `agentic_orchestration/research/cycle-13/2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md` (companion to prior SC-4 research note)
- [ ] All 3 expansion topics covered across the per-ARPG dimensions
- [ ] Cross-ARPG synthesis per topic
- [ ] Source citations + robots.txt compliance per Discipline #20
- [ ] Timing classification per Discipline #18 (which findings inform Wave 1 vs Wave 2 vs Wave 4)
- [ ] NO Mode B catalogue crawl — analytical research only
- [ ] Round-trip: not applicable — no cross-seam contract change

## Out of scope (explicit non-goals)

- Mode B catalogue crawl
- Engine code modifications
- Substrate database modifications
- Recommendations beyond what each topic explicitly invites (present landscape neutrally)
- Re-researching base SC-4 territory (the 4-ARPG modifier-partitioning landscape) — that's already covered

## Open questions for the agent to resolve

- Source coverage: PoE2/LE/D4/GD priority order matches prior SC-4; if a new specialty source surfaces (e.g., GD community theorycrafting forum vs official GD wiki), prioritize per dimension
- Coverage-vs-depth tradeoff: 3 expansion topics across 4 ARPGs is significant scope; if any topic's depth requires sacrificing breadth elsewhere, prioritize what feeds Wave 1 first (Topic 1 9-category verification > Topic 2 synergy > Topic 3 degenerate-patterns)

## References

- `agentic_orchestration/research/cycle-13/2026-05-27-arpg-modifier-partitioning-landscape.md` (base SC-4 research)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 2.5 + § 3.1 + § 5.2
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-handoff-to-knight-rider.md` § 4.1.4
- `agentic_orchestration/operating-procedures/legolas.md` (Mode A protocol)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #18 + #20 + #26 + #30

---

**Cycle:** 13
**Wave:** 0 / Sidecar EXPANSION
**Gates:** feeds Wave 1 doc 42 verification + Wave 2 T4 synergy scan implementation + Wave 4 sim degenerate-state detection methodology
**Priority:** P2 — fire parallel with Wave 1 dispatch + SC-2 expansion + SC-6 audit

---

## Completion record

**Status:** COMPLETE
**Completed:** 2026-05-27
**Output:** `agentic_orchestration/research/cycle-13/2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md`
**robots.txt compliance:** verified — pathofexile.com, lastepoch.com, grimdawn.com all PERMITTED; game wikis accessed via WebSearch aggregate only (consistent with base SC-4 discipline)
**Discipline #18 timing classification:** Topic 1 = Wave-1-informing (doc 42); Topic 2 synergy framework = Wave-2-informing (rocket); Topic 3 degenerate-state methodology = Wave-4-informing (gamora SC-7)
