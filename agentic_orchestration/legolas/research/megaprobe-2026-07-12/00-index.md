# Mega-Probe 2026-07-12 — Index

**Commission:** gandalf, 2026-07-12 (Matt's G1 ruling: "collect entire surface of re-probe at once")
**Filed:** legolas, 2026-07-12
**Purpose:** Re-characterize all 515 canon corpus rows (19 games) from retired mobile-harvest vocabulary to structured mechanical FACTS. Replace suffix slots (mob/geo/ctrl/def/econ/elem) with delivery + footprint per new vocab. Engine-prefix 6-slot (attr/range/tempo/amp/proxy/commit) carried forward from atlas bc6 keys.

**Output directory:** `agentic_orchestration/legolas/research/megaprobe-2026-07-12/`

---

## Schema notes (corrected 2026-07-12 per gandalf mid-run brief)

**CORRECTED POSITIVES (full schema — 6 fact families per kit):**
```
kit_id · game · folk_name · atlas_key (verbatim provenance)
delivery:      {value: projectile|line|beam|at-target|self-origin|orbit|aura-pulse|other, conf, evidence}
footprint:     {value: point|small-radius|large-zone|ring|cone|lane|chain-hop|multi-point|other, conf, evidence}
geo_text:      1–2 sentence plain-text spatial behavior
control:       {ailments: [...], centrality: core|rider|none, conf}
defense:       {layers: [armor|resist|dodge|block|shield-absorb|sustain-leech|hp-stack|glass|other], primary, conf}
economy:       {resource_verbatim, model: spend|cooldown|meter|reserve|ammo|proc|recipe|draft|harvest|self-cost|other,
                meter_type: rage|combo|focus|charge|n/a, builder_source, plain_text, conf}
element:       {label_verbatim, damage_mode: hit|dot|hybrid, conf}
movement:      {verbs: [...], policy_while_casting: rooted|walk|full-move, skill_is_movement: bool, conf}
prefix_claims: {attr, range, tempo, amp, proxy, commitment} — each {value, conf, evidence}
mechanics_notes · era_confirmed · post_cutoff · rank1_upgrade · sources_used: [prov keys + live URLs]
```

**Negatives (light schema):** kit_id · folk_name · game · status · atlas_key · delivery · footprint · why_negative · era_span · post_cutoff · dossier_owed · prov · mech_note

**delivery vocab:** projectile | line | beam | at-target | self-origin | orbit | aura-pulse | other

**footprint vocab:** point | small-radius | large-zone | ring | cone | lane | chain-hop | multi-point | other

**commit vocab:** instant | wind-up | channel (NEVER "snap" — code hygiene flag only)

**Confidence rules (corrected):**
- Prefix slots: source-verified confidence per slot (NOT formula avg_conf × multiplier — that approach retired)
- delivery/footprint: source-verified confidence (approximate the quality of mechanic knowledge for that skill)
- Post-cutoff kits: all slot conf capped at 0.50; `dossier_owed: true`

**Three directed sweeps (restore per gandalf brief):**
1. Support-existence (ctrl C2): does ANY solo-context pure-support kit exist? Answer in index.
2. Line-vs-projectile (geo G2): inside single-target/projectile kits, flag true line geometry.
3. Shield-split (def D1): flag which kits are actually shield/ES/ward kits vs armour/HP.

**UPGRADE-OWED games (reduced schema — missing 5 of 6 fact families):**
- d2, poe1, d3, d4, gd — in-place upgrade pass runs AFTER `hot` completes; delivery/footprint/post-cutoff preserved

---

## Game order + status

| # | Game | File | Corpus rows | Status | Commit |
|---|---|---|---|---|---|
| 1 | d2 | `d2-facts.jsonl` | 58 (51 pos / 7 neg) | **DONE — UPGRADE-OWED** | 1462eaf |
| 2 | poe1 | `poe1-facts.jsonl` | 91 (85 pos / 6 neg) | **DONE — UPGRADE-OWED** | 848c1b0 |
| 3 | d3 | `d3-facts.jsonl` | 46 (42 pos / 4 neg) | **DONE — UPGRADE-OWED** | 8eea8ec |
| 4 | d4 | `d4-facts.jsonl` | 45 (41 pos / 4 neg) | **DONE — UPGRADE-OWED** | fa4684b |
| 5 | gd | `gd-facts.jsonl` | 41 (38 pos / 3 neg) | **DONE — UPGRADE-OWED** | def1fbc |
| 6 | le | `le-facts.jsonl` | 35 (32 pos / 3 neg / 4 pc) | **DONE (full schema)** | 995a732 |
| 7 | poe2 | `poe2-facts.jsonl` | 38 (34 pos / 4 neg / 7 post-cutoff) | **DONE (full schema)** | 998c6a8 |
| 8 | di | `di-facts.jsonl` | 23 (20 pos / 0 neg / 3 post-cutoff) | **DONE (full schema)** | 1df4d50 |
| 9 | tq + tq2 | `tq-facts.jsonl` | 26 (19 pos / 2 neg / 5 post-cutoff TQ2-EA) | **DONE (full schema)** | 1cf9122 |
| 10 | tl1 + tl2 + tli | `tl-facts.jsonl` | 22 (16 pos / 1 neg / 5 post-cutoff TLI-2026) | **DONE (full schema)** | 3de8aa6 |
| 11 | chronicon | `chronicon-facts.jsonl` | 17 (17 pos / 0 neg / 0 post-cutoff) | **DONE (full schema)** | 234f657 |
| 12 | undecember | `undecember-facts.jsonl` | 17 (17 pos / 0 neg / 4 post-cutoff ud-s7-2025) | **DONE (full schema)** | 8729cd6 |
| 13 | hades1 + hades2 | `hades-facts.jsonl` | 13 (13 pos / 0 neg / 4 post-cutoff hades2-1.0+) | **DONE (full schema)** | 3dc0a96 |
| 14 | vs | `vs-facts.jsonl` | 24 (22 pos / 2 neg / 1 post-cutoff vs-1.13-2025+) | **DONE (full schema)** | 2945325 |
| 15 | hot | `hot-facts.jsonl` | 19 (18 pos / 1 neg / 2 post-cutoff hot-1.1-2026) | **DONE (full schema)** | 7384750 |

**Unit B** (founding-roster lineage enrichment, 45 rows): PENDING — `roster-lineage-enrichment.jsonl`

**Unit C** (per-game meta verify, 19 rows): PENDING — `per-game-meta.jsonl`

**Unit D** (mint dossiers re-expressed in Unit A schema): PENDING — `mint-dossiers-reexpressed.jsonl`

---

## Post-cutoff notes per game

- **d2:** 6 Warlock kits (d2-wl-*) — Reign of the Warlock Season 13, launched Feb 2026. All capped at conf≤0.5, dossier_owed=true.
- **poe2:** All 38 rows from 0.1–0.2 era; post-0.2 patches (0.3–0.5, Dawn of the Hunt) = post-cutoff. Check per-row.
- **d4:** S4–S7 era items may be post-cutoff; flag per-row.
- **le:** Epoch 1.0+ kits; verify per-row.
- Other games: mostly pre-cutoff; flag any confirmed post-cutoff.

---

## Continuation protocol

Each game-file is self-contained JSONL. Sessions can pick up from the next PENDING game in the table. Update this index status column + commit column as each file lands.
