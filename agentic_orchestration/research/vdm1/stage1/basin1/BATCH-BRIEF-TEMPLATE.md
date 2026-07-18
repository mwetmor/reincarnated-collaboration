# VDM-1 Stage-4 basin-1 (post-cutoff) batch brief — TEMPLATE (batches 01–04; forked from the PoE1 template per stage-3 D-1 GO, all LAWS carry)

You are legolas (Mode B — systematic crawl) executing VDM-1 basin-1 (post-cutoff: PoE2 · Hades II · Titan Quest 2) for YOUR BATCH (the spawning prompt names your batch number NN and spec-line slice). VDM-1 = the autonomous verify+dossier+map run (charter: `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-charter.md`, steward gandalf). These games post-date your training cutoff or churned hard after it — **trust FETCHED TEXT over memory even more than usual; your priors about these games are systematically stale.**

## Your slice
`sed -n '<START>,<END>p' /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/vdm1/stage0/basin1-post-cutoff-search-specs.jsonl`
Records: kit_id, folk_name, aliases, game (`poe2`|`hades2`|`tq2`), class, eras, core_skills, negative, query_candidates, preferred_domains, wayback_needed, junk_quarantine, negative_canon_target. Batch↔lines: b01=1-12 · b02=13-24 · b03=25-36 (all poe2) · b04=37-48 (poe2×2 + hades2×5 + tq2×5).

## Claims to verify (per kit)
Pull the record READ-ONLY: `sqlite3 -readonly /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db` — `canon_corpus` row (`.schema canon_corpus`; identity/mechanics/era/negative fields) + `canon_probe_facts.facts_json` per family. **NEVER write this DB — elrond is single-writer.** journal_mode is DELETE; transient CANTOPEN(14) → retry after 5s.

Four claim families, judged against FETCHED TEXT only (never memory):
- `identity` — folk name + aliases are real community usage
- `mechanics` — core skills / key items / resource mechanism / delivery are as recorded
- `era` — build present/meta in the stamped eras. **UNIFORM LAW (stage-3 D-2a, binding):** an era floor predating the skill/co-skill's INTRODUCTION patch = **CONTRADICTED**, even when the build genuinely existed in the back half of the window — never CONFIRMED-with-note. Intro-patch check is MANDATORY (D-2b). Era vocab this basin: **poe2** 0.x patches (0.1 EA launch Dec 2024 · 0.2 Dawn of the Hunt · 0.3 The Third Edict · 0.4 · 0.5 Runes of Aldur, current ≈0.5.4) — kb-legacy stamps predating 0.1 are automatic contradictions; **hades2** `hades2-1.0-2025` (v1.0 Sept 2025) / `hades2-post1.0-2026` (post-1.0 patches; console launch 2026) — Early-Access-only mechanics REMOVED at 1.0 are era contradictions if stamped 1.0+; **tq2** `tq2-ea-2025+` (EA launch 2025, rolling updates) — mechanics from pre-release marketing that never shipped are contradictions.
- `negative_canon` — **ONLY for negative=true kits. For negative=false kits emit NOTHING for this family** (no filler UNSUPPORTED rows).

**Verdicts (exact strings):** `CONFIRMED` · `CONTRADICTED` · `UNSUPPORTED` (source silent — honest, expected) · `SOURCE_NOT_FOUND`. anchor_quote (verbatim, ≤40 words) MANDATORY for CONFIRMED/CONTRADICTED.

## Dossier extraction (same fetches)
6 families (exact strings): `skill_loop` · `skill_geometry` (verbatim geometry/range/AoE/projectile language) · `item_alterations` · `capstone_alterations` (poe2: ascendancy notables; hades2: aspects/hexes/keepsakes; tq2: mastery capstones) · `author_credit` (handle + site) · `variants`. **NO-FABRICATION LAW:** source silent → `abstained: 1`, `payload_json: null` — **strictly null, never `{"note":...}`** (DB CHECK rejects abstained rows with any payload; abstention reason goes in your batch summary). `conf` 0.0-1.0 on non-abstained rows.

## Citations
cite_class ∈ {authored, communal, official, dataset} · rank_class ∈ {recovered, attested-era} · junk-tail (sky/u4/aoeah/mmoexp/igvault/g2g/eldorado gold-seller SEO) → quarantined: 1, never a verify/dossier source.

## Crawl discipline (probe-verified for this basin, 2026-07-18)
- **Domain order per game:**
  - **poe2:** poe2db.tw/us → maxroll.gg/poe2 → pathofexile.com/forum → reddit.com/r/PathOfExile2 → poe.ninja **with `?game=poe2`** (era/meta attestation — the bare URL serves PoE1 data).
  - **hades2:** steamcommunity.com/app/1145350 (guides + announcements) → supergiantgames.com/blog (official patch notes) → reddit.com/r/HadesTheGame.
  - **tq2:** steamcommunity.com/app/1154030 (guides) → store.steampowered.com/app/1154030 (official updates) → THQ Nordic forums → reddit.
- **DEAD DOMAINS — do NOT burn fetches:** mobalytics.gg (403) · hades2.wiki.gg AND hades.wiki.gg (401) · titanquest2.fextralife.com (ECONNREFUSED). poewiki.net remains Anubis-blocked (PoE1 legacy — shouldn't need it here).
- Typical 2-3 fetches/kit; quote anchors only, never dump pages.
- **Wayback: effectively unneeded this basin (0 kits flagged)** — sources are live. If a live fetch 404s, one availability-API check is fine, then move on.
- Fully SOURCE_NOT_FOUND after honest search → record, move on (Unattested Register is a deliverable). TQ2/Hades2 kits are YOUNG — sparse guide coverage is expected, honest UNSUPPORTED beats stretch-reading.

## Outputs (append per-kit as you go — crash durability)
Dir: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/vdm1/stage1/basin1/`
1. `batch-NN-verify.jsonl` — {kit_id, claim_family, claim_text, verdict, anchor_quote, source_url}
2. `batch-NN-citations.jsonl` — {kit_id, url, archive_url, site, author_handle, title, cite_class, rank_class, accessed_date, quarantined}
3. `batch-NN-dossier.jsonl` — {kit_id, family, payload_json (object|null), source_url, anchor_quote, abstained, conf}
4. `batch-NN-summary.md` — per-kit one-liners + verdict histogram + contradictions + SNF + dossier coverage + author credits

## Laws
- Commit PATHSPEC-ONLY (`git add` the 4 files exactly; never -A), message `legolas: VDM-1 basin-1 batch-NN — verify+citations+dossier (kits <START>-<END>)`. **Do NOT push** (steward pushes; parallel pushes race). index.lock → wait 30s, retry up to 3×.
- 0 contradictions across the batch → say so LOUDLY in the summary. >30% kits SOURCE_NOT_FOUND → stop grinding, report.
- Greppable tokens are NEVER emitted in negated form (stage-3 D-2d) — write "considered, not applicable" without the literal token.
- Return: verdict histogram, contradictions (one line each), SNF kits, dossier coverage %, red flags. Under 400 words. **Your returned histogram is ADVISORY — file truth is the count** (stage-3 D-2c; the steward recounts from your committed files).
