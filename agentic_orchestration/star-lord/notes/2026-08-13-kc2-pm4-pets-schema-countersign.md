# KC2-PM4 — star-lord cross-seam cell: **the pets countersign, the mask completion, and a rename I left half-finished in July**

> **Run:** KC2-PM4 (conductor: gandalf, `RUN-CONDUCTOR`) · **Cell:** export-seam cross-seam
> commission, fired after gamora's I-2 landing · **Author:** star-lord (export / output /
> telemetry / llm) · **Date:** 2026-08-13
> **Answers:** `reincarnated-engine/src/reincarnated/export/MIGRATION.md` `[2026-08-13]` I-2 entry ·
> gamora's landing note § 12 (three calls) and § 9 defects 5 + 6
> **Status:** COMPLETE. Validator **32 → 33** checks; **17/17 batons re-gate GREEN**; baton test
> file **98 → 115** passing. **No baton rewritten. No simulation code touched. No driver touched.**

---

## 0 — The one-paragraph answer

**All three of gamora's calls are decided, and the countersign found a fourth thing nobody
asked about: `waves[].pets[]` landed on the wire carrying 17 fields and *zero* boundary
validation.** M-13's basis predicate reads `actors[]`, and the whole point of `PetActor` is that a
pet is not an actor — so the widening that covered `Actor.hp_max_basis` at I-1 covered nothing
here. A new field with no check at the write boundary is Discipline #8's named failure mode and it
is the export seam's to close, not the simulation seam's. `G-PETS` closes it, with five obligations
and eleven falsification tests. **Separately: `PROVENANCE_VOLATILE_KEYS` is repaired — and the
repair that mattered was not adding the missing key, it was that the mask had never stated whether
it applied at the top level or at every depth, and its two consumers had each guessed differently.**

---

## 1 — ⚑ THE COUNTERSIGN: `Wave.pets: list[PetActor] = []` — **ACCEPTED AS PLACED**

The field earned the signature before it got it, which is the right order. **The kills identity now
closes on the wire alone**, no driver in the loop:

```
run_summary.actors_killed        183   (roster bodies only — correct, and now CHECKABLE)
pets with death_cause == "killed_by_player"   584
                                 ---
                                 767   = the reference cell's kill count, EXACT
```

⚑ **One accounting correction to the commission text and to the landing note § 6.1 gloss.** The
sum quoted as "584 player-killed + 6 ttl_expired + 183 roster = 767" is **773**, not 767. There are
two identities and they are different sums:

* **kills:** `183 roster + 584 pet player-kills = 767` ✔
* **pet population:** `584 killed + 6 ttl_expired + 30 alive-at-death = 620` ✔

**The 6 TTL expiries are not kills** and must not enter the 767. The finding is unaffected — both
identities close exactly — but a wrong arithmetic gloss on a correct finding is how a correct
finding later gets doubted, so it is corrected here rather than inherited.

### The three calls

| call | verdict | the reasoning that decided it |
|---|---|---|
| **(a)** `PetActor` in `baton_v1_schema` or a sim-side sidecar? | **SCHEMA. Accepted as placed.** | A sidecar is a second artifact with its own path, digest, write-ordering, and its own way of going missing — joined to the baton by convention. The baton is drax's ONLY input by charter § 11, and `owner_id` / `spawn_tick` are joins **into** `actors[]` and `events`. **A join that lives in another file is a join a consumer can silently skip.** The blindness this field closed was caused by a fact living where the wire could not see it; a sidecar re-opens exactly that, in better-looking clothes. |
| **(b)** `Literal` enums for `hp_max_basis` / `death_cause`? | **SPLIT** — `death_cause` **YES**, `hp_max_basis` **NO** | The split is on whether the vocabulary is **closed**. `death_cause` is closed, tiny and sim-authored; a typo there is silent and a consumer counting kills just under-counts. Now `PetDeathCause = Literal["killed_by_player", "ttl_expired"]`. **Measured before closing:** exactly those two plus `null` across all **1,869** pet rows on the three I-2 batons. `hp_max_basis` is **PARAMETRIC** — `MEASURED-PET-BAND-B-LO@w{wave}` embeds the wave — so a `Literal` could only be written by enumerating waves, i.e. a schema that must be edited every time the sim fights somewhere new. **It is validated at the boundary instead**, against `PET_HP_MAX_BASIS_EXACT` + `PET_HP_MAX_BASIS_PREFIXES`, exported as `pet_hp_max_basis_is_known()` so a consumer checks the *same* rule the wire is gated on rather than re-deriving a near-miss of it. |
| **(c)** `_integrity.pet_count`? | **GRANTED, additive-nullable** | Every member of `_integrity` exists so a **truncated structure cannot pass as a short one**. `pets[]` arrived as the second-largest array on the wire with no such guard. `Optional[int] = None`; the emitter now always sets it, **including `0`**. `AC-11.6` checks it **only when present** — absence means "not declared", `0` means "declared, and there were none", and **collapsing those two is precisely how a dropped array passes as an empty one**. The 3 I-2 batons predate the field and validate with the check skipped; gamora's next emission carries it. |

### ⚑ And the thing nobody asked about: **G-PETS**

Five obligations, each one a thing a consumer would otherwise have to take on trust:

1. `actor_id` unique run-wide **and disjoint from `actors[]` and the reserved player id** — a pet
   id and a roster id can never accidentally join to each other.
2. `owner_id` **RESOLVES** into `actors[]`. This is the join that turned the conductor's L-2
   `w160_pet0011`-vs-`w160_a001` ambiguity into a lookup instead of a dispute. **An unresolvable
   owner is that dispute coming back silently.**
3. Death is **one fact stated three ways**: `alive_at_wave_end` ⟺ `death_tick is None` ⟺
   `death_cause is None` ⟺ `death_t_s is None`, with `death_cause` inside the closed vocabulary.
   `death_tick: null` for a pet that outlived the run is a **fact**; this is what keeps it readable
   as one rather than as a hole somebody later "fills".
4. `spawn_tick` inside its own wave's `[tick_start, tick_end]`; `death_tick >= spawn_tick`. The
   tick is the key, and a key outside its wave joins to nothing.
5. `hp_max_basis` drawn from the known vocabulary — call (b)'s open half, made checkable anyway.

**Green on arrival: all five already hold on all 1,869 landed pet rows.** `G-PETS` is a guard
against the next lap, not a finding about this one — and it is *because* it is green on arrival that
the 11 falsification tests matter: each breaks exactly one obligation and asserts the gate reds.

⚑ **Consumer-visible:** `validate_baton_wire` returns **33** results, not 32; the adapter's full
gate wall reads **67**, not 66 (`VALIDATOR 33 + G-E 33 + G-STATS 1`).

⚑ **And here I was wrong out loud, and the tree corrected me.** I first wrote *"nothing in the tree
hard-codes the number"* — I had grepped the **simulation drivers** and not the **tests**.
`tests/test_kc2_run_adapter.py::test_HALT_PIN_the_gate_wall_refuses_the_emit_and_names_all_four`
asserts `len(run.results) == 66` **and** the wall's `Counter` composition, deliberately: *"a gate
cannot silently LEAVE the wall either: a shrinking denominator is the cheapest possible green."*
**The composition guard fired on a denominator that GREW, which is exactly what it is for.** Pin
moved to 67 with the reason written into its docstring rather than absorbed. **A wall that grows
must say so as loudly as one that shrinks.**

---

## 2 — ⚑ `PROVENANCE_VOLATILE_KEYS` — **TAKEN.** Handed over at I-1, again at I-2. Repaired.

```python
EMISSION_IDENTITY_VOLATILE_KEYS = ("_emitted_at", "baton_run_id")
HOST_STATE_VOLATILE_KEYS = ("tree_state_untracked_entries_excluded",
                            "tree_state_untracked_entries_outside_src")
PROVENANCE_VOLATILE_KEYS = EMISSION_IDENTITY_VOLATILE_KEYS + HOST_STATE_VOLATILE_KEYS
```

**The split is by CAUSE**, because the two causes are not the same kind of fact. Emission identity
is minted per emission, by design. Host state measures the **machine** at emission time, not the
run — and the schema's own note on those fields already said so: *"The count is provenance colour;
the grade is the claim."* **`engine_tree_state`, `tree_state_policy`, `engine_version_sha` — the
grade, the rule, the code pin — are NOT masked and never will be.** Those are claims about the run.

**Reproduced and closed, measured on the I-2 reference baton** (clone it, bump the three keys):

| mask | differences |
|---|---|
| raw | 3 |
| OLD tight mask | **1** — `sim_pin.tree_state_untracked_entries_excluded: 2703 != 2704` (the reported defect, to the digit) |
| **completed mask** | **0** |

### ⚑ The deeper defect, which is the reason this was worth doing properly

The mask **never stated its own semantics**, and its two consumers each guessed differently: the
emitter's own test did `pop()` at the top level, gamora's scripts stripped at every depth. **They
agreed only because every key happened to be top-level.** The instant a nested key joined the
tuple, a top-level `pop` of it becomes a no-op **that reports EXACT** — a determinism check that
passes by not looking. So the fix is not only the missing key:

* `mask_volatile(payload)` is now the one application, strip-at-every-depth, non-mutating.
* The emitter's own determinism test was moved onto it, and a regression test
  (`test_volatile_mask_is_complete_and_strips_at_depth`) pins the nested behaviour, pins that the
  **grade** is never masked, and pins non-mutation.
* gamora's locally-DECLARED `HOST_STATE_KEYS` (PM-1 findings script) is now redundant. **It was
  right, and it was declared out loud, and it proved the tight mask insufficient — it was just
  living in the wrong seam.** Nothing of gamora's was edited; the import gets the fix for free.

---

## 3 — ⚑ THE `water→ice` FAILURE IS MINE, IT IS FOUR WEEKS OLD, AND THE FIX IS NOT THE RENAME

**Diagnosis.** Commit `1038e285` (2026-07-12, **mine** — "star-lord: water→ice substrate rename
across llm/telemetry/export, Unit 3 / Wave 2") renamed the substrate display value `water` → `ice`
across three of my four sub-areas and updated **two** test files (`test_d2_substrate_coupling`,
`test_ws1a4_lite_flavor_judgment`). It missed a **third**:
`tests/test_cycle13_normal_season_export.py::TestRoundTrip::test_manifest_has_elements_block`
carried its own hand-copied `["fire", "wind", "water", "earth"]`.

**It has failed on every run since, and it took another seam's full wall to surface it.** That is
the part worth writing down: a red test in my seam sat red for four weeks and the person who
noticed was gamora, running a wall for an unrelated reason.

**Why the one-line rename would have been the wrong fix.** Re-typing `water` → `ice` in the
assertion restores green and leaves the duplicated literal — the actual defect — armed for the next
rename. So instead:

* `CYCLE13_CANONICAL_ELEMENT_IDS = ("fire", "wind", "ice", "earth")` hoisted out of
  `_build_season_manifest`, which now builds the `elements` block **from** it.
* `_validate_canonical_element_ids()` runs **at import** against
  `generation.kit_space_schema.CANONICAL_ELEMENTS_LOWERCASE` — the engine-wide canonical-7+1 set
  that elrond's shadow-table CHECK constraint also matches, and the same cross-seam import
  `export/kit_space_emitter.py` already makes. **Had this existed in July, the rename would have
  raised at import the instant the canonical set moved** (Discipline #8) instead of failing
  quietly in one un-updated assertion.
* The test asserts against the constant, not a copy of it (Discipline #9).

**Output bytes UNCHANGED — verified**, at insertion order and under the writer's `sort_keys=True`.
53/53 in that file pass.

⚑ **NOT touched, on purpose:** `seasonal_elements.suffusion.canonical_slot` is still `"water"`.
That is the **slot-routing** layer, deliberately excluded from `1038e285` per Discipline #14 — it
names a slot, not a substrate display value. "Fixing" it would be a real output change dressed up as
a typo repair. Written down so the next reader does not correct it.

### ⚑ 3.1 — And chasing the test literal found the SAME COMMIT SILENTLY DROPPING WHOLE KITS

This is the part I would not have found by fixing the assertion. `kit_space_emitter` reads
`export_dict["dominant_element"]` — a persisted **substrate-display value** — and tested it against
`CANONICAL_ELEMENTS_LOWERCASE` **without** the `elem_rekey_water_to_ice` normalizer that `1038e285`
applied at every other export read boundary. A historical dict carrying `water` hit
`log.warning(... "— skipping"); continue`.

**The kit was dropped from the emission entirely** — absent from `kits/`, from the kits index, and
from the chronicle event — leaving nothing downstream able to distinguish a *dropped* kit from a
kit that never existed. **A silent drop at an export boundary, behind a WARNING.** Measured on the
emitter's own fixture: **17 of 20 kits emitted; 3 `water` kits vanished.** That is the failure mode
this seam exists to prevent, shipped by me, four weeks ago, in the same commit.

Fixed by **importing** the rocket-authored shared contract
(`simulation/resistance_matrix.normalize_substrate`, a pure leaf module) rather than writing a
fourth hand-copy of a one-entry remap — a fourth copy is how the next rename gets missed too.
**⚑ Consumer-visible**, and MIGRATION-filed as such: a `water` export dict that previously produced
*no* kit now produces `kit_ice_<seq6>`, so kit counts, `kits_index`, per-primary sequence numbering
and the chronicle event's `kit_ids` all move for any batch containing historical `water` kits. It
restores intended behaviour rather than adding new behaviour — **but a consumer that recorded the
short counts recorded a bug.** `test_kit_space_emitter.py` 27 → **31 passing** (all 4 of the
failures gamora's wall attributed to that file).

**Not consolidated here:** `one_realm_bundle_assembler._normalize_catalog_element_water_to_ice` is a
fourth local copy of the rule with a different shape (it walks a catalog dict). Correct and in use;
consolidating it is a separate in-seam item, flagged not taken.

---

## 4 — ⚑ A CLAIM IN THE I-2 MIGRATION THAT IS NOT TRUE, MEASURED BEFORE I TOUCHED ANYTHING

The I-2 entry says the fourteen frozen batons *"still validate and round-trip unchanged."*

| claim | verdict, measured at `e9e73adb` in an isolated worktree |
|---|---|
| re-**validate** / re-**gate** unchanged | **TRUE — 17/17 green** |
| **round-trip byte-for-byte** | **FALSE, and already false before my change: 3 of 17** |

The 14 pre-amendment batons re-serialise with `waves[].pets: []` **added**, because that is what a
defaulted field does. `_integrity.pet_count: null` now joins it, taking the figure to **0 of 17**.

**This is benign and it is not a regression** — frozen batons are verify-from-bytes and are never
rewritten, every consumer path (`read_baton` → validate → gate) is unaffected, and
`from_wire(payload) == baton` model equality still holds. **But "round-trips unchanged" is a
byte-level claim and it was not true when it was written.** Any additive defaulted field on a
countersigned model has this property. The correct sentence is "re-validates and re-gates
unchanged", which is true and is the thing that matters. Corrected in MIGRATION § 4 rather than
inherited.

---

## 5 — WHAT I DID NOT TOUCH

`simulation/` · the pm4 driver scripts · all 17 batons (read-only, verified from bytes, never
opened for writing) · `run.py`'s sim-side pet surface · gamora's `HOST_STATE_KEYS` declaration ·
`seasonal_elements[*].canonical_slot`. **Pets do NOT enter `actors[]` — gamora's refusal stands and
the countersign upholds it; `G-PETS` obligation 1 now makes the id spaces provably disjoint, which
is the same refusal expressed as a check instead of as a convention.**

---

## 6 — SELF-ATTACK

1. **`G-PETS` is green on arrival, which means it has never caught anything.** Its whole value is
   prospective. The 11 falsification tests are the only evidence it *can* catch anything, and they
   test the checker, not the wire.
2. **`pet_count` is nullable, and nullable-when-skipped means the three I-2 batons carry an
   unguarded 620-row array forever.** The guard only binds from the next emission. I chose
   backward-compat over retroactive coverage; the alternative was rewriting frozen artifacts, which
   is not a trade I would make.
3. **Closing `death_cause` to a `Literal` is a NARROWING of a field that is four hours old.** It is
   the right moment to do it (one lap of data, three batons, no external consumer yet) and the
   wrong moment to be confident: I closed it on 1,869 rows from **one fixture at one checkpoint**.
   If a future contract emits a third cause, this is a schema amendment — deliberately.
4. **The `water→ice` failure is the real finding of this cell and it is about me, not about pets.**
   I shipped a rename in July with a test-update gap, and my own seam's wall would have told me on
   the same day. The import-time validator makes that specific class loud; it does not make me
   more likely to run the wall.
5. **I did not price the `mask_volatile` change against every consumer.** I grepped the tree and
   the only importers are gamora's PM-1 findings script (which gets the fix for free and will now
   report tight ≡ extended) and my own test. If something outside the tree imported the tuple and
   depended on it having exactly two members, it breaks — and I would rather it broke than that it
   kept reporting EXACT while drifting.

---

## 7 — PINS

**Engine at launch:** `e9e73adb`. **Files changed (explicit paths, no `git add -A`):**
`export/baton_v1_schema.py` · `export/baton_v1_emitter.py` · `export/baton_v1_validator.py` ·
`export/cycle13_normal_season_export.py` · `export/MIGRATION.md` · `export/AGENT_STATE.md` ·
`tests/test_baton_v1.py` · `tests/test_cycle13_normal_season_export.py`.
**Gates:** validator 33/33 · stub green · **17/17 batons** · `test_baton_v1.py` **115 passed** ·
`test_cycle13_normal_season_export.py` **53 passed**.
