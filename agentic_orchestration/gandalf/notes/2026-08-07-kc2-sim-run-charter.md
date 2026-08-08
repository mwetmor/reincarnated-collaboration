# KC2-SIM — Run Charter (autonomous; desirable-run pattern)

**Conductor:** gandalf (`RUN-CONDUCTOR`). **Chartered:** 2026-08-07, fresh per the KC2-DERIVE handoff § 2 ("this doc is raw material, not the charter").
**Launch authorization:** Matt, same session — *"ok, agreed. Go for the architecture pass and the full autonomous run."* Launch fires on the § 10 ARCHITECT gate reading clean.
**Supersedes-by-subsumption:** KC2-DERIVE (handoff `2026-08-07-kc2-derive-handoff.md`) — its probe/spec/calibration phases are Phases A–B + D here; instead of stopping at a KIT-CAL-2 charter for a later lap, this run carries **derive → build → calibrate → emit** per Matt's directive.
**Pattern authority:** `agentic_orchestration/operating-procedures/desirable-run-pattern.md` (§ 2 elements, § 4 halt taxonomy, § 5 safeties, § 6 failure-lap observations — all applied).

---

## § 0 — Intent sentence (rubric-law pin)

> The RDR battle sim runs the EoR Warlord kit through a Crucible wave-arena, calibrated against the verified fixture's measured targets, and emits a JSON baton encoding one specified run such that the following session can build the Godot presentation **from the baton alone**.

**Owner's question at exit** (the rubric every gate must trace to): *can the next session build the Godot scene from this baton alone, and does the simmed run's shape match the measured fixture?* Decomposed into G-A..G-E below; the predicate-vs-intent diff runs at G-B and any residue is named out loud (pattern § 6.3).

## § 1 — Ruling ledger (all Matt-ruled 2026-08-07, this session; veto-open)

| R | Ruling | Matt's word |
|---|---|---|
| **R-KC2-1** | Devotion = **(d)**: no proc mechanism this lap. Spec section = descriptive + **contribution envelope** computed from P-E5 templates × P-E1 cadence (uptime × magnitude, error bars stated). Baton damage is kit-native, declared in provenance. RDR receiving-surface re-grill GATED on empirical criterion: **measured proc-share in hand** (this run produces it). | "I agree with (d)" |
| **R-KC2-2** | Calibration-gate authority = **micro-oracles (both sittings' kit-internal reads) + s1 ramp (1→93, through the envelope) = BINDING**; **s2 field outcomes = INFORMATIVE** (one-sided inequality: sim kit-alone at 150–160 must clear ≤ fixture-with-turrets; faster ⇒ anomaly tripwire → finding). Split is per-measurement, not per-sitting: s2's energy 1,477/2,576 and HP-orb 20,005 BIND (attribution-clean); s2 clear times / kill rates / intake inform only (turret DPS + thinned-field second-order confound). | "ok, agreed" |
| **R-KC2-3** | Build staging = internal run sequencing (one-lap composition lean; KR informed, capacity conflicts escalate). | "I agree on … 2-3" |
| **R-KC2-4** | Dissolved: sim runs the full ladder; **binds only at fixture-data bands** (1–93, 150–160 + micro-oracles); ceiling language = U-8's measured answer, not a framing choice. | (dissolution accepted with 2-3) |
| **R-KC2-5** | 08/03 = **non-play exploratory entry** (Matt: didn't play, "just maybe looked around"). Save-consistent (map instance + .bak, zero defenses, zero deaths, +14 s). "Dialogue-miss false start" specificity STRUCK as unconfirmed. CLOSED, nothing rides on it. | "I don't recall 2-5 … just maybe looked around" |
| **R-KC2-6** | Specified-run pick = **Matt from top-3 candidate summaries at a declared checkpoint** (his one scheduled mid-run touch, Phase E). | "I agree on forks 2-6…" |
| **R-KC2-7** | Baton truth-boundary = **hybrid**: sim owns causal combat truth (who hit whom for how much when; HP + energy tracks; deaths; wave clocks; player path + circle sweep); presentation owns locomotion aesthetics within baton constraints (monster approach choreography between spawn and engagement). Final schema form ruled in-run by conductor **with drax consult**, veto-open. | "I agree on … 2-7" |

## § 2 — Substrate manifest (bounded IN; frozen at launch) + work surface

**Substrate (read-only, verified on disk at L0):**
- `agentic_orchestration/legolas/notes/2026-08-05-eorwarlguts-save-parse.md` (identity 99.97%; regime; format corrections; EoR ALLOCATED-15 vs TOTAL-26 scale note § 2.5)
- `agentic_orchestration/gandalf/notes/2026-08-05-eor-ceremony-cross-verification.md` (envelope +3.9%/−0.5%; grimtools-on-camera)
- `agentic_orchestration/legolas/notes/2026-08-01-eor-endgame-build-of-record.md` (§ 1.4–1.7 build spec, `b28gD0KN`)
- `agentic_orchestration/gandalf/notes/2026-08-01-eor-warlord-playtest-directions-v3.md` (PART II gap table § II.2; probe queue § II.4; § 5-AFTERMATH corrected 2026-08-05)
- `agentic_orchestration/legolas/notes/2026-08-01-gd-pack-density-ranking.md` (dense-room targets; .arz extraction pattern lineage)
- Footage: **`/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-1/`** (s1: 41.6-min video + 142 screenshots) + **`eor-test-2/`** (s2: 17.2-min video 1,034 s 1920×1080@60 + ceremony screenshots #495–611). *(Handoff path `matt-notes-from-pc/GD-matt-test/` corrected at L0.)*
- Save: `/Volumes/reincarnated/matt-notes-from-pc/gd-save/_EoRWarlGuts/` (SHA-verified; `player.gdc` = `b8e6f510…`)
- Edition-II `.arz` corpus: **`~/Games/vendor/grim-dawn-edition-II-20260724/`** (join-safe at client 1.3.0.5 per patch-delta probe; werewolf family = declared confound). *(CORRECTED in-run at Phase A per P-E5 return: the charter's original pin `~/Games/vendor/grim-dawn/` is the Edition-I tree — no GDX3, hence no Oathkeeper/EoR records. Ledger § A.2; each probe return verifies its corpus provenance.)*
- Claim vocabulary in force: *name-identical; derived within +3.9%/−0.5%* — "matches 100%" retired. Parse-over-frames governs. M1 (Lokarr fixed offers {50,100,150,180}) ≠ M2 (death−20↓10 rewind) — never blurred.

**Work surface (NOT frozen — the thing being built):** `~/Games/reincarnated-engine/` main, at launch HEAD **`ebf13240`** = gap-table basis `28eddef4` + 2 BR-2 shape-truth commits (nova=sixteen-corridors; `shape` semantics on two families). **G-B obligation:** re-verify the § II.2 BUILD/EXTEND rows against launch HEAD — the gap table was measured at `28eddef4`.

## § 3 — Phases and gates

| Phase | Work | Executes | Gate |
|---|---|---|---|
| **A — probes** | P-E1 spin cadence/radius/drain · P-E5 devotion→proc-template join (7 bindings) · U-8 tier→wave map + ceiling (TIER18=180 anchor; M1 offer-set edge) · U-9 `spawnMinModifier` operator order · **P-E6** Crucible wave-composition tables · galadriel: banner ID + per-wave clear-time timelines (both sittings, attempts labeled) · **P-X1** emission-format inventory (recon, evidence-only) | legolas ×5, galadriel (background, named); Explore recon | **G-A:** each probe LANDED or fallback-declared with provenance grade; U-8/U-9 closure state DECLARED |
| **B — spec** | One section per § II.2 row, DB-cited (EoR cited at **TOTAL 26**): channel state machine BUILD · moving circle BUILD · energy drain EXTEND (vs 1,477/2,576) · RF charge-stacks EXTEND · auras EXTEND (Divine Mandate exclusive) · pack opposition COMPOSE (on Lane-2 machinery at HEAD) · block PARAMETERIZE (likely dissolves — 2H) · retaliation EXCLUDED · devotion envelope (R-KC2-1) · **Crucible encounter spec** (wave engine; composition per P-E6/U-8/U-9; simplified run-control: start-wave parameter + single life — no M1/M2 fidelity, declared; **no defense structures**, declared) · **baton schema spec v1** (star-lord consult; truth-boundary per R-KC2-7 with drax consult; **drax signs the coverage list before build**) | named-gandalf SPEC-AUTHOR drafts; conductor folds | **G-B:** every row DB-cited or named-HALT · schema consumer-signed · **tolerances PINNED** from Phase-A instrument data · intent-diff run, residue named |
| **C — build** | Mechanism stack in `simulation/` (gamora): channel machine + moving circle → energy/RF/aura extends → pack opposition + wave engine. Baton emitter in `export/` (star-lord) against schema v1. Conductor writes **zero production code**. | gamora laps; star-lord | **G-C:** gamora tests green + **jack-ryan Gate-2 PASS** on the seam work |
| **D — calibrate** | Order: micro-oracles (direct-binding) → s1 ramp through envelope (BINDING) → s2 inequality (INFORMATIVE tripwire) → full-ladder runs beyond fixture bands (reported, unbound) | gamora batch runner; conductor judges | **G-D:** BINDING rows within pinned tolerance, else Gate-B-of-Run-A pattern (diagnose → DB-cited correction or FINDING → severity rule § 5) |
| **E — specify + emit** | Seeded batch (N seeds × start-configs {wave-1, checkpoint-150}) → pre-registered selection criteria (§ 4.5) → **top-3 summaries → Matt picks (R-KC2-6)** → baton emitted: full-run truth + provenance block (calibration grade · envelope disclosure · U-8/U-9 state · sim/spec/seed pins) + **handoff note for the Godot session** | conductor + star-lord | **G-E:** schema-valid · **consumer-stub round-trip green** · coverage checklist 100% vs the drax-signed list · provenance complete · committed |

## § 4 — Pre-registered rules

1. **Tolerance pinning (informed goalposts):** numeric tolerances for G-D are pinned at **G-B close**, from Phase-A instrument data (galadriel's timing noise floor + probe precision), **before any build begins.** Goalposts precede results; they do not precede knowledge of instrument noise.
2. **No free-parameter fitting:** calibration adjustments are limited to DB-cited corrections (a demonstrably misread value). A fit failure beyond correction is a FINDING — the run may never tune the sim to match the fixture. An abstraction-mismatch finding (sim's combat model diverges structurally from GD's) is an honorable, valuable outcome: it quantifies the sim's abstraction gap.
3. **Coverage before accuracy (KIT-FIDELITY inversion):** the consumer (drax) signs the baton coverage list at G-B, before the emitter exists; G-E proves round-trip consumability by stub, not emission-by-assertion.
4. **Probe fallbacks (pre-declared):** P-E1 parameters engine-side-not-DB → footage-derived estimate, provenance ESTIMATED. U-9 undecidable from DB → external corroboration with provenance grading; still red → monster-count claims carry PARTIAL provenance and the DPS-join rows drop to INFORMATIVE (run continues). P-E6 partial → compose what is DB-resident, declare gaps. Banner ID unresolvable → "Vanguard-likely, unconfirmed" (affects informative-weight only, per R-KC2-2).
5. **Selection-criteria classes for Phase E (thresholds pin at G-D close, before the batch fires):** mechanism coverage (channel uptime, RF stacks, aura active), narrative shape (a clear-rate inflection/wall inside the run; death or cash-out ending), band relevance (reaches the 150–160 showcase band under some start-config), technical cleanliness (zero anomaly flags).
6. **Namespace guard:** the baton is a **run-trace artifact**, versioned `baton/v1` — it does not squat the season-bundle `encounters` key reserved by Lane-1 (T3-V7 braid law). P-X1 maps the existing emission formats so the baton extends `export/` machinery, never a parallel format.
7. **Commit centralization:** Phase-A agents write notes but do NOT commit (interleave guard, OP § 4.10 composition note; named deviation from the handoff sketch's "each commits its own note"). Conductor commits at each gate close = the run-memory beat. Engine-side build commits are gamora's own (seam discipline + tag conventions).

## § 5 — Halt taxonomy (run-specific)

**Commitment-boundaries — HALT to Matt:** the Phase-E pick (R-KC2-6, scheduled) · any NEW player-experience-defining design surface beyond the gap table (e.g., a monster-AI grammar fork surfacing during pack-opposition work) · jack-ryan Gate-2 BLOCK · decisions-log contradiction · BINDING miss > 2× pinned tolerance after DB-cited correction attempts (structural finding → halt-or-fallback is Matt's word) · push to remote.
**Reasoning-boundaries — conduct rules in-run, veto-open ledger:** spec-content choices (DB-cited) · schema final form (R-KC2-7, with drax consult) · selection-criteria application · gate diagnoses + finding reclassifications · internal sequencing · probe-fallback invocations per § 4.4.

## § 6 — Matt interface (declared)

One scheduled touch: the **top-3 pick** at Phase E. Otherwise red-flag pings only (the § 5 commitment list). Every in-run ruling lands in the run-state ledger veto-open — one word reverses. Push to remote: end-of-run, Matt's word. Phase-boundary fold notes are the run's readable progress reports.

## § 7 — Honorable fallback (a PASS at fallback grade)

Mechanisms built + Gate-2 passed + calibration deltas published as findings + baton emitted with `calibration_grade: PARTIAL` + holes named + queue rows filed. The Godot session can still build from it — a scene needs internal coherence more than fixture-exactness, and the provenance block tells the truth about what it stands on.

## § 8 — Run-memory protocol

Each gate close = a committed fold note (`agentic_orchestration/gandalf/notes/2026-08-XX-kc2-sim-<gate>.md` or delta-block equivalent) + run-state ledger update. On ANY session resumption or post-compaction turn: charter-freshness gate re-fires (role def + OP § 2 + pattern doc + THIS CHARTER from disk). Disk governs.

## § 9 — Seam routing + lane composition

Named agents only (OP § 4.10): legolas probes · galadriel extraction · named-gandalf spec drafts · gamora mechanisms · star-lord emitter · jack-ryan Gate-2 · drax consulted (coverage sign + truth-boundary), **not building** (his Godot build is the NEXT session, fed by the baton — presentation surfaces get Matt's eye natively there, per pattern § 6.2).
**KR interface:** this charter's commit is launch notice; gamora/star-lord capacity conflicts escalate to KR; closeout summary at run end.
**Tier-3 / Q42 composition (L0-reconciled):** the § II.2 gap table was measured 08-01, AFTER both KR lanes fired — verbs already reflect lane state. Pack opposition COMPOSES on Lane-2 arena/horde machinery at HEAD; Tier-3 W2 red-flag routing into sim spec is honored; KC2-SIM delivers the calibrated single-kit + wave-engine truth that Tier-3's fit layer later consumes. No double-build.

## § 10 — ARCHITECT gate record (open-questions pass)

`▶ ROLE: ARCHITECT — run-authorization boundary; every decision the run will hit, classified`

| Decision | Class | Disposition |
|---|---|---|
| Devotion mechanism scope | **RESOLVED** | R-KC2-1 (d) |
| Devotion RDR receiving surface | **GATED+TRACKED** | empirical criterion: measured proc-share (this run produces it); re-grill after; tracker row carries it |
| Calibration authority | **RESOLVED** | R-KC2-2 |
| Build staging | **RESOLVED** | R-KC2-3 internal |
| Ceiling framing | **RESOLVED** | R-KC2-4 dissolved → U-8 measured answer |
| 08/03 accounting | **RESOLVED** | R-KC2-5 closed |
| Specified-run pick | **RESOLVED** | R-KC2-6 mechanism (Matt at checkpoint) |
| Baton truth-boundary | **RESOLVED** (mechanism) | R-KC2-7: in-run, drax consult, veto-open |
| G-D tolerances | **GATED+TRACKED** | § 4.1 pin at G-B from Phase-A data |
| U-8/U-9 closure | **GATED+TRACKED** | Phase A; § 4.4 contingencies pre-registered |
| Banner ID | **GATED+TRACKED** | galadriel; informative-weight only |
| Baton schema form | **GATED+TRACKED** | G-B drax sign + R-KC2-7 |
| Block row disposition | **GATED+TRACKED** | G-B (likely dissolves — 2H) |
| Defense structures in sim | **RESOLVED** | excluded, declared simplification |
| M1/M2 run-control fidelity | **RESOLVED** | simplified start-wave + single life, declared |
| Retaliation | **RESOLVED** | EXCLUDED per gap table |
| Selection thresholds | **GATED+TRACKED** | § 4.5 pin at G-D close |
| Engine HEAD drift | **RESOLVED** | pinned `ebf13240`; G-B re-verify obligation |
| Tier-3/Lane overlap | **RESOLVED** | § 9 composition declaration |
| Werewolf-family confound | **RESOLVED** | declared; P-E6 flags if werewolves appear in Crucible composition |
| Push | **RESOLVED** | Matt's word at end |

**Verdict: zero OPEN Matt-gated forks. Gate CLEAN → LAUNCH AUTHORIZED** (Matt's pre-authorization applies: "Go for the architecture pass and the full autonomous run").

---

**Signed:** gandalf, `RUN-CONDUCTOR`, 2026-08-07. The forks are drained, the goalposts precede the results, and the run ends at verified consumability — not at emission.
