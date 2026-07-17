# S2 — Migration-Readiness Census V11 (THE SCOREBOARD, post-econ-recrawl application + phantom ruling)

**Date:** 2026-07-17 · **Author:** elrond (autonomous atlas-parity run, econ-recrawl-application charge)
**Commissioner:** gandalf-prime (Matt autonomous-run authorization 2026-07-17)
**Source of writes:** Legolas econ-recrawl at commit `f4110f20` — 7 classified / 1 unverifiable
**Corpus state (POST-write):** 585 rows / **563 kit-grain (519 positives + 44 negatives) + 22 NULL-grain** / 562 cell_key resolved (incl. 1 -bt sentinel) / 4 dossier_owed held-out / 585 engine_key 1:1 (0 orphans)
**Scope:** Post-econ-recrawl (7 classifications + 1 phantom ruling) — provenance tag `econ-recrawl-application-2026-07-17`, phantom tag `phantom-kit-provenance-collision-2026-07-17`.

**md5-stability:**
- Pre-Part-1: `20040c5ac09ff3091161747a629e927d`
- Post-Part-1 writes: `20040c5ac09ff3091161747a629e927d`
- Post-census (read-only): `20040c5ac09ff3091161747a629e927d`
- Census read pass DID NOT modify DB: **True**

---

## §1 Headline

| Metric | Count | % |
|---|---|---|
| **Candidate pool (denominator)** | **564** | 100.0% |
| **Expressible-now** | **558** | **98.94%** |
| Blocked | 6 | 1.06% |
| — of which dossier_owed held-out | 4 | 0.71% |

Denominator composition: 519 corpus positives at kit grain (V10: 520; V11: **519** after `d2-wl-void-rift` phantom→negative) + 45 founding roster = **564** (V10: 565; V11: **564**).

Corpus expressible: **513/519 (98.84%)**  ·  Roster expressible: **45/45 (100.0%)** (UNCHANGED — verified)

---

## §2 Delta vs V10 — two-lever decomposition (iron law 4)

Δ decomposes cleanly into:
- **Recrawl-application flip effect** (7 UNKNOWN sole-blocker kits flip clean): +7 kits expressible.
- **Denominator effect** (phantom `d2-wl-void-rift` → negative=1): −1 denominator; −1 from blocked count (phantom WAS blocked in V10, not expressible → expressible baseline UNCHANGED by this lever, denominator shrinks by 1).

**Expected V11 identity (baseline-anchored):**
- Expected expressible = V10 551 + apply_flip 7 + denominator_effect_expressible 0 = **558**
- Expected denominator = V10 565 + denominator_effect -1 = **564**
- Expected blocked = V10 14 − apply_flip 7 + denominator_effect_blocked -1 = **6**

**DB truth check:**
- Actual expressible = **558** vs expected 558 → OK
- Actual denominator = **564** vs expected 564 → OK
- Actual blocked = **6** vs expected 6 → OK

| Scoreboard | Pool expressible | % | Corpus | Roster |
|---|---|---|---|---|
| V10 (published, post-Wave-C landed + corpus-align) | 551/565 | 97.50% | 506/520 | 45/45 |
| **V11 (this run, post-econ-recrawl application + phantom ruling)** | **558/564** | **98.94%** | **513/519** | 45/45 |
| **Δ vs V10** | **+7** | **+1.44pp** | **+7** | 0 |
| — apply-flip contribution | +7 | | +7 | 0 |
| — denominator effect (phantom −1) | 0 | | 0 | 0 |

**Headline movement: V10 97.50% → V11 98.94% (+1.44pp).**

---

## §3 PHANTOM RULING — `d2-wl-void-rift` (LOUD; Matt veto-open)

**RULING: `d2-wl-void-rift` set to `negative=1` with flag `phantom-kit-provenance-collision-2026-07-17`.** Row retained (total 585 conservation). Denominator −1 (565→564). Corpus positives −1 (520→519).

**Evidence base (DB truth AGREES with sheet):**
1. **Sheet enumeration:** two independent D2R Warlock skill-tree enumerations (rpgstash Chaos/Demon/Eldritch guide + fextralife wiki) show NO skill named "Void Rift" across all 30 Warlock skills.
2. **DB corroborating audit trail:** kit ALREADY carried three prior audit flags — `kb-only-backfill-attempted-2026-07-16`, `econ-audit-ambiguous-2026-07-16`, `econ-recrawl-unverifiable-2026-07-16`. THREE independent verification attempts, including this pass, FAILED to find mechanics.
3. **Web-search noise pattern:** Google "Void Rift Warlock" returns exclusively Destiny-2 Voidwalker-Warlock content. Destiny-2 Voidwalker is a real Warlock subclass; "D2" shorthand collision with Diablo-2 during mob-harvest-v3 provenance is the likely harvest-origin failure mode.
4. **Corpus consistency check:** the OTHER five D2R Warlock kits in the corpus (`d2-wl-abyss`, `d2-wl-blood-boil`, `d2-wl-echoing-strike`, `d2-wl-fire`, `d2-wl-tainted-summoner`) all appear in the same enumerated skill-trees — the source enumeration is high-fidelity. Void Rift's exclusion from that enumeration is exclusionary evidence, not a gap.

**Alternative considered and rejected:** editorial-inferred classification (per `poe2-snipe-mirage-deadeye` precedent 07-16). Rejected because Snipe/Mirage precedent was "no dedicated guide but skill demonstrably exists in game"; void-rift is "skill demonstrably does not exist in source universe" — no substrate to editorialize.

**Alternative considered and rejected:** row DELETION. Rejected because deletion loses provenance history + breaks 585-total conservation + breaks git lineage. Negative=1 flip preserves all audit history and enables future disposition changes.

**Matt veto-open:** if Matt disagrees, negative=1 can be reverted by `UPDATE canon_corpus SET negative=0 WHERE kit_id='d2-wl-void-rift'`; denominator returns to 565 and the phantom flag remains as documentation. No destructive change.

---

## §4 Sheet projection cross-check

Sheet projected (charge instruction):
- **Phantom removed:** 558/564 = 98.9%
- **Phantom kept:** 558/565 = 98.8%

**Actual V11 result (phantom REMOVED per elrond ruling):** 558/564 = 98.94%

- Δ vs charge projection ceiling 558: **+0** kits (+0.00pp)
Actual EXACTLY matches sheet projection. Recrawl-application landed clean; no per-kit divergence.

---

## §5 Blocked-on-what — ranked buckets (V11)

| Bucket category | Kits touched | Sub-buckets |
|---|---|---|
| **shapeshift (GX-02 docket)** | 3 | mechanic:shapeshift=3 |
| **wave-D:drain (deferred WC-19)** | 2 | econ:DR=2 |
| **ailment-wave-c+ residue** | 1 | ailment-wave-c+:unknown-ailment=1 |

### §5b Bucket detail (individual buckets ranked)

| # | Bucket | Count |
|---|---|---|
| 1 | `mechanic:shapeshift` | 3 |
| 2 | `econ:DR` | 2 |
| 3 | `ailment-wave-c+:unknown-ailment` | 1 |

---

## §6 Blocked-tail rosters (DERIVED FROM DB)

Named kit rosters per residual blocker:

### `mechanic:shapeshift` (3 kits)
- `gd-berserker-wereforms` — Berserker (FoA mastery)
- `la-ferality-wildsoul` — Ferality Wildsoul
- `la-phantom-beast-awakening-wildsoul` — Phantom Beast Awakening Wildsoul

### `econ:DR` (2 kits)
- `hot-norseman-frost-avalanche` — Frost Avalanche Norseman
- `vs-queen-sigma` — Queen Sigma

### `ailment-wave-c+:unknown-ailment` (1 kit)
- `di-spiritform-druid-pvp` — Spirit-Form Druid (complaint-tier)

**Expected-residual tail (per charge):**
- shapeshift 3 (Matt-fork GX-02): expected `la-ferality-wildsoul`, `la-phantom-beast-awakening-wildsoul`, `gd-berserker-wereforms` OR similar — verify per-DB.
- econ:DR 2 (WC-19 → Wave-D): expected `hot-norseman-frost-avalanche`, `vs-queen-sigma`.
- unknown-ailment 1: expected `di-spiritform-druid-pvp`.
- void-rift: phantom-negative per §3 ruling — NOT in blocked tail.

Cross-check DB-truth-vs-expected:
- shapeshift bucket: **3 kits** (gd-berserker-wereforms, la-ferality-wildsoul, la-phantom-beast-awakening-wildsoul)
- econ:DR bucket: **2 kits** (hot-norseman-frost-avalanche, vs-queen-sigma)
- unknown-ailment bucket: **1 kits** (di-spiritform-druid-pvp)

---

## §7 Part 1 write ledger

Provenance tag: `econ-recrawl-application-2026-07-17` · Source commit: `f4110f20`
Phantom tag: `phantom-kit-provenance-collision-2026-07-17` · SS-overlay tag: `ss-overlay-werewolf-form-buff-2026-07-17:GX-02-docket-evidence`

Writes applied THIS RUN: **0** (idempotent re-run — all target kits already carry the provenance tag; no changes needed). DB state reflects the writes from a prior run.

**First-run write ledger (fresh, from stdout capture — 12 row-touches):**

| # | kit_id | action | provenance-fragment |
|---|---|---|---|
| 1 | `d2-bowazon` | econ_status: gap → native; econ_gaps: drop UNKNOWN; corpus.flags: += econ-recrawl-application | `econ-recrawl-application-2026-07-17:f4110f20:spend/steady-mana (leech-sustained). Multishot 4→23, Strafe fixed 11...` |
| 2 | `d2-fireclaw-wolf` | econ_status: gap → native; econ_gaps: drop UNKNOWN; corpus.flags: += econ-recrawl-application | `econ-recrawl-application-2026-07-17:f4110f20:spend/steady-mana + SS-overlay. Fire Claws 4 mana/attack; Werewolf 15/40s...` |
| 3 | `d2-fury-wolf` | econ_status: gap → native; econ_gaps: drop UNKNOWN; corpus.flags: += econ-recrawl-application | `econ-recrawl-application-2026-07-17:f4110f20:spend/steady-mana + SS-overlay + Feral Rage buff-maintenance descriptor. Fury 4 mana/attack; Feral Rage 3/20s buff...` |
| 4 | `d2-kicksin` | econ_status: gap → native; econ_gaps: drop UNKNOWN; corpus.flags: += econ-recrawl-application | `econ-recrawl-application-2026-07-17:f4110f20:spend/steady-mana + AM Cobra Strike + PC Fade. Dragon Talon mana-spend/kick (leech-sustained)...` |
| 5 | `d2-rabies-wolf` | econ_status: gap → native; econ_gaps: drop UNKNOWN; corpus.flags: += econ-recrawl-application | `econ-recrawl-application-2026-07-17:f4110f20:spend/steady-mana + SS-overlay. Rabies 10 mana/bite; Werewolf 15/40s...` |
| 6 | `poe1-whispering-ice` | econ_status: gap → native; econ_gaps: drop UNKNOWN; corpus.flags: += econ-recrawl-application | `econ-recrawl-application-2026-07-17:f4110f20:spend w/ cooldown-gate rider. Icestorm 0.75s cast + 6.50s CD; Int-per-10 = DAMAGE scaling...` |
| 7 | `vs-phieraggi` | econ_status: gap → native; econ_gaps: drop UNKNOWN; corpus.flags: += econ-recrawl-application | `econ-recrawl-application-2026-07-17:f4110f20:NR/auto-fire (VS-genre-native). 1.4s CD auto-fire; Revival is passive multiplier, NOT per-cast consumable...` |
| 8 | `d2-wl-void-rift` | negative: 0 → 1 (PHANTOM RULING); corpus.flags: += phantom-kit-provenance-collision; engine_key econ_gaps: UNKNOWN → [] | `phantom-kit-provenance-collision-2026-07-17:f4110f20:no D2R Warlock skill 'Void Rift' exists per two independent enumerations...` |
| 9 | `d2-fireclaw-wolf` | corpus.flags: += SS-overlay-werewolf-form-buff GX-02 docket evidence | `ss-overlay-werewolf-form-buff-2026-07-17:GX-02-docket-evidence` |
| 10 | `d2-fury-wolf` | corpus.flags: += SS-overlay-werewolf-form-buff GX-02 docket evidence | `ss-overlay-werewolf-form-buff-2026-07-17:GX-02-docket-evidence` |
| 11 | `d2-rabies-wolf` | corpus.flags: += SS-overlay-werewolf-form-buff GX-02 docket evidence | `ss-overlay-werewolf-form-buff-2026-07-17:GX-02-docket-evidence` |
| 12 | `d2-kicksin` | corpus.flags: += AM Cobra Strike charge-stack + PC Fade activation-toggle secondaries | `am-cobra-strike-charge-stack-2026-07-17:on-hit-cobra-fill/on-hit-finisher-discharge + pc-fade-self-buff-2026-07-17:activation-toggle (per Icy-Veins)` |

**Attribution summary:** 12 row-touches across 8 distinct kit_ids (all 7 classification applies + phantom ruling; 3 SS-overlay stamps on the werewolf triple; 1 combined kicksin AM+PC secondary stamp).

---

## §8 D2 collision audit (broader mob-harvest-v3 ambiguity scan)

Per charge: scan D2-game kits (and SEARCH-DERIVED/unharvested rows) for Destiny-2-signature vocabulary. This is read + flag ONLY confirmed-obvious cases; ambiguous cases list-only for Legolas follow-up.

**Total D2-game positive kits scanned:** 51
**Signature vocabulary checked:** void / solar / arc / stasis / strand / nova / dawnblade / sunbreaker / nightstalker / gunslinger / rift / well-of-radiance / voidwalker / titan / hunter-subclass

**Suspects surfaced: 0** — no other D2-game kit carries Destiny-2-signature vocabulary in kit_id or folk_name. Void-rift is the isolated collision.

D2R Warlock kits verified as REAL (per sheet enumeration cross-check): `d2-wl-abyss`, `d2-wl-blood-boil`, `d2-wl-echoing-strike`, `d2-wl-fire`, `d2-wl-tainted-summoner` — all appear in rpgstash + fextralife Warlock skill-tree enumerations. Only `d2-wl-void-rift` is anomalous.

**Broader audit disposition:** the collision appears TIGHTLY LOCALIZED to the void-rift phantom. No mass-rewrite warranted. If Legolas fires a follow-up Mode B pass on ambiguous candidates, the void-rift precedent (§3) is the template for handling.

---

## §9 Iron-law asserts (PRE V10-state / POST V11-state)

| Assert | PRE (V10) | POST (V11) | Notes |
|---|---|---|---|
| total_corpus | 585 | 585 | UNCHANGED (phantom→negative preserves rows) |
| total_engine_key | 585 | 585 | 1:1 UNCHANGED |
| kit_grain | 563 | 563 | UNCHANGED (no grain writes) |
| null_grain | 22 | 22 | UNCHANGED |
| **kit_positives (denominator base)** | **520** | **519** | −1 (phantom) |
| **kit_negatives** | **43** | **44** | +1 (phantom) |
| **pool = corpus positives + roster 45** | **565** | **564** | −1 (phantom) |
| combat-kit (row_class) | 563 | 563 | UNCHANGED |
| system-record (row_class) | 22 | 22 | UNCHANGED |
| cell_key_resolved | 562 | 562 | UNCHANGED |
| bt_sentinel | 1 | 1 | UNCHANGED |
| orphans engine→corpus | 0 | 0 | UNCHANGED |
| orphans corpus→engine | 0 | 0 | UNCHANGED |
| dossier_owed | 4 | 4 | UNCHANGED |

Cross-check assertions:
- `roster_expressible == 45`: 45 == 45 — OK
- `total 585 conservation`: rows conserved via negative=1 (NOT row-delete) — OK
- `denominator identity`: 519 corpus positives + 45 roster = 564 == 564 — OK

---

## §10 Reproducibility

- **Script:** `../scripts/corpus_s2_census_v11_2026_07_17.py`
- **Backup:** `../corpus.db.pre-v11-2026-07-17-backup` (integrity_check=ok, taken before Part 1 write)
- **Source of writes:** Legolas econ-recrawl at commit `f4110f20` — `agentic_orchestration/legolas/research/econ-recrawl-2026-07-17/`
- **Transactional writes** — Part 1 wrapped in single transaction; PRE asserts held before writing, POST asserts held after; census is a pure READ on the POST-write state.
- **Idempotent** — Part 1 writes check for provenance tag `econ-recrawl-application-2026-07-17` and treat re-runs as verified no-op per-row.
- **Delta decomposition** (§2) reports apply-flip effect and denominator effect separately, per iron law 4 — the two levers are NOT conflated.
- **md5 stability**: post-writes `20040c5ac09f...` == post-census `20040c5ac09f...`: **True**

**Consumers:** governs S5 corpus→engine migration staging. Next re-run: when econ:UNKNOWN residual (9 remaining post-V11) is closed, when shapeshift GX-02 docket rules, or when econ:DR Wave-D spec lands. Matt may veto the phantom ruling by reverting negative=0 (reproducibility instructions embedded in §3).
