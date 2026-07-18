# MIGRATION — VDM-1 stale-flag bulk reclassification (`mobile_blocking_mechanics`)

**Date:** 2026-07-18
**Author:** elrond (single-writer of `corpus.db`)
**Store:** `agentic_orchestration/research/curated/corpus.db` → `canon_corpus`
**Script (byte-rebuildable):** `agentic_orchestration/research/curated/scripts/corpus_stale_flag_reclass_2026_07_18.py`
**Charter:** `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-charter.md` §2 — the 2026-07-12 `mobile_blocking_mechanics` flags ruled "stale; refreshed during probe backfill, never trusted as current truth."
**Triage input:** `agentic_orchestration/research/vdm1/stage0/stale-flag-inventory.md` (legolas Stage-0, commit 6ea07069 — triaged all 515 flagged rows).
**Backup (WAL-consistent `.backup`):** `corpus.db.pre-stale-reclass-2026-07-18-backup` — md5 `4d2f9e961f214f15962f6d742e28ab8a` (integrity ok, 585 rows; gitignored per curated-dir policy).
**schema_meta ledger:** row `stale-flag-reclass-2026-07-18` (corpus_schema_meta 17 → 18).

---

## Rule applied

The mechanical tier ONLY: for the 16 flag values legolas classed **STALE-LANDED** (mechanism now
fully in-engine via mechanics-run Waves A/B/C + ailment-layer, i.e. Waves A–D per
`canonical/current-to-end-state/current-to-end-state-engine.md`), the flag no longer describes a
current blocker. Each such flag was moved aside **additively** — history is NOT deleted:

- **(a) original survives, queryable** — new column `canon_corpus.mobile_blocking_mechanics_archived TEXT`
  receives the original string, provenance-prefixed `LANDED-<wave>: <original string>`.
- **(b) live reading no longer presents as a blocker** — `mobile_blocking_mechanics` for those rows
  set to sentinel **`expressible-now`**.
- **(c)** per-flag-value count ledger below.

`<wave>` is the landing wave named in legolas's per-flag "Status:" line (A / A+B / B / B+C / C / C+D).

**Reversibility:** the raw form is preserved twice — in the archived column and in the file backup.
Restoring the original live flag = `UPDATE canon_corpus SET mobile_blocking_mechanics =
substr(mobile_blocking_mechanics_archived, instr(mobile_blocking_mechanics_archived,': ')+2)
WHERE mobile_blocking_mechanics_archived IS NOT NULL;`

---

## Count reconciliation (inventory "~397" → exact 402)

Legolas's inventory summarized the STALE-LANDED tier as **~397**. The **exact** sum of the 16
per-flag counts in his consolidated register is **402**. The full partition of the 515 flagged rows
is exact and reconciles cleanly:

| Tier | Rows |
|---|---:|
| STALE-LANDED (reclassified this run) | **402** |
| STALE-PARTIALLY / STALE-LARGELY (deferred, per-kit split) | 79 |
| classification-workflow artifact `evidence record — see harvest report` (deferred) | 18 |
| STILL-OPEN `form-swap` (10) + `union/recipe` (6) (deferred) | 16 |
| **Total** | **515** |

(402 + 79 + 18 + 16 = 515.) The "~397" was an approximation in the inventory's summary block; the
register's per-flag arithmetic is authoritative. No row was reclassified that legolas did not class
STALE-LANDED.

---

## Per-flag-value count ledger (STALE-LANDED — reclassified)

| Rows | Landed wave | Archived as `LANDED-<wave>: <flag>` (original flag string) |
|---:|:--|:--|
| 193 | A | direct-hit instant verbs native |
| 66 | A+B | soul-control troop command exists; turret/pet AI variants + summon economy needed |
| 39 | B+C | sustained-stream/channel verb + movement-tax tuning |
| 32 | C | mark/tag ledger + consume-trigger operators |
| 18 | C | rotational/orbital substrate addendum — build pending |
| 11 | C | thorns/stat-retaliation channel |
| 8 | B+C | self-cost contract operators |
| 8 | A | battle-sim auto-aim native |
| 7 | C+D | return-path/carom projectile solver |
| 7 | B | reservation/aura toggles — loot-operator extension |
| 3 | B | on-kill resource-spawn economy (corpse/soul ammo) |
| 3 | B | finite-ammo/consumable economy |
| 3 | C | element-application addendum covers hybrid caps — status-gate ops verify |
| 2 | B+C | lodge/retrieve ammo economy + return-path solver |
| 1 | A | reap/possession is RDR-native |
| 1 | A | default-attack scaling native to sim |
| **402** | | **live flag → `expressible-now`; original preserved in archived column** |

---

## Deferred tiers — UNTOUCHED (explicitly not this run)

No row below was altered: live flag unchanged, no archived value written. Verified POST (see asserts).

### STALE-PARTIALLY / STALE-LARGELY — per-kit split needed (79 rows)
| Rows | Flag | Why deferred |
|---:|:--|:--|
| 45 | no rule matched — Mac pass to classify | classification-workflow artifact; per-kit reclassify vs Wave A–D vocab |
| 17 | dash/blink verb — sim support verify; deflect riders new | dash/blink landed, deflect in Wave-D fidelity ledger — split per kit |
| 9 | echo/clone actors — troop-command adjacent | mostly landed; true player-input mirroring may surface fidelity note |
| 5 | persistent/mobile zone entities — VFX slot model adjacent; follow-zones new | static zone landed; mobile follow-zones not in spec |
| 3 | stochastic ops in loot-operator framework — per-cast roll verify | largely landed; per-kit surface verify |

### Classification-workflow artifact (18 rows)
| Rows | Flag | Why deferred |
|---:|:--|:--|
| 18 | evidence record — see harvest report | not a mechanism descriptor; requires per-kit harvest-report lookup |

### STILL-OPEN — do NOT touch (16 rows)
| Rows | Flag | Why deferred |
|---:|:--|:--|
| 10 | form-swap stat-block hotswap | GX-02 shapeshift docket OPEN; Matt forks A–E unruled |
| 6 | union/recipe evolution system (pair-grain authoring) | no Wave coverage; docket candidate |

**form-swap 10:** `chr-fire-berserker, d4-pulverize, d4-rabies-lacerate, di-blood-knight,
di-druid-bear, gd-berserker-wereforms, le-reaper-form-lich, le-swarmblade-druid, poe2-demon-form,
poe2-shaman-bear`.
**union/recipe 6:** `hades1-merciful-end, hades2-glorious-disaster, hades2-hail-storm,
vs-fuwalafuwaloo, vs-phieraggi, vs-vandalier`.

---

## Asserts (all PASS; single transaction, ROLLBACK-on-any-mismatch)

| Assert | Result |
|---|---|
| Total `canon_corpus` row count unchanged | 585 → 585 ✓ |
| Content-md5 over the **66 untouched columns** (all except `mobile_blocking_mechanics`) byte-identical | PRE `e11b431380a2b2ba97ae994e15fc1dbe` = POST `e11b431380a2b2ba97ae994e15fc1dbe` ✓ |
| DO-NOT-TOUCH 16 rows (form-swap 10 + union/recipe 6) unchanged across pre-existing columns (incl. their live flag) | PRE `b69e11dfaff0c2a2bab454313078beb0` = POST `b69e11dfaff0c2a2bab454313078beb0` ✓ |
| STALE-LANDED rows migrated (archived-prefix count == sentinel count == 402) | 402 = 402 ✓ |
| Half-migrated rows (archived XOR sentinel) | 0 ✓ |
| Residual live-blocker rows (live flag non-null, non-sentinel) == deferred-tier sum | 113 = 113 ✓ |
| No deferred flag value altered; no archived value on any deferred row | 0 deferred rows touched ✓ |
| All pre-existing table row counts conserved; `corpus_schema_meta` +1 | conserved; 17 → 18 ✓ |
| `PRAGMA integrity_check` | ok ✓ |

**Untouched-column invariant construction:** the md5 is computed over the 66 columns of
`canon_corpus` EXCLUDING `mobile_blocking_mechanics` (the only live field mutated) and the
freshly-added `mobile_blocking_mechanics_archived` (purely additive; did not exist PRE). Column set
is derived at runtime from `PRAGMA table_info` so a future column-add cannot silently drop out of the
invariant. The deferred-16 fingerprint intentionally INCLUDES `mobile_blocking_mechanics` — those
rows' live flag must survive intact — and excludes only the new archive column (NULL for them).

**Post-commit checkpoint:** `PRAGMA wal_checkpoint(TRUNCATE)` returned `(0,0,0)` — committed pages
folded into the main file, no residual WAL, so concurrent `sqlite3 -readonly` crawlers observe the
committed state. (Two `.backup` / readonly-open steps hit transient SQLITE_CANTOPEN(14) from
concurrent-crawler sidecar contention; re-verified clean via `immutable=1` and a busy-timeout retry.
The backup file is a standalone consistent DB — integrity ok, 585 rows, untouched-md5 matches live.)

---

## Concurrency note

Two legolas crawl agents were reading this DB via `sqlite3 -readonly` throughout. The write was a
single short transaction (one `ALTER ADD COLUMN` + 16 `UPDATE`s + one meta `INSERT`) under
`PRAGMA busy_timeout`; WAL journalling kept readers non-blocking. Post-run TRUNCATE checkpoint left
the store clean for them.

---

## Not in scope / follow-on

- The deferred STALE-PARTIALLY (79) and artifact (18) tiers are the probe-backfill lane's per-kit
  reclassification work — NOT a mechanism gap for most, but requires per-kit judgment.
- STILL-OPEN form-swap (GX-02, Matt-gated) and union/recipe (docket candidate) remain correctly
  flagged as live blockers; they are the probe-backfill lane's evidence-collection targets.
- The sentinel `expressible-now` is a *live-reading* convenience, not a claim of EXACT engine
  fidelity: several landed mechanisms carry Wave-D fidelity-ledger residue (orbit 2D sub-projectile
  motion, deflect conditions) that is enhancement, not structural blocker. See inventory
  "Fidelity-deferred" note.
