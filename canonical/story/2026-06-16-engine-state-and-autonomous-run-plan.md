# Engine State + Autonomous Run Plan — 2026-06-16

> **STATUS:** CURRENT (load-bearing as of 2026-06-16) — see `canonical/00-ground-state.md`. This is the session-boundary state snapshot + the authorized autonomous-run plan. Re-entry doc for the next session.

**Date:** 2026-06-16
**Author:** gandalf (story-and-design steward)
**Status:** v1 — state snapshot + run plan. T4 capstone design COMPLETE; pre-authorization envelope ratified.
**Authority:** Matt 2026-06-16 — ruled Q8 Path Pure ("Good reframe. Let's go with path pure."), confirmed the three-tier pre-authorization envelope + Option 1 + wave-close push policy ("Confirm the envelope and Option 1, write the doc").
**Companion docs:**
- `canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` — the cert wave (W-A…W-F); RESOLVE/MEASURE split.
- `agentic_orchestration/cert-wave-2d-W-D-close-2026-06-13.md` — W-D close + D1–D6 dispositions.
- `agentic_orchestration/gandalf/notes/2026-06-15-telegraph-dispatch-3-gate-phase-ruling.md` — dispatch 3 fires at W-C RESOLVE-clear (GO).
- `canonical/story/2026-06-13-companion-as-hall-of-heroes-ally-commitment.md` — T4 companion layer; Path Pure ruled (v1.1).
- `agentic_orchestration/gandalf/notes/2026-06-13-q8-companion-convergence-matrix-FINAL.md` — Q8 68-cell matrix.
- `agentic_orchestration/skill_handoff_2026-06-15.md` — rogue arc close (b6 Decision 2 HELD; Option 1/2 fork).

---

## 0. TL;DR

1. **T4 capstone design is COMPLETE.** Q1–Q10 all ratified; the last open question (Q8 season-1 bootstrap) ruled **Path Pure** 2026-06-16. No T4 design work remains.
2. **The engine frontier is clean and nothing is in motion** — a good launch point for an autonomous run. W-D (six-axis MEASURE) CLOSED 2026-06-13; the cert critical path (W-E throughput) has not started; the telegraph wave is parked, not running.
3. **Two completion-blocker lists** (§ 3, § 4) name exactly what remains for (A) a commit-grade battle sim and (B) a complete end-to-end pipeline. **The keystone, on both lists, is the representative-loadout fix** — kits are currently measured stripped of ~60–70% of their real loadout (0 skill investment + synthetic gear). It is upstream of *trustworthy* 1D-deletion and b6-deletion.
4. **The autonomous run is authorized** (§ 5) on a three-tier pre-authorization envelope: additive work runs fully-gated; destructive deletions fire on pre-registered clean criteria; only ambiguity parks for Matt. Plus Option 1 (the bounded b6 composition investigation) and wave-close push authorization.

---

## 1. T4 capstone design — COMPLETE

The T4 capstone design arc (Q1–Q10, the 25-strategy catalog, the Q6/Q7 convergence/bridge matrices, the Q8 companion-convergence matrix) is **closed.** Final ratifications:

| Question | Disposition | Ratified |
|---|---|---|
| Q1–Q5 | Mechanic locks (mana shield / chain count / DDA retirement / GEOMETRY_COLLAPSE / RESOURCE_CONVERSION) | 2026-06-12 |
| Q6/Q7 | Proxy-convergence (33 pairs) + dual-proxy pools (14); **both bridge types ratified co-equal** — Golem (aggregative, go-wide) + Baby Good Mimic (replicative, go-deep) | 2026-06-15 |
| Q8 | Companion-convergence matrix (68 valid cells of 625); companion = Hall-of-Heroes ascended form; convergence item = shared-season bond between two past selves | 2026-06-13 |
| Q8 season-1 bootstrap | **Path Pure** — season 1 fights solo; companion layer activates season 2 when the first molt returns | **2026-06-16** |
| Q9/Q10 | Ratified | 2026-06-12 |

**Path Pure consequences (locked, per the commitment doc § 7):** season-1 onboarding does not teach the companion system (there is no companion); the 4th gear slot renders as a sealed pedestal-in-waiting in season 1; rocket companion-generation produces records for season ≥ 2 only; every companion is, without dilution, a self the player used to be. The season-2 first-molt-return is a tentpole emotional beat to design toward.

**No T4 design questions remain open.** The remaining T4 work is *implementation* (companion generation, gauntlet validation), not design — and it lives on the pipeline blocker list (§ 4), not the design queue.

---

## 2. Current engine frontier (what IS — descriptive)

### 2.1 The 2D certification wave

The cert wave certifies the commit-grade spatial combat engine across six phases (W-A…W-F). The RESOLVE/MEASURE split: **RESOLVE** (W-C exit) = the engine produces the right *fight outcome / spatial behavior*; **MEASURE** (W-D/W-F exit) = the engine produces the right *8-axis behavioral-identity (BC) tuple*.

| Phase | What it certifies | State |
|---|---|---|
| W-A…W-B | Type-wall (`CommitGradeVerdict` vs `SearchGradeEstimate`) | DONE — wall up at W-B |
| W-C | RESOLVE — right fight outcome / spatial behavior | PASSED |
| W-D | MEASURE — six-axis BC tuple wired-not-default; cond.4 PASS (gate-read) | **CLOSED 2026-06-13** |
| W-E | Throughput proof | **NOT STARTED — critical path** |
| W-F | 1D engine (`search_estimator`) deletion + cond.5 defensive-bridge boss re-validation + § 6.4 close ("the archive measures the kit") | PENDING (gated on W-E) |

§ 6.4 ("the archive measures the current kit = measured fact") **stays OPEN; it closes at W-F.** wired-not-default ≠ discriminates: W-D wired the axes, but "measures the kit" is only established when RESOLVE (W-C) AND MEASURE (W-F) both pass.

### 2.2 The telegraph / dodge wave

Temporal-decoupling design: the sim mints danger-zone SHAPE + wind-up TIME; the piloted Godot game owns dodge-resolution. State:
- Dispatches 1, 2 — fired (cert-independent).
- **Dispatch 3 (combat model) — GO.** Ruled to fire at W-C RESOLVE-clear (not full W-F); the K4≥K2/M1 movement-credit finding ruled orthogonal-by-design (D2's "gather inverts the margin" is an outcome/mechanism finding, the orthogonal reading the ruling required).
- rocket combat-model build (`51867f5`, engine) — CODE done, TAG HELD pending role-floor Gate-2.

### 2.3 Generation state

- Envelope composer has a coordinate-derived **role-floor** (rocket v2.2, `rocket/v2.2-envelope-role-floor`) — role-PRESENCE guaranteed.
- **b6 stays WHOLE** (Decision 2 HELD, upgraded "net"→"SPEC"). b6 is the in-tree worked example of boss-efficacy the envelope must match before b6 retires. The rogue arc CLOSED the single-global-modifier architectural hypothesis (RULED OUT); the real constraint is a **kit-composition boss-efficacy deficiency**, isolated for the first time.
- **Companion corpus = ZERO records.** The Q8 companion layer cannot be exercised or measured until rocket runs a companion-generation pass.

### 2.4 The measurement gap (load-bearing — reframes "zero kills")

Generated kits currently enter the balance sim **stripped of most of their realized loadout:**
- **Skill investment = 0.** `compute_investment_multiplier_p1` scales damage 0.35× at 0 points → 1.0× at 15 points (`per_skill_emitter.py`). Kits measure at 0 points → 0.35× damage.
- **Synthetic stopgap gear.** `compute_balance_gear_stats()` (`gear_catalog.py`) supplies ~937 hp / ~225 armor / ~3% crit / ~150 flat damage — explicitly marked "Stopgap… Remove this block," NOT the spec'd Legendary T1 + 4-piece Set.

**Consequence:** the rogue's "~192 mean damage vs a 123,356-HP boss / zero kills" verdict reflects a kit measured at ~30–40% of its real power. The battle sim is currently measuring the wrong kit even where the engine is correct. This is why the representative-loadout fix sits at the head of both blocker lists.

### 2.5 D-series and export

- **D4 proxy-port** (Axis-2A discrimination) — arity=8 RESOLVED; unblocked; awaits priority.
- **D5 reference-kit** (resource/CC-differentiated; exercises Axis-5 Resource + Control) — READY, not picked up.
- **D6 grouping-vocab loader** — FIXED (loader path restored; 5824 tests collect); dispatch ready for formal closure.
- **W-D-export** (star-lord) — Gate-1 PASS-WITH-WARN (additive-migration, parallel-safe); MIGRATION simulation-seam v1.31 on disk → **unblocked.**

---

## 3. BLOCKER LIST A — the commit-grade BATTLE SIM

*What remains before the battle sim is complete: an engine that (i) produces the right answer AND (ii) is fed the real kit.*

**Axis (i) — the engine produces the right answer (cert wave):**
1. **W-E throughput proof** (gamora) — NOT started. Critical path. Proves the commit-grade engine sustains the throughput the balance loop needs.
2. **W-F — 1D deletion + cond.5 + § 6.4 close** (gamora). Deletes `search_estimator`; re-validates the defensive-bridge boss; closes § 6.4. Gated on W-E.

**Axis (ii) — the engine is fed the real kit (measurement completeness):**
3. **Representative-loadout fix** — the keystone. Three sub-steps:
   - (a) **gandalf** authors the representative-loadout design contract (task #21): full 15-point node selection + real Legendary T1 + 4-piece Set, defining the canonical measured loadout.
   - (b) **rocket** materializes real Legendary + Set gear generation (retires the `compute_balance_gear_stats` stopgap).
   - (c) **gamora** wires full node selection + real gear into the sim's measured loadout.

**Hard dependency:** cond.5 (W-F boss re-validation) must run on **real loadouts** to be trustworthy → the representative-loadout fix (3) is upstream of a trustworthy W-F (2).

**Battle sim COMPLETE = {1, 2, 3} done, with 3 upstream of 2's cond.5.**

---

## 4. BLOCKER LIST B — the end-to-end PIPELINE

*generate → simulate/balance → measure (BC tuple) → archive → export. Includes all of List A, plus:*

5. **W-D-export** (star-lord) — emits the BC tuple to the archive. Unblocked (v1.31 on disk); needs to fire.
6. **Companion-generation pass** (rocket) — the corpus has zero companion records; the pipeline cannot end-to-end the Q8 companion path until Hall-sourced companion kits (season ≥ 2) are generated.
7. **Axis-discrimination completeness** — D4 proxy-port (Axis-2A) + D5 reference-kit (Axis-5 Resource/Control). The BC tuple wires these axes but they are currently inert/uniform; these make them discriminate.
8. **D6 formal closure** — loader fixed; dispatch closure is housekeeping, not a true blocker.
9. **Generation-quality gate (b6 / envelope boss-efficacy)** — NOT a pipeline-completion blocker (the pipeline runs with b6 as the boss-capable spec), but the open architectural item: the envelope composer must reach **b6-parity boss efficacy**, re-measured on real loadouts, before b6 retires. This is the Option 1 investigation (§ 5).

**Pipeline COMPLETE = List A + {5, 6, 7}, with {8} as cleanup and {9} as the b6-retirement gate (separable).**

---

## 5. The AUTHORIZED autonomous run plan

### 5.1 Governing principle — park-and-advance; pre-authorize the destination AND the evidence-gate; park only on ambiguity

recognition→validate→commit is not suspended for the run — it is **automated.** The critique-pair gates (jack-ryan Gate-2 + gandalf design-endorse) ARE the validation step; pre-authorizing them to be **terminal-on-clean-pass** lets KR run the full loop autonomously and surface Matt only when validation comes back **ambiguous** or a **new design question** appears. Safety: every deletion is a git commit — revertible; the downside of an autonomous-delete-on-clean-gate that later proves wrong is a `git revert`, not lost work.

### 5.2 The three-tier pre-authorization envelope (RATIFIED Matt 2026-06-16)

**Tier 1 — pre-authorize FULLY** (additive; gated; no destructive conclusion). KR fires, critique-pair gates, work advances. Matt needed only if a gate FAILS:
W-E throughput · W-D-export · telegraph dispatch 3 · rocket role-floor Gate-2 (releases `51867f5` tag) · D5 reference-kit · D6 close · D4 proxy-port · **the representative-loadout keystone** (contract → materialize → wire) · companion-generation (season ≥ 2).

**Tier 2 — pre-authorize the deletion to FIRE on a pre-registered clean criterion** (destination known; trigger gated on evidence; park on ambiguity):
- **1D deletion (W-F):** fires when W-E passes + cond.5 boss re-validation passes clean (Gate-2 PASS + gandalf endorse) + type-wall verified intact + § 6.4 criteria met — **and cond.5 runs on real loadouts.** Park on any PARTIAL / type-wall hole.
- **b6 deletion:** fires when the envelope composer hits **b6-parity boss efficacy** on the rogue cell, **re-measured on real loadouts.** Park if parity is not reached.

**Tier 3 — ALWAYS parks for Matt:** any gate FAILURE/PARTIAL on a destructive step; scope amendments; new design questions; the b6 "accept the deficiency vs keep investigating" fork if parity is not reached.

**Option 1 — AUTHORIZED:** the bounded composition investigation (envelope-vs-b6 boss-efficacy diff; cheap because b6 is the answer key). Lets the run reach the b6-deletion evidence-gate instead of parking immediately on "no path to the criterion."

**Push policy — AUTHORIZED:** wave-close pushes pre-authorized on both repos. KR pushes accumulated commits at each wave close.

### 5.3 Dependency-ordered queue (park-and-advance)

**Wave 1 — immediate, independent:** D6 close · W-D-export · rocket role-floor Gate-2 (release `51867f5`) · telegraph dispatch 3.

**Wave 2 — the measurement keystone (gates the trustworthy deletions):** gandalf authors representative-loadout contract → rocket materializes real Legendary+Set gear → gamora wires full nodes + real gear → re-measure the rogue (and gauntlet) on real loadouts.
*Parallelization:* W-E throughput (Wave 3) is loadout-independent, so gamora can run W-E in parallel with rocket's gear materialization; they contend only at the final wire + re-run.

**Wave 3 — cert critical path:** W-E throughput → cond.5 boss re-validation (on real loadouts) → § 6.4 close → **1D deletion (Tier-2 auto-fire on clean gate).**

**Wave 4 — generation completeness + the b6 question:** companion-generation pass (season ≥ 2) · D5 reference-kit · D4 proxy-port · **Option 1** envelope-vs-b6 boss-efficacy investigation (re-measured on real loadouts) → if envelope hits b6-parity, **b6 deletion (Tier-2 auto-fire)**; if not, **PARK** the accept-vs-investigate fork for Matt.

### 5.4 What parks for Matt at next session (expected)

- The b6 accept-vs-investigate fork, IF the envelope does not reach b6-parity on real loadouts.
- Any Tier-2 deletion gate that returns PARTIAL/ambiguous.
- Any new design question surfaced by the re-measurement (e.g., if real loadouts change the kit-identity picture enough to reopen a strategy's design).
- DoT-as-boss-bridge follow-on (gandalf brief `81285d7`), if Option 1 surfaces it as the mechanism.

---

## 6. Push manifest (parked commits, wave-close push authorized)

**Collab (`origin/main..HEAD`, 6):** `746d3b2` Path Pure · `1959350` Q6/Q7 ratified · `423352b` jack-ryan Gate-1 telegraph math-notes · `e906d63` gate-phase ruling · `f03a5e1` KR cert-wave sequencing fold · `46900c7` jack-ryan Gate-1 DELTA.

**Engine (`origin/main..HEAD`, 3):** `51867f5` rocket i-frame dodge (CODE, tag held) · `0aa324d` jack-ryan decisions-log methodology entry · `28b9074` gamora DoT-bridge confound control (read-only).

Per the authorized wave-close push policy, KR pushes these (and run-accumulated commits) at each wave close.

---

## 7. Next-session re-entry

**Read first:** this doc + `canonical/00-ground-state.md` + the run's wave-close summaries (KR will author per wave).

**State the run should have advanced:** Wave 1 closed (D6, export, role-floor, dispatch 3); the representative-loadout keystone authored + materialized + wired; W-E throughput proven; possibly 1D deletion fired (if cond.5 clean on real loadouts); companion generation begun.

**Most likely open at re-entry:** the b6 accept-vs-investigate fork (Matt design call); any parked Tier-2 ambiguity; the gandalf player-journey authoring for the Path-Pure season-2 companion-return beat (design, not blocking the engine).

---

## (Final). Cross-references

- Cert wave: `canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md`; W-D close `agentic_orchestration/cert-wave-2d-W-D-close-2026-06-13.md`.
- Telegraph: `canonical/story/telegraph-dodge-temporal-decoupling-2026-06-15.md`; dispatch-3 ruling `agentic_orchestration/gandalf/notes/2026-06-15-telegraph-dispatch-3-gate-phase-ruling.md`.
- T4 companion: `canonical/story/2026-06-13-companion-as-hall-of-heroes-ally-commitment.md` (Path Pure v1.1); Q8 matrix `agentic_orchestration/gandalf/notes/2026-06-13-q8-companion-convergence-matrix-FINAL.md`.
- Rogue arc / b6 Decision 2 / Option 1-2: `agentic_orchestration/skill_handoff_2026-06-15.md`.
- Ground-state oracle: register in `canonical/00-ground-state.md` § 1 (same commit family).

---

**Signed:** gandalf (story-and-design steward), 2026-06-16.
**For:** the engine-state snapshot at the moment T4 design closed (Path Pure ruled) — naming the two completion-blocker lists (commit-grade battle sim; end-to-end pipeline) with the representative-loadout fix as the shared keystone upstream of both deletions, and the authorized park-and-advance autonomous run plan (three-tier pre-authorization envelope + Option 1 + wave-close pushes) that works those blockers down without halting the trunk.
