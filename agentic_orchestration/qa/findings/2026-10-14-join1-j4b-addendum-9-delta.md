# Finding — 2026-10-14 — JOIN-1 J4b ADDENDUM-9 delta: the build-file sheet, rows 28–32, and the 23-site table

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: **the 23-site table is COMPLETE** for rows 28–32 once two attachments are written into it, WARN-1 and WARN-2. **Neither adds a site.** R-1…R-3 carry over to the new sheet.)
**Target:** engine `1ae57713` (ADDENDUM-9), against my census Gate-2 `8281adb67` and ADDENDUM-8 delta `926932a9f`; drax inventory ADDENDUM A (godot `7ab66a3`); legolas C-14 stage 3 (collab `34a5629dc`)
**Developer:** gamora / drax · conductor gandalf
**Principles applied:** 1, 3, 5 · Disciplines #10, #12

**`8281adb67` is discharged.**
- **WARN-1 (sites for rows 29–31):** S07 extended (freeze), S20 chill, S21 Oculus trigger, S22 teleport, S23 thorns.
- **WARN-2:** "always on" is declared a zero-cost rebuff pilot policy. The omitted cost is printed (≈ 35 frames per cycle, ≈ 0.7–1 % duty), and the no-FA sensitivity is printed.
- **The INFOs:** L-07's Hell floor; Static scale-free; FREEZE > HITREC; `oculus:<kit>` stream.

**`926932a9f`'s R-1…R-3** are carried on the conductor's sheet (`c14285481`) and must be carried onto the 23-site sheet (WARN-3).

## Independent checks
- **The sheet arithmetic recomputes:**
  - life 2,821 × 78.5835 = **221,684** (× 97.06 = 273,819; × 46.98 = 132,527);
  - EHP parity `(20005/2821)·(0.25/0.20)` = **8.86** on every elemental family, below every arm, so **M-a is UN-PREDICTED in all three arms**. The withdrawal of "LOWER at use-weighted" is correct;
  - regen `⌊88·467/100⌋` = 410 / 256 per frame = **40.0 mana/s**;
  - full rotation 149.5 / 1.6 s = 93.4 mana/s, so the unconstrained phase is **19.3 s**.
- **The FA-primary H1 tables: 372 / 372 is sound.**
  - I re-ran H1 at clvl 99, Def 3,017 (3,267 vs missiles) against C-14 stage 3's per-attack `hit` / `hit_champ` (champion `⌊AR·149/100⌋` at mlvl 87): **186 / 186 exact.**
  - For the unique and unique+ES halves, stage 3 publishes **summaries only**. Computing them from stage 7's `ar_unique` / `ar_unique_extra_strong` at the FA Defence gives **54 [51–60.25] (41–74)** and **64 [63–70] (53–80)**, which is **exactly** legolas's § 7.3 summaries.
  - *INFO-1:* the grid file should cite that the unique/ES rows are checked against stage-3 **summaries** (per-attack values computed from stage-7 AR), not per-attack references.
- **Booking: everything goes through `_ss_hit`, so no census rows. SOUND.** `_ss_hit(b, dmg)` (`:4021`) is the existing player→monster booking (applied / pool_truncated / dropped, kill, pet death) that Soulfire already uses. Static, thorns and her packets add **no `_cons_add` line**. S10's belt heals are left to the build, with any new `_cons_add` a named finding.
  - *INFO-2:* to avoid a second Matt round-trip, the sheet could carry a **conditional census consent**: "any `_cons_add` line added inside a J4b branch, enumerated by `census_grep` at the commit, is within consent". That is Matt's choice.

## WARN-1 — Frozen Armor's TRIGGER has no named site. Attach it to S21's `on_struck` G-A

The table places FA's **effects**: freeze via S07 (`body_locked` on attack and motion) and chill via S20 (speed and cadence factor). The **trigger**, which sets the freeze or chill state on the attacking body, is not placed. ADDENDUM-9 § 3.2 defines it as "a landed, unblocked melee hit carrying physical damage … after S09's block". That is exactly where **S21** (`_apply_slot` `:5936`, after S09) and **S23** sit; drax's inventory gives S23 a shared `on_struck` G-A.

*Action:* write into the table that **the FA trigger is part of S21's single `on_struck` G-A**, together with the Oculus draw and the thorns booking, in a declared order (e.g. FA state, then thorns, then the Oculus draw). The draw count and the per-cell gates then hang on one call. **No new site.**

## WARN-2 — Row 32's per-hit budget would also consume DoT RATES. Exclude DoT rows via S13's existing touch

I read the port. `_mitigate` (H-8, `:6400`) is called in the slot's row loop for **direct rows** (`:6223`). It is also called by `_dot_register` (`:5231`), which mitigates a DoT row **as a per-second rate** before registering it on the timeline. Both calls happen inside `_apply_slot`'s resolution, under S17's slot context. So the "per-hit budget of 8 · r_DMG" would also be spent on a magic-family DoT row's **rate** (SlowLife / SlowChaos / SlowAether), subtracting an amount from a per-second quantity. That is a unit error.

**Good news on the deferred path:** mitigation happens **at launch**, so deferred packets carry already-mitigated `direct` (`:4805ff` lands them without re-mitigating). The S17 context covers them correctly.

*Action:* declare that **flat absorb applies to direct rows only**. A DoT rate is never reduced by it (JUDGED; D2's absorb acts on damage instances). Implement it by having **S13's existing touch in `_dot_register`** mark the call as a DoT rate for the mirror's H-8 lever. **No new site.** Add a grid row: a hit with one direct and one DoT magic row spends the budget on the direct row only.

## WARN-3 — Carry R-1…R-3 onto the 23-site sheet, with R-2 extended to S22

The 19-site sheet (`c14285481`) carries my ADDENDUM-8 delta as:
- **R-1:** S10 keys on L-S7, not `kit_is_gd()`;
- **R-2:** S02's DEATH-at-entry test;
- **R-3:** deferred-projectile block decided at the resolve tick.

ADDENDUM-9 does not restate them. **The 23-site sheet must.** Extend **R-2 to S22**: the once-per-tick teleport at `:2037` also runs **before the sealed death check**, so it must not fire after lethal intake in the same tick. State the order at `:2037` too: **teleport, then lane frames**, or the reverse, declared.

R-3's launch-time decision applies equally to **S21/S23 on projectiles**: the Oculus trigger on a weapon-damage missile is decided at the resolve tick. Print the latency.

## The site table: COMPLETE at 23, with WARN-1/2 attached
- Row 28 needs no site (S02 / S04 → `_ss_hit`).
- Row 29: S07 extended (freeze) + S20 (chill), with the trigger on S21 (WARN-1).
- Row 30: S21 (the 25 % draw on `oculus:<kit>`, after S09) + S22 (the position write at `:2037`; 10-try search out of tree; walkability by `kc2rt_pilot_move.gd:159` + geometry).
- Row 31: S23, sharing S21's G-A and booked via `_ss_hit`.
- Row 32: H-8, consented, with the S17 budget and S13's DoT mark (WARN-2).
- **No new members beyond M-5; one new JOIN-only stream; no census rows** (by design).
- **S01–S15, S16b and S17–S23 = 23. S16a is engine-side.**

## INFO
- **INFO-3: Warmth.** The pinned build file gives Warmth **1 hard point** (slvl 27, 342 %), which supersedes KP-434's 18-point default. That is correct by KP-435 (Matt: the sheet from the pinned build). The conductor should **record the supersession on the ledger**, so KP-434 does not read as live.
- **INFO-4: the M-a registration route.** Registering "≥ Warlord" when expected intake < life + belt on every wave is a pre-run computation, which is fine. Add a **margin** (e.g. expected intake ≤ 0.8 × (life + belt) on every wave), so a near-tie expectation never registers a direction: INFO-4's rule from ADDENDUM-6 applied to this route.

## Action
- [ ] gamora / drax: write WARN-1 (FA trigger on S21) and WARN-2 (direct rows only, via S13) into the table text; INFO-1, INFO-4.
- [ ] conductor: the 23-site sheet carries R-1…R-3, with R-2 extended to S22 and R-3 to S21/S23 projectiles; INFO-2 (the conditional census consent) as Matt's choice; INFO-3 on the ledger. **Then put it to Matt.**
- [ ] Matt: the KP-312 ruling on 23 sites.

## References
- engine `1ae57713`; godot `kc2_runtime/sim/kc2rt_fight.gd` (`:4790-4822`, `:5222-5236`, `:6195-6232`, `:6400`), inventory `7ab66a3` (read-only)
- collab `agentic_orchestration/legolas/research/2026-10-14-join1-c14-sorc-build-file/c14_stage3.json`, README § 7.3; `…/2026-10-14-join1-c13-enemy-anchor/d2_unique_ar_r1.json` (H1 re-runs above); the ruling sheet `gandalf/notes/2026-10-14-j4b-kp312-port-site-ruling-sheet.md` (`c14285481`)
