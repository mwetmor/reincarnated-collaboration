# Gate-1 Disposition — 2026-07-06 — batch-2 Leg A economy-axes math note

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1 pre-fire)
**Disposition:** **RATIFY-WITH-CONDITIONS**
**Target:** `reincarnated-engine/src/reincarnated/generation/notes/legA-economy-axes-math-2026-07-06.md` (no code, no tag)
**Developer:** rocket (generation seam) + gamora adjacency (sim-binding, parallel consult)
**Governing spec:** `canonical/reap-die-rise-engine/batch2-build-spec-2026-07-06.md` §2/§3/§5/§8
**Dispatch:** `agentic_orchestration/dispatches/2026-07-06-rocket-batch2-legA-economy-axes.md`
**Principles applied:** 1 (math-before-code), 3 (cross-seam impact), 4 (decisions-log truth), 6 (cross-seam round-trip)
**Disciplines applied:** #1 (math-before-code), #1.2 (code-citation), #11 (empirical inspection), #24 (sweep-isolation)
**ADRs applied:** ADR-002 (tiered approval), ADR-004 (MIGRATION.md cross-seam)

---

## Disposition summary

**RATIFY-WITH-CONDITIONS.** The math note is sound, honest, and code-cited. I independently
verified every load-bearing `file:line` citation (Discipline #11 — did not take them at face
value); all reconcile. The three axes are well-formed, the sweep-isolation audit is clean, the
structural-honesty invariant is genuine (not rigged to pass), the cross-seam FINDING is correctly
escalated (not silently added), and LHS-within-6-strata is the right sampling call. **Route B is
the correct binding route** on process/contract grounds.

**One Gate-1 finding requires resolution before Leg-B fires (Condition C1 below): the "18-cell"
enumeration the build rests on does NOT reconcile as written, but the defect is a doc/vocabulary
gap in the governing spec, not in rocket's note.** Details in the cell-enumeration section. The
remaining conditions (C2–C4) are binding-but-light — they attach process rigor to the Leg-B build,
they do not gate the Leg-A note.

The economy axis is **not** a decisions-log conflict (Principle 4): it operationalizes the
Matt-ruled Q1(a) axis framing verbatim; no locked decision is contradicted.

---

## 1. Math-before-code + code-citation (Discipline #1 / #1.2) — VERIFIED CLEAN

I byte-checked the load-bearing citations against the engine tree this session:

| Claim (note §1.0) | Cited | Verified value in tree | Verdict |
|---|---|---|---|
| `_ENERGY_COST` table | `per_skill_emitter.py:170` | `{1:10.0, 2:20.0, 3:30.0, 4:40.0}` | ✓ exact |
| `_COOLDOWN` table | `per_skill_emitter.py:174` | dict keyed `(tier,role)` | ✓ |
| `_CAST_TIME` table | `per_skill_emitter.py:194` | `{1:0.3, 2:0.5, 3:0.7, 4:1.0}` | ✓ exact |
| emitted cost/cooldown consumed | `:609,610,611` | `energy_cost=_ENERGY_COST[tier]` etc. | ✓ |
| cost-check gate | `combatant.py:388-393` | line 392 `if self.mana < effective_cost` | ✓ (method spans 388+) |
| stat-derived regen (no field) | `combatant.py:644` | `compute_mana_regen(5.0, INT, WIS)` | ✓ exact |
| gear-only per-kit modulation | `gear_schema.py:377-384` | `combined_ability_modifiers`, `_MULTIPLICATIVE={cooldown_factor, energy_cost_factor}` | ✓ |
| T4 precedent (kit-declared field) | `combatant.py:293,680-684,951` | `t4_cost_resource:str="mana"` + `gamora_combatant_fields` extraction | ✓ |
| Leg-1 salts (`+500`, `+900_000`) | leg1 note §4.1/§4.3 | `season_generation_pipeline.py:952-959` `+500`; role-split `+900_000` | ✓ |

**Range justifications are not hand-wavy.** Each bound is argued from a concrete pool/regen
arithmetic against the max-INT chassis (`c=0.60` → T1 casts ~53× on a 320 pool; `c=1.60` → T3 nuke
~6.7 casts; upper cutoffs justified as "adds no information the wall already probes"). `BETA=0.25`
fixed with a stated confound rationale (§1.1). `RAMP=0.04` justified against the 240s fight window.
This is the standard I hold Discipline #1 to. **No hand-waving found.**

INFO (non-blocking): §1.0 cites the cost-check as `combatant.py:388-393`; the actual `mana <`
comparison is line 392. Immaterial — the method genuinely begins at 388. Noting for the record only.

## 2. Sweep-isolation (Discipline #24) — AUDIT CLEAN

The confounded-pair audit (§4) holds under scrutiny:

- **E1 ⊥ E3** — cost writes `energy_cost`; cadence writes `cooldown_seconds`. Disjoint emitted
  fields. Pool-coupling at fight time is the economy itself, not a *parameter* confound. Correct
  distinction; correctly drawn. ✓
- **E1a ⊥ E1b (BETA fixed)** — the argument is right: a *continuous* slope knob would alias with
  `c` at tier-1 (both scale the tier-1 cost multiplicatively). Fixing `BETA=0.25` makes `s` a clean
  2-level categorical and `c` a clean continuous factor — they cannot alias because `s` moves only
  the tier-*slope*, not the tier-1 anchor. The reason `BETA` is not itself an axis is exactly the
  isolation reason, correctly named. ✓
- **`_CAST_TIME` excluded** — cadence (`how often can I start a cast`) and cast-time (`how long a
  cast occupies me`) are two throughput handles; making both axes double-counts throughput and
  confounds E3. Excluding cast-time as the fixed physical floor is the correct call, and it mirrors
  the Leg-1 geometry-jitter exclusion (same isolation logic). ✓ The note also correctly flags that
  `k<0.70` mostly hits the cast-time floor and stops mapping new space — a real reason the lower
  bound sits at 0.70, not lower.
- **Not overloaded onto `gamora_combatant_fields`** — verified: that channel is T4-keyed
  (`t4_alteration_output` → extraction at `combatant.py:680-684`). Routing economy through it would
  couple the economy sweep to the T4 sweep. Discipline #24 forbids it; the note correctly demands a
  separate channel. ✓
- **The one adjacency the note self-flags** — `on_kill` regen (E2) couples to trash *density*
  (a shell/encounter property, not a Leg-1 axis), so E2 must be swept across BOTH shells. Correctly
  identified and handled by the Leg-B two-shell design. ✓ This is the sharpest catch in the note.

**Confounded-pair audit result: NONE. Confirmed.** The Leg-B map will be interpretable.

## 3. Structural-honesty clause (spec §3) — INVARIANT GENUINE, RANGES NOT PRE-BIASED

This is the load-bearing check: are the axes rigged to pass? **No.** Verified two ways:

1. **The default corner is a byte-verified KNOWN FAILURE.** At `{c=1.0, s=flat, g_flat=1.0,
   RAMP=0.0, k=1.0}` the emitted tables are *identical* to today's `_ENERGY_COST` /
   `compute_mana_regen(5.0,...)` / `_COOLDOWN` (I verified the defaults reproduce the cited tables
   exactly). The current chassis reads 0.0 KPM on both shells (gamora §2.3, floor 9.90/11.65,
   byte-verified `db2df69`). So the **center of the axis cube is a measured failure**, and the
   ranges span *outward* from it. §7 composition rule 4 hard-wires this as a regression anchor:
   any Leg-B run MUST reproduce the 0.0-KPM timeout at the default corner or the binding is wrong.
   That is a built-in refutation check, which is exactly what a non-rigged pilot needs.

2. **The ranges are symmetric-about-baseline, not tilted toward clear.** `c∈[0.60,1.60]` around
   1.00; `g_flat∈[0.60,1.80]` around 1.00; `k∈[0.70,1.50]` around 1.00; `RAMP∈[0.0,0.04]` with 0.0
   = baseline. There is no floor of the range that is itself a guaranteed clear — the note even
   names an *expected-to-FAIL* region (glass-economy, §3) as a deliberate negative anchor, which is
   the tell of an honest map (a rigged map has no expected failures).

**The HALT stays genuine.** If no composition clears, spec §3's designed HALT fires with the
measured landscape, and the problem is correctly located below the economy layer. The note does not
bake in a clear it cannot prove exists (§1.4, §8 refutation ledger). **Structural-honesty clause: PASS.**

## 4. Cross-seam contract FINDING (§5) — CORRECTLY ESCALATED; Route B is the right call (process angle)

**Correctly escalated, not silently added.** The note surfaces the required `resource_economy`
kit→sim loadout field as a FINDING (§5) and routes it to knight-rider as a Gate-1 item, per the
dispatch's Principle-6 gate (dispatch line 36) and ADR-004. No field, no MIGRATION.md, no code lands
in this dispatch. The `Round-trip: not applicable — no contract field added` justification is valid
per Principle 6 clause (ii) (the change is *not yet made*; math-design-only). This is textbook
handling of a cross-seam contract change at the design stage. ✓

**Route A vs Route B — my read (process/contract-discipline; gamora owns the sim-side technical call):**

**Route B is correct on process grounds.** Three reasons, all Discipline-#24 / ADR-004 flavored:

1. **Sweep-isolation legibility.** Route A bakes `c·slope` and `k` into the *emitted per-skill*
   `energy_cost`/`cooldown_seconds`. That hides the economy axis *inside* skill values — to know
   what `c` a cohort ran, you would back it out of per-skill cost. Route B keeps the full triple in
   ONE inspectable loadout dict, which is the clean per-cohort measurement surface Discipline #24
   wants. For a *map*-producing pilot, reading the axis directly off the loadout beats reverse-
   engineering it from baked skill values.
2. **Precedent parity.** `t4_cost_resource` is verified in-tree (`combatant.py:293` field,
   `:680-684` extraction, `:951` construction) as exactly this kind of object — a kit-declared
   field the sim consumes to shape resource behavior. Route B is a *sibling* of an existing
   contract, not a new *kind*. New-kind contracts carry more architectural risk; sibling contracts
   are the low-blast-radius choice ADR-004 prefers (backward-compat additive dict).
3. **Route A is internally incoherent for E2 anyway.** The note correctly shows regen is
   stat-derived in-sim (`combatant.py:644`) with no emitted field to bake into, and `on_kill` needs
   a kill-event mana-add hook. So Route A *already* requires a new regen loadout field + the hook —
   it does not actually avoid the contract change, it just splits the economy across two
   representations (baked cost/cadence + a regen field). Splitting the axis representation is the
   worse sweep-isolation surface. Route B unifies it for the same contract cost.

**Process caveat (this is why the disposition is RATIFY-WITH-CONDITIONS, not clean RATIFY):** the
final Route A/B call and the kill-hook-triviality confirmation are **gamora's sim-side technical
call** (parallel consult in flight), not mine. My ratification of Route B is on the *contract-
discipline* axis. If gamora's technical read surfaces a sim-side reason Route B is more expensive
than the note assumes (e.g., the kill-event hook is non-trivial, or combatant-init ordering makes
a single-read modulation awkward), that is a legitimate override — the note itself says "gamora
concurs or overrides." **Condition C2** records this: the Route decision is ratified as B *pending
gamora's technical concurrence*; a gamora override to Route A is not a Gate-1 re-open, it is the
adjacency working as designed.

**MIGRATION.md + round-trip deferred to the Leg-B build — correct per ADR-004.** ADR-004 requires
the MIGRATION.md *before tagging* the change, and Principle 6 requires the round-trip smoke *when
the completion record lands*. Neither triggers on a design-only note that adds no field. Authoring
them WITH the Leg-B build code (after Gate-1 ratifies the route) is the same discipline the Leg-1
note followed for the `proxies` population-behavior change. ✓

## 5. §8 CELL-ENUMERATION VERIFICATION NOTE (Matt-required) — DOES NOT RECONCILE AS WRITTEN → Gate-1 FINDING (Condition C1)

**Verdict: the "18 BC cells" of the full fresh emission does NOT reconcile against the engine's
actual enumerable BC-cell space as a literal count, and the reconciliation gap lives in the
GOVERNING SPEC's vocabulary, not in rocket's note. This is a Gate-1 finding. It does not block the
Leg-A math, but it must be resolved before Leg B fires (and certainly before Leg C).**

### (a) What the engine's actual BC-cell space is

The BC archive is an **8-axis discretization** totaling **68,040 cells** at full resolution
(`canonical/reap-die-rise-engine/qd-engine-bc-axes-lock-2026-05-20.md:28,95,601`:
`6×5×3×3×3×3×4×7 = 68,040`). Every emitted kit targets an 8-tuple
`(eng_bin, geo_bin, proxy_bin, ctrl_bin, tempo_bin, var_bin, def_bin, econ_bin)`
(`bc_target_source.py:120,197`; consumed at `bc_target_composer.py:315`). **There is no "18-cell"
constant anywhere in the generation code** — I grepped the generation tree; the only cell-scoping
constant is `_DEFERRED_PROXY_BINS` (`bc_target_composer.py:97`), which gates proxy bins, not an
18-cell roster. Batch-1 emitted into **7 BC cells** (serial-content tracker: "700 gauntlet-passed
kits @ 38.9% yield (7 BC cells × 100)"). So the enumerable space is 68,040; the batch-1 realized
subset was 7.

### (b) What the "18" actually is

The "18" is a **Matt-ruled demo-roster composition model**, NOT a subset-enumeration of the 68,040
space. Source: `faction-derivation-stack-spec-2026-07-06.md` §5 line 83 — *"Roster = 18 kits = 18 BC
cells, exactly 1:1. Every mechanical voice in the engine's space is present exactly once"* — built
across three Matt iterations (4-zone/20-kit → 18-kit; §5 line 72). The 18 is a **roster tiling
target** (3 zones, 4 rotating factions, the demo's playable cast), not a count of the discretized
axis space. The derivation-stack §3 phrasing — *"Full 18-cell emission — every BC cell populated at
the corpus floor"* — **conflates two distinct objects**:

- **Object 1: the enumerable BC space** = 68,040 cells (or the far smaller *realized-viable* subset
  the gauntlet admits — batch-1 realized 7).
- **Object 2: the demo roster** = 18 kits chosen to tile 18 distinct mechanical voices 1:1.

"Every BC cell populated" (Object 1 language) and "18 cells" (Object 2 count) cannot both be
literally true — 68,040 ≠ 18. The spec is using "18-cell emission" as shorthand for *"the emission
that yields the ~1,800-kit population (≥100/cell × 18 target roster cells) from which the 18-kit
roster and the 30–50 faction library are derived"* (derivation-stack §3 line 23: "~1,800-kit
population"). The **math is self-consistent** (18 cells × ≥100/cell ≈ 1,800), but the *word* "cell"
is doing double duty — sometimes meaning a point in the 68,040 discretization, sometimes meaning one
of the 18 roster-target voices.

### (c) Does the Leg-B pilot cell selection map correctly into it?

**Yes, the Leg-B selection is representative and maps correctly — this half reconciles cleanly.**
Spec §3 selects 2–3 pilot cells: **1 plain-caster (proxy ~0, the floor test)**, **1 summoner (proxy
≥0.25, the C2 band-2 cert)**, optional hybrid (§8 D2). These are drawn from the **INT-band** of the
target space (the economy axes ride INT-band kits per note §0). The plain-caster cell probes
`proxy_bin=solo`; the summoner cell probes `proxy_bin∈{proxy-light,proxy-heavy}` — the exact bins
`_DEFERRED_PROXY_BINS` gated and batch-2 un-gates. The two cells span the proxy-share axis's two
C2 bands (the whole reason C2 exists), and the economy axes are orthogonal to proxy-share (note §7
rule 3: economy ⊥ G4). So the pilot cells are a *representative* slice of the caster region the
18-target roster must eventually tile. **The pilot-cell → target-space mapping is sound.**

### (d) The finding

The **count reconciliation fails at the vocabulary layer**: "18 BC cells" is a roster-target count,
not an enumeration of the 68,040-cell discretized space, and the derivation-stack §3 phrase "every
BC cell populated" reads as if the two are the same object. **rocket's note is not at fault** — it
correctly scopes the economy axes to INT-band kits and never claims to enumerate the 18; it inherits
the "18-cell" phrase from the spec. **The fix belongs in the governing spec**, not in rocket's note.

**This matters for Leg C, not Leg A/B.** The Leg-A math is unaffected (axes are defined on INT-band
kits regardless of how many roster cells exist). The Leg-B pilot is unaffected (2–3 named cells,
explicitly enumerated, verified representative in (c)). But **before Leg C fires the "full fresh
18-cell emission," the spec must state which 18 target cells are meant** — the enumerable identity
of the 18 (which 8-tuple regions), how they map onto the 68,040 space, and the relationship between
"18 target cells" and "≥100 gauntlet-passed kits/cell." Without that, Leg C's yield-planning and the
derivation's "every mechanical voice present exactly once" claim rest on an unenumerated set.

**Condition C1 (see below) records this as a spec-vocabulary finding routed to gandalf (SPEC-AUTHOR)
via knight-rider.** It is NOT a BLOCK on Leg A — it is a Gate-1 flag that must close before Leg C.

## 6. Sampling scheme (§8 D4) — LHS-within-6-strata RATIFIED

**Ratified.** The reasoning is correct:

- A full grid at 4 continuous points × 2 slope × 3 regen-shape = **384 cells**, ~15× the ~25/cell
  Leg-B budget (spec §3). Infeasible at pilot scale, and it wastes samples in corners the
  identity-region analysis (§3) already predicts are dead. Correct rejection.
- LHS gives even marginal coverage of each continuous axis (`c`, `k`, regen-magnitude) at ~25
  samples, decorrelating the continuous axes by construction (near-orthogonal columns) — which
  directly serves Discipline #24 (readable single-axis gradients). Correct.
- Treating the categoricals (`s`×`r` = 6 strata) as *strata* rather than LHS columns, and running
  continuous-LHS *within* each stratum (~4 samples/stratum → ~24/cell), is the right structure for
  a small-N pilot whose job is *coverage that reveals whether a viable region exists*, not a precise
  response surface. Correct.
- The rejected alternative (sparse grid on `c`,`k` holding regen flat) is correctly rejected —
  holding regen flat pre-decides the builder-spender (`on_kill`) hypothesis is irrelevant, which is
  precisely the caster-vs-trash question. Keeping regen-shape in the search is right.

INFO (non-blocking): at ~4 continuous-LHS samples per stratum the marginal-effect estimates per
stratum are *thin*. The note acknowledges this ("thin, but the pilot's job is coverage"). Acceptable
for a GO/HALT-region pilot; if the pilot GOs, Leg C densifies the identified viable stratum (note §6,
spec §4). No condition — just flagging that per-stratum statistical power is coverage-grade, not
inference-grade, which the GO/HALT criterion (contiguous *region*, not point-significance) tolerates.

---

## Binding conditions

- [ ] **C1 (spec-vocabulary finding, routed to gandalf via knight-rider; closes before Leg C, NOT
      Leg A):** The "18 BC cells" / "full 18-cell emission" language conflates the 68,040-cell
      enumerable BC space (Object 1) with the 18-kit demo-roster tiling target (Object 2). Before
      Leg C fires, the governing spec (or derivation-stack §3) must enumerate the identity of the
      18 target cells (which 8-tuple regions), their mapping onto the 68,040 space, and the
      "18 cells × ≥100 kits/cell ≈ 1,800 population" arithmetic. Leg A and Leg B are unaffected
      (pilot cells are explicitly named + verified representative, §5(c)).
- [ ] **C2 (Route B ratified pending gamora concurrence):** Route B (single additive
      `resource_economy` loadout dict) is ratified on contract-discipline grounds. gamora's
      parallel sim-binding consult owns the final technical call + the kill-hook-triviality
      confirmation. A gamora override to Route A (for a stated sim-side reason) is the adjacency
      working as designed, NOT a Gate-1 re-open. Whichever route lands, it carries a MIGRATION.md +
      round-trip smoke authored WITH the Leg-B build code (ADR-004 / Principle 6).
- [ ] **C3 (Leg-B build carries the round-trip):** When the `resource_economy` field lands in the
      Leg-B build, the completion record must show the round-trip smoke: kit emits `resource_economy`
      → sim reads it → economy modulates a fight → default-corner regression check reproduces the
      0.0-KPM timeout (note §7 rule 4). Gate-2 verifies this at the Leg-B commit (Principle 6 Gate-2
      check). Missing it is a WARN→BLOCK.
- [ ] **C4 (default-corner regression anchor is a hard Leg-B pass-gate):** The note's built-in
      refutation check (§1.4, §7 rule 4) — any Leg-B run reproduces 0.0 KPM at
      `{c=1.0, s=flat, g_flat=1.0, RAMP=0.0, k=1.0}` — must be an explicit, checked assertion in the
      Leg-B pilot, not just prose. If the default corner does NOT reproduce the known failure, the
      binding is wrong and the pilot HALTs on integrity grounds before any GO/HALT read.

---

## Action

- [ ] rocket: no action required on the Leg-A note — it is ratified. Carry C2/C3/C4 into the Leg-B
      build coordination with gamora.
- [ ] knight-rider: route C1 to gandalf (SPEC-AUTHOR) as a spec-vocabulary finding to close before
      Leg C; carry C2 (Route B pending gamora) into the Leg-B build dispatch.
- [ ] gamora: sim-side Route A/B call + kill-hook triviality confirmation (parallel consult; C2).
- [ ] Matt (informational, no decision needed at Gate-1): Leg A ratified-with-conditions; the only
      finding that needs eyes before Leg C is C1 (the 18-cell enumeration vocabulary gap). Not a BLOCK.

## References

- Note under review: `reincarnated-engine/src/reincarnated/generation/notes/legA-economy-axes-math-2026-07-06.md`
- Governing spec: `canonical/reap-die-rise-engine/batch2-build-spec-2026-07-06.md` §2/§3/§5/§8
- Derivation-stack (18-cell roster model): `canonical/reap-die-rise-engine/faction-derivation-stack-spec-2026-07-06.md` §3/§5
- BC axes lock (68,040-cell enumeration): `canonical/reap-die-rise-engine/qd-engine-bc-axes-lock-2026-05-20.md` :28,95,601
- Dispatch: `agentic_orchestration/dispatches/2026-07-06-rocket-batch2-legA-economy-axes.md`
- Code verified: `per_skill_emitter.py:170,174,194,609-611`; `combatant.py:388-393,644,680-684,951`; `gear_schema.py:377-384`; `bc_target_source.py:120,197`; `bc_target_composer.py:97,315`
- Leg-1 pattern precedent: `generation/notes/leg1-summon-genpath-int-variation-math-2026-07-06.md` §4; salts `season_generation_pipeline.py:952-959`
- Serial-content tracker (7-cell batch-1, 18-cell batch-2 language): `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md`

**Signed:** jack-ryan, 2026-07-06 — Gate-1 DESIGN-MODE, RATIFY-WITH-CONDITIONS. The math is honest and
the axes are not rigged to pass. The one finding is a spec-vocabulary gap (18 ≠ 68,040), inherited from
the spec, closes before Leg C. Route B is right on contract grounds; gamora owns the technical override.
