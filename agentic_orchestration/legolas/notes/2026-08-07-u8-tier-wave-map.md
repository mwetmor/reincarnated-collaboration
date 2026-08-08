# U-8 — Crucible tier→wave map, ladder ceiling, token gating, checkpoint semantics — 2026-08-07

**Probe:** U-8 (Phase A, KC2-SIM autonomous run) · **Conductor:** gandalf · **Agent:** legolas (UNKNOWN-RESEARCHER)
**Mode:** A (analytical / primary-source measurement)
**Access mode:** read-only throughout. No file outside this repo was written; every vendor archive was
opened read-only. **Nothing committed** (per commission).
**Scratch:** `agentic_orchestration/legolas/scratch/2026-08-07-u8-tierwave/`

---

## VERDICT BLOCK

**CLOSED on all four questions.** Three of the four are settled from **the game's own Lua source**, not
from inference — the Crucible's wave sequencer, reward dispenser and Lokarr dialogue trees were
extracted from `Scripts.arc` / `Conversations.arc` and read directly. **This is a first-of-kind lane
for this project: the `.arz` corpus does not contain the wave logic, and no prior probe had opened the
survival script or conversation archives.**

**Headline corrections to the working model, both load-bearing:**

1. **The ladder is 200 waves, not 170.** Twenty tiers × ten waves. `170` was the ceiling under
   Ashes-of-Malmouth/Forgotten-Gods (v1.0.x–v1.2.1.5) and is **stale for the 1.3.x fixture client**.
   Fangs of Asterkarn added tiers 18–20 (waves 171–200). Proven by a clean three-cut differential:
   two independent pre-FoA corpora carry tiers 1–17 and *only* 1–17; the FoA corpus carries 1–20.
2. **"Start on Wave 150" starts you on wave *151*.** The label names the checkpoint you are credited
   with having *cleared*; the first wave actually fought is **label + 1**. Same for the death-rewind
   ("Restart on Wave 130" → first fought is 131). The sim's start-wave parameter must be `label + 1`.

**On "cashing out at 170":** the community framing is **half right and mis-attributed**. Cash-out is not
a wave-170 mechanism — it is offered at **every** 10-wave boundary, from wave 10 onward, and always has
been. What *was* special about 170 is that under AoM/FG it was the **terminal** wave: the event ended by
itself there. Post-FoA nothing terminates at 170; the run continues to 200. Both halves are DB-CITED.

**Bonus closures (not commissioned, delivered because the source was open in front of me):**
the Crucible tribute award formulas, the defense purchase price, and the full 200-row per-wave monster
scaling table for all three difficulties — which together **close U2 of the 2026-08-05 save-parse note**
(§ 7 below), an item that note recorded as UNRESOLVED because "Crucible prices live in `Grim Dawn.exe`,
not in the database." They do not. They live in `Conversations.arc` and `Scripts.arc`.

---

## 0 — Sources, and the lane that had to be built

### 0.1 Why the `.arz` alone could not answer this

The commission pointed at the `.arz` corpus. The `.arz` carries the **content** of each wave (which
monster proxies spawn where) but **none of the sequencing**: every wave-control record resolves to an
engine script hook, e.g.

```
records/scriptentities/tier18spawnpoint01.dbr
    onAddToWorld = gd.survival.tier18Waves.spawnPoint01OnAddToWorld
```

An exhaustive field-value scan of all four `SurvivalMode*.arz` archives (6,393 records, every field)
for `checkpoint|survivalmode_|tier\d|wave|tribute|merit` returned **no** wave-ordering, checkpoint or
cost data — only these script-hook strings (`scratch/p1_fieldscan.py`, `p1_hits.json`).

**The lane I opened instead:** the full Grim Dawn install at `~/Games/vendor/grim-dawn/` ships
`resources/Scripts.arc` and `resources/Conversations.arc` inside each survival mod folder. These are
ARC v3 containers — the same container the display-name bridge already reads — and they hold **plain-text
Lua source with the original developer comments intact**, plus Lokarr's dialogue trees. Twenty-four Lua
files and sixteen `.cnv` files extracted clean. This is the authoritative layer.

### 0.2 Corpus

| # | Source | Class | Used for |
|---|---|---|---|
| S1 | `~/Games/vendor/grim-dawn-edition-II-20260724/` — `database.arz`, `GDX1/2/3.arz`, `SurvivalMode{,1,2,3}.arz`, 8× `Text_EN.arc` | **Primary (game data), FoA / v1.3.0.0** | tier inventory, wave content, scaling tables, tags |
| S2 | `~/Games/vendor/grim-dawn/` (depot 2026-07-23, **pre-FoA**: no `gdx3`, no `survivalmode3`) — incl. `Scripts.arc`, `Conversations.arc` | **Primary (game source)** | the wave sequencer, rewards, Lokarr dialogue |
| S3 | `~/Games/vendor/grim-dawn-edition-I-20260723/` (**pre-FoA**) | Primary (game data) | second independent pre-FoA control |
| S4 | Banked patch notes `scratch/2026-08-01-eor-addendum/raw_{132117,142410,155979,157189}.txt` | **Primary (developer)** | v1.2.0.0 / v1.2.1.3 / v1.3.0.0 / v1.3.0.4 Crucible sections |
| S5 | `grimdawn.com/guide/{about/fangs-of-asterkarn,game-settings/crucible}` (fetched 2026-08-07) | **Primary (developer)** | "+30 waves"; cash-out framing; difficulty unlock |
| S6 | Steam store, Crucible Mode DLC app 483840 (fetched 2026-08-07) | Primary (publisher) | 150 base / +20 AoM → 170 |
| L1 | `legolas/notes/2026-08-05-eorwarlguts-save-parse.md` | Internal | token inventory, TIER18 anchor, U2/U3 |
| L2 | `legolas/notes/2026-08-01-gd-pack-density-ranking.md`, `2026-08-04-gd-1305-patch-delta-probe.md` | Internal | extraction lineage; the "200th wave" patch line |

Tooling written for this pass (all read-only, all in scratch): `lib.py` (merged 8-archive stack,
84,663 records), `p1_fieldscan.py`, `p2_cnv.py` (`.cnv` string+operand scanner — new), `p3_tier1820.py`,
`p4_scaling.py`. Extracted source banked under `scratch/lua/` and `scratch/cnv/`.

**Read-only discipline:** every vendor path was opened for read only; the single write outside scratch
is this note.

---

## 1 — TARGET 1: the full tier→wave map — **CLOSED, DB-CITED, exact**

### 1.1 The map

Twenty tiers of ten waves. **Tier *n* covers waves 10(*n*−1)+1 … 10*n*.**

| tier | waves | ships in | checkpoint at tier end | token |
|---:|---|---|---|---|
| 01 | 1–10 | base Crucible | — | — |
| 02 | 11–20 | base | — | — |
| 03 | 21–30 | base | — | — |
| 04 | 31–40 | base | — | — |
| **05** | **41–50** | base | **wave 50** | `SURVIVALMODE_TIER05CHECKPOINT` |
| 06 | 51–60 | base | — | — |
| 07 | 61–70 | base | — | — |
| 08 | 71–80 | base | — | — |
| 09 | 81–90 | base | — | — |
| **10** | **91–100** | base | **wave 100** | `SURVIVALMODE_TIER10CHECKPOINT` |
| 11 | 101–110 | base | — | — |
| 12 | 111–120 | base | — | — |
| 13 | 121–130 | base | — | — |
| 14 | 131–140 | base | — | — |
| **15** | **141–150** | base *(terminal until AoM)* | **wave 150** | `SURVIVALMODE_TIER15CHECKPOINT` |
| 16 | 151–160 | **AoM** (`SurvivalMode1`) | — | — |
| 17 | 161–170 | **AoM** *(terminal until FoA)* | — | — |
| **18** | **171–180** | **FoA** (`SurvivalMode3`) | **wave 180** | `SURVIVALMODE_TIER18CHECKPOINT` |
| 19 | 181–190 | **FoA** | — | — |
| **20** | **191–200** | **FoA** — **terminal** | — | — |

**All four measured anchors confirmed, and the map extended by two tiers past the highest anchor.**

### 1.2 Four independent proofs of the mapping

1. **Developer source comments**, one per tier file, verbatim — the strongest possible citation:
   `tier01waves.lua` → `-- Waves 1 through 10 for Survival Mode`; `tier05` → `41 through 50`;
   `tier10` → `91 through 100`; `tier15` → `141 through 150`; `tier16` → `151 through 160`;
   `tier17` → `161 through 170`. **17 of 17 present pre-FoA files read; all conform.**
2. **The dispatcher arithmetic** (`eventcontrol.lua`): `rewardTier = math.floor(wave / 10)`, then
   `rewardTier == 0 → tier01Waves`, `== 14 → tier15Waves`, `== 15 → tier16Waves`, `== 16 → tier17Waves`.
   Substituting: wave 1 → tier01 ✓, wave 51 → tier06 ✓, wave 151 → tier16 ✓.
3. **The `.arz` inventory**: `records/proxies/tier{NN}waves/proxy_w{01..10}_p{01..06}[a-z]` — exactly
   ten wave indices per tier, twenty tier directories, **925 spawn-point proxies, 0 unresolved pool
   references**.
4. **The checkpoint tags** land on tier ends with no exceptions: `tagNotification_Checkpoint05/10/15/18`
   = *"You can now resume the Crucible on Wave 50 / 100 / 150 / 180."*

### 1.3 Per-tier structure (for the sim's wave engine)

Spawn points per wave rise with tier; tiers 17–20 use only 5–6 of the six points on every wave.
Resolved against the pools (`scratch/p3_tier1820.py`):

| tier | waves | spawn-pt proxies | distinct pools | unresolved | distinct monsters | mutators active |
|---:|---|---:|---:|---:|---:|---:|
| 13 | 121–130 | 50 | 100 | 0 | 207 | 5 |
| 14 | 131–140 | 50 | 95 | 0 | 191 | 5 |
| 15 | 141–150 | 55 | 130 | 0 | 273 | 6 |
| 16 | 151–160 | 54 | 109 | 0 | 164 | 6 |
| 17 | 161–170 | 52 | 110 | 0 | 196 | **7** |
| 18 | 171–180 | 55 | 98 | 0 | 156 | 7 |
| 19 | 181–190 | 56 | 94 | 0 | 153 | 7 |
| 20 | 191–200 | 55 | 86 | 0 | 139 | 7 |

**Mutator ladder — DB-CITED** (`survivalevent.lua` `SurvivalEvent_SelectMutators`), by
`rewardTier = floor(wave/10)`: `≥17 → 7` · `≥15 → 6` · `≥13 → 5` · `≥11 → 4` · `≥9 → 3` · `≥6 → 2` ·
`≥3 → 1` · else 0. This reconciles with the v1.2.0.0 patch line *"Waves 150-170 now have 6 mutators…"*
at the band level; the code is finer-grained (150–169 → 6, 170+ → 7).

---

## 2 — TARGET 2: the ladder ceiling on Gladiator — **CLOSED. Wave 200.**

### 2.1 The three-cut differential (the decisive test)

Tier directories present in each corpus cut, counted mechanically across the whole survival stack:

| corpus cut | tiers present | max tier | ⇒ ceiling |
|---|---|---:|---:|
| `~/Games/vendor/grim-dawn/` (depot 2026-07-23, pre-FoA) | 1 … **17** | 17 | **wave 170** |
| `grim-dawn-edition-I-20260723/` (pre-FoA) | 1 … **17** | 17 | **wave 170** |
| `grim-dawn-edition-II-20260724/` (**FoA v1.3.0.0**) | 1 … **20** | 20 | **wave 200** |

Two independent pre-FoA cuts agree; the FoA cut adds exactly three tiers. **Tiers 18/19/20 are
`SurvivalMode3.arz`-exclusive** — 55 / 56 / 55 spawn-point proxies, 100% exclusive, 0 unresolved
references — and they draw predominantly on **`poolsbossgdx3` / `poolsbasicgdx3` / `poolsherogdx3`**,
i.e. Fangs-of-Asterkarn creature content (46 / 45 / 49 gdx3 pool references, versus 20–21 for tiers
16–17). 90 of tier-18's monsters and 67 of tier-20's do not appear in tier 17. **This is authored new
content, not placeholder and not copy-paste.**

### 2.2 Corroboration, four independent sources, all agreeing on 150 → 170 → 200

| source | class | statement |
|---|---|---|
| Steam, Crucible Mode DLC (app 483840) | publisher | *"Conquer 150 Unique Waves"* · *"Owners of the Ashes of Malmouth expansion can contend with an additional 20 challenging waves, **bringing the total to 170!**"* |
| `grimdawn.com/guide/about/fangs-of-asterkarn/` | **developer** | *"Crucible Expanded – delve deeper into the Crucible's challenges with **thirty additional waves** (requires the Crucible DLC)."* |
| v1.2.0.0 notes (banked `raw_132117.txt`) | **developer** | *"**Waves 150-170** now have 6 mutators…"* — top band was 170 in Dec 2023 |
| v1.3.0.4 notes (banked `raw_157189.txt` line 42) | **developer** | *"Grava'Thull is no longer a guaranteed spawn in the **200th wave** of the Crucible."* |

170 + 30 = 200. The `.arz` says 20 tiers × 10. **Agreement is total.**

### 2.3 Where the game itself ends the run — and what 170 actually was

Each tier is one `SurvivalEvent`; it runs its ten waves and then **pauses**, posting
`tagNotification_Continue` (*"Speak to the Master of the Crucible to Continue"*). Terminality is a
single call, `gd.survival.eventControl.eventFinished()`, placed in exactly one tier's end callback.
Its location moves as content ships — this is the cleanest possible ceiling evidence:

| build | tier15 end callback | tier16 | tier17 | terminal wave |
|---|---|---|---|---|
| base Crucible (`SurvivalMode.arz` scripts) | `completeProgressToken` **+ `eventFinished()`** | *(absent)* | *(absent)* | **150** |
| AoM (`SurvivalMode1` scripts) | `completeProgressToken` only | `completeProgressToken` + `tier10ProgressToken` | **`eventFinished()`** | **170** |
| FoA (`SurvivalMode3`) | — | — | — | **200** — see gap G1 |

**So the "cash out at 170" folklore decomposes into two separate true things:**

- **Cash-out is universal, not a 170 mechanism.** `npc_event_02.cnv` (mid-event Lokarr) offers
  *"I wish to collect my reward!"* → quest event `endEvent` → `gd.survival.eventControl.eventFinishedCashOut()`
  → `dispenseReward()`. It is available at **every** tier boundary. The developer guide states it in
  exactly those terms: *"Every 10 waves of enemies, you have to make a difficult choice: continue on
  for the next 10 encounters for a chance of greater reward, or **cash out** what you've earned and not
  risk your own demise."*
- **170 was terminal under AoM/FG, so "stopping at 170" was not a choice, it was the end.** In that era
  it was also the top reward row reachable. The framing hardened, then the game moved and the framing
  did not.

**Ruling for the sim: on a v1.3.x client there is no terminal reward point at 170. Play continues to
200.** Waves 161–180 contain ordinary tier-17 and tier-18 content with no reward event between them:
reward tier is `floor(wave/10)`, so 170 → row 17, 180 → row 18, and the reward tables have always had
rows through 20 (§ 2.4).

### 2.4 What waves 161–200 reward — DB-CITED

`rewards.lua` holds five loot tables indexed by `rewardTier`, **each with rows [0…20] in every build,
including the base Crucible** (chest grades A→N, five chest positions):

| rewardTier | waves | `rewardTable` row (5 chest slots) |
|---:|---|---|
| 16 | 160–169 | l, m, n, m, l |
| **17** | **170–179** | l, **n, n, n**, l |
| **18** | **180–189** | m, n, n, n, l |
| **19** | **190–199** | m, n, n, n, m |
| **20** | **200** | **n, n, n, n**, m |

Row 20 is the strict apex. There are parallel `compensationTable` (failed the next tier),
`checkpoint50/100/150Table` (failed after a checkpoint start) and `checkpointBonusTable`, all also
[0…20]. **This is design headroom that predates the content**: the base-Crucible
`eventcontrol.lua` header comment reads, verbatim,
`-- Reward Tiers occur every 10 waves, up to 200 waves`, and `rewards.lua`'s reads
`-- Reward Tiers occur every 10 waves, up to 20 tiers`. Crate authored the 200-wave frame at Crucible
launch and shipped the waves in three tranches.

**Honesty note — do not use the tables as ceiling evidence.** I checked, and must report the negative:
the per-wave monster scaling record `balancingadjustment_survivalmode_enemies01.dbr` is **200 entries
long and byte-identical between the pre-FoA and FoA cuts — 0 changed cells across every column**. The
same is true of the reward tables. Their length proves the **design** ceiling was always 200; it does
**not** prove any wave was playable. Only the tier content + the `eventFinished()` placement do that.
Anyone re-deriving this should not stack these as independent evidence.

### 2.5 Difficulty does not change the ceiling — it changes the wall

All three Crucible difficulties run the same 200 waves; `Aspirant/Challenger/Gladiator` map internally
to `Game.Difficulty.Normal/Epic/Ultimate` and select one of three scaling records. All three are
200 rows. Monster `characterLifeModifier` (% bonus), at tier boundaries:

| wave | Aspirant | Challenger | **Gladiator** |
|---:|---:|---:|---:|
| 100 | 53 | 130 | 190 |
| 150 | 108 | 218 | 304 |
| 160 | 118 | 240 | 328 |
| **170** | **128** | **240** | **344** |
| **171** | **164** | **290** | **420** |
| 180 | 227 | 400 | 610 |
| 190 | 324 | 510 | 800 |
| **200** | **438** | **612** | **990** |

**Wave 171 is a step discontinuity, not a continuation** — Gladiator jumps +76 pp in one wave where
waves 161–170 stepped ~+4 pp each. The FoA band is a deliberate wall. Full 600-row table
(200 waves × 3 difficulties × 9 scaling columns) emitted to
`scratch/2026-08-07-u8-tierwave/u8_survival_wave_scaling.csv` — **directly consumable by the sim, and
version-stable** (identical pre/post FoA).

---

## 3 — TARGET 3: tribute/token gating and the offer set — **CLOSED**

### 3.1 The offer is a **FIXED SET**. Not highest-token, not highest-token+1.

**Directly read from Lokarr's start dialogue** (`npc_event_01.cnv`, AoM cut). The player options are a
hand-authored static list, one entry per shipped checkpoint, doubled by the Extra-Spawn variant:

```
Forget the bet. Let's begin. (Standard Crucible)      -> startEvent
Start on Wave 50                                      -> startTier05Event
Start on Wave 100                                     -> startTier10Event
Start on Wave 150                                     -> startTier15Event
Nevermind the bet. (Standard Crucible with Extra Spawn)
Start on Wave 50 (Extra Spawn)  /  100  /  150
```

The base-Crucible cut of the same file offers **only** `{Standard, 50, 100}`. The list grows by one
literal dialogue entry per expansion. **It is not computed from token state.** Pre-1.2.1.3 the entries
were merely *condition-gated* on token possession (`SURVIVALMODE_TIER10CHECKPOINT` appears twice as a
branch condition in the AoM `.cnv`); the list itself was always fixed.

**This resolves the commission's three-way question outright: offer = FIXED SET.**

### 3.2 The gate was removed in v1.2.1.3 — prior art's attribution is **CORRECT**

I re-verified the version attribution because the changelog thread is stacked newest-first and it is
easy to mis-read. Walking the version headers in banked `raw_142410.txt`: header
`[COLOR=orange][SIZE=115][b]V1.2.1.3[/b][/SIZE][/COLOR]` at line 109, `[aname=Crucible]` at line 120,
and the lines in question at 122–124. **They are under V1.2.1.3.** Verbatim:

> *"The Crucible no longer requires previously unlocking the wave 50/100/150 checkpoints on a character
> to start on them. **They are now immediately available for all characters.** The higher difficulties
> continue to be gated by beating wave 100 on the previous difficulty, or using a Crucible merit."*
>
> *"**Tributes are no longer required to start a Crucible at higher waves, but are still required for
> restarting or retrying a Crucible run.** End of event Tribute rewards have been reduced to compensate."*

So: **M1 (start offers) is ungated and free. M2 (death-rewind) costs tributes and is capped at 3 uses.**
Never blur them — the game itself does not.

### 3.3 Reconciling the fixture: offered 180, holds tokens through TIER15

No contradiction. The offer set does not read the token inventory on a 1.3.x client. The fixture's
`.gdc` holds TIER05/10/15 (legacy 2022 artifacts, per L1 § 4) and **not** TIER18 — yet Lokarr offered
`{50, 100, 150, 180}` on camera, because post-1.2.1.3 **every** checkpoint entry displays for every
character. The 180 entry exists because `SurvivalMode3` ships
`tagNotification_Checkpoint18 = "You can now resume the Crucible on Wave 180."`

**Two distinct gates, and only the second still bites:**

| gate | what it controls | status on 1.3.x |
|---|---|---|
| checkpoint tokens `TIERnnCHECKPOINT` | which start-waves Lokarr offers | **RETIRED v1.2.1.3** — all offered always |
| `SURVIVALMODE_{NORMAL,CHALLENGER,GLADIATOR}` + `Game.UnlockNextSurvivalDifficulty()` | which *difficulty* you may enter | **LIVE** |

Difficulty unlock, DB-CITED from `rewards.lua`: `tier10TokenGlobalMP` and `tier15TokenGlobalMP` each
call `Game.UnlockNextSurvivalDifficulty()`; `completeTokenGlobalMP` grants NORMAL / +CHALLENGER /
+GLADIATOR by `Game.Difficulty.Normal/Epic/else`, plus `GLADIATORBONUSSPAWNS` when the 6th spawn was
active. Amended by **v1.3.0.0**: *"Unlocking the next Crucible difficulty now also triggers at **Wave
110 and Wave 160**, rather than requiring clearing the Crucible Waves 1-100."* — i.e. checkpoint starts
now count. The developer guide still documents the old rule (*"Once you defeat the first 100 waves…"*);
**the guide is stale, the patch note governs.**

*Fixture cross-check, unsolicited:* the fixture's token set is `{TIER05, TIER10, TIER15, NORMAL,
CHALLENGER, GLADIATOR, DEFENSEBUILT, POWERUPACTIVE, 4POWERUPS}` — exactly a completed-on-Gladiator
profile **without** `GLADIATORBONUSSPAWNS`, i.e. fordprefect completed the ladder on Gladiator without
the 6th spawn point. Consistent with L1 and with `survival-greatest-wave = 170`, which is precisely the
2022-era ceiling.

---

## 4 — TARGET 4: checkpoint semantics — **CLOSED. First wave fought = label + 1.**

### 4.1 The two paths, read from source

**M1 — checkpoint start** (`eventcontrol.lua`), verbatim, with its own developer comment:

```lua
-- Start the Event at Wave 151
function gd.survival.eventControl.startTier15Event()
    Game.SetSurvivalWaveTier(151)
    Game.SetSurvivalDifficulty(151)
    gd.survival.rewards.checkpoint150Used()
    checkpointActivated(151)          -- sets checkpointUsed = true
    checkpoint = true
    gd.survival.eventControl.swapEventEntity()
    gd.survival.tier16Waves.startSurvivalModeEvent()
end
```

The sibling functions carry `-- Start the Event at Wave 51` / `at Wave 101` and set 51 / 101.
**The developer's own comment for the "Start on Wave 150" option says "Start the Event at Wave 151."**

**The wave counter** (`survivalevent.lua`, `SurvivalEvent_SpawnNext`) — increments *before* each wave,
and the checkpoint suppresses exactly the first increment:

```lua
if checkpointUsed then
    checkpointUsed = false
else
    Game.IncrementSurvivalDifficulty()
    Game.IncrementSurvivalWaveTier()   -- Increment wave # on code end for score purposes
end
...
waveEvent.waveIndex = waveEvent.waveIndex + 1
```

⇒ counter set to 151, increment skipped, `waveIndex = 1` → spawns `tier16waves/proxy_w01_*` = **wave 151**.

**M2 — death rewind** (`eventcontrol.lua` `restartEvent`):

```lua
if Game.GetSurvivalRestarts() < 3 then
    ...
    if wave >= 50 then
        local startingWave = ((math.floor (wave / 10)) * 10) - 20
        if startingWave > 1 then
            Game.SetSurvivalWaveTier(startingWave)
            Game.SetSurvivalDifficulty(startingWave)
        end
        if startingWave > 80 then gd.survival.rewards.RestartTest(startingWave) end
    end
end
```

No `checkpointActivated` call ⇒ the increment **fires** ⇒ from a wave-55 death, counter 30 → 31 →
`floor(31/10)=3` → tier04Waves → **first fought = 31**.

### 4.2 The invariant

**The two paths are implemented differently and mean the same thing.** M1 pre-sets `label+1` and
suppresses one increment; M2 pre-sets `label` and lets the increment run. Both land on:

> **`first_wave_fought = checkpoint_label + 1`**, and the HUD's "Current Wave" reads the wave being
> fought (`tagHUDWaveTier01 = "Current Wave"`, `…Info = "The Wave of Monsters you are currently
> fighting."`). The label names the last wave you are **credited with having cleared**.

**Sim parameter:** `start_wave = 151` for the "150" offer; `101` for "100"; `51` for "50"; `181` for
"180". A sim that starts at 150 will run one extra wave and mis-tier the entire run.

*This is a live falsifiable prediction against the fixture:* the wave-150 sitting's first HUD frame
should read **151**, and a sitting labelled "150→160" is exactly tier 16 (waves 151–160), 10 waves.
Routing to gandalf for frame confirmation — it costs one screenshot.

### 4.3 M2 formula — DB-CITED, and it matches the in-game text exactly

`startingWave = floor(wave/10) * 10 − 20`. The tutorial tag states the same rule in the other order:
*"20 waves before where you stopped, rounding down to the nearest 10th (ex. ending on Wave 55 will
restart you on wave 30)."* The two orderings are **algebraically identical** because 20 is a multiple of
10 — `floor(w/10)*10 − 20 ≡ floor((w−20)/10)*10`. **The project's stated M2 rule is confirmed with no
edge cases.** Guards: unavailable below wave 50 (`checkRestartCounterGlobalMP` returns −1 if
`wave < 50`); **hard cap of 3 restarts** (`Game.GetSurvivalRestarts() < 3`), matching
*"You may restart up to 3 times."*

### 4.4 Two engine quirks the sim should model or knowingly ignore

- **One-wave tier override.** `checkpointWave` overrides `rewardTier` in `SurvivalEvent_SelectMutators`,
  `SurvivalEvent_StartBonusTimer` and the trap roll — then is reset to 0 at the end of the first
  `SpawnNext`. So after an M1 start the mutator count, bonus timer and trap rate use the *checkpoint's*
  tier for **exactly one wave**. (I initially misread this as pinned for the whole run; corrected here.)
- **Bonus timer**, DB-CITED: `timer = (1 / ((multiplier + 1) ^ 0.49)) * (defaultTimer + tier * tierBonus)`
  with `defaultTimer / tierBonus` = 75000/10000 (Aspirant), 75000/11000 (Challenger),
  **80000/12000 (Gladiator)** ms. Hero kill +4 s, boss +8 s, nemesis +12 s.
- **Score**, DB-CITED (`records/game/playerscore.dbr`):
  `survivalScoreEquation = survivalMonsterScore*(1 + survivalCurrentWaveTier / 10)*survivalBonusMultiplier`,
  with per-kill `commonBonus [1,2,4]`, `championBonus [3,6,12]`, `heroBonus [30,60,120]`,
  `bossBonus [400,800,1600]`, `questBonus [100,200,400]` indexed by difficulty.

---

## 5 — Terminology: GD conflates "tier" and "wave". Pin it before the sim inherits the bug.

Three different things wear the word *tier* in this codebase. The sim must not merge them:

| term | meaning | range | where |
|---|---|---|---|
| **tier** (content) | a 10-wave band / one `tierNNwaves` module | 1–20 | `.arz` proxy paths, Lua module names |
| **rewardTier** | `floor(wave / 10)` — the reward-table index | 0–20 | `eventcontrol.lua`, `rewards.lua` |
| **`survivalWaveTier`** / "Wave Tier" | **the wave number itself**, 1–200 | 1–200 | `Game.{Get,Set,Increment}SurvivalWaveTier`, HUD *"Current Wave"* |

Note `rewardTier ≠ tier`: at wave 151, content tier = 16 but rewardTier = 15. They differ by one
everywhere except at exact multiples of 10. **`SURVIVALMODE_TIER18CHECKPOINT` uses the *checkpoint*
numbering (`nn` = content tier = wave/10), not rewardTier.**

---

## 6 — Corrections to prior art

1. **`legolas/notes/2026-08-05-eorwarlguts-save-parse.md` § 4 — extend.** That note correctly found
   `tagNotification_Checkpoint18` (wave 180) and correctly superseded the "TIER15 is the max checkpoint"
   framing. It stopped one step short: **the ladder itself runs to wave 200 (tier 20)**, and 180 is the
   last *checkpoint*, not the last *wave*. Its table should gain tiers 19–20 with "no checkpoint."
2. **Same note § 7.2 / U2 — CLOSED, and its premise corrected.** U2 recorded Crucible prices as
   "not in any `SurvivalMode*.arz` — engine-side… Crucible prices live in `Grim Dawn.exe`."
   **They are not in the exe.** They are in `Conversations.arc`: `object_defensesite_01.cnv` carries
   *"Create this defense (spend **5 Tributes + 7000 Iron Bits**)"* and *"…5 Tributes + 10000 Iron
   Bits"*; `npc_event_03.cnv` carries the restart ladder *"Restart at Checkpoint (Spend **5 / 15 / 30**
   Tributes)"*. See § 7.
3. **Same note § 11 U3 (clamp-on-load) — still open, but now testable.** With the award formulas in hand
   (§ 7) the ledger is arithmetic, not hypothesis.
4. **Community/wiki folklore "the Crucible is 170 waves" — STALE on 1.3.x.** Live web search still
   returns "150 or 100 are the only checkpoints" and "170 total"; both are pre-FoA. **Do not use
   community wiki text for Crucible wave facts on this client.** Grade any such claim EXTERNAL-STALE.
5. **`grimdawn.com/guide/game-settings/crucible/` difficulty-unlock text is stale**, superseded by
   v1.3.0.0's Wave 110 / Wave 160 rule (§ 3.3).
6. **Crucible achievement text is stale and is not ceiling evidence.** `achS001-003` still read
   *"Complete the Crucible through Wave 150"*, unchanged since the base DLC. The token they grant fires
   from `completeProgressToken`, which in the AoM build runs at the end of tier15 **and** tier16 —
   neither of which is the terminal tier. **Achievement text ≠ ladder ceiling.**

---

## 7 — Unsolicited closures (delivered because the source was open)

**Defense purchase — DB-CITED** (`object_defensesite_0N.cnv`): **5 Tributes + 7,000 or 10,000 Iron
Bits** per base defense; *"Each Defense can be upgraded twice"* with *"the Tribute and Iron Bits cost
goes up each time"* (`tagTutorialTip63TextC`). Named defenses: Inferno / Deathchill / Stormcaller
Beacon, Stonewall / Vanguard Banner, Barricade.
**⇒ the fixture's four base defenses cost exactly 20 Tributes.**

**M2 restart cost ladder — DB-CITED** (`npc_event_03.cnv`): **5 → 15 → 30** Tributes for restarts 1/2/3
(and a parallel **10 → 20 → 40** ladder on the post-completion restart branch). Cap 3.

**Tribute awards — DB-CITED** (`rewards.lua`), `d` = 0.74 / 1.15 / 1.35 (Aspirant/Challenger/Gladiator)
for end-of-event and 1.2 / 1.8 / 2.29 for per-tier:

```
per completed tier :  T = d_tier * ((rewardTier * 0.15) + 1.25)
end of event       :  T = d_end  * ((rewardTier * 0.29)^1.8 + 2.95)         rewardTier <= 15
                      T = d_end  * ((rewardTier * 0.29)^1.8 - 2.95)         rewardTier >  15
   if failed / restarted:  T = T/1.5 - {0.1, 0.8, 1.1}[difficulty]
   if a checkpoint was used and you failed:  T = T/4
   ... and T = 0 outright if (checkpoint150Used and rewardTier <= 15)      [and 50/<=5, 100/<=10]
```

The last clause is the code behind v1.3.0.0's *"Failing the Crucible on the same tier as a checkpoint no
longer awards Tribute."* **Applied to the fixture** (Gladiator, started at checkpoint 150, died at wave
160 ⇒ `rewardTier = 16`): the zero-award clause does **not** fire (16 > 15); award ≈
`1.35 * (4.64^1.8 − 2.95) = 17.4` → failed `/1.5 − 1.1 = 10.5` → checkpoint `/4 ≈ **2.6 Tributes**`.
Tribute cap is 150 (`tagHUDTribute01Info`).

**Ledger check, reported honestly and NOT claimed as closed:** L1 measured `tributes 999 → 128`, a net
−22 from a hypothesised 150 clamp. Four defenses = **20**. That leaves a residual of ~2 against a
model that also has to absorb the 08-04 sitting's earnings (capped), the unattested 08-03 session, and
rounding. **The inputs are now all in hand; the arithmetic belongs to whoever owns L1's U2/U3.** I am
not claiming closure on the clamp.

**Per-wave monster scaling table** — `scratch/2026-08-07-u8-tierwave/u8_survival_wave_scaling.csv`,
600 rows (200 waves × 3 difficulties), 9 columns, version-stable pre/post-FoA.

---

## 8 — Gaps, stated plainly

| # | Gap | Why it is open | What closes it | Impact |
|---|---|---|---|---|
| **G1** | **`SurvivalMode3`'s Lua is not on disk.** No corpus here carries `survivalmode3/resources/Scripts.arc` or `Conversations.arc` — Edition-II is a curated `.arz`+`Text_EN.arc` subset, and the full install predates FoA. So `startTier18Event`'s literal (**181**, by the 51/101/151 pattern) and the relocation of `eventFinished()` from tier17 to **tier20** are **STRUCTURALLY INFERRED, not read.** | the archives were never fetched | one depot pull of the FoA `survivalmode3` resources | **Low.** The 200 ceiling is independently DB-CITED (§ 2.1) and developer-CITED (§ 2.2). Only the exact `181` literal and the `eventFinished()` line rest on the pattern — and the pattern is 3/3 exact across two prior expansions. |
| **G2** | The FoA `npc_event_01.cnv` offer list was not read. `{50,100,150,180}` is MEASURED on-camera from the fixture and corroborated by `tagNotification_Checkpoint18`; the dialogue file itself is behind G1. | same as G1 | same as G1 | Low — two independent confirmations already. |
| **G3** | Whether any wave 181–200 content changed in v1.3.0.1–1.3.0.5. The corpus is pinned at 1.3.0.0; the fixture client is 1.3.0.5. | Edition-III cut not taken | Edition-III depot cut | Low, and **bounded**: the 08-04 patch-delta probe already grepped 1.3.0.1–1.3.0.5 and found exactly one Crucible line, at wave 200 (Grava'Thull spawn), plus nothing on tiers 18–20 tuning. |
| **G4** | Wave-order *within* a tier is not fully deterministic: each spawn point picks one proxy at random from its `{w,p}` list, and each proxy picks one weighted pool. Density is a distribution, not a number. | by design | already characterised in `2026-08-01-gd-pack-density-ranking.md` | Sim must sample, not tabulate. |

**No gap touches the four commissioned questions' verdicts.**

---

## 9 — Grade summary

| # | Target | Verdict | Provenance |
|---|---|---|---|
| 1 | Full tier→wave map, all 20 tiers | **CLOSED** | **DB-CITED** ×4 independent (developer source comments · dispatcher arithmetic · `.arz` inventory · checkpoint tags) |
| 2 | Ladder ceiling on Gladiator = **wave 200**; 170 is not terminal post-FoA | **CLOSED** | **DB-CITED** (three-cut tier differential · `eventFinished()` placement) **+ EXTERNAL-CORROBORATED** (Steam DLC page · grimdawn.com FoA guide · v1.2.0.0 and v1.3.0.4 patch notes) |
| 2b | "Cash out" = every 10 waves, not a 170 mechanism | **CLOSED** | **DB-CITED** (`npc_event_02.cnv` + `questevents.lua` + `SurvivalEvent_Update`) **+ EXTERNAL-CORROBORATED** (grimdawn.com Crucible guide, verbatim) |
| 2c | What waves 161–200 reward | **CLOSED** | **DB-CITED** (`rewardTable[16..20]`) |
| 3 | Offer set = **FIXED SET**, ungated since v1.2.1.3 | **CLOSED** | **DB-CITED** (`npc_event_01.cnv` static option list, base vs AoM) **+ EXTERNAL-CORROBORATED** (v1.2.1.3 notes, version attribution re-verified) |
| 3b | Difficulty gate is separate and still live | **CLOSED** | **DB-CITED** (`rewards.lua`) + v1.3.0.0 amendment (Wave 110 / 160) |
| 4 | `first_wave_fought = label + 1`, both M1 and M2 | **CLOSED** | **DB-CITED** (`startTier{05,10,15}Event` + `SurvivalEvent_SpawnNext` + `restartEvent`), incl. the developer's own `-- Start the Event at Wave 151` |
| 4b | M2 = `floor(w/10)*10 − 20`, ≥50 only, max 3 | **CLOSED** | **DB-CITED**, algebraically identical to the in-game tutorial text |

---

## CLOSURE VERDICT

**CLOSED** — all four commissioned questions settled from primary game source, with two named
low-impact gaps (**G1** `SurvivalMode3` Lua not on disk ⇒ the `startTier18Event` literal `181` and the
`eventFinished()`-at-tier-20 line are structurally inferred rather than read; **G2** the FoA offer-list
file likewise). Neither gap changes any verdict: the wave-200 ceiling is independently established by
the tier differential and by Crate's own patch notes and store copy.

### tier→wave table

| tier | waves | tier | waves | tier | waves | tier | waves |
|---:|---|---:|---|---:|---|---:|---|
| 01 | 1–10 | 06 | 51–60 | 11 | 101–110 | 16 | 151–160 |
| 02 | 11–20 | 07 | 61–70 | 12 | 111–120 | 17 | 161–170 |
| 03 | 21–30 | 08 | 71–80 | 13 | 121–130 | **18** | **171–180** |
| 04 | 31–40 | 09 | 81–90 | 14 | 131–140 | **19** | **181–190** |
| **05** | **41–50** ◆ | **10** | **91–100** ◆ | **15** | **141–150** ◆ | **20** | **191–200** ✦ |

◆ = checkpoint at tier end (50 / 100 / 150) · tier 18 end = checkpoint **180** ◆ · ✦ = **terminal wave 200**
**Rule:** tier *n* = waves 10(*n*−1)+1 … 10*n* · `rewardTier = floor(wave/10)` · M1 start "wave *L*" ⇒ **first fought = *L*+1**

---

**Signed:** legolas, 2026-08-07. The map ended at the `.arz`, so I went past it: the Crucible's wave
engine is 24 files of commented Lua sitting inside an archive nobody here had opened. It answers every
question the database could not, in Crate's own words — including the one comment that settles the
whole probe: `-- Start the Event at Wave 151`.
