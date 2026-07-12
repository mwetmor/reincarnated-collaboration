# Mega-Probe 2026-07-12 — Index

**Commission:** gandalf, 2026-07-12 (Matt's G1 ruling: "collect entire surface of re-probe at once")
**Filed:** legolas, 2026-07-12
**Purpose:** Re-characterize all 515 canon corpus rows (19 games) from retired mobile-harvest vocabulary to structured mechanical FACTS. Replace suffix slots (mob/geo/ctrl/def/econ/elem) with delivery + footprint per new vocab. Engine-prefix 6-slot (attr/range/tempo/amp/proxy/commit) carried forward from atlas bc6 keys.

**Output directory:** `agentic_orchestration/legolas/research/megaprobe-2026-07-12/`

---

## Schema notes

**Positives (full schema):** kit_id · folk_name · game · status · atlas_key · attr · range · tempo · amp · proxy · commit · delivery · footprint · era_span · post_cutoff · dossier_owed · prov · mech_note

**Negatives (light schema):** kit_id · folk_name · game · status · atlas_key · delivery · footprint · why_negative · era_span · post_cutoff · dossier_owed · prov · mech_note

**delivery vocab:** projectile | line | beam | at-target | self-origin | orbit | aura-pulse | other

**footprint vocab:** point | small-radius | large-zone | ring | cone | lane | chain-hop | multi-point | other

**commit vocab:** instant | wind-up | channel (NEVER "snap" — code hygiene flag only)

**Confidence rules:**
- Engine-prefix slots use `avg_conf` from atlas bc6 key as baseline
- `delivery` conf = avg_conf × 0.9
- `footprint` conf = avg_conf × 0.85
- Post-cutoff kits: all slot conf capped at 0.50; `dossier_owed: true`

---

## Game order + status

| # | Game | File | Corpus rows | Status | Commit |
|---|---|---|---|---|---|
| 1 | d2 | `d2-facts.jsonl` | 58 (51 pos / 7 neg) | **DONE** | pending |
| 2 | poe1 | `poe1-facts.jsonl` | 91 | PENDING | — |
| 3 | d3 | `d3-facts.jsonl` | 46 | PENDING | — |
| 4 | d4 | `d4-facts.jsonl` | 45 | PENDING | — |
| 5 | gd | `gd-facts.jsonl` | 41 | PENDING | — |
| 6 | le | `le-facts.jsonl` | 35 | PENDING | — |
| 7 | poe2 | `poe2-facts.jsonl` | 38 | PENDING | — |
| 8 | di | `di-facts.jsonl` | 23 | PENDING | — |
| 9 | tq + tq2 | `tq-facts.jsonl` | 26 | PENDING | — |
| 10 | tl1 + tl2 + tli | `tl-facts.jsonl` | 22 | PENDING | — |
| 11 | chronicon | `chronicon-facts.jsonl` | 17 | PENDING | — |
| 12 | undecember | `undecember-facts.jsonl` | 17 | PENDING | — |
| 13 | hades1 + hades2 | `hades-facts.jsonl` | 13 | PENDING | — |
| 14 | vs | `vs-facts.jsonl` | 24 | PENDING | — |
| 15 | hot | `hot-facts.jsonl` | 19 | PENDING | — |

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
