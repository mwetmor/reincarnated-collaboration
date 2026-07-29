# Finding — 2026-07-29 — WR1-G2-M12 (fused M-1 mitigation law + M-2 frigidring nova)

**Reviewer:** jack-ryan (DEV-MODE, Gate 2)
**Verdict:** **PASS-with-notes** on `ddf51a8` — **plus one BLOCK-tier FORWARD finding** against
R-WR1-11(b) and the M-12b build now in flight. The landing under review is clean; the ruling that
supersedes it is not.
**Severity:** WARN (landing) · **BLOCK (forward, successor cell)**
**Target:** engine `ddf51a8` · build note `49f343b1`
**Developer:** gamora
**Run:** WR1-2026-07-28, cell `WR1-BUILD-M12` (conductor: gandalf, RUN-CONDUCTOR; charter §8.9)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate before commit), 3 (cross-seam impact),
4 (decisions/charter as truth), 5 (severity + escalation), 6 (cross-seam contract round-trip)
**Disciplines cited:** #1 (math before code), #2 (smoke-test vs full-regen), #8 (schema validation at
boundaries), #9 (attribution clarity), #10/#11 (empirical inspection over assumption), #12
(semantic-shifting changes declared, not buried)
**ADRs:** ADR-002 (tiered approval), ADR-004 (MIGRATION for cross-seam handoff), ADR-006 (read-only)

**Review posture:** read-only on the engine tree. I ran the test suites (which writes
`.pytest_cache` only) and imported the shipped modules to re-measure. I wrote nothing into
`reincarnated-engine/`. No `git checkout`, `stash`, or `worktree` was used — gamora is building
M-12b in the same tree.

---

## What I found

Seven claims were checked by re-measurement, not by reading the landing's prose. **All seven hold.**
The regression's AFTER state I reproduced exactly; its BEFORE state is accepted as audit-of-record,
and I say below precisely where the audit stops and the record begins.

### 1 — Spec-example reproduction table: reproduces byte-for-byte, independently of the tests

I imported `gd_nova` / `gd_mitigation` directly and called the shipped functions rather than
trusting `pytest`:

| cell | spec | my measurement | Δ |
|---|---|---|---|
| r=5, A=342.36, cold 14% | 524.3 | **524.28** | −0.02 |
| r=5, A=358.36 (errata) | 524.3 | **524.28** | −0.02 |
| r=9, A=358.36 | 536.9 | **536.83** | −0.07 |
| r=9, A=342.36 | — | **536.83** | armour-invariant |
| r=5, cold 0% | 595.1 | **595.06** | −0.04 |
| REGION arm, r=5, A=55.95 | 693.9 | **693.92** | +0.02 |
| Arm C ceiling 16/16 | 254 | **254.40** | +0.40 |
| T-M1-1 `taken(41, 342.36)` / `(41, 483.36)` | 12.3 / 12.3 | **12.3 / 12.3** | 0.00 |
| T-M1-2 `taken(541, 342.36)` | 301.35 | **301.348** | 0.00 |

All inside the spec's ±0.5. The errata-3 saturation claim also holds on measurement: the raw
physical leg at r=5 is **298.29**, below every candidate armour value, so r=5 and r=9 each return
the *same* delivered number at 342.36 and at 358.36. The armour step moves delivered damage by
exactly 0.00 HP. gamora's sharpening of the spec is correct, and it is correct for the reason
given.

### 2 — Opt-in default-off: verified structurally and on disk

- `ddf51a8` touches **13 files, all `.py` / `.md`**. Zero artifacts, zero traces, zero `output/`
  paths in the diff.
- `find` over the engine tree for any `*_fix3*` file modified since 2026-07-29 03:00 returns
  **empty**. No banked artifact moved.
- The string `gd_replica` appears in exactly two places outside `gd_mitigation.py` itself: a prose
  comment in `combatant.py`. **There is no production writer.** The only writer is the BQ-3 door,
  and `_coerce_mitigation_law` validates against a closed set and **rejects rather than defaults** —
  a typo'd law raises `CalibrationOverrideLeak` instead of silently reporting a GD comparison it
  never ran. That is the right failure direction and it is tested both ways.
- M-1's production-path invariance is genuinely *measured*, not argued: `T-M1-6` asserts
  `_mitigate_physical/_mitigate_elemental` equal the untouched `foundation/math_model.py` functions
  at three magnitudes, **with a non-vacuity guard** (the same defender under the GD law must return
  a different number). That is the strongest form of this test and it is the form shipped.

### 3 — Regression claim

The 41 new tests rerun clean (`41 passed`). **I then ran the full suite myself against the landed
tree and got an exact match to the record:**

```
60 failed, 5884 passed, 3 warnings, 21 errors in 1436.81s (0:23:56)
```

`5884 / 60 / 21` is byte-for-byte gamora's recorded AFTER state, reproduced independently. I
confirmed the tree was still exactly `ddf51a8` for `src/` and `tests/` for the duration (no
modified tracked files — gamora had not yet landed M-12b), so the count is attributable. `5884 −
41 = 5843` closes the "+41 is exactly the new tests" arithmetic against the recorded BEFORE, and
**no test in the new file appears anywhere in the failure set.**

**Where my audit stops:** I could not independently reproduce the BEFORE side. Doing so requires
either mutating the working tree (`git stash` / `checkout`) or extracting `HEAD~1` elsewhere and
overriding package resolution — the first is forbidden while gamora builds in the same tree, the
second risks a wrong baseline via the editable install and would have been worse evidence than
none. **The BEFORE counts (5843 / 60 / 21) and the empty failure-name diff are accepted as
audit-of-record, not as reproduction.** The record is internally consistent and the method gamora
describes (same-tree `git stash -u`) is the correct one. I flag the limit rather than imply a
verification I did not perform.

**On the BQ-3 door claim, which I could check directly.** gamora reports that BQ-3's T-4b
closed-set test "fired on the new `mitigation_law` field exactly as designed; the field was
DECLARED rather than the test loosened." I reran that suite against the landed tree: **39 passed**,
T-4b included, with `mitigation_law` present in `ALL_OVERRIDE_FIELDS`. The resolution is the
correct one for a schema-boundary guard (Discipline #8) — the guard was answered, not weakened.
(I also inspected `.pytest_cache/v/cache/lastfailed`, but it proved **non-probative**: it is a
cumulative 387-entry cache, byte-identical before and after my full run, so it reflects accumulated
history rather than either run's failure set. I record that I looked and that it establishes
nothing, rather than leaving it to be re-derived.)

### 4 — The pinned divergence test, and my independent read on the oracle

**The falsification holds. I re-derived it from first principles without touching gamora's code**,
and then confirmed against gamora's shipped `discrete_ring_oracle`.

For spokes of angular spacing `S` and a coverage window of angular half-width `arcsin(b/r)`, the
count over a uniform target azimuth has expectation exactly `W/S` and maximum `⌊W/S⌋+1`. The spec's
`n(r) = W/S + 1` (small-angle `W = 2b/r`) is the **maximum-count formula labelled as an
expectation**. My independent computation reproduces gamora's table to the digit at all six radii:
−46.0% / +11.6% / +23.8% / +62.9% / +116.8% / +156.4% vs the mean. **R-WR1-11's ruling is correct.**

The test does pin **both** sides, as claimed:
- it asserts the oracle's `(mean, min, max)` triple at all six radii, so the oracle cannot drift;
- it asserts the spec's ≤5% predicate **in the negative** (`dev_mean > 0.05`), so `n(r)` cannot be
  quietly tuned toward the oracle without the test going red;
- it independently pins the gapless boundary at 7.689 m and asserts min≥1 inside it, min=0 outside.

This is the correct construction for a halt-and-report. I would have written it the same way.

### 5 — TDM boolean guard: real

`raw_payload` line 389 reads `tdm = p.tdm_additive_multiplier if creature_tdm_applies_to_skill_rows
else 1.0`. Because the branch consumes **truthiness**, there are exactly two reachable multipliers —
`1.0` and `0.05`. No float value can produce a partial depth; `0.4` lands in Arm C identically to
`True`. The anti-fitting property R-M2-1 asks for is enforced by the *control structure*, which is
the right place for it (a type annotation alone would not be enforced at runtime). The test asserts
both the declared default's type and the truthiness-collapse behaviour. **Guard confirmed real.**

### 6 — Cold-DoT deviation vs the Gate-2 H-1 fidelity law: the deviation is *required* by H-1, not merely tolerated

I checked the implementation rather than the argument. `spatial_engine.py:4108–4123` ticks the rider
through `_gd_taken_elemental(raw, player_cold_resist)` — it is genuinely **resist-mediated**, which
is the whole point. Routing it through `effect_resolver.tick_effects` instead would (a) require
borrowing a fire/physical/shadow/chaos ailment name for a cold mechanic, putting a wrong element in
every emitted trace; (b) subtract `tick_damage` directly, **bypassing the exact `defensiveCold`
channel M-1 exists to itemize**; (c) apply RDR's ±15% to a flat GD rider and perturb a shared
stream. All three are "costume an RDR mechanic," which H-1 forbids. **I concur with the conductor's
acceptance, and I would go further: the ailment-layer route would have been the Gate-2 violation.**

### 7 — R2 two-endpoint bracket: the adverse side is actually adverse

Measured, not assumed. G-A's predicate is `W_pre ÷ W_post ≥ 1.50` (R-WR1-7).

| R2 endpoint | G-A ratio at r=5 |
|---|---|
| `R2_RESISTS_GATE_ADVERSE` (cold 0.14) — **the default** | **1.000** |
| `R2_RESISTS_LOW` (cold 0.00) — the named arm | 1.135 |

The default is the lower ratio, i.e. the harder gate. **Confirmed adverse.** One observation worth
the conductor's attention: *both* endpoints sit far below 1.50, so on this composed model at fixture
radius the bracket choice is **not load-bearing on the G-A verdict** — the gate misses either way.
That strengthens rather than weakens gamora's position (R-X-1: G-A grades once, on the post-wave
battery), and it means no one can later argue the bracket default cost the gate.

---

## ⛔ BLOCK-TIER FORWARD FINDING — R-WR1-11(b) may be unsatisfiable as ruled, and M-12b inherits it

**This is not a defect in `ddf51a8`.** `ddf51a8` shipped the spec's operator verbatim, halted, and
reported — exactly right. The problem lives in the ruling that resolves the halt, and gamora is
building against it *right now*.

R-WR1-11(a) converts `n(r)` from a scalar to a **per-event realized integer count drawn from the ray
geometry**. R-WR1-11(b) then requires that the ≥541 fixture blow "**must be REACHABLE at fixture
range**."

Using **gamora's own shipped `discrete_ring_oracle`** for the realized maximum, and the M-1 errata
regime (A = 358.36, cold 0.14) that produced the 524.28 reproduction:

| r (m) | realized max n | max delivered | ≥541? |
|---|---|---|---|
| ≤ 1.50 (inside the blast disc) | 16 | 2069.15 | **yes** |
| 1.60 | 7 | 764.15 | **yes** |
| 1.80 | 6 | 622.20 | **yes** |
| 1.81 – 2.49 | 5 → 4 | 518.50 → 414.80 | no |
| 2.50 – 2.70 | 4 | 909.15 | **yes** |
| 2.71 – 3.91 | 3 | 622.20 | **yes** |
| 3.92 – 7.9 | 2 | 414.80 | **no** |
| **5.0 (spec fixture radius)** | **2** | **414.80** | **NO** |
| **5.617 (the landing's live crossing)** | **2** | **414.80** | **NO** |
| 8.0 – 8.99 | 1 | 207.40 | no |
| 9.0 – 12.0 (the ×1.40 band) | 1 | 290.36 | no |

Exact band edges: reachable only for `r ≤ 1.804` and `2.50 ≤ r ≤ 3.919` (where `⌊W/S⌋+1` drops
through 6→5 and 3→2 respectively). Everywhere else in the 12 m footprint, ≥541 is unreachable at
*any* azimuth.

**At fixture range the realized *maximum* delivers 414.80 HP against a measured killing blow of
≥541 — a 23% shortfall that no azimuth can close.** Adding the entire mitigated cold-DoT rider
(60 × 0.86 = 51.6 over 2 s) still only reaches 466.4. The tail is not thin at fixture range; it is
**absent**. The ≥541 blow becomes reachable only at `r ≤ 1.804 m` or `2.50 ≤ r ≤ 3.919 m`.

Consequence: R-WR1-11(b)'s evidence form for G-B is satisfiable **only if the death-2 crossing
actually occurred inside ~3.92 m.** That is an empirical question with a known owner — galadriel has
already read frame 281 for G-8 — and it should be answered *before* M-12b's realized operator is
graded against G-B, not after. If the crossing was at 5+ m, then R-WR1-11 has resolved the n(r)
erratum correctly *and* dissolved the 541 reproduction in the same stroke, and G-B needs a different
evidence form (or the parameter set needs re-interrogation — e.g. whether `projectileUsesAllDamage`
or the band disposition contributes more than modelled).

**Escalation:** conductor (gandalf) + Matt. This is a ruling-level question, not a seam decision,
and it is exactly the class ADR-002 sends upward.

**Two smaller hazards M-12b also inherits (WARN):**

1. **The realized count introduces a second RNG consumer.** Today the nova draws *only* the 80%
   cast gate, from `self._gd_nova_rng` (already plumbed, `spatial_engine.py:2918`, consumed at
   `:4021`). An angular-offset draw per event MUST come from that same dedicated sub-stream. If it
   lands on the main stream, the "nova-free tiers stay byte-comparable against `_fix3`" argument —
   which is currently the *only* evidence for M-2's invariance, since no battery has run — is
   silently voided, and it will not be caught until the all-mechanisms re-run.
   **Second-order consequence, worth declaring up front:** adding a draw to `_gd_nova_rng` also
   shifts the *cast-gate* draw sequence, so this landing's live-fight figures (crossing at
   `t=1.951 s`, `r*=5.617 m`, `489.48` delivered) will not reproduce after M-12b. That is expected,
   not drift — but it should be declared in advance, in the same discipline R-WR1-12 applied to the
   telegraph flag, so nobody reads it later as a regression.
2. **R-WR1-11(c) converts the pinned negative test into "the erratum's tombstone."** The conversion
   must **keep the oracle's six-radius `(mean, min, max)` table as a positive pin.** That table is
   the geometric truth R-WR1-11 elevates to canon; if it leaves the tree along with the negative
   predicate, the ruling loses its own evidence.

---

## Notes (INFO — no action gating the landing)

1. **A derivation typo, now quoted into a binding ruling.** The gapless-boundary formula is written
   as `2r sin(11.25°) ≤ 1.5 ⇔ r ≤ 7.645` in three places (build note §3.4, `gd_nova.n_projectiles`
   docstring, and the divergence test's docstring). **As written that inequality yields 3.844.** The
   correct forms are `r sin(11.25°) ≤ 1.5 ⇒ r ≤ 7.689` (exact perpendicular) and `r·θ ≤ 1.5 ⇒
   7.639` (arc approximation). The *code* is right — the test asserts
   `explosion_radius / sin(spacing/2) = 7.689` and its inline comment distinguishes the two forms
   correctly — and R-WR1-11 quoted the right number (7.69). Only the prose derivation is wrong, and
   it should be repaired because a charter ruling now cites it.
2. **A test docstring over-claims relative to its assertions.**
   `test_INTEGRATION_no_nova_no_change__the_seam_is_inert_when_unarmed` says "the fight takes the
   pre-M-2 path exactly," but both arms run `with_nova=False` **post-landing**. The assertions
   establish seed determinism, not invariance against the pre-landing baseline. The real invariance
   evidence is elsewhere and is good (T-M1-6 for M-1; sub-stream separation + the diff-empty
   regression for M-2). Recommend the docstring be narrowed to what it proves.
3. **`_player_death_element = "cold"` is pinned, not computed** (`spatial_engine.py:4147`), even
   though `by_element` is in scope on the same line. It is empirically right at the modelled radii
   (cold is ~83% of delivered post-mitigation) and the comment declares it — but it flows into
   `replica_frame_emitter` and `FightResult.player_death_element`, i.e. into emitted traces drax and
   star-lord read. Discipline #9: derive it from `by_element` rather than pin it.
4. **`nova_substream`'s "disjoint by construction" overstates.** XOR-with-a-constant guarantees a
   *distinct* seed and therefore an independent stream — not disjointness (two fights whose seeds
   differ by the salt would share streams). The load-bearing claim ("the main stream is untouched on
   nova-free tiers") is true, separately tested, and unaffected. Wording only.
5. **Cold-DoT state is engine-scoped, not target-scoped**
   (`self._gd_nova_cold_dot_remaining_s` / `_rate`). Correct for the modelled scope — `resolve_tick`
   is passed only the player — but it will misattribute the instant the nova is pointed at more than
   one target. Worth a comment pinning the single-target assumption.
6. **Supporting observation for R-WR1-12's verification clause.** I inspected all three
   `_emit_telegraphs` gate sites (`4049`, `5309`, `6845`). Each gates **buffer appends and sink
   calls only** — no combat-state mutation, no RNG draw. The nova's telegraph path calls
   `nova_delivered`, a pure function. This is consistent with "the flag is EMISSION-ONLY," though a
   full purity audit of the generic `_mint_telegraph_spec` remains the conductor's clause to close
   before the baton fires.

---

## Rationale

**Discipline #1 (math before code)** is satisfied in its strongest form here: the spec *is* the math
note, the build note is an honest build-side ledger, and every deviation is in §1 or §3.4 with none
silent. **Discipline #12** is satisfied — three semantic shifts and one deviation are declared at
the top of the commit message, not buried. **ADR-004** is satisfied: MIGRATION.md carries the two
named parse risks (`calibration_override_fields` gaining two names; nova `attack_id` gaining a third
colon-separated segment) for star-lord and drax, with the correct "star-lord owes NOTHING to ship"
framing.

The behaviour that earns this landing a PASS is the one it would have been easiest to skip: gamora
built the falsifier R-M2-4 required, discovered it destroys the spec's own strongest validation,
**shipped the spec's operator anyway**, and pinned the disagreement so neither side can move. That
is Principle 1 and Discipline #11 working exactly as designed, and it is why the run now has a
correct ruling (R-WR1-11) instead of a flattering number. The BLOCK-tier finding above exists
*because* gamora halted rather than fitted.

Gate-2 was correctly **not** self-cleared (charter §8, per-landing law).

---

## Action

- [x] **jack-ryan:** verdict **PASS-with-notes** on `ddf51a8`. Nothing in the landing needs to be
      reverted or re-tagged.
- [ ] **gandalf (conductor) — BLOCK-tier, before M-12b is graded against G-B:** rule on whether
      R-WR1-11(b) is satisfiable. At fixture range the realized maximum is 414.80 vs ≥541. Either
      (a) establish the death-2 crossing radius empirically (galadriel; reachable band is
      r ≤ 1.804 m or 2.50–3.919 m), or (b) restate G-B's evidence form again.
- [ ] **gamora (M-12b), WARN:** draw the realized count's angular offset from `nova_substream`, not
      the main stream. Preserve the oracle's six-radius `(mean, min, max)` table as a positive pin
      when the negative test converts to a tombstone (R-WR1-11(c)).
- [ ] **gamora, INFO (housekeeping, any convenient landing):** repair the `2r sin(11.25°)` typo in
      the three prose sites; narrow the `no_nova_no_change` docstring; derive `_player_death_element`
      from `by_element`; soften "disjoint by construction"; pin the cold-DoT single-target
      assumption.
- [ ] **Matt (ESCALATE):** aware only. The BLOCK-tier item is a conductor ruling in flight, not a
      seam decision. It reaches you if R-WR1-11(b) cannot be satisfied and G-B's evidence form has
      to change a second time.

---

## References

**Engine (`ddf51a8`, read-only):**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/gd_mitigation.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/gd_nova.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py` (`_mitigate_physical` / `_mitigate_elemental`, ~:1372)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/combatant.py` (`mitigation_law`, :297)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (:4040–4195 nova resolve + cold DoT)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/calibration_overrides.py` (`_coerce_mitigation_law`, :257)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/wr1-m12-gd-mitigation-nova-2026-07-29.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (2026-07-29 entry)
- `/Users/admin/Games/reincarnated-engine/tests/test_wr1_m12_gd_mitigation_nova.py`

**Meta-repo:**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-28-wr1-build-m12.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/design-inputs/2026-07-28-wr1-m123-specs.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-28-wr1-wave-relay-run-charter.md` (§8.8 R-WR1-8; §8.9 R-WR1-11 / R-WR1-12)

*Filed by jack-ryan, WR1-G2-M12. Read-only on the engine tree; the builder writes, the reviewer
reads (LAP0 precedent).*
