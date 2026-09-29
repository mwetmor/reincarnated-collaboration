# Finding — 2026-09-29 — Run JOIN-1 charter **v0.2** + precondition **J-P2** (Gate-1 RE-CHECK, pre-launch)

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1 re-check)
**Verdict:** **BLOCK — narrow. ONE new finding, and it is not in the charter.** Charter v0.2 by itself: **PASS.** 7 of 7 BLOCKs **DISCHARGED**, 10 of 10 WARNs disposed (four exceeded). **1 new BLOCK · 4 new WARN · 6 new INFO.** **GO for launch on Matt's word the moment `RC-B1` lands.**
**Targets, both hashed before reading, per the brief's HALT condition:**
- `agentic_orchestration/gandalf/notes/2026-09-29-join-1-run-charter.md` v0.2, 132 lines — derived `789d96915b901b4519de597d289015558dd1cd8b8b570c5c0de01d24c927d9fb` — **matches `789d9691…`. PASSED.**
- `reincarnated-engine/src/reincarnated/simulation/math/kc2-join1-golden-master-instrument-2026-09-29.md` (engine `bec6d254`), 303 lines — derived `54b62b56a4a1960e473976b5aac64c80df058779cfc42fc05476737f706ff170` — **matches `54b62b56…`. PASSED.**

**Predecessor gate:** `qa/findings/2026-09-29-run-JOIN-1-charter-gate1.md` (collab `570251ee4`; v0.1 `b8c2cb92…`) — BLOCK-narrow, 7 BLOCK / 10 WARN / 7 INFO.
**Authors under review:** gandalf (`ARCHITECT`, charter v0.2 + § 9 discharge table) · gamora (`J-P2`, the golden-master instrument).
**Principles applied:** 1 · 2 · 3 · 4 · 5. **Disciplines:** #1, #11, #12, #24, #62(a), #63, #72, #73, #75 cl. 6, #79/Law 3, **#80**, **#86** · K-7 · GL-12 · ADR-002, ADR-004, ADR-006 · CLAUDE.md `git -C` wrong-repo note (both faces).

---

## 0. Verdict in one paragraph

**The seven BLOCKs are discharged, not merely addressed, and two of them are discharged better than I asked.** `J-P2` does the thing I could not require and only hoped for: it classified the 29 rows honestly, found set 1 **non-empty but weak (4 rows)**, and then **printed on its own face that the finding survives the classification** — no EXACT row grades the monster→player mitigation order on the graded path, so the numeric fixture is not an enhancement of the golden master, it *is* the golden master. An instrument note that reports its own blind spot in § 0 and then builds the grain (`G2` intermediates) and the control (`NC-2`, Δ 398.384) that close it is the correct answer to BLOCK-A, and § 5's gate — *"the golden master may not be quoted GREEN until every control has been shown to RED"* — is #80 made operative rather than cited. **The one new BLOCK is one level down and it is the same species the whole gate has been about: the FROZEN "BEFORE" SIDE OF BOTH INSTRUMENTS CANNOT BE PRODUCED AS SPECIFIED.** The invariance command runs `python -m reincarnated.simulation.kc2.run --emit-fixture …` against a worktree of the **sealed** tree — and there is no CLI entry point anywhere in `src/reincarnated/simulation/kc2/` today, let alone in a tree frozen before the emitter was written. The port half has the mirror defect from the other direction: `GM-OQ-2` seats port emission **at J2**, after the extraction it exists to guard. Neither emitter, the CLI, nor the normaliser is seated in § 5; the two `J-S6` tags do not exist and are cut by a **different run** with no carrier. Five clauses and one § 5 row clear all of it. **Nothing here is a design objection, and nothing needs Matt.**

---

## 1. The asked questions, answered

### 1.1 Is each BLOCK discharged (not merely addressed)?

| v0.1 BLOCK | v0.2 / J-P2 | verdict |
|---|---|---|
| **A** golden master unfalsifiable (#80, #86) | § 4.3 rewritten as a numeric diff; `J-S8` substrate row; J-P2 delivers the 4/9/16 classification, the seven-grain fixture with **intermediate stages**, a bit-equality tolerance law with one closed exception, four negative controls with a **must-have-RED gate**, and § 2.2 stating the mitigation-order hole | ⚑ **DISCHARGED — exceeded.** Residual `RC-W1` (wording) |
| **B** `ORACLE` invariance was prose | `J-S6` tags; § 4.7 byte-identical row; § 6 HALT; J-P2 § 6 adds a frozen worktree, PRE-executed-once, three named streams, a **pinned normaliser**, the instrument's **own** negative control, and the three-line seal-digest bridge (#73) | **DISCHARGED IN DESIGN — exceeded. NOT YET IN INSTRUMENT:** see `RC-B1` |
| **C** B0 cannot fail; confounded | § 4.2 pass rule + closed disposition set + *"an undisposed row is a B0 FAIL and a finding, not a deliverable"* + deconfound-first with the APPROX ceiling printed on every figure + Gate-2 + TL restored | **DISCHARGED** |
| **D** lever row cannot evaluate (Law 3) | `gd_referent_value ∈ {value \| NONE — no GD rule}`; L-03/L-08/L-11 named; the 8 implemented ids **enumerated**; 6 `REGISTERED-UNEXERCISED`; § 2.3 names L-14/L-15; L-16 settable | **DISCHARGED** — all three limbs. Census-checked, see `RC-I3` |
| **E** coverage gameable | denominator frozen at J-S2's 14; reclassification (`OUT-OF-ARENA` especially) a named finding; **second fraction: implemented-and-ACTIVE** | **DISCHARGED**. Minor `RC-I4` |
| **F** home margin unsourced (#1) | `J-S7` pins the three D2 frontier tables; the **POINT** is commission `C-12` at J4; a negative result DEFERS home margin **on the fidelity-cost table's own face** | **DISCHARGED** — the row now evaluates on either branch. Residual `RC-W4` |
| **G** no independent gate at J0/J1 | Gate-2 seated at J0 (ablation classes + E-2) and J1 (schema-gap list), in § 5 **and** in § 4.1/§ 4.2; § 3 F4 now names J0, J1, J2, J5 | **DISCHARGED** |

**7 / 7.** The discharge table at § 9 is itself correct: I checked every row against the body and found no row claiming an edit the body does not contain — which is the failure mode a self-reported discharge table invites, and it did not happen here.

### 1.2 BLOCK-A specifically: is the golden master now falsifiable (#80) and on the path (#86)?

**Yes, and the reasoning is J-P2's, not the charter's — which is the right division of labour and worth saying plainly.**

- **#80, falsifiable.** The gate is no longer a pass/fail re-grade. It is a per-cell numeric diff whose fields are **bit-equality by default** (Limb B), with exactly one named float exception carrying its own accumulation-depth invalidation rule (Limb C — *"a realised depth above ~4,500 terms makes the field UNGRADEABLE, not green"*; that is a tolerance that can refuse, which is rare and correct). And it may not be **quoted** green until four controls have each been shown to **red** against the frozen fixture. **An instrument that has never failed has not been shown to be able to** — J-P2 states the rule and then gates on it. That is the discharge; the classification alone would not have been.
- **#86, on the path.** `G2` records `after_stage_1` / `after_stage_2` **positionally**, with `stage_order` naming what stage 1 was, so a reorder shows as a **value** change and not a label change; `armour_branch` distinguishes the two `threat.py:305-310` branches that diverge nonlinearly. `NC-2` needs **no code change** (both `OrderLimb` limbs are live today — I verified `intake.py:331-332`), predicts its non-movement as well as its movement (the nine non-physical families take one multiply and are invariant), and carries a published magnitude, **Δ 398.384 on a 5,000-point hit**. The J-P2 sentence that earns the discharge is the self-indicting one: *"If `G2` held only `applied`, this control would partially pass — and the golden master would be green through a mitigation reorder."*
- **Given J-P2's own finding that set 1 has no oracle-side execution and mitigation order is graded by no EXACT row** — the four set-1 rows are correctly demoted to *"which prereg rows may be quoted beside the gate"*, and the load is carried by `J-S8`. **I agree with that allocation and with the honesty of stating it.** `TA-X-30` is the only set-1 row with a demonstrated red (103/128 movers); `TA-X-07` is explicitly declared **blind to a conserving change**; `TA-X-29(d)` is unexercised; `TA-X-20` grades a predicate's form at two probe distances. A gate resting on those four alone would have been BLOCK-A wearing a classification.
- **One residual, and it is in the charter's paraphrase, not the instrument:** `RC-W1` below.

### 1.3 Is *"frozen from the CONFIGURATION, not the seal verdict"* consistent with J-P1 still requiring the seal?

**Yes — they are different objects, and the de-risking is real.** The fixture's **validity** is a property of the configuration it was emitted under (§ 3.1's limb set, fold settings, arms, salts, packs). `J-P1` is the run's **launch authority** and the source of `J-S1`'s and `J-S6`'s identity. `Q83(b)` / `TA-X-06` is a question about the *port's distinctness grade*, not about what the fight *did*; a behavioural record does not inherit a grading block. JOIN-1's golden master genuinely is not hostage to `Q83(b)`, and the conductor should know he has that.

**Three seams the composition leaves open — one clause each (`RC-W2`):**
1. **The charter's own `J-S8` pin column reads *"frozen at the seal"*** — the precise dependency J-P2 § 3.1 disclaims. Temporal, presumably; it reads as conditional.
2. **There is no failure branch for `J-P1`.** § 8 states the gate and never states what happens if it does not pass, or if the sealed configuration of record differs from § 3.1's. § 7 covers a pack movement (c) and a C-11 alteration (f) — not *"the seal lands on a different limb set"* and not *"the seal does not land."* A precondition with no negative branch is a decision deferred into the run.
3. ⚑ **`J-S6`'s tags do not exist, and they are cut by a different run.** Verified this session: `git tag -l 'kc2/*'` returns **empty in both `reincarnated-engine` and `reincarnated-godot`.** The pin column says *"tags cut at the seal"* — the seal is **KC2-PLAY's** event, and nothing in either document, in either run, seats the cutting. J-P2 § 6.1 opens *"`J-S6` already commits the tags,"* which is true of the charter's intent and false of the repository. **If KC2-PLAY closes without cutting them, JOIN-1's entire preservation story is a commit hash somebody has to find later.** Cross-referenced into `RC-B1`(d) because it is the same omission.

### 1.4 Are the WARN dispositions adequate?

**Yes — all ten disposed, none by relabelling, and four disposed further than asked.**

WARN-1 ✓ (`46 + 3 = 49`; I re-checked the sub-counts and they still close) · WARN-2 ✓ (ROWSET-shaped, derived at launch, and § 7 now says *"applied in § 1 of this document"* — #75 cl. 6 closed against the document that stated the law) · WARN-3 ✓ (TL, GV, E-2 restored; C-12 added) · WARN-4 ✓ (see 1.5) · WARN-5 ✓ **exceeded** — § 6 HALT + § 8 row, and J-P2 § 7(f) adds *"a C-11 disposition that alters the referent is a fixture RE-FREEZE, and the manifest says so on its own face"*, which is the part that makes the HALT bind on the artifact rather than only on the conductor · WARN-6 ✓ (§ 4.5 defines "runs" mechanically; correctly narrowed to *arena* margin, since home margin may DEFER — a detail my own proposed wording got wrong and the conductor got right) · WARN-7 ✓ **exceeded** — `NC-4` turns *"preserve the `KeyError`"* from a clause into a control whose **expected result is an exception**, with the right sentence attached: *"a silent zero here is a worse outcome than any red in this table"* · WARN-8 ✓ **exceeded** — adopted in § 4.4 and then generalised in J-P2 § 5 to all four controls, plus the must-have-RED gate · WARN-9 ✓ · WARN-10 ✓ (the ⛔ owner-eye checkpoint sits exactly where I proposed, between J3 and J4, with red-flag rulings classed `matt`) · INFO-2/4/5 ✓ carried.

### 1.5 Is J-L1 now correctly the rule?

**Yes.** J-L1 asks for the rule, names the full collision set (dockets **1, 3, 4, 5, 7, 8** + family rows **9–19**), fires docket 5 as the first application, returns the sweep's further hits **as one batch, never silently**, and — the part I did not ask for and which is the right instinct — **excludes boundary / world-shape dockets (2 and 12, allies)** from the rule's reach, so a rule about *kit-internal* mechanisms cannot be quoted at a *boundary* disposition later. The census's ordering constraint (*"a deliberate sweep before B3 seeds the lever registry"*) is **satisfied** by the wave plan: sweep at **J0**, registry at **J3 / § 4.4**. It is satisfied but not **asserted** — see `RC-I5`.

---

## 2. NEW BLOCK

### RC-B1 — the frozen "BEFORE" side of both instruments cannot be produced as specified. Neither emitter is seated, and on the oracle side the PRE tree can never have the flag the PRE command passes it (#86, #24)

Both new instruments rest on a baseline captured **before** the J2 extraction. Five limbs, verified this session against the repositories:

**(a) ⚑ The invariance command's PRE side is logically impossible as written.** J-P2 § 6.2 runs, for `SIDE ∈ {pre, post}`:

```
python -m reincarnated.simulation.kc2.run --config "$CFG" --arm "$ARM" --salt "$SALT" \
    --model-pack … --emit-fixture join1-gm-fixture-v1 --out "$OUT"
```

**There is no CLI entry point anywhere in `src/reincarnated/simulation/kc2/`.** Verified: `grep -rln "argparse\|__main__"` over the whole directory returns **nothing**; `run.py` is a 393 KB composition-harness *module* whose docstring says it *"writes no JSON and owns no schema version."* `--emit-fixture` does not exist in `src/reincarnated/` at all — its only occurrence in the engine repo is line 222 of J-P2 itself. That alone is a build gap and would be a WARN. **It is a BLOCK because of what PRE is:** § 6.1 cl. 2 requires the PRE side to be *"executed ONCE"* from a worktree checked out at the **sealed** tag — a tree that by construction predates the emitter and will never contain the flag. **The baseline cannot be taken from the frozen tree, and a baseline taken from a patched frozen tree is not frozen.** § 4.7 is a DONE row under a § 4 headed *"DONE when every row evaluates"*; as specified it cannot evaluate. Same shape as v0.1 BLOCK-D(ii), one level down.

**(b) ⚑ The port half has the mirror defect, from the other direction.** `GM-OQ-2` recommends drax emit the port side of `J-S8` *"at J2 alongside the rulebook."* **J2 is the extraction the fixture exists to guard.** A port baseline first emitted from post-extraction code is not a baseline — it is the refactored system describing itself, which is BLOCK-A's own species on the side of the comparison nobody was watching. The recommendation is one word from correct: the port emits at **freeze**, pre-J2; the J2 emission is the **POST** side.

**(c) Nothing in § 5 seats the build.** § 5's `pre-launch` row seats gamora for the *note*. The oracle emitter, the CLI, drax's port emitter and `tools/join1_stdout_normalise.sed` (whose `sha256` § 6.3 pins, and which does not exist) have **no wave, no seat and no gate**.

**(d) The `J-S6` tags do not exist and are cut by another run** — § 1.3(3) above. `git tag -l 'kc2/*'` is empty in engine and in godot.

**(e) The worktree is cut from the wrong tag, in the wrong repo's sense.** § 6.2 runs `git -C ~/Games/reincarnated-engine worktree add … kc2/referent-v1-runtime` and then executes the **python oracle** in it. Per `J-S6`, `kc2/referent-v1-runtime` is **the runtime / port** (J-P2 § 3.1: *"Port: drax, the godot runtime (`kc2rt_ta.gd` lineage)"*); the oracle's tag is `kc2/referent-v1-oracle`. This is CLAUDE.md's `git -C` wrong-repo hazard **written into a committed command** — and it is the second face, the one that produces a correct reading of the wrong tree.

**Why BLOCK and not WARN.** Every other finding in this re-check is wording or hygiene. This one means that on the day J2 lands, the run discovers it has **no pre-extraction record of either side** and must either reconstruct one from the refactored code or skip the check. Both outcomes are the failure this entire gate — v0.1 and v0.2 — has been about. It is cheap now and unrecoverable later: once the extraction is committed on a shared tree, "before" is gone.

**Minimal discharge (conductor + gamora + drax; one § 5 row and four clauses; none of it needs Matt).**
1. **§ 5 gains a `pre-launch` build row:** gamora — the `G1…G7` oracle emitter **and** the `kc2` CLI entry point; drax — the port emitter to the same schema; the committed `join1_stdout_normalise.sed`. Gate: jack-ryan, alongside the fixture freeze.
2. ⚑ **State the resolution of (a) explicitly, because there is only one honest one:** the PRE tags are cut at a commit that **already contains** the emitter and CLI, and the emitter is **behaviour-neutral by construction** (records, never branches). **Its neutrality is not asserted — it is what the invariance check's own first green measures.** Say so; otherwise someone patches the frozen worktree and the word "frozen" stops meaning anything.
3. **`GM-OQ-2` is answered "at fixture FREEZE for the PRE side; at J2 for the POST side"**, not "at J2".
4. **Fix the tag:** the engine worktree is cut from `kc2/referent-v1-oracle`.
5. **One line into KC2-PLAY's seal checklist:** *"cut `kc2/referent-v1-oracle` (engine) and `kc2/referent-v1-runtime` (godot) at the seal — JOIN-1 `J-S6` depends on them."* An obligation recorded only in the run that consumes it is #73 across a run boundary.

---

## 3. NEW WARN findings — each with the edit that clears it

**RC-W1 — § 4.3 carries two referents for one phrase in adjacent sentences, and its parenthetical drops the exact field BLOCK-A was about.** § 4.3 reads *"a numeric diff against the `J-S8` fixture **on the J-P2 `EXECUTES-THE-BOUNDARY-RULEBOOK` set** (… **applied damage per packet after mitigation** …)"*, then *"**the golden master's verdict is over that set**; `ABSENCE-SATISFIED` and `DOES-NOT-TOUCH` rows are reported, never quoted as the gate."* In the second sentence "that set" means *the four EXACT rows*. In the first it must mean *the boundary-determined quantities* — because the fixture's grains are per-tick and per-packet records over the full 5 × 5, and **no EXACT row grades mitigation order at all** (J-P2 § 2.2). **Read the first sentence with the second sentence's referent and the fixture diff is restricted to four rows, and § 2.2's hole re-opens.** Worse, the parenthetical enumerates **final** values only — and J-P2 § 3 says in terms that *"a diff on FINAL values only is a re-grade wearing a diff's clothes"*, which is why `after_stage_1` / `after_stage_2` exist. **The charter's paraphrase of the fixture omits the field that makes the fixture work.**
**Edit:** *"the golden master is **the per-cell numeric diff of the whole `J-S8` fixture (`G1…G7`, all 25 cells, including `G2`'s per-stage intermediates)** under J-P2's tolerance law. Separately, **of prereg v1.6's 29 EXACT rows only the four in `EXECUTES-THE-BOUNDARY-RULEBOOK` may be quoted beside it**; the other 25 are reported, never quoted as the gate."* Two claims, two sentences, one referent each.

**RC-W2 — `J-P1` has no failure branch, and `J-S8`'s pin column contradicts J-P2 § 3.1.** § 1.3 above. Nothing says what JOIN-1 does if the seal does not land, or if the sealed configuration of record differs from the one the fixture was frozen under.
**Edit:** `J-S8`'s pin column reads *"frozen from the § 3.1 CONFIGURATION (J-P2), not from the seal verdict; FILE and ROWSET digests labelled"*; and § 8's `J-P1` row gains *"if the seal does not land, or lands on a configuration differing from J-P2 § 3.1, the fixture is VOID and re-freezes under a new id; JOIN-1 does not launch on a fixture whose configuration is not the sealed one."*

**RC-W3 — every `research/…` path in both documents is repo-relative with no repo named, and the tree is not in the repo the reader is standing in.** Verified: `research/curated/kits-export/` and `research/datamine-acquisition/` **do not exist in `reincarnated-engine`**; both live at `reincarnated-collaboration/agentic_orchestration/research/…`. `J-S3`, `J-S4` and `J-S7` name them bare, and **J-P2 — which lives in the engine repo — writes `research/evidence/join1/…` as its fixture emission path**, which a reader will resolve against the engine. This interacts directly with § 6's *"a write outside a seat's named tree"* HALT: a HALT boundary cannot bind on a path whose repo is ambiguous. Same hazard CLAUDE.md records twice, in both faces.
**Edit:** absolute or repo-qualified paths on `J-S3`, `J-S4`, `J-S7` and J-P2 § 3.3, and **name the repo the fixture is committed to** (collaboration, alongside the rest of `research/`, unless the conductor intends otherwise — either is fine; the silence is not). J-L5's push posture already covers all three repos, so no scope question follows.

**RC-W4 — `J-S7`'s three tables are GITIGNORED. In a table headed "frozen at launch", "pinned" means something different for this row than for every other row.** Verified: all three exist on disk (`MonStats.txt` 431 KB, `MonLvl.txt` 14.6 KB, `Levels.txt` 66 KB) and **`git check-ignore` reports all three excluded by `agentic_orchestration/research/datamine-acquisition/.gitignore:1: */raw/`**; `git ls-files` on the directory returns empty. The real pin is the upstream `fabd/diablo2 @ 45112569…` commit — a third-party mirror — and the local copies carry no derived digest. **This is KP-92's `tmp/` durability hazard in a different coat, and J-P2 § 7(a) names that hazard as the founding instance five pages earlier.**
**Edit:** `J-S7` gains *"⚑ the raw tables are **gitignored** (`*/raw/`); their pin is therefore the upstream commit **plus a FILE digest derived at launch and recorded in the run state**, not a commit of record in this repo."* Section § 1's header already mandates derive-at-launch; the gap is that a reader assumes committed.

---

## 4. INFO

- **RC-I1 — ⚑ zero relay defects in a note that pins fourteen things, against a charter § 7 that prints *"four relay defects in two laps."*** I re-derived every hash and hand-checked every line pin in J-P2. All four document digests reproduce exactly (`GM-1 db2c0ca3…`, `GM-2 789d9691…`, `GM-3 5e6e87fc…` — my own Gate-1 file — and `GM-4 5a5f45d7…`). All eight source pins are correct: `mitigate` :245 · `raise KeyError` :288 · the two armour branches :305-310 (`…DLEP` absorb / `…DGP` overflow, the Crate typo and all) · `PTH_MINIMUM = 55.0` :317 · `PTH_THRESHOLDS` :318 · `probability_to_hit` :327 · `resolve_hit` :368 · the fold consumption :1826-1836, where the line is literally `om = om + own_add` — **the additive own-term `TA-X-29(b)` describes, present in the code exactly as claimed.** `OrderLimb` :325-332 with **both limbs live**, so `NC-2` genuinely needs no code change. Recorded because the discipline that produced it is the one the charter was worried about.
- **RC-I2 — the two mitigation-order declarations in the codebase DISAGREE TODAY, which strengthens § 2.2 further than J-P2 claims.** `threat.py:267` documents `mitigate` as `intake.OrderLimb.RESIST_THEN_ARMOUR`, and `intake.py:326-330` declares PRIMARY as `ARMOUR_THEN_RESIST` **with an explicit Discipline #12 semantic-shift flag**: *"`threat.mitigate` has DECLARED the opposite order since PM-2."* So J2's extraction does not merely *risk* reordering the rule — **it must choose between two live, contradictory declarations**, and no EXACT row will notice which it picks. `G2`'s `stage_order` field is what records the choice. Recorded so the conductor meets this at J2 as a known fork rather than as a red.
- **RC-I3 — L-16's reclassification is census-faithful and does not re-open BLOCK-D(i).** I raised L-16 at v0.1 BLOCK-D(iii) as a misclassified build item; v0.2 makes it a settable lever with *"player-driven (GD default)"*, which reads like the invented-constant-wearing-an-inherited-label defect BLOCK-D(i) was about. **It is not.** Census § 9 gives L-16 a GD-referent value of `player-driven` — unlike L-14/L-15 (*none*), L-03 (*no GD rule*), L-08 (*undefined*) and L-11 (*no generic term*). GD has a rule ("the player decides"); what is missing is the *alternate* setting. **The conductor's three DECLARED-INVENTED instances (L-03, L-08, L-11) are the complete set, and keeping L-16 out of it was correct.**
- **RC-I4 — `J-S2`'s parenthetical attaches to the wrong number.** It reads *"D2 WW Barb: 14 rows, 9 BOUNDARY **(the § 4.5 coverage denominator)**"* while § 4.5 fixes the denominator at **14** (*"rows mapped / 14"*). Move the parenthetical to `14`, or the row a run quotes under pressure says 9.
- **RC-I5 — the census's ordering constraint is satisfied but not asserted.** *"A deliberate sweep **before** B3 seeds the lever registry"* holds by the wave plan (sweep J0 → registry J3) and by nothing else. One clause on § 4.4 — *"the registry is not seeded until the J0 docket sweep is filed"* — makes it a property of the charter rather than of the current wave ordering.
- **RC-I6 — § 6.2's normaliser destroys its own evidence.** `sed -E -f … -i '' {}` rewrites `stdout.txt` **in place**, so the unnormalised stream — the thing a dispute about the normaliser would need — is gone, and the pinned-`sha256` protection on the filter no longer has anything to protect. Write normalised output to a sibling (`stdout.norm.txt`) and digest both. (Also: `sed -i ''` is BSD-form, correct on this Mac and not portable; harmless here, worth a comment.)
- **RC-I7 — pre-launch state, recorded so a later reader can tell what moved.** No `join*` tree under `agentic_orchestration/`; no `kc2/*` tags in engine or godot; `kits-export/` tracked with both `d2-ww-barb.json` and `gd-eor-warlord.json` present; `simulation/kit_compiler/` present; `research/evidence/join1/` absent. **Nothing has launched.**

---

## 5. Action summary

**gandalf (conductor) + gamora + drax — pre-launch. One BLOCK, four WARNs; none needs Matt:**
- [ ] ⚑ **`RC-B1`** — § 5 gains a pre-launch **build** row (oracle emitter + `kc2` CLI + port emitter + committed normaliser, gated); state that the PRE tags are cut at a commit that already contains a **behaviour-neutral** emitter, whose neutrality the invariance check's first green is what measures; answer `GM-OQ-2` **"PRE at freeze, POST at J2"**; cut the engine worktree from **`kc2/referent-v1-oracle`**; and put one line into **KC2-PLAY's** seal checklist so the two tags actually get cut.
- [ ] `RC-W1` — § 4.3 split into two sentences: the diff is the **whole `J-S8` fixture including `G2` intermediates**; the four set-1 rows are what may be **quoted beside** it.
- [ ] `RC-W2` — `J-S8`'s pin column says *"frozen from the CONFIGURATION"*; § 8's `J-P1` row gains its failure branch.
- [ ] `RC-W3` — name the repo on every `research/…` path, in both documents.
- [ ] `RC-W4` — `J-S7` records that the raw tables are gitignored and that the pin is the upstream commit **plus** a launch-derived FILE digest.
- [ ] `RC-I4` move the parenthetical to 14 · `RC-I5` assert the sweep-before-registry ordering on § 4.4 · `RC-I6` keep the raw stdout.

**Matt — no new surface.** The launch sheet is unchanged from my Gate-1 assessment: **J-L1 (now correctly the rule), J-L2, J-L3, J-L4, J-L5 as drafted.** I agree with all five recommendations. Nothing in this re-check adds a decision, removes one, or changes one.

**ADR-002 approval authority.** Every item above is charter wording, an instrument-note clause, a substrate-row annotation, a wave seat, or a path qualification **inside a not-yet-launched draft** — **mine to approve directly, and I approve `RC-W1` … `RC-W4` and the INFOs on execution, with no re-gate.** `RC-B1` I will sign off on sight of the § 5 row and the four clauses; it is a BLOCK because of what it costs if it is discovered at J2, not because it needs anyone's authority above mine.

**RE-CHECK VERDICT: BLOCK — narrow, one finding, and the charter is not where it lives.** Charter v0.2 discharges all seven BLOCKs and all ten WARNs, four of them past what I asked. `J-P2` is the strongest instrument note this project has produced: it classified honestly, found its own set 1 weak, said so in its first paragraph, and built the grain and the control that close the hole it had just admitted. **`RC-B1` is the same lesson one layer down — the "before" side of an instrument is an artifact somebody has to make, and an instrument whose baseline is produced by the change it guards has no baseline.** Land `RC-B1` and **JOIN-1 is GO for launch on Matt's word.**

---

## 6. References

**Under review**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-29-join-1-run-charter.md` (v0.2, `789d9691…`, 132 lines)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-join1-golden-master-instrument-2026-09-29.md` (`J-P2`, `54b62b56…`, 303 lines, engine `bec6d254`)

**Predecessor + authority**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-09-29-run-JOIN-1-charter-gate1.md` (`5e6e87fc…`, collab `570251ee4`)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-09-29-run-KC2-PLAY-w2-prereg-v1.6-preread.md` (`5a5f45d7…`)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.6.md` (`db2c0ca3…`)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond/notes/2026-09-28-join1-p0-internal-boundary-census.md` — §§ 0, 6 (B8), 7.1, 9 (the lever table, for `RC-I3`)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/operating-procedures/desirable-run-pattern.md` — §§ 1, 5.2, 6.1–6.3
- `/Users/admin/Games/reincarnated-collaboration/CLAUDE.md` — push-pattern section; the `git -C` wrong-repo note, both faces

**Source verified by hand this session**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/threat.py` — :245, :267, :288, :305-310, :317-318, :327, :368, :1826-1836
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/intake.py` — `OrderLimb` :325-332, both limbs live
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/` — **no `argparse`, no `__main__`, no `--emit-fixture` (the `RC-B1` evidence)**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/kits-export/` — tracked; both kit JSONs present
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/datamine-acquisition/d2/raw/` — `MonStats.txt` / `MonLvl.txt` / `Levels.txt` present and **gitignored** (`.gitignore:1: */raw/`)
- `git tag -l 'kc2/*'` — **empty in `reincarnated-engine` and in `reincarnated-godot`**

*Filed 2026-09-29 by jack-ryan, DESIGN-MODE Gate-1 re-check, pre-launch. Both target hashes derived before reading, per the brief's HALT condition. No production code. No push.*

---

# RE-CHECK 2 — 2026-09-29 — charter **v0.3** (`e84cbbcd4`)

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1 re-check 2, pre-launch)
**Verdict:** ⚑ **GO FOR LAUNCH ON MATT'S WORD. `RC-B1` DISCHARGED.** No BLOCK. **2 new WARN, both discharged by ONE corrigendum, and neither gates launch — they gate `J0-F`'s first hour.**
**Target hashed before reading, per the brief's HALT condition:** `agentic_orchestration/gandalf/notes/2026-09-29-join-1-run-charter.md`, 146 lines — derived `e728e8f5529bc8e9bc90131c2439d9f8dacdc3393ede12a78e9c062a5c0173d6` — **matches `e728e8f5…`. PASSED.**
**Principles applied:** 1 · 2 · 3 · 4 · 5. **Disciplines:** #1, #24, #73, #80, #86 · ADR-002 · CLAUDE.md `git -C` wrong-repo note (second face) · § 7 *derive-don't-relay* and *corrigenda-forward*.

## 1. `RC-B1` — DISCHARGED, and on two clauses better than I asked

| `RC-B1` discharge clause | v0.3 | Verdict |
|---|---|---|
| **1.** § 5 gains a gated pre-launch build row with seats | **`J0-F`**, first wave, before anything touches the join path: gamora (engine) · drax (godot); emitters + pinned normaliser; gate **jack-ryan Gate-2** | **DISCHARGED** |
| **2.** PRE tag cut at a commit already containing a *behaviour-neutral* emitter, neutrality measured by invariance's first green | ⚑ **SUPERSEDED BY A BETTER ANSWER.** Emitters are **external harness scripts OUTSIDE the sealed packages**, importing the sealed code **unmodified**. Neutrality is then **structural, not measured** — the sealed tree is never patched, so "frozen" keeps its meaning by construction rather than by evidence. **This dissolves the problem instead of instrumenting it** | **DISCHARGED — exceeded** |
| **3.** `GM-OQ-2` answered "PRE at freeze, POST at J2" | `J0-F` freezes **both sides**, and **"No J2 commit may land before J-S8 is frozen and its digests recorded."** Unambiguous, and stated as a precondition rather than a recommendation | **DISCHARGED in the charter** (see `RC2-W1` for where it is not) |
| **4.** Engine worktree cut from `kc2/referent-v1-oracle` | `J-S6`: each tag in its **OWN** repo, named with its seat — engine tag by gamora, godot tag by drax; "the engine worktree is cut from the ENGINE tag" | **DISCHARGED** |
| **5.** One line into **KC2-PLAY's** seal checklist so the tags get cut | ⚑ **MOOTED BY DESIGN, and that is the stronger disposition.** v0.3 moved tag-cutting **into JOIN-1's own first wave**. My clause 5 asked to *record* a cross-run obligation; v0.3 **removed the cross-run obligation**. An obligation you do not have cannot be dropped at a run boundary | **MOOTED — recorded, per the mooted-escalation corollary** |

**Verified this session, not relayed:** `git tag -l 'kc2/*'` still empty in both repos — **correct and expected under v0.3**, which cuts them at `J0-F`, not at the seal. All four named target trees exist: `simulation/scripts/` (engine), `kc2_play/tools/` and `kc2_runtime/tools/` (godot).

## 2. `RC-W1` … `RC-W4`

| | Disposition | Verdict |
|---|---|---|
| **`RC-W1`** | § 4.3 split into **(i)** the J-S8 fixture diff — *the load-bearing half* — and **(ii)** the four EXECUTES rows *reported beside it*. **Every new particular verified line-by-line against J-P2, none relayed:** the four ids `TA-X-07/20/29/30` (J-P2 :91) · five arms (:114) · salts `0…4` (:115) · `G1.pth_raw`/`pth_effective` (:126) · `G2` positional intermediates + `armour_branch` (:127) · the single Z5 exception (:169) | ⚑ **DISCHARGED — exact.** It restored the field whose omission was the finding |
| **`RC-W2`** | § 8 `J-P1` gains both branches: T-A structural-red after both attempts **or** T-C "no" → **JOIN-1 does not launch**; fixture survives a T-C round-trip unless the fix moves the reference, then **re-frozen, never amended** | **DISCHARGED** |
| **`RC-W3`** | § 9.1 claims *"J-S7 and J-S8 paths now carry their repo."* True of those two rows | ⚑ **PARTIAL — see `RC2-W1`.** I named **`J-S3`, `J-S4` and the J-P2 limb**; the discharge line silently narrowed the finding to two rows |
| **`RC-W4`** | `J-S7` records the tables as GITIGNORED and pins them by **a committed manifest of FILE sha256s derived at launch**; pin column changed to match | **DISCHARGED** |

## 3. New — 2 WARN, one corrigendum clears both

**`RC2-W1` — the instrument the two `J0-F` seats will open is UNAMENDED, and one of its stale clauses instructs a seat BY NAME to do the thing `RC-B1` was raised to prevent.** Verified: J-P2 is still `bec6d254` / FILE `54b62b56…` — the exact hash v0.3's `J-S8` cites as authoritative. Three clauses now contradict the charter that governs them:

- ⚑ **:286 `GM-OQ-2` still answers "drax … at J2 alongside the rulebook."** The charter says both sides freeze at `J0-F` before any J2 commit. **This is `RC-B1`(b) verbatim, still live, in the row addressed to the seat who executes it.** A conductor reading § 9.1 sees RC-B1 discharged; drax reading his own answer row is told J2. That is #73 pointed at a person.
- **:222 `--emit-fixture`** — a flag that exists nowhere in `src/reincarnated/`. Fails **loudly**; harmless.
- **:204 / :211-212** — engine worktree cut from `kc2/referent-v1-runtime`. Under v0.3 that ref lives in **godot**, so in the engine it now fails **loudly** rather than silently. ⚑ **v0.3's per-repo split converted CLAUDE.md's second-face hazard into a first-face one. Worth naming as a gain: the repo separation is what made the wrong command safe.**
- **`RC-W3`'s sharpest limb is here and undischarged:** J-P2 :139-141 emit to bare `research/evidence/join1/…` from a document living in `reincarnated-engine`, where **`research/` does not exist** (verified). `J-S3`/`J-S4` likewise still write `kits-export/…` bare. **`J0-F` is the wave that writes the fixture to that path**, and § 6's *"a write outside a seat's named tree"* HALT cannot bind on a path whose repo is unresolvable.

**`RC2-W2` — `J0-F` states the emitters' INTENT unambiguously and their MECHANISM not at all.** *"External harness scripts under `simulation/scripts/` … run them in worktrees of the tags."* A worktree at `kc2/referent-v1-oracle` **predates the emitter and will not contain it.** Two readings: (a) run the script from the mainline tree with the worktree's `src/` ahead on `sys.path`; (b) copy the script into the worktree. **Only (a) satisfies both "sealed code unmodified" and "frozen"** — (b) writes into a tree the charter calls frozen, which is clause 2's defect re-entering through the door clause 2 closed. Also `kc2_runtime/tools/` **or** `kc2_play/tools/` is an unresolved OR in a path a HALT boundary binds on. **Say (a), and pick one port directory.**

**`RC2-I1`** — v0.3 carries **zero relay defects**: every digest, row id, count and line pin re-derived by hand above. Third consecutive clean lap on § 7's *derive-don't-relay*.

## 4. Action

- [ ] **gamora — J-P2 corrigendum, the FIRST item of `J0-F`, before any emitter is built** (corrigenda-forward, § 7): re-answer `GM-OQ-2` to "**PRE at `J0-F` freeze for BOTH sides; J2 is the POST side**" · replace the `--emit-fixture` command block with the external-harness invocation · fix :204/:211-212 to `kc2/referent-v1-oracle` · repo-qualify :139-141. New FILE sha256 recorded, and `J-S8`'s citation in the charter updated to it.
- [ ] **conductor** — `RC2-W2`: state reading (a) in `J0-F`; name ONE port directory; repo-qualify `J-S3`/`J-S4`.
- [ ] **conductor** — § 9.1's `RC-W3` row reads "J-S7 and J-S8"; the finding named five sites. One line: `PARTIAL — J-S3/J-S4 and J-P2 carried in the corrigendum.`
- [x] **jack-ryan** — Gate-2 seated at `J0-F` on the fixture and the four must-RED controls. Mine already.
- [ ] **Matt** — **nothing new.** No new Matt surface; the launch sheet (§ 6, `J-L1…J-L5`) is unchanged by v0.3.

**ADR-002.** Both WARNs are instrument-note text and charter wording in a not-yet-launched draft — **mine, and I approve them on execution with no re-gate.** I did not hold BLOCK: the charter governs and says so explicitly at `J-S8`, every stale J-P2 clause now fails loudly rather than silently, and the corrigendum lands inside a Gate-2 that is already mine. **Holding a launch on a stale copy of a superseded document would be over-gating — but the corrigendum is a precondition of `J0-F` executing, not a nicety, because `GM-OQ-2` currently tells drax the wrong thing in his own row.**

**RE-CHECK 2 VERDICT: GO FOR LAUNCH ON MATT'S WORD.** `RC-B1` is discharged, twice over on the clauses that mattered — v0.3 did not instrument the patched-frozen-tree problem, it **removed the patch**; and it did not record the cross-run tag obligation, it **removed the cross-run dependency**. ⚑ **The residual is the shape this whole gate keeps finding: the charter moved and the instrument did not.** `RC-B1` was *"an instrument whose baseline is produced by the change it guards has no baseline."* `RC2-W1` is one notch smaller and one layer over — **a discharge recorded in the governing document while the executing document still carries the defect.** The fix is one corrigendum and it is the first hour of `J0-F`.

### References — RE-CHECK 2
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-29-join-1-run-charter.md` — v0.3, `e84cbbcd4`, FILE `e728e8f5…` (§ 1 `J-S6`/`J-S7`/`J-S8` · § 4.3 · § 5 `J0-F` · § 8 `J-P1` · § 9.1)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-join1-golden-master-instrument-2026-09-29.md` — **UNAMENDED** at `bec6d254` / FILE `54b62b56…`; :91, :114-115, :126-127, :139-141, :169, :204, :211-212, :222, :286
- Verified by hand: `git tag -l 'kc2/*'` empty both repos (expected under v0.3) · `simulation/scripts/` · `kc2_play/tools/` · `kc2_runtime/tools/` · `reincarnated-engine/research/` **absent**

*Filed 2026-09-29 by jack-ryan, DESIGN-MODE Gate-1 re-check 2, pre-launch. Target hash derived before reading. No production code. No push.*
