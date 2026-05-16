# Research — Vendor Discovery Sweep (2D VFX, Step B Precursor) — 2026-05-16

**Mode:** A (analytical)
**Commissioner:** knight-rider (per gandalf commission `2026-05-16-step-b-tier1-2dvfx-crawl-commission.md`)
**Approved by:** Matt (Day-4 dialogue, Q1)
**Sources consulted:** itch.io vendor pages (direct fetch), itch.io tag browse pages, GameDevMarket search results
**Cross-check baseline:** `2026-05-16-pixijs-compatible-2d-vfx-libraries.md`

---

## Baseline exclusion list (vendors already in existing research file — NOT duplicated here)

pimen / ansimuz / Pipoya / Foozle / Brackeys VFX Bundle / CreativeKind / unTied Games / Elthen's Pixel Art Shop / ppeldo / LuizMelo / OpenGameArt.org / CraftPix.net

**Note on Frostwindz:** The existing research file lists Frostwindz as a single-pack lightning vendor ("Frostwindz — Pixel Art VFX Lightning (free)"). The sweep found Frostwindz has a substantially broader catalogue spanning death/necrotic, blood, dark-magic, arcane, and cosmic substrates across 10+ paid packs — the existing entry materially under-represents this vendor. Frostwindz is therefore included below as a net-new candidate on substrate-breadth grounds; it is NOT a duplicate of the lightning-only entry.

---

## Candidates Surfaced

### Vendor: Frostwindz (full catalogue — beyond the lightning-only entry in baseline)

- **Primary URL:** https://frostwindz.itch.io
- **Distribution platform:** itch.io
- **Distinctness signal:** Ships class-archetype VFX packs under substrate labels absent from Pimen's 9: Deathbringer (death/necrotic/dark), Blood Knight (blood/life-drain), Dark Mage (dark arcane), Warlock (void-adjacent arcane), Starcaller (cosmic/celestial). Each pack is a discrete substrate cluster with 6 hand-crafted animations. Kinetic coverage also present (Warrior, Paladin, Rogue slash/impact packs).
- **Element / mechanic coverage observed:** death/necrotic (Deathbringer), blood/bleed/life-drain (Blood Knight), dark-arcane (Dark Mage), fire (Fire Mage), frost (Frost Knight), holy/divine (Priest, Paladin), void-adjacent-arcane (Warlock), cosmic/stellar (Starcaller), plus kinetic slash/impact packs (Warrior, Blood Knight melee animations). Lightning pack already in baseline.
- **Register:** pixel-art; canvas sizes 128x128 and 192x128 (narrative-pixel band, larger than Pimen's 32x64 primary tier). Sub-register: hand-drawn-pixel signals visible from preview GIFs; layered PSD files ship with paid packs indicating per-layer construction.
- **Cost structure:** paid; $6.50 per individual class pack; $39.00 for bundle of 13 packs. Free preview versions available for several packs.
- **License:** "Can be used in personal and commercial projects. You can modify the assets. Credit not required. Redistribution or resale not allowed." Confirmed on Deathbringer and Blood Knight pack pages directly.
- **AI-content signals:** "No generative AI was used" — confirmed on both fetched pack pages.
- **Recommendation for Step B inclusion:** YES — ships death/necrotic, blood/life-drain, and cosmic substrate labels not present in Pimen's 9; kinetic class packs add weapon-strike coverage; commercial license confirmed; active creator with 13-pack bundle depth.

---

### Vendor: Pixogen (AFGameAssets)

- **Primary URL:** https://pixogenassets.itch.io/pixel-art-rpg-vfx
- **Distribution platform:** itch.io (primary); also listed on GameDevMarket
- **Distinctness signal:** Explicitly labels "Void" as a discrete element category (8 Void animations: Shield, Portal, Black Hole, Slash, Spin, 2 Explosions, Ball) — distinct from Pimen's "Dark" substrate. Also ships "Technology" VFX (8 effects) which has no parallel in Pimen's catalogue; plus "Attack Slash" variants (8) as a dedicated kinetic-VFX category alongside 8 elemental categories.
- **Element / mechanic coverage observed:** Water, Fire, Wind, Earth, Void (distinct label), Holy, Electric, Ice — 8 primary elemental categories — plus Technology (novel), Fireworks, Explosions, Attack Slash (kinetic). 636 total sprites across 108 animations; 64x64 canvas.
- **Register:** pixel-art; 64x64 per-frame canvas; described as "hand-drawn sprites." Consistent with hd2d-pixel band.
- **Cost structure:** paid; €19.99 for full pack; free Lite version available. Mega Pack (€59.99) bundles full RPG asset suite.
- **License:** "License of AFGameAssets" (downloadable 18 kB file — full terms not fetchable from pack page). License file must be inspected at crawl time. No runtime/redistribut statement available from page metadata.
- **AI-content signals:** "No generative AI was used" — confirmed on pack page tag.
- **Recommendation for Step B inclusion:** YES with caveat — "Void" label is a genuine substrate distinction from Pimen's "Dark"; Technology and Attack Slash add novel coverage. Caveat: license terms not fully verifiable from public page (requires download of license file); resolve at Step B crawl time. Canvas-size consistency (all 64x64) simplifies Pixi.js wiring relative to Frostwindz's larger canvases.

---

### Vendor: Fellor (BitBlast Studio)

- **Primary URL:** https://fellor.itch.io
- **Distribution platform:** itch.io
- **Distinctness signal:** Ships "Poison" and "Crystal" as discrete substrate-level VFX categories. Poison is addressed by Pimen's Acid pack but under a different label/palette register; Crystal is a novel substrate (gem/mineral magical resonance) not present in Pimen's 9 or the existing research file's Tier 1-3 vocabulary. Also ships Smoke (atmospheric kinetic substrate). Packs are compact (8 effects each, 64x64) — low file overhead, easy to evaluate.
- **Element / mechanic coverage observed:** Crystal (8 effects; novel — magical-gem/arcane-mineral aesthetic), Poison (8 effects; 64x64), Ice, Earth, Lightning, Fire, Smoke. Bundle includes Black Knight character animations (kinetic coverage, out-of-scope for this track). Seven distinct VFX substrate packs confirmed.
- **Register:** pixel-art; 64x64 consistent canvas with 32x32 crystal elements. "No generative AI" confirmed. Single-person creator (21-year-old pixel art animator, 2+ years experience).
- **Cost structure:** paid; $2.27-$3.50 per individual pack; $10.40 Collector Pack (35% discount). Low per-pack cost.
- **License:** "Free for personal and commercial use. Redistribution or resale not allowed. Credit optional." Confirmed on Poison and Crystal pack pages directly.
- **AI-content signals:** "No generative AI was used" — confirmed on both fetched pack pages.
- **Recommendation for Step B inclusion:** YES with caveat — Crystal substrate is a genuine novelty; Poison adds palette-register variation from Pimen's Acid. Caveat: creator is relatively new (2 years experience); pack depth is 8 effects per substrate vs Pimen's 10-22; frame counts are lower. Quality floor uncertain — visual inspection required at Step B sample phase.

---

### Vendor: CodeManu

- **Primary URL:** https://codemanu.itch.io
- **Distribution platform:** itch.io
- **Distinctness signal:** Kinetic-VFX specialist. Offers 44 impact/hit FX animations (100x100px) and a separate Blood Effects Vol.1 pack — blood/wound as a standalone substrate. The impact/hit pack is the deepest single-vendor kinetic-VFX catalogue found in the sweep: 44 animations with Pixel FX Designer source files included. No elemental substrate claims; pure kinetic-VFX identity.
- **Element / mechanic coverage observed:** Impact/hit effects (44 animations; 100x100px); Blood Effects Vol.1 (blood/wound substrate; pack page returned 404 during fetch — count and canvas unconfirmed); Free VFX Asset Pack (miscellaneous). No elemental substrates. Kinetic-VFX-only catalogue.
- **Register:** pixel-art; 100x100px canvas for impact pack (wider than standard 64x64; note for Pixi.js atlas strategy). Format: PNG spritesheets.
- **Cost structure:** paid; $4.95 per pack. Also bundled in GameDev Mega Bundle ($39.95 for 32 packs).
- **License:** "Use for personal and commercial purposes. No credit required." Confirmed on impact pack page.
- **AI-content signals:** "No generative AI was used" — confirmed on impact pack page.
- **Recommendation for Step B inclusion:** YES with caveat — best kinetic-VFX depth found in the sweep (44 impact/hit animations); fills the weapon-strike/hit-spark gap Pimen only partially covers. Caveat: 100x100px canvas may require atlas padding review (Drax track flag); Blood Effects Vol.1 pack page returned 404 — confirm availability at Step B time.

---

## Candidates Investigated and Excluded

The following vendors were investigated during the sweep and did NOT meet all five inclusion criteria:

**BDragon1727** — High-volume itch.io creator with 100+ packs (750 Effects Pack, 1050 RPG Effects, shader series). Excluded: no novel substrate tags detected; primarily general explosion/bullet/impact pixel effects; no AI-content statement on vendor page (flags provenance uncertainty). Would add quantity-within-existing-tags, not substrate variance.

**Dajeki** — Excluded: creator page explicitly includes "AI Generated Dark Battlers" pack — AI-content-default vendor.

**Sentient Dream Studio** — Investigated via Dajeki collection (Poison Attacks mini-pack, Holy Effects Pack 01). Excluded: pack page returned 404; unable to verify license terms, AI provenance, or format details. Cannot confirm inclusion criteria. Flag for manual check if another source surfaces this vendor.

**kiddoink / Hoolami / RagnaPixel** — Slash specialists surfaced on itch.io tag browse. Excluded: thin catalogues (1-3 packs each); no AI-provenance statements observable; substrate coverage limited to generic slash with minor elemental variants. Below the vendor-depth threshold for Step B inclusion.

**Pipoya** — Already in baseline (Time Magic, Warp Portal, HEX Shield, Light Pillar series). Not a net-new candidate.

---

## Summary findings

**Total net-new vendor candidates:** 4 (Frostwindz full catalogue, Pixogen, Fellor, CodeManu)

**Substrate gaps addressed:**

| Substrate gap | Addressed by |
|---|---|
| Death / necrotic / decay | Frostwindz (Deathbringer pack) |
| Blood / life-drain / bleed | Frostwindz (Blood Knight), CodeManu (Blood Effects Vol.1 — unconfirmed) |
| Void (distinct from Dark) | Pixogen (explicit Void element category: Black Hole, Portal, Shield, Slash) |
| Cosmic / stellar / celestial | Frostwindz (Starcaller pack) |
| Crystal / gem-arcane | Fellor (Crystal VFX Pack) |
| Kinetic-VFX depth (44 impact/hit animations) | CodeManu (Impact & Hit FX Animations) |
| Technology VFX | Pixogen (8 Technology effects — novel; no parallel in existing research) |
| Dark-arcane / Warlock-class | Frostwindz (Dark Mage, Warlock packs) |

**Substrate gaps NOT addressed by this sweep (confirmed absent or below threshold):**

| Gap | Finding |
|---|---|
| Psychic / mental / dream VFX | No specialist vendor found. Single icon packs exist (Confused / Charmed in Elthen's status pack, already in baseline) but no VFX-quality dedicated psychic substrate vendor. |
| Aether as distinct substrate label | Not found as a standalone vendor category. Closest is Pixogen's Technology or Frostwindz's Starcaller. |
| Dedicated weapon-trail (animated trail behind weapon arc) | No specialist found beyond Frostwindz's class-based slash packs and kiddoink's thin catalogue. |

---

## Knowledge gaps not resolved

- Frostwindz Starcaller, Warlock, and Paladin paid pack pages returned 404 during fetch — likely URL slug differences. Substrate claims for these packs are inferred from the vendor profile page listing, not direct pack-page verification. Confirm at Step B crawl time.
- Sentient Dream Studio pack pages returned 404. Vendor may have moved or taken packs down. Cannot verify inclusion criteria.
- CodeManu Blood Effects Vol.1 pack page returned 404. Availability uncertain.
- Pixogen license file (18 kB download) not publicly readable from pack page — full terms require file download. Treat as "license unclear" until Step B crawl time.
- No Bluesky / Mastodon indie creator accounts surfaced through web search. Social-platform search returned itch.io aggregator results rather than creator profiles. This search vector was not productive via web search tools alone; a manual social-platform browse would be required to exhaust it.

---

## Source list

- https://pixogenassets.itch.io/pixel-art-rpg-vfx (fetched 2026-05-16)
- https://pixogenassets.itch.io (fetched 2026-05-16)
- https://fellor.itch.io/poison-vfx-pack (fetched 2026-05-16)
- https://fellor.itch.io/crystal-vfx-pack (fetched 2026-05-16)
- https://fellor.itch.io (fetched 2026-05-16)
- https://frostwindz.itch.io (fetched 2026-05-16)
- https://frostwindz.itch.io/pixel-art-spells-vfx-deathbringer (fetched 2026-05-16)
- https://frostwindz.itch.io/pixel-art-blood-knight-vfx (fetched 2026-05-16)
- https://frostwindz.itch.io/pixel-art-vfx-dark-mage (fetched 2026-05-16)
- https://codemanu.itch.io/impacthit-fx-animations (fetched 2026-05-16)
- https://codemanu.itch.io (fetched 2026-05-16)
- https://elthen.itch.io/2d-pixel-art-status-effect-sprites (fetched 2026-05-16)
- https://elthen.itch.io (fetched 2026-05-16)
- https://sanctumpixel.itch.io/hit-effect-pixel-art (fetched 2026-05-16)
- https://bdragon1727.itch.io (fetched 2026-05-16)
- https://pimen.itch.io/wood-spell-effect (fetched 2026-05-16)
- https://itch.io/game-assets/tag-pixel-art/tag-slash (fetched 2026-05-16)
- https://itch.io/game-assets/tag-pixel-art/tag-void (fetched 2026-05-16)
- https://itch.io/c/1124621/pixel-art-fx (fetched 2026-05-16)
- https://dajeki.itch.io (fetched 2026-05-16)
- Web searches: itch.io pixel art VFX tag searches (necrotic/decay/poison, void/arcane/aether, slash/weapon-trail, stagger/stun/knockback, social platforms, GameDevMarket) — 6 queries, 2026-05-16

---

— legolas, 2026-05-16
