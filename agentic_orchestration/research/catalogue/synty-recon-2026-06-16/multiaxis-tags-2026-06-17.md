# Synty catalogue — multi-axis tags (substrate-half + density map)

**Author:** elrond | **Date:** 2026-06-17 | **Commission:** `agentic_orchestration/gandalf/requests/2026-06-17-elrond-catalogue-multiaxis-tagging.md`

**Substrate:** `synty_catalogue.db` (schema 1.2) — 157 pack rows / 156 content collections. Tags are ADDITIVE columns on `packs`.

**Axis discipline:** 1+5 substrate-GIVEN; 2 doc-DERIVED; **3+4 substrate-VOTED — now gandalf-CURATED** at the semantic-layer rep-audit (ruling 2026-06-17 §1.3/§1.4/§1.6). Axis 3 accepted as-proposed (no change); axis 4 carries the Option A consumption rule + the frontier-western value-split (see Axis 4 section).


## Axis 1 — register distribution

- `ANIMATION`: 6 packs
- `INTERFACE`: 8 packs
- `POLYGON`: 102 packs
- `POLYGON_MINI`: 4 packs
- `SIMPLE`: 37 packs

## Axis 2 — contribution_role distribution (every pack routes)

- `environment`: 89 packs
- `armor-base-skinned`: 38 packs
- `ui`: 8 packs
- `bestiary`: 7 packs
- `anim`: 6 packs
- `accent-attach-static`: 6 packs
- `weapon-base-static`: 3 packs

## Axis 5 — seam distribution

- `overworld`: 63 packs
- `char-named-silhouette`: 28 packs
- `descent`: 14 packs
- `bestiary`: 11 packs
- `weapon-prop`: 10 packs
- `char-skeletal`: 10 packs
- `ui`: 8 packs
- `nature`: 7 packs
- `anim`: 6 packs

## Axis 3 — PROPOSED time_period strata (gandalf curates) — rep examples


### `modern` — 62 packs
- **INTERFACE - Apocalypse HUD** (chars=0, weps=0) — name-token 'apocalypse': modern/post-apocalyptic
- **INTERFACE - Military Combat HUD** (chars=0, weps=0) — name-token 'military': modern military
- **POLYGON - Apocalypse Pack** (chars=134, weps=915) — name-token 'apocalypse': modern/post-apocalyptic
- **POLYGON - Apocalypse Wasteland** (chars=0, weps=162) — name-token 'apocalypse': modern/post-apocalyptic
- **POLYGON - Battle Royale Pack** (chars=2, weps=58) — name-token 'battle royale': modern/near-future shooter
- **POLYGON - Boss Zombies** (chars=9, weps=0) — name-token 'zombie': modern-horror zombie
- **POLYGON - Casino** (chars=19, weps=0) — name-token 'casino': modern casino
- **POLYGON - City Characters Pack** (chars=19, weps=0) — name-token 'city': modern city
- …and 54 more

### `timeless-na` — 33 packs
- **POLYGON - Adult Face Plates** (chars=0, weps=0) — name-token 'face plates': modular-face — period-agnostic
- **POLYGON - Alpine Mountain - Nature Biome** (chars=0, weps=0) — name-token 'nature': nature biome — period-agnostic
- **POLYGON - Arid Desert - Nature Biome** (chars=0, weps=0) — name-token 'nature': nature biome — period-agnostic
- **POLYGON - Dog Pack** (chars=0, weps=0) — name-token 'dog': animal — period-agnostic
- **POLYGON - Easter Pack** (chars=0, weps=0) — name-token 'easter': seasonal
- **POLYGON - Enchanted Forest - Nature Biome** (chars=0, weps=0) — name-token 'nature': nature biome — period-agnostic
- **POLYGON - Gingerbread** (chars=0, weps=0) — name-token 'gingerbread': seasonal
- **POLYGON - Holiday Gnomes** (chars=0, weps=0) — name-token 'holiday': seasonal
- …and 25 more

### `medieval-fantasy` — 28 packs
- **ANIMATION - Goblin Locomotion** (chars=0, weps=0) — name-token 'goblin': fantasy
- **INTERFACE - Dark Fantasy HUD** (chars=0, weps=0) — name-token 'dark fantasy': gothic medieval-fantasy
- **INTERFACE - Fantasy Warrior HUD** (chars=0, weps=0) — name-token 'fantasy': generic medieval-fantasy
- **INTERFACE- Fantasy Menus** (chars=0, weps=0) — name-token 'fantasy': generic medieval-fantasy
- **POLYGON - Adventure Pack** (chars=10, weps=13) — name-token 'adventure': fantasy adventure
- **POLYGON - Dark Fantasy** (chars=15, weps=24) — name-token 'dark fantasy': gothic medieval-fantasy
- **POLYGON - Dark Fortress** (chars=0, weps=17) — name-token 'dark fortress': medieval-fantasy fortress
- **POLYGON - Dungeon Pack** (chars=16, weps=73) — name-token 'dungeon': medieval-fantasy dungeon
- …and 20 more

### `unresolved` — 17 packs
- **ANIMATION - Base Locomotion** (chars=0, weps=0) — no time-period token matched — gandalf rep-audit required
- **ANIMATION - Bow Combat** (chars=0, weps=0) — no time-period token matched — gandalf rep-audit required
- **ANIMATION - Emotes and Taunts** (chars=0, weps=0) — no time-period token matched — gandalf rep-audit required
- **ANIMATION - Idles** (chars=0, weps=0) — no time-period token matched — gandalf rep-audit required
- **ANIMATION - Sword Combat** (chars=0, weps=1) — no time-period token matched — gandalf rep-audit required
- **INTERFACE - Modern Menus** (chars=0, weps=0) — no time-period token matched — gandalf rep-audit required
- **POLYGON - Bow and Crossbow** (chars=0, weps=4) — no time-period token matched — gandalf rep-audit required
- **POLYGON - Bubblegum Killstick Kit** (chars=0, weps=7) — no time-period token matched — gandalf rep-audit required
- …and 9 more

### `sci-fi-future` — 10 packs
- **INTERFACE - Sci-Fi Menus** (chars=0, weps=0) — name-token 'sci-fi': explicit sci-fi
- **INTERFACE - Sci-Fi Soldier HUD** (chars=0, weps=0) — name-token 'sci-fi': explicit sci-fi
- **POLYGON - Mech Pack** (chars=1, weps=12) — name-token 'mech': mech = sci-fi
- **POLYGON - Sci-Fi Horror** (chars=0, weps=17) — name-token 'sci-fi': explicit sci-fi
- **POLYGON - Sci-Fi Outpost Map** (chars=0, weps=0) — name-token 'sci-fi': explicit sci-fi
- **POLYGON - Sci-Fi Space Pack** (chars=52, weps=7) — name-token 'sci-fi': explicit sci-fi
- **POLYGON - Sci-Fi Worlds Pack** (chars=64, weps=74) — name-token 'sci-fi': explicit sci-fi
- **SIMPLE - Space** (chars=0, weps=0) — name-token 'space': space = sci-fi
- …and 2 more

### `renaissance-early-modern` — 3 packs
- **POLYGON - Pirate Pack** (chars=14, weps=36) — name-token 'pirate': age-of-sail early-modern
- **POLYGON - Samurai Empire** (chars=0, weps=34) — name-token 'samurai': feudal-Japan sengoku ~ early-modern
- **POLYGON - Samurai Pack** (chars=8, weps=16) — name-token 'samurai': feudal-Japan sengoku ~ early-modern

### `antiquity` — 2 packs
- **POLYGON - Ancient Egypt** (chars=0, weps=28) — name-token 'ancient egypt': Egypt = bronze-age antiquity
- **POLYGON - Ancient Empire** (chars=11, weps=15) — name-token 'ancient empire': ancient empire = greco-roman antiquity

### `industrial-steampunk` — 2 packs
- **POLYGON - War Map - WWI** (chars=9, weps=7) — name-token 'war map - wwi': WWI industrial-era
- **SIMPLE - Trains** (chars=0, weps=0) — name-token 'trains': rail = industrial-era

## Axis 4 — cultural_identity strata — gandalf-CURATED (ruling 2026-06-17 §1.3/§1.4)

Mode flags guard the Mode A/B/C/D collapse: **A**=geographic-origin, **B**=cultural-tradition, **C**=naming-allusion / register-default (NOT a real culture), **D**=metadata/no-cultural-read.


> **CONSUMPTION RULE (Option A — gandalf ruling §1.3 / §1.6; READ-TIME gate, NOT a data migration).** `cultural_identity_proposed` is binding as a **cultural-tradition substrate ONLY for rows where `cultural_mode_flag ∈ {A, B}`.** For **Mode-C** rows the value is a `register_default_skin` (genre-default — generic-fantasy / sci-fi / modern-western-urban — NOT a culture); **Mode-D** is null; **unresolved** has no cultural home. Downstream cultural-rotation / faction surfaces (canonical/48 seasonal-rotation operator; any Fate-genre faction-architecture surface) read cultural-tradition ONLY from Mode-A/B rows, and never inherit generic-fantasy / sci-fi / modern-western as a culture. The `cultural_mode_flag` column already partitions this — nothing in the data changes; the consumption rule does. (This is the exact Mode-C artifact the §4.4 rep-audit exists to catch — the S.-American-Indigenous-Shotgun failure mode.)


> **VALUE-SPLIT (gandalf ruling §1.4; additive — DOES touch data).** The `modern-western` homonym is split: the **Mode-B** frontier rows (Western Frontier / Western Pack — the American-frontier cultural tradition, cowboys) carry the new value **`frontier-western`** (cultural-tradition); the **Mode-C** apocalypse / city / battle-royale rows retain **`modern-western`** (register-default sense, de-fanged by Option A).


### Mode-A/B — cultural-tradition-BINDING (Option A: these reads are authoritative)


#### `east-asian` [mode B] — 2 packs — cultural-tradition substrate
- **POLYGON - Samurai Empire** (chars=0) — name-token 'samurai' [mode B]: Japanese samurai tradition
- **POLYGON - Samurai Pack** (chars=8) — name-token 'samurai' [mode B]: Japanese samurai tradition

#### `norse` [mode B] — 2 packs — cultural-tradition substrate
- **POLYGON - Viking Realm** (chars=0) — name-token 'viking' [mode B]: Norse cultural tradition
- **POLYGON - Vikings Pack** (chars=1) — name-token 'viking' [mode B]: Norse cultural tradition

#### `frontier-western` [mode B] — 2 packs — cultural-tradition substrate
- **POLYGON - Western Frontier Pack** (chars=42) — name-token 'western' [mode B]: American frontier cultural tradition (cowboys; Mode-B; split from modern-western homonym per gandalf ruling 2026-06-17 §1.4)
- **POLYGON - Western Pack** (chars=2) — name-token 'western' [mode B]: American frontier cultural tradition (cowboys; Mode-B; split from modern-western homonym per gandalf ruling 2026-06-17 §1.4)

#### `egyptian` [mode A] — 1 packs — cultural-tradition substrate
- **POLYGON - Ancient Egypt** (chars=0) — name-token 'ancient egypt' [mode A]: explicit Egypt geography

#### `greco-roman` [mode B] — 1 packs — cultural-tradition substrate
- **POLYGON - Ancient Empire** (chars=11) — name-token 'ancient empire' [mode B]: greco-roman classical tradition

#### `w-euro-medieval` [mode B] — 1 packs — cultural-tradition substrate
- **POLYGON - Knights Pack** (chars=2) — name-token 'knights' [mode B]: W-European chivalric tradition

### Mode-C/D + unresolved — NON-binding (Option A: NOT a cultural-tradition read)

Mode-C = register_default_skin (genre, not culture); Mode-D = null; unresolved = no cultural home. A cultural-rotation / faction surface MUST NOT inherit these as a culture.


#### `unresolved` [mode ?] — 74 packs — no cultural home — do NOT force one
- **ANIMATION - Base Locomotion** (chars=0) — no culture token matched — gandalf rep-audit required
- **ANIMATION - Bow Combat** (chars=0) — no culture token matched — gandalf rep-audit required
- **ANIMATION - Emotes and Taunts** (chars=0) — no culture token matched — gandalf rep-audit required
- **ANIMATION - Idles** (chars=0) — no culture token matched — gandalf rep-audit required
- **ANIMATION - Sword Combat** (chars=0) — no culture token matched — gandalf rep-audit required
- **INTERFACE - Modern Menus** (chars=0) — no culture token matched — gandalf rep-audit required
- **POLYGON - Adult Face Plates** (chars=0) — no culture token matched — gandalf rep-audit required
- **POLYGON - Boss Zombies** (chars=9) — no culture token matched — gandalf rep-audit required
- …and 66 more

#### `modern-western` [mode C] — 30 packs — register_default_skin (genre, not culture)
- **INTERFACE - Apocalypse HUD** (chars=0) — name-token 'apocalypse' [mode C]: post-apoc modern-western default skin
- **INTERFACE - Military Combat HUD** (chars=0) — name-token 'military' [mode C]: modern military
- **POLYGON - Apocalypse Pack** (chars=134) — name-token 'apocalypse' [mode C]: post-apoc modern-western default skin
- **POLYGON - Apocalypse Wasteland** (chars=0) — name-token 'apocalypse' [mode C]: post-apoc modern-western default skin
- **POLYGON - Battle Royale Pack** (chars=2) — name-token 'battle royale' [mode C]: modern military-shooter
- **POLYGON - City Characters Pack** (chars=19) — name-token 'city' [mode C]: modern western-urban default
- **POLYGON - City Pack** (chars=18) — name-token 'city' [mode C]: modern western-urban default
- **POLYGON - City Zombies Pack** (chars=100) — name-token 'city' [mode C]: modern western-urban default
- …and 22 more

#### `generic-fantasy` [mode C] — 24 packs — register_default_skin (genre, not culture)
- **ANIMATION - Goblin Locomotion** (chars=0) — name-token 'goblin' [mode C]: fantasy-race allusion
- **INTERFACE - Dark Fantasy HUD** (chars=0) — name-token 'dark fantasy' [mode C]: gothic-fantasy allusion
- **INTERFACE - Fantasy Warrior HUD** (chars=0) — name-token 'fantasy' [mode C]: generic-fantasy
- **INTERFACE- Fantasy Menus** (chars=0) — name-token 'fantasy' [mode C]: generic-fantasy
- **POLYGON - Adventure Pack** (chars=10) — name-token 'adventure' [mode C]: generic-fantasy
- **POLYGON - Dark Fantasy** (chars=15) — name-token 'dark fantasy' [mode C]: gothic-fantasy allusion
- **POLYGON - Dark Fortress** (chars=0) — name-token 'dark fortress' [mode C]: gothic-fantasy allusion
- **POLYGON - Dungeon Pack** (chars=16) — name-token 'dungeon' [mode C]: generic-fantasy
- …and 16 more

#### `sci-fi` [mode C] — 12 packs — register_default_skin (genre, not culture)
- **INTERFACE - Sci-Fi Menus** (chars=0) — name-token 'sci-fi' [mode C]: sci-fi register (acultural)
- **INTERFACE - Sci-Fi Soldier HUD** (chars=0) — name-token 'sci-fi' [mode C]: sci-fi register (acultural)
- **POLYGON - Mech Pack** (chars=1) — name-token 'mech' [mode C]: sci-fi register
- **POLYGON - Sci-Fi City Pack** (chars=40) — name-token 'sci-fi' [mode C]: sci-fi register (acultural)
- **POLYGON - Sci-Fi Cyber City** (chars=18) — name-token 'sci-fi' [mode C]: sci-fi register (acultural)
- **POLYGON - Sci-Fi Horror** (chars=0) — name-token 'sci-fi' [mode C]: sci-fi register (acultural)
- **POLYGON - Sci-Fi Outpost Map** (chars=0) — name-token 'sci-fi' [mode C]: sci-fi register (acultural)
- **POLYGON - Sci-Fi Space Pack** (chars=52) — name-token 'sci-fi' [mode C]: sci-fi register (acultural)
- …and 4 more

#### `na` [mode D] — 8 packs — null cultural read (nature biome)
- **POLYGON - Alpine Mountain - Nature Biome** (chars=0) — name-token 'nature' [mode D]: nature biome — no cultural read
- **POLYGON - Arid Desert - Nature Biome** (chars=0) — name-token 'nature' [mode D]: nature biome — no cultural read
- **POLYGON - Enchanted Forest - Nature Biome** (chars=0) — name-token 'nature' [mode D]: nature biome — no cultural read
- **POLYGON - Meadow Forest - Nature Biome** (chars=0) — name-token 'nature' [mode D]: nature biome — no cultural read
- **POLYGON - Nature Pack** (chars=1) — name-token 'nature' [mode D]: nature biome — no cultural read
- **POLYGON - Swamp Marshland - Nature Biome** (chars=0) — name-token 'nature' [mode D]: nature biome — no cultural read
- **POLYGON - Tropical Jungle - Nature Biome** (chars=0) — name-token 'nature' [mode D]: nature biome — no cultural read
- **SIMPLE - Forest Animals** (chars=0) — name-token 'forest' [mode D]: nature biome

---

## §3 Density-gap findings — the base-mesh gap-fill routing surface

Gap-fill rule (brief §0/§3): temporal-cultural regions where Synty supplies NO skinned-character base route to **image-to-3D / Sidekick**, NOT to a Synty base mesh. The gap is **asymmetric by contribution layer** — a cultural register can ship rich environment+weapon coverage but a HOLLOW skinned-character base; that still forces character gap-fill.


### Finding 1 — sci-fi POLYGON skinned-character coverage: EXISTS (brief premise refuted)

The brief's apparent gap ("only `SIMPLE - Space Characters` seen; POLYGON sci-fi packs look environment-only") is **refuted by the substrate.** POLYGON sci-fi ships substantial humanoid skinned-character coverage:

- **INTERFACE - Sci-Fi Menus** — `ui`, 0 humanoid skinned chars
- **INTERFACE - Sci-Fi Soldier HUD** — `ui`, 0 humanoid skinned chars
- **POLYGON - Mech Pack** — `environment`, 0 humanoid skinned chars
- **POLYGON - Sci-Fi City Pack** — `armor-base-skinned`, 40 humanoid skinned chars
- **POLYGON - Sci-Fi Cyber City** — `armor-base-skinned`, 18 humanoid skinned chars
- **POLYGON - Sci-Fi Horror** — `environment`, 0 humanoid skinned chars
- **POLYGON - Sci-Fi Outpost Map** — `environment`, 0 humanoid skinned chars
- **POLYGON - Sci-Fi Space Pack** — `armor-base-skinned`, 52 humanoid skinned chars
- **POLYGON - Sci-Fi Worlds Pack** — `environment`, 20 humanoid skinned chars
- **SIMPLE - Space** — `environment`, 0 humanoid skinned chars
- **SIMPLE - Space Characters** — `environment`, 0 humanoid skinned chars
- **SIMPLE - Space Interiors** — `environment`, 0 humanoid skinned chars

**Answer (coverage half):** POLYGON sci-fi humanoid skinned-character base = **~110 characters** across Sci-Fi City (40), Sci-Fi Space (52), Sci-Fi Cyber City (18). These are genuine skinned bodies (Cyborg / Soldier / Mercenary / Crew / EVA-Suit / SpaceSoldier / Android). `SIMPLE - Space Characters` ships a single baked `Characters.fbx` (set-aside register). Sci-Fi *environment* packs (Horror, Outpost, Worlds-vehicles, Mech) carry NO humanoid skinned base. **Conclusion: sci-fi-body does NOT require full gap-fill** — the POLYGON consumption line already supplies a sci-fi skinned base. This UPDATES the prior-canon "sci-fi = zero coverage, full image-to-3D, deferred v1.1+" entry. (galadriel's parallel spike answers the mask-mechanism half.)


### Finding 2 — cultural-register coverage is asymmetric by contribution layer

Several named cultural registers ship environment + weapon coverage but a THIN or ABSENT skinned-character base — character gap-fill is forced even where set-dressing is rich:

- **POLYGON - Ancient Egypt** (egyptian): 0 humanoid chars, 28 weapons, `environment` — NO skinned base — char gap-fill forced
- **POLYGON - Viking Realm** (norse): 0 humanoid chars, 184 weapons, `environment` — NO skinned base — char gap-fill forced
- **POLYGON - Vikings Pack** (norse): 0 humanoid chars, 31 weapons, `environment` — NO skinned base — char gap-fill forced
- **POLYGON - Samurai Empire** (east-asian): 0 humanoid chars, 34 weapons, `environment` — NO skinned base — char gap-fill forced
- **POLYGON - Samurai Pack** (east-asian): 8 humanoid chars, 16 weapons, `armor-base-skinned` — skinned base PRESENT
- **POLYGON - Goblin War Camp** (fantasy): 0 humanoid chars, 27 weapons, `environment` — NO skinned base — char gap-fill forced
- **POLYGON - Knights Pack** (w-euro-medieval): 0 humanoid chars, 11 weapons, `accent-attach-static` — NO skinned base — char gap-fill forced
- **POLYGON - Western Frontier Pack** (modern-western): 42 humanoid chars, 15 weapons, `armor-base-skinned` — skinned base PRESENT

**Egypt + Vikings are the sharp cases:** rich weapon/environment coverage (Egypt 28 weapons, Viking-Realm 184 weapons) but ZERO/near-zero humanoid skinned base. Their character base is a gap-fill target despite the apparent 'coverage'.


### Finding 3 — ZERO-coverage cultural registers (full gap-fill route)

Searched the corpus for these registers — **none present at any layer**:

- **Mesoamerican / Aztec / Maya / Inca:** 0 packs. Full image-to-3D / Sidekick route.
- **Indo-Asian (India / Hindu / South-Asian):** 0 packs. Full gap-fill.
- **Persian / MENA / Ottoman / Arab:** 0 packs. Full gap-fill.
- **Sub-Saharan African:** 0 packs. Full gap-fill.

These match the `canonical/48` roster's later cultural registers — the rotation's non-Euro-Sinitic cultural homes are exactly where Synty supplies nothing.


### Finding 4 — steampunk / industrial thinness

- **Industrial-era set-dressing exists** but thin: only `POLYGON - War Map - WWI` and `SIMPLE - Trains` read industrial. Western (frontier 19thC) covers the modern-industrial edge but reads modern-western, not Victorian-steampunk.
- **Victorian-steampunk proper:** 0 packs. No steampunk skinned-character base — full gap-fill for a steampunk class register.


### Finding 5 — corpus-structure notes for routing

- **Sidekick Character Creator (collection 157753)** is in `collections-157.json` but is NOT a content pack — it ships no FBX corpus and is correctly absent from the 157 DB pack rows. It is the gap-fill *mechanism* (parametric humanoid base), not a tagged geometry pack. The '157 packs' = 157 DB rows across 156 content collections (Water Guns ships 2 FBX packs).
- **WAVE split is contribution-aligned:** the WAVE-2 extracted-unitypackage packs (Knights / Kids / Battle Royale / Gang Warfare / Western / Nature) contribute the `accent-attach-static` silhouette-breaker layer (`SM_Chr_Attach_*` hats/beards/hair/ammo) with only 2-3 baked whole-character meshes each. The WAVE-1 FBX SourceFiles packs contribute the skinned-character armor bases. The two waves split cleanly along the armor-base vs accent contribution axis.
- **Upstream classifier caveat (honest):** the WAVE-1 asset classifier labels rigged `SK_Veh_`/`SK_Bld_` meshes as `character` in Sci-Fi Worlds / Street Racer / Pro Racer. The contribution_role routing GUARDS these by name (they route `environment`); the asset rows are left unrewritten (reversibility — the raw classification is preserved, the routing corrects above it).

