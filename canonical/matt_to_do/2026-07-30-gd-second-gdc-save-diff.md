# T11 — Pull a SECOND Grim Dawn character save (`.gdc`) — now the DECISIVE test for Fork 1

**Filed:** 2026-07-30, gandalf (RUN-CONDUCTOR, WR3-KITE-COMMIT) · **Source:** R-WR3-26(6) U-1/U-2 · **AMENDED per R-WR3-29(4):** the same pull now closes the VETERAN byte question, which decides the stage-map arm. · **RE-AMENDED per R-WR3-32(3):** the decisive item is now **U-3** (Veteran own-stage ×1.40 vs pooled ×2.14 — a 1.62× HP spread): kill ONE named monster before the save so `greatestMonsterKilledLifeAndMana` records a Veteran-inflated HP we can compare against corpus. U-4 rides free (worth ≤5 % if own-stage, per the degeneracy).

## The ask (~2 minutes, upgraded)

Create a **throwaway GD character with Veteran toggled ON** at creation, save immediately, and copy its
`player.gdc`. Ideally also: toggle Veteran OFF, save again, copy that too (two files = the byte's
on/off states known by provenance). Bonus if convenient: get hit once by a known weak enemy between
snapshots for the damage-field diff. Drop the file(s) anywhere under `/Users/admin/Games/vendor/`
and say the word.

Save location on a standard install: `<GD user dir>/save/main/_<CharacterName>/player.gdc`.

## What it unblocks — now GATING

1. **U-2 (difficulty probe): is `0x80` the Veteran bit?** The referent save reads `difficulty = 128`
   = Normal + bit 7. If a known-Veteran save reads 128, the referent was played on **Veteran**
   (+40% monster damage), which inverts the S1_PAK basis: S2_FULL + Veteran reaches both measured
   damage numbers, and S1's signature 269.66 fit breaks (38% overshoot). **Matt's Fork-1 re-ruling
   and the stage-2c calibration lap wait on this.** (Also answerable from memory: was Veteran
   checked at character creation?)
2. **U-1/U-2 (discriminator note): field labels + single-event-vs-aggregate semantics** of
   `greatestDamageReceived` / `lastHitBy` — the before/after diff closes both.
3. **U-4: `greatestMonsterKilledLevel` semantics** (monster's level vs player's level at kill) —
   decides whether Primordian is cl 18 plain or cl 13 Veteran, which re-derives skill rank (5 vs 4)
   and would re-base the payload pin set.
