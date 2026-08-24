# VFX P2 — SUPPLEMENT curation DELTA (elrond, 2026-08-24)

**Run:** VFX ARCHETYPE-BINDING RUN · charter `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md` · ledger **L-30 / L-32**
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executed by:** elrond (data steward), named sub-agent
**Predecessor:** `2026-08-24-vfx-p2-dossier-curation.md` (main lane — 26 dossiers → 114 candidates)
**Migration record:** `../../research/curated/MIGRATION-vfx-p2-supplement-curation-delta-2026-08-24.md`
**Script:** `../../research/scripts/vfx_p2_supplement_curation_delta_2026_08_24.py`
**DB:** `../../research/curated/corpus.db` · schema stamp `vfx-p2-supplement-curation-2026-08-24/P2-delta`

---

## 1 · Verdict

**PASS, ADDITIVE.** 4/4 supplement dossiers curated. **+12 candidate rows, +4 dossier rows,
+15 finding rows** — 4 WARN / 11 INFO / **0 UNRESOLVED**.

The main lane is **provably untouched**: 114 / 26 / 25 rows before and after, and a digest over
every main-lane candidate's `(archetype_id, rank, primary_url_norm, conformance)` is **identical
across the delta**. `integrity_check = ok`, `foreign_key_check = 0`. The four dossiers are
**byte-unmodified** (git-clean; `dossier_md5` pinned per row).

Instrumentation was confirmed live before the verdict was reported (G-S5): a **negative control**
against a temp DB with **twelve** injected defect classes fired all twelve detectors —
`missing-required-field`, `unparseable-coverage`, `malformed-primary-url`, `duplicate-rank`,
`duplicate-field`, `zero-coverage`, `poe-leakage`, `extra-field`, `no-search-log`,
`supplement-dossier-missing`, `downgrade-target-missing`, `unmanifested-dossier`.

---

## 2 · Per-dossier conformance

| job | dossier | archetype | cands | log | joins | `meets_min_three` | verdict | findings |
|---:|---|---|---:|---:|:-:|:-:|---|---:|
| 27 | `gtc_nonpoe_supplement.md` | `ground_targeted_circle` | 3 | 5 | ✓ | ✓ | CONFORMING-WITH-FINDING | 1 |
| 28 | `st_nonpoe_supplement.md` | `single_target` | 4 | 6 | ✓ | ✓ | **CONFORMING** | 0 |
| 29 | `ww_clean_baseline.md` | `whirlwind` | 2 | 5 | ✓ | **0** | CONFORMING-WITH-FINDING | 7 |
| 30 | `ma_video_companion.md` | `melee_arc` | 3 | 7 | ✓ | ✓ | CONFORMING-WITH-FINDING | 6 |

Every hard-required field present on all 12 candidates · all 12 primary URLs structurally
well-formed · **12/12 coverage flags parsed** against the chartered grammar · every filename
mapped to a `vfx_archetype` row · **zero PoE leakage** (the parse-level confirmation of L-32's
oEmbed-level finding).

`whirlwind` records `meets_min_three = 0` as a **fact in the column**. It is filed at **INFO**, not
WARN: the charter § 4 floor of ≥3 is a *main-lane hunt* criterion, and job 29's brief was
verification-plus-alternates. The count is still reported so P3 cannot mistake this for a full hunt.
*The column is the fact; the severity is routing.*

---

## 3 · The `whirlwind#1` downgrade (L-32, the load-bearing finding)

`ww_clean_baseline.md`'s **Part 1 is not a candidate.** It is a verdict *on* the main lane's
`whirlwind#1` (`youtube:3BnHvNZ_4YM`), and it **downgrades that row's usability**. Curated as
finding **`S002` / `extraction-master-downgrade` / WARN**, carrying the three verdict fields
**verbatim**:

| field | verdict |
|---|---|
| `whirlwind_timestamp` | **UNKNOWN** — Blizzard's article confirms WW is in the video; GameSpot's mirror places "Combat Improvements" at 05:22–06:55; **no source gives a frame-exact time inside `3BnHvNZ_4YM`**. |
| `max_resolution` | **UNKNOWN** — quality menu / format manifest unavailable; a missing `maxresdefault` thumbnail cannot distinguish 720p from lower. |
| `frame_extraction_adequate` | **Y**, qualified — real gameplay-camera footage, not concept art or title cards, **but** low/unknown resolution limits fine-particle analysis. |

**The main-lane row was NOT edited.** Its flags (`windup=Y; active=Y; impact=Y`) stand exactly as
the dossier lane wrote them, and its `conformance` still reads `CONFORMING` — because it *was*
conforming as curated. The downgrade travels **beside** the row as a finding, not through it as a
mutation. Two honest UNKNOWNs stay UNKNOWN; curation does not resolve them into a score.

To make the target unambiguous, `vfx_curation_finding` gained **`target_curation_run`** (§ 5): this
finding lives in the supplement run but points at the *main* run's `whirlwind#1`. Without it,
`whirlwind#1` now names two different videos in two different lanes.

**Consequence (L-32, for P3 to rule — not curation):** the Matt incumbent `whirlwind#0`
(`youtube:KaMPoPywM40`) carries the reference load as **primary** with nameable-discountable
confounds; the quarterly video demotes to **provenance corroborator**. Curation records the
downgrade and the composition question. It does not answer it.

### 3.1 Both whirlwind alternates are ARCHIVAL — carried, not laundered

| row | source | archival status (`confounds` + `readability_notes`, verbatim on the row) |
|---|---|---|
| `whirlwind#1` @supplement | D3, Blizzard March-2012 core-skill clip via **bluetracker.gg archive** | runes explicitly absent; **wing/backpiece absence could not be frame-checked from a text-only archive**; *"the surviving URL is archival, so playback availability should be checked before adopting it as the extraction master."* **Playback availability is UNVERIFIED.** |
| `whirlwind#2` @supplement | D3 **2008 pre-release build** | predates the runestone system, so cyclones/wings are structurally absent; *"2008-era image quality is suitable mainly for silhouette, cadence, and radius — not fine particles or material response."* |

Both are `WARN / archival-source` and stamped `CONFORMING-WITH-FINDING`. Both carry
`windup=N` — **neither is full-lifecycle.** L-32's classification (silhouette/cadence donors, *not*
extraction masters) is reproduced from the rows themselves rather than asserted over them.

**The honest shape of the whirlwind pool after this delta:** every confound-free candidate is
archival and windup-less; the only full-lifecycle, live, first-party candidate
(`whirlwind#1` @main) is the one just downgraded on timestamp and resolution; and the row Matt
validated in the field (`whirlwind#0`) has unrated coverage by deliberate refusal. **There is no
clean, full-lifecycle, confound-free, extraction-grade whirlwind reference in the corpus.** That is
a finding, not a gap to paper over.

---

## 4 · Post-delta coverage — the two 100%-PoE archetypes

Both hunts succeeded. **Neither archetype lacks a full-lifecycle non-PoE video any longer.**

| archetype | pool | non-PoE | **non-PoE full-lifecycle video** | PoE share: before → after |
|---|---:|---:|---:|---|
| `ground_targeted_circle` (T1, 115 skills) | 3 → **6** | **3** | **3 / 3** | 100% → **50%** |
| `single_target` (T1, 90 skills) | 4 → **8** | **4** | **4 / 4** | 100% → **50%** |

`ground_targeted_circle` gains **D3 Meteor rune variants**, **GD Devastation**, **Lost Ark
Doomsday**. `single_target` gains **D3 Magic Missile**, **LE Javelin** (first-party MP4),
**GD Panetti's Replicating Missile**, **UNDECEMBER Fireball** — a source game the original hunt
order never listed. All 7 rows are `windup=Y; active=Y; impact=Y` video.

**205 skills — ~18% of the voted corpus — are no longer bound to one studio's grammar by sampling
accident.** Corpus-wide PoE share falls **53.5% → 48.4%** (61/126). C-1 is *reduced*, not retired.

**Stated with its limit:** these are *parse-level* verifications of coverage flags the research lane
self-reported. Curation confirms the flags parse, the URLs are well-formed, the archetypes join, and
no PoE row leaked. Whether the footage *is* what the flags claim is galadriel's P3 delta to judge.

---

## 5 · Schema delta (two additive nullable columns; full rationale in MIGRATION § 2)

| change | why |
|---|---|
| `vfx_reference_candidate.confounds TEXT` | Job 29's whole purpose is confound-status. Folding it into `readability_notes` would be a silent transformation of the exact field the job was run to produce. |
| `vfx_curation_finding.target_curation_run TEXT` | NULL = the finding is about its own run. Non-NULL = it is about **another** run's row. Required by § 3: `(archetype_id, rank)` is no longer unique across lanes. |

**No `lane` column was added.** Backfilling one would have mutated the 114 existing rows; leaving it
NULL would make NULL mean both "main lane" and "unset". Lane is **derived** in two new views,
`v_vfx_reference_candidate_p2` and `v_vfx_reference_dossier_p2` — one query surface across both
lanes, zero stored redundancy, zero mutation.

**Lane discriminator = `curation_run`**, exactly as the predecessor MIGRATION § 1 anticipated
("a later curation lands beside this one rather than over it").

---

## 6 · Findings (15 — 4 WARN / 11 INFO / 0 UNRESOLVED)

| kind | sev | n | note |
|---|---|---:|---|
| `extraction-master-downgrade` | WARN | 1 | **§ 3** — targets the main lane. |
| `archival-source` | WARN | 2 | **§ 3.1** — both whirlwind alternates. |
| `cross-run-primary-reuse` | WARN | 1 | **§ 6.1**. |
| `no-secondary-urls` | INFO | 4 | `melee_arc#1..3` (field absent) + `whirlwind#2` (§ 6.2). |
| `source-game-string-variance` | INFO | 3 | **§ 6.3**. |
| `same-skill-alternate-media` | INFO | 1 | **§ 6.1** — job 30 doing its job. |
| `short-dossier` | INFO | 1 | `whirlwind`, § 2. |
| `nonstandard-dossier-format` | INFO | 1 | `ww_clean_baseline.md`'s Part-1 block. |
| `manifest-not-extended` | INFO | 1 | § 6.4. |

### 6.1 One video, two archetypes — and one gif, one video

**`cross-run-primary-reuse` (WARN).** `youtube:lYrecr253lY` — the Lost Ark Berserker showcase — is
the main lane's **`dash_attack#4` primary** (Shoulder Charge, `t=251s`) *and* the supplement's
**`melee_arc#3` primary** (Tempest Slash, `t=67s`). Different skills, different seek points, one
video. Not a defect — a multi-skill showcase legitimately demonstrates two archetypes — but **P3
must not anchor both archetypes on it without saying why**, per L-29(6): one reference cannot anchor
two archetypes whose causality classes differ. The seek points are reported on the finding rather
than assumed, because they are what makes the double use defensible or not.

**`same-skill-alternate-media` (INFO).** Supplement `melee_arc#1` is **D3 Grim Scythe on video**;
main-lane `melee_arc#2` is **the same skill as a gif** (`news.blizzard.com`). This is job 30's
stated purpose — a video companion for a gif canonical on a 76-skill archetype — recorded so P3
**pairs** them deliberately instead of counting them as two independent references.

### 6.2 A template token left in a field

`whirlwind#2`'s `secondary_urls` reads the literal `(optional)`. Zero URLs extract. Curated as
single-source; **the raw token is preserved verbatim in `secondary_urls_raw` and is not repaired.**
A malformed dossier is curated-with-finding, never fixed — that discipline is what makes § 1 a
measurement rather than an assurance.

### 6.3 The corpus now spells the same game two ways

`Diablo 3` (supplement) and `Diablo III` (main) are one game; `Diablo III, 2008 pre-release build`
packs build provenance into the game field. **Not normalized** — game strings are preserved verbatim
in both lanes because expansion / season / build qualifiers are real provenance (predecessor
MIGRATION § 4.5). Reported so any P4 rollup keyed on `source_game` groups them **deliberately**.

### 6.4 `jobs/_manifest.tsv` still lists only 26

Jobs 27–30 were briefed via prompt files (`27..30-*.prompt.md`, all present and verified). The
prompt files are the supplement lane's manifest of record. Stated so a later reader does not read
the TSV as the complete job list.

---

## 7 · A landmine found and defused in the predecessor script

Verifying the predecessor's documented re-runnability surfaced a **live hazard unrelated to this
delta**: `vfx_p2_dossier_curation_2026_08_24.py` globs `dossiers/*.md`, and the directory now holds
four files whose names are **job names, not archetype names**. A re-run would have written **12 rows
with dangling `archetype_id`s into the main lane** and produced FK violations.

Two behaviour-preserving fixes applied to the predecessor (**it was not re-run against the live
DB**; the recorded rows are untouched):

1. Column-explicit `INSERT`s — a positional insert would break against the two new columns.
2. A pinned `SUPPLEMENT_LANE_FILES` guard — the four files are skipped **loudly** (an INFO finding
   names each skip), never silently.

**Verified**, not assumed: restored from the true pre-state backup, applied both `ALTER`s, re-ran
the patched predecessor → **114 candidate rows and 26 dossier rows identical to the live DB**
(modulo `curated_at`), 0 FK violations, `confounds` all NULL.

---

## 8 · Boundaries honoured

Additive only — two nullable columns, two views, three run-scoped row sets. No main-lane row's value
altered, proved by digest. Dossiers read-only and byte-unmodified. No engine store read or written;
ADR-004 unaffected. Nothing repaired. Conventions **imported** from the predecessor module, not
copied, so the two lanes cannot drift.

**Routed onward (D-1..D-5, MIGRATION § 6):** the whirlwind composition question (P3 delta rules it,
armed with § 3 + § 3.1) · the `dash_attack`/`melee_arc` shared video (P3, against L-29(6)) · the
gif↔video Grim Scythe pairing (P3) · `source_game` string variance (P4 rollups) · C-1 reduced but
not retired at 48.4% PoE (P3/P4).
