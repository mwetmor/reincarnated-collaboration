# Devotion payload probe — the void is not a void

**Author:** elrond (data steward) | **Date:** 2026-07-25 | **Commission:** gandalf, GD program (G-5 key)
**Predecessor:** `2026-07-25-gd-player-mechanism-census.md` §5.1 — devotion proc binding ranked #2
(18/41 kits, 44%), payloads recorded as EMPTY, flagged "one source away."
**Verdict:** **HELD. READABLE TODAY. The census's §5.1 hole closes on this source.**
**Scope discipline:** bounded probe. Read-only. **Zero writes to `corpus.db`. Zero migration performed.**

---

## 0. Bottom line

| Question | Answer |
|---|---|
| Q1 — held? | **YES.** Full Grim Dawn install banked locally, three copies. Devotion records in all four `.arz` archives. |
| Q2 — readable by the width-one adapter? | **YES, unmodified.** `ArzArchive` imported as-is; devotion records decode on first attempt. No parser work needed. |
| Q3 — extraction size? | **823 header rows / ~11,776 payload field rows / 65 celestial powers / 110 constellations.** |
| Q4 — Matt fetch needed? | **NO. Not applicable — nothing to fetch.** Q4 is moot; no `matt_to_do` drafted. See §5. |

**The one number that matters: 65 celestial powers, each with an explicit trigger, an explicit
internal cooldown, and a full rank-array damage/effect payload.** That is the surface the G-5
devotion build item needs to be specced against, and it is sitting on this Mac.

---

## 1. Q1 — INVENTORY: what is held

### 1.1 The holdings

Three GD installs are banked under `/Users/admin/Games/vendor/`:

| Path | `database.arz` | Note |
|---|---|---|
| `grim-dawn/` | 58,338,379 B | Full install incl. all `.arc` resource paks |
| `grim-dawn-edition-I-20260723/` | 58,338,379 B | Edition-I depot pin |
| `grim-dawn-edition-II-20260724/` | 58,338,379 B | **Edition-II depot pin — used by this probe** (matches the attestation-scope census, so counts are comparable) |

Byte-identical base `database.arz` across all three. Probe ran against **Edition-II** for continuity
with `2026-07-25-gd-attestation-scope-census.md`.

### 1.2 Devotion records present — per archive

| Archive | Total records | Devotion-path records |
|---|---:|---:|
| `database/database.arz` | 34,114 | 1,714 |
| `gdx1/database/GDX1.arz` | 18,447 | 981 |
| `gdx2/database/GDX2.arz` | 16,451 | 1,113 |
| `gdx3/database/GDX3.arz` | 24,178 | 176 |
| **UNION (dedup, later archives override base)** | **82,131** | **3,242** |

### 1.3 The lane structure — four distinct sub-lanes, all held

The census guessed `records/ui/skills/devotion/`. That guess was **half right**, and the half it
missed is the important half. The real structure separates presentation from behaviour:

| Path | Count (union) | What it actually is |
|---|---:|---|
| `records/skills/devotion/**` | **823** | **THE BEHAVIOUR LANE.** Star-node passives + celestial-power payload records. This is the answer. |
| `records/ui/skills/devotion/constellations/` | 110 (non-background) | **THE GATING LANE.** Affinity given/required, point costs, tree placement. |
| `records/ui/skills/devotion/` | 626 | Presentation only — bitmaps, button positions, the `skillName` pointer that joins UI node → behaviour record. |
| `records/skills/devotion/pets/` | 147 | Pet-scaling lane (`PetPlayerScaling`, `Pet`). |

Sub-lane rtype breakdown of the behaviour lane (823): `Skill_Passive` 502 · untyped 107 ·
`PetPlayerScaling` 100 · `Pet` 20 · plus 34 distinct `Skill_Attack*` / `Skill_Buff*` /
`SkillBuff_*` classes carrying the active procs.

### 1.4 What is held vs missing — against the census's four named voids

The census named four things it could not attest. All four are held:

| Census void (§5.1) | Held? | Where |
|---|---|---|
| "what a devotion proc does" | **HELD** | `offensive*` / `defensive*` / `retaliation*` rank arrays on the payload record |
| "the proc's trigger condition" | **HELD** | `templateAutoCast` → autocast controller with explicit `triggerType` + `targetType` + `chanceToRun` |
| "the proc's ICD" | **HELD** | `skillCooldownTime` — present on **62** of the 65 celestial powers |
| "devotion point-cost / affinity gating" | **HELD** | `affinityGiven1..3` / `affinityRequired1..3` + named affinity on the 110 constellation records |
| "devotion binding rules (which skill a proc attaches to)" | **PARTIAL — see §4.1** | The trigger *condition* is exact; the *player's chosen binding target* is a save-game/runtime choice, not authored in `.arz` |

**Bonus, unasked-for and load-bearing:** `FileDescription` on the behaviour records carries the
**human-readable devotion name in-record**, formatted `<Constellation> - <Proc Name>`
(e.g. `'Bat - Twin Fangs'`). **The `.arc` tag-bridge flagged PENDING at G4 of the GD-SLICE run is
NOT required for this lane.** Names come free.

---

## 2. Q2 — READABLE: smoke test, one record verbatim

### 2.1 Adapter status: works unmodified

`ArzArchive` from `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` was imported
**as-is** and pointed at devotion records. **Decoded on first attempt. Zero parser changes. Zero new
format work.** The width-one proof generalizes to this lane with no engineering.

(Only `ArzArchive` was imported. `build_rows` and the DB-apply path were deliberately NOT run —
they are hard-coded to the Flames-of-Ignaffar kit and would be a migration, not a probe.)

### 2.2 Fully-decoded record — VERBATIM PROOF

**This is the census's own example.** `gd-ravenous-earth-oppressor.fidelity_notes` said, verbatim:
*"Twin Fangs devotion proc named ('wonderful combo') but payload behavior unfetched."*

Here is Twin Fangs, fetched. `records/skills/devotion/tier1_01e_skill.dbr`
(archive `database/database.arz`, rtype `Skill_AttackProjectileBurst`, **276 fields decoded**,
25 non-default):

```
    Class = 'Skill_AttackProjectileBurst'
    FileDescription = 'Bat - Twin Fangs'
    cameraShakeAmplitude = 0.11999999731779099
    distanceProfile = 'Maximum'
    offensiveLifeLeechMin = [20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0,
                             30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 40.0]
    offensiveLifeMax = [46.0, 53.0, 60.0, 67.0, 74.0, 81.0, 88.0, 95.0, 102.0, 109.0,
                        116.0, 123.0, 130.0, 137.0, 144.0, 151.0, 158.0, 165.0, 172.0, 186.0]
    offensiveLifeMin = [28.0, 32.0, 36.0, 40.0, 44.0, 48.0, 52.0, 56.0, 60.0, 64.0,
                        68.0, 72.0, 76.0, 80.0, 84.0, 88.0, 92.0, 96.0, 100.0, 108.0]
    offensivePierceMin = [40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0,
                          90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0, 140.0]
    projectileLaunchNumber = 2
    projectileLaunchRotation = 10.0
    projectilePiercingChance = 100.0
    skillBaseDescription = 'tagDevotionEffectA01Desc'
    skillCooldownTime = 0.6000000238418579
    skillDisplayName = 'tagDevotionEffectA01'
    skillDownBitmapName = 'ui/skills/icons/skillicon_devotionstar01_down.tex'
    skillExperienceLevels = [0, 30000, 63816, 104308, 155181, 221016, ... 20 entries]
    skillMaxLevel = 1
    skillProjectileName = 'records/fx/skillsdevotion/batfang_projectile_fx01.dbr'
    skillTemplates = ['records/skills/base_template skills/skill_attackprojectile.dbr', ... 35]
    skillUltimateLevel = 1
    skillUpBitmapName = 'ui/skills/icons/skillicon_devotionstar01_up.tex'
    targetingMode = 'Target'
    templateAutoCast = 'records/controllers/itemskills/cast_@enemyonattack_20%.dbr'
    templateName = 'database/templates/skill_attackprojectileburst.tpl'
    weaponDamagePct = [10.0, 10.0, 11.0, 11.0, 12.0, 12.0, 13.0, 14.0, 14.0, 15.0,
                       15.0, 16.0, 16.0, 17.0, 17.0, 18.0, 18.0, 19.0, 19.0, 20.0]
```

And the trigger, resolved one hop — `records/controllers/itemskills/cast_@enemyonattack_20%.dbr`:

```
    FileDescription = '20%'
    autoTargetRadius = 22.0
    chanceToRun = 20
    targetType = 'Enemy'
    templateName = 'database/templates/skillautocastcontroller.tpl'
    triggerType = 'AttackEnemy'
```

**Read that as a spec sentence:** *Twin Fangs fires on a 20% chance when you attack an enemy
(`triggerType=AttackEnemy`, `chanceToRun=20`), on a 0.6 s internal cooldown, launching 2 fully-piercing
projectiles 10° apart at 22 wu auto-target radius, dealing 108–186 vitality + 140 pierce + 20%
weapon damage with 40% life leech at rank 20 of 20.*

That is exactly the shape of statement the census said we could not make about a single devotion.
We can now make it 65 times.

### 2.3 Name resolution — all four census-named devotions land

The census named four devotions as evidence of the void. All four resolve, with constellation:

| Census name | `FileDescription` | Record |
|---|---|---|
| Meteor Shower | `"Ulzuin's Torch - Meteor Shower"` | `records/skills/devotion/tier3_07g_skill.dbr` |
| Eldritch Fire | `"Solael's Witchblade - Eldritch Fire"` | `records/skills/devotion/tier2_11e_skill.dbr` |
| Targo's Hammer | `"Anvil - Targo's Hammer"` | `records/skills/devotion/tier1_05e_skill.dbr` |
| Bonds of Bysmiel | `"Bysmiel's Bonds"` (4 star nodes `tier2_12a..d`) | `records/skills/devotion/tier2_12*.dbr` |

Note the last one is a **finding, not a match**: the census recorded "Bonds of Bysmiel" as if it
were a proc. In the source it is a **constellation** (`Bysmiel's Bonds`) whose nodes are passives —
the corpus's kit prose conflated a constellation with a celestial power. That conflation is invisible
without this source and would have mis-specced the build item. See §4.2.

### 2.4 Trigger vocabulary — 29 distinct trigger templates across 65 powers

The full proc-trigger vocabulary of Grim Dawn's devotion system, enumerated:

| Count | Trigger template |
|---:|---|
| 9 | `cast_@enemyonattack_15%` |
| 5 | `cast_@selfonattack_20%` · `cast_@enemyonattackcrit_100%` |
| 4 | `cast_@selfonattack_25%` · `cast_@enemyonattack_25%` · `cast_@selfonattackcrit_100%` · `cast_@selfonanyhit_30%` · `cast_@enemyonattack_20%` |
| 2 | `cast_@enemyonanyhit_33%` · `cast_@selfonattack_33%` · `cast_@enemyonattack_30%` · `cast_@enemyonattack_100%` · `cast_@selfonanyhit_25%` |
| 1 | `cast_@selfat45%health_100%` · `cast_@selfonmeleehit_20%` · `cast_@enemyonblock_50%` · `cast_@enemyonattack_35%` · `cast_@selfat50%health_100%` · `cast_@selfonblock_50%` · `cast_@selfonanyhit_15%` · `cast_@selfonanyhit_20%` · `cast_@selfonattack_100%` · `cast_@selfat40%health_100%` · `cast_@selfonattack_15%` · `cast_@selfonblock_33%` · `cast_@enemyonanyhit_50%` · `cast_@enemyonanyhit_20%` · `cast_@enemyonanyhit_30%` · `cast_@enemylocationonanyhit_30%` |

**The design read (offered, not ruled — Gandalf interprets):** the whole system reduces to a small
orthogonal product — **trigger event** {`onattack`, `onanyhit`, `onattackcrit`, `onmeleehit`,
`onblock`, `at<N>%health`} × **target frame** {`self`, `enemy`, `enemylocation`} × **proc chance**
{15/20/25/30/33/35/50/100%} — plus a per-power ICD. Six events, three frames, eight chance values.
That is a **notably small and buildable** specification surface for a mechanism at 44% kit-count.

**The pet-vs-self flag the census asked for is the `@self`/`@enemy` axis**, corroborated by
`isPetDisplayable` on the payload record and the 147-record `records/skills/devotion/pets/` lane.

---

## 3. Q3 — SIZING the full extraction

### 3.1 Record and row counts (measured, not estimated)

| Quantity | Count |
|---|---:|
| `exact_skill` HEADER rows (devotion behaviour records) | **823** |
| — of which **CELESTIAL POWERS** (carry `templateAutoCast`) | **65** |
| — with explicit ICD (`skillCooldownTime`) | **62** |
| — pet-lane flagged | 244 |
| CONSTELLATION records (affinity / point-cost gating lane) | **110** |
| Distinct constellation names (in-record, no `.arc` needed) | 107 |
| **`exact_skill_field` PAYLOAD rows** (boilerplate excluded, arrays expanded) | **~11,776** |
| Distinct payload field names | 261 |
| Max rank-array depth | 48 |

**On the two row numbers.** A naive "every non-zero field" count gives **117,363** rows. That number
is wrong to publish and I am recording why: it is dominated by engine boilerplate —
`skillExperienceLevels` (20-element XP tables on all 65 powers), `skillTemplates` (35-element
template chains), `skillBlackList`, `characterRacialProfile`. Excluding a 12-name boilerplate set
and filtering to behaviour-bearing field families yields **11,776**. **11,776 is the number to plan
against; 117,363 is what you get if you bank the lane without a field policy.** The 10× gap is the
single largest cost lever in this extraction and it is a *curation* decision, not a parsing one.

### 3.2 Effort

| Task | Effort | Note |
|---|---|---|
| Parser work | **ZERO** | `ArzArchive` works unmodified. Proven in §2. |
| Multi-archive merge | **SMALL** | 4 archives with override precedence (base < gdx1 < gdx2 < gdx3). The probe already implements it in 3 lines. Must be explicit in schema meta — an unmerged extraction silently reads stale base-game values for FG-patched devotions. |
| Field policy (the 11,776-vs-117,363 decision) | **MEDIUM** | The real work. Needs a boilerplate deny-list + `is_core` assignment across 261 field names. Analogous to the 136-row FoI `FIELD_CLASS` map, at ~2× the field breadth. |
| Trigger-controller resolution | **SMALL** | One extra `read_record` hop per power; 29 distinct controllers, decode once and cache. |
| Constellation/affinity lane | **SMALL** | 110 records, flat scalar fields, no arrays. |
| Verification (tier-1 anchors) | **MEDIUM** | Per GD-SLICE law, needs a byte-match oracle. **Float32 canonicalization is mandatory** — `skillCooldownTime=0.6` presents as `0.6000000238418579`; the exact trap that failed G3 3/22 on the first FoI run. Documented, not re-learnable-the-hard-way. |

**Overall: ONE focused run**, comparable to the GD-SLICE run in shape but with the parser already
paid for. The dominant cost is the field policy, not the pipe.

### 3.3 Schema work needed (DESIGN ONLY — no migration performed)

The existing `exact_skill` / `exact_skill_field` pair is **structurally sufficient for the payload**
and needs no change to carry it — that is the TSR-2 extension property the GD-SLICE run demonstrated,
now exercised a second time at 823× the width. Devotion-specific fields land as `is_core=0`
extension rows exactly as `offensiveSlowFireMin` did.

What the pair **cannot** carry, and what a new lane would need:

1. **`devotion_power` (trigger surface).** `record_path` PK; `trigger_type`, `target_type`,
   `chance_to_run`, `auto_target_radius`, `icd_sec`, `constellation_name`, `power_name`,
   `autocast_record` (raw provenance). ~65 rows. **This is the table the G-5 build item is actually
   asking for.** Note it is a *derived* table — one hop off the payload record — so per my
   reversibility principle it stores `autocast_record` verbatim alongside the decoded fields.
2. **`devotion_constellation` (gating surface).** `affinity_given_{1,2,3}` + names,
   `affinity_required_{1,2,3}` + names, star count, tier. ~110 rows. Nothing in the current schema
   models a point-economy gate.
3. **`devotion_node` (tree structure).** UI node → behaviour record join
   (`records/ui/skills/devotion/tierN_MMx.dbr` `skillName` → `records/skills/devotion/...`).
   Needed only if the build item cares about tree topology; **skippable for a v1 payload spec.**

**Recommendation (steward authority, my domain):** bank the payload into the existing
`exact_skill`/`exact_skill_field` pair with a boilerplate deny-list, and add **only tables 1 and 2**.
Defer table 3. Additive, backup-first, `MIGRATION-*.md` per ADR-004, same discipline as GD-SLICE.
**Not doing it now — this was a probe, and the field policy deserves its own gate.**

---

## 4. HONEST UNKNOWNS — first-class

### 4.1 Devotion→skill BINDING is not in the `.arz`, and probably never will be

The census asked for "devotion binding rules (which skill a proc attaches to)." The trigger
*condition* is fully attested (§2.2). But **which player skill a celestial power is bound to is a
runtime player choice**, stored in the save game, not authored in the database. I found no
authored binding field, and I would not expect one — GD's design intent is that binding is the
player's decision.

**What this means for the build item:** "devotion proc binding" as a *mechanism* is
`(trigger event × target frame × chance × ICD) + a player-chosen attachment point`. The first part is
now fully specced. The second part is a **UI/state design question, not a datamining question**, and
no amount of further extraction will answer it. **This should be routed to Gandalf as a design
question, not left on my docket as a data gap.** Flagging explicitly so it is not mistaken for
something one more crawl would close.

### 4.2 The corpus conflates constellations with celestial powers

§2.3: "Bonds of Bysmiel" is recorded in kit prose as a proc; in the source it is a **constellation**
(`Bysmiel's Bonds`) of passive nodes. I did not audit how widespread this is — the probe was bounded.
**27 kits touch devotion strings** across 10 corpus columns (`kit_dossier.payload_json` 34 mentions,
`kit_mapping.mapping_json` 17, `kit_dossier.anchor_quote` 11, and 7 more). The census's 18-kit
count is the *named-devotion* subset of a wider 27-kit mention surface.

**CANNOT ATTEST:** how many corpus devotion names are constellations vs powers vs star nodes.
**What would attest it:** a string join from corpus devotion mentions → `FileDescription` after the
extraction lands. Cheap — a SQL query, once the lane exists. **Until then, any kit-count over
"devotion procs" is soft**, because some fraction of it counts constellations. This does not threaten
the #2 ranking (44% is far past threshold and constellations are devotion-system usage either way),
but it does mean the build item must not be specced off the kit prose alone.

### 4.3 `skillMaxLevel = 1` on the powers, but 20-element rank arrays

Twin Fangs has `skillMaxLevel=1` and `skillUltimateLevel=1`, yet its damage arrays have 20 entries.
The FoI precedent (`skillMaxLevel` 16 + ultimate 10 = 26 ranks) does not apply. My working reading
is that celestial powers scale on **devotion points invested in the constellation**, not on a skill
rank the player buys — which would make the 20 the constellation-progress axis. **I did not verify
this**, and it matters: it determines what the rank index *means* in the banked rows. **Must be
resolved before banking**, or `exact_skill_field.rank` carries an unlabelled semantic.
Max array depth across the lane is **48**, not 20, so at least one lane has a different axis again.

### 4.4 Edition pin not captured

Probe ran against Edition-II. Per the `gd-edition-pin-2026-07-24` convention, a real extraction must
capture edition label + depot + manifest id + `arz_sha256`. I did **not** compute hashes here — out
of probe scope. The three installs' base `database.arz` are byte-identical *by size*; I did not
checksum them. Flagging so the extraction run does it properly rather than inheriting my shortcut.

### 4.5 What I did NOT check

Bounded probe. Not examined: `records/skills/devotion/pets/` internals beyond record counts;
the 502 `Skill_Passive` star nodes' stat-bonus payloads in detail (counted, not characterized);
`_devotiontree.dbr` (1,678 fields — clearly the tree topology, unparsed); `.arc` text tags
(unnecessary for this lane, per §1.4); the 79 `records/creatures/enemies/devotion/` Monster records
(likely shrine-guardian encounters, not player mechanism — **not** part of this lane).

---

## 5. Q4 — MATT FETCH SPEC: **NOT APPLICABLE**

Q4 was conditional on Q1 = NO. **Q1 = YES.** There is nothing for Matt to fetch — the full Grim Dawn
install including all four `.arz` archives and every `.arc` resource pak is already resident on this
Mac under `/Users/admin/Games/vendor/`, banked 2026-07-23/24.

**No `matt_to_do` entry drafted. Nothing to route.** Recording this explicitly so the absence is
read as a deliberate finding rather than an omission.

---

## 6. REPRODUCTION

```bash
cd /Users/admin/Games/reincarnated-collaboration
python3 agentic_orchestration/elrond/notes/2026-07-25-devotion-payload-probe.py
```

Prints Q1 inventory, Q2 full decode + trigger controller, Q3 sizing + trigger vocabulary.
**Read-only:** `.arz` files opened via `Path.read_bytes()`; `corpus.db` **not opened at all** by the
script. Verified post-probe: `corpus.db` mtime unchanged (Jul 24 21:29), vendor `.arz` mtimes
unchanged, `git status` shows no modification under `research/`.

Depends on `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` (imports
`ArzArchive` only; `build_rows` and the DB-apply path are deliberately not invoked).

---

## 7. WHAT THIS UNBLOCKS

The census said: *"the kit-count says 'build it'; the payload void says 'you cannot yet specify
what.'"* **The payload void is closed.** The devotion surface can now be specced from primary source:

- 65 celestial powers, named, with constellation attribution
- 29 trigger templates reducing to 6 events × 3 target frames × 8 chance values
- 62 explicit ICDs
- Full rank-array damage/effect payloads per power
- 110 constellations with affinity-give/require point economy

**One caveat carried forward, and it is not small:** §4.1 — the *binding* half of "devotion proc
binding" is a player-choice design question that no extraction will answer. The build item should be
chartered knowing that the mechanism it is copying is half data (now held) and half UX (still open).

**Recommended next step** (offered, not ruled — knight-rider sequences): a bounded extraction run
against gates in the GD-SLICE shape, whose first gate is the **field policy** (§3.1) and whose
second resolves the **rank-axis semantics** (§4.3). Both must land before rows are banked.
