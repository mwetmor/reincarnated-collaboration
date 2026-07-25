# DISPATCH — L4b (W-PRO) run report, RECONSTRUCTION

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Program:** `agentic_orchestration/gandalf/notes/2026-07-24-tool-capability-program-charter.md`
**Lap charter:** `agentic_orchestration/gandalf/notes/2026-07-25-tcp-l4-expansion-bakeoff-charter.md`

---

## §0 — What happened, and what this dispatch is NOT

The L4b cell **ran to completion and then died on the last step.** Its final logged line was
literally *"Now the report."* — then the agent stream timed out.

**Everything upstream of the report survived and is on disk.** Build, three cycles, judgment,
diffs, crops, the L-J restore, the blast-radius fingerprint, and the TCP-27 vacate all landed and
are verified. I checked the lab myself before writing this: Pro's addon is parked at
`~/Games/mcp-lab/_swap/pro_addon_godot_mcp_USED/`, Murzak's `0.19.1` is back at
`project/addons/godot_mcp`, `.mcp.json` points at 27435, and the three PRE-L4B banked files are in
`evidence/l4/l4b/swap/`.

**This dispatch is NOT a re-run.** Do not touch the wire. Do not swap addons. Do not open Godot.
A second run is a *different run*, and re-running would burn the swap procedure to reproduce data we
already hold. **The artifacts are read-only inputs. You are writing prose from evidence.**

**Stamp it honestly.** The report header must say it is a **RECONSTRUCTION from surviving
artifacts, authored after the executing agent terminated** — a fresh reader of artifacts is a
different epistemic object than the agent that ran them, and any claim you cannot source to a file
must be marked `UNRECOVERABLE` rather than inferred. That distinction is the whole value of the
stamp; do not smooth it over.

## §1 — The narrative spine, recovered from the terminated agent's transcript

These are the executing agent's own words. Use them to structure the cycle story; verify each
against the artifacts before you assert it.

1. *"Two problems — one in my own harness."*
2. *"The saved names are `SM_Bld_Base_Pillar_02` / `SM_Prop_Brazier_05` — **collision-rename residue
   from cycle 1, frozen in**. And **my own verifier's `global_transform` returned identity**, making
   clause 5 vacuous. Fixing the instrument first."*
3. *"All six metric clauses now verifiable. One real defect remains — **the props are saved under the
   wrong module names**. Cycle 3."*
4. *"My crop coordinates were in display space, not pixel space. Let me project the actual world points."*
5. *"All six clauses judged by eye and by number."*
6. *"Byte-identical. Now the L-J restore — verified by file inventory, never a version string."*
7. **★** *"**L-J's exact failure mode, live**: the Pro addon I installed as **44 files** was **79 files**
   at restore — while `plugin.cfg` still said `1.15.1`."*
8. *"`timeout` isn't on macOS — RC=127 means the editor never ran. Retrying."*
9. *"Restore verified."* → blast-radius fingerprint → TCP-27 vacate → **stream died.**

**Item 7 is the most load-bearing thing this lap produced and it must lead the findings section.**
L-J says *restore by inventory, never by version string.* The version string lied by **35 files**.
That is the law vindicated empirically, live, on the exact procedure it governs. Pin what grew — the
agent said it was about to. If the growth is unattributed in the artifacts, say so.

## §2 — Numbers I have already extracted (verify, do not re-derive blind)

**P-2 — non-destruction, `evidence/l4/l4b/diff/L4B_WPRO_DIFF.json`:**

| | cycle 1 | final |
|---|---|---|
| outside-addition pixels considered | — | 1,730,817 |
| **outside changed pixels** | — | **59** |
| **outside max channel delta** | — | **1** |
| whole-frame changed px | 121,839 | 119,338 |
| inside-addition changed px | — | 119,279 |
| mask `masked_in_px` / dilate | 342,783 / 24 px | same |

**W-PRO PASSES P-2.** My pre-registered prediction was **FAIL**. Record the reversal plainly and
cross-reference **TCP-24** — the mechanism I predicted from (`set_owner_recursive`) had already been
re-attributed to Godot's `PackedScene.pack()` before this cell ran, so this is a *confirmation of the
corrected attribution*, not a bolt from the blue. Say that; do not oversell it.

**P-5 — iteration cost, from `evidence/l4/l4b/wire/*.jsonl`:** 90 wire calls across 11 plans
(`read1,2,3,5` = 2/3/6/1 · `read4` = 23 · `probe` = 4 · `c1a` = 22 · `c1b` = 15 · `c2` = 7 · `c3` = 7),
**3 cycles**. Comparator: W-MUR **117 calls / 24 plans / 3 cycles**.

**P-3 — route.** `c1a` uses `add_node`; `c2` uses `execute`/`script`; `c1b`/`c2`/`c3` use
`save_scene`. So Pro **reached for a script route in cycle 2** where Murzak never did. Read
`evidence/l4/l4b/P3_FIRST_PROMPT_BANKED.md` and confirm the first prompt carried **no method noun**
before you claim the route was unprompted. If it did carry one, P-3 is contaminated for this cell and
you must say so.

## §3 — Two things the conductor now knows that you should NOT re-investigate

1. **The quilted pillars are NOT yours, NOT Pro's, and NOT Murzak's.** Traced and closed this
   session. `MaterialList_PolygonGeneric.txt` declares `SM_Bld_Base_Pillar_01` →
   `Slot: Generic_Concrete (Uses custom shader)` — **one slot, no albedo texture**.
   `render_catalogue.gd` treats `"uses custom shader"` as a no-albedo sentinel and routes it to a
   neutral material (your own *"no-albedo / glass quilt fix, Matt review 2026-06-21"*), which is why
   `catalogue/.../cat_dark1_thumb_SM_Bld_Base_Pillar_01.png` renders clean.
   `kit_replica_level.gd:770` and `:808` apply `tex_atlas` **unconditionally** to pillars and
   toppers, in **all five kits** — the only two consumption sites of `tex_atlas` in the file. Atlas
   onto never-atlas-authored UVs = the swatch bands. **Note it in the report as substrate, cite this
   dispatch, and move on.** A separate product dispatch will carry the fix.
2. **The flanking stairs are a defect in MY spec, not in Pro's execution.** Charter clause 2 says
   *"one at each of the dais's +X and −X ends … ascending toward −Z"*, which places both flights
   entirely outside the dais footprint, arriving at its back corner against the wall. Both cells
   built it faithfully. **Score conformance against the clause as written.** Do not "fix" it and do
   not mark it a Pro defect.

## §4 — Deliverable

`agentic_orchestration/drax/notes/2026-07-25-tcp-l4b-wpro-run-report.md`, same shape as your L4a
report. Required: the RECONSTRUCTION stamp (§0); the six-clause conformance table with measured
numbers; P-1..P-6 each resolved to a recorded fact **or** marked `UNRECOVERABLE`; the frames index;
the L-J file-count finding (§1.7) as its own section; the blast-radius/restore verification with the
artifacts that prove it; and an explicit **artifact inventory** of everything under
`evidence/l4/l4b/` and `prep/l4b_residue/`.

**Ship the frames index even for frames you cannot fully explain.** L-A binds: the pictures are the
deliverable, prose is the accompaniment.

**HALT to gandalf** if: the restore verification does not actually check out against
`evidence/l4/l4b/swap/PRO_INVENTORY.sha256`; or the artifacts contradict any number in §2; or
`P3_FIRST_PROMPT_BANKED.md` contains a method noun.

---

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`). This dispatch exists on disk rather than only in a
session transcript because Matt asked *"where can I find the prompt to understand the from → to?"* and
the honest answer for the brief layer was *"you can't."* That is now fixed going forward.
