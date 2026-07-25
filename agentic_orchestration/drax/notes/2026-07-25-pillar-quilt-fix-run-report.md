# RUN REPORT — Pillar-quilt fix in `reincarnated-godot` (TCP-37 ④)

**Agent:** drax (presentation seam) · **Date:** 2026-07-25
**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-drax-pillar-quilt-fix.md`
**Authorization:** Matt, verbatim — *"The pillar-quilt fix — go."*
**Commits (reincarnated-godot, NOT pushed):** `ce1c1af` fix · `188fd27` instruments + proofs ·
`398609c` AGENT_STATE
**Verdict:** **DONE.** All four §4 exit predicates met. Two findings the dispatch did not
anticipate are declared in §7, one of which materially changed the shape of the fix.

---

## 1 — Headline

The quilt is gone from all five kits, and the two kits that were *legitimately* atlased changed
**zero pixels in every framing** — which is the claim that actually mattered.

| measurement | result |
|---|---|
| module surfaces examined (5 kits × pillar + topper) | 11 |
| surfaces whose binding changed | **4** |
| kits unchanged entirely (dark-fantasy, dungeon-realms) | **2 of 5** |
| before/after frame pairs rendered | **20** |
| changed pixels across all 20 pairs | 396,108 |
| changed pixels **outside** the pillar/topper silhouette | **0** |
| I7 play-camera frames differing, any kit | **0 px** |
| resolver-delegation parity (render_catalogue) | 13,229 meshes / 203,453 slot entries / **0 mismatches** |

---

## 2 — The defect, re-derived (and one correction to §0)

The dispatch located the defect at two `_apply_single_tex(inst, tex_atlas)` call sites. **There are
four.** The atlas reaches the column through two different code paths:

- the plain `StandardMaterial3D` path — `_apply_single_tex()` — on the one non-occluded corner;
- the **SE-occlude `ShaderMaterial` path** — `_build_occlude_mat(occlude_shader, tex_atlas)`, which
  feeds the same atlas in as the shader's `stone_tex` — on the other **three** corners.

`se_corner = [false, true, true, true]`, so three of four pillars and three of four toppers were
quilting through the path the dispatch did not name. A fix that cured only the two named sites
would have left 75% of the columns quilted. Both paths are now routed through the sentinel.

---

## 3 — The fix, and the ruling on "shared helper vs duplicated check"

**Ruling: shared helper, and `render_catalogue.gd` refactored to consume it.** The dispatch left
this to me and asked it be logged. The reasoning: leaving a second copy in `render_catalogue.gd`
would have reproduced the exact condition that caused the bug — two implementations of one idea,
free to drift. New file:

- **`~/Games/reincarnated-godot/scripts/synty_material_list.gd`** — the one Synty MaterialList
  reader. Texture index, list parser, the sentinel (`is_sentinel`), the glass/water classifiers,
  the texname-skew resolver, the neutral colour constants.

Consumers: `kit_replica_level.gd` (new) and `render_catalogue.gd` (delegated; its private
resolver deleted).

**Per-surface policy in the builder**, in priority order:

1. glass / water marker → neutral glass
2. **resolved PNG → that texture** ← this is what actually cures the quilt
3. mesh known with **zero** slot lines → neutral masonry (the genuine no-albedo module)
4. anything else — unresolved name, mesh absent from the list → **the kit's atlas, i.e. today's
   behaviour, deliberately unchanged**

Rule 4 is the important one. An unresolvable material name is *reported* as unresolvable and left
alone. It is never resolved to the nearest-looking file on disk.

### Per-kit outcome (measured, `scripts/audit_kit_module_slots.gd`)

| kit | module | MaterialList slot | binds | Δ |
|---|---|---|---|---|
| dark-fantasy | `SM_Bld_Pillar_05` | `PolygonDarkFantasy_Mat_01_A` | atlas | — |
| dark-fantasy | `SM_Bld_Topper_Base_01` | `PolygonDarkFantasy_Mat_01_A` | atlas | — |
| dungeon-realms | `SM_Env_Dwarf_Pillar_04` | `PolygonDungeonRealms_Mat_01_A` | atlas | — |
| dungeon-realms | `SM_Env_Dwarf_Pillar_Cap_02` | `PolygonDungeonRealms_Mat_01_A` | atlas | — |
| dwarven-dungeon | `SM_Bld_Base_Pillar_01` | `Generic_Concrete` | `Generic_Concrete.png` | **FIXED** |
| dwarven-dungeon | `SM_Gen_Prop_Plinth_02` | `Generic_01_A` | atlas | — |
| ancient-egypt | `SM_Bld_Pillar_Ornate_01` s0 | `PolygonAncientEgypt_01_A` | atlas | — |
| ancient-egypt | `SM_Bld_Pillar_Ornate_01` s1 | `Stone_Wall_Mural_02` | **unresolved → atlas kept** | — |
| ancient-egypt | `SM_Bld_Base_Roof_Cap_End_01` | `Stucco_01` | `Stucco_01.png` | **FIXED** |
| dark-fortress | `SM_Bld_Base_Pillar_01` | `Generic_Concrete` | `Generic_Concrete.png` | **FIXED** |
| dark-fortress | `SM_Bld_Base_Roof_Cap_End_01` | `Generic_01_A` | `Generic_01_A.png` | **FIXED** |

dark-fortress's topper is a **generic-family** module: the pack's own generic list points it at the
Generic atlas, not at the DarkFortress alt atlas the kit binds as `tex_atlas`. The re-bind is
visually near-neutral (both atlases carry similar content at those UVs) but the binding is now
what the pack declares. Recorded so the small diff on that surface is not mistaken for noise.

---

## 4 — Evidence (all paths absolute; frames are LOCAL by repo policy)

`.gitignore` in `reincarnated-godot` deliberately excludes rendered Synty frames — they are
derivative IP and must not reach a shared remote. Text proofs carry no Synty IP and **are**
committed. My ruling on "the repo's evidence convention" (dispatch §4.2) is therefore: **frames
live at the local path below and the path is the deliverable; proofs are committed alongside.**

**Root:** `/Users/admin/Games/reincarnated-godot/harness_logs/quiltfix_2026-07-25/`

| deliverable | path |
|---|---|
| **Money sheet — Matt's eye, unaided** | `.../MONEY_before_after.png` |
| before/after pairs, room-only, 5 kits × 4 framings | `.../before_room/` · `.../after_room/` |
| before/after pairs WITH occupant (first pass) | `.../before/` · `.../after/` |
| pillar/topper silhouette masks | `.../mask/` |
| triptych sheets (before / after / changed-pixels) | `.../SHEET_box.png` · `SHEET_pillars.png` · `SHEET_cam.png` |
| close-up crops | `.../CROP_R2_dwarven-dungeon__pilB.png` · `CROP_R4_dark-fortress__pilB.png` · `CROP_R3_ancient-egypt__pilA.png` |
| authored-scene (M2) before/after | `.../m2_before/` · `.../m2_after/` |
| **text proofs (committed)** | `.../PROOF_audit.log` · `PROOF_parity.log` · `PROOF_diff.log` |

The distance record of the defect — `~/Games/mcp-lab/evidence/l4/sheet/L4_ROW3_pillars.png` — was
**read, not re-shot**, per §2.2.

### 4.1 — The play-camera pair, honestly framed

The dispatch binds L-A: play camera, judgeable unaided. **At the current 17.5 m room the I7 play
camera (`CAM_DIST` 16.5, 20° telephoto) frames floor only — no column enters the shot.** That is a
pre-existing tension already documented in `shoot_kit_replica.gd`'s header (the reference frame
Matt has been judging was shot when the room was 7.5 m). So the play-camera pair is shipped and it
is *evidence of no regression* — **0 changed pixels, all five kits** — while the judgeable-for-the-
fix frames are `__box` (identical pitch/yaw/FOV/aim, dollied back along the same view axis) and the
two close-ups. Same camera moved, not a different camera.

### 4.2 — No-regression, as a number rather than a squint

The first diff pass was contaminated: the occupant's Binbun aura is not frame-deterministic and
moved ~6.8% of the play-camera frame **between two runs of identical code**. I added `--nopilot` and
re-shot both sides (the before side by stashing only `kit_replica_level.gd`, verified restored
byte-identically by sha256).

Then, rather than assert "pillar/topper only", I made it testable: a `--mask` pass renders the same
camera with everything but the Pillars holder hidden and the columns flat-white, and
`quiltfix_diff.py contain` asks whether every changed pixel falls inside that silhouette.

```
20 frames · 396,108 changed pixels · 0 outside the pillar/topper silhouette · ALL PASS
```

`REF_dark-fantasy` and `R1_dungeon-realms`: **0 changed pixels in all four framings.** The sentinel
provably does not catch legitimately-atlased modules.

---

## 5 — "Library-wide": what the material lists actually flag

Scanned the full corpus — **43 MaterialList files, 26,394 mesh blocks, 231,990 slot lines.** Two
genuine no-albedo classes exist:

1. **974 pure-sentinel slots** (`Default-Material (No Albedo Texture)` — no material name at all).
2. **7 known-but-zero-slot mesh blocks** (dark-fantasy `SM_Bld_Base_Ceiling_01` and
   `SM_Bld_Wall_Alcove_02_Alter`, plus 5 elsewhere).

**Neither class touches any module `kit_replica_level.gd` builds.** In the five kits' blast radius
(floor / wall / pillar / topper) there are **zero** additional no-albedo modules to fix — every one
of the 11 surfaces names a material. So the "enumerate and fix others" clause is answered with
evidence rather than a change, and the neutral-material branch is ported and live but fires on none
of the current roster.

**A change I measured and deliberately did NOT make.** Class 1 looks like an obvious library-wide
quilt to fix. It is not: the 974 slots are almost all **character** mesh surfaces (`SM_Chr_*`,
`Chr_*`), where the pack primary atlas is the *correct* read and flattening them to neutral grey
would have regressed hundreds of catalogue thumbnails to cure a defect they don't have. Two
building modules carry it (`SM_Bld_Base_Floor_Hole_01` surface 2, in dwarven-dungeon and
dark-fortress); neither is a kit module. Left alone, enumerated here.

**Floor and wall were checked and are not defective.** Their bindings are tiling maps, not atlases,
so they cannot quilt; where a kit's `tex_floor`/`tex_wall` differs from the list (ancient-egypt) it
is a deliberate photographic-parity choice recorded in the kit table, and the charter freezes the
room's photographic identity. Out of scope, and changing them would have been the kind of quiet
scope creep this dispatch warns about. `walltop_level.gd` (the dark-fantasy reference builder) was
checked too: its pillar/topper are legitimately atlased, so it has no defect to fix.

---

## 6 — Beyond the named scope, with reasons

**Fixed** — same defect, text side, would have silently resurrected the quilt:

- `scenes/kit_replica_r2_dwarven.tscn` — the authored R2 room baked the atlas onto all four
  pillars (one `StandardMaterial3D`, three occlude `ShaderMaterial`s). Fixed; toppers untouched
  (legitimately atlased). Verified: 1,294 changed pixels in the box framing, matching the
  generator's 1,299 on the same geometry.
- `scripts/emit_r2_tscn.py` — the emitter that produces that scene. Without it, a re-emit undoes
  the fix. Now re-emits the corrected scene **byte-identically** to the hand-edited file.

**Deliberately NOT fixed** — closed-lap records, changing them would retro-edit a completed
experiment's inputs:

- `scripts/tcp_l2_gen_pro_plan.py` and `scenes/tcp_l2_pro_room.tscn` keep the pre-fix binding. A
  future lap re-running the Pro plan must take the corrected one. Flagged to gandalf.

**mcp-lab: zero writes.** Read `evidence/l4/sheet/L4_ROW3_pillars.png`,
`evidence/L4_KIT_CONSTANTS.md`, and `project/scene_before.tscn` (grep, to confirm the crypt kit is
dark-fortress). Nothing written. The frozen substrate keeps its quilt.

---

## 7 — HALT items and declared ambiguities → gandalf

Per §3's HALT rule, reported rather than guessed.

### 7.1 — One genuine material-intent ambiguity (does not block; behaviour unchanged)

**ancient-egypt `SM_Bld_Pillar_Ornate_01` surface 1 → `Slot: Stone_Wall_Mural_02 (Uses custom
shader)`.** No file of that name ships. Three plausible neighbours exist and they are three
different intents: `Textures/Murals/Wall_Mural_02.png`, `Textures/Murals/White_Wall_Mural_02.png`,
`Textures/Walls/Stone/Wall_Stone_02.png`. The resolver's rules are **name-shape transforms, never
similarity matches**, so it returns unresolved and the surface keeps the atlas — exactly as before
this fix. Nothing was guessed. If you want that surface resolved, it needs a human ruling on which
of the three Synty meant.

### 7.2 — The dispatch's §0 characterisation was subtly off, and it changed the fix

§0 describes `SM_Bld_Base_Pillar_01 → Slot: Generic_Concrete (Uses custom shader)` as a module
"whose pack material list declares no albedo", and §1 asks that such modules "get the neutral-
material treatment".

Taken literally that would have painted the dwarven-dungeon, dark-fortress and ancient-egypt
pillars **flat grey**, discarding the concrete and stucco Synty actually authored — and it would
*not* have matched `render_catalogue.gd`'s idiom, which the dispatch cites as the model.
`render_catalogue`'s `_is_sentinel` fires on the **parenthesised descriptor only**; resolution then
falls through to the material name, and `Generic_Concrete` resolves to a real PNG. Its neutral
`_stone_mat` route is reserved for meshes with **zero** slot lines.

`Generic_Concrete (Uses custom shader)` is therefore not "no albedo" — it is **a named albedo the
kit builder was ignoring**. I implemented the sentinel as specified *and* the resolution the
sibling script actually performs; the second is what cures the quilt on these five kits. Flagged
because the difference is the whole fix, and because a literal execution of §1 would have shipped
three grey columns and called it done.

### 7.3 — Two latent defects surfaced, not silently changed

- **Cross-list mesh-name collision.** When a pack ships two MaterialLists that define the same mesh
  name, the slot lists **concatenate** and the surface cursor walks off the end. Measured: 2
  occurrences corpus-wide (`polygon-dark-fortress`: `FX_Fire_01`, `SM_Bld_Base_Wall_Half_01`),
  neither a kit module. Behaviour left exactly as the render_catalogue lineage had it — this
  dispatch does not quietly change unrelated resolution — but it now emits a `push_warning` instead
  of being silent.
- **`project.godot` carried an uncommitted `[rendering] mesh_lod` deletion before this session
  started.** Not mine, left untouched. Flagging it because the concurrent L5-D dispatch judges this
  repo by git attribution and treats an uncommitted change at its cell end as a HALT.

---

## 8 — Read / write list

**Read (reincarnated-godot):** `scripts/kit_replica_level.gd`, `scripts/render_catalogue.gd`,
`scripts/shoot_kit_replica.gd`, `scripts/walltop_level.gd`, `scripts/walltop_occlude.gdshader`,
`scripts/emit_r2_tscn.py`, `scripts/tcp_l2_gen_pro_plan.py`, `scripts/tcp_l2_dump_plan.gd`,
`scripts/kit_contact_sheet.py`, `scripts/run_replica_mp4.sh`, `scenes/kit_replica_r2_dwarven.tscn`,
`catalogue/packs.json`, `project.godot`, `AGENT_STATE.md`, `.gitignore`, and 43
`Assets/Synty/**/MaterialList_*.txt` + the texture trees of the five kit packs.

**Read (mcp-lab — READ ONLY, zero writes):** `evidence/l4/sheet/L4_ROW3_pillars.png`,
`evidence/L4_KIT_CONSTANTS.md`, `evidence/l4/` listing, `project/scene_before.tscn` (grep only).

**Read (meta-repo):** this dispatch, `2026-07-25-drax-l5d-seam-arrival.md` (to resolve "the crypt
kit" — it is **dark-fortress**), `CLAUDE.md`.

**Wrote (reincarnated-godot) — new:** `scripts/synty_material_list.gd`,
`scripts/audit_kit_module_slots.gd` + `scenes/audit_kit_module_slots.tscn`,
`scripts/verify_syntyml_parity.gd` + `scenes/verify_syntyml_parity.tscn`,
`scripts/quiltfix_diff.py`, `harness_logs/quiltfix_2026-07-25/**`.

**Wrote (reincarnated-godot) — modified:** `scripts/kit_replica_level.gd`,
`scripts/render_catalogue.gd`, `scripts/shoot_kit_replica.gd`, `scripts/emit_r2_tscn.py`,
`scenes/kit_replica_r2_dwarven.tscn`, `AGENT_STATE.md`.

**Wrote (meta-repo):** this report; completion record appended to the dispatch.

**Not pushed.** Either repo.

---

## 9 — Rulings log

| # | ruling | reasoning |
|---|---|---|
| R1 | Shared helper, and `render_catalogue.gd` refactored to consume it | A second copy would recreate the drift that caused the bug. Delegation gated on a golden-reference differential test (0/203,453 mismatches) before it was allowed. |
| R2 | Route **all four** call sites, not the two named | The SE-occlude path quilts identically and covers 3 of 4 corners. |
| R3 | Unresolved slot → keep the atlas | The dispatch's own HALT rule. Reporting an unresolvable name beats inventing a resolution. |
| R4 | Neutral colours via `albedo_color`, not a solid texture | Matches `render_catalogue`'s `_stone_mat`/`_glass_mat` exactly; a raw `ImageTexture` bypasses sRGB→linear and lands the grey a stop bright (the trap `_load_tex` already documents). |
| R5 | `recursive` is a caller parameter, default false | Kit roots need a subtree walk (packs nest `Walls/MudBrick/`); the catalogue enumerates dirs explicitly and flipping it globally would change which textures resolve for 26k thumbnails. Not this seam's call. |
| R6 | Fix the authored `.tscn` **and** its emitter | Fixing only the scene means the next re-emit resurrects the quilt. |
| R7 | Leave TCP-L2 Pro-plan artifacts on the old binding | Closed-lap records; retro-editing an experiment's inputs is worse than a stale binding. Flagged for the next lap. |
| R8 | Do **not** reroute the 974 pure-sentinel slots | Measured: they are overwhelmingly character surfaces where the atlas is correct. Would have regressed hundreds of thumbnails. |
| R9 | Room-only (`--nopilot`) diffs + a silhouette containment test | The aura's non-determinism swamped the signal at ~6.8%/frame; "pillar/topper only" is a claim about regions and deserved a number, not a squint. |
| R10 | Evidence frames stay local; text proofs committed | `.gitignore` policy — rendered Synty geometry is derivative IP and must not reach a shared remote. |

---

## 10 — Exit predicate check (dispatch §4)

1. **Sentinel ported + call sites routed, all five kits, commit citing the dispatch** — met.
   `ce1c1af`; four call sites; five kits; audit table in §3.
2. **Evidence set per §2 (pairs + close-up + no-regression diff), filed** — met. §4; ruling R10 on
   the filing convention.
3. **Additional no-albedo modules enumerated, fixed, shown** — met. §5: the corpus scan found two
   real classes, neither in the builder's blast radius; both enumerated, with the measured reason
   one of them was deliberately not rerouted.
4. **Read/write list declared; rulings logged** — met. §8, §9.
