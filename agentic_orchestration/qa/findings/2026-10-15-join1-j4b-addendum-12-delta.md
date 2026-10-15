# Finding — 2026-10-15 — JOIN-1 J4b ADDENDUM-12 + CORRIGENDUM-1 (drax's 17 kit questions; the lock-machine form), delta Gate-1

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: one site-scope confirmation before the build touches S07; the rest are INFO. **The KP-439 site table does not change**, subject to WARN-1.)
**Target:** engine `8dce5245` (ADDENDUM-12), `595e6a05` (CORRIGENDUM-1, folding legolas C-14 stage 7, collab `cf57913e0`); questions at godot `bc3c656`
**Developer:** gamora · drax mirrors · conductor gandalf
**Principles applied:** 1, 3, 5 · Disciplines #10, #12

## The RNG law: the row replay is WELL-DEFINED
- **Generation:** `crit:*`-style seeds (sha256 of `arm|salt|stream_id`), **`random()` only**, so every tape is homogeneous.
- **Engine-generated tapes served through the `ReplayStream` door.** The port never generates. An exhausted tape is a MISMATCH, never a wrap.
- **Gate, per cell and stream:** `n_mismatch == 0` and `unserved == 0`.
- **The replay row logs `(stream_id, draw_index, u)`**, and the engine re-derives `u` bit-equal from the seed, then recomputes the row through the form.
- **`r32(u) = int(u·2^32)` is exact:** `u = k/2^53`, so `u·2^32 = k/2^21`, a pure power-of-two scaling, and `int` is floor. The result lies in [0, 2^32).
- **`bounded(n) = r32 % n`** equals D2's `roll & (n−1)` for power-of-two n and `roll % n` otherwise. Both are exact in integers. The `n = 0` edge has no draw, is asserted never to fire, and is labelled JUDGED.
- **The streams of record** (CORRIGENDUM-1 § 1):

  | Stream | Draws | Basis |
  |---|---|---|
  | `dmg:` | **one per explosion / impact, shared by every unit in the radius, max exclusive** | sourced; replaces the per-target roll |
  | `pyre:` | per (pyre, unit, frame) | |
  | `softhit:` | its own stream, drawn right after each pyre roll, so pyre positions stay independent | counted; no GD effect, JUDGED |
  | `gethit:` | FB explosion targets in the [H/16, H/4) tiers | |
  | `potion:` | randLimited first | JUDGED; the other order is a sensitivity |
  | `block:` | | |
  | `oculus:` | GETHIT-flag hits only | sourced, `EventFunc21` |

  The canonical within-frame order (intake → her packets by kind, creation index and `actor_id` → potions) fixes every stream position.
- *INFO-1:* write two positions explicitly into the canonical order:
  - (a) **the Oculus destination-search draws** (2 per try, at most one search per tick, at S22 `:2037`) come **after all of the tick's intake and before her lane frames**;
  - (b) **within one intake hit:** `block:` → (unblocked) damage → the HITREC test → (GETHIT) FA, then the `oculus:` 25 % draw, then thorns.
  
  Both are implied by CORRIGENDUM-1 § 2 Q4 and ADDENDUM-9 § 3.3. The replay needs them stated.
- **Declared, correctly:** the distributions are D2's, but the **seed identity is not** (D2 seeds per unit; JOIN draws one stream per class). That goes on the fidelity table.

## Q8 (L-21): ACCEPTED. Row 16 ACTIVE is fair
- **The trigger is SOURCED** (`SUnitDmg.cpp` L2090–2228):
  - **Fire Ball explosions only** (Meteor impact and pyre carry no GetHit flag);
  - the divisor-16 / 8 / 4 tiers on the post-mitigation, pre-cap packet `d` against the body's `H`, which is scale-free under r_HP;
  - no get-hit on frozen bodies;
  - `mGH` taken on all GD bodies (JUDGED; 69/70 R1 types).
- **The length is JUDGED at 8 frames** (her own FHR length on the receiving side; no GD-native monster hit reaction exists), with 4 / 16 sensitivities and an L-21-off negative control.
- ACTIVE in fraction (b) is fair: the D2 mechanism is implemented and reached, and its magnitude is a labelled judgement printed on the fidelity table.
- *INFO-2:* make the **sourced constants pack rows**, not form literals:
  - the divisors 16 / 8 / 4;
  - the 50 % branch's polarity (JUDGED);
  - softhit `19/128`;
  - the FB-only flag.
  
  ADDENDUM-12 § 2 Q8 listed `RB-K-l21_trigger` and `RB-K-l21_softhit_missiles`, but CORRIGENDUM-1 § 4 lists only `RB-K-l21_length_frames`.

## WARN-1 — Q8's ATTACK-TIMER RESET may exceed S07's consented scope. drax confirms before the build touches S07

The KP-439 ruling sheet consents **S07 as a gate**: `body_locked(b, run_tick)` → `continue` on the body's action and motion (`_resolve_threat` swing loop, `choose_slot`, the motion step). CORRIGENDUM-1 Q8 adds that **the body's in-progress attack is cancelled, and its attack timer reset to 0** (JUDGED; the "timer freezes" variant is the sensitivity).

- A **freeze** is pure gating: S07 skips the body while it is locked, and its timer resumes afterwards.
- A **reset** is a **write** to sealed per-body cadence state (`busy_until` / the cadence counter at `:3324` / `:3403`, gd_engage `:421` / `:945`).

*Action:* drax confirms one of:
- (a) the reset is implementable **inside S07's G-A** as added-only lines, writing to the body dictionary under `rulebook != null`. That is within the consented guard form, recorded in the inventory, with no scope change;
- (b) it needs lines outside S07's consented regions. Then it is a **site-scope amendment for Matt** (KP-312), or Q8 takes the **freeze** variant as the value of record, with the reset as the sensitivity.

**Until confirmed, build S07 with the freeze variant.**

## The other rulings: ACCEPTED
- **Q10 (stamina):**
  - **697 is SOURCED** (74 + 98 + 525; MODEL-VERIFIED). It replaces 1,179; BO's un-traced operation keeps 1,179 / 1,254 as sensitivities.
  - **Drain 24/256** = 40/256 × (100 − 40)/100, from War Traveler's `staminadrainpct` 40 (a VERBATIM corpus row). That is the standard reading of "Slower Stamina Drain"; legolas confirms the operation, and 40/256 is the sensitivity.
  - Walk / run are 7.26 / 10.26, so the WALK scale is 121/171, an exact rational. The RUN displacement stays the GD pilot AS-IS.
  - Stamina rarely binds for a mana-bound caster (A4 § 4.7 arithmetic), so it is low-stakes either way.
- **Q5:** Fire Ball **explodes** at range end and at the arena bound (code-only, moderate confidence), with "vanish" as a sensitivity. The motion of 0.75 m per frame is confirmed. Size → radius stays JUDGED.
- **Q11:** D2's own **1/256 progress counter**, with the GD tick standing in for the D2 base-speed frame (anim = ⌊rate·256/100⌋, fire at ≥ 256·n). It reproduces stage 7's examples (e.g. a 16-tick attack at −33 takes ⌈4096/171⌉ = 24 ticks), and the floor (171 vs 171.52) is D2's. Right to replace the exact-rational form.
- **Q12 `≥`:** cited (the code returns "no get-hit" when damage < maxHP/divisor).
- **Q13:** 83 = min(75 + 8, 95, uncapped 125). The `RB-K-res_uncapped` pack row is right.
- **Q14:** column order is a JUDGED pilot policy (each column is its own hotkey). Super Mana 500 already includes ×2, so the class factor must not be applied twice.
- **Q17:** `ceil(25·s)`, JUDGED.

**The design calls:**
- **Q6, nearest fire-killable target:** right; it never wastes a cast on an immune body.
  - *INFO-3:* add **"within Fire Ball's range (37.5 m at the primary yard key)"** to eligibility. A nearest-but-out-of-range target would otherwise spend mana on a range-end explosion, a systematic pilot cost against her.
  - Print **the Meteor hit rate**: the impact point is fixed with no lead, so a marching body can leave the 4.8 m radius in the 2.4 s. The cluster-point sensitivity is there; the rate makes it legible.
- **Q9:** regen per frame before the action poll.
- **Q15:**
  - the Cruel window is 25 frames on her timeline (12–13 ticks against the sealed 13; printed);
  - banner and Cruel apply to FB, Meteor and pyre only;
  - not to Static (proportional, scale-free) or thorns (not a damage pool);
  - the sensitivity covers both.
- **Q16:**
  - the board resets;
  - player state carries, with the exact integer rebase;
  - the belt refills;
  - mana carries against the Warlord's energy reset (asymmetry declared; "mana full" is a sensitivity).
- **The lock machine (§ 3):** A4 § 3 / A6 restated as a form: rank, equal-rank replacement, no block draw inside BLOCK, the gated block, CAST pre-emption, and the rebase. The **NEW** `last_block`-updates-on-animation rule is labelled PROVISIONAL → legolas. The ≥ 40-scenario grid has a 1-frame-perturbed negative control. **Sound.**

**Pack rows for star-lord's next cut: COMPLETE apart from INFO-2.**
- `RB-K-meteor_pyre.offsets_subtiles`;
- `RB-K-res_uncapped`;
- `RB-K-stamina_max` 697;
- `RB-K-stamina_drain_256` 24 (with the formula);
- `RB-K-l21_length_frames` 8 (JUDGED);
- the stream-id rows (`dmg:` / `pyre:` / `softhit:` / `potion:` / `gethit:`);
- the `potion_class_factors` note;
- `RB-K-kit_id` WARN-1.

## The site table: UNCHANGED, apart from WARN-1
- The new streams and laws live **mirror-side** or in the engine forms.
- `gethit:` and the monster lock ride **S04** (the explosion) and **S07** (the lock).
- The progress counter rides **S20**'s consented cadence-factor placements. It needs per-body progress state; keep it mirror-side, keyed by body, or in the body dictionary under S20's guard, consistent with "no new member".
- The Oculus GETHIT narrowing rides **S21**.
- Pyre stacking and softhit run through **S02 / S04 → `_ss_hit`**.
- **No new site.** WARN-1 is the only possible scope question.

## Action
- [ ] drax: WARN-1 (the reset inside S07's G-A, or the freeze variant; anything else goes to Matt). Mirror the tape door and the lock grid.
- [ ] gamora: INFO-1 (the two draw positions in the canonical order); INFO-2 (the L-21 trigger constants as pack rows); INFO-3 (the FB range in eligibility; the Meteor hit-rate print). Then the build per § 5 / CORRIGENDUM-1 § 3, fail-first, each commit alone.
- [ ] star-lord: the next pack cut, with the rows above plus INFO-2.
- [ ] legolas: the `staminadrainpct` and BO stamina operations; the `last_block` update point.
- [ ] Matt: only if WARN-1 resolves to (b) with the reset retained.

## References
- engine `8dce5245`, `595e6a05`; collab `cf57913e0` (C-14 stage 7, README § 11); godot `bc3c656`; the KP-439 ruling sheet (S07 / S20 / S21 consents)

---

## Addendum — legolas C-14 stage 8 (collab `cb7b01319`) on Q10

- **Drain 24/256 per RUN frame is CONFIRMED** (40, then −40 % War Traveler, C-truncated). gamora's value stands over stage 7's 40/256. My Q10 note's "legolas confirms the operation" is discharged.
- **Max stamina with BO = 1,179**: BO acts on base stamina only, and item Vitality adds +94 unscaled. **BO is always on (KP-436), so PRIMARY = 1,179.** This **supersedes CORRIGENDUM-1's 697**, and my Q10 line above ("697 is SOURCED … replaces 1,179") is superseded with it. 697 (BO not on stamina) becomes the sensitivity, and 1,254 is retired, being contradicted by stage 8. gamora folds the change (conductor).
- **The arithmetic checks:** 1,179 ÷ (24/256 × 25 frames/s) = 1,179 ÷ 2.34375 = **503 s** of continuous running from full, with no regen counted. The **J-S8 window is 343 / 384 / 447 s** per cell (min / mean / max), so **she cannot exhaust stamina inside any cell's window, even running every frame.**
- **The consequences, to be declared in the fold:**
  - **row 27 (stamina, INTERNAL) is REACHED-INSENSITIVE on this board.** Frames at stamina 0 are predicted to be **0**, printed as its reach count. INTERNAL rows are not in fraction (b), so (b) does not move;
  - **the WALK branch is unreached**: every moving frame is RUN, so the running melee auto-hit and the running block ÷3 apply whenever the pilot moves her. That is the A4 § 4.7 coupling, now one-sided;
  - the 697 sensitivity (about 297 s) **does** reach WALK inside the window, so it is the arm that exercises the branch. Print it.
- **The site table is unaffected.** The verdict is unchanged: GO-WITH-AMENDMENTS (WARN-1 stands).
