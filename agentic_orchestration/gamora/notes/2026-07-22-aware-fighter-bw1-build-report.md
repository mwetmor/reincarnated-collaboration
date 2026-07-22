# Aware-Fighter BW-1 — Build Report (as-built vs charter)

**Author:** gamora (seam owner, `simulation/`), 2026-07-22
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-22-aware-fighter-build-charter.md`
**Math note:** `agentic_orchestration/gamora/notes/2026-07-22-aware-fighter-bw1-math.md`
**Reviewer target:** jack-ryan Gate-2 (this is PRODUCTION ENGINE CODE). **Verdict-consumable + DRIFT-CRITIC-consumable.**
**Discipline:** commit-never-push (both repos); the conductor holds the engine push until Gate-2 PASS.

---

## TL;DR

**Equivalence battery: PASS.** 256/256 fights bit-equal (metric triple + decision trace) between the
legacy nearest-first fighter (worktree @ stamp `a3671d4`) and the refactored BLIND policy seam.
BEFORE-leg cross-check vs the recorded W3′ gate-output: clean (256/256 matched, 0 mismatch → HEAD ≡
stamp on the fight path). **Zero red-flags. Zero RNG-stream-divergence class. No tolerance bands used.**
Unit tests: 32 new (policy seam) + 27 existing spatial = **59 passed**. All six charter deliverables
landed. One HONEST FLAG for prereg: AWARE all-5-candidate cost is 5.47× BLIND (above the ~3-4× target);
a lean gate set is 1.46× (within budget) — the gate set is pinned at prereg, not this wave.

---

## Empirical seam recon — a charter-vs-reality correction (Discipline #11)

The charter cited `spatial_engine.py:1338` as the player target-selection site. **Empirically that
line is the point-geometry AOE hit-resolver, NOT the player's target choice.** The real player
target-choice seam is TWO `min(distance_to)` sites (verified at HEAD `f738d44`):
- **`_get_player_primary_target` fallback (was :1543)** — movement/point-attack target
  (`min(alive_mobs, key=distance_to)`), with a boss-focus override.
- **`_select_skill_for_entity` (was :1915)** — the attack `nearest_target`
  (`min(targets, key=distance_to)`), shared by player AND mobs.

The seam was scoped to the PLAYER at BOTH sites; mob/ally target choice (and the taunt-weighted
variant) stays byte-identical (charter §1.5). HEAD drift check: HEAD `f738d44` is one commit past the
W3′ stamp `a3671d4`; the intervening commit added ONLY a decisions-log entry (no `simulation/` code),
so HEAD ≡ stamp on the fight path — later confirmed empirically by the 256/256 cross-check.

A second empirical correction: `threat_tier` / `archetype_tag` (charter §1.2's substrate) are
**SpawnSpec** fields, NOT runtime `SpatialEntity` attributes. The exposure map reads the RUNTIME
surface that IS present — `max_hp` (tier-encoded threat proxy: swarm/magic=150, elite/boss=2500),
`preferred_behavior`, `aggro_radius_m` — a within-seam read, no entity-construction change (math note
§3.1.1). Behaviorally equivalent on the gate roster; literal `threat_tier` plumbing is out-of-scope.

---

## Section-by-section: as-built vs charter §2 deliverables

### §2.1 Policy seam — DONE
Extracted the player target choice + movement intent into `simulation/spatial_gauntlet/policy/`
(new package): `considerations.py`, `exposure_map.py`, `seam.py`, `__init__.py`. The legacy
hardcoded player `min(distance_to)` is **REPLACED** — no dual code path, no legacy branch behind a
flag (charter §1.4, the ablation property). Threaded via `SpatialFightEngine._policy_config` and
`run_spatial_fight(policy_config=)`; default `None → BLIND → byte-identical` production behavior.
**Skill selection (`_select_player_skill_v2`) untouched** (charter §2.1); no energy-type-branch
entanglement forced a wider refactor — no red-flag needed.

### §2.2 Considerations architecture — DONE
Considerations are DATA: a `PolicyConfig` is an ordered `(name, weight)` list; the decision code
path is fixed, the consideration SET is the swappable surface. **BLIND = {distance}**, scored raw as
`-distance` so `argmax U ≡ argmin distance` EXACTLY (tie-break: both keep first-extremum; IEEE-754
negation is exact → no epsilon, math note §1.4). The map is built lazily — ONLY when a weighted
consideration reads it (`needs_exposure_map`), so BLIND is zero-cost.

### §2.3 Equivalence battery — **PASS** (THE HARD GATE)
Harness: `agentic_orchestration/gamora/notes/2026-07-22-aware-fighter-bw1-equivalence-battery.py`
(the packaged repeatable artifact, §2.5). Sequencing exactly per charter:
- **(a) BEFORE (legacy):** a detached git worktree at stamp `a3671d4` (`/tmp/aware-before-worktree`)
  with a **byte-neutral** decision-trace instrument installed (worktree-only, uncommitted — the
  stamp is not contaminated). Ran the 256 via the legacy `min(distance_to)` path with
  `trace_decisions=True`. **Cross-checked the triples against the recorded W3′ `gate-output.json`:
  256/256 matched, 0 mismatch** → HEAD ≡ stamp, no drift.
- **(b) AFTER (BLIND):** the same 256 via the policy seam in BLIND config (main engine tree).
- **(c) Standard:** bit-equal metric triples (`mobs_killed`/`total_aoe_hits`/`player_damage_total`)
  AND decision-trace equality (`(tick, chosen_target_id, movement_intent)`), NO tolerance bands.

**Result: 256/256 bit-equal. triple_mismatch=0, trace_mismatch=0, key_asymmetry=0,
rng_divergence_class=0. verdict=PASS.** Verdict:
`2026-07-22-aware-fighter-bw1-battery-verdict-full.json`. The 256 = 32 cells × {matched-baseline,
encounter} × 4 seeds {20260722–25}, reproduced by IMPORTING the W3′ runner's
selection→formation→scenario→fight machinery (same cell/seed/composition/parity logic).
`player_gather_primitive` OFF both configs (charter §3). Each leg ran in a subprocess with its own
`sys.path` pinned to the correct engine (BEFORE→worktree, AFTER→main), verified in the verdict JSON
(`engine_before` / `engine_after`). Fights sequential (Discipline #3). Smoke slice (2 pairs × 1 seed)
ran first and PASSed (Discipline #2).

**RNG-stream-divergence class (charter §2.3):** the harness has an explicit detector — a case with
provably-identical decisions (trace equal) but a divergent triple would be reported as its own class
for the conductor to rule on. **It did not fire** (0 occurrences); the seam is a deterministic
argmax over distances and consumes no RNG, so no divergence was expected or observed.

### §2.4 Damage-intake metric — DONE
`SpatialEntity.damage_taken` accumulator (per-fight) + `SpatialFightResult.player_damage_taken`
scalar (no time series). Enemy-inflicted only: the main mob-attack site (`spatial_engine.py` ~:4281)
+ aura/coverage-pressure (~:3772); self-inflicted LC HP costs EXCLUDED (defensive-exposure signal,
not cost-economy — math note §5.1, Discipline #12). Mirror of `player_damage_total`
(`delivered_damage_dealt`). Wired through the batch runner: `run_spatial_fight` already returns the
`SpatialFightResult` list; the field rides that surface (no runner-signature change). **Additive,
default 0.0, brownfield-safe, INTERNAL-to-seam** (the positional `_INSERT_SQL` does not persist it —
same status as `player_damage_total` / `total_displacement`): **no DB migration, no telemetry-schema
change** (charter §2.4/§3). No `MIGRATION.md` needed — nothing downstream (star-lord) consumes a new
persisted column.

### §2.5 Tests — DONE
- Unit: `reincarnated-engine/tests/test_aware_fighter_policy_seam.py` (32 tests — seam, scoring, map,
  intake metric).
- Battery: packaged as the repeatable artifact above (`--smoke` for the slice, no-arg for full 256×2,
  `--leg` for a single leg).

### §2.6 Build report — this document.

---

## The AWARE consideration candidate list (I PROPOSE; prereg PINS — charter §2.2)

Five computable candidate considerations, each a normalized `s ∈ [0,1]` over the exposure/influence
map (runtime `max_hp` threat-proxy + `preferred_behavior` + geometry; math note §3.3). Mapped to the
charter's candidate families:

1. **`exposure_incoming_threat_density`** — Σ θ(m)·K(dist(player,m)) over mobs near the PLAYER
   (kernel K(d)=max(0,1−d/R)); score = lower exposure ⇒ more desirable. *(exposure / incoming-threat density)*
2. **`cluster_density`** — Σ θ(m)·K(dist(c,m)) around the candidate c; higher cluster ⇒ more
   desirable (AOE value). Distinct semantics from `player_gather_primitive` (scores which mob to
   FIGHT, not where to walk — Discipline #12). *(cluster density)*
3. **`crossfire_overlap`** — θ-weighted ranged threat straddling both flanks of the player→c axis;
   lower crossfire ⇒ more desirable. *(crossfire / arc overlap)*
4. **`lane_pressure`** — Σ θ(m) within a lane half-width of the player→c approach segment; clearer
   lane ⇒ more desirable. *(lane / corridor pressure)*
5. **`escape_gradient`** — cosine-alignment of (player→c) with the negative threat-density gradient
   (toward safety). *(escape-gradient)*

These are wired + tested + shipped as `AWARE_CANDIDATE_CONFIG` (equal weights at proposal). **The
GATE consideration set + weights are pinned at prereg by conductor + Matt (charter §2.2 / §4), NOT
this wave.**

---

## Test + battery counts

| Artifact | Count | Result |
|---|---|---|
| Policy-seam unit tests (`test_aware_fighter_policy_seam.py`) | 32 | PASS |
| Existing spatial-gauntlet tests (`test_spatial_gauntlet_scenarios.py`) | 27 | PASS (no regression) |
| Combined engine run | 59 | PASS |
| Equivalence battery — smoke (2 pairs × 1 seed × 2 legs) | 4 fights compared | PASS |
| Equivalence battery — FULL (256 × 2 legs) | 256 fights compared | **PASS, bit-equal** |
| BEFORE cross-check vs recorded W3′ | 256 | clean (0 mismatch) |

---

## Commits (commit-never-push; both repos)

**Engine repo (`reincarnated-engine`, branch `main`) — held for Gate-2 PASS before push:**
- `1dc8251` — intake metric (`player_damage_taken` + accumulator + wiring).
- `880ad06` — policy seam (considerations/exposure_map/seam packages + engine wiring + byte-neutral
  decision-trace instrument).
- `2d99f15` — policy-seam unit tests (32).

**Collaboration repo (`reincarnated-collaboration`) — math note, harness, verdicts, report** (this
commit; see the accompanying commit hash).

---

## Owed / flagged for Gate-2

1. **AWARE cost — HONEST FLAG (not a blocker).** All-5-candidate AWARE = **5.47× BLIND** on a 40-mob
   worst-case arena (above the ~3-4× target). A LEAN {distance + 1 read} set = **1.46× BLIND** (within
   budget). The dominant cost is the per-candidate O(N²) kernel. Mitigations available to prereg
   (per-tick map cache; single shared θ-density field; prune to the pinned subset). The battery gates
   BLIND, not AWARE (charter §2.3); the gate set is pinned at prereg and won't be all 5. Recorded in
   math note §3.4.1. **Nothing owed in BW-1; this is a prereg-tuning input.**
2. **Runtime substrate deviation.** Exposure map reads `max_hp` (not literal `threat_tier`) +
   `preferred_behavior` because tier/archetype are spawn-time, not runtime (math note §3.1.1).
   Behaviorally equivalent on the gate roster. If prereg wants literal `threat_tier` on the entity,
   that is a separate additive plumbing task (out of BW-1 scope) — flagged for the ARCHITECT
   open-questions pass at the prereg boundary.
3. **Semantic-shift declarations (Discipline #12), framed for the decisions-log (jack-ryan writes):**
   (a) player target selection is REPLACED (not branched) — "nearest-first" re-expressed as "argmax
   of a single {distance} consideration", behavior proven identical; (b) `cluster_density` ≠
   `player_gather_primitive` (distinct semantics); (c) `player_damage_taken` excludes self-inflicted
   HP costs (deliberately scoped to enemy-received). These are surfaced here for the Gate-2 reviewer
   and a decisions-log entry, per the charter's semantic-shift discipline.
4. **Battery evidentiary bulk.** The two full per-fight trace dumps (`…-battery-before-full.json` /
   `…-after-full.json`, ~650 KB each) are reproducible via the harness and are NOT committed (only the
   verdict JSONs + smoke JSONs are). If Gate-2 wants the full traces archived, they regenerate
   deterministically with `python3 …-equivalence-battery.py`.
5. **BEFORE-leg worktree** (`/tmp/aware-before-worktree`) is a detached worktree at stamp `a3671d4`
   with a worktree-only (uncommitted) trace hook. It is transient scaffolding for the battery; safe to
   `git worktree remove` after Gate-2. The stamp itself is uncontaminated.

## Out-of-scope confirmed untouched
Mob AI · formation builders / `arena.py` · skill selection (`_select_player_skill_v2`) · `corpus.db`
(read-only, md5-checked) · telemetry schema (beyond the within-seam intake field) · anything outside
`simulation/`. `player_gather_primitive` OFF both configs.
