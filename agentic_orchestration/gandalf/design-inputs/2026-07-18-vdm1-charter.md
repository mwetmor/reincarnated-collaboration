# VDM-1 — VERIFY + DOSSIER + MAP: unified corpus run charter

> **STATUS:** CURRENT (load-bearing as of 2026-07-18) — the constitution of the VDM-1 autonomous run.

**Date:** 2026-07-18
**Author:** gandalf (ELICITOR → SPEC-AUTHOR; run steward)
**Status:** v1 — RATIFIED, run launching
**Authority:** Matt 2026-07-18 — rulings R-1..R-9 (R-10 dissolved by events; see § 2). Supersedes-extends `claude-mobile-session-docs/ARPG-canonical-kit-research/rdr-verify-1-recommendation.md` (VERIFY-1 memo), whose verification framework is absorbed intact per R-1.
**Companion docs:**
- `claude-mobile-session-docs/ARPG-canonical-kit-research/rdr-verify-1-recommendation.md` — the verification framework (absorbed; its §1 triage, §2 claim model, §5 laws, §7 priors all bind)
- `agentic_orchestration/research/curated/corpus.db` — the substrate (elrond single-writer)
- `canonical/current-to-end-state/current-to-end-state-engine.md` — census V10 state (97.5% expressible-now)
- `agentic_orchestration/gandalf/design-inputs/2026-07-16-shapeshift-gx02-docket.md` — the one open mechanism docket (D-05; enriched by this run, not ruled by it)
- `canonical/matt_decision_needed/2026-07-13-ip-clearance-devlog-and-hook-surface.md` — gates the devlog citation *export* only (not the crawl)

---

## 0. TL;DR

One crawl, three harvests, one authoring pass. Each of the 585 corpus records is fact-checked against located sources (four verdicts, quoted anchors), its citation captured (URL + archive + author + class), its compile dossier extracted (skill loop, geometry verbatim, item/capstone alterations, variants — abstain where the source is silent), and its **engine-mapping authored on our side** (motion_frame, t4_doors, substrate flags) to a graded fidelity. Every kit reaches a terminal state; no simulation code is written in-run. PoE1's 94 records first — patch 3.29 lands **July 24** and churns their sources forever. Matt's single touchpoint: THE REVIEW BOOK at run end (R-8b); red-flag pings only, otherwise autonomous, push-as-you-go (R-9).

---

## 1. Matt rulings of record (2026-07-18)

| # | Ruling |
|---|---|
| R-1 | **Unified charter** — verification + citation + dossier + mapping ride one crawl (the one-bird thesis; churn hits all payloads equally) |
| R-2 | **Dossier depth: middle tier** — loop + geometry + alterations (Bar-2 sufficient; Bar-3 exhaustive rejected) |
| R-3 | **PoE1 with full extraction before July 24** — cut breadth (small basins), never depth, if pressed |
| R-4 | **PoE1 tranche doubles as V-0 calibration** — priors + cost model graded at its close; remaining ~490 re-planned against measurement |
| R-5 | **D-01 RESOLVED: two-mode emission** — `faithful` (per-kit graded capability, unlocked by dossier grade) + `generative` (all kits, coordinate-driven); three fidelity bars with Bar-3 (numeric parity) excluded; no-fabrication law |
| R-6 | **"Complete the engine-mapping" = MAPPED (data only).** Terminal states: MAPPED or MAPPED+DOCKET. New simulation behavior ships post-run via normal seams and gates — never inside this run |
| R-7 | **Parsimony ladder ratified as written** (§ 5) — quantitative mints free + ledgered; qualitative mints docket-only from the named roster, or ≥3-build evidence for novel classes |
| R-8 | **(b) end-of-run review** — no per-basin pings; everything compiles into THE REVIEW BOOK; calibration checkpoint self-adjudicates against pre-registered thresholds |
| R-9 | **Push-as-you-go authorized** (per-basin checkpoint commits + push; pathspec-only on `git add` AND `git commit` per Discipline #62) |
| R-10 | **DISSOLVED** — proxy fork resolved by events (Matt 2026-07-06 Option 1 → Waves A/B/C landed, census V10 97.5%); shapeshift = 3 kits → MAPPED+DOCKET into GX-02 |
| — | **Mode C** (player-raised composition) — tossed for now per Matt; parked note, zero planning weight |

## 2. Corpus state at launch (measured 2026-07-17/18)

- 585 canon_corpus rows · 565 census denominator (system/meta excluded) · **V10: 551/565 expressible-now (97.5% — spec ceiling)**
- Probe facts: 478/585 kits × 10 families, conf 0.67–0.74 · **107 kits zero probe facts** (53 = Lost Ark)
- **source_urls: 60/585 (~10%)** · **sources_used: 403/478 = 84% kb-memory-only, zero fetched URLs** — the corpus is a projection of model belief, verified nowhere; the kb-contradiction delta (VERIFY-1 §7 sleeper study) is a first-class deliverable
- Engine-native mapping columns (`motion_frame`, `t4_doors`, `option_c_substrate_flags`): **0/585 — this run's authoring surface**
- `core_skills` exists in the mobile JSONL (1–3 names/kit) but never landed in the DB — Stage-0 ingestion fix (elrond)
- `mobile_blocking_mechanics` flags are a 2026-07-12 snapshot **pre-dating Waves A/B/C** — stale; refreshed during probe backfill, never trusted as current truth

## 3. The four output streams (one crawl feeds all)

1. **VERDICTS** — VERIFY-1 §2 claim model intact: identity / mechanics / era / negative-canon claims; four-value vocabulary (CONFIRMED · CONTRADICTED → errata · UNSUPPORTED → partition analysis · SOURCE-NOT-FOUND → Unattested Register). Verdicts judge *fetched text only*, quoted audit anchors mandatory. In-place v1 → v1.1; errata ledger; no silent edits.
2. **CITATIONS** — per source: URL + Wayback/archive snapshot + site + author handle + access date + class: `authored` / `communal` (folk builds — credit wiki/community) / `official` (dev-published) / `dataset` (poe.ninja class). Junk-tail domains quarantine-only. **A citation exists only if the page was fetched live this run** — never from memory.
3. **DOSSIER** (extraction — new structured content, source vocabulary, R-2 middle tier):
   - skill loop (core + supports/auras/curses/triggers as the guide names them)
   - skill geometry verbatim (shape, radius/range, projectile count, zone size, cadence — descriptive lineage, not tuning targets)
   - item-alterations (items that change what the skill *is*)
   - capstone-alterations (ascendancy/paragon choices altering skill behavior — raw material for T4-door authoring)
   - author-credit block (→ stream 2)
   - variants (optional family — budget/alternate-element/boss-killer listings when guides carry them)
4. **MAPPING** (our-side authoring, gandalf): per kit — `motion_frame`, `t4_doors`, `option_c_substrate_flags`, skill/element/scaffold coordinates via the crosswalk tables; fidelity grade **EXACT / CLOSE / APPROX / GAPPED** + deviation notes.

**Epistemics wall between streams 1–3 and 4:** extraction speaks only what the page says (silence stays NULL — the no-fabrication law); mapping is design judgment *over* extracted truth and is labeled as such (`mapping_provenance: authored-vdm1`). Conf-provenance tags separate `verified-v1.1` from legacy `kb` everywhere.

## 4. Terminal states (R-6)

Every kit-grain row (negatives/graveyard INCLUDED — boss-emission-ready per D-02) reaches exactly one:

- **MAPPED** — full mapping authored in current + quantitatively-expanded space, graded EXACT/CLOSE/APPROX
- **MAPPED+DOCKET** — mapping authored as far as the space reaches + a mechanic-gap docket (spec + build-evidence roster). Known docket destinations: shapeshift → GX-02 (3 kits). Implementation is post-run seam work (gamora/rocket, normal gates)

Zero kits unexamined; zero mechanisms unspecified; zero sim code written in-run.

## 5. The parsimony ladder (R-7, applied in order per kit)

1. **Map** in existing space →
2. **Approximate + fidelity note** (loop preserved, texture deviates — recorded, never hidden) →
3. **Quantitative mint** (skill slots, chain length, T4 door count) — free under Matt's pre-ratification, every mint = one `mint_ledger` row (what, which builds forced it, ladder-step audit) →
4. **Qualitative mint** (new mechanism class) — **docket + spec only**, from the named residual roster (post-V10 tail: shapeshift 3 · fidelity-deferred items on the Wave-D ledger) or, for a genuinely novel class, **≥3 distinct builds** blocked on the same mechanism; else it stays a fidelity note.

**Tripwire:** mint-rate above pre-registered expectation halts the basin → red-flag ping.

## 6. Sequencing + calibration

**PoE1's 94 first** (hard fire: 3.29 lands July 24; league churn + Wayback friction forever after). Then: post-cutoff strata (links days-fresh) → database-keyed GD/LE → kb deep canon (d2/d3/d4 — the sleeper-study basins) → **LA harvest-grade** (53 no-probe kits; official-class sources) → small basins → residue triage. The 107 no-probe kits get harvest-grade probe authoring (fetched-evidence conf, not kb); 45 "no rule matched" + 70 unclassified get classified in-lane.

**Calibration checkpoint (post-PoE1, self-adjudicating under R-8b):** grade VERIFY-1 §7 priors (identity ~.97 · core skills ~.90 · key items ~.85 · era ~.85 · negative-canon ~.95) + kb-contradiction delta + extraction cost (+25–40% estimate) + mint-rate. **Rubber-stamp detector binds: ~0% contradiction = the run failed, re-audit the verifier.** Within thresholds → continue autonomously. Breach → red-flag ping Matt with the numbers.

**Red-flag halts (only Matt-pings in the run):** contradiction-rate breach (either direction) · mint-rate explosion · SOURCE-NOT-FOUND ≫ expected (search-spec failure) · any single-writer or grain-law violation.

## 7. Seam routing

| Who | Does | Never |
|---|---|---|
| **legolas** | Mode-A crawl: locate/fetch/archive; verdict evidence; extraction payloads → returned artifacts | writes corpus.db |
| **elrond** | single-writer ingest; schema landing zone (`kit_dossier`, `kit_citations`, `verify_ledger`, `kit_mapping`, `mint_ledger`, `mechanic_gap_docket`); Stage-0 ingestion fixes; errata application | judgment calls on mapping |
| **gandalf** | run stewardship; crosswalk tables (element incl. physical/chaos-class · supports → {chain-links, traits, affixes} · items → gear-affix lane); mapping authoring + grades; REVIEW BOOK | production/sim code |
| **rocket / gamora** | consulted on generation-space fit / docket sim-expressibility | in-run code changes |

Wayback snapshotting per citation URL is in-charter (benign external write; citation durability is the run's point). Legolas needs no API key (WebSearch/WebFetch as agent tooling).

## 8. Deliverables

v1.1 corpus + errata ledger · Unattested Register · fact/judgment partition (per-axis UNSUPPORTED aggregation) · calibration report (priors vs measured + kb-memory delta) · mapping-coverage histogram (by grade) · mint ledger · gap dockets (GX-02 enriched) · 10% blind re-projection rider on judgment-grade axes (post-partition) · **devlog citation export** (ships within whatever the 2026-07-13 IP-clearance decision rules) · **THE REVIEW BOOK** (R-8b — the single end-of-run Matt review: every mapping by grade with deviations, all mints, all dockets, all errata, the honest residue).

## 9. Run mechanics

Ledger file: `agentic_orchestration/gandalf/notes/2026-07-18-vdm1-run-state.md` (stage table + per-basin rows; the interruptible spine). Commits auto-fire per team discipline; push per basin checkpoint (R-9); **pathspec-only on add AND commit** (Discipline #62). Trust-but-verify at ARTIFACT level on every agent return. corpus.db reads outside elrond: `sqlite3 -readonly` only.

---

## Cross-references

Decision lineage: D-01 (resolved per R-5) · D-02 (graveyard mapped, boss-lane) · D-05 (GX-02 docket — enriched, not ruled) · D-07 (dissolved by events: Matt 2026-07-06 Option 1 + Waves A/B/C + census V10) · VERIFY-1 memo (absorbed) · One Realm MVP (emission remains downstream of this run; this run authors *data readiness*, not emission).

Tracker-delta: new run row → `current-to-end-state-engine.md` PART-forward (VDM-1 launched: corpus v1→v1.1 + citations + dossiers + mappings owed; PoE1 deadline July 24) — gandalf writes at first basin checkpoint.

---

**Signed:** gandalf (run steward)
**For:** turning a remembered corpus into a cited, verified, compile-ready one — one crawl, three harvests, one authoring pass.
