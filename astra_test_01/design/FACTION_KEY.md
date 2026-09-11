# Four-faction visual key

Recorded: 2026-09-10.

Status: user-agreed working faction labels for the next character, equipment,
environment, and VFX test suite. Names may be refined through visual review.
The source-game associations below are internal reference notes, not names or
text to put into the game.

## The key

### F01 — The Last Vigil

- Inspiration: Diablo II.
- Identity: weathered defenders pursuing an ancient evil.
- Character and gear vocabulary: practical silhouettes, worn iron, leather,
  sacred relics, and ritual objects.
- Stronghold vocabulary: fortified camps, candlelit sanctuaries, crypts, and
  blackened timber.
- Working motive: hold back or destroy the ancient evil they remember.

### F02 — The Unbound

- Inspiration: Path of Exile 1.
- Identity: outcasts seeking power and passage beyond their imprisonment.
- Character and gear vocabulary: scavenged equipment developing into
  extravagant finery, forbidden artifacts, and unsettling relics.
- Stronghold vocabulary: ruined temples, repurposed ancient structures, and
  impossible maps or passages.
- Working motive: reach or understand the being or place beyond their world.

### F03 — The Iron Remnant

- Inspiration: Grim Dawn.
- Identity: survivors reclaiming a world occupied by supernatural forces.
- Character and gear vocabulary: firearms, heavy coats, military remnants,
  alchemical equipment, and improvised protection.
- Stronghold vocabulary: barricades, battered industrial structures, and
  settlements under siege or occupation.
- Working motive: recover their home from supernatural invaders.

### F04 — The Keepers of Hours

- Inspiration: Last Epoch.
- Identity: rival inheritors of a broken history, each believing they know what
  must be restored.
- Character and gear vocabulary: ceremonial armor, arcane instruments, and
  deliberate ornamental geometry.
- Stronghold vocabulary: monumental stonework and fractured observatories.
- Working motive: restore the version of history they believe should survive.

These motives and visual vocabularies are starting briefs, not finished lore or
visually qualified designs. PoE2 remains an optional additional reference; no
fifth faction or final placement has been agreed.

## What the latest discussion establishes

- Four coherent groups draw inspiration from game/era traditions. Build
  categories and elements vary within each faction; neither determines faction
  membership in this proposed test-suite direction.
- Characters, equipment, and strongholds must read as related within a faction.
  All four factions must also feel intentionally part of one game.
- Use shared camera, grounding, rendering, lighting-response, motion-quality,
  and combat-readability rules. Exact values and visual anchors remain to be
  selected together with the user.
- Different historical characters can meet in the same location. An act or zone
  need not correspond one-to-one with a source game or character's origin.
- Preserve individual character identity within faction identity. Recoloring
  the same ensemble does not establish roster distinctiveness.
- Starting ARPG clothing and complete uncovered heads/faces/hair are required.
  Helmet visibility must be separable from whether a helmet is equipped.
- The production ambition is 100+ characters, three progression tiers per
  character, and approximately 50 additional uniques. Whether starter clothing
  is included in those tiers, and whether uniques are items or complete sets,
  remains unresolved; do not treat 350 as a certified asset count.
- The 24 active VFX archetypes remain reusable across characters and appropriate
  monsters, with element and stylistic variations. Archetype behavior and
  element meaning must survive those variations.

## Scope and relationship to existing documents

This records the current conversation for the new test-suite design. It does
not rewrite game canon, migrate faction AI, choose a production renderer, or
change the literal ASTRA TEST 01 acceptance criteria.

- [Original ASTRA test](../../codex-3d-modeling/ASTRA%20TEST%2001%20painted%20character%20vfx.md)
  remains the fixed contract for the existing runs.
- [Archive frame](../../canonical/reap-die-rise-story/archive-frame.md) currently
  specifies five element courts and other earlier geography rules. Reconcile
  the new four-faction direction explicitly before implementing game allegiance
  or territory behavior.
- [Style register](../../canonical/reap-die-rise-story/style-register.md)
  specifies the existing stylized 3D game presentation. The painted ASTRA
  experiment has not by itself replaced that production choice.
- [Ensemble specification](../../canonical/reap-die-rise-game/ensemble-asset-pipeline-spec.md)
  supplies reusable construction and certification ideas. Its always-covered
  head assumption is superseded for this test suite by the user's exposed-head
  requirement; its two-mesh band ladder is not proof of three distinct gear sets.
- [VFX binding specification](../../agentic_orchestration/gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md)
  is sealed despite its filename. Preserve its 24 active bindings, layer rules,
  and explicitly held cases.

## Immediate visual proof to prepare

One board per faction, pairing representative people, starter clothing, advanced
gear, a stronghold, and VFX. Then one mixed-faction scene under shared lighting.
Use those concrete comparisons to agree the shared style and faction differences
before scaling animation or writing production-specific rendering assumptions.

The ten-character validation batch must represent all four factions. Exact
roster allocation, gear coverage, monster fixtures, performance targets, and
acceptance thresholds belong in the forthcoming test-suite architecture.
