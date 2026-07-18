# VDM-1 Basin-5 Batch c09 — Summary (vs c09, 11 kits)

**Batch:** c09 | **Game:** Vampire Survivors (vs) | **Date:** 2026-07-18  
**Source routed to:** vampire.survivors.wiki (fandom.com 402-blocked; wiki.gg mirror used per c08 canary)

---

## Per-kit one-liners

| kit_id | verdict summary | notes |
|---|---|---|
| vs-out-of-bounds-freeze | identity CONFIRMED, mechanics CONFIRMED, era UNSUPPORTED | Arcana XII — freeze→explosion; era vs-1.13-14-2025+ not attested from fetched dates |
| vs-phieraggi | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | Union weapon; rotating lasers; revive-scaling confirmed verbatim |
| vs-queen-sigma | identity CONFIRMED, mechanics CONFIRMED, era UNSUPPORTED | Patch 0.11.0 (Aug 2022); dlc-era label not attested |
| vs-red-death | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | Patch 0.2.12 Feb 2022; reaper-unlock + Death Spiral + 100% movespeed all confirmed |
| vs-runetracer-no-future | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | Patch 0.4.2 Apr 2022; bounce+explosion confirmed verbatim |
| vs-soul-eater | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | Jan 2022; aura-pulse + lifesteal confirmed; no element |
| vs-thousand-edge | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | Oct 2021; movement-direction aiming confirmed; individual daggers not beam confirmed |
| vs-thunder-loop | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | Patch 0.2.12 Feb 2022; double-hit confirmed; lightning damage type NOT attested |
| vs-unholy-vespers | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | Oct 2021; orbit confirmed; no holy/dark damage type attested |
| vs-vandalier | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | Jan 2022; union recipe confirmed; slot liberation confirmed verbatim |
| vs-vlad-dracula | identity CONFIRMED, mechanics CONFIRMED, era CONFIRMED | Ode to Castlevania DLC, Oct 2024; unlock condition confirmed; starting weapon Wine Glass (not "Dracula kit" generic) |

---

## Verdict histogram (advisory — steward recounts from files)

- CONFIRMED: 30
- UNSUPPORTED: 3 (vs-out-of-bounds-freeze era, vs-queen-sigma era, plus shock/stun riders on Thunder Loop not in fetched text)
- CONTRADICTED: 0
- SOURCE_NOT_FOUND: 0

---

## Contradictions

NONE. Zero contradictions across all 11 kits.

---

## SOURCE_NOT_FOUND kits

NONE. All 11 kits resolved from vampire.survivors.wiki.

---

## Dossier coverage

All 11 kits dossier'd. skill_loop, skill_geometry, item_alterations: all non-abstained (11/11 = 100% on these three families). capstone_alterations, author_credit: abstained all 11 (roguelite weapons have no mastery/aspect layer; wiki entries are communal/uncredited). variants: 1 non-abstained (vs-vlad-dracula alt skin); 10 abstained.

**Coverage % (non-abstained rows / total rows):** 33 non-abstained / 66 total = ~50% — expected for roguelite batch; capstone/author/variants are structural abstentions for this game class.

---

## Element-attestation summary (per kit)

| kit_id | element attested | anchor / note |
|---|---|---|
| vs-out-of-bounds-freeze | NONE | Explosion damage is physical; "freeze" is control not an element-family in VS |
| vs-phieraggi | NONE | "pure physical laser damage" — no elemental type stated |
| vs-queen-sigma | NONE | No elemental property stated |
| vs-red-death | NONE | No element stated |
| vs-runetracer-no-future | NONE | "pure physical (30 base damage)" — no elemental type |
| vs-soul-eater | NONE | No element stated; aura is physical |
| vs-thousand-edge | NONE | "physical knife damage" — no elemental type |
| vs-thunder-loop | NONE ATTESTED | Wiki uses "lightning strikes" and "lightning bolts" descriptively but provides NO formal lightning-damage-type classification in stats. ELEMENT LAW: name/visual language only → not attested. |
| vs-unholy-vespers | NONE ATTESTED | No holy or dark damage type in fetched text. Name-only rejection applies. |
| vs-vandalier | NONE | "standard projectile damage" — no element |
| vs-vlad-dracula | NONE | No element or damage type in fetched text |

**Element attestation: 0 of 11 kits carry a confirmed element.** Thunder Loop and Unholy Vespers were the two candidates per ELEMENT LAW — both rejected: Thunder Loop wiki uses "lightning" as description but never as a damage-type classifier in stats; Unholy Vespers has no holy/dark type stated. Correctly UNSUPPORTED per canary pattern.

---

## Rotation-shaped UNSUPPORTED kits

ALL 11 kits are rotation-shaped-UNSUPPORTED. Vampire Survivors weapons are auto-firing evolutions/unions with no player-directed skill rotation. The following deserve specific callout:

- **vs-out-of-bounds-freeze** — arcana passive modifier, not a rotation
- **vs-phieraggi** — auto-rotating beam union; no rotation
- **vs-queen-sigma** — character kit; passive scaling; no rotation
- **vs-red-death** — character kit; no rotation
- **vs-runetracer-no-future** — auto-fire bouncing projectile; no rotation
- **vs-soul-eater** — always-on aura; no rotation
- **vs-thousand-edge** — continuous auto-fire; no rotation (movement-direction aiming ≠ rotation)
- **vs-thunder-loop** — random sky-strike; no rotation
- **vs-unholy-vespers** — perpetual orbit; no rotation
- **vs-vandalier** — auto-fire bomb bird; no rotation
- **vs-vlad-dracula** — character kit; no rotation

---

## Red flags / steward notes

1. **vs-out-of-bounds-freeze era:** Era field is `vs-1.13-14-2025+` as ONLY era. Fetched text gives patch date 23 May 2022 (Patch 0.6.1) — arcana introduced well before 1.13. The era label appears to represent a post-cutoff review/relevance window, not introduction date. Steward should decide if this era record needs correction.

2. **vs-queen-sigma era:** Labeled `vs-dlc-era` but introduced in Patch 0.11.0 (18 August 2022) — before DLC era. "DLC era" label is misleading; wiki date is pre-DLC base game. Steward should flag for era correction.

3. **vs-vlad-dracula starting weapon:** DB records `core_skills: ["Dracula kit"]` (generic). Fetched wiki text is specific: starting weapon is **Wine Glass** (alt skin: Ebony Diabologue). This is a meaningful precision gap; downstream mapping should use Wine Glass.

4. **Thunder Loop / Unholy Vespers element:** Both rejected per ELEMENT LAW. Downstream mapper should note these as element-silent; no engine family assignment from this batch.

5. **vs-out-of-bounds-freeze mechanics note:** Wiki states arcana affects 14 weapons including DLC-specific ones. The `core_skills` field in DB lists `["Out of Bounds(arcana)", "Clock Lancet", "freeze weapons"]` — accurate but incomplete; 14-weapon scope is broader than recorded.

---

## Author credits

No authored guides used. All citations are communal wiki entries (vampire.survivors.wiki). No author_handle attested for any kit.

---

## Source routing note

vampire.survivors.wiki (wiki.gg mirror) = 11/11 coverage. fandom.com was skipped per c08 canary 402-block finding. No 404s except initial `/w/Vlad_Dracula` (corrected to `/w/Vlad_Tepes_Dracula` via search).
