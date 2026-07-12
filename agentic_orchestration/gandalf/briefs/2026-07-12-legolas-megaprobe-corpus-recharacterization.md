# LEGOLAS MEGA-PROBE — full corpus re-characterization (Mode A, single batched commission)

> **PASTE INTO MATT'S EXISTING LEGOLAS WINDOW** (the session that produced the mint-list dossiers, `96a4801`) — it already carries role + corpus context. If fired fresh instead: adopt legolas (read `.claude/agents/legolas.md` + OP skill) first; this brief is self-contained. Authored by gandalf 2026-07-12 under Matt's G1 ruling: *"collect the entire surface of the re-probe and send it out at once."*

## Mission

Re-characterize the ARPG canon corpus as **FACTS, not codes**. The mobile harvest's suffix key-slots (mob/geo/ctrl/def/econ/elem) are mobile-invented vocabulary that never passed a design gate; Matt ruled them un-trustable for engine joins (*"I think it's likely that we will mis-key the corpus using this strategy… I am very suspicious"*). You collect per-kit mechanical facts finer than ANY current vocabulary; gandalf's mapping tables compress them into engine vocabularies later. **The harvest authorizes the DATA, not the key.**

One pass per kit, every field at once — per-kit lookup cost dominates, so you never revisit a kit.

## Inputs (read first)

1. `agentic_orchestration/gandalf/views/corpus-rekey-spec-v1.md` §1–§2 — the engine-frame ruling + fate table
2. `claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/rdr-kit-atlas-v3.csv` — the substrate: **canon rows only** (exclude `corpus=rdr-roster` provenance rows). 515 canon rows = 478 positives + 37 negatives across 19 games (`game` column is authoritative)
3. `final-docs-v3/canon-harvest-pipeline-spec-v2.md` §4 — sources + derivation classes + THE POST-CUTOFF LAW (binding, below)
4. `final-docs-v3/rdr-kit-atlas-generator.py` — code vocabularies (to READ the old codes; you never EMIT them)
5. `agentic_orchestration/gandalf/views/roster-atlas-rebuilt-v1.csv` — the 45 founding-roster rows (Unit B)
6. Your own mint dossiers at `agentic_orchestration/legolas/research/mint-list-dossiers-2026-07-12/` (Unit D)

## Binding laws

1. **SOURCE-MATCH LAW (Matt directive 2026-07-12).** Every kit row carries a `prov` field (e.g. `mb;od2;kb`) naming the sources the mobile harvest used. **Consult those sources FIRST, per kit** — decode keys via the §4 table below. Re-reading the same sources makes every delta a *correction*, never a source artifact. Then: where a **Rank-1 mechanical-truth source** exists for that game (PoB codes, Grimtools links, lastepochtools, Maxroll planner links) and the kit's `prov` shows the original pass didn't use it, consult it too and flag `rank1_upgrade: true`.
2. **THE POST-CUTOFF LAW (harvest spec §4, verbatim binding):** budget ≥1 era search per game before trusting knowledge; EXPECT ≥1 content stratum to postdate training. Post-cutoff records: search-derivation mandatory, **confidence ≤0.5 ceiling, `dossier-owed` flag**, heavy abstains over confabulation. Era-stratification + negative-canon riders apply.
3. **Facts, not codes.** Never emit the retired vocabulary codes (S/L/M/N geo, D/M/C ctrl, H/M/L mob, etc.). Emit the structured fields + plain-text below. Abstain-not-guess; per-field confidence; `null` + `abstain_reason` beats invention.
4. **Measured-vs-projected law:** everything you return is a CLAIM with confidence. Corpus rows can never carry "measured" values — measured = gauntlet fingerprints only, which do not exist for corpus kits.
5. **Raw artifacts immutable.** You write NEW files under your own research dir only; never edit `final-docs-v3/` or `claude-mobile-session-docs/`.
6. **Operational hygiene (run-notes law):** planner-code sources outrank prose, always. API-first (poe.ninja has one); rate-limit courtesy; Reddit via API terms; no player PII. Wayback Machine for era-authentic tier lists ("what 2006 believed, not what 2026 remembers").

## §4 source table (folded in verbatim — decode `prov` keys against this)

| Game | Rank-1 (mechanical truth) | Rank-2 (canonicity/usage) | Rank-3 |
|---|---|---|---|
| PoE1 | PoB codes (`pb`, team) | poe.ninja API (`pn`, team) · mobalytics (`mb`) · odealo (`od2`) | wiki, forum archive, reddit |
| PoE2 | planner links (team) | **mobalytics-poe2 (`mb2`)** · poe2 ninja equivalent (`pn2`, team-verify) · maxroll-poe2 | aoeah/boostmatch/mtmmo live lists, reddit |
| D2/D2R | — | maxroll (`mx`) · icy-veins (`iv`) · diablo-wiki (`dw`) | Basin wiki, Wayback era lists |
| D3 | — | maxroll/icy-veins set-archetype tiers | era snapshots |
| D4 | Maxroll planner links | maxroll/mobalytics tiers | season retrospectives |
| LE | lastepochtools | LE tier lists, forum compendia | reddit |
| GD | **Grimtools links** | forum build compendium | reddit |

`kb` = settled-history knowledge (live-URL backfill owed at audit). **Games not in this table** (vs, di, tq/tq2, hot, undecember, chronicon, tl1/tl2, tli, hades1/hades2): route by each kit's `prov` keys + kb, one era check per game per the POST-CUTOFF LAW. Undecember note from run-notes: kr-trunk basins are primary; thein.ru holds the full runes library (Russian tooling basin).

## Unit A — per-kit fact sheets (the core; 478 positives full-depth, 37 negatives light)

Per kit, one JSONL record:

```
kit_id · game · folk_name · atlas_key (verbatim provenance)
delivery:      {value: projectile|line|beam|at-target|self-origin|orbit|aura-pulse|other, conf, evidence}
footprint:     {value: point|small-radius|large-zone|ring|cone|lane|chain-hop|multi-point|other, conf, evidence}
geo_text:      1–2 sentence plain-text spatial behavior (the fact the fields compress)
control:       {ailments: [...], centrality: core|rider|none, conf}
defense:       {layers: [armor|resist|dodge|block|shield-absorb|sustain-leech|hp-stack|glass|other], primary, conf}
               — shield/ES/ward/barrier is DISTINCT from armor/resist; block DISTINCT from dodge
economy:       {resource_verbatim, model: spend|cooldown|meter|reserve|ammo|proc|recipe|draft|harvest|self-cost|other,
                meter_type: rage|combo|focus|charge|n/a, builder_source, plain_text, conf}
element:       {label_verbatim (the game's OWN damage-type name), damage_mode: hit|dot|hybrid, conf}
movement:      {verbs: [...], policy_while_casting: rooted|walk|full-move, skill_is_movement: bool, conf}
prefix_claims: {attr, range, tempo, amp, proxy, commitment} — each {value, conf, evidence};
               commitment enum = instant|wind-up|channel (full 6-slot re-verify, Matt's tempo suspicion)
mechanics_notes: free text — anything the kit needs that no field captures (feeds the mechanics-gap census)
era_confirmed: bool (against the row's `eras` field) · post_cutoff: bool · rank1_upgrade: bool
sources_used:  [prov keys + live URLs]
```

**Negatives (37 rows):** light schema — delivery + footprint + one-line why-negative confirmation. They are warnings for whitespace classification, never emission candidates.

**Directed sweeps riding Unit A (no extra passes):**
- **Support-existence sweep (ctrl C2):** does ANY solo-context genre-canonical kit exist whose orientation is pure support? Answer explicitly in the index either way.
- **Line-vs-projectile (geo G2):** inside single-target/projectile kits, flag true line geometry (PoE Spark/Arc class) distinctly.
- **Shield-split (def D1 feed):** inside kits the mobile pass called "mitigation," flag which are actually shield/ES/ward kits.

**Effort stratification:** T1 games deep (decode planner codes where `prov` has them — mechanical truth, fast); T2/T2b moderate; T3 survivor-tier light (kb + one verification is usually sufficient — the kits are mechanically simple).

## Unit B — founding-roster lineage enrichment (45 rows; Matt's own directive)

For each `roster-atlas-rebuilt-v1.csv` row: **genre-lineage stats ONLY** — do NOT re-characterize our kits' mechanics (engine sources are ground truth for our kits). Collect: genre ancestors ({game}/{era}/{folk-name}, seeded from `lineage_targets` + fresh search) · ancestor game names · era span · ancestor tiers · recency (latest era attested) · longevity (distinct-era count) · conf · sources. Purpose: §F.5(3) duplication tiebreaks need the SAME stats on roster rows that corpus rows carry.

## Unit C — per-game meta verify (19 rows, cheap)

Per game: tier assignment verify · era-strings verify · one-line note. **HoT: confirm-or-refute the T3 lean explicitly** (Matt flag).

## Unit D — mint-dossier reconcile (9 kits, no re-research)

Re-express your mint-list dossiers into the Unit-A schema; flag any field a dossier lacks. Keeps the mint kits joinable with the probe output.

## Output + continuation protocol

- Dir: `agentic_orchestration/legolas/research/megaprobe-2026-07-12/`
- Files: `<game>-facts.jsonl` per game · `negatives-light.jsonl` · `roster-enrichment.csv` · `game-meta.csv` · `mint-reconcile.jsonl` · `00-index.md`
- **Game order** (run-notes calibration wisdom): d2 first (smallest, most consolidated — stress-tests the schema for pennies) → poe1 (biggest, best data) → d3 → d4 → gd → le → poe2 → di → tq/tq2 → tl1/tl2/tli → chronicon → undecember → hades1/hades2 → vs → hot.
- **Commit per game** (auto-commit per CLAUDE.md, no push) so partial progress survives. `00-index.md` tracks per-game status (PENDING/DONE, kit counts, abstain rates, rank1-upgrades, post-cutoff flags, anomalies).
- **If the session exhausts before completion:** Matt re-fires "continue the mega-probe" in the same window → read your own `00-index.md`, resume at the first non-DONE game. The brief never needs re-pasting.
- Final message per firing: ≤200-word status + index path.
