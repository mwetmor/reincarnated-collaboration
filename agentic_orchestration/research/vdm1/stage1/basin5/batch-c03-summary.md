# VDM-1 basin-5 batch-c03 summary — Chronicon (chr-a, 8 kits)

**Crawl date:** 2026-07-18
**Domain order outcome:** chronicon.fandom.com → 402 (as canary warned); archive.org → blocked. Primary sources: steamcommunity.com (guides + discussions), smattymattyca.wordpress.com, steamah.com, earlyguides.com, steamdb.info patch-note snippets (403 on direct fetch; snippet text from search), rawg.io. Steam 429 rate-limit hit repeatedly; serialized with 5–15s waits.

---

## Per-kit one-liners

- **chr-arrow-storm-warden** — SOURCE_NOT_FOUND effective (skill names "Arrow Storm" unattested in all accessible text; Warden class confirmed as archer/nature class; Focus resource unconfirmed). Full dossier abstained.
- **chr-bee-warden** — SOURCE_NOT_FOUND effective (skill name "Bee Swarm" unattested; Warden confirmed as poison/nature/summoner class with pet capabilities; specific skill text absent). Full dossier abstained.
- **chr-bleed-berserker** — CONFIRMED across identity/mechanics/era. Bloodsoaked Garb set text directly attests Physical Damage + Bleed DoT engine. Era 1.0 August 2020 confirmed from patch notes. Dossier richly populated.
- **chr-bloodbinder-warlock** — CONTRADICTED on economy. Fetched guide states mana-stacking is the resource approach; claimed HP-drain/self-cost economy is not attested. Poison element (Living Blood) CONFIRMED. Dossier populated for attested facts.
- **chr-demon-legion-warlock** — Identity CONFIRMED (demon army, Demonologist tree, companion damage scaling). Mechanics UNSUPPORTED on shadow damage type specifically (shadow skulls mentioned but not tied to demon-summon damage in fetched text). Era 1.0 CONFIRMED. Dossier partially populated.
- **chr-fire-berserker** — CONFIRMED across identity/mechanics/era. Fire damage explicitly stated. Dragonfire Garb set text confirms fire explosions. Rage resource confirmed. Fire Avatar confirmed as optional ultimate (not sole identity skill).
- **chr-firestorm-warlock** — CONFIRMED across all families. Firestorm named skill confirmed. Sun+Moon cross-proc mechanic confirmed with verbatim mechanic text. Ritual of Souls + Soul Warp confirmed. DLC era confirmed. Richest dossier of the batch.
- **chr-frost-berserker** — CONFIRMED across identity/mechanics/era. Shattering Cold named skill confirmed. Freeze-then-shatter loop confirmed verbatim. Northern Rage set + Frostbound tree confirmed. Rage resource confirmed.

---

## Verdict histogram (ADVISORY — steward recounts from files)

| Verdict | Count |
|---|---|
| CONFIRMED | 17 |
| UNSUPPORTED | 7 |
| CONTRADICTED | 2 |
| SOURCE_NOT_FOUND | 0 (SNF-effective on 2 kits via UNSUPPORTED wall) |

Note: chr-arrow-storm-warden and chr-bee-warden returned UNSUPPORTED on all claim families because fandom 402 + archive blocked and Steam guides did not surface the specific skill names. These are functionally SNF-equivalent — see SNF section.

---

## Contradictions

1. **chr-bloodbinder-warlock / economy:** corpus claims "self-cost HP economy." Fetched guide ("The Brutal Bloodbinder") states "the good ol' mana stacking approach is the way to go" — no HP-drain mechanic described. Poison element is confirmed. CONTRADICTED on the self-cost/HP-drain economy claim specifically.

2. **chr-bloodbinder-warlock / mechanics (secondary):** corpus records "shield-absorb" as primary defense. Fetched guide identifies "mana stacking" as both offense and defense mechanism; no shield-absorb layer described. CONTRADICTED on primary defense characterization.

---

## SNF / thin-domain kits

**chr-arrow-storm-warden** and **chr-bee-warden**: skill names "Arrow Storm" and "Bee Swarm" do not appear in any accessible text. The Warden page on fandom is 402; archive is blocked; Steam discussions and guides discuss Storm Caller / Lightning / Nimbus / Vine Shot / Nature skills but not these exact names. This is consistent with the small-indie / thin-source expectation for Chronicon. Both kits are recorded with UNSUPPORTED verdicts and fully abstained dossiers. The Unattested Register is the deliverable.

SNF rate: 2/8 = 25% (below the 30% stop-grinding threshold).

---

## Dossier coverage

| Kit | Families populated | Families abstained | Coverage |
|---|---|---|---|
| chr-arrow-storm-warden | 0 | 6 | 0% |
| chr-bee-warden | 0 | 6 | 0% |
| chr-bleed-berserker | 5 | 1 (capstone) | 83% |
| chr-bloodbinder-warlock | 4 | 2 (geometry, full-skill-loop partial) | 67% |
| chr-demon-legion-warlock | 4 | 2 (capstone) | 67% |
| chr-fire-berserker | 5 | 1 (capstone) | 83% |
| chr-firestorm-warlock | 6 | 0 | 100% |
| chr-frost-berserker | 6 | 0 | 100% |

**Batch dossier coverage (non-SNF kits):** 30 populated / 36 possible = **83%**. Full batch (including SNF kits): 30/48 = **63%**.

---

## Element-attestation summary (per kit)

| Kit | Element attested | How attested | Anchor |
|---|---|---|---|
| chr-arrow-storm-warden | Physical — NOT ATTESTED | skill names absent; corpus records physical | no fetched source confirms "deals physical damage" |
| chr-bee-warden | Poison — NOT ATTESTED | skill names absent; Warden confirmed as poison-capable class | no fetched source attests "Bee Swarm deals poison damage" |
| chr-bleed-berserker | Physical + Bleed — ATTESTED | "+25% Physical Damage... Internal Hemorrhage dealing an additional 200% damage per second" | Bloodsoaked Garb set text; bleed IS the damage engine |
| chr-bloodbinder-warlock | Poison — ATTESTED | "summon slime-like creatures whenever an enemy is hit by a poison skill" | Living Blood proc trigger text directly names poison |
| chr-demon-legion-warlock | Shadow — PARTIAL (class-level) | "shadow and fire skulls are damage sources for Warlock builds" | shadow mentioned as a Warlock damage type but not tied to demon-summon hits specifically |
| chr-fire-berserker | Fire — ATTESTED | "enchanting priority – fire damage... This build creates huge explosions" + "Smoldering Stone rune... deals 300% of your fire damage" | Dragonfire Garb guide text |
| chr-firestorm-warlock | Fire — STRONGLY ATTESTED | "Firestorm spam... over 2000% fire damage increase... Fire Storm is explicitly identified as a fire skill" + Sun+Moon mechanic text | multiple independent guides |
| chr-frost-berserker | Cold/Frost — ATTESTED | "Frost Damage focused build... ice damage... Shattering Cold... Icebergs fists increases Shattering Cold damage... frost damage enchant priority" | Northern Rage guide text |

**Element law note:** Demon Legion shadow is recorded as partial-attested (class-level only; demon-hit text does not name shadow damage type explicitly from fetched sources). Mapper should treat as low-confidence shadow. All other element records are direct damage-descriptor attestations per the law.

---

## Author credits

- **smattymatty** (smattymattyca.wordpress.com): authored chr-fire-berserker (Dragon Storm build, July 2021) and chr-firestorm-warlock (Sun+Moon Deathbringer, March 2022).
- Remaining guides: anonymous/handle-unknown Steam community authors.

---

## Red flags

1. **Bloodbinder economy contradiction** (see above). The corpus self-cost/HP-drain claim is not supported by the most authoritative available guide. Possible sources: an earlier version of the build mechanic that was redesigned, OR a KB inference error about the "blood magic" flavor implying HP cost when the actual mechanic is mana-stacking. Elrond/steward should flag for review.

2. **Demon Legion shadow attestation is weak.** "Shadow skulls" and shadow as a Warlock damage type are attested at class level, but no guide text ties demon-summon attack damage specifically to shadow type. Could be fire (Infernal Demon fires fire-skull projectiles per the 1.0.0.5 guide). Downstream mapper should note uncertainty.

3. **Fire Avatar status.** Corpus records "fire-berserker" with folk name "Fire Avatar Berserker" implying Avatar is the identity skill. Fetched text shows Fire Avatar as one optional ultimate among fire builds; the Dragonfire Garb set is the actual load-bearing identity mechanism. Folk name may overstate Avatar centrality.

4. **Sun+Moon mechanic is cross-elemental.** The proc-chain is fire-amplifies-frost AND frost-amplifies-fire. The chr-firestorm-warlock record labels this as "fire" but the actual mechanic produces dual-element play. The firestorm-dominant variant does use fire as primary, but the Sun+Moon mechanic itself is a cross-trigger. Downstream mapper note.

5. **fandom 402 + archive blocked:** the two SNF kits (chr-arrow-storm-warden, chr-bee-warden) cannot be resolved without a live wiki source. No grind performed per brief instructions. These remain in the Unattested Register.
