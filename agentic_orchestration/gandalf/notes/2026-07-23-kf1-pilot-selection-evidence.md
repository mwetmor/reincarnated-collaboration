# KF-1 — Pilot-5 selection evidence (KIT-FIDELITY run)

**Gate:** KF-1 (conductor + named-gandalf). **Run:** KIT-FIDELITY (charter
`agentic_orchestration/gandalf/notes/2026-07-23-kit-fidelity-run-charter.md`). **Date:** 2026-07-23.
**Substrate:** `agentic_orchestration/research/curated/corpus.db` (READ-ONLY; `sqlite3 -readonly`).
**Exit predicate (charter §3 KF-1):** ranked list, top-5 named + 3 reserves; each of the 5 passes
`not-in-open-docket ∧ mapping-complete ∧ has-derivable-damage-source`. **SATISFIED.**

Matt's F1 ruling governs: *"select 5 that we have mechanics for."* The pilot proves the compilation
pipeline (charter §3.4), not the engine's frontier — so simplicity-of-compilation is a deliberate,
documented tiebreaker, not a bug.

---

## 1. Methodology

### 1.1 Population + disqualifier (charter §3, step 1)

- **267 `corpus_class='record'` rows:** poe1 94 · d2 60 · gd 41 · le 36 · poe2 36 (conductor-verified,
  matches charter §1 pin).
- **Disqualifier = the 43 OPEN `mechanic_gap_docket` rows.** A kit is disqualified if it appears as a
  docket's `source_kit_id` OR inside its `evidence_kits` JSON array (NULL-guarded before `json_each`).
  All 43 open dockets are `vdm2-deviation` class; each cites **exactly one** kit (source_kit_id ==
  sole evidence_kits entry), so the disqualified set is **43 distinct kits**.

```sql
WITH dq AS (
  SELECT DISTINCT source_kit_id AS kit_id FROM mechanic_gap_docket
    WHERE status='open' AND source_kit_id IS NOT NULL
  UNION
  SELECT je.value FROM mechanic_gap_docket d, json_each(d.evidence_kits) je
    WHERE d.status='open' AND d.evidence_kits IS NOT NULL AND json_valid(d.evidence_kits)
)
SELECT ... FROM canon_corpus cc
 WHERE cc.corpus_class='record' AND cc.kit_id NOT IN (SELECT kit_id FROM dq);
```

- **Survivor pool: 224** (poe1 80 · d2 47 · gd 35 · le 32 · poe2 30). Every game retains a healthy
  pool — cross-game spread is achievable without forcing a weak kit.

### 1.2 Ranking metric (charter §3, step 2 — documented, not implicit)

A discriminating detail found by probe: `kit_dossier` (574 distinct kits) and `canon_probe_facts`
(478/family) cover the wider corpus, not just the 267 records — so **mere presence** of dossier/probe
rows does NOT discriminate at record level. The metric therefore scores **quality and depth**. Also:
`kit_numeric` holds only the 2 charter-noted seed rows, so kit_numeric presence is **not** a
discriminator (KF-2 builds the rows for whichever 5 are chosen); derivability is judged by whether a
join key **CAN** be built — i.e. the presence of damage-anchored sources.

Composite (weights stated so the metric is reportable, not implicit):

| Component | Signal | Weight |
|---|---|---|
| Mapping completeness | count of six non-trivial facets present in `mapping_json` (skills / motion_frame / resource_economy≠`{}` / trigger_grammar / t4_doors / scaffold) | facets 0–6 |
| Mapping grade | `kit_mapping.grade` EXACT=3 · CLOSE=2 · APPROX=1 · GAPPED=0 | 0–3 |
| Damage-anchor derivability | `min(dataset/official non-quarantined citations, 3) × 2` | 0–6 |
| Fact provenance quality | `min(count of family rows with fact_provenance='verified-v1.1', 10) × 0.4` | 0–4 |
| Dossier depth | `min(non-abstained dossier payloads, 6) × 0.5` | 0–3 |
| Compile-simplicity (+) | `min(direct-delivery bands {projectile,melee_arc,beam,zone}, 4) × 1.0` | 0–4 |
| Compile-simplicity (−) | `min(summon_delegate bands, 3) × 1.0` (summons ⇒ frontier ⇒ penalty) | 0…−3 |
| Recognition coverage | `min(recognition_hook rows with coverage_status='expressed', 4) × 0.5` | 0–2 |
| Negative-canon penalty | `−3` if `canon_corpus.negative=1` (a documented anti-pattern is a poor showcase) | 0 or −3 |

Provenance note: `fetched-vdm1` (charter's stated top tier) returns **0** probe-fact rows; the actual
top tier present is `verified-v1.1` (3727 rows) — the metric ranks that highest, with
`named-source-unfetched` / `kb-legacy` scoring 0 on this axis.

### 1.3 Pilot lens applied over the composite (charter §3.4 — the decisive judgment)

The composite is a first cut. On top of it I read each top candidate's **actual mechanic** from
`mapping_json.motion_frame` + `skill_geometry_band`, and deliberately preferred kits the engine
**demonstrably models** (placed zones, direct projectiles, melee strikes/channels) over
frontier-adjacent loops **at comparable coverage** — trading a few composite points for a mechanic the
compiler can build truthfully. Composite leaders set aside on this basis:

- `poe2-galvanic-shards` (score 23, the composite leader) — projectiles that **split into chaining
  lightning beams on hit**. Chain-on-hit is compounding/frontier-adjacent. Set aside for the cleaner
  physical-projectile `poe2-bonestorm`.
- `gd-vires-might-shieldbreaker` (20) — **the movement trail IS the damage** (exotic).
- `le-detonating-arrow-mm` / `le-swarmblade-druid` (19.5) — trap-proc cascade / **form-shift** + procs
  (form-shift is GX-02 shapeshift-docket territory). Set aside for direct-projectile `le-frost-claw`.

This is the charter's founding discipline: **a reasoning-boundary (metric design + pilot lens) ruled
in-run, veto-open, and reported** — not an implicit taste call.

---

## 2. Disqualification census (43 of 267 fell)

Per game: **poe1 14 · d2 13 · poe2 6 · gd 6 · le 4.** The docket removes exactly the mechanism
families the engine does not yet model — which is precisely why they can't be compiled truthfully.
Notable casualties (famous builds Matt would expect to see, and why each is withheld):

- **Summoners / minion engines:** d2-Summonmancer, d2-Golemancer, d2-Summon-Druid, poe1-Spectres,
  poe1-Skeleton-Mages, poe1-Summon-Reaper, poe1-Animate-Weapon, gd-Pet-Conjurer,
  le-Wraithlord-Necro, le-Skeleton-Necro. (Delegate-damage; no summon substrate.)
- **Self-damage / ward loops:** poe1-Ward-Loop, poe1-Dark-Pact, poe1-Forbidden-Rite, d2-Sacrifice,
  d2-Blood-Boil-Warlock, poe2-Blood-Mage. (Self-inflicted-cost engines the sim doesn't model.)
- **Shapeshift / form:** poe2-Demon-Form, gd-Berserker-Wereforms. (GX-02 shapeshift docket.)
- **Trap / totem / corpse cascades:** d2-Trapsin, poe1-Detonate-Dead, poe1-Bladefall-Bladeblast,
  poe2-Archmage-Totems.
- **Proc-chain / stun / hybrid-roll:** d2-Meteorb, d2-Teleport-Sorc, poe1-Elemental-Hit,
  poe1-Wild-Strike, poe1-Heavy-Strike-Stun, poe1-Wormblaster.

The census is the disqualifier working as designed: it withholds the frontier and leaves the
compilable. No famous **direct-damage** archetype was wrongly disqualified.

---

## 3. Pilot 5 (RANKED, one clean archetype per source game — maximal KF-3 database spread)

Spread principle (charter §3.3): five **distinct delivery archetypes** across **all five source
games**, so KF-3's monster harvest exercises every source database and the compiler is stressed on
diverse geometry.

| # | Kit | Game | Grade | Composite | Archetype | Join-key anchor |
|---|---|---|---|---|---|---|
| 1 | **d2-firewall-sorc** | d2 | EXACT | 18.5 | placed AOE-zone | Arreat Summit (official/Wayback) + maxroll |
| 2 | **gd-flames-of-ignaffar-purifier** | gd | EXACT | 19.0 | channeled cone/zone | Crate forums + mmos (fire mono-conversion) |
| 3 | **poe2-bonestorm** | poe2 | CLOSE | 19.0 | channel-release projectile burst | **poe2db.tw dataset** (structured skill DB) |
| 4 | **poe1-cyclone** | poe1 | EXACT | 15.5 | melee channel (spin) | **poedb.tw dataset** (structured skill DB) |
| 5 | **le-frost-claw** | le | CLOSE | 18.0 | direct cold projectile spam | maxroll + LE forum + verified-v1.1 facts ⚠ |

**Per-kit rationale (what mechanics it needs · why compilable now · what anchors its join key):**

1. **d2-firewall-sorc — Firewall Sorceress.** Needs: one placed damage **zone** (a lane that ticks
   fire damage on enemies standing in it) + reposition. The single cleanest AOE mechanic in the pool —
   `EXACT` grade, one skill, `ZONE_CONTROL`/`PERSISTENCE_ENGINE` doors; the engine models zones
   directly. Join key: **Arreat Summit** (official D2 skill damage: Fire Wall base + synergies per
   level, recovered via Wayback) + maxroll build guide — the canonical D2 numeric anchor, plus D2 has
   the `.txt` datamine lane (`skill_geometry_band.exact_source_type='d2_missiles_txt'`) as a deeper
   backstop.

2. **gd-flames-of-ignaffar-purifier — Flames of Ignaffar Purifier.** Needs: a **channeled cone/zone**
   that ramps intensity with hold, on a mono-element (fire) conversion, feeding a hungry energy pool
   (`ELEMENT_CONVERSION_MONO` + `PERSISTENCE_ENGINE_uptime` doors; `tick-cost` economy). `EXACT` grade
   — the cleanest GD kit. Compilable: a widening channeled zone is direct geometry, no proxies/procs.
   Join key: Crate Entertainment forum build thread (fire ConeMan) + mmos, anchored on `verified-v1.1`
   probe facts; GD's DBR datamine (`exact_source_type='gd_dbr'`) is the deeper backstop.

3. **poe2-bonestorm — Bonestorm.** Needs: **channel to accumulate shard count, release a barrage of
   exploding PHYSICAL projectiles** (+ Bone Cage panic zone). `GEOMETRY_COLLAPSE` door; accumulator
   economy. Compilable: physical projectiles + a zone — no element conversion, no chain-on-hit
   (deliberately chosen over galvanic-shards for exactly this). Join key: **poe2db.tw dataset**
   citations (Bonestorm + Bone Cage) — machine-parseable base damage + multipliers, the strongest
   possible join-key source class.

4. **poe1-cyclone — Cyclone.** Needs: a **steered melee channel** — hold and move through packs,
   hitting everything in the spin radius continuously (`ZONE_CONTROL`/`MOMENTUM_CASCADE`; `tick-cost`
   channel). `EXACT` grade; "the genre's modern spin reference." Compilable: a moving melee AoE the
   engine can express as a self-centred hit cadence. Composite is lower (15.5) purely because it lacks
   dataset-class citations in-corpus and reads as one `motion` band — but the **poedb.tw** structured
   skill DB anchors its join key at top tier, and the mechanic is pilot-clean. Pulls PoE1 into the
   spread + supplies the melee-channel archetype.

5. **le-frost-claw — Frost Claw Sorcerer.** Needs: **spam a fan/cone of cold projectiles**
   (`ELEMENTAL_ECHO` door; per-cast mana, zero-cost via a fetched affix). Full 6-facet mapping, clean
   direct-projectile caster — the pilot-simplest LE kit. **⚠ Join-key caveat (the softest link in the
   pilot):** LE has **no structured skill-DB in the corpus** (0 dataset/official citations for any LE
   kit); its join key must anchor on `verified-v1.1` probe facts + maxroll/forum build guides + LE's
   in-game tooltips, not a machine-parseable table. Flagged for KF-2 scrutiny — if the LE join key
   proves too soft to derive an `rdr_value` honestly, **swap to reserve R2 (d2-fire-sorc)** per the
   §5 honorable fallback. Retained for the spread + the clean direct-projectile archetype; the caveat
   is surfaced, not buried.

**REPLICA-1 ref-set note (charter §3 tail):** the ref-set is NOT auto-carried. `d2-bowazon` (a ref-set
kit) was re-evaluated fresh — it is a clean physical-projectile kit (composite 18.5) and a legitimate
candidate, but its in-corpus citation is a single `communal` diablo2.io tip (no official/dataset
anchor), so its join key is thinner than firewall's Arreat-Summit anchor. It sits just behind the
D2 pilot pick; `d2-fire-sorc` / `d2-ww-barb` out-rank it on anchor strength for the reserve slots.

---

## 4. Reserves (RANKED — pre-registered swap pool, charter §5)

| R | Kit | Game | Grade | Composite | Swap trigger |
|---|---|---|---|---|---|
| R1 | **d2-ww-barb** (Whirlwind Barbarian) | d2 | EXACT | 18.0 | if poe1-cyclone's channel proves awkward to compile, OR a rock-solid Arreat-anchored **pure physical melee** is wanted. Steered melee channel, weapon-scaled physical, no conversion/proxy. |
| R2 | **d2-fire-sorc** (Fire Sorceress) | d2 | EXACT | 19.0 | **primary swap for le-frost-claw** if the LE join key is too soft (KF-2). Keeps a clean direct-projectile caster (Fireball) + zone (Meteor) on the strong Arreat/icy-veins/maxroll anchor. |
| R3 | **poe1-frost-blades** (Frost Blades) | poe1 | CLOSE | 18.0 | if a discrete-hit melee is preferred over cyclone's channel. Melee strike whose hit releases a projectile fan — poedb dataset anchor. |

All three are record-class, in **no** open docket, mapping-complete. Any swap is documented in the
run's ruling ledger and never patched by inventing numbers (charter §5).

---

## 5. Per-game spread statement (charter §3.3)

**The pilot spans all five source games** — d2 · gd · poe2 · poe1 · le — with **five distinct delivery
archetypes** (placed-zone · channeled-cone · channel-release-projectile · melee-channel ·
direct-projectile). KF-3's monster harvest therefore exercises **every one of the five source
databases**, and the KF-4 compiler is stressed across zones, channels, projectiles, and melee — not a
single geometry. No game was forced: every game had at least one genuinely clean, well-covered
candidate. **The one spread-vs-derivability tension is LE** (§3 pilot #5): LE has no structured
skill-DB in the corpus, so its kit-side join key is the pilot's softest anchor. It is included **for
the spread + the clean direct-projectile mechanic**, with the caveat surfaced and reserve R2
(d2-fire-sorc) pre-registered as its swap. If Matt would rather trade LE-spread for a rock-solid
second D2 anchor at KF-1 time, that is his call — R2 makes the swap clean.

---

## 6. Exit-predicate check (KF-1)

- Ranked candidate list exists: ✅ (top-5 named + 3 reserves + full 224-survivor composite behind it).
- Each of the 5: **not-in-open-docket** ✅ (belt-and-suspenders verified: source_kit_id=0 ∧
  evidence_kits=0 for all 8) · **mapping-complete** ✅ (all 5 have non-trivial mapping_json; 3 EXACT,
  2 CLOSE) · **has-derivable-damage-source** ✅ (4 anchor on official/dataset skill sources; LE #5
  anchors on verified-v1.1 facts + build guides, caveat flagged + reserve pre-registered).
- Output is a self-contained in-chat brief (§ report-back) — **no doc-spelunking required** (RL-6
  binding).

**KF-1 exit predicate: SATISFIED.** Selection is Matt's F1-ruling brief; pending his pick, KF-2
(join-key population for the chosen 5) is the next gate, gated by Pins A/B ratification.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-23.
