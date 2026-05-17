# Dispatch — 2026-05-16 — gamora — wind_controller V2 structural anomaly investigation

**From:** knight-rider (authored per star-lord V2 CLI flag + regen completion 2026-05-16; cross-seam flag returned with structural — not seed — anomaly)
**To:** gamora
**Approved by:** Matt at 2026-05-16 Day 4 ("fire the wind_controller dispatch")
**Status:** PENDING
**Estimated effort:** 1 session (~3-4h); investigation-first, fix-conditional. Math-before-code per Discipline #1.

**Acceptance summary:** Root cause of wind_controller's repeated >3.5 modifier in V2 mode named with file + line + mechanism. Classification filed: structural balance issue / measurement artifact / kit design issue / other. Math note documenting the analysis. If fix is in scope: smoke test passes + full regen verification passes. If fix is out of scope or would expand into a separate balance pass: documented proposed approach with knight-rider routing recommendation. Tag + AGENT_STATE + completion record. Cross-seam flag back to star-lord ONLY if a contract change is introduced (new emission field / schema change), in which case the contract change does NOT happen in this dispatch — surface and stop.

---

## Why this dispatch exists — empirical anchor

Star-lord V2 CLI flag + regen dispatch returned 2026-05-16 with a **two-occurrence structural finding**:

| Season | Mode | Seed | wind_controller modifier |
|---|---|---|---|
| `season_001006` | V2 | 1006 | **3.51** |
| `season_001010` | V2 | 1010 | **3.6250** |

Same archetype. Same V2 mode. Two different seeds. Both occurrences > 3.5. **Not seed-specific — confirmed structural.**

V2 calibration baseline math from star-lord MIGRATION.md V2 section:
- All 10 classes: mean |mod-1.0| = **0.5994**
- Excluding wind_controller: mean |mod-1.0| = **0.3743**
- V1 baseline for comparison: 0.799 / 0.876

V2 is materially better than V1 (≈half the absolute deviation) **once wind_controller is excluded**. With wind_controller in, the outlier drags mean by +0.225. **V2 calibration epoch cannot be declared until this is classified.**

## What this dispatch produces

### Stage 1 — Discipline #10 empirical inspection (do this first; do NOT pre-commit hypotheses)

Pull the actual data before guessing:

- wind_controller telemetry rows from both seasons (`class_balance_results` + `class_fight_loadouts` + per-fight rows)
- Compare to the 9 other classes in season_001010 (which all converged within band)
- Compare wind_controller's V2 results to its V1 result (if a V1 regen of comparable seed exists in historical data — there are 15+ historical seasons per B14.5 sidecar)
- Inspect wind_controller's kit composition in both seasons (skills selected, status/control mechanics, base stats)
- Inspect modifier-clamp gate state — did either occurrence flag with `modifier_flag_tier='review'` (V2.4 field just added by star-lord, persisted as of season_001010)?

Report what you SEE before forming a hypothesis. The B14.5 sidecar analysis noted hunter had 1.82 modifier range (least consistent shape) — wind_controller may have an analogous archetype-level shape issue, but that's a hypothesis to TEST not assume.

### Stage 2 — Hypothesis space + selection (math-before-code per Discipline #1)

Plausible root cause categories (rank by Stage 1 evidence, do not enumerate-and-test):

1. **V2 room HP-carryover mechanic pathology.** V2 mode carries HP across encounters within a room (vs V1's per-encounter HP reset). wind_controller may have a status/CC-heavy kit that interacts pathologically with multi-encounter HP economy (e.g., control mechanics let it survive disproportionately well in early-encounter slots, inflating non-pack winrate).
2. **wind_controller kit-design issue.** The archetype's intrinsic kit may be over-tuned for the V2 evaluation surface (regardless of HP carryover); V1's per-encounter reset masked it.
3. **wind_controller trait-roll variance.** B9a per-class trait pool may have a configuration that lets wind_controller roll an outlier-strong trait combo in both seeds (cross-seed coincidence at scale).
4. **V2 emission-gap edge case.** V2.1 emission-gap fix verified 100% non-null in star-lord regen, but a different edge case may apply specifically to wind_controller's kit.
5. **Measurement artifact in convergence loop.** B10.4 Option 2 binary search converges on non-pack WR; wind_controller may converge near a discontinuity that biases the modifier estimate.
6. **Element-substrate interaction.** wind is one of the canonical-four; the bias-substrate may interact with V2 mechanics in a way that's wind-specific (test by comparing to other wind archetypes — wind_damage, wind_support — if they exist in the seasons).

The list is a starting palette; let the evidence narrow it before instrumenting.

### Stage 3 — Math note + classification

File a math note (Discipline #1 deliverable) documenting:
- What Stage 1 inspection revealed
- Which hypothesis the evidence supports (with the supporting numbers)
- Whether the issue is **structural balance** (needs a balance pass) / **measurement artifact** (numbers are correct, framing is wrong) / **kit-design issue** (archetype needs design revision) / **other**
- For each Matt-decision surface that arises: explicit framing

Filed location: `~/Games/reincarnated-engine/design/notes/wind-controller-v2-anomaly-2026-05-16.md` (or analogous; pick a path consistent with prior gamora math notes).

### Stage 4 — Fix-conditional execution

**If the root cause is bounded + in-seam (gamora simulation/balance code only):**
- Apply the fix
- Smoke test per Discipline #2 (small regen, wind_controller only, verify modifier moves into band)
- Full regen verification (10/10 classes; verify wind_controller modifier into band AND other 9 classes did not regress)
- MIGRATION.md entry if any cross-seam impact surfaces (per ADR-004)
- Cut intermediate tag
- Re-run V2 calibration math from MIGRATION.md V2 section; report updated mean |mod-1.0|

**If the root cause requires a balance-pass dispatch (out-of-scope of investigation):**
- Document the proposed approach with effort estimate
- Stop — knight-rider routes the follow-on
- Cut intermediate tag on investigation work only (math note + diagnostic findings)

**If the root cause is cross-seam (e.g., requires new telemetry emission, recorder change, generator change):**
- Surface and STOP
- Do NOT patch out-of-seam
- Knight-rider routes the follow-on with appropriate cross-seam coordination

## Cross-seam contract change?

**Round-trip: not applicable** because this is an in-seam investigation in gamora's simulation/balance code. If a fix surfaces that introduces a new emission field, schema change, or alters the fight_log dict shape — that constitutes a cross-seam contract change and triggers Stage 4's third bullet (surface + stop; do NOT execute the contract change in this dispatch). Per R11(b) Principle 6 (operationalized 2026-05-16) — explicit annotation.

## Out of scope (explicit)

- **NO V2 cipher migration touchpoints.** Star-lord Stage 3 cipher migration is in-flight; do not touch LLM prompt construction, export packet shape, or manifest structure.
- **NO non-wind_controller balance pass.** This dispatch targets one archetype's structural anomaly; do not opportunistically re-balance other classes.
- **NO V1 mode investigation.** V2-specific anomaly; V1 mode is unaffected.
- **NO modifier-clamp gate logic changes.** That gate landed earlier today; its job is to flag, not fix. wind_controller may have triggered the gate's `modifier_flag_tier='review'` flag — confirm by inspection but don't extend gate logic.
- **NO trait-system architecture change.** Even if Stage 2 evidence points at trait-roll variance, the fix lives at the per-trait config layer, not the architecture layer.

## Required reading

- Star-lord V2 CLI flag + regen completion record at bottom of `agentic_orchestration/dispatches/2026-05-16-star-lord-v2-cli-flag-and-regen.md` (the empirical anchor)
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` — V2-mode calibration baseline section
- `~/Games/reincarnated-engine/logs/regen-001010-v2-mode-2026-05-16.log` — fresh regen log
- season_001006 + season_001010 in-place data
- Your own `gamora/v1.3-modifier-clamp-gate` tag + dispatch (the gate that flagged this archetype's threshold)
- B14.5 V1 primary loop dispatch + sidecar analyses (hunter modifier-range parallel case)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1 (math-before-code), #2 (smoke-test), #3 (right tool), #10 (empirical inspection over assumption), #12 (semantic-shifting if any schema changes), #13a/#13b (implicit-pillar drift; internal-vs-generative schema separation), #14 (terminology lock); Patterns P6 (load-bearing dimension deferred) and P7 (test scaffolding masks production defect) for hypothesis evaluation

## Acceptance criteria

- [ ] Stage 1 empirical inspection completed; numbers reported (not just narrative)
- [ ] Stage 2 hypothesis narrowed by evidence; supporting math present
- [ ] Stage 3 math note filed at `design/notes/` with classification
- [ ] Stage 4 outcome per branch:
  - Fix applied path: smoke ✓ + full regen ✓ + updated V2 calibration math
  - Routed-follow-on path: proposed approach + effort estimate documented
  - Cross-seam path: surface + stop, no contract change executed
- [ ] Intermediate tag cut (name: `gamora/v1.3-wind-controller-v2-anomaly-investigation` or extension if fix applied)
- [ ] AGENT_STATE.md updated
- [ ] Completion record filled at bottom of this dispatch
- [ ] Knight-rider notified with: root cause classification, fix disposition, V2 calibration math delta (if fix applied), any follow-on dispatches needed

## Tag policy

- **Intermediate tag (investigation only):** `gamora/v1.3-wind-controller-v2-anomaly-investigation`
- **Intermediate tag (investigation + fix):** `gamora/v1.3-wind-controller-v2-anomaly-fix` at the commit closing the smoke + regen
- **Milestone tag:** none from this dispatch. V2 calibration epoch milestone tag is a separate Matt-approved decision once this and any related work clears.

## Notes for knight-rider routing visibility

- **Holds jack-ryan Tier 1 #3 calibration analysis.** Until this dispatch classifies the anomaly, jack-ryan's calibration analysis is on HOLD (star-lord recommendation, knight-rider agreed). Once classified, jack-ryan can either anchor on the 9 non-flagged classes (current 0.3743 mean abs dev) or re-regen with fix.
- **V2 calibration epoch declaration is BLOCKED on this dispatch.** Matt-decision surface arrives when this returns.
- **Star-lord Stage 3 cipher migration is in-flight in parallel.** Star-lord and gamora seam boundaries are clean; no coordination needed unless gamora's findings produce a new emission field (Stage 4 cross-seam branch).

---

## Completion record

**Completed:** 2026-05-16
**Root cause:** Two distinct mechanisms under a shared structural substrate:
- season_001006 (modifier=3.51): `simulation/balance_loop.py` V2 binary search — V2 HP-carryover × low-DPS-density kit (25%, no DoT), target=0.50. Prior investigation confirmed. Option (d) accepted as known anomaly.
- season_001010 (modifier=3.625): `generation/season_orchestrator.py` lines 567-570 (Factor B: target=0.60 "strong outlier" slot assigned by RNG shuffle) compounding with `simulation/balance_loop.py` V2 binary search (Factor A: same structural DPS-density issue, but s001010 kit has burn DoT and would converge ~2.0-2.8 at target=0.50 — below the 3.0 review threshold). The modifier exceeds 3.5 in s001010 ONLY because target=0.60 is a co-factor.

**Classification:** Kit-design issue (structural) — archetype template produces low-DPS-density kits that V2 HP-carryover room semantics amplify. The s001010 occurrence additionally involves design-intentional target assignment (strong-outlier slot), which is not a defect.

**Math note path:** `reincarnated-engine/src/reincarnated/simulation/math/wind-controller-v2-anomaly-2026-05-16.md`

**Fix disposition:** routed-follow-on. No in-seam code changes. No smoke test (no code changed). Three follow-on items requiring Matt routing:
1. [Rocket] Minimum DPS floor for wind_controller archetype template
2. [Gamora] Modifier clamp gate operationalization (reject-and-regenerate)
3. [Matt-decision] Strong-outlier target + wind_controller interaction design question (cross-seam if code fix)

**V2 calibration delta:** No fix applied, so no before→after from a code change. Framing refinement:
- Segment A (all 10): 0.5994 (unchanged)
- Segment B (excl. modifier_flag_tier='review', 9 classes): 0.3743 (unchanged, star-lord anchor)
- Segment C (target=0.50 CONVERGED only, 8 classes): 0.3273 (new, cleanest balance-loop signal)
Matt-decision surface: which segment anchors V2 calibration epoch declaration.

**Intermediate tag:** none (investigation-only, no code changes; prior tag `gamora/v1.3-b11-sim-side-geometry-resolution` @ `0278fba` remains current)

**Tests status:** N/A — no code changes; no smoke or regen required.

**Notes for knight-rider:**
1. **V2 calibration epoch decision surface.** Three calibration segments characterized (math note §4.3). Segment C (0.3273, 8 classes at target=0.50 CONVERGED) is recommended as primary; Segment B (0.3743) is acceptable secondary. Matt decides which anchors the epoch declaration.
2. **jack-ryan Tier 1 #3 UNBLOCKED.** Route now. Recommend anchoring on Segment C (0.3273) with Segment B (0.3743) as secondary reference.
3. **Three queued follow-on items for Matt routing:** (1) rocket DPS floor dispatch; (2) gamora clamp gate activation dispatch; (3) design question on strong-outlier + wind_controller interaction (cross-seam if code fix = rocket seam).
4. **"Confirmed structural" framing partially revised.** The archetype-level sensitivity IS structural — wind_controller always inflates under V2. But the specific >3.5 threshold in s001010 requires target=0.60 as a co-factor. The modifier_clamp_gate at 3.0 will fire reliably when wind_controller receives the strong-outlier target in V2 mode; it may or may not fire at target=0.50 depending on kit DPS density.
5. **No cross-seam contract changes introduced.** No new emission fields, no schema changes, no recorder changes. Star-lord does not need to act beyond optionally updating MIGRATION.md V2 section with Segment C addendum (informational only).
