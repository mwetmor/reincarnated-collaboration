# Environment Tileset Vendor Scout — 2026-05-19 (F6 Track A)

**Mode:** B (systematic catalogue crawl)
**Commissioner:** knight-rider (F6 dispatch — VS2a Drift-15 environment tileset sweep; pre-approved batch 2026-05-19)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-19-legolas-vs2a-F6-drift15-environment-tileset-sweep.md`
**Framework:** `canonical/story/per-season-environmental-theming-2026-05-19.md` (F3; gandalf)
**Crawl date:** 2026-05-19
**Prior crawl reference:** `environment-tileset-vendor-scout-2026-05-17.md` (2026-05-17; methodology + Tier-1 findings)
**Time cap:** 8h (honored)
**JSONL output:** `agentic_orchestration/research/catalogue/environment-substrate-inventory-2026-05-19.jsonl`

---

## Section 1 — Crawl Strategy and Scope

### What the 2026-05-17 crawl established

The 2026-05-17 crawl executed the same Tier-1 vendor sweep and surfaced the core findings:

- **Pimen:** zero environment assets (VFX-only)
- **CreativeKind:** no tileset packs; individual prop structures only ($2–$3 each)
- **Ansimuz:** top-down assets exist but retro register and sidescroller-primary
- **Pipoya:** CC0 but exterior/overworld only; 48×48 option noted but theme mismatch
- **Foozle:** Lucifer Collection — CC0 stone dungeon + lava dungeon; retro register; genre-appropriate aesthetically (Diablo-era); free
- **Elthen:** 29+ packs at $10 each; retro-to-borderline register; strong thematic depth; license Patreon-linked
- **CraftPix:** Drift-13 filter applied; pixel packs retro register; subscription gating on best packs
- **Kokoro Reflections** (secondary discovery): 48×48 exact-meter-fit packs; Reaper/Phoenix/Naga/Wizard's Hideout/Snow Castle; HD-2D-adjacent pending visual inspection

Top candidate shortlist from 2026-05-17: Kokoro Reaper > Kokoro Phoenix > Elthen Cultist > Elthen Arcane > Kokoro Naga.

### What this 2026-05-19 crawl adds

1. **Updated Kokoro Reflections catalogue** — two new packs discovered not present in 2026-05-17 data:
   - **KR Elemental Dungeon Tiles** ($15.99; 42 MB) — fire/water/earth/wind elemental dungeons at 48×48; direct element-system alignment
   - **KR Heavenly Palace Tileset** ($16.99; 20 MB) — celestial/angelic palace; published ~14 days ago; wide prop coverage

2. **Elthen new pack verification** — Cave Tileset and Arctic Tileset confirmed; Swamp Tileset confirmed (4 color variants); all 32×32 retro register

3. **Tier-2 sweep supplement** — additional itch.io search pass executed; no new HD-2D-class vendors surfaced above Kokoro Reflections quality bar

4. **Register conclusion confirmed** — the 2026-05-17 register finding holds: HD-2D-class top-down dungeon tilesets remain scarce; Kokoro Reflections is the single clearest HD-2D-adjacent vendor; KR Elemental Dungeon is the most strategically significant new pack given its four-element structural alignment with Reincarnated's element system

### Style register target (unchanged from 2026-05-17)

Hand-drawn pixel-art (HD-2D-shaped), Candidate B per `canonical/story/style-register.md`. NOT retro Stardew/SNES-class. NOT vector. NOT anime hand-drawn raster. The target aesthetic: pixel-resolution art with hand-drawn illustration sensibility as shipped in Octopath Traveler / Sea of Stars / Eastward.

**Persistent register finding:** The top-down dungeon interior tileset landscape remains overwhelmingly retro pixel-art at 16×16 and 32×32. Kokoro Reflections (48×48) is the single vendor whose packs are most plausibly HD-2D-adjacent based on file size, prop depth, and reviewer description — but visual confirmation by gandalf is required. Elthen packs are stylistically above basic retro (their own description: "carefully crafted sprite work") but 32×32 tile dimension places them below HD-2D density target.

### Room dimension anchor (per `canonical/story/arena-room-hallway-system.md`)

PIXELS_PER_METER = 48. Target rooms: 720×720 (15m small), 1440×1440 (30m default), 2160×2160 (45m large).

Tile compatibility:
- **32×32 px tiles:** 0.667m/tile; 22.5 tiles/side in default room (non-integer — slight scale adjustment needed OR accept fractional tile at room edge)
- **48×48 px tiles:** 1.0m/tile (exact); 15 tiles/side in small room; 30 tiles/side in default room; 45 tiles/side in large room
- **64×64 px tiles:** 1.333m/tile; integer-compatible within tolerance

---

## Section 2 — Vendor-by-Vendor Scout (2026-05-19 Delta)

### 2.1 Tier-1 Vendors — Status vs 2026-05-17

Findings from 2026-05-17 are confirmed and inherited. No material changes to Tier-1 vendor coverage status. Summary:

| Vendor | Environment coverage | Status |
|---|---|---|
| **Pimen** | ZERO | SKIP — VFX-only catalogue confirmed |
| **CreativeKind** | Individual props only (~10–15 items $2–$3 each) | WATCH as prop-layer supplement; no tileset packs |
| **Ansimuz** | Retro; sidescroller-primary; Tiny RPG Dungeon top-down but 16×16 | SKIP for VS2a; CC0 dungeon noted for placeholder use |
| **Pipoya** | CC0; exterior/overworld only; 48×48 variant is only an overworld sheet | SKIP for interior room system |
| **Foozle** | Lucifer Collection: stone dungeon + lava dungeon at 32×32; CC0; retro register | CANDIDATE (secondary) — best free CC0 option; genre-appropriate aesthetically |
| **Elthen** | 29+ themed packs at $10; 32×32; retro-to-borderline | CANDIDATE POOL — deep thematic breadth; register borderline; tile variant counts unconfirmed |
| **CraftPix** | Mixed register; pixel packs retro; best packs subscription-gated | SECONDARY — free pack only viable without subscription; register not HD-2D |

### 2.2 Kokoro Reflections — Full Updated Catalogue (NEW packs confirmed 2026-05-19)

Kokoro Reflections is the primary HD-2D-adjacent vendor for environment tilesets. All packs ship at 48×48 px (32×32 also included). All explicitly state commercial use rights. No NFT. No AI stated.

**Full pack inventory (confirmed 2026-05-19):**

#### KR Elemental Dungeon Tiles — **NEW; PRIORITY ADDITION**
- URL: https://kokororeflections.itch.io/kr-elemental-dungeon-tiles
- Price: $15.99
- File size: 42 MB (eldun_fwew.zip) — largest content pack discovered
- Tile dimensions: 48×48 px primary (32×32 included)
- Perspective: Top-down (RPG Maker format confirmed)
- License: Commercial use rights included; no AI stated
- Coverage confirmed:
  - **Floor:** water, lava, poison water, basic ground, brick, concrete, special tile, transparent special tile, ground covers, crystals — per-element variants (fire/water/earth/wind)
  - **Wall:** brick, dark stone, cloud wall, two wall types per element (with decorative border / without), concrete
  - **Props:** dragon head statues, elemental-themed pillars, snake statues (left/right), jeweled pillars, torch bases, vertical/horizontal decorative spans, crystal piles, throne bases
  - **Functional/interactive:** bridges, doors (open/closed), windows (open/closed), magic rings, platforms, buttons, diamond decorations
  - **Special:** matching mega thrones across all four elements; sample RPG Maker maps included
- `primary_fit_seasons`: fire dungeon / lava domain / water palace / earth sanctum / wind temple / elemental cavern — maps directly to fire/water/earth/wind element seasons
- `deliverable_register`: pixel-art-raster
- **Strategic significance:** This is the single pack with four-element structural alignment matching Reincarnated's element system. One purchase covers four thematic season environments. The fire/water/earth/wind theming mirrors the game's canonical element taxonomy. At 42 MB this is likely the deepest content pack in the entire catalogue.

#### KR Legendary Palaces ~ Reaper Tileset
- URL: https://kokororeflections.itch.io/kr-legendary-palaces-reaper-tileset-for-rpgs
- Price: $9.99; file size: 8.5 MB
- Tile dimensions: 48×48 px (32×32 included)
- Coverage: floor (foggy gray / purple water / fancy tiles / spike traps / fog ground), wall (fog-wrapped types), props (stairs/pillars/arches/throne/windows/statues/chains/lanterns/gravestones), animated (treasure chest / black-white-purple torch variants), overlays (fog layers black+white, parallax background)
- `primary_fit_seasons`: death / undead palace / necromancer lair / dark cathedral / underworld domain / shadow realm
- `deliverable_register`: pixel-art-raster

#### KR Legendary Palaces ~ Phoenix Tileset
- URL: https://kokororeflections.itch.io/kr-legendary-palaces-phoenix-tileset-for-rpgs
- Price: $9.99; file size: 7.4 MB
- Tile dimensions: 48×48 px (32×32 included)
- Coverage: floor (lava / dark ground / fiery orange-edged / purple contrast / glittery fire paths / spike traps / fiery weeds), wall (dark / light / stone-brick orange tones), props (pillars/arches/throne/fire-windows/treasure box/statues/magic rings/lanterns), animated (chest / fire torches)
- `primary_fit_seasons`: fire / volcanic peak / phoenix rebirth / flame palace / lava domain
- `deliverable_register`: pixel-art-raster

#### KR Legendary Palaces ~ Naga Tileset
- URL: https://kokororeflections.itch.io/kr-legendary-palaces-naga-tileset-for-rpgs
- Price: $8.99; file size: 13 MB (largest in Legendary Palaces series)
- Tile dimensions: 48×48 px (32×32 included)
- Coverage: floor (water / marble black/teal/purple/gold / scale floors / scale gold-edged / decorative edges / spikes / pits / gold edging), wall (matching per floor type with coordinated roofs), props (stairs/pillars/arches/throne/windows/animated chest/push blocks/bridge rails/statues/magic rings/diagonal stairs/ladders ×3/snake wall decor/jewels)
- `primary_fit_seasons`: serpentine domain / water palace / jade sanctum / naga lair / underground river
- `deliverable_register`: pixel-art-raster

#### KR Snow Castle Tileset
- URL: https://kokororeflections.itch.io/kr-snow-castle-tileset-for-rpgs
- Price: $15.99; file size: 38 MB — includes regular + ruined variants
- Tile dimensions: 48×48 px (32×32 included)
- Coverage: floor (snow/dirt / water variants: blood + poison / lava / stone paths / rugs / spike traps / pits / fencing / ground covers / battlements), wall (brick and stone walls / roof tiles in plain stone + red + black + snow), props (stairs / chests / heraldry / flags / tapestries / torches / prison cells / kitchens / armory items / thrones / furniture / windows / pillars / towers / angled walls / doors / arches / trees / decorative), animated (levers / doors / flames / treasure chests), ruined variants of all above
- `primary_fit_seasons`: ice palace / winter domain / frost castle / snow sanctum / blizzard fortress / ruined fortress
- `deliverable_register`: pixel-art-raster
- Notes: Highest content depth of individual Kokoro packs at 38 MB. Regular + ruined variants provide visual variety for different dungeon states. $15.99 higher than Legendary Palaces series.

#### KR Heavenly Palace Tileset — **NEW; confirmed 2026-05-19**
- URL: https://kokororeflections.itch.io/kr-heavenly-palace-tileset-for-rpgs
- Price: $16.99; file size: 20 MB; published ~14 days ago (May 2026)
- Tile dimensions: 48×48 px (32×32 included)
- License: Commercial use permitted; no NFT/blockchain; games only
- Coverage: floor (grass / dirt / cloud animated / water / waterfalls / brick / tile / concrete / rugs / tables / fences), wall (brick/tile/concrete in plain+detailed with optional dark blue variants), props (trees / gates / pillars / domes / statues / chandeliers / candles / fireplaces / windows / bridges / thrones / fountains / beds / bookcases / curtains), animated (fire / fountains / glowing symbols / levers / gates / torches / treasure chests / doors)
- Rating: 5.0/5 stars (2 ratings; very new)
- `primary_fit_seasons`: celestial domain / angelic fortress / heavenly palace / divine sanctuary / light realm / Sun season / High Priestess / Justice
- `deliverable_register`: pixel-art-raster
- Notes: The animated cloud floor is distinctive. Divine/celestial theme fills a season-anchor gap not covered by other Kokoro packs. Richest prop list in the Kokoro catalogue (fountains, chandeliers, bookcases). Brand new pack — limited community validation yet.

#### KR Wizard's Hideout
- URL: https://kokororeflections.itch.io/kr-wizards-hideout-for-rpgs
- Price: $8.99; file size: 8.3 MB (v2); rating: 5.0/5 (5 reviews)
- Tile dimensions: 48×48 px (32×32 included)
- Coverage: floor (cavern floors), wall (cavern walls), props (colorful crystals / magical implements / potion bottles / shelving with books / crystal balls), lighting layer
- `primary_fit_seasons`: wizard cavern / hermit lair / scholar den / alchemist hideout / mystic cave
- `deliverable_register`: pixel-art-raster

### 2.3 New Tier-2 Additions — Not in 2026-05-17 Crawl

#### Yapability — Dungeon Tileset With Stage Objects (64×64)
- URL: https://yapability.itch.io/dungeon-tileset-with-stage-objects64x64
- Tile dimensions: 64×64 px
- License: Commercial and non-commercial use stated
- Coverage: floor, wall, stage objects (named in title)
- Note: Product page returned 429 on direct fetch; summary data from search snippet only. Register and exact content unconfirmed. 64×64 is integer-compatible with 48 px/m grid (1.333m/tile). Flag for follow-up fetch.
- `deliverable_register`: pixel-art-raster (inferred; unconfirmed)

#### Cainos — Pixel Art Top Down Basic (free)
- URL: https://cainos.itch.io/pixel-art-top-down-basic
- Price: Free (NWYP)
- Tile dimensions: 32×32 px
- License: Free + commercial; credit appreciated not required; no redistribution
- Coverage: floor (grass / stone ground), wall (wall tileset), props (48 props / grasses / trees / shadows)
- Theme: Outdoor grassy ruin (exterior — NOT dungeon interior)
- Register: Retro pixel art
- File size: 2.5 MB
- Notes: Exterior-only theme; not relevant for interior room system. Noted for VS2c+ open-air register.
- `deliverable_register`: pixel-art-raster

---

## Section 3 — Updated Top Candidate Packs (Cross-Vendor, Ranked)

Summary table for gandalf Track B shortlist authoring. All packs are top-down perspective, 48×48 unless noted.

### Candidate 1 — Kokoro Reflections: KR Elemental Dungeon Tiles ★ NEW PRIORITY

| Field | Value |
|---|---|
| Vendor | Kokoro Reflections |
| Pack name | KR Elemental Dungeon Tiles |
| URL | https://kokororeflections.itch.io/kr-elemental-dungeon-tiles |
| Price | $15.99 |
| License | Commercial use included; no AI stated |
| Tile dimensions | 48×48 px (32×32 included); exact 1m/tile at 48 px/m |
| File size | 42 MB |
| File format | RPG Maker MV/MZ + Unity/Godot/Tiled universal sheets |
| Coverage | floor ✓, wall ✓, props ✓, functional elements ✓, animated objects ✓ |
| Coverage tier | Full (floor + wall + props confirmed) |
| Sourcing category | TILESET |
| Room dimension fit | MULTI_BAND (estimated; 42 MB content depth strongly suggests) |
| `primary_fit_seasons` | fire dungeon / lava domain / water palace / earth sanctum / wind temple / elemental cavern |
| Season-anchor mapping | Fire → fire/volcanic seasons; Water → water/aquatic seasons; Earth → earth/mountain/stone seasons; Wind → wind/aerial/sky seasons |
| Style register | hand-drawn-pixel (HD-2D-adjacent; visual inspection required) |
| `deliverable_register` | pixel-art-raster |
| AI disclosure | None stated |
| Sample images | 5 preview thumbnails on product page |

**Why this is the new priority candidate:** The four-element structural design (fire/water/earth/wind, matching Reincarnated's element taxonomy) at $15.99 for 42 MB of 48×48 content is the single most strategically aligned pack found in either the 2026-05-17 or 2026-05-19 crawl. One purchase covers four season-anchor environments. The wall count per element (two wall types per element per documentation) is lower than Kokoro Reaper/Naga's wall variety — flag for gandalf visual inspection of whether two-wall-per-element is sufficient for default-room fill.

---

### Candidate 2 — Kokoro Reflections: KR Snow Castle Tileset ★ UPGRADED

| Field | Value |
|---|---|
| Vendor | Kokoro Reflections |
| Pack name | KR Snow Castle Tileset |
| URL | https://kokororeflections.itch.io/kr-snow-castle-tileset-for-rpgs |
| Price | $15.99 |
| License | Commercial use; see kokororeflections.com/terms-use/ |
| Tile dimensions | 48×48 px (32×32 included) |
| File size | 38 MB |
| Coverage | floor ✓ rich (10+ variants including snow/dirt/water/lava/stone/rugs/battlements), wall ✓ (brick+stone+roof variants), props ✓ rich (prison cells/kitchens/armory/thrones/heraldry/flags), animated ✓ (levers/doors/flames/chests) |
| Bonus | Regular + ruined variants of everything |
| Coverage tier | Full |
| `primary_fit_seasons` | ice palace / winter domain / frost castle / blizzard fortress / ruined keep / cold dungeon |
| Style register | hand-drawn-pixel (HD-2D-adjacent; visual inspection required) |
| `deliverable_register` | pixel-art-raster |

**Why upgraded:** 38 MB file size suggests deepest content among Legendary-Palaces-adjacent packs. Regular + ruined variants (2× the content) provide VS2a single-pack + VS2b variety without a second acquisition. Ice/winter theme fills a season-anchor the other Kokoro packs don't cover (death/fire/water/wizard/heavenly are covered; ice was the gap).

---

### Candidate 3 — Kokoro Reflections: KR Legendary Palaces ~ Reaper Tileset

| Field | Value |
|---|---|
| Vendor | Kokoro Reflections |
| Pack name | KR Legendary Palaces ~ Reaper Tileset |
| URL | https://kokororeflections.itch.io/kr-legendary-palaces-reaper-tileset-for-rpgs |
| Price | $9.99 |
| Tile dimensions | 48×48 px (32×32 included); 8.5 MB |
| Coverage | Full (floor + wall + props + animated + overlays/fog layers + parallax background) |
| `primary_fit_seasons` | death / undead palace / necromancer lair / dark cathedral / underworld domain / shadow realm |
| Style register | hand-drawn-pixel (HD-2D-adjacent) |
| `deliverable_register` | pixel-art-raster |

**Why this remains top-3:** Most distinctive atmosphere among the Legendary Palaces series — fog overlays + parallax background + multi-color torch animations (black/white/purple) are unique layering capabilities. Death/shadow theme maps strongly to Tarot-anchored season vocabulary (Death card, Tower card, Hermit card with cave variant). Lowest price in the series at $9.99.

---

### Candidate 4 — Kokoro Reflections: KR Heavenly Palace Tileset ★ NEW

| Field | Value |
|---|---|
| Vendor | Kokoro Reflections |
| Pack name | KR Heavenly Palace Tileset |
| URL | https://kokororeflections.itch.io/kr-heavenly-palace-tileset-for-rpgs |
| Price | $16.99 |
| Tile dimensions | 48×48 px (32×32 included); 20 MB |
| Coverage | Full; richest prop list in Kokoro catalogue (fountains, chandeliers, domes, bookcases, curtains, animated clouds) |
| `primary_fit_seasons` | celestial domain / angelic fortress / divine sanctuary / light realm / heavenly palace |
| Season-anchor mapping | Sun / Justice / High Priestess / Strength / Star tarot anchors |
| Style register | hand-drawn-pixel (HD-2D-adjacent; very new pack — limited community validation) |
| `deliverable_register` | pixel-art-raster |
| Note | Published ~14 days ago; 5.0/5 but only 2 ratings |

---

### Candidate 5 — Kokoro Reflections: KR Legendary Palaces ~ Naga Tileset

| Field | Value |
|---|---|
| Vendor | Kokoro Reflections |
| Pack name | KR Legendary Palaces ~ Naga Tileset |
| URL | https://kokororeflections.itch.io/kr-legendary-palaces-naga-tileset-for-rpgs |
| Price | $8.99 |
| Tile dimensions | 48×48 px (32×32 included); 13 MB (largest in Legendary Palaces) |
| Coverage | Full; richest floor variety in Legendary Palaces (water + 4 marble types + scale variants) |
| `primary_fit_seasons` | serpentine domain / water palace / jade sanctum / underground river |
| Style register | hand-drawn-pixel (HD-2D-adjacent) |
| `deliverable_register` | pixel-art-raster |

---

### Candidate 6 — Kokoro Reflections: KR Legendary Palaces ~ Phoenix Tileset

| Field | Value |
|---|---|
| Vendor | Kokoro Reflections |
| Pack name | KR Legendary Palaces ~ Phoenix Tileset |
| URL | https://kokororeflections.itch.io/kr-legendary-palaces-phoenix-tileset-for-rpgs |
| Price | $9.99 |
| Tile dimensions | 48×48 px (32×32 included); 7.4 MB |
| Coverage | Full (floor/wall/props/animated) |
| `primary_fit_seasons` | fire / volcanic peak / phoenix rebirth / flame palace / lava domain |
| Style register | hand-drawn-pixel (HD-2D-adjacent) |
| `deliverable_register` | pixel-art-raster |
| Note | Now secondary to KR Elemental Dungeon for fire-season coverage — Elemental Dungeon's fire part covers similar theme at higher content depth |

---

### Candidate 7 — Elthen: 2D Pixel Art Cultist Dungeons Tileset

| Field | Value |
|---|---|
| Vendor | Elthen's Pixel Art Shop |
| Pack name | 2D Pixel Art Cultist Dungeons Tileset |
| URL | https://elthen.itch.io/2d-pixel-art-cultist-dungeons-tileset |
| Price | $10 (or $160 bundle of 31) |
| Tile dimensions | 32×32 px |
| Coverage | floor, wall, props (orb/sword statues, braziers), animated (occult rotating pillars ×8 symbols, stone gates, 3 portal variants, spike/spear traps) |
| `primary_fit_seasons` | occult ritual / dark magic lair / forbidden temple / void ceremony / cultist shrine |
| Style register | pixel-art retro-to-borderline |
| `deliverable_register` | pixel-art-raster |

**Why still in top 10:** The rotating occult pillars with 8 symbols and 3 portal variants are unique prop assets not found in the Kokoro catalogue. The dark-cult/forbidden-ceremony thematic is distinct from death-palace (Reaper) or elemental dungeon. If the VS2a season anchor has occult/ceremonial framing, this pack's animated prop set may be preferable to higher-register alternatives.

---

### Candidate 8 — Elthen: 2D Pixel Art Arcane Dungeons Tileset

| Field | Value |
|---|---|
| Vendor | Elthen's Pixel Art Shop |
| Pack name | 2D Pixel Art Arcane Dungeons Tileset |
| URL | https://elthen.itch.io/2d-pixel-art-arcane-dungeons-tileset |
| Price | $10 (or $160 bundle) |
| Tile dimensions | 32×32 px; 125 kB total |
| Coverage | floor, wall, props, animated (energy pipes, magical barriers, torches, crystals, levers) |
| `primary_fit_seasons` | arcane tower / mage sanctum / magical laboratory / enchanted ruins |
| Style register | pixel-art retro-to-borderline |
| `deliverable_register` | pixel-art-raster |

---

### Candidate 9 — Foozle Lucifer: Dungeon Tileset (free CC0 baseline)

| Field | Value |
|---|---|
| Vendor | Foozle (foozlecc.itch.io) |
| Pack name | Lucifer — Dungeon Tileset |
| URL | https://foozlecc.itch.io/lucifer-dungeon-tileset |
| Price | Free (NWYP) |
| License | CC0 1.0 — no attribution required; commercial unrestricted |
| Tile dimensions | 32×32 px; 149 kB; Aseprite source files |
| Coverage | floor, wall, dungeon environmental elements |
| `primary_fit_seasons` | stone dungeon / dark crypt / generic dungeon |
| Style register | pixel-art retro (Diablo-era aesthetic) |
| `deliverable_register` | pixel-art-raster |

**Why this stays in the list:** CC0 makes it ideal for immediate drax pipeline integration testing before paid packs are acquired. Aseprite source enables modification. Genre alignment (Diablo-era aesthetic) is strong. Recommendation: acquire free as placeholder while Track B/C selection proceeds.

---

### Candidate 10 — Kokoro Reflections: KR Wizard's Hideout

| Field | Value |
|---|---|
| Vendor | Kokoro Reflections |
| Pack name | KR Wizard's Hideout |
| URL | https://kokororeflections.itch.io/kr-wizards-hideout-for-rpgs |
| Price | $8.99; file size: 8.3 MB (v2); rating: 5.0/5 (5 reviews) |
| Tile dimensions | 48×48 px (32×32 included) |
| Coverage | floor (cavern), wall (cavern), props (crystals/magical implements/potion bottles/shelving/crystal balls), lighting layer |
| `primary_fit_seasons` | wizard cavern / hermit lair / scholar den / alchemist hideout / mystic cave |
| Style register | hand-drawn-pixel (HD-2D-adjacent) |
| `deliverable_register` | pixel-art-raster |

---

## Section 4 — Season-Anchor Coverage Map

Cross-referencing Reincarnated's Tarot-derived season anchors (per `canonical/story/cosmology-reincarnated.md`) against the candidate inventory:

| Season anchor | Compatible themes from candidate pool | Best candidate pack(s) |
|---|---|---|
| **Death** | abandoned ruin / crypt / overgrown graveyard / ossuary / undead palace | Kokoro Reaper (death/shadow/undead palace) |
| **Tower** | broken citadel / shattered keep / collapsing parapets / ruined fortress | Kokoro Snow Castle (ruined variant) |
| **Hermit** | cave / cathedral interior / monastic chamber / secluded grotto / wizard lair | Kokoro Wizard's Hideout; Elthen Cultist Dungeons |
| **Sun** | volcanic peak / sun-baked ruin / golden desert / celestial domain | Kokoro Phoenix (fire/volcanic); Kokoro Heavenly (celestial) |
| **Waxing Crescent** | new-growth forest / dawn meadow / first-light shore / spring ruin | Val Sama 66 Spring Ruins (secondary; wall-variety gap) |
| **Full Moon** | moonlit forest / night ruin / silver-hued plateau | No strong primary match — COVERAGE GAP; see Findings-Blockers |
| **Capricorn** | mountain peak / cold crag / high-altitude shrine / ice palace | Kokoro Snow Castle (winter/frost/ice palace) |
| **Hanged Man** | overgrown gallows / suspended platforms / inverted spaces | No strong primary match — COVERAGE GAP |
| **Fire element** | lava domain / volcanic dungeon / flame palace | KR Elemental Dungeon (fire part); Kokoro Phoenix; Elthen Lava Dungeons |
| **Water element** | water palace / aquatic sanctum / underground river | KR Elemental Dungeon (water part); Kokoro Naga |
| **Earth element** | stone dungeon / dwarven cave / earth sanctum / mountain interior | KR Elemental Dungeon (earth part); Elthen Dwarven Caves |
| **Wind element** | sky temple / cloud palace / aerial sanctum | KR Elemental Dungeon (wind part; cloud wall tiles noted) |
| **Dark/Void/Occult** | forbidden temple / void ceremony / cultist shrine | Elthen Cultist Dungeons |
| **Magic/Arcane** | mage sanctum / ley-line nexus / arcane tower | Elthen Arcane Dungeons; Kokoro Wizard's Hideout |

**Season anchors with NO strong coverage:** Full Moon (moonlit/silver) and Hanged Man (suspended/inverted) have no direct candidate pack match. These would require: (a) creative reuse of an existing pack with palette modification, or (b) Tier-2 sweep targeting specific themes, or (c) LLM-generated custom content.

---

## Section 5 — Findings-Blockers (Updated)

### Blocker 1 — HD-2D register confirmation still required via visual inspection

**Unchanged from 2026-05-17.** The top-down dungeon interior tileset landscape lacks a vendor that clearly matches the HD-2D register without visual confirmation. Kokoro Reflections is the strongest candidate but no pack has been formally confirmed as HD-2D-register by gandalf. File sizes (8–42 MB) and prop depth suggest above-retro quality; visual confirmation is the blocking gate before any pack can be presented as a valid VS2a candidate at the locked register.

**Recommended resolution:** Gandalf examines sample images from Kokoro product pages (all accessible without purchase) to give a binary HD-2D-pass/flag for each pack. Given the track record (KR Lizardfolk Temple previously assessed as "hand-drawn pixel art at moderate-to-high fidelity"), the probability of at least one Kokoro pack passing the visual gate is high. If none pass, Path A/B per 2026-05-17 Blocker 1 applies.

### Blocker 2 — KR Elemental Dungeon wall count per element

The KR Elemental Dungeon documentation states "two wall types per element (with decorative border / without)" — this is at or near the UNDER_VARIETY threshold for default-room wall coverage (≥6 required; 2 documented). However, with four elements × 2 wall types = 8 wall type variants in the total pack. For a single-element season room, the 2-type per-element wall count may produce visible repetition at the 30-tile-wide default room scale.

**Recommended resolution:** Gandalf assess whether 2 wall types per element (with/without decorative border variation) is visually sufficient for a 30×30-tile default room, or whether the pack's wall depth requires pairing with a supplement. If the two wall types have sufficient visual differentiation (e.g., one heavily decorated vs one plain), repetition at room scale may be acceptable.

### Blocker 3 — Tile variant counts for Elthen packs (unchanged)

Elthen packs document animated prop richness but not floor/wall tile variant counts. All Elthen packs are categorized as UNDER_VARIETY until download-confirmed. Small file sizes (23–125 kB) for Elthen packs suggest limited tile sets; paid acquisition at $10 required for variant-count verification.

**Recommended resolution:** Acquire Elthen Dungeon (free) for pipeline testing + 1–2 thematic packs ($10 each) at Track B to verify variant counts. Total cost ≤$30 for verification.

### Blocker 4 — Season-anchor coverage gaps (Full Moon, Hanged Man)

No candidate pack directly maps to "moonlit/silver" (Full Moon) or "suspended/inverted" (Hanged Man) season anchors. These are secondary anchors and VS2a ships only one pack — if the VS2a target season has one of these anchors, a custom sourcing pass would be needed.

**Recommended resolution:** At Track B shortlist time, gandalf confirms which season is the VS2a target. If Full Moon or Hanged Man, surface as Tier-2 sweep requirement. If any other anchor, existing candidate pool covers it.

### Blocker 5 — KR Heavenly Palace is brand new (limited community validation)

Published ~14 days ago; only 2 ratings at time of crawl. The pack's actual content depth and technical quality are unvalidated by the community.

**Recommended resolution:** Defer Heavenly Palace to VS2b+ unless the VS2a season anchor specifically requires celestial/divine theming. The Legendary Palaces series (Reaper/Phoenix/Naga) and Elemental Dungeon have stronger community validation records.

---

## Section 6 — Tier-1 Coverage Sufficiency Assessment

**Is Tier-1 sufficient? YES with register caveat.**

The Kokoro Reflections catalogue (with the KR Elemental Dungeon addition) provides:
- Sufficient seasonal breadth: fire / water / earth / wind / death / shadow / ice / winter / wizard / celestial themes all covered
- Sufficient dimensional fit: all packs at 48×48 (exact 1m/tile at project scale)
- Sufficient license clarity: commercial use explicitly stated on all packs
- Sufficient prop coverage: Full-tier coverage (floor + wall + props) confirmed on all major packs
- Sufficient content depth (by file size proxy): 8–42 MB packs vs Elthen's 23–125 kB range

**Register is the open question, not breadth.** A Tier-2 sweep is NOT recommended at this stage — the recommendation is gandalf visual inspection of Kokoro packs as the rate-limiting step.

**Tier-2 sweep recommendation:** Defer unless gandalf's Track B visual inspection finds that NO Kokoro pack passes the HD-2D register gate. If that occurs, Tier-2 priority sweep vendors: Szadi Art (itch.io), Raou TDRPG Interior ($18 / 400+ tiles), Phantom Cooper Aesthetic Biomes (24×24), and the Yapability 64×64 pack (pending fetch confirmation).

---

## Section 7 — Source List

All sources accessed 2026-05-19 unless noted as inherited from 2026-05-17.

**2026-05-19 new fetches:**
- https://kokororeflections.itch.io/ (catalogue browse)
- https://kokororeflections.itch.io/kr-elemental-dungeon-tiles (fetched 2026-05-19)
- https://kokororeflections.itch.io/kr-heavenly-palace-tileset-for-rpgs (fetched 2026-05-19)
- https://kokororeflections.itch.io/kr-snow-castle-tileset-for-rpgs (fetched 2026-05-19)
- https://elthen.itch.io/ (catalogue browse; confirmed current pack list 2026-05-19)
- https://elthen.itch.io/cave-tileset (fetched 2026-05-19)
- https://elthen.itch.io/2d-pixel-art-arctic-tileset (fetched 2026-05-19)
- https://elthen.itch.io/2d-pixel-art-swamp-tileset (fetched 2026-05-19)
- https://cainos.itch.io/pixel-art-top-down-basic (fetched 2026-05-19)
- https://itch.io/game-assets/tag-dungeon/tag-top-down (fetched 2026-05-19)
- https://craftpix.net/categorys/pixel-art-tilesets/ (fetched 2026-05-19)
- Web searches (2026-05-19): 2× — "itch.io top-down dungeon tileset 48x48 HD-2D pixel art commercial 2026"; "itch.io hand-drawn pixel HD-2D top-down dungeon tileset commercial 48x48 2025 2026"

**Inherited from 2026-05-17 (see environment-tileset-vendor-scout-2026-05-17.md § Source List for full URLs):**
Pimen catalogue / Elthen catalogue / Ansimuz catalogue / Foozle catalogue / Pipoya catalogue / CreativeKind catalogue / CraftPix pixel tilesets / Foozle Lucifer Dungeon / Foozle Lucifer Lava Dungeon / Seliel catalogue / Kokoro Reaper/Phoenix/Naga/Wizard product pages / Val Sama 66 Spring Ruins / PIXELHUNT 135 Backgrounds / Miguelsgp 64×64 Dungeon / Itch.io tag pages (dungeon+top-down, dungeon+tileset, dark-fantasy+top-down)

---

*Filed by legolas, 2026-05-19. All data is read-only from public sources. No assets acquired. Track B (gandalf shortlist) gated on this filing.*
