# Dispatch — 2026-06-01 — legolas — WS1A.Q18 Phase 1 parallel sampler commissioning (Sampler-A/B/C fan-out)

**From:** knight-rider (wave orchestrator)
**To:** legolas (Mode A research seam — commissioner + coordinator)
**Approved by:** Matt 2026-06-01 verbatim "hand to KR to fire the wave" + jack-ryan Phase 1 Gate-1 PASS (pending)
**Wave tag:** `WS1A.Q18-flavor-pool-research`
**Phase / phase-gate:** Phase 1 (3-sub-agent parallel fan-out); no formal PG at Phase 1 close (Phase 2 fires automatically once all 3 samplers return)
**Estimated effort:** Phase 1 wall-clock dominated by sub-agent web-research; legolas's coordination overhead is minimal (commission 3 sub-agents in single multi-agent invocation; absorb 3 returns)
**Acceptance:** 3 sampler outputs (JSONL + manifest JSON) at `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/`; legolas confirms all 3 well-formed before signaling Phase 2 (in-seam triage)

---

## 1. Context

Phase 0 (elrond data-medium consultation, PG-0) closed PASS at commit `9decb18`. Medium choice: **E.γ-prime — JSONL per-row + sidecar manifest JSON.** Format spec at `agentic_orchestration/elrond/consultations/2026-06-01-q18-flavor-pool-data-medium.md` § 3.1 (per-row schema) + § 3.2 (sidecar manifest schema) + § 4 (Phase 3 expansion format).

Phase 1 fires now: you commission 3 parallel sampler sub-agents (Sampler-A ARPG canon / Sampler-B JRPG-isekai canon / Sampler-C tabletop-myth canon) via a single multi-agent Agent-tool invocation per operational sequence § 4.1.

**Authoritative operational sequence:** `agentic_orchestration/gandalf/notes/2026-06-01-q18-flavor-pool-research-operational-sequence.md` — read § 2 Phase 1 + § 4.1 fan-out diagram + § 9.1/9.2/9.3 sampler prompt drafts (which are finalized below per elrond's format spec).

**Decision authority:** Phase 1 commissioning is yours per legolas seam authority (Mode A coordinator). Matt 2026-05-23 hive-mind directive: seam-owners decide in-scope; Matt is LAST-resort escalation.

---

## 2. Sub-agent fan-out pattern

```
                         legolas (this dispatch)
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        Sampler-A         Sampler-B         Sampler-C
        (ARPG canon)      (JRPG/isekai)     (tabletop/myth)
              │               │               │
              ▼               ▼               ▼
        sample-A.jsonl    sample-B.jsonl    sample-C.jsonl
        sample-A.manif    sample-B.manif    sample-C.manif
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                      legolas absorbs 3 reports
                      (Phase 2: in-seam triage)
                              ▼
                       sample-triage.md
```

**Sub-agent type:** `general-purpose` (web search + research + structured output capability).

**Invocation pattern:** single message with 3 Agent tool calls in parallel (per knight-rider OP § parallel-fan-out discipline; per hive-mind protocol).

---

## 3. Sampler-A prompt (finalized — ARPG canon)

Use this VERBATIM as the prompt to Sampler-A sub-agent (sub-agent type `general-purpose`):

> You are an ARPG genre researcher commissioned by gandalf (story-and-design steward) via legolas (research seam) for the Reincarnated project's WS1A.Q18 flavor-pool research-and-lock wave. Your task: sample the ARPG canon for **sub-element / flavor-element vocabulary** mapped to **8 canonical primary elements** (fire / water / earth / wind / lightning / holy / shadow / physical).
>
> **Primary sources to survey (target 5-10 candidates per primary):**
> - Diablo 1, 2, 3, 4, Immortal (skill databases per class tree; legendary/unique affix vocabulary; ailment vocab)
> - Path of Exile 1 + 2 (passive tree clusters; gem categories; ascendancy theming; ailment vocab — Ignite/Shock/Chill/Freeze/Bleed/Impale/Poison)
> - Last Epoch (skill trees + mastery elemental sub-categories; status effect taxonomy; minion theming)
> - Grim Dawn (devotion constellations; Eldritch/Order/Primordial category; Aether/Chaos/Vitality/Eldritch fifth-element vocab — load-bearing for shadow/holy mapping)
> - Lost Ark (engraving + skill names by class element)
> - Torchlight 2 / Infinite (skill trees; legendary set theming)
> - Wolcen / Chronicon / Titan Quest (skill/passive vocab per element)
>
> **For each primary element (fire / water / earth / wind / lightning / holy / shadow / physical), surface 5-10 candidate sub-element/flavor keywords.**
>
> **Specifically focus on:**
> - **Lightning gap-fill** (plasma / arc / volt / surge / storm / thunder / bolt / coil / static / spark — what does genre actually use)
> - **Holy gap-fill** (light / radiant / dawn / sanctum / blessed / consecrated / divine — but flag over-religious-coded risk)
> - **Shadow gap-fill** (umbra / void / shade / wraith / abyss / dusk / night — distinguish from earth-decay e.g. miasma, water-deep e.g. abyss)
> - **The 7-vs-8 empirical question for physical:** does ARPG canon treat physical with sub-element vocabulary (bleed / pierce / blunt / crush / sever / impale) AS sub-elements, or as flat-primary with no sub layer? Grim Dawn treats piercing/bleeding as sibling damage types; PoE has bleed+impale+maim as ailments not subs. Survey carefully; answer empirically.
>
> **Bound:** You are a SAMPLER, not exhaustive inventory. Surface 5-10 candidates per primary; let downstream Phase 3 expansion deepen.
>
> ## Output format (E.γ-prime per elrond Phase-0 consultation 2026-06-01)
>
> **Two files at `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/`:**
>
> ### File 1: `sample-A.jsonl` (per-candidate rows; one JSON object per line; no outer array; UTF-8)
>
> Per-row schema — required fields:
>
> ```json
> {
>   "candidate": "string — sub-element/flavor keyword (lowercased; singular form preferred)",
>   "primary_element": "fire | water | earth | wind | lightning | holy | shadow | physical",
>   "track": "ARPG",
>   "source_citations": [
>     {
>       "source": "string — game/work title (e.g., 'Diablo 4', 'Path of Exile')",
>       "locator": "string — skill/spell/affix/passive name OR page reference (e.g., 'Sorcerer skill: Incinerate')",
>       "notes": "string — optional per-citation clarification"
>     }
>   ],
>   "recognizability_score": 1,
>   "substrate_type": "material | phenomenon | proper_noun | mythological | mechanical_keyword | ailment | other",
>   "cross_primary_contamination": ["list of OTHER primary elements where this candidate also appears in genre canon; empty list [] if no contamination"],
>   "sampler_notes": "string — optional",
>   "row_id": "string — unique within file; recommended format: A-<primary>-<candidate>-<seq> (e.g., 'A-fire-cinder-001')",
>   "sample_date": "string — ISO-8601 date (e.g., '2026-06-01')"
> }
> ```
>
> **Field constraints:**
> - `candidate`: lowercase; singular noun preferred; no leading/trailing whitespace
> - `primary_element`: enum (8 values listed above)
> - `track`: literal string `"ARPG"` for all your rows
> - `source_citations`: at least 1 entry per row; each entry has `source` + `locator` (notes optional)
> - `recognizability_score`: integer 1 (niche) / 2 (common) / 3 (ubiquitous)
> - `substrate_type`: enum (7 values listed above)
> - `cross_primary_contamination`: empty list `[]` if no contamination; otherwise list of primary names from the enum
> - `row_id`: unique within file
> - `sample_date`: ISO-8601 date
>
> **Authoring discipline:**
> - One row per (candidate × primary) pair you surface. If a candidate is flex across primaries, that's MULTIPLE rows (one per primary), each with the other primaries in `cross_primary_contamination`.
> - If the SAME candidate has multiple source citations from the ARPG sources, those go into the SAME row's `source_citations` array (NOT as separate rows). Phase 4 frequency analysis counts citations from the array.
> - Append rows incrementally. Validate well-formedness before handoff: every line must parse as JSON.
> - Candidates without specific source citations are dropped at sampler-self-validation (do NOT emit rows with empty `source_citations` lists or hand-wave entries).
>
> ### File 2: `sample-A.manifest.json` (qualitative narrative + per-primary judgments; single JSON object)
>
> ```json
> {
>   "track": "ARPG",
>   "sampler_id": "A",
>   "sample_window": {
>     "started": "ISO-8601 datetime",
>     "completed": "ISO-8601 datetime"
>   },
>   "row_count": 0,
>   "per_primary_yield": {
>     "fire": {
>       "score": "STRONG | MEDIUM | WEAK | MISALIGNED",
>       "row_count": 0,
>       "rationale": "string — qualitative narrative on what you found",
>       "continue_stop_expand_recommendation": "CONTINUE | STOP | EXPAND",
>       "expansion_focus_if_recommended": "string — optional"
>     },
>     "water": { ... },
>     "earth": { ... },
>     "wind": { ... },
>     "lightning": { ... },
>     "holy": { ... },
>     "shadow": { ... },
>     "physical": { ... }
>   },
>   "source_coverage_breadth": [
>     {
>       "source": "string — game/work title",
>       "yield": "STRONG | MEDIUM | WEAK | MISALIGNED",
>       "notes": "string — optional"
>     }
>   ],
>   "substrate_tagging_gaps": "string — narrative on cross-primary contamination patterns observed",
>   "seven_vs_eight_signal": "string — your empirical read on whether physical surfaced sub-element vocab in ARPG canon, or collapsed",
>   "track_alignment_concerns": "string — content/constraint/alignment issues per Reincarnated positioning (e.g., source-X anti-pattern vocab; track-X off-Reincarnated-positioning)",
>   "sampler_summary": "string — top-level narrative paragraph"
> }
> ```
>
> **All 8 primaries required in `per_primary_yield`** (if a primary yielded zero, mark `score: "WEAK"` or `"MISALIGNED"` with `row_count: 0`).
>
> ## Acceptance criteria
> - [ ] `sample-A.jsonl` authored with rows per § File 1 schema; well-formed JSONL (each line parses as JSON)
> - [ ] `sample-A.manifest.json` authored per § File 2 schema; all 8 primaries present in `per_primary_yield`
> - [ ] All rows carry at least 1 source citation with specific `source` + `locator`
> - [ ] Per-primary yield judgments named (STRONG / MEDIUM / WEAK / MISALIGNED)
> - [ ] 7-vs-8 signal stated explicitly in manifest
> - [ ] Files committed to repo at `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-A.jsonl` + `sample-A.manifest.json`
> - [ ] Brief report-back to legolas (parent agent): row count, per-primary yield summary (1 line each), 7-vs-8 signal, any issues encountered

---

## 4. Sampler-B prompt (finalized — JRPG / isekai / anime canon)

Use this VERBATIM as the prompt to Sampler-B sub-agent (sub-agent type `general-purpose`):

> You are a JRPG / isekai / anime genre researcher commissioned by gandalf via legolas for the Reincarnated project's WS1A.Q18 flavor-pool research-and-lock wave. Your task: sample the JRPG / isekai / anime canon for sub-element / flavor-element vocabulary mapped to 8 canonical primary elements (fire / water / earth / wind / lightning / holy / shadow / physical).
>
> **Primary sources to survey (target 5-10 candidates per primary):**
> - Final Fantasy series (Fire/Fira/Firaga + Blizzard/Blizzara + Thunder + Aero + Holy + Drain + Bio + Stone families — 30-year locked spell-element vocab)
> - Persona / SMT (Agi=fire / Bufu=ice-water / Zio=lightning / Garu=wind / Hama=light-holy / Mudo=shadow-dark / Megido=almighty; sub-element vocab is rigidly structured)
> - Mushoku Tensei (spell categorization: Fire / Water / Earth / Wind / Detoxification / Healing / Curse / Summoning / Sword Magic)
> - KonoSuba (spell-name conventions; isekai-genre-typical flavor markers)
> - Slime / That Time I Got Reincarnated (magicule + element classifications)
> - Solo Leveling / Overlord (necromancy + shadow-element vocab specifically — load-bearing for shadow pool)
> - Tower of God / Berserk / Black Clover (element-magic vocab; unusual primary mappings)
>
> **For each primary element, surface 5-10 candidate sub-element/flavor keywords.**
>
> **Specifically focus on:**
> - **Lightning gap-fill, holy gap-fill, shadow gap-fill** (same focus as Sampler-A)
> - **The 7-vs-8 empirical question for physical:** does JRPG/isekai canon treat physical with sub-element vocab (Phys/Cut/Blunt/Pierce/etc.), or as flat-primary?
>
> **Specific to track B:**
> - Reincarnated is PROVISIONALLY isekai-positioned per D10; this track informs player-facing flavor vocabulary recognizability
> - Persona's element-vocab is canonical-locked across 30 years of JRPG genre; treat as load-bearing reference
> - Solo Leveling's shadow-army vocabulary is the strongest isekai-shadow precedent; mine deeply
>
> **Bound:** You are a SAMPLER, not exhaustive inventory. Surface 5-10 candidates per primary; let downstream Phase 3 expansion deepen.
>
> ## Output format (E.γ-prime per elrond Phase-0 consultation 2026-06-01)
>
> **Two files at `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/`:**
>
> ### File 1: `sample-B.jsonl` — same per-row schema as Sampler-A § File 1 above, with:
> - `"track": "JRPG_isekai"` (literal for all rows)
> - `"row_id": "B-<primary>-<candidate>-<seq>"`
>
> ### File 2: `sample-B.manifest.json` — same schema as Sampler-A § File 2 above, with:
> - `"track": "JRPG_isekai"`
> - `"sampler_id": "B"`
>
> Same field constraints, authoring discipline, and acceptance criteria as Sampler-A. Validate well-formed JSONL before handoff. Drop candidates without specific source citations.

---

## 5. Sampler-C prompt (finalized — tabletop + mythological + alchemical)

Use this VERBATIM as the prompt to Sampler-C sub-agent (sub-agent type `general-purpose`):

> You are a tabletop + mythological + alchemical genre researcher commissioned by gandalf via legolas for the Reincarnated project's WS1A.Q18 flavor-pool research-and-lock wave. Your task: sample tabletop + mythological + alchemical sources for sub-element / flavor-element vocabulary mapped to 8 canonical primary elements (fire / water / earth / wind / lightning / holy / shadow / physical).
>
> **Primary sources to survey (target 5-10 candidates per primary):**
> - D&D 5e + Pathfinder (energy damage types: Fire / Cold / Acid / Electricity / Sonic / Radiant / Necrotic / Force / Psychic; spell-school taxonomy; sub-element keywords)
> - MTG color pie (White=holy, Blue=water+lightning, Black=shadow, Red=fire, Green=earth+wind — loose alignment; mine card-name vocab)
> - Western alchemical tradition (four-classical + ether/aether; sub-substance vocab — sulphur / mercury / salt / etc.)
> - Eastern five-element Wu Xing (Wood/Fire/Earth/Metal/Water; cross-check on substrate-coherent vocab)
> - Folklore / mythology (especially for holy gap — sanctum / blessed / consecrated / sacred / divine — and shadow gap — umbra / abyss / void / wraith / shade)
>
> **For each primary element, surface 5-10 candidate sub-element/flavor keywords.**
>
> **Specifically focus on:**
> - **Lightning gap-fill, holy gap-fill, shadow gap-fill** (same focus as Sampler-A)
> - **The 7-vs-8 empirical question for physical:** does tabletop canon treat physical with sub-element vocab (bludgeoning/piercing/slashing as sibling damage types)?
>
> **Specific to track C:**
> - This track is the CROSS-CHECK that prevents over-fitting to ARPG (Track A) or JRPG/isekai (Track B) quirks
> - Tabletop sources are most rigorous for damage-type taxonomy; treat as recognizability-validation reference
> - Mythological sources are load-bearing where ARPG + JRPG yield is weak (especially holy + shadow; possibly lightning)
>
> **Bound:** You are a SAMPLER, not exhaustive inventory. Surface 5-10 candidates per primary; let downstream Phase 3 expansion deepen.
>
> ## Output format (E.γ-prime per elrond Phase-0 consultation 2026-06-01)
>
> **Two files at `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/`:**
>
> ### File 1: `sample-C.jsonl` — same per-row schema as Sampler-A § File 1 above, with:
> - `"track": "tabletop_myth"` (literal for all rows)
> - `"row_id": "C-<primary>-<candidate>-<seq>"`
>
> ### File 2: `sample-C.manifest.json` — same schema as Sampler-A § File 2 above, with:
> - `"track": "tabletop_myth"`
> - `"sampler_id": "C"`
>
> Same field constraints, authoring discipline, and acceptance criteria as Sampler-A. Validate well-formed JSONL before handoff. Drop candidates without specific source citations.

---

## 6. Your acceptance (legolas)

1. **Mkdir if needed:** `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/`
2. **Commission 3 sub-agents in single multi-agent invocation** per operational sequence § 4.1 parallel-fan-out discipline. All 3 prompts above (§ 3 / § 4 / § 5) used VERBATIM.
3. **Sustained-background-process discipline** per hive-mind protocol — sub-agents may take wall-clock time for web research; legolas waits for all 3 to return without polling (foreground Agent calls block; this is acceptable).
4. **Absorb 3 sample reports + manifests** as they return.
5. **Validate JSONL well-formedness** for all 3 files: `python -c "import json; [json.loads(line) for line in open('<path>')]"` succeeds.
6. **Brief report-back to KR** (this dispatch's parent agent) — see "Completion record" template below.
7. **Phase 2 trigger:** Phase 2 (in-seam triage) fires automatically once all 3 samplers return; you author `sample-triage.md` per operational sequence § 2 Phase 2.

**Commits:** auto-commit per CLAUDE.md addendum 2026-05-25 (in-scope Phase 1 work-products of authorized wave cycle). Push to remote remains Matt-explicit.

---

## 7. Out of scope

- **Phase 2 triage authorship is a SEPARATE fire** — Phase 2 fires automatically once Phase 1 returns; but for THIS dispatch the focus is Phase 1 commissioning + Phase 1 acceptance. Phase 2 instructions for you are in operational sequence § 2 Phase 2; you may proceed to Phase 2 in-seam directly once Phase 1 returns clean.
- **Phase 3 expansion sub-agents** — gated on PG-1 (gandalf ratification of Phase 2 triage); do NOT spawn expansion sub-agents until KR fires Phase 3 dispatch.
- **In-flight amendments** to sub-agent prompts after fire — sub-agents run as-prompted; if a fundamental scope error emerges mid-run, surface to KR via report-back at sub-agent return.

---

## 8. Cross-seam contract change? (Principle 6)

**Answer:** NOT applicable in this dispatch. Phase 1 commissioning + outputs live entirely within `agentic_orchestration/legolas/research/`; no engine substrate / telemetry DB / loadout dict / export packet modified. Round-trip not applicable.

---

## 9. References

- **Authoritative operational sequence:** `agentic_orchestration/gandalf/notes/2026-06-01-q18-flavor-pool-research-operational-sequence.md` (read § 2 Phase 1 + § 4.1 fan-out + § 9.1/9.2/9.3 sampler drafts as origins of the § 3/§ 4/§ 5 prompts above)
- **Phase-0 elrond consultation (PG-0 verdict):** `agentic_orchestration/elrond/consultations/2026-06-01-q18-flavor-pool-data-medium.md` (read § 3.1 per-row schema + § 3.2 manifest schema as origins of the format spec above)
- **Wave-state file:** `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/wave-state.md`
- **Legolas OP:** `agentic_orchestration/operating-procedures/legolas.md` (Mode A research; sub-agent commissioning; sustained-background-process)
- **Hive-mind protocol:** `agentic_orchestration/operating-procedures/hive-mind-protocol.md`

---

## Completion record (you append at completion)

```markdown
---

## Completion record
**Completed:** 2026-06-XX HH:MM
**Outputs:**
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-A.jsonl` + `sample-A.manifest.json`
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-B.jsonl` + `sample-B.manifest.json`
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-C.jsonl` + `sample-C.manifest.json`
**Total row count (across A+B+C):** <int>
**Per-sampler row counts:** A=<int>, B=<int>, C=<int>
**JSONL well-formedness validated:** yes/no
**Per-track per-primary yield summary:** brief table or 8 × 3 grid (STRONG/MEDIUM/WEAK/MISALIGNED)
**7-vs-8 preliminary signal (composed across 3 samplers):** <text — does physical have sub-vocab signal or collapse?>
**Notable issues:** <text or "none">
**Routing back to KR:** proceed to Phase 2 (in-seam triage) / hold for KR review / specific issue surfaced
```

After completion record append, Phase 2 fires automatically (legolas authors `sample-triage.md` per operational sequence § 2 Phase 2). KR routes Phase 2 triage to gandalf for PG-1 ratification.

---

**End of Phase 1 legolas commissioning dispatch.**
