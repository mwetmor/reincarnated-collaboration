# LEGOLAS COMMISSION — Lost Ark full class-kit tranche (new source `la-`)

> **PASTE INTO EXACTLY ONE SESSION** (commit-as-mutex discipline, 2026-07-11).
> **Mode:** B — systematic catalogue harvest, at mega-probe depth (full Unit-A schema).
> **Commissioned:** gandalf, 2026-07-15, on Matt's ruling (census-freeze lift: *"Queue the full Lost Ark tranche post-Edition-II"* → Edition II shipped; Matt fired this in parallel with the atlas D2 pass).
> **READ-ONLY across all sources. NO corpus.db writes** — elrond curates downstream. Findings land in YOUR dir (path in §6).

---

## 1. Mission

Harvest **Lost Ark** as a NEW corpus source (`la-` prefix — verified absent from corpus prefixes) at **class-kit grain**, full mega-probe schema, so the rows join `canon_corpus` + `probe_facts` directly at curation. Lost Ark is the genre's biggest MMO-ARPG absent from our 19-game corpus; its class-engraving system is the densest build-identity vocabulary in the genre.

**Kit grain = CLASS ENGRAVING grain, not class grain.** Each LA class carries two Class Engravings defining distinct playstyles (e.g., Berserker: Mayhem vs Berserker's Technique; Sorceress: Igniter vs Reflux). Each engraving identity = one candidate row. Expect ~27+ classes × 2 ≈ **~55 rows** — but VERIFY the live class roster first (POST-CUTOFF LAW: the game has added classes past your training; enumerate from a live source before you start, and record the roster + count in your index).

## 2. Binding laws

1. **HONING-ECONOMY CONFOUND LAW (Matt-ruled, verbatim anchor):** LA's power curve is gear-honing-indexed; *kit identity claims must separate class/engraving design from honing economy.* Every row carries a `honing_confound` annotation where sources conflate character power with gear level. Tier/meta claims especially: an engraving's tier standing is often a honing-ceiling artifact — say so when it is.
2. **Intrinsic-only bar** (same bar as the pull tranche): skill + tripod + class-engraving + awakening mechanics are IN; gear-assembled identity (set effects, accessory/ability-stone engraving stacking, bracelets, elixirs) is **documented-but-excluded** — note it in `mechanics_notes`, never in the identity fields.
3. **Solo-PvE orientation with honest context:** corpus rows key to solo-PvE mechanical identity. LA is raid-centric — characterize the kit's mechanical behavior (what the skills DO), annotate `context` where an identity is raid-dependent. **Do NOT silently drop Bard / Paladin / Artist:** the genre's canonical group-support classes get rows with `context: group-support` annotated — they are the strongest stress-test of our C2 support-retirement ruling (which found zero SOLO-context pure supports; these are group-context, so the ruling predicts curation classes them system-record/negative-for-solo — collection must not pre-judge that).
4. **PvP excluded** as identity (LA balance splits PvP/PvE); note PvP-only variants in one line, no rows.
5. **POST-CUTOFF LAW + SOURCE-MATCH:** live-URL sourcing preferred (maxroll.gg Lost Ark, community class guides, official patch notes, wiki; KR inven via translations where load-bearing); kb-only rows flagged for backfill. `sources_used` per row.
6. **Destroyer cross-reference, don't duplicate:** `la-destroyer` was already probed at flagship depth in the pull-evidence tranche (`agentic_orchestration/research/knowledge/mcd-pull-mechanic/2026-07-15-pull-intrinsic-classkit-tranche.md`). Read it first; your Destroyer rows ENRICH it (both engravings), and any delta vs that record gets an explicit flag line.
7. **Zero invention:** a field you cannot source stays null with low conf — never interpolated.

## 3. Per-row schema — mega-probe Unit A, verbatim

Use the EXACT Unit-A JSONL schema from `agentic_orchestration/gandalf/briefs/2026-07-12-legolas-megaprobe-corpus-recharacterization.md` (read its Unit-A block before starting; the correction lineage in that dir shows what a reduced schema costs — do not re-collapse):

`kit_id` (`la-<class>-<engraving-slug>`) · `game: la` · `folk_name` (the community's name for the engraving playstyle) · delivery {value, conf, evidence} · footprint · geo_text · control {ailments, centrality} · defense {layers, primary} · economy {resource_verbatim, model, meter_type, builder_source, plain_text} — **LA's class identity gauges (e.g., Rage Meter, Arcana deck, Esoteric orbs, Shock/Hallucination gauge) are exactly what this family wants; capture the gauge mechanic verbatim** · element {label_verbatim, damage_mode} · movement {verbs, policy_while_casting, skill_is_movement} · prefix_claims {attr, range, tempo, amp, proxy, commitment — each {value, conf, evidence}; commitment enum = instant|wind-up|channel} · mechanics_notes (free text; feeds the mechanics-gap census — flag anything our engine vocabulary lacks) · era fields (§4) · rank1_upgrade · sources_used.

**Directed sweep riding the pass — PULL/GRAVITY CARRIERS:** beyond Destroyer, flag every class/engraving carrying intrinsic pull/vacuum/gravity displacement (enemy-moves-to-point mechanics). One index section listing carriers + skill names + evidence. This feeds the pull-slice re-keys; empty verdict is a valid answer, stated explicitly.

## 4. Era + meta fields (per row AND one per-game meta block)

- `era_year`: record BOTH KR release (2019) and global release (2022) at the game level; per-row, the engraving's debut patch/era if later (several engravings/classes post-date launch). Curation picks the convention — you record facts.
- `stabilization_patch`: where community canon names the patch/era an engraving's identity stabilized, record it; else null (this feeds the atlas provenance-name display).
- Per-row tier standing (release-era + current) with the honing-confound annotation per Law 1; longevity/lineage stats in the Unit-B shape (ancestors, era span, recency) so §F.5(3) duplication tiebreaks work on `la-` rows.
- One per-game meta block in the index: tier proposal for LA itself, roster count verification, patch-era timeline sketch.

## 5. Negatives

Engine-negative patterns (identity assembled from gear/honing rather than kit; pure-PvP identities) get LIGHT rows: delivery + footprint + one-line why-negative. Warnings for whitespace classification, never emission candidates.

## 6. Output + continuation protocol (mega-probe pattern)

- Home: `agentic_orchestration/legolas/findings/2026-07-15-lost-ark-classkit-tranche/` — `index.md` (mission, roster-of-record + count, per-class status table, sweep-answer sections, meta block) + `rows/<class>.jsonl` (both engravings per file).
- **Per-class commits.** First class = the CALIBRATION COMMIT — gandalf spot-checks it before the run is deep; a full-schema class cannot land in 3 minutes, and a fast first commit is itself a red flag.
- Continuation: the index carries your own progress state; a re-fired session told "continue" resumes from the index without re-briefing.
- Close: index finalized with sweep answers (pull-carriers, support-context findings, mechanics-gap notes rollup) + UPGRADE-OWED empty.

**On return:** gandalf verify → elrond curation commission (la- rows + engine re-keys + pull-tranche batch) → Edition III emission → Build Horizon re-vendor.

---

**Signed:** gandalf (SPEC-AUTHOR)
**For:** the genre's largest missing source, landed curation-ready in one pass — and the pull slice's carrier census riding along.
