# GD-SLICE run charter (RATIFIED by standing rulings — TSR-5 "skill slice charters the moment TSR-3 rules"; TSR-3 RULED GD-first, Matt 2026-07-24)

**Date:** 2026-07-24 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executes:** elrond (schema + adapter + curation) — **serial AFTER his LE-park commission returns** (same-seam discipline)
**Pattern:** desirable-run (`operating-procedures/desirable-run-pattern.md`) — fit test §2
**Sequencing:** parallel-safe with TSF6-TRACK-A (elrond vs gamora seams, no shared writes — TSR-5 ruling)

---

## §0 Intent (the owner's question, one sentence)

Prove the TRUE-SOURCES pipe end-to-end **at width one**: GD .arz primary source → GD adapter → the ONE normalized exact-fields schema (TSR-2) carrying player-facing canonical values + raw provenance columns (TSR-1) → corpus rows for **Flames of Ignaffar**, verified byte-true against .arz ground truth (TSR-4 tier-1 family anchor + tier-2 in-pipe asserts).

**Rubric-law note:** the owner's question is "does the adapter architecture WORK end-to-end on the hardest landed source" — one skill through the whole pipe, EXACT. This run is **not coverage** (the harvest lap is next) and not the monster lane (TSF6-TRACK-A). VERIFIED claim ceiling: "the GD adapter path is proven at width one."

## §1 Substrate (bounded, frozen at launch)

| Item | Role |
|---|---|
| `GDX1.arz` → `records/skills/playerclass07/purifyingflame1.dbr` (on disk at `~/Games/vendor/grim-dawn/`) | FoI ground truth — 26-rank arrays (`skillMaxLevel` 16 + 10 ultimate), cone geometry (`maxRange` 9.1 / `endWidth` 4.5 / `startWidth` 2.2), `timeBetweenAttacks` 300 ms, `skillManaCost` r1 7.0 → r26 69.0, fire min/max + burn DoT + `weaponDamagePct` rank tables |
| legolas TQIT parser knowledge (probe §0: 24-byte header, LP_string record entries, LZ4-block, type-IDs, flat string table) | format truth — elrond productionizes into HIS curation tooling (the probe script was an instrument, not a product) |
| `agentic_orchestration/research/curated/corpus.db` | the write target — **elrond's Matt-authorized write channel; READ-ONLY law for every other agent** |
| `agentic_orchestration/legolas/notes/2026-07-23-gd-arz-extraction-probe.md` §2 | the anchor-verify oracle values (G3) |

## §2 Fit test

- **F1:** YES — one skill, one game, one schema draft, enumerable columns + gates.
- **F2:** YES — G1–G5 all machine-checkable; exit = gates green + slice report + MIGRATION.
- **F3:** YES — architecture forks pre-drained (TSR-1 truth register, TSR-2 adapter shape, TSR-4 verification stack); residual schema micro-calls are elrond's seam authority + conductor reasoning-boundaries (ledger GSL-1..n).
- **F4:** YES — TRUE-SOURCES intent is conductor-resident (the grill's author); elrond owns schema/curation seam.

→ gandalf conducts; elrond executes; KR not engaged (single-seam).

## §3 Pre-registered gates

- **G1 — schema:** normalized exact-fields schema draft committed as a MIGRATION note (elrond's shape call). MUST carry: player-facing **canonical value** columns + **raw provenance** columns (raw field name, raw value, source record path, source file + version/patch) per TSR-1; game-agnostic core + per-game extension pattern per TSR-2 (the first adapter proves the schema).
- **G2 — adapter:** FoI rows land via the adapter; **tier-2 in-pipe asserts green on every row** (non-null, monotonic rank arrays where the field class implies monotonicity, range bounds) — oracle-free, mechanical.
- **G3 — anchor verify (tier-1):** landed values **BYTE-MATCH** the probe-note .arz values across the five R-K5 field families + geometry + cadence + the 26-rank count. FoI = GD's first formula-family anchor in the TSR-4 compiler-test-suite. **Any mismatch = HALT-diagnose** (parser vs adapter vs schema — name which layer), never tolerance-fudge.
- **G4 — provenance + name bridge:** raw columns populated; display name via the `skillBitmapName` workaround (`skillicon_flamesofignaffar1up.tex` → "Flames of Ignaffar", probe §3) with a provenance flag noting the .arc tag-bridge (`tagGDX1Class07SkillName04A`) is pending — **.arc parsing is NOT in scope**.
- **G5 — contradiction hygiene:** existing grimtools-derived GD rows (60-rank shape) FLAGGED in curation notes against the 26-rank primary truth. **No silent overwrite of banked rows this run** — reconciliation is the harvest lap's charter.

**Honorable fallback:** a record-class the probe didn't cover fails to parse → **BLOCKED-FORMAT** with bytes-evidence; the run completes on what parses and says so out loud.

## §4 Sequencing + Matt interface

- **Elrond serial order:** LE-park commission (TSR-7(ii), executing) FIRST → this slice SECOND. Conductor fires the slice commission when the park returns verified.
- **In-run:** red-flag pings only; rulings ledger GSL-1..n, veto-open.
- **At end:** slice report + schema MIGRATION → jack-ryan Gate-2 (corpus-write class) → Matt's eye. The slice's schema is the template the remaining adapters (D2, PoE1, PoE2, D4) build against — that generalization moment is a Matt checkpoint, not an in-run commitment.

---

## §5 Run status (conductor ledger)

- **2026-07-24 — chartered.** Elrond LE-park fired first (same turn); slice commission fires on park-verified. Report lands at `agentic_orchestration/elrond/notes/2026-07-24-gd-slice-run.md`.
- **2026-07-24 — commission fired** (LE-park verified `796025b9`; elrond background, same-seam serial honored).
- **2026-07-24 — RUN EXECUTED, ALL GATES GREEN — RUN DONE** (elrond `ebb9f95b`: adapter 560 lines + MIGRATION 190 + report 71). **G1 PASS:** `exact_skill` + `exact_skill_field` landed additive in corpus.db (backup + md5 first); TSR-1 served by explicit `canon_key`↔`raw_field` two-column mapping; TSR-2 by per-row `is_core` — **107 core + 29 GD-extension**, next adapter adds extension rows with zero schema change. **G2 PASS:** probe parser productionized into reusable `ArzArchive`; 136 rows, tier-2 asserts 136/136; one parser bug found+fixed (string-table u32 count-prefix; record-walk lands exactly on end boundary post-fix). **G3 PASS 22/22 BYTE-MATCH** — with the charter's HALT-diagnose law exercised as written: first run failed 3/22 on statics (9.1/2.2/0.3); diagnosed to the COMPARISON layer (float32 has no exact 9.1; the widened float64 IS the byte-true value; `struct.pack('<f',…)` round-trip proof); fix = bit-pattern equality at source-native single precision — **no epsilon, no tolerance-fudge**. **G4 PASS** (raw provenance populated; `skillBitmapName` name workaround; `.arc` tag-bridge + `source_version` flagged pending). **G5 PASS, ZERO overwrites** — the grimtools 60-rank shape is banked NOWHERE in corpus (FoI `kit_numeric` = formula scalars); contradiction lives only in the source-probe note; flag recorded at MIGRATION §G5. **Conductor verification (sequence recorded honestly):** elrond's commit rode the conductor's `f93f61e8` push BEFORE verification (it sat beneath the TSF6/bake-off closure commit in local history); verification executed immediately after and CLEAN by conductor's own hand — independent `--verify-only` re-run re-parsing `GDX1.arz` primary source = 22/22 PASS + read-only DB spot-check (header 26-rank exact; 136/107 counts; fire-min 8/129/262, weapon-% 9/42/58 vs oracle). **Exit predicate MET.** Four harvest-lap hand-offs flagged in the report (geometry-band `exact_json` upgrade, `source_version` via depot manifest, `.arc` bridge, grimtools-row re-verification rule); the **generalization moment** (this schema as the D2/PoE1/PoE2/D4 adapter template) stays a MATT CHECKPOINT per §4, not auto-fired. jack-ryan Gate-2 (corpus-write class) rides the standing queue.

---

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-24.
