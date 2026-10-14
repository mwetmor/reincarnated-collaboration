# Finding — 2026-10-14 — JOIN-1 J4b ADDENDUM-4 + ADDENDUM-5 (the C-13 binding), delta Gate-1: the last design gate before the build

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: three WARNs must be folded **before the port sites are listed for Matt**, because each changes what a site computes bit for bit)
**Target:** engine `e96c96a9` (ADDENDUM-4), `8c922eb1` (ADDENDUM-5), with ADDENDUM-3 `94ed4e42` read for the dispositions; against my gates `2c5413335`, `5ad04470f`, `1a4bee308`
**Inputs:** legolas C-13 (collab `d5cff2332` / `9347dc22e` / `c81376a83` / `a83290a69`; stage 5 of record: r_HP ×40.5458, r_DMG ×97.0646, use-weighted ×46.979); KC2 KP-428, KP-430, KP-431
**Developer:** gamora · conductor gandalf
**Principles applied:** 1, 3, 4, 5 · Disciplines #10, #12

**All three prior gates are discharged:**
- **`5ad04470f` WARN-1/2** (ADDENDUM-3 § 1–2): the per-anchor table; L-24 `d2` self-contained, never through `base_multiplier`; off-default intake L-04/05/06 refusing.
- **`1a4bee308` WARN-1** (§ 6): static pre-count, landed-row recorder, bounds.
- **`1a4bee308` WARN-2** (§ 7): the (b) sub-count format, with forced or reach controls.
- **INFO-1** (Elemental split by GD's rule, § 5) and **INFO-2** (one lock primitive and per-frame order, § 3).

## WARN-1 — r_DMG PRIMARY pairs maxima while r_HP pairs medians. That asymmetry favours her survival, and the fidelity line must say so

`anchor_r_hp` is **median ÷ median** (GD trash HP ÷ D2 normal HP, R1). `anchor_r_dmg` PRIMARY is **GD max slot ÷ D2 best attack**. The statistic-matched counterpart to r_HP is a central-tendency pair: ADDENDUM-5 already prints **mean ÷ mean = ×78.58**. So:
- **her offense is anchored at typical enemy scale;**
- **her life (and heals and absorbs) at extreme enemy scale.**

The result is ×1.24 more anchored life than the statistic-matched arm, and ×2.07 more than use-weighted.

Calling PRIMARY a "worst-case pairing" is correct for *damage*, but it is the **best case for her survival**. Read unlabelled, it reverses the reader's intuition.

KP-430 keeps PRIMARY as the result of record (a conductor ruling; I do not override it). **Before the prereg:**
- (a) the fidelity line states the direction: *"PRIMARY favours her survival relative to the statistic-matched (mean÷mean ×78.6) and use-weighted (×47.0) anchors"*;
- (b) mean ÷ mean is printed beside PRIMARY and USE-WEIGHTED, as the arm whose statistic matches r_HP's;
- (c) the M-a "un-predicted at PRIMARY" line carries the same note.

## WARN-2 — The quantile anchor (L-24 `ar_anchor = quantile`) is not yet specified tightly enough for bit-exact engine and port, or for the attackers it will meet

**The choice itself is sound.** The linear map reproduces D2's median CtH on her, but compresses the IQR from 6 to 3 and the range from 23 to 7. A rank-preserving map onto D2's AR distribution, with mlvl fixed per role (85/87/88), reproduces D2's marginal. It is labelled JUDGED, the #12 shift is named (scalars `anchor_r_ar` / `anchor_r_lvl` → ECDF tables, kept as the linear sensitivity rows), and the raw refusal stands. Four specification gaps remain:

1. **Population.** `F_𝔊,role` is built over the **95 BOARD cells**. The intake attackers in her runs include **pets/summons, the pre-pass bodies and REF-only bodies** (step-2b population; the drain carriers in § 6 are REF/summon bodies). State:
   - the attacker population the ECDF covers;
   - the **role** of a summon or pet (no role pair is declared for it);
   - and **refuse at bind** for any attacker record with no role, rather than defaulting it.
2. **Out-of-range and tie rules.** GD OA is narrow and **heavily tied** (bodies of one record share one OA). Declare:
   - the ECDF convention (right-continuous, or mid-rank for ties);
   - the quantile interpolation (lower, nearest, linear);
   - and the clamp for an OA outside the ECDF's support.
   
   These decide the realised per-body AR and must be identical on both mirrors.
3. **Weighting coherence.** `F` is body-weighted, while `Q` is slot-weighted over D2 rows. The marginal is reproduced "by construction" only under those weights. At run time the weight is **landed attacks**. Print the landed-attack-weighted CtH distribution beside the construction-weighted one.
4. **The D2 unique AR distribution is owed (stage 6).** Boss/nemesis taking the champion distribution is labelled. Name it as a known interim on the fidelity table.

## WARN-3 — `physical_contact` must count Pierce: 21 GD projectile slots are Pierce-only

The predicate "a melee weapon swing, **or a projectile with a non-zero Physical component**" decides two things: whether a hit rolls (rather than auto-hitting at CtH 100) and whether it is blockable. Pierce **maps to her physical DR** (row 25), and a GD Pierce projectile is the analogue of D2's physical arrows and spikes, which do carry `ToHit`. Yet:
- `pm2_tg2_attack_damage.csv` has **543 projectile slots (`Skill_AttackProjectile*`): 251 with Physical, and 21 that carry Pierce without Physical** (e.g. `dermapteran_madqueen_stinger_burst`, `fabius_bladenova_proc`);
- under the predicate as written, those 21 **auto-hit her and cannot be blocked**.

*Action:* `physical_contact` = weapon swing **or** a projectile whose damage rows include **Physical or Pierce** (state Bleeding's treatment too). Re-count the roll and block sets.

## Checks requested

**(1) The quantile anchor and its #12 shift: SOUND IN KIND; tighten per WARN-2.**

**(2) The L-24 additions: SOURCED and correctly composed.**
- **Monster spells auto-hit.** Only `ToHit` missiles roll (71/684).
- **Running auto-hit.** `PLRMODE_RUN` in melee `GetResultFlags`; Basin's running exemption.
- **The sealed d100 is still drawn and ignored** on auto-hit rows, so no stream moves.
- **G1 `autohit=1`.** The J3-INTAKE-ROLL tripwire counts rolled rows only, so it stays 0 by construction.
- One predicate serves the roll set and the block set (subject to WARN-3).

**(3) The action-lock precedence: SOUND.** DEATH > CONTROL_GD > HITREC = BLOCK > CAST:
- interruptible casts are pre-empted, and a cast pre-empted before its action frame spawns no missile, with the mana spent (refund is a named operand);
- a blocked hit never causes hit recovery; an unblocked hit during BLOCK switches the mode;
- under `d2` a stun does not end a whirl; under `gd` a control lands and ends it (JUDGED, labelled);
- freeze and chill fold into one chill;
- the gates are counted on a per-frame lock log.

*INFO-1:*
- declare whether **a block can be rolled while she is in HITREC** (the D2MOO block gate's mode conditions);
- declare **how a GD world-tick attack is placed on the D2-frame timeline** (e.g. assigned to the first frame f with `ceil(f·AS/400)` = k, with all intake ordered before her action poll within that frame). Both are bit-exactness items for the row replay.

**(4) P-1…P-8 forms and controls: SOUND.**
- **P-2 `d2-strict` is the right default** under KP-420 (D2 has no player sleep, trap, petrify or root, so dropped and counted; the damage still lands). `d2-nearest` is a DECLARED-INVENTED sensitivity. An unmapped family refuses at bind.
- **The forced-landing control** (8 families × 3 settings, row identity, a fail-first registry deletion) plus the reach count is exactly WARN-2's form. Row 22 → REACHED-INSENSITIVE (named) if the reach is 0.
- **P-3:** the DoT receiver law (replace-if-stronger on the post-mitigation rate; the poison floor at `1·r_DMG`; unmapped forms routed to burn, DECLARED). It is graded **per landed application**, not on survival-confounded totals.
- **P-4:** chill length is DECLARED from the R1 cold-attack median (100 frames). Casting is unslowed (sourced), so KP-426's cadence coupling is correctly zero.
- **P-6:** the banner goes additively into row 5's pool (×1.27–1.28), with the multiplicative sensitivity. A blocked hit does not trigger Cruel, a #12 shift that is declared.
- **P-7 / P-8:** row-identity controls. P-8 shares one regen function with her H09.

*INFO-2:* confirm that P-8's `max(1, floor(max_256/3000))·(100+bonus)/100 + manarecovery` **is** the D2MOO line ADDENDUM-1 § E transcribes for her, so the two kits run one function, not two near-copies.

**(5) The row-25 completeness refusal: RIGHT.** One home for the map, checked at bind (`IntakeFamilyUnmapped`), with a fail-first entry deletion. *INFO-3:* the check must enumerate **both** halves of `threat.load_profiles()` (roster **and** pet profiles), plus the DoT-corrected families. The same population rule applies to P-2's and P-3's bind-time registries.

**(6) Anchored life 97,453 / 47,167 vs 20,005: CORRECT** under the unit rule:
- 1,004 × 97.0646 = 97,452.9 and 1,004 × 46.979 = 47,166.9. Life is a kit-life quantity (× r_DMG), which preserves hits-to-die against her D2 home.
- The fidelity line that the attack **rate** stays GD-native (time-to-die not anchored on the rate leg) is right and necessary.
- The per-family EHP parity points recompute: 19.925 × (1−res_her)/(1−res_his) gives fire 79.7, Elemental 56.5, cold/lightning/poison 44.8.
- The magic-absorb exclusion is properly costed: ≤ 777 / 376 GD HP per magic-family hit (KP-431).

**(7) Predictions: PAIRED TOTALS / ROW IDENTITY throughout.**
- M-a is un-predicted at PRIMARY, and LOWER at USE-WEIGHTED conditional on the pre-run G2-weighted `r_DMG*`. Correct, with the condition computed before any run.
- *INFO-4 (the J3a lesson):* **"survival monotone non-decreasing in r_DMG" across arms that differ by < 2 %** (mean÷mean 78.58 vs basic 79.04; R2/R3/R4 81.6–89.4) **will be decided by trajectory noise, not by r_DMG.** Register the ordering only between **well-separated** arms (e.g. use-weighted 47.0 vs PRIMARY 97.1, or vs mean÷mean 78.6), and declare the near-ties un-predicted.

## Before the port sites go to Matt
- One consolidated site table with **unique ids**:
  - the original `f72316b7` § 4 kit sites;
  - ADDENDUM-3's site-10;
  - ADDENDUM-4's site-11…16;
  - and the sweep items mapped onto them.
  
  Each carries its guard form and its predicate-at-defaults (the KP-360 shape).
- **site-16 (the drain recorder):** state whether it is a **port** site (counting under her port-emitted profile) or an engine-side read of oracle run attributes (no port edit). Only the former needs a Matt ruling.
- Fold WARN-2 and WARN-3 into the site behaviour first. They change what site-11/14 and the L-24 branch compute.

## Action
- [ ] gamora: ADDENDUM-6 (binding corrigendum, alone) folding WARN-1…3 and INFO-1…4, plus the consolidated site table. Then the J4b prereg.
- [ ] legolas: stage 6 (the D2 unique AR distribution), plus the owed list (ADDENDUM-4 § 10).
- [ ] conductor: note WARN-1's direction on the KP-430 line.
- [ ] Matt: the consolidated port-site list once WARN-2/3 are folded; nothing before.

## References
- engine `e96c96a9`, `8c922eb1`, `94ed4e42`; `data/kc2/pm2_tg2_attack_damage.csv` (the projectile census above, read-only)
- collab `agentic_orchestration/legolas/research/2026-10-14-join1-c13-enemy-anchor/README.md` §§ 6–7 (block, hit law and running exemption sources), `r_dmg.json`
