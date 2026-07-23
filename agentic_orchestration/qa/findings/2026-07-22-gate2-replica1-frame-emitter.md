# Finding — 2026-07-22 — REPLICA-1 G2 frame emitter

**Reviewer:** jack-ryan (DEV-MODE, Gate-2, BLOCK authority)
**Severity:** PASS (no WARN, no BLOCK — two INFO notes for the record)
**Target:** engine commit `1564e2fc74902114d83c97ded40e4d6b01052611` (`1564e2f`)
**Developer:** gamora (simulation seam)
**Conductor:** gandalf `RUN-CONDUCTOR` (REPLICA-1 run; charter RL-3)
**Principles applied:** Review Principles #1 (math/design-before-code), #2 (smoke-gate), #3 (cross-seam impact), #4 (decisions/spec as truth), #5 (severity); Engineering Disciplines #1, #2, #3, #11, #12; charter G2 governing claim.

## Verdict — PASS

The governing claim — **observability-only, zero combat-logic change, default-off path byte-identical** — holds under line review, static guard-scan, determinism scan, and a green test suite at the commit. The emitter lands as an idiomatic default-off observability seam matching the engine's existing `telemetry_writer` / `_trace_decisions` / `emit_telegraphs` convention. No cross-seam touch, no telemetry-schema change. Cleared to tag/push at conductor+Matt discretion.

## What I found

I line-reviewed the full `spatial_engine.py` diff (+98), the new `replica_frame_emitter.py` (362 lines), and the design note, then independently re-ran the test sweep and two static proofs at `1564e2f`. Every added line in `spatial_engine.py` is a sink-closure, a `frame_sink is not None` None-guard, a pure read of state the loop already holds, or a comment — I found NOT ONE line that mutates entity state (`.hp/.x/.y/.is_alive/.energy` or any accumulator), draws from any RNG stream (`_rng`/`_resolver_rng`/`_resolver_rng_dmgvar`), or alters control flow on the `frame_sink=None` path. A grep of all 14 `_frame_sink` references confirms each is either the ctor assignment (:2439), the `_frame_on_hit` factory body (:3539, which returns `None` when the sink is `None` so the 5 `_apply_skill_damage` call sites pass `on_hit=None` and their per-target loops skip the invocation), or a site explicitly guarded by `if self._frame_sink is not None:`. There is no unguarded sink access on any code path, so the default path is provably inert by construction. The nondeterminism scan of the emitter returned NONE (no `time`/`datetime`/`uuid`/`monotonic`/`random`/`perf_counter`); `engine_git_hash` is passed in by the driver rather than read at emit time; the non-finite guard `_finite()` raises `ValueError` (fail-loud) on NaN/Inf per spec §6. I reproduced gamora's test attestation: the spatial/fight/resolver/combat/aura/economy sweep = **210 passed, 0 failed** at `1564e2f`, and every spatial-keyed selection I ran is green. gamora's own inertness proof (`frame_sink=None` bit-equal to the sealed ablation cell, intake `10334.753710727`, |Δ|<1e-9) is corroborated structurally by the guard-scan: a side-effect-free reader on a fully-guarded None path cannot shift the fight.

## Line-review detail (the load-bearing check)

- **`_apply_skill_damage` resolver loop (:2306-2311)** and **flat loop (:2336-2340):** the `on_hit` invocation is placed AFTER all mutation (`target.hp -= dmg`, the `is_alive` flip, `_on_kill_energy_burst`), guarded `if on_hit is not None:`. Reads only in-scope locals (`attacker`, `target`, `dmg`/`_tdmg`, `_delivered_this_hit`, `_resolver_skill.canonical_element` via getattr, `target.hp`, `target.is_alive`, `skill_idx`, `geometry_type` [the function's positional param :2214]). No NameError risk when the sink fires; fully skipped when it does not. CLEAN.
- **`_frame_on_hit` factory (:3534-3549):** returns `None` when `self._frame_sink is None` → the callers receive `on_hit=None`. Closure is a pure read that maps `(attacker,target,dmg,...)` to a `damage` frame event. CLEAN.
- **header (:3586-3587), decision (:4051-4054), telegraph (:4490-4492), deaths_from_diff + tick at loop bottom (:4892-4894), footer (:5165-5168):** all `if self._frame_sink is not None:` guarded, all after their respective mutation, all pure reads. Loop-bottom placement (after all mutation, before `_tick_counter += 1`) is correct per spec §2. CLEAN.
- **DoT capture (:4817-4823, :4845-4850)** — the most scrutinized block: `_dot_frame_el` is read with `self._frame_sink is not None` FIRST in the `and` chain, so Python short-circuits and the None path never touches `combatant_state`. The `max(..., key=...get)` is a pure read that does NOT pop/consume the dict; the element is captured as a string BEFORE the per-element bucket `.clear()` at :4840 (correct ordering — reading after the clear would null the element for every mob). The `dot()` emit at :4845 passes `hp_after=e.hp` after the `-= _dot` subtract and `lethal=(not e.is_alive)` after the flip — both correct. CLEAN. (See INFO-2.)

## Rationale

- **Charter G2 governing claim + Review Principle #4 (spec as truth):** "observability only — ZERO combat-logic change in the same commits" is satisfied — verified line-by-line and by exhaustive guard-scan, not by attestation alone.
- **Review Principle #2 (smoke-gate) + Discipline #2:** the smoke evidence is present and independently reproduced (byte-identical determinism, inertness bit-equal, burst present, tests green). This is exactly the "smoke-test before full-regen" posture; no full regen was needed to prove inertness.
- **Discipline #11 (empirical inspection over assumption) + #12 (semantic-shift framing):** the two spec-letter deviations (fight_key-for-UUID, threat_tier null) are documented in the design note §5/§7 and the slice report, and are already RATIFIED by the conductor in RL-3 — the developer surfaced them rather than burying them. Correct discipline.
- **Review Principle #3 (cross-seam impact):** no telemetry-schema change, no `output/`-path policy in the engine seam (naming lives with the collab driver), no cross-repo touch. The `replica-frame/v1` schema is a collab-owned contract (gandalf), not an engine telemetry schema.

## INFO notes (for the record — non-blocking)

- **INFO-1 — RATIFIED deviations, logged here for the finding trail.** `fight_id` (uuid4) is omitted in favor of the deterministic `fight_key`, and `threat_tier` is honest-null in the header roster. Both are correct calls (a uuid4 in the frame file would break the spec's own §6 byte-identity gate — the load-bearing acceptance criterion) and both are already conductor-ratified (charter RL-3). No action. Note only: if a UUID cross-ref is ever wanted, it must be `uuid5(NAMESPACE, fight_key)`-derived to preserve byte-identity (design note §5 already flags this).
- **INFO-2 — `_dot_frame_el = None` executes unconditionally on the DoT-active path.** At :4819 the `_dot_frame_el = None` initializer runs whenever `_dot > 0.0`, i.e. also on the `frame_sink=None` path, before the `frame_sink is not None` guard at :4820. This is a single dead-store of `None` to a fresh local (never read when the sink is None) — it is NOT combat logic, NOT a state mutation, NOT an RNG touch, and does not affect byte-identity of engine state or the frame file. It is a micro-cost (one name-bind per DoT-active entity-tick) on an already-gated cold path (the ref-set cells carry no DoT, so this block is inert there anyway). Flagged for tidiness only: the initializer could sit inside the guard. No action required; not worth a re-commit on its own.

## Provenance nuance (noted, not a defect)

Frame headers emitted for the ref set record `engine_git_hash=2f43045` because emission preceded the emitter commit (the frames were generated against the bit-equal combat substrate). This is honest as the COMBAT-substrate hash (inertness bit-equal proven), and post-`1564e2f` emissions self-record correctly. Already captured in charter RL-3. No action.

## Mechanism finding (concur)

I concur with gamora's Discipline #11 mechanism finding (ratified in RL-3): the ref-set kit_ids are LABELS on the gate's neutral BC-cells (synthetic martial kits, all `element: null`), so the population carries no elemental DoT and `geometry=dot` events legitimately fire zero times on this content. The DoT channel is unit-proven and dormant, correct code awaiting a DoT-bearing population (new-prereg territory, not an emitter change). This is a faithful reflection of what the ablation gate actually measured — engagement-geometry, not elemental-DoT. Not an emitter defect.

## Action

- [x] Developer (gamora): none required for PASS. INFO-2 tidy-up (move `_dot_frame_el=None` inside the guard) is optional, defer to any future touch of that block — do NOT re-commit solely for it.
- [ ] Matt / conductor (gandalf): none blocking. Engine commit `1564e2f` is Gate-2 CLEARED; push remains at conductor+Matt authorization per commit-never-push (charter RL-3, ADR-006).

## References

- Commit: `1564e2f` — `git -C ~/Games/reincarnated-engine show 1564e2f` (4 files: `replica_frame_emitter.py` new 362L, `spatial_engine.py` +98, design note, AGENT_STATE)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (diff line-reviewed; guard-scan of all 14 `_frame_sink` refs)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/replica_frame_emitter.py` (nondeterminism scan clean; `_finite` fail-loud guard :29-39)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/replica1-frame-emitter-2026-07-22.md` (design note, Discipline #1 before-code)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-22-replica1-frame-schema-spec.md` (`replica-frame/v1` — §5 emission map, §6 determinism)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-22-replica-1-godot-sim-window-run.md` (charter; RL-2 authorized Shape B; RL-3 conductor verification + ratified deviations)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-22-replica1-g2-emitter-slice.md` (developer slice report)
- Test verification at `1564e2f`: `python3 -m pytest tests/ -k "spatial or fight or resolver or combat or aura or economy" -q` → **210 passed, 0 failed** (19.15s); all spatial-keyed selections green.
