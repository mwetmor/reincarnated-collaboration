# Elrond Ruling — Mob-harvest-v3 HIGH-tier Re-crawl Application (Ruling 17)

**Date:** 2026-07-17
**Author:** elrond (autonomous atlas-parity run; Matt authorization 2026-07-16)
**Commissioner:** gandalf-prime — RUN RULING 17 (Matt veto-open)
**Legolas source commit:** `b14f3de6` — `agentic_orchestration/legolas/research/mh-v3-high-recrawl-2026-07-17/`
**Precedent (own):** `atlas/di-spiritform-phantom-2026-07-17.md` · `atlas/void-rift-phantom-2026-07-17.md`
**Triage docket referenced:** `atlas/mob-harvest-v3-triage-2026-07-17.md` §4 (HIGH-13 slate) · §9 (0-2 phantom → MEDIUM/LOW deferred threshold)

---

## §0 Headline verdict — mh-v3 provenance-audit lane CLOSED

**HIGH-tier result: 12 verified-authentic / 1 re-key-clean / 0 phantom / 0 unverifiable.**

Zero phantoms surfaced. Per triage docket §9 threshold (`≥3 phantoms in HIGH → MEDIUM+LOW mandatory`), the 0-phantom outcome MATERIALLY MEETS the "MEDIUM+LOW deferred to on-demand" branch. This application pass CLOSES the mob-harvest-v3 corpus-wide provenance-audit lane. mh-v3 corpus-audit priority DOWNGRADED — signal-ranked risk did not correlate with phantom-hood at HIGH tier.

Interpretation: the two known phantoms (`d2-wl-void-rift` V11 write, `di-spiritform-druid-pvp` V13 write) are OUTLIERS, not tips of a systemic-corruption iceberg. Signal-ranking correctly SURFACED risk; the risk-signals do NOT per-kit predict phantom-hood — they predict "worth verifying." Verification was the right action; the reassuring result is the right outcome.

---

## §1 Ruling-17 four-point split (what was applied)

Ruling 17 constrains this pass to METADATA-ONLY writes on the 13 HIGH-tier rows. No kit_id changes. No negative changes. No row add/delete. Zero-census-movement. That is WHY census V14 does NOT mint from this application — zero-movement re-mint would be ceremony; the iron-law assert block (§4) is the proportionate check.

### Point 1 — Verification stamps (all 13 rows)

Standard flag token `mh-v3-high-recrawl-verified-2026-07-17:legolas-b14f3de6` appended to 11 rows.
Sole-source variant `mh-v3-high-recrawl-verified-sole-source-2026-07-17:legolas-b14f3de6` appended to `ud-seal-veil-daimonios` (per sheet §11 — Pocket Gamer is authoritative for the UD build corpus but is the only source; sole-source thinness rides on the flag).
ADDITIONALLY `di-bombardment-wizard-pvp` receives `folk-name-essence-derived-2026-07-17` (per sheet §3 + index — folk_name maps to a community archetype built on the "Continuous Bombardment" Meteor essence, NOT to a first-class in-game skill; pattern-tracking exemplar for future re-crawls).

### Point 2 — `d2-ghost-pvp` metadata corrections (NOT key mutation)

- `folk_name`: `Ghost` → `Ghost Assassin (WW/Trap)`
- `mech_note`: replaced with authoritative D2 PvP Ghost = Assassin WW/Trap description. Docket §4 speculation ("could be Ghost-Warrior Barb build") explicitly CORRECTED — Mind Blast is a Shadow Discipline Assassin skill, not Barbarian.
- `flags`: appended standard verification token + `mh-v3-recrawl-rekey-candidate-2026-07-17:gandalf-ruling-17:Matt-veto-open`

Re-key candidate `d2-ghost-assassin-pvp` **PARKED to E-next admission lane** per gandalf-ruling-17. Rationale for PARKING rather than executing key mutation this run:

- Current `kit_id d2-ghost-pvp` is referenced by 9 minted atlas artifacts: served E3, armed E4, `canon_engine_key` mapping, and E-series census artifacts.
- Key mutation is an edition-boundary re-mint ceremony (parallel to the E-next admission-lane treatment of di-spiritform's `di-druid-pvp-cc-stack-2026` per gandalf-ruling-16 §"Admission candidate parked").
- Mid-run kit_id mutation would (a) require a new mint-verify pass across all 9 artifact anchors, (b) deliver ZERO incremental expressibility (the row is already expressible), (c) bypass edition-lane admission discipline.
- Downstream classifier ambiguity is DE-RISKED for THIS run via folk_name correction + mech_note authoritative statement + rekey-candidate flag — future consumers reading `folk_name='Ghost Assassin (WW/Trap)'` will not mis-classify.

### Point 3 — `source_urls` enrichment (5 rows)

Legolas reported kits 1–4 + 10 (kit numbering per application sheet: `di-cyclone-monk-pvp`, `di-bone-wall-necro-pvp`, `di-bombardment-wizard-pvp`, `d2-ghost-pvp`, `hot-landsknecht-grenades`) had empty source_urls. Verified in-DB: all 5 were NULL. Populated from the sheet's per-kit live-URL lists (curated authoritative subset — 2 to 5 URLs per row).

Guard: `WHERE source_urls IS NULL OR source_urls = ''` prevents overwriting the 8 rows that already have populated source_urls (d2-wl-abyss, d2-wl-blood-boil, d2-wl-echoing-strike, d2-wl-fire, d2-wl-tainted-summoner, tli-iris2-thunder-magus, ud-cwc-spin-caster, ud-seal-veil-daimonios).

### Point 4 — Hard constraints (STOP-and-flag conditions)

None triggered. See iron-law assert table §4.

---

## §2 Per-row disposition applied

| # | kit_id | Disposition | Applied writes |
|---|---|---|---|
| 1 | `di-cyclone-monk-pvp` | verified-authentic | flag STD; source_urls populated (5 URLs) |
| 2 | `di-bone-wall-necro-pvp` | verified-authentic | flag STD; source_urls populated (5 URLs) |
| 3 | `di-bombardment-wizard-pvp` | verified-authentic (MED-HIGH conf; folk_name essence-derived) | flag STD + `folk-name-essence-derived-2026-07-17`; source_urls populated (4 URLs) |
| 4 | `d2-ghost-pvp` | re-key-clean (metadata corrections only; key mutation PARKED) | folk_name update; mech_note replaced; flag STD + rekey-candidate flag; source_urls populated (5 URLs) |
| 5 | `d2-wl-blood-boil` | verified-authentic | flag STD; source_urls unchanged (already populated) |
| 6 | `d2-wl-tainted-summoner` | verified-authentic | flag STD; source_urls unchanged (already populated) |
| 7 | `d2-wl-echoing-strike` | verified-authentic | flag STD; source_urls unchanged (already populated) |
| 8 | `d2-wl-fire` | verified-authentic | flag STD; source_urls unchanged (already populated) |
| 9 | `d2-wl-abyss` | verified-authentic | flag STD; source_urls unchanged (already populated) |
| 10 | `hot-landsknecht-grenades` | verified-authentic | flag STD; source_urls populated (2 URLs — thinner HoT community corpus per sheet §10) |
| 11 | `ud-seal-veil-daimonios` | verified-authentic (sole-source thinness) | flag SOLE-SOURCE variant; source_urls unchanged (already 1 URL — Pocket Gamer, authoritative for UD corpus) |
| 12 | `ud-cwc-spin-caster` | verified-authentic | flag STD; source_urls unchanged (already populated) |
| 13 | `tli-iris2-thunder-magus` | verified-authentic | flag STD; source_urls unchanged (already populated) |

**Row-count self-audit:** 13 rows targeted / 13 rows written to (13 flag updates + 5 source_urls populates + 1 folk_name + 1 mech_note = all writes accounted). No row added, no row deleted.

---

## §3 SQL — forward + reversal

### Forward SQL (applied; single transaction)

```sql
BEGIN;

-- ============================================================
-- RULING 17 POINT 1: Verification stamps on 13 HIGH-tier rows
-- ============================================================

-- 11 rows get the standard verification token
-- (12 verified-authentic + 1 re-key-clean, minus ud-seal-veil-daimonios which gets sole-source variant)
-- (di-bombardment-wizard-pvp also gets an additional folk-name-essence-derived flag applied separately)

UPDATE canon_corpus
   SET flags = CASE 
                 WHEN flags IS NULL OR flags='' THEN 'mh-v3-high-recrawl-verified-2026-07-17:legolas-b14f3de6'
                 ELSE flags || ',mh-v3-high-recrawl-verified-2026-07-17:legolas-b14f3de6'
               END
 WHERE kit_id IN (
   'di-cyclone-monk-pvp',
   'di-bone-wall-necro-pvp',
   'd2-wl-blood-boil',
   'd2-wl-tainted-summoner',
   'd2-wl-echoing-strike',
   'd2-wl-fire',
   'd2-wl-abyss',
   'hot-landsknecht-grenades',
   'ud-cwc-spin-caster',
   'tli-iris2-thunder-magus'
 )
   AND (flags IS NULL OR flags NOT LIKE '%mh-v3-high-recrawl-verified-2026-07-17:legolas-b14f3de6%');

-- ud-seal-veil-daimonios: sole-source variant token (per sheet §11 sole-source thinness ride)
UPDATE canon_corpus
   SET flags = CASE 
                 WHEN flags IS NULL OR flags='' THEN 'mh-v3-high-recrawl-verified-sole-source-2026-07-17:legolas-b14f3de6'
                 ELSE flags || ',mh-v3-high-recrawl-verified-sole-source-2026-07-17:legolas-b14f3de6'
               END
 WHERE kit_id = 'ud-seal-veil-daimonios'
   AND (flags IS NULL OR flags NOT LIKE '%mh-v3-high-recrawl-verified-sole-source-2026-07-17:legolas-b14f3de6%');

-- di-bombardment-wizard-pvp: standard verification token AND folk-name-essence-derived flag
UPDATE canon_corpus
   SET flags = CASE 
                 WHEN flags IS NULL OR flags='' THEN 'mh-v3-high-recrawl-verified-2026-07-17:legolas-b14f3de6,folk-name-essence-derived-2026-07-17'
                 ELSE flags || ',mh-v3-high-recrawl-verified-2026-07-17:legolas-b14f3de6,folk-name-essence-derived-2026-07-17'
               END
 WHERE kit_id = 'di-bombardment-wizard-pvp'
   AND (flags IS NULL OR flags NOT LIKE '%mh-v3-high-recrawl-verified-2026-07-17:legolas-b14f3de6%');

-- ============================================================
-- RULING 17 POINT 2: d2-ghost-pvp metadata corrections
-- (kit_id UNCHANGED per ruling — key mutation parked to E-next
--  as re-key candidate; folk_name + mech_note + flags update only)
-- ============================================================

UPDATE canon_corpus
   SET folk_name = 'Ghost Assassin (WW/Trap)',
       mech_note = 'Authoritative D2 PvP Ghost = Assassin WW/Trap archetype: Mind Blast stun (Shadow Discipline) + Fade DR + Open Wounds bleed stacking on Whirlwind weapons + low-level trap complement + Dragon Flight teleport-strike. Anti-caster specialization. NOT a Barbarian build (docket-speculated Ghost-Warrior Barb hypothesis is INCORRECT per PureDiablo TienJe guide, items7 Skibum guide, diablowiki.net, d2jsp forum discourse). Re-key candidate d2-ghost-assassin-pvp PARKED to E-next admission lane per gandalf-ruling-17: current kit_id d2-ghost-pvp referenced by 9 minted atlas artifacts including served E3 + armed E4 + canon_engine_key; key mutation rides edition-boundary re-mint ceremony, not mid-run. See agentic_orchestration/legolas/research/mh-v3-high-recrawl-2026-07-17/ + atlas/mh-v3-high-recrawl-application-2026-07-17.md.',
       flags = CASE 
                 WHEN flags IS NULL OR flags='' THEN 'mh-v3-high-recrawl-verified-2026-07-17:legolas-b14f3de6,mh-v3-recrawl-rekey-candidate-2026-07-17:gandalf-ruling-17:Matt-veto-open'
                 ELSE flags || ',mh-v3-high-recrawl-verified-2026-07-17:legolas-b14f3de6,mh-v3-recrawl-rekey-candidate-2026-07-17:gandalf-ruling-17:Matt-veto-open'
               END
 WHERE kit_id = 'd2-ghost-pvp'
   AND folk_name = 'Ghost';

-- ============================================================
-- RULING 17 POINT 3: source_urls enrichment (5 rows NULL/empty)
-- Only writes where source_urls is currently NULL or empty
-- ============================================================

UPDATE canon_corpus
   SET source_urls = '["https://diablo.fandom.com/wiki/Cyclone_Strike", "https://gamerant.com/diablo-immortal-best-cyclone-strike-monk-build-skills-gear-gems-reforge/", "https://gamerant.com/diablo-immortal-best-pvp-battleground-monk-build-skills-gear-gems-reforge/", "https://www.icy-veins.com/diablo-immortal/monk-cyclone-storm-build-guide-for-raids", "https://mbaker2307.wixsite.com/mbakerdesign/mystic-wind-cyclone-strike-monk/"]'
 WHERE kit_id = 'di-cyclone-monk-pvp'
   AND (source_urls IS NULL OR source_urls = '');

UPDATE canon_corpus
   SET source_urls = '["https://diablo.fandom.com/wiki/Bone_Wall_(Diablo_Immortal)", "https://immortal.maxroll.gg/build-guides/bone-wall-necromancer-pvp-guide-battlegrounds-rite-of-exile", "https://www.icy-veins.com/diablo-immortal/necromancer-bone-spear-pvp-build-guide", "https://www.dexerto.com/diablo/best-diablo-immortal-necromancer-builds-1870129/", "https://www.diablofans.com/builds/109604-pvp-bone-spear-necro"]'
 WHERE kit_id = 'di-bone-wall-necro-pvp'
   AND (source_urls IS NULL OR source_urls = '');

UPDATE canon_corpus
   SET source_urls = '["https://diablo.fandom.com/wiki/Meteor_(Diablo_Immortal)", "https://game8.co/games/Diablo-Immortal/archives/378701", "https://www.dexerto.com/diablo/best-diablo-immortal-wizard-builds-1872848/", "https://www.icy-veins.com/diablo-immortal/wizard"]'
 WHERE kit_id = 'di-bombardment-wizard-pvp'
   AND (source_urls IS NULL OR source_urls = '');

UPDATE canon_corpus
   SET source_urls = '["https://www.purediablo.com/forums/threads/pvp-ww-ghost-assassin-guide-v2-0-by-tienje.1070/", "https://www.items7.com/blog/how-to-build-a-ghost-sin-by-skibum/", "https://diablo2.diablowiki.net/Guide:PvP_C/C_WW_Shadow_Assassin_v1.10,_by_Voide", "https://www.icy-veins.com/d2/whirlwind-assassin-whirlwindsin-build", "https://maxroll.gg/d2/guides/whirlwind-assassin"]'
 WHERE kit_id = 'd2-ghost-pvp'
   AND (source_urls IS NULL OR source_urls = '');

UPDATE canon_corpus
   SET source_urls = '["https://steamcommunity.com/app/2218750/discussions/0/7953990088758033015/", "https://www.youtube.com/watch?v=bF5kS1D0BDs"]'
 WHERE kit_id = 'hot-landsknecht-grenades'
   AND (source_urls IS NULL OR source_urls = '');

COMMIT;
```

**Idempotency verified:** re-running the same SQL after write is a no-op (md5 unchanged). The `NOT LIKE` guards prevent double-append of the same flag token; the `WHERE folk_name = 'Ghost'` guard prevents re-clobbering the d2-ghost-pvp folk_name if already updated; the `IS NULL OR ''` guards on source_urls prevent overwriting populated fields. Confirmed empirically post-write (re-run md5 identical to first-run md5).

### Reversal SQL (in case of Matt veto)

Preferred reversal (full backup restore — bit-identical to pre-write state):

```bash
cp corpus.db.pre-mh-v3-application-2026-07-17-backup corpus.db
# md5 must be 99def837a90aec875d030cfd8279772d
```

Alternative reversal (SQL-only, for surgical audit):

```sql
BEGIN;

-- Reverse Point 1: strip verification tokens from 13 rows
UPDATE canon_corpus
   SET flags = REPLACE(REPLACE(REPLACE(flags,
                 ',mh-v3-high-recrawl-verified-2026-07-17:legolas-b14f3de6', ''),
                 'mh-v3-high-recrawl-verified-2026-07-17:legolas-b14f3de6,', ''),
                 'mh-v3-high-recrawl-verified-2026-07-17:legolas-b14f3de6', '')
 WHERE kit_id IN (
   'di-cyclone-monk-pvp','di-bone-wall-necro-pvp','di-bombardment-wizard-pvp',
   'd2-ghost-pvp','d2-wl-blood-boil','d2-wl-tainted-summoner','d2-wl-echoing-strike',
   'd2-wl-fire','d2-wl-abyss','hot-landsknecht-grenades','ud-cwc-spin-caster',
   'tli-iris2-thunder-magus'
 );

UPDATE canon_corpus
   SET flags = REPLACE(REPLACE(REPLACE(flags,
                 ',mh-v3-high-recrawl-verified-sole-source-2026-07-17:legolas-b14f3de6', ''),
                 'mh-v3-high-recrawl-verified-sole-source-2026-07-17:legolas-b14f3de6,', ''),
                 'mh-v3-high-recrawl-verified-sole-source-2026-07-17:legolas-b14f3de6', '')
 WHERE kit_id = 'ud-seal-veil-daimonios';

UPDATE canon_corpus
   SET flags = REPLACE(REPLACE(flags,
                 ',folk-name-essence-derived-2026-07-17', ''),
                 'folk-name-essence-derived-2026-07-17', '')
 WHERE kit_id = 'di-bombardment-wizard-pvp';

-- Reverse Point 2: restore d2-ghost-pvp folk_name + mech_note + strip rekey flag
UPDATE canon_corpus
   SET folk_name = 'Ghost',
       mech_note = 'PvP-named hybrid: Mind Blast stunlock + traps + claw WW burst; control-chain dueling identity.',
       flags = REPLACE(REPLACE(REPLACE(flags,
                 ',mh-v3-recrawl-rekey-candidate-2026-07-17:gandalf-ruling-17:Matt-veto-open', ''),
                 'mh-v3-recrawl-rekey-candidate-2026-07-17:gandalf-ruling-17:Matt-veto-open,', ''),
                 'mh-v3-recrawl-rekey-candidate-2026-07-17:gandalf-ruling-17:Matt-veto-open', '')
 WHERE kit_id = 'd2-ghost-pvp';

-- Reverse Point 3: NULL out source_urls for the 5 previously-empty rows
UPDATE canon_corpus SET source_urls = NULL WHERE kit_id = 'di-cyclone-monk-pvp';
UPDATE canon_corpus SET source_urls = NULL WHERE kit_id = 'di-bone-wall-necro-pvp';
UPDATE canon_corpus SET source_urls = NULL WHERE kit_id = 'di-bombardment-wizard-pvp';
UPDATE canon_corpus SET source_urls = NULL WHERE kit_id = 'd2-ghost-pvp';
UPDATE canon_corpus SET source_urls = NULL WHERE kit_id = 'hot-landsknecht-grenades';

COMMIT;
```

Backup restore is preferred; the surgical SQL reversal above is retained for future audit / partial-reversal contingencies.

---

## §4 Iron-law assert table (pre / post — ZERO-CENSUS-MOVEMENT)

| Metric | Pre-write | Post-write | Δ | Status |
|---|---|---|---|---|
| Total rows | 585 | 585 | 0 | UNCHANGED |
| Kit-grain rows (`grain='kit'`) | 563 | 563 | 0 | UNCHANGED |
| Kit-grain positives (`grain='kit' AND negative=0`) | 518 | 518 | 0 | UNCHANGED |
| Kit-grain negatives (`grain='kit' AND negative=1`) | 45 | 45 | 0 | UNCHANGED |
| Null-grain rows (`grain IS NULL`) | 22 | 22 | 0 | UNCHANGED |
| `dossier_owed=1` | 4 | 4 | 0 | UNCHANGED |
| Roster (`roster_atlas`) | 45 | 45 | 0 | UNCHANGED |
| Pool denominator (518 pos + 45 roster) | 563 | 563 | 0 | UNCHANGED |
| Expressible (structural) | 560 | 560 | 0 | UNCHANGED |
| Expressibility ratio | 560/563 (99.47%) | 560/563 (99.47%) | 0 | UNCHANGED |

STOP-and-flag conditions: none triggered. All hard constraints per Ruling 17 point 4 preserved:
- NO kit_id changes (0 rows affected in identity column)
- NO negative changes (0 rows flipped)
- NO row add/delete
- 585 total conserved
- Kit-grain 563 (518 pos / 45 neg) conserved
- Null-grain 22 conserved
- `dossier_owed` 4 conserved
- Expressibility MUST NOT move: pool = 518 corpus positives + 45 roster = 563 (composition unchanged by metadata-only writes); expressible-set membership unaffected (no flips into or out of the 560 expressible set)

---

## §5 md5 chain

- **Pre-backup / pre-write:** `99def837a90aec875d030cfd8279772d`
- **Post-write:** `48a1f90c407826e438aa5f53ef45215f`
- **Post-idempotency-re-run:** `48a1f90c407826e438aa5f53ef45215f` (identical to post-write; re-running the SQL is a no-op)
- **Backup file:** `../corpus.db.pre-mh-v3-application-2026-07-17-backup` (bit-identical to pre-write state — md5 `99def837a90aec875d030cfd8279772d`)

---

## §6 No-V14 rationale

Ruling 17 point 4 mandates zero-census-movement. This pass:

- Does not flip any row's `negative` value.
- Does not add or delete any row.
- Does not touch any `kit_id`.
- Only writes to `flags`, `folk_name` (1 row), `mech_note` (1 row), and `source_urls` (5 rows).

Census pool composition is a function of (kit-grain positives + roster). Neither moved. Expressibility is a function of pool composition + per-row express-blocker signals; none of the touched columns are express-blockers. Therefore expressibility is provably UNCHANGED at 560/563.

A V14 census-mint at this state would report identical scoreboard numbers to V13. The iron-law assert table §4 IS the proportionate check per ruling 17 point 4. V14 mint is not fired.

Downstream consumers of the census tracker should treat V13 (post-di-spiritform-phantom-write) as the current census baseline. This ruling record supplements V13 with the flags/metadata refinements applied on 13 HIGH-tier rows.

---

## §7 Provenance-integrity closure

**HIGH-tier verification pass on mob-harvest-v3 provenance-audit lane: CLOSED with 0 phantoms.**

Per triage docket §9 threshold table:

| HIGH-tier phantom count | Docket branch | Applied here |
|---|---|---|
| 0-2 phantoms | MEDIUM+LOW deferred to on-demand | ✓ APPLIED (0 phantoms) |
| ≥3 phantoms | MEDIUM+LOW mandatory verify | NOT triggered |

**mob-harvest-v3 corpus-wide audit priority: DOWNGRADED.** Mode-B re-crawls of MEDIUM (37 kits) and LOW (408 kits) mob-harvest-v3 tiers are DEFERRED to on-demand — triggered only if a specific kit surfaces downstream classifier ambiguity, external-consumer complaint, or E-next admission-lane review flag.

Known phantoms remaining in `provenance_tag='mobile-harvest-v3'` `source_date='2026-07-12'` at this state:
1. `d2-wl-void-rift` (V11 phantom write; Matt-veto-open at time of write; state = negative=1)
2. `di-spiritform-druid-pvp` (V13 phantom write; Matt-veto-open at time of write; state = negative=1)

Both are OUTLIERS per this verification pass. Neither is representative of a systemic mh-v3 corruption pattern.

---

## §8 Cross-seam notes

- **Legolas:** commissioned Mode B widened-scope re-crawl on 13 HIGH-tier slate; delivered clean 12-verified-authentic + 1 re-key-clean + 0 phantom + 0 unverifiable outcome in `agentic_orchestration/legolas/research/mh-v3-high-recrawl-2026-07-17/` (commit `b14f3de6`). Precedent-method reference (di-spiritform recrawl + econ-recrawl) validated as scalable Mode B pattern for future targeted re-crawls.
- **Gandalf-prime:** RUN RULING 17 (Matt veto-open) authored; this application executes ruling points 1–4 as scoped.
- **Star-lord:** no engine-side action required (metadata writes are corpus.db-only; no telemetry impact).
- **Knight-rider:** application-pass sequenced under autonomous atlas-parity run; audit-lane closure signal for docket-management to update mh-v3 priority to DEFERRED-ON-DEMAND.
- **Matt:** VETO-OPEN. Reversal preferred = backup restore (§3, md5 `99def837a90aec875d030cfd8279772d`); SQL-surgical reversal also documented (§3). Re-key candidate `d2-ghost-assassin-pvp` PARKED to E-next admission lane — no incremental Matt-gate this run.

---

## §9 Admission candidate parked (for E-next / E4-ratification)

Following the precedent set by gandalf-ruling-16's parking of `di-druid-pvp-cc-stack-2026`:

**Candidate kit_id:** `d2-ghost-assassin-pvp` (re-key from `d2-ghost-pvp`)
**Type:** re-key mutation (not new-row admission — 1-for-1 identity swap)
**Gate:** rides E-next admission docket at the E4-ratification Matt gate.

Rationale for parking rather than executing this run:
1. `kit_id d2-ghost-pvp` is referenced by 9 minted atlas artifacts (served E3 + armed E4 + canon_engine_key + edition census artifacts). Mid-run key mutation requires cross-artifact mint-verify pass.
2. Delivers ZERO incremental expressibility this cycle — the row is already in the 560 expressible set post- V13.
3. Downstream classifier ambiguity is DE-RISKED this cycle via folk_name correction + mech_note authoritative statement + rekey-candidate flag on the row.
4. Edition-lane admission discipline: all identity mutations ride E-next batch review, not one-off ruling records mid-run.

If Matt vetoes the parking and requests immediate key mutation, reversal is straightforward (backup restore + fresh re-key application with cross-artifact update).

---

## §10 Status

- Ruling: **APPLIED**
- Matt: **VETO-OPEN**
- V14 mint: **NOT FIRED** (zero-census-movement per Ruling 17 point 4; iron-law assert §4 is the proportionate check)
- mh-v3 audit lane: **CLOSED** (0 phantoms; MEDIUM+LOW deferred to on-demand per docket §9)
- Re-key candidate `d2-ghost-assassin-pvp`: **PARKED** to E-next admission lane
