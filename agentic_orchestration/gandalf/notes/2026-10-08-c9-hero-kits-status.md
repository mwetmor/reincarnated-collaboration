# C-9 hero kits: Fire Sorceress (battle mage) and Barbarian — status for the Sim Session

**STATUS:** CURRENT. **Authored:** 2026-10-08 by gandalf (C-9 RUN-CONDUCTOR), answering Matt's question relayed by the Sim Session (JOIN-1 conductor). The source is a read-only sweep of C-9's records; every claim below cites a file. `R` = `astra_test_01/burst/runs/C-9`.

**Headline.** C-9 owns the hero kits' **look**: the sprite-cell packs, animation clips, release times and Barrow VFX. C-9 does **not** own the gameplay numbers. **Both hero packs are DRAFT; neither is declared COMPLETE.** Every C-9 timing was **measured off the animation clips**; none was read from a game data table. D2 gameplay numbers reached C-9 only via the Sim Session's timing packets, quoted in the ledger. No D2 table file exists under C-9.

## 1. What C-9 has

### Fire Sorceress, battle mage — `d2-fire-sorc-bm`, v6 (R-C9-237)
- **Kit and manifest:** `R/join1_render/kits/d2-fire-sorc-bm_v6.json`, `R/join1_render/manifests/d2-fire-sorc-bm_v6_clips.json`.
- **Pack:** `R/join1_pack_v6/d2-fire-sorc-bm/`, 64/64 cells, 744 frames, **DRAFT**.
- **Clips (s):**
  - idle 2.3333; walk 1.1; run 0.7;
  - cast_fireball_m 1.0333 (12 frames);
  - cast_meteor 2.9667 (16 frames);
  - block 0.6 (5 frames);
  - hit 0.7; death 2.3.
  - The cast clips come from Mixamo Pro Sword and Shield (R-C9-134).
- **Releases:**
  - Fire Ball 0.2667 s (frame r=3) and Meteor 1.80 s (r=9), measured by the orb-tip trace (`R/so_mx/work/r152_release_tip_ss152b.json`);
  - the release socket is `main_tip` (weapon_r −0.5689 m, orb radius 0.09 m);
  - block raise 0.18 s, lower 0.20 s.
- **Locomotion:** walk 1.368 m/s and run 3.646 m/s, both foot-lock measurements. Model height 1.6995 m.
- **Barrow VFX** (`R/barrow_full/godot/scripts/`):
  - **Fire Ball:** `fire_ball_fx.gd`, from the C-7 kit `fire_bolt_e1_B`. 1510 px/s ≈ 15.0 m/s, range ≈ 5.17 m, impact at tick 18 of 60. Burst condensed to 0.75 (`?fb=c75`); Matt called it "perfect" (R-C9-118).
  - **Meteor:** `meteor_fx.gd` / `meteor_a_fx.gd`, default "mix4". The fall is 0.82 s, set by eye; `?fall=2.4` shows the packet value.
  - **Crater:** `crater_v4_fx.gd`, 12.6 s from the packet formula.
  - **Object scorch:** `scorch_fx.gd`, radius 2.2 m.
- **Gameplay damage radius:** **none exists in C-9.** R-C9-110 asked for it to be matched to the visual; it was never set.
- **Stale text, flagged:**
  - The prose in `R/barrow_full/godot/data/slots/so_bm134.json` and `spell_fx.gd` still quotes the old releases (0.1333 / 1.6667).
  - `spell_fx.gd` is a placeholder.

### Barbarian, dual-wield kit of record — `d2-ww-barb-mx` (R-C9-133)
- **Kit and manifest:** `R/join1_render/kits/d2-ww-barb-mx.json`, `R/join1_render/manifests/d2-ww-barb-mx_clips.json`.
- **Source:** `R/bm_mx/s3/export/bm_join_mx_manifest.json`, from Mixamo Pro Melee Axe plus Dual Weapon Combo.
- **Pack:** `R/join1_pack/d2-ww-barb-mx/`, 80/80 cells, **DRAFT**. (The 10-02 handoff calls it "final"; the index does not.)
- **Clips (s):**
  - idle 1.8; walk 1.3333; run 0.7333;
  - attack 2.4 (release 0.9333, the sword);
  - combo 3.6333 (axe release 0.7333, second strike 1.1);
  - shout / Battle Orders 2.8333 (release 1.2667);
  - whirlwind_dual start 0.2 s, and a loop of 0.2667 s at 3.75 rev/s;
  - hit 1.4667; death 2.3.
- **Sockets:** sword tip 0.7768 m, axe tip 0.8089 m. Walk 0.955 m/s and run 2.148 m/s (foot-lock).
- **Whirlwind VFX:**
  - **Not live for the barbarian.** The Barrow binds `whirlwind_channel.gd` to the warlord only (`barrow_full.gd:1454`).
  - The two-ribbon dual variant (R-C9-133) is not wired.
  - The only barbarian artifact is a parameter dump for kc2_play: `R/barrow_full/take/build/whirlwind_params_barbarian_dual.json` (R_ENGAGE 3.527 m, spin-up 0.7 s, spin-down 0.8 s, clip omega 1350°/s), marked for a re-dump.
- **Open:** the normal attack is a gap (R-C9-111), and its candidate is not shipped.
- **Older kit:** `d2-ww-barb` (`R/nb_join/`, `R/join1_pack_draft/`) is DRAFT and superseded by `-mx`.

## 2. Where the numbers come from
- **Clip lengths, releases, strides, sockets:** measured from the GLBs with C-9 instruments. No game table was used.
- **"Skills.txt Id 47/56/149/151" in the kits:** labels only.
- **D2 version of record:** the JOIN-1 charter (`agentic_orchestration/gandalf/notes/2026-09-29-join-1-run-charter.md`, J-S3/J-S3b) gives "D2 1.13 classic, `fabd/diablo2 @ 45112569…`, datamined". The tables are at `agentic_orchestration/research/datamine-acquisition/d2/raw/`.
- **Timing packets** (Sim Session, legolas):
  - `agentic_orchestration/legolas/research/2026-10-01-join1-d2-animation-timing/` (collab `b0f9d77fa`);
  - J4a `…/2026-10-01-join1-j4a-d2-ww-barb/` (`d865df7d5`);
  - J4b `…/2026-10-01-join1-j4b-d2-fire-sorc/` (`4eda5de34`).
- **As quoted in C-9's ledger:**
  - Barbarian (N-C9-ENDGAME-GEAR): IAS 35% each weapon, FCR 0; shout 13 ticks, release tick 9; Whirlwind 4-tick interval; A1 16 frames / 15 ticks, hit on tick 7.
  - Sorceress: FCR 105 → 8 ticks (0.32 s), action tick 5, **final** (R-C9-118). Meteor impact +2.4 s, fixed. Fire field 12.6 s at level 20.
  - R-C9-111/116 carry earlier, superseded values.
- **C-9's use of the packets:** look-only. There is one retime tool (`R/nb_join/scripts/j_law_retime.py`, 25 ticks/s, two-segment warp), plus the crater life and `?fall=2.4`.
- **Authored VFX constants:** inherited from the source kits (C-7 Fire Bolt, `wwcr_whirlwind.gd`). The Meteor lane-B constants (ROCK_R, RING_R, BURN_R, AHEAD) have no recorded source.

## 3. What C-9 still plans, and what belongs to the Sim Session
- **Sim Session / JOIN-1** (KC2 drax, R-C9-135) owns the gameplay side:
  - J4a/J4b kit oracles and the D2 adapter (legolas → gamora → star-lord → drax);
  - the two-segment warp landing each visual release on its D2 tick;
  - damage radii, projectile speeds, delays and cast rates;
  - the B0-N grading gate;
  - the J3→J4 owner-eye checkpoint with Matt.
- **The 10-06 handoff:** "C-9 owes nothing there right now."
- **C-9's open items for these kits:**
  1. Declare the packs COMPLETE when JOIN-1 wires them. The sorceress v6 is the J4b target (KP-362).
  2. The barbarian's normal attack.
  3. The barbarian two-ribbon Whirlwind VFX plus a parameter re-dump.
  4. A gameplay radius matched to each spell's visual, **given numbers from J4**.
  5. The release-lint gap: it covers casts only.
  6. Clean up the stale release prose.
- **Needed from the Sim Session:** the J4a/J4b gameplay numbers once fixed (radii, speeds, cast and attack rates), so C-9 can match visuals to them, and a decision on whether her shield block is in (it is excluded under Q95; the pack has it).

## 4. Read first
- `R/so_mx/RESUME.md`;
- the two kit JSONs and their `_clips` manifests;
- `R/bm_mx/s3/export/bm_join_mx_manifest.json`;
- the VFX scripts named above;
- ledger N-C9-JOIN1-CONTRACT, N-C9-ENDGAME-GEAR, and R-C9-89/90/93/95/101/110/111/116/118/130/133/134/135/142/143;
- `reincarnated-godot/docs/join1-sprite-cell-contract-2026-09-29.md`.
