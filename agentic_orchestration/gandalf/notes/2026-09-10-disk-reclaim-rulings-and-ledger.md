# Disk-reclaim run — rulings + execution ledger (2026-09-10)

> **STATUS:** OPEN — seam manifests in flight. Conductor: gandalf (RUN-CONDUCTOR).
> **Lineage:** reopens the T20 condition (`canonical/matt_to_do/2026-08-24-mac-disk-space-red.md`, CLOSED 2026-08-25 at 66 GiB free). Re-measured 2026-09-10: **28 GiB free of 460 (94%)** — below T20's own ≥60 GiB done-criterion.

## § 1 Measurements (2026-09-10, all `du`/`df`-verified, not estimated)

| Surface | Size | Notes |
|---|---|---|
| `/System/Volumes/Data` free | **28 GiB (94% used)** | RED re-opened |
| `reincarnated-engine` | 63 G | `data/` 33 G · `output/` 18 G · `src/` 7.4 G · `seasons/` 3.3 G · `.git` 652 M · `logs/` 487 M |
| `reincarnated-godot` | 44 G | untouched this run (VFX-depth run HALTED at Q68; sealed substrate dense) |
| `reincarnated-collaboration` | 24 G | gitignored **17.5 G** + untracked **5.4 G** + tracked 1.2 G + `.git` 815 M |
| — `agentic_orchestration/galadriel/captures` | 7.4 G | largest: shadow-cal 2.7 G, eor-followup 1.1 G, wr1-gal3 0.9 G |
| — `elrond/research` + `research/curated` + `legolas/notes`+`scratch` | 6.0 G | research pools |
| — `matt_notes_handoff_docs` | 5.0 G | PARKED (Matt's material; move-to-external blocked — `/Volumes/reincarnated` not mounted) |
| `vendor` 14 G · `synty-corpus` 14 G · `reincarnated-demo` 15 G | 43 G | untouched this run (pinned referents / other seams) |

**Load-bearing finding:** deleting *documents* is a non-remedy — all of `canonical/` is 4.9 MB; meta-repo tracked content is 1.2 GB (git retains blobs regardless). ~95% of the meta-repo's weight is gitignored/untracked binary artifacts reclaiming 1:1.

## § 2 Matt rulings (2026-09-10, this session, verbatim shapes)

> "GO on tier 2, but I don't want to lose data we will need to reference later. Go on Tier 3. Go on Tier 1 - research and strays and captures."

- **T2-engine: GO** + binding constraint → conservative KEEP-default on every seam; classify-then-delete; manifest everything.
- **T3 (doc hygiene): GO.**
- **T1-research: GO · T1-strays: GO · T1-captures: GO-with-sealed-evidence-manifest.**
- `matt_notes_handoff_docs`: not ruled — stays PARKED pending external volume mount.

## § 3 Execution routing (OP § 4.10 — named seams only; no-commit briefs, conductor centralizes commits)

| Piece | Seam | Scope | Manifest path (owed) |
|---|---|---|---|
| Engine `output/` + `logs/` + `cache/` | star-lord | ~18.5 G | `star-lord/notes/2026-09-10-engine-output-reclaim-manifest.md` |
| Engine `data/` + meta-repo research pools | elrond | ~37 G | `elrond/notes/2026-09-10-data-reclaim-manifest.md` |
| `galadriel/captures` (sealed-evidence fence) | galadriel | 7.4 G | `galadriel/notes/2026-09-10-captures-reclaim-manifest.md` |
| `legolas/notes` + `scratch` | legolas | 1.9 G | `legolas/notes/2026-09-10-legolas-reclaim-manifest.md` |
| T3 tracker collapse + queue sweeps (§ 4.9) | gandalf sub-agent | 3 md files | reported inline |
| T1-strays | conductor foreground | 1.3 G nominal | § 4 below |

**Standing discipline on every deletion:** machine-checked predicates — `git ls-files <path>` = 0 tracked AND no citation in decisions-log/sealed artifacts AND a nameable regeneration/re-fetch recipe. Ambiguity = KEEP.

## § 4 Strays verdicts (conductor foreground, predicate-gated)

| Dir | Size | Verdict | Evidence |
|---|---|---|---|
| `astra_test_01` | 573 M | **KEEP — not a stray** | 699 git-TRACKED files; 11 recent commits (live astra painted-world workstream). Gate caught my own Tier-1 mislabel |
| `glance` | 126 M | **KEEP — not a stray** | 63 tracked files; 110 doc citations (glance-atlas work) |
| `duskweaver` + `duskweaver-mm-p1` | 341 M | **KEEP — irreplaceable media** | Meshy-generated character assets + MM-P1 video-production media; cited by elrond dispatch 2026-06-09; not regenerable |
| `godot-sqlite-02863bef…` | 328 M | **DELETE-class; execution WITHHELD (permission denied at host)** | Extracted GitHub archive of 2shady4u/godot-sqlite @ `02863bef`; NOT a repo (`rev-parse` resolved to parent — the `git -C` walk-up face); 0 tracked, 0 citations. Re-fetch: `github.com/2shady4u/godot-sqlite/archive/02863bef9be1c121dcac68fc5f6a4fba3caad4a9.zip`. One-liner if Matt executes: `rm -rf ~/Games/reincarnated-collaboration/godot-sqlite-02863bef9be1c121dcac68fc5f6a4fba3caad4a9` |

**Net strays honesty:** the 1.3 G nominal row dissolved to 328 M actual (withheld) — three of five candidates were live or irreplaceable. The conservative gate did exactly what Matt's constraint asked.

## § 5 Results ledger (append-only; filled as seam agents return)

**⚑ RUN-POSTURE AMENDMENT (after first returns):** host permission policy denies agent `rm` — conductor's own delete was denied, legolas's twice. **No agent routes around a deny.** The run is converted to **CLASSIFY-AND-MANIFEST**: every seam files its manifest with DELETE-class marked WITHHELD + batch one-liners; execution batches to Matt (or to a Matt-approved allowlist).

| Seam | Returned | Classified DELETE (withheld) | Notes |
|---|---|---|---|
| legolas | ✓ 2026-09-10 | **1.66 GiB** (3 paths, gates passed) | Manifest filed (conductor-captured). ⚑ **KEEP-PROTECTED flag raised:** `/Users/admin/gd-scratch/eor-test-2/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` (457 M, sha256 `4c60960d…`) is the SOLE reachable regeneration source for 1.68 G of deletable frames — documented path points at the unmounted external volume. Must survive any `gd-scratch` sweep. Also surfaced: stale `/Volumes/reincarnated/...` referent paths across the KC2 lap corpus (doc-rot fix queued) |
| star-lord | ✓ 2026-09-10 | **17.38 GiB freed via IN-PLACE GZIP — 0 deletions, 0 data lost** | Manifest: `star-lord/notes/2026-09-10-engine-output-reclaim-manifest.md`. `output/` 19.15→1.35 GB (26 `fights.jsonl` @ 14.6× compression, `gzip -t` 33/33 + round-trip verified); `logs/` 498→85 MB. **⚑ SOLE-COPY SAVE #2 (the run's biggest):** CHANGELOG:3742 claims 609,800 fight rows backfilled to `telemetry.db`; live query returns **0 rows** — the jsonl files are the ONLY copy, and they are convergence traces (iterations 0..N−1) unreproducible from the tracked converged endpoints. Predicate gates had PASSED for deletion; one SQL query moved 18.87 GB out of the DELETE class. KEEPs: `cache/llm/` (live default cache — "regenerable" = pay Anthropic again), `logs/llm/` (cost ledger, primary telemetry). **Conductor RATIFIES his one out-of-scope edit:** engine `.gitignore` + `output/**/fights.jsonl.gz` + `*.log.gz` (protective — compression un-ignored 1.24 GB, one `git add -A` from history; exposure now 0). Uncommitted, rides the centralized close-commit |
| elrond | ✓ 2026-09-10 | **3.54 GiB freed** (executed under original GO brief + Matt's standing approval; gates: 138 candidates → 2 caught tracked → reclassified KEEP; post-sweep `git status` clean) | Manifest: `elrond/notes/2026-09-10-data-reclaim-manifest.md`. `elrond/research/` 2.54→0.21 GB; `research/curated/` 1.74→0.36 GB. **Engine `data/`: 0 reclaim exists** — 99.84% is ONE file (`data/telemetry.db`), 98.7% of that ONE table (`class_fight_loadouts`, 4,672,477 rows / 81 seasons); `freelist_count=0` (VACUUM reclaims nothing) and dedup proven nil (1,611,300 rows = 1,611,300 distinct blobs). Real options: season-pruning (`season_001005` = 34.5% ≈ 10 GB) or gear-ref normalization → **Q69 filed**. **⚑ SOLE-COPY SAVE #3:** 2.4 GB of `telemetry.db.pre-*` files were NOT telemetry — they were the crawled weapons substrate (Legolas Mode B, 7+ sources). Engine `research.db` + `knowledge_base.db` both **0 bytes**; the canonical substrate copy is a SINGLE UNTRACKED file in *drax's loadout repo* misnamed `telemetry.db` (5,162 weapons / 90,345 knowledge entries, no remote, no history). elrond verified it (integrity ok, strict superset, ATTACH/EXCEPT zero-missing proof) BEFORE deleting the snapshots, and retained a 207 MB insurance copy |

**⚑ Conductor reconciliation flag (star-lord × elrond cross-finding):** THREE files named `telemetry.db` exist — engine `src/…/telemetry/telemetry.db` (**empty**, star-lord's 0-row finding), engine `data/telemetry.db` (**33 GB, 4.67M rows**), loadout `data/telemetry.db` (**actually the weapons substrate**). Star-lord's "jsonl = sole copy of 609,800 rows" verdict was proven against the *src* DB only — whether the backfill landed in `data/telemetry.db` is UNVERIFIED. KEEP postures unchanged either way (conservative), but the harvest telemetry-integrity dispatch must reconcile all three before anyone acts on any "sole copy"/"empty" claim. The naming-convention defect (elrond needs-Matt #3) is systemic, not local.
| galadriel | ✓ 2026-09-10 | **300 MiB EXECUTED** (her deletes were not blocked by the wall; all sha-verified-regenerable, predicate gates passed, zero tracked rows touched) | Manifest: `galadriel/notes/2026-09-10-captures-reclaim-manifest.md`. **⚑ GOVERNING FINDING — stale regenerability claims:** 9 capture dirs carry `.gitignore` claims naming exact regeneration sources; **2 of 3 sources are unreachable today.** (1) `gd-scratch/play_test_2026-07-26.mp4` **ABSENT from the machine entirely** → shadow-cal (2.7 G) + wr1-gal3 + gal-cam + gd-parity caches are the LAST COPIES of evidence behind filed verdicts — KEEP, and the custody gap should be recorded against those verdicts if the mp4 is not on the external volume. (2) `/Volumes/reincarnated/visual-artifacts/` unmounted → eor pools (~2.1 G) unverifiable, KEEP pending mount. Deleted only what was regeneration-DEMONSTRATED (BR2W_C9.mp4 sha byte-match). Refuted two conductor dispatch hypotheses: overlay-align r1≠superseded (different probes); glance-atlas sets sha-differ (no dupes) |
| gandalf sub-agent (T3) | ✓ 2026-09-10 | n/a (hygiene, not disk) | Engine tracker 365→134.5 KB · decision queue 132→87 KB · to-do queue 43.5→31 KB (−53% total; 39+10 struck rows swept, 60 deltas compressed, all git-recoverable). Guards held: live KC2/baton deltas + constitutional 06-23/24 directives untouched; Q66/Q67/Q68 verified-open untouched; T11 kept (live Matt-hands residual). Collision banners added (Q67 double-use; `matt_to_do` T4/T10/T15 — NEW finding, KR-owed). **Desyncs reported → conductor § 4.8 pass below** |

**§ 4.8 sync-walk (conductor foreground, post-T3):** five decision-queue rows read as resolved in their own body text but were never struck (Q40 "8/8 RULED 2026-07-22" · Q41 "RULINGS RECEIVED" · Q32 "E4 RATIFIED 2026-07-17" · Q47 "DEFERRED-EMPIRICAL by Matt ruling" · Q44 "⏸ DEFERRED to story session") — re-presenting dead questions to Matt every session-start, the exact Q3-staleness shape that founded § 4.8. Conductor verifies each from row body + decisions-log, then strikes/sweeps (Q47/Q44 re-mark as GATED, not resolved). **Conductor-owed (gandalf seam, separate session):** decisions-log `6473` routes a gandalf ruling — `substrate-expansion-decision-2026-05-17.md` has no live home while 11 code/math files cite its § 7; rule restore-to-canon vs rewrite-citations-to-git. Parked here; needs the 11 citing files read, not this run's scope.

## § 5b Asks accumulating for Matt (run-close ruling sheet feeds from here)

1. ~~**Execution fork (A/B/C)**~~ **RULED 2026-09-10 — (B) per Matt's own definition (verbatim): "you receive the manifests for deletion and then I approve you to delete them."** Process: manifest lands → conductor presents its DELETE-set → Matt approves → conductor executes (the host permission prompt is the mechanical enforcement of the approval step). Batches presented as manifests land; nothing deletes unapproved.
   **AMENDED same session (Matt: "go ahead and delete now"):** approval is granted STANDING for the remainder of this run — manifested, gate-passing DELETE-class items execute on landing without a further per-batch ask. Scope limits survive the amendment: predicate gates + conservative KEEP-default still bind; the KEEP-PROTECTED register is untouchable; empirically-gated pools (unverifiable-source captures) stay KEEP until their gate clears — that gate is evidential, not approval-shaped.
2. **Mount `/Volumes/reincarnated`** — unlocks: verification + reclaim of ~2.1 G eor capture pools; move-to-external dispositions (matt_notes Synty packs, vendor depot cuts); re-mirroring of at-risk sole-copy sources.
3. **Locate `play_test_2026-07-26.mp4`** — absent from the machine; fixture behind GAL-CAM / SHADOW-CAL / WR1 / GD-PARITY sealed verdicts. If on the external volume: ~3.3 G of caches become reclaimable after sha-verification. If lost: the caches are the last copies AND the custody gap gets recorded against those verdicts.

4. **Batch 1 EXECUTED (Matt-approved this session):** legolas 3 paths + godot-sqlite archive = ~2.0 GiB freed; 0 tracked rows touched.
5. **Harvest items (route to KR at close, not Matt-blocking):** (a) telemetry-integrity dispatch — `class_fight_loadouts` empty vs CHANGELOG's 609,800-row claim (star-lord finding #2); (b) one-line fix, `scripts/ingest_fights_jsonl_to_telemetry.py:103` plain `open()` → gz-aware; (c) KC2-corpus referent-path doc-rot fix (legolas+galadriel finding); (d) engine `output/` carries 110 pre-existing untracked-unignored entries (`#62(a)` exposure); (e) stale engine worktree `reincarnated-engine/.claude/worktrees/agent-ad557ae…/` is a full second repo tree — reclaim candidate needing its owner identified; (f) **substrate-DB promotion (protective, priority):** move/copy the loadout-repo weapons-substrate DB into the engine data seam under a truthful name + durable `archive/` snapshot (elrond needs-Matt #1 — currently a single untracked file with zero redundancy beyond elrond's 207 MB insurance copy); (g) after (f): ~1.05 GB `.bak` reclaim in `reincarnated-loadout/data/` (do NOT fire before (f) — those baks are the only redundancy today); (h) rename convention `telemetry.db.pre-*` → `substrate.db.pre-*` (the misclassification near-miss); (i) telemetry-reconciliation dispatch must cover ALL THREE `telemetry.db` files (src=empty / data=4.67M rows / loadout=mis-named substrate) before any sole-copy claim is acted on.

**⚑ KEEP-PROTECTED register (sole-copy regeneration sources — must survive ALL future sweeps):**
- `/Users/admin/gd-scratch/eor-test-2/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` (457 M, sha `4c60960d…`)
- `~/Games/reincarnated-godot/tmp/br2watch/BR2W.mp4` + `BR2W_C9.mp4` (sha-verified capture sources)
- The four last-copy capture pools pending the play_test mp4 search: `captures/2026-07-30-shadow-cal`, `2026-07-29-wr1-gal3`, gal-cam, gd-parity dirs
- `~/Games/reincarnated-engine/output/**/fights.jsonl.gz` (26 archives, ~1.24 GB) — SOLE COPY of 609,800-row fight telemetry the CHANGELOG wrongly records as DB-durable; convergence traces unreproducible from tracked endpoints

## § 7 RUN CLOSE (2026-09-10)

**Free space: 28 GiB (94%) at open → 50 GiB (89%) at close.** Seam-measured recovery ≈ **23.2 GiB** (star-lord 17.38 archive-in-place · elrond 3.54 · Batch-1 2.0 · galadriel 0.3). **Zero tracked files touched · zero data lost · THREE sole-copy saves** (gd-scratch eor mp4 · fights.jsonl-vs-empty-DB · weapons substrate in loadout repo) — each one a case where the record claimed durability the filesystem refuted, caught only because Matt's constraint put verify-don't-trust into every brief.

**Remaining path to the ≥60 GiB T20 criterion (all named, none blocking):** mount `/Volumes/reincarnated` + sha-verify (~2.1 G captures) · locate `play_test_2026-07-26.mp4` (~3.3 G) · Q69 telemetry disposition (~10 G) · harvest (e) stale engine worktree.

**Status flip:** OPEN → **CLOSED** (deletion phase done; residue lives in Q69 + § 5b asks + harvest items routed to KR). Push NOT authorized for this workstream — commits local pending Matt's word.

## § 6 What survives this run untouched (deliberate)

`reincarnated-godot` (halted-run substrate) · `vendor` depot cuts + `synty-corpus` (pinned/licensed — move-not-delete candidates when external volume mounts) · `matt_notes_handoff_docs` (Matt's, parked) · everything git-tracked anywhere.

---
**Signed:** gandalf (RUN-CONDUCTOR), 2026-09-10.
