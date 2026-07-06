# Demo-Readiness Unattended Run — Spec

> **STATUS:** SPEC — CURRENT (Matt-ratified grill G1–G10, 2026-07-03). **Author:** gandalf (SPEC-AUTHOR). **v1.2** (jack-ryan, 2026-07-06): criterion C hygiene strikes — `ProxySpawn` lift + "2026-06-24 ratification" refs removed (§1-C + §3 W3 step 1); C's satisfaction path re-pointed at the Option-1 batch-2 build (Matt-ruled 2026-07-06). See decisions-log `2026-07-06: W3 summoner emission — Matt rules Option 1`.
> **Gate-1:** ✓ PASSED-WITH-AMENDMENTS 2026-07-03 — jack-ryan DESIGN-MODE (2 BLOCK + 4 AMEND + 2 NOTE, **all folded — v1.1**) + gandalf DRIFT-CRITIC self-audit. Record: §11.
> **Authority chain:** `proxy-t4-suite-spec-2026-07-02.md` v3 · `proxy-pairing-q6-q7-2026-07-02.md` v2 (RATIFIED — Phase-3 authority: partition · 65-pair matrix · 14×3 pools · P1–P7 · rules i–vi) · `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` (D.1 queue) · `agentic_orchestration/gandalf/notes/2026-07-02-kr-relay-b1-rebase-fire-order.md` + addendum · Matt rulings §2 (this doc).
> **Objective (Matt 2026-07-02, verbatim):** *"plan a comprehensive overnight run so that the engine and content emission pipeline are both 100% ready for the Demo."* Demo work (hero-rig Q7, camera Q8, the vertical slice) opens AFTER this run, from a real registered bundle.

---

## §1 Definition of done (acceptance criteria)

| # | Criterion |
|---|---|
| **A** | **One callable driver** emits all six content types (kits / monsters / factions / gear / weapons / flavortext) into a single Godot-consumable bundle — serial D.1 #1 assembly driver, with the `proxies` landing key present. **Supersedes the one-realm §5.1 hand-join** (dead — do not execute the stale ask). |
| **B** | **Zero hollow spots** in the emitted bundle: no NULL `flavor_text`, no NULL `main_weapon`, no NULL names; monsters + gear pool + factions actually written. (Serial PART B's hollow-spot list, inverted, is the checklist.) |
| **C** | **Summoner un-gate executed**: `_DEFERRED_PROXY_BINS` lifted and the emission fires with proxy bins + the T4 suite + the pairing layer (G1) live. **Export-hold satisfied:** Matt's G-rulings (2026-07-03) authorize this emission exercise — the `export/MIGRATION.md` v1.81-1.82 hold's first Matt-authorized exercise. **v1.2 hygiene strikes (jack-ryan 2026-07-06):** the `ProxySpawn` lift reference is STRUCK — `ProxySpawn` (`mechanic_alteration.py:46`) is a docstring reference to the register Matt RETIRED 2026-07-02; there is nothing to lift. The "both Matt-ratified 2026-06-24" clause is STRUCK — no provenance for a 2026-06-24 ratification exists in the engine tree. **C's satisfaction path is Option-1 batch 2** (Matt-ruled 2026-07-06): the summon gen-path build + re-fire; the structural-gap finding is `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md` (RESOLVED). |
| **D** | **Full-spectrum scale (G2)**: thousands of candidates (samples-per-cell raised; mechanism seam-owned — one wide run or several registered batches), gauntlet-filtered to the in-band survivor set. Estimated 100–400 in-band; *"may be substantially less"* (Matt) — **the count is a measured output, not a promise.** Pilot beat (§4) sizes the run. |
| **E** | **Composition target (G4)**: ~25% of emitted kits proxy-dominant, targeted at generation and **confirmed post-hoc by hypothesis test** with measured-composition tagging (§5). |
| **F** | **Run(s) registered** — minimal run registry (serial D.1 #8): run_id · timestamp · config hash · bundle path · gauntlet summary · cert status. **star-lord drafts the schema, jack-ryan ratifies — no Matt gate (G9).** Lands the "callable → registered" stages of the staged-pipeline direction. |
| **G** | **Verified**: gandalf DRIFT-CRITIC bundle-vs-spec audit + jack-ryan Gate-2 QA + **curation shortlist** (rubric §8) ready for Matt's demo-roster pick (G7). |

**Readiness split:** engine-ready = W0 + W2 (calibration sweeps certified, pairing layer live). Pipeline-ready = W1 + W3 (driver + wiring + one registered fully-flavored full-spectrum bundle). Verified = W4.

---

## §2 Rulings register (Matt, 2026-07-03)

| # | Ruling | Resolution in this spec |
|---|---|---|
| G1 | **(a)** — pairing layer rides the run | W2; mandatory degrade path (§7): W2 stall → W3 fires singleton-only, never halts the emission |
| G2 | **Full spectrum** — *"Why not run the full spectrum of combinations (thousands, likely driven down to 100-400 in band kits; estimation, may be substantially less)?"* | Adopted; supersedes the two-batch framing. §4: pilot sizing beat + flavor-only-survivors ordering. Doubles as the first empirical measurement of the engine-tracker III.4 [MEASURE] pair (per-kit wall-clock + in-band yield) |
| G3 | **No cap** — ~$50 in the key; errors out when empty | Survivors-only LLM ordering retained (correct regardless of cap); spend logged per pass |
| G4 | **No new resource** — proxy kits are caster-subset (mana pool); select ~25% of kits for proxy-dominant trees (+ proxy-focused T4); hypothesis test + post-hoc tag | Necro-energy B4 prereq → **no-op**. New items: rocket composition knob (W0) + gamora hypothesis test & tagging (W4). §5 |
| G5 | **Propagate-now** (gear-as-power lean), conditional on D3-confidence — answered: D3 = build-floor cert on fixtures vs both boss shells; population confidence via per-kit balance-loop + gauntlet gate | DDA propagation ON for this run, **re-certified by a W0 single-parameter sweep** (Disc #24) before W3; bundle carries the `proxy_scaling` contract for Godot; launch study refines the inheritance model. §6 |
| G6 | **Supersede** (default written in; Matt may veto in passing) | B3 backfill dies: the ~60 null-name gear stubs + unapplied weapon descriptors are marked non-canonical, never ship; B3's live remainder = the W1 wiring itself + curation rubric on new output |
| G7 | **(a)** — Matt picks the roster; *"the more kits emitted in band with passing KPM, the more options"* | Tiered shortlist (§8) + full in-band table; composes with G2 scale |
| G8 | **Agreed** — halt-loud with the W2-degrade asymmetry | §7 |
| G9 | **Confirm** — registry schema delegated | star-lord drafts, jack-ryan ratifies (criterion F) |
| G10 | **Yes** — Binder spec authored in the run window | §9 |

---

## §3 Wave plan

> Every row carries a `gates-on:` token (fork-4, Matt-ruled 2026-07-02) — KR carries these into dispatch headers + board rows. **Semantics (Gate-1 #3 fix; carries into the Glance contract):** `gates-on: X` = *this row fires only after X closes* — dependents declare their dependencies; the inverse ("unblocks") is never encoded. Deadlock-proof under a literal reader.

### W0 — Prereqs (rocket · gamora · star-lord) — `gates-on: —`

| Item | Owner | Notes |
|---|---|---|
| B4 prereq re-scope | star-lord | Necro-energy = **RESOLVED no-op** (mana, caster-subset — G4). Remaining: export DDA-lock widen + F-f enforcement consumer. KR pins exact scope at dispatch from its closeout rows. `gates-on: —` |
| **DDA propagation sweep** | gamora | Single-parameter flip (propagation ON), math-note-first, D3 fixtures + method carry; re-earn the build-floor cert with propagation live. Double-dip degeneracy → halt-loud with finding, ship (b)-config (§6). `gates-on: —` |
| **Proxy composition knob** | rocket | Generation-side weighting for the ~25% proxy-dominant target (mechanism rocket's: bin weights and/or proxy-skill weighting across the caster family). `gates-on: —` *(feeds W3 + §5)* |
| **2-type proxy-decl check** | rocket | Named prerequisite from the B1 fire order: generation must EMIT exactly-2 cross-family proxy decls or CONVERGENCE kits cannot exist in the run. If it cannot: **file loud as a named gap, no silent skip.** `gates-on: —` *(feeds W2)* |
| CONVERGENCE cert fixture | rocket | The 2-summon-skill kit as **FIXTURE only** (zero-hand-authored-content: never ships; shipping CONVERGENCE kits come from the emission run). `gates-on: —` *(feeds W2)* |
| proxy_type→family classifier | rocket | Phase-3 residual (14 types → 6 families per the pairing-spec partition). `gates-on: —` *(feeds W2)* |

### W1 — Pipeline completion (star-lord) — `gates-on: —`

Serial D.1 rows, verbatim scope: **#1** assembly driver (all six types, one bundle, `proxies` landing key + stage-2 run record) · **#3** faction block wiring (built + validated — wire it) · **#4** weapon descriptor wiring (built + validated — wire it) · **#5** gear-pool writer into the bundle (B2 landed gear_pool 0→150) · **#2** flavor-call wiring (`name_monster()` MUST · `name_skill()` flavor_text · `name_gear_item()`) · **#8** minimal run registry — **sequenced (Gate-1 #5):** star-lord drafts the schema → jack-ryan ratifies at the **W0/W1 boundary** (fast pass; Discipline #8 schema-at-boundary — ratify BEFORE the writer builds against it, not at W4 after two waves already wrote) → THEN the writer builds · **+ mark the superseded ~60 null-name gear stubs non-canonical (G6)**.

### W2 — Pairing layer (rocket → gamora) — `gates-on: W0.classifier · W0.2-type-decl-check · W0.fixture` *(degrade path §7)*

CONVERGENCE + DUAL_PROXY strategy classes + 65-pair matrix + 14×3 pool wiring per the **ratified pairing spec** (its full authority: partition · matrix · pools · P1–P7 · derivation rules i–vi, incl. (v) labeled inheritance + (vi) single visual identity) → gamora cert (the A2/A3/A5/A6 method from the B1 re-cert carries; seeds 53M+; Disc #18/#24 discipline). Phase-1/2 precondition **met** (B1-REBASE closed: `40e351e` + `67fc0a9`). Design-OPEN — no Matt gate; **Gate-1 critique-pair on the dispatch** per MASTER protocol before fire.

### W3 — THE EMISSION RUN (star-lord + rocket) — `gates-on: W0(all) · W1(all) · W2(soft — §7 degrade) · singleton-smoke-green · registry-schema-ratified`

**Preconditions (hard, Gate-1 #2/#5):** singleton-config smoke green + registry schema ratified.

1. **Un-gate**: lift `_DEFERRED_PROXY_BINS` (`bc_target_composer.py:97,318`); correct the stale reason-string. *(v1.2, jack-ryan 2026-07-06: the `ProxySpawn` lift reference is STRUCK — `mechanic_alteration.py:46` is a docstring reference to the register Matt RETIRED 2026-07-02; nothing to lift. The proxy-bin lift alone composes hollow kits until the summon gen-path exists — see criterion C's Option-1 batch-2 path.)*
2. **Pilot beat** (§4): first ~20 candidates → measure per-kit wall-clock + convergence yield → project → size samples-per-cell to the run window.
3. **Full-spectrum emission**: thousands of candidates, all six content types, T4 suite + pairing layer (per W2 state) + proxy bins live.
4. **Gauntlet filter**: recompose-first balance loop + ≥9/18 criterion per kit → the in-band survivor set.
5. **Flavor passes — split by content class (Gate-1 #4)**: **kit-identity flavor on gauntlet SURVIVORS ONLY** (G2/G3 ordering — failed candidates never bill); **monster / gear / faction flavor keys off bundle-membership** (written once at assembly — these aren't gauntlet-filtered content, so survivor-gating them would strand criterion B on a W3 partial). All calls per-item → resumable, no double-billing on retry.
6. **Bundle assembly + register** (criterion A/B/F).

### W4 — Verify + curate-prep (gandalf · gamora · jack-ryan · KR) — `gates-on: W3`

DRIFT-CRITIC bundle-vs-spec audit (checklist = criterion B + the six-type matrix + the pairing-spec derivation rules; **six-type presence = a mechanical assertion — key-present + non-NULL count per type — never a read-through** (Gate-1 #7)) · jack-ryan Gate-2 QA · **G4 hypothesis test + post-hoc `proxy_dominant` tagging** (gamora, math-note-first; §5) · **proxy-T4 offer-table verify** (every proxy-dominant kit's η offer table carries ≥1 proxy-focused T4) · curation shortlist (§8) · tracker/board updates with `gates-on:` tokens.

---

## §4 Scale + cost engineering (G2/G3)

- **Mechanism seam-owned**: one wide run or several registered batches — rocket/star-lord pick; all batches register (criterion F handles either).
- **Pilot sizing beat is mandatory** (measure, don't assume — the per-kit balance-loop wall-clock at scale is the one unverified load-bearing quantity in this spec; see §11 framing audit). First ~20 candidates → project → size.
- **Yield honesty**: the in-band count is an output. Report actuals; no fake precision. This run IS the first empirical measurement of engine-tracker III.4's [MEASURE] pair.
- **LLM ordering**: identity/flavor only post-gauntlet. Projection at 400 survivors ≈ $10–20 total (kit identities + monsters + gear + factions). Key ≈ $50; error-out = natural cap (G3). Log spend per pass.
- **Near-dupes at high N are acceptable this run** — curation ignores them; the distinctiveness ceiling is a launch concern (III.4: 300-sharp beats 400-with-reskins).

## §5 Composition targeting + hypothesis test (G4)

- **Target**: ~25% of emitted kits proxy-dominant (the ARPG summoner share Matt named). Rocket owns the knob (W0); the target steers generation — it does not hard-gate emission.
- **Post-hoc tagging (substrate-led)**: gamora classifies each emitted kit's *actual* skill-tree composition (proxy-skill weight share) and applies `proxy_dominant: true/false` **from measured composition, not from intent** (Discipline #41 spirit).
- **Hypothesis test**: measured share vs ~25% target; math-note-first; report the actual with confidence interval. If the knob under/overshoots, the finding (not a silent re-run) comes back — retuning is a named follow-up, not an unattended loop.
- **T4 linkage**: proxy-dominant kits must be *eligible* for proxy-focused T4s (SOVEREIGNTY / FISSION / ZONE_CONTROL / CONVERGENCE / DUAL_PROXY per family gates); W4 verifies ≥1 in each such kit's η offer table. (PROXY_INVERSION stays deferred-by-ruling — η never offers it.)

## §6 DDA propagation (G5)

- **Ruling applied**: propagation ON for this run (Matt's gear-as-power lean — the D3-vanilla lesson: pets that don't scale with power fall out of band; RoS fixed it with full stat inheritance).
- **Guard (sharpened by Gate-1 #1 — the load-bearing catch):** the D3 cert baseline was derived with the proxy `damage_modifier` **hard-coded to 1.0** (`proxy-fight-calibration-2026-07-02.md:72,77`) — proxy DPS received ZERO player-power scaling in the certified fixtures. The propagation flip therefore establishes a **NEW build-floor, not a re-earn of the old one** (the killing-blow arithmetic changes). The W0 sweep accordingly: (i) derives the propagation-live floor (fixtures + D3 method carry; boss anchor dm 5.0 @ 4.5s / swarm 0.20 must hold by construction); (ii) **RE-CERTIFIES `demo_bone_acolyte` + `demo_crypt_lieutenant` against that floor as an explicit acceptance gate** — a floor-regression on either is a halt-condition, same standing as degeneracy. Either failure → halt-loud with the math-note finding; run proceeds (b)-configured (the still-certified 1.0 baseline) with the finding attached for Matt.
- **Emission contract**: the bundle carries the `proxy_scaling` flag explicitly so Godot realizes summoner power growth; the launch-track study refines the exact inheritance model (percent inheritance vs minion-specific channels — the PoE-minion-tree question) later.

## §7 Failure policy (G8)

| Failure | Response |
|---|---|
| **W2 (pairing) stalls** | **Degrade**: W3 fires singleton-only. **Concrete config (Gate-1 #2):** Phase-1 η members live (ASCENSION / SOVEREIGNTY / FISSION / ZONE_CONTROL); CONVERGENCE + DUAL_PROXY η-gated to 0.0. **This config is smoke-tested green BEFORE W3 fires, regardless of W2 state** — an unattended run may not discover mid-flight that "pairing OFF" was never an executable state. Still demo-ready (both certified melee summoners + full singleton T4 suite). CONVERGENCE/DUAL land as a named follow-up. |
| W1 wiring / W3 flavor failure | One retry → **halt the wave loud + park**. A NULL-riddled bundle is NOT readiness — emitting it would fake criterion B. |
| Pilot projects past the run window | Size down to widest-feasible config; report the projection + chosen config. |
| DDA sweep degeneracy OR demo-summoner floor-regression | Ship (b)-config (the still-certified 1.0 baseline) + finding (§6). |
| LLM key exhausts | Natural halt (G3); registered partial state + spend log; flavor resumes on refill (calls are per-item — resumable, no double-billing on survivors already named). |
| Anything else | Halt-loud per engineering disciplines; park state; never silent-skip. |

## §8 Curation rubric (G7 — Matt picks)

Shortlist: **tiered top ~20–30** + the full in-band table (sortable by KPM band-position / element / archetype). Mandatory rows: both certified melee summoners (`demo_bone_acolyte`, `demo_crypt_lieutenant`) · ≥1 CONVERGENCE kit (G1, if W2 lands) · element spread · archetype spread · **summoner share of the final roster ≈ the G4 percentage** (2–3 of 8–10) · name/flavor quality (the demo's face) · **no ranged summoners** (the `demo_gravecaller` nav-gap deferral stands — launch-track fix).

## §9 Run-window parallel authoring (gandalf — not run-gating)

1. **Label→glyph mapping spec** (engine-tracker III.8, the one MVP-CRITICAL PART-III item — drax consumes at the Goldilocks fork UI; Discipline #41: map to emergent clusters, don't pre-impose).
2. **Glance contract spec** (incl. the `gates-on:` token convention as a format-law amendment — gandalf proposes, jack-ryan ratifies per canonical-doc-format §6.7).
3. **Binder spec** (G10 — asset registry + binding rules + resolved manifest; ready when demo work opens).

## §10 Out of scope (explicit)

Q7 hero-rig retarget · Q8 camera G3 sign-off · the vertical slice (all open the demo phase AFTER this run) · Goldilocks matchup matrix (III.1) · horde density (III.3) · per-kit level model (III.2) · hundreds-scale *tuning* (III.4 — this run measures, doesn't tune) · Glance *build* (contract first) · B3 backfill (superseded, G6) · ranged-summoner nav fix (launch) · PROXY_INVERSION (deferred-by-ruling) · precise proxy-share fine-tuning (launch — this run targets + measures).

## §11 Gate-1 record

**gandalf DRIFT-CRITIC self-audit (framing audit Q1–Q3):**
- **Q1 load-bearing assumptions**: (i) samples-per-cell scales without architecture change — supported by the substrate-led no-pre-imposed-N language (`season_generation_pipeline.py:41`) + ~2,293 active substrate rows; (ii) **per-kit balance-loop wall-clock at thousands-scale — UNVERIFIED** → the pilot beat is the guard, and W3 cannot skip it; (iii) flavor passes are per-item and resumable — KR/star-lord verify at dispatch; (iv) D3 constants + propagation flip compose — the W0 sweep gates.
- **Q2 refuting evidence in hand**: none refuting; (ii) is the honest hole and is guarded, not assumed away.
- **Q3 refine vs execute**: refined already — pilot beat + degrade paths exist *because* of Q1(ii).

**jack-ryan DESIGN-MODE pass (2026-07-03): PASS-WITH-AMENDMENTS — all eight findings folded same-day (→ v1.1):**

- **#1 [BLOCK → §6]** D3 cert was derived with `damage_modifier` hard-coded 1.0 → the propagation flip creates a NEW floor; both demo summoners re-certified as an explicit gate; floor-regression = halt-condition. *(The load-bearing catch — my Q1(iv) said "the W0 sweep gates" but under-specified WHAT it must re-certify.)*
- **#2 [BLOCK → §7]** singleton degrade config named concretely + smoke-gated before W3, regardless of W2 state.
- **#3 [AMEND → §3]** `gates-on:` semantics defined (dependents declare); all tokens rewritten; the definition carries into the Glance contract spec.
- **#4 [AMEND → W3.5]** kit flavor survivor-gated; monster/gear/faction flavor bundle-membership-keyed; per-item resumability stated.
- **#5 [AMEND → W1 #8]** registry schema ratified at the W0/W1 boundary, before the writer builds against it.
- **#6 [AMEND → pipeline]** batched decisions-log registration (G1–G10 + the proxy-T4 four rulings + the Q6/Q7 six rows) precedes KR dispatch authoring — jack-ryan's write, his seam; routed via the KR relay.
- **#7/#8 [NOTE → W4 / §9 affirmed]** six-type check mechanical; §9 authoring stays off the critical path (KR: not a wave dependency).

---

**Pipeline from here:** Gate-1 ✓ passed + folded (§11) → **jack-ryan's batched decisions-log registration lands** (G1–G10 + proxy-T4 four rulings + Q6/Q7 six rows — Gate-1 #6; the run must not fire against rulings living only in spec headers) → **KR authors the wave dispatches** (this spec is the single authority they cite; `gates-on:` tokens carried under the §3 semantics) → **fire the unattended run** → W4 returns land the curation shortlist + hypothesis-test findings + registered bundle → **demo phase opens** (Q7 King Rig · Q8 camera · the slice — `gates-on: W4`) from a real bundle.

**Signed:** gandalf, 2026-07-03 (SPEC-AUTHOR), against Matt's G1–G10 rulings, same session. **v1.1** same-day: Gate-1 folds complete (jack-ryan DESIGN-MODE PASS-WITH-AMENDMENTS; findings #1–#8 all dispositioned in-spec).
