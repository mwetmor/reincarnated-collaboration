# Drax /forge Phase 3 Close — Gandalf Design Review

**Date:** 2026-06-09
**Author:** gandalf (story-and-design steward)
**Reviewing:** `agentic_orchestration/drax/notes/2026-06-09-forge-phase-3-close-report.md` (commit `5ae75d3`)
**Against dispatch:** `agentic_orchestration/dispatches/2026-06-09-drax-forge-phase-3-two-layer-buffer-space-prototype.md` (commit `bb45124`; gandalf-authored, Gate-1 amended)
**Final preview consulted:** `https://reincarnated-loadout-bvy27r3hf-matthew-wetmore-s-projects.vercel.app`
**Code spot-checked:** `reincarnated-loadout/src/components/Cosmograph/TwoLayerCanvas.tsx`, `Forge.tsx`, `twoLayerTypes.ts`
**Routes to:** jack-ryan Gate-2 → knight-rider aggregation → Matt

---

## Verdict: PASS-WITH-DESIGN-RECOMMENDATIONS

The two-layer + buffer-space pattern is architecturally validated at the 2D web rendering layer. Phase 3 honors the dispatch quality criterion in structure; one quality-criterion sub-claim (rare-lineage discovery moment) is genuinely deferred and correctly flagged. Three design-side recommendations and one Matt-call surface follow.

---

## § 1. Quality Criterion alignment (dispatch § 4.5)

The quality goal: "players discover marginal-lineage and cross-substrate kit combinations through buffer-space exploration without explicit tutorial — buffer scale carries semantic meaning ergonomically, and visual register distinction reads categorically."

**Sub-claim by sub-claim:**

- **Categorical visual register (primitive-anchors vs kit-clusters).** SATISFIED. The nebula five-ring gradient (260px outer @ 0.04α → bright center @ 0.75α) reads categorically distinct from 2-5px kit dots and 3-12px star clusters at 2×+. Diablo II-class regional-marker-vs-constellation-member legibility achieved without tutorial. This is the strongest Phase 3 finding.

- **Gesture semantics carry meaning ergonomically (tight = related; cross-buffer = unusual; buffer-only = discovery).** SATISFIED at architecture; the three-mode classification fires reliably and the badge surfaces semantic to the player. The "I found something" gesture-as-meaning anchor lands.

- **Cross-substrate discovery moment.** SATISFIED via the dual-overlapping-circle hybrid render — the buffer-only lasso surfaces these reliably and they read as categorically different from primary-zone kits. This is a genuine PoE-class affix-territory-exploration moment in 2D form.

- **Rare-lineage discovery moment.** NOT VALIDATED — this is the one sub-claim Phase 3 cannot empirically honor because the corpus is rare-lineage-empty (YELLOW 1). Drax correctly flagged. See § 2 YELLOW 1 disposition.

**Refutation conditions checked:**

- "Acceptance criteria pass without advancing the quality goal" — NEGATIVE for cross-substrate; UNRESOLVED for rare-lineage (corpus-gated, not architecture-gated).
- "Dispatch pre-commits to a decision Matt has not ratified" — NEGATIVE; Branch A explicitly fenced (criterion 12); primitive-curation explicitly deferred to Pattern B.
- All other refutation conditions: NEGATIVE.

**Honor verdict:** Phase 3 honors the quality criterion at architectural-pattern scope. The one unhonored sub-claim is empirically gated, not design-failure.

---

## § 2. Three YELLOW observations — design-side disposition

### YELLOW 1 — Corpus gap (rare-lineage kits absent)

**Design verdict:** the 310-hybrid stand-in is structurally inadequate as a substitute for rare-lineage validation. Hybrids and rare-lineages serve distinct discovery functions: hybrids are *boundary-crossing combinations* (PoE-style cross-element affix territory); rare-lineages are *marginal-tradition exposures* (Diablo II uniques-from-elsewhere). Conflating the two in design discourse risks the marginal-lineage recognition records × 5 (2026-05-23) being downgraded to "covered by hybrids" when they are explicitly NOT — that body of work specifically named cultural-tradition marginality as a separable axis.

**Disposition: deferred-validation item, empirical-evidence trigger.** The trigger is engine rare-lineage kit generation. Phase 3 does NOT need to re-fire post-corpus-enrichment — the buffer-space architecture is already proven discoverable via hybrids; what's needed is a smaller follow-on (call it Phase 3-supplement) that re-renders /forge against an enriched corpus once rare-lineage kits exist, and validates that rare-lineage kits land in buffer space with appropriate visual differentiation from hybrids (different gesture? different render? different anchor-relationship?).

**Recommendation to KR:** flag for the rare-lineage-kit engine generation commission backlog (this is a substrate-corpus question; routes through rocket/elrond at the engine layer, not drax). When that lands, drax re-validates at the player-surface layer. No re-fire of Phase 3 proper.

### YELLOW 2 — Physical element dominance (43% of corpus visible at physical anchor)

**Design verdict: this is the explicit Matt-call.** The drax framing is correct that there are two interpretations; the design-steward recommendation is **preserve substrate-honesty (option a)** per Discipline #59 (substrate-coverage honesty). Specifically:

- Normalizing visual cluster size against substrate distribution would be a Discipline #59 violation — design surfaces would be lying about what the corpus IS. The physical-element over-representation is a real substrate fact; if it reads as physical bias, the substrate IS physical-biased, and the right response is to fix the substrate (corpus expansion / generation rebalance), NOT to mask it visually.
- Diablo-genre parallel: Diablo II's monster-distribution skews in act 2 vs act 5 were ALWAYS read as "act 2 has fewer enemy types" not "the renderer is misleading me." Players read distribution as information, not bias-failure — IF the rendering is consistent.
- Isekai/Solo-Leveling parallel: marginal-element scarcity in skill-tree visualization is a discovery signal in those traditions, not a UX defect.

**However,** the design-steward read of the preview IS that 428/1000 reads strong. If Matt judges this confusing rather than informative, the fix vector is corpus rebalance (engine commission to widen non-physical element generation), NOT visual normalization at the render layer.

**Matt-call framing for KR routing:**
> "Preview shows physical cluster ~43% of dot count. Two paths: (A) preserve substrate-honesty at render layer + commission corpus rebalance (gandalf recommendation per Discipline #59); (B) normalize visual at render layer regardless of substrate. (B) violates Discipline #59 — Matt's call whether the player-confusion risk overrides #59."

**Recommendation: route (A) unless Matt explicitly overrides.**

### YELLOW 3 — `classifyLasso()` threshold scaffold value

**Design verdict: TODO with empirical trigger is correct disposition, BUT close-report has a documentation drift that should be corrected.**

The close report § "Lasso classification threshold" states the function uses `anchor.outer_glow_radius` (~260px) as the threshold. **Actual code uses different magic numbers:** the live `classifyLasso()` (TwoLayerCanvas.tsx lines 174-202) thresholds are `1200 + lassoR` for "nearby anchor", `1100` for "within-anchor distance cutoff", `600` for cross-buffer lasso-radius minimum, and `2` for the multi-anchor-overlap count. None of these are `outer_glow_radius`. They're tuned to kit-zone-outer radius (~1050px) and inter-anchor SPACING_X (2750px), not to nebula glow boundary.

**This is a Discipline #40 candidate flag drax already correctly identified at scaffold-status. The amendment recommendation:**
1. Drax: correct the close-report sentence + AGENT_STATE.md TODO to reference the ACTUAL scaffold values (`1100` within-anchor / `1200` nearby-anchor / `600` cross-buffer-radius / `2` multi-anchor-count) not `outer_glow_radius`.
2. The empirical re-validation trigger remains correct: anchor count change (post-Legolas) OR world-size change OR kit-zone-radius change.

**Severity:** documentation-drift, not functional bug. The thresholds AS WRITTEN work for current 8-anchor 4×2 grid. Just label them honestly.

---

## § 3. Two methodology hotspots (Discipline #18.2 — post-baseline timing)

### Hotspot A — Substrate-vector proximity (criterion 2) unvalidated

**Design verdict:** consultation trigger has fired. Per Discipline #18.2 refinement (methodology consultation fires AFTER baseline at extension hotspots, NOT before), Phase 3 IS the baseline; concrete pain is now surfaced (criterion 2 passes on face, not rigorously). This is the textbook #18.2 trigger condition.

**Recommendation to KR: commission elrond methodology consultation NOW.** Specific scope:
- Define substrate-vector proximity metric for cosmograph spatial layout (likely cosine distance on PSS-weighted element vector, but elrond should adjudicate)
- Evaluate whether current radial-baseline + force-directed layouts satisfy the metric
- Establish what threshold of substrate-vector-distance correlation with spatial-distance qualifies as "criterion 2 rigorously validated"

This consultation gates downstream work (UMAP comparison, Branch A vs B post-Legolas).

### Hotspot B — Algorithm selection (force-directed vs UMAP)

**Design verdict: dependent on Hotspot A.** Drax close-report sequencing is correct — UMAP comparison without a substrate-vector metric to compare against is methodologically empty. Wait until Hotspot A returns; then run UMAP comparison at the substrate-vector-distance level.

**Recommendation to KR:** queue Hotspot B as a follow-on to Hotspot A consultation; do NOT fire in parallel.

---

## § 4. Algorithm comparison finding — production recommendation

**Drax recommendation:** force-directed for production visual quality (min NN 94.5px vs 29.7px); baseline as design-validation tool.

**Design verdict: concur, with a substrate-led caveat.**

Force-directed produces better player-facing quality (organic spatial coherence; better kit separation). Baseline (radial + dynamic zone radius) produces better designer-side communication (deterministic; buffer-by-construction; corpus-imbalance handled explicitly).

Both viable, but the right answer is workstream-relative:
- **/forge as design-validation surface:** baseline. Determinism wins for cross-team communication; the buffer-by-construction property makes design discussions tractable ("the gap exists because I put it there at X spacing"). Use this when discussing layout-design with Matt.
- **Player-facing production (UE port):** force-directed OR (post-Hotspot-A) UMAP. The organic-spatial-coherence property is what isekai/ARPG audiences read as "this place feels alive." Determinism doesn't matter to the player; substrate-fidelity does.

**Caveat:** the force-directed buffer-emerges-from-physics property fails Discipline #59 IF the buffer width varies materially with corpus size. The baseline's dynamic-zone-radius (capped at 1200px) is more honest about corpus-imbalance. Production force-directed should inherit a similar safety-clamp; recommend drax + (post-Hotspot-A) elrond joint-spec when UE-port commission is authored.

**No design-block on the recommendation; concur with force-directed for production, baseline-retained for design tooling.**

---

## § 5. UE-port gap notes — WS2 commission implications

**Phase 3 surfaces:**
- Spherical-shell celestial geometry
- Volumetric nebula context
- Niagara VFX particle transitions for LOD
- AAA fidelity visual register
- 3D spatial context for buffer-space (depth + parallax)

**Design verdict on WS2 commission scope-authoring timing:** wait until Legolas Branch A/B decision lands first.

Reasoning: WS2 Niagara nebula-rendering scope authoring needs to know:
1. Does primitive-anchor render as figurative nebula (Branch B; Phase 3 baseline) OR as glyphic structure (Branch A; Tal Rasha recognition record DEFERRED)?
2. Is the anchor count 8 (elements) or ~12 (zodiac post-Legolas) or hybrid?

Both decisions are gated on Legolas zodiac-substrate-corpus completion + the Branch A/B call. Authoring WS2 scope NOW would either pre-commit Branch B (premature) or fork the scope into "if Branch A then X else if Branch B then Y" (wasted authoring effort).

**Recommendation to KR:** WS2 scope-authoring fires post-Legolas-Wave-final-completion + post-Branch-A/B-Matt-call. Phase 3 findings ARE the inheritance for WS2 (visual register confirmation, LOD pattern, buffer-emergence, mobile-responsive lessons) — captured here for later consumption. Do not fire WS2 authoring lane now.

---

## § 6. Branch A/B composition with Phase 3 findings

**Legolas Wave 3 status:** 294 entries across 20 traditions COMPLETE. N ≥ 400 trigger (Branch A viability) NOT yet met. N < 400 trigger (Branch B fallback) potentially met if Wave 3 is final mandatory completion — but Legolas may have additional Waves planned.

**Phase 3 information value for Branch A/B:**

Phase 3 demonstrates that the figurative-vs-symbolic visual register distinction works at 2D web layer (criterion 12 PASS via nebula-cloud register). This INFORMS but does not RESOLVE Branch A/B because:

- Branch B (Phase 3 baseline) is now validated at 2D pattern level. The figurative-nebula-anchor register is player-readable and Discipline-#59-honest.
- Branch A (Tal Rasha glyphic) remains pre-empirical at the player-surface layer. Phase 3 explicitly fenced this per criterion 12.
- The Branch A/B call is NOT "does Branch B work?" (Phase 3 says yes) — it is "does Branch A unlock something Branch B can't, in a way that justifies the additional complexity?" That's gated on Legolas zodiac corpus N + cultural-tradition coverage + cohesion-judge-pass.

**Recommendation: Phase 3 does not change the Branch A/B trigger conditions.** Wait for Legolas Wave-completion criteria to fire per the existing recognition record protocol. Phase 3 strengthens the "Branch B works" floor (good fallback if Branch A doesn't qualify); does not pre-commit either direction.

---

## Matt-call surfaces (itemized for KR routing)

1. **YELLOW 2 — Physical element dominance:** route option (A) substrate-honesty preservation + corpus-rebalance commission (gandalf recommendation per Discipline #59) UNLESS Matt overrides to (B) visual normalization. This is the explicit Matt-call drax flagged.

2. **Force-directed-as-production recommendation acknowledgment:** drax's recommendation is design-side concurred but the actual production-vs-design-tool split is a Matt-architectural-call moment worth surfacing. (Lower priority than #1.)

3. **WS2 commission timing-gate:** confirm WS2 scope-authoring defers until post-Legolas-final-Wave + post-Branch-A/B-decision. (KR can hold this as standing pattern unless Matt overrides.)

---

## Routing recommendation to KR

**Sequence:**

1. **NOW (fire immediately):** elrond methodology consultation on Hotspot A (substrate-vector proximity metric). Per Discipline #18.2 the post-baseline trigger has explicitly fired. Concrete pain is surfaced; consultation scope is defined above (§ 3 Hotspot A). This is the only immediately-firing commission from this review.

2. **NOW (low-cost drax follow-on):** drax amends close-report § "Lasso classification threshold" + AGENT_STATE.md TODO to cite ACTUAL scaffold values (`1100/1200/600/2`) not `outer_glow_radius`. Discipline #40 honesty fix. Ten-minute amendment.

3. **NEXT-SESSION (Matt-routing):** YELLOW 2 disposition (Matt-call on substrate-honesty vs normalization). KR aggregates this with jack-ryan Gate-2 + carries to Matt.

4. **AFTER Hotspot A returns:** queue elrond Hotspot B (UMAP comparison at substrate-vector level). KR holds in commission backlog.

5. **AFTER Legolas-final-Wave + Branch-A/B-Matt-call:** WS2 Niagara commission scope-authoring (gandalf lane). KR holds.

6. **WHEN rare-lineage kit engine generation lands:** drax Phase-3-supplement re-render against enriched corpus, validate rare-lineage buffer-space discovery. KR holds in long-arc backlog.

**Not commissioned by this review:** new canonical-doc amendment, gandalf canonical-write, rare-lineage engine commission (already in backlog per 2026-05-23 recognition records × 5; not surfaced new by this review).

---

## Discipline observations honored

- **#21 + #22 (no-sleep / timezone-agnosticism):** verdict uses workstream-relative framing throughout (NEXT-SESSION, AFTER Hotspot A returns, etc.); no time-of-day or sleep references.
- **#11 (empirical inspection):** spot-checked TwoLayerCanvas.tsx — surfaced documentation-drift on classifyLasso() thresholds (close-report says `outer_glow_radius`; code uses `1100/1200/600/2`). This is the value of empirical inspection over assumption.
- **#25 + #41 (substrate-led + rep-audit):** YELLOW 1 disposition preserves marginal-lineage axis separability from hybrid axis (semantic-layer audit; substrate votes at geometry, design audits at semantic). YELLOW 2 disposition routes corpus-rebalance via engine, not render-layer normalization (substrate-led).
- **#59 (substrate-coverage honesty):** central anchor of YELLOW 2 recommendation. Render layer should not lie about substrate distribution.

---

**Signed:** gandalf
**For routing:** jack-ryan Gate-2 → knight-rider aggregation → Matt
