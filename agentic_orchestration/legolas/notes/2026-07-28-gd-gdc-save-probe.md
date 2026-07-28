# G-7 — Grim Dawn `.gdc` character-save probe — 2026-07-28

**Mode:** A (analytical / primary-source lane establishment)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Conductor:** gandalf · **Authority:** R-KC1-4, `agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` (Matt-ratified)
**Lane:** KIT-CAL-1 parallel, non-gating
**Access mode:** read-only throughout. Nothing was written, copied, or modified outside this repo.

---

## Headline

**NOT FOUND.** There is no Grim Dawn save data — no `.gdc`, no `.gdd`, no `.map`, no GD directory
of any kind — anywhere on this Mac or on the one mounted external volume. Grim Dawn is **not
installed** on this machine and never has been. Parse work is **STOPPED at STEP 1** per commission.

The play test `GP-gd-2026-07-26-s1` ran on **Matt's Windows PC**. Its saves are unreachable from
any agent session on this host.

**Action filed:** `canonical/matt_to_do/2026-07-28-gd-gdc-save-copy.md` (queue row **T11**).

**Consolation prize, and it is not small:** the STEP-2 parse lane is now **fully mapped** against
the authoritative community format reference (§ 3). Every field G-7 asked for has been located to a
named struct member. When the save lands, the parse is a mechanical exercise against a known map,
not an investigation. § 4 records the one real risk (struct-version drift past the reference build)
and the fallback.

---

## 1 — Locations searched (all negative)

| # | Path / method | Result |
|---|---|---|
| 1 | `~/Documents/` | Exists; contains only `League of Legends`, `OpenTTD`. **No `My Games`** — the parent of GD's default save root does not exist. |
| 2 | `~/Library/Application Support/Steam/userdata/116655798/` | 8 app-id dirs present (`241100`, `371970`, `427520`, `493340`, `570`, `7`, `892970`, `config`…). **No `219990`.** No GD Steam-cloud mirror. |
| 3 | `~/Library/Application Support/Steam/steamapps/common/` | `Factorio`, `Stranded Deep`, `Valheim`, controller configs. **No Grim Dawn.** |
| 4 | `~/Library/Application Support/Steam/steamapps/*.acf` + `libraryfolders.vdf` | 4 manifests (`313120`, `427520`, `493340`, `892970`). **No `appmanifest_219990.acf`.** Single library folder; no secondary Steam library exists to search. |
| 5 | Windows-compatibility layers: CrossOver, Whisky (both App-Support and Containers), Parallels (`~/Parallels`, `~/Library/Parallels`), Porting Kit, bare `~/.wine` | **None of these exist on this machine.** No Wine prefix of any kind. (Consistent with the 2026-07-23 viability note, which treated Wine as a *hypothetical* install for `ArchiveTool.exe` — it was never actually installed; the `.arz` lane was built in Python precisely because Wine was absent.) |
| 6 | `find ~ -maxdepth 6 -iname '*Grim*Dawn*'` | Zero hits. |
| 7 | `mdfind -name 'player.gdc'` and `mdfind "kMDItemFSName == '*.gdc'"` (Spotlight index) | Zero hits. |
| 8 | `find / -xdev` with `/System`, `/private`, `/usr`, `/Library/Caches`, `*/node_modules`, `/Applications` pruned, `-iname '*.gdc'` | Zero hits. Covers the whole boot volume. |
| 9 | `/Volumes/reincarnated` (the PC↔Mac share, searched separately since `-xdev` excludes it): `-iname '*.gdc' -o -iname '*.gdd' -o -iname 'player.gd*'` | Zero hits. Volume holds `agent-prompts/`, `engine-output/`, `matt-notes-from-pc/`, `meshy-handoff/`, `synty-assets/`, `visual-artifacts/`. `matt-notes-from-pc/` contains **only** three `.md` console-probe notes. |
| 10 | `/Volumes/` enumeration | Exactly two: `Macintosh HD`, `reincarnated`. No unmounted-but-visible candidate. |

**mtime evidence: N/A** — no file was found, so the "was it played after 2026-07-26" drift check
**could not be run**. That check moves to the follow-up pass and is carried into T11 as a required
field (§ 5, drift protocol).

### 1.1 — Corroborating evidence that GD is PC-only for this project

Not inference — three independent records already say so, and this probe is consistent with all of them:

- `canonical/matt_to_do/2026-07-24-gd-edition-II-steam-fetch.md` fetches the depot with
  **`-os windows`** into a vendor directory. We acquired GD's *data files* on the Mac; we never
  acquired GD.
- `/Volumes/reincarnated/matt-notes-from-pc/` — the share is literally named for the direction of
  travel. All three console-probe notes (`GD-console-notes{,-v2,-v3}.md`) are Matt's handwritten
  transcriptions *from* the PC.
- `matt_to_do` **T9** and **T10** both describe GD sittings as "Matt PC sitting" / "the GD PC"
  (T10 installs OBS *on the GD PC*).

**Grade: CERTAIN.** The save is not here, and there is no configuration under which it would be.

---

## 2 — What the save would answer (and how good the answer would be)

Recorded now so the value of T11 is legible before it is executed. Each row names the exact struct
member from § 3.

| G-7 target | `.gdc` carrier | Grade once parsed |
|---|---|---|
| Character level | `header.level`, `character_bio.level`, `play_stats.maxLevel` | **MEASURED**, triple-redundant |
| Attribute allocation | `character_bio.physique / .cunning / .spirit` (floats) + `.attributePointsUnspent` | **MEASURED** |
| Skill points per skill | `character_skills.skills[]` → `.name` (DBR record path) × `.level` | **MEASURED**, per-skill |
| **Onslaught rank** | the `skills[]` entry whose `.name` is the Onslaught DBR path × its `.level`; `.enabled` also present | **MEASURED** |
| Werewolf-transform line | same vector; the Fangs-of-Asterkarn transform skill + its modifiers appear as their own `skills[]` entries | **MEASURED** |
| **Devotion = zero** | `character_bio.devotionPointsUnspent`, `.totalDevotionUnlocked`; `character_skills.devotionReclamationPointsUsed`; per-entry `skill.devotionLevel` | **MEASURED** — see § 2.1, this is a *stronger* test than the commission assumed |
| Equipped gear at run end | `inventory.equipment[12]` + `weapon1[2]` + `weapon2[2]`, each an `item` | **MEASURED for END-state** — see § 2.2, an important caveat |
| Poison-DoT item identity | that item's `baseName / prefixName / suffixName / componentName / augmentName` (all DBR record paths, joinable to the banked `.arz`) | **MEASURED if still equipped at save**; else NOT RECOVERABLE |

### 2.1 — The devotion-zero test is better than expected

The verdict's current claim is negative-observational: *no devotion proc fired in 313 stills*
(`2026-07-26-gd-playtest-v1-efficacy-verdict.md` § 9), upgraded 2026-07-28 to ATTESTED on Matt's
"I definitely did not utilize any devotion points."

The `.gdc` supports a **positive, conjunctive** test:

```
devotionPointsUnspent == totalDevotionUnlocked      → nothing assigned
AND devotionReclamationPointsUsed == 0              → nothing assigned-then-refunded
AND ∀ s ∈ skills[] : s.devotionLevel == 0           → no constellation node holds a rank
```

All three together close the refund loophole that neither the proc-absence observation nor the
attestation can close. Devotion **assigned** and devotion **fired** are different propositions, and
the save is the only artifact that speaks to the first one directly.

Corollary already visible: `play_stats.healthPotionsUsed` / `.manaPotionsUsed` do the same job for
the **potions 0/0 control**, which is currently also observational. One parse upgrades two controls.

### 2.2 — Gear: the save is an ENDPOINT, not a series (load-bearing caveat)

`.gdc` stores the character as of last save. It has **no history**. Therefore:

- If the poison-DoT item found at `play_time ≈ 6052` was **still worn at run end**, we get its full
  identity — `baseName` joins straight to the banked Edition-II `.arz`, and `componentName` /
  `augmentName` are where a low-level poison DoT most plausibly lives (a component on a weapon is
  far likelier at L12 than an affixed base item — *hypothesis, not finding*).
- If it was swapped out before the save, it is **gone**. No amount of parsing recovers it.
- Anything equipped *after* 2026-07-26 overwrites the run-end state silently. This is the drift
  hazard, and it makes T11's "don't play that character" instruction load-bearing rather than
  courteous.

This is the same **SAVE-cumulative vs session-scoped** distinction the artifact-verification note
established (`2026-07-26-gd-playtest-v1-artifact-verification.md` § "Banked prefix"). The gear read
is SAVE-cumulative in exactly that sense: it is an endpoint carrying an unknown amount of
post-run mutation.

---

## 3 — STEP-2 lane, fully mapped (deliverable in its own right)

Reference implementation obtained and read: **`AaronHutchinson/Grim-Dawn-Save-Decryption`**
(`decrypt-player.cpp` 1,644 lines, `decrypt-player.h` 404 lines, `decrypt-helper.h`), itself an
updated fork of the original by "Christopher" at `lost.org.uk/grimdawn.html` — the root community
source every downstream GD save tool descends from. **Primary source** for format purposes: it is
executable code that round-trips real saves, not prose.

### 3.1 — Cipher (confirmed from source, supersedes my prior sketch)

```
k = read_u32_le(file)          # first 4 bytes, NOT xor-masked on read
k ^= 0x55555555                # → initial running key
for i in 0..255:               # 256-entry key table
    k = (k >> 1) | (k << 31)   # rotate right 1, 32-bit
    k = (k * 39916801) & 0xFFFFFFFF
    table[i] = k
```

Two distinct read primitives — **conflating them is the classic way this parse fails**:

- `read_int()` / `read_short()` / `read_byte()`: `ret = raw ^ key`, **then** advance the key:
  `for each byte b of raw: key ^= table[b]`. Note the key advances on the **ciphertext** bytes.
- `next_int()`: `ret = raw ^ key`, key **NOT** advanced. Used only for block lengths and the
  end-of-block sentinel.
- `read_float()` = bit-reinterpret of `read_int()`.
- Strings: length-prefixed; `wstring` (the character name) is UTF-16.

### 3.2 — File skeleton

```
read_key()
read_int()  == 0x58434447   # "GDCX" LE — the magic
read_int()  == 2
header.read()               # wstring name · string tag · u32 level · u8 sex · u8 hardcore
read_byte() == 3
next_int()  == 0
read_int()  == 8            # FILE VERSION  ← see § 4
```

then, **in this fixed order**, sixteen top-level structures. `read_block_start()` returns the block
ID and reads the length via `next_int()`; `read_block_end()` asserts the cursor landed exactly on
`start + len` and that the sentinel `next_int()` is `0`. That end-of-block assertion is a free,
strong integrity check — **keep it on**; a silent mis-parse is the failure mode that matters.

| Order | Struct | Block ID | Inner version | Carries (for us) |
|---|---|---|---|---|
| 1 | `uid` | — | — | save identity (16 bytes) — **use as the `save_identity` join key the artifact-verification note § 505 flagged as missing** |
| 2 | `character_info` | **1** | 5 | difficulty, money, `hasBeenInGame` |
| 3 | **`character_bio`** | **2** | 8 | **level, exp, unspent attr/skill/devotion, totalDevotionUnlocked, physique, cunning, spirit, health, energy** |
| 4 | **`inventory`** | **3** | 4 | **`equipment[12]`, `weapon1[2]`, `weapon2[2]`**, bags/sacks |
| 5 | `character_stash` | 4 | 6 | — |
| 6 | `respawn_list` | 5 | 1 | — |
| 7 | `teleport_list` | 6 | 1 | — |
| 8 | `marker_list` | 7 | 1 | — |
| 9 | `shrine_list` | **17** | 2 | (out-of-sequence ID — real, not a typo) |
| 10 | **`character_skills`** | **8** | 5 | **`skills[]`, `itemSkills[]`, masteriesAllowed, skill/devotion reclamation counts** |
| 11 | `lore_notes` | 12 | 1 | — |
| 12 | `faction_pack` | 13 | 5 | — |
| 13 | `ui_settings` | 14 | — | hot-slot bindings (which skills were on the bar) |
| 14 | `tutorial_pages` | 15 | — | — |
| 15 | **`play_stats`** | **16** | — | **playTime, deaths, kills, hitsInflicted, criticalHitsInflicted, greatestDamageInflicted, health/manaPotionsUsed, maxLevel** |
| 16 | `trigger_tokens` | 10 | — | quest tokens |

### 3.3 — Field maps for the three blocks G-7 needs

```cpp
class character_bio {                 // block 2
  uint32_t level, experience;
  uint32_t attributePointsUnspent, skillPointsUnspent;
  uint32_t devotionPointsUnspent, totalDevotionUnlocked;
  float    physique, cunning, spirit, health, energy;
};

class skill {                         // element of character_skills.skills[]
  string   name;                      // DBR record path → joins to the banked .arz
  string   autoCastSkill, autoCastController;
  uint32_t level;                     // ← THE RANK
  uint32_t devotionLevel;             // ← 0 for every entry ⟺ no devotion assigned
  uint32_t experience, active;
  uint8_t  enabled, unknown1, unknown2;
};
class character_skills {              // block 8
  vector<skill> skills;
  vector<item_skill> itemSkills;      // name · itemName · itemSlot — granted-by-gear skills
  uint32_t masteriesAllowed, skillReclamationPointsUsed, devotionReclamationPointsUsed;
};

class item {                          // base of inventory_equipment
  string   baseName, prefixName, suffixName, modifierName,
           transmuteName, componentName, relicBonus, augmentName;
  uint32_t stackCount, seed, componentSeed, unknown, augmentSeed, var1;
};
```

Every `*Name` on `item` is a DBR record path, so **gear identity resolves against the Edition-II
`.arz` corpus we already hold** (`~/Games/vendor/grim-dawn-edition-II-20260724/`) with no additional
acquisition. The poison-DoT question becomes a join, not a lookup.

### 3.4 — A hypothesis worth one cheap test at parse time

`play_stats` carries aggregate counters but **no per-skill use counts** — no `onslaught`, no
`claws`, no `charge`, no `life_healed`. Yet the in-game `game.PlayStats` overlay displays exactly
those, and the whole T-A/T-B OCR series is built on them. They are stored somewhere.

The only candidate in the mapped format is `play_stats.v` — `vector<unknown_data>`, where
`unknown_data = { string str; uint32_t num; }`, annotated in the reference as **"Usage unknown"**.

A `(string, uint32)` vector is precisely the shape of a **per-skill counter table**.

**If that holds**, the `.gdc` carries the OCR series' endpoint *natively and exactly* — turning the
banked `54 onslaught / 358 claws / 175 charge / 12468.06 healed` from an OCR reading into a
byte-exact cross-check of galadriel's whole pipeline. **If it doesn't**, we have cost ourselves one
`print` statement. Dump `v` unconditionally on the first parse.

Flagged explicitly as **HYPOTHESIS, UNTESTED** — shape-based inference from a field the reference
authors themselves could not name. It does not enter any evidence layer until a save is parsed.

---

## 4 — The one real risk: struct-version drift

The reference is pinned to **GD 1.1.9.1** (AoM + FG + Crucible). Matt's PC runs the **Edition-II /
Fangs-of-Asterkarn** build. Every version assert in § 3.2 is a hard `throw`. Expansions that add
character state (Fangs adds a mastery, and FoA-era patches touched inventory) routinely bump these.

**Expect the strict parse to throw on first contact.** That is not a HALT, it is the expected
opening move. Mitigations, in order:

1. **Log, don't throw.** Replace each version assert with a recorded observed-vs-expected pair. The
   block-length + end-sentinel machinery already tells us independently whether a block parsed
   cleanly, so we can tolerate an unknown version and still detect a genuine mis-parse.
2. **Partial parse is explicitly acceptable** (commission grants this). Blocks 2 and 8 —
   `character_bio` and `character_skills` — carry level, attributes, every skill rank, and the whole
   devotion answer, and they sit **early** in the file (positions 3 and 10). Even if `inventory`
   (position 4) drifted and cost us the gear read, bio + skills still land. Sequence the parse to
   bank each block as it completes rather than at the end.
3. **Version-current fallback:** **GD Stash** (Java, Nexus mods/2) has shipped Fangs-of-Asterkarn
   format support; `Odie/gd-edit` (Clojure) is the other actively maintained reader. Either can be
   consulted as a *format reference* to repair drifted offsets. No credentials, no game install
   needed to read their source. **Read-only use as documentation — we do not run an editor against
   Matt's save.**
4. **The scratch-copy rule stands regardless.** Parse a copy; never open the original, not even
   read-only, with a tool that has a write path.

---

## 5 — Drift protocol for the follow-up pass

When the save arrives, **before** parsing, record and report:

- `mtime` of `player.gdc`. **If `mtime > 2026-07-26`, the state has drifted past the recorded run**
  and every field in § 2 downgrades from MEASURED-at-run-end to MEASURED-at-save-time. Say so in
  the header of the follow-up note; do not let it be inferred.
- `play_stats.playTime` vs the run's terminal `play_time ≈ 7094`. This is the **precise** drift
  measure and it is better than `mtime`: `playTime` is in-game seconds and directly comparable to
  the banked series. `playTime ≈ 7094` ⟹ no drift. `playTime ≫ 7094` ⟹ quantified drift, in the
  same units the run is recorded in.
- `uid` (block 1) — bank it as the `save_identity` component of the `(save_identity, play_time_ms)`
  key that artifact-verification § 505 identified as missing from the §2.1 protocol. This probe can
  **supply** that field, closing a named protocol gap as a side effect.

---

## 6 — Gaps not resolved

1. **The character's name is not recorded anywhere in the repo.** Grepped the efficacy verdict, the
   artifact-verification note, the wind-down handoff, and the run charter — the character is
   described ("Soldier → Fangs-of-Asterkarn werewolf transform, L12") but never named. This is why
   T11 asks Matt to copy the *whole* `_<CharacterName>` directory rather than a path we specify
   exactly, and why he must tell us the name. Minor, but it is why the instruction is shaped the way
   it is.
2. **Cloud-vs-local save location on the PC is unknown to us.** GD writes to
   `Documents\My Games\Grim Dawn\save\` with cloud off, and to Steam `userdata\...\219990\remote\`
   with cloud on. T11 names both; Matt checks both.
3. **Whether the save survived at all.** L12 characters get deleted. If the character is gone, G-7
   is permanently unanswerable and devotion-zero stays ATTESTED. Named in T11 as an acceptable
   answer so the row can be struck cleanly rather than lingering.
4. **`play_stats.v` contents** — see § 3.4. Untestable without a file.
5. **Actual Edition-II struct versions** — untestable without a file. § 4 is preparation, not
   measurement.

---

## 7 — Sources

| # | Source | Class | Accessed |
|---|---|---|---|
| S1 | `github.com/AaronHutchinson/Grim-Dawn-Save-Decryption` — `decrypt-player.cpp`, `decrypt-player.h`, `decrypt-helper.h` | **Primary** (working implementation) | 2026-07-28 |
| S2 | `lost.org.uk/grimdawn.html` — "Christopher", origin of S1 | Primary (upstream), thin on prose | 2026-07-28 |
| S3 | `github.com/Odie/gd-edit` + `odie.github.io/gd-edit-docs/` | Secondary (maintained alt reader) | 2026-07-28 |
| S4 | GD Stash, `nexusmods.com/grimdawn/mods/2` — FoA format support | Secondary (version-current fallback) | 2026-07-28 |
| S5 | `github.com/ChrisElison/GDParser`, `github.com/dandels/gdlc` | Tertiary (surveyed, not read) | 2026-07-28 |
| L1 | `canonical/matt_to_do/2026-07-24-gd-edition-II-steam-fetch.md` | Internal | — |
| L2 | `agentic_orchestration/gandalf/notes/2026-07-26-gd-playtest-v1-efficacy-verdict.md` | Internal | — |
| L3 | `agentic_orchestration/gandalf/notes/2026-07-26-gd-playtest-v1-artifact-verification.md` | Internal | — |
| L4 | `agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` (R-KC1-4) | Internal | — |
| L5 | `agentic_orchestration/legolas/notes/2026-07-23-gd-mac-extraction-viability.md` | Internal | — |

Scratch copies of S1's three files are at `/tmp/gd-decrypt-player.{cpp,h}` and
`/tmp/gd-decrypt-helper.h` — **/tmp, deliberately.** Not banked in-repo: third-party source, and
§ 4 says we may end up targeting a different reference anyway. Re-fetch is one `curl`.

---

**Signed:** legolas, 2026-07-28. The trail ends at the water's edge — the save is on the other bank.
I have mapped the far shore so the crossing is short when the boat comes.
