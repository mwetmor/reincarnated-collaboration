# Finding — 2026-10-15 — JOIN-1 J4b ADDENDUM-12 CORR-4, ADDENDUM-13 + CORR-1 (L-21 flinch as a WORLD lever), delta gate

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: two WARNs before his flinch-on arm is graded. ⚑ **Rows 22–24: elrond is right**, so `d2` should be PRIMARY. ⚑ **The consent scope (item 3): inside S07's consent, on one condition.**)
**Target:** engine `ae5b67bb` (ADDENDUM-12 CORR-4; forms `e0973a8e` / `d071f249` / `3f54a448`; grid collab `6bf3026d6`), `7e97ba2c` (ADDENDUM-13), `c9adb325` (ADDENDUM-13 CORR-1; forms `bac5b8b8` / `e4c0ab52`, `b0db74e8` / `e003e656`; grid collab `1a44b7c56`, 140/140); elrond's audit collab `865f9ce0d`
**Rulings:** Matt KP-452 (a GETHIT restarts the attack; S07 widened to write per-body timers), KP-453 ("flinch … for GD kits and other kits or it could not balance"); KP-420 ("native mechanics, both directions")
**Developer:** gamora / elrond / drax · conductor gandalf
**Principles applied:** 1, 3, 4, 5 · Disciplines #10, #12

## (1) The port-only flinch-on Warlord arm and its engine row replay: SOUND for DECISIONS. EFFECTS need a gate (WARN-1)
- **The diagnosis is right.** Flinch changes monster behaviour inside `run.simulate_wave`'s do-not-substitute loop, so the engine cannot emit `JOIN[warlord, gd-decoded @ 196, L-21 on]` without an oracle edit (a re-seal). His flinch-on arm is therefore **PORT-EMITTED**, on the same basis as her kit (M-1). Label it so on the fidelity table.
- **The cross-mirror basis for the trigger is sound.** The `gethit` grain `{tick, kit, source, target_id, d, H, tier, drew, draw_index, flinch, lock_end}` lets the engine recompute every decision bit-exactly (operand = the booked `damage_raw`; the draw from the tape).
- **The null path is anchored.** On the port, the flinch-OFF G1–G7 must stay 7/7 against `4c30b0d64` (that is also the comparator's port leg). The leech-reconciled HP identity holds per cell.

**WARN-1 — the row replay checks that each flinch was DECIDED correctly, not that it was APPLIED correctly.** The lock's effect is the ruled behaviour, and nothing checks it: the body neither acts nor moves inside `[k, lock_end)`, and its timers re-anchor at `lock_end` (RESET, KP-452).

*Action:* add per-cell **effect gates** computed from the port's grains:
- **(a)** **0** monster attack rows (G1 / threat rows) from a body inside any of its lock windows;
- **(b)** **0** body displacement inside a lock (from G4 or the motion log);
- **(c)** under RESET, each body's first attack after `lock_end` falls no earlier than the re-anchored cadence allows (the form's `reanchor_at` + the slot's interval);
- **(d)** the same three gates on **her** arm's L-21 locks.

A violation is a negative control failing its own row identity (a halt).

## (2) The trigger map: ACCEPTED, with one sensitivity correction (WARN-2)
- **Hers:** Fire Ball only, SOURCED (Meteor impact, pyre, Static and thorns carry no GetHit flag).
- **His (JUDGED):** disc yes, Soulfire yes, summons yes (0.0134 % of his applied damage), bleed no (D2: DoT ticks never get-hit).
- **One sourced tier law** (16 / 8 / 4) as WORLD rows `RB-W-l21_*`; an unmapped `(kit, source)` **refuses** (`L21Unmapped`).
- **The lock is 4 world ticks** (8 frames at AS 196) **for both kits on one time base.** Each kit has its own `gethit:<kit_id>` stream, drawn in ledger emission order.
- **The near-permanent-flinch risk** on his disc (`d/H` ≈ 0.08–0.38, inside the tier band, at 12.25 hits/s) is honestly printed as a risk, not a prediction.

**WARN-2 — the disc's divisor-class sensitivity points the wrong way.** CORR-1 § 4 cites D2's per-source classes: **8 for a 1H swing / bow, 32 or 64 for a 2H weapon, 16 otherwise**. ADDENDUM-13 § 1.2 maps the disc as **a weapon hit** (JUDGED), but takes class 16, with sensitivity (i) "weapon-class divisor 8".
- **His weapon is two-handed** (Gutsmasher, `mace2h_d107`; Lap L § 3.2).
- So the class implied by the disc-as-weapon-hit reading is **32 / 64**, which **lowers** the flinch threshold to `H/32`. That makes near-permanent flinch **more** likely, not less.
- Divisor 8 is the 1H class, which does not fit his record.

*Action:*
- make sensitivity (i) **the 2H-weapon class (32, with 64 as well if legolas cannot pin which)**, and keep class 16 as of record if the conductor prefers "everything else". Print 8 only as a labelled lower bracket;
- **print his flinch duty** (the share of body-ticks spent locked, per wave) as a first-class diagnostic beside his primary baseline. If it is near 1 under the JUDGED mapping, that single judgement is setting the primary comparator, and the reader must see it.

## (3) ⚑ Consent scope: the S07 ledger pass is INSIDE KP-452 + KP-453's consent, on ONE condition
- **I agree with the conductor.** The flinch decision is made at **S07**, already consented and widened by KP-452 to write per-body timers, by **one added-only pass inside S07's existing G-A** that reads the tick's **booked `damage_dealt` rows**. There are **zero lines at the 5 HP-write sites.**
- It is the same site, the same guard form and the same ruled behaviour. Matt ruled that hits flinch monsters (KP-453) and that the attack restarts (KP-452), and reading the booked row is how the ruled trigger gets its faithful operand (post-k, post-Cruel; Cruel is ON in the run of record).
- It adds no new surface, and the J4b hunk audit at base `d419666` covers it.

**The condition: no new member on the fight.** "Rows emitted since the previous pass" needs a **cursor**.
- If the cursor (and any per-body lock state) lives **mirror-side**, in the rulebook object, and the pass reads the fight's **existing** event list, it is inside consent.
- **If the build needs a new member** on `kc2rt_fight.gd` (a cursor index, a lock map), that is the **M-3 / M-5 class** and needs naming on the sheet for Matt, as M-5 was.
- drax confirms at build which case holds. If it is the first, nothing goes to Matt.

## (4) ⚑ Rows 22 / 23 / 24 (GD control, DoT and chill landing ON her): elrond is RIGHT. `d2` is PRIMARY, `gd` the sensitivity

**The KP-453 test** (elrond § 14, and gamora's own § 4 principle): *whose behaviour does the rule describe?*
- The **delivery** is WORLD: which GD monster skills apply a control, DoT or cold hit, and with what magnitude and GD duration. It is identical for both arms and already shared.
- The **reception** (rows 22 / 23 / 24) is **her body's law**:
  - D2 players have no sleep, trap, petrify or root state;
  - stun is capped and newest-replaces;
  - freeze becomes chill on a player;
  - a DoT replaces-if-stronger per D2 form;
  - poison cannot kill.
  
  These are properties of the **defender's game**, not of the monsters.

**gamora's own table already treats every other defender-side law this way:**
- **row 20** (the intake hit law: "the law reads the defender's stats in the defender's game");
- **row 17** (her hit recovery: "the defender's own recovery … recommend native");
- **row 25** (her resist table).

Rows 22–24 are the **same class of rule**. Making them `gd` while keeping rows 17 / 20 / 25 `d2` would be internally inconsistent. Her body would carry D2 hit-chance and resist laws while receiving GD player states her game does not have.

**KP-420 settles it directly:** "native mechanics, **both directions**". Enemy effects on her resolve by her native mechanics, with anchored magnitudes. KP-453 widened what counts as **world** (monster reactions). It did not reclassify **defender receiver laws**, and its stated rationale (cross-kit balance of a world capability) applies to the monster's reaction, not to the player's.

**So, as ADDENDUM-1 had it:** her arm runs rows 22 / 23 / 24 at `d2`, with `gd` as the printed sensitivity. **No fresh Matt ruling is needed:** it follows from KP-420 plus the census (elrond § 14), and gamora's recommendation would be the departure from both. The stakes:
- row 22 is REACHED-INSENSITIVE on J-S8 anyway;
- rows 23 (DoT stacking) and 24 (chill −50 % on her movement) are reached, which is why the classification matters.

## (5) The damage-class world-modifier rule: SOUND, and read off the oracle
- **The classes and their modifiers:**

  | Damage class | Modifiers | Oracle evidence |
  |---|---|---|
  | direct-primary | banner + Cruel / Ascended | his disc (`banner_factor`, `run.py:2939`; Cruel / Ascended `:2942–2953`) |
  | direct-secondary (proc) | Cruel only | Soulfire |
  | DoT | Cruel only | bleed |
  | summon | banner only | pet hits (`damage_against(…, dmg_mult)` `:3070` / `:3127`) |
  | proportional / retaliation | none | no oracle exemplar: JUDGED "no", with "yes" as the sensitivity |
- **One rule, by class, for every kit:** elrond's note 1 is satisfied.
- **Her Q15 is unchanged and consistent:** Fire Ball, Meteor and pyre are direct-primary (the pyre as D2 per-frame hits, with the DoT class as a sensitivity); Static is proportional; thorns are retaliation.
- **Composition stays declared:** banner additive into the pool for both (his via `BANNER_ADDITIVE_OF_RECORD`).

## (6) The prereg: CORRECT
- **M-c for the PRIMARY pairing is withdrawn until PREREG-ADDENDUM-C.** It recomputes CORRIGENDUM-1's rule (both readings, capacity ≥ 1.67, the conjunction, pairing on waves both kits reached, < 6 pairs = NO VERDICT) from **his flinch-on grains only**, alone, before any graded run, reading nothing of hers. Flinch changes his kill rate and so his tail share. ADDENDUM-B's {159, 160} came from flinch-off data and cannot carry over.
- **ADDENDUM-B stands for the off / off sensitivity pairing.**
- **The rest is right:**
  - M-a stays un-predicted, with no route for the primary pairing;
  - NC-ANCHOR and the arm orderings are evaluated at the primary setting (flinch equal across her arms; a higher r_HP only raises her flinch rate, in the registered direction);
  - the grader refuses a primary grade without his flinch-on GO + `gethit` grains (NO VERDICT);
  - the **asymmetry line** ("flinch only for her") is printed.
- *INFO-1:* ADDENDUM-A § F's row-replay-mismatch halt now covers **his `gethit` rows too**. Add WARN-1's effect-gate violations to § F as NO VERDICT.

## Also noted
- **CORR-4 (RESET of record; `freeze` and `runs_on` as sensitivities):** it implements KP-452. drax's correction that S07 as built was `runs_on` is honestly recorded.
- **v5 cut decisions:**
  - stream ids carry the kit id `d2-fire-sorc-c14` (every tape changes, none served yet, correct before any run);
  - `RB-HOOK-L-21` lever row `{gd: NONE, d2-world}`, with JOIN default `d2-world` for every kit in the primary pairing;
  - `RB-K-velocity_walk_run` as exact integers.
  
  **All sound.**
- **elrond's MIXED rows 28 / 29:** the world halves (whether monster defences reduce %-life damage; the monster freeze / chill reaction in the shared monster control body) apply to any kit by declaration. There is no live asymmetry, since the Warlord has no %-life or monster-CC source.

## Action
- [ ] gamora: WARN-1 (the effect gates, plus § F); WARN-2 (the 2H-class sensitivity; the flinch-duty print); INFO-1. Then PREREG-ADDENDUM-C, alone, from his flinch-on grains.
- [ ] drax: confirm (3)'s condition (cursor and lock state mirror-side; no new fight member) at build. Emit his flinch-on arm with the `gethit` grain.
- [ ] conductor: **rule rows 22–24 `d2` primary** per (4), since KP-420 and the census govern. Matt only if you decide to depart from that.
- [ ] Matt: none, unless (3)'s condition fails (a new member) or the conductor departs from (4).

## References
- engine `ae5b67bb`, `7e97ba2c`, `c9adb325`; collab `865f9ce0d` (elrond § 14 / P0 § 17), `6bf3026d6`, `1a44b7c56`; Lap L `method.md` § 3.2 (Gutsmasher `mace2h_d107`); sealed `run.py:2939–2953`, `:3070`, `:3127` (cited by elrond, read-only)
