# Hive-Mind Protocol Amendments — 2026-05-21 Evening

**Date:** 2026-05-21 (evening, post P0 close + BDI formalism)
**Author:** gandalf (story-and-design steward)
**Purpose:** capture protocol amendments authorized this evening for integration into `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.3 (tomorrow's session)
**Authority:** Matt-approved (this conversation)
**Status:** AUTHORED — pending protocol v1.3 fold-in tomorrow

---

## 0. TL;DR

Three substantive additions to the QD-engine rebuild protocol, authorized this evening:

1. **BDI resonance formalism** added as foundational mathematical structure (`canonical/story/build-defining-resonance-formula-2026-05-21.md`); 5 hypothesis tests (H1-H5) added to P1+ workstream as diagnostic measurements
2. **Gear-as-substrate moves into V1 pre-gauntlet scope** (P1-P2 territory; was post-P7). Phase G timing revised; gear-archetype becomes 4th substrate axis in V1.
3. **Tier 4 keystone architecture** declared open-question; design pass scheduled pre-P5 with BDI rank-completion framing

These amendments do NOT change the existing P0-P7 critical path structure. They add scope, sharpen architecture, and surface explicit open questions.

---

## 1. Amendment 1 — BDI resonance formalism added

### 1.1 Canonical reference

New canonical doc: `canonical/story/build-defining-resonance-formula-2026-05-21.md`

Core structure: Build-Defining Index (BDI) measures interaction-term dominance in WR landscape; ω-field (mechanical overlap) + τ-field (thematic resonance) predict pairwise β; rank-3 γ-triples are signature builds; Tier 4 keystones are rank-completers.

### 1.2 Hypothesis tests for hive-mind execution (P1+)

Per build-defining doc § 7.1, **five hypothesis tests** are added to the P1+ workstream as **diagnostic measurements** (not generation constraints):

| Test | Hypothesis | Owner | Phase |
|---|---|---|---|
| H1 | Pairwise interaction outliers exist in WR landscape | rocket (model fit) + legolas (synthesis) | P1 |
| H2 | ω-field predicts β-magnitude | gandalf (ω-table) + rocket (correlation analysis) | P1 |
| H3 | τ-field bridges produce negative-τ build-defining moments | gandalf (τ-table) + rocket (set-comparison analysis) | P1 |
| H4 | Rank-3 γ-coefficients dominate β-coefficients in signature builds | rocket (rank-3 model fit) | P1 |
| H5 | BDI correlates with cohesion-judge score | post-P5 (requires cohesion-judge scores at archive scale) | **P5+** |

### 1.3 Non-blocking, non-constraining properties

Per Matt's explicit directive this evening, the hypothesis tests have these safety properties:

- **Read-only against archive data.** No impact on substrate composer or convergence loop.
- **Diagnostic, not generative.** Tests measure whether resonance is empirically real; they do NOT mandate that the composer select for high-BDI vectors.
- **No endless-loop risk.** BDI is a metric, never a hard filter. The composer's diversity-maintenance has priority. The convergence loop's reject-and-recompose pathway handles non-convergence at any substrate vector.
- **Optional adoption.** If H1-H4 confirm, P1+ substrate composer CAN optionally weight high-BDI vectors as a generative bias (additive, not exclusive). If tests don't confirm, formalism parks; existing composer continues as baseline.

### 1.4 Decision gate: BDI-E

Per build-defining doc § 10, **BDI-E is the gate** at which the hive-mind decides:
- If H1-H4 confirm → adopt BDI-aware composer extension (BDI-F) as P2+ optimization
- If results mixed → reframe formalism; refine ω/τ tables; re-test
- If tests fail → park formalism; existing architecture continues

BDI-E gate timing: post-H1-H4 execution; tomorrow-morning earliest if attribution data + archive fits land cleanly.

### 1.5 Workstream additions

**P1 new workstreams (added to protocol v1.3):**

| New ID | Scope | Effort estimate | Dependency |
|---|---|---|---|
| W1.20 | BDI hypothesis-test infrastructure (model-fit harness + ω/τ table data structures) | 1-2 weeks | None |
| W1.21 | H1 + H2 + H3 + H4 execution + result synthesis | 1 week | W1.20 |
| W1.22 | BDI-E gate decision (gandalf + Matt design call) | 0.5 day | W1.21 |

### 1.6 Tier 4 architecture connection

The Tier 4 keystone catalogue authorship (T4-B per hive-mind state evening doc § 4.3 open question 11-14) is **directly informed by the BDI rank-completion framing.** Each catalogue keystone is authored as the third leg of a known high-β substrate-pair, producing a known rank-3 identity.

This is **pre-P5 design work** (gandalf + Matt) that lands before the keystone catalogue ships in code (rocket; P3-P4 territory per math note v1.1 § 4).

---

## 2. Amendment 2 — Gear-as-substrate LITE path (V1 derived-tag; v1.1/v2 substrate promotion)

### 2.1 Decision (revised late 2026-05-21 evening)

Per Matt 2026-05-21 evening (post cross-repo concern surfaced): **adopt the LITE path** — `signature_gear_archetype` lands as a DERIVED TAG in v1 (not a generative substrate), promoting to full substrate in v1.1/v2 post-P7.

**Rationale:** cross-repo coherence concern (demo/Unity/loadout need canonical class-identity-to-gear contract between now and P7) is solved by LITE; engine-internal disciplined sequencing (3-substrate empirical test as dispositive) is preserved by LITE; v1.1/v2 promotion has clean retrofit path. Full architectural rationale: `canonical/story/gear-as-substrate-2026-05-21.md` § 0.5.6.

**Verified precondition:** stat distributions are NOT random in post-legacy-archetype world. `ELEMENT_SCALING_ATTRIBUTE` (`element_biases.py:28`) is canonical and deterministic (fire/water/lightning/shadow → INT; earth/wind/holy → WIS; physical → STR). The rule-table operates on stable foundation.

### 2.2 Phase G-LITE timing

| Phase | Scope | Timing |
|---|---|---|
| G0 | Architectural commitment | This conversation (done) |
| **G1-LITE** | Rule-table v1 finalization (15 archetypes; deterministic rule mapping substrate-vector → gear-archetype) | Pre-P1 (gandalf + Matt design call; tomorrow's session) |
| **G2-LITE** | Generation-pipeline `signature_gear_archetype` computation + telemetry column + per-class persistence | **P1** (~3-5 days; rocket) |
| **G3-LITE** | DEFERRED — gear-instance generation constrained by archetype | Deferred to v1.1/v2 |
| **G4-LITE** | Cohesion-judge light prompt extension (signature_gear_archetype as identity hint) | **P5** (~1 day; star-lord) |
| **G5-LITE** | Demo + loadout app + Unity consume signature_gear_archetype | **P1+** (parallel work; drax + Unity team) |
| G6 | Spirit-swap meta-layer integration (Spirit's Core Gear) | Post-P5 (unchanged) |
| **G7-LITE** | DEFERRED — 4-substrate empirical validation gate | Deferred to v1.1/v2 promotion |
| **G-PROMOTE-v1.1** | Promote rule-table to search-space (signature_gear_archetype becomes generative substrate) | v1.1/v2 (post-P7) |

### 2.3 New workstreams in P1 / P5 (LITE)

| New ID | Scope | Effort | Owner |
|---|---|---|---|
| **W1.15-LITE** | `signature_gear_archetype` derivation function + 15-archetype rule table + telemetry column + per-class persistence | **3-5 days** | rocket |
| ~~W1.16~~ | (DEFERRED — composer extension is v1.1/v2 work) | — | — |
| ~~W1.17~~ | (DEFERRED — gear-instance archetype-filter is v1.1/v2 work) | — | — |
| **W5.3-LITE** | Cohesion-judge prompt extension to receive signature_gear_archetype as identity hint (P5 priority 4 in lightweight form) | **1 day** | star-lord |
| ~~W2.5~~ | (DEFERRED — gear_loadout_cycling_hook reframing waits for full substrate promotion in v1.1/v2) | — | — |

### 2.4 Critical-path impact (LITE)

P1 workstream addition: **~3-5 days for W1.15-LITE** (was 2-3 weeks for full V1 inclusion). P5 workstream addition: **~1 day for W5.3-LITE** (was 1-2 weeks). Total v1 engine cost: **~1 week** (was 3-4 weeks).

BDI workstreams (W1.20, W1.21, W1.22) remain unchanged — they can run against the 3-substrate space with signature_gear_archetype available as proxy 4th-dimension context for diagnostic analysis (without it being a generative input).

### 2.5 Cross-repo unblocking (the deciding factor)

The LITE path unblocks player-facing surfaces:

| Surface | Owner | Pre-LITE state | Post-LITE state |
|---|---|---|---|
| reincarnated-demo (Pixi.js) | drax | No canonical class-identity-to-gear mapping; presentation incoherence risk | Canonical contract via signature_gear_archetype; coherent class-identity rendering |
| reincarnated-loadout (React/Vite) | drax | Cannot label "your signature gear"; ad-hoc mapping conflict risk | Filters "signature gear" vs "any gear" from canonical field |
| Unity production | drax | No stable gear-identity contract for visual rigging | Stable contract; identity-rigging work proceeds |
| Spirit-swap meta-layer (post-P5) | knight-rider sequences | "Spirit's Core Gear" deferred to post-P7 alongside full substrate | Per-spirit signature gear available in form library from v1; mechanic depth (gameplay loop) lands post-P5 |

### 2.6 The "blunderbuss must be viable in battle simulation" discipline (LITE)

Preserved in LITE form: every gear-archetype in the v1 rule-table value-set must be sim-viable. The rule-table value-set is the 15-archetype catalogue per `gear-as-substrate-2026-05-21.md` § 3. Catalogue locks at G1-LITE per archetype-by-archetype sim-viability verification (gandalf + Matt design call + rocket sim verification).

### 2.7 Full V1 inclusion case archived

The full V1 inclusion case (W1.15, W1.16, W1.17, W2.5 at 2-3 weeks each) is **archived** as a candidate path; preserved in this doc and in gear-as-substrate-doc § 0.5.5 history for reference. The LITE path supersedes; the full V1 case may be revisited if LITE path empirically shows insufficient richness during P5 BDI testing (unlikely given the formalism, but a real backstop).

---

## 3. Amendment 3 — Tier 4 keystone architecture open-question

### 3.1 Surfaced gap

The math note v1.1 § 4 specified Tier 4 keystones as mechanic-altering (qualitative regime change). It did NOT specify:

- Hierarchy (signature capstone + secondary capstones recommended in BDI § 6, pending Matt design call)
- Authorship pattern (hand-authored catalogue recommended; ~30-50 keystones)
- Gear-Tier 4 coupling (signature capstone REQUIRES gear-substrate to express full mechanic)
- Development phasing (T4-A pre-P5; T4-B P3-P4; T4-C P5; T4-D post-P7)

### 3.2 Authorship phases (proposed)

| Phase | Scope | Owner | Timing |
|---|---|---|---|
| T4-A | Tier 4 architecture design call (hierarchy + authorship pattern + gear coupling decisions) | gandalf + Matt | Pre-P3 (tomorrow's session or this week) |
| T4-B | v1 catalogue authorship (~30-50 keystones; each designed as rank-3 completer per BDI § 6) | gandalf + Matt (design); rocket (engine integration) | P3-P4 |
| T4-C | Cohesion-judge prompt extension for signature-vs-secondary capstone distinction (refines P5 priority 2) | star-lord + gandalf | P5 |
| T4-D | Gear-anchored signature capstone extension | gandalf + Matt | Pre-P5 (parallel to G1) |
| T4-E | Procedural/LLM-augmented Tier 4 variant generation | Deferred | v2+ |

### 3.3 BDI integration

Per BDI § 6 + § 8.3:
- **Signature capstone** = the Tier 4 keystone that completes the kit's primary rank-3 resonance (gear-anchored when gear-substrate live)
- **Secondary capstones** = additional Tier 4 keystones that deepen primary resonance (boost γ) or open auxiliary rank-2 resonances (auxiliary β-pairs)

The catalogue authorship (T4-B) explicitly targets known rank-3 identities (e.g., Powder Hex-Cannon, Smoke-Vampire, Inferno-Knight per BDI § 5.1).

### 3.4 Open questions for tomorrow's design call

Per BDI doc § 5.1 and hive-mind state evening doc § 4.3:
- Final hierarchy decision (1 signature + 1-3 secondaries; vs all-defining; vs only-one-Tier-4)
- Authorship pattern (hand-authored catalogue v1; LLM-augmented v2; or hybrid)
- Gear-anchoring strength (mechanical-degradation-without-gear vs cosmetic-only)
- Catalogue size (~30-50; final number TBD)

---

## 4. Protocol v1.3 fold-in instructions

When the protocol doc is amended tomorrow to v1.3, the following sections receive updates:

| Protocol section | Update |
|---|---|
| § 1 — Overview | Add reference to BDI formalism + gear-substrate-as-V1 + Tier 4 design pass |
| § 2 — Phase summary table | Add G1-G7 + T4-A-T4-D + BDI-A-BDI-H phases |
| § P1 — workstream list | Add W1.15, W1.16, W1.17, W1.20, W1.21, W1.22 |
| § P2 — workstream list | Add W2.5 |
| § P3 — workstream list | Reference T4-B (catalogue authorship phase) |
| § P5 — workstream list | Reference G4, G7, T4-C, BDI-G |
| § 6 (cohesion-judge) | Reference BDI § 8 and § 9 for prompt-extension informed by BDI hints |
| § 13 (v1/v2 trajectory) | Note that gear-substrate is now V1; trait-cluster-as-substrate remains v2; BDI rank-4+ deferred |

---

## 5. Risk and discipline notes

### 5.1 Scope expansion risk

P1 effort estimate adds **~1.5-2 weeks** under LITE path (W1.15-LITE ~3-5 days + BDI infrastructure W1.20-W1.22 ~1-2 weeks). This is bounded. **Mitigation:** the BDI tests are diagnostic and can run in background (parallel to other P1 work); gear-substrate LITE work has clean engine boundaries (rocket-only seam) and doesn't block other workstreams. Full V1 inclusion case (3-4 weeks added) archived in favor of LITE.

### 5.2 BDI test-result risk

If H1-H4 fail or return mixed signal, the BDI formalism doesn't immediately operationalize. **Mitigation:** the formalism is hypothesis-grade by design (build-defining doc § 11 caveat); failure is informative, not blocking. Existing substrate composer + cohesion-judge architectures remain the baseline. Failed tests park the formalism without breaking critical-path work.

### 5.3 4-substrate cohesion-judge risk

Adding gear-archetype to P5 cohesion-judge means testing at 4-substrate scale instead of 3. **Mitigation:** per gear-substrate doc § 0.5.3, the test is "delta on top of 3-substrate baseline" — clean attribution preserved. If 4-substrate fails but 3-substrate passes, we have clean isolation of the failure mode.

### 5.4 Tier 4 catalogue authorship risk

Hand-authoring 30-50 Tier 4 keystones is substantive design work. **Mitigation:** the BDI framing (each keystone = rank-3 completer for known substrate-pair) gives the authorship an explicit structure rather than blank-page creativity. Genre canon provides reference (PoE keystone-catalogue patterns; D3 set-bonus patterns).

---

## 6. Tomorrow's first-action sequence (updated post LITE-path adoption)

Per p0-closure-note + hive-mind state evening doc, tomorrow's session begins with:

1. **Read 45-season LC-011 attribution data + babysit-summary artifact**
2. **LC-011 final disposition decision** (floor-lock vs Option C vs mixed)
3. **W1.13 dispatch fire-or-revise decision** (per FIRE-GATE § 0.0)
4. **W0.7 cumulative Gate-2 ratification** (jack-ryan + gandalf critique-pair)
5. **NEW: Protocol v1.3 fold-in** (integrate BDI + gear-substrate-LITE + Tier 4 amendments per this doc § 4)
6. **NEW: ω-table + τ-table v1 design call** (gandalf + Matt; BDI-B per build-defining doc § 10)
7. **NEW: Gear-archetype rule-table v1 finalization (G1-LITE)** (gandalf + Matt; 15-archetype rule mapping substrate-vector → gear-archetype; verify each archetype is sim-viable)
8. **NEW: Tier 4 architecture design call (T4-A)** (gandalf + Matt; hierarchy + authorship + gear coupling decisions — now informed by signature_gear_archetype being available as identity-anchor)

Items 6-8 are gandalf-Matt design pass items; can occur in sequence within a single tomorrow's session (estimated 2-3 hours total of discussion).

**Note on item 7:** the LITE-path rule-table is simpler than the originally-scoped substrate-vector composer. It's a deterministic mapping f(element, role, range, stat_distribution_signature) → gear_archetype. Tomorrow's design call locks the 15-archetype value-set + the rule logic; rocket implements the function + telemetry column as W1.15-LITE (3-5 days).

---

## 7. Cross-references

- `canonical/story/build-defining-resonance-formula-2026-05-21.md` — BDI formalism + hypothesis tests + Tier 4 rank-completer framing
- `canonical/story/gear-as-substrate-2026-05-21.md` § 0.5 — gear-substrate timing revision rationale
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 — math note (§ 4 Tier 4; § 6 substrate-as-cohesion)
- `canonical/story/p5-cohesion-judge-prompt-priorities-2026-05-21.md` — P5 prompt-engineering priorities (sharpened by BDI § 8-9)
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.2 — protocol doc (to be amended to v1.3)
- `agentic_orchestration/p0-closure-note-2026-05-21.md` — P0 closure context
- `agentic_orchestration/hive-mind-state-evening-2026-05-21.md` — evening state snapshot
- `agentic_orchestration/dispatches/2026-05-21-rocket-w1-13-skill-tree-node-population.md` § 0.0 — W1.13 FIRE-GATE
- `agentic_orchestration/dispatches/2026-05-21-legolas-substrate-as-cohesion-empirical-validation-probe.md` — probe verdict (4.35; supports resonance hypothesis at small sample)

---

**Signed:** gandalf (story-and-design steward)
**For:** clean protocol-amendment capture; tomorrow-morning fold-in to protocol v1.3; hypothesis-test pre-loading for hive-mind execution; gear-substrate V1 architectural commitment.
