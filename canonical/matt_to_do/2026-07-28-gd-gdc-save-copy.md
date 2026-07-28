# Matt to-do — copy the Grim Dawn character save off the GD PC

**Raised:** 2026-07-28 by legolas (G-7 probe, ruling R-KC1-4)
**Status:** OPEN
**Queue row:** T11
**Why only Matt:** the save lives on your Windows PC. No agent session on the Mac can reach it —
verified exhaustively (ten search paths, findings note § 1). This is a file-copy across a machine
boundary; there is no credential involved and nothing sensitive, it is purely a reachability wall.

---

## Do this

**1 — Find the character folder.** It is in ONE of these two places. Check both; take whichever exists.

```
# (a) Steam Cloud OFF — the default
C:\Users\<your Windows username>\Documents\My Games\Grim Dawn\save\main\_<CharacterName>\

# (b) Steam Cloud ON  (your SteamID3 is 116655798 — read off the Mac's Steam userdata dir)
C:\Program Files (x86)\Steam\userdata\116655798\219990\remote\save\main\_<CharacterName>\
```

The character is the **Soldier who transformed into the Fangs-of-Asterkarn werewolf and reached
level 12** — the one from the 2026-07-26 play test. Its folder name starts with an underscore. We
do not have its name written down anywhere, which is why this says `<CharacterName>` rather than
naming it.

**2 — Copy the WHOLE folder** (not just `player.gdc`) to the share:

```
/Volumes/reincarnated/matt-notes-from-pc/gd-save/
```

Copy the folder recursively, including any `Backup` subfolder. The backups matter — if you have
played that character since 2026-07-26, an older backup may sit closer to the recorded run than the
live save does.

**3 — Tell us the character's name** when you report back. One line is enough.

---

## Please do NOT play that character before copying

`.gdc` stores **only the current state** — there is no history in it. Every session you play
overwrites the end-of-run state we are trying to recover. Specifically at risk: the gear you were
wearing at the end of the run, including the item that added the poison DoT. If you have already
played it since 2026-07-26, **copy it anyway** — we will measure the drift and grade the findings
accordingly (`play_stats.playTime` vs the run's `≈ 7094`, which quantifies it exactly). Just tell us.

## If the character was deleted

Say so and this row gets struck. That is a clean answer, not a failure — it just means the devotion
claim stays player-attested instead of becoming measured.

---

## What this unblocks

Upgrades the KIT-CAL-1 kit spec's build identity from **ATTESTED** to **MEASURED**:

- **Devotion = zero.** Currently your word plus "no proc seen in 313 stills". The save supports a
  positive three-part test (`devotionPointsUnspent == totalDevotionUnlocked`, `devotionReclamation
  PointsUsed == 0`, every skill's `devotionLevel == 0`) that also closes the assigned-then-refunded
  loophole neither of the current sources can touch.
- **Onslaught's exact rank** — the number the UI hid behind werewolf form all run.
- **Every skill rank**, including the whole werewolf-transform line.
- **Attribute allocation** (physique/cunning/spirit) and confirmed level.
- **The poison-DoT item's identity** — if it was still equipped at the end. Its record path joins
  straight to the Edition-II `.arz` corpus we already hold, so no further acquisition is needed.
- **Bonus, same parse:** `healthPotionsUsed` / `manaPotionsUsed` turn the potions-0/0 control from
  observed into measured, and the save's `uid` supplies the `save_identity` join key that
  artifact-verification § 505 flagged as missing from the §2.1 protocol.

Read-only throughout on our side: the file is copied to a scratch dir and parsed there. Nothing
writes to your save, ever.

## Related

- Probe + full parse lane (already mapped, so the follow-up is short):
  `agentic_orchestration/legolas/notes/2026-07-28-gd-gdc-save-probe.md`
- Ruling R-KC1-4: `agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md`
- Attestations being upgraded:
  `agentic_orchestration/gandalf/notes/2026-07-26-gd-playtest-v1-efficacy-verdict.md` § 9
