# Painted-2D complete game-art pipeline — SCOPE MAP v0.1

> **STATUS:** DESIGN SWEEP (gandalf, ARCHITECT, 2026-09-11) at Matt's word: *"don't limit yourself to the scopes I've listed. Ultra-think through all known (and research to find unknown) scopes potentially involved within this 2D painted complete game art pipeline."* Known scopes from the inside (Diablo II's pre-rendered pipeline is the direct ancestor; Hades / Darkest Dungeon the modern painted ones); unknowns commissioned to legolas as **R9** (`gandalf/requests/2026-09-11-legolas-mode-a-r9-pipeline-scope-discovery.md`). Companion: `astra_test_01/burst/SPEC.md § 6` (T1–T5 instruments) — this map is the superset those bursts draw from.
> **Legend — Gen:** A = Astra generates · D = deterministic tool derives · E = engine/runtime does it · H = human-authored (Matt/gandalf) · A→D = Astra generates, tool derives the usable data. **When:** C-1 (this run) · C-2 (roster/monsters run) · P (product build) · M (marketing).

## 1. Player characters

| # | Scope | Gen | Oracle / software | Bible / manifest fields | When |
|---|---|---|---|---|---|
| 1.1 | Base body per identity, 8 dirs | A | T0/T1 (identity vector, silhouette64, visibility table, drift48, G1–G6) | parts[], side, palette bins, silhouette read | C-1 |
| 1.2 | **Animation inventory** — the clip table per kit family: idle · walk · run · attack per weapon class (1H swing / 2H / thrust / bow / staff / throw) · cast · channel loop (whirlwind, beam) · dash/blink · hit-react · block · dodge · death + corpse · interact/loot · town idle · level-up/victory · summon/totem-place. D2 shipped NU/WL/RN/A1/A2/BL/SC/TH/KK/S1–S4/DT/DD/GH/TN/TW; our 24 archetypes each imply a body clip | H (table) → A | `clip_table.json` validator: frame counts, fps, loop flag, **event frames** (contact, spawn, hit) — the retiming-safe keyframes | motion contract | C-1 (idle/walk/cast) → C-2 |
| 1.3 | **Attack-speed retiming** (IAS): runtime skips/duplicates frames; event frames must survive | E + D | manifest marks event frames; oracle: no event frame dropped at any supported speed | motion.events[] | P |
| 1.4 | Modular gear layers per slot (head/torso/shoulders/arms/legs/boots/belt/back/weapon/offhand); **weapon class changes the clip** | A→D | T2 gear_overlay, fit, helmet toggle, set_consistency; slot × clip matrix validator | slots[], region map | C-1 (torso) → C-2 |
| 1.5 | Secondary motion painted per frame (cloth, hair, cape) | A | hair-mass / cape area continuity (part_metrics) | rigidity: cloth/hair | C-1 |
| 1.6 | Stature tiers (trash : elite : mini-boss : boss ≈ 1 : 1.6 : 2.4 : 4.4 — style-register survivor) | H → D | measured height vs tier table | scale table | C-2 |
| 1.7 | Portraits (inventory paperdoll, select screen, dialogue) — a close-up painted register | A | **identity-across-scales** oracle (portrait vs sprite identity vector; face transcription) | portrait register card | P |
| 1.8 | Status overlays (frozen shell, burning, chilled, poisoned) — shader tint/overlay, not painted per frame (D2 palette-shifted) | E (+A overlay sprites) | element hue bands; colorblind check (§ 9) | element palette | P |
| 1.9 | Death/corpse/gib layers; dismemberment for modular bosses | A→D | last-frame persistence; gib parts = part masks | parts[] rigidity | C-2 |
| 1.10 | Hit-flash, selection outline, behind-wall transparency, shadows | **E** (never painted) | `no_floor_shadow`; outline is a shader | — | P |

## 2. Monsters and kits

| # | Scope | Gen | Oracle / software | Fields | When |
|---|---|---|---|---|---|
| 2.1 | Body plans first-class: humanoid · quadruped · serpentine · flying · swarm · slime · dragon/boss (doc-37 form-bias survivor) | A / A→rig | frame-sheet ≤ ~1.5× hero; **modular Skeleton2D above** (parts painted once); gait oracle per plan (4-leg gaits) | plan, gait template | C-2 |
| 2.2 | Monster clip set (smaller: idle, walk, attack ×2, hit, death, special) | H → A | clip_table | motion | C-2 |
| 2.3 | Variants: palette swaps (champion/unique), size scaling, auras | D + E | palette-swap tool with **hue-band preservation** (element meaning survives the swap) | variant rules | C-2 |
| 2.4 | **Kit → art brief translation** — the engine emits kits (serial content emission); an LLM step turns kit data (element, court, archetype, tier) into a bible-conformant brief | A (text) → A | brief validator against bible vocabulary (no franchise nouns, one motif, plain budget) | faction/court vocabularies | C-2 |
| 2.5 | **Enemy legibility** — enemies must not read as scaled player models (style-register requirement; Mirror-fight exception) | D | identity-vector distance player↔enemy classes ≥ threshold; silhouette64 distance | class silhouettes | C-2 |
| 2.6 | Bosses: multi-phase looks, arena-scale VFX, phase-transition states | A→rig | phase validator | — | P |

## 3. Environment (plates, tiles, props)

| # | Scope | Gen | Oracle / software | Fields | When |
|---|---|---|---|---|---|
| 3.1 | Floor/terrain plates per biome; surface materials (stone/soil/wood/water); transitions | A→D | T3 plate_scale, edge_sockets, texel-density check, seam similarity | biome plate library, material tags | C-1 (one plate) → P |
| 3.2 | Walls/structures with **y-sort split pieces** and **occlusion masks** (see-through when the player is behind) | A→D | mask derivation; split-line validator | occluder parts | C-2 |
| 3.3 | Props: static · interactive with states (door closed/open/locked · chest closed/open/looted · crate/barrel intact/broken · lever · shrine · waypoint · portal) — state sheets on transparent | A | state-set validator (all states present, same footprint, same light); footprint from mask | prop catalogue, state lists | C-1 (chest) → P |
| 3.4 | **Projection-angle oracle** — box-like props' and plate edges' angle histogram must match projection C's ground axes ("the crate is drawn at the wrong angle") | D | `projection_check.py` (edge-direction histogram vs expected dimetric axes) | projection constants | C-1 |
| 3.5 | Scale table across classes (doorway = 2× hero, chest ≈ 0.5×, table ≈ 0.6× …) | H → D | measured vs table via masks | scale table | C-1 |
| 3.6 | Baked plate light + local light sources (torches, lava, glowing runes) → **normal maps** for dynamic 2D light; plate key must match sprite key | A→D | T5 plate_light, normal_from_height | light sources[] with positions | C-1 |
| 3.7 | Ambient animation on static plates (torch flicker, water, banners) as overlay strips | A | loop seam + emissive gates | overlay sockets | P |
| 3.8 | Exterior plates: sky/backdrop, **parallax layers** (Hades) | A | parallax layer registration | — | P |
| 3.9 | **Act/biome register + transition plates** — per-act identity (Q44, open) and Q38's *biome morph per element court, meeting in the middle* → A→B transition plates | H → A | biome palette distance per plate; transition plate validator | act registers | P (Q44 gates it) |
| 3.10 | Procedural assembly interface: room graph → plate selection → socket matching → walkable union → nav; plate metadata (exits, spawn/loot/prop sockets, light sources) | D + E | T3 plate_assembler, nav_from_masks; **minimap derived from masks** (D2's automap came from tile data) | plate metadata schema | C-1 (2 plates) → P |
| 3.11 | Decals (blood, scorch, footprints) layer + caps/fade policy | A + E | decal atlas builder | decal atlas | C-1 (blood) |

## 4. VFX

| # | Scope | Gen | Oracle | Fields | When |
|---|---|---|---|---|---|
| 4.1 | 24 archetypes × elements × materials (sealed binding spec) | A | T4 archetype_validator, lifecycle, attachment, element_hue, material_matrix | archetype table | C-1 (1) → C-2 |
| 4.2 | Persistent overlays: auras/buffs, shields, channel loops, totem bodies | A | loop seam, sort-layer under/over | layer rules | C-2 |
| 4.3 | System VFX: loot-drop beam, level-up, portal, shrine, waypoint, hit-flash (E), screen shake (E) | A / E | lifecycle | — | P |
| 4.4 | **Story-signature VFX** — the Glitch Archive's own register: *deletion/corruption* on a kit being erased, *adapter-absorb* when a kit is rescued, glitch UI motifs | H (STORYWRIGHT) → A | a distinct sub-register card; must NOT bleed into ordinary elemental VFX (motif-bleed oracle applied to VFX) | glitch register | P (story) |
| 4.5 | Telegraphs / ground warnings readability | A + D | contrast vs floor plates; colorblind check | telegraph palette | C-2 |
| 4.6 | Sort layers, additive vs normal blend, emissive masks | D | G9, emissive-from-energy | blend policy | C-1 |

## 5. Items and loot

| # | Scope | Gen | Oracle | Fields | When |
|---|---|---|---|---|---|
| 5.1 | **Ground item sprites** (D2: one per base item — hundreds) | A | register consistency across the set (identity-vector distribution); footprint | item base list | P |
| 5.2 | **Inventory icons** (grid cells; rarity frames; sockets) — a symbolic small-scale register where AI ornament noise is worst | A | icon register card; HF-energy cap; silhouette read at cell size | icon register | C-2 |
| 5.3 | Equipped appearance = gear layers (1.4) per base type; **weapon base × clip set** matrix | A→D | T2 | slots × bases | C-2 |
| 5.4 | Uniques/sets (~50) with distinct art | H → A | motif-bleed oracle (a unique's motif stays on the unique) | unique motifs | P |
| 5.5 | Consumables/currency (potions, scrolls, gems, runes, gold) | A | icon oracles | — | P |

## 6. UI / HUD / screens

| # | Scope | Gen | Oracle | Fields | When |
|---|---|---|---|---|---|
| 6.1 | HUD frame (orbs/flasks/bars), skill bar, buff icons, minimap frame, cursor | A (frames) + E | register vs anchors; **no generated text ever** (glyph gibberish) | UI register | P |
| 6.2 | **Skill icons** — 24 archetypes × elements × kits: an icon language | H (icon grammar) → A | icon register; element hue; silhouette read at 32/64 px; set-consistency | icon grammar | C-2 |
| 6.3 | Panels: inventory/paperdoll, stash, vendor, skill tree (PoE-scale painted backgrounds), character sheet | A | register | — | P |
| 6.4 | Typography: register-consistent font choice (never AI-rendered text) | H | — | — | P |
| 6.5 | Title/menu/loading art; **narrative stills** for the Glitch Archive frame (kid / floppy / VR adapter) | A | register + story review | — | P/M |
| 6.6 | Accessibility: **colorblind-safe element bands** (deuteranopia/protanopia simulation of VFX/telegraphs/icons), UI scale | D | `cvd_check.py` (simulate CVD, verify element bands stay separable) | element palette | C-2 |

## 7. Technical / format

| # | Scope | Gen | Oracle / software | When |
|---|---|---|---|---|
| 7.1 | Sheets/atlases (max texture size, mips, filtering), pivots, per-frame metadata, hit/hurt boxes **from masks**, sockets (staff tip, hands, hips), sort anchors, collision footprints | D | pack + manifest + validators | C-1 |
| 7.2 | Engine import: Godot SpriteFrames / AnimatedSprite2D / Skeleton2D / CanvasTexture+normal / Light2D / YSort; manifest → importer | D | `godot_import.py` (T2) | C-1 |
| 7.3 | **Resolution policy**: on-screen hero height at 1080p/1440p/4K vs native cell (627 px → 240-px hero); D2R re-rendered for 4K; Matt's "3× looks blurry" lives here | H → D | resolution table; texel-density oracle | C-1 (decide) |
| 7.4 | Memory/streaming budget: N chars × clips × dirs × frames × layers × 512² | D | budget calculator (R5) | C-2 |
| 7.5 | Color management (sRGB/gamma consistency across generated assets), premultiplied alpha, dark fringe (G9), compression (PNG/WebP/Basis) | D | gamma check; G9 | C-1 |
| 7.6 | Runtime layer composition vs baked composites (D2 COF) + content-addressed loadout cache | E + D | cache validator | P |
| 7.7 | **Asset invalidation graph** — every receipt records the bible rule ids it was generated under; a rule change re-gates or regenerates dependents (pivot insurance, mechanized) | D | `deps_ledger.py` | C-1 |

## 8. Process / QA / governance

| # | Scope | Gen | Oracle / software | When |
|---|---|---|---|---|
| 8.1 | The bible + renderer + comparator + known-bad factory + transcription validator (T0/T-cross) | D | — | C-1 |
| 8.2 | **HITL review console** — local HTML gallery with flip-book, anchors side-by-side, controls, and **approve/reject/notes buttons that write Matt's verdicts to JSON** (the HITL gates as clicks, not chat) | D | `hitl_console` (no server; file:// + download-JSON or a 1-file local server) | **C-1 (HITL run)** |
| 8.3 | **Model-version drift oracle** — the generator itself drifts when OpenAI ships a new image backend: re-run a frozen probe set (same prompt + refs) on a cadence; distance to approved assets; alarm on drift. Matt's DAX-drift pattern applied to the generator | D | `model_drift_probe.py` | C-1 (define) → P |
| 8.4 | Regression locks (run_03 numbers; approved assets' hashes) | D | T0-b | C-1 |
| 8.5 | Roster cohesion at scale: identity-vector distribution, palette usage, HF energy across 100+; faction clustering; outliers | D | `cohesion_stats.py` | C-2 |
| 8.6 | **IP / similarity** — perceptual-hash + identity-vector distance against a *source-game reference corpus* (no "too close to D2's Barbarian"); franchise-noun ban in prompts; model ToS for commercial use; provenance metadata (C2PA?) | D + H | `ip_similarity.py`; legal review (Matt) | C-2 (R9 unknown) |
| 8.7 | Content moderation constraints (gore) — record refusals | — | ledger | C-1 |
| 8.8 | No in-image text; localization untouched by art | H | glyph detector | C-1 |
| 8.9 | Lineage: content-addressed assets, receipts, prompts, reference roles, model/version stamps | D | ledger | C-1 |

## 9. Marketing / store (TRAILER-CUT adjacency; dormant seam)

Key art, Steam capsules (all sizes), screenshots, trailer stills, app icon; **logo/wordmark is vector and human-made** (the imagegen skill's own advice). When: M.

## 10. What this map changes now

- **SPEC § 6 gains three C-1 instruments** not in the earlier list: `projection_check.py` (3.4), `deps_ledger.py` (7.7), `hitl_console` (8.2). `model_drift_probe.py` (8.3) is *defined* in C-1 (probe set frozen at K1) and run later.
- **Bible schema gains** `scale_table`, `clip_table`, `light_sources[]`, `slots[]`, `element_palette` (with CVD-safe bands), `icon_grammar`, and the `glitch_register` sub-card.
- **Two live Matt-queue intersections:** Q44 (act register) gates 3.9; Q38's biome morph is the working answer. The Glitch Archive story-signature VFX (4.4) is a STORYWRIGHT fold, not a run item.
- **Unknowns → R9** (legolas): scopes I have not listed, and evidence for the ones marked uncertain (8.3, 8.6, 7.3, 7.4).

— gandalf, 2026-09-11
