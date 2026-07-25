# GD Probe #2 — SIMPLE CHECKLIST

**~15 minutes. Do the tests in order. Stop whenever you want — Tests 1–3 are the session.**
Full-detail version (only if you want the *why*): `2026-07-25-gd-teleport-probe-directions.md`
**Screenshots go to:** the `reincarnated` share → `visual-artifacts/2026-07-25-gd-teleport-probe/`

---

## SETUP (2 min)

1. Launch Grim Dawn → **Custom Game** → your **empty mod**. Not a Hardcore character.
2. Press **`** (backtick — above Tab) to open the console.
3. Type: `character.LogData true`
4. Type: `character.ShowAngerLevels true`

---

## TEST 1 — `game.Spawn` ★ THE ONE THAT MATTERS (5 min)

5. Find a quiet spot. Type: `game.killMonsters`
6. Type: `game.Spawn` — **with nothing after it** — press Enter.
   📸 **Screenshot whatever prints, even an error. The error text IS the answer.**
7. Type: `game.Spawn records/creatures/monsters/zombie/zombie01.dbr`
   If it errors, try **once each** (then stop — don't hunt):
   - `game.Spawn records\creatures\monsters\zombie\zombie01.dbr`
   - `game.Spawn zombie01.dbr`

**Write down:**
- [ ] Did ANYTHING spawn? (yes/no)
- [ ] If yes: does it attack you? Does it show green words like a normal monster?
- [ ] If no: 📸 the exact error text.

---

## TEST 2 — `character.WarpCursor` (3 min)

8. Type: `character.WarpCursor true`
9. Click the ground far away.
10. Click on the FAR side of a monster (so you'd pass it).

**Write down:**
- [ ] Did you appear where you clicked? Instant, or animated?
- [ ] How far can you click? (whole screen / short hop)
- [ ] Warping PAST a monster — did it aggro you? **(the important one)**

---

## TEST 3 — `game.PlayStats` (2 min)

11. Type: `game.PlayStats`
12. 📸 **Screenshot EVERYTHING that appears** — even the boring parts.

**Write down:**
- [ ] Does it show **damage dealt / DPS / HP numbers** anywhere? (yes/no)

---

## TEST 4 — the zombie's angry wave (no extra time — just watch)

13. Next time any monster does the **yelling / arm-waving beat** before it attacks:
    **read the TOP-LEFT green word during the beat.**

**Write down:**
- [ ] The word: ______________ (I'm expecting `AlertBeforePursue` — prove me wrong)
- [ ] Does the beat feel LONGER when it spots you from far away vs. up close?

---

## SEND BACK

- The screenshots
- Test 1: spawned? — or the exact error
- Test 2: warp works? aggro-on-pass?
- Test 3: combat numbers yes/no
- Test 4: the word, if you saw one

**If anything fails: don't troubleshoot. Say it failed and move on — the error text is the data.**

---

*gandalf, 2026-07-25. Repo copy is operative: `agentic_orchestration/gandalf/pc-handoff/2026-07-25-gd-probe2-SIMPLE-checklist.md`*
