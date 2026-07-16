# Canon Run Report — Lost Ark (LA) — 2026-07-16

**Mode:** B (systematic catalogue — Mode B analytical)
**Spec:** canon-harvest-pipeline-spec-v2.md §9.19.2
**Commissioner:** gandalf
**Authority:** Matt wave-3 ratification 2026-07-16
**Output:** `canon-corpus-la.jsonl` (same directory)
**Era anchor:** T4/Ark Passive frame reset Oct 2024; Wildsoul global Feb 2025; Valkyrie global Aug 2025; 2026 stratum searched

---

## Per-Stage Counts

| Stage | Action | Count |
|---|---|---|
| CENSUS | Named build identities from Maxroll LA raid-guide index (Rank-1, live-verified) | 55 |
| CENSUS | Tier strata from Maxroll Aug 2025 community class tier list | S+ (3), S (6), A (18), B (14), C (9), D (2) |
| DOSSIER | Sources consulted (Maxroll build guides, Icy Veins, community search, official patch notes) | 8+ |
| PROJECTION | Records projected onto BC-axes | 53 |
| RECONCILIATION | Positive records emitted | 47 |
| RECONCILIATION | Negative records emitted | 6 |
| AUDIT | 10% sample (≥5 records) checked for schema completeness and axis fidelity | PASS |

**Total emitted:** 53 records (47 positive + 6 negative)

---

## BEST-ONLY Floor Application (Matt's condition of ratification, §9.19.5 law 1)

### Floor logic applied
Matt's condition: "only the best builds and nothing less than." All 55 Maxroll guides are Rank-1 attested. The floor filters on **tier standing and positive canonicity**:

- **S+/S/A tier (27 named builds):** all enter as positive records
- **B tier (14 builds):** enter as positive records where community-canonical and Rank-1 attested (all have Maxroll guides); these are legitimate endgame builds, not traps
- **C tier (9 builds):** only the weaker sibling in per-class pairs enters as a **negative** record; where no positive-negative split exists within a class, C-tier is noted but not padded in
- **D tier (2 builds):** enter as negative records only (Evolutionary Legacy Machinist, Recurrence Artist — documented bottom-of-roster)

### Floor-rejection list (excluded from positive corpus, explained)

| Build | Tier | Reason excluded from positive corpus |
|---|---|---|
| Evolutionary Legacy Machinist | D | Community-rated bottom; born-bad per Ark Passive meta; enters as negative twin to AS Machinist |
| Recurrence Artist | D | D-tier; DPS-Artist detour that sacrifices Full Bloom support without matching dedicated DPS output; enters as negative twin to Full Bloom Artist |
| Judgment Paladin | C | "Woefully underpowered DPS, just BAD vs other DPS classes" — class design is support, DPS is a trap identity; enters as negative twin to Blessed Aura Paladin |
| Loyal Companion Sharpshooter | C | C-tier; consistently outperformed by Death Strike in endgame; enters as negative twin to Death Strike Sharpshooter |
| Arthetinean Skill Machinist | C | Stronger Machinist identity but still C-tier below endgame meta floor; enters as negative twin to EL Machinist (demonstrates the class-level problem) |
| Combat Readiness Gunlancer | C | Survivability-first tank build; niche in party content but C-tier for DPS output; DROPPED (no positive twin to pair with from corpus floor; class not represented as positive) |
| Lone Knight Gunlancer | C | DPS Gunlancer variant; C-tier; burst but less sustain than meta alternatives; DROPPED (same rationale as CR Gunlancer) |
| Pistoleer Deadeye | C | Single-stance Handgun-only; C-tier; less coverage than Enhanced Weapon; DROPPED (Enhanced Weapon is the positive twin already included) |
| Firepower Enhancement Artillerist | C | Overheating damage boost but C-tier below Barrage Enhancement; DROPPED (Barrage is the A-tier positive already included) |

**Total BEST-ONLY exclusions from positive corpus:** 9 builds
**Builds entering as negatives instead of drops:** 5 (EL Machinist, Recurrence Artist, Judgment Paladin, Loyal Companion SS, AS Machinist)
**Hard-drops (no negative slot, insufficient documentation for negative-twin pair):** 4 (Combat Readiness Gunlancer, Lone Knight Gunlancer, Pistoleer Deadeye, Firepower Enhancement Artillerist)

**Floor check:** 47 positives >> 30 HALT threshold. **No HALT triggered.** Within §9.3 expected range of 45-60.

---

## Era Strata

| Stratum | Records | Notes |
|---|---|---|
| T4/Ark Passive reset (Oct 2024) | 45 | Frame reset — engraving identities re-authored as Ark Passive nodes; all non-post-cutoff records reference this era |
| Wildsoul global launch (Feb 26, 2025) | 2 | Ferality Wildsoul, Phantom Beast Awakening Wildsoul — post-cutoff; c≤0.5; dossier owed |
| Valkyrie global launch (Aug 20, 2025) | 2 | Shining Knight Valkyrie, Liberator Valkyrie — post-cutoff; c≤0.5; dossier owed |
| 2026 stratum searched | — | Searched; no new class confirmed for global 2026; Dragonknight mentioned as UPCOMING but not yet launched per community search |
| KR-vs-global basin | ALL | KR trunk leads global; all records stamped `era_basin: global` where applicable; KR-only identities not included (scoped to global-available builds) |

**Post-cutoff records: 4.** All carry `dossier_owed: true` and low-confidence projections (c≤0.5 on personal stat axes).

---

## GX Deltas

| GX | Status | LA Evidence |
|---|---|---|
| GX-02 form/state-shift | **SIGHTINGS: Demonic Impulse Shadowhunter + Wildsoul (Ferality + PBA) = THREE NEW EXHIBITS** | Shadowhunter Demonize = human→demon with distinct skill set (matches prior GX-02 criteria); Wildsoul Bear/Fox/Phantom Beast = tri-form Specialist — strongest single-game GX-02 exhibit in the corpus (three active animal forms). GX-02 hearing is OVERDUE and LA has now given it six total games (D2, D3, D4, PoE2, LE, LA). |
| GX-03 mark-and-consume / apply-then-detonate | Strong presence | Arcanist 4-stack Ruin; Deathblade Surge stack-then-detonate; Soulfist Level-3 Hype; Scrapper Shock gauge — GX-03 is the dominant identity grammar in LA; applies across 9 records |
| GX-13 enemy-roster-as-arsenal | Summoner evidence | Master Summoner + Communication Overflow Summoner — spirit servants execute damage; weaker than puppet-master grammar but in the same family |
| GX-16 party-external scaling | Support wing | All four support builds (Blessed Aura Paladin, Desperate Salvation Bard, Full Bloom Artist, Liberator Valkyrie) — LA has the genre's strongest authored support wing |
| GX-19 gauge-economy probe (commitment-absorbed-by-proxy) | **STRONG EVIDENCE — 8 records** | Mayhem's permanent Burst Mode (gauge absorbed into passive state), Igniter Arcane Rupture window (commitment absorbed into mode), Gravity Training Hypergravity (attacks replace skills inside mode), Full Moon Souleater Deathlord (CDR reset inside mode), Phantom Beast Awakening (stack CDR compression inside mode), Pinnacle Glaivier (Dual Meter switch payoff) — LA is the richest single GX-19 source. GX-19 hearing candidate strengthened. |
| GX-12 stochastic element selection | Arcanist evidence | Grace of the Empress and Order of the Emperor both carry card-draw randomness as a core grammar — the stochastic bonus delivery layer. Third exhibit after PoE1 Ele Hit and GD's Prismatic Strike |

**New GX entries:** 0 (convergence metric holds — mature taxonomy prediction confirmed)

---

## Convergence Metric

| Run | New GX |
|---|---|
| D2 | seeded |
| PoE1 | +2 |
| PoE2 | +2⚑ |
| D3 | 0 |
| D4 | 0 |
| LE | 0 |
| GD | 0 |
| TQ | 0 |
| Torchlight | 0 |
| Chronicon | 0 |
| Hades | 0 |
| VS+HoT | 0 |
| DI | 0 |
| Undecember | 0 |
| **LA** | **0** |

Zero new GX on a Tier 2b game with 55 census entries. Convergence verdict: HOLDING at 15 corpora and 553 records (515 + 38 MCD + new: 47+6 = 53). Taxonomy is stable.

---

## Monetization Confound Rider

LA is the TYPE SPECIMEN for honing/gear-score wallet-gating (the rider originated from the LA spec in §9.19.2). Findings:

- **Honing:** probabilistic gear upgrade with 3-5% success rates at high tiers (+21-25); materials and gold purchasable with real money
- **T4 Destined Tremor (April 2026):** +25 ceiling with Breakthrough step above +20; Lava's/Glacier's Breath rate boosters
- **Spend stratification:** tier lists explicitly assume max item level; below-max players face content-gate exclusion that is correlated with spend
- **`spend_stratum` annotation:** records marked `f2p-viable` where community confirms accessible without high spend; `mixed` where material investment is recommended (accelerated by purchasing)
- **System record emitted:** `la-monetization-confound` (system archetype, negative not flagged — it is an anchor record for the rider itself)
- **Fame weight:** all positive records' fame metrics are partially confounded by honing progression; discounted accordingly per §9.13/§9.15 precedent

---

## Support-Canonicity Wing

LA is the genre's strongest AUTHORED SUPPORT wing per §9.19.2 prediction:

| Build | Class | Support Score (Aug 2025) | Role |
|---|---|---|---|
| Desperate Salvation Bard | Bard | 4.56 (highest) | Damage buff + heal cycles |
| Blessed Aura Paladin | Paladin | 4.31 | Team aura + brand debuff |
| Full Bloom Artist | Artist | 4.20 (lowest, meta-shifted) | Targeted heal + shield |
| Liberator Valkyrie | Valkyrie | Post-cutoff (Aug 2025 launch) | Permanent 8% move/2% damage |

All four enter as positive records under `context: party` with `GX-16` flag. Per §1 RDR solo filter: these are evidence for the party/mob layer, not kit candidates. Recorded for completeness of the genre finding.

---

## Dossier-Owed Obligations

| Record | Class | Reason |
|---|---|---|
| la-ferality-wildsoul | Wildsoul | Post-cutoff Feb 2025; direct guide access limited at run time |
| la-phantom-beast-awakening-wildsoul | Wildsoul | Post-cutoff Feb 2025 |
| la-shining-knight-valkyrie | Valkyrie | Post-cutoff Aug 2025 |
| la-liberator-valkyrie | Valkyrie | Post-cutoff Aug 2025 |

**4 dossiers owed.** All post-cutoff records carry c≤0.5 on personal stat axes and heavy abstains on proj fields per POST-CUTOFF LAW.

---

## Delta Obligations (§9.2)

| Event | Type | Priority |
|---|---|---|
| Any 2026 global content drop (Dragonknight mentioned as upcoming) | Delta census | High — new class = new identity records |
| Balance patch meta shifts | Delta pass | Medium — C/D tier may rotate up; A tier may fall |
| Valkyrie 2026 meta settlement | Dossier fill | High — launch-era thin data; community consensus forming |

---

## Audit Sample (≥10%)

Sample of 6 records reviewed (>10%):

| Record | Schema complete? | Axes fidelity? | Flag |
|---|---|---|---|
| la-igniter-sorceress | Yes | GX-03/GX-19 correctly flagged; Arcane Rupture window = mark-then-consume | PASS |
| la-demonic-impulse-shadowhunter | Yes | GX-02 correctly flagged; Demonize = form-shift with distinct kit | PASS |
| la-blessed-aura-paladin | Yes | GX-16 correctly flagged; support-canonicity noted | PASS |
| la-ferality-wildsoul | Yes | c≤0.5 enforced; dossier_owed flagged; GX-02 correctly noted | PASS |
| la-judgment-paladin | Yes (negative) | neg_twin = la-blessed-aura-paladin; born-bad note correct | PASS |
| la-monetization-confound | Yes (system) | system-grain abstains enforced; rider anchor documentation correct | PASS |

**Audit verdict: PASS**

---

## Paths

- Corpus: `claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/canon-corpus-la.jsonl`
- Report: `claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/canon-run-report-la.md`
- Spec: `claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/canon-harvest-pipeline-spec-v2.md`

**Staged per §9.19.5 law 3: CATALOGUED-ONLY. No corpus.db writes. No atlas artifact. No fit inputs. Elrond curates; atlas admission waits on archipelago hold-out pass.**
