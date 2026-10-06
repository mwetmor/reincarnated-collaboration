# Run C-9 Phase 2: handoff to a fresh session, focus barrow_v2

**STATUS:** CURRENT (handoff). **Authored:** 2026-10-06 by gandalf (RUN-CONDUCTOR, session aab928), at Matt's request (R-C9-160).

**Supersedes for orientation:**
- `2026-10-02-c9-phase2-handoff.md` (§2 contract, §9 constraints and §10 still apply; read those sections);
- `2026-10-06-c9-phase2-state.md`.

**Read with:** `2026-10-06-c9-phase2-session-record.md`, which records what this session did and the eight barrow_v2 attempts.

**Truth of record:** `astra_test_01/burst/runs/C-9/ledger.json`, rulings through **R-C9-160**. The ledger wins over this note.

---

## 1. Where things stand

- **Playtest 1 is done.** Matt played the dressed **warlord** build in the KC2 2D arena (REFERENT-v1 sealed r2, KC2 KP-302). Every w151–160 enemy family has a JOIN-1 pack. The sorceress and barbarian arena turns are **KC2's** next work (J2–J4 kit oracles, per the Sim Session). C-9 owes nothing there right now.
- **barrow_v2 is THE focus of the next session.** Matt's goal (R-C9-156): *"play the arena … in the barrow_v2 as we imagined in the painting but in true 3D like the barrow v1"*. The order is sequential:
  1. build barrow_v2 to **v1's quality** in v1's engine;
  2. later, a joint job with KC2: the fight sim runs inside it with 3D enemies (we have every enemy as a GLB).
- **Matt's latest verdict (R-C9-160):** the R-C9-159 SW section *"still isn't up to the same standards as barrow_v1."* He wants a fresh perspective.

## 2. The look and the rules (fixed; don't relitigate)

- **Look of record:**
  - **sketch A**, `barrow_v2/sites/BV3r2-A.png` (Fjord Headland), plus sketch B's stream from the barrow into the mere;
  - the spawn plan `barrow_v2/sites/BV3r2-A_spawns.png`.
- **Quality bar:** **barrow v1**, the live Barrow page and `runs/C-9/barrow_full/`. Matt on v1: *"Hard to believe it is real 3D."*
- **Layout and rules of record:** `barrow_v2/layout_v2.json` **v6**, with `tools/validate_layout_v2.py` R1–R13 at 66/66 and a negative control. It contains:
  - the six spawn anchors from the sealed pack;
  - the organic walkable floor (it contains every 8 m spawn disc, keeps open lines to (0,0), and has no interior blockers);
  - exit lanes from each door to its disc;
  - the clean-floor rule;
  - `models[]` slots.
- **Doors sized to their monsters (R-C9-154):** barrow door ≥ 5 × 6.5 m, hall great door ≥ 4.5 × 4.5 m, sea cave ~7 × 9 m with a ~5 m stair.
- **v1's engine and camera (R-C9-159):** barrow_v2 is a **level inside `runs/C-9/barrow_full/godot/`**, camera pitch 52.95354°, **yaw 47°**. It inherits v1's systems:
  - `barrow_heather.gd` heather cards with gust wind;
  - `snow_field.gd` footprints;
  - snowfall and gusts;
  - two-sun painted light;
  - the pen/ink and paper post pass;
  - crater v5 surfaces.
- **Plants are v1's 3D cards, never painted-only. Water moves.**
- **The wreck follows sketch A:** heeled, half-sunk in the shore ice, broken ribs, a dragon prow, a snapped mast.

## 3. What exists now (the R-C9-159 SW section, the latest attempt)

- **Level:** `barrow_full/godot/scenes/barrow_v2_sw.tscn` with `scripts/barrow_v2_sw.gd`, which extends `barrow_full.gd`. Data: `barrow_full/godot/data/barrow_v2_sw/`.
- **Pipeline, scripts and re-run steps:** `barrow_v2/SECTION_RESUME.md` (lane BS):
  - build: `tools/section_sw_build.py`, then `v2sw_prep.py`;
  - runner: `barrow_full/godot/tools/v2sw_run.gd -- guide|lit|stills|v1stills|film`;
  - ground paint: `v2sw_paintcfg.py`, `v2sw_drive.sh`, `v2sw_stitch.py`;
  - model bakes: `v2sw_model_bake.py`.
- **What it shows:** `barrow_v2/section_v1cam/look/R-C9-159_*` (sketch A | v2 | v1 sheets; a 65 s walk film).
- **Models:** the Tripo builds are in `barrow_v2/models/builds/`, reduced and normalised in `barrow_v2/godot/models/build/`. They are the hall, porch, gable, barrow, wreck (v1, disliked), wreck2 (R-C9-159), cavecliff, staircliff, cliffplain and crag. The v1 reuse kit is in `barrow_full/web_painted/models/barrow/`.
- **What works:** v1's heather and wind, snowfall, footprints, animated water and bobbing floes, and small ground seams (2–6/255).
- **What fails Matt's bar:**
  - blotchy, cellular-looking model and rock bakes;
  - the ground painted at **half** density, so it's coarse;
  - the wreck reads as a pale tub from above;
  - the worn footpath painted as a dark streak;
  - the cave/stair view cramped by v1's 19 × 13 m window;
  - the west lagoon (−1.3 m) behind a spit, a two-water-level liberty that still needs Matt's ruling.

## 4. Fresh-perspective notes from the conductor (hypotheses, not rulings)

**The conductor's own errors to avoid:**
1. Coupling barrow_v2 to the 2D arena (R-C9-156).
2. Inventing a new pipeline each round instead of **replicating v1 literally**.

v1 = a greybox render with real models → **ONE paint-over of the WHOLE scene, ground AND models together**, at **full plate density (100.6 px/m)**, in **16 chunks of 1344 × 832** over 53 × 41 m → the **take**: 54 plates **cut by geometry from that same painting**, worn by projection or baked onto each model's UVs, **unlit** ("the painting is the world's light") → tuft density masks from the painting drive v1's 3D heather → pen and paper post.

The R-C9-159 attempt departed from v1 in ways that plausibly explain its look:

| v1 | R-C9-159 | Likely effect |
|---|---|---|
| Models and ground painted **in one painting**, same hand and same light | Ground painted separately; each model painted on its own from a 4-view sheet | Mismatched hands and blotchy bakes |
| Bakes **unlit**, the painting is the light | Bakes **lit by v1's ramp** (a deviation, for rotated instances) | Double shading, muddy and cellular |
| **Full** plate density, chunk 1344 × 832 | **Half** density, 8 big tiles of 2816 × 3328 | Coarse grain; less painter detail per metre |
| Heather placement **derived from the painting's tuft masks** | Heather placed by the layout's density map | Plants that don't sit in the painted ground |

**Recommended first move for the fresh session (cheap and diagnostic):**
1. A **v1-vs-v2 forensic**: measure texel density, palette, lighting terms and shader settings of v1's ground and plates against R-C9-159's at the same camera.
2. Then re-run the **same SW corner with v1's pipeline replicated exactly**, deviation by deviation, with no new inventions. Use rotated-instance-safe bakes only if v1's projection can't cover a case, and state why.

Judge it against a v1 still at the same zoom before scaling up. barrow_v2 is about 3× v1's area, so plan about 48 v1-size chunks for the whole site, with neighbour context and a single low-res master for colour consistency (this part did help seams).

**Open questions for Matt** (ask early, one recommendation each):
- **Water level:** a lagoon (two levels), or one sea with the wreck up on the beach?
- **The wreck:** approve a sketch-A wreck built **as a model designed to read from 52.95° above** (deck, ribs and prow visible from the top), not a side-view hull.
- **Scale and composition:** v1's window shows 19 × 13 m. Should the cave, stair and wreck views be composed for that window (moving or turning the cave face) rather than for the whole-site sketch?

## 5. Other open items (not barrow_v2; each awaits Matt's go)

1. **Sorceress hood fix, option B** (R-C9-152; stills in `so_mx/look/R-C9-152_*`). Matt said "Not now". When resumed (lane notes in `so_mx/RESUME.md`):
   - rebuild the Barrow web page with `PIN_SHA=b4de84e65 PIN_PATHS="scripts/eor_kc2_fx.gd scripts/whirlwind_channel.gd" bash barrow_full/tools/build_web_painted.sh`, which also ships the R-C9-152 EoR smoke and the `eorsmoke` row;
   - make one loadout commit and push (R-C9-117);
   - render the JOIN-1 sorceress v5 pack. **First delete the empty `join1_pack_v5/d2-fire-sorc-bm/`.**
2. **Mixamo remainder** (R-C9-150): wretch and revenant zombie clips, and "stand up" as an emerge.
3. **Hellhound** left-foreleg brass band barely reads (an optional repaint).
4. **Cleanup:**
   - run **manifest 14b** (1.94 GiB; the command is in `cleanup/manifest_14_report.md`);
   - manifest 15 (godot receipt dirs with 6.5 GiB untracked, weak old-run candidates) waits for a calm audit with the Sim Session.
   - Disk is about 34–37 GiB free; the gate is 20.
5. **Lint gap:** the manifest lint checks cast releases only; index_cells covers attack contact frames.

## 6. Interfaces, budgets, constraints

- **KC2 / the Sim Session** (peer gandalf session "Sim Session"): it owns kc2_play and the oracle. barrow_v2 is **decoupled** (nothing for it on KC2's list). The joint "KC2 sim inside 3D barrow_v2" is a later scoping talk.
- **Budgets:**
  - Astra: weekly allowance; Matt says there is plenty, and the run ledger shows `images_used` 1251.
  - Meshy: about 1,900 credits, keeping the 10-credit guard.
  - fal: per-lane ledgers; Tripo is about $0.40 per build.
- **Constraints** (the 10-02 handoff §9, unchanged):
  - keys via `source ~/.zshrc`, never printed;
  - no franchise, studio or artist names in prompts or filenames (refs_guard);
  - **Matt runs deletions**;
  - never work around a permission denial;
  - `git commit --only`, `git status --porcelain` before, `git show --stat HEAD` after, `git -C` for cross-repo;
  - collab/engine/godot pushes are push-as-lands (JOIN-1); loadout pushes deploy Vercel (R-C9-117), so push once and check once;
  - heavy lock `runs/C-7/conductor_scripts/heavy_lock.py C-9 -- <cmd>`;
  - disk gate 20 GiB (lanes halt at 21);
  - commit the ledger from the conductor, because lane commits sweep in other appends.
- **Lanes:** all idle. Subagent ids from session aab928 can't be messaged from a new session; spawn fresh drax lanes pointing at the RESUME files.

## 7. Fresh-session prompt (paste into a new session)

```
You are gandalf, RUN-CONDUCTOR for Run C-9 Phase 2 (Reincarnated), focus: barrow_v2.
Read your operating procedure skill (reincarnated-gandalf-operating-procedure) and run its
session-start protocol, then read, in order:
  1. agentic_orchestration/gandalf/notes/2026-10-06-c9-phase2-session2-handoff.md (this handoff)
  2. agentic_orchestration/gandalf/notes/2026-10-06-c9-phase2-session-record.md (what was tried, §3)
  3. astra_test_01/burst/runs/C-9/ledger.json, rulings R-C9-144..160
  4. astra_test_01/burst/runs/C-9/barrow_v2/SECTION_RESUME.md
Look at sketch A (barrow_v2/sites/BV3r2-A.png), the latest attempt
(barrow_v2/section_v1cam/look/R-C9-159_*), and the v1 Barrow (barrow_full; live page) before
proposing anything. Goal: barrow_v2 in true 3D at barrow v1's quality, as a level of the
barrow_full project. Start with the v1-vs-v2 forensic in handoff §4, then propose ONE plan to
me with one recommendation per open question. Conduct; don't build. Keep me posted briefly.
```
