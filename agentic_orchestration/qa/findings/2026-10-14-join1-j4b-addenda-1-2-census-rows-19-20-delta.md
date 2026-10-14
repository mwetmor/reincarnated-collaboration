# Finding — 2026-10-14 — JOIN-1 J4b ADDENDUM-1 + ADDENDUM-2 and the Sorceress census rows 19/20, delta Gate-1

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: the enemy-anchored design and both new rows are sound in kind; two WARNs before the J4b prereg)
**Target:** engine `4cabc43d` (ADDENDUM-1), `20ff8684` (ADDENDUM-2); collab `20790cd34` (census § 7, row 19), `9096b2e97` (census § 8, row 20); against my Gate-1 `2c5413335`
**Rulings in force:** KP-420 (Matt), KP-421, KP-422, KP-423 (row 21 pending; a later delta)
**Developer:** gamora / elrond · conductor gandalf
**Principles applied:** 1, 3, 4, 5 · Disciplines #10, #12

**Key:** **[C-13]** = the item depends on legolas's enemy-anchor numbers, not yet bound.

**My Gate-1 is discharged:**
- WARN-1 (rotation under refusal) by ADDENDUM-1 § E (a)–(c), with the realised ratio predicted;
- WARN-2 (one integer timeline, absolute offsets, integer regen transcribed from D2MOO);
- INFO-2/3/4/6/8/9 and the yard set.

## WARN-1 — L-22 `magnitude_anchor`: its scope and application points are incomplete after ADDENDUM-2

ADDENDUM-1 § B says L-22 applies "at the adapter boundary … never inside GD law", and defines the raw line as `r_HP = r_DMG = 1` with "`DA_kit` from raw D2 defense". ADDENDUM-2 then adds two **enemy-side** anchors, `r_AR` and `r_LVL`, applied **per body inside the intake resolve** under L-S6 `d2` (`AR_eq = OA_body·r_AR`, `mlvl_eq = level_body·r_LVL`), and retires the DA-solve as her setting. Three gaps follow:

1. **What `raw` does to `r_AR` and `r_LVL` is unstated.** If raw sets them to 1, GD OA enters D2's equation as if it were D2 AR. That is a units claim, not a raw measurement. If raw keeps them, raw is not raw.
2. **L-22 has two application points, not one:** (i) the kit's magnitudes at the adapter boundary; (ii) the enemy's attack operands inside the L-S6 `d2` form. State both. The second is legitimate (it is the D2 law's operand, not GD law), but "never inside" is false as written.
3. **The `gd` setting's Defence → DA solve must carry the label DECLARED-INVENTED** wherever it runs (census § 8.1, P0 § 7.1). ADDENDUM-2 calls it "this setting's operand mapping".

**Linear ratio scaling of OA → AR and level → mlvl is itself a JUDGED functional form [C-13].** Print it as such, with the two games' distributions beside it.

*Action:* the prereg gives L-22 a table: every anchor (`r_HP`, `r_DMG`, `r_AR`, `r_LVL`, the CtH solve), its value under `raw` and under `enemy-anchored`, and its application point.

## WARN-2 — Row 20 `d2`, composed from L-04/L-05/L-06, inherits GD's sub-70 damage scalar; and NC-J4b-ROW20's direction argument does not hold

**The rulebook's row-2 form at the pin `3eefaa2e`** (`forms.resolve_hit`) returns `base = crit.base_multiplier(p)` under L-06 `no-roll-no-crit`, and `base_multiplier` is **`p/70` when p < 70** (`crit.py:224`). Composing `d2` as {L-04 floor 5, L-05 ceiling 95, L-06 `no-roll-no-crit`} therefore scales every landed hit with CtH < 70 by CtH/70: ×0.07 at the 5 % floor. **D2 has no such term:** a landed hit deals its damage, multiplier 1.0, as the row-20 law states. This could easily be the dominant intake effect at D2 CtH values against a defensive sheet **[C-13 for how many bodies sit below 70]**.

**NC-J4b-ROW20's prediction is Σ intake (`gd`) ≥ Σ intake (`d2`), on the ground that `gd` "can only add hits and multipliers".** That ignores the same scalar on the `gd` side. For 55 ≤ PTH < 70, `gd` multiplies damage by PTH/70 < 1. The direction is not implied, so as reasoned it may be false.

*Action:*
- make L-S6 `d2-ar-def` **self-contained**: equation, integer floor and clamp (5–95), `roll ≤ CtH`, multiplier exactly 1.0, no tier, no sub-70 scalar. Grid it.
- Re-derive NC-J4b-ROW20's direction from both settings' actual forms, or declare it unpredicted with the per-body PTH/CtH distributions printed.

## Checks requested

**(1) The unit rule (r_HP for enemy-damaging quantities, r_DMG for kit-life ones): SOUND as a single discipline.**
- Kit damage × r_HP preserves hits-to-kill on a zero-resist body. Kit life × r_DMG preserves hits-to-die.
- Dimensionless and kit-internal quantities cross natively.
- Cross-unit comparisons are consistent. The FHR threshold `dmg_GD > life_GD/12` ⇔ `dmg_GD/r_DMG > life_D2/12`. L-21's softhit test compares scaled damage to GD HP, which preserves the D2 ratio.

**INFO-1, for the inheritance clause (§ H 2):** "leech computed in D2 units then ×r_DMG" must be written explicitly as `leech_GD = pct · (dealt_GD / r_HP) · r_DMG`. The naive `pct · dealt_GD` is off by r_HP / r_DMG. The Barbarian (WW leech) is where this binds.

**INFO-2 [C-13]:**
- r_DMG must be computed on **the same quantity** in both games: raw pre-mitigation damage per landed hit, across families.
- Native resists against GD's family mix make the JUDGED GD-only family map (Pierce/Bleeding → DR%; Aether/Chaos/Vitality → magic res) a material term. **Print the intake share by family** beside the main result.

**(2) L-22: well-placed** (a rulebook lever; `NONE — no GD rule` at the referent; default `enemy-anchored` for D2 kits per KP-420; one game-pair `ANCHOR` layer, not per kit). Subject to WARN-1. NC-J4b-ANCHOR's predictions (applied damage moves by r_HP; survival with r_DMG) are falsifiable once the ratios bind **[C-13]**.

**(3) Row 20's two settings and J3-INTAKE-ROLL: CORRECT, apart from WARN-2.**
- Under `d2`, the 95 cap makes PTH ≥ 100 impossible, so the tripwire is 0 **by construction** (reported as such), and the decoded GD roll is inapplicable (D2 rolls `d100 ≤ CtH`; no tier).
- Under `gd`, the tripwire is **live**, reported per body. A body ≥ 100 is J3-INTAKE-ROLL's case: a named finding, then a lever build.
- No new draw stream: the sealed `randint(1,100)` is reused. `roll ≤ CtH` matches D2's 0–99 < CtH.
- Row 35 binding `PTH_MINIMUM` = 5 with every summon pth ≥ 122.04 passes `SplitRecordRefused`.

**INFO-3:** fix the D2 order **hit → block → damage** in the intake resolve (census § 8.1), and predict the draw count: `block:<kit>` draws == landed **blockable** hits, excluding hits that land during BL.

**(4) Registration. Recommendation: two NEW ids, and the D2 intake law in ONE home.**
- **Row 19 → new id (L-S5 → L-23 `player_block_model`).** No existing lever carries a block model.
  - I confirm the class WIDEN. `PLAYER_BLOCK_PCT` is read nowhere on the fight path: only its declaration (`threat.py:126`) and a report field (`:2317`).
  - Its GD default is a **measured** 0.0, so `gd` reproduces REFERENT-v1 (elrond § 7.2's reasoning is right).
- **Row 20 → new id (L-S6 → L-24 `intake_hit_law`)**, intake-only by definition. That satisfies W1's "per direction" requirement **without** distributing one D2 law across L-04/L-05/L-06.
  - When L-24 = `d2-ar-def`, any off-default **intake** setting of L-04/L-05/L-06 **refuses** at bind, so the law has one home (the § 4.1 intake-order precedent).
  - This is also the cleanest cure for WARN-2.
  - L-04/L-05/L-06 keep their intake-lane GD-side meanings unchanged.
- **Denominators 20 / 12 are correctly recorded as named findings** against the J0 anchor (`b48500a4d`), with reasons. Coverage becomes harder, not easier, before grading. **ACCEPTED.**

**(5) Row 21 (potions) by a JUDGED drink policy: ACCEPTABLE IN PRINCIPLE**, as a declared **pilot policy**, the same shape as ADDENDUM-1 § E's rotation rows. Five conditions, to be checked at the row-21 delta:
- (a) elrond classes the row first; no design ahead of the census.
- (b) **Supply is declared:** belt capacity, potion tiers, whether the belt refills between waves (D2 home potions are finite; GD's Warlord potion is cooldown-limited). The asymmetry is printed.
- (c) **Units:** health and rejuvenation life restore are kit-life (×r_DMG); mana restore is native. D2's heal-over-time profile goes through the integer frame law.
- (d) The drink thresholds are policy rows, with **no-potion** and an alternate threshold as printed sensitivities.
- (e) The Meteor-starvation and M-a predictions are re-registered before any run, as ADDENDUM-2 § 5 already commits.

## Also noted
- **ADDENDUM-1 § C block law** (75 % cap, full negate, BL by FBR through the integer law, no casting during BL, the JUDGED blockability split) and **§ D's sheet derivation** (Hell penalty, her cap rather than GD's 80, applied once) are sound, with the sourcing owed to legolas.
- **KP-422's stat allocation** is labelled JUDGED, with max-block and no-Dex sensitivities. Right.
- **Fractions (a) 20/20 and (b) 12/12** are predicted with the row-9 caveat and named shortfalls. Right.

## Action
- [ ] gamora: the J4b prereg folds WARN-1 (the L-22 anchor table; DECLARED-INVENTED label), WARN-2 (self-contained L-24 `d2`; NC-J4b-ROW20 re-derived), INFO-1 and INFO-3. Registration per (4) at the Gate-2 that registers the ids.
- [ ] elrond: row 21 class (KP-423).
- [ ] legolas: C-13 numbers, plus the block, FBR and intake-hit-law sources.
- [ ] Matt: none new.

## References
- engine `4cabc43d`, `20ff8684`; rulebook pin `3eefaa2e` `src/join2_rulebook/forms.py` (`resolve_hit`), `crit.py:224` (`base_multiplier`); `src/reincarnated/simulation/kc2/threat.py:126, :2317` (read-only)
- collab `agentic_orchestration/elrond/notes/2026-10-01-join1-j0-sorceress-census.md` §§ 7–8; my Gate-1 `qa/findings/2026-10-14-join1-j4b-fire-sorc-adapter-gate1.md`
