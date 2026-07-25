# Research — GD Custom Game Console Unlock — 2026-07-25

**Mode:** A (analytical)
**Commissioner:** Matt (direct; unblocks live playtest session)
**Sources consulted:**
- `/Users/admin/Games/vendor/grim-dawn/Grim Dawn Modding Guide.pdf` (Crate official, v1.2, 2016) — primary
- `/Users/admin/Games/vendor/grim-dawn/Grim Dawn.exe` — binary inspection (strings extraction)
- `/Users/admin/Games/vendor/grim-dawn/Engine.dll` — binary inspection (ARZ loading sequence)
- `/Users/admin/Games/vendor/grim-dawn/Game.dll` — binary inspection (console command registry)
- `/Users/admin/Games/vendor/grim-dawn/mods/survivalmode/database/SurvivalMode.arz` — ARZ parse
- `/Users/admin/Games/vendor/grim-dawn/survivalmode1/database/SurvivalMode1.arz` — ARZ parse
- `/Users/admin/Games/vendor/grim-dawn/survivalmode2/database/SurvivalMode2.arz` — ARZ parse
- `/Users/admin/Games/vendor/grim-dawn/database/database.arz` — ARZ parse (vanilla reference)
- `/Users/admin/Games/vendor/grim-dawn/ModdingTutorial.zip` — zip listing
- Prior research: `2026-07-24-playtest-capture-instrument-scoping.md` §2.4

---

## Headline — most consequential finding first

**Q1 result is UNRESOLVED and requires a 30-second test on Matt's machine before anything else.**

The prior research (§2.4, community sources) claimed the console is accessible "only in Custom Game mode." Binary inspection of `Grim Dawn.exe` finds NO conditional guard matching that claim: the `WidgetConsole` is registered unconditionally and bound to the `accentgrave` key (the backtick/tilde key) without any game-mode check visible in string data. Additionally, `autorun.txt` is read at game startup (before mod or map loading) and may execute console commands without any mode gate. If the console is accessible in Campaign mode, the Custom Game problem dissolves.

**Matt should press the backtick/tilde key (\`) in a running Campaign session right now.** If a console opens, commands `character.ShowAngerLevels` and `character.LogData` can be run there. The prior community claim may be wrong, outdated, or misattributed.

If the console does NOT open in Campaign, proceed to Q4 (the ModdingTutorial path).

---

## Q1 — Is the console REALLY Custom-Game-only, or is there a launch flag?

### Binary evidence from `Grim Dawn.exe`

The console command table is registered in `Grim Dawn.exe` at offset ~2680700–2686700. It contains all expected commands — `character.ShowAngerLevels`, `character.LogData`, `game.God`, `game.Invincible`, `character.SetPlayerInvisible`, etc. — with no conditional flag around them. The `WidgetConsole::Render` function is bound to the `accentgrave` key (tilde/backtick) in the key-binding section of the same binary. No string matching "Custom Game" appears adjacent to the console initialization.

### Launch flags found in `Grim Dawn.exe`

Binary inspection revealed the following launch flags registered in the exe:

```
/basemods  /map  /player  /exec  /logPerformance  +connect  /demo  /nocommit
/rcompat   /renderer  /d3d9  /d3d11  /d3d12  /sound  /nogdx1  /nogdx2  /nogdx3
```

`/exec` is registered alongside console command "Exec — Executes a script." This may allow running a script of console commands at launch via `"Grim Dawn.exe" /exec mycommands.txt`. **Unconfirmed** — the flag is present in the binary but its argument format and exact behavior are not documented in the modding guide.

### `autorun.txt` mechanism

The string `autorun.txt` appears in `Grim Dawn.exe` immediately in the game initialization sequence (after "Grim Dawn %s initializing..." and before any mod loading). This is consistent with `autorun.txt` being read and executed at game startup as a console script, independent of game mode. This is a documented behavior in Titan Quest (same engine lineage), but **not confirmed in GD by any non-community source we can access**. If it works, an `autorun.txt` in the GD installation directory containing `character.ShowAngerLevels 1` would enable the overlay without Custom Game.

### What prior research §2.4 said

Prior research (web sources, mostly 403'd) stated the console is "accessible only in Custom Game mode." This is community-sourced, not verified from binary or Crate documentation. The binary analysis does not confirm this gate. The claim may describe a UI design decision (tilde key only opens the console when no menu is blocking), not a code gate — in which case it may simply work in Campaign too once you're in-world.

**Action required:** Test backtick/tilde in Campaign before spending any time on a mod.

---

## Q2 — Does the Crucible (survivalmode) appear in the Custom Game list?

**No. Crucible is a separate main-menu entry, not a Custom Game mod.**

Binary evidence: `Grim Dawn.exe` contains three separate localization tags in its menu structure:
- `tagPlayGameModeCampaign`
- `tagPlayGameModeCustom`
- `tagPlayGameModeSurvival`

The string `survivalmode` is hardcoded in the exe with dedicated handling, and its resource path appears as `mods/survivalmode/Resources/<something>.map` — loaded via its own code path, not via the generic Custom Game loader.

**Even if Crucible appeared in Custom Game, it would be the wrong arena.** The ARZ analysis below rules it out on contamination grounds.

### Crucible ARZ contamination — EMPIRICALLY CONFIRMED, ALL THREE VERSIONS

The calibration targets are: `ViewDistance`, `SightAngerRate`, `InnerSightAngerRate`, `MaxPursuitDistance`, `PursuitTime`, `WanderDistance`, `distressCallRange` — all read from vanilla `database/database.arz` controller records.

ARZ parsing of all three Crucible database files confirms contamination:

**`mods/survivalmode/database/SurvivalMode.arz`** (3,147 records total):
- 175 controller records contain the target AI fields
- All show systematic overrides vs. vanilla; representative examples:
  - `ViewDistance`: 80.0 across Crucible (vanilla: 15.0–16.0)
  - `MaxPursuitDistance`: 125.0 across Crucible (vanilla: 60.0–75.0)
  - `SightAngerRate`: 5.0 (vanilla: 4.0–8.0, monster-dependent)
- 984 of 1,083 creature records with `distressCallRange` differ from vanilla (bumped to 50.0; vanilla: 15–20)

**`survivalmode1/database/SurvivalMode1.arz`** (1,004 records):
- 56 controller records with AI field overrides
- Pattern: `ViewDistance` = 80.0, `MaxPursuitDistance` = 125.0 across all

**`survivalmode2/database/SurvivalMode2.arz`** (811 records):
- 63 controller records with AI field overrides
- Same pattern: `ViewDistance` = 80.0, `MaxPursuitDistance` = 125.0

**Verdict: All Crucible database versions aggressively expand monster aggro range (ViewDistance 80 vs vanilla 15, MaxPursuitDistance 125 vs vanilla 65–75). Any measurement taken in Crucible would describe Crucible-tuned AI, not vanilla AI. Crucible is unusable as a measurement arena.**

---

## Q3 — Would a "vanilla-passthrough" mod work?

The hypothesis: create `mods/probe/database/database.arz` as a byte-identical copy of vanilla `database/database.arz`, and include `mods/probe/resources/Maps.arc` with a minimal compiled world.

**Findings on each sub-question:**

### (a) Must the .arz filename match the mod folder name?

**No. User mods must use the filename `database.arz`.**

Evidence:
- Crate modding guide (v1.2, Tutorial 01): "The files other players need to play your mod are: `/steamapps/common/Grim Dawn/mods/ModName/database.arz`" — explicit flat filename.
- `Engine.dll` loading sequence (binary): the engine loads these archives in order: `/database/database.arz` → `/gdx1/database/gdx1.arz` → `/gdx2/database/gdx2.arz` → `/gdx3/database/gdx3.arz` → `/survivalmode1/database/survivalmode1.arz` → `/survivalmode2/...` → `/survivalmode3/...` → `/mods/database.arz`. The `/mods/database.arz` suffix is the user mod slot — the engine prepends the mod's folder path at runtime.

`SurvivalMode.arz`, `SurvivalMode1.arz`, `SurvivalMode2.arz` use folder-named files because they are Crate-internal hardcoded entries, not user mods loaded via the Custom Game path.

**A vanilla-passthrough mod must have its ARZ at `mods/probe/database/database.arz`.**

### (b) Does a mod's .arz replace the base database or merge/override?

**Override (later load wins on matching records).** The Engine.dll loading sequence is strictly ordered: vanilla `database.arz` loads first, then expansions, then the user mod last. A later-loading archive's records override earlier matching records. A byte-identical copy of vanilla `database.arz` placed in the mod position would override each of the 34,114 vanilla records with identical values — net behavioral delta of zero. **The vanilla-passthrough hypothesis on the database side is correct. A byte-identical copy is a provable no-op.**

### (c) Is Levels.arc sufficient for a world, or does the game need a specific map declaration?

**Levels.arc cannot be used directly as Maps.arc.** The game expects a compiled world in `resources/Maps.arc` within the mod directory. Vanilla's `resources/Levels.arc` (221 MB) contains the entire campaign world in ARC format, but it is not in the correct path or structure to satisfy a Custom Game map requirement. A Custom Game mod needs `mods/<modname>/resources/Maps.arc` containing a compiled `.wrl` world.

### (d) Is there a mod manifest file required?

**No manifest file found in survivalmode or documented in the guide.** The only required files are `database/<name>.arz` and `resources/*.arc`. No `mod.txt`, `modinfo.xml`, or manifest was found in any mod directory structure examined.

### Net verdict on Q3

The vanilla-passthrough hypothesis is **partially valid** and **partially incomplete**:

- The database side works: a byte-identical copy of `database.arz` (renamed to `database.arz`) in `mods/probe/database/` would be a provable no-op on all calibration variables.
- The map side does NOT work by copying `Levels.arc`. A compiled world must be provided in `Maps.arc`. **The hypothesis as stated (copy Levels.arc) is WRONG for the map component.**

The cheapest fix: build the ModdingTutorial world to provide the Maps.arc (see Q4).

---

## Q4 — If Q3's map gap fails, what is the cheapest legitimate path?

### Recommended path: Build the ModdingTutorial (Crate's own, no third-party content)

`ModdingTutorial.zip` (in the game installation directory) ships with full source files including a buildable world:

- `source/Maps/TutorialWorld.wrl` (16,656 bytes) — world descriptor
- `source/Maps/TutorialWorld.sd` (965 bytes) — scene descriptor
- `source/Maps/Region01.lvl`, `Region01.rlv`, `Region01.tga` — compiled region data

This is NOT just a stub. The 48-byte `assets/Maps/TutorialWorld.map` is the build-output pointer; the full source is in `source/Maps/`. The AssetManager (Windows tool, `AssetManager.exe` in the GD install directory) can build this mod on Matt's Windows PC.

**Steps:**
1. Extract `ModdingTutorial.zip` into the GD installation's `mods/` directory (so that `mods/ModdingTutorial/` exists).
2. Launch `AssetManager.exe`.
3. Open the ModdingTutorial mod (Mod dropdown).
4. Go to Build → Build. This compiles the source to `mods/ModdingTutorial/database/database.arz` + `mods/ModdingTutorial/resources/Maps.arc` (and other arcs).
5. Launch Grim Dawn → Custom Game → the tutorial mod should appear.
6. The ModdingTutorial's `database.arz` contains only the tutorial's custom enemies/items — it does NOT override vanilla controller records for the calibration variables.
7. Once in a Custom Game session with the tutorial, press backtick. Issue `character.ShowAngerLevels` and `character.LogData`.

**Contamination check for the tutorial mod:** The ModdingTutorial source only defines custom test enemies (`TestBoar`, `TestPrawn`, `TestBoss`), custom NPCs, and custom items. It does NOT define controller records. When the tutorial's `database.arz` is built, it will contain only these custom records. Vanilla controller records (`ViewDistance`, `SightAngerRate`, etc.) will come from vanilla `database.arz` unmodified. **The tutorial mod is clean for our calibration purposes, as long as measurement is done on vanilla campaign monsters (not the tutorial's TestBoar/TestPrawn).**

**To measure vanilla monsters in the tutorial map:** spawn vanilla campaign enemies using `game.Spawn records/creatures/enemies/<target>.dbr` from the console, or simply confirm that the console does work in the tutorial world and then switch to testing in Campaign mode if Q1 turns out to not require Custom Game.

### Alternative to consider: autorun.txt

If the console is gated to Custom Game (Q1 unresolved) but `autorun.txt` is not, Matt could:
1. Create a file `autorun.txt` in the GD installation directory.
2. Add the line `character.ShowAngerLevels 1` (exact syntax unconfirmed).
3. Launch the game normally. If autorun.txt executes console commands at startup, the overlay would activate in any game mode.

This is **unverified behavior** — not in the modding guide, and the community sources 403'd. Treating as a quick-test candidate, not a confirmed path.

---

## Coverage-boundary declaration (D-a, MANDATORY)

**What I could check and DID check:**
- All binary strings in `Grim Dawn.exe`, `Engine.dll`, `Game.dll` via Python regex extraction (Mac-resident; DLLs are Windows PE binaries — inspecting strings only, not executing)
- Full ARZ parse of `database.arz` (34,114 records), `SurvivalMode.arz` (3,147), `SurvivalMode1.arz` (1,004), `SurvivalMode2.arz` (811) using the proven ARZ adapter; confirmed 0 decompression errors in all four files after correcting for a count-prefixed string table format variant in the mod ARZs
- Full mod directory structure for `mods/survivalmode/`, `survivalmode1/`, `survivalmode2/`, `mods/` root
- `ModdingTutorial.zip` full file listing; confirmed `.wrl` world source IS present
- Crate modding guide PDF cover-to-cover via `pdftotext`
- `Scripts.arc` and `System.arc` raw string inspection (no console-related strings found in these two files; they contain Lua gameplay scripts and UI mesh/shader data)

**What I could NOT check:**
- Whether the tilde console actually opens in Campaign mode at runtime — binary strings do not confirm the runtime conditional; only a live test resolves this
- `autorun.txt` actual behavior — present in the init sequence string but behavior (whether it auto-executes console commands) is not confirmed from binary alone; community sources 403'd
- The `/exec` launch flag's argument format and whether it executes console scripts pre-world-load
- The `DummyMod` + `levels/world001.map` runtime path — this string pair appears in player save-data parsing code and may represent a fallback/dev mode; its accessibility to a regular user is unconfirmed
- Crate forum documentation and community guides (403 on Crate forums; no alternative primary source found)
- Whether AssetManager on Windows PC will successfully build the ModdingTutorial on a current GD installation (v1.3.x, post-FoA) — the tutorial source is from 2016; template compatibility is not verified
- Version skew warning: the modding guide is v1.2 (2016); the depot is v1.3.0.0 (2026-07-23, Fangs of Asterkarn). The guide predates 7+ years of patches. Specific guide claims (e.g., "database.arz" filename) are corroborated by Engine.dll binary evidence. Claims not corroborated by binary should be treated as version-uncertain.

---

## Recommended procedure for Matt (Windows PC, in priority order)

**Step 0 — Test tilde in Campaign RIGHT NOW (30 seconds):**
1. Load any existing Campaign character to the in-world state (not the menu).
2. Press the backtick/grave key (`` ` ``, usually left of 1 on US keyboards; may also be apostrophe).
3. If a console appears: type `character.ShowAngerLevels 1`, press Enter, then `character.LogData 1`. Done.
4. If no console appears: proceed to Step 1.

**Step 1 — Try autorun.txt (2 minutes, no mod required):**
1. Create a file named `autorun.txt` in the GD installation directory (`steamapps/common/Grim Dawn/`).
2. Add the line: `character.ShowAngerLevels 1`
3. Launch GD normally. Load a Campaign character. Check if the anger overlay appears.
4. If it works: you have console command access without Custom Game.
5. If it does not work: proceed to Step 2.

**Step 2 — Build the ModdingTutorial (15–30 minutes):**
1. Extract `ModdingTutorial.zip` (in `steamapps/common/Grim Dawn/`) to the `mods/` subdirectory. Result: `steamapps/common/Grim Dawn/mods/ModdingTutorial/` with `assets/`, `database/`, `source/` subdirectories.
2. Launch `AssetManager.exe` from the GD installation directory.
3. At first-time setup: set Working directory = GD installation directory; Build directory = same.
4. Open the `ModdingTutorial` mod (Mod menu → should list it).
5. Build → Build. Wait for completion.
6. Launch GD → Play Custom Game → select ModdingTutorial → create a new character.
7. Enter the tutorial world. Press backtick.
8. Issue: `character.ShowAngerLevels 1` then `character.LogData 1`.
9. To measure vanilla monsters: use `game.Spawn` to spawn a vanilla enemy, OR test on the tutorial's test enemies (TestBoar, TestPrawn) to validate the console overlay works, then move to Campaign for actual measurement.

**Do NOT use Crucible (Survival mode) for any measurement.** All three Crucible ARZs inflate `ViewDistance` to 80 (vanilla: 15) and `MaxPursuitDistance` to 125 (vanilla: 65–75). Measurements taken in Crucible describe Crucible-tuned AI.

---

## Source list

| Source | Type | Location |
|---|---|---|
| Grim Dawn Modding Guide.pdf (v1.2, 2016) | Primary — Crate official | `/Users/admin/Games/vendor/grim-dawn/Grim Dawn Modding Guide.pdf` |
| Grim Dawn.exe (v1.3.0.0, 2026-07-23) | Primary — binary | `/Users/admin/Games/vendor/grim-dawn/Grim Dawn.exe` |
| Engine.dll (v1.3.0.0) | Primary — binary | `/Users/admin/Games/vendor/grim-dawn/Engine.dll` |
| Game.dll (v1.3.0.0) | Primary — binary | `/Users/admin/Games/vendor/grim-dawn/Game.dll` |
| database.arz (vanilla) | Primary — database archive | `/Users/admin/Games/vendor/grim-dawn/database/database.arz` |
| SurvivalMode.arz | Primary — database archive | `/Users/admin/Games/vendor/grim-dawn/mods/survivalmode/database/SurvivalMode.arz` |
| SurvivalMode1.arz | Primary — database archive | `/Users/admin/Games/vendor/grim-dawn/survivalmode1/database/SurvivalMode1.arz` |
| SurvivalMode2.arz | Primary — database archive | `/Users/admin/Games/vendor/grim-dawn/survivalmode2/database/SurvivalMode2.arz` |
| ModdingTutorial.zip (2016) | Primary — Crate tutorial source | `/Users/admin/Games/vendor/grim-dawn/ModdingTutorial.zip` |
| Prior research §2.4 | Secondary — community-sourced claims | `research/knowledge/gd/2026-07-24-playtest-capture-instrument-scoping.md` |
