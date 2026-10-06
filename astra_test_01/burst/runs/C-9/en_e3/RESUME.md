# EN-E3 — resume point (paused under R-C9-147, 2026-10-03 ~01:50Z)

Paused by the conductor (barrow_v2 moved ahead). **No Astra paint bursts until the conductor says the weekly allowance is free again.**
Disk rule on resume: HALT if `df -k /System/Volumes/Data` < 21 GiB. Lane allotment 1.2 GiB of new output from the resume
baseline (en_e3 1,938,732 KiB at 01:20Z); used so far: en_e3 +231 MiB, packs +147 MiB = ~0.37 GiB.
All heavy work goes through `runs/C-7/conductor_scripts/heavy_lock.py C-9 -- <cmd>`. EN3_TMP = this session's scratchpad
(any writable dir works; n05 only puts its temp frames there).

## Done (do not redo)
- **en-woollyrhino** (frosthorn, rhino_h02): pack `join1_pack/en-woollyrhino`, 72/72 cells, 960 PNG, true_size factor 1.29
  (base 3.1 m, designed 4.0 m). Kit `join1_render/kits/en-woollyrhino.json`. Chain `work/chain_fh_e.sh`.
- **en-crawlerlarva_p**: pack `join1_pack/en-crawlerlarva_p`, 32/32 cells, 416 PNG, true_size factor 1.0. Supersedes
  `join1_pack/en-crawlerlarva` (index sha 567115366c21, pinned in the kit).

- **en-abomination** (rift horror, kc_bounty13): pack `join1_pack/en-abomination`, 72/72, true_size factor 1.2 (base 2.0 m). Chain `work/chain_rh_c.sh`. DONE 2026-10-03 (abomination-only resume).

- **en-burrowworm_p**: DONE 2026-10-03 (R-C9-157), 32/32, commit 7285a3cea.
- **en-hellhound** (rime wolf): DONE 2026-10-06, 64/64, factor 1.047; chain `work/chain_rw_e.sh` (RW_VAR=a). Open: the left-foreleg brass band barely reads at 1x.

## Next: nothing queued in this lane (all R-C9-157 items landed). Older notes below are historical.
1. **en-burrowworm_p** — everything up to the kit is done (`export/worm_p/worm.glb` with the n22 emerge fix and the
   painted `work/tex_worm_PG.png`; kit + manifest written; the kit's `supersedes` pins `join1_pack/en-burrowworm`
   index sha 08bdc4fc4d13). Remaining: the Godot cell render + index_cells + validate_sockets + j_runtime_resample +
   48 lint + stills/film — run the worm half of `work/chain_pz_d.sh` from its `gate`/`mkdir -p $C9/join1_pack/$K` line
   (K=en-burrowworm_p, N=worm), then its final step: the E-heading "after" emerge strip
   `work/strip_worm_emerge_E_after.png` -> copy to `artifacts/`.
2. ~~Abomination~~ DONE above. (Old notes: **Abomination (rifthorror, kc_bounty13 -> pack en-abomination)** — arm check done (W/S strips `work/strip_rh_v1_{W,S}.png`:
   both arms rise in the impale windup and drive down at f45; accepted). Built at 2.0 m (`builds/rifthorror_prep20.glb`,
   rig v2 n17 s_with_margin 1.013). Paint canvas ready: `work/canvas_rifthorror_G.png` + `work/layout_rifthorror_G.json`.
   Remaining: **(Astra, needs the conductor's go)** `EN3_BODY="a hunched many-limbed two-legged horror" python3 scripts/n07_paint_brief.py
   rifthorror rifthorror_G work/canvas_rifthorror_G.png EN3-RHPG <artifacts/EN3-RH/EN3-RH_a_r1.png> "<look words from the n01 entry>"
   "THE MARKER: ... LEFT great arm ..."`, refs_guard, fire; then a chain like `work/chain_fh_e.sh` with: 06a/06b/n08 on
   `builds/rifthorror_prep20.glb`, export with **scripts/n24_rig_horror.py**, VFX already generated (`export/rifthorror_vfx`),
   a `work/mk_states_rifthorror.py` (sockets: spike tips = arm_L_3/arm_R_3 tips for impale/swipe, maw for drain, chest for
   the rift cast), kit true_size: records kc_bounty13 + chthonianmonstrosity_h01, scale 1.0, designed 2.4 m, base 2.0 m,
   factor 1.2.
3. **Hellhound (rimewolf, direwolf_frozenwastes_01 -> pack en-hellhound)** — rig v1 built at 4.4 m
   (`builds/rimewolf_rig_v1.glb`), n17 s_with_margin 0.963 (binding attack_snap f11) -> rebuild prep at **4.2 m**, then
   the paint canvas. **(Astra)** paint brief EN3-RWPG with the marker line forcing the brass band onto the **LEFT
   foreleg only** (the sheet b_r1 put one on the near right foreleg in the right profile). Kit true_size: record scale 1.5,
   designed length 4.4 m (nose to tail tip at sheet scale) — verify the base length from n04 before writing the factor.
   VFX generated (`export/rimewolf_vfx`). Release sockets: maw for bite/snap/breath.

## Known gap (unchanged)
48_manifest_lint checks release times on casts only: the attack negative control passes (exit 0) on every attack-only
creature; index_cells covers attack contact frames. Rhino adds a cast negative control (`_neg_release_cast_frosthorn.json`,
exit 1 = caught).

## Cleanup candidates for Matt (lane-superseded; ~0.3 GiB)
builds/frosthorn_rig_v1-3.glb, frosthorn_prep.glb, frosthorn_prep_c.glb, frosthorn_prep32.glb, frosthorn_prep32_c.glb,
worm_rig_fix1.glb, rifthorror_rig_v1.glb, rifthorror_prep.glb, and the older maw/crab/gazer/raptor/rimethorn rig versions.
