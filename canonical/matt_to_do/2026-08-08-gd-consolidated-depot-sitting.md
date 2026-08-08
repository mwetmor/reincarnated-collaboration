# T15 — ONE consolidated DepotDownloader sitting (monster stat-table closure + all parked depot rows)

**Parked:** 2026-08-08, gandalf (`RUN-CONDUCTOR`, KC2-SIM), under charter amendment **R-KC2-8**
(Matt: *"I definitely do not want to ship the data packet (baton) without the actual monster stat
tables"*) — ledger L-55, `agentic_orchestration/gandalf/notes/2026-08-07-kc2-sim-run-ledger.md`.
**Why only Matt:** Steam-authenticated depot fetch (the T7/T10/T12/T13 pattern) — agents hold no
Steam credentials. DepotDownloader is resident at `vendor/depotdownloader/` on THIS Mac.

## What you already hold — buy/download NOTHING new

- **Edition-II `.arz` database records** — base + gdx1 + gdx2 + gdx3 (T7, struck 2026-07-24;
  16 files, 189 MB, `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`). These carry the
  monster stat RECORDS (HP / damage / resist fields) that G-STATS reads.
- **Crucible/SurvivalMode `.arz` ×3** (T4, struck 2026-07-23, `~/Games/vendor/grim-dawn/`).
- The sitting below fetches the RESIDUAL only: template + script + level/map archives that turn
  those records into fully-derived stats (the C-1 band-A eHP class, 7/896) plus the FoA-era
  Crucible currency (`survivalmode3`).

## The action — one sitting, four parked rows close at once (~15–30 min)

Same DepotDownloader pattern as T7 (the working precedent: `2026-07-24-gd-edition-II-steam-fetch.md`).

1. **The widened L-46(e) list** (the KC2-SIM load-bearing item): `templates.arc` + `Scripts.arc` +
   `Maps.arc` + `Levels.arc` (base + gdx1/gdx2/gdx3 equivalents) + the **FoA `survivalmode3`**
   depot (gdx3-era Crucible) → into `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`.
   *(By the R-L53-1 loading law, FoA's Maps re-ship supersedes sm1 exactly as sm1 superseded
   sm_mod — this fetch is what makes the loadable-arena determination current.)*
2. **T10-depot** (parked 2026-07-30): gdx3 `Creatures.arc` (~0.5 GB) → `vendor/grim-dawn/`.
   Werewolf `.anm` timings; the parser is already written.
3. **T12** (parked 2026-08-01): `Levels.arc` ×4 — **size-check FIRST** (largest archive class in
   a GD install; several-GB likely). Subsumed by item 1's Levels entry — one fetch covers both rows.
4. **T13** (parked 2026-08-04): Edition-III **manifest LOOKUP first** (client v1.3.0.5 vs corpus
   1.3.0.0; the T7 precedent — Edition-I→II manifests were byte-identical for base/gdx1/gdx2).
   Only depots whose manifests CHANGED get re-fetched, into
   `/Users/admin/Games/vendor/grim-dawn-edition-III-<date>/`.

On intake: legolas SHA-pins + inventories every file (standing pattern from the T7 cut record).

## What it unblocks

- **G-STATS** — the KC2-SIM baton-emit gate born of R-KC2-8 (spec § 11, 33rd check): every encoded
  wave's roster INCLUDING summon bodies must carry MEASURED combat stats (eHP inputs + damage)
  folded into the sim's kill term before the baton emits. The run PARKS at G-STATS (emit withheld,
  everything else delivered) until this sitting lands.
- **C-1 closure lap** (band-A eHP, 7/896 — THE load-bearing open item for T-1 per the locomotion
  lap): templates close the derivation class. Whether the pull FULLY closes C-1 is the closure
  lap's finding — residuals surface as named findings; G-STATS holds the emit either way.
- **U-8 G1** (the widened item's original target) · T10's werewolf-form player timings · T12's
  per-room placement counts · T13's boss-HP-hotfix experiment — the full parked-row set.
- **GAUNTLET-HARNESS** (sequel candidate registered at L-55): corpus kits vs Crucible 150+ for
  WR/KPM bands — gated on this sitting + C-1 closure + the fixture-reproduction gate.

**Not blocking the run's current beats:** the Gate-2 verdict fold, mechanism adjudication, G-D
close, and Phase-E seeded-batch prep all proceed without it — only the EMIT blocks.

---

## ✓ DONE 2026-08-08 — struck by Matt under ruling R-T15-1 (the Edition-III cut)

The pre-fetch gate found **PIN DRIFT** (client v1.3.0.5 vs corpus 1.3.0.0): the residual fetch
this file scoped would have produced a **hybrid corpus** — v1.3.0.5 archives over 1.3.0.0 records.
Matt cut **Edition-III whole** instead: `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/`
— 38 data files, 3.4 GB, buildid 24619876 (patched 2026-08-07T19:33Z); predicted manifest table
(`depot.pins.predicted.txt`) registered pre-fetch, scored **8/8**; `templates.arc` PRESENT;
Levels ×4 · Maps ×4 · Scripts ×8 · Creatures ×5 incl. gdx3. Closes T10-depot + T12 + T13 with
this row.

- **FINDING A** — manifest-pin premise validated bidirectionally (changed ⇒ differ 7/7;
  unchanged ⇒ identical 1/1; T7's converse 11/11); public PICS mirror == authenticated read 8/8
  ⇒ no-auth corpus-drift detection going forward → jack-ryan decisions-log candidate.
- **FINDING B** — the corpus MOVED under the live run (`database.arz` + `SurvivalMode3.arz` +
  Text_EN changed; only `SurvivalMode2.arz` identical) → **R-KC2-9 (Matt):** KC2 results are
  Edition-II-scoped (correct for fixture explanation — both sittings predate the patch);
  **G-STATS reads Edition-III; the baton emit stays PARKED until it does.**
- Intake (SHA-pin + inventory, T7 pattern) + record-granularity II→III diff commissioned to
  legolas at fold **L-59**. Edition-II tree verified untouched (16/16 SHA); Edition-I freeze
  untouched.

**Fold:** KC2 ledger L-59, `agentic_orchestration/gandalf/notes/2026-08-07-kc2-sim-run-ledger.md`.
