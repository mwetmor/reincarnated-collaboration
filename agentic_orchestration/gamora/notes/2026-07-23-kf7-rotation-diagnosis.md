# KF-7 rotation diagnosis — why compiled kits emit skill_idx==0 only (gamora, simulation seam)

**Run:** KIT-FIDELITY · **Gate:** KF-7 (rotation follow-up) · **Ledger:** KFL-21b · **Conductor:** gandalf (RUN-CONDUCTOR) · **Date:** 2026-07-23
**Engine HEAD at diagnosis:** `c5a2f2d` (unchanged — Class B, ZERO code). corpus.db READ-ONLY (no re-harvest). Report committed-not-pushed.

---

## VERDICT: **Class B — DESIGN GAP** (with a legitimately-mono-skill subset). ZERO code emitted.

The Phase-2 rotation selector, the SpatialEntity skill fields (`skill_cooldowns` len 2, `energy`,
`commit_skill_idx`), and the selector invocation path are **ALL correctly wired and ALL firing**. The selector
IS invoked for the compiled/projection fighter, DOES evaluate every skill in the kit, and correctly returns the
DPS-max skill. **The degenerate mono-skill output is the CORRECT output of a faithful selector operating on kits
that lack the rotation-discriminating metadata (`role` / per-skill cast-priority / distinct cooldowns).** That
metadata **does not exist in the corpus** — the KF-2 harvest schema never captured it. There is no wire to
connect; there is a missing INPUT.

This is explicitly **NOT** the `flat_damage` (KF-5) dead-wire pattern. In `flat_damage`, a live value existed
and one rename connected it to a resolver that already knew the effect name. **Here the discriminating input
(per-skill role / cast-priority) is universally `None` in the source data — wiring a gate to a field that is
`None` on every skill of every kit connects nothing.** Assigning a role/priority to each skill IS a new design
surface (a data-capture decision), which is precisely the Class B "genuine metadata gap" the charter defines.
Per charter LAW (Class B → "NO CODE. Return a decision-shaped memo … Matt rules"), no diff is emitted, the 40
frames are UNCHANGED, and the rider/validation-table branch (which fires "only if you re-emit") does NOT fire.

---

## The mechanism, traced with file:line evidence

### 1. The selector's only live path for these kits is DPS-max
`spatial_engine.py:2073-2084` `_dps_score(entity, idx)` = `damage_multiplier / max(cooldown_seconds, 0.5)`.
`spatial_engine.py:2087-2125` `_select_player_skill_v2` → for the mana-default family (`etype in
("mana","cooldown","energy","steady","overflow","stamina-as-resource")`, line 2124) returns
`greedy_capstone()` = `max(ready_pool, key=lambda i: _dps_score(entity, i))` (line 2111-2113).
All 5 compiled kits carry `energy_type="mana"` (`kit_compiler.py:547,624`), so **greedy-DPS-max is the ONLY
selection logic that runs**. The rage/combo/charge-stack branches (`:2127-2153`) are Phase-R BUILT-but-inert.

### 2. The KERNEL selector this ports is ALSO DPS-max — its variety comes only from role-keyed gates
`ai_strategies.py:472` `_common` → `return max(available, key=dps_score)`. Its ONLY multi-skill variety comes
from three gates that fire BEFORE the DPS sort:
- reactive-heal (`:428-431`): `hp_pct < 0.40` → a skill with `role in ("sustain","defensive")`
- combo-spend (`:435-438`): `energy_type=="combo" and mana>=3` → a skill with `role in ("burst_damage","area_damage")`
- control-first (`:456-464`): `role == "control"` → the control skill

**Every one of these gates keys off `skill.role`.** The spatial port faithfully reproduces this: it, too, only
diverges from DPS-max via role-keyed gates (`spatial_engine.py:2020` `skill.get("role","") == role`; `:2068`
`.get("role","") in _SPENDER_ROLES`; `:854` `skill_dict.get("role","")`). **Every role read defaults to `""`.**

### 3. Compiled kits carry NO `role` — so no variety gate can engage
`kit_compiler.py:586-611` builds the `skill_dict` with: `id, name, geometry_type, spatial_geometry_type,
geometry_params, canonical_element, scaling_attribute, damage_scaling_type, damage_multiplier, energy_cost,
cadence, tier, effects` + underscore provenance. **There is NO `role` key, NO `cooldown_seconds` key, NO
`range_m` key, NO `cast_priority` key.** Empirically confirmed on all 5 compiled kits: every skill reports
`role=None, cooldown_seconds=0.0(None), range_m=None`. With `role=None`:
- every role gate (control-first / sustain-react / combo-spend) is INERT → the DPS sort is the whole story;
- `cooldown_seconds=None` → `_dps_score = dm/max(0.5,0.5) = 2·dm` for ALL skills → the ordering is **pure `dm`**.

### 4. The corpus never harvested per-skill role / cast-priority / cooldown — verified, not presumed
`CorpusKitReader.read_kit('d2-fire-sorc').skills[0]` carries exactly these fields:
`cadence_class, chain, count_per_cast, delivery_class, element_primary, fork, geometry_value, ordinal,
pierce, range_band, source_skill, speed_band, width_band`.
**No `role`. No `cooldown_seconds`. No `cast_priority`. No per-skill rotation ordering signal.** The KF-2
harvest captured geometry / element / cadence-class / delivery / projectile-count, but never a combat ROLE or a
cast-priority. So there is nothing in the compiler's source to pass through — the gap is upstream of the seam.

### 5. The consequence splits three ways across the roster (per-kit taxonomy)

| kit | n_skills | skill_idx histogram (seed20260722/blind, HEAD) | cause | legitimate? |
|---|---|---|---|---|
| **d2-firewall-sorc** | 1 | {0: …} | only one skill exists | **YES — mono-skill by composition** |
| **poe1-cyclone** | 1 | {0: …} | only one skill exists (channel-commit) | **YES — the charter's named cyclone exception** |
| **d2-fire-sorc** | 2 | **{0: 2}** (Meteor/idx1 never fires) | `dm`-TIE: FireBall 2.63 == Meteor 2.63 → `max()` returns FIRST → idx0 | **NO — Meteor structurally cannot fire** |
| **gd-flames-of-ignaffar** | 2 | (GAP: 0 damage) | `dm`-TIE: 1.0 == 1.0 → idx0 | NO — but GAP; no damage regardless of which fires |
| **poe2-bonestorm** | 2 | **{0: 10}** (Bone Cage/idx1 never fires) | `dm`-DOMINANCE: Bone Storm 10 >> Bone Cage 1 → greedy correctly never picks the low-DPS control skill | borderline — greedy-DPS-CORRECT, but Bone Cage never fires |

`max()` tie-resolution proof: `max([0,1], key={0:5.26,1:5.26}.__getitem__) == 0` — Python's `max` returns the
FIRST element among equals. This is why the fire-sorc's Meteor (identical `dm` to FireBall) is structurally
unreachable: it can never STRICTLY exceed FireBall's score, and it loses every tie by index order.

**Matt's field report** ("doesn't use any of its skills except what it originally did") is thus corroborated:
for fire-sorc the second skill is unreachable by construction; for bonestorm the second skill is a control tool
the greedy-DPS selector is designed to skip. The DEALT-pct exit predicate is unaffected — the fired skill's
magnitude is anchored correctly (aggregate median 96.51, all in [80,120]); the frames are damage-faithful, they
are just **rotation-flat**.

---

## Split verdict (mixed, as the charter permits)

- **firewall-sorc, cyclone → NO GAP.** Single-skill kits. `skill_idx==0`-only is the composition truth. cyclone
  is the charter's explicitly-named channel-commit mono-skill case — documented here from the composition
  evidence (n_skills=1, `cadence='channel'`), not forced toward variety.
- **fire-sorc, bonestorm → GENUINE DESIGN GAP.** These carry ≥2 skills but no metadata by which a faithful
  selector could choose skill 1 over skill 0 in a way that reflects the source game's rotation. fire-sorc's
  second skill is unreachable (dm-tie); bonestorm's second skill is a control tool greedy-DPS is built to skip.
- **gd-flames → GAP-masked.** Also a dm-tie, but it is a HELD/GAP kit (0 damage), so rotation variety is moot
  until its T4 damage base lands. No action distinct from the fire-sorc case.

---

## Options memo — the missing metadata and 2-3 capture paths (Matt rules)

**What is missing (exactly):** a per-skill signal that lets the selector reflect the SOURCE game's rotation.
Two candidate shapes, either sufficient:
- **(shape α) per-skill `role`** ∈ {primary_attack, burst_damage, area_damage, control, sustain, …} — lights the
  EXISTING kernel + spatial role gates with ZERO selector change once present; OR
- **(shape β) per-skill `cast_priority` / `rotation_ordinal`** — an explicit "fire skill i before skill j when
  both ready" ordering, consumed by a small new selector branch (a role-agnostic priority tiebreak).

Note: `damage_multiplier` and `energy_cost` ARE present and distinct for bonestorm (10/1, cost 10/10) but NOT
for fire-sorc (2.63/2.63) — so cost/dm alone cannot rescue fire-sorc; a role or priority signal is required.

### Path 1 — Harvest per-skill `role` from the corpus source rows (KF-2 schema extension)
- **What:** extend the KF-2 harvest to capture a combat `role` per skill from the already-crawled source
  material (skill descriptions / gem tags / class-guide role language). Compiler passes it through at
  `kit_compiler.py:586` skill_dict (one added key); the kernel + spatial role gates light with no selector code.
- **Cost:** MEDIUM-HIGH. Re-opens the KF-2 harvest (elrond/legolas seam, not gamora) — corpus is READ-ONLY to
  this seam. Requires a role taxonomy + a per-skill labeling pass (LLM-assisted or manual) across the pilot-5
  (and eventually the full corpus). Cross-seam; needs a harvest dispatch. Highest fidelity (role is the native
  ARPG concept; matches how the kernel already thinks). Fixes fire-sorc AND bonestorm AND generalizes.
- **Risk:** role-labeling is a judgment call per skill (is Meteor "burst_damage" or "area_damage"? is Bone Cage
  "control"?) — introduces a small design surface + a labeling-consistency burden. But it is the RIGHT surface.

### Path 2 — Derive a proxy `role` in the compiler from ALREADY-harvested fields (in-seam, zero re-harvest)
- **What:** the compiler synthesizes a `role` from fields the corpus ALREADY carries: `cadence_class`
  (spam/channel/cooldown), `delivery_class` (projectile/zone), `geometry_value` (single_target / ground_targeted_circle
  / placed_lane / multi_projectile / cone / whirlwind). E.g. `placed_lane + zone → "control"`; `cooldown +
  low-cadence → "burst_damage"`; `spam/channel projectile → "primary_attack"`. Compiler-local map at
  `kit_compiler.py:586`; lights the existing role gates.
- **Cost:** LOW. Pure in-seam compiler work, no corpus write, no harvest dispatch. Would let bonestorm's Bone
  Cage (placed_lane/zone → control) fire via the control-first gate, and would break the fire-sorc dm-tie IF the
  two skills map to different roles (Meteor is `ground_targeted_circle/zone/cooldown`, FireBall is
  `single_target/projectile/spam` — they DO differ, so a cadence/geometry-derived role WOULD split them).
- **Risk / why I do NOT lean here despite the low cost:** this is **fabricating a design signal from geometry**,
  which is exactly the class of move the charter's "NO new design surface" clause and Discipline #12 warn
  against. A geometry→role heuristic is a real balance/behavior decision dressed as a derivation — it decides
  "zone skills are control, spam projectiles are primary" as a GLOBAL rule, which is often wrong (a fireball
  nuke is not a "primary attack"; a bonestorm channel is the main DPS, not a builder). It would produce MORE
  rotation motion but LOWER fidelity — motion that reflects a gamora-invented heuristic, not the source game.
  If chosen, it MUST be logged as a Discipline #12 semantic-shift (rotation is now geometry-derived), not a fix.

### Path 3 — Author an explicit per-kit `cast_priority` on the pilot-5 compiled records (curated, narrow)
- **What:** since the pilot-5 is a tiny curated set, hand-author a `cast_priority` (rotation ordinal) per skill
  for JUST these 5 kits (a small table in the compiler or a sidecar), consumed by a minimal role-agnostic
  priority-tiebreak branch in `_select_player_skill_v2`. E.g. fire-sorc: `[Meteor-on-cooldown-else-FireBall]`;
  bonestorm: `[Bone Cage as opener/control, then Bone Storm]`.
- **Cost:** LOW-MEDIUM. In-seam; needs a small new selector branch (~10 lines) + a 5-kit priority table + a math
  note (this changes selection semantics → Discipline #1 + #12). Highest per-kit fidelity for the DEMO roster
  (a human encodes the intended rotation), but does NOT generalize to the full corpus (every new kit needs a
  hand table) and encodes MY reading of each source rotation (a design judgment Matt should own or ratify).
- **Risk:** a hand table is authoritative-looking but is a curated design artifact; it must be Matt-ratified per
  kit (it decides how each pilot "plays"). Does not scale; a stopgap for the 5-kit watch demo, not a system.

### My lean
**Path 1 (harvest per-skill `role`) is the correct long-term fix; Path 3 (curated `cast_priority` for the
pilot-5) is the right SHORT-TERM move IF a rotation-varied watch demo is wanted before the harvest can be
re-opened.** Reasoning:
- Path 1 fixes the gap at its true location (the corpus lacks role; the selector already consumes role
  correctly), generalizes to the whole corpus, and matches the kernel's native concept. It is cross-seam
  (harvest, not gamora) and MEDIUM-HIGH cost, so it is not a same-lane action — it is a KF-2-extension dispatch.
- Path 3 is the honest stopgap: it makes the 5 demo kits play their intended rotations with a human-authored
  ordering, at the cost of not generalizing and needing per-kit ratification. It keeps fidelity HIGH (a human
  encodes the real rotation) whereas Path 2 keeps fidelity LOW (a geometry heuristic guesses).
- **I explicitly do NOT lean Path 2.** It is the cheapest and the most tempting (zero re-harvest, lights the
  existing gates), but it launders a global design decision as a derivation and would produce lower-fidelity
  motion. If Matt wants the cheap path anyway, it is viable — but it must ship as a declared semantic-shift, not
  as a "wiring fix."

**Scope note (named, not crept):** fixing rotation is NOT the DEALT-pct fidelity work KF-7 shipped. The frames
are damage-faithful today; this gap is orthogonal (which skill fires, not how hard). Whichever path Matt rules,
it is a NEW small workstream (Path 1 = harvest dispatch; Path 3 = a selector branch + per-kit table + math note),
not a silent extension of the KF-7 re-emission. No frames were touched by this diagnosis.

---

## Exit-predicate accounting (Class B branch)

- Classification stated with file:line evidence: **DONE** (Class B; §1-§5 above).
- Class B → options memo, **zero code**: **DONE** (no engine diff; HEAD unchanged at `c5a2f2d`; 40 frames
  untouched; rider + validation-table branch correctly NOT fired — it gates on re-emission).
- Report committed (not pushed): pending this write's commit in COLLAB.

**One-line summary for the conductor:** Class B DESIGN GAP — the rotation selector + entity skill fields are
fully wired and firing; compiled kits emit skill_idx==0-only because the corpus never harvested per-skill
`role`/`cast_priority`, so every role-keyed variety gate (kernel `ai_strategies.py:456-464` + spatial mirror) is
inert and the selector falls to pure DPS-max — which ties to idx0 for fire-sorc (dm 2.63==2.63) and correctly
skips bonestorm's low-DPS Bone Cage (dm 10 vs 1); firewall + cyclone are legitimately mono-skill. No wire to
connect (the discriminating input is `None` in the source), so ZERO code per Class B LAW; options memo above,
lean = harvest `role` (long-term) / curated per-kit `cast_priority` for the pilot-5 (short-term stopgap), NOT
the geometry→role heuristic (fidelity-lowering). Matt rules.
