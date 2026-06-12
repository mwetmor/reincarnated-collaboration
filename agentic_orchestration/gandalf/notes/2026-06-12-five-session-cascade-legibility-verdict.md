# Verdict — 5-Session Cascade Legibility Review (Questions A / B / C)

**STATUS:** CURRENT — Pattern B verdict (gandalf, 2026-06-12); maximum-effort review per Matt request
**Author:** gandalf
**Scope reviewed:** all 5 session specs + gamora proxy kernel handoff dispatch, cross-checked line-by-line against the two canonical translation sources:
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` (hypothesis doc — read in full)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (BC mechanical substrate doc — read in full)

**Context:** the 5 specs were authored in a mobile remote-control session WITHOUT access to Mac-resident canonical docs. Matt asked: (A) is the 5-session cascade the right next step; (B) if not, should gandalf one-shot all specs; (C) if the cascade is right, are the specs adequately linked to the two canonical docs for infallible rocket/gamora implementation.

---

## 0. Top-line

**A) YES — the 5-session cascade is the right structure.** The decomposition (T4 / proxy+companion / core mechanics / kit identity / validation) is seam-aligned, the dependency graph is sound, and the SPEC-vs-HYPOTHESIS-vs-BOTH classification is a correct translation of the hypothesis doc's architecture. Keep it.

**B) NO — do not one-shot all specs.** The mobile session is itself the empirical refutation of the one-shot alternative: spec authoring without dialogue and without doc access produced content that is *internally coherent but silently forked from locked canon* (see § 2). Additionally, Q1–Q8 (and the 441-pair convergence matrix behind Q8) are genuine design decisions only Matt can make; one-shot authoring would bake in gandalf's guesses at the project's highest-leverage choice points.

**C) The specs are linked in INTENT but NOT in VOCABULARY.** As written, rocket and gamora CANNOT implement against them infallibly — every place a spec touches the locked BC measurement vocabulary, it re-derives bin names, bin counts, thresholds, and metrics from memory, and the re-derivations conflict with the lock doc. The fix is a **normalization pass (desk work, gandalf-authored), not a rewrite** — roughly 85% of the spec content survives untouched. Punch list at § 3.

**The mobile work verdict:** not wasted. The T4 catalog, the ProxyCombatant interface, the numeric pass/fail criteria, the three-tier proxy architecture, the modifier-vector decision (companions as pre-fight vectors, not fight entities — a genuinely good architecture call that collapses 2.4M fights to 40K applications) all survive. What broke was precision-of-citation: Session 3's header *cites* the BC axes lock doc while its content *contradicts* it — citation from memory, not from reading. That is exactly the failure mode Matt suspected, confirmed empirically.

---

## 1. Forensics recap (the interrupted sessions)

- Gamora's spatial re-point Phase 3/4 closed cleanly at 11:01–11:06 with Gate-2 PASS — **unaffected** by the interruption.
- The remote session's rocket + gamora subagent invocations fired after the 13:40 handoff commit and left **zero durable artifacts** in either repo. Nothing to recover; nothing corrupted; only session time lost.
- The "two drafted work assignments": the gamora proxy kernel handoff dispatch EXISTS (committed, 189 lines); the rocket assignment exists ONLY as the handoff doc's "Rocket fires next on" classification — **no rocket dispatch file was ever written.**

---

## 2. The drift findings (Question C evidence)

### 2.1 Systematic bin-vocabulary fork

The locked vocabulary (qd-engine-bc-axes-lock § 3) vs what the specs use:

| Axis | LOCKED (canonical) | SPECS USE (drifted) | Where |
|---|---|---|---|
| Axis 2 Damage Geometry | single-target / small-AOE / large-AOE / chain / multi-spawn (5 bins; aoe_radius thresholds; damage-weighted argmax) | "AoE_burst / DoT_stack / single_target" as Axis 2 bins | S1 eligibility gates; S2 §5.2/§6.3 weights; S3 §3.1; S5 Test 3 |
| Axis 2B Control Density | damage-pure (<20%) / mixed (20–60%) / control-pure (≥60%); **effect-budget weighted**; 30%-slow inclusion floor | HIGH/MEDIUM/LOW at ≥0.50/0.25; **skill-count ratio**; 0.5s duration floor | S3 §4; S1 NETWORK_AMPLIFIER gate; S2 weights; S4 labels |
| Axis 3A Damage Tempo | low / medium / high at <2 / 2–6 / ≥6 **damage events per second** | Burst / Sustained / Mixed by **first-3s damage fraction** | S3 §5.1; S2 weights; S4 labels; S5 Tests 2–3 |
| Axis 3B Amplitude Variance | flat / variable / spiky at CV <0.3 / 0.3–0.7 / ≥0.7 (**3 bins, per-event magnitudes**) | HIGH/LOW at CV 0.60 (**2 bins, per-tick damage**) | S3 §5.2 |
| Axis 4 Defensive Profile | tank / mitigator / dodger / glass (eHP ratio + avoidance_rate formulas) | "sustain / evasion / glass_cannon" — **"sustain" is not an Axis 4 bin at all** | S2 §4.2/§5.2/§6.3; S4 §2.2/§5.2; S5 Tests 2–3 |
| Axis 5 Resource Economy | HP-economy / damage-taken-converts / charge-stack / starved / overflow / generator-spender / steady (**7 structural+statistical bins**) | "Mana / Rage / Combo / Focus / Stamina" (**energy types as bins**) + claims "6 bins (was 5)" | S3 §2.3; S2 §4.2/§5.2 weights |

**Critical nuance:** the drift is CONSISTENT across all five specs — the mobile session re-derived a coherent *parallel* vocabulary. So the fix is mechanical re-pointing plus a handful of design rulings, not structural surgery.

### 2.2 Concrete errors the drift produces

1. **Cell-count math is wrong (S3 §2.3).** 68,040 = 6×5×3×3×3×3×4×7 — the locked grid **already contains 7 Axis 5 bins including charge-stack**. The lock's charge-stack bin was awaiting a *generation-side mechanic to fill it*, not a new bin. Session 3's "Axis 5 now has 6 bins (was 5)" and the 81,648-cell expansion are double-counting. Delete; no QD grid expansion occurs.
2. **Charge-stack mechanic contradicts the lock's bin detection (REAL design conflict, not vocabulary).** The lock detects charge-stack structurally + statistically: `mean_charge_fraction ≥ 0.75 AND variance < 0.20` — a **build-then-HOLD** pattern (PoE Frenzy maintenance). Session 3 + handoff Item 4 specify **spend-all-at-threshold** — build to 5–10, dump, repeat. Spend-all kits will run mean ≈ 0.5 with high variance and would be classified **generator-spender**, not charge-stack, under locked rules. Ruling needed: either (a) amend the lock's detection to structural-only for the new energy_type (my recommendation — the structural charge mechanic IS the identity; the statistical test was designed to catch charge-stack patterns in kits that *don't* declare one), or (b) redesign the mechanic toward hold-with-decay. This must resolve **before handoff Item 4 fires.**
3. **Two geometry layers conflated.** Engine skill-geometry (implementation palette; doc 09 lineage) and Axis 2 BC bins (kit-level measurement via damage-weighted argmax) are different layers. S1's "Axis 2 multi-target bin," S3's "geometry type catalog" (listing DoT_stack — a tempo/stacking concept — as a geometry), and S5's Test 3 all blur them. The normalization adds an explicit two-layer statement + a skill-geometry → Axis-2-bin contribution mapping. Also: verify with rocket whether "beam" already exists in the engine's geometry palette before S3 declares it NOT BUILT.
4. **S5 hypothesis tests would select wrong populations.** Test 2 and Test 3 pass criteria are written against "Axis 3A = Burst," "Axis 4 = Sustain," "Axis 2 = AoE" — none of which exist as locked bins. Implemented as written, the tests compare phantom cohorts. After normalization, Test 3's burst-vs-sustained comparison should either re-point to locked bins (3A high-vs-low tempo; 3B spiky-vs-flat) or — better — surface "front-load profile" (first-3s damage fraction) as an explicitly NEW proposed measurement, because it captures an experiential dimension (opener-dominance) the locked axes genuinely don't. The mobile session accidentally invented a candidate axis; canonize the invention as a *flagged proposal*, not a silent rename of 3A.

### 2.3 Linkage gaps to the hypothesis doc (beyond vocabulary)

5. **Session 5 validates the corpus but never writes the library.** The hypothesis doc's center of gravity is the pattern-cell schema (`pattern_cells`, `bc_axis_signature` 8-vector, KPM targets per power plane, graduation ladder PROVISIONAL → … → LIBRARY-LOCKED). Session 5's tests are corpus-level statistics; nowhere does any spec say which Session 5 outputs populate which `pattern_cells` fields, or how a sim-side PASS feeds the PROVISIONAL→PLAYTEST graduation chain. One added section in S5 ("Outputs → pattern-cell field mapping") closes this. Without it, the cascade validates the engine but leaves the hypothesis doc's library architecture unfed.
6. **Axis 2A sim-deferral closure is implicit, not declared.** All 6 proxy-family T4 strategies depend on Axis 2A proxy bins, which the lock marks ALWAYS DEFERRED (solo-only sim). The ProxyCombatant handoff is precisely the extension that retires that deferral — but no spec says so. Declare it, so the lock doc's deferral matrix gets amended when Items 1+2 land (jack-ryan will rightly ask at Gate 2 what authorized the deferral retirement).

### 2.4 Internal inconsistencies (small, fix in the same pass)

7. **Dispatch status contradiction.** The handoff dispatch §0 asserts "Session 2 … is now locked," while Session 2's own header says DRAFT, locking after Session 1 ratification, and the overview doc says "No implementation fires before spec is locked and Matt-ratified per session." Resolution at § 4 below.
8. **"5 modifier types" vs 6 rows** (S2 §6.2 and dispatch §3 both tabulate six: damage_amp, cc_duration_mult, survivability_mod, resource_gen_mod, aoe_radius_mod, enemy_cc_mult).
9. **Faction coverage gap (design call, not error).** The 8-faction catalog has no home for `mesoamerican`, `sub_saharan_african`, or `south_southeast_asian` lineages — three entire lineage families resolve only via nearest-match fallback. Either add 1–2 factions (e.g., a Mesoamerican/sun-cycle faction; a sub-Saharan ancestral faction) or explicitly accept absorption. Given Sunfire Dominion already spans two lineage families, a 9th–10th faction is cheap and the representational dividend is real. Matt call at Session 2 lock (this is S2 open question #1 enlarged).
10. **S2 §6.3 archetype→modifier mapping** is written entirely in drifted vocabulary, and it is the one table rocket implements *directly* — highest-priority normalization target.

---

## 3. The normalization punch list (what I author as desk work)

| # | Item | Spec(s) touched | Type |
|---|---|---|---|
| N1 | Re-point all axis bin names/thresholds to lock vocabulary; per-row design judgment where no clean mapping exists (e.g., "sustain Axis 4" → tank/mitigator per intent) | All 5 + dispatch | Mechanical + judgment |
| N2 | Delete QD-grid expansion claim; correct to "fills existing charge-stack bin" | S3 §2.3 | Correction |
| N3 | Charge-stack detection ruling (structural-only vs mechanic redesign) | S3 §2, dispatch Item 4, lock-doc amendment proposal | **Matt ruling** |
| N4 | Two-layer geometry statement + skill-geometry → Axis 2 mapping; verify beam vs engine palette with rocket | S1, S3, S5 | Mechanical + 1 query |
| N5 | "Front-load profile" measurement: canonize as flagged NEW proposal, not silent Axis 3A rename | S3 §5.1, S5 Tests 2–3 | Proposal |
| N6 | S5 outputs → pattern_cells field mapping section | S5 | Addition |
| N7 | Declare Axis 2A deferral retirement; queue lock-doc deferral-matrix amendment | S2, dispatch | Addition |
| N8 | Fix "5 vs 6 modifier types"; dispatch lock-status line | S2, dispatch | Correction |
| N9 | Faction coverage gap ruling | S2 §7 | **Matt ruling** |

N1–N2, N4–N8 are gandalf desk work — no Matt session required; deltas presented for review at the top of the Session 1 dialogue. N3 and N9 join Q1–Q8 as **Q9 and Q10** in the Session 1 gating dialogue.

---

## 4. Sequencing recommendation (what fires when)

1. **Gandalf normalization pass (desk work, next work unit).** Author N1–N2, N4–N8 as spec revisions. Output: revised specs + a one-page delta summary.
2. **Gamora handoff: partial fire is safe NOW, with one amendment.** Items 1, 2 (ProxyCombatant + simulate_fight extension) and 5 (terrain assessment) are engine-level interfaces untouched by bin drift and independent of Q1–Q10 — Matt can ratify Session 2 §3 *specifically* and those items fire. Item 3 (modifier application) is also drift-immune on the gamora side (caps + clamping are vocabulary-independent; the drift bites rocket's *derivation*, not gamora's *application*). **Item 4 (charge-stack) HOLDS pending N3** — firing it as written builds a mechanic the locked archive would misclassify. Amend the dispatch's "now locked" line to "§3 interface Matt-ratified 2026-06-12; full Session 2 lock pending Session 1 ratification."
3. **Session 1 dialogue proceeds as planned** — Q1–Q8 plus Q9 (charge-stack detection) and Q10 (faction coverage), opening with the normalization delta review (~10 minutes).
4. **Rocket dispatch is authored AFTER normalization** — never before. Rocket's Session 3/4 work is the seam where every drifted table (weights, §6.3 mapping, Axis 2B measurement, label assignment function) lands as code. Dispatching rocket against the current text would faithfully implement the fork.

---

## 5. One design observation beyond the mandate

The companion-as-modifier-vector decision (S2 §0) deserves explicit praise and a canonical anchor: it is the same shape as Diablo 3's follower system done *right* — followers as stat-vectors kept D3 companions balanceable in a way D2's mercenary-as-full-combatant never was, and the 2.4M→40K fight collapse is the engineering dividend. When Session 2 locks, this decision should graduate to a short canonical/story note so future seasons don't accidentally re-promote companions to fight entities "for realism" — that is the drift vector I will be watching for.

---

**Sign-off:** gandalf, 2026-06-12. Anchors: hypothesis doc (2026-05-31), BC axes lock (2026-05-20), Sessions 1–5 specs, gamora handoff dispatch, session-close handoff. Pattern B verdict; auto-commit per standing discipline.
