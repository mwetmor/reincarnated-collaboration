# Tier-3 Family-Membership Sidecar — CENSUS

**Run:** Tier-3 Encounter-Geometry Run · ruling **L-13(b)** · conductor gandalf `RUN-CONDUCTOR`
**Author:** elrond (data steward) · 2026-07-22
**Sidecar:** `agentic_orchestration/elrond/notes/2026-07-22-tier3-family-membership-sidecar.json`
**corpus.db (READ-ONLY, mode=ro):** md5 `d091881dc1507753577f56f4998a64a5`

> Transcription-with-provenance ONLY. No new rulings, no fabrication. Working labels — NOT canon.

---

## Tier provenance (FOUND)

| tier | source artifact | rows |
|---|---|---:|
| RATIFIED | `corpus.db` table `atlas_gateA_labels_2026_07_14` | 86 |
| PROPAGATED | `agentic_orchestration/research/curated/atlas/atlas-archipelago-mock.json` (stratum=core, non-self-seed) | 44 |
| DOCKET | `agentic_orchestration/research/curated/atlas/atlas-e4-family-candidates.json` `dockets[*].members` | 145 |
| **TOTAL rows** | | **275** |

Active (non-shadowed) rows: **248** · shadowed rows: **27** · conflicts: **19**.

---

## Spine coverage delta (the headline)

- **BEFORE** (gateA RATIFIED only, on-spine): **46 kits / 267**, across **5 families**.
- **AFTER** (all three tiers, active on-spine): **131 kits / 267**, across **9 families**.
- **Delta:** +85 spine kits · +4 families with spine membership.

## Per-family spine counts (active on-spine): before -> after

| family | before (RATIFIED only) | after (all tiers) | delta | note |
|---|---:|---:|---:|---|
| WHIRLWIND | 7 | 7 | +0 |  |
| CHANNELED-BEAM | 6 | 6 | +0 |  |
| AURA | 5 | 6 | +1 |  |
| TOTEM-SENTRY | 16 | 32 | +16 |  |
| TRAP-MINE | 12 | 26 | +14 |  |
| MINION-PET | 0 | 0 | +0 | still zero-spine |
| MELEE-STRIKE | 0 | 15 | +15 | RECOVERED (was zero-spine) |
| DOT-AILMENT | 0 | 20 | +20 | RECOVERED (was zero-spine) |
| MULTI-PROJECTILE-VOLLEY | 0 | 14 | +14 | RECOVERED (was zero-spine) |
| SHAPESHIFT | 0 | 5 | +5 | RECOVERED (was zero-spine) |
| IDENTITY-GAUGE | 0 | 0 | +0 | still zero-spine |
| CHAIN-BOUNCE | 0 | 0 | +0 | still zero-spine |
| DASH-STRIKER | 0 | 0 | +0 | still zero-spine |
| **TOTAL (distinct kits)** | **46** | **131** | **+85** | |

> Each spine kit resolves to exactly ONE active family (the conflict rule collapses cross-tier
> duplicates), so the after-column sums cleanly: 131 family-assignments = 131 distinct on-spine kits. No kit is double-counted.

---

## Per-era spread of resolved (active on-spine) kits

| age (era_year) | shelf | resolved kits | of era spine |
|---|---|---:|---:|
| Age I | D2 (2000) | 27 | 60 |
| Age II | PoE1 (2013) | 53 | 93 |
| Age III | GD (2016) | 20 | 41 |
| Age IV | PoE2+LE (2024) | 31 | 73 |
| **all** | | **131** | **267** |

### Per-era × family (active on-spine)

| family | Age I | Age II | Age III | Age IV |
|---|---:|---:|---:|---:|
| WHIRLWIND | 3 | 1 | 1 | 2 |
| CHANNELED-BEAM | 0 | 2 | 3 | 1 |
| AURA | 1 | 4 | 0 | 1 |
| TOTEM-SENTRY | 3 | 14 | 3 | 12 |
| TRAP-MINE | 6 | 12 | 5 | 3 |
| MELEE-STRIKE | 8 | 0 | 5 | 2 |
| DOT-AILMENT | 2 | 12 | 2 | 4 |
| MULTI-PROJECTILE-VOLLEY | 3 | 8 | 0 | 3 |
| SHAPESHIFT | 1 | 0 | 1 | 3 |

---

## Zero-membership family recovery (the L-13(b) purpose)

Families with **zero on-spine membership BEFORE** (RATIFIED-only): MINION-PET, MELEE-STRIKE, DOT-AILMENT, MULTI-PROJECTILE-VOLLEY, SHAPESHIFT, IDENTITY-GAUGE, CHAIN-BOUNCE, DASH-STRIKER (8 families).

- **RECOVERED** (now carry >=1 on-spine member): **MELEE-STRIKE, DOT-AILMENT, MULTI-PROJECTILE-VOLLEY, SHAPESHIFT** (4).
- **Still zero-spine**: MINION-PET, IDENTITY-GAUGE, CHAIN-BOUNCE, DASH-STRIKER (4).

Recovery-source breakdown (which tier supplied each recovered family's first spine member):

| family | recovered via tier(s) | on-spine count |
|---|---|---:|
| MELEE-STRIKE | DOCKET | 15 |
| DOT-AILMENT | DOCKET | 20 |
| MULTI-PROJECTILE-VOLLEY | DOCKET | 14 |
| SHAPESHIFT | DOCKET | 5 |

> Still-zero families are HONEST HOLES — their docket/draft members are all off-spine (annex/system
> games), OR they are fresh-draft families (CHAIN-BOUNCE, DASH-STRIKER) with no materialized-tier
> artifact. No fabrication was used to fill them.

---

## Conflicts (cross-tier family disagreement)

**19 conflict(s)** — kit carries different families across tiers. Active row = highest-precedence tier; losers kept with `shadowed_by`.

| kit_id | active family (tier) | shadowed family (tier) | on_spine |
|---|---|---|:---:|
| `poe1-forbidden-rite` | TOTEM-SENTRY (RATIFIED) | DOT-AILMENT (DOCKET) | True |
| `d2-frenzy-barb` | TRAP-MINE (RATIFIED) | MELEE-STRIKE (DOCKET) | True |
| `le-smite-paladin` | TRAP-MINE (RATIFIED) | MELEE-STRIKE (DOCKET) | True |
| `d2-rabies-wolf` | TRAP-MINE (PROPAGATED) | SHAPESHIFT (DOCKET); DOT-AILMENT (DOCKET) | True |
| `d2-smiter` | TRAP-MINE (PROPAGATED) | MELEE-STRIKE (DOCKET) | True |
| `gd-blight-fiend-ritualist` | TRAP-MINE (PROPAGATED) | DOT-AILMENT (DOCKET) | True |
| `gd-wendigo-totem-ritualist` | TOTEM-SENTRY (PROPAGATED) | DOT-AILMENT (DOCKET) | True |
| `poe1-hexblast-mines` | TRAP-MINE (PROPAGATED) | DOT-AILMENT (DOCKET) | True |
| `poe1-toxic-rain` | TRAP-MINE (PROPAGATED) | DOT-AILMENT (DOCKET) | True |
| `tq-druid-squall-caster` | TOTEM-SENTRY (PROPAGATED) | DOT-AILMENT (DOCKET) | False |
| `tq-onslaught-assassin` | TRAP-MINE (PROPAGATED) | MELEE-STRIKE (DOCKET) | False |
| `d2-fireclaw-wolf` | MELEE-STRIKE (DOCKET) | SHAPESHIFT (DOCKET) | True |
| `d2-maul-bear` | MELEE-STRIKE (DOCKET) | SHAPESHIFT (DOCKET) | True |
| `chr-bleed-berserker` | MELEE-STRIKE (DOCKET) | DOT-AILMENT (DOCKET) | False |
| `la-perfect-suppression-shadowhunter` | IDENTITY-GAUGE (DOCKET) | SHAPESHIFT (DOCKET) | False |
| `la-demonic-impulse-shadowhunter` | IDENTITY-GAUGE (DOCKET) | SHAPESHIFT (DOCKET) | False |
| `d4-rabies-lacerate` | SHAPESHIFT (DOCKET) | DOT-AILMENT (DOCKET) | False |
| `d4-tornado-werewolf` | SHAPESHIFT (DOCKET) | MULTI-PROJECTILE-VOLLEY (DOCKET) | False |
| `le-werebear-druid` | SHAPESHIFT (DOCKET) | DOT-AILMENT (DOCKET) | True |

Of the 19 conflicts, **8** are SAME-TIER (a kit proposed to two DOCKETs — the discovery docket legitimately lets one kit match multiple axis-signatures). For these, the active row is picked deterministically by **lowest `docket_id`** (docket order: 1 MELEE-STRIKE · 2 IDENTITY-GAUGE · 3 SHAPESHIFT · 4 DOT-AILMENT · 5 MULTI-PROJECTILE-VOLLEY · 6 MINION-PET). The remaining 11 are cross-tier, resolved by RATIFIED>PROPAGATED>DOCKET. This is a data-integrity call, NOT a design ruling — a consumer wanting a kit's alternate family reads the shadowed rows.

### Same-family shadowed duplicates (provenance-preserved, NOT conflicts)

| shadowed tier | shadowed_by (winning tier) | rows |
|---|---|---:|
| DOCKET | DOCKET | 8 |
| DOCKET | PROPAGATED | 9 |
| DOCKET | RATIFIED | 10 |
| **total shadowed** | | **27** |

---

## Gaps (honest holes)

| gap | detail |
|---|---|
| Fresh-draft families unmaterialized | CHAIN-BOUNCE + DASH-STRIKER exist only as B3 fresh-draft flags (grill Appendix B B3) — NO tier artifact enumerates kit_id memberships. Not transcribed; would require a ruling to materialize. On-spine count for both = 0 by absence of source, not by fabrication-refusal. |
| PROPAGATED tier is hypothesis-grade | The 44 τ-propagated rows ran ~1/3 precision (global-τ umbrella defect, per archipelago post-mortem). They are HYPOTHESIS-tier by charter and carry `tier=PROPAGATED` + `shadowed_by` semantics so a consumer can filter them out. Not ratified truth. |
| Off-spine members excluded from spine counts | 117 active rows resolve to a family but sit off the record-267 spine (annex/system games: la/d3/d4/vs/tq/di/hot/chronicon/undecember/tl2/tli/hades1/hades2/tq2/mcd/tl1). They ARE in the sidecar (on_spine=false) but do not count toward the 267 coverage. |
| SUMMONER-LEGION (B3 observation) | grill B3 flags a record-class summoner mass claimed by nothing (Spectres/Skeleton Mages/Golementalist/etc.). No docket exists yet — deliberately NOT invented here. |

---

*Filed by elrond (data steward), 2026-07-22. Materialization is transcription; every row cites its origin.*
