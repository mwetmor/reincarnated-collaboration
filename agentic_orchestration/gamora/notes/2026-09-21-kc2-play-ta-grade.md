# KC2-PLAY · T-A **GRADE** — verdict **`STRUCTURAL`** @ coverage **89/89**, 6/6 counted band rows graded

> **STATUS:** CURRENT — W3 grading seat. **Author:** gamora (simulation seam), 2026-09-21.
> **Graded object:** drax's `kc2_runtime` emission at `~/Games/reincarnated-godot/tmp/kc2/ta/` —
> **25 cells, 0 emission failures**, manifest `kc2play.ta_manifest.v1`, runtime `0.3.0-w3-fight-and-ta`
> (`c031aef`, built on `9bb8a99`).
> **Graded against:** prereg **v1.4** (IMMUTABLE), my own band-widths file **P-a** and its three addenda,
> register **v0.3**, `V0` limb set.
> **Authority:** grading only. ⚑ **NO WIDTH WAS ADJUSTED. NO ROW WAS RECLASSIFIED. NO BAND WAS RESCUED.**
> Where the prereg could not decide something it is **reported as a finding about the prereg, never repaired**.
> **K-7 held** — all three sealed cells `shasum`-verified before any read, opened READ-ONLY by key, never re-run.
> **This is graded run #1 against v1.4.** Two graded runs against v1.4 both `STRUCTURAL` ⇒ HALT to Matt (§ G).

---

## § 0 · PINS — **every one derived this session by `shasum -a 256`, none retyped**

| pin | artifact | prereg v1.4 says | **derived here** | state |
|---|---|---|---|---|
| **P-a** | `gamora/notes/…-ta-band-widths.md` | `7a5d4aa3…` | `7a5d4aa3305ed14748a903b60ebfe48ac1a186fdb951fb6b8608abba92406750` | ✓ |
| **P-b** | galadriel T-B expected-values note | `8186202c…` | `8186202cc0c78ae9ef428c57164fac35bd1adb0e14ec5310c395783361653158` | ✓ |
| **P-c** | galadriel expected-values JSON | `a8b85331…` | `a8b85331764ba3fe90f45cf7cd6f1a25f6dc0dae4a7e7fa555c487f0b153ea0b` | ✓ |
| **P-d** | galadriel release-labels JSON | `15dace60…` | `15dace604c8d5bb4888223a8b25a07a038bae44431ebd194d682545c0f29c58a` | ✓ |
| ⚑ **P-e** | `…/simulation/math/kc2-play-v3p3-monster-offense-prereg-2026-09-20.md` | **`97e5a4c7…`** | ⚑ **`27fc59378aee8c9d412f486a63864a3b2ceb5c5473520b60ad80128d47d99cdc`** | ⚑ **MISMATCH — § 0.1** |
| **P-f** | v3.3 lifted rows (11,847,705 B) | `e51b54a1…` | `e51b54a118f657ba7abd4298e5fcea86cfab3aeedebf8dd70a1239c5ea1b776e` | ✓ |
| **P-g** | v3.2 lifted rows (362,156 B) | `e0117429…` | `e011742935f14efaba2e9eb45e7bca11e1131fc19d6f936526498d4f7ac1af96` | ✓ |
| prereg v1.4 itself | — | (self) | `3c83c7ac9a80bf20f34034a6e91765f08bcad34a8d5b97dc4c354e2e2e245cdf` | derived |
| register v0.3 (file) | — | *(machine form pinned, not file hash)* | `5028b555313df2f4690cd96881c700c7d66a4733612894c150c2448915510444` | derived |
| register v0.3 (machine form) | emitter-derived | — | `453231e0afefbf101010677bb72e685c43c2fa68666dbac44f118d1e14b07e68` (emitted, 28 rows) | ✓ consistent |

**Sealed cells, hash-verified and never opened for anything but a keyed read:**

| cell | pinned | **derived** |
|---|---|---|
| `[M-POL2]` `…-mpol2-20260825_114420.json` | `ad61ad2a8c799d6e` | `ad61ad2a8c799d6ef11a68436756c253f0a34fbb1052e575cdf9f9cd3a44dc5c` ✓ |
| `[MECH]` `…-mech-20260816_124031.json` | `20b05cb4ef3bd888` | `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b` ✓ |
| `[W1W]` `…-w1walls-20260825_220058.json` | `7a992c81ca6e56e5` | `7a992c81ca6e56e54a53534b438a9ddf87ed42f1bf1a3d0ecc2d2f3c3db7881b` ✓ |

### ⚑ 0.1 · **CAP CONDITION `C1` IS TRIPPED — P-e's pin does not reproduce, and the reason is worse than a stale byte**

`C1` is *"verdict file absent / unparseable / **any pinned sha mismatched**."* P-e's does not reproduce.
**The full chain, derived from git, not inferred:**

| commit | time | file sha256 | what it is |
|---|---|---|---|
| `7119e4a9` | 21:54 | ⚑ **`97e5a4c7…` — THE PIN** | the Addendum (weighted-coverage read) |
| `5adf9c23` | 21:57 | `2e211c9e…` | ⚑ **ADDENDUM 2** — the 4.7 σ resolution |
| *(prereg v1.4 filed)* | **22:12** | — | pins `97e5a4c7…` |
| `b87e282c` | 22:17 | ⚑ **`27fc5937…` — CURRENT** | the dead refusal rule **struck at all four sites** |

**Two distinct defects, one in each direction, and I own the second:**

1. ⚑ **The prereg's pin annotation is factually false.** It reads *"This sha covers the body AND both addenda — the Addendum-2 σ correction is inside it."* **It does not.** `git show 7119e4a9:<path> | grep -c "ADDENDUM 2"` returns **0**. The pinned commit predates Addendum 2 by three minutes. *(The prereg's § E.3 nevertheless reproduces Addendum 2's content correctly and in full — so the prereg **read** the right document and **pinned** the wrong revision of it. The reasoning is sound; the pin is not.)*
2. ⚑ **The prereg's own `OQ-2` asked me to change a file the same document pins, and said nothing about the pin moving.** OQ-2: *"Ask gamora for a strike-through pointer AT § 5, not only at the addendum."* I filed exactly that at `b87e282c`, five minutes after v1.4 was filed. **That half is mine.** Neither party did anything wrong in isolation — **the process has no rule for "a pinned artifact whose pinning document requests a change to it,"** and that is the finding.

⚑ **AND THE STALE PIN POINTS AT A DOCUMENT THAT CONTRADICTS THE PREREG THAT PINS IT.** The pinned revision still carries the **dead** refusal rule live (*"T-A must report refusals per salt; nonzero ⇒ UNGRADEABLE"*) at all four sites; the prereg's own change-row 9 rules that rule dead, and `b87e282c` struck it. **A builder who obeyed the pin would have implemented refusal under `ORACLE`, `TA-X-25(a)` would be RED, and every band would have been measured on a board 216–273 bodies per arm lighter than the one the widths came from.** drax built against the **current** P-e and that is why `TA-X-25` is green. **The pin discipline would have produced the wrong build; the builder's judgement produced the right one, and the record should say so.**

**Disposition: reported, not repaired.** Nothing in the two post-pin commits moves a row I graded — the V25 prohibitions, the four population cardinalities, the honest-fail counts (338 / 342) and the composition expectations (0.6172 / 0.3828) are byte-identical across the three revisions; the only V25 delta is the **addition** of `V25-P5a`'s per-config split (21 → 22 rows), which is the strike itself. **So the grade below does not move, and I did not HALT for it.** ⚑ **Whether a false pin annotation inside an immutable document is a HALT is the conductor's call, not mine — I have given the derivation so it can be made without repeating the work.**

---

## § 1 · **THE VERDICT**

```
STRUCTURAL @ coverage 89/89, 6/6 counted band rows graded
```

**Antecedent (§ G, first hit on the ordered walk `STRUCTURAL → INDETERMINATE → STATISTICAL → PASS`):**

> **`STRUCTURAL` — ≥ 1 EXACT row RED.** **Two EXACT rows are RED**, independently:
> * **`TA-X-06`** (distinctness D) — `port(W1, s) ≡ port(M-POL-2, s)` on **5 of 5 salts**. The relation the row asserts is **absent**.
> * **`TA-X-07`** (seven-term conservation) — **11 of 25 cells** carry `|residual| > 1e-6` read as **ABSOLUTE**, which is the reading the text's own citation chain establishes (§ 5).

**Consequences as written:** port is wrong; **no W4 until repaired**; the **T-B quoting cap TRIPS** (on `C2`, and independently on `C1` per § 0.1); the two-attempts counter increments to **1**.

⚑ **The mixed-outcome rule applied, explicitly.** Four of six COUNTED BAND rows are also RED. **This does not raise or lower the verdict**: *"A BAND row can never outrank an EXACT row in either direction."* Had every EXACT row been green, those four reds would have made the verdict `STATISTICAL` — a finding, handoff proceeding, cap intact. They do not get to do that here, and they also do not get to be hidden behind the structural red: **they are the larger fidelity story and § 4 reports them at full weight.**

⚑ **Three EXACT rows are UNGRADEABLE on this emission** (`TA-X-01`, `TA-X-15`, and half of `TA-X-16`). UNGRADEABLE is **orthogonal** per § G and would have produced `INDETERMINATE` on its own. It is subordinate here only because `STRUCTURAL` is hit first on the ordered walk. **It is not a smaller problem for being outranked** — § 3.2.

⚑ **No conforming `kc2play.ta_verdict.v1` file exists.** drax's emission is a **manifest** and says so on its face (`⚑ RAW_AND_UNGRADED`) — correctly, by the seats' own division. **This document is the grade; the verdict file is still owed**, and it cannot be assembled from the manifest alone because the manifest carries none of the seven P-pins (§ 0 derives them so that it can be).

---

## § 2 · PRECONDITIONS

| id | requirement | emitted | verdict |
|---|---|---|---|
| **`P-1`** | 89 ids mapped mechanically, counts sum to 89, **zero unmapped** | `mapped 89 / total 89 / unmapped 0 / closes true`; **IMPLEMENTED 65 · DIVERGENCE 8 · RUNTIME-CHOICE 13 · OUT-OF-SCOPE 3 = 89** | ⚑ **GREEN** |
| **`P-2`** | `M-POL-2` salt 0 twice, second with a no-op fold drawing zero values; identical digests | `digest_plain == digest_with_noop_fold == bc3f2db3…`, `identical: true`, `noop_fold_draws: 0` | **GREEN** |
| **`P-3`** | `roll_population` + `roll_law` declared and diffed at boot | `POOL-466`, cardinality asserted **466**, law `{alternative: WEIGHTED:pool_weight, name: UNIFORM:randrange}` | **GREEN** (self-reported; `TA-X-25(c)` is the behavioural check and it is also green) |

⚑ **Three conditions raised against `P-1`, none of which changes its green:**

1. **`P-1` gates COMPLETENESS, not TRUTH**, and at least one mapping is false. Census row **`M4`** is mapped `IMPLEMENTED` with the note *"V11-RELEASE-1: p01–p04 all at t=0.0; p05 one burst at t=4.000 s; no drip"* — and **there is no such implementation.** `sim/kc2rt_fight.gd:507-511` takes `board.roll_wave(w)` and appends **every** returned body at wave start; no `4.0`-second offset exists anywhere in `sim/`. The row the prereg grades as `TA-X-15` is mapped implemented and is not. **This is a finding about the coverage map, not a reclassification of `P-1`.**
2. The runtime's own `⚑ gate_shape_finding`, which I second: *"the four dispositions have NO CELL for 'the pack cannot supply this'."* Three rows (`M17` + two) are carried as `RUNTIME-CHOICE(absent_ref)` with the registered choice `REFUSED` and **counted as `refusals: 3`** so the mapping cannot hide them. **That is the right handling of a gate shape that has no cell for the case** — and it is a gap in the prereg's gate, reported forward.
3. `loader/kc2rt_coverage.gd:69` still holds a constant **named** `CHARTER_DENOMINATOR`, now `:= 89`. The *value* is right; **`OQ-3`'s point was that the name asserts the charter as authority for a number the census enumerates**, and the rename is still owed.

---

## § 3 · THE **EXACT** ROWS — 24

Legend: **GREEN** / **RED** / **UNGRADEABLE** (no value emitted) / **GREEN-BY-CONSTRUCTION** (the mechanism makes the other value impossible; § F.1's own class test).

### 3.1 · The table

| id | statistic | observed | verdict |
|---|---|---|---|
| `TA-X-01` | port self-determinism — any arm/salt run twice → identical digest | ⚑ **no probe exists.** `P-2` runs `M-POL-2` s0 twice *with a fold inserted*; the harness concedes it. No `TA-X-01` key in any artifact | ⚑ **UNGRADEABLE** |
| `TA-X-02` | coverage 89/89, zero unmapped | `89/89`, `unmapped 0`, `closes true` | **GREEN** |
| `TA-X-03` | inertness A — `M-POL-2-NULL ≡ M0`, all 5 | identical **5/5** | **GREEN** |
| `TA-X-04` | inertness B — `W1-NULL ≡ M-POL-2`, all 5 ⚑ *not M0* | identical **5/5** | **GREEN** |
| `TA-X-05` | distinctness C — `M-POL-2 ≢ M0`, ≥ 1 salt | distinct **5/5** (`n_identical 0`) | **GREEN** |
| ⚑ `TA-X-06` | distinctness D — `W1 ≢ M-POL-2`, ≥ 1 salt | ⚑ **identical 5/5** (`n_identical 5`) | ⚑ **RED** — § 6 |
| ⚑ `TA-X-07` | conservation, **7 named quantities / 6 sink terms** | 7 named, 6 sinks present, 0 missing. ⚑ **11 of 25 cells `|resid| > 1e-6`** (max `1.699e-6`); all 25 `|rel| ≤ 1.6e-14` | ⚑ **RED (absolute) / GREEN (relative)** — § 5 rules it **ABSOLUTE ⇒ RED** |
| `TA-X-08` | denominator identity, both sub-identities | `n_ticks_observed = D + PRE_FIGHT` **25/25**; `n_chan + n_released = D` **25/25**; `uptime + released/D = 1.000000` **25/25** | **GREEN** |
| `TA-X-09` | all **9** `math_rules.test_vectors` | `9/9 REPLAYED`, `green true`, `in_prereg_nine true` on each | **GREEN** ⚑ *(condition: of the **29** vectors the runtime replays, **7 fail against the STORED DIGITS** — 2-dp storage and float-representation — while **0 fail against the LAW**. All seven are outside the nine. Reported, not graded.)* |
| `TA-X-10` | containment supremum `max_body_radius_m ≤ 43.758085029822276` (W1) | W1 per salt `[41.680359, 40.175148, 41.770790, 41.570423, 43.176945]` — **max 43.176945**, margin **0.581 m** | **GREEN** |
| ⚑ `TA-X-11` | wall-clamp zeros, every W1 arm | `n_wall_clamps_player = n_wall_clamps_body = 0`, **5/5**, wall `armed: true`, `r_wall_m 43.7580850298223` | **GREEN** ⚑ *(carried caveat, restated because a green here invites over-reading: **"the port never needed to clamp," NOT "the port's wall works." A port with no wall at all also scores zero.** The oracle's own counters are structural zeros — margin 0.807 %.)* |
| `TA-X-12` | pool inertness under ORACLE — total pool damage `== 0.0` | `0.0` on **25/25**; aprons `armed: false` | **GREEN** ⚑ *(and the cell names the trap itself: under `ORACLE` the aprons are **ABSENT, not present-at-zero** — a zero satisfied because the pilot never entered would be a structural zero wearing a measurement's badge. `DIV-19` is ablated separately under `PLAY`.)* |
| `TA-X-13` | no player crit | `0` on **25/25**; `CritLimb.LO (x1.0)` of record | **GREEN** |
| `TA-X-14` | the two DO-NOTs | `cause == "energy"` → **0** on 25/25 (counted, so the zero is assertable); no release-on-every-cast — releases are event-scheduled, `n_release_events` 10–24 against thousands of casts | **GREEN** |
| ⚑ `TA-X-15` | release schedule — p01–p04 at `t=0.0`, p05 **one burst at `t=4.000 s`**, no intra-point stagger | ⚑ **no value emitted.** Source: every body of a wave is appended at wave start (`kc2rt_fight.gd:507-511`); no `4.0 s` offset exists in `sim/` | ⚑ **UNGRADEABLE** — and the source evidence points RED. ⚑ **I do not convert it: I did not measure the schedule, and a red I inferred is not a red I graded.** |
| ⚑ `TA-X-16` | **p06 OFF** | value **`false`** in `v0_limb_set`, ⚑ precedence **`MODULE-DEFAULT`**, not `DRIVER-OF-RECORD`; ⚑ and `grep` finds **one** consumer — the required-key list. The limb is declared and **never read**; the board rolls **every** `<wave>|<point>` key the pack carries, including **spawn_point 6 in 7 of the 10 waves** | ⚑ **GREEN ON THE DECLARED VALUE · UNGRADEABLE ON ENFORCEMENT.** Whether "spawn point p06" and "p06 bonus spawns" name the same object is adjudicated nowhere. ⚑ *Direction note: if they ARE the same, the port is spawning bodies it should not — and the port is **under** the analytic body count, not over (§ 8, H3), so this cannot be the body-count shortfall's cause.* |
| `TA-X-17` | spawn offset `‖spawn_xy − anchor_xy‖ ≤ 8.0` m, every body | ⚑ **no per-body statistic emitted.** Law is `rho = extents · u₂`, `extents = 8.0`, `u₂ ∈ [0,1)` ⇒ **violation is impossible**; `TA-X-18` green confirms the polar law is the one in play | **GREEN-BY-CONSTRUCTION** ⚑ *(named mechanism, § F.1's class test satisfied. The prereg asked for "every body, arm, salt"; the emission carries no such aggregate — a report-face gap, not a red.)* |
| `TA-X-18` | scatter three-law discriminator, `u₁=u₂=0.5` → `(−4.0, 0.0)` | `polar_of_record [-4.0, 4.9e-16]` vs expected `[-4.0, 0.0]`; `uniform_in_area [-5.656854, …]`; `box_retired [0.0, 0.0]`; pairwise separation `> 1e-6`; **green** | **GREEN** |
| ⚑ `TA-X-19` | arrival unconditionality — no damage predicate reads an arrival's `px, py` | ⚑ **the port has no arrival limb at all.** `Kc2RtLaws.arrival_tick` has **zero call sites**; monster→player damage is applied **inline at the cast tick** (`kc2rt_fight.gd:946-1000`); no body carries a `px`/`py` field | ⚑ **GREEN-VACUOUSLY.** The negative is satisfied because the positive does not exist. ⚑ **This is `TA-X-11`'s caveat in a second row and it must be read the same way** — and the absent deferred-arrival limb is itself a fidelity matter the oracle has and the port does not (it also means `TA-X-21`'s `CEIL` assertion is asserted in a vector table and **never exercised**). |
| `TA-X-20` | hit-test 2.99 m hit / 3.01 m miss; no angular gate; no target cap | `failures 0`, `green true`; 3.0 m **behind** → HIT (no angular gate); 12 bodies inside → **12** hits (no cap) | **GREEN** ⚑ *(clears the **resolved predicate** only; `R2D-5` still owns the DRAWN radius, so a green T-A does not clear `V17` — `OQ-6`'s split, adopted.)* |
| `TA-X-21` | quantisation rule per site + **zero bare `round(`** on the port's threat path | vector table **12 rows, 0 failures**: `8.5→8`, `10.5→10`, `2.5→2` (GDScript would give 9/11/3), 7 negative controls, `CEIL` and `TRUNCATE` rows asserted. Purity scan **27 files / 9,599 lines / 0 violations**. Independent scan: **exactly one** bare `round(` in executable code, at `sim/kc2rt_quant.gd:138`, inside the vector table's own *"what GDScript would give"* display — **zero on the threat/cadence/arrival path** | **GREEN** ⚑ *(condition: the purity scan's exemption is **file-level**, so a future bare `round(` anywhere in `kc2rt_quant.gd` would go unreported despite the comment claiming the allowance is expression-scoped.)* |
| `TA-X-22` | flag-off release cause under ORACLE — `cause == "interrupts_channel_flag"` **0** | `0` on **25/25** | **GREEN** |
| ~~`TA-X-23`~~ | ~~board-roll composition~~ | struck at v1.2, id retired | — |
| `TA-X-24` | attack-phase model is `ENGAGE`; `sha256(actor_id) mod n` never evaluated | positive: `phi` one-shot on first reach (`kc2rt_fight.gd:858-883`), `"phi": -1` at init, limb `PhaseModel.ENGAGE` **DRIVER-OF-RECORD**. negative: the only `sha256` uses in the runtime are register/pack/cell digests — **no hash of any actor id** | **GREEN** ⚑ *(the negative has no mechanical assertion — no purity rule, no vector row, no artifact key. It is verified by search, which is weaker than `TA-X-21`'s scanned negative.)* |
| ⚑ `TA-X-25` | the NO-DATA path, three clauses | **(a)** `n_nodata_refused == 0` on **25/25** ✓ · **(b)** both counters present and emitted per arm per salt; `Σ n_measured_inert_spawn` per arm = **30 / 34 / 30 / 34 / 34**, all `> 0` ✓ · **(c)** `Σ n_nodata_spawn_inert` per arm = **273 / 216 / 273 / 216 / 216**, all `> 0` ✓ | ⚑ **GREEN on all three clauses** |

### 3.2 · ⚑ The three UNGRADEABLE EXACT rows, and why being outranked does not shrink them

`TA-X-01` · `TA-X-15` · `TA-X-16`(enforcement half). **On their own they are the `INDETERMINATE` antecedent** — *"0 EXACT red, ≥ 1 EXACT UNGRADEABLE"* — and `INDETERMINATE` trips the cap and **does not** increment the two-attempts counter. Because `TA-X-06` and `TA-X-07` are red, the walk stops at `STRUCTURAL` first and the counter **does** increment.

⚑ **The consequence a grader must not let pass silently: a repair pass that fixes only `TA-X-06` and `TA-X-07` would not reach `PASS`. It would reach `INDETERMINATE`** — and `INDETERMINATE` trips the cap just as hard. **All five must be closed**, and the three ungradeable ones need *emission*, not *repair*:

| row | what closing it needs |
|---|---|
| `TA-X-01` | a genuine repeat probe — **any arm, any salt, run twice with nothing inserted**, byte-exact. `P-2`'s two-leg probe is not this and the harness says so. Cheapest of the five. |
| `TA-X-15` | either an implementation of the p05 `t = 4.000 s` burst **and** a statistic that prints the realised schedule, or a conductor ruling that census `M4`'s `IMPLEMENTED` mapping is wrong. **Not gradeable either way until something is emitted.** |
| `TA-X-16` | one line adjudicating whether `spawn_point 6` is the same object as `p06_bonus_spawns`, and — if it is — a filter plus a counter. |

---

## § 4 · THE **BAND** ROWS — 15 ids

**Graded arm: `M-POL-2`** — the arm the sealed widths were derived from. **Statistic: MEAN-OF-SALTS**, never pooled (§ C.2 / P-a § 3). **Every band prints `value @ coverage 89/89`** — the **rule** coverage of `P-1`, *not* a population coverage (§ C.5).

### 4.1 · COUNTED — **6 graded, 4 RED**

| id | statistic | **port mean-of-salts** | per-salt 5-vector | **governing band (P-a)** | verdict | deviation |
|---|---|---:|---|---|---|---|
| `TA-B-09` | **channel split** | **0.460383** @ 89/89 | `.456539 .453042 .449773 .473144 .469415` | **[0.105100, 0.125689]** | ⚑ **RED** | **+0.334694 = +32.5 half-widths** |
| `TA-B-03` | `frac_moving` on `D` | **0.538389** @ 89/89 | `.542259 .548044 .549511 .524139 .527991` | **[0.8331, 0.8818]** | ⚑ **RED** | **−0.294711 = −12.1 half-widths** |
| `TA-B-06` | plant ratio (5.0 s) | **0.469537** @ 89/89 | `.481928 .480519 .462500 .435897 .486842` | **[1.0052, 1.5646]** | ⚑ **RED** | −0.535663 = −1.9 half-widths |
| `TA-B-05` | `P(chan\|stationary)` | **0.973018** @ 89/89 | `.969802 .966604 .984170 .975298 .969217` | **[0.5868, 0.8448]** | ⚑ **RED** | +0.128218 = +1.0 half-widths |
| `TA-B-02` | uptime on `D` | **0.975570** @ 89/89 | `.972354 .964286 .985738 .980898 .974573` | **[0.7840, 1.0]** *(clipped above)* | **GREEN** | in band |
| `TA-B-04` | `P(chan\|moving)` | **0.977850** @ 89/89 | `.974508 .962374 .987023 .985983 .979361` | **[0.8120, 1.0]** *(clipped above)* | **GREEN** | in band |

⚑ **`TA-B-02` is green BECAUSE OF THE CLIP, and the report says so rather than letting it read as a pass.** The **unclipped** upper bound is **0.974330**; the port's **0.975570 exceeds it by +0.001240**. The governing band in P-a is the **clipped** one — *"clipped above at 1.0 ⇒ [0.7840, 1.0]"* — and P-a's own § 4 power table already classes `TA-B-02` and `TA-B-04` as *"weak — both clip at 1.0 — a one-sided band is half a test."* **I grade the band as written: GREEN.** ⚑ **But the honest statement is that the strongest one-sided reading of uptime is also a miss, and the clip is what carries it.** No width was adjusted to produce that sentence and none may be adjusted to erase it.

⚑ **The two catastrophic reds are both MOTION rows, and they are the run's real fidelity story.** `TA-B-09` at **+32.5 half-widths** is the single largest miss anywhere in this grade — and `TA-B-09` is the row P-a's Addendum 2 registered as *"the most discriminating BAND row T-A has,"* displacing `TA-B-03`. **The tightest instrument in the set is the one most violently missed.** The state partition is the mechanism:

| | `CHANNELLING` | `CH_AND_MOVING` | `MOVING` | `IDLE` | split | frac_moving |
|---|---:|---:|---:|---:|---:|---:|
| **oracle** (pooled seal) | 287 (10.3 %) | 2211 (79.4 %) | 166 | 119 | **0.1154** | **0.854** |
| **port** (`M-POL-2` s0) | **2248 (44.4 %)** | **2676 (52.8 %)** | 70 | 70 | **0.4565** | **0.542** |

**The oracle's pilot channels while moving four-fifths of the fight; the port's pilot stands still for nearly half of it.** That is one divergence expressing itself through `TA-B-09`, `TA-B-03`, `TA-B-05` and `TA-B-06` — **four reds, one cause**, and the cause is the pilot's motion, not the channel policy.

### 4.2 · REPORTED-NOT-COUNTED — 5

| id | statistic | observed | note |
|---|---|---|---|
| `TA-B-01` | terminal wave | **160.00** @ 89/89; 5-vec `[160,160,160,160,160]`; band `[151, 157.75]` ⇒ **OUTSIDE** | ⚑ **Required sentence, printed: `BAND / NON-DECISIVE / REPORT-ONLY` — this band admits every arm in the seal, including the `M-POL` G5 control the run built to be different. A terminal wave inside or outside it is not evidence of fidelity either way.** The finding that matters is not the number but the **reason**, and that is § 7. |
| `TA-B-07` | release duty on `D` | **0.024430** @ 89/89; band `[0.0, 0.215952]` ⇒ **in band** | ⚑ `released/D ≡ 1 − uptime` **exactly** (P-a Addendum 1). **`TA-B-07` and `TA-B-02` are one row with a sign flip and must not be counted as two pieces of evidence.** In band only because the band is clipped **below** at 0. |
| `TA-B-08` | ordering `P(chan\|moving) > P(chan\|stationary)` | mean-of-salts: `0.977850 > 0.973018` — **holds, margin 0.004832** | ⚑ **Per salt it holds 4/5 and INVERTS on salt 1** (`0.962374 < 0.966604`). The row survives at the graded grain and fails at the salt grain; both are printed because the prereg does not say which grain the ordering is asserted on. |
| `TA-B-14` | `n_avoidance_vetoes`, `n_pool_occupancy_ticks` | port W1: **0 and 0** on 5/5 | ⚑ **Oracle `[W1W]`: `W1` = 2 and 0 · `W1-NULL` = 0 and 0 · `W1-PROBE` = 0 and 2.** This row is **the whole of § 6** — it is the counter that carries `TA-X-06`'s entire mechanism, and it is the one the prereg declined to band. |
| `TA-B-15` | NO-DATA spawn count and fraction, per arm per salt | § 4.4 | reference points labelled as what they are |

### 4.3 · UNGRADEABLE-DECLARED — 4, all confirmed, none rescued

| id | statistic | re-verified this session |
|---|---|---|
| `TA-B-10` | per-wave durations | ⚑ **The port DOES emit them** (`per_wave_durations`, 10 rows/salt, with `ticks`, `bodies`, `coverage`, `pool_picks`). **There is still no oracle side** — the sealed per-salt cells carry `terminal_wave` / `terminal_reason` / `n_waves` and no per-wave `duration_s`. **Declaration stands. Emitted ≠ gradeable**, and I will not manufacture a width for a statistic the oracle never published. |
| `TA-B-11` | arrival latency / co-arrival / `n_deferred` | absent from both seals. ⚑ **And now absent from the port too** — no arrival limb exists (`TA-X-19`). |
| `TA-B-12` | intake by wave and family; **leech per tick** | ⚑ **Re-swept both seals by key this session: `leech`, `intake`, `damage_total` return ZERO matching keys.** The port emits all three richly (14 damage families, 10 waves, a 5,064-entry leech trace). **Declaration stands — and § 8 H4 is why this is now the most expensive ceiling in the run.** |
| `TA-B-13` | `max_body_radius_m` (W1) | an extreme not a mean; sample degenerate; its own t-band rejects the oracle's maximum. Its falsifying power sits entirely in `TA-X-10`/`TA-X-11`, both green. |

### 4.4 · ⚑ `TA-B-15` — NO-DATA, per arm per salt, with **pool picks** beside every count (§ F.5 cl. 3)

| arm | salt 0 | salt 1 | salt 2 | salt 3 | salt 4 | **ARM Σ** |
|---|---|---|---|---|---|---|
| **`M0`** / `M-POL-2-NULL` | 64/132 = .4848 | 58/133 = .4361 | 49/138 = .3551 | 49/137 = .3577 | 53/134 = .3955 | **273 / 674 = .4050** |
| **`M-POL-2`** / `W1` / `W1-NULL` | 45/133 = .3383 | 54/151 = .3576 | 34/136 = .2500 | 39/136 = .2868 | 44/136 = .3235 | **216 / 692 = .3121** |

**Pool picks behind every one of those salts: 54.** `measured_inert` per arm: **30 / 34**. `refused`: **0**, every arm, every salt.

**The two reference points, labelled as what they are (§ F.3's box):**
* **analytic expectation over ten waves = `0.3828`** — ⚑ **the expectation**;
* **sealed-cell single-salt five-wave observation = `0.1134`** — ⚑ **one sample of it, not a parameter.**

⚑ **Zero is the anomaly and there is none:** the minimum salt is 34, the minimum arm sum 216. `TA-X-25(c)` is green at the arm level and would have been green at the salt level too — **but the prereg declined the tighter row on a reasoned mechanism argument and I note that declining it was correct: 34 is comfortable, not safe, and a single thin salt could have reached zero.**

### 4.5 · ⚑ PER-WAVE ROWS — each with **its own coverage AND its pool-pick count** (§ F.5 cl. 2 + 3)

`M-POL-2` arm, mean of 5 salts. ⚑ **These are BODY-population figures and they divide by BODIES, not by `D` and not by the T-B windows** (§ C.5's third denominator class — never pooled with the `@ 89/89` above).

| wave | port bodies | `E[bodies]` | ratio | **port coverage** | analytic frac | **pool picks** | port duration_s |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 151 | 18.6 | 26.50 | 0.702 | **0.9027** | 0.8642 | **5** | 37.22 |
| 152 | 10.6 | 17.75 | 0.597 | **0.6018** | 0.5493 | **6** | 30.96 |
| 153 | 16.8 | 23.50 | 0.715 | **0.5809** | 0.5920 | **6** | 36.64 |
| 154 | 9.6 | 12.00 | 0.800 | **0.8533** | 0.8712 | **4** | 36.83 |
| 155 | 13.8 | 18.33 | 0.753 | ⚑ **0.2541** | 0.4182 | **5** | 36.64 |
| 156 | 18.6 | 17.87 | 1.041 | **0.8786** | 0.6401 | **6** | 42.32 |
| 157 | 13.6 | 20.38 | 0.667 | ⚑ **0.3931** | ⚑ 0.2999 | **6** | 46.24 |
| 158 | 26.8 | 33.00 | 0.812 | **0.8513** | 0.7065 | **6** | 28.60 |
| 159 | 5.0 | 9.25 | 0.541 | **0.6800** | 0.5135 | **5** | 40.95 |
| 160 | 5.0 | 5.00 | 1.000 | **0.5200** | 0.6000 | **5** | 57.40 |
| **POOLED** | **138.4** | **183.58** | ⚑ **0.754** | **0.6879** | **0.6172** | **54** | 393.8 |

⚑ **Why cl. 3 earns its place here, concretely:** wave **159** carries a coverage of `0.6800` over **5 bodies and 5 picks**; wave **158** carries `0.8513` over **26.8 bodies and 6 picks**. **Read as body counts these look like claims of very different strength; read as pool picks they are 5 against 6.** The body count overstates 158's evidence by the design effect and understates how little separates them. *A wave at 0.30 over 4 picks and a wave at 0.30 over 20 picks are not the same claim* — and here almost every wave is 4–6 picks, so **no per-wave figure in this table rests on more than six independent draws.**

⚑ **Wave-label completeness (§ F.5 cl. 4):** the port's per-wave rows sum to `D` exactly (`Σ ticks = 5064 = D` on salt 0) and no `wave = -1` / UNLABELLED bucket appears. **The one-frame gap galadriel found is a footage artifact and has no sim-side analogue** — stated rather than left as an unexplained absence.

---

## § 5 · ⚑ `TA-X-07` — **ABSOLUTE OR RELATIVE? IT IS DETERMINABLE FROM THE TEXT, AND IT IS ABSOLUTE**

**The question:** eleven cells carry `|residual| ≈ 1.07–1.70e-6` on an `offered` near `1.0e8` — i.e. `~1.0–1.6e-14` **relative**. The prereg's tolerance cell reads **`1e-6`** and does not say which.

**The answer: ABSOLUTE — established by the citation chain, not by preference.**

1. Prereg § F.2 carries the bare figure `1e-6` and cites nothing of its own for it. Its concordance table (§ D) routes `TA-X-07` to **gamora § 2.4 · `E-2`**.
2. **P-a § E-2** — the governing text — writes the identity and then, in the same code block's caption: *"`residual → 0` **(module tolerance 1e-6)**."* ⚑ **"Module tolerance" is a citation, not an adjective.** It names an instrument in the engine.
3. **The instrument, read this session at `simulation/scripts/gamora_kc2_pm4_i16_measured_board_2026_08_14.py:1059`:**

```python
abs(cons["residual"]) <= 1e-6 and cons["⚑ counterplay_absorbed_total"] > 0.0)
```

⚑ **`abs(residual) <= 1e-6`. Absolute, with no reference to `offered`.** The `1e-6` in the prereg is that comparison's right-hand side, transcribed twice and never re-typed as a relative bound. **The prereg meant ABSOLUTE, and the text can decide it.**

**Therefore `TA-X-07` is RED on 11 of 25 cells:**

| arm family | cells over `1e-6` | worst |
|---|---|---|
| `M0` / `M-POL-2-NULL` | salt **4** (×2 arms) | `−1.698732e-6` |
| `M-POL-2` / `W1` / `W1-NULL` | salts **0, 1, 4** (×3 arms) | `−1.490116e-6` |
| **total** | ⚑ **11 distinct cells of 25** | |

⚑ **Correction to the count the commission carried:** the manifest raises **13 rows**, but **two are duplicates of `M-POL-2 salt 0`** — the distinct count is **11**, and I derived it independently from the cells before reading the raised list. *(The duplicate entries are an emission defect in `⚑ conditions_raised_to_the_grader`, not a grading matter.)*

⚑ **A ruling I will not make and the conductor should, because it is a prereg question and not a measurement:** `1.7e-6` on `1.0e8` is **float64 accumulation over ~10⁵ additions**, not created or destroyed damage. **The row's stated purpose — *"a non-zero residual means damage is being created or destroyed, which is not a fidelity difference, it is a broken port"* (P-a § E-2) — is not what an absolute `1e-6` measures at this magnitude.** ⚑ **The tolerance is doing a different job than the sentence that justifies it.** But the prereg is immutable, a graded run now exists, and *no post-hoc widening, by anyone* (A-3; L-88). **So it grades RED and the widening question goes to Matt, where a width change after a graded run belongs.** ⚑ **This is mine: I wrote "module tolerance 1e-6" into a width file without asking whether an instrument sized for a per-fight residual was the right instrument for a ten-wave one.**

---

## § 6 · ⚑ `TA-X-06` — THE CLASSIFICATION QUESTION. **THE ROW WAS MIS-CLASSED AT AUTHORING, AND THE EVIDENCE WAS ALREADY PINNED WHEN IT WAS**

**The measurement:** `port(W1, s) ≡ port(M-POL-2, s)` byte-identically on **5 of 5 salts** — not just on the digest but on every statistic in the cell: `D`, all six census rows, the board census, the conservation residual, the leech total. In the port, **`W1`, `W1-NULL` and `M-POL-2` are one arm wearing three names.**

**drax's diagnosis, which I have tested and confirm:** `ArenaFold(armed=True, avoidance=True)` carries **two limbs**. He implemented the **wall** (`CIRCLE`, `R_wall = 43.758085029822276`, response `STOP` never slide) and it **never binds** — port `max_body_radius_m` tops out at `43.176945`, clamps `0/0`, the structural zero `TA-X-11` predicts. He declared `ABS-ARENA-AVOIDANCE-MECHANISM` for the second limb rather than invent a veto rule.

### ⚑ 6.1 · The oracle's own seal proves the wall was never the mechanism

Read this session from `[W1W]` (`7a992c81…`), `⚑ pools / per_arm` — **and already printed in P-a Addendum 2 § A2, pinned as `P-a`, before prereg v1.0 was written:**

| arm | `avoidance` | clamps player | clamps body | ⚑ `n_avoidance_vetoes` | ⚑ `n_pool_occupancy_ticks` |
|---|---|---:|---:|---:|---:|
| `W1` | True | **0** | **0** | ⚑ **2** | 0 |
| `W1-NULL` | True | **0** | **0** | **0** | 0 |
| `W1-PROBE` | **False** | **0** | **0** | **0** | ⚑ **2** |

**Three facts fall straight out, and the third is new:**

1. ⚑ **The wall contributes NOTHING to the oracle's `W1`-vs-`M-POL-2` distinction. Its clamp counters are zero on every arm.** The only counter that separates `W1` from `W1-NULL` is **`n_avoidance_vetoes`, 2 against 0.**
2. ⚑ **So `TA-X-06`'s distinctness, in the oracle, is carried ENTIRELY by the avoidance limb** — the limb with no published trigger rule, on a boundary `ABS-ARENA-BOUNDARY` declares absent, in a cell of record `V8-CELL-1` says ran **wall-less**.
3. ⚑ **New, and it sharpens what the limb DOES without supplying the rule:** `W1` shows **2 vetoes / 0 occupancy**; `W1-PROBE`, the same configuration with `avoidance = False`, shows **0 vetoes / 2 occupancy**. ⚑ **An exact complementary pair.** The avoidance limb **vetoes entry into the pool region**; without it the same two ticks are spent occupying it. **That tells us the limb's EFFECT. It does not tell us its TRIGGER** — the geometry and threshold that decide *when* a veto fires are nowhere in the pack, and without them the effect cannot be reproduced.

### 6.2 · ⚑ My read: **YES, MIS-CLASSED — and precisely how**

**Not because the relation is false.** `W1 ≠ M-POL-2` is a true fact about the oracle.

**The mis-class is this:** `TA-X-06` was classed **EXACT** while, in the same document, **the only mechanism that makes its relation true was classed `TA-B-14` — REPORTED-NOT-COUNTED, "oracle values 0–2", no width, no trigger rule, nothing owed.** ⚑ **An EXACT row was built on an input the same prereg declared unspecifiable.** That is not a judgement call that went the wrong way; it is two rows in one file that cannot both be right.

**And the information needed to catch it was on the record before v1.0 existed.** P-a Addendum 2 § A2 — the file the prereg pins as `P-a` — prints the `2`-vs-`0` avoidance vetoes **in the same table as the `0/0` clamps**, and its own carried caveat says *"a port with no wall at all also scores zero."* ⚑ **The prereg quotes that caveat at § E (`TA-X-11`) and does not apply it to `TA-X-06`, one row above.** The caveat and the row it invalidates sit seven lines apart.

⚑ **The consequence, stated plainly: `TA-X-06` is unfalsifiable in the honest direction.** A port that implements the fully-specified wall and refuses to invent the unspecified limb **cannot** pass it. The only route to green is to invent a veto rule — **and then the row is green about a rule nobody wrote.** A row that can only be passed by invention is not an EXACT row; it is a trap for the conscientious builder.

**⚑ drax's call was correct and the record should say so.** He declared the absence, routed it, named the consequence in the code comment *and* in the emitted absence ledger *and* in the relation row's own `why`, and did not fill it. Given a choice between a true red and a green about a fiction he chose the true red. ⚑ **That is exactly the behaviour the run wants, and a conservative call that goes unremarked is the mooted-escalation defect one level down.**

**⚑ I am not reclassifying it.** The prereg is immutable and a graded run now exists; changing it is a HALT to Matt and **that call is the conductor's, not mine.** The grade above stands as written: **`TA-X-06` RED ⇒ `STRUCTURAL`.** This section is the evidence, not the remedy.

⚑ **One thing a re-class must NOT do, flagged now so it is not discovered later:** striking `TA-X-06` does **not** make this run `PASS`. `TA-X-07` is independently red, and `TA-X-01`/`TA-X-15` are independently UNGRADEABLE. **The verdict survives the removal of the row most likely to be challenged**, and that is worth knowing before anyone spends effort challenging it.

---

## § 7 · ⚑ THE CONDUCTOR'S TWO READS

### 7.1 · READ 1 — `terminal_reason` on all 25 cells. ⚑ **`cleared`. NOT `player_death`. On every one.**

| arm | terminal wave 5-vec | `terminal_reason` | `killer_id` | `n_live_bodies` | HP minimum across the 5 salts |
|---|---|---|---|---:|---|
| `M0` | `[160,160,160,160,160]` | **`cleared` ×5** | `""` ×5 | 0 ×5 | 84.61 % – 94.07 % |
| `M-POL-2` | `[160,160,160,160,160]` | **`cleared` ×5** | `""` ×5 | 0 ×5 | **79.44 %** – 91.36 % |
| `M-POL-2-NULL` | `[160,160,160,160,160]` | **`cleared` ×5** | `""` ×5 | 0 ×5 | 84.61 % – 94.07 % |
| `W1` | `[160,160,160,160,160]` | **`cleared` ×5** | `""` ×5 | 0 ×5 | 79.44 % – 91.36 % |
| `W1-NULL` | `[160,160,160,160,160]` | **`cleared` ×5** | `""` ×5 | 0 ×5 | 79.44 % – 91.36 % |

**Against the oracle's own four sealed arms: `player_death` on 20 of 20 cells**, at waves `151–156`.

⚑ **The ambiguity the conductor named is RESOLVED, and it resolves to the worse branch.** The port did not die on wave 160 as the referent did. **It ran out of content, with every body dead, no killer, and a player who never fell below 79.4 % of maximum HP on any of the 25 runs.** The lowest HP the player reached in **413 seconds of the hardest content in the pack** is a 20.6 % dip.

⚑ **This also retires any reading of `TA-B-01` as a near-miss.** `[160 × 5]` is not "four waves past the band"; it is **the ladder running out**. Had the pack carried waves 161–170 the terminal vector would be some other number, and the statistic would still be measuring the same thing: **the port is not in a fight.**

### 7.2 · READ 2 — ⚑ **UNDONE WORK, NOT ABSENT DATA. 338 of 338, proven.**

**The question:** do the 338 NO-DATA records carry offense in the game's substrate that our decode never took, or does the game genuinely give them none?

**The test, and it needed neither the video nor the referent.** POOL-466 was rebuilt from the pack by a **third independent route** (the 109 pools referenced by `wave_spawn` rows at `global_wave ∈ [151,160]`, then their `pool_member` sets) — **cardinality 466, agreeing with both prior routes** — and the 338 identified as the members absent from `pm2_tg2_attack_damage.csv`. Then each of the six pinned source CSVs was asked which of those records it contains:

| source CSV | distinct records | **∩ the 338 NO-DATA** | **∩ POOL-466** |
|---|---:|---:|---:|
| `pm2_tg2_attack_damage.csv` (damage) | 237 | **0** | 128 |
| `pm2_tg2_monster_timing.csv` (ANCHOR-169) | 169 | **0** | 128 |
| `pm2_tg2_attack_slots.csv` (slots) | 164 | **0** | 124 |
| `pm4r_speed_terms.csv` (run speed) | 184 | **0** | 128 |
| ⚑ **`pm4l_mitigation_by_body.csv`** (armour + resist) | **937** | ⚑ **338 — 100.0 %** | ⚑ **466 — 100.0 %** |

⚑ **Every single one of the 338 is present in the mitigation extraction.** Not 90 %. Not 337. **338 of 338.** The same upstream, the same `record_path` keys, the same pipeline — **reached all 466 for one dimension and 128 for the other.**

**That is decisive on the class of the finding:**

* **The records exist, resolve, and carry per-body data.** A record that yielded a full armour-and-resist board is not a record the substrate lacks.
* **The offense passes stop at a scope boundary, not at a data boundary.** Damage, slots, timing and speed all terminate at the *same* ~128-record intersection; mitigation does not. **A boundary that four passes share and a fifth does not is a decision about what was extracted, not a property of what exists.**
* ⚑ **And the offense decode measures its own shortfall INSIDE the set it did cover.** Across the 169 timing records: **169 of 169 declare `num_attack_slots > 0`** — *not one covered monster is slotless* — and the totals are **996 slots declared against 667 decoded (67.0 %), with 136 of 169 records decoding fewer slots than they declare.** ⚑ **The extraction already knows it is one-third short on the records it did visit. There is no basis for believing the 338 it never visited are the only slotless creatures in the game.**
* **Family mix:** the 338 are **260 champion + 78 normal**; the covered 128 are **86 normal + 42 champion**. ⚑ **The gap falls hardest on champions** — the bodies that hit hardest.

⚑ **VERDICT ON READ 2: Matt's testimony is CORROBORATED by the substrate's own files. `ABS-MONSTER-OFFENSE-NO-DATA-POOL466` is an honest-fail we can no longer stand behind as a declaration of absence.** It is **a decode lap we owe.** The right remedy is **lifting more offense, not registering more absence** — and the work is scoped, not speculative: it is the same extraction, run to the same record set the mitigation pass already reached.

⚑ **What this does to the class of the divergence (carried per the conductor, and it makes things worse):** a NO-DATA body is **not** "a monster that did not attack." It is **a monster whose attacks we failed to lift.** So the substrate carries a **systematic bias with a known sign — the model is easier than the game** — and the port inherits it. ⚑ **"The port faces more harmless monsters" is therefore an indictment of the substrate and NEVER an exoneration of the port**, which is exactly how § 8 H2 grades it.

⚑ **One boundary on my own answer, because I will not overclaim it:** I proved the 338 are **reachable and carry data**, and that the offense passes share a scope boundary the mitigation pass does not. **I did not read the game's own `.dbr`/`.arz` files — none are on this host** — so I have not shown *per record* that each of the 338 carries attack rows upstream. ⚑ **Given `169/169` coverage-declares-slots and a `67 %` decode rate inside the covered set, the burden has moved: absence is now the claim that needs evidence.** Confirming it per record needs the game files, which is **legolas's seat, not mine** — and it is one read, not a project.

---

## § 8 · THE FOUR HYPOTHESES — **TESTED**, each labelled

### ⚑ H1 — *"Release duty is the single term that could move all three deltas at once."*
### **MECHANISM CONFIRMED — AND THE HYPOTHESIS REFUTED. Both halves are load-bearing.**

**CONFIRMED, exactly and with the mechanism named: the port fires ZERO Type-A releases.**

Release census by type, all 25 cells: `causes = {type_b: N}`, `types = {B: N}`, `closed_by = {type_b_lockout_elapsed: N}`. ⚑ **Type A does not appear once.** `M-POL-2` events per salt: `20, 24, 10, 13, 17`; released ticks `140, 168, 70, 91, 119` = **exactly 7 ticks per event**, matching `⚑ typeB_duration_ticks = 7`.

**Against `⚑ acceptance`'s own populations, read from `[M-POL2]`'s `⚑ declared_constants`:**

| | `REF_TYPEA_N` | `REF_TYPEB_N` | `REF_N_RELEASES` | `REF_TYPEA_TIME_S` | `REF_TYPEB_TIME_S` |
|---|---:|---:|---:|---:|---:|
| **the referent** | **11** | 8 | 19 | **14.4 s (75.2 %)** | 4.75 s (24.8 %) |

**And in the oracle's own realised fold, per salt:**

| salt | `D` | released | ⚑ **typeA** | typeB | **A share** | `n_typeA_scheduled` → `fired` |
|---:|---:|---:|---:|---:|---:|---|
| 0 | 1084 | 104 | **96** | 8 | **92.3 %** | 6 → 6 |
| 1 | 305 | 32 | **32** | 0 | **100 %** | 2 → 2 |
| 2 | 106 | 23 | **16** | 7 | 69.6 % | 1 → 1 |
| 3 | 185 | 16 | **16** | 0 | **100 %** | 1 → 1 |
| 4 | 1103 | 110 | **96** | 14 | 87.3 % | 6 → 6 |
| **Σ** | | **285** | ⚑ **256** | 29 | ⚑ **89.8 %** | |

⚑ **`n_typeA_scheduled` equals the number of wave transitions in each salt exactly** (terminals `156,152,151,151,156` ⇒ `6,2,1,1,6`). **Type A is one release per wave transition — precisely the conductor's framing — and the port fires none of them.** The port implements the Type-B limb faithfully (event rate ≈ `λ_B = 0.0435/s`, duration exactly 7 ticks) and the dominant limb not at all.

**REFUTED as "the single term that moves all three deltas," on four independent grounds:**

1. ⚑ **It is not three deltas. It is one.** `released/D ≡ 1 − uptime` **exactly** — my own Addendum 1 identity, and the port reproduces it (`uptime + release_duty = 1.000000` on 25/25). `TA-B-02` and `TA-B-07` are **one row with a sign flip**. Release duty moving uptime is not a second symptom; it is the same number read backwards.
2. ⚑ **The magnitude does not survive contact with the arithmetic — and most of the 9× gap is NOT a port defect.** A faithful Type-A would add `10 transitions × 16 ticks = 160` released ticks, giving duty `≈ 0.059` and uptime `≈ 0.941`. **Still far above the oracle's 0.879, still inside the clipped band.** ⚑ **The oracle's duty of 0.121 is high because its fights were SHORT** — `D` of 106–1103 ticks with 1–6 transitions, so a 16-tick Type-A burst is a large share of a tiny fight. The port's `D` is ~4,800 ticks with 10 transitions. **`TA-B-07` and `TA-B-02` are confounded with fight length and are not scale-free** — a port that survives longer scores a lower Type-A duty *with a perfect Type-A limb*. ⚑ **That confound is a defect in my width file, not in the port: I banded a duty without asking whether its numerator scales with waves while its denominator scales with ticks.**
3. ⚑ **It cannot touch the four motion reds.** Released ticks are **140 of 5,064** and land in `MOVING`/`IDLE`. The reds live in the split *within* the channelling population — `2248` stationary against `2676` moving. Restoring Type-A adds ~160 ticks to the non-channelling side and **leaves 44.4 %-vs-10.3 % exactly where it is.** `TA-B-09`'s **+32.5 half-widths** are untouched.
4. ⚑ **It cannot touch survival.** Leech exceeds intake by **73–177×** (H4). A 3.5 % swing in channel time is not visible against that.

**Net: a real, exactly localised port defect worth fixing — and the smallest of the four findings, not the unifying one.**

### ⚑ H2 — *"The port faces more harmless monsters than the oracle's one sealed cell happened to roll."*
### **CONFIRMED ON THE MEASUREMENT — REFUTED AS AN EXPLANATION OF SURVIVAL — AND RECLASSED BY § 7.2 FROM VARIANCE TO BIAS.**

**Computed on the same denominator, per arm:**

| | NO-DATA share | vs analytic `0.3828` | vs sealed sample `0.1134` |
|---|---:|---|---|
| **port `M0` family** | **0.4050** (273/674) | **+0.022 above** | far above |
| **port `M-POL-2` family** | **0.3121** (216/692) | −0.071 below | far above |
| **analytic expectation** | **0.3828** | — | — |
| **oracle sealed cell** | **0.1134** (11/97) | ⚑ **−0.269 below** | — |

⚑ **The conductor's framing is confirmed exactly: the port sits mid-to-high bracket, astride the analytic point estimate; the oracle's one sealed cell sits at the FAVOURABLE EXTREME.** Its `0.8866` coverage against an expectation of `0.6595` is an ordinary draw at `z = 2.30` on the corrected cluster-based σ (P-e Addendum 2) — **an ordinary draw at the lucky end.** Between a quarter and two-fifths of the port's board cannot attack, and **that is the honest consequence of rolling POOL-466 as `L-49` rules.** The port is not wrong to see it.

**But it is REFUTED as the cause of clearing ten waves, and the refutation is not close:**
* Lifting the port to the oracle's own favourable `0.8866` coverage would raise armed bodies by `0.8866/0.6879 ≈ 1.29×`.
* Total intake would rise from ~55 k to ~71 k against a leech total of **7.3 M**.
* ⚑ **The player would still never drop below ~73 % HP.** Composition cannot carry this finding; it is off by two orders of magnitude.
* ⚑ **And the decisive control is the oracle itself: it ran the same POOL-466 exposure, saw the same class of gap, and killed the player 20 times out of 20.**

⚑ **RECLASSED per § 7.2.** With 338 of 338 proven present in the mitigation extraction, the NO-DATA class is **not a property of the fight** — it is a hole in our decode. So the divergence is **real, ours, and of known sign: the model is easier than the game, and the port is easier still.** ⚑ **H2 is therefore an indictment of the substrate. It is not, at any point, an exoneration of the port.**

### ⚑ H3 — *"Total body count — name the grain."*
### **GRAIN NAMED — and the fork's unstated branch is the one that is true.**

⚑ **`216–273 NO-DATA per arm is the SUM OVER THAT ARM'S FIVE SALTS.** Per salt it is **34–64**, in-bracket. That is the conductor's first branch: the port is **not** spawning far more bodies than the oracle.

⚑ **But naming the grain surfaces a finding neither branch of the fork anticipated: the port spawns materially FEWER bodies than the analytic, not more.**

| | per salt, waves 151–160 |
|---|---:|
| analytic `E[bodies]` at the config of record | **183.58** |
| analytic under ceiling `C-c`'s `limitN` cap (−11.500) | **172.08** |
| ⚑ **port `M-POL-2` family, measured** | ⚑ **138.4** |
| ⚑ **port `M0` family, measured** | ⚑ **134.8** |

**The port is at 75.4 % of the uncapped expectation and 80.4 % of the capped one — short by ~34–45 bodies per salt.** It is below expectation on **9 of 10 waves** (§ 4.5), on both arms, on all five salts.

⚑ **And the shortfall is in bodies per pick, not in picks.** Pool picks are **54 per salt, identically, on all 25 cells** — 5.4 per wave against the sealed cell's 4.6. **`bodies/pick` is 2.50–2.56 for the port against `97/23 = 4.22` for the sealed cell.** The port makes slightly *more* picks and gets **~40 % fewer bodies out of each one.** That points at `count_bounds` handling or the champion limb — **exactly Trap 6, which the prereg declares outside T-A's reach**, and exactly what `TA-X-25`'s own box warns it cannot see: *"a port rolling POOL-466 with wrong `pool_weight`s, wrong `count_bounds`, or a weighted name draw passes all three clauses."* ⚑ **Here is a live instance of that blind spot, found by arithmetic against the analytic rather than by any T-A row.**

⚑ **Caveat named, per the prereg's own cross-arm rule:** the `97 / 23 / 11` figures are from the sealed **`[MECH]`** cell — **a different arm** — and cross-arm comparison measures a configuration difference. **The analytic `183.58` does not have that problem**: it is computed at the config of record, at `p06_bonus_spawns = false` per `V0-36`, over exactly 151–160. **The 25 % shortfall rests on the analytic, not on the cross-arm figure.**

### ⚑ H4 — *"Sustain — check leech-per-tick and regen against `V15-10`'s identity."*
### ⚑ **THE INSTRUMENT IS MISMATCHED — `V15-10` IS AN ENERGY IDENTITY, NOT A LEECH ONE — AND THE SUSTAIN DIVERGENCE IS THE RUN'S LARGEST FACT AND IS OUTSIDE T-A ENTIRELY.**

**1 · `V15-10` does not govern what the hypothesis asks it to.** Read from the v3.2 lifted rows (`e0117429…`):

```
V15-10  key: energy.tip_the_scales
        value: {leech_total: 200.0, leech_duration_s: 2.0, cooldown_s: 1.0, ⚑ stacking: "NON-STACKING"}
        note: ⚑ STACKING FLIPS NET SUSTAIN FROM -1.03/s TO +98.97/s
```

⚑ **`energy.tip_the_scales` is an ENERGY-pool identity** — `drain 176.4 − regen 75.37 − tts 100.0 = −1.03/s`. **It says nothing about life leech per tick.** ⚑ **This is § C.5's hazard in a fourth costume: two quantities sharing the word "leech," on two different pools, and a hypothesis routed to the wrong one.**

**2 · Graded on its own terms, `V15-10` is GREEN and drax's regen repair is correct.** The runtime derives `tip_the_scales_per_s = 200.0/2.0 = 100.0`, computes `net_sustain_per_s`, and **refuses to boot if it moves from `−1.03` by more than `0.005`** — the identity is enforced, not assumed. Regen is applied **every tick unconditionally**, and the first draft's not-channelling gate (which made every arm terminate at wave 151 by `dry_out` with an identical `D` of 110) is removed and documented. ⚑ **His diagnosis was right and the repair is sound. The residual is not regen, and `V15-10` does not discriminate here**: at `−1.03/s` against a `1594` ceiling the pool empties in ~1,548 s, and the fight is 413 s — **so would `+98.97/s`. Neither limb dries out inside this fight, so "no dry-out" proves nothing either way.**

**3 · The actual sustain finding, which no prereg row reaches:**

| | value |
|---|---|
| total intake per cell | **41.6 k – 98.0 k** |
| total leech per cell | **7.12 M – 7.79 M** |
| ⚑ **leech ÷ intake** | ⚑ **73× – 177×** |
| leech ÷ damage offered | ~6.9 % (consistent across all 25 cells) |
| HP minimum, all 25 cells | ⚑ **never below 79.44 %** |
| HP at terminal, all 25 cells | **20005.0 = max** |

**Life leech is `V1-LAW-10` — `pool × (adcth_pct/100) × heal_increase`, with overkill pro-rated — and `V1-LAW-13`, the per-tick cap, is MEASURED-ABSENT and asserted zero.** ⚑ **So leech scales without ceiling against a ~105 M damage output, and the player is unkillable by construction, not by luck.**

**4 · ⚑ T-A CANNOT GRADE ANY OF IT.** `leech`, `intake` and `damage_total` return **zero matching keys** on both seals — re-swept by key this session, confirming P-a Addendum 1 § A3. **That is precisely why `TA-B-12` is `UNGRADEABLE-DECLARED`.** The port emits all three richly; there is nothing to compare them to.

⚑ **The conclusion, and it reorders the run's priorities: the sustain surplus is the dominant cause of the survival divergence, it is not testable against `V15-10`, and it is invisible to every row T-A has.** The ceiling P-a declared as a modest gap turns out to sit over the largest divergence in the emission. **The three hypotheses T-A can see explain a few per cent each; the one it cannot see explains the rest.**

---

## § 9 · DECLARED CEILINGS — restated, as the prereg requires, with what this run did to each

| # | ceiling | status after this run |
|---|---|---|
| **C-a** | **The refusal discriminator is structurally dead under `ORACLE`.** `TA-X-25(a)`'s `0` is an identity, not a discriminator | ⚑ **HOLDS, and the port confirms it: `refused = 0` on 25/25, exactly as construction requires.** The run traded a per-salt discriminator for a per-arm one-bit presence test; **the trade was correct and the report does not print it as though the discriminator survived.** Only the `PLAY`-side probe can settle it |
| **C-b** | **The ten-wave composition expectation has NO empirical check** — the sealed census covers 151–155; the fight scope is 151–160 | ⚑ **HOLDS AND IS NOW LOAD-BEARING.** Waves 156–160 carry **50.9 % of the port's bodies** and the whole of H2's comparison. **No cell has ever validated that half**, and K-7 forbids making one. **Carried, not closed** |
| **C-c** | **The `limitN` residual** — `−11.500` bodies over 151–160, expected coverage-fraction-invariant | ⚑ **NOW MEASURABLE AND STILL UNSETTLED.** The port is **34–45 bodies short per salt** — **3–4× the cap's predicted effect** — so the cap cannot account for it. A measured pass over the capped config would separate them |
| **C-d** | **Honest-fail row (b) `342` does not decompose against (a) `338` + 6 measured-inert** | ⚑ **OPEN. `OQ-4` asks me to state (b)'s grain in one line and I have not; it is owed and it is one line.** ⚑ *I confirm the grain disagreement is real: `v20_monster_attack_slot` resolves **688** distinct rows on `(record_path, kind, slot, damage_type)` against **678** on the published key — 10 rows silently collide, including a 15.0 m attack against a 3.0 m one on the same record.* |
| **trap 6** | **THE BOARD ROLL** — 12 of 29 live draw sites; divergence shows as a different SET of monsters | ⚑ **OPEN, AND IT JUST COST THE RUN A FINDING.** `TA-X-25(c)` proved **membership** and the composition defect walked straight through it: **`bodies/pick` 2.50 against 4.22** (H3) was found by arithmetic against the analytic, **not by any T-A row.** Closure is still a sibling emitting per-wave class counts |
| **`TA-X-11`** | the clamp zeros are **structural**; *a port with no wall at all also scores zero* | ⚑ **HOLDS — and § 6 shows it applies to `TA-X-06` too, where it was not carried.** ⚑ **And `TA-X-19` is now a second instance of the same shape**, satisfied because the port has no arrival limb at all |
| **S5 / 29 sites** | a stream divergence is **visible and not locatable** | **HOLDS.** 34 sites declared / **29 live** / 5,856 draws on `M-POL-2` s0, and no sealed cell to place them against |
| **`TA-B-12`** | intake / damage family / leech have **no oracle side** | ⚑ **HOLDS, and it is now the most expensive ceiling in the run — § 8 H4.** |
| ⚑ **NEW** | ⚑ **`TA-B-07` / `TA-B-02` are confounded with fight length** — a Type-A-per-wave numerator over a per-tick denominator | ⚑ **MINE.** Declared here, after the fact, which is the wrong order and is said so plainly |
| ⚑ **NEW** | ⚑ **`TA-B-06`'s window construction was never specified** — § 10 | ⚑ **MINE** |
| ⚑ **NEW** | ⚑ **`ABS-MONSTER-OFFENSE-NO-DATA-POOL466` is not a declared absence — it is undone decode work (§ 7.2)** | ⚑ **Reclassification owed at the substrate, not here** |

---

## § 10 · ⚑ CONDITIONS RAISED — including two defects that are mine

1. ⚑ **`TA-B-06`'s WINDOW IS TWO DIFFERENT CONSTRUCTIONS UNDER ONE NAME, AND THE UNDER-SPECIFICATION IS MINE.** Read from the seal: `n_window = 61 × n_waves` exactly on all five salts (`366/6`, `122/2`, `61/1`, `61/1`, `366/6`) — ⚑ **ONE 5.0-second window PER WAVE.** The port: `n_windows = D / 61` (83, 77, 80, 78, 76) — ⚑ **the WHOLE RUN tiled into 5.0-second windows.** **P-a § 2.4 says only `"plant ratio (window 5.0 s)"` and Addendum 1 says only `"(window 5.0 s / fight-wide)"`. Neither says one window per wave.** ⚑ **The port implemented a defensible reading of an under-specified construction, and the band it fails was written by me without enough of a definition to bind it.** **I grade the row as written — RED at −1.9 half-widths — and record that its red does not localise what it appears to.** *This is § 3 of my own width file, in my own band row, for the third time in this seam.*
2. **`TA-X-07`'s tolerance does the wrong job for the sentence that justifies it** — § 5. Widening is forbidden post-hoc; the question goes to Matt.
3. **`TA-X-06`'s classification** — § 6. Evidence supplied; the call is the conductor's.
4. **P-e's pin does not reproduce, and its annotation is false** — § 0.1. `C1` tripped.
5. **Census row `M4` is mapped `IMPLEMENTED` and has no implementation** — § 2, `TA-X-15`.
6. **`TA-X-16` has a declared value and no enforcement**, at `MODULE-DEFAULT` precedence, with `spawn_point 6` rolled in 7 of 10 waves and the identity question unadjudicated.
7. **`⚑ conditions_raised_to_the_grader` contains two duplicate rows** — 13 entries, 11 distinct cells.
8. **`TA-B-08` inverts on salt 1** while holding at the graded grain; the prereg does not say which grain it is asserted on.
9. **The purity scan's `round(` exemption is file-level, not expression-level.**
10. **Of the 29 vectors the runtime replays, 7 fail against the stored digits and 0 against the law** — all outside the prereg's nine.
11. ⚑ **No conforming `kc2play.ta_verdict.v1` exists** and it cannot be built from the manifest, which carries none of the seven P-pins. **§ 0 derives them so it can be.**

---

## § 11 · WHAT I JUDGE THE RUN SHOULD DO NEXT

**Ordered by what each buys, not by effort.**

1. ⚑ **Rule `TA-X-06`, and rule it at the level it actually sits.** The evidence in § 6 says the row cannot be passed without invention. **The decision is Matt's** (immutability + a graded run exists). ⚑ **Whatever is decided, the verdict does not move** — `TA-X-07`, `TA-X-01` and `TA-X-15` are independently sufficient. **So rule it for the record's sake, not to change the outcome.**
2. ⚑ **Take the decode lap (§ 7.2). This is the highest-value item in the run and it is not a T-A item.** 338 of 338 proven present in the mitigation extraction; 169/169 covered records declare attack slots; 67 % of declared slots decoded. **Route the per-record upstream confirmation to legolas** (it needs the game files, which are not on this host) **and then lift the offense.** ⚑ **Every band in this grade was measured against a board we now know is systematically softer than the game.** Regrading against a fuller decode is worth more than any repair below it.
3. ⚑ **Emit the oracle-side sustain statistics, or accept that T-A cannot see the largest divergence it has.** `leech` and `intake` are absent from both seals; a sibling that emits them is the only thing that converts § 8 H4 from an observation into a gradeable row. **Until then a green T-A is compatible with an unkillable player, and that must be said on the report's face.**
4. **Close the three UNGRADEABLE EXACT rows before the next graded run** (§ 3.2) — `TA-X-01` is cheap and unambiguous; `TA-X-15` needs a ruling as much as an implementation. ⚑ **A repair pass that fixes only the two reds lands on `INDETERMINATE`, which trips the cap just as hard.**
5. **Fix the Type-A release limb** (§ 8 H1) — a real, exactly localised defect. ⚑ **But do not expect it to move the bands: it buys ~3.5 pp of uptime and nothing else.** Fix it because it is wrong, not because it will change a verdict.
6. **Chase `bodies/pick` 2.50 vs 4.22** (§ 8 H3) — `count_bounds` or the champion limb. ⚑ **This is trap 6 and no T-A row will ever catch it; it needs the sibling that emits per-wave class counts.**
7. ⚑ **Before any T-A v1.5, fix the two width defects that are mine** — `TA-B-06`'s window construction, and `TA-B-07`/`TA-B-02`'s fight-length confound. ⚑ **Both are cases where a band was pinned without its construction being specified tightly enough to bind a second implementation. That is the same defect twice and it belongs in the disciplines, not just in a corrigendum.**
8. **Carry `OQ-1` / `OQ-3` / `OQ-4`** — the charter's superseded sizing, the `CHARTER_DENOMINATOR` rename, and (b)'s grain, which is mine and is one line.

---

*Graded 2026-09-21 by gamora (simulation seam), Run KC2-PLAY Wave 3. **Prereg v1.4 graded as written: no width adjusted, no row reclassified, no band rescued, no post-hoc widening.** All seven P-pins and all three sealed-cell digests **derived this session by `shasum -a 256`, never retyped** — and one of the seven did not reproduce, which is § 0.1. **K-7 held**: sealed cells hash-verified, opened READ-ONLY by key, never re-run, never re-graded. **No simulation executed. No production code touched. No push.** Where the prereg could not decide, it is reported.*
