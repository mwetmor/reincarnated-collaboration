# Finding — 2026-07-23 — KF-7 consolidated Gate-2 (magnitude shape + rotation diagnosis)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2, BLOCK authority)
**Severity:** INFO — Part 1 **PASS-WITH-NOTES** (no BLOCK) · Part 2 **ENDORSE** (classification sound; no BLOCK)
**Run:** KIT-FIDELITY (Matt-ratified autonomous) · **Ledger:** KFL-21c · **Conductor:** gandalf (RUN-CONDUCTOR)
**Target (Part 1):** engine range `a63d656..c5a2f2d` (1 commit, pushed, branch main)
**Target (Part 2):** `agentic_orchestration/gamora/notes/2026-07-23-kf7-rotation-diagnosis.md` (Class B, ZERO code; HEAD unchanged at `c5a2f2d`)
**Developer:** gamora (simulation seam)
**Predecessor:** my KF-5 Gate-2 (`2026-07-23-kf5-gate2-review.md`, PASS-WITH-NOTES; item-6 ESCALATED → Matt RULED option (a))
**Principles applied:** Disciplines #1 (math-before-code), #2 (smoke vs full-regen), #8 (schema/eval boundary), #11 (empirical inspection), #12 (semantic-shift / attribution); Review Principles #1, #2, #4, #5

---

## PART 1 — engine range `a63d656..c5a2f2d`: PASS-WITH-NOTES

The range implements Matt's item-6 ruling (option (a): compiler injects `base_mean` as magnitude) **exactly**, verified at source, live-compile, smoke, and per-kit-arithmetic level — not on the commit's word. The math note §10 authors the re-derivation BEFORE the code (Discipline #1) and is airtight. No BLOCK.

### Per-item verdict table (Part 1)

| # | Item | Verdict | Load-bearing evidence |
|---|------|---------|----------------------|
| 1 | Magnitude = band mean, None-guarded (matches ruling exactly) | **GREEN** | `kit_compiler.py:283-285`: `(base_min+base_max)/2.0 if (base_min is not None and base_max is not None) else base_max`. This is Matt's ruling verbatim ("`(base_min+base_max)/2.0` when both present, else `base_max`"). **Live-verified per kit:** bonestorm `(205+309)/2=257.0`, fire-sorc `(227+258)/2=242.5`, cyclone `(270+483)/2=376.5`, firewall `(1296+1320)/2=1308.0` — `magnitude==expect_mean` MATCH=True on all four; GAP kit (gd-FoI) injects `None` (KF-4 smoke confirms base_min/base_max both None → magnitude None → partial-in-gap). **None-guard semantics are exact:** base_min/base_max are set as a PAIR in the compiler (`:239-240` — max from `hi`, min from `lo if lo is not None else hi`) or both stay None; there is no single-None path, so `else base_max` is defensively-dead-but-correct (both-None → None; the only reachable None case). |
| 2 | KF-5 smoke band re-center [90,150]→[70,130] — legitimate guard, not pass-anything | **GREEN** | New band = analytic `[80,120]` (= `100 × [0.80,1.20]`, kit-independent since injected==expected base) + ~10pt margin each side (§10.3). **It is a genuine center-drift guard, not widened:** a base_max regression pushes center→120.23, band-max-corner 144.28 **> 130 → RED**; a base_min regression → center 79.77, min-corner 63.8 **< 70 → RED**; faithful base_mean → center 100, band [80,120] fully inside → GREEN. Width is the SAME ±20% envelope as the old band — only the center slid down 20.23. The band still catches the specific regression this fix must guard (magnitude back to base_max), so it is a fidelity gauge, not a variance gate. Self-run smoke: **PASS**, empirical [80.01, 117.94], center ~100, n=59, determinism byte-identical. Matches conductor's run. |
| 3 | `damage_resolver.py:942` docstring ±15%→±20% (my INFO-1) | **GREEN** | `:941-943` docstring now reads "±20% per-hit roll … live constants _DMGVAR_LO=0.80 / _DMGVAR_HI=1.20 = ±20% … INFO-1 docstring fix". Docstring ONLY; the constant `magnitude *= rng.uniform(_DMGVAR_LO, _DMGVAR_HI)` is untouched. Resolves my prior INFO-1 exactly. No combat change. |
| 4 | Additive tick field `skill_cooldowns` (rider-ii; v1-additive, zero-derivation) | **GREEN** | `replica_frame_emitter.py:234-236`: `[_finite(float(c), "skill_cooldown") for c in (getattr(ent, "skill_cooldowns", None) or [])]`. **Pure read** of a REAL live field (`SpatialEntity.skill_cooldowns`, declared `list[float]` at `spatial_engine.py:939`; decremented per-tick at `:4732`; set at cast sites `:3317/:4272/:4554`) — mutates nothing, derives nothing. **Null-safe** → `[]` for mobs/pre-fight (matches the existing `energy`/`commit_state` guarded-optional pattern). **Correctly v1-additive:** `SCHEMA_VERSION` stays `"replica-frame/v1"` — adding a key to a JSON tick record is backward-compatible; no bump owed. Observation-path only, so determinism byte-identity is preserved (self-run smoke confirms). |

### Prior-review disposition (requested): positivity assert — IMPLEMENTED, in the PRIOR range, NOT outstanding

My KF-5 finding's NOTE requested a realized-damage POSITIVITY assert on the projection path (finite ≠ live; a non-GAP damage base must assert `amount>0`, not merely finite). **Status: IMPLEMENTED and live — but it landed at `b492c77` (the R-KF5-1 fix inside the prior KF-5 range), not in this KF-7 range.** `smoke_kf5_expected_pct.py:149-153` computes `all_positive = all(a > 0.0 for a in amounts)` and folds it into `ok` (HEALTHY-PATH assert 1). `git log -L 145,153` confirms these lines were introduced at `b492c77` as the healthy-path rewrite that replaced the old zero-damage-blocker branch. This KF-7 range **inherits** the assert and it PASSES (self-run: `amount>0 on all 59 hits, min 1233.7 max 1818.6`). So the positivity-assert item is **closed** — not outstanding. (My separate self-commitment to fold the *discipline-refinement* into engineering-disciplines Disc #11 remains mine to do, documentation-only per ADR-002; it does not gate this range.)

### NOTE (INFO, for the record) — my own prior finding carried a direction slip; gamora correctly did NOT propagate it

My KF-5 finding's item-6 table (line 44) said "kill times shift ~-17% … mobs die faster." **That is a direction slip.** Under option (a), per-hit damage DROPS (bonestorm magnitude 309→257, ×0.8317), so mobs take LONGER to die → **kill times LENGTHEN ~+20%** (`1/0.8317 = 1.2023`). My own line 48 stated the correct direction. gamora's math note §10.3.1 explicitly catches this, adopts the line-48 direction, and states the line-44 slip is NOT propagated. **This is correct developer behavior** — the range carries the right direction (damage down, kill times up), `mean_mobs_killed` is expected DOWN on the 120s wall (observed, not tuned, per charter Task 4). I record the correction here so the finding trail is self-consistent: the authoritative direction is **damage÷1.202, kill-time×1.202**.

---

## PART 2 — rotation diagnosis: ENDORSE (Class B classification is SOUND)

**Verdict: ENDORSE.** The "no wire to connect — this is a missing INPUT, not an unwired existing field" classification is SOUND at the SOURCE level, not merely presumed. I independently verified every load-bearing claim against the corpus reader and the selector code. The per-kit taxonomy is sound. The zero-code disposition is correct under the charter's Class B law. (Per charter I do NOT rule on capture-path 1/2/3 — that fork is Matt's; I review classification soundness only.)

### Review-question 1 — is "no wire to connect" sound, or is there an existing corpus field that could legitimately discriminate rotation? — SOUND

The decisive check is what the per-skill source structure actually carries. `SkillRow` (`kit_reader.py:33-47`) — the ONLY per-skill record the compiler reads — carries exactly: `ordinal, source_skill, geometry_value, element_primary, delivery_class, width_band, range_band, speed_band, pierce, chain, fork, count_per_cast, cadence_class`. This **matches the diagnosis's §4 field list exactly.** Examined for a legitimate rotation discriminator:
- **No combat `role`.** The `factor_role` that DOES exist (`CompositionFactor:62`) is a **damage-math** role (base/modifier/hit_chance/crit_ev/mitigation) — it discriminates how a factor enters the damage product, NOT rotation priority. It cannot key a rotation gate. (Confirmed the compiler's `role` reads at `:213-268` are this damage-math role, a different concept from the selector's `skill.role`.)
- **No `cooldown_seconds`** per-skill (cooldown is engine-derived at cast time, not harvested).
- **No `cast_priority`/`rotation_ordinal`.** `ordinal` exists but is list-position in the mapping, not intended cast-priority — using it AS rotation order would fabricate semantics (list-order ≠ designed priority).

So there is **no existing corpus field that could legitimately discriminate rotation without fabricating a design signal.** The one field that could (`ordinal`) is a provenance index, not a rotation intent. The diagnosis's Path 2 (geometry→role heuristic) is correctly self-flagged as fabrication (Disc #12) — and I concur it is fabrication, not a latent wire. **"No wire to connect" holds.**

### Review-question 2 — is the per-kit taxonomy sound? — YES

Every causal claim confirmed LIVE (compiled the pilot roster, read `damage_multiplier`/`role`/`cooldown_seconds`/`cast_priority` off each skill_dict, replicated `_dps_score`):

| kit | n_skills | live evidence | diagnosis class | my verdict |
|---|---|---|---|---|
| d2-firewall-sorc | 1 | idx0 only exists | mono-skill by composition | **SOUND (NO GAP)** |
| poe1-cyclone | 1 | idx0 only (channel-commit) | charter's named mono-skill exception | **SOUND (NO GAP)** |
| d2-fire-sorc | 2 | FireBall dm=2.63 == Meteor dm=2.63; both dps_score=5.26; role/cd/prio all `<<absent>>` → `max()` returns idx0; Meteor unreachable | genuine DESIGN GAP | **SOUND** |
| poe2-bonestorm | 2 | Bone Storm dm=10 (dps 20) >> Bone Cage dm=1 (dps 2); greedy-DPS correctly skips the low-DPS control tool | genuine DESIGN GAP (greedy-correct, control never fires) | **SOUND** |
| gd-flames-of-ignaffar | 2 | GAP (0 damage); dm-tie masked | GAP-masked | **SOUND** |

Confirmed too: fire-sorc's `energy_cost` DIFFERS (14.5 vs 10.0) but cost does NOT enter `_dps_score` on the mana-default greedy path — so cost cannot rescue the tie (diagnosis line 111 exact). The mono/tie/dominance split is faithful to the mechanism, not forced toward variety.

### Review-question 3 — is the selector genuinely fully-wired-and-firing (so the gap is input, not wiring)? — YES

- **Selector fires:** `_select_player_skill_v2` (`spatial_engine.py:2087`) → for `etype in ("mana",...)` (`:2124`) returns `greedy_capstone()` = `max(ready_pool, key=_dps_score)`. All 5 kits are `energy_type="mana"` → greedy-DPS-max is the only live branch (rage/combo/charge branches are Phase-R built-but-inert). Confirmed.
- **`_dps_score` collapses to pure `dm`** when `cooldown_seconds` is absent: `dm/max(cd,0.5)` with `cd=(… or 0.0)=0.0` → `2·dm` (`:2082-2084`). Ordering is pure `dm`. Confirmed.
- **The selector DOES consume `role` correctly — the input is what's missing.** Kernel `ai_strategies.py` has three role-keyed variety gates: reactive-heal (`:428-431`, `role in ("sustain","defensive")`), combo-spend (`:435-438`, `role in ("burst_damage","area_damage")`), control-first (`:456-464` + bc-coordinate tri-state, `role=="control"`). The spatial port mirrors them (`:854`, `:2020 == role`, `:2068 in _SPENDER_ROLES`). **Every gate defaults `role` to `""` via `.get("role","")`** — so with `role` absent on every compiled skill, every gate is inert and selection falls to the DPS sort. The gates are real and correctly keyed; they starve because the input is None. This is the genuine "wire present, input absent" pattern the diagnosis claims — verified.

### Review-question 4 — is zero-code correct under Class B law? — YES

The charter's Class B law is "genuine metadata gap → NO CODE, decision-shaped memo, Matt rules." This IS a genuine metadata gap (per-skill rotation `role`/`cast_priority` is universally absent in the source data; connecting a gate to a field that is None on every skill of every kit connects nothing). HEAD is unchanged at `c5a2f2d`; the 40 frames are untouched; the re-emission rider + validation-table branch correctly did NOT fire (they gate on re-emission). **Zero-code is the correct disposition.** This is explicitly NOT the `flat_damage` (KF-5) dead-wire pattern — there, a live value existed and one rename connected it; here the discriminating input does not exist in the source. The diagnosis draws that distinction correctly (§ intro + line 20-24).

### One NOTE on the diagnosis (INFO, non-blocking, does not affect the verdict)

The diagnosis's own lean (Path 1 long-term / Path 3 short-term / explicitly-not Path 2) is a well-reasoned options memo, and its Disc-#12 flag on Path 2 (geometry→role is a laundered global design decision, not a derivation) is exactly right — if Path 2 is ever chosen it MUST ship as a declared semantic-shift, not a "wiring fix." I ENDORSE that framing. **But path selection is Matt's fork per the charter, and I do not rule on it** — I confirm only that all three paths correctly presuppose new input/design (none is a latent wire), which is what makes the Class B classification sound regardless of which path Matt picks.

---

## Consolidated verdict

- **Part 1 (engine range `a63d656..c5a2f2d`): PASS-WITH-NOTES.** 4 GREEN / 0 RED / 0 GAP. Ruling implemented exactly; math-before-code satisfied; smoke PASS byte-identical; positivity assert confirmed live (landed prior range, closed). Notes are INFO-only (my own prior direction-slip, corrected here; gamora correctly did not propagate it).
- **Part 2 (rotation diagnosis): ENDORSE.** Class B DESIGN GAP classification is SOUND at source level (SkillRow carries no rotation discriminator; the only candidate field, `ordinal`, is provenance not intent). Per-kit taxonomy sound (all causal claims live-verified). Selector genuinely fully-wired-and-firing (gates real, keyed on `role`, starved by absent input). Zero-code correct under Class B law. Capture-path fork left to Matt per charter.
- **No BLOCK on either part.**

## Action

- [x] Developer (gamora): both parts pass. No fix-forward required. Ruling-exact, math-airtight, diagnosis-sound.
- [x] jack-ryan (self): my prior KF-5 finding line-44 direction slip is corrected in this finding's Part-1 NOTE (authoritative direction: damage÷1.202, kill-time×1.202). The Disc #11 positivity-assert discipline-refinement remains my documentation-only follow-up (ADR-002), non-blocking.
- [ ] Matt: (a) item-6 ruling is DONE (this range implements it). (b) The rotation capture-path fork (Path 1 harvest `role` / Path 3 curated `cast_priority` / Path 2 geometry-heuristic-with-Disc#12-declaration) awaits your ruling — the Class B classification that gates it is SOUND per this review. No action owed on either KF-7 part before that fork.
- [x] Conductor (gandalf): both verdicts PASS/ENDORSE → the range stands and the diagnosis is endorsed for the ledger. Push per your discipline; I do not push.

## References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/kit_compiler/kit_compiler.py:283-285` (magnitude=band-mean, None-guarded), `:239-240` (paired base_min/base_max assignment → None-guard exactness), `:213-268` (damage-math `factor_role`, distinct from rotation role), `:586-611` (compiled skill_dict — no role/cd/cast_priority), `:2087-2125`… → see spatial_engine
- `~/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py:941-943` (docstring ±20% fix; constant untouched)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/replica_frame_emitter.py:234-236` (additive `skill_cooldowns`, pure read), `:26/:168` (`SCHEMA_VERSION` stays v1)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:939` (`skill_cooldowns: list[float]` live field), `:2073-2125` (`_dps_score` + `_select_player_skill_v2`), `:854/:2020/:2068` (spatial role gates), `:4732` (per-tick cooldown decrement)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/ai_strategies.py:428-431/435-438/456-464` (kernel role-keyed variety gates)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/kit_compiler/kit_reader.py:33-47` (`SkillRow` — the corpus per-skill surface; no rotation discriminator), `:58-65` (`CompositionFactor.factor_role` = damage-math role)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/kit_compiler/smoke_kf5_expected_pct.py:149-153` (positivity assert; introduced `b492c77`), `:171` (band [70,130])
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kf5-expected-pct-2026-07-23.md` §10 (KF-7 re-derivation, math-before-code)
- Self-run: `smoke_kf5_expected_pct` (PASS, [80.01,117.94], n=59, byte-identical) · `smoke_kf4_compiler` (36G·0R·1GAP) · per-kit `compile_kit` magnitude==band-mean MATCH=True
- `~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-23-kf7-rotation-diagnosis.md` (reviewed) · `…/jack-ryan/notes/2026-07-23-kf5-gate2-review.md` (predecessor)
