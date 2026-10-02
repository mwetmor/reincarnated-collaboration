# Run C-9 Phase 2 — handoff to a fresh conductor session

**STATUS:** CURRENT (handoff) · **Authored:** 2026-10-02 by gandalf (RUN-CONDUCTOR, C-9 Phase 2), at Matt's request before a session reset and a temp-file purge.
**Supersedes for orientation:** the in-session context of conductor session `7b4d3123` (transcript retained at `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a.jsonl`).
**Durable record of truth (read these, not this summary, when they disagree):**
- `astra_test_01/burst/runs/C-9/ledger.json`: every ruling (R-C9-1..134, with Matt verbatim), 176 milestones and notes. Write it with python json, indent=2, ensure_ascii=False and a trailing `\n`.
- Charter: `agentic_orchestration/gandalf/notes/2026-09-26-illuminated-archive-run-C-9-charter.md`.
- Matt queues: `canonical/matt_decision_needed/README.md` and `canonical/matt_to_do/README.md`.

---

## 1. The goal of record (R-C9-132, Matt, 2026-10-01 night)

> "the goal for the night should be to get the 3 characters up and running in terms of animations and VFX needed to have all 3 characters run the crucible/arena. We also need to create our enemies for the crucible/arena with their animations and VFx."

The crucible/arena is **KC2-PLAY's Cathedral Arena**. It is a 2D Sprite2D runtime (`reincarnated-godot/kc2_play`), owned by the **KC2 drax** under the **Sim Session** (a separate gandalf session, the KC2-PLAY / JOIN-1 conductor). C-9 produces **JOIN-1 sprite-cell packs**; KC2 consumes them.

**Status:** all three heroes are DONE. 30 enemy packs exist. Matt opened the seal pipeline at oracle v3.11 (Sim Session), so the KC2 drax will now port the rules and wire PLAY with these packs, which means **deliveries are now being consumed.**

## 2. The contract every pack obeys

`reincarnated-godot/docs/join1-sprite-cell-contract-2026-09-29.md`:
- 768² cells, anchor (384, 448), ppm_render 151.337 (canvas ±2.54 m).
- 8 unique headings, never mirrored; one clean cycle per state; no baked durations.
- `release_index` must be an exact rendered sample.
- Pack roots are immutable once declared.
- KC2 applies the two-segment warp [0,r]/[r,N−1] so the visual release lands on the D2/GD tick.

Tooling lives in `runs/C-9/join1_render/`:
- `kits/*.json` and `manifests/*_clips.json`;
- `render_cells.gd` (supports `local_m` socket offsets and `h_model.crown_bone`);
- `index_cells.py`, `validate_sockets.py`, `j_runtime_resample.py` (takes `--out`);
- manifest lint with negative controls. **Known gap:** it checks release times on *casts* only, not attack contact frames; index_cells covers those.

**Big-creature size (open, KC2 drax's ruling, KC2 ledger KP-222):** creatures too big for the canvas are built **max-fit**, with a `true_size` block in the kit giving each roster record's factor. KC2 either accepts the downscale or scales the sprite at runtime by the factor. The void drone (1.22–2.44) shows the per-kit ppm ruling is required.

**Emerge UI (Sim Session, from footage):** p05 ambush bodies show their in-world health bar from the first spawn frame. Nothing in our packs assumed otherwise. We advised KC2 to anchor the bar to the record position, not the sprite top.

## 3. Hero packs (final)

| Hero | Kit of record | Pack | Cells | Notes |
|---|---|---|---|---|
| Barbarian | DUAL WIELD sword + axe (Q93/R-C9-133) on Mixamo Dual Weapon Combo; whirlwind = extended-arm two-blade spin (v7 rigid-spin recipe, e48/e52) | `join1_pack/d2-ww-barb-mx` | 984 PNG | chest socket moved Spine02→Spine (index 534a0202). ORIGINAL stance width (Matt preferred it; T12_12d −25% is parked) |
| Sorceress | battle-mage set + ONE-HANDED ORB-STAFF (~0.75 m, orb atop) + SHIELD, on Mixamo Pro Sword and Shield (R-C9-134) | `join1_pack_v3/d2-fire-sorc-bm` | 744 | height 1.7004 m (crown_bone head_end fix); releases re-measured |
| Dark knight / EoR warlord | two-handed MACE on Mixamo Great Sword clips; extended-arm EoR spin, RED tint (R-C9-127/130) | `join1_pack/gd-eor-warlord` | 856 | final_k_eor2. "The Mixamo animations for the dark knight are amazing." **Cape still not right**: spring-bone cape prototype is OPEN |

Older pack `join1_pack/d2-fire-sorc` is the pre-battle-mage sorceress, superseded by v3.

Movement: **class movement skills only**: no jump, strafe or universal roll (R-C9-129). The ported wwcr whirlwind effect goes on **2H carriers only** (R-C9-130).

## 4. Enemy packs (in `runs/C-9/join1_pack/`)

**Tier 1 (all built, painted):** en-acolyte-m, en-acolyte-f, en-wraith, en-revenant, en-brute, en-wretch, en-imp, en-golem, en-gaunt, en-icebrute (true_size), en-cryptmaw, en-ossuarycrab, en-cinderstalker, en-ossuarybloom, en-cryptgazer, en-rimethorn, en-blightsac, en-cryptglutton, en-voidlord (rylok #17, 2.60 m, emerge 3.467 s).
- Death swap f3f53e7f0: brute, icebrute and golem use clean de-rooted Pro Magic deaths.

**Tier 2 (referent line-up order, `legolas/research/2026-10-02-kc2-footage-reads/BUILD_PRIORITY.md`):**

| Pack | Roster record | State |
|---|---|---|
| en-voiddrone, en-voiddrone_boss | chthonianservitor (+boss grade) | done, 3.6 m max-fit, 4 legs a side; small front-leg kink remains in *impale* (slash fixed) |
| en-crawlerlarva | beetle_maggot01_maggotsummon | 0.9 m, **PROVISIONAL texture** (Tripo projection) |
| en-burrowworm | aetherialworm_b01..b04 | 2.8 m, emerge instead of crawl, **PROVISIONAL texture**; check the pale-green head-end bunch at emerge f20 |
| en-statue | possessedstatue | 2.05 m, 1.87 m two-handed spear (main_tip/main_grip), Great Sword set, painted |
| en-bonegolem | golembone_phase01 | 2.20 m, painted; the slam "stalk" is foreshortening, not stretch (measured) |
| en-warden | hero01 w159 final boss | 2.63 m true size, **PROVISIONAL texture** |
| en-magister | hero01 w160 vanguard nemesis | 2.54 m true size, **PROVISIONAL texture** |
| en-witch | heroine01 w156 (serves both witches) | 2.07 m, **PROVISIONAL texture**, green-spill despilled |
| en-mindtaker | heroine01 w155 | 1.80 m, free weight-transfer rig (en49) + bridge cut (en55), **PROVISIONAL texture** |

**Still to build:**
- woolly rhino: brief `EN3-FH` written and refs-guarded; the quadruped rig has horn-toss and charge clip types;
- the skeleton nemesis (skeleton_01a_b): free transfer from the revenant rig, then the bridge cut, then a stills check;
- fleshhulk;
- aetherialcolossus;
- aetherialwisp VFX for the w160 summons (unassigned).

Each new pack is reported to the Sim Session (it logs them in its KC2 ledger: KP-228 covers everything up to the four bosses).

## 5. Lanes (all drax subagents; all IDLE at handoff)

| Lane | Last agent id | Domain | Next work |
|---|---|---|---|
| EN-E2 | a824488f9315b726a | humanoid enemies, Tripo → Meshy/transfer rig → Mixamo clips → D7 paint | (1) paint passes on the 4 bosses, swapping in a calmer Pro Magic standing idle + walk for the Warden and Magister (the caster set's overhead arm reads wrong on plate); (2) skeleton nemesis sheet + transfer rig; (3) fleshhulk and colossus |
| EN-E3 | aa0b15bfaab4216ed | non-biped Blender rigs (n10 quadruped, n11 crab, n19 biped, n22 worm), n17 fit-to-canvas at 5% | (1) woolly rhino (fire EN3-FH); (2) paint passes on the larva and worm; (3) the worm emerge check |
| E1 | addec3162b35c27cd | dark knight / EoR | spring-bone cape prototype (deferred) |

A fresh session cannot SendMessage these ids (they belong to the old session). **Spawn new drax lanes** with a dispatch that points at this doc, the lane's own folder (`runs/C-9/en_e2/`, `en_e3/`, `wl_e1/`) and its spend ledgers.

## 6. Budgets and accounts (as of 2026-10-02 evening)

- **ChatGPT Astra (codex image CLI):** Matt used a reset, so it is back to a FULL weekly balance. The weekly limit was hit once this week. **Track Astra calls against the WEEKLY limit, not only per-lane caps.** Ledger images: 987 / 1500 (run cap).
- **Meshy:** account balance **1,927 credits**. The "30" was a conductor lane cap and can be raised; rigs cost 5 each, and the lane guard reserves 10 per call (keep the guard).
- **fal:** per-lane ledgers sum to roughly $19 for the whole run; Matt topped up $25 on 10-01. Remaining work needs about $2–3 (Tripo $0.40 per build). Per-lane ledgers: `runs/C-9/*/fal_spend_*.json`.
- **Disk gate 20 GiB** (R-C9-88). At handoff the disk was ~18 GiB, partly a macOS update being prepared (~3.9 GB visible plus a "prepare update" snapshot). Cleanup manifest 13 is staged (§8).

## 7. Open items for Matt

- **Loadout Vercel push:** loadout is `ahead 1` with 3f1ee3e (it includes 34298c1). It carries crater v5 (`?v5=ab`), the dark knight final_k_eor2 + EoR + eyes, the sorceress robe and props, and Meteor smoke as light puffs. It was held for the Vercel Hobby rate-limit window (opened ~02:07Z Oct 3). Push with `git -C ~/Games/reincarnated-loadout push origin main` (R-C9-117 authorizes loadout playtest pushes), check once (no polling: the firewall challenges it), then send Matt the select-page link. Glance auto-deploys are disabled (`glance/app/vercel.json` git.deploymentEnabled=false).
- **Decisions still open:**
  - the EoR tint (red vs original);
  - the new Meteor smoke look;
  - keep the clock-hour telegraph ring?
  - make the collab/loadout repos private (offered);
  - the Creature/Zombie Mixamo packs (not downloaded);
  - mount the footage share (blocks the KC2 re-wire);
  - the Pi's SMB drive is broken (the telemetry move failed twice).
- **Telemetry DB:** archived, nothing outstanding. The zst and raw copies are on the PC at `C:\Users\mhwet\reincarnated-archive\2026-10-01\`, the Mac copy at `~/Games/_telemetry_archive/`, and the Mac original was removed.
- **Parked:**
  - barbarian Mixamo stage 2 (axe + shield; needs the sparse repair of s2/work/v0.glb);
  - T12_12d stance narrowing;
  - a possible Mixamo idle for the barbarian (Matt considering it).

## 8. Cleanup manifests

- 10 and 12: run, done.
- **13** (`runs/C-9/cleanup/manifest_scratch_prune_13.txt`, 335 entries, ~15.9 GiB) covers two things:
  - (a) the old conductor session's scratchpad (`/private/tmp/claude-501/…/7b4d3123…/scratchpad/*`, 11.1 GiB);
  - (b) untracked reincarnated-godot `harness_logs/*` and `tmp/*` older than 3 days (4.8 GiB). The Sim Session OK'd (b), and anything under `tmp/kc2/` from the last 3 days stays.

  Run it with:
  ```
  awk '{print $NF}' ~/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/cleanup/manifest_scratch_prune_13.txt | tr '\n' '\0' | xargs -0 rm -rf
  ```
  Before deleting, the small things worth keeping from the scratchpad were copied into `agentic_orchestration/gandalf/notes/2026-10-02-c9-handoff-kit/` (the Morning Look template and the web-build script).
- The Sim Session's own temp folder (~16 GB) has its own script, handed to Matt.
- The older run folders C-3..C-8 (~20 GiB untracked) are **heavily referenced** by later provenance (tens of thousands of path references), so do not bulk-delete them without a reference audit.

## 9. Standing constraints (unchanged; violating any is a defect)

- **Keys:** never print an API key; load them with `source ~/.zshrc >/dev/null 2>&1`.
- **Prompts and names:** no franchise, studio, character, item or artist names in prompts, briefs or filenames (refs_guard enforces it).
- **Permissions:**
  - never work around a permission denial, and never launder one through another agent or session;
  - Matt runs deletions, or explicitly says "run manifest N";
  - installs into cliffside3d only on Matt's word.
- **Git:**
  - `git commit --only <paths>`;
  - `git status --porcelain -- <paths>` before and `git show --stat HEAD` after;
  - `git -C <repo>` for anything cross-repo;
  - never `git add -A`;
  - never commit raw Mixamo FBX (retargeted GLBs are ignored in collab, and `animations/mixamo/` is ignored in godot).
- **Pushes:** collab, engine and godot are push-as-work-lands under JOIN-1 (R-C9-84); the godot pushes are released by the Sim Session conductor. Loadout pushes deploy the playtest (R-C9-117), so mind the Vercel quota. Demo is a fresh ask.
- **Heavy work:** the heavy lock for Blender and Godot (`runs/C-7/conductor_scripts/heavy_lock.py C-9 -- <cmd>`); disk gate 20 GiB; no uncompressed frame dumps.
- **Cleanup lists:** confirm with the active lanes (and the Sim Session for godot) before writing one.
- **Mixamo:** Matt's own Adobe account; packs live in `reincarnated-godot/animations/mixamo/`. Downloaded so far: Great Sword, Pro Sword and Shield, Pro Melee Axe, Pro Magic, Action Adventure, Gestures Basic, Dual Weapon Combo. Nothing for staff, wand or book exists in the library.

## 10. Where Matt tests

The Vercel select page (barbarian / sorceress / dark knight, with overnight variants as query flags) on his phone. Morning Look artifact: https://claude.ai/artifact/8xCjr9N6A2sKHq8o1YvhrP.

---

## 11. Fresh-session prompt (paste into a new session)

```
You are gandalf, RUN-CONDUCTOR for Run C-9 Phase 2 (Reincarnated). Read your operating
procedure skill (reincarnated-gandalf-operating-procedure) and run its session-start
protocol, then read, in order:
  1. agentic_orchestration/gandalf/notes/2026-10-02-c9-phase2-handoff.md  (this handoff)
  2. astra_test_01/burst/runs/C-9/ledger.json  (rulings R-C9-120..134 at minimum)
  3. agentic_orchestration/legolas/research/2026-10-02-kc2-footage-reads/BUILD_PRIORITY.md
Then:
  a. Check disk (gate 20 GiB). If cleanup manifest 13 has not been run, ask me.
  b. If the loadout repo is still ahead of origin, push it (R-C9-117), check the
     deploy once, and send me the select-page link.
  c. Spawn two drax lanes per handoff §5 — EN-E2 (boss paint passes with calmer
     Warden/Magister idle+walk, skeleton nemesis via transfer rig, fleshhulk, colossus)
     and EN-E3 (woolly rhino from brief EN3-FH, larva/worm paint passes, worm emerge
     check). Give each the budgets in handoff §6 and the constraints in §9.
  d. Report each new pack to the Sim Session (peer gandalf session) with cells,
     height, true_size factors and release times.
Conduct; don't build. Keep me posted briefly.
```
