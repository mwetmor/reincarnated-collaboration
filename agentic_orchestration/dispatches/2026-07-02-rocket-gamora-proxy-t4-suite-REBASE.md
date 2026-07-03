# Dispatch — 2026-07-02 — rocket (→ gamora, serial) — proxy-T4 suite B1-REBASE (Lane B)

**From:** knight-rider
**To:** rocket (Phase 1 — execution-layer strategies) → gamora (Phase 2 — sim-eval + magnitude cert). SERIAL, same engine repo.
**Approved by:** Matt 2026-07-02 (B1-REBASE relay — four rulings folded into spec v3; supersedes the two-lane relay's B1 row)
**Estimated effort:** 2–3 days (Phase 1 + Phase 2). Phase 3 (CONVERGENCE + DUAL_PROXY) is a LATER dispatch behind gandalf's Q6/Q7 artifacts — NOT this dispatch's work.
**Acceptance:** the v1 S1–S6 execution classes + the retired five-name revival classes + the `:45-46` docstring register are REMOVED; the ratified catalog-v2 PROXY family is activated at the execution + sim-eval layers for the demo subset (ASCENSION + SOVEREIGNTY + FISSION + newly-designed ZONE_CONTROL); INVERSION carries a deferred-by-ruling exclusion; A1–A6 (spec v3 §8) pass on ratified members.
**Status:** **GATE-1 CLEARED — ENDORSE-WITH-FOLDS (jack-ryan + gandalf, 2026-07-02); folds applied below. CLEAR TO FIRE Phase 1.**

## Gate-1 outcome (folds applied 2026-07-02)

Both critics ENDORSE-WITH-FOLDS. They converged on a **factual correction that resolves the two reserved ZONE_CONTROL items**:

- **ZONE_CONTROL family — RULED GEOMETRY (not COMBAT).** jack-ryan (the delegated family-ruler per the relay) found `GEOMETRY_COLLAPSE` is in the **GEOMETRY** family, not COMBAT (`t4_catalog_v2.py:91`) — spec §6.1's "COMBAT lean" rested on a misread. ZONE_CONTROL's own eligibility (§6.1: "mirroring GEOMETRY_COLLAPSE's dominance-gate") belongs next to the member it mirrors. gandalf corroborated (design Fold 5). **ZONE_CONTROL enters GEOMETRY.** Spec §6.1 correction (COMBAT→GEOMETRY) is **gandalf-owed** (routed); THIS dispatch's GEOMETRY assignment governs for rocket.
- **Overlap / max-1 — RULED: GEOMETRY gets a max-1 multi-slot rule** once ZONE_CONTROL joins it. ZONE_CONTROL + GEOMETRY_COLLAPSE both gate the same 60%-dominance AoE surface — a real mechanic collision (double-dip). Putting ZONE_CONTROL in GEOMETRY (not COMBAT) lets the fix be a clean within-family rule; the DEFENSE max-1 (intra-family mechanic homogeneity) is the exact precedent. (Note: the v3-spec paraphrase "restricts only ELEMENT and DEFENSE" is factually off — the max-1 is on DEFENSE only; ELEMENT has none. Corrected here.)

Folds F-a…F-g are integrated into Scope/Acceptance below.

## Context — why this is a rebase, not a fresh B1

The prior B1 (rocket `17d5f80` 21:55 + gamora `02d7cd5` 22:07) built a **drafted parallel v1 S1–S6 family** in ignorance of ratified prior art. Between the two phases (22:04), a parallel gandalf session executed **Matt's prior-art catch** (*"didn't we already have these scoped in a doc? I know for a fact we did"*) and retired v1 in favor of the **ratified catalog-v2 PROXY family** (`t4_catalog_v2.py:53-58`, 7 gen-side consumers). KR caught the drift (⛔ BLOCKED — REBASE) before recording B1 closed; Matt ruled the re-base scope. **The A3 differentiation METHOD is proven and carries forward — it re-runs on ratified members.** Spec v3 §3 gives the v1→ratified retirement map; §2 the ratified family; §6/§7 the rulings.

**The four Matt rulings this dispatch executes (all folded into spec v3):**
1. **Five-name dormant register RETIRED** (§6). Provenance closed in git (`f9762a8`→`d6bca67`): ResourceBuffer / MechanicReplacement / ZoneControl / ConditionalModifier / ProxySpawn are the below-the-cut tail of a 2026-05-25 Legolas scored shortlist, parked as ONE docstring line — never designed, zero canonical presence. "Dormant capstones alive" = activate the ratified catalog. Rebase REMOVES the four improvised revival classes + the `:45-46` docstring line.
2. **ZONE_CONTROL enters as a newly DESIGNED 26th catalog member** (§6.1; COMBAT-family lean). The one retired-list fantasy with no catalog-v2 owner + real genre precedent. Gate-1 confirms family + rules the GEOMETRY_COLLAPSE overlap / COMBAT max-1 question.
3. **Demo family = FIVE ratified members, two-phase.** Phase 1 (this dispatch): ASCENSION + SOVEREIGNTY + FISSION + ZONE_CONTROL riding. Phase 2 (later, behind gandalf Q6/Q7): CONVERGENCE + DUAL_PROXY.
4. **PROXY_INVERSION DEFERRED WHOLLY** (§7.1; kit-viability + timing-degeneracy). Catalog constant STANDS; execution layer carries a deferred-by-ruling exclusion (η never offers it) with a ruling-cite comment. Named re-entry: INVERSION-v2 kit-level redesign — parked, no commitment.

## Required reading before starting

- `canonical/reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` — **spec v3 (GOVERNS)**: §2 ratified family, §3 v1-retirement map, §4 η integration, §5 R1–R5, §6 register retirement, §6.1 ZONE_CONTROL design authority, §7 two-phase / §7.1 INVERSION deferral, §8 acceptance
- `t4_catalog_v2.py:53-58` — ratified PROXY family constants + family map (the 7 live consumers)
- `agentic_orchestration/gandalf/notes/2026-06-12-session-2-proxy-companion-architecture-spec.md` — 14-type Tier-1 taxonomy + per-type ASCENSION upgrade table (§2 references it)
- The prior-B1 commits being retired: `rocket/v-proxy-t4-suite-strategies-1` @ `17d5f80` (v1 classes + revival classes) + `gamora/v-proxy-t4-suite-eval-1` @ `02d7cd5` (v1 cert) — salvage the η/gate/test scaffolding; retire the v1 members
- gamora D3 cert `gamora/v-proxy-fight-calibration-1` @ `abb010d` — the four certified SCAFFOLD magnitudes (R2 hard boundary)
- `mechanic_alteration.py` — η architecture (:65/:69/:338), ABC (:255), the retired v1.1 docstring register (:45-46), the v1 S1–S6 classes (:986+ — retire), `sim_prerequisite` (:266-271 — retires with register)

## Cross-seam contract change? (Principle 6 gate — YES)

- **Removals:** v1 S1–S6 strategy classes + four improvised revival classes + `:45-46` docstring register + `sim_prerequisite` mechanism (retires with register).
- **Addition:** ZONE_CONTROL as a new `t4_catalog_v2.py` constant + **GEOMETRY** family-map entry (26th member) — a generation-side surface change with the 7 existing consumers to keep consistent.
  - **F-c (Gate-1 F2 / gandalf Fold 4) — count-guard bump:** `t4_catalog_v2.py:118-122` asserts `len == 25` at import (a Disc #11 count-guard). Bump to **26**; add the `FAMILY_MEMBERSHIP_V2` GEOMETRY entry; update the `# GEOMETRY family (N)` header comment. Name these explicitly so the import assert is not a surprise.
- **Round-trip:** MIGRATION.md entry (generation seam) for the family remap (v1 retired → ratified activated) + the ZONE_CONTROL catalog addition; note the emit-shape implication for B4 (`primary_t4` now a ratified-family value — the DDA-lock widening already routed to B4 stays valid). Cross-seam → MIGRATION before tag (ADR-004).

## Scope

### Phase 1 — rocket (execution-layer strategies)
- [ ] **Retire v1:** remove the S1–S6 strategy classes (`mechanic_alteration.py:986+`); remove the four improvised dormant-revival classes; remove the `:45-46` docstring register + the `sim_prerequisite` mechanism it fed. **Lineage in the commit message** (per §6 ruling — no silent delete).
- [ ] **Activate the demo subset with RATIFIED eligibility gates** (spec §2): ASCENSION (≥1 Tier-1 mechanical proxy), SOVEREIGNTY (Passive Fighter/Golem; energy≠mana; ≥3 chains), FISSION (Golem/Passive Fighter/Bodyguard; HP-tracking mid/full tier). Each `opportunity_scan()` → 0.0 outside its gate.
- [ ] **ZONE_CONTROL (§6.1) — GEOMETRY family (Gate-1 ruled; NOT COMBAT):** add the catalog constant + **GEOMETRY** family-map entry; build the strategy with the control/AoE-dominance eligibility gate (mirror GEOMETRY_COLLAPSE's dominance-gate; rocket derives the exact threshold + documents it); decl-level zone anchor; **start-modest magnitudes** (doc-47 Phase-4 DDA lesson) as SCAFFOLD for gamora. Salvage code from the improvised revival class only where it matches this design.
  - [ ] **F-a (Gate-1) — GEOMETRY max-1 multi-slot rule:** add a max-1 rule to the GEOMETRY family (ZONE_CONTROL + GEOMETRY_COLLAPSE both gate 60%-dominance AoE → no kit may carry both). Mirror the DEFENSE max-1 implementation. (Session-1 §2.2 max-1 is on DEFENSE only, not ELEMENT — correct any inherited paraphrase.)
  - [ ] **F-b (gandalf) — deliberate defensive-lane coverage check:** check whether the control/AoE-dominance gate captures **Terrain-Anchor defensive kits** (plausibly AoE/control-dominant). If it does, the Phase-1 defensive-lane gap (see open-questions) partially closes without a Phase-2 dependency. Document the overlap in the gate-derivation note — deliberate, not accidental.
- [ ] **INVERSION exclusion (§7.1):** η never offers INVERSION; implement with a ruling-cite comment (not a bare skip). Catalog constant stands.
- [ ] **η wiring (spec §4):** axis_match keys off DECL SHAPE per §4.2; thematic per element-resonance; sim_viability→1.0 on activation; manifestation ladder (FISSION integer/entity axis T4_active-only).
- [ ] **CONVERGENCE Phase-2 prerequisite check (named, §7):** confirm generation can EMIT 2-type cross-family proxy decls; if not, file it as a **named prerequisite on Phase 2** (not a silent skip).
- [ ] MIGRATION.md entry (family remap + ZONE_CONTROL addition); math-note-first (Disc #1); AGENT_STATE updated
- [ ] Tag: `rocket/v-proxy-t4-rebase-strategies-1`

### Phase 2 — gamora (sim-eval + magnitude cert), after Phase 1 lands
- [ ] **Re-certify magnitudes** for the four activated members against the D3-certified scaffold — the ratified numbers are **PROVISIONAL-by-ratification**; math-note-first (Disc #18), single-parameter-isolated sweeps (Disc #24), fresh seeds 53M+, boss anchor FIXED per D3 harness.
- [ ] **A2/A3/A5/A6 (spec §8) on ratified members.** A3 re-runs the proven differentiation method: the two D3-certified fixtures must draw DIFFERENT top members (Matt-doubt test).
  - [ ] **F-d (gandalf Fold 6) — A3 named risk pair:** ASCENSION ("servant changes what it is") and SOVEREIGNTY ("second hero fights beside you") both upgrade proxy autonomy and their gates overlap on Passive Fighter. If both certified fixtures are count-1-full-body-Fighter shapes they could BOTH lean SOVEREIGNTY and fail A3. Verify the axis_match tiebreak (§4.2: count-N minimal → ASCENSION; count-1 full body → SOVEREIGNTY) actually separates them; name ASCENSION-vs-SOVEREIGNTY as the specific pair at collapse-risk.
  - [ ] **F-e (gandalf Fold 2) — ZONE_CONTROL A2 = DENIAL not damage:** the A2 control-heavy fixture must be a boss whose optimal line is *forced through* the zone (a HARD fixture requirement, not soft). If the boss can fight around it, or the zone reads as a damage puddle, ZONE_CONTROL collapses to an AoE reskin and fails A4. The distinctness is positional/denial ("the ground turns against them"), not damage.
- [ ] **A5 boundaries:** R1 (bridge-state no-propagation; Set-#6 Clause B only sanctioned cross-surface) + R2 (calibrated `proxy_commander.py:59-70` untouched) explicit test assertions.
  - [ ] **F-f (Gate-1 F3) — GEOMETRY max-1 assertion:** add an A5 test — no kit draws both ZONE_CONTROL and GEOMETRY_COLLAPSE (the enforcement point for the F-a max-1 ruling).
- [ ] **A6 rulings enforced:** register retirement executed (classes + docstring REMOVED); INVERSION exclusion asserted (no kit draws it); solo-bin zero-effect; no eligible-kit class left with zero family members (§4.2 coverage note — critical with INVERSION deferred).
- [ ] MIGRATION.md sim-side note; AGENT_STATE updated
- [ ] Tag: `gamora/v-proxy-t4-rebase-eval-1`

### Phase 3 — DEFERRED (NOT this dispatch)
CONVERGENCE + DUAL_PROXY strategy classes + matrix/pool wiring + cert, authored as a LATER dispatch after gandalf's Q6 pair-matrix + Q7 compatibility pools land. Named here so the two-phase boundary is explicit.

## Acceptance criteria (spec v3 §8)
- [ ] A1 emission bands (checked at B4, not here) — the family members are in `t4_candidates`, `primary_t4` a ratified-family value
- [ ] A2 sim delta per activated member (proxy amplified, never the caster body)
- [ ] A3 differentiation PASS on ratified members (different tops)
- [ ] A4 legibility (one-clause read per member — feeds D5). **ZONE_CONTROL's clause = area-DENIAL** ("the ground itself turns against them"), NOT damage (F-e) — else it fails the §20d distinctness bar as an AoE reskin.
- [ ] A5 R1/R2 boundaries asserted
- [ ] A6 rulings enforced (retirement executed; INVERSION excluded; coverage held)

## Quality criterion

**Game-quality goal this dispatch serves:** the summoner class fantasy peaks — not breaks — at capstone unlock. A summon-bearing kit draws a proxy-focused T4 that amplifies the proxies (who carry 100% of the kill, W2), from a family whose members are structurally differentiated by decl shape, so *different* summoners get *different* capstones. This is the ratified design, finally at the execution layer — the honest answer to Matt's *"will only one T4 work for all Proxies?"* doubt.

**Refutation conditions (surface if any apply):**
- The retirement is incomplete (any v1 S1–S6 class, revival class, or the `:45-46` docstring survives) — A6 fails
- ZONE_CONTROL's family/overlap questions were resolved by the agent rather than at Gate-1 (§6.1 reserves them for jack-ryan)
- INVERSION is reachable by any kit (η offers it) — ruling-4 violation
- A member makes caster-alone viable (T4 amplifies the body not the proxy) — R1 violation
- An eligible-kit class is left with zero family members after INVERSION's deferral (§4.2 coverage) — regression against a defensive-type kit
- Magnitudes are shipped un-certified or the sweeps are not single-parameter-isolated (Disc #24)
- CONVERGENCE's 2-type-decl prerequisite is silently skipped rather than named on Phase 2

## Out of scope (explicit non-goals)
- CONVERGENCE + DUAL_PROXY (Phase 3 — behind gandalf Q6/Q7)
- The Q6/Q7 artifacts themselves (gandalf-owed)
- INVERSION-v2 redesign (parked, §7.1 — no commitment)
- The B4 emission run + DDA-lock validator widening (separate B4 dispatch; this dispatch makes `primary_t4` a ratified-family value, B4 widens the emitter to accept it)
- The ranged-proxy NAV question (PART E fork; B5 curation decides)
- T4 flavor naming/narration (phase-5 pass)

## Open questions for the agent (document; escalate to KR)
- ZONE_CONTROL exact eligibility threshold (rocket derives from bc control/AoE-dominance axes; documents the derivation) — the DESIGN of the gate is §6.1 rocket's; the FAMILY (GEOMETRY) + overlap RULE (GEOMETRY max-1) is Gate-1-ruled above
- Whether the improvised revival-class code is salvageable for ZONE_CONTROL (§6.1 permits where it matches the new design)
- CONVERGENCE 2-type-decl emit capability (confirm or name-as-prerequisite for Phase 3)

## ⚑ Carried Matt-plate item (Gate-1 gandalf Fold 3 — NOT a fire-blocker)
**Phase-1 defensive-lane capstone thinness.** With INVERSION deferred wholly and DUAL_PROXY in Phase 2, a pure-defensive **non-Bodyguard** proxy kit (Terrain Anchor / Warcry-Buff Spirit) at Phase-1 demo has **only ASCENSION** — one family member, so A3 differentiation can't fire for that kit-shape and the summoner gets no capstone choice-feel. Satisfies A6 ("no zero-member class") but is thin. **Not a blocker** (gandalf: the four-member roster is a healthy demo cut in aggregate; the gap is local to the defensive sub-lane). **Empirical gate:** verify the defensive-proxy-bin count on the B4 emission run (`proxy_contribution_pct` telemetry on defensive-bin kits). If near-zero → accept. If non-trivial → consider F-b (ZONE_CONTROL gate absorbs Terrain-Anchor kits) or pulling DUAL_PROXY's defensive slice forward. Surfaced to Matt; carried to the B4 report.

## References
- spec v3 (governs) · B1-REBASE relay (Matt 2026-07-02) · retired tags `17d5f80`/`02d7cd5` · D3 cert `abb010d` · provenance `f9762a8`→`d6bca67`
- MASTER: `2026-07-02-one-realm-mvp-build-MASTER.md` §8 (Lane B — B1 row bumps to this scope)
