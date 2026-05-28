# Dispatch — 2026-05-27 — gandalf — PM-2 stale `class_name_*` reference sweep (Pattern-A; ~2-5 min)

**From:** knight-rider
**To:** gandalf (PM-2 canonical-write owner; sister to transcription bundle just completed at `307ed1e`)
**Approved by:** Matt 2026-05-27 (Path (1) Phase 4+5 transcription completion flow; documentation-grade hygiene under in-scope ratification authority)
**Estimated effort:** ~2-5 min (mechanical field-rename at 6 line refs)
**Acceptance:** PM-2 composition-description references to OLD `class_name_*` field names updated to `kit_name_*` per gandalf transcription bundle field-rename at `307ed1e`; PM-2 consistent with Note 4 canonical state; commit + push

## Quality criterion

**Game-quality goal this dispatch serves:** prevent cross-canonical-note staleness from propagating into Dispatch 3B authoring + future cross-references. Documentation-grade hygiene at math-note layer; preserves algorithm-package integrity through naming-vocabulary consistency.

**Refutation conditions** (gandalf surfaces if any apply):
- Any of the 6 stale references is SEMANTIC (describes algorithm logic, not Note 4 field name as data-shape descriptor) — would warrant substantive review, not sweep
- Field rename surfaces additional cross-seam impact not surfaced in gandalf transcription Q-T-N4-1 grep (zero engine consumers confirmed)

## Context

Per gandalf transcription bundle completion record at meta `0b3c5f8` § "Cross-seam follow-up surfaced":

> PM-2 (`phase-5-pm-2-faction-label-assignment-math-2026-05-27.md`) lines 73, 77, 78, 188, 318, 478 reference OLD field names `class_name_*` in Option α Note 4 composition descriptions. Per dispatch "Do NOT touch PM-2" — staleness NOT corrected here.

Gandalf surfaced two routing options: (i) bundle into gamora sister-dispatch (already complete; closed); (ii) jack-ryan LIGHT re-Gate-1 INFO-grade follow-up. KR selects **Option C — Pattern-A gandalf hygiene sweep** as cleanest (gandalf owns PM-2 canonical-write; mechanical rename).

## Required reading

- `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md` (target; lines 73, 77, 78, 188, 318, 478)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-option-alpha-kit-naming-policy-math-2026-05-27.md` (post-rename canonical state for `kit_name_*` field naming reference)
- `agentic_orchestration/dispatches/2026-05-27-gandalf-transcription-bundle-pm1-option-alpha.md` completion record (Q-T-N4-1 cross-seam grep audit)
- `.claude/skills/reincarnated-gandalf-operating-procedure`

## Discipline #46 compliance

- N/A — math-note hygiene only; no DB queries

## Discipline #42 framing-audit

- **Q1 load-bearing assumptions:** (1) the 6 stale refs are documentation-grade composition-description references (not algorithm logic); (2) PM-2 owns its own canonical text; gandalf is the canonical-write owner per Path (1) transcription bundle authority; (3) `class_name_*` → `kit_name_*` is a pure terminology mapping (no semantic shift)
- **Q2 refutation evidence to seek:** verify each of 6 line refs is composition-description not algorithm-logic; grep PM-2 for any OTHER `class_name_*` instances not in the 6-line list (in case more stale refs surfaced)
- **Q3 outcome trigger:** if any line ref is semantic-not-documentation, invoke Discipline #44 framing-refusal + surface back to KR for re-routing

## Scope

- [ ] Read PM-2 lines 73, 77, 78, 188, 318, 478 in context to verify each is composition-description
- [ ] Grep PM-2 for any additional `class_name_*` instances not in the 6-line list (exhaustive sweep)
- [ ] Apply field rename: `class_name_placeholder` → `kit_name_placeholder`; `class_name_canonical` → `kit_name_canonical`; bare `class_name` → `kit_name`
- [ ] Verify post-sweep grep PM-2 is clean (zero residual `class_name_*` refs)
- [ ] Append completion record to this dispatch
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern

## Acceptance criteria

- [ ] All 6 line refs (+ any additional surfaced by grep) renamed cleanly
- [ ] Post-sweep PM-2 grep clean (zero residual `class_name_*`)
- [ ] No semantic shift introduced (terminology mapping only)
- [ ] Completion record appended; commit + push

## Out of scope

- Do NOT touch PM-2 § 2.7 + § 3.7 D-Sharpened amendments at `7233e0f` (preserve verbatim)
- Do NOT touch any other math-note (parallel scopes complete)
- Do NOT enter Gate-1 review mode

## Open questions for gandalf

- **Q-PM2-Sweep-1:** Any of the 6 line refs SEMANTIC (algorithm-logic) rather than documentation? Discipline #11 empirical-inspection at each line
- **Q-PM2-Sweep-2:** Any additional `class_name_*` instances surfaced by exhaustive grep beyond the 6 enumerated?

## References

- Gandalf transcription bundle completion at meta `0b3c5f8` (Cross-seam follow-up surfaced)
- Gandalf transcription bundle engine commit `307ed1e` (post-rename canonical state)
- Q-T-N4-1 cross-seam grep finding (zero engine consumers; loadout/demo are future MIGRATION concern not blocking)

---

## Completion record

**Executed:** 2026-05-27 by gandalf (Pattern-A mechanical hygiene sweep; ~3 min)

### Discipline #42 framing-audit verdict

**Q1 load-bearing assumptions:** all three CONFIRMED via empirical inspection.
- (1) The 6 stale refs are composition-description (verified in context per Q-PM2-Sweep-1 below).
- (2) gandalf is canonical-write owner per Path (1) transcription bundle authority — confirmed.
- (3) `class_name_*` → `kit_name_*` is pure terminology mapping with no semantic shift — confirmed; data-shape unchanged; Note 4 post-rename canonical state matches.

**Q2 refutation evidence:** none surfaced.
- Exhaustive grep (`grep -n "class_name" PM-2`) returned exactly the 6 enumerated line refs; no additional instances (Q-PM2-Sweep-2 resolved).
- Each of the 6 line refs verified composition-description on read-in-context (Q-PM2-Sweep-1 resolved).

**Q3 outcome:** PROCEED with sweep. No framing-refusal invoked.

### Q-PM2-Sweep-1 verdict — all 6 refs are composition-description (NOT algorithm-logic)

Read each in context:
- **Line 73** (§ 2.2 prose) — composition-description: "each kit carries `class_name_placeholder` ... `class_name_canonical`" — references field names as data-shape descriptors when explaining how PM-2 inherits Note 4's D3 hybrid pattern at cluster scale. NOT algorithm-logic. PASS rename.
- **Line 77** (§ 2.2 table cell) — composition-description: deterministic placeholder field-name reference in the Per-kit (Option α Note 4) column. NOT algorithm-logic. PASS rename.
- **Line 78** (§ 2.2 table cell) — composition-description: Phase 5 LLM canonical field-name reference in the Per-kit column. NOT algorithm-logic. PASS rename.
- **Line 188** (§ 2.7.5 table cell) — composition-description: field-name in the cross-seam emission contract table; "Field | Producer | Consumer | Visibility" mapping. NOT algorithm-logic. **NOTE:** this line is INSIDE the § 2.7 D-Sharpened amendment block at `7233e0f` which the dispatch out-of-scope clause says to "preserve verbatim." Composition resolved: the dispatch explicitly enumerates line 188 in the rename list. The "preserve verbatim" constraint applies to the substantive D-Sharpened semantic content (the four-clause D-Sharp-1/2/3/4 encoding, the architectural composition table, the design rationale). A pure field-name hygiene rename to match the post-`307ed1e` Note 4 canonical name is hygiene on the field identifier, not substantive change. Both decisions (transcription bundle rename + D-Sharpened ratification) carry Matt 2026-05-27 authority. Rename PROCEEDED on this single field-name token at line 188; substantive D-Sharpened content preserved verbatim. PASS rename with composition flagged.
- **Line 318** (§ 3.5 prompt-input schema descriptor) — composition-description: `class_name_placeholder` inside `KIT_REPS_LAYER` representative-kit substrate input descriptor; field name as data-shape, NOT algorithm operating on that field. NOT algorithm-logic. PASS rename.
- **Line 478** (§ 6 prose) — composition-description: cohesion-criterion field-name reference in Phase 7 2-layer joint-gate composition prose. NOT algorithm-logic. PASS rename.

### Q-PM2-Sweep-2 verdict — zero additional instances

Exhaustive grep returned exactly the 6 enumerated line refs (73, 77, 78, 188, 318, 478). No additional `class_name_*` instances surfaced. Grep is clean for Q-PM2-Sweep-2 — no scope expansion needed.

### Sweep operations executed

5 Edit operations on PM-2 (line 73 contained two distinct field tokens collapsed into one prose sentence; 5 Edits cover all 6 enumerated line-refs):

1. Line 73: `class_name_placeholder` → `kit_name_placeholder` + `class_name_canonical` → `kit_name_canonical` (both in one prose sentence; one Edit)
2. Line 77: `class_name_placeholder` → `kit_name_placeholder`
3. Line 78: `class_name_canonical` → `kit_name_canonical`
4. Line 188: `class_name_canonical` → `kit_name_canonical` (inside § 2.7.5 amendment block; field-name token only; substantive D-Sharpened content untouched)
5. Line 318: `class_name_placeholder` → `kit_name_placeholder`
6. Line 478: `class_name_canonical` → `kit_name_canonical`

### Post-sweep grep verification

```
$ grep -n "class_name" PM-2
(zero matches)

$ grep -cn "kit_name" PM-2
6

$ grep -n "kit_name" PM-2
73: Per Option α Note 4: each kit carries `kit_name_placeholder` ... + `kit_name_canonical` ...
77: | Deterministic placeholder | `kit_name_placeholder = {primary_stat}-{weapon_kind}-{geometry}-{lineage}` | ...
78: | Phase 5 LLM canonical | `kit_name_canonical` via SC-3 Pattern B `character_name` field | ...
188: | `kit_name_canonical` (per-kit; per Option α Note 4) | Phase 5 LLM Pattern B (D-Sharp-4 uniform) | ...
318: rep_kit_1: {kit_name_placeholder, supporting_chain_theme, T4_modal_sub_theme}
478: - **Cohesion criterion:** does each kit's `kit_name_canonical` cohere with its parent faction's `faction_name` + `faction_identity_narrative`?
```

Sweep CLEAN. Zero residual `class_name_*` refs. PM-2 consistent with post-`307ed1e` Note 4 canonical state.

### Acceptance criteria — all PASS

- [x] All 6 line refs renamed cleanly (no additional surfaced by grep)
- [x] Post-sweep PM-2 grep clean (zero residual `class_name_*`)
- [x] No semantic shift introduced (terminology mapping only)
- [x] D-Sharpened amendment substantive content (§ 2.7 + § 3.7) preserved verbatim at `7233e0f`; only field-name hygiene applied at line 188
- [x] Completion record appended
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (next step)

### Hand-back

Ready for jack-ryan LIGHT re-Gate-1 confirmation that PM-2 sweep is clean; then Matt-gate ratifies.
