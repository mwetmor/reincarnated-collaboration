# VDM-1 basin-5 batch-c04 — Chronicon chr-b summary

**Batch:** c04 · game: chronicon · 8 kits  
**Crawl date:** 2026-07-18  
**Primary sources:** steamcommunity.com/app/375480 (guides + discussions), store.steampowered.com/app/2206120 (official Mechanist DLC page)  
**Domain canary:** chronicon.fandom.com → 402 confirmed. archive.org → blocked. Steam community is the sole live source tier.

---

## Per-kit one-liners

| kit_id | identity | mechanics | era | notes |
|---|---|---|---|---|
| chr-fulmination-templar | CONFIRMED | UNSUPPORTED | CONFIRMED | Skill names confirmed; proc-chain/WIS/Conviction detail absent from fetched text |
| chr-high-ranger-warden | CONFIRMED | CONFIRMED | CONFIRMED | Bleed DoT + High Ranger set fully attested |
| chr-mechanist-rocketeer | CONFIRMED | CONFIRMED | CONFIRMED | Fire attribute confirmed from official DLC page + Japanese guide |
| chr-mechanist-saw-master | CONFIRMED | CONFIRMED | CONFIRMED | Physical + chain-hop pattern confirmed |
| chr-mechanist-turret-drone | CONFIRMED | CONFIRMED | CONFIRMED | Holy element confirmed via Mechpriest tree + Holy Lance Turret attestation |
| chr-pet-warden | CONFIRMED | CONFIRMED | CONFIRMED | Physical damage confirmed; companion diversity confirmed |
| chr-plague-curse-warlock | CONFIRMED | CONFIRMED | UNSUPPORTED | Shadow damage attested; era DLC floor not explicitly confirmed in fetched text |
| chr-thorns-templar | CONFIRMED | CONFIRMED | CONFIRMED | Physical base attested verbatim; reflect + chain lightning variants confirmed |

---

## Verdict histogram (advisory — file truth is the count)

- CONFIRMED: 20
- UNSUPPORTED: 4  
- CONTRADICTED: 0
- SOURCE_NOT_FOUND: 0

**0 CONTRADICTED across the batch.**

---

## SNF kits

None. All 8 kits have at least one attesting source. Fulmination-templar mechanics are UNSUPPORTED (not SNF — identity+era confirmed).

---

## Dossier coverage

| kit_id | non-abstained families / 6 | abstained |
|---|---|---|
| chr-fulmination-templar | 3/6 (skill_loop, item_alterations, variants) | skill_geometry, capstone_alterations, author_credit |
| chr-high-ranger-warden | 4/6 (skill_loop, skill_geometry, item_alterations, variants) | capstone_alterations, author_credit |
| chr-mechanist-rocketeer | 4/6 (skill_loop, skill_geometry, item_alterations, variants) | capstone_alterations, author_credit |
| chr-mechanist-saw-master | 4/6 (skill_loop, skill_geometry, item_alterations, variants) | capstone_alterations, author_credit |
| chr-mechanist-turret-drone | 4/6 (skill_loop, skill_geometry, item_alterations, variants) | capstone_alterations, author_credit |
| chr-pet-warden | 5/6 (skill_loop, skill_geometry, item_alterations, capstone_alterations, variants) | author_credit |
| chr-plague-curse-warlock | 4/6 (skill_loop, skill_geometry, item_alterations, variants) | capstone_alterations, author_credit |
| chr-thorns-templar | 5/6 (skill_loop, skill_geometry, item_alterations, capstone_alterations, variants) | author_credit |

**Overall coverage: 33/48 families non-abstained = 69%. Author_credit universally abstained (no handles recovered from Steam community posts — authors unnamed). Capstone_alterations abstained 6/8 kits due to thin source depth.**

---

## Element-attestation summary (per-kit)

**chr-fulmination-templar — lightning (partial)**  
Evidence: build names "Fulmination Holy Reckoning" + "Fulmination War God"; fetched text mentions "holy damage boosting Lusombra's Boots" and "chain lightning" as Templar ability tree; build guides use "lightning" framing. Element label = lightning per elem_raw, attested via skill-set + community naming. NOT a verbatim "deals lightning damage" per-skill description — source-text level is name+community framing only. Downstream note: elem_raw=lightning is plausible; anchor is indirect.

**chr-high-ranger-warden — physical via bleed (attested)**  
Fetched text: "The main damage type is bleed ethereal damage." Physical is the underlying damage family for bleed in Chronicon. Element law: physical/bleed attested as damage-type descriptor. Engine has no physical family — element-silent for mapping.

**chr-mechanist-rocketeer — fire (STRONGLY attested)**  
Official Steam DLC page: "the fire Pyrotechnics ... skill trees." Japanese guide: "Rocketeer — Fire-based skill ... deals 'fire attribute' damage." Two independent sources confirm fire as damage-type descriptor. Cleanest element attestation in batch.

**chr-mechanist-saw-master — physical (attested)**  
Official Steam DLC page: "the physical Frontliner ... skill trees." Japanese guide: "Saw Master — Physical/bleed-focused skill ... dealing 'physical' damage." Confirmed. Engine has no physical family — element-silent for mapping.

**chr-mechanist-turret-drone — holy (STRONGLY attested)**  
Official Steam DLC page: "the holy Mechpriest skill trees." Japanese guide: "聖属性タレット『Stinger』" (holy attribute turret Stinger). Community: "Holy Lance Turrets ... Holy Drones ... probably single best skill this game has ever seen." Three independent source layers confirm holy. NOTE: DB mech_note flagged `HO elem = possibly 'holographic'` — RESOLVED: holy, not holographic. This is a red-flag correction (see below).

**chr-pet-warden — physical (attested)**  
Community: "All for One set for 2k+ percent physical damage." Physical is the pet damage baseline. Wolfcaster variant adds frost via wolf-Ice Shard link — that is a build-variant conversion, not the base kit element. Base kit: physical. Engine-silent for mapping.

**chr-plague-curse-warlock — shadow (attested)**  
Community: "a desecrators set with some defensive GR's and most things teched for shadow damage." Shadow Tree confirmed with skills (Life Reap, Sudden Death, Bone Spears etc.). Build described as "Poison/Frost/Shadow Warlock" as a distinct variant. Shadow attested as damage-type descriptor for the Desecrator/Plague Warlock kit. Poison also present but shadow is the elem_raw entry and is confirmed.

**chr-thorns-templar — physical base (STRONGLY attested, with lightning conversion variant)**  
Community verbatim: "Base Thorns element is physical (flat thorns * physical % * thorns %)." Lightning conversion via "Lightning Thorns" passive + Avenger ability also attested. Base element = physical. Engine-silent for mapping; Avenger conversion = separate downstream note.

---

## Contradictions

**NONE** — 0 contradictions across 8 kits.

**Notable correction (not a contradiction — internal DB inconsistency flagged for elrond):**  
`chr-mechanist-turret-drone` DB mech_note: "HO elem in old code = possibly 'holographic' in Chronicon's Mechanist context." Fetched text resolves this unambiguously as HOLY (three independent source layers). Elrond should update mech_note. This is an internal DB note inconsistency, not a verify contradiction (verdict is against fetched text, not DB fields).

---

## Red flags

1. **chr-mechanist-turret-drone holy/holographic** — DB mech_note uncertainty now resolved: element is holy, not holographic. Elrond correction warranted.
2. **chr-fulmination-templar mechanics UNSUPPORTED** — Proc-chain from melee hits, WIS attribute, Conviction resource are all probe-fact/kb-only claims. No fetched source text confirms these at verbatim level. Source-thin (fandom 402, Steam discussions reference external Imgur galleries). Downstream mapper should treat mechanics details as low-conf.
3. **chr-plague-curse-warlock era UNSUPPORTED** — Warlock Desecrator build is confirmed as DLC-associated (Desecrator set, DLC skills) by implication but no fetched text explicitly stamps the "ancient-beasts-dlc" era floor. Low risk — kit is clearly DLC content.
4. **Wolfcaster Pet Warden frost variant** — The Wolf Posse Wolfcaster build converts wolf/Ice Shard damage to frost ("almost all of our damage is frost damage"). This is a VARIANT of Pet Warden, not the base kit. elem_raw=physical is correct for the base Pet Zoo kit. Downstream mapper should be aware of frost conversion in the Wolfcaster sub-variant.

---

## Negative canon

All 8 kits have negative=0. Nothing emitted.
