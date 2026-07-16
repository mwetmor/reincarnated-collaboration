# Corpus curation log — Edition-III Stage B: Lost Ark 58-row class-engraving curation

> **STATUS:** CURRENT (record of a completed ingest + key batch). Edition-III Stage B.
> **Author:** elrond (data steward) · **Date:** 2026-07-15
> **Store:** `agentic_orchestration/research/curated/corpus.db` (elrond-owned, gitignored — this log is the committed record)
> **Batch class:** INGEST + KEY (class-engraving grain). Additive; NO treatment=hybrid keys; NO survivor re-keys.
> **Script:** `agentic_orchestration/research/scripts/corpus_edition3_stageB_lostark58_2026_07_15.py`
> **Source:** `agentic_orchestration/legolas/findings/2026-07-15-lost-ark-classkit-tranche/rows/*.jsonl` (29 files × 2 rows = 58; gandalf-verified ACCEPT)
> **Commission:** `agentic_orchestration/gandalf/briefs/2026-07-15-elrond-edition3-one-batch-commission.md` §2.

---

## 0. What landed

58 Lost Ark rows at **class-engraving grain** (29 classes × 2 identity paths), `la-` prefix, keyed
into corpus.db at full completeness. Corpus 651→**709** (+58); engine_key 625→**683** (+58). All 58
key as `combat-kit`; the raw JSONL row is preserved verbatim in `canon_engine_key.raw_json` (no
destructive transform). `la-` corpus rows total = 62 (58 class-engraving + 4 Destroyer skill-grain
from Stage A).

## 1. Honing-economy confound law (every row)

LA power is gear-honing-indexed (`honing_confound` + `il_confound` on every row: e.g. *"skill damage
and crit values scale with honing tier"*, IL-1100 Enlightenment gate). Kit-identity claims key ONLY
from class design. Concretely, to keep honing out of the keys:
- **`amp_val`** derived from the CLASS-DESIGN cadence (BURST identity → `spiky`; SUSTAINED → `flat`),
  NEVER from the honing-scaled amp-magnitude prose (which reads "Crit +9-15% at max level" etc.).
- **`tempo_val`** = design cadence (BURST→high / SUSTAINED→med), NOT a honing-ceiling tier claim.
- The honing confound is CARRIED into `flags` (`honing-economy-confound:…`) + `mech_note` on every
  row, so the contamination is legible but never leaks into `treatment`/`function`.

## 2. Six normalization dispositions (brief §2) — executed with provenance

| # | disposition | rows | provenance |
|---|---|---|---|
| 1 | `group_context` ABSENT → **false** | `la-destroyer-rage-hammer`, `la-destroyer-gravity-training` | index census names 6 group-context rows; Destroyer not among them |
| 2 | `group_context` ABSENT → **false** | `la-slayer-predator`, `la-slayer-punisher` | same census backing |
| 3 | `pull_carrier` ABSENT → **false** | `la-slayer-predator`, `la-slayer-punisher` | index pull census EXACT: Destroyer ×2 only |
| 4-5 | `legacy_engraving_system` false → **TRUE** | `la-souleater-nights-edge`, `la-souleater-full-moon-harvester` | in-row evidence: `legacy_engraving_name` present + `engraving_debut` Global Dec 2023; index finding 4 lists Ark-Passive natives as Valkyrie/Guardianknight/Wildsoul ONLY → Souleater is legacy-converted |
| 6 | `la-sorceress-reflux` `pull_carrier` null → **false** (RESOLVED) | `la-sorceress-reflux` | bounded search — see §3 |

Each normalization is recorded in the row's `flags` (`normalization:…` tokens) + `mech_note`. The
ORIGINAL (pre-normalization) values are preserved in `raw_json` — the normalization is a keying
decision on stated evidence, fully reversible.

## 3. Sorceress Reflux pull_carrier resolution (disposition 6)

The index flagged `la-sorceress-reflux` `pull_carrier: null` (PENDING) with `control.ailments`
including `pull` — *"Reverse Gravity by name implies gravitational pull mechanic … Conf 0.75 pending
verification."* Resolved via the index's recommended **bounded targeted search** ("Lost Ark
Sorceress Reflux Reverse Gravity vacuum pull skill", executed 2026-07-15, one pass).

**Finding.** Reverse Gravity is a **tripod-conditioned lift-and-slam**: *"disengaging gravity to
send anyone in her personal space floating upward, then re-engaging it … to slam them back to the
ground."* It has a vacuum-GROUP side effect (*"vacuum/pull effect that groups enemies together
before the impact"*), but the source frames it as a **push/lift** mechanic (*"while it won't LIFT
push-immune bad guys"*).

**Verdict: `pull_carrier=false`, RESOLVED (not merely PENDING).** Under the register v1.2 boundary
rule — `pull` = INWARD HORIZONTAL displacement, force DIRECTION defines the level — Reverse Gravity's
dominant mechanic is vertical (float-up + slam-down), not the horizontal inward-draw the register
`pull` defines. And under the intrinsic-only bar, the effect is a **tripod outcome** (LA's
skill-upgrade tree = a conditional-behavior/configuration layer, closer to gear-assembly than
base-skill-intrinsic). The evidence does not establish an intrinsic horizontal pull at
class-identity grain. The PENDING provenance is preserved in `flags` + `mech_note`; the raw `pull`
ailment token stays in `raw_json` (never destroyed) but does NOT set `ctrl_function=pull`. Reflux
keys `ctrl_function=knockback` (its base Sorceress skills DO apply knockback per the row evidence —
the honest non-pull key). **Pull census stays EXACT: Destroyer ×2 only.**

## 4. Pull census (index EXACT) — 2 carriers

The 2 index-census pull carriers key `ctrl_function=pull` as a RIDER on a damage-primary identity
(honing-confound-clean — pull is a class-design density mechanic, not gear):
- `la-destroyer-gravity-training` — `control.ailments=["pull","stagger"]`, `centrality=core`; Vortex
  Gravity is the SOLE active in Hypergravity Mode → the pull-carrier identity. cell_key
  `rooted|at-target|spiky|melee_strike|damage|pull|absorb|generator-spender|solo|melee|high|channel|active|build→spend`.
- `la-destroyer-rage-hammer` — `pull_carrier=true`, `centrality=rider`; amplifies Gravity Release
  skills incl. the pull-containing Gravity Compression. cell_key
  `rooted|at-target|flat|melee_strike|damage|pull|absorb|generator-spender|solo|melee|med|channel|active|build→spend`.

All 56 other identity paths key `ctrl_function` per the ailment map (NOT pull), asserted in-script:
the pull-keyed LA set == exactly {`la-destroyer-rage-hammer`, `la-destroyer-gravity-training`}.

## 5. Group-support rows (6, C2 ruling) — collected, not dropped

The 6 index-census group-context rows (`la-artist-full-bloom`, `la-bard-desperate-salvation`,
`la-bard-true-courage`, `la-gunlancer-combat-readiness`, `la-paladin-blessed-aura`,
`la-valkyrie-liberator`) key as **combat-kit with `group_context=true` preserved** (flags:
`group_context:true;context=group-support;solo-legible-identity-keyed;C2-preserved`). Their
`treatment`/`function` reflect the solo-legible identity (damage-primary or support-buff-utility);
the group-context flag is first-class so downstream analysis can segment them. NOT silently dropped,
NOT force-negated to system-record. Asserted in-script: the group-context-keyed set == exactly the
index census 6.

## 6. Isotope collapse (flag-c cross-grain + intra-LA) — explicit verdict, not silent coexistence

The 58 LA rows occupy **43 distinct cell_keys** (34 singleton + 6 doubles + 1 triple + 1 quad + 1
quintuple). This is the expected **element-free-key isotope collapse** (register §2): LA class
identities sharing the same 14-coordinate abstract signature (differing only in element/flavor/
numbers, which the identity key EXCLUDES by design) legitimately co-inhabit one atlas cell. The
heaviest cluster is the melee-warrior/martial-artist `damage|knockback/none|…` region (5 rows →
one cell: Deathblade Surge / Reaper Lunar Voice / Scrapper Shock Training / Souleater Full Moon
Harvester / Striker Deathblow).

**Verdict (flag c):** same-cell coexistence at atlas grain is LEGITIMATE. **All 58 rows persist as
distinct kit_ids with full provenance** (raw_json, mech_note); the atlas cell carries the
multiplicity as `kit_count`/depth. The collapse is a truth about the genre's behavioral clustering,
not a keying loss. Cross-grain: the 6 Destroyer rows (4 skill-grain + 2 engraving-grain) are all
distinct cells — the skill-grain rows use `delivery=melee` + specific geometries, the engraving-grain
rows use `delivery=at-target` + `melee_strike`, no collision.

## 7. UPGRADE-OWED confidence bands (carried, not blocking)

Per-row confidence bands carried into `flags` (`UPGRADE-OWED:…`): Valkyrie ≤0.8, Guardianknight ≤0.8,
Wildsoul 0.75-0.8, Souleater 0.85, Aeromancer tier-uncited. Keys are CATEGORICAL, so conf-banded
NUMERIC values do not block keying. The official-patch-notes / namu.wiki-KR backfill stays a
REGISTERED future legolas item (not this batch).

## 8. Naming

"Dragonknight" (brief) = **Guardianknight** (official Global). Index resolution stands; kit_ids as
committed (`la-guardianknight-dreadful-roar`, `la-guardianknight-hellfire-successor`). No separate
dragonknight rows.

## 9. Proofs (in-script, all PASS)

| proof | result |
|---|---|
| row count | 29 files, 58 rows ingested |
| disposition 4-5 | souleater legacy_engraving_system false→TRUE applied (both) |
| pull census | pull-keyed LA set == {rage-hammer, gravity-training} (index EXACT) |
| disposition 6 | Sorceress Reflux keyed function=knockback (NOT pull) |
| group-support | group-context-keyed set == index census 6 |
| frozen-guard | 469 survivors + 7 Stage-A rows byte-identical before+after |
| counts | corpus 651→**709** (+58); engine_key 625→**683** (+58); hybrid **0** |

Treatment×function distribution (LA 58): damage/knockback 33 · damage/none 18 · damage/stun 3 ·
damage/expose 2 · damage/pull 2. **All damage-primary** — no forced hybrid, no forced
control-primary; the frontier stays honest.

WAL checkpointed; integrity_check = ok.

## 10. Reversibility

Every mapping is a stated rule over the tranche's own fields (documented in the script's field
mappers). The raw JSONL row is preserved verbatim in `raw_json`. The ingest is idempotent. Backup
`corpus.db.pre-edition3-2026-07-15-backup` preserves the pre-batch state.

---

**Signed:** elrond (data steward) — 58 class-engraving identities keyed from class design alone,
the honing economy held out of every key, the six normalizations applied on evidence with the raw
preserved, the pull census kept exact, the supports collected not dropped, and the isotope collapse
named as the honest genre clustering it is.
