# Finding — 2026-07-16 — Wave-B economy engine spec (Gate-1 / DESIGN-MODE stress-test)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-AMENDMENTS (no BLOCK)
**Target:** `canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` (was DRAFT-FOR-GATE-1, gandalf-prime DRIFT-CRITIC PASS-WITH-NOTES)
**Author under review:** gandalf (SPEC-AUTHOR, autonomous atlas-parity run cycle 2)
**Charge:** gandalf-prime, Matt authorization 2026-07-16 (autonomous run — sub-agents iterate engine toward 100% atlas mechanical parity). Fired on ailment Gate-2 return (`cec8f12`, QA single-instance).
**Principles applied:** Disciplines #1, #8, #11, #12, #13; Review Principles #2, #3, #4; ADR-002 (jack-ryan tier).

---

## Verdict

**PASS-WITH-AMENDMENTS.** The spec is sound, code-grounded, and ready for build-slice dispatch per §12.2. The five §10 escalation rulings (a–e) were audited for internal consistency and code-grounding per charge — **all five stand as ruled; none reversed, none flagged as engine-contradicted.** Ten amendments enumerated below are corrections, reconciliations, and path-fixes — NO BLOCK, NO ruling reversal, NO code defect. Spec-text edits authorized by the charge have been applied (strike/correct/tidy + verdict stamp + STATUS line). Amendments 6–10 ride into the rocket/gamora implementation charges as citation/path corrections.

---

## What I found (descriptive)

The spec extends `bc_target_composer` to add two first-class econ_bin values (`reservation`, `persistent-condition`) and lift the existing deferred `charge-stack` bin with an AM/RC sub-shape field, unblocking 118 kits. Every load-bearing engine-touchpoint claim was checked against live code. The core claims hold: `_DEFERRED_ECON_BINS` (:95), `_ECON_BIN_COST_TYPE_MAP` (:236), `resolve_cost_type` (:247), `check_infeasibility` (:304) exist as cited; the Wave-A A3 reservation machinery (`summon_economy.ECONOMY_RESERVED` :39, `reservation_per_proxy` :59, `reservation_resource` :60) exists and is genuinely extensible to non-proxy carriers as §3 claims; `resource_economy.py` is an additive-only frozen-key config surface that new fields extend cleanly via `_validate`; `effect_resolver.tick_effects` (:55) and `damage_resolver._add_or_refresh` (:1156) / `resolve_skill` (:345) exist as cited. Corpus rosters reproduce: PC/RS/AM/RC/LC/DR any-occurrence counts (45/42/18/18/3/2) match §0; 14/14 named exemplar kits are present. Five citation-level inaccuracies (the `combatant.py:tick` consumer site, the `commitment_state_machine.py` path + extension shape, the empty-`[]`-map semantics, the un-acknowledged existing charge-stack template library, and the proposed-vs-existing `ActiveEffect.category` field) were found and corrected. The ruling-10 riders (TH thorns count, NR disposition) were resolved against corpus ground truth.

---

## Amendments (10)

### A1 — [note #1] cost_type contradiction §4.3 ↔ §4.8/§12.1 — RESOLVED, emission-surface-wins (CODE-CONFIRMED). Severity: WARN → resolved by strike.
`resolve_cost_type` (`bc_target_composer.py:256–274`): when the feasible map is `[]`, `if feasible:` is False and the function falls through to `return role_priority[0]` — a VALID cost_type (mana for most roles), NOT an empty family. **An empty `[]` map does not express "no cost" — it silently resolves to mana.** An empty map is DEFERRED semantics: the bin never reaches the resolver while it sits in `_DEFERRED_ECON_BINS`. A LIFTED active bin MUST carry a resolvable non-empty map. §4.3's lean parenthetical ("both need same cost_type_map = `[]` — the meter IS the resource") is factually wrong about the code and was STRUCK. §4.8/§12.1's `["mana","focus","stamina-as-resource"]` is the correct emission surface. Zero-marginal-cost kits express near-zero cost via `resource_economy.cost_scale`, not an empty map. **note #1 ruling upheld with code citation.**

### A2 — [note #2] trigger-boundary — CONFIRMED CLEAN, no chain leakage. Severity: INFO.
`proc_trigger_condition`'s enum `{on-hit-threshold, on-crit, on-cast-linked, on-kill, on-damage-taken}` (§2.4) is entirely single-trigger primitives — one armed condition → one terminal linked cast. No value encodes trigger-of-a-trigger, chain depth, mark-consume, or re-trigger back-door. `on-cast-linked` (Poet's-Pen) is the closest risk but is the arming READ off the player's own cast, terminal in one bonded spell. §2.2(iii), §9 (CWDT chain DEFERRABLE), and the e=(B) `persistent_trigger` extension hook all hold the boundary. Chain-of-triggers remains Wave-C's `trigger + mark-consume` family. **No spec edit needed; boundary sound as written.**

### A3 — [note #3] §8 HP-economy table looseness — TIDIED. Severity: INFO.
`HP-economy` kit-touch corrected from loose "3 (LC + 2 overlap)" to LC×3 exact (corpus: `["LC"]`×2 + `["RS","LC"]`×1). DR's 2 kits are NOT HP-economy-mapped — drain's Wave-C home is the open §7.3 question, not pre-assigned.

### A4 — [ruling-10 TH rider] §8 `damage-taken-converts` count 0 → 3 — CORRECTED. Severity: WARN.
The "0" was the count of the `damage-taken-converts` *econ_gaps token* (genuinely 0). But a real thorns-retaliation roster exists: corpus folk_names **Retaliation Warlord (gd), Thorns Barbarian (d4), Thorns Invoker (d3)** all carry `econ_gaps=["UNKNOWN"]` and sit in the scoreboard's `econ:UNKNOWN=38` bucket (census §3 row 5). They are damage-taken-converts-family — retaliation = passive reflect keyed off damage-taken, NOT a trigger-cast, so PC proc-loop does NOT cover them. A 4th thorns kit (Thorns Barrier Templar, chronicon) is already `["PC","BT"]` and rides PC. **Wave-C park stands; count is 3, not 0.** Park rationale corrected in §8: the 3 need a `damage-taken-converts` re-tag pass + a passive-reflect sim consumer, neither in Wave-B scope.

### A5 — [ruling-10 NR rider] NR no-resource ×4 — RULED steady-absorbs, no new bin. Severity: ruling (INFO).
NR is NOT a scoreboard bucket and carries ZERO `econ_gaps` tokens in the corpus (`LIKE '%NR%'` = 0). Ruled: NR routes to the existing `steady` bin with near-zero cost via `resource_economy.cost_scale ≈ 0`, NOT a new econ_bin. Grounds: (1) no ranked roster to amortize a bin; (2) `steady` already resolves a valid cost_type + `cost_scale` range (0.60, 1.60) scales toward near-zero-effective (default-corner no-op logic, `resource_economy.py:50`); (3) a "no-resource" bin would carry the same empty-map hazard A1 struck. **Disposition: no Wave-B action. Reopen as a Wave-C `cost_scale`-floor item only if a future census surfaces a ranked NR roster (>~10 kits).** Recorded at §5.3.

### A6 — [WARN] `combatant.py:tick` consumer-site is WRONG. Rides into gamora charge.
`combatant.py` is a state dataclass (`CombatantState`) with NO `tick` method (confirmed — no `def tick`/`def step`/`def advance`). The per-tick fight loop lives in `spatial_gauntlet/spatial_engine.py` (E4 channel-tick service :2326; D4 `_step_proxy_population` :2189). Every "combatant.py:tick" consumer-site citation (§2.8, §3.7, §4.7, §12.1) is imprecise. §1 EXISTS table + §12.1 routing corrected to "`spatial_engine` per-tick loop + `effect_resolver.tick_effects`"; §2.8/§3.7/§4.7 inherit the §1 correction. **gamora wires PC/AM/RC consumers into the spatial-engine tick + `effect_resolver.tick_effects`, mirroring E4 channel-tick and D4 proxy-population precedents — NOT a `combatant.py:tick` method.**

### A7 — [WARN] `commitment_state_machine.py` PATH wrong + extension mis-modeled. Rides into rocket + gamora charges.
Module is at `src/reincarnated/simulation/spatial_gauntlet/commitment_state_machine.py`, NOT the bare `simulation/commitment_state_machine.py` cited in companion-docs (was line 20) and §13 (was line 614). It is the E4 axis: a stateless `.get`-based parser (`read_commitment`), NOT a registry of "commitment_states." `commitment_bin ∈ {snap, wind-up, channel}` is a per-SKILL field (`skill_schema.py:222–223`; None = exempt). ESCALATION-e ruling (B) — split into `persistent_toggle` + `persistent_trigger` — STANDS, but the implementation is **widening the `commitment_bin` enum by 2 values** (rocket owns `skill_schema.py` widen) + a new branch in the E4 consumer at `spatial_engine.py:~2220+` (gamora owns), governed by Discipline #12 (additive widening, same pattern as Wave-A `PROXY_TYPE_TARGETING → PROXY_TYPE_BEHAVIOR`) — NOT "add two states to a machine." Path fixed at companion-docs; extension-shape corrected at §2.6.

### A8 — [INFO] `substrate_templates.py` under-claimed. Rides into rocket charge.
`substrate_templates.py` ALREADY carries `W1_4_CHARGE_STACK` (~25 templates: `charge_up_*`, `stack_builder_*`, `charge_decay_*`, `multi_charge_*`, `charge_on_hit_*`, `overdrive_*`) from Cycle-12 Layer-3. §4.5/§4.8 read as if greenfield-authoring. rocket EXTENDS/REUSES that family (add AM/RC sub-shape routing + any missing `evolution_meter`/`ammo_meter`/`throwing_reload` templates) and must verify template_id overlap to avoid duplicates. §4.8 annotated. This is a "the engine already does X" gap in the direction of under-claiming existing scaffold (net-positive for the charge — less new code than the spec implies).

### A9 — [INFO] `ActiveEffect.category` is PROPOSED, not existing.
`ActiveEffect` (`combatant.py:109`) fields are `name / params / duration_remaining / source_element / tick_accumulated` — there is no `.category` attribute today. §2.3/§4.3's "new `.category` values" read as if extending an existing field. New PC/AM/RC sub-shape state should land in the `params` dict (the ailment layer's precedent — it uses `params` for magnitude/threshold), not a new top-level `.category`. §1 EXISTS table annotated.

### A10 — [INFO] primary-vs-any-occurrence count discipline. Flagged for implementers.
§0's "44 primary / 42 primary / 16 primary" are SCOREBOARD bucket-attributions (census v7 §3 rows 2/4/8/9 — the authority). These differ from naive single-token `econ_gaps` exact counts (`["PC"]`=43, `["RS"]`=37-exclusive, `["AM"]`=17, `["RC"]`=18) by the scoreboard's overlap primary-attribution logic. **Not an error** — the scoreboard is correct authority per the gate stamp. Flagged so build-slice implementers read counts from the scoreboard, not a raw token grep, and so the V8 post-lift census reconciles against the same bucket logic.

---

## Escalation audit (all five stand — per charge, do NOT reopen; flag-and-annotate only)

- **a (one-active-at-a-time PC):** consistent. No engine contradiction — a one-active aura-slot model plugs into `ActiveEffect` cleanly (one entry, `params.stack_count` for Frenzy internal). STANDS.
- **b (hybrid RS: % auras / flat slots):** consistent + backward-compatible. `summon_economy` A3 already ships the flat shape (`reservation_per_proxy`, `reservation_resource`); the % shape is a new `resource_economy` field. Forcing summoner-slots under % would misrepresent D2 integer counts and break A3 backward-compat. STANDS — strongly code-supported.
- **c (one bin + sub_shape):** consistent + smallest-lift, code-confirmed. `charge-stack` already exists as a deferred bin; lifting + sub_shape field is a smaller change than two new bins; both sub-shapes route through the same (now non-empty) cost_type map. STANDS.
- **d (LC/DR defer to Wave C):** consistent. `HP-economy` is HARD-INFEASIBLE per LC-030 (`check_infeasibility:329–333`) — reversing it is a pool-content decision, not a spec-lift; thin roster (5 kits) does not amortize. STANDS. (Note: the LC roster of 3 and DR roster of 2 are corpus-confirmed exactly.)
- **e (split commitment-state):** consistent AS A DESIGN RULING; extension-point description corrected (A7). The player-agency-vs-game-plays-itself AI distinction is real and the split is defensible. STANDS — only the code-shape of the extension was mis-described, not the ruling.

---

## Roster spot-check result

Corpus `agentic_orchestration/research/curated/corpus.db` (read-only):
- **Any-occurrence econ_gaps counts:** PC 45, RS 42, AM 18, RC 18, LC 3, DR 2 — **all match §0 table.**
- **Scoreboard primary buckets (authority):** PC 44, RS 42, AM 16, RC 16, LC 3, DR 2 (census v7 §3) — **match §0 spec ruling column.**
- **14/14 named exemplar kits present:** Auradin (d2), CoC Ice Nova (poe1), Poet's Pen VD (poe1), CWDT Self-Hit Loop (poe1), Wormblaster (poe1), Throw Barbarian (d2), Grim Feast Overleech (poe2), Reaper Form Lich (le), Aspect of Guan Yu Spear (hades1), Queen Sigma (vs), Frost Avalanche Norseman (hot), Runic Invocation Runemaster (le), Cadence Witchblade (gd), Corpse Explosion Necromancer (di).
- **§7.2 LC/DR rosters exact-match** corpus kit_ids (le-reaper-form-lich, poe2-grim-feast, hades1-aspect-guan-yu; vs-queen-sigma, hot-norseman-frost-avalanche).

Rosters are grounded. No fabricated exemplars.

---

## Action

- [x] jack-ryan: spec-text edits applied (strike §4.3 parenthetical; §8 table HP-economy + damage-taken-converts corrections; §6 registry note; companion-docs + §13 path-fix; §2.6 extension-shape note; §4.8 template note; §1 EXISTS consumer-site + ActiveEffect notes; §5.3 NR ruling; §2.4 trigger confirmation; STATUS line; verdict stamp).
- [x] jack-ryan: decisions-log entry (engine repo).
- [ ] rocket (build charge): honor A7 (commitment_bin enum widen at `skill_schema.py`, not a state machine) + A8 (reuse `W1_4_CHARGE_STACK`, verify template_id overlap) + A1 (non-empty cost_type map for lifted charge-stack). Author pre-code math note (Discipline #1) as ailment/Wave-A did. MIGRATION.md at the gen→sim boundary (Review Principle #3, ADR-004).
- [ ] gamora (build charge): honor A6 (consumer site = `spatial_engine` per-tick loop + `effect_resolver.tick_effects`, NOT `combatant.py:tick`) + A9 (sub-shape state in `ActiveEffect.params`). S6 gauntlet cert pre-lift (Review Principle #2). MIGRATION.md.
- [ ] KR: §12.2 slice sequencing (RS first / PC second / charge-stack third) stands; A4 TH re-tag + A5 NR are Wave-C parks (no Wave-B action).
- [ ] Matt (veto surface only — NOT owed a decision): all five escalation rulings remain veto-open; Gate-1 found none engine-contradicted.

---

## References (files reviewed, read-only)

- Spec: `canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md`
- `src/reincarnated/generation/bc_target_composer.py` (`_DEFERRED_ECON_BINS`:95, `_ECON_BIN_COST_TYPE_MAP`:237, `resolve_cost_type`:247, `check_infeasibility`:304)
- `src/reincarnated/generation/summon_economy.py` (A3: `ECONOMY_RESERVED`:39, `reservation_per_proxy`:59, `SUMMON_ECONOMY_KEYS`:51, `build_summon_economy`:78)
- `src/reincarnated/generation/resource_economy.py` (`RESOURCE_ECONOMY_KEYS`:38, `DEFAULT_RESOURCE_ECONOMY`:50, `COST_SCALE_RANGE`:71, `_validate`:101)
- `src/reincarnated/generation/substrate_templates.py` (`W1_4_CHARGE_STACK`:295)
- `src/reincarnated/simulation/spatial_gauntlet/commitment_state_machine.py` (E4 parser; `read_commitment`:88; bins :38–40)
- `src/reincarnated/generation/skill_schema.py` (`commitment_bin`:222–223)
- `src/reincarnated/simulation/combatant.py` (`ActiveEffect`:109; `CombatantState`:148; no `tick` method)
- `src/reincarnated/simulation/effect_resolver.py` (`tick_effects`:55)
- `src/reincarnated/simulation/damage_resolver.py` (`resolve_skill`:345, `_add_or_refresh`:1156)
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (per-tick loop: channel-tick :2326, `_step_proxy_population`:2189)
- Scoreboard: `agentic_orchestration/research/curated/atlas/s2-readiness-census-v7-2026-07-16.md` (§3 bucket detail)
- Corpus: `agentic_orchestration/research/curated/corpus.db` (`canon_engine_key.econ_gaps`, `canon_corpus.folk_name/game`)
- Precedent: `reincarnated-collaboration/canonical/reap-die-rise-engine/ailment-layer-engine-spec.md` (Gate-1/Gate-2 pattern); `agentic_orchestration/jack-ryan/reviews/2026-07-16-ailment-layer-spec-gate1.md`
