# LEGOLAS COMMISSION — mint-list dossiers + prefix probes (Mode A, analytical)

> **PASTE INTO EXACTLY ONE SESSION** (fresh legolas session). Commissioned by gandalf 2026-07-12 under Matt's usage-offload directive. Read-only across all sources; file findings; no external-state writes beyond your own findings files + commit.

## Context (all you need)

The ARPG canon corpus (`claude-mobile-session-docs/ARPG-canonical-kit-research/`, 15 games / 563 records) is being re-keyed into the ENGINE coordinate frame — schema of record: `agentic_orchestration/gandalf/views/corpus-rekey-spec-v1.md` (read §1–§2 before starting). V4-r2 (`agentic_orchestration/gandalf/views/V4r2-roster-adjacency-rebuilt.md`) found 9 named genre ancestors ABSENT from the corpus. Matt's ruling anticipated this path: research the full details, then mint them as new corpus entries.

## Unit 1 — Mint-list dossiers (9 kits)

| Priority | Missing ancestor | For roster kit | Note |
|---|---|---|---|
| HIGH | poe1 totem archetype (Hierophant / Ancestral Warchief) | K18 | deep-iconic harvest hole — poe1 shipped totems 10+ years |
| HIGH | d3 Call of the Ancients | K5 | STR proxy-light anchor ancestor |
| MED | poe1 Ring of Shields (+ Replica) | H1, B7 | orbital-guard ancestor |
| MED | poe1 Blood Magic keystone kit | K26 | blood family attested cross-game; the keystone entry itself missing |
| MED | d2 Teleport Sorceress (as kit identity) | B5 | Enigma-era build-definer |
| MED | d3 Dashing Strike Monk · le Shift Bladedancer | B6 | movement-verb kits under-harvested (utility-vs-identity crawl bias) |
| LOW-MED | poe1 Vaal Blade Vortex | B10 | operator-tier variant of attested base |
| LOW | d2 Sacrifice | K26 | arguably negative-canon — recommend shipped/negative status, Matt rules |
| LOW | poe1 Flame Dash | B5 | utility not kit-identity — candidate for a NO-MINT recommendation |

**Dossier shape per kit** (one file each; dossier-format reference: `final-docs-v3/canon-harvest-pipeline-spec-v2.md`):
- game · patch/era span (league/version strings) · tier · folk name(s) · build identity (2–4 sentences) · shipped vs negative-canon status · lineage (ancestors/descendants by name) · sources
- **Per-slot ENGINE-PREFIX claims** as {value, confidence high/med/low, one-line evidence}: attr {STR,DEX,INT,WIS} · range {melee,mid,ranged} · tempo {low,med,high} · amp {flat,spiky,variable} · proxy {solo,light,heavy} · commitment {**instant**,wind-up,channel} (canon enum — never "snap")
- geo/ctrl/mob/def/econ/elem as **PLAIN-TEXT descriptors** — do NOT mint codes; those vocabularies are pending design sessions

## Unit 2 — PoE2 crossbow post-cutoff check

K8 Crossbow Sniper (`DRLS…` ranged/low/spiky/DEX): verify whether PoE2 crossbow skills (post-training-cutoff patches) attest this cell; short note with per-slot claims for the best 1–2 exemplars.

## Do-NOTs

- Do NOT edit `rdr-kit-atlas-v3.csv` or any raw harvest artifact — immutable; your dossiers are NEW files (elrond mints DB rows later)
- Do NOT invent key codes, ratings, or roster recommendations — claims + confidence + evidence only
- PoE1 3.29 delta re-harvest stays **PARKED** (~July 24) — out of scope here

## Output + report

File under `agentic_orchestration/legolas/` per your OP conventions: one dossier per kit + `00-index.md` summarizing confidence per slot per kit. Auto-commit per CLAUDE.md discipline (no push). Final message: ≤200-word summary + the index path.
