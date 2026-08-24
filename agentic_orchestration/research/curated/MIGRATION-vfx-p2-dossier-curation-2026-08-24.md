# MIGRATION — VFX P2 reference-dossier curation, 2026-08-24

**Schema version stamp:** `vfx-p2-dossier-curation-2026-08-24/P2`
**Author:** elrond (data steward), named sub-agent of gandalf (`RUN-CONDUCTOR`)
**Run:** VFX ARCHETYPE-BINDING RUN — charter `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md`, phase **P2 tail**, ledger **L-14 / L-15 / L-18 / L-19 / L-24**
**Script:** `../scripts/vfx_p2_dossier_curation_2026_08_24.py` (transactional, idempotent, additive)
**DB:** `agentic_orchestration/research/curated/corpus.db`
**Predecessor:** `MIGRATION-vfx-archetype-vote-2026-08-23.md` (P1 — the four `vfx_*` vote tables)
**Class:** **ADDITIVE.** Three new tables. **No P0-a/P1 table, column, index, view, trigger or row is altered or deleted.**

---

## 1 · Backups + reversibility

| Artifact | md5 | State |
|---|---|---|
| `corpus.db.pre-vfx-p2-20260824T130336Z-backup` | `4137a171af74a971a57fa9eef5153a1e` | **TRUE PRE-STATE** — taken before any DDL ran. Authoritative restore point. |

The backup filename is **pinned as a script constant**, not stamped per invocation. A re-run must not
shadow the true pre-state with a post-DDL copy — the first backup is the only one worth having.

`pragma integrity_check` = **ok**. `pragma foreign_key_check` = **0 violations**.

**Reversibility.** Two independent routes. (a) Restore the pre-state backup. (b) Additive-only removal:
`drop table vfx_reference_candidate; drop table vfx_reference_dossier; drop table vfx_curation_finding;`
— nothing else in the DB references them. The script is idempotent: a re-run deletes and rebuilds only
rows carrying `curation_run = 'vfx-p2-dossier-curation-2026-08-24'`, so a later curation lands beside
this one rather than over it.

**ADR-004.** No engine-side change. No engine store was read or written. The dossiers were opened
**read-only and are byte-unmodified** — `vfx_reference_dossier.dossier_md5` pins the exact input text
this curation read, so any later edit to a dossier is detectable rather than silent. Star-lord's
MIGRATION docs are unaffected. Cross-seam findings are filed in § 6; none is acted on here.

---

## 2 · What landed

| Table | Rows | Purpose |
|---|---:|---|
| `vfx_reference_candidate` | **114** | 113 parsed dossier candidates + 1 Matt-contributed incumbent. |
| `vfx_reference_dossier` | **26** | One row per dossier: provenance, md5, candidate count, conformance verdict. |
| `vfx_curation_finding` | **25** | Everything that did not verify cleanly, as rows. 6 WARN / 19 INFO / **0 UNRESOLVED**. |

All three are keyed on `curation_run`, and `vfx_reference_candidate` carries `(archetype_id, vote_run)`
as a declared foreign key into `vfx_archetype` — the candidate corpus is bound to the *vote that
produced the archetypes*, not to a floating archetype name. If a future vote re-cuts the archetypes,
this candidate set stays attached to the vote it was researched against, and the divergence is visible.

### 2.1 Schema notes (design rationale)

- **Three columns per URL, not one.** `primary_url_raw` (verbatim, markdown-link form preserved) ·
  `primary_url` (extracted, the join key) · `primary_url_norm` (the dedup key). The raw form is the
  *evidence*; the extracted form is what you *query*; the normalized form is the only honest basis for
  duplicate detection, because `youtu.be/X` and `youtube.com/watch?v=X` are the same video and must
  collide. Collapsing these three into one column would have hidden real cross-dossier reuse (§ 4.1) —
  which is precisely the finding this curation exists to surface.
- **Coverage flags are stored parsed AND raw.** `coverage_windup/active/impact` are 1/0/NULL beside
  `coverage_raw`. NULL means *the flag did not parse*, never *the flag is N*. The curation is fully
  reproducible from `coverage_raw`; the transformation is a projection, never a rewrite.
- **`candidate_rank` is authoring order, not preference.** The DDL comment says so, because a column
  called "rank" in a table feeding a *selection* gate will be misread as a ranking otherwise. **P3
  selects; curation only records the order the researcher wrote them in.** `rank = 0` means
  *contributed out-of-band* — it has no position in any dossier's ordering (see § 3.4).
- **Findings are first-class rows, not prose in a note that gets lost.** `vfx_curation_finding` carries
  a severity, a subject, and mandatory prose stating the finding's own cause. Anything needing a
  downstream decision is `status = 'UNRESOLVED'` rather than folded into a clean verdict.
- **`conformance` is per-candidate AND per-dossier**, derived from the findings actually raised rather
  than asserted. A dossier's verdict cannot be cleaner than its candidates'.
- **Nothing was fixed.** Per the task boundary, a malformed dossier is curated-with-finding, never
  repaired. No dossier required it in the event (§ 4), but the discipline is what makes § 4's result
  a measurement rather than an assurance.

---

## 3 · Method as executed

### 3.1 Grammar verification precedes parsing

Before writing a parser, the dossier grammar was **verified uniform**: across all 26 files, every body
line is a heading, a blank line, or `- <key>: <value>`. **Zero** continuation lines, zero non-conforming
body lines. This is what licenses a line-grammar parse to be lossless — a wrapped field would have been
silently truncated by a naive parser, and the check is cheap enough that assuming it would have been
indefensible.

Field-key census across the corpus: `source_game` 113 · `skill_or_mtx_name` 113 · `primary_url` 113 ·
`media_type` 113 · `temporal_coverage` 113 · `why_it_fits` 113 · `readability_notes` 113 ·
`secondary_urls` **109**. The 8th field is the only one not universal (§ 4.3).

### 3.2 Grain

**CANDIDATE.** One row per `## Candidate N:` block. 113 blocks across 26 dossiers (range 3–6 per
dossier, median 4), plus the incumbent = **114 rows**.

### 3.3 URL normalization (the dedup key)

`primary_url_norm` collapses: scheme · `www.` · trailing slash · host case · and the YouTube identity
family (`watch?v=X`, `youtu.be/X`, `/embed/X`, `/shorts/X` → `youtube:X`). Everything else normalizes to
`host/path?query`. This is deliberately conservative — it collapses *spellings of the same resource*,
never *different resources on the same site*.

### 3.4 The Matt-contributed incumbent (ledger L-18 / L-19)

Curated as one row: `archetype_id='whirlwind'`, `candidate_rank=0`, `provenance='matt-incumbent'`,
`validation_status='VALIDATED-INCUMBENT'`, `dossier_path=NULL`, `source='Matt (live word, 2026-08-23)
— ledger L-18 / L-19; oEmbed-verified by conductor'`, `source_date='2026-08-23'`.

Matt's two confounds are carried **verbatim** into `readability_notes`:
(i) added cyclones/tornadoes are Dust-Devil-era BUILD modifications, not base-skill VFX;
(ii) cosmetic wings occlude VFX readability.

**Its temporal-coverage flags are NULL, and that is a deliberate refusal.** The incumbent was
contributed as a working referent, not phase-rated by the dossier lane. Curation does not invent flags
to make a row look complete — filed as finding `F008` so P3 either rates it or knowingly leaves it
unrated. `validation_status` is a separate column from `provenance` precisely so that "who contributed
this" and "has this been validated in the field" never get conflated.

### 3.5 Verifying the verifier (G-S5)

The real corpus produced **zero UNRESOLVED findings**. That result is only worth reporting if the
detectors can fire, so a **negative-control run** was executed against a temp copy of the pre-state DB
with deliberately corrupted dossiers: a truncated dossier, a stripped required field, a broken
coverage grammar, an `ftp:/example` primary URL, a duplicated candidate number, a duplicated field key,
a manifest/disk mismatch, and a filename that resolves to no archetype.

**All nine injected defects fired their intended detectors** (`short-dossier`,
`missing-required-field`, `unparseable-coverage`, `malformed-primary-url`, `duplicate-rank`,
`duplicate-field`, `manifest-gap`, `unmanifested-dossier`, `archetype-join-fail`), and
`pragma foreign_key_check` returned 4 violations against the dangling archetype — versus 0 on the real
run. **The clean verdict in § 4 is therefore a measurement, not an absence of instrumentation.**

---

## 4 · Verification results

### 4.1 Per-dossier conformance

26/26 dossiers: `archetype_joins = 1` (every filename resolves to a `vfx_archetype` row under
`vote_run = 'vfx-archetype-vote-2026-08-23'`) · `meets_min_three = 1` (charter § 4 P2 floor held —
**zero short dossiers**) · search log present (5–7 entries each).

| verdict | dossiers |
|---|---:|
| `CONFORMING` | 20 |
| `CONFORMING-WITH-FINDING` | 6 (`self_buff`, `melee_arc`, `aura`, `ground_slam`, `chain`, `leap_strike`) |

Every one of the six carries exactly one INFO-severity finding (a missing `secondary_urls` or a `gif`
media type). **No dossier carries a structural defect.**

### 4.2 Schema conformance, per candidate

114/114 rows: all seven hard-required fields present and non-empty · primary URL structurally
well-formed (scheme, dotted host, no illegal characters, no prose-bleed) · **113/113** dossier
candidates' coverage flags matched the chartered grammar `windup=Y/N; active=Y/N; impact=Y/N` exactly.
Zero malformed secondary URLs across 109 secondary-URL fields.

### 4.3 Findings (25 rows — 6 WARN / 19 INFO / 0 UNRESOLVED)

| kind | sev | n | disposition |
|---|---|---:|---|
| `cross-archetype-primary-reuse` | WARN | 6 | **The material finding — see § 5.** |
| `cross-archetype-url-reuse` | INFO | 11 | Same reference as *secondary* under two archetypes. |
| `no-secondary-urls` | INFO | 4 | `aura#2`, `chain#4`, `ground_slam#5`, `self_buff#4` — single-source; corroboration rests wholly on the primary. |
| `non-video-media` | INFO | 2 | `leap_strike#3`, `melee_arc#2` are `gif`. Charter prefers video; **retained** — P3 weighs it, curation does not drop it. |
| `archetype-uncovered` | INFO | 1 | `knockback` has zero candidates — **expected**, F-3 held per L-14. The one archetype of 27 with no reference corpus. |
| `incumbent-coverage-unrated` | INFO | 1 | § 3.4. |

**Zero UNRESOLVED.** No missing field, no unparseable flag, no malformed URL, no duplicate rank, no
join failure, no manifest gap. The manifest's 26 requested archetypes and the 26 dossiers on disk are
the same set.

### 4.4 Coverage statistics (P3 input)

| measure | count | of 113 dossier candidates |
|---|---:|---:|
| windup documented | 91 | 80.5% |
| active documented | 113 | **100.0%** |
| impact documented | 110 | 97.3% |
| **full lifecycle** (all three) | **90** | **79.6%** |

**Windup is the scarce phase** — it is the only flag any candidate lacks in quantity, and it is the
phase a telegraph-literacy design (charter § 3.6) most depends on.

**23 of 26 archetypes carry at least one full-lifecycle *video* candidate.** The three that do not:

| archetype | candidates | full-lifecycle | windup coverage |
|---|---:|---:|---|
| `aura` (T1, 73 skills) | 5 | 0 | 0 of 5 |
| `self_buff` (T1, 112 skills) | 4 | 0 | 1 of 4 |
| `defensive_dash` (T4, 4 skills) | 5 | 0 | 0 of 5 |

This is **not** a lane failure — it is the substrate speaking. `aura` and `self_buff` are exactly the
two archetypes P1 recorded as `motion_signature_attested = NULL` ("none attested — no path
signature"). A persistent, non-projectile, no-path effect has no *windup* to film in the sense the
other archetypes do. The gap is coherent with the vote rather than contradicting it, and P3 should
expect it rather than treat those three as under-researched. `defensive_dash` is separately the T4
singleton-tier archetype (4 skills).

### 4.5 Source-game distribution (114 rows)

| source_game | n |
|---|---:|
| Path of Exile | 61 |
| Grim Dawn | 15 |
| Diablo III | 10 |
| Last Epoch | 9 |
| Diablo II: Resurrected | 6 |
| Diablo IV | 4 |
| Lost Ark | 3 |
| Diablo III: Reaper of Souls | 1 |
| Diablo IV (Season 14) | 1 *(the incumbent)* |
| Hades / Hades II / Path of Exile 2 / Torchlight: Infinite | 1 each |

**PoE is 53.5% of the corpus.** That is the chartered hunt order (§ 4 P2: "PoE MTX shop + official
showcases" first) working as designed — PoE's MTX business model means it is the only ARPG that
publishes first-party per-effect showcase video systematically. But it is a **style-register
concentration risk for P3**: if the canonical reference for most archetypes is PoE, the binding spec
inherits PoE's visual register by sampling accident rather than by decision. Logged as a P3-facing
observation, not a curation defect. Note also that `Diablo III` / `Diablo III: Reaper of Souls` and
`Diablo IV` / `Diablo IV (Season 14)` are **not** normalized — the strings are preserved verbatim as
authored, since the expansion/season distinction is real provenance, not noise.

---

## 5 · The material finding — independent cross-archetype reference convergence

Six candidate pairs share a **primary** reference across two archetypes. Because the Codex lane ran
**26 serialized jobs with zero cross-job context** (each job saw only its own archetype's
`researcher_gloss`), independent convergence on the same source material is a real signal rather than
a copy-paste artifact.

| archetype pair | shared **primary** refs | shared refs incl. secondary | total distinct shared sources |
|---|---:|---:|---:|
| **`blink` ↔ `teleport`** | **2** | 2 | **4** |
| **`circle` ↔ `ring`** | 1 | 2 | **3** |
| `cone` ↔ `ground_slam` | 1 | 1 | 2 |
| `aura` ↔ `circle` | 1 | 1 | 2 |
| `line` ↔ `vortex_pull` | 1 | 0 | 1 |
| `line` ↔ `single_target` | 0 | 2 | 2 |
| `ground_targeted_circle` ↔ `line` | 0 | 1 | 1 |
| `fork` ↔ `teleport` | 0 | 1 | 1 |
| `ricochet_bounce` ↔ `whirlwind` | 0 | 1 | 1 |

**`circle` ↔ `ring` is the pair P1 pre-registered.** Ledger L-10 banked falsifier **F-a** as
PENDING-P3 with "`circle`/`ring` likeliest". An independent research lane reaching for the same
material for both is **a datum for F-a**, arriving from a direction the vote did not construct.

**`blink` ↔ `teleport` was NOT pre-registered, and it is the stronger signal** — twice the primary
overlap and four distinct shared sources (incl. Shadow Strike and the Lightning Warp effect). Filed as
a candidate **F-e** for P3's falsifier register.

**Stated with its uncertainty, because this is a hypothesis and not a truth.** Shared reference ≠
archetypes must merge. Skills like Shadow Strike and Lightning Warp arguably *instantiate both*
mechanics, so the convergence may say "these two skills are boundary cases" rather than "these two
archetypes are one." **What would falsify it:** if P3's judged selection lands *different* canonical
references for `blink` and `teleport` on readability/parameterizability grounds without strain, the
convergence was researcher sampling, not archetype identity. If P3 finds itself unable to distinguish
them without inventing a criterion, F-a/F-e fire. **Curation does not decide this — it records that
the question is now empirical.**

### 5.1 L-19's companion-clip question, answered

L-19 asked whether the `whirlwind` dossier carries a clean-baseline WW companion clip to compose with
the incumbent. **It does.** `whirlwind#1` is Diablo IV Whirlwind via the official Blizzard VFX
material, `windup=Y; active=Y; impact=Y`, with readability notes recording restrained dust and blade
highlights preserving the rotating silhouette. It carries **neither** of Matt's two confounds — no
Dust-Devil build modification, no cosmetic wing occlusion — while remaining the same game and the same
base skill as the incumbent. **Incumbent (owner-validated, confounded) + `whirlwind#1` (clean baseline,
full lifecycle) compose exactly as L-19 anticipated.**

---

## 6 · Findings routed onward (not acted on here)

| # | Finding | Route |
|---|---|---|
| **C-1** | PoE = 53.5% of the reference corpus — style-register concentration risk for the binding spec. | P3 / gandalf at P4. Charter § 3.2 "style-register fit" scoring. |
| **C-2** | Windup is the scarce phase (80.5% vs 100% active); 3 archetypes have zero full-lifecycle video, all three coherently explained by NULL motion signature. | P3 selection gate — expect it, do not treat as under-research. |
| **C-3** | `blink` ↔ `teleport` convergence — candidate falsifier **F-e**, not pre-registered at P1. | P3 falsifier register, beside F-a. |
| **C-4** | The incumbent carries unrated temporal coverage by deliberate refusal. | P3 rates or knowingly declines. |
| **C-5** | `knockback` remains the one archetype of 27 with zero reference corpus (F-3 held). | Standing — resolves with F-3's disposition, not here. |

No engine-seam finding arose from this curation. P1's L-12 items (`orbit` absent from
`_RICH_TO_SPATIAL`; stale `data/kit_space`) are unchanged and remain routed as filed.

---

## 7 · Queries for downstream consumers

```sql
-- P3 selection pool for one archetype, incumbent first, full-lifecycle candidates next
select candidate_rank, source_game, skill_or_mtx_name, primary_url, coverage_raw,
       provenance, validation_status, why_it_fits, readability_notes
  from vfx_reference_candidate
 where curation_run = 'vfx-p2-dossier-curation-2026-08-24' and archetype_id = ?
 order by (provenance = 'matt-incumbent') desc, full_lifecycle desc, candidate_rank;

-- archetypes lacking a full-lifecycle video reference (P3 expectation-setting)
select a.archetype_id, a.support_tier, a.member_skills
  from vfx_archetype a
 where a.vote_run = 'vfx-archetype-vote-2026-08-23'
   and not exists (select 1 from vfx_reference_candidate c
                    where c.archetype_id = a.archetype_id
                      and c.curation_run = 'vfx-p2-dossier-curation-2026-08-24'
                      and c.full_lifecycle = 1 and lower(c.media_type) = 'video');

-- everything that did not verify cleanly
select severity, kind, archetype_id, candidate_rank, detail
  from vfx_curation_finding
 where curation_run = 'vfx-p2-dossier-curation-2026-08-24'
 order by case severity when 'UNRESOLVED' then 0 when 'WARN' then 1 else 2 end, kind;
```

---

*Curation executed by elrond, 2026-08-24, under charter § 4 P2 tail and ledger L-24. Dossiers read-only
and byte-unmodified (md5-pinned per row). Verdict and its limits in § 4; the material finding in § 5.*
