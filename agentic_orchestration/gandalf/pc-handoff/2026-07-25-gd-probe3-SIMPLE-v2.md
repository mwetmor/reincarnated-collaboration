# GD Probe — SIMPLE checklist v2 (round 2)

*One page. Same setup as last time: Custom Game, backtick console. Round 1 results are in —
this round: 2 spawn retries, 1 damage-log check, and the first 3 real trials.*

---

## TEST 1 — Spawn retry (research came back — round 1 had TWO problems: no quotes AND a wrong path)

The real record lives at `records/creatures/enemies/` (there is no `creatures/monsters/`
anywhere in the database — 34,114 records checked). Documented working form is a QUOTED
path with forward slashes.

1. **PASTE this line** (don't type it — the quote key registers poorly in the console,
   per the modder who documented the command):

   `game.Spawn "records/creatures/enemies/zombie_a01.dbr"`

2. If nothing happens: type `game.Spawn records/creatures/` and press **TAB, not Enter** —
   the console autocompletes file paths. Screenshot whatever it shows.

- [ ] Result 1: ______________________
- [ ] Tab autocomplete screenshot: yes / no

*(Backups if a01 spawns nothing: `zombie_b01.dbr`, `zombie_c01.dbr`, and
`testdummy_killable.dbr` — same folder.)*

**Bonus fix from the same research:** `game.PlayStats` takes NO argument — the bare command
is the working form (that's why `game.PlayStats true` errored but the panel still showed).
For the toggles, if `character.ShowAngerLevels true` errors again, try
`character.ShowAngerLevels 1` and note which form takes.

## TEST 2 — Does the console print DAMAGE lines during a fight?

1. Make sure `character.LogData true` was entered this session (if it errors, try
   `character.LogData` with no argument — note which form is accepted).
2. Fight ONE zombie with the console open (backtick toggles; fight, then reopen).
3. Screenshot the console right after the kill.

- [ ] Do lines with damage numbers / hit results appear? (yes/no + screenshot)

## TEST 3 — First 3 zombie trials (the real thing — L0 protocol)

Per trial (~2 min each):

1. `game.killMonsters` — clear the screen.
2. Walk (don't warp past monsters) to ONE fresh ordinary zombie.
3. **Screenshot PlayStats panel BEFORE** (kills count matters).
4. Fight it to the death. Nothing fancy — basic attacks are fine, same weapon each trial.
5. **Screenshot PlayStats panel AFTER** + one console screenshot.
6. Jot: rough seconds the fight took, and how much of your HP globe it cost (none / sliver /
   quarter / more).

- [ ] Trial 1: ____s, HP cost ______
- [ ] Trial 2: ____s, HP cost ______
- [ ] Trial 3: ____s, HP cost ______

*Same zombie TYPE each time if possible (the plain shambler, not the burning/fat ones).*

## TEST 4 — One AlertBeforePursue timing (only if one shows up; don't hunt)

If a zombie does the yell-beat: count "one-one-thousand…" until it starts moving.
- [ ] Beat length: ~____s  ·  Spotted you from: close / far

---

*Drop screenshots in `visual-artifacts/GD-matt-test/` and notes in `matt-notes-from-pc/` as
before. Round 1 was exactly what we needed — the three state names you wrote down each
confirmed a different mechanism family.*
