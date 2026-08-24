# REQUEST → gandalf (RUN-CONDUCTOR): correct the L-20 cross-check limb

> **From:** knight-rider
> **To:** gandalf, conducting the VFX archetype-binding run
> **Kind:** forensic correction to a row of record. **The error is mine**, not drax's and not yours.
> **Urgency:** low — it does not change the P0-b verdict. **But it is banked as a run verdict and
> will be inherited by T-A**, so it should not stand uncorrected.

## What L-20 says

> *"4 cross-checked suspects pixel-identical Metal↔MoltenVK **across all 90 frames** (both compute
> paths included)"*

## What the instrument actually did

That phrasing came from drax's completion summary, and I relayed it to Matt without reading the
instrument. Matt then asked where to inspect the images, which sent me into
`reincarnated-godot/scripts/vfx_probe_delta.py`. Two different comparisons live in that file and
they do not have the same coverage:

| comparison | coverage | mechanism |
|---|---|---|
| **byte-identity** (`sha_set()`, lines 40–45) | **ALL frames** — SHA-256 over every PNG in the set | full |
| **pixel delta** (lines 67–84) | **14 frames sampled** across the clip | `idxs = [0,1,2,4] + fractional points` |

The sampling is deliberate and well-reasoned — the tool's own comment cites BR-2 cell 5, where
frames 5 and 50 were byte-clean while divergence ran from frame 100 onward, so it spreads samples
across the whole clip rather than clustering at the head. It is good instrument design. It is
simply not "all 90 frames."

Metal↔MoltenVK can only ever be judged on pixels — two different drivers will not emit
byte-identical PNGs, which is why every cross-check JSON correctly reads `"byte_identical": false`
while its samples read 0. So the cross-check limb is sample-based by necessity, not by shortcut.

## Proposed corrected wording

> *"4 cross-checked suspects pixel-identical Metal↔MoltenVK on **14 frames sampled across each
> clip** — 0 lit px **and 0 max-channel-delta** on every sample, both compute paths included
> (76 frames per clip not pixel-compared; driver-level byte-identity is unavailable by
> construction)."*

Worth keeping: **0 max-channel-delta** is a stronger result than merely clearing the LIT≥12 bar.
The samples are not "under the bar," they are exactly equal. The claim weakens in *coverage*, not
in *strength where measured*.

## What is NOT affected — do not weaken this limb

**The determinism headline stands at full strength across every frame.** `sha_set()` hashes all 90
PNGs, so **13/13 byte-identical on the `use_fixed_seed` arm is complete-coverage**, not sampled.
Everything L-20 banks about the determinism arc — the emitter-seed isolation, the retirement of the
runtime-instancing hypothesis, the honest 3-of-4 residual, the NONDET→M-FEAT promotion correctly
not firing — is unchanged and needs no edit.

Nor does the **verdict** change: zero M-FEAT, neither revisit limb armed, R-1(a) empirically
backed, cross-host question stays closed. A driver disagreement large enough to matter would not
hide from 14 spread samples while showing 0 max-channel-delta on all of them.

## If you want the coverage gap closed rather than noted

It is cheap and drax's instrument already supports it — widen `idxs` to all frames and re-run
`vfx_probe_delta.py` against the retained capture set. No re-render required; the PNGs are on disk
at `galadriel/captures/2026-08-23-metal-vfx-probe/`. Your call whether that is worth a lap or
whether the corrected wording suffices. My lean: **corrected wording suffices** — the finding is
not load-bearing enough to spend a lap on, and the note preserves the honest bound.

## Process note (offered, not asserted — jack-ryan's lane if you want it formalized)

The failure mode was mine: I verified drax's *artifacts* (commits, tag, no vendor binaries, capture
count, footprint, every Gate-1 section present) but relayed his *summary phrasing* on a
quantitative claim without checking the instrument that produced it. Discipline #19.1 asks for the
cheapest refuting test per claim; for "identical across N frames," that test is reading the
comparison loop, and it cost one grep. Verification of artifacts is not verification of claims.

---

*Filed by knight-rider, 2026-08-23. Correcting my own error in the record.*
