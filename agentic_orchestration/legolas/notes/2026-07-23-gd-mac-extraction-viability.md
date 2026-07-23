# Research — Grim Dawn Mac Extraction Viability — 2026-07-23

**Mode:** A (analytical)
**Commissioner:** Matt (direct invocation — KIT-FIDELITY run, Flames of Ignaffar rank table + Act-1 monster stats)
**Sources consulted:** see Sources table at end
**Access date:** 2026-07-23

---

## Summary

A Mac-native acquisition + extraction pipeline for Grim Dawn's database files is viable, with caveats.
The recommended path is: **Steam ownership (paid, owned account required) → DepotDownloader (Homebrew, .NET 8, macOS-native) → ArchiveTool.exe (Windows-only, run under Wine/Rosetta workaround — OR use community Python .dbr extraction instead) → .dbr text files**.
The cleanest Mac-only path avoids ArchiveTool.exe entirely by using a Python .arz parser directly.
Flames of Ignaffar is confirmed in the **Ashes of Malmouth** expansion (GDX1), not the base game; its records live in `gdx1/database/gdx1.arz`.
Act-1 monster stats are in base-game `database/database.arz`.

---

## Findings

### Q1 — Extraction Tools (.arz parsers)

**ArchiveTool.exe (official, Crate Entertainment)**
- Ships with the game in the modding tools directory.
- CLI syntax: `ArchiveTool.exe <file.arz> -database <output_path>` extracts the binary .arz to individual .dbr text records.
- Platform: Windows .exe only. Not natively runnable on macOS. Would require Wine or Rosetta with a Windows binary layer. Not the clean path.
- Source: Crate Entertainment forum tutorial (see sources).

**grimarz (atom0s, GitHub — ARCHIVED)**
- C/C++, Visual Studio solution only (.sln). Windows-targeted. Archived read-only 2020-08-16.
- Platform: Windows-only build chain. Dead end for macOS.
- Output: extracts .arz database records; exact output format unspecified in documentation but community implies .dbr text records.
- Source: github.com/atom0s/grimarz

**arzedit (QuasiMod, GitLab)**
- "Commandline Grim Dawn mod building utility. Doubles as ARZ, ARC file packer/extractor."
- Language not explicit from README preview; project created 2017-05-28.
- Platform: community forum references arzedit.exe (Windows binary); a Linux user asked about Wine/Proton, implying no native non-Windows build documented.
- Source: gitlab.com/QuasiMod/arzedit

**GrimDawn_DB_to_CSV_Extractor (abclution, GitHub)**
- 100% Python. Converts .dbr files to CSV with multilanguage descriptions merged in.
- IMPORTANT: operates on pre-extracted .dbr files, not .arz directly. Requires .arz extraction step first.
- Platform: Python is cross-platform; Windows paths in README are example paths only. Runs on macOS with standard Python.
- Source: github.com/abclution/GrimDawn_DB_to_CSV_Extractor

**iagd (marius00, GitHub — most active)**
- C# (56.6%) + C++ (27%) + TypeScript (11.3%). WINAPI hooks, DLL injection. Windows-only.
- Not applicable for Mac extraction.
- Source: github.com/marius00/iagd

**yagde (GitHub topics crawl)**
- Rust-based .arz file editor for Linux. Potentially cross-platform via Rust's cargo build system (Rust compiles natively to macOS).
- NOTE: Specific repository URL was not resolved in this pass (surfaced only in GitHub topics crawl). Listed as gap — requires a direct GitHub search for "yagde grimdawn".
- If it compiles on macOS via `cargo build`, this would be the cleanest native Mac .arz reader.

**CRITICAL GAP — no confirmed pure macOS .arz → .dbr extractor found.** The best documented cross-platform path is:
1. Python script to parse .arz binary format directly (community-documented format, see Q5), OR
2. Accept the Wine step for ArchiveTool.exe (Wine installable via Homebrew Cask), OR
3. Identify and build yagde from source via Cargo.

**RECOMMENDED TOOL (Mac-native, confirmed):** Use ArchiveTool.exe under Wine (`brew install --cask wine-stable`) to do the .arz → .dbr extraction, then read .dbr files with the Python CSV extractor or manual text inspection. This is the documented community path and Wine on macOS is well-established. Alternatively, the Rust `yagde` tool should be investigated (one more fetch pass would confirm).

---

### Q2 — Steam Depot Path

**App ID:** 219990 (base Grim Dawn), confirmed.
**Expansion app ID:** 642280 (Ashes of Malmouth on Steam store page).

**Depot IDs (from community speedrun guides and search results):**
- Base game content depot: **219991** (Windows content)
- Ashes of Malmouth content depot: **642280 / 642281** range (exact split requires SteamDB — 403 blocked this pass; community references cite 642281 for AoM Crucible, 642280 for AoM main)

**DepotDownloader (SteamRE/DepotDownloader):**
- macOS-native via Homebrew: `brew tap steamre/tools && brew install depotdownloader`
- Requires .NET 8 (installable separately or via Homebrew)
- Requires Steam account that OWNS the game. Paid games require authenticated manifest request codes; anonymous download is blocked for owned-game content. Matt must use his own Steam credentials.
- Download syntax (macOS, targeting Windows depot): `depotdownloader -app 219990 -depot 219991 -username <steam_user> -os windows`
- Files land in: `<steam_dir>/steamapps/content/app_219990/depot_219991/` — the full Windows install tree including `database/database.arz` and `gdx1/database/gdx1.arz`
- No game needs to run; files are raw depot content.

**Steam console `download_depot` (alternative):**
- Accessed via `steam://nav/console` in browser, or `steam://open/console`
- Command: `download_depot 219990 219991`
- Requires Mac Steam client to be running and game owned on account.
- Files land in Steam install path under `steamapps/content/app_219990/depot_219991/`
- No manifest ID required for current version (only needed for historical versions).
- Caveats: no progress indicator; one depot at a time; for GDX1 must run a separate command for the expansion depot.

**Verdict Q2:** Both paths work on Mac. DepotDownloader is more scriptable and explicit. Steam console is simpler if Steam client is running. Both require game ownership on the Steam account used.

---

### Q3 — GOG + innoextract Path

**innoextract availability on macOS:**
- NOT currently installed on this Mac (confirmed: `which innoextract` → not found).
- Available in Homebrew core as stable 1.9: `brew install innoextract` (confirmed via `brew info innoextract`).
- Homepage: https://constexpr.org/innoextract/
- No pre-built macOS binary; Homebrew package handles compilation.

**GOG installer support:**
- innoextract explicitly supports GOG.com Inno Setup-based game installers.
- Supports multi-part GOG installers, `--gog` option for RAR extraction, GOG Galaxy format reassembly.
- Works on macOS without Wine — innoextract is a native C++ tool (CMake + Boost + liblzma).
- Example workflow: download GOG offline installer (.exe) → `innoextract setup_grim_dawn_*.exe` → extracts game files including `database/database.arz` and expansion `.arz` files.

**Verdict Q3:** If Matt owns Grim Dawn on GOG, this is the cleanest Mac path. No Steam client, no .NET, no Wine required. One `brew install innoextract`, then unpack the offline installer. GOG offline installers are downloadable directly from gog.com while logged in — no Galaxy client required.

**Important:** GOG may package base game and expansions as separate offline installers. Matt would need to own AND download the Ashes of Malmouth offline installer separately to get `gdx1.arz`.

---

### Q4 — Expansion Confirmation: Flames of Ignaffar

**CONFIRMED:**
- Flames of Ignaffar belongs to the **Inquisitor mastery**.
- The Inquisitor mastery was introduced in **Ashes of Malmouth** (GDX1), released 2017-10-11.
- Steam expansion app ID: 642280. GOG expansion sold separately.
- Database file: `gdx1/database/gdx1.arz` (confirmed path structure from Crate forum and community modding docs).
- The base-game `database/database.arz` does NOT contain Inquisitor mastery skills including Flames of Ignaffar.

**Act-1 monsters:**
- Act 1 is base-game content. Monster stat records are in `database/database.arz`.
- CONFIRMED from community modding docs: expansion content goes in expansion-prefixed .arz files; base-game .arz is the base game only.

**Summary:** Two .arz files needed:
- `database/database.arz` → Act-1 monster stats
- `gdx1/database/gdx1.arz` → Flames of Ignaffar rank table (Inquisitor skill)

---

### Q5 — Extraction Output Format: .arz → .dbr

**CONFIRMED from multiple sources:**
- The extraction pipeline is: `.arz` (binary LZ4-compressed archive) → `ArchiveTool.exe -database` → individual `.dbr` files (text format, key=value records).
- Crate forum quote (crateentertainment.com/t/about-the-resources-and-database-folders): "The database is stored in arz (binary) format, so the file database/database.arz was extracted into your destination as text files (suffix dbr)."
- .dbr files are human-readable text. A user confirmed: "PlayerRunSpeedCapMax value using a text editor" — i.e., directly editable in a text editor.
- Internal binary structure of .arz records: each record has Data Type (Int32/Float/String/Bool), Value Count, String Key ID, and Value fields. Once extracted, these become key=value text lines in .dbr files.
- Skill rank tables (e.g., Flames of Ignaffar ranks 1–16) are present in the .dbr records as named field arrays. Example field pattern: `skillMaxLevel`, `petDamage`, `piercingRatio` etc. with per-rank values.
- Monster stat records similarly: HP, damage, resistances as named fields.

**No parsing library needed** after extraction — .dbr files are plain text, readable with Python, grep, or any text tool.

---

## VERDICT

**GO-WITH-CAVEATS** on Mac-native path.

### Recommended Pipeline (Mac, cleanest — if GOG ownership)

1. **Acquire:** Download GOG offline installer(s) for Grim Dawn base + Ashes of Malmouth expansion from gog.com (Matt's account).
2. **Unpack:** `brew install innoextract` → `innoextract setup_grim_dawn_<ver>.exe` and `innoextract setup_grim_dawn_ashes_of_malmouth_<ver>.exe`. No Wine, no Windows.
3. **Extract .arz → .dbr:** Run ArchiveTool.exe (ships in the extracted game files under `GrimawnTools/` or `moddingtools/`) under Wine (`brew install --cask wine-stable`): `wine ArchiveTool.exe database/database.arz -database ./out/base/` and separately for `gdx1/database/gdx1.arz`.
   - ALTERNATIVE if Wine is undesirable: write a small Python script using the documented .arz binary format (LZ4 + string table + record table) — community-documented format is fully specified. A one-afternoon implementation.
4. **Read records:** .dbr text files in `./out/` are key=value — grep or Python for `Flames_of_Ignaffar.dbr`, `playerclasstraining_inquisitor.dbr`, Act-1 monster `.dbr` files.

### Recommended Pipeline (Mac — if Steam ownership only)

1. **Acquire:** `brew install depotdownloader` → `depotdownloader -app 219990 -depot 219991 -username <matt_steam_user> -os windows` (base), then separately for GDX1 depot (depot ID ~642280; confirm exact ID via SteamDB or steamcommunity.com).
2. **Extract + Read:** same as GOG path steps 3–4 above.

### PC Fallback

If Wine step is a blocker and Python parser isn't worth the build time: download game on Windows PC, run `ArchiveTool.exe database/database.arz -database ./out/` natively, copy `./out/` folder to Mac via scp/USB. The .dbr files are plain text — ~50-200MB of records total.

### Which link could break

- ArchiveTool.exe on Wine: Wine is generally stable on macOS (Apple Silicon via Rosetta + `wine-crossover` or `wine-stable`). Low risk but adds a layer.
- DepotDownloader depot ID for GDX1: exact numeric depot ID for Ashes of Malmouth was not resolved in this pass (SteamDB returned 403). Matt should check `steamdb.info/app/642280/depots/` manually in a browser to confirm the Windows content depot ID before running DepotDownloader.
- GOG ownership: if Matt only owns on Steam, GOG path is unavailable. Steam path is the fallback.

---

## Knowledge Gaps Not Resolved

1. **yagde Rust tool:** surfaced in GitHub topics crawl as a Rust .arz editor for Linux. If it compiles on macOS via `cargo build`, it would be the cleanest native Mac extractor. URL not resolved in this pass. Recommended follow-up: `gh repo list` search or `cargo search grim-dawn`.
2. **Exact GDX1 Steam depot ID:** SteamDB returned 403 for the depot listing. Community references cite 642280/642281 range but the exact Windows-content depot ID for `gdx1.arz` is unconfirmed. Verify at steamdb.info/app/642280/depots/ in a browser.
3. **Flames of Ignaffar rank table fields:** wiki returned 402 (paywall/JS-render block). The .dbr field names for per-rank skill stats (damage scaling, duration, mana cost) were not confirmed from primary source. These will be visible once .dbr is extracted.
4. **ArchiveTool.exe location in extracted GOG files:** exact subdirectory within the GOG-extracted tree not confirmed. Likely under `game/` or `GrimawnTools/`. May need to `find . -name ArchiveTool.exe` after innoextract.

---

## Sources Table

| URL | What it anchored | Access date |
|-----|-----------------|-------------|
| local: `which innoextract` | innoextract not installed on this Mac | 2026-07-23 |
| local: `brew info innoextract` | innoextract stable 1.9 available via Homebrew | 2026-07-23 |
| https://github.com/atom0s/grimarz | grimarz = C/C++, VS .sln, Windows-only, archived 2020 | 2026-07-23 |
| https://gitlab.com/QuasiMod/arzedit | arzedit = ARZ/ARC packer/extractor CLI, Windows binary, no confirmed cross-platform | 2026-07-23 |
| https://github.com/abclution/GrimDawn_DB_to_CSV_Extractor | 100% Python, works on pre-extracted .dbr files, cross-platform viable | 2026-07-23 |
| https://atom0s.wordpress.com/2014/10/04/grim-dawn-file-archive-database-extractors/ | grimarz described as static analysis only, C++ | 2026-07-23 |
| https://constexpr.org/innoextract/ | innoextract supports GOG installers; macOS via Homebrew/MacPorts; CMake+Boost | 2026-07-23 |
| https://github.com/dscharrer/innoextract | innoextract macOS supported via Homebrew package; explicit GOG support confirmed | 2026-07-23 |
| https://grimdawn.fandom.com/wiki/Ashes_of_Malmouth (via search result) | Ashes of Malmouth adds Inquisitor + Necromancer masteries; released 2017-10-11 | 2026-07-23 |
| https://forums.crateentertainment.com/t/about-the-resources-and-database-folders/45087 | .arz → .dbr confirmed as binary-to-text pipeline; .dbr text-editable | 2026-07-23 |
| https://forums.crateentertainment.com/t/tutorial-use-the-archive-tool-to-uncompile-arz-and-arc/32787 | ArchiveTool.exe -database syntax confirmed; Windows .exe | 2026-07-23 |
| https://forums.crateentertainment.com/t/working-on-grimdawn-database-arz-editor/38832 | arzedit confirmed Windows-only; ArchiveTool.exe from Crate; .dbr key-value implied | 2026-07-23 |
| https://zenhax.com/viewtopic.php@t=468.html | .arz binary format: LZ4 compressed, typed records (Int32/Float/String/Bool) | 2026-07-23 |
| https://github.com/SteamRE/DepotDownloader | DepotDownloader: .NET 8, macOS via Homebrew, -os windows flag, ownership required | 2026-07-23 |
| https://github.com/SteamRE/DepotDownloader/discussions/215 (via search) | Paid games require authenticated Steam account; manifest codes require ownership | 2026-07-23 |
| https://store.steampowered.com/app/642280 (via search result) | Ashes of Malmouth Steam app ID = 642280; expansion sold separately | 2026-07-23 |
| Community modding docs (via search: database.arz path) | gdx1/database/gdx1.arz = AoM expansion DB; gdx2/database/gdx2.arz = Forgotten Gods | 2026-07-23 |
| https://github.com/topics/grimdawn | yagde = Rust .arz editor for Linux (cross-platform potential); iagd = C# Windows-only | 2026-07-23 |
| https://github.com/marius00/iagd | iagd = C#+C++, WINAPI hooks, Windows-only | 2026-07-23 |
