# VDM-1 Stage-4 basin-2 (GD/LE) batch brief — TEMPLATE (batches 01–07; forked from the basin-1 template, all LAWS carry)

You are legolas (Mode B — systematic crawl) executing VDM-1 basin-2 (Grim Dawn · Last Epoch) for YOUR BATCH (the spawning prompt names your batch number NN and spec-line slice). VDM-1 = the autonomous verify+dossier+map run (charter: `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-charter.md`, steward gandalf). **Stale-priors split for this basin:** GD base/AoM/FG content (2016–2019) is pre-cutoff-stable — your priors are usable as SEARCH heuristics but NEVER as verdict grounds; GD `patch-1.1-1.2`/`foa-pending` and LE `1.2-woven`/`1.4-omens` are post-cutoff or churned-after-cutoff — treat exactly like basin-1 (fetched text only, priors systematically stale).

## Your slice
`sed -n '<START>,<END>p' /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/vdm1/stage0/basin2-gdle-search-specs.jsonl`
Records: kit_id, folk_name, aliases, game (`gd`|`le`), class, eras, core_skills, negative, query_candidates, preferred_domains, wayback_needed, junk_quarantine, negative_canon_target. Batch↔lines: b01=1-12 · b02=13-24 · b03=25-36 (all gd) · b04=37-48 (gd 37-41 + le 42-48) · b05=49-60 · b06=61-72 (le) · b07=73-78 (le, 6 kits).
⚠ **The spec's `preferred_domains` field is PARTIALLY STALE — this template's domain order OVERRIDES it** (spec-gen probes post-dated the field authoring): grimtools.com and lastepochtools.com are 403-browser-required to crawlers; do not burn live fetches on them (see crawl discipline).

## Claims to verify (per kit)
Pull the record READ-ONLY: `sqlite3 -readonly /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db` — `canon_corpus` row (`.schema canon_corpus`; identity/mechanics/era/negative fields) + `canon_probe_facts.facts_json` per family. **NEVER write this DB — elrond is single-writer.** journal_mode is DELETE; transient CANTOPEN(14)/BUSY → retry after 5s.

Four claim families, judged against FETCHED TEXT only (never memory):
- `identity` — folk name + aliases are real community usage
- `mechanics` — core skills / key items / resource mechanism / delivery are as recorded. ⚠ basin-1 precedent: post-cutoff-era kb rows contradicted on CONTENT (identity/mechanics), not just era — do not assume kb mechanics fields are right for the churned eras. ⚠ Resource-field artifact (2 hits b01/b02, systematic): `spirit/focus` resource labels in gd rows — GD's universal resource is Energy ("Spirit" is a GD STAT name, the likely confusion source); LE uses Mana (+Ward overshield). Verify resource-mechanism claims against fetched text specifically; flag every hit for the elrond sweep
- `era` — build present/meta in the stamped eras. **UNIFORM LAW (stage-3 D-2a, binding):** era floor predating the skill/co-skill's INTRODUCTION = **CONTRADICTED**; floor postdating attested presence = **CONTRADICTED** (floor-too-late class, ERRATA-17 precedent). Intro check is MANDATORY (D-2b). Era vocab this basin:
  - **gd:** `base-2016` · `aom-2017` (Ashes of Malmouth xpac) · `fg-2019` (Forgotten Gods xpac) · `patch-1.1-1.2` (long live-patch era) · `foa-pending` (Fangs of Asterkarn — verify SHIP STATUS from fetched text; mechanics from pre-release marketing that never shipped = contradictions, tq2-analog rule). **Mastery→expansion intro-check instrument:** Inquisitor/Necromancer masteries debuted with AoM, Oathkeeper with FG — a kit on those masteries stamped `base-2016` is an automatic D-2a candidate; CONFIRM the mastery's debut from fetched text before issuing the verdict.
  - **le:** `beta-0.8-0.9` (pre-1.0 EA) · `1.0-launch` (Feb 2024) · `1.1-harbingers` (2024) · `1.2-woven` · `1.4-omens` (post-cutoff seasons — fetched text only). Mastery/skill debut patches churned across beta→1.x; verify intro from patch notes/guides, never memory.
- `negative_canon` — **ONLY for negative=true kits** (this basin: gd-blade-trap, gd-reap-spirit, gd-stun-jacks, le-shield-bash-le, le-soul-feast, le-tempest-strike). For negative=false kits emit NOTHING for this family.

**Roster-hygiene note (ingest-8):** `le-ring-of-shields` and `le-shift-bladedancer` carry NULL era/core_skills kb fields — nothing-to-contradict for the NULL fields; verify what IS recorded, extract dossier forward, and record attested eras in your summary for steward backfill (VBV BACKFILL-1 precedent — do not stretch-verdict against absent claims).

**Verdicts (exact strings):** `CONFIRMED` · `CONTRADICTED` · `UNSUPPORTED` (source silent — honest, expected) · `SOURCE_NOT_FOUND`. anchor_quote (verbatim, ≤40 words) MANDATORY for CONFIRMED/CONTRADICTED.

**Claim-vs-claim is NEVER contradiction grounds (b01 steward ruling, BINDING):** verdicts measure FETCHED SOURCE TEXT vs the claim. A kb/spec field disagreeing with ANOTHER kb/spec field (e.g. DB era vs spec era vs negative_canon_target framing) is an INTERNAL inconsistency — report it in your summary red-flags for the steward/elrond erratum queue, and verdict the claim against fetched text alone (CONFIRMED / UNSUPPORTED as the source actually supports). The anchor_quote for CONFIRMED/CONTRADICTED must be verbatim FETCHED language — never our own spec/kb text.

## Dossier extraction (same fetches)
6 families (exact strings): `skill_loop` · `skill_geometry` (verbatim geometry/range/AoE/projectile language) · `item_alterations` · `capstone_alterations` (gd: devotion constellations + mastery capstones + xpac set identities; le: passive-tree capstones + unique/set item identities + weaver/season mechanics if attested) · `author_credit` (handle + site) · `variants`. **NO-FABRICATION LAW:** source silent → `abstained: 1`, `payload_json: null` — **strictly null, never `{"note":...}`** (DB CHECK rejects; abstention reason goes in your batch summary). `conf` 0.0-1.0 on non-abstained rows — **NUMERIC float only, never a string tag** (D-5 lesson).

## Citations
cite_class ∈ {authored, communal, official, dataset} · rank_class ∈ {recovered, attested-era} · junk-tail (sky/u4/aoeah/mmoexp/igvault/g2g/eldorado gold-seller SEO) → quarantined: 1, never a verify/dossier source (basin-1 b03 fired the run's first quarantines — the tail is live in this genre's SEO).

## Crawl discipline (probe-verified 2026-07-18)
- **Domain order per game:**
  - **gd:** forums.crateentertainment.com (build compendiums + patch notes — primary) → steamcommunity.com/app/219990 guides → reddit.com/r/Grimdawn. **grimtools.com is 403-browser-required** — NEVER fetch live; grimtools build-links quoted in forum/reddit posts are fine as citation URLs, but the VERIFYING TEXT is the surrounding post, not the calc page. **grimdawn.fandom.com is paywalled-DEAD · maxroll.gg has NO GD coverage (404)** — do not try either.
  - **le:** maxroll.gg/last-epoch (ALIVE — primary) → forum.lastepoch.com → steamcommunity.com/app/899770 guides → reddit.com/r/LastEpoch. **lastepochtools.com is 403-browser-required** — same rule as grimtools · **tunklab is DEAD.**
- Typical 2-3 fetches/kit; quote anchors only, never dump pages.
- **Wayback: 2 kits flagged** (gd-blade-trap, gd-stun-jacks — both negative=true). Availability API `http://archive.org/wayback/available?url=<URL>&timestamp=<YYYYMMDD>`; gd era→timestamp: base≈2016-2017 · aom≈2018 · fg≈2019-2020 · patch-era≈2021-2024. Wayback snapshots of grimtools calc pages are JS-shells — do not bother; wayback FORUM threads instead.
- Fully SOURCE_NOT_FOUND after honest search → record, move on (Unattested Register is a deliverable). GD community text is old-forum-shaped (long compendium threads) — one good compendium post can anchor several claim families; LE young-season kits (1.2/1.4) may be guide-sparse — honest UNSUPPORTED beats stretch-reading.

## Outputs (append per-kit as you go — crash durability)
Dir: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/vdm1/stage1/basin2/`
1. `batch-NN-verify.jsonl` — {kit_id, claim_family, claim_text, verdict, anchor_quote, source_url}
2. `batch-NN-citations.jsonl` — {kit_id, url, archive_url, site, author_handle, title, cite_class, rank_class, accessed_date, quarantined}
3. `batch-NN-dossier.jsonl` — {kit_id, family, payload_json (object|null), source_url, anchor_quote, abstained, conf}
4. `batch-NN-summary.md` — per-kit one-liners + verdict histogram + contradictions + SNF + dossier coverage + author credits

## Laws
- Commit PATHSPEC-ONLY (`git add` the 4 files exactly; never -A), message `legolas: VDM-1 basin-2 batch-NN — verify+citations+dossier (kits <START>-<END>)`. **Do NOT push** (steward pushes; parallel pushes race). index.lock → wait 30s, retry up to 3×.
- 0 contradictions across the batch → say so LOUDLY in the summary. >30% kits SOURCE_NOT_FOUND → stop grinding, report.
- Greppable tokens are NEVER emitted in negated form (stage-3 D-2d) — write "considered, not applicable" without the literal token.
- Return: verdict histogram, contradictions (one line each), SNF kits, dossier coverage %, red flags. Under 400 words. **Your returned histogram is ADVISORY — file truth is the count** (stage-3 D-2c; the steward recounts from your committed files).
