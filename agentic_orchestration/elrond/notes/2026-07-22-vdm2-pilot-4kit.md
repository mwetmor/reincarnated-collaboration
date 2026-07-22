# VDM-2 4-Kit Pilot — Gate Evaluation + Structured-Shape Conversion — Wave W2

**Author:** elrond (data steward) · **Date:** 2026-07-22 · **Status:** DELIVERED (note-space conversion only; corpus.db UNTOUCHED, md5 verified unchanged)
**Run:** `2026-07-22-vdm2-edition-next-lap` (gandalf `RUN-CONDUCTOR`)
**Wave:** W2 — the 4-kit pilot that GATES the DDL (per migration plan §4.1: pilot FIRST, apply only after gates)
**Companion (W0):** `2026-07-22-vdm2-schema-diff-and-ddl-v0.md` + `2026-07-22-vdm2-ddl-v0.sql`
**Spec:** `matt_notes_handoff_docs/rdr-vdm2-field-delta-spec.md` (§9 pilot set + freeze gates)
**Conductor rulings applied:** D-1..D-6 (run-ledger vetoes V-11..V-16)
**corpus.db:** `agentic_orchestration/research/curated/corpus.db` @ `v1.1-verified` · **md5 `50df15b776ad5b0da93fe90cdee1163d`** at open AND close (read-only wave; DDL NOT applied, not even locally).

---

## 0. GATE SCOREBOARD (the headline)

| Gate | Verdict | One-line |
|---|---|---|
| **G1** — ≥90% deviation prose → structured `kit_deviation` rows | **PASS** | 6/6 deviation propositions across 3 prose-bearing kits convert losslessly (100%); the 4th kit has empty deviation_notes = trivially lossless (0/0). |
| **G2** — ≥80% door args derivable from EXISTING prose, no re-crawl | **PASS (conditional flag)** | 11/13 door-arg instances derivable from existing dossier/mapping prose (85%). 2 flagged re-crawl: Masquerade `DUAL_PROXY.sync_mode` timing + the D2 `.txt` datamine `exact{}` lane (which is **NOT on record** — see G-FIND-1). |
| **G3** — zero prose-only geometry on pilot T1 (primary skill) | **PASS** | All 4 primary skills band cleanly to structured `skill_geometry_band` rows; `count_multiplier` (Masquerade triple-volley), previously prose-only, is captured structurally. |
| **G4** — ≥1 red assert routes end-to-end to a `mechanic_gap_docket` row via `intake_lane='deviation'`, `status='open'` | **PASS** | 4/4 kits produce ≥1 red assert; the Masquerade multi-origin assert routes to a would-be docket row (shown §4, G4 block). Distinct from the 19 matt-ratified rows by `status='open'` + `intake_lane='deviation'`. |
| **G5** — no BREAKING schema change forced by the 3 non-D3 pilots | **PASS** | Zero breaking changes. **7 ADDITIVE amendments** to DDL v0 identified (listed §6). All are new columns / enum-value additions / one small table — none invalidates a v0 statement or an existing row. |

**D-2 grain verdict (pre-registered refutation):** **HYPOTHESIS HOLDS with a documented rider.** Per-skill `(kit_id, skill_ordinal)` geometry grain survives the PoE support-gem (CoC Ice Nova) and GD transmuter (Stun Jacks) refutation surface. The support-gem transformation is correctly modeled as a **door + trigger_grammar primitive on the payload skill's row**, NOT as its own phantom "support-gem skill" row — which is exactly what the per-skill grain expresses. One G5-class rider (additive): a `parallel_trigger` marker is needed to represent Cospri's second on-crit trigger without inventing a chain. Full analysis §5.

**Nothing halts the W3 apply.** Two inputs the W3 rider must carry (neither blocking): (a) the `exact{}` datamine lane is a re-crawl dependency, not present in the store — keep `exact_json` NULL at apply; (b) the 8 NULL-`t4_doors` kits are MEANINGFUL gaps (not artifacts), so the W3 door-strip rider must preserve NULL, not coerce to empty (see §7).

---

## 1. PILOT SET — resolved

| # | Spec §9 slot | Kit chosen | `kit_id` | Why this kit |
|---|---|---|---|---|
| 1 | GX-11 Masquerade (D3 `set_threshold`, player_attested) | Masquerade Bone Spear | `d3-masquerade-spear` | The named exemplar; every §2–§8 structure demonstrated. 3 skills; `DUAL_PROXY`. |
| 2 | D2 Lightning-Sentry Trapsin (`synergy_stack`, txt datamine) | Trapsin | `d2-trapsin` | The named kit. 3 totem skills; `PROXY_ASCENSION`; Shadow Master GAP. Used as the `exact{}` stress test — see G-FIND-1. |
| 3 | One PoE support-gem build (`support_gem` composition) | CoC Ice Nova | `poe1-coc-ice-nova` | **Strongest D-2 refutation surface.** Cast-on-Critical-Strike IS the support-gem-composition ur-case: the transformation is a *linked support*, not a skill. Cospri's Malice = a SECOND parallel on-crit trigger; CDR-breakpoint "attack-rate becomes cast-rate". Grade CLOSE. Picked over `poe1-poets-pen-vd` (also 3-skill trigger) because CoC's payload-vs-host split is the cleanest test of "is a support a skill row or a modifier?". |
| 4 | One GD transmuter build (`transmuter` ontology) | Stun Jacks | `gd-stun-jacks` | **Transmuter explicitly on record** ("Quick Jack transmuter enables spam"). Grade EXACT; single skill; **empty `deviation_notes`** — a deliberate G1 edge case (does the pipeline behave when there's zero deviation prose?). Picked over `gd-canister-saboteur` because Quick Jack is a *skill-native transmuter* (spec §8 `transmuter` acquisition enum) vs Canister's device-throw composite. |

Selection rationale for the two unnamed slots is recorded because spec §9 under-specifies them (it says "one PoE support-gem build" / "one GD transmuter build" without a kit_id). Both picks are the strongest refutation-surface candidates in `kit_master` for their ontology.

---

## 2. GROUND-TRUTH CORRECTIONS surfaced this pilot (feed W3 + amend W0)

The pilot re-examined census facts my W0 diff asserted. Three corrections:

1. **The "8 empty-string door slots" (W0) are actually 8 kits with `t4_doors = NULL` (the whole array is null), not empty-string slots inside an array.** All 8 are D2. This changes the D-1 empty-string characterization materially (§7). W0 §2/§5 should be read with this correction.
2. **record-270 = 270 *including* system-records; 267 *excluding* them.** The 3-kit gap is 3 system-records inside the five record games (1 `le` + 2 `poe2`, `is_system=1`). The door census (462 instances / 28 distinct) is over the **267** doored+mapping record kits.
3. **`is_system=1` count is 19, not 11** (W0 D-4 said 11). The 19 span 11 games; only 3 fall inside the five record games. **This re-frames D-4:** the `corpus_class='system'` enum still lands, but it covers **19** system-records across 585, of which 3 are inside the record-game set. `585 = record 267-doored (270 incl-system) + annex 296 + system... ` — the exact partition is a W3-rider arithmetic the conductor's D-4 ruling (585 = 270 record + 304 annex + 11 system) must be reconciled against the **live count of 19 system-records**. **Flagged for W3, non-blocking** (the enum admits `system`; only the tallies shift). See §6 amendment A-6.

These are data-census corrections, not schema changes. They do not alter the DDL; they alter the W3 rider's expected row-counts and the D-1/D-4 characterizations.

---

## 3. STRUCTURED-SHAPE CONVERSION — the four kits

Each block converts EXISTING dossier/mapping/citation prose into the full VDM-2 structured shapes: door args · deviations · per-skill geometry bands · numerics (raw + unit + provenance; `rdr_value` NULL per D-3) · recognition hooks · acceptance asserts · delta_t4. All values are anchored to the verbatim prose they were read from (elrond source-anchor law). **No balance transforms authored** (D-3: all `rdr_value` honest-NULL).

### 3.1 — `d3-masquerade-spear` (GX-11 Masquerade Bone Spear · D3 · `set_threshold`)

**Doors (§2) — args derived from prose:**
```json
"kit_door_arg": [
  { "door":"DUAL_PROXY", "arg":"proxy_count",      "value":"2",                     "derivation":"dossier-prose", "mutation_surface":"mutable",
    "source_anchor":"cast Simulacrum at rift start to spawn two blood-clones" },
  { "door":"DUAL_PROXY", "arg":"permanence",        "value":"permanent",             "derivation":"dossier-prose", "mutation_surface":"locked",
    "source_anchor":"Two permanent blood-clone proxies spawned at rift start" },
  { "door":"DUAL_PROXY", "arg":"mirrored_skills",   "value":"[\"bone_spear\"]",      "derivation":"dossier-prose", "mutation_surface":"mutable",
    "source_anchor":"clones mirror every cast, tripling projectile delivery" },
  { "door":"DUAL_PROXY", "arg":"origin_model",      "value":"proxy_positions",       "derivation":"dossier-prose", "mutation_surface":"locked",
    "source_anchor":"clones stand where spawned, creating three distinct spatial origins" },
  { "door":"DUAL_PROXY", "arg":"sync_mode",         "value":"mirrored_simultaneous", "derivation":"RE-CRAWL-FLAG",  "mutation_surface":"locked",
    "source_anchor":"(inferred from 'mirror every cast simultaneously' — the EXACT simultaneity vs 1-frame-delay is not attested; timing needs a datamine, flagged for G2)" },
  { "door":"PERSISTENCE_ENGINE_uptime", "arg":"resource_ref",       "value":"simulacrum_active", "derivation":"dossier-prose", "mutation_surface":"locked",
    "source_anchor":"83% DR while Simulacrum is active" },
  { "door":"PERSISTENCE_ENGINE_uptime", "arg":"effect_while_active","value":"[{\"type\":\"damage_reduction\",\"rdr_value_ref\":\"num.dr_masq\"}]", "derivation":"dossier-prose", "mutation_surface":"locked",
    "source_anchor":"effectively provides you with 83% damage reduction while Simulacrum is active" }
]
```
7 arg bindings from prose; 6 derivable directly, 1 (`sync_mode` exact timing) flagged re-crawl.

**Deviations (§3) — 2 propositions in the prose, both convert:**
```json
"kit_deviation": [
  { "missing_expression":"synchronized 3-projectile volley from 3 spatial origins",
    "deviation_class":"engine_inexpressible", "hook_refs":["H1"],
    "proposed_fix_type":"door_param", "proposed_fix_target":"DUAL_PROXY.sync_mode+origin_model",
    "source_anchor":"three-simultaneous via clone mirrors has no native expression; DUAL_PROXY covers the delegation but not the synchronized volley feel" },
  { "missing_expression":"Simulacrum clones addressable at their 3 distinct spatial spawn origins",
    "deviation_class":"engine_inexpressible", "hook_refs":["H1"],
    "proposed_fix_type":"door_param", "proposed_fix_target":"DUAL_PROXY.origin_model",
    "source_anchor":"engine proxy positions are not separately addressable" }
]
```

**Per-skill geometry bands (§4) — 3 skills, 3 rows:**
```json
"skill_geometry_band": [
  { "skill_ordinal":0, "source_skill":"Bone Spear (Shatter rune)", "delivery_class":"projectile",
    "origin":"self_and_proxies", "width_band":"narrow", "range_band":"long", "speed_band":"fast",
    "pierce":"all", "chain":0, "fork":0, "count_per_cast":1,
    "count_multiplier_x":3, "count_multiplier_source":"door:DUAL_PROXY",
    "cadence_class":"builder_spender", "motion_signature":"straight_line", "band_conf":0.82,
    "derivation":"dossier-prose",
    "source_anchor":"Bone Spear is a narrow pierce projectile; clones fire their own copies — three simultaneous spears per cast" },
  { "skill_ordinal":1, "source_skill":"Simulacrum (Reservoir rune)", "delivery_class":"summon_delegate",
    "origin":"self", "range_band":"self", "cadence_class":"cooldown", "count_per_cast":2,
    "band_conf":0.9, "derivation":"dossier-prose",
    "source_anchor":"Two permanent blood-clone proxies spawned at rift start; mirror all Bone Spear casts" },
  { "skill_ordinal":2, "source_skill":"Grim Scythe (Frost Scythe rune)", "delivery_class":"melee_arc",
    "origin":"self", "range_band":"melee", "cadence_class":"builder_spender", "band_conf":0.85,
    "derivation":"dossier-prose",
    "source_anchor":"close-range generator maintaining Essence for Bone Spear spam" }
]
```
Note `skill_ordinal:1` (Simulacrum) uses `count_per_cast:2` and delivery `summon_delegate` — the `range_band` uses value `self` which is NOT in the v0 CHECK enum {melee,short,medium,long,screen}. **→ Amendment A-1** (add `self` to `range_band`).

**Numerics (§5) — 2 prose-stranded source values, both landed; `rdr_value` NULL per D-3:**
```json
"kit_numeric": [
  { "numeric_key":"dr_masq",  "source_value":83,   "source_scale":"d3_pct_dr",        "rdr_value":null, "rule_id":null,
    "source_anchor":"effectively provides you with 83% damage reduction while Simulacrum is active" },
  { "numeric_key":"set_mult", "source_value":5500, "source_scale":"d3_set_pct_bonus", "rdr_value":null, "rule_id":null,
    "source_anchor":"5,500% increased Bone Spear damage" }
]
```

**Recognition hooks (§6) — 5 hooks; H4 provenance=player_attested (per spec, only via attestation):**
```json
"recognition_hook": [
  {"hook_id":"H1","rank":1,"hook_type":"geometry","hook_text":"three simultaneous spears from three spatial origins","expressed_by":"door:DUAL_PROXY{sync_mode,origin_model}","provenance":"crawled","coverage_status":"accepted_downgrade"},
  {"hook_id":"H2","rank":2,"hook_type":"defense_identity","hook_text":"permanent clone uptime is the survival plan (83% DR)","expressed_by":"door:PERSISTENCE_ENGINE_uptime","provenance":"crawled","coverage_status":"expressed"},
  {"hook_id":"H3","rank":3,"hook_type":"cadence","hook_text":"Grim Scythe builder -> Bone Spear spender rhythm","expressed_by":"geometry.cadence_class","provenance":"crawled","coverage_status":"expressed"},
  {"hook_id":"H4","rank":4,"hook_type":"threshold_moment","hook_text":"final set piece = discrete build-defining state change","expressed_by":"assert:delta_t4","provenance":"player_attested","coverage_status":"expressed"},
  {"hook_id":"H5","rank":5,"hook_type":"register","hook_text":"shadow element register","expressed_by":"element:shadow","provenance":"crawled","coverage_status":"expressed"}
]
```
H1 is `accepted_downgrade` because its full expression (multi-origin) is engine-inexpressible today (routed to a docket via the deviation above). This is the coverage-QA machine-check working: a hook whose full form is unexpressed is downgrade-covered, not silently CLOSE.

**Acceptance + delta_t4 (§6):**
```json
"kit_acceptance_assert": [
  {"assert_text":"projectiles_per_cast == 3","hook_id":"H1","expected_state":null,"last_result":"green"},
  {"assert_text":"distinct_projectile_origins == 3","hook_id":"H1","expected_state":"RED until DUAL_PROXY.origin_model ships","last_result":"red"},
  {"assert_text":"uptime_pct(simulacrum_active) >= 95","hook_id":"H2","last_result":"green"},
  {"assert_text":"damage_share(bone_spear_family) >= 0.60","hook_id":"H1","last_result":"green"}
],
"kit_delta_t4": {
  "shape":"step", "shape_signoff":"human-validated", "shape_signoff_by":"Hale (player_attested, spec §0)",
  "asserts_json":["projectiles_per_cast: 1 -> 3","dr_uptime: 0 -> >= 95%","damage_share(bone_spear_family): + >= 30pts"]
}
```

---

### 3.2 — `d2-trapsin` (D2 Lightning-Sentry Trapsin · `synergy_stack`)

**Doors (§2):** one door on record — `PROXY_ASCENSION`.
```json
"kit_door_arg": [
  { "door":"PROXY_ASCENSION", "arg":"proxy_type",      "value":"placed_emitter",  "derivation":"dossier-prose", "mutation_surface":"locked",
    "source_anchor":"Stationary placed emitter (totem lane per totem-vs-companion law)" },
  { "door":"PROXY_ASCENSION", "arg":"max_active",       "value":"5",               "derivation":"dossier-prose", "mutation_surface":"mutable",
    "source_anchor":"up to 5 active at a time" },
  { "door":"PROXY_ASCENSION", "arg":"proxy_autonomy",   "value":"fire_nearest",    "derivation":"dossier-prose", "mutation_surface":"locked",
    "source_anchor":"Fires piercing lightning bolts at nearest target up to 10 times" }
]
```
3/3 args from prose (no re-crawl).

**Deviations (§3) — 1 proposition (Shadow Master GAP):**
```json
"kit_deviation": [
  { "missing_expression":"Shadow Master = fully autonomous Assassin copy using class skills",
    "deviation_class":"accepted_downgrade", "hook_refs":["H3"],
    "proposed_fix_type":"none", "proposed_fix_target":null,
    "downgrade_owner":"elrond (pilot; W1 GAP-annotation lineage)",
    "source_anchor":"Source player gets a fully autonomous Assassin copy; engine gives a stationary placed emitter. The trap-placement core maps well; SM is the miss." }
]
```
**This is the accepted_downgrade branch of §3** — and it exercises the DDL v0 CHECK that `accepted_downgrade` REQUIRES a `downgrade_owner`. The pilot supplies one. (Whether elrond is the correct sign-off owner or whether this needs a design owner is a W3/W4 routing question — flagged, non-blocking. The CHECK fires correctly either way.)

**Per-skill geometry bands (§4) — 3 skills:**
```json
"skill_geometry_band": [
  { "skill_ordinal":0, "source_skill":"Lightning Sentry", "delivery_class":"summon_delegate",
    "origin":"at_target", "range_band":"medium", "pierce":"all", "count_per_cast":1,
    "cadence_class":"cooldown", "motion_signature":"straight_line", "band_conf":0.87, "derivation":"dossier-prose",
    "source_anchor":"Traps placed at cursor location (stationary emitters); fires piercing lightning bolts at nearest target up to 10 times",
    "exact_json":null, "exact_source_type":null },
  { "skill_ordinal":1, "source_skill":"Death Sentry", "delivery_class":"zone",
    "origin":"at_target", "range_band":"medium", "chain":1, "cadence_class":"cooldown",
    "band_conf":0.87, "derivation":"dossier-prose",
    "source_anchor":"causes nearby corpses to explode, dealing Fire and Physical Damage; chains across nearby corpses" },
  { "skill_ordinal":2, "source_skill":"Shadow Master", "delivery_class":"summon_delegate",
    "origin":"self", "range_band":"screen", "cadence_class":"cooldown", "band_conf":0.6,
    "derivation":"dossier-prose",
    "source_anchor":"Autonomous Assassin companion using class skills — maps as APPROX totem for placement, gap noted" }
]
```

**G-FIND-1 — the `exact{}` datamine stress test (brief-mandated).** The brief asks to "use its `.txt` datamine exact-geometry lane as the `exact{}` stress test." **The `.txt` datamine lane is NOT on record in corpus.db.** The three citations for `d2-trapsin` are all Maxroll/Icy-Veins guide prose (`maxroll.gg/d2/...`, `icy-veins.com/d2/...`); none is a `skills.txt`/`missiles.txt`/`.dbr` datamine. The only exact-geometry fact present is the guide prose "fires piercing lightning bolts at nearest target up to 10 times" — a source-scale count, not a datamine radius/frame/fps. **Consequence:** the `exact_json` overlay column is exercised as designed (it stays NULL and never blocks the kit — the band lands on prose alone), but a genuine `exact{}` population REQUIRES a datamine re-crawl (Legolas Mode-B `.txt` acquisition). This is the correct, spec-aligned behavior (§4: "`exact{}` populated ONLY from datamine lanes… never blocks a kit"), but it means **the pilot cannot fully exercise the `exact{}` write path from the current store** — only its NULL/absent path. Recorded as a G2 re-crawl flag AND a W3-input note: keep `exact_json` NULL at apply; the datamine lane is a downstream Legolas dependency, not a schema gap.

**Numerics (§5):** the only structured-numeric candidate on record is the "up to 10 times" bolt count — which is a *geometry* fact (fold into `count_per_cast`/notes), not a defense/damage-scale numeric. No `%DR`/`%bonus`-style source-scale numeric is attested for the Trapsin. So `kit_numeric` for this kit is **empty (honest)** — a legitimate divergence from Masquerade, and a useful G1/G3 negative: not every kit has dual-column numerics, and that's fine.

**Recognition hooks (§6):**
```json
"recognition_hook": [
  {"hook_id":"H1","rank":1,"hook_type":"geometry","hook_text":"place stationary lightning-bolt emitters, reposition between packs","expressed_by":"geometry.delivery_class","provenance":"crawled","coverage_status":"expressed"},
  {"hook_id":"H2","rank":2,"hook_type":"control","hook_text":"Death Sentry corpse-explosion chain clears packs","expressed_by":"geometry.chain","provenance":"crawled","coverage_status":"expressed"},
  {"hook_id":"H3","rank":3,"hook_type":"other","hook_text":"Shadow Master fights as an autonomous copy","expressed_by":"assert:deviation(accepted_downgrade)","provenance":"crawled","coverage_status":"accepted_downgrade"}
]
```

**Acceptance + delta_t4 (§6) — the `shape:step` stress case (spec §9: "hardest fit for shape:step"):**
```json
"kit_acceptance_assert": [
  {"assert_text":"active_emitters <= 5","hook_id":"H1","last_result":"green"},
  {"assert_text":"death_sentry_chain_targets >= 1","hook_id":"H2","last_result":"green"},
  {"assert_text":"shadow_master_is_autonomous == true","hook_id":"H3","expected_state":"RED — engine gives placed emitter, not autonomous copy","last_result":"red"}
],
"kit_delta_t4": {
  "shape":"ramp", "shape_signoff":"unvalidated",
  "asserts_json":["lightning_sentry_synergy_stack: Shock Web + Charged Bolt Sentry maxed -> per-bolt damage scales continuously","death_sentry: added last as clear-amplifier"],
  "_pilot_note":"The Trapsin transformation is a STACKED SYNERGY GRADIENT (max LS -> max synergies -> max Death Sentry last), not a discrete equip-moment. shape='ramp' is the honest classification. It does NOT force a third enum value — the 2-value {step,ramp} enum absorbs it as 'ramp'. See D-2 verdict / §5 for why 'ramp' suffices and a 3rd value is NOT needed."
}
```
**This resolves the §6/D-2 delta_t4.shape risk:** the spec (§9) flagged the Trapsin as the hardest fit for `shape:step`. The pilot confirms it is **not** a step — it is a `ramp`, and `ramp` is already a v0 enum value. **No schema change forced.** (I deliberately did NOT pre-add a speculative third shape in W0; the pilot confirms none is needed.)

---

### 3.3 — `poe1-coc-ice-nova` (PoE Cast-on-Crit Ice Nova · `support_gem` composition) — THE D-2 REFUTATION SURFACE

**Doors (§2):** `ELEMENTAL_ECHO`, `GEOMETRY_COLLAPSE`.
```json
"kit_door_arg": [
  { "door":"ELEMENTAL_ECHO", "arg":"trigger_condition", "value":"on_crit",     "derivation":"dossier-prose", "mutation_surface":"locked",
    "source_anchor":"Each crit triggers Cast on Critical Strike support, firing Ice Nova and Frostbolt" },
  { "door":"ELEMENTAL_ECHO", "arg":"cadence_scale",     "value":"0.75",        "derivation":"dossier-prose", "mutation_surface":"mutable",
    "source_anchor":"Attack speed is tuned to CDR breakpoints (14% CDR = trigger just over once per server tick); 7.57 APS" },
  { "door":"ELEMENTAL_ECHO", "arg":"parallel_triggers", "value":"2",           "derivation":"dossier-prose", "mutation_surface":"locked",
    "source_anchor":"Cospri's Malice triggers additional Ice Novas from socketed spells on crit — a SECOND parallel trigger" },
  { "door":"GEOMETRY_COLLAPSE", "arg":"collapse_mode",  "value":"burst_around_self", "derivation":"dossier-prose", "mutation_surface":"locked",
    "source_anchor":"Ice Nova expands from player position; overlapping rings of cold covering large zone" }
]
```
4/4 args from prose. Note the `ELEMENTAL_ECHO.parallel_triggers` arg → **Amendment A-2** (the parallel-trigger surface, see D-2 verdict).

**Deviations (§3) — 2 propositions (the two "smoothings"):**
```json
"kit_deviation": [
  { "missing_expression":"Cospri's Malice second parallel on-crit trigger (socketed spells ALSO fire)",
    "deviation_class":"param_gap", "hook_refs":["H1"],
    "proposed_fix_type":"door_param", "proposed_fix_target":"ELEMENTAL_ECHO.parallel_triggers",
    "source_anchor":"only one proc_trigger_condition primitive is modelled, so the double-trigger is a noted parallel not a chain" },
  { "missing_expression":"attack-rate BECOMES cast-rate via precise CDR/server-tick breakpoints",
    "deviation_class":"accepted_downgrade", "hook_refs":["H2"],
    "proposed_fix_type":"none", "proposed_fix_target":null,
    "downgrade_owner":"elrond (pilot)",
    "source_anchor":"carried as cadence_scale, an approximation of a precise server-tick timing mechanic. Identity intact." }
]
```
Both convert. One `param_gap` (auto-docket) + one `accepted_downgrade` (owner sign-off). The `param_gap` is the interesting one — it says "the transformation needs an arg the door doesn't yet carry," which is precisely the §2 param-gap intake.

**Per-skill geometry bands (§4) — 2 skills. THE CRITICAL D-2 TEST:**
```json
"skill_geometry_band": [
  { "skill_ordinal":0, "source_skill":"Cyclone (trigger host)", "delivery_class":"motion",
    "origin":"self", "range_band":"melee", "cadence_class":"channel", "count_per_cast":1,
    "motion_signature":"orbit_fixed", "band_conf":0.87, "derivation":"dossier-prose",
    "source_anchor":"channel-move spin whose ONLY job is to generate attack crits; deals no meaningful damage itself — it is the trigger engine's crank",
    "_role":"TRIGGER_HOST (deals no damage; crank only)" },
  { "skill_ordinal":1, "source_skill":"Ice Nova (triggered payload)", "delivery_class":"zone",
    "origin":"self", "range_band":"medium", "cadence_class":"cooldown",
    "count_multiplier_x":2, "count_multiplier_source":"door:ELEMENTAL_ECHO(parallel_triggers)",
    "motion_signature":"orbit_fixed", "band_conf":0.87, "derivation":"dossier-prose",
    "source_anchor":"nova expands from player position on each crit-trigger; multiple Novas per Cyclone revolution blanket a large zone",
    "_role":"TRIGGERED_PAYLOAD (the damage; the transformation targets THIS skill's row)" }
]
```
**The support gems (Cast-on-Crit, Cospri's) get NO skill row of their own.** They are correctly modeled as (a) the `ELEMENTAL_ECHO` door + its `trigger_condition`/`parallel_triggers` args, and (b) `trigger_grammar.proc_trigger_condition=on-crit`, all of which attach to the *payload skill's* geometry row (Ice Nova, `skill_ordinal:1`) via `count_multiplier_source`. **This is exactly what the per-skill grain predicts and the flat-single-`geometry{}` block could NOT express** — a flat block would have to choose ONE geometry for the kit and would collapse the host/payload distinction. See D-2 verdict (§5).

**Numerics (§5):** `cadence_scale=0.75` and the "14% CDR = 7.57 APS" breakpoint are timing tuning, not source-scale defense/damage numerics. Modeled as a door arg (`cadence_scale`) + a hook, not a `kit_numeric` row (there's no `%`-scale value to normalize). `kit_numeric` empty (honest). A second useful negative: trigger-kit "numerics" are cadence params, which belong on the door-arg surface, not the dual-column numeric surface.

**Recognition hooks (§6):**
```json
"recognition_hook": [
  {"hook_id":"H1","rank":1,"hook_type":"cadence","hook_text":"Cyclone crits machine-gun Ice Novas through the crit-trigger link","expressed_by":"door:ELEMENTAL_ECHO{trigger_condition,parallel_triggers}","provenance":"crawled","coverage_status":"expressed"},
  {"hook_id":"H2","rank":2,"hook_type":"cadence","hook_text":"attack-rate becomes cast-rate at the CDR breakpoint — the first power jump","expressed_by":"door:ELEMENTAL_ECHO{cadence_scale}","provenance":"crawled","coverage_status":"accepted_downgrade"},
  {"hook_id":"H3","rank":3,"hook_type":"geometry","hook_text":"overlapping cold rings blanket the screen","expressed_by":"door:GEOMETRY_COLLAPSE{collapse_mode}","provenance":"crawled","coverage_status":"expressed"},
  {"hook_id":"H4","rank":4,"hook_type":"register","hook_text":"cold/water register","expressed_by":"element:cold","provenance":"crawled","coverage_status":"expressed"}
]
```

**Acceptance + delta_t4 (§6):**
```json
"kit_acceptance_assert": [
  {"assert_text":"ice_nova_triggers_per_cyclone_revolution >= 3","hook_id":"H1","last_result":"green"},
  {"assert_text":"parallel_trigger_count == 2","hook_id":"H1","expected_state":"RED until ELEMENTAL_ECHO.parallel_triggers ships","last_result":"red"},
  {"assert_text":"cyclone_damage_share <= 0.05","hook_id":"H1","last_result":"green"}
],
"kit_delta_t4": {
  "shape":"step", "shape_signoff":"unvalidated",
  "asserts_json":["cadence_scale: uncompressed -> 0.75 at 14% CDR breakpoint (discrete jump)","ice_nova_effective_rate: sub-trigger -> one-per-server-tick"],
  "_pilot_note":"CoC delta_t4 is genuinely 'step' — the CDR BREAKPOINT is a discrete threshold crossing ('the first jump in power CoC builds get is at 14% CDR'). Contrast with the Trapsin ramp. The two PoE/D2 trigger-adjacent kits land on OPPOSITE shapes — good evidence the 2-value enum discriminates real structure."
}
```

---

### 3.4 — `gd-stun-jacks` (GD Stun Jacks · `transmuter` · empty-deviation edge case)

**Doors (§2):** `GEOMETRY_COLLAPSE`, `ELEMENT_CONVERSION_MONO`.
```json
"kit_door_arg": [
  { "door":"GEOMETRY_COLLAPSE", "arg":"collapse_mode",   "value":"shotgun_density", "derivation":"dossier-prose", "mutation_surface":"locked",
    "source_anchor":"point-blank shotgun-density identity; jacks spread in a 180-degree sector right before the player" },
  { "door":"GEOMETRY_COLLAPSE", "arg":"projectile_count","value":"variable",        "derivation":"dossier-prose", "mutation_surface":"mutable",
    "source_anchor":"Full Spread + '+1 projectile' scepter raise count" },
  { "door":"ELEMENT_CONVERSION_MONO", "arg":"target_element","value":"lightning",   "derivation":"dossier-prose", "mutation_surface":"locked",
    "source_anchor":"Light's Guardian as one of the best sets for lightning/electrocute damage" }
]
```
3/3 args from prose. `capstone_source_acquisition='transmuter'` (Quick Jack).

**Deviations (§3) — THE EMPTY-DEVIATION EDGE CASE.** `deviation_notes` is EMPTY for this kit.
```json
"kit_deviation": []
```
**G1 behavior when there's zero deviation prose: 0 rows in, 0 rows out — trivially lossless.** This is the correct, designed behavior (an EXACT-grade kit with no engine-inexpressibility has nothing to structure). It confirms the pipeline does not FABRICATE deviations to fill a quota — the no-fabrication law holds at the deviation layer. (The `negative_canon/UNSUPPORTED` verify_ledger row about "trap over-centralization" is explicitly annotation-only, NOT a mapping/deviation input — correctly excluded.)

**Per-skill geometry bands (§4) — 1 skill:**
```json
"skill_geometry_band": [
  { "skill_ordinal":0, "source_skill":"Stun Jacks", "delivery_class":"projectile",
    "origin":"self", "width_band":"wide", "range_band":"short", "speed_band":"fast",
    "pierce":"0", "chain":0, "fork":0, "count_per_cast":1, "count_multiplier_x":null,
    "cadence_class":"spam", "motion_signature":"fan_spread", "band_conf":0.85, "derivation":"dossier-prose",
    "source_anchor":"Stun Jacks spread in a 180-degree sector right before the player, with some jacks flying straight forward and some to the sides" }
]
```
Note `motion_signature:"fan_spread"` — a 180-degree radial fan is NOT one of the v0 seed paths {straight_line, spiral_out, orbit_fixed, sine, mortar_arc, wall_sweep}. Because `motion_signature` is a growable registry (v0 `motion_signature_registry`), this is a **registry-row addition, not a schema change** → **Amendment A-3** (add `fan_spread` to `motion_signature_registry`). `width_band:"wide"` for a 180-degree sector is legal (v0 enum has wide).

**Numerics (§5):** none on record (no `%`-scale value attested; the fidelity note explicitly flags the *absence* of a stun token — a negative, not a numeric). `kit_numeric` empty (honest).

**Recognition hooks (§6):**
```json
"recognition_hook": [
  {"hook_id":"H1","rank":1,"hook_type":"geometry","hook_text":"point-blank 180-degree jack spray — shotgun density","expressed_by":"door:GEOMETRY_COLLAPSE{collapse_mode}","provenance":"crawled","coverage_status":"expressed"},
  {"hook_id":"H2","rank":2,"hook_type":"cadence","hook_text":"energy-hungry spam is the throttle","expressed_by":"geometry.cadence_class","provenance":"crawled","coverage_status":"expressed"},
  {"hook_id":"H3","rank":3,"hook_type":"register","hook_text":"lightning/electrocute register","expressed_by":"door:ELEMENT_CONVERSION_MONO{target_element}","provenance":"crawled","coverage_status":"expressed"}
]
```

**Acceptance + delta_t4 (§6):**
```json
"kit_acceptance_assert": [
  {"assert_text":"projectile_spread_arc_deg >= 120","hook_id":"H1","last_result":"green"},
  {"assert_text":"cast_cadence == spam AND energy_gated == true","hook_id":"H2","last_result":"green"},
  {"assert_text":"stun_on_hit == true","hook_id":"H1","expected_state":"RED — name implies stun; NO stun token attested (§0.3 poster child); engine has no stun without CC","last_result":"red"}
],
"kit_delta_t4": {
  "shape":"step", "shape_signoff":"unvalidated",
  "asserts_json":["Quick Jack transmuter: cast-locked -> spammable (discrete enable)","projectile_count: base -> base + Full Spread + scepter +1"],
  "_pilot_note":"The transmuter (Quick Jack) is a discrete enable — spammability is on/off, so shape='step' is honest. capstone_source_acquisition='transmuter'."
}
```

---

## 4. GATE-BY-GATE EVIDENCE

### G1 — deviation prose → structured `kit_deviation` (threshold ≥90%) — **PASS (100%)**

| Kit | Deviation propositions in prose | Converted losslessly | Class breakdown |
|---|---|---|---|
| `d3-masquerade-spear` | 2 | 2 | 2× engine_inexpressible |
| `d2-trapsin` | 1 | 1 | 1× accepted_downgrade |
| `poe1-coc-ice-nova` | 2 | 2 | 1× param_gap, 1× accepted_downgrade |
| `gd-stun-jacks` | 0 (empty deviation_notes) | 0 | — (trivially lossless) |
| **Total** | **5** | **5** | **100%** |

Every distinct proposition in the deviation prose maps to exactly one `kit_deviation` row with a `deviation_class`, `hook_refs`, and `proposed_fix`. No prose proposition was dropped or merged lossily. All three class values {engine_inexpressible, param_gap, accepted_downgrade} are exercised across the pilot — the enum is complete for this set. The empty-deviation kit confirms zero-fabrication. **G1 PASS.**

### G2 — door args derivable from EXISTING prose, no re-crawl (threshold ≥80%) — **PASS (85%)**

| Kit | Door-arg instances | Derivable from prose | Re-crawl-flagged |
|---|---|---|---|
| `d3-masquerade-spear` | 7 | 6 | 1 (`DUAL_PROXY.sync_mode` exact timing) |
| `d2-trapsin` | 3 | 3 | 0 |
| `poe1-coc-ice-nova` | 4 | 4 | 0 |
| `gd-stun-jacks` | 3 | 3 | 0 |
| **Total** | **17** | **16** | **1** = **94% derivable** |

If we count *distinct arg surfaces that need a re-crawl* rather than instances: **2** flags total —
1. `DUAL_PROXY.sync_mode` exact simultaneity (1-frame vs 0-frame) — the *direction* is in prose ("mirror every cast"), but the *exact timing value* needs a datamine.
2. **The D2 `.txt` datamine `exact{}` lane (G-FIND-1)** — not an arg per se, but the brief's designated `exact{}` stress-test lane, which is **not on record**. Any `exact_json` population is a re-crawl dependency.

13 door-arg *instances* whose value the spec's exemplars would seed, 11 derivable → 85% by the strict brief-instance count; 94% by my full-instance count. Both clear the 80% threshold. **Every re-crawl-needing arg is flagged** (brief requirement met). **G2 PASS**, with the `exact{}`-lane-not-on-record finding attached as the one conditional flag the conductor should carry to W3.

### G3 — zero prose-only geometry on pilot T1 (primary skill) — **PASS**

| Kit | Primary skill (ordinal 0) | Prose-only geometry BEFORE | Structured AFTER |
|---|---|---|---|
| `d3-masquerade-spear` | Bone Spear | "narrow pierce projectile", "tripling projectile delivery" (both prose) | delivery/width/range/speed/pierce bands + `count_multiplier_x=3` w/ source |
| `d2-trapsin` | Lightning Sentry | "stationary placed emitter", "piercing bolts up to 10 times" (prose) | delivery/origin/range/pierce/cadence bands |
| `poe1-coc-ice-nova` | Cyclone (host) + Ice Nova (payload) | "channel-move spin", "nova expands from player" (prose) | 2 rows: motion host + zone payload, w/ `count_multiplier` on payload |
| `gd-stun-jacks` | Stun Jacks | "180-degree sector spray" (prose) | delivery/width/range/speed/cadence bands + `motion_signature=fan_spread` |

The critical prose-stranded fact the spec calls out — Masquerade's `count_multiplier` (triple volley) — is now a structured field with its causal source (`door:DUAL_PROXY`). After conversion, **no primary-skill geometry adjective remains only in prose**: each is either a band value or demoted to `source_anchor` (which is the *provenance*, not the *live* geometry — the live geometry is the band). **G3 PASS.**

### G4 — ≥1 red assert routes end-to-end to a docket via `intake_lane='deviation'`, `status='open'` — **PASS**

Each pilot kit has ≥1 red assert (Masquerade: `distinct_projectile_origins == 3`; Trapsin: `shadow_master_is_autonomous`; CoC: `parallel_trigger_count == 2`; Stun Jacks: `stun_on_hit`). The end-to-end route for the Masquerade red assert (spec's canonical example) to the NEW deviation-intake lane:

**The would-be `mechanic_gap_docket` row** (auto-opened by the `engine_inexpressible` deviation, NOT hand-authored):
```json
{
  "docket_id": "<next autoincrement, e.g. 20>",
  "mechanism_class": "multi-origin-synchronized-volley",
  "spec_text_or_path": "DUAL_PROXY delegates the mirrored cast but cannot address the 3 distinct spatial proxy origins; 'distinct_projectile_origins == 3' is RED until DUAL_PROXY.origin_model ships. Fix: door_param DUAL_PROXY.origin_model.",
  "evidence_kits": "[\"d3-masquerade-spear\"]",
  "destination": "engine-design-intake",
  "status": "open",                         // <- distinct from the 19 'matt-ratified' VDM-1 rows
  "source_deviation_id": "<the kit_deviation.deviation_id for the H1 engine_inexpressible row>",  // NEW col (DDL v0)
  "source_kit_id": "d3-masquerade-spear",   // NEW col (DDL v0)
  "intake_lane": "deviation",               // NEW col (DDL v0) -- the SECOND intake, distinct from 'mint'
  "provenance_json": "{\"auto_opened_by\":\"vdm2-deviation-intake\",\"hook_ref\":\"H1\",\"assert\":\"distinct_projectile_origins == 3\",\"red_test\":true}",
  "disposition": null,                      // triage happens at RESOLUTION, not open (spec §3)
  "created_date": "<utc>"
}
```

**End-to-end trace (on paper):** red assert `distinct_projectile_origins == 3` → its `hook_id=H1` → the `recognition_hook` H1 with `coverage_status='accepted_downgrade'` → the `kit_deviation` row (`engine_inexpressible`, `hook_refs=["H1"]`, `proposed_fix_target='DUAL_PROXY.origin_model'`) → the auto-wire opens the docket above with `intake_lane='deviation'`, `status='open'` → the deviation's `docket_id` back-fills to the new row. The `status='open'` + `intake_lane='deviation'` pair distinguishes it cleanly from all 19 matt-ratified mint-lane rows (verified: all 19 existing rows are `status='matt-ratified'`). **G4 PASS.** The DDL v0 `kit_deviation` CHECK (RULE-1: accepted_downgrade needs owner; RULE-2: docket linkage) supports this route with no amendment.

### G5 — no BREAKING schema change forced by the 3 non-D3 pilots — **PASS**

Every divergence the three non-D3 kits surfaced is **additive** (new enum value, new registry row, or new column). None invalidates a v0 statement, none touches an existing CHECK on VDM-1 data, none requires a table rebuild, none re-keys frozen data. The 7 amendments are listed in §6. The one path to a breaking change the migration plan §4.2 warned about — "per-skill geometry needs a *restructure* of `mapping_json` itself" — **did NOT materialize**: the per-skill grain reads cleanly from the *existing* `mapping_json.skills[]` array (which is already per-skill), so no restructure of the source is forced. **G5 PASS.**

---

## 5. D-2 GRAIN VERDICT — per-skill geometry survives the refutation surface

**Verdict: the `(kit_id, skill_ordinal)` per-skill grain HOLDS. The spec's flat single-`geometry{}`-per-kit block is refuted (correctly, as W0 predicted). ONE additive rider is needed.**

**The refutation test (D-2, pre-registered):** does support-gem geometry model better as **band-modifiers on a base skill's row** than as **its own skill row**? The CoC Ice Nova kit is the decisive case.

**Finding:** The support gems (Cast-on-Crit, Cospri's Malice) do **not** want their own skill row, AND they do **not** collapse into a single flat kit-geometry. They want to be **a door + trigger-primitive that attaches to the PAYLOAD skill's existing per-skill row.** Concretely:
- Cyclone (`skill_ordinal:0`) is the trigger HOST — a real skill with real geometry (motion/orbit), but zero damage. It gets its own row.
- Ice Nova (`skill_ordinal:1`) is the triggered PAYLOAD — the damage, the zone geometry. It gets its own row.
- The *support gems* are expressed as (a) the `ELEMENTAL_ECHO` door with `trigger_condition=on_crit`, `parallel_triggers=2`, `cadence_scale=0.75`; and (b) `count_multiplier_source='door:ELEMENTAL_ECHO(parallel_triggers)'` on the **payload row**. **They are modifiers-on-a-skill-row, carried via the door-arg + count_multiplier_source fields the per-skill table already has.**

**Why this VINDICATES the per-skill grain (not the flat block):**
1. A flat single-`geometry{}` block would have to pick ONE geometry for the kit. For CoC that is an impossible choice — the *motion* (Cyclone) and the *damage zone* (Ice Nova) are different delivery classes on different skills. The flat block collapses the host/payload distinction that IS the build's identity ("Cyclone is the crank, Ice Nova is the gun"). The per-skill grain preserves it.
2. The support-gem "skill" (Cast-on-Crit) has no geometry of its own — it is a *link relation* between two skills. Giving it a skill row would be a phantom row with all-NULL geometry. Modeling it as a door-arg + a `count_multiplier_source` pointer on the payload row is the correct normalization (tagged-not-encoded: the link is a tag on the payload, not a fabricated entity).
3. The GD Stun Jacks single-skill kit is the trivial confirming case: one skill, one row, transmuter as a `capstone_source_acquisition` + door-arg. No misfit.
4. The Trapsin 3-totem case confirms multi-skill kits need multiple rows (LS / Death Sentry / Shadow Master are three delivered geometries) — a flat block cannot hold three.

**The ONE additive rider (G5-class finding, NOT a failure — D-2 ruling explicitly said this is processable):**
The `ELEMENTAL_ECHO.parallel_triggers` arg (Cospri's second on-crit trigger) needs a home. It is a **door arg** (fits `door_arg_schema`/`kit_door_arg` with no schema change) — BUT to keep it queryable as "this payload is fired by N parallel triggers" without re-parsing prose, the per-skill `skill_geometry_band` benefits from the existing `count_multiplier_source` carrying the door reference, which it already does. **So the parallel-trigger case is expressible with ZERO structural change** — it rides the existing `count_multiplier_x` + `count_multiplier_source` columns. The only *registry* addition is declaring `parallel_triggers` as a legal arg of `ELEMENTAL_ECHO` in `door_arg_schema` (a data row, not DDL). **Net: D-2 grain holds; the support-gem refutation surface is expressed additively; no breaking change; the flat-block spec shape is refuted as W0 predicted.**

---

## 6. DDL AMENDMENT LIST (all ADDITIVE — G5 clean)

None of these is breaking. Each is a new enum value on a *new* (v0-introduced, not-yet-applied) table's CHECK, a new registry row, or a new column. Because DDL v0 is **not yet applied**, these fold into v0 before the W3 apply — they are edits to the draft, not migrations-on-migrations.

| # | Amendment | Target | Kind | Driven by |
|---|---|---|---|---|
| **A-1** | Add `self` to `range_band` CHECK enum | `skill_geometry_band.range_band` | enum-value add | Masquerade Simulacrum + several summon/self skills have `range_band=self` (self-buff/summon delivery). v0 enum {melee,short,medium,long,screen} lacks it. |
| **A-2** | Declare `parallel_triggers` (int) + `trigger_condition` (enum) + `cadence_scale` (pct/real) as legal args of trigger-family doors (`ELEMENTAL_ECHO`, etc.) | `door_arg_schema` DATA rows (not DDL) | registry row(s) | CoC Ice Nova (D-2). Note: `cadence_scale` is a real 0..1, so `arg_type` needs to admit it — see A-4. |
| **A-3** | Add `fan_spread` (180-deg radial) to the motion registry | `motion_signature_registry` DATA row | registry row | GD Stun Jacks 180-degree sector. (Registry is growable by design — this is the intended path.) |
| **A-4** | Add `real` (or `float`) to `door_arg_schema.arg_type` CHECK enum | `door_arg_schema.arg_type` | enum-value add | `cadence_scale=0.75` is a real fraction; v0 arg_type enum {enum,int,ref,bool,list,duration_s,pct} has `pct` but 0.75 is a raw fraction not a percent. Add `real`. |
| **A-5** | Add `at_target` and `self_and_proxies` as documented legal `origin` values (note-level; `origin` is free-TEXT so no CHECK change) | `skill_geometry_band.origin` (doc only) | doc note | Trapsin `at_target`, Masquerade `self_and_proxies`. `origin` is free TEXT in v0 (no enum) — this is a documentation amendment to the column comment, zero DDL change. Recorded so the W4 emitter uses a controlled origin vocabulary. |
| **A-6** | Reconcile `corpus_class` system-record tally: live `is_system=1` count is **19** (across 11 games; 3 inside record-games), not 11 | `canon_corpus.corpus_class` rider (W3) + D-4 ruling arithmetic | data-count correction (no DDL change) | §2 correction. The enum already admits `system` (D-4 ruled). Only the expected row-count in the W3 rider + the D-4 ruling's "585 = 270+304+11" arithmetic needs updating to reflect 19 system-records. |
| **A-7** | Preserve NULL `t4_doors` as meaningful (do NOT coerce the 8 NULL-door D2 kits to empty-array or strip) | W3 door-strip rider behavior (not DDL) | rider-behavior note | §7. The 8 NULL-door kits correlate with GAPPED/MAPPED_DOCKET status — NULL is a signal, not an artifact. |

**A-1 and A-4 are the only two that touch a CHECK constraint** — and both are on tables *introduced by v0 itself* (`skill_geometry_band`, `door_arg_schema`), which do not yet exist in corpus.db. So they are draft edits, incur **no** SQLite CHECK-rebuild penalty, and touch **no** VDM-1 data. A-2/A-3/A-5 are registry/data/doc. A-6/A-7 are rider-behavior. **Zero breaking. G5 clean.**

---

## 7. EMPTY-STRING-DOOR CHARACTERIZATION (D-1 ruling: characterize artifact vs meaningful)

**W0 said "8 empty-string door slots." The pilot corrects this: they are 8 kits whose `t4_doors` array is NULL entirely (not empty-string slots inside an array).** All 8 are D2 kits. Characterization:

| kit_id | grade | terminal_state | tier | n_skills | Artifact or Meaningful? |
|---|---|---|---|---|---|
| `d2-wl-void-rift` | GAPPED | MAPPED_DOCKET | T1 | 0 | **ARTIFACT (phantom):** "probable spec-error / phantom kit; no attested mechanics, identity, or skills." The one true cleanup candidate. |
| `d2-summonmancer` | GAPPED | MAPPED_DOCKET | T1 | 4 | **MEANINGFUL:** kill→corpse→raise loop is "the engine's most common" — un-doored because it's the docketed summoner-GAP, not because data is missing. |
| `d2-grim-ward-barb` | GAPPED | MAPPED_DOCKET | T1 | 2 | **MEANINGFUL:** "named archetype is unattested; kit identity is partial-recovery." Honest low-confidence, not artifact. |
| `d2-horker` | GAPPED | MAPPED_DOCKET | T1 | 3 | **MEANINGFUL:** defining loop is Find-Item loot-economy corpse re-rolls — no combat T4 door is *correct* (it's a farming build). |
| `d2-summon-druid` | GAPPED | MAPPED_DOCKET | T1 | 4 | **MEANINGFUL:** autonomous-pet menagerie = summoner-GAP; un-doored by the same docket. |
| `d2-teleport-sorc` | GAPPED | MAPPED_DOCKET | (null) | 1 | **MEANINGFUL:** "identity is metagame transport service; any combat mapping would be fabrication." NULL door is the no-fabrication law working. |
| `d2-sacrifice` | GAPPED | MAPPED_DOCKET | (null) | 1 | **MEANINGFUL:** self-damage-on-hit "has no engine lane as a build identity." Honest gap. |
| `d2-impale-zon` | APPROX | MAPPED | T1 | 1 | **MEANINGFUL:** identity is a durability-drain penalty; no transformative door exists to assign. The only non-GAPPED of the 8. |

**Verdict:** 7 of 8 are MEANINGFUL (NULL `t4_doors` is a deliberate no-door signal, correlated with GAPPED/MAPPED_DOCKET status — the source did not attest a mappable transformative loop, so no door was fabricated). Only 1 (`d2-wl-void-rift`) is a true ARTIFACT/phantom. **W3-rider consequence (Amendment A-7):** the door-strip rider must NOT coerce these NULLs to empty-arrays or treat them as dirty. It should preserve NULL as the honest "no T4 door attested" state. The single phantom (`d2-wl-void-rift`) is a separate cleanup item — a candidate for the phantom-kit disposition, NOT a door-hygiene fix. **Raws preserved either way** (D-1: raws preserved; the W3 rider strips nothing structural).

---

## 8. WHAT (IF ANYTHING) SHOULD HALT THE W3 APPLY

**Nothing halts W3.** All five gates PASS; D-2 holds additively. The apply can proceed on the v0 DDL + the 7 amendments folded in. Two inputs the conductor should carry into W3 (both non-blocking, both already handled in the amendment list):

1. **`exact{}` datamine lane is not on record (G-FIND-1).** Keep `exact_json`/`exact_source_type` NULL at apply. Genuine `exact{}` population is a downstream Legolas Mode-B `.txt`/DBR datamine acquisition — a W4+ re-crawl dependency, not a W3 schema blocker. The column lands empty and honest (spec §4: exact never blocks a kit).
2. **The 8 NULL-`t4_doors` kits are meaningful (A-7).** The W3 door-strip rider must preserve NULL. If the rider was going to blanket-coerce door arrays, that coercion must be gated to skip the GAPPED/MAPPED_DOCKET kits. One phantom (`d2-wl-void-rift`) is a separate disposition item.

Two things the conductor may want to route (neither blocks W3, both are W3/W4 population-time questions):
- **D-4 arithmetic reconciliation (A-6):** live `is_system=1` = 19, not 11. The `system` enum is fine; the tallies in the D-4 ruling need a one-line update. Data-count only.
- **`accepted_downgrade` owner-sign-off routing:** the pilot supplied `downgrade_owner='elrond (pilot)'` for the Trapsin/CoC downgrades to satisfy the CHECK, but whether the data-steward or a *design* owner (Gandalf/Matt) is the correct sign-off for an `accepted_downgrade` is a W4 process question. The CHECK fires correctly regardless; only the *identity* of the signer is open. Flag for the conductor.

---

## 9. HYGIENE + CLOSE

- **corpus.db UNTOUCHED.** md5 `50df15b776ad5b0da93fe90cdee1163d` at open, mid-work, and close (verified). DDL NOT applied, not even locally. All inspection was read-only (`mode=ro` URI).
- **Namespace discipline:** touched only `agentic_orchestration/elrond/` (this report). Did NOT touch `wave-b-reservation-aura` or `agentic_orchestration/knight-rider/` (parallel KR session owns those).
- **Auto-commit** this report (elrond seam, authorized cycle work). **NO PUSH** (conductor centralizes pushes for this run).
- **Conductor rulings D-1..D-6 all honored:** D-1 (kept `_suffix` doors distinct; characterized empty/NULL slots; W3 strips raws-preserved) · D-2 (per-skill grain as hypothesis, refutation-tested, HOLDS + additive rider) · D-3 (all `rdr_value` honest-NULL; authored zero balance transforms) · D-4 (`system` enum; A-6 flags the 19-vs-11 count) · D-5 (court mapping unblocked — not exercised this pilot, no court data written) · D-6 (`eras_normalized` per-game canonical — not exercised this pilot).

**Signed:** elrond (data steward) · Wave W2 · note-space conversion + gate evaluation only · corpus.db UNTOUCHED · local auto-commit, **no push**.
