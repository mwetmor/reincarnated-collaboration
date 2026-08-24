# Finding — 2026-08-24 — KC2 MODEL-COMPLETION RUN · B-1, the player sustain layer (gamora)

**Reviewer:** jack-ryan
**Severity:** PASS-with-findings (3 × WARN, 5 × INFO, 0 × BLOCK)
**Target:** engine `baf120d8` → `5acf6c92` → `0bdd7704` (not pushed); sibling checkpoint `E-s09-cp150-b1`
**Developer:** gamora (simulation seam)
**Commission:** model-completion charter § 3 Wave 2, ledger **L-20**; ruling facet **(d) BOTH**
**Conductor:** gandalf `RUN-CONDUCTOR` — build returned at **L-21**, `F-B1-1` ruled at **L-22**, gates fired at **L-23**
**Principles applied:** REVIEW_PROCESS.md 1–6 · Disciplines #1, #3, #8, #10, #12, #72 · ADR-002, ADR-004, ADR-006 · charter Law 3, D4, D5 · L-4/DR-1, L-5, L-19, L-22
**Submission route:** no `qa/pending/` file — the build was routed by the conductor's ledger row L-21. Noted, not faulted; the charter routes Wave-2 builds directly to Gate 2.

---

## Verdict

**PASS-with-findings. No BLOCK. B-2 is unblocked.**

All seven claims put to me verify. Five of them I re-derived from bytes rather than reading
gamora's prose, and every one landed exact. The law stack held end to end — math note ALONE with
zero code and zero grades, ADDENDUM ALONE publishing two of gamora's own defects *above* the code
that repairs them, then the landing commit. The D5 parent is untouched and I proved it by rerunning
the frozen gate myself. Law 3's quarantine is not promised, it is machine-enforced, and I could not
find a way through it.

The three WARNs are all **forward-facing**: none is a mechanism defect, none can reach the sim as a
behavioural fault, and none blocks B-2. Two of them (WARN-2, WARN-3) are debts that come due at the
**baton-v2 cut (Wave 4)**, not now. WARN-1 is a discipline drift in the instrument shape that
B-2…B-7 will inherit, which is why I am naming it at B-1 rather than at B-4 when it has five
copies.

**The one sentence that matters for the run:** B-1's headline result is that the commission's
premise was wrong, and gamora said so first, in a zero-grade commit, before building anything. That
is the behaviour the charter's D4 exists to produce. It worked.

---

## 1 — What I verified independently, from bytes and substrate (not from the submission's prose)

| Claim | Method | Result |
|---|---|---|
| New sibling sha `0957daaf…c635b` | `shasum -a 256` on the artifact | **EXACT** |
| Mech sibling sha `20b05cb4…b4f5b`… | re-hashed from bytes | **EXACT** |
| Parent `E-s09-cp150` 20/20 byte-unchanged | I re-ran `verify_frozen()` myself at review time | **20/20, no mismatch** |
| Pinned CSV `0cdfd3af…` (the "no constant moved" basis) | `shasum -a 256 data/kc2/pm4g_defensive_actives.csv` | **EXACT** |
| Corrected § 0 figures 5/20/1/2/10/4 | read from `cells["poll-at-slot__salt0"].activation_counts` | **EXACT** — turtle 5, barrier 20, menhir 1, potion 2, warcry 10, ascension 4 |
| "39 discarded firings per ladder" | 42 total − menhir 1 − potion 2 = **39** = turtle 5 + barrier 20 + warcry 10 + ascension 4 | **EXACT** — precisely the two discarding sites' payload |
| Terminal-wave movement 155→154 · 156→156 · 152→152 · 151→151 · 151→151 | read from all 10 artifact cells | **EXACT** |
| "salt 1 gains a Turtle firing; salt 0 loses the potion entirely" | turtle 5→6 on salt 1; `health_potion` key absent on monitor salt 0 | **EXACT** |
| Census internal arithmetic | 233+208+184+208+84 = **917**; 1+0+1+3+8 = **13**; misses 1+0+0+0+1 = **3** | **CONSISTENT** |
| `thresholdDuration` description quoted in `MONITOR_BASIS` | `pm4g_field_evidence.csv`, grade `MEASURED` | **CHARACTER-FOR-CHARACTER** |
| `lifeMonitorPercent` on `skill_passiveonlifebuffself.tpl` | same CSV, type `real`, grade `MEASURED` | **PRESENT** |
| Menhir constants (θ 33.0, 10.0 s, 21.0 s, regen 120, `skillLifePercent` 35) | `pm4g_defensive_actives.csv` row `willtolive1.dbr` | **EVERY ONE EXACT** |
| Turtle constants (θ 50.0, 100 %, 8.0 s, absorb 6100, controller `cast_@selfat50%health_100%.dbr`) | same CSV row `tier1_29e_skill.dbr` | **EVERY ONE EXACT** |
| Smoke-line "350 pass / 1 PRE-EXISTING fail" | I ran `pytest tests/ -k kc2` | **350 passed, 1 failed** — `test_AC_10_10`, `secondary_streams.py:136`, a file B-1 never touches |
| New test file | I ran `pytest tests/test_kc2_mc_b1_sustain_procs.py` | **18 passed, 0.09 s** |

---

## 2 — The seven commissioned claims, adjudicated

### Claim 1 — premise correction + manifest repair · **VERIFIED**

`fixture.OUT_OF_MODEL` is 13 rows. `ROW_DISPOSITIONS` is 14 — the 13 plus `ulzaads_decree`, which
is correctly a *sub-row* of `devotion_procs` and correctly absent from the fixture tuple. Set
difference is empty, and `test_B1_every_fixture_row_has_a_disposition` enforces it mechanically. Four
rows reclassify; `fighting_spirit` correctly stays OUT (UNBUILDABLE ≠ modelled) and a test asserts it.

The semantic shift is named in five places — module docstring, `out_of_model_manifest()` docstring,
`simulation/MIGRATION.md § 3`, `export/MIGRATION.md REQUEST 2`, and the checkpoint's
`manifest["⚑ semantic_shift"]`. Default is `False`; `test_B1_the_manifest_default_is_the_historical_document_statement`
asserts the historical callers get the § 5.3 tuple verbatim *and gain no key*. `fixture.OUT_OF_MODEL`
is not rewritten. **Discipline #12 satisfied.**

Three of the four reclassified rows are `PARTIAL`, and `RowDisposition` forces each to name the limb
that did **not** fold (`test_B1_every_disposition_row_is_well_formed`). A consumer reading only the
`out_of_model` list on a folded run would over-read those three as fully modelled — but
`⚑ reclassified_in_model` carries `not_folded` on every one, and both MIGRATION entries say so out
loud. Honest.

### Claim 2 — evaluation-point repair · **VERIFIED as decoded, with one grade caveat → WARN-2**

The repair basis traces to decoded substrate, not convenience. Both fields are `MEASURED` in
`pm4g_field_evidence.csv` and the template description is quoted verbatim. The `run.py` and
`counterplay.py` substitutions are surgical: one scalar each, isolated to the K-1 and K-3 predicates
respectively, `None`-default, and `test_B1_floor_hp_is_additive_None_reproduces_the_incumbent_predicate`
proves `floor_hp == hp` is indistinguishable from passing nothing.

The split rule is executable rather than commented —
`test_B1_the_split_rule_is_executable_K4_never_reads_the_floor` fails if K-4 ever reads the floor.
That is the right guard on the right line.

Caveat at WARN-2: the decoded field evidence covers **K-3 directly** and reaches **K-1 by analogy**.

### Claim 3 — activation ledger · **VERIFIED**

Both drain sites repaired, plus a third subtlety gamora caught and I did not expect: at `run.py:3149`
the incumbent iterated `drain_events()` directly and let every non-`heal` row die in the `continue`.
A naive fix (a second `drain_events()` call) would have returned empty — the drain is destructive —
and silently lost the heals. The code drains once, records all, then filters. That is the correct
order and the comment says why.

`B1-P6` is a genuine cross-instrument check, not a restatement: `counts()` derives from
`self.activations` and `test_B1_counts_are_derived_from_the_ledger_not_from_the_telemetry` asserts by
source inspection that it never reads `CounterplayTelemetry`. **True on all 10 cells.** `B1-P5`
worst residual is ~8.7e-9, three orders under the 1e-6 bar.

No `EVENT_TYPES` member minted; the `proc_activation` request is filed in `export/MIGRATION.md` for
star-lord. **ADR-004 respected** — gamora touched no `export/` code and says so in the entry's own
title.

### Claim 4 — UNBUILDABLE rows · **ALL THREE GENUINE**

Checked against `data/kc2/pm4g_defensive_actives.csv` (sha `0cdfd3af…`, verified):

- **`fighting_spirit`** — `trigger = OnHit`, `controller_record` **empty**. The decoded `triggerType`
  picklist (`MEASURED`) is `OnEquip;OnKill;LowHealth;LowMana;AttackEnemy;CastBuff;CastDebuf;HitByEnemy;HitByMelee;HitByProjectile;HitByCrit;AttackEnemyCrit;Block` — **`OnHit` is not a member.** Confirmed.
  `magnitudes = characterOffensiveAbility=108.0 ; offensiveTotalDamageModifier=95.0` matches the cited
  figures exactly. The inertness proof is sound and, importantly, **not new tuning**: `pthThreshold6=135`
  and min PTH 149.2 are prior-lap MEASURED figures established at Lap L / I-11
  (`player_offense.py:163-173`). PTH monotone increasing in OA and already past the top threshold ⇒
  +108 OA moves nothing. Pricing the decode as buying *visible activation and no arithmetic* is the
  honest read.
- **Ulzaad's Decree** — `tier2_37d_skill.dbr` `magnitudes` cell **empty**; `grep -c tier2_37d_skill_buff`
  = **0**. The Maul pair gamora cites as the contrasting pattern is real: `tier2_05f_skill.dbr` (empty)
  + `tier2_05f_skill_buff.dbr` (`defensiveProtectionModifier=-35.0 ; offensiveLifeLeechMin=45.0`).
  The companion genuinely was never extracted.
- **`resilience`** — `grep -c passive02` on the defensive-actives CSV = **0**. Absent, as stated.

No shortcuts. Each names its missing parameter, and
`test_B1_the_unbuildable_set_is_exactly_the_two_named_rows` enforces that the ask is a parameter and
not a gesture.

### Claim 5 — D5 law · **VERIFIED BY MY OWN RECOMPUTE**

Parent and both siblings check out (§ 1 table). `B1-P4` is measured **before the first run and after
the last**, from bytes, and both readings are published in the artifact. The instrument HALTs rather
than writes on mismatch (`_verify_pin`, `_fail`). Sibling-not-successor law is carried in
`identity.law`. Third sibling; neither predecessor shadowed or mutated.

The configuration bind deserves separate credit: `B1-P2a` requires the fold-absent payload digest to
equal the mech sibling's P-5 pin `f5ec56ea…` **exactly**, and HALTs if one keyword of the cell
drifted. That is an empirical bind, not a citation.

### Claim 6 — Law 3 quarantine · **VERIFIED, AND IT IS MECHANICAL**

- Exactly **one** occurrence of `160` in the entire three-commit diff, and it is inside
  `test_B1_no_referent_survival_figure_appears_in_the_module`, the test that forbids it.
- **Zero** occurrences of `160` in the 33 KB checkpoint artifact.
- `declared_constants()["⚑ moved"] == {}` and `constants_introduced == []`, both asserted by test.
- The standing `REFERENT_GRADES` DIAGNOSTIC quarantine (`roster.py:135`, "which nothing reads") is
  untouched by B-1.
- Every terminal-wave figure in the artifact sits under a structural `⚑ report_only: True` /
  `⚑ graded: False` pair, and no predicate is keyed to a survival outcome.

**The strongest evidence is behavioural, not structural.** The monitor limb made survival *worse* on
salt 0 (155 → 154), and gamora published that, explained the mechanism (a proc is a *spend*, and K-3
firing early holds HP above the potion's θ so K-4 never fires), and **refused to re-designate the
record limb on it** — citing R-PM4-27 part 3 in both directions. A build that had been quietly fitted
to the referent would not have shipped that paragraph.

### Claim 7 — Discipline #72 value-set sweep · **MECHANICAL AND COMPLETE inside the engine repo**

The corrected 5/20/1/2/10/4 appears in `AGENT_STATE.md`, `simulation/MIGRATION.md`,
`export/MIGRATION.md`, the landing commit body, and the checkpoint artifact. The stale 68/35/13
survives **only** in the parent math note § 0, which is deliberate and correct — the ADDENDUM carries
a strikethrough correction table so the lineage survives, per the same principle gamora applies to
`fixture.OUT_OF_MODEL` ("editing history in place is how a closed finding silently re-opens").

One leg falls outside gamora's reach → **INFO-4**.

---

## 3 — Findings

### WARN-1 — `B1-P1`'s implemented gate is **wider** than the pre-registered predicate

**Registered** (math note § 2.5, commit `baf120d8`, zero-grade):

> `MONITOR_ON_FLOOR` fires K-3 in **wave 151** and in **wave 153**, where `POLL_AT_SLOT` fires it 0 times.

**Implemented** (`gamora_kc2_mc_b1_sustain_2026_08_24.py`):

```python
p1_holds = any(v["waves_the_monitor_recovers"] for v in p1_per_salt.values())
```

That is an existential over **five salts and all waves**, where the prereg was a conjunction over
**two named waves on salt 0**. The artifact's `claim` string carries the widened wording and labels it
"⚑ THIS IS THE GRADING PREDICATE, AND THE ONLY ONE."

**The verdict is unaffected.** The evidence satisfies the narrow form outright — salt 0
`monitor_waves` is exactly `["151","153"]` with `poll_waves` `["154"]`, and ADDENDUM 1 § A3 publishes
the per-wave table against the registered wording. So this is not a predicate that was widened to
make it pass. But the *falsifier* is disarmed: had salt 0 failed and salt 1 recovered any wave, the
instrument would still print `holds: true` and the registered falsifier ("my census of the censored
ticks is wrong; publish and stop") would never have fired.

It also reads oddly against the same build's exemplary handling of `B1-P2`, where gamora wrote *"I did
not widen the predicate to make it pass"* and decomposed into a strictly narrower set. `B1-P1` got the
opposite treatment silently. The reason to raise it at B-1 rather than later is that **B-2…B-7 inherit
this instrument's shape**, and 4 of 5 salts show zero K-3 wave-set movement — so an `any()` gate will
keep passing on thin evidence as the builds compound.

**Cite:** Discipline #1 (math-before-code), charter **D4**, Review Principle #1.
**Action:** restate `B1-P1` in the artifact using the registered wording, and compute `holds` as the
registered conjunction on salt 0, with the 5-salt ensemble kept as reported sensitivity. Re-cut the
sibling (cheap — 10.3 s) or file an ADDENDUM 2; gamora's call which. **Not blocking B-2.**

### WARN-2 — K-1's evaluation-point repair rests on **trigger-class analogy**, not on a field on its own template

`lifeMonitorPercent` and `thresholdDuration` are `MEASURED` on `skill_passiveonlifebuffself.tpl` —
which is **Menhir's Will's** engine class (`Skill_PassiveOnLifeBuffSelf`, verified in the pinned CSV).

**Turtle Shell is `Skill_BuffSelfShield`**, fired via controller `cast_@selfat50%health_100%.dbr`. That
controller yields `triggerType=LowHealth` and `triggerParam=50.0` — both verified — but **no monitoring
semantics**. `MONITOR_BASIS` bridges the gap with *"Turtle Shell's own trigger is the same class"*,
which is true of the *trigger type* and elides that the field evidence lives on a different template.

This matters more than it looks, because K-1 carries the **larger** census delta (6 censored ticks vs
Menhir's 3), the **only** declared actuation latency (≤ 1 tick), and it is **not** covered by `B1-P1` —
the sole grading predicate is on K-3 alone. So the one limb whose repair is directly decoded is graded,
and the one whose repair is inferred is not.

The fix is a provenance grade, not a code change. **L-19 already minted the precedent**: when the walls
turned out to be derived rather than authored, the conductor created *derived-from-decoded-substrate* as
a legitimate grade distinct from estimation, with the derivation chain shipping in the pack. K-1's
evaluation point needs exactly that treatment, and K-3's does not — K-3 is decoded outright.

**Cite:** L-4/DR-1 (provenance-or-fail), L-5 (closed provenance enum), L-19 (precedent), Discipline #12.
**Action (owed at Wave 4, not now):** K-1 and K-3 carry **different** provenance grades in the Layer-1
pack. Amend `MONITOR_BASIS` to state the template difference in-band rather than compress it to "the
same class". **Escalated to conductor** as a facet-(d) provenance sub-ruling, batched with the baton-v2
schema work.

### WARN-3 — the new ledger is a **run-cumulative** per-wave snapshot shipping with no scope label

`run.waves[0]["counterplay"]["⚑ B1_sustain_procs"] = sustain_procs.as_dict()` executes inside
`simulate_wave`, so **every wave** receives a snapshot of the whole-ladder-to-date activation list.
`as_dict()` emits `n_activations` and the full `activations` list with **no `⚑ scope` key** saying so.

This is the exact shape that produced `D-B1-1` one document earlier — gamora banked the caveat about
`waves[].counterplay.telemetry` being run-cumulative, then summed the five wave dicts anyway. The
instrument here correctly reads `runs[-1]`, so gamora clearly applied the lesson to her own consumption.
It just did not get applied to the **key she is handing to star-lord**: `export/MIGRATION.md REQUEST 1`
describes the row tuple `(run_tick, t_s, wave, proc, kind, magnitude, detail)` and says nothing about
cumulative scope.

The incumbent `telemetry` key carries no label either, so this is not a regression. But baton-v2 hands
this surface to a **Godot team with no lap history**, and a consumer summing `n_activations` across
waves will double-count exactly as gamora did — with none of her context to catch it. Secondary: the
duplication is O(n²) in payload size, trivial at 42 rows, less trivial once B-2…B-7 add procs.

**Cite:** Discipline #8 (schema validation at boundaries), Review Principle #3 (cross-seam impact).
**Action:** add a `"⚑ scope": "RUN-CUMULATIVE snapshot taken at each wave's end — do NOT sum across waves"`
key to `SustainProcFold.as_dict()`, and one sentence to `export/MIGRATION.md REQUEST 1`. One-line fix; I
would rather it land at B-1 than be discovered at the cut.

### INFO-1 — two substrate citations that ride into the artifact are unqualified and unpinned

`MONITOR_BASIS` cites `pm4g_field_evidence.csv` and the `resilience` row cites `pm4g_played_kit.csv`
(row 319), both by bare filename. Neither is in the engine repo — both live at
`reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-g-player-kit/`.
I found and read them, and **both claims check out**, including `onHitActivationChance` carrying grade
`DECLARED: field not on this template`, exactly as the `fighting_spirit` row's "second, weaker gap"
states. But neither is sha-pinned the way `pm4g_defensive_actives.csv` (`0cdfd3af…`) is, and
`MONITOR_BASIS` is *the record limb's substrate basis* — the single string most likely to be quoted
downstream. Under DR-1 these need repo-qualified paths plus pins before the Wave-4 cut.

### INFO-2 — "all 13 rows" is 14

`simulation/MIGRATION.md § 3` and `export/MIGRATION.md REQUEST 2` both describe
`⚑ sustain_row_dispositions` as carrying "all 13 rows". It carries 14 (`ulzaads_decree` is the extra,
correctly). Cosmetic count drift in a cross-seam handoff doc.

### INFO-3 — `sustain_procs.py` docstring cites the math note but not ADDENDUM 1

Module docstring lines 3–4 point only at `kc2-mc-b1-player-sustain-2026-08-24.md`. The ADDENDUM is
where that note's § 0 figures were corrected and where `B1-P2` was decomposed. The instrument docstring
cites both correctly; the module should match.

### INFO-4 — the value-set sweep's one leg outside gamora's reach

`canonical/current-to-end-state/current-to-end-state-engine.md:41` still asserts the retired reading:
*"every missing player-side layer (Menhir's Will, Turtle Shell, Fighting Spirit, Ascension) extends
survival."* B-1 retires it — the layers were present and firing since I-4. The conductor **did** strike
and revise the parallel sentence in RULING-NOTE § 3 per L-21; the tracker line was not swept. gamora
cannot write there.
**Action:** conductor / canon-steward propagates the L-21 revision to the tracker.

### INFO-5 — one paragraph in `export/MIGRATION.md` was overtaken by L-22

The `F-B1-1` paragraph says *"In a Layer-1 model pack that row must be labelled as an identified
stand-in."* **L-22** subsequently ruled that no use-policy row exists in Layer 1 **at all** — the human
pilots the potion, Layer 1 carries only the decoded effect rules, and θ lives in the named
non-truth bin. Not a build defect (the ruling postdates the commit). Flagged so star-lord implements
**L-22**, not the pre-ruling text, at the cut.

---

## 4 — Approval disposition (ADR-002)

| Item | Tier | Disposition |
|---|---|---|
| WARN-1 `B1-P1` restatement | within-seam, instrument only | **jack-ryan APPROVES the fix** — gamora's call whether re-cut or ADDENDUM 2 |
| WARN-2 K-1 provenance grade | cross-seam / schema-adjacent | **ESCALATED to conductor** — facet-(d) provenance sub-ruling, batched with baton-v2 |
| WARN-3 ledger scope label | cross-seam wire surface | **jack-ryan APPROVES** the additive key + MIGRATION sentence (additive, default-visible, no behaviour) |
| INFO-1…INFO-3 | documentation | **jack-ryan APPROVES** |
| INFO-4 | collaboration canon | **routed to conductor / canon-steward** |
| INFO-5 | cross-seam handoff text | **routed to conductor**, star-lord to implement L-22 |
| B-2 hold (L-23) | — | **RELEASE RECOMMENDED.** Breaker semantics verified additive and `None`-default; nothing in B-2's control-state path composes with an unresolved B-1 defect. |

Nothing here is BLOCK. Nothing requires Matt.

---

## 5 — What I want on the record for the rest of Wave 2

Three behaviours in this build are the standard B-2…B-7 should be held to, and I would rather name
them than have them regress quietly:

1. **The premise correction came first, in a zero-grade commit.** The commission said "add the missing
   sustain layers." Six were not missing. gamora established that before writing a line of code, which
   means the finding cannot have been manufactured to explain a result.
2. **Two self-caught defects were published ALONE, above the code that repairs them** — including a
   pre-registered predicate recorded **FAILED AS WRITTEN** and replaced by a *narrower* set, with the
   failing digest printed. That is what D4 is for.
3. **The unfavourable result was published and refused as a basis for re-designation.** The faithful
   repair shortened survival on salt 0, and the record limb stood on its substrate argument.

WARN-1 is the one place the discipline slipped, and it slipped in the direction of a weaker gate. Worth
fixing now precisely because everything around it is this tight.

---

## References

**Engine repo** (`/Users/admin/Games/reincarnated-engine/`):
- `src/reincarnated/simulation/kc2/sustain_procs.py` (new, 368 lines)
- `src/reincarnated/simulation/kc2/run.py` (`simulate_wave` +1 kwarg; `out_of_model_manifest` +1 kwarg)
- `src/reincarnated/simulation/kc2/counterplay.py` (`begin_tick` / `low_health_heals` +1 kwarg each)
- `src/reincarnated/simulation/kc2/fixture.py:234-248` (`OUT_OF_MODEL`, unchanged)
- `src/reincarnated/simulation/scripts/gamora_kc2_mc_b1_sustain_2026_08_24.py` (the instrument)
- `src/reincarnated/simulation/scripts/gamora_kc2_pm4_i26_spawn_structure_fold_2026_08_16.py` (`replay` +1 passthrough)
- `src/reincarnated/simulation/math/kc2-mc-b1-player-sustain-2026-08-24.md` + `…-ADDENDUM-2026-08-24.md`
- `src/reincarnated/simulation/MIGRATION.md` · `src/reincarnated/export/MIGRATION.md` · `src/reincarnated/simulation/AGENT_STATE.md`
- `src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b1-20260824_132106.json`
- `tests/test_kc2_mc_b1_sustain_procs.py` (18 tests)
- `data/kc2/pm4g_defensive_actives.csv` (sha `0cdfd3af…`, verified)

**Collaboration repo** (`/Users/admin/Games/reincarnated-collaboration/`):
- `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md` (L-20…L-23)
- `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-pack-reframe-and-gap-rulings.md` § 3 (revised)
- `agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-g-player-kit/pm4g_field_evidence.csv`
- `canonical/current-to-end-state/current-to-end-state-engine.md:41` (INFO-4)
