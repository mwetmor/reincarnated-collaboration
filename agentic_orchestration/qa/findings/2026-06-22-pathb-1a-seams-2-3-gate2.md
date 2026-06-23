# Finding — 2026-06-22 — Path B Step 1a seams 2 (gamora) + 3 (star-lord) Gate-2

**Reviewer:** jack-ryan (DEV-MODE, Gate-2, BLOCK authority)
**Targets:** `bae3bf1` tag `gamora/v-pathb-1a-sim-consumption` · `3320403`+`86dcadb` tag `star-lord/v-pathb-1a-telemetry-export`
**Developers:** gamora (seam 2), star-lord (seam 3)
**Upstream (context only, not under review):** rocket `14ee022` — schema widening, already Gate-2 PASS-WITH-INFO (`e2413ef`)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact), 6 (cross-seam round-trip / MIGRATION), 5 (severity); Disciplines #1, #2, #11, #12
**Holds checked:** structural-only (no 1b mint / no 1c calibration / no balance-signal regen), intermediate tags only, compat-shim non-permanence — ALL respected.

---

## SEAM 2 (gamora) — VERDICT: PASS

### What I found
Two pinpoint consumer fixes, both matching her math note byte-for-byte. `spirit_guide._displaced_value` (switch `:251-270`, new `_DISPLACED_SLOT_FIELD` map `:114-130`) replaces the legacy 4-string switch with a normalization map built FROM `gear_schema.EQUIPPED_SLOTS` (verified — not re-hardcoded; the equipped half is `**{name: name for name in EQUIPPED_SLOTS}`, the legacy half mirrors `gear_schema._LEGACY_FIELD_MAP`). She removed the `loadout.weapon/.armor/.accessory` shim reads, reading canonical fields via `getattr(loadout, field)`. `combatant.py:889` widened to `_carried.get("main_hand") or _carried.get("weapon") or _carried.get("main_weapon")` (ordering correct: current serialize path first, legacy tolerance, substrate path last). G-SOLO byte-identity re-asserted structurally through `combined_stats()`+`total_power_score()`.

### THE LOAD-BEARING INTERPRETATION QUESTION — her reading is CORRECT
I verified this first-hand, not on her say-so:
- `_displaced_value` switches on `candidate.slot`. I grepped `gear_generation.py:75 _BASE_TYPE_TO_SLOT` and confirmed every base-type maps to EXACTLY one of `{weapon, armor, accessory, off_hand}` (`grep -oE` over the whole table returns only those 4 distinct values). No gear today carries a `.slot` of `main_hand`/`chest`/`amulet`/`head`/`belt`/`ring_*`/`hands`/`feet`. So a literal `candidate.slot == "main_hand"` switch would NEVER fire today — confirming the "6-of-10 silently mis-valued" bug is **forward-looking**, biting only when 1b mints gear destined for the 6 new slots.
- **Present-tense byte-identity (no masked bug):** pre-1a `loadout.weapon` is now a shim `@property` returning `self.main_hand` (verified `gear_schema.py:297-307`: weapon→main_hand, armor→chest, accessory→amulet). Her code reads `loadout.main_hand`/`chest`/`amulet` directly. Same objects. The 4 legacy candidate slots resolve to the identical displaced item pre- and post-change; the 6 new slots were `return 0.0` before (default branch) and resolve now — but no candidate carries those names today, so today's behavior is unchanged. Her normalization is sound and masks NOTHING; it is purely forward-extending, exactly as her Discipline #12 note declares.
- Bonus correctness: she preserves the `GearInstance.slot` value `"weapon"` even though the Loadout FIELD is `main_hand` — the two-taxonomy split is internally consistent with star-lord's test assertion `result["main_hand"]["slot"] == "weapon"`.

### Smokes (load-bearing ones spot-run by me, not trusted from the commit msg)
- Her smoke `pathb_1a_sim_consumption_smoke_2026_06_22.py`: **35/35 PASS** (ran it). Includes all-10-slot resolution, legacy-4 resolution, genuinely-unknown→0.0, G-SOLO byte-identity, weapon-key precedence.
- `tests/test_spirit_guide.py`: **44/44 PASS** (ran it).
- Broad batch (`-k loadout/gear/spirit/combatant/canonical`): 1037 passed; the one failure (`test_foundation.py::...rotating_elements_are_canonical_substrates`) is PRE-EXISTING — fails identically at rocket's `14ee022` (verified via checkout); element-config drift, unrelated to loadout/sim.

### Rationale
Principle 1 (math note precedes + grounds the change), Principle 2 (smoke before any regen), Discipline #11 (she inspected the two taxonomies empirically rather than trusting the dispatch's literal wording) and #12 (semantic-shift declared and justified). Compat-shim hold respected: she removed spirit_guide's dependency on `.weapon/.armor/.accessory` and correctly did NOT delete the shims (rocket's file, other readers remain) — flagged for 1c. No new cross-seam contract → Principle 6 round-trip N/A (correctly declared).

### Action
- [x] Developer (gamora): nothing required. Clean.

---

## SEAM 3 (star-lord) — VERDICT: PASS

### What I found
Zero production code change; the widening lands in test updates + a new round-trip smoke + the export-side MIGRATION section. His core claim — that the export surface is already opaque-TEXT pass-through with no path destructuring the 4 keys — is **verified first-hand**:
- Grepped every `loadout_json` producer/consumer (`--include='*.py'`). Producers: `balance_loop.py` via `serialize_loadout(loadout)` (opaque string). Storage: `recorder.py:record_class_fight_loadouts()` stores it as TEXT, never parses slot keys. The ONLY `json.loads` of a loadout in production is `canonical_loadout.py:78` `return json.loads(best["loadout_json"])` — it returns the dict WHOLE; it does not index `["weapon"]`/`["main_hand"]`/any slot key. No caller of `select_canonical_loadout` destructures the 4 keys (verified the call-sites).
- The only per-slot computation, `legendary_count`, is `count_legendary(loadout)` operating on the `Loadout` OBJECT (rocket-owned, already widened), NOT on JSON keys. So no production export path breaks on the 4→10 key shift.
- `season_exporter._load_db_class_data` + `schemas.ExportClass.carried_gear` (`dict[str, Any] | None`) pass through opaquely — confirmed unchanged in the diff.

### Round-trip smoke (ran it: 18/18 PASS) — both load-bearing arms genuinely exercised
- **RT-1 (12 checks):** real production write path — `Loadout` → `serialize_loadout()` → `record_class_fight_loadouts()` → DB read-back; all 10 EQUIPPED_SLOTS keys present, `main_hand` id matches, 6 empties → null, `legendary_count=1`. This is a production fixture, not a hand-rolled dict (dispatch requirement met).
- **RT-2 (6 checks):** genuine brownfield — a historical 4-key row (`weapon/off_hand/armor/accessory`) persisted as opaque TEXT and `json.loads`-parsed WITHOUT error, 4 keys intact. This genuinely exercises parse-tolerance (the load-bearing acceptance item), not a stub.

### Other acceptance items (all verified)
- `tests/test_canonical_loadouts.py`: **29/29 PASS** (ran it). The 8 he updated correctly migrate `weapon/armor/accessory` assertions → `main_hand/chest/amulet` + `set(keys)==set(EQUIPPED_SLOTS)`, and correctly preserve `GearInstance.slot == "weapon"` (the value, distinct from the field key).
- **No DB migration is correct:** `migrations.py` untouched; `loadout_json TEXT NOT NULL` is opaque TEXT, shape lives in-JSON. No `.sql`/DDL added in either commit. Verified.
- MIGRATION co-author section present (`### star-lord seam 3` at `MIGRATION.md:56`), thorough, carries the drax seam-4 forward note.
- Pre-existing failure `test_cycle12_layer4_convergence.py::...test_dataclass_fields_exist`: genuinely unrelated — fails in `skill_tree.py:422 NotImplementedError` (retired `SkillTreeGenerator.generate()`); nothing to do with loadout/export. Not chased.

### Rationale
Principle 6 (cross-seam contract on the export side → MIGRATION section required + round-trip smoke; both present). Principle 2 (smoke before regen). Discipline #11 (empirical confirmation that the surface is opaque rather than assuming). Brownfield holds respected: additive, historical 4-key rows still parse.

### Action
- [x] Developer (star-lord): nothing required. Clean.

---

## Ownership-handoff cleanliness (gamora ↔ star-lord) — CLEAN
- gamora committed 5 files via `--only` and did NOT touch `tests/test_canonical_loadouts.py` (verified: `git show --stat bae3bf1` has no canonical_loadout entry).
- star-lord fixed the 8 broken `test_canonical_loadouts.py` tests in `3320403`.
- No double-edit conflict, no orphaned breakage: the file is owned by exactly one seam (star-lord), and the test currently passes 29/29. The two seams are internally consistent on the load-bearing two-taxonomy detail (field key `main_hand` vs `GearInstance.slot` value `weapon`). Handoff is clean.

## INFO carried forward to 1b / 1c
- **(1c) Compat-shim deletion gate:** rocket's `.weapon/.armor/.accessory` `@property` shims on `gear_schema.Loadout` are now unread by spirit_guide (seam 2 removed that dependency). Remaining readers to migrate before deletion: any test helpers still using legacy attribute access, and drax seam-4 once it widens. gamora's flag stands — shims must not outlive 1c. jack-ryan to track at 1c open.
- **(1b) Forward-correctness now in place:** `_displaced_value`'s 6-new-slot valuation is live but dormant — it only activates when 1b mints gear carrying an equipped-slot id (or carrying one of the legacy high-level names destined for a new slot). 1b's Gate-2 should include a smoke that mints a `head`/`belt`/`ring_*` candidate and asserts `_displaced_value` returns non-zero (the first real exercise of gamora's forward path).
- **(1b/1c) DB shape is in-JSON, not in-schema:** no column carries slot structure. Any 1b/1c analysis querying per-slot resist must `json.loads(loadout_json)` and tolerate BOTH 4-key (historical) and 10-key (post-1a) shapes — RT-2 is the canonical brownfield-parse pattern to reuse.
- **(reminder) Post-1a win-rates are NOT a balance signal (CONCERN-3).** Neither seam ran a season for signal; correct. 1c is where calibration re-opens.

## References
- `src/reincarnated/spirit_guide/spirit_guide.py` (`:114-130`, `:251-270`)
- `src/reincarnated/simulation/combatant.py:889`
- `src/reincarnated/generation/gear_schema.py` (`EQUIPPED_SLOTS:206`, `_LEGACY_FIELD_MAP:215`, shims `:297-307`)
- `src/reincarnated/generation/gear_generation.py:75` (`_BASE_TYPE_TO_SLOT`)
- `src/reincarnated/generation/canonical_loadout.py:32,78` (`count_legendary`, opaque `json.loads`)
- `src/reincarnated/simulation/notes/pathb_1a_sim_consumption_smoke_2026_06_22.py` (35/35)
- `src/reincarnated/export/pathb_1a_telemetry_roundtrip_smoke_2026_06_22.py` (18/18)
- `tests/test_spirit_guide.py` (44/44), `tests/test_canonical_loadouts.py` (29/29)
- `src/reincarnated/generation/MIGRATION.md:56` (star-lord seam-3 section)
- Math note: `src/reincarnated/simulation/math/pathb-1a-sim-consumption-2026-06-22.md`
