# Architectural Grammar — columns & arches as coherent built structure (the Synty cathedral-ruin rule)

**Type:** gandalf design ruling → Drax build brief (WS2 second wave) + Galadriel review commission.
**Date:** 2026-06-15 (Pattern-B with Matt — second-wave battle-room presentation pass)
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-15 verbatim — *"the colums themselves are never standing alone (unless it is rubble) and they are part of the structure of the walls… the arches should either be used across wall tops as windows or across columns as a separate 'wall' set which is decorative but still physically bounded and built as if it was actually made as a coherent structure. Think of real architecture and use these assets as they would need to be used on a real physical building."*
**Parent:** `canonical/story/battle-room-presentation-decoupling-2026-06-15.md` (this is a §2-adjacent refinement — it constrains HOW the wall ring + annulus dressing use columns and arches; it does NOT touch the sim-invariant). Folds into that canon once Drax builds + Galadriel validates (recognition→validate→commit).
**Reference:** POLYGON Dark Fantasy crypt scene (Image #65 — the canon we replicate).

---

## 0. TL;DR

Columns and arches in the battle-room must read as **a real building that could stand** — a coherent load path, not scattered decorative verticals. Two rules:

1. **Columns never stand alone.** A column either CARRIES something (an arch, an entablature, a rail) or it IS rubble (fallen, broken, on its side). No upright orphan columns.
2. **Arches never float.** An arch either (a) tops an opening in a wall plane (a **window**, with masonry continuing above/beside — this is what motivates the god-rays), or (b) springs column-to-column in a regular rhythm as an **arcade** (a see-through but physically-bounded screen-wall), or (c) spans between two wall masses as a **gallery/bridge** at an upper level. Every arch lands on a real support at BOTH ends.

The governing invariant: **coherent load path — every arch springs from something at both feet; every column carries something or is rubble; no orphan verticals, no floating spans.** Plus a floor-color coherence fix (annulus floor = playable floor; restores the Layer-2 invisible-sub-region read).

---

## 1. My reading of the reference (the architectural inventory of Image #65)

The reference is a **ruined gothic cathedral / crypt bay.** Its architecture is doing five specific things we have under-used:

| Element | What the reference does | What we must replicate |
|---|---|---|
| **Pier → arch → wall** | A compound pier at the left springs a pointed, **traceried** gothic arch set INTO the wall plane (masonry above + beside it). | Arches as openings IN walls, not free shapes on top of walls. |
| **Arcade** | Behind the front arch, a receding series of arches on columns — an aisle/cloister screen. | A regular rhythm of arches on columns forming a see-through bounding wall. |
| **Gallery storey** | A raised walkway (statue + gold votives, top-right) ABOVE the fighting floor, with an edged balustrade, reached by stairs. | Multi-level structure — the grandeur is that the building has floors. |
| **Balustrade** | The tomb has balusters (little columns) carrying a rail. | Columns-in-railings as a third structural use. |
| **Coping + rubble** | Low boundary walls topped with hexagonal capstones; the only loose stone is FALLEN rubble (broken drums/blocks). | Built low walls with a top course; loose verticals only as fallen rubble. |

**The load path reads.** Piers rise → arches spring between them → wall infills between → a gallery sits on the lower structure → light enters through the arched openings. You believe it was built. That belief is the target — it is the difference between "a place" (the iter2fix verdict) and "a real place."

## 2. The COLUMN rule

A column may appear ONLY in one of these four roles. Anything else is forbidden.

1. **Pier (carries an arch).** A column/compound-pier standing at the springing point of an arch, bearing it. Always paired with the arch it carries.
2. **Arcade member (carries the arch run).** One column in a regular rhythm of columns carrying a continuous arch run (see §3b). Spacing regular; never one-off.
3. **Engaged column / pilaster (in the wall).** A column set against or half-buried in a wall plane as articulation — reads as part of the wall, not free-standing.
4. **Baluster (carries a rail).** A short column in a railing/balustrade on a raised-level edge or a tomb (see the reference's sarcophagus rail).

**FORBIDDEN:** a free-standing upright column carrying nothing. The ONLY free-standing-on-the-ground stone vertical allowed is **RUBBLE** — a fallen column drum/fragment, on its side, broken, scattered. Rubble reads as collapse, never as a standing element. (We already removed broken Synty cape attachments to bake clean; this is the same discipline applied to columns — an upright orphan column is a "broken attachment" of the architecture.)

## 3. The ARCH rule

An arch may appear ONLY in one of these three roles. Anything else floats and is forbidden.

- **(a) Window-in-wall.** The arch is the head of an opening cut into a wall plane. Masonry continues ABOVE the arch and to BOTH SIDES; the arch springs from the wall jambs or from engaged columns. Add tracery where the asset supports it. **This is the god-ray motivator** — light enters the room through these openings, so position them where the establishing camera's light shafts can pass through.
- **(b) Arcade (arch-across-columns screen).** A regular rhythm of arches, each springing from one column to the next, forming a continuous colonnade. It is decorative and see-through but **physically bounded and structurally complete** — every arch lands on a column at both feet; the run begins and ends on a column or a wall mass (no half-arch dangling into space). This is Matt's "separate 'wall' set… built as if it was actually made as a coherent structure." Use it as a second, inner bounding screen inside the outer wall ring, or to wall a gallery edge.
- **(c) Gallery/bridge span.** An arch spanning between two wall masses at an upper level, carrying a walkway or reading as a flying span. Both ends land on a wall mass or pier.

**FORBIDDEN:** an arch sitting on top of a wall as a free silhouette with nothing springing it; a single orphan arch with one or both feet landing on empty floor; an arch whose span doesn't correspond to the gap it bridges.

## 4. The load-path invariant (the one test)

Before placing any column or arch, ask the single question that makes the building real:

> **"If this were stone and gravity were on, would it stand — and is it doing a job?"**

- Every **arch** springs from a real support (pier / column / wall jamb / wall mass) at **both** feet.
- Every **column** carries a real load (arch / entablature / rail / gallery) **or** is rubble.
- No orphan verticals. No floating spans. No decoration that contradicts the load path.

This is the architectural analog of the sim-invariant discipline: the load path is the "invariant" the dressing must respect, exactly as the playable footprint is the invariant the visual footprint must respect.

## 5. Storeys — where grandeur actually comes from

The reference's grandeur is not "tall walls." It is that **the building has floors.** Replicate the storey structure:

- A **lower arcade** (§3b) carrying an **upper gallery** with a balustrade edge (§2.4), reached by the stairs we already have.
- Place set-pieces (statuary, votive arrays, banners) on the gallery so the upper storey reads as inhabited, exactly as the reference puts the statue + gold votives up top.
- The gallery sits OUTSIDE the playable footprint (it is annulus/backdrop per Layer 2) — combatants never go up there; it is pure grandeur backdrop. Keep it in `nonpassable_dressing`.

## 6. Part-1 of the wave — the floor-color coherence fix (do this first; it is certain)

Matt: *"the outer square of the ground (the extra space after the main simulator floor spec) is a darker color tile than the main spec. Can you please make them all the same color?"*

This is a **Layer-2 coherence fix**, not a cosmetic tweak. The decoupling canon §2 requires the floor to "flow continuously pit → annulus → outer ring" so the playable footprint is an **invisible sub-region**. A darker annulus tile visually re-draws the playable boundary — it re-creates a faint version of the exact "tabletop board boxed pit" the whole Layer-2 move eliminates. **Make the annulus/outer floor the same material + color as the playable-spec floor** so the playable footprint stays invisible. (If the darker ring was an intentional readability demarcation, replace it per decoupling §2 "optional demarcation": LOW see-over elements / a floor-texture ring at most — never a value/color step that boxes the pit.)

## 7. Acceptance criteria

- **Floor:** annulus floor reads continuous with the playable floor; no color/value step outlining the playable square. Parity unchanged (35/35 — this touches presentation only).
- **Columns:** zero upright orphan columns. Every standing column is a pier / arcade member / engaged column / baluster. Loose verticals are rubble only.
- **Arches:** zero floating arches. Every arch is a window-in-wall / arcade member / gallery span, landing on real support at both feet.
- **Load path:** the §4 test passes on visual inspection from the establishing camera and each per-zone camera.
- **Storeys:** at least one lower-arcade → upper-gallery storey relationship present, reading as a coherent built level.
- **Grandeur + register-2 hold:** wall-cutaway transparency (Layer 3) still correct from every camera; register-2 stays 6/6; god-rays now pass THROUGH the window arches.
- **Parity sacrosanct:** combatants never leave the sim-spec tiles; re-verify after the build.

## 8. The three-way review Matt asked for (me / Drax / Galadriel)

- **gandalf (this doc):** the design reading + the rule. Done.
- **Drax:** review Image #65 for **buildability** — which Synty POLYGON Dark Fantasy modular pieces compose a pier→arch bay, an arcade run, a gallery+balustrade, and window-in-wall openings; flag any asset constraint that bends the rule (e.g., if no traceried-arch piece exists, name the nearest); then build §6 (floor fix, certain) + a FIRST PASS at §2–§5. Report buildability observations alongside the build.
- **Galadriel:** review Image #65 for the **architectural-grammar gap** — score our current iter3 against the reference specifically on (a) coherent-load-path read, (b) arcade/colonnade presence, (c) storey/gallery presence, (d) arch-as-window (god-ray-motivating) presence, (e) any orphan-column / floating-arch falsifiers in our current build. Quantify the gap so the next iteration has a target, exactly as the dressing-density and warm:green gaps were quantified.

---

**Signed:** gandalf, 2026-06-15
**For:** the architectural-grammar rule that makes the battle-room read as a real building — columns never stand alone (pier / arcade / engaged / baluster, or rubble), arches never float (window-in-wall / arcade-across-columns / gallery-span, landing on real support at both feet), governed by one load-path test ("would it stand, and is it doing a job?"), with storeys (lower arcade → upper gallery) as the true source of grandeur and the annulus floor recolored to match the playable floor so the playable footprint stays an invisible sub-region; grounded in a close reading of the POLYGON Dark Fantasy reference and folding into the battle-room decoupling canon once Drax builds and Galadriel validates.
