# Dispatch — 2026-05-27 — legolas + elrond — Cycle 14 substrate enrichment bundle (INT-AoE + Monk + Hybrid)

**From:** knight-rider
**To:** legolas (Mode B catalogue crawl per sub-fix); elrond (curation per sub-fix)
**Approved by:** Matt 2026-05-27 verbatim "slight cycle 14 scope creep but not insurmountable" + Option α architectural pivot (substrate-led discipline: enrich substrate BEFORE clustering fires so emergent classes against enriched data are produced from the start)
**Estimated effort:** Sub-Fix 1 (INT-AoE) ~1-2 weeks; Sub-Fix 2 (Monk) ~1-2 weeks; Sub-Fix 3 (Hybrid) ~1-2 weeks; **PARALLEL** with math-note authoring + each other
**Acceptance:** ~1,500-3,000 additional substrate rows landed in v1_scope; per-sub-fix completion records; Option α clustering algorithm operates on enriched substrate at Stage 3 re-impl time

## Context

Matt 2026-05-27 ratified Option α architectural pivot (substrate-clustered emergent classes; no pre-authored fixed class taxonomy). Per scaffold-drift consolidated package § 3.2 (BC-axis gaps surfaced by elrond Stage 1 audit at `06a3b7f`):

- **INT-AoE near-empty** — canonical fireball/chain-lightning/blizzard mage substrate ABSENT (6 thin rows)
- **WIS-melee-light (monk)** — 0 rows (no unarmed / martial-arts / monk-staff substrate)
- **Cross-attribute hybrid** — substrate-thin (spellblades / magus-arcane-blades / runeblades absent)

Per Option α + substrate-led discipline (Discipline #25 + Path A architectural commitment), enrich substrate FIRST so emergent classes against the enriched data naturally include fireball-mage + monk + spellsword at Wave 5 production season generation. This avoids designing emergent classes against an empty substrate cell.

**Per kicker § 3.6:** 3 dispatches; bundled as ONE per KR routing (same legolas Mode B + elrond curation pattern; parallel sub-fix execution similar to substrate sidecar Fix A+B+C model).

**Pre-Wave-5 composition:** substrate enrichment provides ~1,500-3,000 additional substrate rows; math notes specify clustering algorithms that operate on whichever substrate population exists at fire-time. Both tracks must complete before Stage 3 re-implementation fires.

**EXCLUDED per Matt 2026-05-27 triage:**
- Multi-spawn summoner — separate engine subsystem work per `project_pet_system` memory (~4-6 weeks focused sprint); substrate enrichment alone insufficient
- DEX rebalancing — RESOLVES NATURALLY when INT + WIS substrate enriched (DEX's 47% proportion drops to ~35-38% as side-effect)
- Skirmisher shield-family expansion — OPTIONAL (gandalf-leaning-defer; substrate-thin clusters of 17 shields can still emerge as legitimate-but-small class; revisit per Wave 5 evidence)

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle (post Option α pivot)
- `agentic_orchestration/gandalf/notes/2026-05-27-option-alpha-kr-revert-kicker.md` § 3.6 (substrate enrichment substantive spec)
- `agentic_orchestration/gandalf/notes/2026-05-27-option-alpha-pivot-and-math-note-inventory.md` (Option α architectural context)
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 3.2 (BC-axis gaps surfaced empirically)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-wave-1-5-class-roster-substrate-audit.md` (Stage 1 audit — gap evidence)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` (substrate composition reference)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 (per-attribute weapon profile — enrichment respects)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (Option α / β / C cell-type matching; Hybrid sub-fix composes with Option C cross-attribute ω-penalty)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` Discipline #20 (robots.txt + Claude-agent directive respect — applies to legolas Mode B crawls)
- `.claude/skills/reincarnated-legolas-operating-procedure` (Mode B catalogue-crawl protocol)
- `.claude/skills/reincarnated-elrond-operating-procedure` (curation + DB enrichment)
- `.claude/skills/reincarnated-hive-mind-protocol`
- Substrate library DB: `~/Games/reincarnated-loadout/data/telemetry.db` (`weapon_knowledge_entries` + `weapon_sim_props` per SC-6 audit § 1.1)

## Math-before-code

Not applicable — substrate enrichment is data-acquisition work, not algorithmic. Composition policy v1 (Option α/β/C) provides existing constraints; enriched rows respect composition gates per `weapon-substrate-composition-policy-v1-2026-05-24.md`.

## Cross-seam contract change? (Principle 6 gate)

**POSSIBLY** — enrichment adds rows to existing `weapon_knowledge_entries` + `weapon_sim_props` schema; no NEW columns (per SC-6b enrichment already landed columns are sufficient). If schema extension needed for INT-AoE-specific or monk-specific stats, route via elrond + KR for separate dispatch.

**MIGRATION.md** per ADR-004 at `agentic_orchestration/elrond/research/substrate-enrichment-2026-05-27/MIGRATION.md` (or elrond-OP-preferred location) capturing per sub-fix:
- Rows added (count + source attribution)
- v1_scope flag updates
- weapon_type_family classifications applied
- weapon_kind classifications applied
- Cross-seam round-trip clause: rocket Stage 3 re-impl substrate clustering at Math Note 1 fires consumes enriched rows; emergent classes include fireball-mage + monk + spellsword if substrate votes for them

## Scope

### Sub-Fix 1 — Substrate INT-AoE enrichment (~1-2 weeks)

**Goal:** enrich substrate for fireball-mage emergent class candidates per Wave 5 emergent generation

- [ ] **legolas Mode B catalogue crawl:**
  - Wikipedia / Wikidata: fireball-spell-tomes, elemental-orbs, AoE-staves, lightning-rods, chain-lightning-implements, ice-storm-implements, meteor-staves
  - Genre canon: D&D fireball-tradition + PoE elemental hit / spell-cascade + LE elemental traditions + DnD wizard schools (Evocation focus) + Final Fantasy / Anime mage-archetype implements
  - Mythological references: Greek/Norse/Slavic/Vedic fire deities' implements; thunder gods' instruments
- [ ] **elrond curation:**
  - Per-row: classify primary_stat=INT; weapon_type_family=caster-arcane; weapon_kind per existing enum; cultural_lineage_canonical + register_canonical per substrate; quality_composite_score
  - v1_scope=1 flag for candidates passing Tier-S/A composition policy gates
  - Spot-check ~10% of enriched rows for AI-tell / fabrication / classification errors
- [ ] **Target:** ~50-150 INT-AoE substrate rows; sufficient for fireball-mage emergent cluster to vote at Wave 5 generation
- [ ] **Output:** Sub-Fix 1 completion notes at `agentic_orchestration/elrond/notes/2026-05-27-substrate-enrichment-int-aoe-completion.md`
- [ ] **Composition with HYBRID Crusader:** if any enriched INT-AoE implement crosses into faith/divine register (e.g., holy-fire crusader-mace), tag for caster-faith Cycle 15 Path A discriminator (Interpretation III alignment)

### Sub-Fix 2 — Substrate Monk enrichment (~1-2 weeks)

**Goal:** enrich substrate for WIS-melee-light (monk) emergent class candidates per Wave 5 emergent generation

- [ ] **legolas Mode B catalogue crawl:**
  - Wikipedia / Wikidata: unarmed weapons (bagh nakh, tekko, knuckles, cestus, brass knuckles, shotel), martial-arts traditions (Shaolin / Krav Maga / Capoeira / Muay Thai / Karate / etc.), knuckle-weapons, monk-staves (bo-staff / shakujo / jo), sash-weapons (sansetsukon / kusari-fundo), tonfa, nunchaku
  - Genre canon: D&D monk-tradition (Way of Open Hand / Way of Four Elements) + PoE templar/spectre-monk + Lost Ark Soulfist / Striker classes + Diablo II/III Monk-class implements
  - Mythological references: Asian/Pacific monk-warrior traditions; Pacific islander warrior implements
- [ ] **elrond curation:**
  - Per-row: classify primary_stat=WIS; weapon_type_family=caster-faith OR new sub-classification (martial-light-monk?); weapon_kind per existing enum; cultural_lineage_canonical (predominantly east_asian / south_asian / oceanic / pre_classical Greek pankration / etc.); quality_composite_score
  - v1_scope=1 flag for candidates passing composition policy
  - Edge case: tonfa / nunchaku / staff implements may cross between WIS-melee-light + WIS-caster-faith; gandalf design-call follow-on if uncertain
- [ ] **Target:** ~50-100 WIS-melee-light substrate rows; sufficient for monk emergent cluster
- [ ] **Output:** Sub-Fix 2 completion notes at `agentic_orchestration/elrond/notes/2026-05-27-substrate-enrichment-monk-completion.md`

### Sub-Fix 3 — Substrate Hybrid enrichment (~1-2 weeks)

**Goal:** enrich substrate for cross-attribute hybrid emergent class candidates per Wave 5 emergent generation; composes with substrate composition policy v1 Option C cross-attribute ω-penalty

- [ ] **legolas Mode B catalogue crawl:**
  - Spellblades / magus-arcane-blades / runeblade traditions / rune-staves / battle-mages: D&D Eldritch Knight + Bladesinger + Hexblade + Magus PoE class + LE Falconer / Mage-Knight + FFXIV Red Mage / Dark Knight + Anime spellsword archetypes
  - Holy paladin-knight (STR+WIS): D&D Paladin oaths + Norse/Christian holy-knight traditions + FFXIV Paladin
  - Battle-mage (STR+INT): magitek-warrior archetypes + WoW Death Knight + Anime magic-knight
  - Mythological references: Arthurian + Celtic + Norse + Vedic hybrid warriors
- [ ] **elrond curation:**
  - Per-row: classify primary_stat (STR/DEX/INT/WIS) + secondary_stat per weapon_sim_props; weapon_type_family (likely hybrid OR cross-attribute variant); weapon_kind per existing enum
  - **Cross-attribute classification:** per Option C ω-penalty (`OMEGA_CROSS_ATTRIBUTE_PENALTY=0.80` per gandalf verdict `da16652` + gamora impl `b3f4db5`); rows where primary_stat ≠ traditional cell mapping flagged as Option-C-eligible
  - Composition policy v1 Option C cell-type matching gates apply
- [ ] **Target:** ~50-150 hybrid substrate rows; sufficient for spellsword / paladin-knight / battle-mage emergent clusters
- [ ] **Output:** Sub-Fix 3 completion notes at `agentic_orchestration/elrond/notes/2026-05-27-substrate-enrichment-hybrid-completion.md`
- [ ] **Composition with caster-faith HYBRID:** Path C Cycle 15 deferred commitment composes — Cycle 15 enrichment may extend hybrid sub-fix; this dispatch covers Cycle 14 pre-Wave-5 enrichment only

### Cross-sub-fix coordination

- [ ] All 3 sub-fixes fire IN PARALLEL (legolas Mode B sessions are independent per domain; elrond curation can stream as enrichment lands per domain)
- [ ] Per Discipline #20 robots.txt + Claude-agent directive respect: pre-flight verification per source domain crawl
- [ ] **Substrate library MIGRATION.md** consolidated per ADR-004 (one MIGRATION doc covering all 3 sub-fixes; cross-seam round-trip with rocket Stage 3 re-impl + gamora damage_resolver consuming new substrate via existing weapon_sim_props schema)
- [ ] Update SC-6b implementation report cross-reference if rows materially shift family distribution per SC-6b § 1.3
- [ ] Append completion records per sub-fix to this dispatch
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] Sub-Fix 1: ~50-150 INT-AoE substrate rows landed at `weapon_knowledge_entries` + `weapon_sim_props`; v1_scope flagged; spot-check 10% verified
- [ ] Sub-Fix 2: ~50-100 WIS-melee-light substrate rows landed; v1_scope flagged
- [ ] Sub-Fix 3: ~50-150 hybrid substrate rows landed; Option C classifications applied; v1_scope flagged
- [ ] Substrate library MIGRATION.md authored covering all 3 sub-fixes per ADR-004
- [ ] Cross-seam round-trip smoke: rocket Stage 3 re-impl substrate clustering at Math Note 1 fires can consume enriched rows (acceptance verified at Stage 3 re-impl time; this dispatch lays the substrate foundation)
- [ ] Per-sub-fix completion records appended to dispatch
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern

## Out of scope (explicit non-goals)

- Do NOT extend to multi-spawn summoner (separate engine subsystem; deferred per Matt triage)
- Do NOT extend to DEX rebalancing (resolves naturally per Matt triage)
- Do NOT extend to Skirmisher shield-family expansion (optional; gandalf-leaning-defer; revisit per Wave 5 evidence)
- Do NOT extend schema beyond existing `weapon_knowledge_entries` + `weapon_sim_props` columns (per SC-6b enrichment + Option α scope; if INT-AoE-specific stats needed, route separate dispatch)
- Do NOT touch character JSON output schema (Stage 3 re-impl scope)
- Do NOT touch substrate clustering algorithm (Math Note 1 specifies; this dispatch enriches what algorithm consumes)
- Do NOT touch damage_resolver / fight engine (gamora seam)
- Do NOT amend canonical docs (gandalf seam if architectural amendment needed)
- Do NOT block on math-note authoring (parallel; both must complete before Stage 3 re-impl)
- Do NOT enter Phase D substrate cleaning execution mode (per elrond OP — targeted enrichment only)

## Open questions for sub-agents

- **Q-Enrich-1 (legolas Sub-Fix 1 INT-AoE):** are there source domains where INT-AoE substrate is well-catalogued (e.g., Wikipedia article on "fictional fireball spells" / PoE wiki for spell tradition implements)? Per Discipline #20 robots.txt verification at source level.
- **Q-Enrich-2 (legolas Sub-Fix 2 Monk):** how to handle ambiguous tonfa/nunchaku/staff cross-classification (WIS-melee-light vs WIS-caster-faith)? legolas surfaces; gandalf Pattern-A if needed for design-call follow-on.
- **Q-Enrich-3 (elrond Sub-Fix 3 Hybrid):** Option C ω-penalty classification — does each hybrid row get a single primary_stat per existing schema OR new dual-stat schema extension? Per SC-6b columns existing schema sufficient (`primary_stat` + `secondary_stat` in `weapon_sim_props`); confirm.
- **Q-Enrich-4 (cross sub-fix):** target row counts per sub-fix — are ~50-150 (INT-AoE + Hybrid) and ~50-100 (Monk) the right sizes for substrate vote? Smaller = thin emergent class; larger = over-saturated. legolas + elrond decide per substrate vote density evidence.

## Hive-mind decision-routing reminder

Per Matt 2026-05-23 directive (hive-mind protocol § 4) + scope-doc § 4.1: legolas + elrond autonomous within their seams; cross-seam questions route via Pattern-A query (gandalf for design-call follow-on if WIS-melee-light vs WIS-caster-faith ambiguity surfaces). Matt is LAST-resort escalation.

## Anti-stall discipline

1. **Per-sub-fix batching** — complete one sub-fix's crawl + curation + DB ingest before moving to next; survives session boundaries
2. **legolas Mode B background processes** — per Discipline #19, crawls run as nohup background processes; status via JSON summary artifact existence + DB row counts; do NOT poll via Agent tool
3. **For LLM-assisted classification** (cultural_lineage_canonical / register_canonical / weapon_kind on edge cases) — batch in chunks of ~50 rows per LLM call
4. **If scope expansion** (e.g., monk sub-fix surfaces ~500 candidates instead of 50-100) — STOP and surface to KR for scope amendment

## References

- `agentic_orchestration/gandalf/notes/2026-05-27-option-alpha-kr-revert-kicker.md` § 3.6 (substrate enrichment substantive spec)
- `agentic_orchestration/gandalf/notes/2026-05-27-option-alpha-pivot-and-math-note-inventory.md` (Option α architectural context)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-wave-1-5-class-roster-substrate-audit.md` (Stage 1 audit; gap evidence)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` (substrate composition)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6b-substrate-enrichment-implementation.md` (SC-6b enrichment reference; column schema)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 (per-attribute weapon profile)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (Option α/β/C composition policy)
- `agentic_orchestration/GOVERNANCE.md` ADR-004 (cross-repo coordination + MIGRATION.md)
- Engineering disciplines #19 + #20 + #11
- Hive-mind protocol § 4 (decision-routing) + § 10.2 (mid-phase specialist recovery)

## Sequencing note

This dispatch fires IN PARALLEL with math-note bundle dispatch (`agentic_orchestration/dispatches/2026-05-27-gandalf-cycle-14-option-alpha-math-notes-bundle.md`). Per kicker § 3.6: "these 3 dispatches fire IN PARALLEL with math-note authoring. Neither blocks the other. Substrate enrichment provides ~1,500-3,000 additional substrate rows; math notes specify clustering algorithms that operate on whichever substrate population exists at fire-time. Both tracks must complete before Stage 3 re-implementation fires."

Wave 1.5 Stage 3 re-implementation fires when BOTH:
- All 5 math-notes Matt-ratified per Discipline #18 hotspot
- Substrate enrichment landed at sufficient row count for emergent classes to vote

A/B comparison post Wave 5 (gandalf): which emergent classes from enriched substrate map to doc 48 archetypes? Which doc 48 archetypes the substrate doesn't vote for? Which emergent classes weren't anticipated?
