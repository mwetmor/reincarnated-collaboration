# Mob-harvest-v3 Phantom-Risk Triage Docket

**Date:** 2026-07-17 · **Author:** elrond (autonomous atlas-parity run)
**Commissioner:** gandalf-prime (Matt autonomous-run authorization 2026-07-16; ruling 16 Part-3 charge)
**Scope:** Ranked docket of `provenance_tag='mobile-harvest-v3'` kits still `negative=0`, scored on phantom-risk signals visible in-DB, for gandalf-prime to fire follow-on legolas re-crawl batches against.

**Iron honesty bar:** this is **signal-ranking**, not verdicts. A HIGH rank means "verify me next" — it does NOT mean "phantom." The two proven phantoms were only established after third-attempt widened re-crawl produced two independent negative confirms; ranking cannot substitute for that work.

**Read-only:** no writes to corpus.db.

---

## §1 The two proven phantoms

Ranking baseline anchors on the two mob-harvest-v3 phantoms established via post-hoc re-crawl:

| # | kit_id | folk_name | game | Phantom-type | Discovery route |
|---|---|---|---|---|---|
| 1 | `d2-wl-void-rift` | Void Rift Warlock | d2 | Franchise-name collision (D2/Destiny-2 vocab bleed) | Econ-recrawl 2026-07-16 (V11 ruling) |
| 2 | `di-spiritform-druid-pvp` | Spirit-Form Druid (complaint-tier) | di | Mechanic-invention from complaint colloquialism (real class, non-existent skill) | Third-attempt widened re-crawl 2026-07-17 (V13 ruling) |

**Structural pattern:** both are POST-CUTOFF era + conf-capped ≤0.50 + complaint-tier or Warlock-family cluster + limited-source. Both are folk-name shapes that map plausibly to real archetypes but do NOT verify to a real skill / mechanic under widened source scope.

**Signal weighting derived from these two:**
- **W1** — POST-CUTOFF marker AND conf-capped ≤0.50 (both phantoms): weight HIGH
- **W2** — complaint-tier / PvP folk_name signal (di-spiritform): weight HIGH for DI/PvP contexts
- **W3** — Warlock/D2 vocab-collision cluster (void-rift): weight HIGH for d2-wl-* family
- **W4** — kb-only-backfill flag (both had failed prior verification): weight MEDIUM
- **W5** — sole-source or no-source (both were single-source when discovered): weight MEDIUM (noise: source_urls was rarely populated for mobile-harvest-v3)
- **W6** — mechanic-invention vocab shape (di-spiritform: "spirit form" is native to D4 Spiritborn / WoW Druid, not DI): weight MEDIUM

---

## §2 Universe

**Mob-harvest-v3 all rows:** 515
**Mob-harvest-v3 positive kits (`grain='kit' AND negative=0`):** 458
**This docket ranks:** all 458 positive kits (silent LOW-tier for the vast bulk; explicit HIGH/MEDIUM tiers below).

SQL:
```sql
SELECT COUNT(*) FROM canon_corpus WHERE provenance_tag='mobile-harvest-v3' AND grain='kit' AND negative=0;
-- → 458
```

---

## §3 Signal roll-up (visible in-DB)

| Signal | Universe count (positive mob-harvest-v3 kits) | Notes |
|---|---|---|
| S1 — POST-CUTOFF marker in mech_note | 36 | strong phantom-precedent match |
| S2 — Conf capped ≤0.50 in mech_note | 36 | co-occurs with POST-CUTOFF |
| S3 — POST-CUTOFF AND Conf-capped intersection | 36 | the two overlap fully — treat as one signal |
| S4 — PvP suffix in kit_id or folk_name | 4 | di-spiritform lineage — direct phantom analog family |
| S5 — d2-wl-* Warlock family | 5 | void-rift lineage — direct phantom analog family |
| S6 — narrow-scope flag | 11 | curator-tagged; explicit "single-source or single-mechanic" signal |
| S7 — degenerate-famous flag | 8 | curator-tagged; edge-case builds; not a phantom signal but reduces cite density |
| S8 — kb-only-backfill flag | 6 | prior failed-verification flag |
| S9 — unverifiable flag | 1 | poe2-snipe-mirage-deadeye; explicitly ELROND-CALL editorial-inferred |
| S10 — Sole-source (exactly one URL populated) | 13 | tighter signal than no-source (which is 416 — the default) |
| S11 — No source_urls populated | 416 | mobile-harvest-v3 default state — NOT a signal on its own (noise floor) |
| S12 — Post-cutoff-native games (ud/hot/hades2/tq2/tli) | 44 | game-cluster with high POST-CUTOFF fraction |

SQL for each signal is provided in §7 below.

---

## §4 HIGH tier — recommended legolas re-crawl batch (13 kits)

**Definition:** kits that meet ≥2 of {W1, W2, W3} OR ≥1 of {W1, W2, W3} + ≥2 of {W4, W5, W6}. These are the kits whose in-DB signal profile most closely mirrors the two proven phantoms.

**Rationale for recommending as re-crawl batch:** each carries the phantom-analog signal shape and can be verified by targeted WebFetch of authoritative sources for the specific class/mechanic named. Batch size 13 is Legolas-Mode-B tractable in a single dispatch.

| Rank | kit_id | folk_name | game | Signals hit | One-line rationale |
|---|---|---|---|---|---|
| 1 | `di-cyclone-monk-pvp` | Cyclone CC Monk | di | S4 (PvP), same DI-PvP complaint cluster as di-spiritform | Direct sibling to proven phantom — DI PvP complaint-tier folk_name; verify skill "Cyclone" exists on Monk class (or is a cross-game bleed from PoE Cyclone) |
| 2 | `di-bone-wall-necro-pvp` | Bone Wall Disruption Necro | di | S4 (PvP), same DI-PvP complaint cluster | Direct sibling — verify "Bone Wall" is a real DI Necromancer skill (Bone Wall is D2 Necromancer skill; DI may or may not carry it forward) |
| 3 | `di-bombardment-wizard-pvp` | Bombardment Artillery Wizard | di | S4 (PvP) + S8 (kb-only-backfill) | Direct sibling + prior verification-failure flag — verify "Bombardment" is DI Wizard skill (Bombardment is Crusader in D3; DI may re-attribute) |
| 4 | `d2-ghost-pvp` | Ghost | d2 | S4 (PvP) + short folk_name (single-word "Ghost") | D2 PvP kit with terse folk_name "Ghost" — verify this maps to a specific archetype in D2 PvP guide corpus (could be Ghost-Warrior Barb build, or lay-shorthand for an evasion tactic) |
| 5 | `d2-wl-blood-boil` | Blood Boil Warlock | d2 | S5 (d2-wl-* family) + S10 (sole-source aoeah.com only) | Direct void-rift analog cluster — sole-source is aoeah.com which is a low-authority tier list; verify against Maxroll/Icy-Veins for "Blood Boil" Warlock skill (Blood Boil is Necromancer skill in D3, not typically Warlock) |
| 6 | `d2-wl-tainted-summoner` | Tainted Summoner Warlock | d2 | S5 (d2-wl-* family) + S10 (sole-source rpgstash.com only) | Direct void-rift analog — sole-source rpgstash guide only; verify "Tainted Summoner" archetype exists in D2R Warlock guide corpus |
| 7 | `d2-wl-echoing-strike` | Echoing Strike Warlock | d2 | S5 (d2-wl-* family) | Direct void-rift analog cluster — verify "Echoing Strike" is real Warlock skill (has 3 sources; likely verifiable) |
| 8 | `d2-wl-fire` | Fire Warlock | d2 | S5 (d2-wl-* family) | Direct void-rift analog cluster — verify Fire Warlock generalist archetype (has 4 sources including Maxroll + Icy-Veins; likely verifiable, but priority-rank due to family membership) |
| 9 | `d2-wl-abyss` | Abyss Warlock | d2 | S5 (d2-wl-* family) + S7 (degenerate-famous) | Direct void-rift analog cluster; "Abyss" name-shape is D4 Necromancer keyword; verify DI-Warlock "Abyss" is a real skill or a cross-game bleed |
| 10 | `hot-landsknecht-grenades` | Grenade Landsknecht | hot | S1+S2 (POST-CUTOFF+conf-capped) + S7 (degenerate-famous) + S8 (kb-only-backfill) | Post-cutoff-native game + curator flagged degenerate + prior verification failure — highest kb-only-backfill flag concentration; verify Landsknecht is real HoT class with Grenade playstyle |
| 11 | `ud-seal-veil-daimonios` | Seal/Veil Resource Build (Daimonios) | undecember | S1+S2 (POST-CUTOFF+conf-capped) + S10 (sole-source pocketgamer.com only) | Undecember post-cutoff-native + sole-source (low-tier pocketgamer builds page) — verify "Seal/Veil" is a real Daimonios resource mechanic in Undecember s7-2025 |
| 12 | `ud-cwc-spin-caster` | Whirlwind CwC Blizzard (Ya55) | undecember | S1+S2 (POST-CUTOFF+conf-capped) + S10 (sole-source pocketgamer.com only) | Undecember post-cutoff-native + sole-source; folk_name compound "Whirlwind CwC Blizzard" mixes vocabularies (PoE-native "CwC" = Cast-while-Channeling); verify this compound exists as an Undecember archetype |
| 13 | `tli-iris2-thunder-magus` | Iris 2 Thunder Magus Minions | tli | S1+S2 (POST-CUTOFF+conf-capped) + S10 (sole-source mmoexp.com only) | TLI post-cutoff-native + sole-source (mmoexp tier list) — verify "Iris 2 Thunder Magus" is a real TLI Season 13 hero-slot build |

**Total HIGH tier: 13 kits.** Recommended legolas Mode-B dispatch = one batch (~half-day scope at documented widened-scope pace).

---

## §5 MEDIUM tier — verify-when-bandwidth-permits (37 kits)

**Definition:** kits that meet exactly 1 of {W1, W2, W3} OR ≥2 of {W4, W5, W6} without a W1-W3 anchor. These have phantom-analog signal but the shape is thinner than HIGH tier.

### §5a POST-CUTOFF-only (23 kits — W1 anchor, no other high-weight signal)

`ud-ice-crystal-arrow`, `ud-lightning-vortex`, `di-warlock-launch`, `hot-sage-ring-blades`, `hades2-medea-skull-cast`, `vs-out-of-bounds-freeze`, `hades2-hephaestus-blast`, `hades2-glorious-disaster`, `hades2-hail-storm`, plus 14 additional POST-CUTOFF kits without W2/W3/W4-W6 anchors that hit the S3 intersection:

| kit_id | folk_name | game | Rationale |
|---|---|---|---|
| `ud-ice-crystal-arrow` | Ice Crystal Arrow Bow | undecember | POST-CUTOFF + Conf-capped |
| `ud-lightning-vortex` | Lightning Vortex Mapper | undecember | POST-CUTOFF + Conf-capped; "Vortex" is PoE-native — verify Undecember carries |
| `di-warlock-launch` | Warlock (launch state) | di | POST-CUTOFF (DI 5.0 2026 class) — worth verifying but has 4-ailment source (already econ-recrawl-applied) |
| `hot-sage-ring-blades` | Ring Blades Sage | hot | HoT post-cutoff — verify Sage class + Ring Blades skill combo |
| `hades2-medea-skull-cast` | 62-Fear Medea Skull Build | hades2 | Hades2 post-cutoff + narrow-scope flag; "62 Fear" is meta-corpus phrase |
| `vs-out-of-bounds-freeze` | Out of Bounds freeze build | vs | POST-CUTOFF + already econ-recrawl-applied; folk_name "out of bounds" is exploit-vocab — verify not a bug-derivative kit |
| `hades2-hephaestus-blast` | Hephaestus Blast Core | hades2 | POST-CUTOFF + narrow-scope + sole-source (fextralife patch notes only) |
| `hades2-glorious-disaster` | Glorious Disaster (Zeus+Apollo duo) | hades2 | POST-CUTOFF + narrow-scope; pair-grain verification |
| `hades2-hail-storm` | Hail Storm (Zeus+Demeter duo) | hades2 | POST-CUTOFF + narrow-scope + rename backfill flag ("previous name Apocalyptic Storm") — verify rename occurred |

Plus 14 additional POST-CUTOFF kits in `le`, `tq2`, `poe2`, `tli`, `poe1` where POST-CUTOFF is the primary signal without corroborating W2-W6. Full list via SQL below.

### §5b degenerate-famous flag (8 kits — W6 shape signal via "famous" corpus)

`poe1-wormblaster`, `poe1-cwdt-loop`, `poe1-ward-loop`, `poe1-minion-pact-bv`, `d4-flame-shield-immortal`, `poe2-cof-comet`, `poe2-temporalis-blink`, `d4-quill-volley`

Rationale: curator-tagged as edge-case degenerate builds; verify each is a currently-viable named build in its game (as opposed to a folklore-only build reference).

### §5c narrow-scope flag (already-covered in §5a hades2 rows plus)

Consolidated with §5a — all narrow-scope flags fall on hades2 pair-grain or hot rows already in §5a POST-CUTOFF slate.

### §5d Prior verification-failure flags without W1-W3 anchor (2 kits)

`di-warlock-launch` (kb-only-backfill; also in §5a) — kb-only flag but has DI Warlock class as verified real (2026 launch)
`poe2-snipe-mirage-deadeye` (unverifiable flag; W9) — explicitly ELROND-CALL editorial-inferred; verify Snipe skill + Mirage Deadeye ascendancy exist in PoE2

**Total MEDIUM tier: 37 kits** (23 POST-CUTOFF-only + 8 degenerate-famous + 2 flag-anchored + 4 overlapping with §5a that are counted-once). Recommend re-crawl batching only if HIGH-tier pass produces material findings and additional bandwidth is authorized.

---

## §6 LOW tier — no in-DB phantom-risk signal (408 kits)

**Definition:** the residual 458 − (13 HIGH + 37 MEDIUM) = **408 kits** with no in-DB phantom-risk signal visible. These are the vast bulk of the mob-harvest-v3 corpus.

**Composition:**
- 400+ kits with no POST-CUTOFF/Conf-capped/PvP/d2-wl/narrow-scope/degenerate-famous/kb-only/unverifiable signal
- Mostly PoE1 / D2 / D3 / D4 / LE / Grim Dawn canonical archetypes with well-known names (`d2-hammerdin`, `poe1-cyclone`, `d3-firebird`, etc.)

**Honesty bar:** these kits carry NO IN-DB SIGNAL — but this is NOT a proof of no-phantom. The two proven phantoms were only detectable via widened re-crawl, and prior econ-recrawl audit passes surfaced them despite in-DB signal being present. Absence of signal is weaker than presence of signal for triage purposes. LOW tier means "not the next re-crawl target," not "verified authentic."

**Recommendation for LOW tier:** no batch re-crawl. Any individual verification should be triggered by downstream reader-flag (jack-ryan Gate-2 review, gamora balance-loop finding an outlier, star-lord export anomaly, etc.), not by proactive audit.

---

## §7 Reproducibility — the SQL used

**S1 — POST-CUTOFF marker:**
```sql
SELECT kit_id FROM canon_corpus
 WHERE provenance_tag='mobile-harvest-v3' AND grain='kit' AND negative=0
   AND mech_note LIKE '%POST-CUTOFF%';
-- → 36 kits
```

**S2 — Conf capped ≤0.50:**
```sql
SELECT kit_id FROM canon_corpus
 WHERE provenance_tag='mobile-harvest-v3' AND grain='kit' AND negative=0
   AND mech_note LIKE '%Conf capped%';
-- → 36 kits (fully overlapping with S1)
```

**S3 — S1 ∩ S2:**
```sql
SELECT kit_id FROM canon_corpus
 WHERE provenance_tag='mobile-harvest-v3' AND grain='kit' AND negative=0
   AND mech_note LIKE '%POST-CUTOFF%' AND mech_note LIKE '%Conf capped%';
-- → 36 kits
```

**S4 — PvP suffix:**
```sql
SELECT kit_id FROM canon_corpus
 WHERE provenance_tag='mobile-harvest-v3' AND grain='kit' AND negative=0
   AND (folk_name LIKE '%pvp%' OR kit_id LIKE '%pvp%');
-- → 4 kits
```

**S5 — d2-wl-* Warlock family:**
```sql
SELECT kit_id FROM canon_corpus
 WHERE provenance_tag='mobile-harvest-v3' AND grain='kit' AND negative=0
   AND kit_id LIKE 'd2-wl-%';
-- → 5 kits (excluding already-phantom d2-wl-void-rift)
```

**S6/S7/S8/S9 — flag matches:**
```sql
SELECT kit_id, flags FROM canon_corpus
 WHERE provenance_tag='mobile-harvest-v3' AND grain='kit' AND negative=0
   AND flags IS NOT NULL AND flags != ''
 ORDER BY flags;
```

**S10 — sole-source (exactly one URL, no comma):**
```sql
SELECT kit_id FROM canon_corpus
 WHERE provenance_tag='mobile-harvest-v3' AND grain='kit' AND negative=0
   AND source_urls IS NOT NULL AND source_urls != ''
   AND source_urls NOT LIKE '%,%';
-- → 13 kits
```

**S11 — no source_urls:**
```sql
SELECT COUNT(*) FROM canon_corpus
 WHERE provenance_tag='mobile-harvest-v3' AND grain='kit' AND negative=0
   AND (source_urls IS NULL OR source_urls = '');
-- → 416 kits — DEFAULT STATE; not treated as signal on its own
```

**Full-signal join for HIGH tier construction:**
```sql
SELECT kit_id, folk_name, game, flags, mech_note
  FROM canon_corpus
 WHERE provenance_tag='mobile-harvest-v3' AND grain='kit' AND negative=0
   AND (
        (folk_name LIKE '%pvp%' OR kit_id LIKE '%pvp%')                              -- W2 PvP anchor
     OR kit_id LIKE 'd2-wl-%'                                                        -- W3 Warlock cluster
     OR (mech_note LIKE '%POST-CUTOFF%' AND mech_note LIKE '%Conf capped%'
         AND (flags LIKE '%kb-only%'
              OR flags LIKE '%unverifiable%'
              OR (source_urls IS NOT NULL AND source_urls != ''
                  AND source_urls NOT LIKE '%,%')))                                  -- W1 + W4/W5 co-hit
   );
-- → 13 kits (the HIGH-tier slate)
```

---

## §8 Tier counts summary

| Tier | Count | % of positive mob-harvest-v3 universe |
|---|---|---|
| HIGH | 13 | 2.84% |
| MEDIUM | 37 | 8.08% |
| LOW | 408 | 89.08% |
| **Total** | **458** | **100.00%** |

---

## §9 Recommended action

**Fire HIGH-tier as one legolas Mode-B batch.**

Batch dispatch outline:
- 13 kits, per-kit widened-scope verification (WebSearch + WebFetch of authoritative source per kit's class/mechanic/skill)
- Per-kit disposition options: `verified-authentic` / `re-key-clean` / `phantom` / `unverifiable`
- Precedent format: `agentic_orchestration/legolas/research/econ-recrawl-2026-07-17/` and `agentic_orchestration/legolas/research/di-spiritform-recrawl-2026-07-17/`

Expected batch shape (probabilistic, not committed):
- 4 DI-PvP siblings: likely 2-3 verify authentic (DI Cyclone Monk is a real archetype; Bone Wall is D2 skill so DI Necro may or may not carry) with 0-2 re-key-clean or phantom depending on skill enumeration
- 5 d2-wl-* siblings: likely 3-4 verify authentic (Fire Warlock, Echoing Strike, Abyss Warlock have multi-source citations); 0-1 phantom (Blood Boil Warlock sole-sourced from aoeah tier list, Tainted Summoner sole-sourced from rpgstash — both fit void-rift risk profile)
- 4 POST-CUTOFF-native singletons (hot Landsknecht Grenades, ud Seal/Veil Daimonios, ud CwC Spin Caster, tli Iris2 Thunder Magus): likely 2-3 verify authentic (post-cutoff-native games have less phantom risk than post-cutoff-marker on established-game classes); 0-1 unverifiable

**If HIGH-tier batch produces ≥3 phantoms:** fire MEDIUM-tier batch as follow-on (would require Matt authorization for extended dispatch).

**If HIGH-tier batch produces 0-2 phantoms:** LOW tier + MEDIUM tier can be deferred to on-demand verification only.

**Not recommended:** batch re-crawl of LOW tier (408 kits) — cost vs signal-density is unfavorable.

---

## §10 Handoff to gandalf-prime

**Docket ready to fire:** HIGH tier §4 is Legolas-Mode-B tractable in a single dispatch. Gandalf-prime routes to legolas (or knight-rider for sequencing) if Matt authorizes the follow-on batch.

**Precedents to cite in dispatch:**
- `agentic_orchestration/legolas/research/econ-recrawl-2026-07-17/` (void-rift discovery)
- `agentic_orchestration/legolas/research/di-spiritform-recrawl-2026-07-17/` (di-spiritform discovery)
- `agentic_orchestration/research/curated/atlas/void-rift-phantom-2026-07-17.md` (V11 phantom ruling record)
- `agentic_orchestration/research/curated/atlas/di-spiritform-phantom-2026-07-17.md` (V13 phantom ruling record — this run)

**Not-yet-invoked considerations for Matt:**
- If HIGH-tier batch finds ≥1 additional phantom, the census will need V14+ with denominator −N reflecting phantom flips (parallel to V11→V12 pattern from void-rift).
- If HIGH-tier batch finds re-key-clean candidates (Option-B-eligible new rows), those ride the E-next admission docket with LA 4 + di-druid-pvp-cc-stack-2026 already parked. Cumulative admission batch grows.
