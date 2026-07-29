# Finding — 2026-07-29 — WR1-G2-M4TO9 (gamora Z.4 build wave, five landings)

**Reviewer:** jack-ryan (DEV-MODE, read-only)
**Severity:** PASS-with-notes (overall) — per-commit verdicts in §0
**Target:** engine `2456b20` → `1e5b136` → `a110890` → `3183efb` → `a42d052` (tip)
**Developer:** gamora
**Run / cell:** WR1-2026-07-28 · WR1-BUILD-M4TO9 · conductor gandalf (`RUN-CONDUCTOR`)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact), 5 (severity),
6 (cross-seam round-trip) · **Disciplines:** #1, #2, #8, #10, #12 · **ADR-004**
**Method:** every headline claim RE-MEASURED on my own instruments in clean worktrees
(`/tmp/jr_wr1_base` @ `7a5eb88`, `/tmp/jr_wr1_tip` @ `a42d052`). No engine mutation; both
worktrees and one synthetic probe file removed at close. Engine tree verified clean
(`git status --porcelain -- src/ tests/` empty, before and after).

---

## §0 — VERDICT PER COMMIT (per-landing law, charter §8.13 Z.4)

| commit | mechanism | verdict |
|---|---|---|
| `2456b20` | M-9 + M-7(b) | **PASS** |
| `1e5b136` | M-6 | **PASS-with-notes** (WARN-A) |
| `a110890` | M-4 | **PASS** |
| `3183efb` | M-5 | **PASS-with-notes** (WARN-B, WARN-C) |
| `a42d052` | A-EFF-1 scoping | **PASS** |
| — | wave-level | **WARN-D** (P-5 discharge route, pre-battery) |

**OVERALL: PASS-with-notes. The lane is open — the post-wave battery may fire.**
No finding moves a number, and nothing here contaminates a 150-fight battery's *arithmetic*.
Two findings (WARN-A, WARN-D) land inside the battery's own artifact of record and are
cheapest to close BEFORE it fires. WARN-B must close before the baton / G-D. WARN-C is a
guard-strength item with no live violation and may ride.

---

## §1 — CLAIM 1: THE BYTE-IDENTITY CHAIN — REPRODUCED, AND THE NORMALIZATION IS NOT OVER-BROAD

**What I did (not what I read).** Two clean worktrees at `7a5eb88` and `a42d052`; `--smoke` into
separate `--out-dir`s; comparison by my own normalizer, not the builder's.

**Traces — the tighter test.** I stripped exactly three keys — `crit`, `crit_multiplier`,
`hp_provenance` — plus volatile `fight_id` / `created_at`, and nothing else. Result: 5/5 trace
files **line-for-line identical**, combined digest `63233e8bf581` on both sides.

This is the audit the conductor asked for. An over-broad normalization hides drift by stripping
more than it declares; I stripped *only the three declared additive keys* and still got identity,
which proves the additive set **is exactly those three** and that no fourth field moved under
cover. The normalization is tight, not generous.

**Report, pre-existing surface.** Identical except one list: `static_assertions_passed` grows
10 → 12 (`A-HP-4` and `A-EFF-1` added; `A-HP-3` and `A-FRZ-1` labels extended). **No number
moves anywhere in the report.**

**Environmental deltas confirmed environmental:** `engine_git_hash` (`7a5eb88` → `a42d052`) and
`trace_path` (my two out-dirs). Both are properties of *where I ran it*, not of what ran.

**VERDICT: the five-tree byte-identity spine holds on the pair I measured.** M-9 and M-6 are
class-(B) as claimed. Discipline #12's "measured, not asserted" is discharged.

---

## §2 — `2456b20` (M-9 + M-7b): **PASS**

### 2.1 No silent state — verified by exhaustion, not by reading

`set_effect_name_policy` accepts `warn` and `strict` and **refuses `silent` / `off` / `none` / `""`
with `ValueError`**. Default is `warn`. There is no third state to fall into. ✓

### 2.2 The AST guard pins the literal set against the ladder

`_effect_loop_chain` walks the `elif` chain *structurally* — `name == "x"` contributes `"x"`,
`name in ("a","b")` contributes both, `name in AILMENT_NAMES` (a `Name`, not a literal)
contributes nothing and is the registry-derived half by construction. It then asserts set
equality against `_HANDLED_EFFECT_LITERALS`, asserts the `else` exists, and asserts the `else`
calls `_on_unhandled_effect_name`.

**T-M9-2b is the right shape for a guard's own falsifier:** it proves the *extractor's*
sensitivity against a **synthetic source string**, not by mutating the kernel. A test that edits
the real module to prove itself is a test that can leave the module edited. Correct instinct.

**The dispatch-dict rejection is the right call.** A refactor of the hottest loop carries real
byte-identity risk to fix a bookkeeping problem a 30-line test solves. Discipline #10.

### 2.3 A-FRZ-1 is executable and REFUSES CORRECTLY — four independent probes

I drove violating fixtures through `assert_static_pins` myself rather than trusting the suite:

| probe | result |
|---|---|
| `{"name":"freeze"}` on player kit | **REFUSED** — `A-FRZ-1: a 'freeze' emitter was compiled at player kit skill feral_claws_r16` |
| `{"name":"freeze"}` on a **mob** | **REFUSED** — `... at trash mob zombie_a01_0` (mob-side leg live) |
| `{"name":"chill","params":{"label":"freeze"}}` | **REFUSED** |
| `{"name":"chill","params":{"element":"freeze"}}` | **REFUSED** |
| `{"name":"chill","params":{"shatter_damage_percent":0.20,"shatter_threshold_fraction":0.25}}` | **REFUSED** — leg (ii) live |

The last row is the load-bearing one and it passes at **the exact nesting the engine reads**
(`effect_resolver.py:245-246` reads `effect.params.get("shatter_threshold_fraction"/
"shatter_damage_percent")`; the guard reads the same `params` dict). The renamed-ailment threat
model — *a burst operator by another spelling* — is genuinely covered.

`--arm-freeze-shatter` makes it a **gate, not a wall**, and the disarm lands in the artifact's own
assertion list (`A-FRZ-1 ** DISARMED ** ... This artifact is a shatter experiment, NOT a guarded
battery`). An artifact produced disarmed cannot be mistaken for a guarded one. Good.

### 2.4 INFO — A-FRZ-1 matches `freeze` EXACTLY, not as a substring

`"freeze" in (nm, el, lbl)` is exact membership. A name like `deep_freeze` slips A-FRZ-1 — it was
refused in my probe, but **by A-DOT-1** (unknown dispatch name), one guard upstream. Today the
coverage is total because A-DOT-1 runs first and the registry names are enumerated. It stops being
total the moment the registry gains a name *containing* `freeze` as a substring. Recorded, not
prescribed.

---

## §3 — `1e5b136` (M-6): **PASS-with-notes**

### 3.1 Re-measured and reproduced

- **P-2 satisfied:** all **269** damage records on the smoke traces carry non-null `crit`.
  `crit_multiplier` is `float` on the 13 crits and `None` on the other 256 — exactly the
  `false`/`null`-by-meaning contract MIGRATION documents.
- **Per-tier crit reads reproduce to the digit:** 1/9 · 0/8 · 2/26 · 5/73 · 5/73. All five.
- **Fixture `crit_chance = 0.0411`** is the play-test's own `66/1606 = 0.041096` — sourced at
  `kitcal_g5_scenarios.py:319` with a `[MEASURED, run-aggregate]` provenance comment. The
  "the sim player has been critting invisibly" finding is real.
- **`crit_multiplier` is read from attacker state, never back-computed** — verified at source
  (`spatial_engine.py:4503-4507`: `CRIT_DAMAGE_MULTIPLIER + attacker.combatant_state
  .ability_modifiers["crit_bonus_damage"]`). A back-fitted multiplier would silently absorb every
  other term on the path and read as a crit factor. The builder names that hazard and avoids it.
- **Discipline #12 exposure claim re-measured independently.** I grepped `output/` myself:
  **one** file contains the literal `on-crit`, and the hit is the substring inside
  `non-criterion`. Zero real occurrences. Byte-identity holds on every reachable state, and the
  "on-crit is a live `PROC_TRIGGER_CONDITIONS` member with no producer" wake-up is honest.

### 3.2 MIGRATION.md adequacy for drax (ADR-004 / Principle 6) — **ADEQUATE, parseable cold**

I read the entry as drax would, with no wave context:

- **Crit keys:** producer table (`on_hit` vs `dot`), the `false`/`null` semantics stated as
  *by meaning, not by default*, the KF-5 v1-additive precedent cited, an explicit
  **consumer-safety** clause ("a consumer that ignores both keys is byte-identical to its pre-M-6
  behaviour; a consumer that reads them must treat `crit_multiplier = null` as *did not crit*, not
  as zero"), and an explicit "star-lord owes nothing / NDJSON only" scope line.
- **EVADE:** a pre/post **value-set table** for `decision.intent`, the arming precondition stated
  plainly (`piloted_competence` default-`None`, passed by nothing in production ⇒ **production
  traces cannot contain `"evade"`**), and the consequence named in one sentence — *a downstream
  exhaustive match on `intent` is now non-exhaustive*.

**The contract change is parseable from the doc alone. G-D can proceed on this.** WARN-1 from my
`m3-m12b` finding is **CLOSED**, and closed at the right level of detail — the entry states why
the record mattered even though nothing was owed to ship.

### 3.3 **WARN-A — the report declares absent a mechanism it now carries**

`kitcal_g5_harness.py:106` still ships in `NAMED_ABSENT`:

> `"crit labelling in the trace (HALT-3) — the resolver crits but no call site logs it; surfacing it is a mechanism change (P-6 verdict declined to glue)."`

Every report emitted at `a42d052` carries this string **alongside a populated per-tier `crit`
block on every fight**. I confirmed both in the same artifact. The file contradicts itself.

`NAMED_ABSENT` exists (assembly note §8) precisely so *nobody mistakes an absence for the
fixture's behaviour* — a stale entry inverts that function into a false absence claim. This lands
in the 150-fight battery report and travels to the baton reader.

**Not a number. It is the artifact of record.** One-line deletion; cheapest before the battery.

---

## §4 — `a110890` (M-4): **PASS**

### 4.1 The armed delta — reproduced EXACTLY

My own `--smoke --gd-cadence` at the tip against my own `7a5eb88` baseline:

| | baseline (`7a5eb88`) | armed (`a42d052 --gd-cadence`) |
|---|---|---|
| boss arm A | **28.80 s, player win** | **32.00 s, MONSTER win** |
| boss arm A presses/s | **2.431** | **1.031** |
| boss arm A p:m ratio | 2.92 | **1.43** |
| boss arm B | — | 47.00 s, monster win |

Every claimed figure to the digit. **T-M4-13 fires.**

### 4.2 Default-OFF is genuinely dark — and §1 IS the proof

The unarmed tip run is byte-identical to `7a5eb88` (§1). Its report carries
`cadence_generation: "pre-m4"`, `cadence_model: {"armed": false}`, `non_poolable_with: []`. With
no `gd_cadence`, no pause keys exist and **no draw is taken** — so the fourth sub-stream cannot
perturb the main stream. That is the correct construction (H-M4-b pre-empted, not discovered),
and the salt is disjoint: `GD_SWING_PAUSE_STREAM_SALT = b"GDSWNG"` vs `GD_NOVA_STREAM_SALT =
b"GDNOVA"`.

### 4.3 The math note re-derives — every number, Discipline #1

- intervals **0.888889 s** (1/1.125) and **1.111111 s** (1/0.9) ✓
- `GD_ratio(T) = (T/0.900 + 0.350)/(T/1.125) = 1.250 + 0.39375/T`; at `T=1` → **1.64375**, and
  the composer's own `cadence_model.gd_ratio_at_t_base` reports `1.6437500000000003` ✓
- distortion sweep with `SIM_ratio` held at 11.11111 (correct — the sim's mob interval is a code
  constant, not an animation length): **5.453 / 6.760 / 7.346 / 7.679**. All four reproduce.
  Range [5.45, 7.68], never approaching 1 ✓
- quantization `0.888889 → 0.900` = **+1.2500%**, inside A-M4-2's 11% arm band ✓

**The strongest leg is the one that needs no assumption at all** and it should be quoted first
in the baton: `playerAttackSpeedCapMax = 200.0` ⇒ GD's own legal floor is `T_base/2.0`; the sim
runs `0.100 s`; therefore the sim's player cadence is **outside Grim Dawn's legal range for every
`T_base > 0.200 s`**. That is not a mis-tune, it is off the dial, and it holds without measuring
`T_base` at all. A-M4-1's grade-D status gates the *exact corrected cadence*, not the *existence
of the correction* — correctly stated.

### 4.4 CLAIM 7 — P-4 stamp plumbing EXISTS and FIRES

Verified on my own armed run:

```
cadence_generation  = "m4-gd"
non_poolable_with   = ["_fix3", "post-M-1/M-2 pre-M-4 batteries"]
cadence_model       = {"armed": true, "player_arm": "P-mace", "t_base_s": 1.0,
                       "player_interval_s": 0.8888888888888888,
                       "player_interval_quantized_s": 0.9,
                       "gd_ratio_at_t_base": 1.6437500000000003}
filename            = kitcal_g5_smoke_m4cadence_report.json
```

**The armed path keeps every guard live**, which matters because the battery runs armed: my
`--gd-cadence` run passes **12/12 static pins plus 2 insensitivity pins**, including `A-EFF-1`
(STRICT armed and asserted) and `A-FRZ-1`. Baseline `7a5eb88` reports 10 static + 2; the tip
reports 12 static + 2. So P-1 (STRICT) and P-5's structural discharge both hold on the *armed*
path, not only the default one.

`cadence_model` is read **from the composer at report time**, not hand-typed — the C-4 lesson
applied (a stamp that disagrees with the code that ran is worse than no stamp). The filename
carries `_m4cadence` so a report copied out of its directory is still distinguishable at a
glance. **P-4 discharged.** Third occurrence of the SS-1 non-poolability lesson, now a header
field rather than a fourth reminder — the right place to end it.

### 4.5 CLAIM 8a — T-M4-13's composed-ceiling deviation: **I CONCUR, independently**

The spec band `1.10–1.30` presses/s is the **composed ceiling** (1/0.9 = 1.1111). The harness
measures the **realized** rate over the whole fight — approach, lock, death included — so it sits
at or below the ceiling by the duty cycle (1.031). The substituted predicate is:

1. realized presses/s ∈ `[0.5, ceiling]` for every post-M-4 boss fight; **and**
2. **every** pre-M-4 boss rate strictly exceeds **every** post-M-4 boss rate; **and**
3. mean kill-time strictly increases.

**That is strictly stronger than the spec band, not a widening.** (2) in particular is a
separation assertion the original band could not make. Asserting the predicate that carries the
meaning, and declaring the difference, is the correct move. **Deviation accepted.**

### 4.6 CLAIM 8b — A-M4-3's class band: **ACCEPTED, with a grade to carry**

`TRASH_SWING_PAUSE_S = (0.45, 1.20)` is labelled **grade C, class band** at the constant
(`kitcal_g5_scenarios.py:130`) with the measurer named (legolas, EXT-B §3.4's 30-row table,
collapsible in one pass). That is R-X-5 compliant — name the measurer, never dress a guess as a
per-record read.

**INFO for the conductor, not a defect:** `kitcal_g5_scenarios.py:545` selects
`BOSS_SWING_PAUSE_S if row.tier == "boss" else TRASH_SWING_PAUSE_S`, so under `--gd-cadence`
**every non-boss row** draws from the grade-C band. The boss band `(0.30, 0.40)` is M-grade;
trash / champion / mixed_pack cadence in the post-wave battery is **not**. G-A should carry the
grade per tier rather than grading all four tiers at the boss's evidence level.

---

## §5 — `3183efb` (M-5): **PASS-with-notes**

### 5.1 Composition re-derived (Discipline #1) ✓

```
bioLife(13) = ((13 × 51)^1.53) + 2400 = 23,145.108
factor      = 1 + (−71 + 35)/100      =      0.640000
hp          =                            14,812.869   vs measured 14,812  →  0.0059 %
```

Claimed 0.006%. ✓ The `cl ≥ 20` discriminator also re-derives: `0.69/0.84 = 0.8214286` vs
`0.81013` separate by **1.3947%** (claimed 1.394%). ✓

### 5.2 The provenance channel refuses derived-over-measured ✓

- `provenance_from_grade` **raises** on an unknown grade rather than defaulting to `D`. That is
  the load-bearing choice: defaulting would quietly make a measured number overwritable.
- `assert_derivation_allowed` raises `HpProvenanceError` when `current_provenance == "M"`.
- Deriving the tag from the row's existing `hp_grade` rather than adding a second hand-maintained
  field is correct — two hand-maintained fields on one fact drift, which is the defect class this
  whole cell has been retiring.
- **A-HP-4 holds on the emitted trace, measured:** across my 5 smoke fights, every `mob` entity
  carries a tag (12 `M` + 12 `D`); the `player` entity is `null`, which is correct — A-HP-4 is an
  *opposition* predicate. A partially-tagged roster (the hazard named) does not exist.
- **M-5 moves no shipped number** — confirmed by §1's trace identity.

### 5.3 **WARN-B — `hp_provenance` reaches `replica-frame/v1` with NO MIGRATION.md entry (ADR-004)**

`replica_frame_emitter.py` gains, in the **entity block**, directly beneath `max_hp`:

```python
"hp_provenance": getattr(ent, "hp_provenance", None),
```

`grep -n hp_provenance src/reincarnated/simulation/MIGRATION.md` → **no output.** `3183efb`
touches no MIGRATION.md.

This is a **new key on the schema drax parses** — the same class of change as M-6's `crit` pair,
which *did* get an entry one commit earlier. The M-6 entry's own opening states the rule being
broken here:

> *"This entry exists because a silent additive field is how a consumer ends up rendering a
> default and calling it data."*

The mitigating facts are real: v1-additive, `null` on every production path, no consumer owes
anything to ship. Those are also **exactly** the mitigating facts of the crit keys — and the crit
keys were filed anyway, correctly. The distinguishing fact here is that this is a **repeat of a
gap repaired in the immediately preceding commit**, which is why it is a WARN rather than an INFO.

**Cite:** ADR-004 (cross-seam handoff requires MIGRATION.md), Review Principle 3 (cross-seam
impact called out explicitly), Principle 6 (cross-seam contract round-trip before the consumer
reads).

**This does NOT contaminate the battery.** It must close **before the baton emission / G-D**,
where drax reads `replica-frame/v1` cold. Roughly a 20-line append modelled on the M-6 entry.

### 5.4 **WARN-C — the T-M5-9 hero-term ban is DEFEATABLE; it is not executable as claimed**

The commit says the ban is *executable*, and H-M5-a instructs Gate-2 to treat any hero-keyed
constant as a BLOCK. I tried to defeat it cheaply, per the conductor's instruction. **I defeated
it four ways in a single file that the test PASSED on:**

```python
HERO_LIFE_MULTIPLIER: float = 2.4906        # ast.AnnAssign — the guard only walks ast.Assign
TIER_SCALE = {"hero": 2.4906}               # dict value — not an Assign target
def hero_pool_scale_factor(base): ...       # FunctionDef — not an Assign
HERO_POOL_ADJ = 2.4906                      # Assign, hero-named, but no mult/scale/factor/coeff token
```

`python3 -m pytest tests/test_wr1_m5_hp_provenance.py::test_T_M5_9_... -q` → **1 passed.**

The `ast.AnnAssign` hole is the sharpest of the four: **every module constant in
`gd_monster_hp.py` itself is an `AnnAssign`** (`BIO_LEVEL_FACTOR: float = 51.0`,
`P_QUEST_BOSS_PP: float = 35.0`, …). The guard is blind to *exactly the idiom the module it
protects is written in*.

**The 4702-literal half genuinely works** — I planted `HERO_POOL: float = 4702.0` in a third file
and the test failed with `['zz_jr_probe.py:1 literal 4702']`. But the forbidden move R-M5-1
describes is **fitting a ratio** (≈2.49, or a champion `bio` constant), not planting the anchor
value. **The operative half is precisely the weak half.**

**Grading:** WARN, not BLOCK. `test_T_M5_9` **passes on the real tree** and I found **no hero-keyed
constant anywhere** — the *rule* is honoured, only the *guard* is soft. My probe file was
synthetic, lived only in `/tmp/jr_wr1_tip`, and was deleted; the engine tree is clean.

The refusal itself is the strongest thing in this landing and I want it on the record: the builder
was handed a spec predicate (T-M5-3) that could not be satisfied, and **declined to invent a
champion `bio` constant that would make 813 fall out.** Two anchors (813 and 4,702) cannot both
discipline a constant invented to satisfy one. That is R-M5-1's forbidden move one tier down, and
recognizing it unprompted is the behaviour this gate exists to reward.

### 5.5 CLAIM 8c — T-M5-3's inverse-check respec: **ACCEPTED, with one INFO**

The respec asserts three things. Two are load-bearing:

- **the falsifier** — `gd_monster_hp(11, −71, 0, "Champion") = 14,588.298 ≠ 813` (over by 17.9×),
  so **nobody can quietly reuse the boss curve for a champion**. This is the assertion that earns
  the respec; it converts an unsatisfiable predicate into a live trap.
- **the branch check** — the `Quest` branch does *not* close 813, so `P = +50` is identified.

**INFO:** the third — `gd_monster_hp(11, −71, 0, "Champion", bio=CHAMPION_IMPLIED_BIO_AT_CL11)
== 813.0` — is algebraically definitional, since `CHAMPION_IMPLIED_BIO_AT_CL11 ≡ 813.0/0.79`.
It is `(813/0.79) × 0.79 == 813`. It confirms the Champion factor is 0.79 and nothing more; it is
not independent evidence that the composition rule reproduces 813. The docstring's "asserts three
things" reads as three measurements. Two are.

`A-M5-1` is filed grade C with the measurer named (legolas; the HP re-grade note already closed
813), and `bio` is a **keyword-only** operand with no non-boss default — so reaching for a
non-boss actor's HP without supplying its curve is a visible act. Correct construction.

### 5.6 INFO — the "MESSAGE VERBATIM" claim is not literally true

The commit states A-HP-3 *"KEEPS ITS ID AND MESSAGE VERBATIM (cited in three notes)."* The ID is
intact and the guard is genuinely **stronger** (it now also asserts the hero slot's tag is `M`
*and* that the rule actually refuses — an inert guard being worse than the three bespoke asserts
it replaced, H-M5-b). But the emitted pin label gained a suffix:

```
7a5eb88:  "A-HP-3 hero slot = MEASURED 4702, not derived"
a42d052:  "A-HP-3 hero slot = MEASURED 4702, not derived (M-5 provenance rule armed)"
```

A note citing the string exactly will no longer match. Trivial; recorded because "verbatim" was
the claim.

---

## §6 — `a42d052` (A-EFF-1 scoping): **PASS**

### 6.1 The scope restores — verified directly, including on the exception path

```
default                          → warn
inside effect_name_policy_scope  → strict
after normal exit                → warn
after the armed region RAISES    → warn
```

Both entry points behave. "The replica path does not run unarmed" and "nothing else is armed by
accident" are both true. `EFFECT_NAME_POLICY` is a module global, so an unscoped arm in a
preflight is exactly a process-wide arm — the original defect is real and the fix is the right
shape (context manager, not a teardown call that a `raise` can skip).

### 6.2 The `"control"` half is a FINDING, disposed of correctly

I concur with the conductor's routing and want the reasoning on the record, because the temptation
here was to patch:

- `"control"` is **not** a `dot`-class silent break. Rocket's E2 math note
  (`generation/math/economy-axis-e2-2026-07-09.md` §(b), source-verified) records that a
  control-ROLE skill emits one primary effect named `"control"` carrying only
  `{element, damage_scaling_type}`, that the kernel has no branch for it, and that the lock the
  sim resolves lives on the **signature ailment riding chain_A** instead. Deliberate emission,
  documented no-op.
- STRICT is nonetheless **right to refuse it**, and that is the point.
- Therefore M-9's pre-registered promotion criterion — *"STRICT becomes the global default once
  one full PRODUCTION battery runs green under it"* — is **NOT met**, and `"control"` is its
  **named blocker**.

**Promoting on evidence rather than on enthusiasm.** The alternative — special-casing `"control"`
into the handled set to make the suite green — would have destroyed the instrument on its first
real reading. It was not taken.

### 6.3 The census scope note is the right correction — and it corrects *my* number

My `m3-m12b` census ("0 unhandled across 5,110 JSON / 19,642 effect instances") walked **banked
artifacts**. The live emission path emits `control`. The census is not contradicted — **its base
did not include a live production emission run**, and it should be quoted with that scope from
here on. Recording a reviewer's number's limits rather than quietly working around it is the
behaviour Discipline #8 asks for.

---

## §7 — CLAIM 6: THE FULL REGRESSION

**Method: I RE-RAN IT.** Not an audit of the builder's log. Reason: this is the third consecutive
lap on which I have re-run rather than audited, and the reason has not changed — the pre-registered
criterion is an **empty failure-NAME diff against a baseline I produced myself**. An audit of
someone else's raw log can confirm arithmetic but cannot confirm that the log came from the tree
under review. My `7a5eb88` baseline (`/tmp/jr_wr1_after_names.txt`, 81 names) is my own from the
previous gate, so the diff is between two artifacts I produced on the same instrument. The
`a42d052` run is the fourth commit's own discovery mechanism (it is what caught the process-global
policy leak), which makes an independent re-run the appropriate instrument rather than a
formality.

Tree state captured before and after: `git status --porcelain --untracked-files=no -- src/ tests/`
**empty both times**; `HEAD` unchanged at `a42d052a989ef29a8d5d1e3d143d193bf5fbf8b9`.

### Result — the claim reproduces on every term

```
JR_REG2_START  2026-07-29T11:20:16Z    HEAD = a42d052a989ef29a8d5d1e3d143d193bf5fbf8b9
JR_REG2_END    2026-07-29T11:43:58Z    (23 m 41 s)
  60 failed, 6004 passed, 3 warnings, 21 errors
  failure_name_count = 81
  names ONLY in a42d052 (new failures)   : (none)
  names ONLY in 7a5eb88 (fixed/vanished) : (none)
```

| term | claimed | my measurement |
|---|---|---|
| failed | 60 | **60** ✓ |
| passed | 6004 | **6004** ✓ |
| errors | 21 | **21** ✓ |
| failure-name diff, both directions | EMPTY | **EMPTY** ✓ (81 names each side) |
| delta vs `7a5eb88` baseline | +93 | **6004 − 5911 = 93** ✓ |

My own `7a5eb88` baseline was `60 failed, 5911 passed, 21 errors / 81 names` (previous gate,
`/tmp/jr_wr1_after_7a5eb88.txt`). **The pre-registered empty-NAME-diff criterion is met in both
directions on a baseline and a target I produced on the same instrument.** Nothing regressed and
nothing was silently repaired. Discipline #2 discharged.

### New-suite arithmetic, verified independently

I collected each new suite rather than trusting the sum:

| suite | tests |
|---|---|
| `test_wr1_m9_effect_name_policy.py` | 19 |
| `test_wr1_m6_crit_labelling.py` | 18 |
| `test_wr1_m4_attack_speed.py` | 22 |
| `test_wr1_m5_hp_provenance.py` | 34 |
| **total** | **93** |

`6004 − 5911 = 93` closes **exactly** on the new suite — no incidental test-count drift hiding in
the delta. All four suites plus `test_kitcal_g5_harness.py` green in my own run: **123 passed**
(93 + 30).

---

## §8 — WARN-D: P-5's DISCHARGE ROUTE IS NOT NAMED, AND THE BATTERY IS NEXT

Charter §8.13 ratifies **P-5** as pre-registered gate law:

> *shatter-count 0 on every tier/regime in the post-wave battery (H-1 tripwire)*

**There is no `shatter_count` field on the report and none on any fight record.** I enumerated
both key sets on my armed run. What exists instead is:

1. `A-FRZ-1` — a **static emission refusal at preflight**, which I verified refuses five distinct
   violating fixtures (§2.3); and
2. `freeze_shatter_armed: false` on the report header.

Together these are a *structural* discharge: no shatter-bearing effect can be compiled, therefore
the runtime count is zero **by construction**. That argument is sound and is arguably **stronger**
than a counted zero — but it is **not the predicate as ratified**, and a conductor grading the
battery against P-5 will look for a per-tier/per-regime count that does not exist.

This is the same seam the conductor already had to name explicitly for **P-2** (received-side crit
is a structural zero, not a measured one). The wave has now hit it twice. Naming the discharge
route *before* the battery costs a sentence; discovering it *after* a 150-fight run costs a
grading dispute over the artifact of record.

**Either** add `shatter_count: 0` per tier/regime to the report, **or** the conductor amends P-5 to
accept the structural discharge with A-FRZ-1's preflight pass as the named evidence. Reviewer has
no preference between them — only that one be chosen before the battery fires.

---

## §9 — BATTERY CONTAMINATION ASSESSMENT (asked at BLOCK volume)

**Nothing here contaminates a 150-fight battery's arithmetic.** No finding moves a number; the
byte-identity spine holds on my own measurement; M-4's behavioural change is opt-in, stamped, and
declared non-poolable.

Ordered by where each must close:

| # | finding | severity | must close before |
|---|---|---|---|
| WARN-A | `NAMED_ABSENT` declares crit labelling absent while the report carries it | WARN | **the battery** (it lands in the artifact of record) |
| WARN-D | P-5 has no `shatter_count`; discharge is structural and unnamed | WARN | **the battery** (it is the grading predicate) |
| WARN-B | `hp_provenance` on `replica-frame/v1` with no MIGRATION entry | WARN | **the baton / G-D** |
| WARN-C | T-M5-9's hero-term ban is defeatable four ways | WARN | may ride — no live violation |
| INFO ×4 | A-FRZ-1 exact-vs-substring · A-M4-3 grade-C on 3 of 4 tiers · T-M5-3's definitional third assertion · A-HP-3 label not verbatim | INFO | — |

**Two of these are single-line edits (WARN-A, and WARN-D if taken as a report field).** Both land
inside the battery report. Closing them costs minutes now and cannot be closed retroactively
without re-running 150 fights.

---

## §10 — WHAT THIS WAVE DID WELL (on the record, because it is the pattern to repeat)

1. **The full regression was the criterion, and it earned that status.** It found a defect the
   targeted suites structurally could not — a process-global policy leak visible only when the
   harness suite and the emission-driver suite run in one process. Discipline #2.
2. **Two findings the instruments produced were reported, not worked around** — the structural
   mob-crit zero (pinned by T-M6-9b so opening that door is a named change) and `"control"` as
   STRICT's promotion blocker. Both were more convenient to suppress than to file.
3. **A spec predicate that could not be satisfied was named, not bent** (T-M5-3), and the fit that
   would have satisfied it was refused by name.
4. **Byte-identity was treated as an acceptance test rather than a claim** — and it survived my
   own tighter normalization, which is the harder version of the test.

---

## Action

- [ ] **gamora — before the battery fires:** delete or rewrite `NAMED_ABSENT[2]`
      (`kitcal_g5_harness.py:106`). The report cannot declare crit labelling absent while
      carrying a populated `crit` block (WARN-A).
- [ ] **gamora — before the baton / G-D:** MIGRATION.md entry for `hp_provenance` on
      `replica-frame/v1`'s entity block, modelled on the M-6 crit entry (ADR-004, WARN-B).
- [ ] **gamora — may ride:** strengthen `test_T_M5_9` to walk `ast.AnnAssign`, `ast.Dict` keys and
      `ast.FunctionDef` names, and widen the token set beyond
      `mult/scale/scaling/factor/coeff` — or downgrade the commit's "executable ban" language to
      match what the guard actually covers (WARN-C).
- [ ] **gandalf (conductor) — before the battery fires:** choose P-5's discharge route — add
      `shatter_count` per tier/regime, or amend P-5 to accept A-FRZ-1's preflight refusal as the
      named structural evidence (WARN-D).
- [ ] **gandalf (conductor) — at G-A:** carry A-M4-3's grade C on trash / champion / mixed_pack
      cadence; only the boss swing-pause band is M-grade (§4.6).
- [ ] **Matt:** no decision required. Nothing here exceeds seam authority; no ADR is implicated;
      no locked decisions-log entry is in conflict. HALT-1 (`freeze` emission) remains parked in
      `canonical/matt_decision_needed/2026-07-29-rdr-freeze-emission.md` and P-5 guards the battery
      regardless of its disposition.

---

## References

**Commits reviewed** (`~/Games/reincarnated-engine`): `2456b20` · `1e5b136` · `a110890` ·
`3183efb` · `a42d052`

**Engine files read:**
- `src/reincarnated/simulation/gd_attack_speed.py`
- `src/reincarnated/simulation/gd_monster_hp.py`
- `src/reincarnated/simulation/damage_resolver.py`
- `src/reincarnated/simulation/effect_resolver.py`
- `src/reincarnated/simulation/MIGRATION.md`
- `src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py`
- `src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_scenarios.py`
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py`
- `src/reincarnated/simulation/spatial_gauntlet/replica_frame_emitter.py`
- `src/reincarnated/simulation/math/wr1-m4-attack-speed-2026-07-29.md`
- `src/reincarnated/simulation/math/wr1-m5-hp-provenance-2026-07-29.md`
- `tests/test_wr1_m4_attack_speed.py` · `tests/test_wr1_m5_hp_provenance.py` ·
  `tests/test_wr1_m6_crit_labelling.py` · `tests/test_wr1_m9_effect_name_policy.py`

**Collaboration-repo inputs:**
- `agentic_orchestration/gandalf/notes/2026-07-28-wr1-wave-relay-run-charter.md` §8.12–§8.15
- `agentic_orchestration/gandalf/design-inputs/2026-07-29-wr1-m4to9-specs.md`
- `agentic_orchestration/gamora/notes/2026-07-29-wr1-build-m4to9.md`
- `agentic_orchestration/qa/findings/2026-07-29-gate2-gamora-wr1-m3-m12b.md` (WARN-1/WARN-2 closure)

**Reviewer artifacts** (ephemeral, `/tmp`): `jr_bi_base/` · `jr_bi_tip/` · `jr_bi_m4/` ·
`jr_wr1_after_a42d052.txt` · `jr_wr1b_after_names_jr.txt` · `jr_wr1b_reg_meta_jr.txt` ·
`jr_wr1_g2b_regression.sh`. Worktrees `/tmp/jr_wr1_base` and `/tmp/jr_wr1_tip` removed at close.
