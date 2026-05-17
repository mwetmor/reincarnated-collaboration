# D19 — VFX Library Extension Plan (Planning Phase)

**Authored:** 2026-05-17 by drax-loadout (Track B, hive-mind phase-1-p1)
**Status:** PLANNING COMPLETE — implementation BLOCKED on Matt vendor acquisitions (CraftPix premium, Fellor Crystal, Frostwindz Deathbringer)
**Scope:** Planning only. No production code modified. No vendor packs acquired.
**Authority:** Phase-1 P1 hive-mind distributed L1 (drax in-seam); D19 scope per `scope-of-work-phase-1-p1.md` § 1.5
**Companion docs:**
- `scope-of-work-phase-1-p1.md` § 1.5 (D19 definition)
- `canonical/story/substrate-expansion-decision-2026-05-17.md` (substrate set + cosmology integration)
- `canonical/story/substrate-identity-declarations-2026-05-17.md` (7 declarations; iconic_register + cosmological_commitment)
- `canonical/story/style-register.md` (HD-2D pixel-art register; VFX conformance requirement)
- `agentic_orchestration/CHANGELOG.md` 2026-05-17 vendor-acquisitions entry
- `agentic_orchestration/research/knowledge/vfx-to-pool-expansion-opportunities-2026-05-17.md` (legolas reverse audit; READY-TO-FIRE; SHIPPED)

---

## § 1 — Per-Substrate VFX Coverage Matrix

**Methodology:** On-disk inventory sourced from `reincarnated-demo/public/assets/` (the demo's actual asset tree). Catalogue-only entries sourced from legolas reverse audit § 4 and per-vendor JSONL files. HD-2D conformance from style-register.md locked register: hand-drawn-pixel-art at pixel resolution; pimen "derived_register": "hand-drawn-pixel" is register-verified.

### § 1.1 — Fire

**On-disk VFX assets:**

| Vendor | Pack | Path | Asset type | Animation count | HD-2D register |
|---|---|---|---|---|---|
| Pimen | Fire Spell Effect 3 | `pimen/fire-spell-effect-3/` | Spell VFX | 9 animation groups (Barrier, Fire Beam, Fire Bite, Fire Claw/Slashes, Fire combo, Fire Shield, Hit Effect, Extras) | HD-2D-conformant (metadata confirmed: `derived_register: hand-drawn-pixel`) |
| CreativeKind | Fire_attack | `CreativeKind/Fire_attack/` | Character attack VFX | sprite-sheet-based; not extracted/inspected | HD-2D-conformant (CreativeKind is the canonical hand-drawn-pixel vendor) |
| CreativeKind | Fire_Elemental_Creativekind | `CreativeKind/Fire_Elemental_Creativekind/` | Character sprite | entity-as-VFX-anchor | HD-2D-conformant |
| CreativeKind | Fire_Lord_Creativkind | `CreativeKind/Fire_Lord_Creativkind/` | Boss sprite (fire register) | entity | HD-2D-conformant |
| Chierit Elementals bundle | fire_knight (zip) | `Elementals_bundle/Elementals_fire_knight_FULL_v1.1.zip` | Character sprite (UNEXTRACTED) | n/a — zip only | HD-2D-conformant (chierit per per-slug doc) |

**Catalogue-only (not on-disk):**
- Pimen Fire Spell Effect series beyond v3 (packs 1, 2 exist in catalogue; only v3 on-disk)

**Gap assessment:** Fire coverage is STRONG. Multiple packs on-disk across spell VFX (pimen) + character sprite (CreativeKind + chierit). No blocking gap for fire-substrate demo rendering. The chierit fire_knight ZIP is unextracted — extraction needed before integration but content is present.

**Visual register confidence:** HD-2D-conformant across all on-disk fire assets.

---

### § 1.2 — Water

**On-disk VFX assets:**

| Vendor | Pack | Path | Asset type | Animation count | HD-2D register |
|---|---|---|---|---|---|
| Pimen | Water Spell Effect 03 | `pimen/water-spell-effect-03/` | Spell VFX | 7 animation groups (Water Beam, Water Burst, Water Combo, Water hit effect, Water Magic Circle, + 2 more) | HD-2D-conformant |
| Pimen | Ice Spell Effect 02 | `pimen/ice-spell-effect-02/` | Spell VFX (water-flex/cold) | 0 raw animations listed — likely zip/rar format inside | Status UNKNOWN (may be unextracted archive) |
| Chierit Elementals bundle | water_priestess (zip) | `Elementals_bundle/Elementals_water_priestess_FULL_v1.1.zip` | Character sprite (UNEXTRACTED) | n/a | HD-2D-conformant |

**Catalogue-only (not on-disk):** Pimen ice-spell-effect series (v1, v3 — catalogue shows v1 and v3; only v2 on-disk at ice-spell-effect-02). Fellor frost/ice packs (catalogue; not on-disk). Frostwindz ice packs (catalogue; not on-disk).

**Gap assessment:** Water/cold VFX coverage is ADEQUATE but not deep. The ice-spell-effect-02 pack exists on-disk but may be an unextracted archive (raw/ shows 0 animations). Wiring needed. Water character sprite (chierit water_priestess) exists as ZIP — unextracted. No blocking gap, but ice-spell-effect-02 extraction status should be verified at implementation time.

**Visual register confidence:** HD-2D-conformant for pimen packs; chierit pending extraction.

---

### § 1.3 — Earth

**On-disk VFX assets:**

| Vendor | Pack | Path | Asset type | Animation count | HD-2D register |
|---|---|---|---|---|---|
| Pimen | Earth Spell Effect 03 | `pimen/earth-spell-effect-03/` | Spell VFX | 11 animation groups (Boulder, Earth Burst, Earth Hammer, Earth Mine, Earth Spike, Earth Trap 1, Earth Trap 2, Extra Earth Elemental, Hit Effect, Impale, Petrify) | HD-2D-conformant |
| CreativeKind | Crystal_golem_creativekind | `CreativeKind/Crystal_golem_creativekind/` | Monster sprite (earth/crystal sub-register) | entity | HD-2D-conformant |
| CreativeKind | Crystal_Wisp_Creativekind | `CreativeKind/Crystal_Wisp_Creativekind/` | Monster sprite | entity | HD-2D-conformant |
| Chierit Elementals bundle | ground_monk (zip) | `Elementals_bundle/Elementals_ground_monk_FULL_v1.3.zip` | Character sprite (UNEXTRACTED) | n/a | HD-2D-conformant |
| Chierit Elementals bundle | crystal_mauler (zip) | `Elementals_bundle/Elementals_Crystal_Mauler_Full_v1.0.zip` | Character sprite (UNEXTRACTED) | n/a | HD-2D-conformant |
| Chierit Elementals bundle | leaf_ranger (zip) | `Elementals_bundle/Elementals_Leaf_ranger_Full_v1.0.zip` | Character sprite (UNEXTRACTED) | n/a | HD-2D-conformant |
| Chierit Elementals bundle | metal_bladekeeper (zip) | `Elementals_bundle/Elementals_metal_bladekeeper_FULL_v1.1.zip` | Character sprite (earth-metal sub-register; UNEXTRACTED) | n/a | HD-2D-conformant |

**Catalogue-only (not on-disk; pending Matt acquisition):**
- CraftPix premium wood-nature pack (earth biological-organic VFX) — PENDING ACQUISITION
- Fellor Crystal gem cluster pack — PENDING ACQUISITION

**Gap assessment:** Earth VFX coverage is GOOD on spell VFX (pimen earth-spell-effect-03 is the richest pack on-disk: 11 animation groups). Character sprite coverage is STRONG in chierit ZIPs (ground_monk, crystal_mauler, leaf_ranger, metal_bladekeeper) pending extraction. The biological-organic VFX gap (root/bark/leaf/petal/vine/moss per CHANGELOG) is real — earth's biological sub-register has no on-disk VFX pack equivalent. This gap is addressed by the CraftPix premium wood-nature acquisition (pending). Earth is NOT blocked for fire-through-water range combat demos; the biological-organic VFX gap matters for plant/root/vine skill effects specifically.

**Visual register confidence:** HD-2D-conformant for pimen + CreativeKind. Chierit pending extraction.

---

### § 1.4 — Wind

**On-disk VFX assets:**

| Vendor | Pack | Path | Asset type | Animation count | HD-2D register |
|---|---|---|---|---|---|
| Pimen | Wind Spell Effect 03 | `pimen/wind-spell-effect-03/` | Spell VFX | 12 animation groups (Air attack, Extras, Hit Effects, Multi Slashes, Projectile 1, Projectile 2, + more) | HD-2D-conformant |
| Chierit Elementals bundle | wind_hashashin (zip) | `Elementals_bundle/elementals_wind_hashashin_FULL_v1.1.zip` | Character sprite (UNEXTRACTED) | n/a | HD-2D-conformant |

**Catalogue-only (not on-disk):** CraftPix Top-Down Wind and Lightning VFX (catalogue entry; would serve wind + lightning dual-substrate coverage). Pimen wind series beyond v3.

**Gap assessment:** Wind VFX coverage is ADEQUATE for smoke-test demos. The pimen wind-spell-effect-03 is on-disk with 12 animation groups (strongest animation count of the four canonical packs). Character sprite (chierit wind_hashashin) is present as ZIP. No blocking gap.

**Visual register confidence:** HD-2D-conformant.

---

### § 1.5 — Lightning

**On-disk VFX assets:**

| Vendor | Pack | Path | Asset type | Animation count | HD-2D register |
|---|---|---|---|---|---|
| Pimen | Thunder Spell Effect 03 | `pimen/thunder-spell-effect-03/` | Spell VFX (lightning) | 11 raw animation categories (Burst, Electric bow, Electric Disc, Electric Explosion, Electric Trap, Hit Effect x4 variants, Shield, Thunder Ball, Thunder Bullet, Thunder Whip, Thunder Spell Circle) — 30+ w/ blur/without blur variants per metadata | HD-2D-conformant (metadata confirmed: `derived_register: hand-drawn-pixel`) |
| CreativeKind | God_of_Lightning_Dark_Version | `CreativeKind/God_of_Lightning_Dark_Version_Creativekind/` | Monster sprite (lightning/dark palette) | entity | HD-2D-conformant |
| CreativeKind | God_of_Lightning_Light_Version | `CreativeKind/God_of_Lightning_Light_Version_Creativekind/` | Monster sprite (lightning/light palette) | entity | HD-2D-conformant |
| CreativeKind | Lightning_horizontal | `CreativeKind/Lightning_horizontal/` | VFX animation (lightning bolt horizontal) | animation | HD-2D-conformant |
| CreativeKind | Lightning_vertical | `CreativeKind/Lightning_vertical/` | VFX animation (lightning bolt vertical) | animation | HD-2D-conformant |
| CreativeKind | Lich_Creativekind | `CreativeKind/Lich_Creativekind/` | Monster sprite (includes Lightning palette variant) | entity (5 color palettes including Lightning) | HD-2D-conformant |
| Chierit Elementals bundle | lightning_ronin (zip) | `Elementals_bundle/Elementals_lightning_ronin_full_v1.0.zip` | Character sprite (UNEXTRACTED) | n/a | HD-2D-conformant |

**Catalogue-only (not on-disk):** Fellor Lightning VFX Pack (catalogue; not on-disk — confirmed by catalogue JSONL, no fellor directory in public/assets). Pixogen electric-bolt (catalogue; Pixogen Lite is on-disk at `PixelArtRPGVFXLite/` — see below). Ansimuz electric-explosion (catalogue only).

**On-disk Pixogen note:** `PixelArtRPGVFXLite/` exists on-disk at `public/assets/PixelArtRPGVFXLite/` but contains only `License.txt`, `ReadMe.txt`, and `Textures/` directory. The Pixogen Lite pack is present but may be retro-register (per style-register.md, Pixogen is higher-resolution than retro but not the primary HD-2D target). The Pixogen Full pack (Path-A acquisition per CHANGELOG) would supplement lightning + void coverage.

**Gap assessment:** Lightning is surprisingly WELL-COVERED for a not-yet-active substrate. Pimen thunder-spell-effect-03 is on-disk with ~30 animation variants (the richest single VFX pack on-disk by animation count — 30 blur/no-blur pairs across 11 animation categories). CreativeKind has God_of_Lightning (two palette versions) + dedicated Lightning_horizontal + Lightning_vertical VFX + Lich with lightning palette. Chierit lightning_ronin is present as ZIP. **Lightning is the most VFX-ready of the three new substrates.** No additional VFX acquisition required for lightning; the Fellor pack would add depth but is not blocking.

**Visual register confidence:** HD-2D-conformant across all pimen + CreativeKind assets. Chierit pending extraction. Pixogen Lite register TBD (likely retro-adjacent rather than HD-2D; see Note below).

**NOTE:** Pimen's "Thunder Spell Effect 03" covers the lightning substrate despite the "thunder" pack name. The pack slug `thunder-spell-effect-03` contains explicitly `Electric bow`, `Electric Disc`, `Electric Explosion`, `Electric Trap`, `Thunder Ball`, `Thunder Bullet`, `Thunder Burst`, `Thunder Whip` animations — these are lightning/electric VFX animations semantically. The name mismatch (thunder vs lightning substrate) does not affect usability; the VFX content is lightning-coherent per the substrate-identity-declarations `iconic_verbs: [arcs, chains, discharges, leaps to, stuns, flashes, strikes, courses through]`.

---

### § 1.6 — Holy

**On-disk VFX assets:**

| Vendor | Pack | Path | Asset type | Animation count | HD-2D register |
|---|---|---|---|---|---|
| CreativeKind | Angel_Guardian_Creativekind | `CreativeKind/Angel_Guardian_Creativekind/` | Character sprite (holy/light sub-register) | entity | HD-2D-conformant |
| CreativeKind | Angel_Mage_Creativekind | `CreativeKind/Angel_Mage_Creativekind/` | Character sprite (holy/light; blue palette) | entity (blue palette confirmed from directory structure) | HD-2D-conformant |
| CreativeKind | angel_v1 | `CreativeKind/angel_v1/` | Character sprite (angel) | entity | HD-2D-conformant |
| Chierit Elementals bundle | light_valkyrie (zip) | `Elementals_bundle/Elementals_light_valkyrie_complete_v1.1.zip` | Character sprite (holy/light; UNEXTRACTED) | n/a | HD-2D-conformant |

**Catalogue-only (not on-disk):**
- CreativeKind Holy Spell Effects pack (catalogue JSONL: `creativekind/full-2026-05-16.jsonl` — legolas confirms holy-register VFX at GREEN-list) — CATALOGUE-ONLY, NOT ON-DISK
- Pimen Holy Spell Effect (catalogue; not on-disk)
- Frostwindz Paladin/Priest packs (catalogue; holy-adjacent; not on-disk)

**Gap assessment:** Holy has CHARACTER SPRITES on-disk (Angel Guardian, Angel Mage, angel_v1 from CreativeKind; light_valkyrie from chierit as ZIP) but NO DEDICATED HOLY SPELL VFX on-disk. The CreativeKind Holy Spell Effects pack is catalogue-only. This is the most significant VFX gap among the three new substrates — holy has entity sprites but no standalone spell-effect animations matching the substrate's `iconic_verbs: [consecrates, sanctifies, burns away, judges, reveals, blesses, uplifts, shines through]` and `geometry_affinities: [radiant_aura: PREFER, shaft: PREFER, nova: PREFER]`. Demo rendering of holy combat skills would need to repurpose generic light/explosion effects or use entity character animations only, which is insufficient for the substrate's radiant_aura + nova geometry profile.

**Visual register confidence:** HD-2D-conformant for CreativeKind character sprites. Chierit light_valkyrie pending extraction. Dedicated holy spell VFX: ABSENT (no on-disk pack).

---

### § 1.7 — Shadow

**On-disk VFX assets:**

| Vendor | Pack | Path | Asset type | Animation count | HD-2D register |
|---|---|---|---|---|---|
| CreativeKind | Dark_Hole | `CreativeKind/Dark_Hole/` | VFX (dark/void; shadow-adjacent) | animation | HD-2D-conformant |
| CreativeKind | Dark_Soul_Creativekind | `CreativeKind/Dark_Soul_Creativekind/` | Monster sprite (shadow-adjacent) | entity | HD-2D-conformant |
| CreativeKind | Lich_Creativekind | `CreativeKind/Lich_Creativekind/` | Monster sprite (shadow/undead; 5 color palettes including Magenta, Green, Blue, Red, Lightning) | entity | HD-2D-conformant |
| CreativeKind | Mutant_skeleton | `CreativeKind/Mutant_skeleton/` | Monster sprite (shadow/undead sub-register) | entity | HD-2D-conformant |
| Chierit Elementals bundle | shadow_stalker (zip) | `Elementals_bundle/Elementals_shadow_stalker_complete_v1.0.zip` | Character sprite (shadow; UNEXTRACTED) | n/a | HD-2D-conformant |

**Catalogue-only (not on-disk):**
- CreativeKind shadow-tendril VFX (catalogue GREEN-list per legolas; distinct from Dark_Hole entity) — CATALOGUE-ONLY
- Frostwindz Deathbringer pack (bone/death VFX) — PENDING MATT ACQUISITION
- Pimen Dark Spell Effect (catalogue; shadow-tagged; not on-disk)

**Gap assessment:** Shadow has some on-disk assets (Dark_Hole, Dark_Soul, Lich, Mutant_skeleton from CreativeKind; shadow_stalker from chierit as ZIP). Dark_Hole is a VFX animation directly (not just a character sprite), which gives shadow the most "real VFX" coverage of the new substrates beyond lightning. However, shadow's signature `combat_pillar: CONCEALMENT_AND_DRAIN` and `geometry_affinities: [tendril: PREFER, void_pool: PREFER, creep: PREFER]` are not well-served by Dark_Hole alone (which is void-pool but not tendril or creep). The CreativeKind shadow-tendril pack is catalogue-only. Frostwindz Deathbringer would add bone/death VFX that serves shadow's undead-adjacent register (per CHANGELOG Matt reframe under expanded 6-substrate cosmology). Shadow needs both Deathbringer (pending) and shadow-tendril (catalogue-acquisition candidate) to reach geometry-profile coverage.

**Visual register confidence:** HD-2D-conformant for CreativeKind + chierit assets. Frostwindz Deathbringer register TBD (pending acquisition — Frostwindz is RETRO-pixel register per style-register § empirical landscape "Foozle, Frostwindz — 16-bit-shaped, low-resolution, classic indie register"). **RISK: Frostwindz is likely RETRO register, not HD-2D-conformant.** Surface to gandalf for register-coherence judgment before wiring into shadow combat rendering.

---

## § 2 — Vendor Acquisition Dependency Mapping

### § 2.1 — CraftPix Premium (wood-nature)

**CHANGELOG authorization:** "ACQUIRE HIGH PRIORITY" per 2026-05-17 entry.
**Payment/download status:** PENDING MATT ACTION.
**Projected on-disk path:** `public/assets/craftpix/wood-nature/` (demo-repo; drax authority).
**Substrates served:** Earth (biological-organic sub-register rebuild post-cull).
**What it fills:**
- Earth spell VFX for plant/root/vine/bark/leaf/wood skills. Current on-disk coverage: pimen earth-spell-effect-03 covers boulder/spike/hammer/trap/petrify (stone/impact earth register) but has zero wood/organic/plant VFX.
- The pool D1 re-score under substrate_native is expected to assign wood/root/bark/vine/leaf/moss/lichen to earth allow-list. CraftPix wood-nature VFX maps directly to these semantic entries.
**Estimated asset count:** Unknown without acquisition. CraftPix premium packs typically contain 5-20 sprite animation sets. CHANGELOG projects "root/bark/leaf/petal/vine/moss/lichen/wood" as the fill target — suggest 6-10 distinct animation types.
**Integration touch-points:**
- Demo: `src/combat/VFXLayer.ts` or equivalent VFX dispatch call-site — add wood-nature animation types to earth VFX router
- Loadout: substrate-browser thumbnail surface (D21) should show biological earth sample; loadout does not render VFX animations directly, but a static preview frame could be referenced
- Element-coherence: skills tagged `root_apply` (earth's ailment_signature) would select from this pack for their animation
**Register risk:** CraftPix vendor catalogue (craftpix JSONL) shows CraftPix packs at retro-pixel register in some cases. Verify HD-2D-conformance on acquisition before wiring — if retro, restrict to UI thumbnails only, not in-combat VFX.

### § 2.2 — Fellor Crystal Gem Cluster

**CHANGELOG authorization:** "ACQUIRE MED PRIORITY" per 2026-05-17 entry.
**Payment/download status:** PENDING MATT ACTION.
**Projected on-disk path:** `public/assets/fellor/crystal/` (demo-repo; drax authority).
**Substrates served:** Earth (gem/crystal/precious-metal sub-register; reinforces the 13-entry crystal/gem/precious-metal allow-list cluster that D1 cull keeps).
**What it fills:**
- Crystal visual effects for earth-crystal skills and Crystal_golem + Crystal_Wisp monster tier interactions. Current on-disk: CreativeKind Crystal_golem and Crystal_Wisp have entity sprites but no dedicated crystal-burst or crystal-aura VFX animations.
- The Fellor catalogue JSONL confirms crystal/gem VFX packs exist in the Fellor catalogue. On-disk, there is NO fellor directory at `public/assets/` — zero Fellor assets on-disk currently.
**Estimated asset count:** Fellor catalogue shows 7 packs total; crystal-specific count unknown without acquisition. Estimate 4-8 animation types (crystal shatter, crystal burst, crystal aura, gem glow, etc.).
**Integration touch-points:**
- Demo: earth VFX router addition — crystal-register skills route to Fellor crystal animations
- Loadout: substrate-browser earth entry could show crystal preview frame alongside organic (CraftPix) and stone (pimen)
- Element-coherence: items with crystal/gem element-tag in gear pool would benefit from crystal VFX in skill display
**Register risk:** Fellor register unknown without inspection (no on-disk assets to gauge). Fellor JSONL classification suggests pixel-art but register quality unclear. Verify on acquisition.

### § 2.3 — Frostwindz Deathbringer (bone)

**CHANGELOG authorization:** "ACQUIRE per Matt override 2026-05-17" with explicit Matt reframe: bone/death/skeleton VFX maps to shadow substrate, not earth-flex.
**Payment/download status:** PENDING MATT ACTION.
**Projected on-disk path:** `public/assets/frostwindz/deathbringer/` (demo-repo; drax authority).
**Substrates served:** Shadow (bone/death/skeleton VFX serving shadow's undead-adjacent cosmological_commitment and court_resonance "forms that walked alongside what they did not name").
**What it fills:**
- Shadow spell VFX for drain/corrupt/shroud skills. The Frostwindz Deathbringer pack is described as bone/death/skeleton VFX — directly serves shadow's undead-necromantic register.
- Current on-disk shadow VFX: Dark_Hole (void-pool type), Lich entity sprite, Dark_Soul entity, Mutant_skeleton entity. No dedicated shadow spell-effect animations for the `tendril / creep / drain` geometry profile. Deathbringer would fill the "what does a drain-life skill look like" gap partially (the bone-drain/life-siphon visual read is genre-canon).
**Estimated asset count:** Frostwindz Deathbringer is identified as a specific pack in the catalogue (Frostwindz has 15 packs total in catalogue). Pack-level count unknown without acquisition. Estimate 5-15 animation types (bone spear, skeleton summon, death wave, bone wall, decay aura, etc. per necromancer-archetype genre conventions).
**Integration touch-points:**
- Demo: shadow VFX router — bone/death animations for drain + corrupt + shroud skill types
- Loadout: substrate-browser shadow thumbnail — bone/death visual register represents shadow's un-ascended-form cosmological role
- Element-coherence: shadow archetype skills (drain/corrupt) route to Deathbringer animations
**Register risk:** HIGH RISK. Frostwindz is explicitly classified as RETRO-pixel register in style-register.md: "ansimuz, Pipoya, Foozle — 16-bit-shaped, low-resolution, classic indie register" — Frostwindz is in the same family. This pack is likely NOT HD-2D-conformant. Wiring to in-combat VFX rendering under the HD-2D register lock would violate style-register.md. MITIGATION options: (1) Use Deathbringer assets as UI-only (substrate browser thumbnail; no in-combat render); (2) Acquire a HD-2D shadow VFX alternative alongside/instead; (3) Surface to gandalf for register disposition before wiring in-combat.
**TODO(drax): Register verification required on Frostwindz Deathbringer acquisition. Do NOT wire to combat VFX without register confirmation or gandalf EXCEPTION.** Track this as a pre-integration gate item.

---

## § 3 — Substrate-Coverage Gaps (Per Substrate)

### § 3.1 — Fire: ADEQUATE

No blocking gaps. Fire has both spell VFX (pimen fire-spell-effect-3; 9 animation groups) and character sprites (CreativeKind Fire_attack, Fire_Elemental, Fire_Lord; chierit fire_knight ZIP). The chierit fire_knight ZIP extraction is the only pending action before full fire coverage is demo-ready.

Gap: None blocking Phase-1 P1.

### § 3.2 — Water: ADEQUATE

No blocking gaps for Phase-1 P1 core demo. Pimen water-spell-effect-03 (7 animation groups) on-disk. Chierit water_priestess ZIP pending extraction. Ice sub-register gap: pimen ice-spell-effect-02 appears unextracted (raw/ shows 0 animations); requires verification. The water substrate does not have cold/ice as a distinct registered VFX layer at this point, which may matter once sub-register VFX routing is implemented.

Gap: Ice-spell-effect-02 extraction verification needed. Not blocking.

### § 3.3 — Earth: MODERATE GAP (biological-organic sub-register)

Stone/impact earth register: ADEQUATE (pimen earth-spell-effect-03, 11 animation groups).
Crystal/gem register: PARTIAL (CreativeKind entity sprites only; no crystal VFX animations — Fellor acquisition fills this).
Biological-organic register: ABSENT from on-disk VFX. No root/bark/vine/moss/leaf animations exist on-disk. CraftPix premium wood-nature acquisition fills this gap.

Gap: Two VFX sub-registers absent from disk (crystal VFX = Fellor; biological = CraftPix). Both pending acquisition.

### § 3.4 — Wind: ADEQUATE

Pimen wind-spell-effect-03 (12 animation groups — richest canonical-four pack). Chierit wind_hashashin ZIP pending extraction. No blocking gap.

Gap: None blocking Phase-1 P1.

### § 3.5 — Lightning: STRONG (best-covered new substrate)

Pimen thunder-spell-effect-03 with ~30 animation variants (blur/no-blur pairs across 11 categories: Burst, Electric bow, Electric Disc, Electric Explosion, Electric Trap, Hit Effect, Shield, Thunder Ball, Thunder Bullet, Thunder Whip, Thunder Spell Circle). CreativeKind God_of_Lightning (two palette variants) + Lightning_horizontal + Lightning_vertical VFX + Lich with lightning palette. Chierit lightning_ronin ZIP. The lightning substrate has the deepest on-disk VFX coverage of the three new substrates, with both dedicated spell-effect animations AND entity sprites.

Gap: Fellor Lightning VFX Pack (catalogue-only) would add depth but is NOT a blocking gap for Phase-1 P1. The pimen thunder pack already covers all lightning geometry affinities (arc, bolt_line, chain_lightning, branching, projectile).

Register note: The pimen thunder-spell-effect-03 pack name uses "thunder" but contains electric/lightning content. At implementation time, the manifest should tag this pack as `substrate: lightning` regardless of the pack's commercial name.

### § 3.6 — Holy: SIGNIFICANT GAP (entity sprites only; no spell VFX on-disk)

Entity sprites on-disk: CreativeKind Angel_Guardian, Angel_Mage, angel_v1 (all human-angel forms in holy register). Chierit light_valkyrie ZIP. These give holy a character sprite foundation.

Spell VFX on-disk: NONE. No radiant_aura, shaft, nova, or consecrate-zone animations exist in the on-disk asset tree. The CreativeKind Holy Spell Effects pack (GREEN-list per legolas reverse audit § 4.1) is catalogue-only. Pimen Holy Spell Effect is catalogue-only.

Gap: Holy spell VFX is the LARGEST blocking gap for holy-substrate combat rendering. Without dedicated holy spell VFX on-disk, holy archetype skills (consecrate, sanctify, burn away, reveal, bless) have no substrate-coherent animation source. This requires either: (a) CreativeKind Holy Spell Effects acquisition (catalogue-only, not in the Matt-authorized three acquisitions); or (b) Creative reuse of existing light/explosion VFX with color filtering (workaround). The Frostwindz Paladin/Priest packs (catalogue) also serve holy register but are in the Frostwindz RETRO family.

**OBSERVATION for knight-rider:** The three Matt-authorized acquisitions (CraftPix, Fellor, Frostwindz) do NOT include a dedicated holy spell VFX pack. Implementing holy combat rendering for Phase-1 P1 will require either a fourth acquisition (CreativeKind Holy Spell Effects) or the color-filter workaround. Surface to Matt as L3 acquisition gap.

### § 3.7 — Shadow: PARTIAL GAP (entity sprites + 1 VFX; no tendril/drain animations)

On-disk VFX: CreativeKind Dark_Hole (void-pool geometry; one animation). Entity sprites: CreativeKind Dark_Soul, Lich, Mutant_skeleton + chierit shadow_stalker ZIP.
Missing: tendril, creep, drain geometry profile VFX. Shadow's PREFERRED geometry shapes (tendril, void_pool, creep) are not well-served by Dark_Hole alone. The CreativeKind shadow-tendril pack (GREEN-list per legolas) is catalogue-only. Frostwindz Deathbringer (pending acquisition) fills bone/death register but is RETRO-pixel register risk.

Gap: Shadow-tendril VFX absent. Drain/creep animations absent. Frostwindz Deathbringer fills bone register at RETRO register risk. Consider adding CreativeKind shadow-tendril as a fourth acquisition (surface to knight-rider as L2 observation).

---

## § 4 — Integration Plan for VFX Library Extension

This section describes the implementation steps once Matt's acquisitions land on-disk. **Implementation is BLOCKED until packs are downloaded.**

### § 4.1 — On-disk placement workflow

When Matt downloads vendor packs, the following placement convention applies:

```
reincarnated-demo/public/assets/
  craftpix/
    wood-nature/          ← CraftPix premium wood-nature contents unpacked here
      metadata.json       ← drax authors post-acquisition (pack_slug, substrate, register, asset_count)
      raw/                ← raw sprite sheets / animation frames
      sheets/             ← processed atlases (if applicable)
  fellor/
    crystal/              ← Fellor crystal gem cluster unpacked here
      metadata.json
      raw/
      sheets/
  frostwindz/
    deathbringer/         ← Frostwindz Deathbringer unpacked here
      metadata.json
      raw/
      sheets/
```

Naming convention: lowercase vendor name / lowercase pack name, no spaces. Follows the existing `pimen/thunder-spell-effect-03/` pattern.

**metadata.json schema** (drax authors per pack on placement):

```json
{
  "pack_slug": "<vendor>-<pack-name>",
  "pack_name": "<human-readable name>",
  "vendor": "<vendor>",
  "substrate": "<primary substrate this pack serves>",
  "substrate_sub_register": "<optional sub-register: biological-organic | crystal-gem | bone-death>",
  "source_url": "<acquisition url>",
  "derived_register": "<hand-drawn-pixel | retro-pixel | unknown>",
  "register_verified": false,
  "license": "<license type>",
  "attribution_required": false,
  "attribution_text": null,
  "asset_count": 0,
  "animations": []
}
```

The `register_verified` field defaults to false; drax sets it to true after visual inspection at implementation time.

### § 4.2 — Demo rendering wiring (call-sites + VFX routing)

This section anticipates the demo-side integration work but does NOT touch demo files (Track A owns demo; Track B is planning only).

**VFX dispatch architecture (anticipated):** The demo combat rendering has a VFX layer that plays sprite animations keyed to skill effects. At implementation time, the wiring adds:

1. **Per-substrate VFX manifest** (see § 4.4 below) — maps substrate → animation types → on-disk paths.
2. **Element-keyed routing** — the existing CreativeKind/chierit precedent routes by element. Post-Phase-1 P1, routing extends to: `fire → pimen/fire-spell-effect-3`, `water → pimen/water-spell-effect-03`, `earth → pimen/earth-spell-effect-03 + craftpix/wood-nature + fellor/crystal`, `wind → pimen/wind-spell-effect-03`, `lightning → pimen/thunder-spell-effect-03 + creativekind/lightning-*`, `holy → [catalogue-pending]`, `shadow → creativekind/dark-hole + frostwindz/deathbringer [register-gated]`.
3. **Geometry-affinity routing** — per the substrate-identity declarations, each geometry type maps to preferred animations within the substrate's VFX pack. Example: `earth + pillar geometry → pimen earth_spike animation`; `earth + ground_targeted_circle geometry → pimen earth_trap animation`.

**For demo wiring (Track A / demo-instance drax):** Surface geometry-affinity routing plan as a hive log HANDOFF entry when acquisitions land.

### § 4.3 — Loadout app surface (D21 substrate browser + D22 embodiment display + element badges)

The loadout app (drax-loadout seam, this Track B session) will consume VFX metadata in the following surfaces:

**D21 — Substrate browser thumbnails:**
- Each substrate card in the browser shows a representative VFX static frame as the visual identity anchor.
- Static frame selection: the "most iconic" animation frame from the substrate's primary VFX pack — e.g., lightning substrate browser card shows a frame from pimen thunder-spell-effect-03 (electric disc or thunder burst frame); holy shows angel guardian or light_valkyrie sprite; shadow shows dark_hole.
- Loadout app does NOT animate these frames (that would be demo concern). Static PNG frame import via the manifest.
- At this stage: no loadout VFX code changes until D21 is implemented. Thumbnails will use a `substrate_thumbnail_url` field in the manifest once manifest schema is agreed.

**D22 — Embodiment display:**
- The embodiment display shows the player's current form. VFX are display-mode only (no live Pixi.js in loadout). Loadout may show a static sprite frame from the chierit Elementals packs for each substrate's canonical form.
- Chierit entity packs are ZIPs requiring extraction. At D22 implementation: extract, verify register, add to manifest, reference from embodiment display.

**GearGrid / SkillDetailPanel element badge surface:**
- Skill element badge colors are already substrate-keyed in loadout (v0.21 cipher consumption). When canonical-7 substrates are active, three new color entries are needed: lightning (electric yellow), holy (radiant gold/white), shadow (deep purple/black). No VFX involved — color badge only.
- This is a small CSS/Tailwind addition at D21 implementation time. No VFX assets required.

### § 4.4 — Per-substrate VFX manifest schema (proposed)

Proposing the following JSON schema for the VFX manifest that the demo rendering call-sites + loadout substrate browser consume. Star-lord will consume this for D15/D17/D18 manifest cipher work — coordinate via hive log.

**Path:** `reincarnated-demo/public/assets/vfx-manifest.json` (demo-side) + mirrored as a seam export for loadout consumption.

```json
{
  "schema_version": "1.0",
  "substrates": {
    "fire": {
      "primary_pack": "pimen/fire-spell-effect-3",
      "register": "hand-drawn-pixel",
      "register_verified": true,
      "geometry_animation_map": {
        "burst": "pimen/fire-spell-effect-3/raw/Fire combo",
        "cone": "pimen/fire-spell-effect-3/raw/Fire Claw And Slashes",
        "area_sustain": "pimen/fire-spell-effect-3/raw/Barrier",
        "ground_targeted_circle": "pimen/fire-spell-effect-3/raw/Fire Shield"
      },
      "thumbnail_frame": "pimen/fire-spell-effect-3/sheets/fire_combo_frame_0.png",
      "entity_packs": [
        "CreativeKind/Fire_Elemental_Creativekind",
        "CreativeKind/Fire_attack",
        "Elementals_bundle/Elementals_fire_knight_FULL_v1.1.zip"
      ],
      "acquisition_status": "on-disk"
    },
    "water": {
      "primary_pack": "pimen/water-spell-effect-03",
      "register": "hand-drawn-pixel",
      "register_verified": true,
      "geometry_animation_map": {
        "area_sustain": "pimen/water-spell-effect-03/raw/Water Burst",
        "circle": "pimen/water-spell-effect-03/raw/Water Magic Circle",
        "wave": "pimen/water-spell-effect-03/raw/Water Combo"
      },
      "thumbnail_frame": "pimen/water-spell-effect-03/sheets/water_burst_frame_0.png",
      "entity_packs": [
        "Elementals_bundle/Elementals_water_priestess_FULL_v1.1.zip"
      ],
      "acquisition_status": "on-disk"
    },
    "earth": {
      "primary_pack": "pimen/earth-spell-effect-03",
      "register": "hand-drawn-pixel",
      "register_verified": true,
      "supplementary_packs": [
        { "pack": "craftpix/wood-nature", "sub_register": "biological-organic", "acquisition_status": "pending-matt" },
        { "pack": "fellor/crystal", "sub_register": "crystal-gem", "acquisition_status": "pending-matt" }
      ],
      "geometry_animation_map": {
        "ground_targeted_circle": "pimen/earth-spell-effect-03/raw/Earth Trap 1",
        "pillar": "pimen/earth-spell-effect-03/raw/Earth Spike",
        "slam": "pimen/earth-spell-effect-03/raw/Earth Hammer",
        "melee_arc": "pimen/earth-spell-effect-03/raw/Earth Burst"
      },
      "thumbnail_frame": "pimen/earth-spell-effect-03/sheets/earth_spike_frame_0.png",
      "entity_packs": [
        "CreativeKind/Crystal_golem_creativekind",
        "Elementals_bundle/Elementals_ground_monk_FULL_v1.3.zip",
        "Elementals_bundle/Elementals_Crystal_Mauler_Full_v1.0.zip"
      ],
      "acquisition_status": "partial-on-disk"
    },
    "wind": {
      "primary_pack": "pimen/wind-spell-effect-03",
      "register": "hand-drawn-pixel",
      "register_verified": true,
      "geometry_animation_map": {
        "cone": "pimen/wind-spell-effect-03/raw/Extras",
        "projectile": "pimen/wind-spell-effect-03/raw/Projectile 1",
        "vortex_pull": "pimen/wind-spell-effect-03/raw/Air attack",
        "line": "pimen/wind-spell-effect-03/raw/Multi Slashes"
      },
      "thumbnail_frame": "pimen/wind-spell-effect-03/sheets/air_attack_frame_0.png",
      "entity_packs": [
        "Elementals_bundle/elementals_wind_hashashin_FULL_v1.1.zip"
      ],
      "acquisition_status": "on-disk"
    },
    "lightning": {
      "primary_pack": "pimen/thunder-spell-effect-03",
      "register": "hand-drawn-pixel",
      "register_verified": true,
      "supplementary_packs": [
        { "pack": "CreativeKind/Lightning_horizontal", "sub_register": "bolt-line", "acquisition_status": "on-disk" },
        { "pack": "CreativeKind/Lightning_vertical", "sub_register": "bolt-line", "acquisition_status": "on-disk" }
      ],
      "geometry_animation_map": {
        "arc": "pimen/thunder-spell-effect-03/raw/Electric bow",
        "bolt_line": "CreativeKind/Lightning_horizontal",
        "branching": "pimen/thunder-spell-effect-03/raw/Burst(48x48)",
        "chain_lightning": "pimen/thunder-spell-effect-03/raw/Thunder Whip",
        "projectile": "pimen/thunder-spell-effect-03/raw/Thunder Bullet"
      },
      "thumbnail_frame": "pimen/thunder-spell-effect-03/sheets/thunder_burst_frame_0.png",
      "entity_packs": [
        "CreativeKind/God_of_Lightning_Light_Version_Creativekind",
        "CreativeKind/Lich_Creativekind",
        "Elementals_bundle/Elementals_lightning_ronin_full_v1.0.zip"
      ],
      "acquisition_status": "on-disk"
    },
    "holy": {
      "primary_pack": null,
      "register": "unknown",
      "register_verified": false,
      "supplementary_packs": [
        { "pack": "CreativeKind/holy-spell-effects", "sub_register": "radiant-aura", "acquisition_status": "catalogue-only" },
        { "pack": "pimen/holy-spell-effect", "sub_register": "shaft-nova", "acquisition_status": "catalogue-only" }
      ],
      "geometry_animation_map": {},
      "thumbnail_frame": "CreativeKind/Angel_Guardian_Creativekind/sprite_frame_0.png",
      "entity_packs": [
        "CreativeKind/Angel_Guardian_Creativekind",
        "CreativeKind/Angel_Mage_Creativekind",
        "Elementals_bundle/Elementals_light_valkyrie_complete_v1.1.zip"
      ],
      "acquisition_status": "entity-only-on-disk"
    },
    "shadow": {
      "primary_pack": "CreativeKind/Dark_Hole",
      "register": "hand-drawn-pixel",
      "register_verified": true,
      "supplementary_packs": [
        { "pack": "CreativeKind/shadow-tendril", "sub_register": "tendril", "acquisition_status": "catalogue-only" },
        { "pack": "frostwindz/deathbringer", "sub_register": "bone-death", "acquisition_status": "pending-matt", "register_risk": "likely-retro-pixel" }
      ],
      "geometry_animation_map": {
        "void_pool": "CreativeKind/Dark_Hole"
      },
      "thumbnail_frame": "CreativeKind/Dark_Soul_Creativekind/sprite_frame_0.png",
      "entity_packs": [
        "CreativeKind/Dark_Soul_Creativekind",
        "CreativeKind/Lich_Creativekind",
        "Elementals_bundle/Elementals_shadow_stalker_complete_v1.0.zip"
      ],
      "acquisition_status": "partial-on-disk"
    }
  }
}
```

**Schema design notes:**
- `geometry_animation_map` keys mirror the `geometry_affinities` field names from substrate-identity-declarations. This is the load-bearing connection between the canonical declarations and demo rendering.
- `acquisition_status` values: `on-disk` / `pending-matt` / `catalogue-only` / `entity-only-on-disk` / `partial-on-disk`
- `register_risk` field on supplementary packs flags Frostwindz register uncertainty — implementation must check this before wiring combat VFX.
- `thumbnail_frame` is a static PNG path for loadout substrate-browser use (no animation required).

**Star-lord coordination note:** This manifest schema proposes a structure star-lord can consume in D15/D17/D18 LLM prompt-template work (substrate → VFX register → LLM `visual_prompt` field generation). Surface in hive log for star-lord alignment before finalizing schema.

---

## § 5 — License + Attribution Tracking

### § 5.1 — CraftPix Premium (wood-nature)

**License type:** CraftPix uses a Pro License (commercial royalty-free per CraftPix standard terms; includes game-as-product use). Attribution is NOT required for CraftPix Pro (the standard CraftPix paid license explicitly does not require attribution in-game or in credits). Commit-message attribution is optional but good practice.
**Action at acquisition:** Verify current CraftPix license page matches this characterization (license terms can evolve). Specifically verify: (1) no per-game-title registration required; (2) resale or asset distribution restrictions.
**Attribution text (if required):** "Art assets from CraftPix.io" — add to About/footer in loadout if Pro license requires it.

### § 5.2 — Fellor Crystal Gem Cluster

**License status:** UNKNOWN pending acquisition. No Fellor license terms are documented in the catalogue research files (`fellor/full-2026-05-16.jsonl` does not include license field confirmation). The Pixogen precedent (proprietary-with-attribution per `pixogen/findings-summary-2026-05-16.md`) suggests independent itch.io vendors vary widely.
**Action at acquisition:** Read license.txt or itch.io license declaration before wiring. Specifically check: (1) attribution-required or not; (2) commercial use allowed; (3) resale restrictions.
**Attribution text (if required):** "Crystal VFX assets from Fellor (itch.io)" — add to About/footer in loadout.

### § 5.3 — Frostwindz Deathbringer

**License status:** UNKNOWN pending acquisition. Frostwindz has 15 packs in catalogue; no explicit license terms documented in the research files. The Frostwindz vendor is a prolific itch.io publisher; typical terms are CC0 or royalty-free commercial but must be verified per pack.
**Action at acquisition:** Read Frostwindz Deathbringer pack license page. Per register-risk assessment: if the pack is CC0, it can be freely used as a UI-only asset even under the retro-pixel register constraint (UI thumbnails aren't subject to style-register.md's in-game rendering constraint in the same way combat VFX are).
**Attribution text (if required):** "Deathbringer VFX by Frostwindz (itch.io)".

### § 5.4 — Pimen Packs (on-disk)

**License status:** All pimen packs on-disk are `commercial-royalty-free` per metadata.json `license` field (confirmed in thunder-spell-effect-03/metadata.json). Per Pimen precedent established during the pimen full-crawl, pimen packs require commit-message attribution per the CC-BY-4.0 pattern (noted in AGENTS.md as Pimen full-crawl precedent for pixel-battle-effects / cutting-and-healing). The existing `reincarnated-loadout/AGENT_STATE.md` notes game-icons.net CC-BY attribution is now in the footer. Pimen attribution should follow the same pattern when pimen VFX appear in loadout UI surfaces.
**Attribution text:** "Spell Effect VFX by Pimen (itch.io)" — append to About/footer when pimen assets surface in loadout substrate browser.

### § 5.5 — CreativeKind (on-disk)

**License status:** Commercial use; CreativeKind assets are typically sold with a royalty-free commercial license. No specific per-pack attribution requirement documented. Attribution in commit messages is current practice (AGENT_STATE note).
**Action:** Confirm CreativeKind Holy Spell Effects license terms if acquired as a fourth pack.

### § 5.6 — Chierit Elementals bundle (on-disk as ZIPs)

**License status:** Chierit packs are present on-disk as ZIP archives in `Elementals_bundle/`. License terms are in the ZIP archives (not yet inspected since ZIPs are unextracted). At extraction time, read the embedded license.
**Attribution text:** TBD pending ZIP extraction and license review.

---

## § 6 — Cross-Seam Implications

### § 6.1 — Star-lord (D17 Spirit-Guide voice; D22 manifest cipher; D15 LLM flavor)

The per-substrate VFX manifest schema proposed in § 4.4 introduces new fields that star-lord needs to be aware of:
- `substrate_thumbnail_url` (or equivalent) will surface in the Court of Forms browser (D17 drax surface). Star-lord's LLM prompt-template work (D15) may need a `substrate_vfx_register` field to ensure LLM-generated `visual_prompt` language aligns with the actual VFX register (hand-drawn-pixel descriptions should not be generated for a substrate whose only VFX are retro-pixel).
- The manifest's `geometry_animation_map` keys (which mirror substrate-identity-declarations `geometry_affinities`) create a machine-readable connection between the canonical spec and the demo renderer. Star-lord should confirm this key-naming convention is compatible with the prompt-template's `geometry_profile` field if one exists.
**Action: surface manifest schema to star-lord via hive log for D17/D22 coordination.**

### § 6.2 — Rocket (D1 substrate identity loader)

The substrate YAML files rocket extracts will contain the `geometry_affinities` field (each entry is PREFER/NEUTRAL/AVOID per declaration). The VFX manifest's `geometry_animation_map` is keyed to the same geometry type names. These must match exactly at implementation time. The geometry types used in the manifest schema above (`burst`, `cone`, `arc`, `bolt_line`, `branching`, `chain_lightning`, `tendril`, `void_pool`, `area_sustain`, `pillar`, `slam`, `projectile`, `ground_targeted_circle`, `radiant_aura`, `shaft`, `nova`) are drawn directly from the substrate-identity-declarations geometry_affinities fields.
**Action: when rocket ships D1 YAML extraction, drax should verify geometry_affinity key names match the VFX manifest schema. Surface any mismatch as FRICTION in hive log.**

### § 6.3 — Gandalf (D26 cross-doc updates; substrate visual register)

The Frostwindz Deathbringer register risk (RETRO-pixel) requires gandalf disposition before wiring to in-combat VFX. The question is: can the shadow substrate's bone/death VFX use retro-pixel assets for combat rendering as an exception (since shadow's iconic_register is "shadow" — the most stylistically ambiguous register), or does the HD-2D lock apply without exception?
Per style-register.md: "This doc supersedes: any implicit register defaults inherited from demo1's existing Pixi.js + Super Pixel Effects tooling... Demo1's retro-pixel register is transitional, not canonical." This suggests the HD-2D lock is firm; retro-pixel Frostwindz assets should NOT be wired to in-combat VFX.

Also: holy's holy-spell-effects gap (§ 3.6 above) is a design tension gandalf should be aware of — holy's cosmological_commitment ("the substrate of revelation — what exposes") requires visually distinctive radiant VFX that the current on-disk inventory cannot provide. If a fourth acquisition (CreativeKind holy-spell-effects) is not authorized, gandalf may want to surface whether the angel entity sprites alone are sufficient for holy combat rendering or whether a creative workaround (pimen explosion composited with color filter) is acceptable as a placeholder.

### § 6.4 — Elrond (catalogue.db curation pipeline)

Newly-acquired packs (CraftPix wood-nature, Fellor crystal, Frostwindz Deathbringer) will need a curation pipeline pre-processor pass per the 4-rule Pimen precedent (style-register tagging, geometry-signature extraction, substrate-classification, asset-count). Elrond should receive a data-intake notification when Matt downloads and places packs.
**Action: drax notifies elrond via hive log when packs land on-disk + provides pack paths for curation pass.**

### § 6.5 — Jack-ryan (D19 Gate-1-equivalent continuous observation)

Jack-ryan continuous-observation should watch for:
1. Register coherence: Frostwindz Deathbringer wired to combat VFX without register verification = Discipline #13 violation (implicit-pillar drift — style-register pillar violated). Flag as WARN if drax wires it without explicit gandalf exception.
2. Geometry-key consistency: VFX manifest `geometry_animation_map` keys must match substrate-identity-declaration `geometry_affinities` keys exactly. Any mismatch = silent-routing failure (Pattern P7 variant).
3. Attribution completeness: on any production deploy of holy/shadow/lightning surfaces in loadout, confirm Pimen CC-BY attribution is in the footer.

---

## § 7 — Effort Estimate for D19 Implementation Phase

**Baseline estimate (knight-rider):** 5-7 days.

**Drax-revised estimate:** 6-9 days across three sub-phases, contingent on acquisition timing:

**Sub-phase A: Extraction + manifest authoring (1-2 days)**
- Extract chierit Elementals ZIPs (lightning_ronin, light_valkyrie, shadow_stalker, + others for canonical-four completeness)
- Verify register on extracted chierit assets
- Author `vfx-manifest.json` with on-disk assets populated
- Verify ice-spell-effect-02 extraction status (may need archive extraction)
- Does NOT require Matt acquisitions — can start immediately

**Sub-phase B: Acquisition intake + register verification (0.5-1 day, depends on Matt)**
- When Matt downloads CraftPix/Fellor/Frostwindz packs: unzip, place at canonical paths, author metadata.json for each pack, run visual register check on Frostwindz Deathbringer
- Update `vfx-manifest.json` with acquisition-status fields changed from `pending-matt` to `on-disk`
- BLOCKED until Matt downloads

**Sub-phase C: Demo VFX wiring + loadout substrate browser (4-6 days)**
- Demo: add `vfx-manifest.json` as a loaded resource; extend VFX dispatcher to route by substrate + geometry type; integrate new packs per geometry_animation_map; smoke-test "demo launches, renders one frame without console errors" per element for all 7 substrates
- Loadout D21: substrate-browser component with per-substrate thumbnails from manifest; static frame import
- Loadout D22 (joint with star-lord): embodiment display showing chierit entity sprites per substrate
- Element badges in GearGrid/SkillDetailPanel: three new color entries for lightning/holy/shadow
- BLOCKED on Sub-phase B for holy/shadow/earth-organic/crystal coverage; lightning/fire/water/wind/earth-stone can begin without acquisitions

**Total: 6-9 days depending on acquisition timing and whether holy spell VFX gap is resolved by a fourth acquisition.**

**Risk: holy spell VFX gap adds 1-2 days if a creative workaround must be designed vs. 0 additional days if a fourth acquisition ships the CreativeKind Holy Spell Effects pack directly.**

---

## § 8 — Open Questions

1. **Holy spell VFX acquisition:** The three Matt-authorized acquisitions (CraftPix, Fellor, Frostwindz) do NOT include a dedicated holy spell VFX pack. Is a fourth acquisition (CreativeKind Holy Spell Effects, ~$5-10) authorized for Phase-1 P1 holy combat rendering? If not, what is the approved workaround? **[Surface to Matt as L3 via knight-rider]**

2. **Frostwindz Deathbringer register exception:** Is the shadow substrate permitted to use retro-pixel Frostwindz assets for combat VFX rendering as a style-register exception, given the bone/death VFX gap? Or should shadow combat rendering use HD-2D-only assets (Dark_Hole + shadow-tendril acquisition) with Deathbringer restricted to UI-only (substrate browser thumbnail)? **[Surface to gandalf as L2 design question]**

3. **Chierit Elementals ZIP extraction:** The chierit Elementals_bundle contains ZIPs for fire_knight, water_priestess, ground_monk, crystal_mauler, leaf_ranger, wind_hashashin, lightning_ronin, light_valkyrie, shadow_stalker, metal_bladekeeper. These are all unextracted. Should drax extract these in Sub-phase A of implementation, or does extraction require explicit knight-rider authorization? Sub-phase A does not require Matt acquisitions. **[L1 in-seam decision — drax can proceed; flagging for awareness]**

4. **VFX manifest schema coordination with star-lord:** The proposed `geometry_animation_map` key naming must align with what star-lord uses in D17/D22/D15 manifest cipher work. Is the geometry type naming agreed, or does it need joint alignment? **[Surface to star-lord via hive log as L2 coordination]**

5. **Creativ eKind shadow-tendril acquisition:** Shadow's geometry profile (tendril, void_pool, creep) is not well-served by Dark_Hole alone. Is CreativeKind shadow-tendril authorized as an additional acquisition alongside Frostwindz Deathbringer? Both address shadow VFX but from different registers (HD-2D shadow-tendril vs RETRO-pixel bone/death). **[Surface to Matt as L3 via knight-rider if shadow tendril gap is blocking]**

6. **Pixogen Lite register assessment:** The PixelArtRPGVFXLite pack is on-disk (`public/assets/PixelArtRPGVFXLite/`) with License.txt + Textures/. What is its register (HD-2D or retro-pixel)? Pixogen is described as "higher-resolution pixel composites" in the legolas research but the Lite pack may be lower-register than Full. **[Drax can inspect at implementation time; no blocking question]**

7. **Pimen thunder-spell-effect-03 pack naming:** This pack is titled "Thunder Spell Effect 03" but the substrate it will serve is `lightning`. The manifest tags it as `substrate: lightning`. Is there any tooling or process concern about the name mismatch (thunder pack → lightning substrate)? **[L1 in-seam — no issue; logged for awareness]**

---

## § 9 — Cross-References

- `agentic_orchestration/hive-mind/scope-of-work-phase-1-p1.md` § 1.5 (D19 definition)
- `canonical/story/substrate-expansion-decision-2026-05-17.md` (substrate set; § 3 naming; § 4 cosmology integration; § 5 VFX coupling)
- `canonical/story/substrate-identity-declarations-2026-05-17.md` (iconic_register + cosmological_commitment + geometry_affinities per substrate)
- `canonical/story/style-register.md` (HD-2D pixel-art register lock; per-register vendor classification; Candidate B rationale)
- `agentic_orchestration/CHANGELOG.md` 2026-05-17 entry (vendor acquisitions: CraftPix premium + Fellor Crystal + Frostwindz Deathbringer authorized; environment tileset track separate)
- `agentic_orchestration/research/knowledge/vfx-to-pool-expansion-opportunities-2026-05-17.md` (legolas reverse audit; TIER 1 candidates: holy GREEN-list at § 4.1; lightning GREEN-list; shadow GREEN-list; CreativeKind shadow-tendril identified)
- `agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl` (pimen thunder/fire/water/earth/wind/ice packs; basis for on-disk inventory)
- `agentic_orchestration/research/catalogue/creativekind/full-2026-05-16.jsonl` (CreativeKind holy-radiance + shadow-tendril catalogue entries)
- `agentic_orchestration/research/catalogue/fellor/full-2026-05-16.jsonl` (Fellor crystal catalogue)
- `agentic_orchestration/research/catalogue/frostwindz/full-2026-05-16.jsonl` (Frostwindz Deathbringer catalogue)
- `reincarnated-demo/public/assets/` (on-disk asset inventory basis for § 1)
- `reincarnated-loadout/AGENT_STATE.md` (drax seam checkpoint; v0.21 cipher consumption COMPLETE as prior state)

---

*Authored 2026-05-17 by drax-loadout under Phase-1 P1 hive-mind distributed authority (L1 in-seam). Planning phase COMPLETE. Implementation BLOCKED on Matt vendor acquisitions (CraftPix premium + Fellor Crystal + Frostwindz Deathbringer). Readiness for implementation: UNBLOCKED for Sub-phase A (chierit ZIP extraction + manifest authoring). BLOCKED for Sub-phase B (acquisition intake). BLOCKED for Sub-phase C holy/shadow/earth-organic/crystal VFX routing.*
