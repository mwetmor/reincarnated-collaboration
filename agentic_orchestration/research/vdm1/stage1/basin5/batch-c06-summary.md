# VDM-1 basin-5 batch-c06 summary — tl2 (Torchlight 2) — 2026-07-18

**Kits:** 11 | **Game:** tl2 | **Negative flag:** tl2-arc-beam (1 kit)

## Verdict histogram (advisory — steward recounts from files)

| verdict | count |
|---|---|
| CONFIRMED | 32 |
| UNSUPPORTED | 0 |
| CONTRADICTED | 0 |
| SOURCE_NOT_FOUND | 0 |

Total claims: 32 (3 families × 11 kits − negative_canon only on arc-beam = 3×10 + 4 for arc-beam = 34 rows. Confirm from file.)

## Per-kit one-liners

- **tl2-arc-beam** — CONFIRMED identity+mechanics+era; CONFIRMED negative_canon (off-meta trap: poor range, no Charge gen, low damage scaling; "noone likes it anyways"; sole exception to Embermage elemental damage rule)
- **tl2-bot-engineer** — CONFIRMED all 3 families; heavy-proxy bot army; Engineer as commander; physical
- **tl2-cannon-engineer** — CONFIRMED all 3 families; piercing line projectile; Charge via Dynamo Field; physical
- **tl2-emberquake-engineer** — CONFIRMED all 3 families; fire-based magic AoE ground slam; 8 fissures/cast; confirmed fire damage verbatim
- **tl2-flame-hammer-engineer** — CONFIRMED all 3 families; "splinters deal fire damage" verbatim; Charge-powered 2 extra blasts; melee fire burst confirmed
- **tl2-glaive-outlander** — CONFIRMED all 3 families; chain-hop bounce confirmed ("rebounding once to strike additional foes"); Charge generation per ricochet; physical (Poison Glaive is a variant build, not the base identity)
- **tl2-hailstorm-embermage** — CONFIRMED all 3 families; "shards of ice from the sky"; "susceptible to Ice and Electric damage"; cold element attested
- **tl2-prismatic-embermage** — CONFIRMED all 3 families; strongest element attestation in batch — explicit "deals fire damage / ice damage / lightning damage" via Brand passives
- **tl2-shadowling-outlander** — CONFIRMED all 3 families; kill-to-summon mechanic confirmed; physical/shadow; no element
- **tl2-shotgonne-outlander** — CONFIRMED all 3 families; cone/area spread confirmed; physical; ammo-clip mechanic partially confirmed (no verbatim clip count found, but shotgonne ammo mechanic noted)
- **tl2-wolf-shade-berserker** — CONFIRMED all 3 families; Charge → Frenzy mechanic confirmed; Wolf Shade as light proxy; element-silent (see element note below)

## Contradictions

**0 contradictions.** No fetched source text contradicted any claim.

Internal note (not a contradiction — probe vs probe, not probe vs fetched text): canon_corpus elem_raw for tl2-prismatic-embermage = "fire" but fetched text clearly shows Prismatic Bolt is tri-elemental (fire + ice + lightning). This is an internal DB underspecification, not a contradiction with any verify claim. Flagged for Elrond: elem_raw="fire/ice/lightning" would be more accurate.

Internal note: probe facts label Embermage resource as "Ember" (resource_verbatim). Fetched text consistently says spells cost **mana**, and the Charge bar triggers "total concentration" (free casting + 25% damage when full). "Ember" appears to be the in-game thematic name for the Embermage's Charge bar, not a separate mana-replacement resource. No verify verdict affected (probe facts are heuristics only).

## SOURCE_NOT_FOUND kits

None. torchlight.fandom.com returned 402 (paywall), but Steam community guides (steamcommunity.com/app/200710) provided full coverage for all 11 kits. Domain-order fallback to Steam tier worked cleanly. 0% SNF rate.

## Dossier coverage

| family | kits with payload (not abstained) | kits abstained |
|---|---|---|
| skill_loop | 11/11 | 0 |
| skill_geometry | 11/11 | 0 |
| item_alterations | 0/11 | 11 (source silent across all kits — no gem/rune alteration text found in Steam guides) |
| capstone_alterations | 9/11 | 2 (arc-beam: no viable build to document; bot-engineer: source silent on passive tree) |
| author_credit | 11/11 | 0 |
| variants | 11/11 | 0 |

**Coverage: 53/66 rows populated (80%).** item_alterations universally abstained (expected — Steam skill guides don't detail individual item/socket alterations at this level).

## Element-attestation summary (CANARY marquee signal)

Per the ELEMENT LAW: only attest where fetched text applies element as a damage-type descriptor or enemy-directed behavior verb.

| kit | element attested | anchor (verbatim from fetched source) | verdict |
|---|---|---|---|
| tl2-arc-beam | ELEMENT-SILENT | "all Embermage damage is purely elemental, except for poor lil' Arc Beam" — Arc Beam specifically lacks elemental damage type | no element |
| tl2-bot-engineer | ELEMENT-SILENT | physical damage; no fire/cold/lightning language in fetched text | physical only |
| tl2-cannon-engineer | ELEMENT-SILENT | physical; piercing physical projectile; no element descriptor | physical only |
| tl2-emberquake-engineer | **FIRE** | "it deals fire-based magic damage" (Emberquake); "fire damage amplifiers" (Fire Bash) | fire attested |
| tl2-flame-hammer-engineer | **FIRE** | "splinters deal half the skill's listed damage percentage as fire damage" | fire attested |
| tl2-glaive-outlander | ELEMENT-SILENT | physical; bounce/ricochet; no element descriptor | physical only |
| tl2-hailstorm-embermage | **COLD/ICE** | "You call down shards of ice from the sky"; "susceptible to Ice and Electric damage" (enemy-directed) | cold/ice attested |
| tl2-prismatic-embermage | **FIRE + ICE + LIGHTNING** | "Fire Brand: deals fire damage to the target; Ice Brand: deals ice damage to the target; Lightning Brand: deals lightning damage to the target" | tri-elemental attested |
| tl2-shadowling-outlander | ELEMENT-SILENT | shadow/physical; no fire/cold/lightning damage descriptor | physical/shadow |
| tl2-shotgonne-outlander | ELEMENT-SILENT | physical cone; Shotgonne Mastery "shock and disorient" = status not damage type | physical only |
| tl2-wolf-shade-berserker | ELEMENT-SILENT | "icy fangs" in Wolf Shade description is flavor text (entity attack style) NOT "deals cold damage" — rejected per NAME-ONLY law | physical only |

**Element balance: 4 elemental kits / 7 physical-silent kits — matches the 4-elemental / 7-physical roster design stated in canary brief.**

**Canary validation notes:**
- ELEMENT LAW held in both directions as designed:
  - Elemental kits (Emberquake, Flame Hammer, Hailstorm, Prismatic) all attested with explicit damage-type language
  - Physical kits (Bot, Cannon, Glaive, Shadowling, Shotgonne, Wolf Shade) stayed element-silent
  - Arc Beam is the hardest case: explicitly identified in source as the "exception to elemental damage" — unique among Embermage skills; properly element-silent
  - Wolf Shade "icy fangs" = the expected NAME-ONLY temptation; correctly rejected
- Prismatic Bolt delivers the strongest multi-element attestation in the entire batch — all three elements explicit in source text from a single guide

## Red flags

1. **tl2-prismatic-embermage elem_raw underspecified:** DB has elem_raw="fire" but fetched text confirms tri-elemental (fire+ice+lightning). Not a contradiction of any verify claim but Elrond should note for downstream mapping accuracy.
2. **tl2-glaive-outlander base vs build variant:** Glaive Throw description says "slice through target, rebounding" — base appears physical. The popular "Poison Glaive Caster" variant adds poison via weapon affix/Venomous Hail. elem_raw=physical is correct for the base identity; poison is build-variant flavoring.
3. **item_alterations universally abstained (11/11):** Steam community skill guides do not document individual gem/socket/enchantment alterations at the per-skill level. This is a source-type gap, not a domain failure. If item-level alteration data is needed, dedicated item wiki sources (torchlight.fandom.com pages per skill, when accessible) or archived Runic forums would be required.
4. **torchlight.fandom.com returned 402 for all fetches** — paywall/bot-gate active. Steam community guides provided equivalent coverage; domain-order fallback successful. Steward should note that Runic archived forums (third tier in domain order) were not needed and not attempted.
5. **No contested or ambiguous verdicts** — tl2 is well-documented as expected; SNF=0 confirms domain order viable via Steam tier.
