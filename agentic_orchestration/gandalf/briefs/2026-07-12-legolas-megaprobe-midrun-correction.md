# MEGA-PROBE MID-RUN CORRECTION — restore the full Unit-A schema (paste into the running legolas window)

> **PASTE INTO THE RUNNING MEGA-PROBE LEGOLAS WINDOW.** Authored by gandalf 2026-07-12 after spot-checking `megaprobe-2026-07-12/` at the 4-game mark (d2 · poe1 · d3 · d4 landed). This corrects a schema drift; it does not restart the run.

## What STANDS (do not redo)

Your `delivery` + `footprint` collection is conformant and good (Trapsin chain-hop evidence is exactly the grade wanted). POST-CUTOFF LAW discipline (conf caps + `dossier_owed`) ✅. Game order ✅. Per-game commits + index discipline ✅. Units B/C/D tracked PENDING ✅. Negatives light-schema ✅.

## The drift

Your index's "Schema notes" declare the mission as *"replace suffix slots with delivery + footprint"* — that is **one-sixth of the commission.** The fired brief (`gandalf/briefs/2026-07-12-legolas-megaprobe-corpus-recharacterization.md`, Unit A) commissions SIX fact families per kit, because six retired key-slots (mob/geo/ctrl/def/econ/elem) all need fact-level replacement, and **per-kit lookup cost dominates — one pass per kit, every field at once.** The landed rows carry none of: `control`, `defense`, `economy`, `element`, `movement`, `geo_text`, `rank1_upgrade`, `sources_used`. Each missing family has a Matt ruling waiting to consume it:

| Missing family | Downstream consumer (ruled 2026-07-12) |
|---|---|
| `control` {ailments, centrality} | ctrl C1 — 123 "mixed" kits resolve per-kit; C2 — support keep-vs-retire decision |
| `defense` {layers, primary} — block DISTINCT from dodge, shield DISTINCT from armor | def D1 — absorb-bin population; D2 — each block kit keys to the layer its block-effect expresses |
| `economy` {resource_verbatim, model, meter_type, builder_source, plain_text} | econ E2 — meter split feeds doc-48 assigner; mechanics-gap census (SU/AM/PC/RC/RS/DR/HV + block-trigger) |
| `element` {label_verbatim, damage_mode} | EL-mech — provenance-only forever, but damage_mode (hit/dot/hybrid) feeds ailment-layer design |
| `movement` {verbs, policy_while_casting, skill_is_movement} | mob M1 — descriptor metadata; M2 — kit-vs-policy boundary |
| `geo_text` | the plain-text fact the delivery/footprint fields compress (audit trail) |
| `mechanics_notes` | mechanics-gap census (your `mech_note` partially covers — keep it, deepen it) |
| `rank1_upgrade` + `sources_used` (live URLs) | SOURCE-MATCH LAW — deltas must be provably corrections, not source artifacts |

## Corrected per-kit record (Unit A, verbatim — this replaces your reduced schema)

```
kit_id · game · folk_name · atlas_key (verbatim provenance)
delivery:      {value: projectile|line|beam|at-target|self-origin|orbit|aura-pulse|other, conf, evidence}
footprint:     {value: point|small-radius|large-zone|ring|cone|lane|chain-hop|multi-point|other, conf, evidence}
geo_text:      1–2 sentence plain-text spatial behavior
control:       {ailments: [...], centrality: core|rider|none, conf}
defense:       {layers: [armor|resist|dodge|block|shield-absorb|sustain-leech|hp-stack|glass|other], primary, conf}
economy:       {resource_verbatim, model: spend|cooldown|meter|reserve|ammo|proc|recipe|draft|harvest|self-cost|other,
                meter_type: rage|combo|focus|charge|n/a, builder_source, plain_text, conf}
element:       {label_verbatim (the game's OWN damage-type name), damage_mode: hit|dot|hybrid, conf}
movement:      {verbs: [...], policy_while_casting: rooted|walk|full-move, skill_is_movement: bool, conf}
prefix_claims: {attr, range, tempo, amp, proxy, commitment} — each {value, conf, evidence}
mechanics_notes · era_confirmed · post_cutoff · rank1_upgrade · sources_used: [prov keys + live URLs]
```

**Prefix slots — correction on method:** your landed rows pass the atlas bc6 key through with formula confidence (avg_conf × fixed multipliers — the banded 0.77/0.73/0.83 clusters betray it). That is not the commissioned *re-verify*. Corrected method, marginal-cost version: while on the kit's sources for the other families, CHECK each prefix claim against what the sources actually show. Where sources support the atlas value, keep it and let conf reflect the SOURCE support. Where sources contradict it, keep the atlas value in `atlas_key` (immutable provenance), emit the source-supported value in `prefix_claims`, and note the delta in `mechanics_notes`. Matt's tempo suspicion is the reason this axis exists — formula-conf is retired from this run.

**The three directed sweeps ride the per-kit pass (restore them):**
1. **Support-existence (ctrl C2):** does ANY solo-context genre-canonical pure-support kit exist? Answer explicitly in the index either way.
2. **Line-vs-projectile (geo G2):** inside single-target/projectile kits, flag true line geometry (Spark/Arc class) distinctly.
3. **Shield-split (def D1):** inside kits the mobile pass called "mitigation," flag which are actually shield/ES/ward kits.

## Sequencing from here

1. **From the next kit onward:** full schema above. No new game lands reduced.
2. **The four landed games (d2 · poe1 · d3 · d4):** mark `UPGRADE-OWED` in the index now; after `hot` completes, run an **in-place upgrade pass** per game — rewrite each row to the full schema, PRESERVING your existing delivery/footprint/post-cutoff work unchanged (git holds the reduced lineage; no separate enrichment files — one file per game stays the truth).
3. Units B/C/D unchanged per the original brief.
4. Index "Schema notes" section: replace with the corrected record above so a continuation session can't re-inherit the reduced schema.

Everything else in the original brief (binding laws, source table, effort stratification, continuation protocol) stands unchanged.
