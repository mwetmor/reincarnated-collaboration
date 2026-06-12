# UE Project Version Control — Matt Decision + Init Spec

**STATUS:** DECISION RECORD + EXECUTION SPEC — Matt approved 2026-06-11 (this session)
**Resolves:** sam Gate-2 WARN (Manifestation Phase-1 wave-close, `agentic_orchestration/qa/findings/2026-06-11-manifestation-phase1-spike-wave.md`) + radagast recommendation ("not another wave undecided")
**Routing:** david-h/mantis (execute at next PC session — batches naturally with Matt's console sitting); jack-ryan (decisions-log canonical write — proposal already in queue; this records Matt's approval + parameters)

---

## 1. The decision (Matt, 2026-06-11)

**Approved: git + Git LFS for the UE project**, as a NEW fifth repository. Parameters Matt ruled explicitly:

1. **Repo root = the UE project folder**: `C:\dev\reincarnated-unreal\Reincarnated\`
2. **Meshy raw GLBs stay OUT** (`RawAssets/` excluded): regenerable via Meshy task-ids (provenance recorded in mantis S6 findings). Version the imported `.uasset`, not the upstream blob.

## 2. Remote — already created (gandalf, Mac-side, Matt-authorized)

`git@github.com:mwetmor/reincarnated-unreal.git` (private). PC's existing SSH key auths it — no new credential work.

## 3. Init spec (david-h/mantis execute)

```bash
cd /mnt/c/dev/reincarnated-unreal/Reincarnated   # (or C:\... from Windows shell)
git init
git lfs install
```

**.gitignore** (UE-standard + project rulings):
```
Binaries/
DerivedDataCache/
Intermediate/
Saved/
.vs/
*.sln
RawAssets/
```
(`RawAssets/` exclusion per § 1.2 — record Meshy task-ids in findings/commit messages as provenance instead.)

**.gitattributes** (LFS tracking — authored binary types):
```
*.uasset filter=lfs diff=lfs merge=lfs -text
*.umap   filter=lfs diff=lfs merge=lfs -text
*.fbx    filter=lfs diff=lfs merge=lfs -text
*.glb    filter=lfs diff=lfs merge=lfs -text
*.png    filter=lfs diff=lfs merge=lfs -text
*.tga    filter=lfs diff=lfs merge=lfs -text
*.jpg    filter=lfs diff=lfs merge=lfs -text
*.wav    filter=lfs diff=lfs merge=lfs -text
*.exr    filter=lfs diff=lfs merge=lfs -text
```
(Note: tracked `*.glb` rule applies only to GLBs *inside Content-adjacent authored paths* — `RawAssets/` is gitignored above and never reaches LFS.)

**First commit:** the Phase-1 wave's authored state — `LV_ManifestationKnoll` (+ both lighting rigs), `SK_EarthAvatar`, `NS_CelestialSphere`, `Config/`, `Reincarnated.uproject`. Then:
```bash
git remote add origin git@github.com:mwetmor/reincarnated-unreal.git
git push -u origin main
```

## 4. Standing notes

- LFS budget: GitHub free tier = 1 GB storage/bandwidth per month. RawAssets exclusion keeps spike-phase footprint well under. If bestiary pipeline industrializes, $5/50 GB data pack is the escape valve — flag at that point, don't pre-buy.
- Commit + push discipline: `reincarnated-unreal` inherits the PC-seam standing wave-close push pattern (CLAUDE.md addendum) — mantis auto-commits authorized UE work-products; push at wave-close.
- DDC is NEVER versioned (gitignored) — Matt's P0.1 warm output is machine-local state.

**Author:** gandalf, 2026-06-11, recording Matt's verbal approval + parameter rulings.
