# GD Trial Sheet v3 — first CERTIFIED fixture set

*One page. Same setup: Custom Game, backtick console, `PlayStats true` + `LogData true` on.
Your 3 round-2 trials worked — this sheet adds the five captures that turn trials into
CERTIFIED fixtures (we found the round-2 trials can't be tied to a specific monster or
character sheet, so the data is real but "unverified-identity"). ~15 min.*

---

## ONCE PER SITTING (before any trial) — the identity block

1. - [ ] **Character sheet screenshot** — open the character window (default key `C`),
   screenshot BOTH tabs if there's a second one. This is the single most valuable capture:
   it's the input the conversion key converts. (Round 2 gave us only level + HP globe.)
2. - [ ] **Difficulty**: which is this save on? Normal / Veteran / Elite / Ultimate: ______
   (it changes monster stats a lot — we couldn't tell from round 2)

## PER TRIAL (same L0 protocol as round 2, plus three lines)

1. `game.killMonsters` — clear the screen.
2. **SPAWN your target this time** (this is what makes the fixture certified):
   `game.Spawn "records/creatures/enemies/zombie_a01.dbr"` — then:
   - [ ] **Hover the spawned zombie and screenshot its nameplate** (name + level if shown).
3. **PlayStats BEFORE screenshot** (as before).
4. Fight it to the death, basic attacks, same weapon.
5. - [ ] **Screenshot IMMEDIATELY after the killing blow** — within a couple of seconds.
   (Two reasons: the DPS field's window expires fast — your T2 shot read 0.00 because ~55 s
   had passed — and we want the HP globe reading before regen refills it.)
6. **PlayStats AFTER screenshot** (this can be the same shot as step 5 if the panel's up).
7. Jot: seconds, HP globe cost (and the globe number right after the kill if you caught it).
8. - [ ] **Did anything else die between trials?** yes / no — (round 2 had one mystery kill
   between trials 2 and 3; totally fine, we just need to know when it happens)

**Target: 3–5 trials, same spawned zombie type, no level-up mid-set** (if you level up,
note which trial it happened after — we split the set there, like round 2's 5→6).

- [ ] Trial 1: ____s · HP cost ____ · globe after kill ____/____
- [ ] Trial 2: ____s · HP cost ____ · globe after kill ____/____
- [ ] Trial 3: ____s · HP cost ____ · globe after kill ____/____
- [ ] Trial 4 (optional): ____s · HP cost ____
- [ ] Trial 5 (optional): ____s · HP cost ____

---

*Drop screenshots in `visual-artifacts/GD-matt-test/test-v3/` and notes in
`matt-notes-from-pc/` as before. Round 2 was a full success — spawn confirmed, trials clean,
and the two number-corrections we made afterward are exactly why this sheet asks for the
nameplate + character sheet.*
