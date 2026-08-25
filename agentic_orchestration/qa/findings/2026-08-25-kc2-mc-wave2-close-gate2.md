# Finding — 2026-08-25 — KC2 MODEL-COMPLETION RUN · WAVE-2 CLOSE GATE (B-5 + B-6 + B-4app)

**Reviewer:** jack-ryan (Gate-2, DEV-MODE)
**Severity:** WARN — **SEAL-CONCUR on all three builds.** 0 BLOCK / 4 WARN / 7 INFO
**Target:** `9729e363…` (B-5, `kc2/alert.py`) · `713c782b…` (B-6, `kc2/actor_state.py`) · `082b599a…` (B-4app, `kc2/gate_model.py`)
**Developer:** gamora (simulation seam)
**Conductor:** gandalf (RUN-CONDUCTOR), ruling `R-L72-3`
**Principles applied:** REVIEW_PROCESS #1 (math-before-code) · #2 (smoke gate) · #4 (decisions-log as truth) · #5 (severity matters). Disciplines #11 (empirical inspection over assumption) · #62(a) (staging width) · #72 (stale-sweep retention).

---

## Method

Same as the B-3app seating: **verify by my own hand, never transcribe.** Every number below was
produced by me — shasums computed here, drivers run here, set-diffs and vocabulary checks computed
here against the sealed artifacts. Where I quote a builder's or the conductor's figure I say so and
say whether my own instrument agreed.

**One self-report first (Discipline #11).** My first search for B-4app's superseded-emission
naming used an alternation inside `grep -F`, which treats `\|` as a literal. It returned a clean
false negative and I was one step from filing a defect that does not exist — the naming is present
and correct at `AGENT_STATE.md:10380`. Caught by cross-checking against a second instrument. The
run has convicted five agents of instrument-before-question; this is the reviewer's turn on the
same list, and it belongs in the record rather than in a quiet retry.

---

## 1 — Seals, guards, tracking, sibling discipline: **CLEAN**

Computed by `shasum -a 256` over every `kc2-checkpoint-*` on disk, then matched against the
ledger's claimed seals. **All seven sealed cells resolve to a file, byte-exact:**

| cell | seal | file | git |
|---|---|---|---|
| b2app | `a4b84ed5…` | `…b2app-20260824_192243.json` | tracked (`118783ef`) |
| b3 | `dd13408e…` | `…b3-20260824_202328.json` | tracked (`118783ef`) |
| b3app | `b941104d…` | `…b3app-20260825_024524.json` | tracked (`39d64f36`) |
| b4 | `08255194…` | `…b4-20260824_232229.json` | tracked (`30a31ef0`) |
| **b5** | `9729e363…` | `…b5-20260825_034842.json` | tracked (`287c14a5`) |
| **b6** | `713c782b…` | `…b6-20260825_002358.json` | tracked (`5eb97e28`) |
| **b4app** | `082b599a…` | `…b4app-20260825_015029.json` | tracked (`d8af5726`) |

**Guards PRE==POST, re-verified by RUNNING each driver myself** (not read off the return):
B-5 printed `ELEVEN guards unmoved (b3app b941104d4185… · b4 08255194273b…)`;
B-6 printed `12 guards unmoved (b5 9729e363c132… · b3app b941104d4185…)`;
B-4app printed `13 guards unmoved (b6 713c782baed3…)`. **B-4app's THIRTEEN is confirmed on a
third independent execution** (build, gamora's post-build re-verify, mine). Parents 20/20 on all
three. Sibling discipline (K-7) holds: every predecessor is present and byte-identical after being
read.

**Superseded emissions.** Three b4app intermediates (`…013832`, `…014355`, `…014722`) and nothing
else are untracked. They are **named with the artifact of record beside them** at
`AGENT_STATE.md:10380` — L-72's claim verifies. Consistent with B-4's W3 posture (superseded driver
revisions left never-staged so the sweep can take them).

---

## 2 — Drivers reproduce: **CLEAN, all three**

I ran all three drivers on the final model. Every derived count and every terminal array reproduced.

| build | claimed | **my run** | set-diffs (computed by me) |
|---|---|---|---|
| B-5 | 27 reg / 27 emitted / 24 hold / 3 FAIL | **27 / 27 / 24 / 3**, IDs `B5-P13`,`B5-P16`,`B5-P22` | `[]` / `[]` ✓ |
| B-6 | "26/26, 25 hold, 0 fail, 1 UNEXERCISED, set-diffs `[]`" | **reg 24 / emitted 26 / 25 hold / 0 fail / 1 UNEXERCISED (`B6-P17`, `holds:null`)** | **see WARN-1** |
| B-4app | 29 reg / 30 emitted / 29 hold / 1 FAIL | **29 / 30 / 29 / 1**, ID `B4app-P22b` | `[]` / `['B4app-P13b']` ✓ |

Terminal arrays reproduced exactly: B-5 `A0 [155,156,152,151,151]` → `A2 [155,152,155,151,152]`;
B-6 `C0 == C1 [155,152,155,151,152]`; B-4app `G0=G0b=G1=G3 [155,152,155,151,152]` ·
`G2a [155,152,151,152,152]` · `G2=G4 [155,152,151,151,152]` · `G5=G6 [151×5]`.
**`chan&move 2368/2700` reproduced on my own run** — L-72's run-level correction is right.
B-6's `anger t [0.12,0.15,0.17,0.22,0.27]` reproduced — five values, 0.17 the mode, never uniform.

---

## 3 — `RESID-D1-2` § 9 DO-NOT audit: **4 of 5 clean; item (2) materially open and unpriced**

The DO-NOT block landed at L-71, *after* B-5 and B-6 sealed and after B-4app's dispatch. Compliance
here is **independent convergence, not obedience**, which is worth more.

| DO-NOT | verdict | evidence (my own) |
|---|---|---|
| (1) hold as a **state** property | **NOT VIOLATED** | the hold is `Mover.alert_hold_until_t_s`, an absolute-clock field in `locomotion.py`; the comment at `locomotion.py:1179` already reads *"the `\"End\"` event is the animation's, not the state's"* — the build reached the decode's own shape before the decode existed |
| (2) `permission[18][cur]==0` as **universal** | **⚑ MATERIALLY PRESENT, UNPRICED** | `grep` for `ActionState`/`action_state`/`permission[18]`/`REPLACE`/`PENDING`/`REJECT` across `alert.py`, `actor_state.py`, `gate_model.py` returns **zero hits**. There is no current-action-type concept anywhere, so every fired closure receives the REPLACE-row `.anm` duration `(frames−1)/(frameRate×speed)` |
| (3) movement gate from state **names** | **NOT VIOLATED** | no gate re-derivation exists in any of the three modules |
| (4) cite `?CanMove@` | **NOT CITED** | zero hits across all three modules, all five math notes, all three drivers |
| (5) velocity-zeroing as unconditional | **NOT VIOLATED** | `locomotion.py:1186-1188` suppresses the step's **travel** (`travel = 0.0`) and asserts nothing about velocity — behaviourally the early-return, which is what was decoded |

**Item (2) is exactly what `R-L72-4`'s § 5 ADDENDUM was commissioned to price, and it is
ABSENT-AT-AUDIT** (see § 9). No finding is filed against the builds for it: B-5 could not have
modelled a regime that had not been decoded, and `C-B5-1` carried the premise openly the whole way.
The exposure is real and it is the seating's one genuinely open measurement.

---

## 4 — BLOCK-1 discharge (`R-L66-2`): **DISCHARGED. Verified arithmetically.**

Both terms are keys on `713c782b…`, under `predicates/B6-P7`:

```
ensemble_summon_damage_total_applied  =     22692.766799999983
ensemble_player_damage_total_applied  = 143786314.7011357
                             ratio    =         0.00015782285572286627
```

Divided by my own hand: **`1.5782285572286627e-04`, exact to the last digit of the emitted
`⚑ ensemble_summon_share_of_player_output`.** Five per-salt pairs are emitted alongside
(`1.56e-4 … 1.13e-4 … 1.73e-4 … 1.18e-4 … 1.63e-4`), so the ensemble figure is not a single-cell
reading wearing an ensemble label. **⚑ The denominator was never unmeasurable — it was UNEMITTED**,
exactly as B-6 states.

**The no-exclusion corollary is respected everywhere the figure is quoted.** The figure appears in
exactly two places (`AGENT_STATE.md:10228` and the B-6 math note's ride table). At
`AGENT_STATE.md:10229-10236` the struck sentence is left struck, the replacement names its two keys
and its artifact, and the corollary is stated in full — *"excluding a hypothesis from a residual
needs an **UPPER** bound on summon offense, and none exists"*, closing with
**"This ratio is a figure, not a licence."** That is the strongest available form. **BLOCK-1 CLOSED.**

---

## 5 — `MD-B4app-6` / `B4app-P22b`: **DISPOSITION — honest-fail-in-place is CORRECT. Ruled.**

**The premise verifies.** `summons.py:1073` emits `"⚑ refusals_priced": self.refusal_prices(…)`
**into the wave payload**; the two rows sit at `:1079` (`C-B3-1`) and `:1109` (`C-B3-8`), both
`"price": self.n_diverted`. Attaching a `⚑ grade` key changes the emitted dict, which changes the
payload, which moves the digest, which breaks `B4app-P1` — the build's **first** predicate.
gamora's stated reason is factually true, not a convenience.

**Ruling: honest-fail-in-place STANDS for the wave close.** Grounds:

1. The alternative repairs are both worse. Patching in place requires either suspending the
   parent-identity predicate for one build — which is grading yourself up by editing the checker
   after seeing the result — or re-sealing B-6, since `713c782b…` is a byte-guard on B-4app.
2. The failing predicate is **not** a shrug. `B4app-P22b` ships with both witnesses, names both
   offending line numbers, names the grade owed (`decoded-false-mechanism`), and names the
   successor. No consumer reading the artifact can mistake those prices for graded ones.
3. It is the honest-fails discipline the run has held since B-3app, applied against the builder's
   own interest.

**Two conditions attach to the disposition, and they are the price of ruling this way:**

- **(a) The ungraded prices are ON THE WIRE** in the wave payload a Godot consumer reads. So
  `MD-B4app-6` is not a queue row that may slip: it must be **the first item of the next build that
  legitimately moves the payload digest**, carrying its own prereg direction row (the change is
  prose-only; terminals must measure exactly zero and must be registered as such *before* the run).
- **(b) `MD-B4app-6`'s scope as written is too narrow.** It says "the ungraded DIVERT prices." It
  must also repair **`B6-P14`** — see INFO-2 — or the predicate whose registered falsifier is *"a
  DIVERT-sourced figure emitted without the grade"* still cannot see this class of defect after the
  repair lands.

Within-seam, no Matt escalation. Routed to the conductor.

---

## 6 — The F-5 correction: **VERIFIED EXACTLY, against B-3's sealed ledger**

I loaded `dd13408e…` and `b941104d…` and diffed their `⚑ refusals` blocks by hand.

- **`C-B3-8` EXISTS on B-3's sealed ledger, priced `1855`** ✓ — verbatim:
  `{"what": "petAngerTransference SHARE ARITHMETIC (D-3 R-4, slot unresolved)", "price": 1855, …}`
- **B-3app dropped exactly FIVE rows:** `C-B3-4`, `C-B3-6`, `C-B3-7`, `C-B3-8`, `C-B3-9` ✓
- **Their sealed prices:** `0` · `0.0` · **`2567`** · **`1855`** · **`1000.0`** — the charter's
  *"2,567 / 1,855 / 1,000.0 among them"* is exact ✓
- **Four unmentioned:** L-63 accounts for `C-B3-8` (price forwarded to it) and for `C-B3-1/-2/-3/-5/-10`.
  `C-B3-4`, `-6`, `-7`, `-9` appear in no disposition. **Four** ✓
- **Restoration is correct in form:** restored under its own subject on B-4app's ledger with
  `price_key: "⚑ HISTORICAL — B-3's own emitted price, read off dd13408e…"`, re-graded
  `decoded-false-mechanism` on D-12, and `⚑ conditioned_on: "D-12, DISCHARGED"`.
- **`C-B3app-10` is correctly a MINT, not a restoration** — its subject (summon *life*) genuinely
  differs from `C-B3-8`'s (share arithmetic); the two were joined only by a shared *number*. That
  distinction is the whole of F-5's substance and B-4app got it right.
- **The other four are dispositioned, not absorbed:** `MD-B4app-7` = "the four un-published B-3
  refusals" ✓.

**One further verification the return did not claim and I will add in its favour:** those five rows
**never left the wire**. `summons.py:refusal_prices()` still emits all nine `C-B3-1…C-B3-9` into the
wave payload. B-3app dropped them from the *checkpoint* ledger only. B-4app ADDENDUM 4's title
("`C-B3-8` NEVER LEFT THE WIRE") is literally true and I confirmed it in source.

---

## 7 — The validator-replacement hole: **WIDER THAN REPORTED. See WARN-2.**

Assessed in full below. The harvest framing *"a census of a field is not a validator of it"* is
correct and **understates the mechanism by one axis**.

---

# WARN-1 — B-6's predicate set-diff was never computed, and L-70 reports it as run and empty

**What I found.** L-70 reads: *"Predicates derived: **26/26**, 25 hold, 0 fail, one UNEXERCISED,
**set-diffs `[]`**, no total typed."* Against the artifact `713c782b…`:

- `⚑ predicates_registered` = **24**, `⚑ predicates_emitted` = **26**. The 26/26 is not on the wire.
- **B-6 emits no set-diff at all.** `grep` of `gamora_kc2_mc_b6_actor_state_2026_08_25.py` finds
  `⚑ predicates_registered: len(reg_ids)` and nothing else. B-5's driver emits
  `registered_minus_emitted` / `emitted_minus_registered` (`:1399-1400`); B-4app's emits
  `B4app-P20` with `in_documents_not_emitted` / `in_emitted_not_documents` (`:1383-1385`). **B-6 is
  the trough between two builds that both had the instrument.**
- **Computed by me** (token scan of `kc2-mc-b6-actor-state-2026-08-25.md` against the emitted keys):
  in-documents-not-emitted `[]`; **emitted-not-in-documents `['B6-P1b', 'B6-P8a']`**. So even had
  the check run, the answer is not `[]`.

**Rationale.** The two escapees are legal — sub-predicates minted during the build, exactly the
class B-4app's `B4app-P20` calls `⚑ successors_are_legal` and discloses rather than back-writing.
**The substance is honest; the record is wrong on both limbs.** This is the fold-derivation clause's
own shape (`R-L65-1`): a fold sentence asserted a count the named artifact contradicts, and asserted
a *check* that was never run.

**Not a BLOCK** because I have now computed the diff and it is clean apart from two disclosed
successors — nothing is hiding behind it.

**Action:**
- [ ] **Conductor:** correct L-70 in-ledger to `registered 24 / emitted 26`, and replace
  "set-diffs `[]`" with the derived value `emitted-not-in-documents ['B6-P1b','B6-P8a'] — legal
  successors, disclosed here because the build did not emit the diff`.
- [ ] **gamora:** the set-diff predicate is a standing carry, not a per-build choice. B-5 had it,
  B-6 lost it, B-4app rebuilt it. Land it in a shared helper so a build cannot ship without it.

---

# WARN-2 — The validator-replacement hole is wider than B-4app reported: **three offenders, three clauses, and the census population was never B-6's own ledger**

**What I found.** `B3app-P14`'s registered form has **four** clauses: a price; `magnitude_class ∈
{measured, bounded, UNBOUNDED-UNMEASURED}`; `magnitude_of ∈ {effect, population}`; and
`magnitude_of == population ⇒ non-empty effect_on_outcome`. I ran all four by hand over every sealed
ledger. B-4app reported the two `magnitude_of: "selection"` values. **There are three offenders on
B-6's sealed ledger, across three different clauses:**

| row | clause breached | value |
|---|---|---|
| `C-B6-3` | **class vocabulary** | `magnitude_class: "decoded-zero"` — outside `{measured, bounded, UNBOUNDED-UNMEASURED}` |
| `C-B6-3`, `C-B6-4` | **`magnitude_of` vocabulary** | `magnitude_of: "selection"` — reported by B-4app ✓ |
| `C-B6-5` | **population ⇒ effect_on_outcome** | `magnitude_of: "population"`, no `effect_on_outcome` block |

Scoped for fairness across the sealed record: `b3app` **0** offenders · `b5` **0** · `b4app` **0** ·
`b6` **3**. (`b3`'s nine `magnitude_class: null` rows pre-date the carry-shape discipline and are
not counted. `b4`'s `C-B4-5` carries `'unbounded-unmeasured'` **lower-case** — a fourth escape, of
the case-variant kind, on a different sealed ledger.) **B-6 is the sole build with a clause-4
escape and the sole build with a novel class value — and it is exactly the build where the
validator was replaced by a census.** The causality is tight.

**And the mechanism is one axis deeper than the harvest says.** `B6-P8` is constructed as
`cens = _refusal_censuses(b3app)` — **its population is B-3app's sealed artifact, not B-6's own
ledger** (`n_refusals: 14`, while B-6's own block holds **5** rows). So two independent regressions
compounded:

1. **the instrument's TYPE changed** — validator → census (B-4app's finding); and
2. **the instrument's POPULATION changed** — own ledger → predecessor's ledger.

**Either alone would have missed all three offenders.** A validator pointed at B-3app's ledger
convicts nothing; a census of B-6's own ledger reports `selection: 2` and passes. The harvest line
*"a census of a field is not a validator of it"* is true and should be paired with its sibling:
**an instrument that changes population silently is the same defect wearing a different hat — and
the population change is the harder one to see, because the numbers still look plausible.**

**Partial restoration is the residual risk.** `B4app-P13b` **does** re-instate a validator — over a
widened, code-read vocabulary `("population","effect-on-record","effect-on-outcome",
"not-applicable")` from `pet_specials.MAGNITUDE_OF_VOCABULARY`, run over this ledger **and every
sealed predecessor**, convicting `C-B6-3`/`C-B6-4`. That is the right shape and it is why this is
WARN and not BLOCK. **But it restores one clause of four.** A reader who sees "validator
re-instated, convicts B-6" will reasonably conclude the field is clean; two live offenders on the
same sealed ledger say otherwise. There is **no `MAGNITUDE_CLASS_VOCABULARY` anywhere in `kc2/`** —
`magnitude_class` has never had a code-side closed vocabulary to validate against, only prose.

**Action:**
- [ ] **gamora:** widen `B4app-P13b` (or a successor) to all four `B3app-P14` clauses, over this
  ledger and every sealed predecessor. Mint `MAGNITUDE_CLASS_VOCABULARY` in code beside
  `MAGNITUDE_OF_VOCABULARY` so the class field is validated rather than described; the case-split
  (`UNBOUNDED-UNMEASURED` in kc2 ledgers vs `unbounded-unmeasured` in `pet_specials.REFUSALS`) is
  resolved by the same act.
- [ ] **gamora:** every census predicate names its **population** on the wire. `B6-P8` should carry
  `⚑ population: "B-3app sealed ledger b941104d…"` — it would have made this visible on sight.
- [ ] **Conductor:** the three sealed rows are byte-guarded and stay so; the repair is forward-only,
  as a `MIGRATION` note for the baton consumer, not a re-seal.

---

# WARN-3 — `B6-P18`'s top-level census is unscoped, and that — not the fold sentence — is where the "86 %" came from

**What I found.** `B6-P18` emits, at top level:

```
n_ticks_channelling_and_moving : 189
n_ticks_channelling            : 220
fraction_of_channel_ticks      : 0.8590909090909091
```

and, beneath, a **five-salt table** summing to `1012 / 1150`. The top-level trio is **salt-0**,
sitting in the aggregate position with **no scope label**. Its own `registered_form` reads *"the
census is emitted per salt WITH its denominator — a numerator alone is BLOCK-1's shape"*, and its
falsifier is *"published without its denominator."* The denominator is there. **The population is
not.**

**Rationale.** L-72 files this as a *conductor* instance — *"L-70's '86 %' quoted a cell without its
scope"* — the second entry in the population-naming rider. By my own hand **the upstream cause is
the build**: the conductor quoted a key that exists, reads `0.859`, and is unlabelled. **Naming the
artifact key — which is all `R-L65-1` requires — would not have prevented this error.** The clause
is satisfied by `B6-P18.fraction_of_channel_ticks` and the sentence is still wrong.

This is `BLOCK-1`'s shape rotated one axis: BLOCK-1 was a **numerator without a denominator**; this
is a **numerator and denominator without a population**. The build caught the first and shipped the
second, in the same predicate, in the same breath.

**Action:**
- [ ] **gamora:** an aggregate slot either aggregates or carries its scope. Either lift the
  top-level trio to the five-salt sum, or rename it `⚑ record_cell_salt0_*`.
- [ ] **Conductor:** re-file the L-70 instance as **build-origin, conductor-propagated** — see the
  ratification input in § 8.

---

# WARN-4 — `R-L71-2`'s § 5 measurement is ABSENT-AT-AUDIT, and it is the one open exposure on the model

**What I found.** No `kc2-mc-b4app-gate-model-ADDENDUM-5-*.md` exists (ADDENDA 1–4 only). No
b4app checkpoint later than `…015029` (`082b599a…`) exists other than my own reviewer re-emission
`…020027`. **ABSENT-AT-AUDIT**, exactly as the seating prompt anticipated.

**Rationale.** § 3 establishes that the three builds carry **no current-action-type concept at
all**, so B-5's `.anm`-derived hold duration is applied universally — i.e. `permission[18][cur]==0`
is treated as universal, DO-NOT item (2). Ten of twenty-six current-action types give
PENDING/REJECT, and `19 Spawn` is REJECT while **Crucible bodies are spawned**. This is the one
place on the final model where a decoded fact has no priced counterpart. Everything else in this
seating either reproduces, is graded, or ships as a named refusal.

Per the corrected `R-L71-3`, the seating audits B-4app against the DO-NOT block and the addendum is
**mandatory before the seating closes**. It is running in parallel and the conductor holds the
seating open. **My concurrence on B-5's seal is not conditional on it** — B-5 sealed two rulings
before the decode existed, and `C-B5-1` carried the premise honestly throughout. But the **B-5
effect figure** must not be quoted at PM5 until the addendum returns.

**Action:**
- [ ] **gamora:** return the § 5 ADDENDUM (per-fired-closure current-action-type at the alert push;
  REPLACE-row census derived not typed; sibling emission, FOURTEEN guards).
- [ ] **Conductor:** hold the seating open; fold the addendum separately; if any of B-5's 26 fired
  closures sits on a non-REPLACE row, the duration-decoupling refusal is minted with its sign
  before PM5 grades anything.

---

# INFO-1 — B-6's `B6-P17` is the two-witness guard's prescribed form, executed

`MD-B5-1` ships as `holds: null`, `⚑ status: "UNEXERCISED"`, with the decoded-endpoint bound
**fully specified and explicitly not run**, and the reason named: running it needs a new limb in
B-5's sealed-adjacent module, i.e. a behaviour change inside a coverage build where it could not be
attributed. *"Specifying the bound and declining to smuggle the limb into a coverage build is the
honest half."* This is candidate-#4's operational form landing correctly, unprompted, one build
after ratification. Recorded for the run-close harvest as adoption evidence.

# INFO-2 — `B6-P14` tests the presence of the remedy, and its scan computes without convicting

B-4app named half of this. The whole of it:

```python
"holds": (sm.DECODED_FALSE_MECHANISM in json.dumps(anger, ensure_ascii=False))
```

Two defects, not one. **(a)** It is a substring presence test for the remedy string, not an absence
test for ungraded DIVERT-sourced prices — B-4app's finding. **(b)** Its scope is the `anger` block
alone, which does not contain `summons.py`'s `refusal_prices()` output at all, so the two rows at
`summons.py:1079/1109` were never in the population. **(c)** `_scan_divert` walks the block and
collects paths, but the result reaches the artifact only as
`⚑ n_divert_keys_on_this_artifact` — **it never enters `holds`.** An instrument that computes and
does not convict is the two-witness guard's own failure mode, in the build that practiced the guard
correctly at `B6-P17`. This is the second clause of the `MD-B4app-6` scope widening in § 5(b).

# INFO-3 — The B-5 driver `git add`s its own checkpoint; a reviewer's re-run silently stages an artifact

Running `gamora_kc2_mc_b5_alert_2026_08_25` printed `git-staged: True` and left my reproduction
`…b5-20260825_055923.json` **in the engine index**. B-6's and B-4app's drivers do not do this. Left
alone it would have ridden the next commit — under whatever author committed next. **This is the
live mechanism behind `D-B5-6`** ("a commit that said ALONE was not alone… the driver had
`git add`ed"), and the repair adopted there (`git diff --cached --name-only` before every scope-
claiming commit) catches it *after* the fact rather than preventing it. I unstaged with
`git reset HEAD <file>`; the file remains on disk and the engine index is clean. `#62(a)` names
staging width as the committer's duty; this is a case where the *tool* widens the staging.

# INFO-4 — `DR-3`'s exact zero is zero-by-absent-data, and PM5 should quote it that way

`DR-3` is registered and measured as `EXACTLY ZERO — byte-identical to G0`, 64 annulus evaluations,
0 refusals. **All 64 also report `n_absent_pair: 64`** — every evaluation found no decoded
min/max pair, and `roster_slots_with_decoded_metres` is `[]`. The zero is therefore "the gate had no
data on this arm", not "the gate bound and refused nothing". This is disclosed — `C-B4app-1` and
`MD-B4app-1` say exactly this, and the overlay arm `G3x` shows the contrast (35 evaluations, **7
refusals**, terminals move). Flagged only so PM5 quotes the zero with its cause attached, per
`R-L72-5`.

# INFO-5 — B-4app's set-diff carries a hardcoded id, and it is defensible

`in_documents_not_emitted: sorted(set(reg_ids) - set(emitted_ids) - {"B4app-P20"})`. The literal is
needed because `emitted_ids` is snapshotted before `B4app-P20` is itself added — the predicate
cannot appear in its own input. Tautologically emitted, so it hides nothing. **Not a defect**, but
it is the shape that hides a real absence if the pattern is copied to a non-self-referential id.
Preferred form: snapshot `emitted_ids` *after* insertion, which needs no name.

# INFO-6 — The two-witness guard's adoption curve is measurable, and B-5's greens are the last unwitnessed set on the model

Censused by me over the emitted predicate blocks:

| build | emitted | carry a CONVICT witness | carry **both** witnesses |
|---|---:|---:|---:|
| B-5 `9729e363…` | 27 | **0** | **0** |
| B-6 `713c782b…` | 26 | 7 | 5 |
| B-4app `082b599a…` | 30 | 28 | **28** |

B-5 carries **no witness-family key under any spelling** — I checked the full key vocabulary, not
just the canonical names. **This is not a breach:** B-5 fired at `R-L63-3`, and candidate #4 was
ratified with the two-witness guard as its operational form at `R-L65-1`/L-65 — *after* B-5 was
already in flight. The curve 0 → 27 % → 93 % across three consecutive builds is strong adoption
evidence for the run-close harvest.

**The consequence that does bind:** under candidate #4 as ratified, an unwitnessed green ships
`UNEXERCISED` — which is precisely the disposition `B4-P17`'s green received at L-63. **B-5's 24
greens are the last unwitnessed green set on the final model**, and any B-5 effect claim at PM5
rests on them. This composes with WARN-4: B-5 is simultaneously the build whose predicates carry no
witnesses and the build whose one open decode exposure (DO-NOT item 2) is unpriced until the § 5
ADDENDUM returns. Not a finding against the build; a **grading constraint on PM5**, and it should
join the prereg rows rather than be discovered there.

# INFO-7 — B-3's nine unclassed refusal rows are the discipline's own start line

`dd13408e…` carries `C-B3-1…C-B3-9` with **no `magnitude_class` on any of them**. The carry-shape
discipline began at B-3app. Not graded, recorded so that a future census over "all sealed ledgers"
does not read nine nulls as nine escapes.

---

## 8 — Fold-derivation clause: **ratification posture, and it MOVED at this seating**

**I arrived intending to ratify the clause as written. I now recommend ratifying it with the
population-naming rider PROMOTED from rider to second limb, and with the limb binding the BUILD as
well as the conductor.** The evidence is WARN-3 and it is decisive:

> `R-L65-1` requires a fold sentence asserting a bound, an exclusion or a count to **name the
> artifact key it derives from**. At L-70 the key exists (`B6-P18.fraction_of_channel_ticks`), reads
> `0.859`, and is **salt-0 in the aggregate slot with no scope label**. Naming it would have
> produced the identical wrong sentence with a citation attached.

A clause that a compliant author can satisfy while shipping the error is not yet load-bearing on
that axis. The one-limb clause caught the L-65 census transcription and the L-72 count family; it
cannot catch the L-67 lever-without-population or the L-70 cell-without-scope, and those are two of
the four conductor instances in the case file. So:

**Recommended form (two limbs, for run-close ratification):**

1. *(existing)* A fold sentence asserting a bound, an exclusion or a count **names the artifact key
   it derives from**, or it does not ship.
2. *(promoted)* **A key that carries a count, a rate or a bound names its POPULATION on the wire**;
   and a fold sentence quoting it **restates that population**. An unscoped aggregate is a
   derivation the reader cannot check.

Limb 2 binds the **builder**, which limb 1 does not. WARN-2's population-switch (`_refusal_censuses(b3app)`
computing a census presented as B-6's) is a second, independent witness for limb 2 from a different
seam of the same build — arrived at by a different route than WARN-3, which is what makes me
confident it is a real axis and not a single bad key.

**On the rest of the case file, from this seating's evidence:**

- The four conductor instances stand. **I add a fifth (WARN-1, L-70's "26/26 … set-diffs `[]`")** —
  and it is the clause's *strongest* instance to date, because it asserts not merely a wrong number
  but that a **check ran** which the build never implemented. That is a category the clause's
  current wording does not name at all, and I recommend it be named: *a fold sentence may not assert
  that a check holds unless the artifact carries the check's output.*
- **The L-70 instance (WARN-3) should be re-filed as build-origin, conductor-propagated.** The
  ledger's habit of assigning these to the conductor is honest but is now costing accuracy: three of
  the five instances I can see have an unlabelled or mis-scoped artifact key upstream of the fold
  sentence. Attributing them all to the fold layer will produce a clause that keeps failing to bind.
- The `R-L67` lever-sentence instance and legolas's rider (*"lever sentences derived from the sim's
  own arms name themselves ARTIFACT-INTERNAL until a decode grounds them"*) fold cleanly into limb 2:
  an artifact-internal lever is a quantity whose population is *the sim*, and saying so is naming it.

**Instance-count reconciliation (owed since `R-L66-3`): I decline to renumber at Gate-2.** Three
agents plus the conductor have each counted a different "fourth". The reconciliation is a run-close
harvest act with all returns in hand, and doing it here from partial evidence would mint a sixth
numbering. Carried to run close with my evidence attached.

---

## 9 — Late arrival check (audit item 9)

Performed at the end of the audit, twice, by directory listing and by timestamp sort:

- `math/kc2-mc-b4app-gate-model-ADDENDUM-{,2-,3-,4-}2026-08-25.md` — **four, no fifth.**
- `output/kc2-checkpoint-E-s09-cp150-b4app-*` newest: `…020027` (**my own reviewer re-emission**,
  untracked and unstaged), then the sealed `…015029` (`082b599a…`).

**§ 5 ADDENDUM: ABSENT-AT-AUDIT.** See WARN-4. Conductor holds the seating open and folds it
separately per `R-L72-4`.

---

## 10 — Smoke: **622/1 EXACT, and the 1 is the registered one**

Run by me, `pytest -k kc2 -q -p no:randomly`:

```
1 failed, 622 passed, 10309 deselected in 66.53s
FAILED tests/test_kc2_locomotion.py::test_AC_10_10_the_literal_30_0_appears_NOWHERE_in_the_arena_surface
E   Failed: bare 30.0 survives in secondary_streams.py:136
```

**622/1 IS the pass condition and it holds.** The failure is `test_AC_10_10` — I-12 lineage,
`secondary_streams.py:136`, re-attributed off this scope by my own B-4 `INFO-5`, and a file none of
the three builds touches. `-k kc2` selects every kc2 test in the repository (10,932 collected,
10,309 deselected), so **`test_AC_10_10` is the only kc2 failure repo-wide** — the claim as stated,
verified by the instrument that states it. The progression 533 → 569 → 591 → 622 across
B-3app/B-5/B-6/B-4app reconciles: +36 (B-5) +22 (B-6) +31 (B-4app).

**Full-suite context — stated with its limit, not padded.** I also launched `pytest tests/`
repo-wide; at the time of filing it had not completed (long generation cells). It is not the
instrument the claim is made on, and the in-seam result above is not conditional on it. The
baseline I recorded at the B-3app seating four builds ago was **10,763 pass / 59 fail / 21 error,
every non-kc2 failure in rocket's `season_generation`/`cycle12` and star-lord's seams,
long-documented as pre-existing**; the partial log shows failure and error blocks in the same
regions and no new cluster. **If the completed run departs from that baseline I will file a
supplement rather than amend this finding** — the seating's own rule about not back-writing a
record after the fact applies to the reviewer first.

---

## Verdict

**SEAL-CONCUR on B-5 `9729e363…`, B-6 `713c782b…`, B-4app `082b599a…`.** No BLOCK.

Nothing I found touches a simulated quantity. Every terminal array, every derived count, every
byte-guard and all seven seals reproduce under my own hand. The four WARNs are, without exception,
**defects in the instruments that describe the artifacts and in the sentences that quote them** —
the same location as B-3app's BLOCK-1, and the run's characteristic failure surface. The builds are
right where they disagree with their own narration, and B-4app in particular corrected three
conductor folds against its own headline and shipped a failing predicate rather than move a digest.

**Wave-2 close CONCURS, conditional only on the § 5 ADDENDUM (WARN-4) returning before the seating
closes** — which is the conductor's own `R-L71-3` fallback and already in flight.

## Action summary

- [ ] **gamora:** set-diff predicate into a shared helper (WARN-1) · widen `B4app-P13b` to all four
      clauses + mint `MAGNITUDE_CLASS_VOCABULARY` (WARN-2) · every census names its population on
      the wire (WARN-2/3) · scope-label or aggregate `B6-P18`'s top-level trio (WARN-3) · return the
      § 5 ADDENDUM (WARN-4) · `MD-B4app-6` first on the next digest-moving build, scope widened to
      include `B6-P14` (§ 5, INFO-2) · drop the `git add` from the B-5 driver or make it opt-in
      (INFO-3).
- [ ] **Conductor (gandalf):** correct L-70's predicate line in-ledger (WARN-1) · re-file the L-70
      "86 %" instance as build-origin/conductor-propagated (WARN-3) · hold the seating open for the
      § 5 ADDENDUM (WARN-4) · carry the two-limb clause form + the "asserted a check that never ran"
      category to run-close ratification (§ 8).
- [ ] **Matt:** nothing. No BLOCK, no cross-seam schema change, no conflict with a locked
      decisions-log entry. `Q65` remains in the queue unchanged by this seating.

## References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/kc2/alert.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/kc2/actor_state.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/kc2/gate_model.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/kc2/summons.py` (`:1073`, `:1079`, `:1109`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/kc2/locomotion.py` (`:1165-1196`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/kc2/pet_specials.py` (`:305-307`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_kc2_mc_b5_alert_2026_08_25.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_kc2_mc_b6_actor_state_2026_08_25.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_kc2_mc_b4app_gate_model_2026_08_25.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-{b3,b3app,b5,b6,b4app}-*.json`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-{b5-alert,b6-actor-state,b4app-gate-model}-*.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (`:10229-10236`, `:10376-10380`)
- `~/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-25-kc2-mc-lap-resid-d1-2/findings.md` (§ 5, § 9)
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md` (L-63…L-72)
- `~/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-08-25-gamora-kc2-mc-b3app-gate2.md` (BLOCK-1 origin)
