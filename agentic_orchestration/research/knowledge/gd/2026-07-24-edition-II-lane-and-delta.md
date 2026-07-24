# Research — GD Edition-II Lane Establishment — 2026-07-24

**Mode:** A (analytical)
**Commissioner:** gandalf
**Authorized by:** Matt, 2026-07-24
**Sources consulted:**
- Steam Web API appdetails endpoint (appids=2699230, accessed 2026-07-24) — primary
- Steam Web API packagedetails endpoint (packageids=966567, accessed 2026-07-24) — primary
- SteamDB search results (secondary; direct page access 403-blocked)
- Multiple Steam community announcement URLs (secondary; confirmed title only)
- Edition-I `.DepotDownloader/*.manifest` files — primary binary (manifest string extraction)
- `agentic_orchestration/gandalf/notes/2026-07-24-gd-edition-I-freeze-fingerprint.md`

---

## Summary

**Q2 step 1 is complete. Step 2 (the actual depot fetch) halts here — it requires Matt's authenticated Steam session.**

The expansion title is confirmed as **"Grim Dawn - Fangs of Asterkarn"** (Steam API primary source). The DLC app ID is **2699230** (Steam API primary). The Edition-I depot mapping is now fully verified from manifest string extraction (no longer inferred). The expansion's specific depot IDs cannot be retrieved without Steam authentication — the SteamDB API returns 403 and the Steam Web API's appdetails endpoint does not expose depot IDs for DLC apps. The safe fetch command uses `-app 2699230` and lets DepotDownloader enumerate its own depot list from Steam's authenticated CDN; a specific `-depot` flag cannot be responsibly populated without verified IDs. The staged command is below.

---

## Findings

### Expansion title — verified from source

- **Matt's recollection:** "Flames of Asterkarn"
- **Gandalf's recollection:** "Fangs of Asterkarn"
- **Verified title (Steam API primary):** `Grim Dawn - Fangs of Asterkarn`
- **Source:** `https://store.steampowered.com/api/appdetails?appids=2699230` — `data.name` field, accessed 2026-07-24
- **Corroborating sources:** Steam store page `store.steampowered.com/app/2699230/`, Steam announcement `steamcommunity.com/games/219990/announcements/detail/687507011804332720`, Crate forums announcement `forums.crateentertainment.com/t/grim-dawn-fangs-of-asterkarn-releases-july-23rd-2026/154855`, Grim Dawn wiki `grimdawn.fandom.com/wiki/Fangs_of_Asterkarn`

**Gandalf's recollection was correct. Matt's recollection ("Flames") was wrong.** Both recollections were appropriately excluded as lookup parameters per the commission's standing constraint.

### DLC app ID — verified from source

- **App ID:** `2699230`
- **Type:** `dlc` (Steam API `data.type`)
- **Parent game:** App 219990 (Grim Dawn base game), confirmed by `data.fullgame.appid`
- **Package ID:** 966567 (confirmed by both appdetails and packagedetails endpoints)
- **Release date:** July 23, 2026
- **Price:** $18.99 USD
- **Requirements:** Requires Forgotten Gods (897670) and Ashes of Malmouth (642280) DLCs to play — relevant for fetch order

### Edition-I depot mapping — now fully verified

Prior to this investigation, depots 897670/897671 were labeled "presumed Forgotten Gods" in the freeze fingerprint (§4). The manifest files in `.DepotDownloader/` contain file path strings extractable as ASCII runs. Results:

| depot_id | Extracted path evidence | Verified identity |
|---|---|---|
| 219991 | (base Windows binary content — not examined; presumed from prior notes) | Base game Windows content |
| 228983–228986, 228990, 229003, 483840 | (base game asset/audio depots — not examined individually) | Base game asset depots |
| 642280 | `gdx1\database\GDX1.arz`, `gdx1\resources\Text_EN.arc` | Ashes of Malmouth (gdx1) main content — **verified** |
| 642281 | `survivalmode1\database\SurvivalMode1.arz` | Ashes of Malmouth Crucible / Survival Mode 1 — **verified** |
| 897670 | `gdx2\database\GDX2.arz`, `gdx2\resources\Text_EN.arc` | Forgotten Gods (gdx2) main content — **verified** |
| 897671 | `survivalmode2\database\SurvivalMode2.arz` | Forgotten Gods Crucible / Survival Mode 2 — **verified** |

The freeze fingerprint's "presumed Forgotten Gods" note for 897670/897671 is now confirmed correct. The SteamDB search result also corroborates: `steamdb.info/depot/897671/` is labeled "Grim Dawn - Forgotten Gods Crucible" in public search result snippets.

**Correction to gandalf freeze fingerprint §4:** The note says "897670/897671 = presumed Forgotten Gods (gdx2) — not verified, inferred from the presence of GDX2.arz." These are now verified. The `survivalmode2/` path confirms 897671 is the Crucible/Survival mode DLC for Forgotten Gods specifically, which aligns with the SteamDB name "Grim Dawn - Forgotten Gods Crucible."

### Fangs of Asterkarn depot IDs — NOT YET VERIFIED (step 2 blocked)

The Steam Web API `appdetails` endpoint does not expose depot IDs in its response for DLC apps. SteamDB (`steamdb.info/app/2699230/depots/`) returns HTTP 403. No public source consulted during this investigation returned verified depot IDs for app 2699230.

**What is known:** App 2699230 is the correct DLC app for the expansion. DepotDownloader with `-app 2699230` will authenticate to Steam and enumerate all depots belonging to this app automatically; explicit `-depot` flags are not required to fetch the expansion content. The prior Edition-I fetch also used `-app` level commands (the depot.config in the Edition-I tree enumerates 12 depots that were fetched as a group).

**What is NOT known (and must not be guessed):** The specific depot ID numbers (e.g., 2699231, 2699232, etc.) for the expansion's content. No depot ID for Fangs of Asterkarn was verified from any source during this pass. These will be visible in the `.DepotDownloader/` directory after Matt runs the authenticated fetch.

### Notes on `records/fx/skillsothergdx3/` signal in Edition-I

The freeze fingerprint §5 flags a single `records/fx/skillsothergdx3/...` FX path in `database.arz`. This path is present in the Edition-I `.arz` as a bare string reference (likely an FX reference baked into a base-game record that points to a GDX3 path). It does not indicate expansion content is present in Edition-I; it indicates Crate pre-wired FX paths for expansion content in the base game binary before the expansion shipped. This is consistent with how `Asterkarn` strings exist in the base game as pre-existing Act-4 geography.

---

## Staged fetch command (Matt executes)

**Preconditions before running:**
1. Edition-I bytes are intact at `/Users/admin/Games/vendor/grim-dawn-edition-I-20260723/` (SHA-256 inventory in freeze fingerprint confirms). Do NOT let this command touch that directory.
2. `/Users/admin/Games/vendor/grim-dawn/` still holds Edition-I bytes (verify before any Steam operation). DepotDownloader may update this directory in-place. If Edition-I bytes need to be preserved there too, copy it first or fetch to a new directory.
3. Target directory does not exist yet (prevents accidental overwrite).

**Command (fetch to new directory, Edition-I untouched):**

```bash
/opt/homebrew/bin/depotdownloader \
  -app 2699230 \
  -username <matt_steam_username> \
  -dir /Users/admin/Games/vendor/grim-dawn-edition-II-20260724 \
  -os windows \
  -filelist /dev/stdin <<'FILELIST'
regex:.*\.arz$
regex:.*Text_EN\.arc$
FILELIST
```

**Rationale for filelist filter:** The Edition-I fetch included all `.arz` and `Text_EN.arc` files and excluded the ~9.7 GB of art/audio/binary content. The same scope applies here so the delta is meaningful (comparing what the adapter consumes). If the filelist approach is unavailable or inconvenient, `-manifest-only` first to inspect what depots and files are included, then decide scope.

**Alternative (fetch all depots for the app, no filelist):**
```bash
/opt/homebrew/bin/depotdownloader \
  -app 2699230 \
  -username <matt_steam_username> \
  -dir /Users/admin/Games/vendor/grim-dawn-edition-II-20260724
```

This fetches everything in all depots for the expansion DLC, including art/audio. Will be large (estimate 2-8 GB based on expansion scope). Use `-manifest-only` first to see the file list without downloading.

**After fetch:** The `.DepotDownloader/` subdirectory will contain manifest files with the depot IDs as prefixes (e.g., `2699231_<manifestid>.manifest`). Those become the verified depot IDs for Edition-II.

**HALT: Matt authentication required.** This command requires Matt's Steam credentials (the expansion is paid DLC). Legolas does not handle credentials. This item is a `matt_to_do/` action.

---

## Delta report — what to check after Edition-II is fetched

Delta is the deliverable. Legolas will produce the actual diff once Edition-II bytes are available. Items ranked by priority per commission:

### P0 — already-banked records

- `records/skills/playerclass07/purifyingflame1.dbr` (FoI, `gd-flames-of-ignaffar-purifier` in corpus, 22 rows, Edition-I certified). If Crate touched it in the expansion patch, the certificate attests fidelity to a build that no longer ships. SHA-256 of Edition-I GDX1.arz is `e28ab2515477ac80bdc3f955b6aa804eee791d4c51fda64c9ea01306522a4539` — if Edition-II GDX1.arz has a different SHA-256, this record is under risk and must be diffed at field level.

### P0 — controller spatial fields

First-of-kind fields from the 2026-07-23 probe: `ViewDistance`, `InnerViewDistance`, `SightAngerRate`, `InnerSightAngerRate`, `MaxPursuitDistance`, `PursuitTime`, `fleeDistance`, `WanderDistance`, `distressCallRange`. These feed TSF6/VDM work. Expansions are exactly when Crate would adjust monster AI pacing for new content. If any controller record that was probed has changed, the sim's spatial parameter inputs are stale.

### P1 — rank-array structure

Any change to `skillMaxLevel`, `skillUltimateLevel`, or array lengths in any playerclass record. Directly interacts with Q1's findings: the true caps are in the `.arz`; if Crate changed them, the rank-adjudication findings above apply to the new values, not the old ones.

### P1 — new field names in string table

Schema-drift tripwire. New field names in the string table indicate the adapter's field vocabulary is incomplete. The adapter currently handles a specific set of field names; any new name is an extension point that needs schema review.

### P2 — .arz header version field

The Edition-I `database.arz` has `version=3` in the TQIT header (confirmed by the adapter's `gd_arz_adapter_2026_07_24.py` output: `HEADER magic=2 version=3`). If the expansion bumps the format version, the parser needs re-validation. **HALT condition:** if the format version changed, escalate to gandalf before any row from Edition-II is trusted.

### P2 — whether templates/ ships in Edition-II depot

Zero `.tpl` files were present in Edition-I. This is a known gap (freeze fingerprint §5). If the expansion depot includes a `templates/` directory, this opens the template bridge that has been pending since the first probe.

---

## HALT conditions

The following conditions halt Edition-II work pending gandalf / Matt ruling:

- **Steam auth required** (present condition) — Matt must run the fetch.
- **Format version bump** in any `.arz` header — parser re-validation required before any row is trusted.
- **Delta too large** — if record count diff is in the thousands, "diff" stops being the right frame; escalate.
- **FoI (`purifyingflame1.dbr`) changed** — the one banked `exact_skill` row's certificate is invalidated; elrond must decide whether to re-extract, re-certify, or version-pin the old row before any new row lands.

---

## Source list

| Source | Path / URL | Access date |
|---|---|---|
| Steam API appdetails (2699230) | `https://store.steampowered.com/api/appdetails?appids=2699230` | 2026-07-24 |
| Steam API packagedetails (966567) | `https://store.steampowered.com/api/packagedetails?packageids=966567` | 2026-07-24 |
| Edition-I depot manifests | `/Users/admin/Games/vendor/grim-dawn/.DepotDownloader/*.manifest` | 2026-07-24 |
| Edition-I freeze fingerprint | `agentic_orchestration/gandalf/notes/2026-07-24-gd-edition-I-freeze-fingerprint.md` | 2026-07-24 |
| SteamDB search results (secondary) | `steamdb.info/app/2699230/`, `steamdb.info/depot/897671/` | 2026-07-24 (403-blocked for direct access) |
| Steam announcement (secondary) | `store.steampowered.com/news/app/219990/view/687507011804332719` | 2026-07-24 |
