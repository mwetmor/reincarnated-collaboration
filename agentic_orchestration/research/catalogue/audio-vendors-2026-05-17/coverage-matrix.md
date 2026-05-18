# Audio Coverage Gap Matrix — 2026-05-17

**Legolas Mode B** | Commissioner: knight-rider (Matt L3 auth 2026-05-17)
**Scope:** 24 geometry_types × 8 elements + UI events + death tiers + biomes + music

**Key:**
- GREEN — multiple strong candidates from CC0 / CC-BY / commercial vendors
- YELLOW — limited candidates; some quality concerns or vendor risk
- RED — no clean candidate; commission or generative path needed

**Density note:** SFX coverage is shared across geometry+element pairs. A single "fire projectile" SFX may serve `projectile+fire`, `multi_projectile+fire`, `fork+fire`, `ricochet_bounce+fire` because they share the same sonic signature (projectile-travel + fire-element). The matrix uses ARCHETYPE GROUPS to reflect this: geometry types that share the same sonic signature are grouped for coverage purposes. This reduces the effective 192-cell matrix (24×8) to ~40-50 distinct sonic slots.

---

## Section 1 — Skill SFX: Geometry × Element

### Geometry Archetype Groups

| Group | Geometry Types in Group | Shared Sonic Signature |
|---|---|---|
| G1 — PROJECTILE | `projectile`, `multi_projectile`, `fork`, `ricochet_bounce` | Whoosh + impact (varies by element) |
| G2 — MELEE | `melee_strike`, `melee_arc`, `whirlwind`, `dash_attack`, `leap_strike` | Swing + impact + body thud |
| G3 — SINGLE-TARGET | `single_target`, `chain_lightning` (partial) | Cast beam + impact hit |
| G4 — AREA | `circle`, `ground_targeted_circle`, `cone`, `ring` | Explosion radius / expanding sound |
| G5 — LINE/BEAM | `line`, `beam_channel` | Channeled sustained beam hum |
| G6 — MOVEMENT | `teleport`, `blink`, `defensive_dash` | Pop/displacement sound |
| G7 — PERSISTENT | `aura`, `totem` | Loop/ambient hum |
| G8 — SLAM | `ground_slam`, `vortex_pull` | Ground impact / pull roar |
| G9 — BUFF | `self_buff`, `self_cast` | Internal cast / buff chime |

### Per-element × per-group coverage

Legend: vendor shortcodes used
- **WS3** = WOW Sound RPG Magic SFX Pack 3 Elemental ($99)
- **WSP** = WOW Sound Pixel Magic SFX Pack ($49)
- **FH** = Fusehive Medieval Fantasy Magic Library ($100)
- **WS1** = WOW Sound RPG Magic SFX Pack 1 ($35)
- **LEO** = Leohpaz RPG Essentials SFX Free ($0)
- **TOM** = TomMusic Free Fantasy 200 ($0)

| Element | G1 PROJECTILE | G2 MELEE | G3 SINGLE-TARGET | G4 AREA | G5 BEAM | G6 MOVEMENT | G7 AURA | G8 SLAM | G9 BUFF |
|---|---|---|---|---|---|---|---|---|---|
| **fire** | GREEN (WS3/WSP/FH/WS1/LEO) | YELLOW (WS1 layered; no labeled fire-melee) | GREEN (WS3/FH) | GREEN (WS3/FH/LEO) | GREEN (WS3/FH) | YELLOW (WS1 generic cast) | GREEN (WS3/WSP) | YELLOW (WS1 impact; no slam-specific fire) | GREEN (WS3/WS1 buffs) |
| **water** | GREEN (WS3/FH/WS1) | YELLOW (layered; water-melee not explicit) | GREEN (WS3/FH) | GREEN (WS3/FH) | GREEN (WS3/FH) | YELLOW (WS1 generic) | YELLOW (FH atm only) | RED (no water-slam candidates) | YELLOW (WS1 heal layer) |
| **earth** | YELLOW (WS3 6-file earth; FH stone/lava) | YELLOW (limited earth-melee; WS1 impact layer) | YELLOW (WS3 generic + earth; FH) | GREEN (WS3/FH ground AoE) | RED (no earth-beam specific) | YELLOW (FH generic) | YELLOW (FH stone hum) | GREEN (WS3 earth + FH lava) | YELLOW (WS1 layered) |
| **wind** | GREEN (WS3/WSP/FH/WS1) | YELLOW (wind-melee not explicit; ELV Wind) | GREEN (WS3/FH) | GREEN (WS3/FH wind AoE) | YELLOW (WS3 wind beam) | GREEN (WSP/FH displacement) | YELLOW (WS3 wind pad) | YELLOW (FH storm; no slam-specific) | YELLOW (WS3 wind buff) |
| **lightning** | GREEN (WS3/FH/WS1/ELV pack 8) | YELLOW (lightning-melee not explicit) | GREEN (WS3/FH chain-lightning) | GREEN (WS3/FH storm/electricity) | GREEN (WS3/FH beam) | YELLOW (WS3 discharge snap) | GREEN (WS3/FH electricity) | YELLOW (FH storm slam) | YELLOW (WS3 lightning buff) |
| **holy** | GREEN (WS3 Light/FH Divine) | YELLOW (holy-melee not explicit) | GREEN (WS3/FH divine) | GREEN (FH divine AoE) | GREEN (WS3/FH holy beam) | YELLOW (WS3/FH generic displacement) | GREEN (WS3 Light aura / FH divine hum) | RED (no holy-slam candidates) | GREEN (WS1 heal/revive / WS3 buff) |
| **shadow** | GREEN (WS3 Dark / FH Dark / WSP Dark) | YELLOW (shadow-melee not explicit) | GREEN (WS3/FH dark) | GREEN (WS3/FH dark explosion) | GREEN (WS3/FH dark beam) | YELLOW (WS3 dark teleport) | GREEN (WS3/WSP/FH dark aura) | YELLOW (FH dark slam) | YELLOW (WS3/WS1 debuff layer) |
| **physical** | GREEN (Kenney Impact / TOM bow+sword / OGA packs) | GREEN (Kenney Impact / TOM / OGA / Leohpaz dungeon) | YELLOW (Kenney Impact; no ST-physical specific) | YELLOW (Kenney explosions; limited) | RED (no physical beam) | YELLOW (Leohpaz dash/evade) | RED (no physical aura loop) | GREEN (Kenney Impact ground hits) | YELLOW (TOM foley) |

**RED cell summary — Skill SFX:**
- water+slam: no candidates
- earth+beam (channeled): no candidates
- holy+slam: no candidates
- physical+beam: no candidates
- physical+aura: no candidates

**YELLOW cell summary (high-priority):**
Most melee×element combinations have WS1 layered options (cast layer + impact layer) but no explicitly pre-labeled fire-melee or water-melee sounds. For the pixel-art register specifically, WSP covers most non-physical elements but has thin earth (6) and water (4) coverage.

---

## Section 2 — UI Events

| UI Event | Status | Candidate vendors |
|---|---|---|
| button-click | GREEN | Kenney Interface (CC0, 100 files) + Kenney UI Audio (CC0, 50 files) + WOW Fantasy UI ($79, 509 files, 5 styles) + Leohpaz Retro RPG UI ($3.49) |
| menu-open | GREEN | Same as button-click |
| menu-close | GREEN | Same as button-click |
| inventory-open | GREEN | Leohpaz RPG Essentials (free, confirmed category) + WOW Fantasy UI + OGA Fantasy SFX Library (CC-BY) |
| equip | GREEN | Leohpaz RPG Essentials (free) + Leohpaz Retro RPG UI ($3.49, confirmed equip/unequip) + WOW Fantasy UI |
| drop (item drop) | YELLOW | Leohpaz RPG Essentials (free, partial) + WOW Fantasy UI (window transitions) — no explicit "drop" candidate |
| chest-open | YELLOW | TomMusic Free 200 (doors/chests/gates, free) + Leohpaz Dungeon (chest open, free) — not specifically labeled |
| pot-break | YELLOW | TomMusic Free 200 (partial foley) — no dedicated pot-break candidate |
| loot-pickup (chime) | GREEN | Leohpaz RPG Essentials (free, confirmed pickup) + OGA Fantasy SFX Library (pickup gold, CC-BY) + WOW Fantasy UI (reward layer) |
| level-up | GREEN | Leohpaz RPG Essentials (free, confirmed) + Leohpaz Retro RPG UI ($3.49) + WOW Fantasy UI (reward) |
| error | YELLOW | Leohpaz RPG Essentials (free, confirmed decline/denied) + Kenney Interface — not fantasy-register |
| dash / dodge-iframe-pulse | YELLOW | Leohpaz Dungeon (dash/evade, free, physical) + WSP displacement sounds — no elemental iframe-pulse specific |
| loot-rarity-tier chime (common/rare/epic/legendary variants) | YELLOW | OGA Fantasy SFX Library (3 jingles: win/lose/achievement, CC-BY); Leohpaz Retro RPG UI (16-bit achievement pack, $2.49) — no multi-tier rarity-chime pack confirmed |

**RED UI events:** none — all covered GREEN or YELLOW with free candidates as baseline.

---

## Section 3 — Death Tiers

| Tier | Status | Candidate vendors |
|---|---|---|
| trash (common enemy death) | GREEN | Leohpaz RPG Essentials (free, confirmed enemy death) + OGA RPG Sound Pack (CC0) + Leohpaz Dungeon (physical death, free) |
| elite (powerful enemy death) | YELLOW | Leohpaz Elemental Creatures ($2.49, elemental creature death per-element) + WS1 layered impact + OGA packs — no explicit "elite death" pack |
| boss (act boss death) | YELLOW | WS1 layered impact (large dark/negative spells) + FH dark/lava impacts — no dedicated boss-death dramatic SFX pack found |
| player (player death) | YELLOW | Leohpaz RPG Essentials (partial, physical) — no dedicated player-death dramatic SFX with ritualistic weight found |

**RED death tiers:** none strictly RED; boss + player-death are YELLOW (layered construction possible from WS1/FH but no direct-map single-file candidate).

**Note:** Boss death and player death have dramaturgical weight in Reincarnated (per audio-scoping-framework.md passage-moment-ritual coupling). YELLOW is technically accurate for coverage but these warrant bespoke construction (layer approach) rather than single-file drops.

---

## Section 4 — Ambient Biomes

| Biome | Status | Candidate vendors |
|---|---|---|
| dungeon | GREEN | PixelLoops Ambient ($3.59) + AD Sounds RPG Soundscapes ($4.99) + TomMusic Free 200 (free) + David Dumais ($75, premium) + kmontesdev CC0 (free, 2GB) |
| cave | GREEN | PixelLoops Ambient ($3.59, cave category confirmed) + David Dumais (caves confirmed) + kmontesdev CC0 (free) |
| swamp | GREEN | PixelLoops Ambient ($3.59, swamp confirmed) + AD Sounds (swamp implied in outdoor/rain) + David Dumais (swamp confirmed) |
| ruined-temple | GREEN | PixelLoops Ambient ($3.59, ruins + magic/temple confirmed) + AD Sounds (inn/blacksmith partial) + David Dumais (cemetery/ruins) |
| forest | GREEN | PixelLoops Ambient ($3.59) + AD Sounds ($4.99) + TomMusic (free, loopable) + David Dumais |
| desert | GREEN | PixelLoops Ambient ($3.59, desert+snow confirmed) + AD Sounds (open field/desert confirmed) + David Dumais (desert confirmed) |
| glowing-cave | YELLOW | David Dumais has "lava" + "underwater" environments — closest proxy. No dedicated "glowing-cave" (bioluminescent cavern) candidate. Layering approach: cave base + magic/temple layer. |
| sewer | YELLOW | AD Sounds has urban rain; David Dumais has "tar/mud/goo" and underwater. No dedicated sewer biome. Layering: cave + water-foley. |

**RED ambient:** none strictly RED. Glowing-cave and sewer are YELLOW (achievable via layering; not native single-loop match).

---

## Section 5 — Music (per-season)

| Slot | Status | Notes |
|---|---|---|
| 001001-005 (historical, already on disk) | GREEN | 5 mp3s exist. Per dispatch: Matt's AI-music workflow. No replacement needed. |
| 002011-015 (D10 seasons, currently silent) | YELLOW | Multiple options (see Section 5 detail below). |
| Future seasons (002016+) | YELLOW | Suno Pro workflow is Matt's current path. Viable with Pro subscription. |

### 002011-015 music gap — pragmatic options

5 D10 seasons currently hit silent fallback. Pragmatic options ranked:

**Option A — Reuse 001001-005 tracks as shared placeholder** (cost: $0, effort: zero)
Rotate existing 5 tracks across the 5 new season IDs. Loses per-season sonic identity but unblocks gameplay. Acceptable for playtest; not for demo ship.

**Option B — Suno Pro per-season generation** (cost: ~$10/mo while generating)
Matt generates one thematic track per season via Suno Pro. Requires active Pro subscription for commercial rights. WMG partnership (Nov 2025) has improved license clarity. CAUTION: current terms state AI output not copyrightable; Suno retains training rights. Verify game-embedded audio clause specifically (terms note "games where audio is integral" may require special terms). Best for internal playtesting.

**Option C — CC0 fantasy music library** (cost: $0, effort: manual curation per track)
Sources: Blacis Fantasy Music Mega Pack (100+ tracks, CC0, free) or OGA CC0 Fantasy Music collection. Assign one CC0 track per season. Attribution not required. CAUTION: Blacis pack is AI-generated — same license flux as Suno. Pure human-composed CC0 tracks on OGA require manual curation per season.

**Option D — Royalty-free commercial library** (cost: $77-99 for large pack, or $10-40/yr subscription)
Bit By Bit Sound Ultimate Retro RPG Music ($77.60, 410+ tracks, royalty-free, attribution required) — assign per-season from diverse catalog. Attribution required in credits. Best long-term solution for demo ship. PixelLoops Fantasy Dungeon Music ($4.49, 20 tracks) as budget alternative for dungeon-heavy seasons.

**Option E — Procedural/skip** (cost: $0)
Ship without per-season music; rely on Tier 1 silence or ambient-only. Lowest effort. Acceptable for alpha; not for demo ship given combat-feel gap.

**Recommended pragmatic path:** B (Suno Pro) for rapid internal iteration; D (Bit By Bit Sound) when demo-ship readiness requires attribution-clear commercial music.

---

## Summary — RED cells requiring commission or generative path

| Slot | RED reason | Recommended path |
|---|---|---|
| water+slam (ground slam water element) | No specific water-ground-slam SFX found | Construct from WS3 water impact layer + earth slam layer (WS1 construction kit approach) |
| earth+beam (channeled earth beam) | No earth-specific beam-channel SFX | Construct from WS3 earth + FH stone atmosphere layer |
| holy+slam | No holy-ground-slam candidate | Construct from FH divine impact + WS3 earth slam |
| physical+beam (no elemental) | No physical channeled-beam SFX | Construct from Kenney + WS1 impacts |
| physical+aura (sustained physical buff loop) | No physical aura loop found | Construct from Kenney + generic tone layer |

**All 5 RED cells are constructible from available YELLOW-or-better vendors via layer composition. No bespoke commission required at this stage.**
