# Finding — 2026-10-08 — JOIN-1 J3d close-out (pin `a8e11af6`), Gate-2

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: everything passes except the new `pct-resist-only` arithmetic, which must be fixed before drax mirrors the L-08 form)
**Target:** engine `904ce71d` (AMENDMENT-1), `0bfb9581` / `5c7b2254` (fail-first, amended), `f82fa527` (AMENDMENT-2), `a8e11af6` (rulebook), `43954d1a` (grids), `31ffe488` (MIGRATION), `5e9b0469` (N-5); collab `5a6aa27cc`
**Developer:** gamora · conductor gandalf (KP-399…403)
**Principles applied:** 1, 2, 3, 5 · Disciplines #10, #12

## WARN-1 — `pct-resist-only` is not exactly 0.0 at DR ≥ 100, and can go NEGATIVE, which heals the target

`forms.proportional_applied` computes:

```
dr = min(res + bonus, 100.0)
return raw - raw * dr / 100.0   # when dr > 0
```

At dr = 100, `raw*100.0/100.0` is not `raw` for about **13 % of f64 raws**. I sampled 200,000 values; 26,550 left a residue, for example:
- `3968.871309542402 → +4.5e-13`
- `3304.079298603607 → −4.5e-13`

The grid passed only because its 8 immune raws (50, 100, 250, …) happen to be exact.

Two consequences:
1. **The AMENDMENT-2 § 3 invariant "DR ≥ 100 is exactly 0.0" is false.**
2. A negative `prop_applied` flows through `min(pa, hp_now)` in `hit_with_proportional`, so **HP rises**.

`floor=True` (D2's integer CB) is exact, but the form's default is `floor=False`.

**Fix (one line, before drax mirrors the form):**

```
if dr >= 100.0: return 0.0
```

then `max(0.0, raw - raw*dr/100.0)` for 0 < dr < 100. Add grid rows with non-dyadic raws, including the two above, at dr ∈ {100, 99.99999999999999}. Then re-certify and move the pin.

## Checks

**(1) WARN-1 of `b06a4344c` is fixed.** G-L02-1 is 3,168 / 3,168 bit-exact against the real `PlayerOffense.damage_against`, across k ∈ {None, 1, 0.93, 1.07}, banner ∈ {1, 1.15} and aura ∈ {0, 12} (`grids.json`, `L-02-sealed`, `n_bad` 0).

**(2) The ADJ-J4 re-basing is correct.** `hit_with_proportional` with `before` does three things in order:
- the proportional packet goes first, on **pre-hit** HP, capped at HP;
- the weapon packets are then capped to the remaining life;
- `leech = weapon applied total`, plus the proportional packet only if `l07_leeches = yes`.

So the lowered leech cap emerges from the order, and G-ADJ-J4-cap gives 125. The sources are cited (D2MOO 1.10f, plus SECONDARY ×3). `after` is kept as a declared alternate.

**INFO-1 (J4):** the form is deterministic per hit. D2's CB is one roll per hit (`rand % 100 < CB%`). J4 needs a JOIN draw for it (S-5 class) or a declared expectation form. N-5 lists the fact; the mechanism is not chosen yet.

**(3) `pct-resist-only`** is ratified in the decisions-log (this date), **conditional on the WARN-1 fix**.

**(4) The integer floor is SOUND.**
- I checked `floor((100/div)/100 · hp) == hp // div` for every divisor 3–30 and every hp from 1 to 200,000: **0 mismatches**.
- **INFO-2:** D2 reduces CB by DR in integer arithmetic (`CB − CB·DR/100`, truncating). The float form gives 87.5 where D2 gives 88 at CB 125, DR 30. Declare this as JUDGED, or add an integer-DR option at J4.

**(5) Certification holds.**
- P-J2-9 `pass: true`.
- GM 7/7 (provenance `a8e11af6`).
- § 4.7 v4 BYTE-IDENTICAL, with HEAD start = end = `a8e11af6` and the kc2 tree unchanged.
- The rulebook diff from `d5384b4b` is **146 insertions, 0 deletions**.
- No `kc2/**` diff.

**(6) The two grid fixes are acceptable.**
- The added straddle row turned a vacuous G-L02-5 (0 rows) into 40/40.
- The G-L02-4 check was tightened to the preregistered exact form.
- Both strengthen the checks, and both were declared before the generator commit.

**(7) MIGRATION `247b879a` DISCHARGES my J3b close-out WARN-1 (`bb6a86230`).**
- (a) The port refusal now reads "until S-7 **and** the row-36 mirror". Row 36 is in the P0 inventory, with "no consented site: in-form hook or a Matt ruling".
- (b) It restates the full KP-360/363 scope, plus the summon emitter re-evaluation item.
- `31ffe488` carries both forward.

## Action
- [ ] gamora: the WARN-1 fix (+ grid rows), alone; re-certify; MIGRATION names the new pin. Declare INFO-2.
- [ ] conductor: INFO-1 into J4a.
- [ ] Matt: none.

## References
- engine `a8e11af6:src/join2_rulebook/forms.py` (`proportional_applied`, `hit_with_proportional`); `grids.json` (`L-07/08` immune rows); MIGRATION `247b879a`, `31ffe488`
- engine `design/decisions/decisions-log.md`, entry "L-08 third value `pct-resist-only`" (this date)
