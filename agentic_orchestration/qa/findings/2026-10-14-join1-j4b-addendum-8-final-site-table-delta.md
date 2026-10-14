# Finding — 2026-10-14 — JOIN-1 J4b ADDENDUM-8 delta: the FINAL port-site table for Matt

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: the sheet may go to Matt once WARN-1 (one guard predicate) and WARN-2/3 (two declarations) are in the table text. **The count stays 19**, and no site is added or removed.)
**Target:** engine `d785f334` (ADDENDUM-8), against drax's inventory (godot `a207180`, `kc2_play/join/J4B-SITE-INVENTORY-a0e75469.md`; lines at `kc2_runtime` `d419666`), my `4a8b31678` and `146a3a84f` WARN-2, and KP-434
**Developer:** gamora / drax · conductor gandalf
**Principles applied:** 1, 3, 5 · Disciplines #10, #12, #75 cl. 6

**`4a8b31678` items and KP-434 are discharged:**
- ES is labelled a JUDGED UPPER ARM, with plain unique (76) beside it in the same table, and both integer tables are emitted.
- `physical_contact_table` is engine-emitted and digested; the port reads it.
- Survival ticks are censored at the fixed horizon H, so both-survive cells contribute 0.
- Warmth is restored to 18 points (378 %), with 1 and 0 points as sensitivities.
- The recomputed regen and rotation figures (25.0 / 14.8 / 6.2 mana/s) follow from `floor(51·(100+bonus)/100)/256·25`.

## S01: the six systems are KIT, not world. CONFIRMED against the census and the code

| # | System | Kit evidence (read here) | Verdict |
|---|---|---|---|
| (i) | Channel verdict / release fold | the Warlord's EoR channel; her `d2-mana` replaces it (census rows 1–2) | **kit** ✓ |
| (ii) | Player summons | his kit summons; she has no summon row | **kit** ✓ |
| (iii) | War Cry and defensive actives | `_cp_begin_tick` `:4524ff` fires War Cry and **Ascension**. Ascension is **`records/skills/playerclass09/ascension1.dbr`** (`counterplay.py:65`), a class skill. **It is NOT the Crucible "Ascended" mutator**, which stays world-side in S19 | **kit** ✓ |
| (iv) | `_cp_absorb` on the direct (`:4772`), deferred (`:4817`) and DoT (`:5408`) paths | War Cry reduction; Turtle Shell, Arcane Barrier, Ascension and Menhir's Will pools: item, devotion and skill procs on his record | **kit** ✓. The `else` returns `raw` |
| (v) | R8 Resilience | **`playerclass09/passive02.dbr`** (`player_sustain.py:204`), a **class passive** (ADDENDUM-8 calls it a "devotion"; correct the wording). It is NOT the Crucible "Resilient" mutator, which S19 keeps | **kit** ✓ |
| (vi) | Dash layers | his movement skills; her Teleport is excluded by her pin; the pilot's base motion stays (AS-IS) | **kit** ✓ |

**No world rule is switched off by S01.** The Banner and the mutators (Cruel, Resilient, Ascended) stay on through S19.

## WARN-1 — S10's guard must key on the POTION LEVER (L-S7), not on kit identity

The census classed potions as a **world/boundary** mechanism: K-4 `defaulthealthpotion` is "the game's universal consumable … not the Warlord's kit" (Sorceress census § 9.2, the BOUNDARY reasoning). Row 21 is a **WIDEN lever** {`gd` = K-4, `d2-belt`}. S10 as written is a G-B on **`kit_is_gd()`**, which conflates kit identity with a lever setting. A D2-kit profile with L-S7 at `gd` (or at a no-potion arm) would then be impossible to express.

*Action:* S10's guard becomes `rulebook == null or player_potion_model == gd`. **S03 already does this correctly** (it keys on `resource_law`), as do S12 and S13. Only S01 keys on kit identity, correctly, because it switches off **kit** systems.

## WARN-2 — S02 runs BEFORE the sealed death check, so the lane must test DEATH at entry

S02's call-out sits at `:2037`: after `_burn_dots`, **before the death check**. If this tick's intake has already taken her HP to ≤ 0, the mirror lane would still run her frames (casts, impacts, kills) posthumously. That would move M-b and M-c. ADDENDUM-4 § 3 makes DEATH terminal and above everything, but nothing yet *sets* DEATH before her frames run.

*Action:* declare in S02 (mirror-side, so no sealed line changes) that **`d2_frames` returns without running any frame when `player_hp ≤ 0`** at entry, with a fail-first control: a scripted lethal intake in tick k produces zero lane events in tick k.

## WARN-3 — Block on a DEFERRED projectile is decided at the resolve (launch) tick, not on arrival. Declare it, or a site is missing

`_apply_slot` resolves the hit **at the swing or launch** (`_resolve_hit` `:5962`). Projectile damage then travels through `_defer_queue` (`_land_attack_packet` `:4752-4769`, `at = run_tick + latency`) and lands later (`:4817`). S09 placed right after `:5962` therefore **decides the block, and starts the BL lock, at launch**. D2 resolves block at collision.

That placement matches the oracle's own order (it resolves to-hit, control and Cruel at launch too). A blocked projectile is never queued, so no damage and no DoT follow, which is correct. Two consequences need a decision:

- **(a) declare** "block decided, and BL lock started, at the resolve tick, as the oracle resolves the hit", with the deferred-latency distribution printed on the fidelity table. **No site change.** *Recommended.*
- **(b) start BL at the arrival tick.** This needs the **deferred path (`:4762` / `:4817`) as a further S09 touch point**, and that is a site-scope change Matt must see.

Pick (a) or (b) **before** the sheet.

## The other site placements: CORRECT
- **S02 at `:2037` after intake:** consistent with ADDENDUM-4 § 3's frame order (intake before her action poll) and INFO-1(b)'s placement.
  - *INFO-1:* this makes her offense run **after** intake within a tick, whereas the Warlord's core block `:1988-2000` runs **before** it. A body she kills in tick k still attacks in tick k, where one he kills does not. Print it on the fidelity table as an order asymmetry. It is small, and it disfavours her.
- **S07 in the `_resolve_threat` swing loop (`:3269`; entries `:3360/:3518/:3817`) and `choose_slot` `:447` plus motion:** correct, and not H-16/17 (drax M3). A skipped attack consumes no draws, which is D2's rule (a recovering monster does not attack). The row replay records it.
- **S09 after `:5962`, before `control.observe` `:5965` and `note_monster_hit` `:5970`:** correct. I read `_apply_slot`. A blocked hit applies no control and opens no Cruel window, and dying slots (`:3518`) enter there too.
- **S17 slot-context G-A in `_apply_slot` before `:5962`:** correct, because H-1 receives only (oa, da). The **auto-hit draw at `:5881` stays unguarded, consumed and ignored**, mirroring the engine's drawn-and-ignored d100 (ADJ-2). Stream positions are preserved on both mirrors.
- S03, S12–S15, S18 and S19 are as stated. New member **M-5** on `kc2rt_control.gd` follows the M-3/M-4 class, and is named in § 5.3 for the ruling.

## Census rows and the hunk audit
- **Booking-census row ADDITIONS (≈ 4–8; S04's conservation bookings, shared by S05/S06, and S10's belt heals):** correctly named for the ruling (KP-360 (a)). *INFO-2:* phrase the consent as **"every booking line added in J4b branches, enumerated by `census_grep` at the commit"**. S13's `d2` DoT branch (replace-if-stronger, plus the one frame of a weaker DoT) may add booking lines too, and an estimate should not cap the consent.
- **The J4b hunk audit at base `d419666`, collapsing J4b tags only, with the nested-guard drift control:** correct (#75 cl. 6). S01 and S03 enclose existing D2/J3c guards, and those must pass through verbatim as base text.

## The count: 19, CONFIRMED
S01–S15 (15) + S16b + S17–S19 (3) = **19**. S16a is engine-side.

## Is the sheet complete per `146a3a84f` WARN-2?
1. **Census rows:** yes (§ 5.3), with INFO-2's wording.
2. **The KP-312 condition set:** yes. It lists the null-guarded set, per-site fail-first, ORACLE identity, J-S8 IEEE-754 bit-equal, my delta Gate-2, Matt's windowed `.app` self-test, and M-5.
3. **S16b's emitter question, answered explicitly:**
   - **S16b needs NO emitter unfreeze IF** the per-family split (a sealed member dict plus its increments at `:6163-6164` / `:6173-6174`) is **read by the out-of-tree JOIN tool through the KP-402 `_new_fight(hooked)` RecFight route**, and written to the **JOIN tool's own** report. The totals are already public members (`:157`, `:158`).
   - **If instead the split is to appear in the output of the frozen emitter `kc2p_join1_gm_emit.gd`, it DOES need an emitter-unfreeze ruling**, on the KP-397/402 precedent, and Matt must be asked explicitly.
   - **Recommended:** the no-unfreeze route, stated on the sheet as the route of record.

## Action
- [ ] gamora / drax: fold WARN-1 (the S10 guard on L-S7), WARN-2 (the DEATH-at-entry declaration and its control), WARN-3 (option a or b), INFO-1 (order asymmetry line), INFO-2 (census consent wording) and the R8 wording into the site table text.
- [ ] conductor: then put the sheet to Matt. **19 sites; S16b by the no-unfreeze route** (or add the unfreeze question if the emitter route is chosen). Add WARN-3(b)'s extra touch point only if (b) is picked.
- [ ] Matt: the KP-312 ruling.

## References
- engine `d785f334`; godot `kc2_runtime/sim/kc2rt_fight.gd` at `9b6dca7` (`:4524-4545`, `:4752-4775`, `:5936-5972`, read-only); engine `counterplay.py:65`, `player_sustain.py:204` (read-only); Sorceress census § 9.2
