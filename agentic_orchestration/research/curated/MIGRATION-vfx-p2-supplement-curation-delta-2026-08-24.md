# MIGRATION — VFX P2 SUPPLEMENT curation DELTA, 2026-08-24

**Schema version stamp:** `vfx-p2-supplement-curation-2026-08-24/P2-delta`
**Author:** elrond (data steward), named sub-agent of gandalf (`RUN-CONDUCTOR`)
**Run:** VFX ARCHETYPE-BINDING RUN — charter `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md`, ledger **L-30** (supplement lane fired, jobs 27–30) / **L-32** (lane closed, rc=0 ×4)
**Script:** `../scripts/vfx_p2_supplement_curation_delta_2026_08_24.py` (transactional, idempotent, additive)
**DB:** `agentic_orchestration/research/curated/corpus.db`
**Predecessor:** `MIGRATION-vfx-p2-dossier-curation-2026-08-24.md` (main lane — 114 / 26 / 25)
**Delta note:** `../../elrond/notes/2026-08-24-vfx-p2-supplement-curation-delta.md`
**Class:** **ADDITIVE.** Two nullable columns, two views, three run-scoped row sets. **No existing row's value is altered or deleted.**

---

## 1 · Backups + reversibility

| Artifact | md5 | State |
|---|---|---|
| `corpus.db.pre-vfx-p2-supplement-20260824-backup` | `831fdd52ea23fc72616894d9be4a193a` | **TRUE PRE-STATE for this delta** — taken before any DDL ran. |
| `corpus.db.pre-vfx-p2-20260824T130336Z-backup` | `4137a171af74a971a57fa9eef5153a1e` | Pre-state for the **main lane** (predecessor). Still the deeper restore point. |

The backup filename is a **pinned script constant**, not stamped per invocation — a re-run must not
shadow the true pre-state with a post-DDL copy.

`pragma integrity_check` = **ok**. `pragma foreign_key_check` = **0 violations**.

### Reversibility

Three routes, in ascending cost:

1. **Row-level.** `delete from vfx_reference_candidate / vfx_reference_dossier /
   vfx_curation_finding where curation_run = 'vfx-p2-supplement-curation-2026-08-24';` plus
   `drop view v_vfx_reference_candidate_p2; drop view v_vfx_reference_dossier_p2;`. The two added
   columns are nullable and read NULL on every pre-existing row, so leaving them in place is
   harmless — but if a strict revert is wanted, see (2).
2. **Column-level.** `alter table vfx_reference_candidate drop column confounds;` and
   `alter table vfx_curation_finding drop column target_curation_run;` (SQLite ≥ 3.35).
3. **File-level.** Restore `corpus.db.pre-vfx-p2-supplement-20260824-backup`.

**Idempotency.** A re-run deletes and rebuilds only rows carrying
`curation_run = 'vfx-p2-supplement-curation-2026-08-24'`; the `ALTER`s are guarded by a
`pragma table_info` check; the views are `drop`-then-`create`.

**ADR-004.** No engine-side change. No engine store read or written. The four supplement dossiers
were opened **read-only and are byte-unmodified** (git-clean; `dossier_md5` pins the exact input
text this curation read). Star-lord's MIGRATION docs are unaffected. Cross-seam findings in § 6;
none is acted on here.

---

## 2 · What landed

| Table | Δ rows | Total | Scope |
|---|---:|---:|---|
| `vfx_reference_candidate` | **+12** | 126 | 4 supplement dossiers, jobs 27–30. |
| `vfx_reference_dossier` | **+4** | 30 | One row per supplement dossier. |
| `vfx_curation_finding` | **+15** | 40 | 4 WARN / 11 INFO / **0 UNRESOLVED**. |

| View (new) | Purpose |
|---|---|
| `v_vfx_reference_candidate_p2` | Both lanes, one query surface, with a **derived** `lane` column. |
| `v_vfx_reference_dossier_p2` | Same, for dossier rows. |

### 2.1 The lane discriminator is `curation_run` — and no `lane` column exists

The predecessor MIGRATION § 1 already established the convention: *"a later curation lands beside
this one rather than over it."* The supplement lane is therefore
`curation_run = 'vfx-p2-supplement-curation-2026-08-24'`, beside
`'vfx-p2-dossier-curation-2026-08-24'`. This also resolves the PK problem for free —
`(curation_run, archetype_id, candidate_rank)` means the supplement's `whirlwind` ranks 1–2 cannot
collide with the main lane's, and candidate ranks stay **as authored** rather than being offset into
an artificial numbering the dossiers never used.

**A stored `lane` column was considered and rejected.** Backfilling it would have mutated the 114
existing rows; *not* backfilling it would have made NULL mean both "main lane" and "unset" — a
column with two meanings is worse than no column. Lane is **derived** in the two views instead:
storage stays truthful, consumers get one surface, and nothing was rewritten to achieve it.

### 2.2 `vfx_reference_candidate.confounds TEXT` (additive, nullable)

`ww_clean_baseline.md` carries a per-candidate `confounds:` field the main-lane grammar never had.
It exists **because confound-status is the entire question job 29 was fired to answer** (L-30: WW
clean-baseline verification; L-32: "two confound-free alternates found, both archival-grade").

Folding it into `readability_notes` would have been a **silent transformation of exactly the field
the job produced**. A side table would have over-normalized a 1:1 optional text attribute and hidden
confound-status from the row P3 reads when selecting. So: a column, on the row, named for what it is.

**Asymmetry, stated rather than smoothed:** the Matt incumbent (`whirlwind#0`, main lane) also has
confounds, but they live as verbatim prose in its `readability_notes` where the main lane put them.
That row is **not** migrated into the new column — migrating it would mutate a recorded row for
tidiness. The incumbent's confounds remain findable in `readability_notes`; new rows use the column.
Anyone querying confound-status across the whole corpus must read both, and this paragraph is why.

### 2.3 `vfx_curation_finding.target_curation_run TEXT` (additive, nullable)

**NULL** = the finding is about a row in its own `curation_run` (true of all 25 main-lane findings,
which is why NULL is the correct and unambiguous default). **Non-NULL** = the finding is about
**another run's** row.

Required by the job-29 result. Its Part-1 block is a verdict on the **main lane's** `whirlwind#1`,
but "whirlwind#1" now names two different videos in two different lanes. Without this column the
finding would silently point at the wrong row — the failure mode is not an error, it is a *plausible
wrong answer*, which is worse.

### 2.4 Conformance stamping excludes cross-run findings

A candidate's `conformance` is derived from WARN/UNRESOLVED findings **raised against its own run's
rows** (`target_curation_run is null`). Without that filter the downgrade finding — which is about
the *main* lane's `whirlwind#1` — would have wrongly stamped the *supplement's* `whirlwind#1`.

Consequence, stated plainly: **main-lane `whirlwind#1` still reads `conformance = 'CONFORMING'`**,
because it *was* conforming as curated. The downgrade travels beside it as a finding, not through it
as a mutation. Consumers must query findings, not conformance alone — see § 7.

### 2.5 Per-dossier `finding_count` is computed after ALL findings are raised

The predecessor computed it mid-loop. Three of this delta's findings
(`source-game-string-variance`) are necessarily raised after every dossier is parsed, because they
compare against the whole corpus. Counting mid-loop would have under-reported them. **A dossier's
verdict must not be cleaner than its facts.**

---

## 3 · Method as executed

### 3.1 Conventions imported, not copied

`norm_url` · `split_md_field` · `url_wellformed` · `md5` · `HEAD_RE` / `FIELD_RE` / `COVER_RE` /
`URL_RE` / `MD_LINK_RE` · `HARD_REQUIRED` / `REQUIRED_FIELDS` are **imported from the predecessor
module**, not re-typed. The two lanes therefore cannot drift in URL normalization, coverage-grammar
parsing or field-requirement definitions — which matters most for `primary_url_norm`, since
cross-lane duplicate detection (§ 4.3) is only meaningful if both lanes normalize identically.

### 3.2 Only the dossier walker is extended

`ww_clean_baseline.md` departs from the main-lane grammar in two ways: a **non-candidate
`## Part 1:` block**, and an **extra `confounds:` field**. The extended walker treats any `## `
heading that is neither `## Candidate N:` nor `## Search log` as a **separate block**, so its fields
can never bleed into the candidate that follows. (The predecessor's walker would have dropped the
Part-1 fields silently — correct by luck of ordering, not by design.) Any non-candidate block the
curation has no home for is reported as `uncurated-dossier-block` WARN **with its full field map
inlined**, so content is never discarded quietly.

### 3.3 Filename → archetype mapping is explicit

Supplement filenames are **job names** (`gtc_nonpoe_supplement`), not archetype names. The mapping
is a pinned dict carrying job number and brief, so a typo cannot silently curate under the wrong
archetype, and each dossier's brief is recorded beside its verdict.

### 3.4 `meets_min_three` for a verification brief

`whirlwind` records `meets_min_three = 0` — the fact, in the column, unconditionally. The finding is
filed at **INFO** rather than WARN because the charter § 4 floor of ≥3 is a *main-lane hunt*
criterion and job 29's brief was verification-plus-alternates. **The column is the fact; the
severity is routing.** Both are present so a reader can disagree with the severity without losing
the fact.

### 3.5 Verifying the verifier (G-S5)

A **negative control** ran against a temp DB with a corrupted copy of the dossier set: a stripped
hard-required field, a broken coverage grammar, an `ftp:/` primary URL, a duplicated candidate
number, a duplicated field key, an all-`N` coverage line, an injected PoE `source_game`, a bogus
extra field key, a removed search log, a deleted supplement dossier, a removed downgrade target, and
an empty jobs directory.

**All twelve injected defect classes fired their intended detectors** — `missing-required-field`,
`unparseable-coverage`, `malformed-primary-url`, `duplicate-rank`, `duplicate-field`,
`zero-coverage`, `poe-leakage`, `extra-field`, `no-search-log`, `supplement-dossier-missing`,
`downgrade-target-missing`, `unmanifested-dossier`. **§ 4's zero-UNRESOLVED result is therefore a
measurement, not an absence of instrumentation.**

### 3.6 Additivity is proved in-script, not asserted

Before the DDL, the script digests every main-lane candidate's
`(archetype_id, candidate_rank, primary_url_norm, conformance)`; after the write it recomputes and
compares. **Digest unchanged: true.** Main-lane row counts unchanged (114 / 26 / 25). Main-lane
`confounds` all NULL. Printed every run.

---

## 4 · Verification results

### 4.1 Per-dossier

| job | dossier | archetype | cands | log | joins | `meets_min_three` | verdict | findings |
|---:|---|---|---:|---:|:-:|:-:|---|---:|
| 27 | `gtc_nonpoe_supplement.md` | `ground_targeted_circle` | 3 | 5 | ✓ | 1 | CONFORMING-WITH-FINDING | 1 |
| 28 | `st_nonpoe_supplement.md` | `single_target` | 4 | 6 | ✓ | 1 | **CONFORMING** | 0 |
| 29 | `ww_clean_baseline.md` | `whirlwind` | 2 | 5 | ✓ | **0** | CONFORMING-WITH-FINDING | 7 |
| 30 | `ma_video_companion.md` | `melee_arc` | 3 | 7 | ✓ | 1 | CONFORMING-WITH-FINDING | 6 |

### 4.2 Per candidate

12/12 rows: all seven hard-required fields present and non-empty · primary URL structurally
well-formed (scheme, dotted host, no illegal characters, no prose-bleed) · **12/12** coverage flags
matched `windup=Y/N; active=Y/N; impact=Y/N` exactly · every `archetype_id` resolves in
`vfx_archetype` under `vote_run = 'vfx-archetype-vote-2026-08-23'` · **zero PoE `source_game`**
(the parse-level confirmation of L-32's oEmbed-level "ZERO PoE leakage").

### 4.3 Findings (15 — 4 WARN / 11 INFO / 0 UNRESOLVED)

| kind | sev | n | disposition |
|---|---|---:|---|
| `extraction-master-downgrade` | WARN | 1 | § 5 — the load-bearing finding. Targets the main lane. |
| `archival-source` | WARN | 2 | § 5.1 — both whirlwind alternates. |
| `cross-run-primary-reuse` | WARN | 1 | `youtube:lYrecr253lY` = main `dash_attack#4` (`t=251s`) **and** supplement `melee_arc#3` (`t=67s`). Different skills, different seek points, one video. P3 must not anchor both without saying why (L-29(6)). |
| `no-secondary-urls` | INFO | 4 | `melee_arc#1..3` (field absent) · `whirlwind#2` (field present but carries the literal token `(optional)` — preserved verbatim, **not repaired**). |
| `source-game-string-variance` | INFO | 3 | `Diablo 3` vs main-lane `Diablo III`; `Diablo III, 2008 pre-release build` packs build provenance into the game field. **Not normalized** — verbatim policy holds (predecessor § 4.5). Reported for P4 rollups. |
| `same-skill-alternate-media` | INFO | 1 | Supplement `melee_arc#1` = D3 Grim Scythe **video**; main `melee_arc#2` = same skill as **gif**. Job 30's stated purpose; recorded so P3 pairs them deliberately. |
| `short-dossier` | INFO | 1 | `whirlwind`, § 3.4. |
| `nonstandard-dossier-format` | INFO | 1 | `ww_clean_baseline.md`'s Part-1 block, § 3.2. |
| `manifest-not-extended` | INFO | 1 | `jobs/_manifest.tsv` still lists only the 26 main archetypes; the four `27..30-*.prompt.md` files are the supplement lane's manifest of record (all present, verified). |

**Zero UNRESOLVED.** No missing field, unparseable flag, malformed URL, duplicate rank, join
failure, PoE leak, or missing downgrade target.

### 4.4 Post-delta coverage — the two 100%-PoE archetypes (the point of jobs 27/28)

| archetype | pool | non-PoE | **non-PoE full-lifecycle video** | PoE share |
|---|---:|---:|---:|---|
| `ground_targeted_circle` (T1, 115 skills) | 3 → **6** | **3** | **3** | 100% → **50%** |
| `single_target` (T1, 90 skills) | 4 → **8** | **4** | **4** | 100% → **50%** |

**Neither archetype still lacks a full-lifecycle non-PoE video.** New sources: D3 Meteor rune
variants · GD Devastation · Lost Ark Doomsday · D3 Magic Missile · LE Javelin (first-party MP4) ·
GD Panetti's Replicating Missile · UNDECEMBER Fireball. All seven are
`windup=Y; active=Y; impact=Y` video.

**205 skills — ~18% of the voted corpus — are no longer bound to one studio's grammar by sampling
accident.** Corpus-wide PoE share falls **53.5% → 48.4%** (61/126): **C-1 reduced, not retired.**

**Limit of the claim.** This is *parse-level* verification of flags the research lane self-reported.
Whether the footage is what the flags claim is galadriel's P3 delta to judge.

---

## 5 · The material finding — `whirlwind#1` downgraded, not edited

`ww_clean_baseline.md`'s Part 1 is **not a candidate**. It is a verdict on the main lane's
`whirlwind#1` (`youtube:3BnHvNZ_4YM`), curated as finding **`S002` / `extraction-master-downgrade` /
WARN / `target_curation_run = 'vfx-p2-dossier-curation-2026-08-24'` / `candidate_rank = 1` /
`subject = 'youtube:3BnHvNZ_4YM'`**, carrying all three verdict fields **verbatim**:

| field | verdict |
|---|---|
| `whirlwind_timestamp` | **UNKNOWN** — Blizzard's article confirms WW appears in the embedded video; GameSpot's mirror places "Combat Improvements" at 05:22–06:55; **no accessible source gives a frame-exact time within `3BnHvNZ_4YM`**. |
| `max_resolution` | **UNKNOWN** — quality menu / format manifest unavailable; a missing `maxresdefault` thumbnail cannot distinguish 720p from lower encodes. |
| `frame_extraction_adequate` | **Y**, qualified — real gameplay-camera footage (spinning blade, environmental lighting, kicked-up dust), not concept art or title cards; **but** low/unknown resolution limits fine-particle analysis. |

**The main-lane row was not touched.** Its flags (`windup=Y; active=Y; impact=Y`) and its
`conformance = 'CONFORMING'` stand as the dossier lane wrote them. The two honest UNKNOWNs stay
UNKNOWN — curation does not resolve an unknown into a score to make a row look complete, the same
refusal the predecessor made for the incumbent's coverage flags.

**Consequence per L-32 — for P3 to rule, not curation:** the Matt incumbent `whirlwind#0`
(`youtube:KaMPoPywM40`) carries the reference load as **primary** with nameable-discountable
confounds (the same standard as `aura`'s VOD); this quarterly video demotes to **provenance
corroborator**. Recorded as a question, not answered.

### 5.1 Both alternates are ARCHIVAL — carried on the rows, not laundered

| row | source | archival status, verbatim from `confounds` / `readability_notes` |
|---|---|---|
| `whirlwind#1` @supplement | D3, Blizzard March-2012 core-skill clip via **bluetracker.gg archive** | Runes explicitly absent ("unmodified by runes"); Wrath of the Wastes postdates it. **"Wing/backpiece absence could not be independently frame-checked from the text-only archive."** **"The surviving URL is archival, so playback availability should be checked before adopting it as the extraction master."** |
| `whirlwind#2` @supplement | D3 **2008 pre-release build** | Predates the runestone system, so cyclones/wings are structurally absent. **"2008-era image quality is suitable mainly for silhouette, cadence, and radius — not fine particles or material response."** |

Both `WARN / archival-source`, both `CONFORMING-WITH-FINDING`, both `windup=N` — **neither is
full-lifecycle**. L-32's classification (silhouette/cadence donors, not extraction masters) is
reproduced *from the rows* rather than asserted over them.

**The honest post-delta shape of the whirlwind pool:** every confound-free candidate is archival and
windup-less; the only full-lifecycle live first-party candidate is the one just downgraded on
timestamp and resolution; and the field-validated row has unrated coverage by deliberate refusal.
**No clean, full-lifecycle, confound-free, extraction-grade whirlwind reference exists in the
corpus.** Stated as a finding, not smoothed into a pool count.

---

## 6 · Findings routed onward (not acted on here)

| # | Finding | Route |
|---|---|---|
| **D-1** | `whirlwind` composition: incumbent-as-primary + downgraded corroborator + two archival donors; no extraction-grade clean baseline exists. | **P3 delta (galadriel)** — rule it, armed with § 5 + § 5.1. L-32 says judged, not assumed. |
| **D-2** | `youtube:lYrecr253lY` primary for **both** `dash_attack` and `melee_arc` at different seek points. | P3 — test against L-29(6) (one reference cannot anchor two archetypes whose causality classes differ). |
| **D-3** | D3 Grim Scythe exists as gif (main canonical) **and** video (supplement) — same archetype, same skill. | P3 — pair deliberately; job 30's deliverable. |
| **D-4** | `source_game` string variance across lanes (`Diablo 3` / `Diablo III` / build-qualified). Verbatim policy retained. | **P4** — any rollup keyed on `source_game` must group deliberately. Candidate for a `game_key` derived column if P4 needs one; **not** a rewrite of the stored strings. |
| **D-5** | C-1 (PoE concentration) **reduced 53.5% → 48.4%**, not retired. Two T1 archetypes de-monocultured; the other 24 unchanged. | P3 / P4 § 3.2 style-register fit. |

No engine-seam finding arose. § 7's predecessor-script hazard is intra-seam and already fixed.

---

## 7 · Predecessor-script compatibility (fixed, verified, not re-run)

Verifying the predecessor's documented re-runnability surfaced a **live hazard independent of this
delta**: `vfx_p2_dossier_curation_2026_08_24.py` globs `dossiers/*.md`, and that directory now holds
four files whose names are **job names, not archetype names**. A re-run would have written **12 rows
with dangling `archetype_id`s into the main lane**, plus FK violations.

Two behaviour-preserving fixes applied to the predecessor:

1. **Column-explicit `INSERT`s.** Its positional inserts would otherwise fail against the two new
   columns (verified: SQLite errors *"table vfx_reference_candidate has 30 columns but 29 values
   were supplied"* — loud, not silently corrupting, but still a break of a documented property).
2. **A pinned `SUPPLEMENT_LANE_FILES` guard.** The four files are skipped with an INFO finding
   naming each skip — **loudly, never silently**.

**Verified, not assumed.** Restored the true pre-state backup → ran the predecessor → applied both
`ALTER`s → **re-ran the patched predecessor**: **114 candidate rows and 26 dossier rows identical to
the live DB** (modulo `curated_at`), `foreign_key_check = 0`, `confounds` all NULL.

**The predecessor was NOT re-run against the live DB.** The 114 / 26 / 25 recorded rows are exactly
as curated on the main pass. One consequence of the guard, recorded so a future re-run is not
mistaken for a discrepancy: a re-run now emits **29** findings, not 25 — the four extra are the
`supplement-lane-file-skipped` INFO rows, and because finding IDs are assigned in order, the
original 25 would renumber `F005`–`F029`. **Finding IDs are stable within a run, not across
re-runs.**

---

## 8 · Queries for downstream consumers

```sql
-- P3 selection pool for one archetype, BOTH lanes, incumbent first
select lane, candidate_rank, source_game, skill_or_mtx_name, primary_url, coverage_raw,
       media_type, provenance, validation_status, confounds, conformance, readability_notes
  from v_vfx_reference_candidate_p2
 where archetype_id = ?
 order by (provenance = 'matt-incumbent') desc, lane, full_lifecycle desc, candidate_rank;

-- EVERY finding about a given row, from ANY run (conformance alone is NOT sufficient:
-- the whirlwind#1 downgrade lives in the supplement run and points back at the main lane)
select curation_run, finding_id, severity, kind, detail
  from vfx_curation_finding
 where archetype_id = ? and candidate_rank = ?
   and coalesce(target_curation_run, curation_run) = ?   -- the run owning the ROW
 order by case severity when 'UNRESOLVED' then 0 when 'WARN' then 1 else 2 end;

-- non-PoE coverage per archetype across both lanes (jobs 27/28 acceptance measure)
select archetype_id,
       count(*) as pool,
       sum(source_game not like '%Path of Exile%') as non_poe,
       sum(source_game not like '%Path of Exile%' and full_lifecycle = 1
           and lower(media_type) = 'video') as non_poe_full_lifecycle_video
  from v_vfx_reference_candidate_p2 group by 1 order by 3, 1;

-- confound-annotated candidates (new column) — NOTE: the Matt incumbent's confounds are NOT here,
-- they are verbatim prose in its readability_notes (see § 2.2)
select lane, archetype_id, candidate_rank, skill_or_mtx_name, confounds
  from v_vfx_reference_candidate_p2 where confounds is not null;
```

---

*Delta executed by elrond, 2026-08-24, under ledger L-30 / L-32. Dossiers read-only and
byte-unmodified (md5-pinned per row). Main lane provably untouched (§ 3.6). Verdict and its limits
in § 4; the material finding in § 5; the honest residual in § 5.1.*
