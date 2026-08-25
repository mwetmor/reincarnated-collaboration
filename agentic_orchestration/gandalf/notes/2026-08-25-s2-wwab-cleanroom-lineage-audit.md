# WW-AB clean-room LINEAGE AUDIT — verdict

**Date:** 2026-08-25
**Author:** gandalf — **DRIFT-CRITIC** (named sub-agent)
**Class:** verdict note
**Status:** CURRENT
**Audits:** the clean-room source set `scripts/wwcr_*` + `scenes/wwcr_*` + `run_wwcr_stage.sh`, as minted at
`reincarnated-godot` `1692d6e` (`drax/v0.1-s2-whirlwind-cleanroom-1`)
**Against:** the adopted SB-1 cut-pattern-blade lineage (`a337d30` et seq.)

⚑ **SCOPE + DEFEAT CONDITION** (added 2026-08-25 on re-ruling; see § Post-audit drift). This verdict
certifies a **provenance claim over a named artifact set** — that no quarantined content entered it. It
does **not** certify a tree hash. `1692d6e` names *where the set stood when audited*, not the subject.

**This verdict is DEFEATED if and only if:** a post-audit change to the named set introduces content
originating in the quarantined lineage. Test it — do not assume it from the presence of drift:
```
git diff <audited-commit>..HEAD -- 'scripts/wwcr_*' 'scenes/wwcr_*' 'run_wwcr_stage.sh' | grep '^+' \
  | grep -Ei 'vfxbo|cpb|kc2|a337d30|sb1|etch|claw|cut_|rig_poe1|cyclone|run_ww[0-9]|PAL_|decay_gamma|sheath'
```
plus a float-literal intersection of the added lines against the quarantined files (method: § Q2).
**A non-empty `git diff` is NOT a defeat.** Comment fixes, harness work and instrument repair move the
tree without touching provenance. Requiring an empty diff makes this certificate expire on contact with
ordinary work — which is how a certificate stops answering while still returning cleanly.
**Authority:** dispatch `2026-08-24-drax-s2-whirlwind-cleanroom-wwab.md` § "gandalf DRIFT-CRITIC audits the lineage"; charter ruling **L-37** (*"ADOPT but hide"*)

---

## TOP-LINE VERDICT — **LINEAGE CLEAN (with findings)**

**No quarantined artifact reached this build.** The declaration checks out against the record, the
artifacts carry no contamination signature, and every channel by which quarantined content could have
arrived is closed.

**Consequence for the bake-off: the datum is VALID.** What Matt compares side-by-side is genuinely
agent-built-from-spec against human-in-the-loop, and his preference is therefore a real answer to the
run's thesis — not an artifact of one build having seen the other.

**Three findings ride with that verdict** (§ Ledger). None voids the datum. One of them —
**the quarantine list was leaky, and the experiment survived on the builder's voluntary abstention
rather than on the list** — must be fixed before the next clean-room dispatch fires, because the next
builder may read the list literally, as the list instructs.

---

## Evidentiary basis, stated honestly

I audited three things and only three: **(1)** the builder's declaration against the dispatch's
enumerated permissions and against the repo record; **(2)** the built artifacts against the
quarantined artifacts, for signatures explicable only by contact; **(3)** the side channels — dispatch
text, scene graph, autoloads, harness.

**I cannot observe the builder's session.** No tool available to me reads what a past session actually
opened. So this verdict is *not* "I watched him and he did not look." It is: **every place contact
would have left a mark, I looked, and there is no mark — including in places the builder could not
have known I would look, and including one place where the arithmetic runs against him and he did not
take the number.** That is the strongest form the evidence can take here, and it is worth saying
plainly what it is short of.

The quarantine binds the builder, not the auditor. I read both sides in full.

---

## Q1 — Declaration audit: **PASS**

### The line ranges are byte-exact, and that is checkable

drax declared reading the sealed spec *"by explicit line range, never whole-file"* (mint note § 6.2).
The spec was amended at `bac7c60f` (2026-08-24 18:34, the L-41 post-seal corrections), so the version
in force at read time is `96e3437c`. Against **that** version:

| Declared range | Section it claims | Next header begins at | Verdict |
|---|---|---|---|
| 60–132 | § 1 + § 1.1 + § 1.2 | **133** (§ 2) | exact |
| 170–181 | § 2.3 | **182** (§ 2.4) | exact |
| 212–227 | § 3.0 | **228** (§ 3.1a) | exact |
| 451–475 | § 3.1.12 (`whirlwind`) | **476** (§ 3.1.13) | exact |

**Every range terminates exactly one line before the next heading.** That is the signature of a
header-grep-driven scoped read. A whole-file read reported afterwards as ranges would not land on four
consecutive off-by-none boundaries. **§ 5 begins at line 916 in that version** — no declared range
comes within 435 lines of it.

Corroboration of read *timing*: the ranges match the **pre**-L-41 file, and the mint note was committed
at **18:35**, one minute after the amendment. Consistent, and not something a fabricated declaration
would get right by accident.

### Reads outside the "What you build FROM" enumeration — one, and it is permitted elsewhere

The RT-4 note (`legolas/notes/2026-08-24-rt4-whirlwind-donor-playback.md`) + its two evidence PNGs are
**not** in the dispatch's exhaustive § "What you build FROM" list — but the dispatch names them in its
**References** block (line 178) and its **Gate** block. **INFO, not a breach.** `framesets.json`
(frameset `ww-native-eor1`) and Donor A are named in the brief. All repo reads
(`CLAUDE.md`, `project.godot`, `data/camera_floor1_ratification.md`, `capture_rig.gd`,
`su_probe.tscn`, `king_rig.gd` grep-only) are off the quarantine list.

### The charter-grep disclosure is corroborated by his own later behaviour

He declares an incidental encounter with charter rows **L-1/L-2** in a header-grep preview, and
separately flags a **push-policy conflict** (L-2 *"push as you go"* vs this wave's COMMIT-ONLY). He
could only have known that conflict existed from that encounter — and he surfaced it rather than
resolving it silently. **A concealed read does not generate a self-incriminating downstream flag.**

### Discipline #1 ordering verified

Mint note committed `78cdc3d6` **18:35** (before minting); results appended `3acffa79` **18:52**; the
godot mint `1692d6e` **18:52**. Math-before-code held.

---

## Q2 — Artifact forensics: **NO CONTAMINATION SIGNATURE** (the load-bearing finding)

### Zero textual contact

Grep of the entire clean-room source set (`wwcr_*.gd`, `wwcr_*.py`, `run_wwcr_stage.sh`,
`wwcr_*.tscn`) for `vfxbo|cpb|kc2|a337d30|sb1|etch|claw|cut_|rig_poe1|cyclone|run_ww[0-9]` returns
**nothing**. No identifier, no comment, no path.

### The numeric intersection, adjudicated one by one

123 float literals in the clean-room, 335 in the adopted set
(`kc2_player_channel.gd` + `kc2_etch.gdshader` + `kc2_cpb_clip.gd`); **63 shared.** Most are 0.0 / 1.0
/ 0.5 / 2.0 / 100.0 / 360.0 and carry no information. Every non-trivial one:

| Value | Clean-room | Adopted | Adjudication |
|---|---|---|---|
| **0.085** | `STAGE_ALBEDO` | stage albedo | **ACQUITTED by the dispatch itself** — C-3 is named verbatim in the Scope checklist: *"Captures rendered at stage albedo 0.085 (C-3)"* |
| **34.0 / 47.0** | `CAM_DIST` / `CAM_YAW` | camera consts | **ACQUITTED** — `data/camera_floor1_ratification.md` states *"Yaw 47° (FIXED)"* and *"Distance 34.0m"*; a permitted, declared read |
| **1.9** | `R_ENGAGE = 1.9 * H_STAND` | ratio | **ACQUITTED** — stated in § 3.1.12 and re-quoted in the dispatch |
| **0.4912** | occlusion-gate hip split | a cadence-silence rev fraction | **ACQUITTED BY ARITHMETIC — the strongest-looking coincidence, and it dissolves.** The clean-room *derives it on the line it appears on*: `0.9088 / 1.85 = 0.4912`, the hip fraction of standing height. The adopted use is a revolution fraction in a comment about cut-density silence. Same digits, unrelated quantities, one of them shown as its own division |
| **0.36** | water element colour `.r`; a prop albedo | `player_rev_period_s` | unrelated domains |
| 2.6 · 0.55 · 1.70 · 0.42 · 0.34 · 0.90 · 0.98 (shared with the CPB shader) | a capture-release second (2.60), a capture-mark time (0.90), element/ambient/key-light colours, an ambient energy, a mob position, a prop albedo | palette stops, HDR energies, `decay_gamma`, `edge_sharpness` | **not one clean-room occurrence occupies the adopted role.** No stop, no energy, no exponent |

**Colour literals: zero shared `Color()` triples.** The adopted heat ramp — `PAL_HEAD (1.00,0.97,0.90)`
→ `PAL_MID (1.00,0.42,0.06)` → `PAL_TAIL (0.98,0.07,0.02)` — appears **nowhere** in the clean-room.

**Cadence diverges:** adopted `player_rev_period_s = 0.36` (≈1000 °/s, derived from a legolas Mode-A
endgame-band midpoint); clean-room `OMEGA_DEG = 900.0` (0.40 s/rev, derived from a 5-tick/s legibility
argument with the Donor-A aliasing failure recorded as a measured negative). 11 % apart, with two
separately-shown derivations.

**Naming:** the only shared prefixes are `TRAIL_*` and `SPARK_*` — and both are lifted from **permitted
text**: the dispatch says *"Tint rides the WEAPON TRAIL and the CONTACT SPARK."* Everything else is
disjoint (`CUT_* / ETCH_* / CLAW_* / PAL_* / SMOKE_*` vs `R_ENGAGE / SPIN_UP_S / OMEGA_DEG / SCUFF_* /
WINDUP_*`).

### The acquittal that would be hardest to fake

Contamination shows up not only in copied numbers but in **inherited discipline**. The adopted lineage
carries a ratified law, stated in a banner at the top of `kc2_etch.gdshader`:

> `⚑ NO CLOCK. There is no TIME here and there must not be.` … *a pure function of the sim tick — no
> RNG state, no wall clock, no accumulation. One clock in the whole scene (GL-18 / FG-10).*

**The clean-room build runs its ramps off `_process(delta)`** — the scaled wall clock — and says so
approvingly (*"so slow-motion and pause affect the effect exactly as they affect the game"*). A builder
who had opened either quarantined file would have met that law in a banner comment and almost certainly
carried it. He did not, because he never met it.

The same pattern holds across every structural axis:

| Axis | ADOPTED (`kc2_player_channel.gd`, 4,217 ln) | CLEAN-ROOM (`wwcr_whirlwind.gd`, 637 ln) |
|---|---|---|
| Body / weapon | Undead Knight + `SM_Wep_WarHammer_Large_04` | King showcase rig + Synty greatsword (1.5150 m) |
| Trail technique | pre-built `ArrayMesh` stroke library, 24-slot pool, **custom `ShaderMaterial`** (`kc2_etch.gdshader`), 3 crossed planes, core+sheath | per-frame `ImmediateMesh` triangle strip from a 10-sample bone history, **`StandardMaterial3D`, no shader anywhere in the build** |
| Colour model | fixed white-hot→orange→red heat ramp, **no element parameter** | **element-parameterized** (wind/fire/water/earth/neutral), `set_element()` asserting exactly 2 tinted surfaces |
| Determinism | seeded (`CUT_SEED 20260813`), per-tick, no delta | deterministic 1/60 s stage stepping, delta-driven effect |
| Ancillary layers | `GPUParticles3D` embers, sparks, and a **smoke BED that is explicitly "a DISC now, not a ring: 'filling the disc'"** | pooled `QuadMesh` sparks + **neutral, never-tinted** scuff quanta; *"no disc, no decal, no radial gradient, no billboard sphere — the absence is the design"* |

Read the last row twice. **On this row's central design question the two builds are not merely
different — they are opposed.** The adopted build fills the disc; the clean-room build's `set_element`
assertion exists specifically to make a filled disc impossible. Convergent contamination does not
produce an inversion of the referent's own thesis.

---

## Q3 — Channel audit: **ALL CHANNELS CLOSED**

- **The dispatch text.** Grepped for `cut.pattern|etch|claw|persist|white.hot|orange|decay_gamma|
  sheath|stroke|undead|warhammer|smoke bed|gpuparticles|shader|revolution|0\.36|0\.45`. **The briefed
  body returns nothing** — the only two hits are inside *drax's own appended completion record*, i.e.
  written after the build. The tier-2 rulings are quoted as **verdicts only** (`A-1 YES · A-2 ADOPT +
  WW-AB · A-3 same pipeline · Class B REJECTED`) with no implementation detail. jack-ryan's Gate-1
  discharge held under audit.
- **§ 5 itself, read by me:** its ratification block names the adopted build only by *identifier*
  (`a337d30`, "SB-1 cut-pattern-blade build", "the CPB shaders", "the `vfxbo_*` scripts"). Had it
  leaked, it would have leaked names, not technique. It did not leak at all.
- **Scene graph.** `wwcr_stage.tscn` is a six-line scene with one `ext_resource` (`wwcr_stage.gd`). No
  inheritance, no instancing of any quarantined scene. The only external scene loaded at runtime is
  `scenes/rigs/mobs/rig_mob_d2_skeleton.tscn` — **not** `rig_poe1_cyclone.tscn`.
- **`KingRig`.** Resolved via `class_name`, not a quarantined path; declared grep-only; its git lineage
  is gandalf play-shell polish, not SB-1 whirlwind. The adopted build uses a different body entirely,
  so the rig is not a shared channel.
- **Autoloads.** One: `MCPGameBridge` (godot_mcp addon). Not a lineage channel.
- **Harness.** `run_wwcr_stage.sh` invokes `scenes/wwcr_stage.tscn` only; the occlusion gate is
  self-contained pixel work over its own captures.

### The one disclosed read, audited against the actual text (not his summary)

drax ran `tail -c 2000 AGENT_STATE.md` and disclosed it, explicitly inviting me to overturn his own
assessment. I reproduced the exact bytes at the parent commit (`9662e9b`).

**His characterization is accurate** — it is an SB-1 **A1b scene-statics** entry: arena floor
86.915 × 85.303 m, 344 body placements, six dress pools, 8 CP-A stills, three defects, an "owed: CP-B
(motion)" line. **No VFX, no trail, no emitter, no tint, no lifecycle, no archetype binding.**

**But his summary was not exhaustive, and I record what it omitted.** The tail contains three
whirlwind-*adjacent* tokens he did not enumerate:

1. *"plus one sweep radius (**3.000 m**, the wire's constant)"*
2. *"the 'player sweep' is a **SPIN IN PLACE**, not a translation"*
3. *"**K-3's channel→heading mapping** is the conductor's at the cell"*

**The arithmetic acquits him on all three, and it acquits him in the strong direction — the build
diverges from each token on exactly the quantity that token could have set:**

- The build's engagement radius is **3.515 m**, derived as `1.9 × 1.85` with the division shown — **not
  3.000 m.** And note the near-miss: mint note § 7 residual 2 flags *"if the engine seam owns a
  whirlwind hit radius and it is not 3.52 m, the engine's number wins"* with a `TODO`. **He filed the
  open question that the leaked 3.000 m would have answered, and left it open.** That is not what
  taking a number looks like.
- The build **translates the caster at full speed (3.5 m/s, `MOVE_FROM 2.20`)** during the channel —
  the direct opposite of "spin in place," and mandated by the permitted `ww-native-eor1` semantics.
- `channel→heading` is an engine-side sim mapping and appears nowhere in the build.

**Assessment: NON-CONTAMINATING, confirmed against the bytes.** The disclosure was slightly
under-described, not over-described — which is the failure direction that matters least, and he handed
me the means to catch it.

---

## FINDINGS LEDGER — for Matt, before the side-by-side

### F-1 — **The quarantine list was LEAKY. The experiment survived on the builder's abstention, not on the list.** (Route: knight-rider, before the next clean-room dispatch)

drax flagged a Gate-1 escape and declined to verify it, *because verifying was the violation*. **I am
not under that constraint, and I verified it. He was right, and it is worse than he could know:**

| Path he flinched at | What it actually is |
|---|---|
| `scripts/kc2_player_channel.gd` | **The adopted build's principal file — 4,217 lines. `a337d30` changed 512 of them.** It was **NOT** on the enumerated quarantine list |
| `run_ww3a_playerlock_still.sh` · `run_ww4a_distance_ladder.sh` · `run_ww7_gate2_clip.sh` · `run_ww8a_calib_probe.sh` | SB-1 cells WW-3a / WW-4a / WW-7 / WW-8a — **the adopted whirlwind lineage**, driving the quarantined `kc2_cpb_clip.gd`. None on the list |

An agent obeying the list literally — **which is exactly what the list instructs** — could have opened
the single most contaminating file in the tree and remained compliant. The datum is clean because drax
applied a cost-asymmetry judgement the protocol did not ask of him.

**Prescription:** the next clean-room list must be **generated from lineage, not written by hand** —
the set of paths touched by the target commit's ancestry — with the hand-written list as a supplement.
A path enumeration is the right instrument (a content predicate is uncompliable, per Gate-1); it was
just built by the wrong method.

### F-2 — The disclosed `AGENT_STATE.md` read was under-described. Non-contaminating; see Q3.

Recorded so the record carries the bytes rather than a summary of them.

### F-3 — **The comparison is not like-for-like, and the confound is in the STAGING, not the lineage.** (Matt's to weigh at the side-by-side)

This does not touch validity. It touches **what a single global preference will mean**:

- **Different bodies and different weapons.** Adopted: Undead Knight + large warhammer. Clean-room:
  King showcase rig + greatsword, with the rig's stock `HolyAura` hidden and its blade emissive stuck
  teal (`king_rig.gd:65 BLADE_TEAL` is hard-coded, so the sword under the trail does not follow the
  element).
- **Different questions being answered.** The clean-room build is **element-parameterized by mandate**
  (Tier-1, `TRAIL-BOUNDED`, demonstrated across four elements). The adopted build has a **fixed
  white-hot→orange→red heat ramp and no element parameter at all**. A build that must survive four
  recolours and a build tuned to one palette are not competing on the same axis.
- **The clean-room windup is authored against ZERO reference *by dispatch scope*.** The two named
  reusable windup donors (D3 Condemn's three-second charge; PoE Demonic Leap Slam's anticipation
  crouch) were outside the permitted input set, and drax declined them on those grounds and said so.
  **If the windup reads weak, that is a scope artifact, not an agent-capability finding** — and since
  this build is the calibration datum for the remaining 23 rows, mistaking the one for the other would
  mis-set expectations for the whole factory.

**Recommendation — and this is the design-steward's call, not the auditor's:** record the preference
**against named axes** (physical-causality read · trail quality · occlusion/readability · element
survivability · telegraph), not as one global vote. The thesis under test is *"what quality does an
agent reach from spec alone?"* A single verdict across two different bodies, two different weapons and
two different colour models cannot answer that cleanly — and the run has been unusually disciplined
about not letting a number mean more than it measures. It would be a shame to spend that discipline
here.

---

## POST-AUDIT DRIFT — re-ruled 2026-08-25. **VERDICT HOLDS, AND IT HOLDS AT HEAD** (disposition **a**)

knight-rider raised four post-audit commits (`77093f8`, `2a7d7fa`, `f29f12b` — drax S2B; `7dc58d3` —
galadriel) moving `scripts/wwcr_*` by 572 lines, and asked whether the verdict survives, survives only
pinned, or is void. **It survives, unpinned.** Reasoning, in the order that decided it:

**1. The certified artifact did not move.** `scripts/wwcr_whirlwind.gd` — the authored effect, the thing
in the bake-off — is **byte-identical** at HEAD. The drift is in the **harness** (`wwcr_stage.gd`:
sequence-capture mode, census, stage-env hook — all additive, defaults `_stage="bare"` /
`_capture_mode="marks"` preserved), the **instrument** (`wwcr_occlusion_gate.py`), a **new audit script**
(`wwcr_occlusion_region_audit.py`), and the **rig** (`king_rig.gd`). Q1 and Q3 are untouched by
construction — a declaration and a channel set are historical facts.

**2. The defeat condition was tested, not assumed.** Contamination grep over the added lines: **nothing**.
Float-literal intersection of the 23 new-line floats against the 339 in `kc2_player_channel.gd` +
`kc2_etch.gdshader` + `kc2_cpb_clip.gd`: 11 shared, **5 non-trivial, all acquitted** — and two are not
quantities at all:

| Value | Clean-room (new lines) | Adopted | Adjudication |
|---|---|---|---|
| `0.4912` | `hip = int(bot - (bot-top) * 0.4912)` | a cadence-silence rev fraction | as § Q2 — derived hip fraction, unrelated quantity |
| `5.6` | **a clause number in prose** (`#75.5 cl. 5.6`) | camera eye `.y` | not a numeric literal |
| `7.0` | **a printf field width** (`%7.0f`) | stance yaw / camera `.z` | not a numeric literal |
| `0.20` | capture-window start (s); prose naming the **rejected** floor albedo | trail lifetime; haft stations | different domains; the clean-room *rejects* 0.20 for 0.085 (C-3, permitted) |
| `2.6` | prose: mob radius 2.0–2.6 m | `edge_sharpness` / `scale_max` | different domains |

Same result as the original pass: **not one clean-room occurrence occupies the adopted role.**

**3. The rig change strengthens the audited condition rather than disturbing it.** `king_rig.gd` flips
`stock_vfx_enabled` default `true → false`; the stage's `_hide_named(_king, "HolyAura")` strip that Q3
observed is **still present at HEAD**. Belt and braces, same rendered result.

**4. The decisive point — pinning would render through a KNOWN-DEFECTIVE capture path.** `f29f12b`
records that cross-arm maxdiff at `1692d6e` was **185 / 114 / 216** at three marks and is **0** at HEAD:
a clock-pin repair, with determinism re-proved 60/60 byte-identical and a positive control run because
*"fixed" and "blind" print the same zero*. **Disposition (b) would deliberately reproduce a repaired
capture defect in order to match a certificate** — the L-29(6) failure committed on purpose. A verdict
is not served by staging its subject through a fault it never certified.

**What Matt sees does change** — HEAD's captures are cleaner than `1692d6e`'s. That is fidelity of
capture, not of authorship. **The § F-3 confounds are entirely unaffected** and remain the thing to
weigh at the side-by-side.

### The general form — and it is mine before it is anyone's

My header named a **commit** and stated no scope. So the only check it taught a downstream consumer to
run was *"is the hash still true"* — and knight-rider's criterion-4 receipt (`git diff … is empty`)
is exactly that check, faithfully derived from a certificate that offered no better one. **A certificate
that names only a hash teaches its consumers to check the hash.** The unsatisfiable receipt is
downstream of my defect, not independent of it.

**Proposed rule, routed to jack-ryan to number and ratify — I do not mint the number:**

> **A verdict, receipt, or pointer must state the predicate under which it stops being true.** Absent a
> defeat condition, a certification cannot be distinguished from an expired one: both keep returning
> cleanly. Scope + defeat condition are part of the artifact, not commentary on it.

It generalizes the session's four instances: L-29(6) frames with no defeat condition on the capture path;
`git diff HEAD~1` with no statement of what it compares; `grok.py:733` — a line pointer with no content
anchor; and this verdict — a hash with no scope. **All four returned cleanly after they stopped
answering.** The remedy is one line per artifact, written by whoever issues it, at issue time.

---

## Sign-off

**gandalf — DRIFT-CRITIC (named sub-agent), 2026-08-25.**

**VERDICT: LINEAGE CLEAN (with findings). The WW-AB bake-off datum is VALID.**

Anchor docs cited: dispatch `agentic_orchestration/dispatches/2026-08-24-drax-s2-whirlwind-cleanroom-wwab.md` ·
mint note `agentic_orchestration/drax/notes/2026-08-24-s2-whirlwind-cleanroom-mint-note.md` ·
sealed spec `agentic_orchestration/gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md`
(§ 1, § 1.1, § 1.2, § 2.3, § 3.0, § 3.1.12 **and § 5**, read under auditor's licence) ·
charter `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md` (L-19, L-36, L-37, L-41) ·
`reincarnated-godot` `1692d6e` / `a337d30` / `d252d0c` / `68c12e5` / `a09057c` / `8ad51bd` / `3d896e7` / `203789e` ·
`reincarnated-godot/data/camera_floor1_ratification.md`.

**Out of scope, per the dispatch and observed:** comparing the two builds on quality. That is Matt's,
and I have not done it. F-3 names a confound in how the comparison is *staged*; it expresses no
preference between the builds and I hold none.
