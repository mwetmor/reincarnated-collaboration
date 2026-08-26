# N-2 resolution — the 4a near-duplicate question (conductor-side; NOT panel-visible)

**Raised:** E-1/E-2 both measured twin+4a vs twin-as-is as near-duplicates (many frames bit-identical; one spark's hue at ~frame 139).
**Method:** read-only reconnaissance (Explore-class per run-pattern § 2.1 exception), receipts + code + git evidence. **Verdict: VERY HIGH confidence.**

## Finding

**4a IS in the render.** Falsified: config miss (both receipts show identical invocation flags; the +4a render executed post-4a code `fde563c`, its FINAL selfcheck carries full scuff telemetry), camera-region miss, and dir mixup (timestamps + selfcheck differ). Confirmed mechanism: always-on gate at `wwcr_whirlwind.gd:566` (`_w > 0.55`), `SCUFF_ENTRAIN_FRAC := 0.10`, measured dust travel 0.5036 m vs 0.4538 m predicted (the known quadrature residue) — **proof of motion, not silence.**

**Why the blind judges saw near-duplicates anyway:** ~8 changed pixels per frame in the engagement-ring region; 41 px of travel over 14 frames across an 18 px quad; 1,428 total changed pixels, neutral RGB. The dust moves exactly as specced — **and the spec's magnitude is below the perceptual threshold at the ratified camera.**

## Conductor's disposition

**The instruments were all green and the eye-level truth is: 4a does not read.** This is the KIT-FIDELITY rubric-law shape (run-pattern § 6.3) caught EARLY and cheaply by the panel instead of expensively by Matt: the treatment's own selfcheck verified motion-in-meters, but the owner's question is motion-on-screen. Standing consequence for every lap-2+ SPEC: **a depth treatment's acceptance criterion is stated at the JUDGING CAMERA in perceptual terms (pixels moved / contrast delta / area affected at k=0.665), never only in world-space meters.** Entrain-magnitude retuning of 4a is NOT ordered now — the lap-2 spec follows the blind differential (X-1/X-2), which subsumes this gap. W1's F-2 constraint (`mi.scale` no-op) is unrelated to this outcome and stands.

**Registry note:** no family action — this is a spec-discipline datum, not a phenomenon family. Banked for the VFX-TWIN-DEV skill draft: *world-space receipts do not certify screen-space reads.*
