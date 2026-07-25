# DISPATCH — Pillar-quilt fix in `reincarnated-godot` (TCP-37 ④: Matt go)

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Authorization:** Matt, verbatim: *"The pillar-quilt fix — go."*
**Lineage:** TCP-30 ② (the defect is OURS, not any tool's) · Matt's library-wide quilt review
2026-06-21 (the fix idiom already exists in `render_catalogue.gd` and was never back-ported).

## §0 — The defect, as the executor derived it (TCP-30 ②, drax-derived — quoted, not recalled)

`~/Games/reincarnated-godot/scripts/kit_replica_level.gd` applies `_apply_single_tex(inst,
tex_atlas)` **unconditionally** to pillar and topper modules (drax located the two call sites at
approx. lines 770 and 808 — **re-locate yourself; line numbers drift**), in **all five kits**, for
modules whose pack material list declares no albedo — e.g. `MaterialList_PolygonGeneric.txt`:
`SM_Bld_Base_Pillar_01 → Slot: Generic_Concrete (Uses custom shader)`. Result: the texture atlas
quilts across the pillar UVs. `render_catalogue.gd` already solves detection — `_is_no_albedo()`
(approx. line 341, matches `"uses custom shader"` etc.) — and routes those meshes to neutral
materials (`Color(0.62, 0.60, 0.58)` / `Color(0.42, 0.42, 0.44)`, comment lineage *"no-albedo /
glass quilt fix (Matt review 2026-06-21)"*).

## §1 — The fix

Port the no-albedo sentinel into `kit_replica_level.gd` and route the pillar/topper texture
application through it for **all five kits**: no-albedo modules get the neutral-material treatment
matching `render_catalogue.gd`'s idiom; everything else keeps the atlas path untouched. **Prefer a
shared helper over a duplicated check** — the month-long divergence between the two scripts IS the
bug's origin story; your call, logged. Product repo, normal seam work, auto-commit per CLAUDE.md.

## §2 — Evidence (L-A binds: play camera, judgeable unaided)

1. **Before/after frame pairs at the play camera** for the crypt kit **+ at least one other kit**.
2. A **close-up pillar pair** (before/after). The distance record of the defect is the L4 contact
   sheet ROW3 (`~/Games/mcp-lab/evidence/l4/sheet/L4_ROW3_pillars.png`) — reference it, don't
   re-shoot it.
3. **No-regression proof:** full kit-replica render before/after + diff — changed regions are
   pillar/topper only. The sentinel must not catch legitimately-atlased modules; if the material
   lists flag OTHER no-albedo modules the current code quilts, list them and fix them under the same
   sentinel (that is the "library-wide" in Matt's correction), showing each in the diff.

## §3 — Scope guard

- **`~/Games/mcp-lab/` is OUT OF SCOPE — zero writes.** The frozen lab substrate
  (`scene_before.tscn`) **keeps its quilt** deliberately (TCP-27 ③): the lab is a historical
  record; the product repo is where the fix lives. The L5 lap runs concurrently on that floor.
- The motion-harness dispatch runs concurrently in `mcp-lab/harness/` — no interaction.

## §4 — Exit predicate

1. Sentinel ported + call sites routed, all five kits; commit(s) in `reincarnated-godot` with
   message citing this dispatch.
2. Evidence set per §2 (pairs + close-up + no-regression diff), filed under
   `agentic_orchestration/drax/notes/` assets or the repo's evidence convention — your ruling.
3. Any additional no-albedo modules found: enumerated, fixed, shown.
4. Read/write list declared; rulings logged.

**Report to:** `agentic_orchestration/drax/notes/2026-07-25-pillar-quilt-fix-run-report.md`
**HALT to gandalf:** if the sentinel's material-list parse is ambiguous for any module (guessing at
material intent is how the quilt was born); anything touching mcp-lab.

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`).
