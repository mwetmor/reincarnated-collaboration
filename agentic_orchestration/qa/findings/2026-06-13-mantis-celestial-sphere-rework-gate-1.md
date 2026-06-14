# Finding — 2026-06-13 — mantis celestial-sphere rework + figure-lighting-rig repair (Gate-1, pre-fire)

**Reviewer:** sam (PC-seam)
**Severity:** PASS-WITH-WARN (4 WARN, 2 INFO; no BLOCK)
**Target:** `agentic_orchestration/dispatches/2026-06-13-mantis-celestial-sphere-rework-and-figure-lighting-rig-repair.md` (DRAFT)
**Developer:** mantis (executor)
**Scope:** PC-seam only (`reincarnated-unreal/`); no engine JSON-contract write (consumes `cosmograph_sphere_001000stars_R8000.json` read-only)
**Mode:** DESIGN-MODE / Gate-1 critique-pair Pattern E
**Principles applied:** #1 (math-before-code), #2 (smoke-gate), #5 (severity matters); Discipline #1; R48.4

## Verdict

**PASS-WITH-WARN.** The dispatch is well-scoped, empirically grounded, and acceptance-testable. The two coupled repairs are correctly bounded against a single shared root cause (the origin star-cloud was both the S1 obstruction AND the figure's de-facto fill light), and § 6 excludes the right adjacent work. Four WARNs below sharpen acceptance-testability and surface one execution-environment hazard the dispatch under-specifies. None rises to BLOCK — all are addressable by tightening dispatch text before fire, not by reworking the mission.

---

## Findings

### WARN-1 — execution-environment hazard: "headless" is asserted but the Niagara-stack edit class is flagged UNVALIDATED over the bridge
**Section:** § 0 TL;DR ("both headless"), § 2 (1.2–1.4 emitter sim-mode migration + user-param exposure + BP authoring)
The dispatch frames repair #1 as headless throughout. But the live plan `2026-06-12-...-live-plan.md` line 13 explicitly records: *"bridge-into-windowed-editor for Niagara stack edits is UNVALIDATED; fallback = mantis hands Matt manual BP steps, or defer S1-sphere."* Sub-steps 1.2 (CPU→GPU sim migration) and 1.3 (expose array user-params on the emitter) are precisely Niagara-stack edits — the unvalidated class. The dispatch does not carry that fallback forward, so it implicitly assumes a capability that is unproven.
**Citation:** Principle #2 (smoke-gate — validate the path before relying on it); standing DXGI constraint (live-plan line 19: SSH/WSL windowed launch crashes at viewport creation).
**Fix:** Add to § 2 a fallback clause: *"If bridge-driven Niagara-stack edits (1.2–1.3) fail or prove unvalidated, mantis produces a precise manual-BP-step list for Matt at the `TheSa` console rather than opening a windowed editor over SSH."* This makes the headless claim conditional and honest, and prevents mantis from attempting a windowed-editor workaround that hits the DXGI viewport-creation crash.

### WARN-2 — acceptance #4 ("WITHOUT GPU crash at default") is not objectively checkable without a target metric
**Section:** § 4 criterion #4; § 2 sub-step 1.5
"Renders the look-up view WITHOUT GPU crash at default (no CVar band-aid needed)" is binary-on-crash but gives mantis no headroom target. The crash was a full-screen volumetric raymarch on a 4060 Ti; "doesn't crash once" is not the same as "stable." Criterion #7 captures `stat gpu`/`stat fps`/`stat unit` but sets no pass threshold.
**Citation:** Principle #2 (smoke-gate / empirical evidence — the criterion is empirical evidence, not time-passage); R48.4.
**Fix:** Tie #4 to a metric from #7 — e.g. *"look-up view holds a stable frame for ≥N seconds with `stat gpu` GPU-frame under the 4060 Ti budget (no rising trend toward device-removed); band-aid CVars OFF."* Also note: #4's "no GPU crash" validation requires a render, which is Matt-at-console/RDP per the DXGI gate — mantis cannot self-verify #4 headlessly. Make that dependency explicit (see WARN-4).

### WARN-3 — acceptance #6 (Rig A/B "judgeable lighting difference") + #5 mythic-weight judgment are render-gated subjective criteria mantis cannot self-close
**Section:** § 4 criteria #5, #6
Both require a rendered Lit view and a human readability judgment. Mantis's headless authoring cannot produce the evidence; they require the Matt-at-console render pass (the S5 re-shoot). The dispatch lists them as mantis acceptance criteria without partitioning "mantis authors the fix" from "render pass confirms the fix."
**Citation:** Principle #5 (severity matters — don't conflate authoring-done with verified-done); Principle #2.
**Fix:** Split § 4 into two tiers: **(A) mantis-closeable headless** (#1, #2, #3-authoring, lights re-aimed/configured, #10) and **(B) render-gated, confirmed at the S1+S5 capture pass with Matt at console/RDP** (#3-renders, #4, #5, #6, #7). Gate-2 then reviews tier-A on the commit; tier-B closes at the subsequent render session. This matches the actual evidence chain (P0.1 produced findings, not captures).

### WARN-4 — Gate-2 (#8) and wave-close push (#9) are sequenced as if render-evidence is in hand at commit; it is not
**Section:** § 4 criteria #8, #9; § 7 gate sequence step 4
With WARN-3 unresolved, Gate-2 would be asked to PASS a commit whose render-gated criteria (#4, #5, #6, #7) are unverifiable at commit time. I can Gate-2 the **headless authoring tier** (math note, root-cause doc, GPU-sim migration, BP authoring, light re-aim, D7) on the commit — but I cannot PASS render-confirmation criteria without the capture evidence.
**Citation:** Principle #2; REVIEW_PROCESS lifecycle (Gate-2 reviews what the commit demonstrates).
**Fix:** State that Sam Gate-2 (#8) reviews the **tier-A headless authoring** on mantis's commit; render-gated tier-B criteria are confirmed post-render and do not block the commit's Gate-2. Wave-close push (#9) fires at tier-A Gate-2 PASS per the standing PC-seam wave-close pattern; it does not wait on the render pass.

### INFO-1 — § 1 math-before-code is sufficient for the reposition; the root-cause requirement is correctly framed as a gate, not an assumption
**Section:** § 1, sub-step 1.1
§ 1 satisfies Discipline #1 well: it specifies R=8,000, names the source JSON, requires a coordinate-convention/handedness/up-axis transform note before binding, AND — correctly — refuses silent count reduction ("document the source of the 1,005,000 before cutting — silent count reduction without root-cause is a Discipline #1 violation"). This is the right posture. The ~1,000× multiplier (1,005,000 vs 1,000 stars) is the load-bearing unknown and the dispatch makes diagnosing it a hard precondition. No fix needed; recording as a strength.

### INFO-2 — scope boundary is clean; coupling rationale is sound
**Section:** § 0 ("Why coupled"), § 6 (out of scope)
The two repairs share a single root cause (the deleted origin star-cloud was the figure's de-facto fill), so bundling them is correct — splitting would create a figure-lighting repair that can't be verified without the sphere present-and-repositioned (exactly acceptance #5's condition). § 6 correctly excludes `FigureStandIn` mesh design (radagast), WS2 cluster-rune overlay, WS3 cinematic, the `SK_EarthAvatar` asset itself, and saving session-only CVar state. No scope creep. The `FigureStandIn` placeholder exclusion is well-routed to radagast's design-fit lens (§ 7.2c), not assumed away.

## R48.4 assessment (lens 4)
The CPU→GPU Niagara sim migration is correctly motivated (the 1M cap is CPU-only; GPU sim removes it) and the nebula taming (1.5) targets the confirmed crash source with concrete CVar reductions. The framing against the 4060 Ti budget is present but soft on the verification side — see WARN-2 (needs a stability metric, not just "didn't crash"). The migration direction itself is sound and respects R48.4's host-aware-concurrency intent; no resource hazard is introduced by the change, and 1.6 (cap star overdraw / GPU bounds) addresses the overdraw vector that froze the editor. WARN-2 is the only R48.4-adjacent tightening needed.

## Cross-cutting flag
None requiring Mac-jack-ryan consultation. This is PC-seam-scoped: `reincarnated-unreal/` BP + Niagara + lighting authoring, consuming an engine-emitted JSON read-only (no engine contract write). No decisions-log entry warranted (routine implementation per decision-log when-to-file table; the geometry lock already lives in canonical § 2.6). If the 1,005,000 root-cause turns out to be a defect in how the engine-side JSON is consumed at the emitter binding, that would become a cross-cutting flag at Gate-2 — not now.

## Action
- [ ] David-H: fold WARN-1 fallback clause into § 2; partition § 4 into tier-A (mantis-headless) / tier-B (render-gated) per WARN-3; restate #8/#9 per WARN-4; add a stability metric to #4 per WARN-2. All four are dispatch-text tightenings — no mission rework.
- [ ] David-H: re-confirm with radagast that the design-fit lens (§ 7.2) is unchanged by these WARNs (it is — they're process/testability, not design).
- [ ] mantis (at fire): honor the WARN-1 fallback — never open a windowed editor over SSH; manual-BP-steps-to-Matt is the fallback, not a bridge workaround.
- [ ] Matt: no decision needed at Gate-1 (no BLOCK). Render-gated tier-B confirmation will need Matt at console/RDP at the post-commit S1+S5 capture pass.

## References
- `agentic_orchestration/dispatches/2026-06-13-mantis-celestial-sphere-rework-and-figure-lighting-rig-repair.md`
- `agentic_orchestration/david-h/notes/2026-06-13-p0-1-s5-blocked-findings-and-routing.md`
- `agentic_orchestration/david-h/notes/2026-06-13-p0-1-resume-after-gpu-crash.md`
- `agentic_orchestration/david-h/notes/2026-06-12-p0-1-render-session-live-plan.md` (Gate-A definition; line 13 unvalidated-bridge flag; line 19 DXGI gate)
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 2.6 (referenced, not re-read this Gate-1)
