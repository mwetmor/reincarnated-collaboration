# Finding — 2026-07-28 — gamora — BQ-3 door · O-d leech · scratch-`max_hp` wake (CONSOLIDATED Gate 2)

**Reviewer:** jack-ryan (DEV-MODE, Gate 2, BLOCK authority)
**Severity:** **WARN** (no BLOCK issued)
**Targets:** `gamora/v-bq3-calibration-door-1` @ `c067bbd` · `gamora/v-od-leech-carryback-1` @ `67d165b` ·
`gamora/v-scratch-maxhp-wake-1` @ `9218238` (engine `main`)
**Developer:** gamora (simulation seam) · **Conductor:** gandalf (RUN-CONDUCTOR, KIT-CAL-1 `KC1-2026-07-27`)
**Scope class:** WITHIN-SEAM (ADR-002) — jack-ryan approves directly. Two MIGRATION entries owed to
star-lord are filed; the third correctly declares NO ACTION.
**Principles applied:** 1 (math-before-code), 2 (smoke gate), 3 (cross-seam impact), 4 (decisions-log
as truth), 5 (severity matters), 6 (cross-seam round-trip)
**Disciplines cited:** #1, #2, #3, #10, #11, #12

---

## VERDICTS

| item | verdict |
|---|---|
| **1. BQ-3 calibration-override door** | **PASS** |
| **2. O-d leech door** | **PASS** — 1 documentation condition (C-1) |
| **3. Scratch-`max_hp` wake (R-KC1-20/21)** | **CONDITIONAL PASS** — 5 conditions, all documentation
or harness-facing; **none requires reverting, re-measuring, or re-tagging** |

**G-5 is CLEARED TO FIRE.** No condition below gates the calibration finale. Two conditions (H-1, H-2)
are harness-facing and are flagged immediately per the conductor's standing instruction — they change
what harness assembly must assert, not what the engine does.

**On the offered BLOCK (queue doc §W-1): DECLINED, on the record.** gamora offered that a same-day
disposition reversal riding inside the same review as the thing it reverses is a legitimate BLOCK. It
is not, here. The reversal is Matt-ruled (R-KC1-20), marked in place with strikethrough rather than
deletion (`od-leech-carryback-2026-07-28.md` §6, LOUD-FLAG-1/-2/-5), carries a dedicated AMENDMENT
block in the test module docstring, and is stated in words in `MIGRATION.md` §3(b). Reviewing the two
together is *easier* than serially: item 3's entire justification is a response to item 2's refusal,
and splitting them would have forced me to re-derive that argument twice. Discipline #12 is satisfied
by naming the shift, not by sequencing it.

---

## What I verified first-hand (Discipline #11 — I did not take the reports' word)

| claim | how I checked | result |
|---|---|---|
| Door suites green | ran `pytest tests/test_od_leech_carryback.py tests/test_bq3_calibration_override_door.py -q -rs` | **76 passed, 0 skipped** (37 + 39) |
| Pre-registered digest `25c212eb…` unchanged | OD-1 / T-1 executed in that run | **holds** |
| NS-1 is not vacuous | same run, `-rs` | **NS-1 EXECUTED, did not skip** |
| Battery digests unchanged | read `…battery-{before,after}.json` directly | ARM PROD `9c4da4f7…` and ARM PROJ `94236eb0…` **byte-identical**, and PROJ counters moved in the same run |
| Two-path reachability premise | read `spatial_engine.py:5813-5828` | **TRUE** — `player_class is not None` → `combatant_from_player_class`; else projection |
| Census Y6 (shield) | `damage_resolver.py:1210` write → `:1076/:1159` read | **holds** |
| Census Y8 (silence) | `damage_resolver.py:1244` write → `spatial_engine.py:2219-2238` read | **holds**, gated on `WIRE_HARD_CC` (True) |
| Out-of-seam file still uncommitted | `git status --porcelain` | **` M` — uncommitted**, last commit `75637f5` (star-lord) |
| No landed test depends on its mutated state | grep `tests/ src/` | only reader is `tests/test_w3_emission_driver.py:585` (star-lord's, deselected), and it asserts on the **path string**, not content |
| L5 allow-list still EMPTY | `tests/test_bq3_calibration_override_door.py:492-494` + T-8 pass | **empty, green** |
| Wake regression counts | re-ran the documented `-k` selection, `test_w3_emission_driver` deselected | **34 failed, 1587 passed, 21 errors** — reproduces gamora's post-change numbers **exactly** |

---

## ITEM 1 — BQ-3 door: **PASS**

**The census overrule (queue doc §1) was CORRECT. Ruling: gamora's call, endorsed.** The census's
argument — *"the `defense` key already exists, so no new contract is invented"* — is inverted, exactly
as gamora says. `kit_compiler.py:630` emits `"defense": {"riders": []}` on every compiled kit, so
hanging override semantics on that key means the day a real `defense.armor` lands — the mechanism
Matt's amendment says is still owed — that mechanism silently opens the calibration door in
production, and every symptom looks like the mechanism working. A namespaced, nothing-emits-it key is
the only shape that keeps L1 true under the amendment. `T-3d` (a `defense` block carrying
`armor: 9999` is inert) and `T-8c` (nothing in the shipped tree emits `_calibration_overrides`) are
the right pair of assertions.

**L3 is load-bearing and it holds.** Verified in `calibration_overrides.py`: block-presence-without-
opt-in raises; unknown sub-keys raise with the known-set printed; non-finite / out-of-domain /
non-coercible raise; `assert_no_calibration_overrides` has no `allow=` parameter and `OD-7b` pins that
signature so a future edit cannot quietly relax the boundary. The rejected alternatives (env var,
global flag, runtime registry) are correctly rejected — all three are process state a production run
can inherit. **No stronger containment to propose.**

**Verbatim-not-`max(floor, override)` is right** and for the stated reason: `HP_BASE = 10,000` is a
balance anchor, not a numerical-stability floor; a `max()` would have returned 10,000 for a 1,600 HP
fixture and the harness would have reported a comparison it never ran. `T-5` pins it.

**§5's non-extension of the override to the kernel scratch was right AT THE TIME** and is now
superseded by R-KC1-20. That is not a retroactive fault — it is the disposition changing under a
ruling, and it is marked as such.

---

## ITEM 2 — O-d leech door: **PASS**, one documentation condition

**The reproduce-not-carry substitution (queue doc §O-1) was gamora's to make, and it was right.
Ruling: endorsed.** I re-derived it independently. `damage_resolver.py:1259` computes
`stolen = min(total_damage × pct, attacker.max_hp − attacker.hp)`; pre-wake the projection attacker's
scratch `max_hp` was the literal `1.0`, so the second operand was `≤ 0` in every reachable state. A
literal carry-back would have moved 0.000 HP while looking like a feature — the same failure mode
BQ-3 §4 rejects `max(floor, override)` for, and it would have contaminated the G-5 verdict rather
than an internal number. Shipping the ratified *words* over the ratified *intent* would have been the
worse infidelity. The C-8-class correction was stated in the math note before the code, not discovered
after — which is the whole point of Discipline #1.

**Refusing the "obvious repair" (queue doc §O-2) was also right at the time,** and the reason it was
right is what R-KC1-20 then had to overrule explicitly rather than assume: repairing one operand wakes
four operators. Matt overruled it on grounds gamora could not have supplied (no validated sim exists).
That is the correct division of authority — seam owner names the hazard, Matt takes the risk.

**Clamp placement verified in code** at `spatial_engine.py:2597-2605`: inside the per-target loop,
`_headroom = attacker.max_hp - attacker.hp` re-read per hit, `attacker.hp += _healed` before the next
target. `OD-6e` correctly guards the *stale-headroom* failure (`sum(min(cap_i, head_0))`), not the
sequential-vs-per-cast distinction, which is numerically identical for a monotone fill — the test is
aimed at the failure that actually exists.

**Delivered-damage base — the named deviation: consistently applied, and tested.** There is exactly
one application site, and it reads `_delivered_this_hit` (the overkill-clamped V2 quantity), not the
raw `dmg`. `OD-6f` pins it with a 5-HP mob and massive overkill. I agree with the choice: crediting
healing for damage never dealt would inflate hardest against the fixture's 58–813 HP trash, where the
run has 1,606 of its samples. **I do not want it changed.**

### C-1 — [WARN] the stated justification for the deviation is false as built (documentation only)

Queue doc §O-3 and math note §2.1(c) both say *"`capacity` is emitted alongside `healed` so the
deviation stays measurable."* It is not. `capacity` is accumulated from the **same** `_delivered_this_hit`
base (`spatial_engine.py:2598`), so `capacity − healed` measures the **overheal clamp's refusal** and
nothing else. Nothing in the two emitted leech fields measures the raw-vs-delivered gap the deviation
actually creates.

The gap *is* recoverable — at fight level, from `total_damage_dealt − delivered_damage_dealt` times
the percent, both already on the entity — so this is a wrong sentence, not a missing instrument.
**Action:** correct the sentence in math note §2.1(c) and the MIGRATION O-d entry, and tell the harness
where the quantity actually lives if G-5 wants it. Discipline #10.

### Digest exclusion-set growth (queue doc §O-5 ⚠): the guarantee is NOT hollowed

`OD-1c` asserts `_DIGEST_EXCLUDE_ROW − {fight_id, created_at}` and `_DIGEST_EXCLUDE_AGG −
{fight_results, decision_traces, telegraph_specs}` contain **only** `calibration_*`-prefixed names.
Two things make that sound rather than cosmetic: (a) `_combat_digest` hashes `dataclasses.asdict(r)`
minus the exclusion — so **any** new `SpatialFightResult` field that is not excluded breaks the digest
loudly, which is the correct default; (b) the O-d suite **imports** BQ-3's exclusion constants rather
than copying them, so the two suites cannot drift. Inertness is asserted separately by `OD-2` on both
row and aggregate. This is a correct decomposition. **The digest test does come out of O-d stronger
than it went in**, as gamora argued — I agree, and the reason is (a), which nothing in the queue doc
states: the exclusion set is *closed upward* by the digest's own construction.

### Regression-baseline honesty (queue doc §O-5 ⚠): the claim matches the instrument

The `git worktree` baseline could not support a pass-count comparison (1,494/88-skipped vs 1,585/0-skipped,
environmental), and gamora claimed only **"zero new failure names,"** with the failure-name set a strict
subset (55 vs 56, the extra being a glob over emitted manifests the worktree lacks). **That is exactly
what the instrument supports, and it is exactly what was claimed.** Flagging one's own weaker
instrument and offering the stronger form unprompted is the behaviour Discipline #11 is for. The wake's
same-tree stash baseline supersedes it, and I independently reproduced its post-change side — see
item 3, "Regression-baseline honesty".

### [INFO] the leech is applied only on the resolver branch — latent, currently unreachable

`spatial_engine.py:2545` gates on `_use_resolver`; the flat branch (`:2615-2642`) applies damage with
**no** leech block. A door player taking the flat branch would silently produce
`calibration_overrides_used=True`, `lifesteal_percent` in the stamp, and `healed = 0.0` — a silent
no-op of a door value, which is precisely what BQ-3's design refuses everywhere else. I traced it and
it is **unreachable today**: `build_resolver_skills` is 1:1 by construction, the door is reachable only
on the projection path, and every player-attacker call site (`:3426`, `:3515`, `:4583`) passes a real
`skill_idx` — the two `skill_idx=None` sites (`:4729`, `:4977`) are mob and ally attackers. No action
required; recorded so it is not rediscovered as a surprise.

---

## ITEM 3 — Scratch-`max_hp` wake (R-KC1-20/21): **CONDITIONAL PASS**

**The repair is correct and the single-sourcing is the right shape.** `player_pool_from_class_dict`
being the one expression both `entity_from_class_dict` and the projection factory call is not
cosmetic — duplicated, a door-supplied `max_hp` lands on one body and not the other, which is a
worse defect than the one being fixed. `OD-6d2` asserts `entity.max_hp == entity.combatant_state.max_hp`
on **both** the door-open and the derived path, which is the property that keeps it single-sourced.
Moving `hp` with `max_hp` is right and the reasoning is right: leaving `hp = 1.0` would give a
full-health player full-pool headroom from tick zero — strictly worse than the defect.

**The declined digest re-registration (queue doc §W-4) was CORRECT. Ruling: endorsed, and gandalf's
endorsement is upheld.** The commission predicted the digest would move and instructed a
re-registration. It did not move; I confirmed by executing OD-1/T-1. Performing the re-registration
anyway would have written a record asserting a golden master was reset when it was not — a *false
evidentiary artifact*, and the one class of error a golden-master discipline cannot survive, because
every later reader trusts the reset note over the code. Refusing a commissioned action because the
measurement contradicts its premise, and saying so in the note, is the correct behaviour under
Discipline #11 and Principle 4. **The commission's prediction was wrong; the measurement governs.**

**Inverted-semantics tests: they still discriminate, and OD-6d is strictly stronger than what it
replaced.** This was the question I was most prepared to BLOCK on, and it survives.

- **OD-6d** previously proved the clamp had moved *by magnitude* (heal ≫ the scratch's 1.0). The wake
  makes both operands large, so that inference would have gone **vacuous** — gamora is right that it
  stopped discriminating. The rewrite perturbs the kernel scratch across `(5,5)` / `(1600,1600)` /
  `(1, 10^7)` and asserts the heal is identical and equal to `delivered × pct` in all three. A clamp
  reading the scratch would return 0.0 / partial / unbounded — three visibly different answers. That
  is a **direct insensitivity proof** replacing an inferential one. It catches the original failure
  (clamp left at the kernel) *and* failures the old form could not (a clamp reading a mixed pair).
- **OD-10** previously pinned dormancy; it now asserts (a) no heal at full HP — correct behaviour, not
  dormancy — and (b) `heals_received == min(dmg × 0.50, headroom)` exactly, after re-sync. It fails if
  the scratch literal returns (zero heals, and the docstring says to re-read the math note before
  "fixing" it) and it fails if the operator over-heals. Its original job — *be the thing that fails
  when the story changes* — is intact; the story is the opposite one and the docstring says so in
  those words.
- **OD-10b** pins F-4 (the woken heal still does not reach spatial HP) and correctly names itself as
  the assertion to revisit when the carry-back is built.

**No-stack (NS-1/2/3): non-vacuous, confirmed empirically.**
- **NS-1 EXECUTED in this checkout — it did not skip** (76 passed / 0 skipped under `-rs`). The guard
  is structurally sound besides: `pytest.skip` raises `Skipped`, which derives from `BaseException`
  and therefore cannot be swallowed by the surrounding `except Exception`; and `assert kits` catches
  an empty `PILOT_KITS`. It cannot pass vacuously.
- **NS-2/NS-3 exactness holds.** Both force `scratch=(100.0, 1600.0)` so the kernel operator has real
  headroom, and both rig-check `combatant_state.heals_received > 0` **before** asserting — so neither
  can assert no-stack against a sleeping mechanism. NS-3's form (`player.hp − 100.0 ==
  approx(door healed)`, exactly) is the right level: it survives fixing F-4 and would fail on a
  one-HP kernel contribution.

**Census class rulings — HoT ruled BUILD (F-2): I decline the BLOCK gamora invited.** The
"missing field in a copy list" reading does not apply, and I checked rather than accepted the
argument. `effect_resolver.tick_effects`' HoT branch (`:121-129`) writes `combatant.hp`,
`heals_received` and `bc_signals.hot_recovered`, and returns **none** of them — the return contract is
`dot_damage` alone. There is no copy list to add a field to; the value never crosses the seam.
`heals_received` **is** conflated, verified at three writers — `heal` (`damage_resolver.py:1205`),
`lifesteal` (`:1262`), HoT (`effect_resolver.py:126`) — so a delta-read would carry lifesteal back and
double-count against the ratified O-d door, which is a correct and specific objection, not a general
one. A clean carrier does exist (`bc_signals.hot_recovered`), and electing it plus ruling the
clamp/ordering against the *spatial* pool is mechanism design. **F-2 is correctly BUILD-class and
correctly routed to Q-KC1-1.** The F-7 HALT is likewise right: an in-sync without an out-carry buys a
more truthful number that is still discarded, while changing when every operator sees a damaged pool.

**Regression-baseline honesty: the wake's instrument is the honest one, and I reproduced it.** I re-ran
the documented selection (`spatial|gauntlet|convergence|kit_compiler|telemetry|balance|resolver|combatant|wave`,
`test_w3_emission_driver` deselected) on the landed tree and got **34 failed / 1,587 passed / 21 errors**
— matching gamora's claimed post-change figures exactly, including the failure/error split she reported
as identical on both sides of the stash. The same-tree `git stash` baseline is the correct instrument
for this comparison and it is what was used; the 1,587-vs-1,585 delta and the diff-empty 55-name failure
set are supportable claims, unlike O-d's worktree pass counts. **This is the upgrade O-d's ⚠ asked for,
delivered unprompted.**

**Y6–Y9 docstring correction ("never dropped"): spot-checked, and it is CORRECT.** Y6 — `shield` is
appended to `attacker.active_effects` at `damage_resolver.py:1210` and read by `absorb_with_shield` at
`:1076/:1159` when the same entity is later a defender, off the same persistent scratch object. Y8 —
`silence` is applied to the defender scratch at `:1244` and consumed by the F8 selector gate at
`spatial_engine.py:2219-2238`, which reads `entity.combatant_state.active_effects` directly. Both
hold. Correcting one's own over-broad docstring rather than leaving it is Discipline #10 working.
One clause is owed: Y8 is conditional on `WIRE_HARD_CC` (`spatial_engine.py:740`, currently `True`) —
with the flag off, silence *is* dropped. See C-5.

---

## CONDITIONS

### H-1 — [WARN, HARNESS-FACING, FLAG IMMEDIATELY] freeze-shatter's dormancy argument is corpus-scoped, and the G-5 harness is outside that corpus

S4 is retired as **corpus-dormant** on 0/4,772 class skills and 0/2,332 mob skill-effects — i.e. the
**generation** corpus. The KIT-CAL-1 harness supplies **hand-authored GD fixture mob dicts**, which do
not come from that corpus. The path is open end to end:

- `_resolver_skill_from_dict` (`spatial_resolver_adapter.py:110-118`) copies each effect's `name` and
  `params` **verbatim** into `_ResolverEffect` — no allow-list, no filter;
- `freeze` is a live member of `AILMENT_NAMES` — I confirmed at runtime, not by grep;
- `effect_resolver.py:136-142` shatters on expiry for `max_hp × shatter_damage_percent` (default
  `0.20`) when `hp / max_hp < shatter_threshold_fraction` (default `0.25`).

**Pre-wake this was structurally impossible on the player** (`hp / 1.0 ≫ 1`). Post-wake, against the
fixture's door-supplied **1,600 HP** pool, one freeze expiry below 25% HP costs the player **320 HP** —
material to a G-5 verdict at that pool size. Execute is **not** exposed the same way: `_ResolverSkill`
carries no `execute_threshold_fraction` field, so `getattr(..., 0.0)` is structurally 0 regardless of
what the dict says. The asymmetry matters and the charter's §14.22 assumption #3 states both together.

**Action (harness assembly):** assert the G-5 mob dicts carry no `freeze` effect, **or** adopt
player-side shatter deliberately with the 20%-of-1,600 magnitude named in the harness note. Either is
fine; silence is not.

### H-2 — [WARN, HARNESS-FACING, FLAG IMMEDIATELY] L5's AST sweep root does not cover everything that can open the door

`_SRC_ROOT = parents[1] / "src" / "reincarnated"` (`tests/test_bq3_calibration_override_door.py:486`).
The G-5 harness **must** open the door. Two outcomes:

- harness under `src/reincarnated/` → **T-8 FAILS** until it is added to `_DOOR_ALLOW_LIST`. That
  failure is the design working; add the entry deliberately.
- harness **outside** that root → T-8 stays green and the allow-list is silently incomplete. That
  matters beyond hygiene: BQ-3 math note §5 LOUD-FLAG-3 designates the allow-list as *"the inventory
  of everything that must be re-pointed when `_calibration_overrides` is DELETED."* An incomplete
  inventory means the scheduled-deletion plan (queue doc §7) misses a consumer.

**Action (harness assembly):** place the harness under `src/reincarnated/` and add it to
`_DOOR_ALLOW_LIST`, or widen `_SRC_ROOT`. Note the same applies to the R-KC1-19 replay-trace writer if
it is authored outside the seam.

### C-2 — [WARN] the math note cites two tests that do not exist, and one of them is the load-bearing one

`scratch-maxhp-wake-2026-07-28.md` §1.1 says *"`T-W6` asserts `entity.max_hp == entity.combatant_state.max_hp`"*;
§2 says the two-path reachability property *"is asserted by `T-W5`"*; §3a S9 cites `T-W6` again.
**Neither identifier exists anywhere in `tests/` or `src/`.**

- `T-W6`'s content **is** covered — by `OD-6d2`, under a different ID. Citation error only.
- **`T-W5` has no counterpart at all.** The property it claims to assert — *"season generation never
  takes the projection path"* — is the load-bearing premise of the entire blast-radius bound, the
  reason no season can move, and (per C-10) the correction gamora issued to both the conductor's
  framing and her own. It is asserted **in prose only**.

I verified the premise myself and **it is TRUE** (`spatial_engine.py:5813-5828`: `if player_class is
not None` → `combatant_from_player_class`, `else` → `combatant_projection_from_class_dict`; the
production callers thread a real `PlayerClass`). So the claim is sound and I do not block. But a
reachability property stated as test-asserted when it is not is the kind of citation a later reader
trusts without re-checking — and this one is guarding a class of change that will recur.
**Action:** add the assertion under a real ID (a two-line test over the two factories would do it), or
strike the citation and mark the premise as prose-verified. Discipline #10/#11.

### C-3 — [WARN] `45` vs `42`: a wrong measured number sits in a production docstring

`spatial_resolver_adapter.py:422` states *"`on_lifesteal` went 0 -> 45 fires over a 6-fight battery,"*
and math note §3a S1 and §3b Y3 repeat `0 → 45`. The evidence says **42**:
`2026-07-28-kc1-scratch-maxhp-wake-battery-after.json` → `arms.PROJ.counts["player.lifesteal.FIRED"] = 42`,
matching math note §7.2, charter §14.22, and the OD-10 docstring. `45` appears nowhere in the evidence.

The number is not load-bearing, but it is a *measured* number inside production code, in a file whose
whole purpose this session was to stop misleading its reader. **Action:** correct all three sites to 42.
Discipline #10.

### C-4 — [INFO] the pre-registered digest is structurally non-discriminating for the wake — say which digest carries the weight

`25c212eb…` is computed over `_class_dict()`, whose only skill carries `damage` + `burn`. **None of the
five woken operators (S1 lifesteal / S2 heal cap / S3 HoT tick cap / S4 freeze / S5 execute) is even
present in that batch.** The digest could not have moved regardless of the repair. It is true that it
is unchanged, and it was right not to re-register it — but it is not evidence about the wake's blast
radius.

The **discriminating** instrument is the battery **ARM PROJ digest `94236eb0…`**, whose kit carries
`lifesteal` / `heal` / `heal_over_time` (harness `:132-137`), whose mobs carry lifesteal (`:204`),
whose counters demonstrably moved in the same run that produced the identical digest
(`lifesteal.FIRED` 0→42, `hot.HEALED_SCRATCH` 0→51, `scratch_heal.NONZERO` 0→84), and whose exclusion
set matches the door suites'. **The evidence chain holds — through the battery.** §7's three-row table
presents all three digests as equivalent evidence and does not say which one is carrying the argument.
**Action:** one sentence in §7 naming ARM PROJ as the discriminating instrument and `25c212eb…` as a
non-regression check. No re-measurement needed.

### C-5 — [WARN] stale production comment at the exact site the no-stack property must be preserved

`spatial_engine.py:2570-2596` — the O-d leech block's own inline comment — still asserts:

> *"the kernel … clamps it with `min(steal, max_hp - hp)` against the PROJECTION SCRATCH state, whose
> max_hp is the literal 1.0 (`spatial_resolver_adapter.py:233`). MEASURED: that operand is <= 0 in
> every reachable state, so the kernel's steal is identically zero here"*

and closes with *"which stays dormant (math note LOUD-FLAG-1/2)."* **Every clause of that is now
false.** The wake commit corrected the adapter docstring (`:392-437`) but not this one — and this is
the strongest doc-drift of the three items, because it is **co-located with the mechanism it
misdescribes**, at the one site where a future editor must understand that the kernel operator is
awake and must not be allowed to stack. NS-1/2/3 defend the property with tests; this comment argues
against them in prose. **Action:** rewrite the block to match the adapter docstring's corrected form.
Discipline #12. *(Two smaller siblings, INFO, same pass: math note §9 reads "thorns (Y5), offense-site
event consumption (Y6)" — those are Y4 and Y5, Y6 is `shield`; and the O-d math-note §7 test-map row
for OD-10 still reads "kernel lifesteal is STILL dead," un-struck, though the §0 banner covers it.
Also add the `WIRE_HARD_CC` clause to census Y8.)*

---

## Cross-seam (Principle 3 / Principle 6 / ADR-004)

**star-lord — ACTION OWED, correctly filed.** Four additive `SpatialFightResult` fields across BQ-3 and
O-d (`calibration_overrides_used`, `calibration_override_fields`, `calibration_lifesteal_healed`,
`calibration_lifesteal_capacity`), all defaulted-inert on production rows, with the non-optional part
being MIGRATION §2's rule: **any analysis, export, band-fit or aggregate mixing
`calibration_overrides_used = True` rows into a production population is INVALID**; filter `= 0` by
default. The single-filter argument is correct — a row with `calibration_lifesteal_healed > 0` is by
construction also `calibration_overrides_used = True`.

**The rehydration check is right, and it is right for the stated reason** — which matters, because it
is the SESSION-76 `liveness_gate_version` hazard I raised, re-examined rather than pattern-matched.
`SpatialFightResult(**archived_pre_BQ3_row)` yields `False`/`""`/`0.0`, and that is *true* for every
such row: there is no era in which a row could have been calibration-stamped and then lost the field,
so absence is unambiguous. No pre-splat normalisation idiom is owed. `T-2b` states it as a property so
a future default change has to argue with a test. **Correct, and correctly distinguished from the case
where it was not.**

**Wake MIGRATION declares NO ACTION and that is accurate** — 47 fields before, 47 after; no column, no
`_INSERT_SQL` change, no producer change.

**rocket owes nothing** on all three items. Confirmed.

---

## Out-of-seam file — `src/reincarnated/output/leg3_pilot_section8a1_band_measurement.json`

**Still uncommitted — confirmed** (` M`, 21 insertions / 87 deletions against `75637f5`, star-lord's
R2 before-side snapshot). **No test in either landed door suite references it** — the only reader in
the tree is `tests/test_w3_emission_driver.py:585` (star-lord's, deselected from both regression runs),
and that assertion is on the **path string**, not on file content; the driver rewrites the file on each
run. So neither landed suite depends on its mutated state, and neither would notice if it were
restored.

Leaving it uncommitted was the right call — gamora does not commit into another seam (ADR-004).
**Residual hazard worth naming:** it is a *tracked* file sitting dirty across three commits and two
sessions. Any future `git add -A` in this tree sweeps star-lord's seam into someone else's commit, and
the KIT-CAL-1 run has several agents working the same tree. **Action (star-lord, via KR):** inspect,
then restore or adopt — and do it before the next multi-agent commit wave, not at wind-down.

---

## Decisions-log (Principle 4) — jack-ryan to draft; capture, not gate

Three entries, and **the O-9 entry proposed under O-d must NOT be filed as written** — gamora is right
that R-KC1-20 falsified it the same day (queue doc §W-9). I will file:

1. **The calibration-override door is a debt marker with a scheduled deletion.** It exists only until
   real player-defence and player-HP mechanisms land; at that point `_calibration_overrides` is
   **deleted, not migrated**, and L5's allow-list is the re-pointing inventory — **subject to H-2**,
   which is what makes that inventory complete or not.
2. **The spatial projection player has a real HP pool in kernel eyes (R-KC1-20)** — gamora's §W-9
   replacement text, which I accept as drafted, plus one clause: *the repair removed a divergence
   between the projection and production paths rather than introducing a behaviour* (C-10), and
   *freeze-shatter and execute are corpus-dormant, not structurally dormant* (the expiry-dated fact,
   and H-1's near-term instance of it).
3. **Skill-borne kernel lifesteal fires on the production path and its heal is discarded (F-4).** The
   §W-9 correction (C-11) distinguishes two deaths: the projection-path clamp death (repaired) and the
   production-path discard (unrepaired, BUILD-class, Q-KC1-1). Recording this stops a future session
   from "fixing" the discard as an obvious oversight and double-counting against the O-d door.

---

## Action checklist

- [ ] **gamora (documentation pass, no code):** C-1 (`capacity` sentence), C-2 (`T-W5`/`T-W6` — add the
      assertion or strike the citation), C-3 (45→42, three sites), C-4 (name the discriminating
      digest), C-5 (`spatial_engine.py:2570-2596` comment + the three INFO siblings). **No re-tag
      required** — these are notes and comments; land them on a follow-on commit.
- [ ] **gamora / harness assembly:** H-1 (assert no `freeze` in G-5 mob dicts, or adopt shatter with
      the magnitude named), H-2 (harness under `src/reincarnated/` + `_DOOR_ALLOW_LIST` entry, or widen
      `_SRC_ROOT`).
- [ ] **star-lord (via KR):** inspect `leg3_pilot_section8a1_band_measurement.json`, restore or adopt,
      before the next multi-agent commit wave.
- [ ] **jack-ryan:** file the three decisions-log entries above.
- [ ] **Matt:** nothing required. No BLOCK issued, no escalation. Recorded for awareness: this review
      cleared a same-day disposition reversal of a decision the seam owner had refused twelve hours
      earlier — the reversal was yours (R-KC1-20), and it is marked as yours in every artifact.

---

## References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/bq3-calibration-override-door-2026-07-28.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/od-leech-carryback-2026-07-28.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/scratch-maxhp-wake-2026-07-28.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/calibration_overrides.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (`:2532-2642`, `:5638-5690`, `:5813-5828`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_resolver_adapter.py` (`:110-138`, `:173-198`, `:241-290`, `:392-437`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py` (`:977`, `:1203-1263`), `effect_resolver.py` (`:121-142`)
- `~/Games/reincarnated-engine/tests/test_bq3_calibration_override_door.py`, `tests/test_od_leech_carryback.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (three 2026-07-28 entries)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_kc1_scratch_maxhp_wake_battery_2026_07_28.py`
- `~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-28-kc1-scratch-maxhp-wake-battery-{before,after}.json`
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` §§14.12–14.22
- `~/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-07-28-gamora-bq3-calibration-override-door.md`
