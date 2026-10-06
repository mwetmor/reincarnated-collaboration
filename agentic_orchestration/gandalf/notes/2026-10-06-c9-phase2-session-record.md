# Run C-9 Phase 2: session record (conductor session aab928, 2026-10-02 → 2026-10-06)

**STATUS:** CURRENT (evidentiary record of one conductor session). **Author:** gandalf (RUN-CONDUCTOR).
**Truth of record:** `astra_test_01/burst/runs/C-9/ledger.json`, rulings **R-C9-135 → R-C9-160**, with Matt verbatim on each. Where this record and the ledger disagree, the ledger wins.
**Companion:** the forward-looking handoff is `2026-10-06-c9-phase2-session2-handoff.md`.

---

## 1. Outcome in one paragraph

Matt's playtest priority 1 was **delivered**: he played the **dressed warlord build in the KC2 2D arena** and died in wave 160, as in his GD footage. REFERENT-v1 was sealed (r2, KC2 KP-302).

C-9's part was to supply what that build needed:
- **every enemy family** for waves 151–160, alternates included;
- the warlord's **eor3** pack;
- the **Eye of Reckoning overlay** atlas.

The **Barrow web page** was upgraded and deployed once (`d069c4b`).

**barrow_v2** went through five approaches. The last runs as a level inside the v1 Barrow engine, with v1's plants, wind, snow and moving water, but Matt judged that it **still falls short of v1's quality**. Its work is handed to a fresh session (R-C9-160).

## 2. What was built and delivered

### 2.1 Enemy packs (JOIN-1 sprite cells, all with `true_size`)

| Lane | Packs (`astra_test_01/burst/runs/C-9/join1_pack/…`) |
|---|---|
| EN-E2 | `en-warden_p`, `en-magister_p`, `en-witch_p`, `en-mindtaker_p` (painted; warden and magister get the calm unarmed locomotion), `en-fleshshaper` (w152), `en-ascended` (w154), `en-vigillord` (w160 nemesis, transfer rig), `en-fleshhulk` and `en-colossus` (Mixamo mutant set, R-C9-150) |
| EN-E3 | `en-woollyrhino`, `en-crawlerlarva_p`, `en-burrowworm_p` (emerge fold fixed), `en-abomination` (w153, pinned), `en-hellhound` (w156 alt) |
| EN-E4 | `en-coilseer` (slith01, w153 alt), `en-gloamwing` (gryphon rig, w158 alt; designed size primary, KC2 ruling) |
| SZ | `true_size` blocks on 18 tier-1 kits, plus the table `join1_render/true_size_table_2026-10-02.{md,json}` |
| E1b | `join1_pack/gd-eor-warlord-eor3` (helm notch fixed: the body's own crown was poking through; R-C9-141) |
| SO | `join1_pack_v4/d2-fire-sorc-bm` (staff aim fixed, calmer idle). **v4 is SUPERSEDED pending v5** (R-C9-152 hood fix) |

**Every w151–w160 family now has a pack.**

KC2 finding raised by C-9 (KP-253): the traced PLAY floor did not contain the v3.8 spawn anchors. Five of the six were partly or fully off it. KC2 now bounds the floor by the anchor-disc hull.

### 2.2 VFX
- **EoR in the Barrow (EOR2):** R-C9-128's port had used the wrong source (`wwcr_whirlwind.gd`). It was re-ported from `kc2_player_channel.gd` (R-C9-143), then restyled per R-C9-152: no arc, no rims, a translucent dusty-red haze plus sparks.
  - Final Barrow code: `b4de84e65`. Web perf: +7 draws, about 0 ms.
- **EoR 2D overlay atlas for kc2_play:** `join1_vfx/eor_overlay/` (manifest `95639a770`). Haze UNDER the actor, sparks OVER; hooks on oracle events. KC2 drops its ribbon.
- **barrow_v2 spawn-delivery VFX (DV):** `join1_vfx/barrow_v2_spawn/`, six sources, oracle-event contract (KC2 KP-268). **Shelved with the 2D route, but reusable.**

### 2.3 Barrow web page (loadout, Vercel)
- **Deployed `d069c4b`:**
  - the sorceress arena kit (`armor=bm134`, `soidle=ss4`);
  - the character-light toggle (`charlight=a|b|c`; **b** matches the cliffside);
  - the Meteor always lands on the ground and scorches objects (`v5=b`; R-C9-142 retired part a);
  - the eor3 helm;
  - the EoR at the R-C9-143 look.
- **NOT yet deployed:**
  - the R-C9-152 EoR (red-tinted smoke + sparks, `b4de84e65`);
  - the sorceress hood fix (option B, `so_mx/export/ss152b`);
  - the `eorsmoke` smoke-tint row.

  All three are built and paused, waiting on Matt's go.

### 2.4 Mixamo (Matt downloaded the Creature ×2 and Zombie ×2 packs)
- Audition (MX), accepted in full (R-C9-150):
  - brutes: mutant idle/walk/run/punch/roar;
  - wretch: zombie idle/attack/hit;
  - revenant: zombie idle;
  - "zombie stand up" as an emerge.
- **Applied so far:** fleshhulk and colossus. **Pending:** wretch, revenant, emerge.

## 3. barrow_v2: what was tried, in order (read this before touching it)

| # | Approach | Rulings | What happened | Lesson |
|---|---|---|---|---|
| 1 | "King's Henge" design: a convex floor from the oracle's spawn geometry | brief artifact `8PPHnVguimBdHBPzSGZw9u` | The legend confused Matt. Seven barrow variants read "too similar" | Design whole SITES with varied spawn sources, not one motif repeated |
| 2 | Site concepts → **Fjord Headland** (sketch A + B's stream) | R-C9-144/145 | Matt chose the site. The spawn plan maps each door to a deliverer | **Sketch A (`barrow_v2/sites/BV3r2-A.png`) is the look of record** |
| 3 | 3D greybox (BX, layout v1→v6, validator) as the paint guide | R-C9-148/149a | "Man-made and square"; the biome sculpt still read as an empty plaza with a "naval-fortress" coast | Primitive geometry imposes its shapes on paint. The validator and layout rules ARE valuable |
| 4 | 2D zone map + Astra chunks painted for the 2D arena skin (BVP) | R-C9-151/154/155 | Seams OK, but the painter invented duplicate doors per chunk, crammed the floor and blocked exit paths | Flat footprints let the painter invent. Floor density kills readability. Doors need exit lanes |
| 5 | **Conductor error:** barrow_v2 coupled to the 2D arena and raced to KC2's P1(e) | R-C9-156 | Matt: "they should never have been connected in parallel. It is sequential improvement" | barrow_v2 is a **true 3D** world like v1, decoupled from kc2_play |
| 6 | True 3D, Tripo models placed (BX) | R-C9-156/158 | The models look good, but the coast was a heightfield and the scene empty at true scale. Model-sheet camera verified at 52.95° | Real models are the right foundation |
| 7 | SW section: coast from the model kit + v1-style paint-over, 28 chunks, projected (BS, separate project) | R-C9-158 | Better, but tile seams, plants painted (unlike v1), no life (wind, water), and Matt disliked the boat | Must be **inside v1's engine**; plants must be v1's 3D cards |
| 8 | SW section as a **level of the barrow_full project**, v1 camera (yaw 47) | R-C9-159 | v1 heather + wind, snow, footprints and moving water all work; seams small. **Still below v1**: blotchy model bakes, coarse half-density ground, a weak wreck, the footpath painted as a streak, a cramped cave view | See the handoff §4 |

Layout/rule assets that **survive** all of this:
- `barrow_v2/layout_v2.json` v6: anchors from the sealed pack, the organic floor, exit lanes, the clean-floor rule, `models[]` slots;
- `tools/validate_layout_v2.py` (R1–R13, 66/66 + negative control);
- doors sized to their monsters (R-C9-154).

## 4. Other rulings this session (one line each; verbatim in the ledger)

| Ruling | Summary |
|---|---|
| R-C9-135 | Matt's playtest order: warlord, sorceress, barbarian, then all three in a barrow arena |
| R-C9-136/137 | Lane reorder (w151–156 gaps first); REFERENT-v1 needs both alternates (slith, hellhound, gryphon) |
| R-C9-138/140/152 | Sorceress: staff aim and idle fixed; hood-hair morph superseded by option B (paused) |
| R-C9-139 | Character light toggle (b = cliffside match) |
| R-C9-141 | Warlord helm notch |
| R-C9-142 | Meteor always lands on the ground; objects get scorched |
| R-C9-143 | Meteor smoke approved; EoR re-ported from the right source |
| R-C9-146 | Red rims, later removed by 152 |
| R-C9-147 / 153 | barrow_v2 before the bosses / 100% barrow_v2 focus (the EoR overlay excepted) |
| R-C9-150 | Mixamo adoption |
| R-C9-157 | Finish the 5 placeholder families for the warlord playtest; sorceress fix stays paused |
| R-C9-160 | This record plus the handoff; barrow_v2 continues in a fresh session |

## 5. Housekeeping done

- **Disk:**
  - manifest 13 plus the EN-E2 intermediates were run (Oct 3; 406/407 entries; the read-only `harness_logs/s2c_rows12_2026-08-25b` was left alone deliberately);
  - **manifest 14 run by Matt** (Oct 6; 2,576/2,576 gone);
  - **manifest 14b is ready, not yet run** (1.94 GiB).

  Free space is about 34–37 GiB.
- **Pushes:**
  - collab pushed as work landed (JOIN-1 authorisation);
  - loadout pushed once (`d069c4b`, under R-C9-117).
- **Process lessons:**
  1. Subagents hit the account's weekly usage limit once (Oct 3→6). EN-E2 and EN-E3 resumed cleanly from their RESUME.md files. Keep RESUME notes current.
  2. On a shared tree, `ledger.json` commits carry other lanes' appends. Commit the ledger with `--only` from the conductor.
  3. Manifest commands must parse full paths. 10 entries in manifest 13 had spaces in them, which `awk $NF` mis-targets.
