# Legolas seam — disk-reclaim manifest (2026-09-10)

> **Author:** legolas (sub-agent, disk-reclaim dispatch). **Captured by:** gandalf (conductor) per the file-write-constraint pattern — authority is legolas's classification.
> **STATUS:** CLASSIFIED — deletions WITHHELD (host permission wall; the run converted to classify-and-manifest, execution batches to Matt). Run ledger: `agentic_orchestration/gandalf/notes/2026-09-10-disk-reclaim-rulings-and-ledger.md`.

## Inventory

| pool | total | tracked (KEEP) | untracked |
|---|---|---|---|
| `legolas/notes/` | 1.5 G | 143 MiB | 1.41 GiB |
| `legolas/scratch/` | 452 M | ~6 MiB | ~410 MiB |

One directory holds 1.44 G of the 1.5 G: `notes/2026-08-15-kc2-pm4-lap-w-p06-election/work/` — 1,437 extracted video frames + OCR crops. Markdown findings across the seam are tiny.

## DELETE set — 1,697 MB (1.66 GiB), all predicate gates PASSED, execution withheld

| path | size | gate | re-fetch pointer |
|---|---|---|---|
| `notes/2026-08-15-kc2-pm4-lap-w-p06-election/work/` | 1442 M | tracked=0 | recipe in `pm4w_findings.md` § 8.3 + referent mp4 (sha256 **verified**, see KEEP-PROTECTED) |
| `scratch/2026-08-12-kc2-pm3-lapc/` | 242 M | tracked=0 | same referent mp4; findings filed in `notes/2026-08-12-kc2-pm3-lap-c-blessings-reference-dot/` |
| `scratch/2026-07-28-murzak-reread/` | 13 M | tracked=0 | redundant 2nd clone of `github.com/IvanMurzak/Godot-MCP` @ `eba58e0` (cited clone survives at `scratch/2026-07-28-pcw1b/`) |

**Batch-execution one-liners (Matt or Matt-approved):**
```
rm -rf ~/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-15-kc2-pm4-lap-w-p06-election/work
rm -rf ~/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-08-12-kc2-pm3-lapc
rm -rf ~/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-murzak-reread
```

## ⚑ KEEP-PROTECTED — the regeneration dependency (the one genuine data-loss risk found)

The documented re-fetch path for both frame sets (`/Volumes/reincarnated/visual-artifacts/…`) points at the **unmounted external volume**. The surviving local copy was located and hash-verified:

- **`/Users/admin/gd-scratch/eor-test-2/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4`** (457 M)
- sha256 `4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8` — byte-identical to the digest pinned in `pm4w_findings.md` § 8.1.

**This file must survive any future sweep of `gd-scratch/`** — it is the sole reachable regeneration source for 1.68 G of deletable frames. Mechanism-claim discipline held: the `.gitignore`'s "regenerable" assertion was tested, found pointing at a dead path, and re-grounded on a verified copy before the DELETE class was assigned.

## KEEP (with reasoning)

- **All 1,585 tracked files** (incl. 27 M `pm4l_applied_damage_by_body.csv`, 12 M `s4_waves_full.json`) — committed seam product.
- **`scratch/2026-08-08-kc2-citation/` (97 M)** — cited by 8 filed docs; re-derivation dependency unverified → ambiguous → KEEP.
- **`scratch/2026-07-28-pcw1b/` (13 M)** — the *cited* Godot-MCP clone (named twice in the provision-cal-w1b note).
- **Thirteen smaller scratch dirs** — each cited by ≥1 filed doc.

Surviving bulk after execution: ~250 MB. Further reclaim here means deleting cited or committed material — needs a ruling, not a judgment call.

## Defect surfaced (routed, not fixed here)

**Stale referent paths in filed docs:** the KC2 lap corpus cites `/Volumes/reincarnated/visual-artifacts/…` — currently unreachable. Re-fetch pointers across that corpus likely share the rot. Cheap to fix; load-bearing for exactly this class of decision.
