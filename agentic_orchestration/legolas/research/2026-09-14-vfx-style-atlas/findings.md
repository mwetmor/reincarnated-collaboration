# Research — VFX style atlas: feasibility + first sample pull — 2026-09-14

> **STATUS:** CURRENT — legolas (commissioned by gandalf; brief `agentic_orchestration/gandalf/requests/2026-09-14-legolas-vfx-style-atlas-feasibility.md`; rulings R-C3-90…95). Filed by gandalf from the agent's returned text. **Samples live OUTSIDE the repo** at `~/Games/vendor/vfx-atlas/` (385 MB kept; `atlas.json` + `samples/<id>/{record.json, contact.png, loop.webp[, frames/, bg.png]}`); study-only, never an image-model reference, never committed. Third run after two host crashes: serial, streamed decode, ≤ 230 MB per process, disk peak ≈ 450 MB, all downloads deleted after cropping.

**Result:** 54 samples (26 pixel · 19 3D · 9 painted; impact/explosion 12 · elemental burst 11 · beam/lightning 10 · projectile 9 · ground area 6 · aura/buff 5) — about 3 per source, not the 60–90 hoped for. Retro sheet rips give the best pixel-trait data but **no timing**; many gameplay-video samples have unreliable numbers (flagged per record).

## 1. Feasibility (§3 of the brief)
Obtainability: **F** free official · **FR** fan rip · **P** purchase/install · **M** Matt's account.

| Source | Format · macOS/Python tool | Timing / layer data | Obtain | Terms (private study) | Disk raw / subset | Go? · effort |
|---|---|---|---|---|---|---|
| **Baldur's Gate II / Icewind Dale** | BAM (V1/compressed/V2) + VVC; Near Infinity (macOS, Java bundled); BAM V1 reader trivial in Python | **Yes** (VERIFIED, IESDP): VVC frame rate, duration, transparent/translucent/blend/brighten flags; BAM palette-0 + EE alpha | P (EE on GOG/Steam) | EULA | ~3–4 GB (unverified) / 50–150 MB | **No-go without install** (no effect sheets on Spriters Resource). With install: Go, medium |
| **Diablo I** | CL2 in MPQ; StormLib (brew); DevilutionX public domain | **Yes** (VERIFIED): `missile_sprites.tsv` frames + delay per direction at 20 Hz tick (DERIVED) | FR (sheets, pulled) · **F: official shareware `spawn.mpq`** | shareware freely distributed | ~25 MB / < 10 MB | **Go.** 2 pulled; spawn.mpq route = exact timing, low–medium |
| **Diablo II** | DC6 in MPQ (Mac MPQ tool; DC6 decoder to write) | **Yes** (VERIFIED): `Missiles.txt` / `Overlay.txt` speed, frames, transparency | P/M; **no missile/spell sheets on Spriters Resource** (VERIFIED) | EULA | ~2 GB / ~30 MB | **No-go without purchase** (timing already public) |
| **Ragnarok Online** | GRF → SPR/ACT + STR; grf-extractor CLI; roBrowser JS loader | Yes in ACT delays / STR keyframes — not in rips | FR (Wayback, 1,277 sheets) · client free but an install | Gravity EULA | ~3–4 GB / < 50 MB | **Go** for rips (2 pulled, no timing) |
| **RPG Maker (RTP)** | MV: PNG cells + `Animations.json`; XP: `.rxdata`; 2003: liblcf; pure-Python renderer | **Yes, complete** (VERIFIED `rpg_sprites.js`): 4 game frames @60 = 66.7 ms/cell, blend normal/add/multiply/screen, hue, flash timings | F | RTP licence limits use to RPG Maker games; study non-distributive | < 10 MB | **Go.** 6 pulled, low; XP/2003 next |
| **SNES/GBA rips** (FF6, CT, SoM, Golden Sun) | PNG sheets via Wayback (live site 403) | **No timing**; no palette cycling / colour-math translucency in rips; GBA rips baked over black | FR | fan rips | < 1 MB each | **Go** for pixel traits; 13 pulled; timing needs emulator capture (medium) |
| **Sea of Stars** | Unity; AssetRipper (Apple Silicon build) | Unity clips if extracted | P | EULA | ~2–3 GB | Footage Go (3 pulled); data needs purchase |
| **Octopath Traveler** | UE4 pak; FModel Windows-only (PRACTITIONER-REPORT) | UE particle assets | P | EULA | ~3–4 GB | Footage only (1 pulled); data blocked on macOS |
| **CrossCode** | web engine; PNG atlases + effect JSON (JSON location PRACTITIONER-REPORT) | JSON carries timing (not accessed) | FR atlases (pulled) · P for JSON | EULA | ~1.5 GB / < 20 MB | **Go.** 4 pulled; with purchase = best modern pixel source, low |
| **Hyper Light Drifter** | GameMaker `data.win`; UndertaleModTool CLI on macOS | sprite frames; speed in objects | P | EULA | ~1 GB | Footage Go (1 pulled); data low–medium |
| **Hades** | `.pkg`; `deppth` (LZ4) | **Yes** (VERIFIED): `Fx.sjson` Books/Slides/blend groups | P/M (no local install found) | EULA | ~15 GB / ~200 MB FX | Data public (mod-tutorial repo); flipbook images need install; footage 3 pulled |
| **League of Legends** | official ability clips (Riot CDN WebM 1056×720@30); CommunityDragon particle textures | textures only; VFX definitions not located | **F** | Riot legal terms; study | clips 2–6 MB | **Go.** 6 clips + 1 texture set, low |
| **Dota 2** | official ability clips (Steam CDN WebM 1080p60); Source 2 Viewer needs game files | particle defs need game files (GameTracking has none) | **F** clips · M game files (DepotDownloader login) | Valve terms | clips 2–19 MB / install 40–60 GB | **Go** clips (6 pulled); data needs Matt's Steam login, medium |
| **D2R / Grim Dawn / Last Epoch / PoE** | YouTube footage; PoE: poe-dat-viewer bundles from patch servers (PRACTITIONER-REPORT); LE: AssetRipper | footage timing only; **local GD edition has no particle/texture archives** (VERIFIED) | F footage | study | 10–20 MB per window | Footage Go, low yield (D2R 1, GD 2, LE 2, PoE 1); PoE bundles = best data route |

## 2. Samples (54; sizes in the atlas)
- **RPG Maker MV** (painted, full timing): `rpgmv-fire-one-2` · `rpgmv-hit-physical` · `rpgmv-ice-one-2` · `rpgmv-thunder-one-1` · `rpgmv-heal-one-2` · `rpgmv-thunder-all-1`
- **FF6** (pixel): `ff6-fire3` · `ff6-ice3` · `ff6-bolt3` · `ff6-fire2` · **Chrono Trigger**: `ct-megabomb` · `ct-flare` · `ct-ice-projectile` · `ct-aura` · **Golden Sun**: `gs-blue-bolt` · `gs-blast` · `gs-eruption` · `gs-glacier` · `gs-restore`
- **CrossCode** (pixel): `cc-shock-pillar` · `cc-shock-burst` · `cc-bomb-explosion` · `cc-bomb-smoke-grey` · **Ragnarok**: `ro-effect1-fire-ring` · `ro-explosion-attack` · **Diablo I** (timing from DevilutionX): `d1-fireball` · `d1-holy-bolt`
- **LoL** (3D): `lol-ezreal-q-mystic-shot` · `lol-ziggs-r-mega-inferno-bomb` · `lol-lux-e-lucent-singularity` · `lol-lux-r-final-spark` · `lol-kayle-r-divine-judgment` · `lol-brand-w-pillar-of-flame` · `lol-ezreal-q-textures` (process)
- **Dota 2** (3D): `dota2-zeus-lightning-bolt` · `dota2-vengefulspirit-magic-missile` · `dota2-crystal-maiden-crystal-nova` · `dota2-lina-light-strike-array` · `dota2-omniknight-heavenly-grace` · `dota2-omniknight-purification`
- **Hades / II** (painted): `hades-zeus-bolt-theseus` · `hades2-water-splash-hit` · `hades2-hecate-eruption-pillar`
- **Modern retro footage:** `sos-green-burst` · `sos-magenta-ring-hit` · `sos-sky-beam` · `hld-reaper-scythe-projectile` · `octopath-special-burst` · **ARPG footage:** `d2r-frozen-orb` · `gd-green-burst` · `gd-fire-hit` · `le-runemaster-lightning` · `le-frost-burst` · `poe-arc-chain-lightning`
- Rejected: `hld-cyan-slash` (crop missed; listed under `rejected_cuts`).

**Record fields:** `{id, game, year, source_url, effect_type, element, register, native_res, frames, native_timing, transparency, measures O1–O9, traits, measure_reliability / measure_note}`; instrument notes in `atlas_meta`.

**Measurement limits:** sheet samples have no O2 ms / O8; O8 invalid on lossy video (codec noise = new drawing every frame); O3 reads 0 on SNES/GBA (palettes top out ~V .97, "white" cores are light grey); all rips verified native 1× (2×2-block test). **LOW reliability (read for traits, not numbers):** `dota2-zeus-lightning-bolt`, `dota2-vengefulspirit-magic-missile`, `dota2-crystal-maiden-crystal-nova`, `hades-zeus-bolt-theseus`, `sos-magenta-ring-hit`, `sos-sky-beam`, `gd-green-burst`, `gd-fire-hit` (very low), `le-frost-burst`. **Oracle reproduced:** `hades2-hecate-eruption-pillar` area/peak 1.00/.90/.55/.34/.22/.20 vs oracle E4 1.00/.85/.53/.35/.24/.20; `hades2-water-splash-hit` = E2 pattern (flash first; core S .06 at peak → .70 in the fade).

**Cross-source patterns (DERIVED):** in pixel rips the flash is a full white/red disc frame inside the sprite (CrossCode bomb, Golden Sun Blast, RO explosion), not an engine layer · fading by stepped flat value bands (CrossCode shock, CT Flare: white → pink → violet → navy) = the pixel form of Hades II's flat planes · CrossCode ships a grey copy of its explosion row (cf. Hades runtime-tinted greyscale + dark duplicate; unverified in data) · LoL Ziggs R / Kayle R end on black/brown smoke discs.

## 3. Needs Matt
| Ask | Unblocks | Disk |
|---|---|---|
| BG2EE / IWDEE + Near Infinity | Infinity Engine sprites + timing/blend flags | ~3–4 GB, ~150 MB subset |
| Hades install + `deppth` | the real flipbook atlases matching `Fx.sjson` | ~15 GB, ~200 MB FX |
| CrossCode purchase | effect JSON timing for the pulled atlases (best modern pixel source) | ~1.5 GB |
| Steam login for DepotDownloader | Dota 2 particle definitions | several GB |
| Diablo II / D2R (Battle.net) | sprites to pair with public `Missiles.txt` | ~2 GB |
| full Grim Dawn depot | GD FX textures/particle files (local edition lacks them) | a few GB |
| Sea of Stars / HLD / Last Epoch | Unity/GameMaker sprite + animation data | 1–3 GB each |

Needs nobody next: Diablo shareware `spawn.mpq`, PoE patch-server bundles, RPG Maker XP/2003 RTP.

## 4. Gaps
1. No timing for SNES/GBA/RO/CrossCode rips; sheet order not a verified play order; a few sheet cuts merged/dropped frames (per record). 2. Footage of Hades/ARPGs/Octopath is noisy (panning, UI, repeated casts); O9 shake and hit-stop not measured. 3. Missing types: no aura for LoL/Hades/ARPGs; no projectile/ground area for Golden Sun; one clean sample each for HLD, Octopath, PoE, D2R; no Secret of Mana. 4. Blocked, not substituted: Infinity Engine, Diablo II sprites, Octopath data. 5. Body-height scaling only for LoL (Ezreal-calibrated) and Hades. 6. Licence notes practitioner-level; three install sizes unverified.

Tools (local, not committed): `~/Games/vendor/vfx-atlas/_tools/{measure.py, finalize.py, render_mv.py, sheet_cut.py, vid.sh, yt.sh, srsheet.sh, unpack.py, addtraits.py}`.

Sources: IESDP VVC/BAM · Near Infinity · DevilutionX MPQ + `missile_sprites.tsv` · MV3D (RPG Maker MV data) · RPG Maker RTP · Spriters Resource (Wayback) · CommunityDragon · Riot ability clips CDN · Dota 2 ability clips CDN · deppth · grf-extractor · AssetRipper · UndertaleModTool · poe-dat-viewer · Diablo II MPQ Tool (Mac) · YouTube footage ids wTgaAZiNSBw, 4_sCtSgGMO0, IXZFmfwsrAA, 4Q9BBLdPjT0, K1D2UadKoG8, W33wsGxZ7EI, b5a-iIras34, ijwA_J29j1k, 5WiYcx9SjZU (measurement only, deleted).
