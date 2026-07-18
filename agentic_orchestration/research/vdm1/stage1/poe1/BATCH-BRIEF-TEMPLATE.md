# VDM-1 Stage-1 PoE1 batch brief — TEMPLATE (batches 03–08)

You are legolas (Mode B — systematic crawl) executing VDM-1 Stage-1 PoE1 for YOUR BATCH (the spawning prompt names your batch number NN and spec-line slice). VDM-1 = the autonomous verify+dossier+map run (charter: `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-charter.md`, steward gandalf). HARD DEADLINE: all 94 PoE1 kits before July 24 (3.29 churns sources).

## Your slice
`sed -n '<START>,<END>p' /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/vdm1/stage0/poe1-search-specs.jsonl`
Records: kit_id, folk_name, aliases, class, eras, core_skills, negative, query_candidates, preferred_domains, wayback_needed, junk_quarantine, negative_canon_target.

## Claims to verify (per kit)
Pull the record READ-ONLY: `sqlite3 -readonly .../agentic_orchestration/research/curated/corpus.db` — `canon_corpus` row (`.schema canon_corpus`; select identity/mechanics/era/negative fields) + `canon_probe_facts.facts_json` per family. **NEVER write this DB — elrond is single-writer.** journal_mode is DELETE; if a transient CANTOPEN(14) occurs, retry after 5s.

Four claim families, judged against FETCHED TEXT only (never memory):
- `identity` — folk name + aliases are real community usage
- `mechanics` — core skills / key items / resource mechanism / delivery are as recorded
- `era` — build present/meta in the stamped eras (⚠ known-weakest field; check skill INTRODUCTION patch vs era floor — batch-02 caught an era stamped before the skill existed)
- `negative_canon` — **ONLY for negative=true kits. For negative=false kits emit NOTHING for this family** (no filler UNSUPPORTED rows — they pollute the partition analysis)

**Verdicts (exact strings):** `CONFIRMED` · `CONTRADICTED` · `UNSUPPORTED` (source silent — honest, expected) · `SOURCE_NOT_FOUND`. anchor_quote (verbatim, ≤40 words) MANDATORY for CONFIRMED/CONTRADICTED.

## Dossier extraction (same fetches)
6 families (exact strings): `skill_loop` · `skill_geometry` (verbatim geometry/range/AoE/projectile language) · `item_alterations` · `capstone_alterations` · `author_credit` (handle + site, devlog credit) · `variants`. **NO-FABRICATION LAW:** source silent → `abstained: 1`, `payload_json: null` — **strictly null, never `{"note":...}`** (the DB CHECK rejects abstained rows with any payload; put the abstention reason in your batch summary, not the payload). `conf` 0.0-1.0 on non-abstained rows.

## Citations
cite_class ∈ {authored, communal, official, dataset} · rank_class ∈ {recovered, attested-era} · junk-tail (sky/u4/aoeah/mmoexp/igvault/g2g/eldorado gold-seller SEO) → quarantined: 1, never a verify/dossier source.

## Crawl discipline (updated from batches 01–02)
- **Domain order: poedb.tw → poe-vault.com → maxroll.gg → pathofexile.com/forum → odealo.com → reddit.com/r/pathofexile → poe.ninja (era attestation).**
- **poewiki.net is Anubis-403-blocked; pathofexile.fandom.com is paywalled — do NOT burn fetches on them live; Wayback snapshots of poewiki are fine.**
- Typical 2-3 fetches/kit; quote anchors only, never dump pages.
- wayback_needed: availability API `http://archive.org/wayback/available?url=<URL>&timestamp=<YYYYMMDD>`. Era→timestamp: 1.x≈2014 · 2.x≈2016 · 3.0-3.6≈2017-2019 · 3.7-3.13≈20190701-20210101 · 3.14-3.19≈2021-2022 · 3.20+≈2023-2026. poe.ninja league archives attest era-meta.
- Fully SOURCE_NOT_FOUND after honest search → record, move on (Unattested Register is a deliverable).

## Outputs (append per-kit as you go — crash durability)
Dir: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/vdm1/stage1/poe1/`
1. `batch-NN-verify.jsonl` — {kit_id, claim_family, claim_text, verdict, anchor_quote, source_url}
2. `batch-NN-citations.jsonl` — {kit_id, url, archive_url, site, author_handle, title, cite_class, rank_class, accessed_date, quarantined}
3. `batch-NN-dossier.jsonl` — {kit_id, family, payload_json (object|null), source_url, anchor_quote, abstained, conf}
4. `batch-NN-summary.md` — per-kit one-liners + verdict histogram + contradictions + SNF + dossier coverage + author credits

## Laws
- Commit PATHSPEC-ONLY (`git add` the 4 files exactly; never -A), message `legolas: VDM-1 stage-1 PoE1 batch-NN — verify+citations+dossier (kits <START>-<END>)`. **Do NOT push** (steward pushes; parallel pushes race). If `git commit` hits index.lock: wait 30s, retry up to 3×.
- 0 contradictions across the batch → say so LOUDLY in the summary. >30% kits SOURCE_NOT_FOUND → stop grinding, report.
- Return: verdict histogram, contradictions (one line each), SNF kits, dossier coverage %, red flags. Under 400 words.
