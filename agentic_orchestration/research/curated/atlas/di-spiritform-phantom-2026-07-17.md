# Elrond Ruling — DI Spirit-Form Druid PvP → Phantom (Option A only)

**Date:** 2026-07-17
**Author:** elrond (autonomous atlas-parity run)
**Commissioner:** gandalf-prime (Matt autonomous-run authorization 2026-07-16)
**Gandalf-prime ruling reference:** Ruling 16 (Matt veto-open)
**Precedent:** `atlas/void-rift-phantom-2026-07-17.md` (V11 `d2-wl-void-rift` phantom write, elrond own precedent)

## Ruling

`di-spiritform-druid-pvp` is a **PHANTOM KIT** (mob-harvest v3 mis-naming / mechanic-invention). Applied as **Option A only** per gandalf-prime ruling 16:

- `negative=1` set on `canon_corpus` row `di-spiritform-druid-pvp`
- Row RETAINED (585 conservation preserved, audit-signal preserved)
- Flag token appended: `phantom-kit-mechanic-invention-2026-07-17:gandalf-ruling-16:Matt-veto-open`
- `mech_note` updated to record phantom finding, real-class reference, and admission-candidate parking

## Options — B and C REFUSED

- **Option B** (create clean `di-druid-pvp-cc-stack-2026` row) — **REFUSED FOR THIS CYCLE**. New-row admission is edition-lane work; rides E-next admission docket with LA 4 at the E4-ratification Matt gate. Admitting Option B would (a) break 585-conservation, (b) unlock zero expressibility that isn't already delivered by the census structure, (c) bypass the edition-lane admission discipline. Recorded as ADMISSION CANDIDATE below.
- **Option C** (delete the row) — REFUSED. Loses the mob-harvest v3 audit signal that surfaced this phantom in the first place.

## Evidence pointers

- **Legolas widened re-crawl (third attempt):** `agentic_orchestration/legolas/research/di-spiritform-recrawl-2026-07-17/00-index.md` + `application-sheet-2026-07-17.md` (gandalf-verified, commit `dc0ce6cd`)
- **Class existence CONFIRMED** — DI Druid class launched 2025-07-03 (Blizzard official announcement news.blizzard.com/en-us/article/24216435; Blizzardwatch hands-on blizzardwatch.com/2025/06/26/diablo-immortal-druid-class; XBOX Wire; Massively Overpowered)
- **Mechanic ABSENT** — two independent full-skill enumerations agree: transformations = {Werewolf L3, Werebear L38, Stag Charge, Raven Swarm}. No "spirit form" / "spiritform" / "spirit shift" skill. Negative confirms verbatim in both source WebFetches.
- **CC vocab all landed** — Werebear roar Stun 2-3s / Mangle Stun 1-3s / Summon Grizzly Stun 4s / Oak Sage Immobilize 4s / Stag Charge Slow 40% / Thorn Armor Slow 40% / Earthquake Knockup / Werewolf Howl damage-amp-marking / Werebear Crush+Bound Knockback / Fire Tornado DoT-burn / Rabid Might self-CC-immunity. Fully within landed set — no new-shape needed.
- **Complaint-tier pattern verified** — us.forums.blizzard.com threads Q3-Q4 2025 + Feb 2026 confirm DI Druid PvP was a major community-complaint topic; the SHAPE (CC-dense objective-denial Druid) is real, but its NAME "spirit form" is uncited in any authoritative source.

## Write applied — SQL forward + reversal

**Forward SQL (applied):**
```sql
BEGIN;
UPDATE canon_corpus
   SET negative = 1,
       flags    = 'kb-only-backfill-attempted-2026-07-16,econ-recrawl-unverifiable-2026-07-16,phantom-kit-mechanic-invention-2026-07-17:gandalf-ruling-16:Matt-veto-open',
       mech_note = 'PHANTOM (mob-harvest v3 mis-naming) — DI Druid class IS real (launched 2025-07-03, Blizzard official) but ''spirit form'' mechanic does NOT exist; real transformations = Werewolf/Werebear/Stag Charge/Raven Swarm; complaint-tier CC stack (stun/slow/knockback/immobilize/damage-amp/DoT) all landed vocab. See agentic_orchestration/legolas/research/di-spiritform-recrawl-2026-07-17/. Admission candidate di-druid-pvp-cc-stack-2026 parked to E-next lane per gandalf-ruling-16 (Option B REFUSED this cycle; breaks 585-conservation). POST-CUTOFF: di-2026-era only. Conf capped ≤0.50.'
 WHERE kit_id = 'di-spiritform-druid-pvp'
   AND negative = 0;
COMMIT;
-- rowcount asserted: 1
```

**Idempotency:** re-running the WHERE clause `AND negative=0` guard returns 0 changes on second execution. Confirmed empirically post-write.

**Reversal SQL (in case of Matt veto):**
```sql
BEGIN;
UPDATE canon_corpus
   SET negative = 0,
       flags    = 'kb-only-backfill-attempted-2026-07-16,econ-recrawl-unverifiable-2026-07-16',
       mech_note = 'POST-CUTOFF: di-2026-era only. Conf capped ≤0.50. ''Complaint-tier'' = PVP overpowered at time of corpus capture. Spirit form = alternate Druid state (not Bear Form). All claims atlas-provenance only.'
 WHERE kit_id = 'di-spiritform-druid-pvp'
   AND negative = 1;
COMMIT;
```

Alternative reversal: `sqlite3 corpus.db ".restore corpus.db.pre-di-spiritform-phantom-2026-07-17-backup"` (full backup restore).

## md5 chain

- Pre-backup / pre-write: `11f73ab3f000b9ada1492fe496e14e09`
- Post-write: `99def837a90aec875d030cfd8279772d`
- Backup file: `../corpus.db.pre-di-spiritform-phantom-2026-07-17-backup` (bit-identical to pre-write state)

## Iron-law impact

| Metric | Pre-write | Post-write | Δ |
|---|---|---|---|
| Total rows | 585 | 585 | 0 (CONSERVED) |
| Kit-grain rows | 563 | 563 | 0 |
| Kit-grain positives | 519 | 518 | −1 |
| Kit-grain negatives | 44 | 45 | +1 |
| Null-grain rows | 22 | 22 | 0 |
| dossier_owed | 4 | 4 | 0 |
| Pool denominator (518 pos + 45 roster) | 564 | 563 | −1 |
| Expressible | 560 | 560 | 0 (the kit was blocked, not expressible) |
| Blocked tail | 4 | 3 | −1 |

No unintended movements. STOP-and-flag condition not triggered.

## Admission candidate parked (for E-next / E4-ratification gate)

**Candidate kit_id:** `di-druid-pvp-cc-stack-2026`
**Proposed folk_name:** `DI Druid PvP CC stack`
**Proposed corpus fields (per legolas application-sheet):**
- `ctrl_raw`: `stun-multi-source, slow, root/immobilize, knockback, damage-amp/marking, self-cc-immunity` (all landed vocab)
- `elem_raw`: `physical, fire, earth` (mixed — Fire Tornado fire; Earthquake/Landslide/Surging Stone earth; most CC physical)
- `source_urls`: Blizzard official news post + Fandom + Blizzardwatch (per legolas re-crawl URL set)
- `source_date`: `2026-07-17`
- `provenance_tag`: `legolas-recrawl-v1-2026-07-17`
- `game`: `di`
- `era_year`: 2025
- `skill_debut_year`: 2025

**Gate:** rides E-next admission docket with LA 4 (Ferality Wildsoul, Phantom Beast Awakening Wildsoul, Liberator Valkyrie, Shining Knight Valkyrie) at the E4-ratification Matt gate. Do NOT admit this cycle.

**Rationale for parking rather than admitting:**
1. Breaks 585-conservation iron law that anchors the census (585 → 586).
2. Delivers zero incremental expressibility THIS CYCLE — the phantom-flag ruling already resolves the blocked tail's unknown-ailment residue.
3. Bypasses edition-lane admission discipline (all new-row admissions ride E-next batch review, not one-off ruling records).
4. The CC-stack shape is well-verified (evidence trail in legolas re-crawl) — admission is not evidence-limited, only lane-gated.

## Cross-seam notes

- **Legolas** — commissioned to re-crawl `di-spiritform-druid-pvp` (Mode B, third attempt widened scope); delivered phantom finding + Option A/B/C recommendation; my ruling accepts phantom finding but selects Option A only per gandalf-prime.
- **Gandalf-prime** — ruling 16 authored (Matt veto-open); scoped to Option A only; parking Option B as admission candidate.
- **Star-lord** — no engine-side action required (Wave-D already landed; blocked tail is corpus.db-side classification).
- **Knight-rider** — will sequence phantom write / V13 census / mob-harvest-v3 triage docket in this run.
- **Matt** — veto-open. Reversal SQL and backup restore both documented above.

## Provenance-integrity finding

This is the **SECOND** confirmed mob-harvest v3 phantom kit surfaced by post-hoc re-crawl:
1. `d2-wl-void-rift` — V11 phantom write (franchise-name collision, D2/Destiny-2 vocabulary bleed)
2. `di-spiritform-druid-pvp` — this ruling (mechanic-invention from complaint colloquialism)

Two independent phantoms in `provenance_tag='mobile-harvest-v3'` with `source_date='2026-07-12'` = **systematic risk**. This ruling record is issued concurrent with the mob-harvest-v3 triage docket (`atlas/mob-harvest-v3-triage-2026-07-17.md`) which enumerates the remaining 458 positive mob-harvest v3 kits and ranks them on phantom-risk signals visible in-DB for further re-crawl targeting.

## Status

- Ruling: **APPLIED**
- Matt: **VETO-OPEN**
- Next census: **V13** (this run)
- Next re-run trigger: Matt veto → V-revert (SQL above) or Matt GX-02 ruling → V14
