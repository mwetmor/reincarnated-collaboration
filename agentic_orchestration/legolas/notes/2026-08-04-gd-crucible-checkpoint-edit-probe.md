# GD Crucible checkpoint edit probe — 2026-08-04

**SALVAGE RECONSTRUCTION** — dead probe agentId `a83611ca47cdaac4a`, died on stream timeout 2026-08-04 after completing all research. This file reconstructs findings from the probe's tool results and interim conclusions preserved in the task transcript.

**Mode:** A (analytical)
**Commissioner:** (implicit — serves the EoR Warlord playtest sitting)
**Scratch:** `agentic_orchestration/legolas/scratch/2026-08-04-crucible-ckpt/`

---

## VERDICT

**A checkpoint-to-150 edit is viable on GD 1.3.0.5, but the question is moot for the current sitting.** The live client's checkpoint-at-wave-70 means the remaining climb is ~80 waves from that point — a shorter route than any save-edit path entails (each path requires backup, edit, and format-compat verification). Play the climb.

**This file is the durable record for future fixture use.**

For future fixtures on 1.3.0.x: the **console path via GDConsoleUnlocker** is the cleanest route — no file parsing, no format compat risk. The **gd-edit FoA fork** is viable if the console path is unavailable, but requires source build or a community-compiled binary. **Upstream gd-edit is stale for 1.3.** GD Stash's Char Editor does NOT touch the token list that governs wave-50/100/150 checkpoint availability.

Risk class: **LOW** on the console path (reversible tokens, no file parsing), **MEDIUM** on the gd-edit FoA path (format update correct per fork diff, but still a write-back to an encrypted binary save), **HIGH** on manual byte-edit (no tooling, XOR-keyed encryption).

---

## §1 — Where Crucible progress is stored

Source: `gdc.clj` lines 74–77 (Block1), lines 534–587 (Block10), and the live-parse of the EoR fixture `player.gdc.eor` from `2026-08-01-eor-addendum/eor_parsed.json`.

Crucible state is in **`player.gdc`** (the character file), not in `.gst` (shared stash) or any formula/quest files.

**Block1** (general character info, unencrypted header fields) holds:
- `:greatest-survival-difficulty-completed` — byte: 0=Aspirant, 1=Challenger, 2=Gladiator unlocked

**Block5/stats block** holds the achievement-only tracking fields:
- `:survival-greatest-wave` — int32 (highest wave ever completed — COSMETIC ONLY, see §2)
- `:survival-greatest-score` — int32 (high score — cosmetic only, not reflected in-game leaderboard if edited)
- `:survival-defense-built` — int32 (achievement counter)
- `:survival-powerups-activated` — int32 (achievement counter)
- `:tributes` — int32 (current tribute balance, in Block1)

**Block10** holds:
- `:tokens-per-difficulty` — array of 3 token lists (per-difficulty), each a vector of string token names

The checkpoint unlock tokens (from the live EoR fixture, difficulty-2 slot) are:
`SURVIVALMODE_TIER05CHECKPOINT`, `SURVIVALMODE_TIER10CHECKPOINT`, `SURVIVALMODE_TIER15CHECKPOINT`, `SURVIVALMODE_NORMAL`, `SURVIVALMODE_CHALLENGER`, `SURVIVALMODE_GLADIATOR`, plus `SURVIVALMODE_DEFENSEBUILT`, `SURVIVALMODE_POWERUPACTIVE`, `SURVIVALMODE_4POWERUPS`, `GD_STASHED`

The **in-game UI checkpoint availability** (which wave you can start from) is gated on these tokens, confirmed by:
- Forum thread 110974 (desioner, 2021-09-07): editing `:greatest-survival-difficulty-completed` works immediately. Editing `:survival-greatest-wave` does NOT unlock checkpoints in-game.
- Tags extraction from `survivalmode2/Text_EN.arc` → `tags_survival2.dec.txt` line 6: `tagNotification_Checkpoint15=You can now resume the Crucible on Wave 150.` — this notification fires when the TIER15CHECKPOINT token is received.
- `tags_survival.dec.txt` lines 105–106: checkpoint-50 and checkpoint-100 tokens follow the same pattern.

**Key conclusion:** to unlock wave-150 start, the token `SURVIVALMODE_TIER15CHECKPOINT` must be present in the difficulty-2 slot of `:tokens-per-difficulty`. The `:survival-greatest-wave` field is cosmetic and does not gate it.

---

## §2 — Per-path findings

### Path A: GD Stash 1.8.2g Char Editor

**Status: CANNOT do this. Wrong surface.**

GD Stash's Char Editor (version 1.8.2g, confirmed current as of the GD Stash forum thread `gdstash_op.txt`) does NOT expose the `:tokens-per-difficulty` list. The changelog shows:
- v1.06: "Crucible Token Points can be edited" — this is the tribute `:currentTribute` field, not the token list
- v1.07: Char Editor shows achievement stats

The Char Editor UI exposes: level/XP, attributes, faction rep, skills/devotions, shrines, riftgates, and tribute count. The checkpoint token list is not in the Char Editor surface per the screenshot evidence and forum thread cross-reference.

**GD Stash CAN set `:greatest-survival-difficulty-completed`** (the Char Editor shows it per the chareditor.png screenshots in scratch). This unlocks which difficulty you can enter, but does not set the wave-150 checkpoint — you would still start at wave 1.

Source: `gdstash_op.txt` changelog; screenshot `chareditor.png`; forum thread t29036.json.

---

### Path B: gd-edit upstream (odie/gd-edit)

**Status: STALE for 1.3.0.x. DO NOT USE.**

Upstream gd-edit's most recent commit is 2024-07-23 ("Avoid caching Exception when loading shrine and gate data"). It does not handle the 1.3.0 format changes — specifically the four new int32 fields appended to item records at block version 13 (`Item-v13-fields` in the FoA fork diff). Loading a 1.3.0.x save with upstream would either error on format version or produce a corrupted write-back.

gd-edit does have first-class token-append support (`char-add-token!` in `set.clj` lines 121–159) — the path `set tokens-per-difficulty/2 SURVIVALMODE_TIER15CHECKPOINT` is syntactically supported and tested by the community (thread 110974). The problem is exclusively the format mismatch.

Source: `set.clj` (scratch copy); upstream commit log from GitHub API; forum thread t35817.json.

---

### Path C: gd-edit FoA fork (c0de-v1k1ng/gd-edit-FoA)

**Status: VIABLE but requires build-from-source or trust of a community binary.**

The FoA fork (pushed 2026-07-26, "Support Grim Dawn 1.3 / Fangs of Asterkarn character saves") adds the `Item-v13-fields` struct and stash-tab v9+ fields, and correctly updates block 8 (skills block) with the new `8-skill-unk` bool field. The token-append logic (`path-is-tokens?` / `char-add-token!`) is identical to upstream and present in the fork.

The fork's gdc.clj was diff'd against upstream (stored in scratch as `gdc_foa.clj` vs `gdc_kirijin.clj` vs `gdc.clj`): Block1/Block10 token structure is **unchanged from upstream** — only item and stash blocks changed. Token append therefore works correctly on 1.3.0.x saves.

**Procedure (future use):**
1. Back up the save directory before touching anything.
2. Build from https://github.com/c0de-v1k1ng/gd-edit-FoA (`clj -T:build build` per the forum thread).
3. Load the character. Run: `set tokens-per-difficulty/2 SURVIVALMODE_TIER15CHECKPOINT`
4. Run `write`. Verify with `show tokens-per-difficulty`.
5. Also set `:greatest-survival-difficulty-completed` to 2 if not already set.

**Risk:** MEDIUM. The format update appears correct per the diff, but this is an encrypted-XOR write-back to a live save and the fork has no released binary for Windows as of 2026-08-04 (kirijin/gd-edit has a Linux binary v0.2.445; roshansoma posted a Windows exe but it was reported broken 2026-08-03 by Sickoptic).

Source: `gdc_foa.clj` diff; `set.clj` token path; t35817.json posts 2026-07-26.

---

### Path D: Manual byte-edit of player.gdc

**Status: NOT RECOMMENDED. High complexity, high risk.**

The `.gdc` file uses a XOR-based stream cipher with an evolving encryption state. The parser (`gdc.clj` lines 993–1200) shows that each block has its own checksum assertion, and the encryption state is threaded through the entire file. Manually inserting a string token into the token list requires: recalculating all downstream encrypted offsets, all block-length fields, the per-block checksums, and the final file checksum. Any error produces an unloadable character or a client crash.

No community-documented byte-patch procedure for this specific operation was found. The probe searched Crate forums and found no thread with a manual hex-edit walkthrough for the token list.

Source: `gdc.clj` lines 993–1052 (read-block / checksum assertion chain); absence of hits on forum searches in scratch.

---

### Path E: Console (character.GrantPlayerToken)

**Status: VIABLE — cleanest path. Requires GDConsoleUnlocker on Windows.**

The console command `character.GrantPlayerToken "SURVIVALMODE_TIER15CHECKPOINT"` directly writes the token to the active loaded character. The token persists to `player.gdc` on session exit.

**Console access:** The standard console (tilde/backtick key) is active in Custom Game mode only per community documentation (forum thread 32174, 2016: "go to a custom game — it doesn't work in the main campaign"). However, **GDConsoleUnlocker** (forum thread 145961, 2026-07-05) patches the running process to enable the console in Campaign mode. It is a small external injector — "just run the program while Grim Dawn is running; it will end instantly and unlock the console."

Binary inspection of `Grim Dawn.exe` found `character.GrantPlayerToken` in the command table (strings output, lines 90444–90447 of the binary). The command takes a quoted token name.

**Procedure (future use):**
1. Launch GDConsoleUnlocker while GD is running (any session type).
2. Load the target character.
3. Press tilde/backtick (~) to open console.
4. Run: `character.GrantPlayerToken "SURVIVALMODE_TIER15CHECKPOINT"`
5. Run: `character.GrantPlayerToken "SURVIVALMODE_GLADIATOR"` (if difficulty not yet unlocked)
6. Save and exit.

**Risk:** LOW. No file parsing. Reversible with `character.RevokePlayerToken`. The token is legitimate game state — it is exactly what the game would have written after the character cleared wave 150 legitimately.

Source: `2026-07-25-gd-custom-game-console-unlock.md`; binary strings from `Grim Dawn.exe`; forum thread `raw_145961.txt`.

---

## §3 — Context: why the 1.1.9.x save lost checkpoint progress

The EoR fixture was built from a 1.1.9.x-era save (gutsmasher.zip). When loaded into 1.3.0.5, GD performs a forward format migration. The probe's prior EoR addendum (2026-08-01) measured the fixture's token state directly:

- Gladiator unlocked: `greatestSurvivalDifficulty = 2`
- Tributes: `currentTribute = 999`
- Wave record: `survivalWaveTier = 170`
- Checkpoint tokens present in difficulty-2 slot: all three (TIER05, TIER10, TIER15)

So **the EoR fixture's Crucible state DID carry through** — the addendum confirmed Gladiator and all checkpoints were present. The field observation (client offered wave-70 checkpoint after a wave-93 death) is consistent with the in-session retry-checkpoint mechanic (tags_survivalui.txt: "restart at the nearest Checkpoint, which is 20 waves before where you stopped, rounding down to the nearest 10th"), not with the fixture lacking the wave-150 start token.

This means the "progress did not carry" description in the commission brief refers to the in-session retry behavior — not a missing persistent token. The fixture is fine. No edit is needed for this sitting.

---

## §4 — Open unknowns

1. **Console in Campaign without GDConsoleUnlocker** — binary inspection found no hard guard, but community consensus (2016, reaffirmed) says Campaign blocks it. The `/exec` launch flag behavior is also unconfirmed. If Matt tests backtick in Campaign and it works, GDConsoleUnlocker is not needed.

2. **kirijin/gd-edit Windows binary reliability** — roshansoma posted a Windows exe 2026-07-30 but it was reported broken 2026-08-03. No verified Windows binary of either fork as of probe close.

3. **SURVIVALMODE_4POWERUPS and SURVIVALMODE_DEFENSEBUILT tokens** — present in the EoR fixture but not clearly documented as required for checkpoint access. Likely achievement counters. Not needed for the wave-150 start.

---

## Source list

| Source | Location | Notes |
|---|---|---|
| gdc.clj (format spec) | `scratch/2026-08-01-eor-addendum/gdc.clj` | Block1/Block10 structure, lines 54–77, 534–590 |
| EoR fixture parse | `scratch/2026-08-01-eor-addendum/eor_parsed.json` | Live token state, measured |
| Forum thread 110974 | `scratch/2026-08-04-crucible-ckpt/raw_110974.txt` | desioner's gd-edit token experiment, 2021-09-07 |
| GD Stash changelog | `scratch/2026-08-04-crucible-ckpt/gdstash_op.txt` | Version history; "Crucible Token Points" = tributes, v1.06 |
| gd-edit upstream set.clj | `scratch/2026-08-04-crucible-ckpt/set.clj` | Token-append logic lines 121–159 |
| FoA fork diff | `scratch/2026-08-04-crucible-ckpt/gdc_foa.clj` | 1.3.0 format changes vs upstream |
| Fork release state | t35817.json posts 2026-07-26 | c0de-v1k1ng/gd-edit-FoA pushed 2026-07-26 |
| Console command list | Binary strings from `vendor/grim-dawn/Grim Dawn.exe` | character.GrantPlayerToken confirmed |
| GDConsoleUnlocker | `raw_145961.txt` (forum thread 145961, 2026-07-05) | Injector enabling console in Campaign |
| Checkpoint tags | `scratch/2026-08-04-crucible-ckpt/tags_survival*.dec.txt` | tagNotification_Checkpoint15 = TIER15CHECKPOINT |
| 1.2.1.3 patch notes | `scratch/2026-08-01-eor-addendum/raw_142410.txt` | Checkpoints free for all chars since v1.2.1.3 |
| Console unlock research | `research/knowledge/gd/2026-07-25-gd-custom-game-console-unlock.md` | Prior console probe |
