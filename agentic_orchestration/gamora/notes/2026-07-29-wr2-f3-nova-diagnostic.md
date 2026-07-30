# WR2-ENCGEO F-WR2-3 — WHY the boss nova goes dark under `body_separation_v2`

**Cell:** WR2-ENCGEO diagnostic (charter §8.19, fired §8.20) · **Agent:** gamora · **Date:** 2026-07-29
**Class:** READ-ONLY diagnostic. **No production code written. No engine-tree change committed.**
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-29-wr2-encgeo-run-charter.md` §8.19
**Predecessor finding:** `agentic_orchestration/gamora/notes/2026-07-29-wr2-cell-c-movement.md` §10
**Engine tree state:** `ecea69f`, tracked-clean BEFORE and AFTER — see §7.

---

## 1 — VERDICT

**(b) — a BUG in the S2S wiring.**

Specifically: **the SS-B-1 surface-to-surface effective range was applied at the shared skill
SELECTOR but not at the nova's own downstream FIRE gate.** The two predicates disagree by exactly
`target.entity_radius`, which opens a **select-but-refuse window** of width 0.5 m (the player's
radius) in which the boss selects the nova, the nova's own gate refuses it, and the shared cooldown
tail **still bills the boss's entire 6.0 s action budget**. The boss's single per-fight nova attempt
is spent inside that window, and it never gets a second one.

The charter's hypothesis — **(a)**, "S2S makes boss MELEE eligible where it was not, starving nova
out of selection" — is **FALSIFIED at the decisive tick**. At the moment the nova is selected, boss
melee has effective range 2.5 m against a target at 10.2086 m: it is not a candidate and does not
compete. The nova is *not* starved by melee. **It is selected, and then refused by its own gate.**
Hypothesis **(c)** is also ruled out: `gd_nova.py` carries no dependency on entity radii or
separation distance anywhere in its cast gate, ring scheduler, or crossing solver (§4).

The BEFORE novas were therefore **NOT an artifact of broken geometry.** They were the mechanic
working. This is a units gap introduced by B, of exactly the class R-WR2-8 was written to prevent —
the same class, one layer downstream of where the ruling was implemented.

---

## 2 — THE PREDICATE THAT FLIPS, QUOTED

Two range predicates govern one skill. SS-B-1 changed the first and not the second.

**(i) The shared selector — CHANGED by SS-B-1.** `_select_skill_for_entity`,
`src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` **:2620-2622** at base `4f09e35`
(**:2641-2643** at HEAD `ecea69f`):

```python
        if body_separation_v2:
            return nearest_dist <= range_m + nearest_target.entity_radius
        return nearest_dist <= range_m
```

The nova skill dict carries `range_m = PRIMORDIAN_FRIGIDRING.fire_range_m = 10.0`
(`kitcal_g5_scenarios.py`, the `row.nova` block). So the selector's effective range for the nova
goes **10.0 → 10.5** when the flag arms.

**(ii) The nova's own fire gate — NOT CHANGED.** `_gd_nova_cast`, same file **:4435** at base
(**:4485** at HEAD):

```python
        if mob.distance_to(target) > p.fire_range_m:
            return False
```

`p.fire_range_m` is `10.0` (`gd_nova.py:199`), read **centre-to-centre**, unconditioned on the flag.

**(iii) The tail that bills the refusal.** The call site at **:5702** (base) / **:5875** (HEAD)
**discards `_gd_nova_cast`'s return value**, and the shared cooldown tail at **:5992** (base) /
**:6165** (HEAD) fires unconditionally after the `elif` chain:

```python
                        mob.skill_cooldowns[skill_idx] = cooldown
                        mob.action_available_at = elapsed + cooldown
```

`cooldown` is the nova's `Delay = 6.0 s`. Note the second line: a refused nova does not merely
re-arm the nova's own cooldown — it sets `action_available_at`, so **the boss takes no action of any
kind for 6.0 s.** (This part is documented spec behaviour — "a REFUSED cast still pays the cooldown,
the AI spent its `Timeout` window", `_gd_nova_cast` docstring. It is correct as written; it is what
converts a 0.5 m units gap into a whole-fight outcome.)

**(iv) Why there is no second attempt.** The boss carries no `skill_rotation_priority`, so selection
falls to `return ready_indices[0]` (base :2665 region). Index 0 is the 2.0 m melee; index 1 is the
nova. Once the boss is in melee contact, `ready_indices[0]` returns **0 forever** and index 1 is
never reached again. Measured: index-1 selected **exactly once per fight, in both arms**.

---

## 3 — THE NUMBERS

One endpoint-leg boss fight (`tier=boss`, `arm=B`, `mitigation_regime=R2_proxy_resists_low`,
`--gd-cadence --with-nova --emit-telegraphs`), base commit `4f09e35`, one flag toggled. Seed
74000802 is the falsifier the charter named; §3.2 replicates across the first six battery seeds.

### 3.1 — Seed 74000802, the decisive ticks

| tick | t (s) | d centre-to-centre (m) | melee eff. range | nova eff. range (selector) | selected | nova gate `d ≤ 10.0` | ring |
|---|---|---|---|---|---|---|---|
| **OFF** 7 | 0.7 | 10.208590523869777 | 2.0 | 10.0 | — | not reached | — |
| **OFF** 8 | 0.8 | **9.231090523869778** | 2.0 | 10.0 | **1 (nova)** | **PASS** | **MINTED** |
| **ON** 7 | 0.7 | **10.208590523869777** | **2.5** | **10.5** | **1 (nova)** | **REFUSE** | **none** |
| **ON** 8+ | — | — | — | — | (boss idle to t=6.8) | — | — |

- ON, tick 7: `10.208590523869777 ≤ 10.5` → **selector admits**. Then
  `10.208590523869777 > 10.0` → **gate refuses**. Surface-to-surface distance at that instant is
  **9.708590523869777 m**, i.e. the nova is *comfortably* inside its declared reach under the very
  measure SS-B-1 adopted — and is refused anyway.
- The 20 % `Chance` branch is **never reached** on the ON arm: the range gate returns before the
  dedicated sub-stream draw. The nova sub-stream is left unconsumed (dedicated, so nothing else
  observes it).
- Boss `action_available_at` after the refusal: `0.7 + 6.0 = 6.7`; next boss action at **t = 6.8**,
  by which time `d = 1.9994` and index-0 melee wins the `ready_indices[0]` pick permanently.
  Boss selections thereafter: **index 0 × 37, index 1 × 0.**
- Fight-level: OFF `elapsed 22.000 s`, `n_nova_crossings 1`. ON `elapsed 61.000 s`,
  `n_nova_crossings 0`. Both `winner = monster`.

### 3.2 — The 0.5 m window swallows the attempt in 6/6 seeds (and why it is 100 %, not ~51 %)

| seed | OFF: d at first nova select / gate / ring | ON: d at first nova select / gate / ring |
|---|---|---|
| 74000800 | 9.2311 @ t=0.8 / PASS / — (lost the 80 % `Chance` draw) | 10.2086 @ t=0.7 / **REFUSE** / — |
| 74000801 | 9.2311 @ t=0.8 / PASS / **minted** | 10.2086 @ t=0.7 / **REFUSE** / — |
| 74000802 | 9.2311 @ t=0.8 / PASS / **minted** | 10.2086 @ t=0.7 / **REFUSE** / — |
| 74000803 | 9.2311 @ t=0.8 / PASS / **minted** | 10.2086 @ t=0.7 / **REFUSE** / — |
| 74000804 | 9.2311 @ t=0.8 / PASS / **minted** | 10.2086 @ t=0.7 / **REFUSE** / — |
| 74000805 | 9.2311 @ t=0.8 / PASS / **minted** | 10.2086 @ t=0.7 / **REFUSE** / — |

**The distance at first selector-eligibility is seed-INVARIANT to every digit printed.** The approach
phase carries no RNG: fixed spawn ring, deterministic closure at **0.9775 m per 0.1 s tick**
(17.0511 → 16.0736 → 15.0961 → … → 10.2086 → 9.2311). Range-gate pass rate: **OFF 6/6, ON 0/6.**

This is the arithmetic that turns a partial defect into a total one, and it should be stated
precisely because the two readings have different scopes:

- **The BUG is general.** The refuse window is `(fire_range_m, fire_range_m + r_target]` = 0.5 m
  wide = **0.5116 tick-steps** at this closing rate. For an arbitrary approach phase, roughly half of
  fights would land in it.
- **The 0/60 darkness is fixture-specific.** Because this fixture's approach phase is deterministic
  and lands at 10.2086 — inside the window — **every** fight of the leg loses its nova. Cell C's
  0/60 is not a coincidence and not a sampling result; it is one arithmetic fact replicated 60 times.

Corroboration on the BEFORE side: OFF minted 5/6 here (83 %), the single miss being the 80 % `Chance`
gate. The WR1 banked 132/180 boss fights = 22/30 distinct seeds = 0.733 at p = 0.8, within 1 σ
(σ = 2.19 on 30 draws — the sub-stream is seed-derived, so the same 30 draws replicate across both
arms and all three legs). **The BEFORE range gate passed 30/30. Nothing about the BEFORE novas was
artifactual.**

---

## 4 — RULING OUT (c)

`gd_nova.py` was read for any dependency on body geometry that B's changed separation could flip.
There is none: `fire_range_m` (`:138`, `:199`) is a scalar creature `mediumRangeMax`; the ring
scheduler and the analytic crossing solver (`radius_at`, `resolve_tick`, `nova_delivered`) resolve
against the **player's point centre** and the ring's own `projectile_distance_m` / `explosion_radius_m`
— never against `entity_radius`, never against a pairwise separation. The `explosion_radius_m` and
`projectile_distance_m` radii are payload footprint, not reach, and no code path conflates them with
the fire gate. **The only predicate whose truth value changes between flag OFF and flag ON is the
selector's range test at :2621.**

---

## 5 — THE ONE-LINE FIX, DESCRIBED (not built)

**Make the nova's own fire gate read the same effective range the selector already used, gated to
the same flag.** At `spatial_engine.py:4435` (base) / `:4485` (HEAD), replace the bare
`p.fire_range_m` comparison with a flag-conditioned effective range:

> `_eff = p.fire_range_m + (target.entity_radius if self._body_separation_v2 else 0.0)`, and gate on
> `mob.distance_to(target) > _eff`.

Flag OFF is byte-identical by construction (the added term is 0.0). The invariant this restores is
the one the defect violates: **the selector's range predicate for skill *i* must be the same
predicate skill *i*'s own cast gate applies.** It is consistent with R-WR2-8 (surface-to-surface) and
with R-WR2-12 (one law everywhere); it is a completion of SS-B-1, not an extension of it. `_bsep`
is a conductor-ruled flag and spec §E marks every B row NO, so **the ruling is the conductor's to
make, not mine** — routed with its falsifier.

**Falsifier for the fix, already run** (monkey-patch in the scratch tree, `/tmp/wr2f3/probe_fix.py`;
no engine file touched). Flag ON + fix, same six seeds: range gate **6/6 PASS** at
`eff_fire_range 10.5` vs `d 10.2086`, `n_nova_crossings` **5/6** — the identical 5/6 pattern as the
OFF arm, with the identical seed (74000800) losing the identical 80 % `Chance` draw. The mechanic is
restored, deterministically.

**Two consequences the conductor should price in, because the fix is not a revert:**

1. **It does not reproduce the BEFORE numbers.** The nova now fires one tick EARLIER, at
   d = 10.2086 instead of 9.2311. The crossing radius changes, and the payload model has REVERSE
   falloff (further hurts more, `gd_nova.py:117`), so the delivered damage moves. S-6 line item.
2. **It moves damage-side outcomes materially.** Seed 74000802: `elapsed` 61.0 s (ON, broken) →
   26.4 s (ON, fixed) vs 22.0 s (OFF). The nova is not cosmetic; its absence was doing a large part
   of the ON arm's fight-lengthening. This is exactly the class R-WR2-8 was flagged to Matt for, and
   it lands adjacent to **F-WR2-2** (the `pre_endpoint` win rate reaching 0.000): on these six seeds
   the fix did **not** restore a win — 74000800 won under OFF with **zero** crossings, so F-WR2-2
   has a component this fix does not reach. **The two findings are not the same finding, and closing
   F-WR2-3 will not close F-WR2-2.**

---

## 6 — TWO ADJACENT OBSERVATIONS, LEDGERED NOT FIXED

Both are pre-existing (present with the flag OFF) and outside F-WR2-3's question. Reported because
they bear on the intent sentence's "worth watching", which is what made F-WR2-3 a finding.

1. **The boss casts its signature exactly ONCE per fight, in every arm.** Measured: index-1 selected
   1× per fight OFF and 1× per fight ON. Mechanism is `return ready_indices[0]` with melee at index
   0 — once the boss is in contact, the nova is unreachable in selection for the rest of the fight,
   regardless of its cooldown. The WR1 BEFORE battery's "132 novas across 180 boss fights" is
   therefore **≤ 1 per fight by construction**, not a rate. A watcher sees one ring at t≈1.55 s and
   never again. If the AFTER watch reads flat, this — not the units gap — is the larger suspect, and
   it is a boss-AI question (`ready_indices[0]`), which the bounded-substrate law keeps out of WR2.
2. **A refused cast idles the boss entirely for 6.0 s** (`action_available_at`, not just
   `skill_cooldowns[idx]`). Spec-documented and defensible for a `Timeout` reading, but it means any
   future select-but-refuse defect on a long-`Delay` skill costs the boss its whole action budget,
   not one skill. This is the **second instance** of the select-but-refuse class after jack-ryan's
   Cell-B Gate-2 **INFO-2** (circle-AoE selects at 3.5 m against `aoe_radius` 3.0) — same seam, but
   INFO-2 is a whiff and this one is a refusal that bills the cooldown. Two instances in one cell is
   a pattern, and the pattern is *the selector and the effect layer measuring reach differently*.

---

## 7 — METHOD, ARTIFACTS, AND TREE STATE

**Method.** The base commit `4f09e35` was extracted to a scratch tree with
`git archive 4f09e35 | tar -x -C /tmp/wr2f3/base` — a read-only plumbing read that writes nothing
to `.git` and creates no worktree. All instrumentation is in-process monkey-patch over
`_select_skill_for_entity` and `SpatialFightEngine._gd_nova_cast`, invoking
`kitcal_g5_harness.run_one_fight` directly with the endpoint leg's own parameters. `trace_dir=None`
throughout, so no artifact was written anywhere near `output/`.

**Scratch artifacts (outside every repo; not committed, regenerable):**
`/tmp/wr2f3/probe.py`, `/tmp/wr2f3/probe_multi.py`, `/tmp/wr2f3/probe_fix.py`,
`/tmp/wr2f3/probe_74000802.json`, `/tmp/wr2f3/probe_multi.json`, `/tmp/wr2f3/probe_fix.json`,
`/tmp/wr2f3/base/` (the extracted base tree).

**Engine working-tree state, asserted per the diagnostic's terms.** `git -C ~/Games/reincarnated-engine
status --porcelain --untracked-files=no` returned **EMPTY both BEFORE and AFTER** this diagnostic;
`HEAD` was `ecea69f` at both checks. (`--untracked-files=no` is the correct predicate here: the tree
carries a long-standing population of untracked `output/` regen artifacts and local dotfiles that
predate this session and that no diagnostic step touched. Zero tracked modifications, zero staged
changes, zero new untracked files under `src/`. The parallel jack-ryan Gate-2 on Cell C sees the tree
exactly as it left it.) SS-1 holds: `output/kitcal_g5/wr1_battery_2/` was read for nothing and
written for nothing.

**Committed deliverable:** this note only. Not pushed.

---

*— gamora, WR2-ENCGEO F-WR2-3 diagnostic, read-only*
