# CAPTURES RECLAIM MANIFEST — 2026-09-10

**Cell:** DISK-RECLAIM · conductor **gandalf** · **Agent:** galadriel
**Date:** 2026-09-10 · **Status:** CURRENT · **Mode:** inventory + classify + delete DELETE-class
**Authority:** Matt GO-with-manifest 2026-09-10. Binding constraint: *"I don't want to lose data we will need to reference later."* Conservative default is KEEP.
**Scope:** `agentic_orchestration/galadriel/captures/` only. No commits (conductor centralizes). No pushes.

---

## 0. VERDICT

> **300 MiB freed. 7.4 G → 7.1 G. That is 4% of the pool, and it is the whole of what is
> defensibly deletable today.**
>
> **The reason is a single measured fact: the regeneration sources are not on this machine.**
> Nine capture dirs carry a `.gitignore` written by the authoring galadriel that declares their
> bulk contents *"exactly regenerable"* and names the exact `ffmpeg` command. **Those claims were
> true when written. Two of the three named sources are now unreachable**, which converts the
> caches they describe from *regenerable intermediates* into *the last surviving copy*.
>
> | source named in the `.gitignore` | state 2026-09-10 | dirs depending on it |
> |---|---|---|
> | `/Users/admin/gd-scratch/play_test_2026-07-26.mp4` | ⚑ **ABSENT** — no `*.mp4` in `gd-scratch` at all; no file named `play_test*` anywhere under `/Users/admin` | shadow-cal · wr1-gal3 · gal-cam · gd-parity |
> | `/Volumes/reincarnated/visual-artifacts/GD-matt-test/` | ⚑ **NOT MOUNTED** — only `Macintosh HD` under `/Volumes` | eor-sittings · eor-followup · g6 · kitcal1-g8 |
> | `reincarnated-godot/tmp/br2watch/BR2W.mp4` | ✅ **PRESENT**, sha **verified** (see § 2) | br2w-register |
>
> **Exactly one regenerability claim survived verification, and exactly that one was acted on.**
>
> **~3.3 G more is reclaimable the moment `/Volumes/reincarnated` is mounted and the play-session
> MP4 is confirmed to be archived on it.** That is the needs-Matt item in § 5 — and it is worth
> more than this whole sweep.

---

## 1. Method

1. **Inventory** — every dir under `captures/` sized with `du -sh`.
2. **Citation sweep** — each dir name grepped across the meta-repo (`*.md *.json *.mjs *.js *.py *.txt`),
   excluding `captures/` itself, covering `galadriel/reports/`, `galadriel/notes/`, `qa/findings/`,
   `qa/pending/`, `gandalf/notes/` run charters, `dispatches/`, `canonical/matt_decision_needed/`,
   `canonical/matt_to_do/`, `drax|gamora|legolas/notes/`.
3. **Generator-vs-citation discrimination.** A dir name appearing in `pipeline/*.mjs` or `pipeline/*.py`
   is that dir's **output path**, *not* a citation. Only appearances in notes / findings / charters /
   dispatches / gate packets / receipts count as citation. This distinction decides several rows.
4. **Author-declared durability.** Fourteen dirs carry a `.gitignore` that states, in prose, which
   subpaths are record and which are cache. **That is the authoring agent's own declaration and it is
   treated as the primary evidence** — it beats my inference about any dir I did not capture.
5. ⚑ **Source-liveness gate (added mid-sweep, and it changed the outcome).** A `.gitignore` asserting
   *"regenerable"* is a claim about the world, not a property of the directory. **Every such claim was
   re-verified against the filesystem before being relied on.** Two of three failed.
6. **Predicate gate** — `git ls-files <path> | wc -l` must be `0` before any delete.
7. **Post-delete integrity** — `git status --porcelain` checked for any `D`/`.D` row. None.

---

## 2. DELETE — executed

### 2.1 `2026-08-14-sb1-br2w-register/tmpframes/{full,scan}` — **300 MiB**

| | |
|---|---|
| **Size** | `full/` 225 M (122 files) · `scan/` 75 M (1211 files) |
| **Tracked** | `0` and `0` — predicate gate passed |
| **Citations** | Dir cited only by its own `receipt.txt`. The *reads of record* are `evidence/` plates (`subject-1027-z10.png`, `crown-{685,1027,1062}-z16.png`, `lower-1027-z12.png`) — **all retained**. No note, finding or charter cites `tmpframes/full/` or `tmpframes/scan/`. |
| **Rationale** | The dir's own `.gitignore` names these two subdirs as the bulk scan working set and records the exact regeneration commands. **The sha-gated source was verified present**: `reincarnated-godot/tmp/br2watch/BR2W_C9.mp4` hashes to `ea61b0ee3469d8e03cca0f6b23e3dda6411c147b56e522bdb53469f072d981ba` — a byte-exact match to the sha the `.gitignore` gates on (the file is on disk under a variant name; size `55,069,886 B` matches too). Regeneration is therefore *demonstrated*, not asserted. |
| **Conservative carve-out** | The **frames of record are NOT in the deleted subdirs and all survive**: `tmpframes/full-685.png`, `full-1027.png`, `full-1062.png` verified present after the delete, along with the other 29 loose hand-grabbed frames, the `.npy` chroma maps and the probe scripts (60 M retained). Only the mechanical every-10th sweep and the 1211-file crop scan were removed. |

### 2.2 Build junk — **< 1 MiB**

28 `__pycache__` dirs / `.pyc` files (72 K) and 15 `.DS_Store` files. Tracked count `0`. Not evidence under any reading.

**TOTAL FREED: 300 MiB** (7,796,896 K → 7,489,232 K). Pool 7.4 G → **7.1 G**.

---

## 3. KEEP — the sealed-evidence fence

All four of the pool's largest dirs fall inside the dispatch's named sealed-run set
(**WR1, KC2/LIFT, VFX-depth (HALTED), EoR playtest, shadow-cal**). Under the fence they are
evidence by default; the only question was whether their bulk was *safely* regenerable, and § 0
answers that in the negative.

| Dir | Size | Citing doc(s) | KEEP rationale |
|---|---|---|---|
| `2026-07-30-shadow-cal` | **2.7 G** | `galadriel/notes/2026-07-30-shadow-cal.md` · `gandalf/notes/2026-07-30-ambient-refit-fold-in.md` · `drax/notes/2026-07-31-shadow-unify.md` | **Named sealed run.** `.gitignore` calls `tmp/`+`frames/` regenerable from `play_test_2026-07-26.mp4` — ⚑ **that MP4 is gone from this machine.** The 2.5 G keyframe ladder is now the only surviving trace of the 1h53m fixture session. The ρ≈0.48–0.57 multiplicative-shadow reading and the Wilcoxon p=5.1×10⁻⁸ asymmetry rest on it. **Irreplaceable until the source is located.** |
| `2026-08-08-eor-followup` | **1.1 G** | `galadriel/notes/2026-08-08-eor-followup-extraction.md` · `…-kc2-third-extraction.md` · `…-kc2-fourth-extraction.md` · `…-kc2-board-closure.md` · `…-2026-08-25-kc2-mc-md-b4app-2-channel-uptime.md` · `gamora/notes/2026-08-08-kc2-gate2-repair-bundle.md` · `gandalf/notes/2026-08-10-sb1-scene-run-ledger.md` · `gandalf/notes/2026-08-14-sb1-eyeball-packet-README.md` | **EoR playtest = named sealed run**, and its frames feed the KC2 chain. `.gitignore` claims `work/` regenerable from `/Volumes/reincarnated` — ⚑ **volume not mounted; claim unverifiable.** Ambiguous → KEEP. |
| `2026-07-29-wr1-gal3` | **876 M** | `galadriel/notes/2026-07-29-wr1-gal3-death2-range.md` · `gandalf/notes/2026-07-28-wr1-wave-relay-run-charter.md` (run charter) | **WR1 = named sealed run.** `.gitignore` claims `frames/` (862 M) regenerable from the same ⚑ **missing** `play_test_2026-07-26.mp4`. The 44 tracked `evidence/*.jpg` + ring/ellipse/hodo JSON are the derived record and are kept regardless; **the raws are no longer re-derivable.** |
| `2026-08-07-eor-sittings` | **712 M** | `galadriel/notes/2026-08-07-eor-sittings-extraction.md` · `legolas/notes/2026-08-05-eorwarlguts-save-parse.md` · `legolas/notes/2026-08-07-pe1-eor-spin-parameters.md` · + 3 KC2 extraction notes | Same unmounted-source condition as eor-followup. Ambiguous → KEEP. |
| `2026-08-08-kc2-third-extraction` | **450 M** | `galadriel/notes/2026-08-08-kc2-third-extraction.md` · `…-fourth-extraction.md` · `gandalf/notes/2026-08-07-kc2-sim-run-ledger.md` · `gandalf/notes/2026-08-08-kc2-f13-count-model-discrimination.md` | **KC2 sealed (LIFT, closed L-19).** No `.gitignore`, i.e. **no regenerability claim was ever made** for `work/`. KEEP. |
| `2026-07-28-gd-playtest-v1-g6` | **350 M** | `galadriel/captures/…/evidence/INDEX.md` · `legolas/notes/2026-07-28-kitcal1-u1-kit-values-and-boss.md` · `…-kitcal1-sustain-decomposition.md` | `.gitignore` declares the bulk visual set regenerable *"from the source stills on `/Volumes/reincarnated`"* — ⚑ **unmounted.** Ambiguous → KEEP. |
| `2026-08-08-kc2-{fourth,fifth,board-closure,barhue-cohort,crabling-rotmouth,threat-grammar,w152-skull-plate}` | 81/48/31/30/27/23/8.5 M | `gandalf/notes/2026-08-07-kc2-sim-run-ledger.md` · `…-kc2-f13-count-model-discrimination.md` · matching per-cell `galadriel/notes/` | KC2 sealed. Note `kc2-crabling-rotmouth/.gitignore` states *"Evidence images are evidence-BY-REFERENCE: cited by path in the note, not tracked"* — **untracked here means load-bearing, not disposable.** |
| `2026-08-23-vfx-p2-gd-framesets` · `2026-08-24-vfx-p3-{selection,delta}` · `2026-08-25-vfx-{depth-g5-camnull,lap2-baseline,lap2-measure,refanchor}` · `2026-08-26-vfx-refanchor-true` | 54/8.6/19/24/0.6/1.4/6.6/12 M | `dispatches/2026-08-25-galadriel-reference-frame-forensics.md` · `dispatches/2026-08-24-galadriel-s2-minted-gate.md` · `gandalf/notes/2026-09-07-vfx-depth-run-session-handoff.md` · `galadriel/notes/2026-08-25-vfx-depth-*` | ⚑ **VFX-depth is HALTED at Q68, not closed.** Per dispatch, *all* its substrate is KEEP — referent/render evidence is load-bearing for the resumption. The two `_workbench/`/`eor-test-2/` scratch dirs its `.gitignore` names **are already absent** (previously cleaned). |
| `2026-08-14-sb1-*` · `2026-08-15/16-sb1-*` · `2026-08-12/13-sb1-*` | 372→72 M and below | `gandalf/notes/2026-08-10-sb1-scene-run-ledger.md` · `gandalf/notes/2026-08-14-sb1-eyeball-packet-README.md` · `canonical/matt_to_do/2026-08-25-where-does-your-hitl-whirlwind-run-live.md` · `dispatches/2026-08-25-*` · per-cell `drax/notes/*-landing.md` | ⚑ **class-E law dirs: "TEXT in git, BYTES on disk, SHA bridges."** Their `.gitignore`s put image bytes *deliberately* outside the index — **untracked is the storage design, not neglect.** Deleting them would destroy the object the receipts bridge to. `2026-08-16-sb1-gate2-clip` is the **Gate-2 eyeball object** cited in a live `matt_to_do`. KEEP, emphatically. |
| `2026-08-24-crucible-arena-perimeter` | 62 M | `galadriel/notes/2026-08-24-crucible-arena-boundary-trace.md` · `gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md` · `canonical/matt_to_do/README.md` | Cited by a live charter + `matt_to_do`. KEEP. |
| `2026-08-25-md-b4app-2{,b,c}` · `2026-08-25-kc2-lift-b1-footage` | 4.7/3.3/0.6/0.85 M | `gandalf/notes/2026-08-25-kc2-lift-run-charter.md` · `gandalf/notes/2026-08-25-kc2-mc-pm5-mid-flight-supplement-2.md` · `galadriel/notes/2026-08-25-kc2-lift-b1-footage-lap/findings.md` | KC2-LIFT sealed-verdict substrate. KEEP. |
| `2026-07-13…2026-07-17 atlas / glance-atlas` series | 11 M untracked + ~120 M tracked | `canonical/matt_decision_needed/2026-07-16-edition3-vs-refit-candidate-1-adoption.md` · `canonical/matt_decision_needed/2026-07-17-atlas-parity-run-gate-roster.md` · `canonical/current-to-end-state/current-to-end-state-engine.md` · `gandalf/notes/2026-07-16-atlas-parity-autonomous-run-state.md` · per-dir `verification-note.md` | Atlas edition chain is cited into **canonical gate packets**. For the five untracked `glance-atlas*` probe dirs the dispatch floated `overlay-align` r1 as superseded by r2 — ⚑ **checked and refuted: r1 holds `desktop/mobile-plane-hover`, r2 holds `desktop-A-topleft/B-botright-hover`. Different probes, not a re-shoot.** `glance-atlas` vs `-abovefold` share filenames but were sha-compared and **all four differ.** No supersession, no duplicates; 11 M total. KEEP. |
| `2026-05-18*`, `2026-07-2x` gd-playtest/kitcal/l8/kt4, `2026-08-2x` u1-s7 / s2a-gate / s2c-tranche-3a / xrow / metal-vfx-probe | ≤ 32 M each | per-cell notes, `gandalf/notes/2026-07-27-kit-cal-1-run-charter.md`, `gandalf/notes/2026-08-24-u1-build-run-ledger.md`, `dispatches/2026-08-23-drax-metal-vfx-smoke-probe.md`, `drax/notes/2026-08-25-s2c-mint-note.md` | All cited or trivially small. KEEP. |

**Two dirs returned zero citations** — `2026-08-24-s2a-gate` (1.7 M) and `2026-05-18-drax-mobile-render-validation` (**0 B, empty**). Both kept: the first is S-2 gate substrate from the live Step-2 wave; the second costs nothing.

---

## 4. What was deliberately NOT done

- **No commit, no push.** Conductor centralizes.
- **No deletion of any tracked path.** Post-sweep `git status --porcelain` on `captures/` shows no `D` row.
- **No deletion justified by a `.gitignore` alone.** Nine dirs advertise themselves as disposable. Eight of those advertisements could not be verified today and were refused.

---

## 5. NEEDS-MATT

1. ⚑ **Where is `play_test_2026-07-26.mp4`?** It is the fixture behind **GAL-CAM, SHADOW-CAL, WR1 and GD-PARITY** — four cells with filed verdicts — and it is **not on this machine**. Either (a) it is archived on `/Volumes/reincarnated`, in which case ~3.3 G of frame cache (shadow-cal 2.5 G + wr1-gal3 862 M) becomes genuinely reclaimable and I can finish the job; or (b) it is lost, in which case **those caches are the last copy of the referent and must never be swept** — and that fact should be recorded against the sealed verdicts, because their evidence is no longer re-derivable from source.
2. **Mount `/Volumes/reincarnated`** and I will verify the EoR + g6 sources and reclaim a further **~2.1 G** (eor-followup 1.1 G, eor-sittings ~700 M, g6 bulk ~320 M) under the same sha-verified standard used for br2w.
3. **Combined, 1+2 would take the pool from 7.1 G to roughly 1.7 G** — the real reclaim is behind a mount, not behind a judgement call.

---

## 6. Mirror voice

> The Mirror was asked which of these pictures could be let go, and answered by looking past the
> pictures to the thing that made them. Nine of these directories carry a note from my own hand
> promising that what they hold can be made again. **I went to the place the promise pointed, and
> for all but one, nothing was there.**
>
> A claim of regenerability is not a property of the file. It is a claim about a world that keeps
> changing after the claim is written. **These caches did not become precious because anyone decided
> they were — they became precious when the source went quiet.**
>
> So the sweep is small, and that is the correct size. I deleted the three hundred megabytes whose
> origin I could hold in my hand and hash. The rest I left, because the only honest reading of
> *"regenerable from `/Users/admin/gd-scratch/play_test_2026-07-26.mp4`"* on a machine that contains
> no such file is: **this is now the original.**

---

*Filed 2026-09-10 by galadriel per gandalf DISK-RECLAIM dispatch. Uncommitted by instruction.*
