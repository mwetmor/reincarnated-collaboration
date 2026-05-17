# Finding — 2026-05-16 — Gate 1 batch: movement-speed-baseline + spatial-data-jsonschema decisions-log entries

**Reviewer:** jack-ryan
**Severity:** WARN (two items; neither is a BLOCK; both correctable pre-commit)
**Target:** `agentic_orchestration/qa/pending/2026-05-16-decisions-log-movement-speed-baseline.md` + `agentic_orchestration/qa/pending/2026-05-16-decisions-log-spatial-data-jsonschema.md`
**Developer:** knight-rider
**Principles applied:** Review Principle 1 (design-to-decisions consistency), Principle 2 (attribution + provenance), Principle 3 (semantic shift labeling), Principle 5 (no pre-commitment on parked questions)

---

## Entry 1 — Movement-speed-baseline

**Verdict: PASS WITH ONE FLAG**

### Questions resolved cleanly

1. **Load-bearing-Stage-A2 framing (Q1):** Correct. Entry explicitly frames Step 3 as POST-VS2a tight follow, NOT indefinite deferral, and carries Matt's verbatim directive with the 🔴 callout. The framing "Stage A2 is the next gauntlet-balance-critical-path item after VS2a ships" is honored without over-claiming.

2. **Discipline #11 — parameter value match (Q2):** All 8 parameters verified against `canonical/story/movement-speed-baseline.md`:
   - Player base 5.75 ✓, Early 6.0 ✓, Mid 7.5 ✓, Late 8.0 ✓
   - Monster trash 5.75 ✓, Fast archetypes 6.6–7.5 ✓
   - PIXELS_PER_METER=48 ✓, AI_SPEED_MULTIPLIER=0.767 ✓
   - Range-profile MS variance DROPPED ✓
   Attribution is clean; source-of-truth cited throughout.

3. **Discipline #12 — semantic shift framing (Q3):** Entry states "all gauntlet-balance claims are provisional" until Stage A2 lands. Calibration-epoch implication section is explicit. The semantic shift is labeled, not buried.

4. **Alternatives completeness (Q4):** Six alternatives (PoE-1 zoom-zoom; D2-classic; abstract-units; defer post-VS2a; per-class base variance; PIXELS_PER_METER alternatives). All six align with real decision points surfaced by gandalf. No missing alternatives apparent.

5. **Single-entry vs split (Q5):** Single-entry is correct. The cascade and the values are coupled; splitting would break the self-referential Step 4 / Step 3 coupling.

6. **Companion cross-reference bidirectionality (Q6):** BIDIRECTIONAL — confirmed. Movement-speed entry references spatial-data entry at line 101; spatial-data entry references movement-speed entry at line 168. Both reference each other's qa/pending path explicitly. Bidirectionality is preserved.

7. **Arena-scale-back-derivation framing (Q7):** Correctly framed as drax-implementation-observation, not a blocker. "Single thing to watch" language is calibrated — case (a) vs case (b) surfaces the two outcomes without asserting which applies.

### Flag (WARN)

**3-band vs 4-band discrepancy — Discipline #11 conflict with source docs.**

The movement-speed entry's implementation cascade table (Step 3) describes gamora Stage A2 as implementing "3-band distance state." The authoritative sources disagree:
- `canonical/story/spatial-data-jsonschema.md` (Section 2 gap-analysis table, Section 4 cross-seam table, Section 6 Step 3): **4-band (melee / near / mid / far)**
- `canonical/story/engine-balance-stewardship.md` line 318: **4-band: melee / near / mid / far**
- The movement-speed source doc (`canonical/story/movement-speed-baseline.md` line 227): states "3-band distance state (melee / near / mid)" — this is where the movement-speed entry drew from, but that phrasing is internally inconsistent with its own parent doc (spatial-data-jsonschema.md) which the movement-speed-baseline.md cross-references as the authoritative spec.

The spatial-data-jsonschema.md is the architectural contract document; its 4-band spec (melee / near / mid / far) is authoritative. The "3-band" in movement-speed-baseline.md appears to be a simplification that dropped the "far" band.

**Action:** knight-rider corrects Step 3 description in movement-speed entry to read "4-band distance state (melee / near / mid / far)" matching the spatial-data source-of-truth. The movement-speed-baseline.md source doc's "3-band" phrasing is a gap in that doc but NOT this entry's bug to fix — that doc's maintenance is gandalf's.

---

## Entry 2 — Spatial-data-jsonschema

**Verdict: PASS WITH ONE FLAG**

### Questions resolved cleanly

1. **Single-entry justification (Q1):** Correct. Architecture + cascade are coupled at every step; splitting would require two entries that would immediately re-merge logically. The Q7 calibration-epoch implication is baked into the cascade (Step 6) which makes it load-bearing to keep together.

2. **Load-bearing-Step-3 framing (Q2):** Clean bifurcation. VS2a-ship gating = Steps 1+2+5; next-balanced-gauntlet gating = Step 3. The table makes both gates explicit per column header. Does not over-claim Step 3 as VS2a-blocking; does not under-claim it as optional.

3. **Discipline #11 — dimension library + movement_profile + vendor inventory match (Q3):**
   - Dimension library: 32.7×14.0m (trash) ✓, 28×28m (elite) ✓, 40×24m (boss) ✓, 50×30m (act-boss) ✓
   - movement_profile: walking / running / crawling / floating / flying / teleporting (6 values) ✓
   - Vendor inventory: PoE ✓, D2 ✓, D3 ✓, D4 (rejected) ✓, Last Epoch ✓, Grim Dawn ✓ — 6 vendors inventoried. Entry says "4-vendor inventory" in knight-rider note Q3 — minor wording error in the note but the entry body itself correctly inventories 6. Not a decisions-log body error.

4. **Discipline #12 — semantic shift framing (Q4):** Calibration-epoch implication section says "movement-speed-blind, spatial-data-blind sim" — correctly extends the semantic-shift framing beyond movement-speed alone to include spatial-data blindness. Downstream-agent warning is explicit ("not to over-anchor on current calibration-epoch numerics").

5. **8 open questions parked cleanly (Q5):** All 8 questions park without pre-commitment. Q7 (calibration-epoch) is flagged load-bearing but the entry correctly describes it as "already baked into Step 3 + Step 6" — the parking is an acknowledgment, not a deferral of the cascade itself.

6. **Companion cross-reference bidirectionality (Q6):** Confirmed bidirectional (see Entry 1, Q6 above).

7. **B12 roadmap-amendment routing (Q7):** Clean. "Knight-rider drafts roadmap amendment if Matt approves co-shipping" — decision routes to Matt, not pre-committed. Phrasing is appropriately conditional.

8. **Alternatives completeness (Q8):** Eight alternatives (pure tile-grid; pure continuous-coordinate; tiles-per-second; procedural-room generation; defer schema; B12 stay deferred; more-than-6 movement_profile values; wall-geometry beyond perimeter). Covers the real decision surface without inventing phantom options.

### Flag (WARN)

**`spatial_complexity_tier` type mismatch in entry's schema fragment vs source-of-truth.**

The decisions-log entry's schema fragment (the JSON block inside the entry body) shows:
```json
"spatial_complexity_tier": 1
```
(integer)

The authoritative gandalf source doc (`canonical/story/spatial-data-jsonschema.md` Section 3, field-by-field rationale) defines:
```
"spatial_complexity_tier" — enum: "open_arena" | "obstacle_arena" | "corridor"
```
(string enum)

And the source doc's own schema fragment shows:
```json
"spatial_complexity_tier": "open_arena"
```

The entry's schema fragment contradicts the source-of-truth schema on this field's type. This is a Discipline #11 attribution failure — the entry's schema fragment was not transcribed faithfully from gandalf's locked schema.

**Action:** knight-rider corrects the schema fragment in the spatial-data entry: replace `"spatial_complexity_tier": 1` with `"spatial_complexity_tier": "open_arena"` to match gandalf's source-of-truth.

---

## Cross-entry coherence check

**Verdict: COHERENT WITH ONE CROSS-ENTRY CONSISTENCY NOTE**

### Clean coherence

- **Matt's directive verbatim:** Both entries quote identically: *"The movement speed must be added into the core of the engine once we come to a decision so that the gauntlet simulation will be balanced."* Wording is consistent.
- **Calibration-epoch implication:** Both flag the same thing — current epoch is movement-speed-blind (and spatial-data entry adds "spatial-data-blind"); both say Step 3/Stage-A2 will re-shift metrics; both say new calibration-epoch entry follows. Consistent.
- **Gamora Stage A2 framing:** Both frame it as ~1.5-2 weeks; both frame it as load-bearing-not-optional; both frame it as POST-VS2a tight follow. Consistent. The 3-band/4-band discrepancy (flagged under Entry 1) is the one point of friction between entries — spatial-data entry correctly says 4-band throughout; movement-speed entry incorrectly says 3-band in one location.
- **Companion references:** Bidirectional and path-accurate on both sides. Commit-together instruction is present in both entries.

### Cross-entry consistency note (informational; already covered by Entry 1 WARN)

The 3-band/4-band discrepancy creates one cross-entry drift: the spatial-data entry is internally consistent on 4-band; the movement-speed entry contradicts it with "3-band" in Step 3. The fix to movement-speed entry's Step 3 (noted above) resolves the cross-entry drift at the same time.

---

## Actions required before commit

- [ ] **knight-rider (movement-speed entry):** Change Step 3 cascade table "3-band distance state" → "4-band distance state (melee / near / mid / far)" to match spatial-data-jsonschema.md and engine-balance-stewardship.md.
- [ ] **knight-rider (spatial-data entry):** Change schema fragment `"spatial_complexity_tier": 1` → `"spatial_complexity_tier": "open_arena"` to match gandalf's locked schema in canonical/story/spatial-data-jsonschema.md Section 3.

Both fixes are ≤30-second edits. No Matt escalation required — both are attribution corrections (Discipline #11), not design decisions. After these two edits, both entries are clear for Matt approval and pair-commit.

---

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-16-decisions-log-movement-speed-baseline.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-16-decisions-log-spatial-data-jsonschema.md`
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/movement-speed-baseline.md` (Matt-approved source-of-truth)
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/spatial-data-jsonschema.md` (gandalf source-of-truth)
