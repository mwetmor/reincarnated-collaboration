# EN-E2 — RESUME point

**UPDATE 2026-10-03 (R-C9-157): the three packs below are DONE** -- en-vigillord 36ec21b24, en-fleshhulk 90ddfdd61 (Mixamo mutant set, max-fit 2.10 m), en-colossus f2726ef91 (mutant set + roar, max-fit 2.50 m). The "Next" list is closed; nothing is in flight. Superseded scratch for Matt: `runs/C-9/cleanup/manifest_en_e2_p2_superseded_scratch.txt`.

## History: paused under R-C9-147, 2026-10-03 ~02:10Z

Paused by the conductor: Matt moved barrow_v2 ahead of the remaining bosses. Resume after the barrow_v2 paint lands.

## Done, committed (collab, `--only`, not pushed)

| Commit | What |
|---|---|
| 3ebb1cc6b | Boss paint passes: `join1_pack/en-warden_p`, `en-magister_p`, `en-witch_p`, `en-mindtaker_p` (56/56 each; supersede the provisional roots) |
| bf5091beb | Five new bodies built through paint, clips, final export, true_size, kits (cells not rendered then) |
| 2483996e9 | `join1_pack/en-fleshshaper` (w152), 56/56, 2.30 m, margin 16.8 %; cast_bolt r=4 0.800 s, cast_area r=9 1.800 s |
| a59eebce3 | `join1_pack/en-ascended` (w154), 56/56, 2.40 m, margin 12.2 %; cast_bolt r=3 0.5333 s, cast_area r=6 1.2667 s |

## Next (in this order; each is ONE command, then commit)

The kits and manifests already exist in `join1_render/kits/` and `join1_render/manifests/`. Each pack is rendered and validated by
`scripts/en58_pack.sh` and committed + ledgered by `scripts/en59_commit_pack.sh`. Run from `runs/C-9/en_e2/`; check `df -h /System/Volumes/Data` first (HALT below 21 GiB).

1. **en-vigillord** (w160 skeleton nemesis, letter x, 2.15 m, free-transfer rig + bridge cut already applied):
   `zsh scripts/en58_pack.sh x en-vigillord en_x_pale idle,walk,run,cast_bolt,cast_area,hit,death "cast_bolt=bolt:12:3.5,cast_area=area:3.0" idle,walk,cast_bolt,death "en-vigillord (w160 nemesis, PAINTED): idle / walk / cast_bolt release / death end"`
2. **en-fleshhulk** (w159, letter d, built at 3.00 m designed): render with
   `zsh scripts/en58_pack.sh d en-fleshhulk en_d_aether idle,walk,run,slam,attack,lob,hit,death "slam=area:4.5,attack=slash,lob=bolt:12:3.0" idle,walk,slam,death "en-fleshhulk (w159, PAINTED): idle / walk / slam / death end"`,
   then MAX-FIT: read `fit x` from the FIT line; if the margin is under 5 % (or the fit factor is < 1), re-run
   `zsh scripts/en10_final.sh d <3.00 x fit, rounded down to 0.05> work/d_tex_final.png`, then `en34_tips.py`, `en46_true_size.py d fleshhulk_unarmed 3.00 fleshhulk_mine`,
   write `work/d_size_call.json` (`designed_height_m` 3.00, `shipped_height_m`, `factor`, `why`), `python3 scripts/en33_kit_r4.py d`, and re-render.
   **The re-render must go to a NEW pack root** (e.g. `en-fleshhulk_f`) if the first root was ever reported; otherwise render to the same root before reporting it.
3. **en-colossus** (w160, letter e, built at 3.20 m designed): the same as 2 with
   `en_e_aether idle,walk,run,lob,attack,slam,roar,hit,death "lob=bolt:12:2.5,attack=slash,slam=area:4.0,roar=aura" idle,walk,lob,death`,
   and `en46_true_size.py e aetherialcolossus 3.20 galakros`.

Lane commit per pack: `zsh scripts/en59_commit_pack.sh <g> <kit> "<subject>" "<note>"` (it runs `git status --porcelain` before and `git show --stat HEAD` after, commits JSON/text only, and appends the ledger milestone).

## Budgets at pause

| Account | Lane used | Cap |
|---|---|---|
| Astra | 68 images | 85 (no images needed for the remaining three packs) |
| Meshy | 20 credits | 200 (none needed) |
| fal | $2.0148 | $3.00 (none needed) |
| Disk output (conductor allotment) | ~105 MB for 2 packs (fleshshaper ~50, ascended ~55) | 1.2 GiB |

## Open

- No grade on the painted bosses (Matt's call later; conductor ruling).
- The warden's first render stalled at 371 PNGs (cause unknown; the retry rendered 704). If it recurs, the render's 2700 s watchdog ends it.
- Superseded scratch for Matt (not deleted): `en_e2/work/_pack_u.log`; the bake-intermediates manifest
  `runs/C-9/cleanup/manifest_en_e2_p2_bake_intermediates.txt` stands. Keep `en_e2/export/final_{h,k,j,q}_v1/`: they are the sources of the
  superseded provisional packs, which their kits still name.
