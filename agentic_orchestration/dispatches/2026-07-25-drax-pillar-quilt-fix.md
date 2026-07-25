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

---

## Completion record

**Executor:** drax · **Closed:** 2026-07-25 · **Verdict: DONE** — all four §4 exit predicates met.
**Report:** `agentic_orchestration/drax/notes/2026-07-25-pillar-quilt-fix-run-report.md`
**Commits (`reincarnated-godot`, NOT pushed):** `ce1c1af` fix · `188fd27` instruments + proofs ·
`398609c` AGENT_STATE.

**Result.** 11 module surfaces across 5 kits; **4 change binding**. dark-fantasy and
dungeon-realms are legitimately atlased and changed **0 pixels in every framing** — the sentinel
provably does not catch them. Across 20 before/after frame pairs: 396,108 changed pixels, **0
outside the rendered pillar/topper silhouette** (proven by a mask pass + containment test, not by
eye); every kit's I7 play-camera frame differs by exactly 0 px. Resolver moved to
`scripts/synty_material_list.gd` and shared by both scripts; `render_catalogue.gd`'s delegation
proven behaviour-identical over 13,229 meshes / 203,453 slot entries / **0 mismatches**.

**Three things the dispatch did not anticipate** (detail in report §7):

1. **§0 named two call sites; there are four.** The atlas also reaches the column through the
   SE-occlude `ShaderMaterial` (`_build_occlude_mat(shader, tex_atlas)`), which covers **3 of 4
   corners**. Curing only the two named sites would have left 75% of the columns quilted.
2. **§0's "declares no albedo" is not what `Generic_Concrete (Uses custom shader)` means.**
   `render_catalogue`'s sentinel fires on the parenthesised descriptor only; resolution then falls
   through to the material name, which resolves to a real PNG. Its neutral route is reserved for
   meshes with **zero** slot lines. A literal execution of §1 would have painted three kits' pillars
   flat grey and discarded the concrete/stucco Synty authored. Sentinel implemented as specified
   **and** the resolution the sibling script actually performs — the latter is what cures the quilt.
3. **The "library-wide" clause is answered with evidence, not a change.** Corpus scan (43 lists /
   26,394 mesh blocks / 231,990 slot lines) found 974 pure-sentinel slots and 7 zero-slot meshes.
   **None is in the builder's blast radius.** The 974 are overwhelmingly *character* surfaces where
   the atlas is the correct read — rerouting them to neutral grey would have regressed hundreds of
   thumbnails to cure a defect they don't have. Enumerated, deliberately not changed.

**HALT item → gandalf (does not block; behaviour unchanged).** ancient-egypt
`SM_Bld_Pillar_Ornate_01` surface 1 names `Stone_Wall_Mural_02`; no such file ships and the three
plausible neighbours (`Wall_Mural_02`, `White_Wall_Mural_02`, `Wall_Stone_02`) are three different
intents. **Not guessed** — left on the atlas, exactly as before. Needs a human ruling if it is to
resolve.

**Beyond scope, fixed with reason:** `scenes/kit_replica_r2_dwarven.tscn` and its emitter
`scripts/emit_r2_tscn.py` baked the same defect into text; without the emitter fix a re-emit would
resurrect it. **Beyond scope, deliberately NOT fixed:** `scripts/tcp_l2_gen_pro_plan.py` /
`scenes/tcp_l2_pro_room.tscn` keep the pre-fix binding — closed-lap records; a future lap re-running
the Pro plan must take the corrected one.

**§3 scope guard honoured — `~/Games/mcp-lab/` had ZERO writes.** Read only:
`evidence/l4/sheet/L4_ROW3_pillars.png` (referenced, not re-shot, per §2.2),
`evidence/L4_KIT_CONSTANTS.md`, `project/scene_before.tscn` (grep, to confirm the crypt kit is
**dark-fortress**). The frozen substrate keeps its quilt.

**Evidence** (frames are Synty derivative IP and stay LOCAL per the repo's `.gitignore`; text proofs
are committed): `/Users/admin/Games/reincarnated-godot/harness_logs/quiltfix_2026-07-25/` —
`MONEY_before_after.png` is the judge-unaided sheet.

**Note for the concurrent L5-D cell:** `reincarnated-godot` is left with **no uncommitted change of
mine**. `project.godot` carries an uncommitted `[rendering] mesh_lod` deletion that **predates this
session** — not this dispatch's, left untouched.

**Signed:** drax, 2026-07-25 (presentation seam).
