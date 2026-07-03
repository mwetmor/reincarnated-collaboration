# Glyph-spec §5 gate — PRE-RUN over the true W3 batch-1 bundle (findings + re-cut basis)

> **STATUS:** FINDINGS NOTE (2026-07-03) — §5 validation gate executed by gandalf against the TRUE 700-kit bundle (canonical run_id `cbeb9471`, bundle `src/reincarnated/output/w3_batch1_bundle.json` @ engine `2839caf`). Result: **v0 → v1.1 re-cut fired** per the spec's own §5 re-cut law. Spec bumped in the same commit.
> **Author:** gandalf (SPEC-AUTHOR → ⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC for F2, judging my own v0)
> **Why pre-run:** W4 has not fired; the paste-block assigns "glyph coverage per §5" to the W4 gandalf invocation. Pre-running found the check as-specced was **not computable** — better caught now than mid-audit.

---

## F1 — Export vocabulary mismatch: 19/31 kit-envelope fields None on all 700 kits (star-lord seam)

The bundle's kit records carry full SUBSTANCE (12 skills each, chains, gear_representative, t4_candidates, bc_target_cell post-v1.90) but a hollow ENVELOPE: `name`, `archetype_tag`, `role_orientation`, `range_profile`, `energy_type`, `dominant_element`, `color_palette`, `stat_distribution`, `movement_speed`, `primary_t4`, `balance_metadata`, `engine_version`, `final_compliance_status`, `source_library`, `seasonal_dominant_element`, `parent_faction_*`, `title_completion`, `t4_alteration_output`, `ai_tell_compliance_score` = None ×700.

**Root cause — same class as the v1.90 bc_target_cell defect, times nineteen:** `KitCandidate.to_character_dict()` (season_generation_pipeline.py:412) emits the data under the W5R vocabulary (`element`, `resource_model`, `cohort_archetype`, `bc_tuple.*`); `build_kit_record()`'s passthrough (one_realm_bundle_assembler.py:283) reads the cycle13-exporter vocabulary (`dominant_element`, `energy_type`, `archetype_tag`, `range_profile`…). Vocabulary mismatch at the driver↔assembler seam — **data exists, names don't line up.**

**Fix spec (star-lord; extend the proven v1.90 bridge in the Step-4 loop, `--recover-from-canonical` regen ~10s, NO gauntlet re-run):**

| Bundle field | Bridge from | Note |
|---|---|---|
| `dominant_element` | char_dict `element` | glyph tint pip — **glyph-load-bearing** |
| `energy_type` | char_dict `resource_model` | **adopt doc-48 vocabulary** (mana / rage / combo / stamina-as-resource / charge-stack) — the cycle13 enum is the stale one; glyph spec §2 updated to match |
| `archetype_tag` | catalog `archetype_name` (encounter) | NAME channel only, per the BC-cutover — never glyph input |
| `range_profile` | `bc_tuple.range` | legacy-compat only; v1.1 derivation reads bc coordinates directly |
| remainder | star-lord triage | which are demo-bundle-load-bearing vs cycle13-legacy is his call; `name`/`flavor_text`/`title_completion` stay None BY RULING (flavor parked resumable) |

## F2 — Axis-existence failure: `role_orientation` is not a coordinate of this population (my v0 miss)

`KitCandidate` has **no role_orientation field**; the gauntlet router hard-codes `role_orientation="damage"` for all 18 archetypes (season_generation_pipeline.py:1557 — "endgame baseline; all 18 kit archetypes are DPS-primary"). My §2 claimed inputs "verified against `export/cycle13_normal_season_export.py`" — **I verified against the retired exporter, not the population's actual coordinate system.** Framing-audit Q2 failure, caught by the gate itself. The population's real coordinates: `bc_tuple` (range × tempo × amplitude × attribute × proxy_density) + `element` + `resource_model` + uniform-template skills.

**Consequence:** v0 rules 2–5 read a phantom axis. Re-cut fired: v1.1 derives from **bc_target_cell coordinates** — which is MORE faithful to the spec's own §1 law (glyphs read the engine's own coordinates; the BC tuple IS the engine's coordinate system post-cutover). New §5 check-0 added: **axis-existence** — verify each derivation input is a live, varying coordinate of the population before evaluating boundaries.

## F3 — Population narrowness: the caster wipeout + the uniform role template

1. **700 survivors = 7 whole cells × 100** (cell-level verdicts). Catalog fielded 18 cells: STR 4, DEX 4, INT 5 (incl. the one proxy-`light` cell), WIS 5.
2. **All 10 caster-attribute cells (INT + WIS) FAILED the gauntlet. Zero casters survive.** Plus one melee-DEX cell. The "11 failed cells" autopsy item is therefore not scattered noise — it is a **systematic caster wipeout** (echoes the W2 caster-alone WR 0.000 evidence; likely structural classification, but that's the W4 autopsy's call, not pre-judged here).
3. **Every kit has the identical skill-role composition: 4 single-target / 4 AoE / 2 control / 2 support** (zero variance across 700). Role variety is composed INSIDE every kit, not ACROSS kits — so no loading-based CONTROLLER/WARDEN discrimination exists in batch-1 either.

**Batch-1 is therefore a 2-glyph population by construction:** BRUISER (melee, 300, 42.9%) + GLASS CANNON (mid/ranged, 400, 57.1%), with variety carried by pips (range 3-way live now; element 6-way once F1 bridges) + tempo/amplitude texture. CONTROLLER/WARDEN capture 0 honestly (no role-varied kits emitted); SUMMONER captures 0 **by adjudicated ruling** (Phase-A proxy-emission refutation). All five Matt-confirmed names stay in the vocabulary — the three unpopulated ones live exactly where the spec designed them to: **grimoire hook-honesty pages for archetypes this run never spawned** (spec §0/§6, one-realm §20a/§20c).

## §5 verdict (batch-1)

| Check | Result |
|---|---|
| **0. Axis-existence (NEW)** | v0 FAIL (role_orientation phantom) → re-cut to BC coordinates; v1.1 PASS |
| **1. Coverage (total function)** | v1.1 PASS — 700/700 map to exactly one glyph, no fall-through (computable from bc_target_cell alone, today) |
| **2. Discrimination** | Re-scoped: measured against the **emitted design span**, not the full vocabulary (with 3 of 5 glyph-populations structurally absent, the "no glyph >40%" ceiling is arithmetically void — 2 live glyphs must average 50%). Within-span: 42.9/57.1 split is healthy. Full-vocabulary discrimination re-tests when a role-varied + proxy-viable population emits |
| **3. Cluster fidelity spot-check** | LIGHT-PASS executed (post-W4-close reconciliation): **range promise VERIFIED** — BRUISER skill `range_m` median 3.0m (max 8), GLASS CANNON median 10.0m (max 12); clean band separation. **"Glass" (fragility) + "cannon" (outsized hit) texture UNVERIFIABLE** — `damage_multiplier` identical across glyphs (mean 1.01 both) and `stat_distribution`/`balance_metadata` are F1-None. Until the F1 bridge lands, GLASS CANNON is honestly a RANGED glyph; the glyph-ART brief (§7, drax/galadriel) should not promise fragility iconography the data can't yet back. Full qualitative tree-read rides the roster-pick session on the finalists, where it has curation value |

## Open fork for Matt (rides the caster-wipeout autopsy — no action now)

The demo's Goldilocks roster span (one-realm §3: melee / caster / ranged / controller / summoner) is **not coverable from batch-1 survivors** — no casters, no summoners, no role-varied kits. Fork at the G7a roster session: (a) demo roster from STR/DEX melee/ranged only, scouting ships 2 glyphs + pips, grimoire carries the other three as hooks — honest and shippable; (b) role-varied/caster-fixed batch-2 emission before the roster pick. Genre note: D2's demo-era classes shipped narrow and honest (five classes, two ranged) rather than wide and hollow; the counter-pull is that the Goldilocks scouting read is the demo's teaching moment for the whole vocabulary. **Matt rules at G7a; the autopsy's failure-mode classification is the evidence that gates it.**

## Routing

- **Spec v1.1** — same commit (this note is the evidence record; the spec is the law).
- **star-lord** — F1 bridge fix rides the existing post-run `identity_glyph` stamp beat (spec §6); KR sequences after W4.
- **W4 gandalf invocation** — "glyph coverage per §5" line-item now reads "per §5 v1.1"; coverage/discrimination are pre-answered above; the invocation's remaining glyph beat is the fidelity spot-check.
- **W4 autopsy item** — headline upgraded per F3.2; classification stays with the assigned owners.

**Sign-off:** gandalf, 2026-07-03. Anchors: scouting-glyph spec v1.1 §4/§5 · engine 2839caf (v1.90 bridge precedent) · season_generation_pipeline.py:412/:1557 · one_realm_bundle_assembler.py:283 · endgame_encounter_catalog.py (18-cell roster) · Phase-A refutation adjudication (85bf46c).
