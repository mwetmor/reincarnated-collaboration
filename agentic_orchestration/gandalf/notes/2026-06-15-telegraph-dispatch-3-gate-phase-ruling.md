# Gate-phase ruling — telegraph combat-model (dispatch 3): W-C RESOLVE-cert, not full W-F

**Type:** gandalf design ruling → KR orchestration input (telegraph/dodge wave, dispatch 3 fire-moment).
**Date:** 2026-06-15 (Pattern-B with Matt — KR surfaced the gate-phase question as "gandalf or you")
**Author:** gandalf (story-and-design steward)
**Authority:** gandalf design call per the telegraph ruling §6/§7.4; KR + jack-ryan did the analytical legwork and landed the conservative read; this ratifies it with the design-side reason + resolves the one open input.
**Parent docs:**
- `canonical/story/telegraph-dodge-temporal-decoupling-2026-06-15.md` (v1.1) — §6 (build on certified 2D engine), §7.4 (single geometry source, spatial-minted)
- `canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` — §5 wave structure (W-A…W-F); the RESOLVE/MEASURE two-cert split (lines 138-143); type-wall is W-B

---

## 0. TL;DR

**Dispatch 3 (gamora telegraph combat-model) fires at W-C RESOLVE-clear, NOT full W-F.** W-F (1D deletion) is later hygiene, not a precondition. Two conditions gate it — one already met, one a single gamora confirmation:

1. **Type-wall enforced — ALREADY MET.** The type-wall (`CommitGradeVerdict` vs `SearchGradeEstimate`) lands at **W-B**, two phases upstream of W-C (cert-wave §5; W-B exit gate IS the §3.1 type-error test). So §7.4's "spatial-minted, never 1D-minted" requirement is structurally satisfied the moment W-C is reached. No action.
2. **K4≥K2/M1 confirmed orthogonal to danger-zone-SHAPE production — one-line gamora confirmation.** Orthogonal-by-design if it is an outcome-CREDIT/attribution finding; relevant if it is a spatial-POSITIONING/geometry defect. The terminology ("movement-*credit*") leans orthogonal; confirm, don't assume.

If both hold → dispatch 3 fires at W-C-clear. The telegraph never touches W-D/W-E/W-F.

---

## 1. The question (KR's, verbatim in substance)

> The telegraph is combat-RESOLUTION geometry — a RESOLVE-cert property (W-C, already passed), not a behavioral-identity-MEASURE property (W-D/W-F). Can dispatch 3 fire once the engine is RESOLVE-certified (W-C-clear), or must it wait for full W-F (1D deleted)? And: does the pending W-C K4≥K2/M1 movement-credit gap touch the telegraph's geometry surface, or is it orthogonal?

KR + jack-ryan landed the conservative read (W-C is the natural gate) and flagged it as a design call. It is. Here is the ruling with its reason.

## 2. Ruling — W-C RESOLVE-clear is the gate

Dispatch 3 fires when the spatial engine is **RESOLVE-certified clean on the geometry surface the telegraph consumes** (W-C). It does **not** wait for W-D (commit-grade BC tuple), W-E (throughput), or W-F (1D deletion).

This is not "W-C is good enough as a compromise." It is "W-C is the *correct* dependency and the later phases are about a different surface."

## 3. Why — the RESOLVE/MEASURE split is exactly this distinction

The cert-wave doc already draws the line the telegraph needs (§5, lines 138-143):

- **RESOLVE (W-C exit):** does the engine produce the right *fight outcome / spatial behavior* — where an attack lands, when, the arena physics. This is the telegraph's whole substance: **danger-zone SHAPE + wind-up TIME per boss attack.** The telegraph is RESOLVE geometry by definition.
- **MEASURE (W-D/W-F exit):** does the engine produce the right *behavioral-identity tuple* — the 8-axis BC kit-identity record. The telegraph is **not** a kit-identity record. It needs nothing from the MEASURE cert.

So the telegraph's dependency lands entirely inside RESOLVE (W-C). MEASURE (W-D/W-F) is a different cert about a different artifact (kit identity), and the telegraph does not read it.

**The §7.4 drift-proofing requirement is satisfied at W-C, not at W-F.** §7.4 requires the telegraph geometry be *spatial-minted, never 1D-estimator-minted*. The control that guarantees this is the **type-wall** (`CommitGradeVerdict` minted only by the spatial path; feeding a `SearchGradeEstimate` is a type error) — and the type-wall is **W-B** (cert-wave §5; the W-B exit gate is the §3.1 type-error test passing). W-F merely *deletes* the 1D engine; it adds no safety the type-wall hasn't already provided. By the time W-C is reached, the wall is up two phases back. **1D deletion is hygiene, not a gate for the telegraph.** Requiring W-F would be requiring the *cleanup* of a hazard the *wall* already contains — belt where the type-wall is already the suspenders-and-belt.

## 4. The K4≥K2/M1 disposition — orthogonal-by-design, one confirmation owed

The telegraph's geometry surface is **danger-zone SHAPE production** — where an attack's footprint falls in 2D space, and the wind-up time. Under the temporal-decoupling design, the sim *mints* this geometry; the piloted Godot game *owns the dodge-resolution* (the player moving out of the zone is the player's skill check, not the sim's). So two surfaces must be distinguished:

- **Telegraph geometry surface** = attack danger-zone SHAPE (+ TIME). What the sim exports.
- **Movement-credit** = does the engine correctly *credit a combatant for moving* (kiting → reduced damage / better survival). A fight-OUTCOME attribution property.

**These are orthogonal by the decoupling.** Movement-credit is a RESOLVE-quality property of the sim's internal balance estimate (it touches the sim's win-rate / survival numbers for non-piloted combatants); it is **not** the danger-zone geometry the telegraph exports to Godot. The sim does not resolve the player's dodge for the telegraph path — Godot does — so a sim-side movement-credit gap does not propagate into the exported shapes.

**The one case where it would be relevant** — and the single thing gamora must confirm: if K4≥K2/M1 is not an outcome-*credit* finding but a spatial-*positioning* defect (the engine mis-placing entities in 2D space), then danger-zone SHAPE production could be downstream of the same defect, and the telegraph would inherit it.

**Confirmation gamora owes (one line):**
> Is K4≥K2/M1 a fight-OUTCOME credit/attribution finding (kiting under-credited in win-rate/survival → **orthogonal**, fire dispatch 3), or a spatial-POSITIONING/geometry finding (entities mis-located in 2D → **relevant**, the telegraph inherits it, clear it first)?

The word "credit" leans orthogonal. But this is load-bearing to a build, so it is a **hard gate**, not an assumption — gamora answers it before dispatch 3 fires, not after.

## 5. What KR does with this

- **Dispatch 3 gate = W-C RESOLVE-clean on the geometry surface**, bounded by one gamora confirmation:
  - If gamora confirms K4≥K2/M1 is outcome-credit (orthogonal) → **W-C is already passed; dispatch 3 fires now.**
  - If gamora reports K4≥K2/M1 is spatial-positioning (relevant) → **dispatch 3 fires once that finding is dispositioned** (still W-C-bounded; still not W-F).
- **Either way, dispatch 3 is decoupled from W-D/W-E/W-F.** The telegraph never blocks on the BC tuple, throughput, or 1D deletion.
- **This does not change dispatches 1, 2** (cert-independent, already firing) or the W-D-gated cert sequence itself (the K4≥K2/M1 disposition before W-D remains its own call — this ruling only settles whether that disposition also gates *the telegraph*, and the answer is: only if it's a positioning defect).

---

**Signed:** gandalf, 2026-06-15
**For:** ruling the telegraph combat-model's fire-moment at W-C RESOLVE-clear (not full W-F) — because the telegraph is RESOLVE geometry (danger-zone shape + time), the type-wall that satisfies §7.4 is already W-B (two phases upstream), and 1D deletion is hygiene not a gate; with the K4≥K2/M1 movement-credit finding ruled orthogonal-by-design to the telegraph's geometry surface (the sim mints shape, Godot owns dodge-resolution), gated on one gamora confirmation that it is an outcome-credit and not a spatial-positioning defect.
