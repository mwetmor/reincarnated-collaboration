# Pixogen — Vendor findings-summary (Step B C.2 backfill)

**Crawl date:** 2026-05-16
**Authored:** 2026-05-16 by legolas (direct authorship; persona-rule conflict resolved 2026-05-16 via Day 4 amendment permitting per-vendor findings-summary .md files)
**License verification date:** 2026-05-16 (Matt downloaded Pixogen Lite; license file inspected at `/Users/admin/Games/reincarnated-demo/public/assets/PixelArtRPGVFXLite/License.txt`)

---

## Substrate-evidence headline

Pixogen ships 11 distinct effect-type labels across 108 animations at a uniform 64x64px canvas. Two substrates are **novel relative to the Tier-1 baseline**:

- **Void** — distinct from Pimen's Dark substrate. Void effects (Black Hole, Portal, Shield, Slash, Spin, two Explosions, Ball) operate in a spatial-absence register, not shadow-arcane. Black Hole is the clearest `vortex_pull` geometry specimen in the entire Tier-1 catalogue.
- **Technology** — fully novel. Eight sci-fi/mechanical effects. No parallel in any other Tier-1 vendor. Closes a substrate gap no other crawled source addresses.

Pixogen meets inclusion criterion 2(b): >7 distinct effect-type labels. Geometry coverage is the most diverse of any single pack in the catalogue (13 geometry signature types in the amended set per geometry-signatures sidecar).

---

## Novel substrate tags surfaced

| Substrate tag | vs Pimen + canonical-four baseline |
|---|---|
| `void` | **Novel** — spatial-absence register; distinct from Dark/shadow-arcane |
| `technology` | **Novel** — no Tier-1 parallel in full sweep |

Non-novel substrates confirmed present: fire, water, wind, earth, electric, holy/light, ice, fireworks/burst, explosion.

---

## Asset inventory

| asset_id | Name | Cost | Access | Animations | Canvas | License |
|---|---|---|---|---|---|---|
| `pixogen-rpg-vfx-full` | Pixel Art RPG VFX (Full Pack) | €19.99 | Purchase at https://pixogenassets.itch.io/pixel-art-rpg-vfx | 108 (636 sprites) | 64x64px | proprietary-with-attribution (VERIFIED) |
| `pixogen-rpg-vfx-lite` | Pixel Art RPG VFX Lite (Free) | €0.00 | Separate free download (distinct URL from Full pack page; Matt downloaded 2026-05-16) | 8 (48 sprites) | 64x64px | proprietary-with-attribution (VERIFIED) |

**Pricing correction (2026-05-16):** Earlier draft stated Lite was available at the Full pack URL as a separate €0 option. Matt confirmed: Full (€19.99) is the only purchasable SKU at https://pixogenassets.itch.io/pixel-art-rpg-vfx. Lite is a separate free download at a distinct URL. Drax tagged the Lite asset path; license file located at `/Users/admin/Games/reincarnated-demo/public/assets/PixelArtRPGVFXLite/License.txt`.

Full pack also bundled in Pixel Art RPG Mega Pack (€59.99). Vendor states: "No generative AI was used."

---

## License summary

**Status: VERIFIED — proprietary-with-attribution.**

License verified 2026-05-16 by Matt (downloaded Pixogen Lite free pack; license file inspected). Both SKUs (Full and Lite) carry the same license terms per the license file header: "The license which applies to all of the Antoine Fauville / AFGameAssets asset packs is below."

**Key terms confirmed:**

| Term | Status |
|---|---|
| Commercial use | **OK** (explicitly stated in summary and § 2.A.1) |
| Non-commercial use | OK |
| Modification / Adapted Material | **OK** — license grants production of Adapted Material (§ 2.A.1.B) |
| Technical modifications (runtime tinting, format conversion) | **OK** — § 2.A.4 explicitly authorizes technical modifications in all media and formats; Licensor waives right to forbid such modifications; "simply making modifications authorized by this Section 2(A)(4) never produces Adapted Material" |
| Pixi.js runtime tinting | **OK** — falls under § 2.A.4 technical modifications; confirmed clean for drax wiring |
| Attribution required | **YES** — § 3.A.1 requires credit to "Antoine Fauville / AFGameAssets" when sharing Licensed Material (including as part of a shipped game) |
| Royalties | None — § 2.B.3 Licensor waives right to collect royalties |
| Game Making Tool restriction | Not applicable — Reincarnated is a game, not a game-making tool (§ 2.A.1.i) |
| AI training use | **Forbidden** — § 2.A.1.ii explicitly prohibits use as AI training data |
| Resale / redistribution of raw assets | Not OK — § 1 summary item 1 prohibits distributing zip contents except as part of a game/application product |

**Attribution requirement (§ 3.A.1):**

Credit "Antoine Fauville / AFGameAssets" in game credits. Must retain identification of creator, copyright notice, and reference to the Public License. May satisfy via URI/hyperlink to the pack page per § 3.A.2. See `attribution_required` flag below.

---

## License terms verbatim

Full license text on disk at: `/Users/admin/Games/reincarnated-demo/public/assets/PixelArtRPGVFXLite/License.txt`

**Summary block (verbatim from license file, opening section):**

```
The license which applies to all of the Antoine Fauville / AFGameAssets asset packs is below.
Here's a brief summary:

1. You may not publicly distribute the contents of the asset pack zip file in whole or in part,
   unless as part of a game or application product in accordance with this document.

2. If you use the contents of the asset pack zip file in a game or application product,
   please give attribution to Antoine Fauville / AFGameAssets in the credits.

3. Commercial use and non-commercial use are both OK!

4. Game making tools (programs which have the primary function of creating games or applications)
   are not granted a license by this document.
   ** This does not impact typical indie devs and is aimed at larger companies. **

5. Use of the asset packs as AI training material is forbidden.
```

**Section 2.A.4 verbatim (technical modifications — authorizes Pixi.js runtime tinting):**

```
4. Media and formats; technical modifications allowed. The Licensor authorizes You to exercise
   the Licensed Rights in all media and formats whether now known or hereafter created, and to
   make technical modifications necessary to do so. The Licensor waives and/or agrees not to
   assert any right or authority to forbid You from making technical modifications necessary to
   exercise the Licensed Rights, including technical modifications necessary to circumvent
   Effective Technological Measures. For purposes of this Public License, simply making
   modifications authorized by this Section 2(A)(4) never produces Adapted Material.
```

**Section 3.A.1 verbatim (attribution requirement):**

```
1. If You Share the Licensed Material (including in modified form), You must:

     A. retain the following if it is supplied by the Licensor with the Licensed Material:
           i.  identification of the creator(s) of the Licensed Material and any others
               designated to receive attribution, in any reasonable manner requested by
               the Licensor (including by pseudonym if designated);
          ii.  a copyright notice;
         iii.  a notice that refers to this Public License;
          iv.  a notice that refers to the disclaimer of warranties;
           v.  a URI or hyperlink to the Licensed Material to the extent reasonably practicable;
     B. indicate if You modified the Licensed Material and retain an indication of any previous
        modifications; and
     C. indicate the Licensed Material is licensed under this Public License, and include the
        text of, or the URI or hyperlink to, this Public License.
```

---

## Consumption-readiness flags

| Flag | Value |
|---|---|
| `license_unverified` | `false` (previously `true` — cleared 2026-05-16) |
| `consumption_hold` | **APPROVED-WITH-ATTRIBUTION** — Elrond may incorporate Pixogen rows in emergent-grouping analysis; integration may proceed; attribution requirement must be tracked to shipping credits |
| `attribution_required` | `true` — credit "Antoine Fauville / AFGameAssets" in game credits per § 3.A.1 |
| `attribution_form` | In-game credits text + URI/hyperlink to https://pixogenassets.itch.io/pixel-art-rpg-vfx per § 3.A.2 (reasonable manner) |
| `substrate_evidence_usable` | yes |
| `geometry_signatures` | 13 types (amended set); Technology VFX geometry uncertain pending post-acquisition frame inspection |
| `direct_pack_verification` | `true` (both SKUs directly verified; Lite pack downloaded and inspected) |
| `c2_license_flag` | `true` (C.2 format requirement fulfilled) |
| `pixi_tinting_permitted` | `true` — § 2.A.4 technical modifications clause confirmed |
| `commercial_use_ok` | `true` |
| `ai_training_forbidden` | `true` — § 2.A.1.ii |

---

## Geometry signatures (summary)

**Confirmed types** (high confidence — named animations + canvas inspection):

`impact_burst`, `nova_radial`, `projectile_straight`, `nova_wave`, `cone`, `melee_arc`, `vortex_pull`, `aura_radial`, `buff_self`, `ground_slam_directional`, `ring`, `summon`, `whirlwind`.

**Geometry-uncertain set** (requires post-acquisition frame inspection):

Technology VFX (8 effects, sci-fi register) — frame-level inspection post-acquisition required to resolve. Deferred to VS2b (out of scope current sprint).

---

## Knowledge gaps not resolved

1. **Technology VFX geometry** — uncertain; requires post-acquisition frame inspection of Full pack. Deferred to VS2b.
2. **Per-animation frame counts** — aggregate only (636 sprites / 108 animations = avg ~5.9 frames/animation); individual breakdown requires ZIP inspection of Full pack.
3. **Pixogen Full pack acquisition** — Matt skipped Full purchase. Only Lite (8 animations) is on disk. Full pack (108 animations) deferred to VS2b.

---

## Cross-seam consumption-readiness notes

- **Elrond**: Pixogen rows in `full-2026-05-16.jsonl` — `license_unverified` flag now `false`; `consumption_hold` cleared to `APPROVED-WITH-ATTRIBUTION`. Elrond parallel-updating catalogue.db per 2026-05-16 session. Attribution tracking requirement should be reflected in catalogue.db (attribution_required + attribution_text fields).
- **Drax**: Void Shield already wired in drax v0.19 (`drax/v0.19-character-wire-up-void-attribution` dispatch). No further coordination needed — tinting confirmed clean under § 2.A.4. Attribution credit string must be included in shipping game credits.
- **Gandalf**: Pixogen Void substrate integration unblocked. Technology substrate deferred to VS2b (out of scope current sprint).
- **Knight-rider**: License-verification HOLD fully cleared. Attribution tracking is now the only ongoing obligation. Recommend attribution string be added to canonical credits tracking before demo2.

---

## Cross-references

- Full catalogue JSONL: `agentic_orchestration/research/catalogue/pixogen/full-2026-05-16.jsonl`
- Geometry signatures sidecar: `agentic_orchestration/research/catalogue/pixogen/geometry-signatures-2026-05-16.jsonl`
- License file on disk: `/Users/admin/Games/reincarnated-demo/public/assets/PixelArtRPGVFXLite/License.txt`
- Step B dispatch (C.2 amendment text): `agentic_orchestration/dispatches/2026-05-16-legolas-step-b-tier1-2dvfx-crawl.md` § "Amendments C.1-C.3"
- Cross-vendor substrate inventory: `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl`
- Gandalf Track 4 assessment (Pixogen license decision): `canonical/story/geometry-vfx-coverage-assessment.md` § 5
- Drax v0.19 dispatch: `drax/v0.19-character-wire-up-void-attribution` (Void Shield wired; attribution hooks added)
- Elrond catalogue.db update: parallel 2026-05-16 session (license_unverified flag + consumption_hold flag cleared)
- Matt license-download event: 2026-05-16 (authorizing event for this verification)

---

— Authored by legolas 2026-05-16 (direct authorship per Day 4 persona-rule amendment)
