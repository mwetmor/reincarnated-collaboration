# Finding — 2026-10-14 — JOIN-1 census delta Gate-2: the Sorceress build file (§ 12), rows 28–32 (§ 13), and P0 §§ 15–16

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **PASS-WITH-NOTES**: every class and the 32 / 23 and 25 / 18 records are accepted. ⚑ **One cross-check bears on the Matt sheet: rows 29–31 need port-site scope that the 19-site table of ADDENDUM-8 (written before KP-437) does not contain.** See WARN-1.)
**Target:** collab `3d1a6edca` (§ 12: build file pinned, mercenary out), `61d2bef7c` (§ 13: rows 28–32; pin + Static Field; BC/FA always on), P0 §§ 15–16; legolas C-14 stage 2 (collab `96f519ed3`)
**Rulings:** KP-435, KP-436 (Matt: Standard variant; BO always on; mercenaries out, period), KP-437 (Matt: Static Field; conductor: BC/FA always on, S-1…S-4 admitted, S-5 folded, exclusions)
**Developer:** elrond · conductor gandalf
**Principles applied:** 3, 4, 5 · Disciplines #10, #12

## Verdict on the questions asked

**Row 28 (Static Field) against WW row 11 (Crushing Blow): CONSISTENT. WIDEN → L-07 `pct-current` + L-08.**
- Same shape: proportional damage on offense, where GD has it on intake only (`intake.PclLimb`); `off` reproduces the referent.
- **Two differences from CB, to register (INFO-1):**
  - (a) Static's **Hell floor** (it cannot take a monster below 50 % life) is a term L-07's registered settings `{off, pct-current, pct-max}` and J3d's `proportional_raw` do not carry. L-07 gains a **floor operand** (`min_hp_frac`, default none), with a grid row and the 1.13 law owed by legolas.
  - (b) Static is cast from her **spell lane** and splashes a radius. It reaches bodies through **S02/S04** (mirror-side lane + the apply-to-body primitive), not through J3c's weapon-packet site S-3, so its L-07/L-08 forms are called mirror-side.
- **Unit:** a share of current life is **scale-free**. It is applied natively to GD HP, never × r_HP (the CB precedent, ADDENDUM-1 § H 2).

**Row 29 (Frozen Armor freezes melee attackers) as GD-EMPTY sharing the L-21 body: CORRECT CLASS** under the § 11 taxonomy rule: the oracle has no monster control state, so a built body is needed.
- **But "sharing L-21's body" covers only HALF of the mechanism.** L-21's port site **S07 is a binary lock** (`body_locked` → `continue` on action and motion). Frozen Armor:
  - **freezes** normal monsters and minions (a lock, S07-compatible);
  - but only **chills** champions and above, and that is a *slow* on monster action and motion speed. A binary gate cannot express it. Under the tier map (trash → normal; champion-hero and boss/nemesis → chill only), **every champion, boss and nemesis takes the chill branch.** See WARN-1.
- The tier mapping should reuse L-24's resolved tiers (`AttackerTierUnresolved` discipline), declared.
- **Composition (INFO-2):** freeze vs monster hit recovery (row 16) on the same body: declare that a frozen body outranks hit recovery, with lengths `max`-refreshed or replaced per the D2 law legolas grades.

**Row 32 (flat magic absorb) reversing KP-431's exclusion: SOUND.**
- KP-431 excluded it because a dedicated build was out of proportion for a 3–8 stat. **One `flat_family_absorb` lever shared with the Barbarian's deferred flat DR/MDR** (P0 § 16) changes that balance, so reversing it is a proper re-ruling, not drift.
- **Unit:** absorb 8 in D2 units × **r_DMG** (a kit-life quantity; ADDENDUM-5/-6 tables). The magic families come from **row 25's map** (Aether / Chaos / Life → magic), a distinct stage from row 25's resist %, so not a double count.
- ADDENDUM-4 § 5.3's exclusion cost line must be **retired** in ADDENDUM-9.

**"Always on" for BO, BC and FA, against the fight window: SOUND AS A DECLARED PILOT POLICY, but not "always on" in D2's own terms. See WARN-2.**

**No double counting: CONFIRMED.**
- Row 31 (thorns) **enables** row 26's Ascended retaliation clause; it does not duplicate it.
- Row 30 (the Oculus' involuntary teleport) is an **item proc**, distinct from her excluded Teleport skill and from row 27's locomotion.
- Row 29 (monster CC) is distinct from row 22 (player CC received) and row 16 (monster hit recovery), with composition per INFO-2.
- S-5 (Oculus +5 mana per kill) folded into row 2 as an operand is correct.
- Frozen Armor's +100 % Defence and Spirit's +250 vs missiles as row-20 operands are correct, and distinct from row 29's freeze mechanism.
- BC's +1 skills (→ slvl 46) is a row-6 operand. Static's mana, cadence and lock entries go into rows 1, 8, 9, 10, 13, 15, 17 and 18 as operands.

**The § 12 mercenary exclusion (Matt, "out, period") and P0 § 15:** recorded with fidelity-cost lines and their directions (offense against fire-resistant bodies understated; survival understated). Correct, and no option is held open.

**Named-finding record: COMPLETE.** The fifth finding, 27 → 32 and 18 → 23, has its reason, ruling, anchor and chain. I re-added the frozen record: INTERNAL 8 + BOUNDARY 23 (AS-IS 4 · WIDEN 14 · GD-EMPTY 5) + OUT-OF-ARENA 1 = **32**. The Barbarian stays at **25 / 18** until his pin (§ 16).

## WARN-1 — Rows 29–31 need port-site scope the 19-site table does not have. Re-check the Matt sheet BEFORE it goes

ADDENDUM-8's final table (engine `d785f334`) predates KP-437. Against it:

| Row | What the port must do | Nearest site | Gap |
|---|---|---|---|
| 28 Static Field | a % of current life, floored, cast from her lane | S02 / S04 (mirror) | none in sealed code. L-07's floor term is mirror-side (INFO-1) |
| **29 Frozen Armor** | freeze (lock) **and** chill (slow) on GD monsters that hit her in melee | S07 (binary lock) | **the chill branch needs a speed factor** on monster action cadence and motion. S07's `continue` cannot express it, so either S07's scope widens or a site is added |
| **30 Oculus** | on being struck (melee or weapon-missile), a 25 % roll, then an involuntary reposition | none. S01(vi) turns the **dash layers OFF** under her profile, and those are the oracle's only reposition primitive | **a trigger in the intake path** (adjacent to S09) and a reposition call that works while S01(vi) is off. Likely a **new site**, plus a JOIN draw stream for the 25 % |
| **31 War Traveler thorns** | damage to a monster on its landed melee hit on her | none | **a new player→monster damage booking from the intake path.** That is a site **and a booking-census row addition** (KP-360 (a)) |
| 32 flat absorb | a flat stage on magic families | S14 (H-8, consented) | none: mirror-side lever method |

*Action:* gamora's ADDENDUM-9 re-maps rows 28–32 onto the table, adding sites or widening scopes as needed, and **the conductor holds the sheet until it does**. The count is then **19 + k**, with the census-row consent extended for row 31 (and for row 29 if the chill books anything). Sending the 19-site sheet now would leave rows 29–31 without consented code paths.

## WARN-2 — "Always on" is a zero-cost REBUFF policy. The fight window is longer than every buff

- **J-S8 per-cell window: 343 / 384 / 447 s** (min / mean / max of G7 ticks ÷ 12.25, from the G-D3 v3 per-cell rows).
- Against that: BC ≈ 155 s, BO ≈ 180 s, FA 288 s. So **every buff expires at least once per cell**: BC and BO about twice, FA at least once.
- "Always on" is therefore **not the buffs' D2 duration law**. It is a pilot policy: *she rebuffs instantly and for free*. That is sound as a JUDGED policy, since home players rebuff between packs.
- **Frozen Armor is material:** +100 % Defence moves her melee CtH from about 74 % to about 57 % (H1 at about 2,900 Defence). A lapse matters.

*Action:* ADDENDUM-9 declares:
- (a) **"always on = rebuffed at zero cost"** on the fidelity table;
- (b) the **omitted rebuff cost**: casts per window (BC + BO from the swap; FA re-cast), their frames (≥ 3 × 8 per BC/BO cycle, plus the swap), and their mana. This is expected at about 1 % duty, printed;
- (c) the **no-FA sensitivity** (KP-437 (1)) printed beside the main result, because FA is the buff whose lapse would move the result.

If the conductor prefers modelled expiry and re-cast, that is a rotation-policy row, not a census row.

## INFO
- **INFO-1:** L-07 gains a floor operand for Static's Hell floor. Static is applied scale-free (no r_HP) and routed through S02/S04.
- **INFO-2:** monster-state composition: freeze > hit recovery on a body; chill and hit recovery coexist; lengths per legolas's 1.13 law.
- **INFO-3:** the Oculus reposition draws a JOIN stream (`reposition:<kit>`), seeded like `block:` / `crit:`. Its destination rule is UNVERIFIED (D2MOO, else JUDGED), so it is labelled until sourced.

## Action
- [ ] conductor: **hold the Matt sheet** until ADDENDUM-9 re-maps rows 28–32 onto the site table (WARN-1).
- [ ] gamora: ADDENDUM-9 covering WARN-1 (sites / scopes for rows 29–31; the census-row consent for row 31), WARN-2 (the rebuff declaration, cost and no-FA print), INFO-1…3, retiring the KP-431 cost line, and the Static rotation and kill-credit rules.
- [ ] legolas: the Oculus destination rule, and the 1.13 Static law (Hell floor, resist interaction, radius).
- [ ] Matt: the KP-312 ruling on the re-mapped table.

## References
- collab Sorceress census §§ 12–13 (at `61d2bef7c`); P0 §§ 15–16; engine `d785f334` (the 19-site table); collab `4c30b0d64` (`gd3_report.json` per-cell G7 ticks, read-only)
