# Blind pair test

You are given 40 images, `pair_01.png` .. `pair_40.png`. Each shows two square crops side by side (LEFT | RIGHT)
from a hand-painted 3D game level, seen from the same fixed high camera at the same zoom.

In SOME pairs both crops come from the SAME build of the level. In the others, one crop comes from a different
build whose painting and rendering may be of different quality (for example: a different painter's hand,
blotchy or patchwork texture, magnified/blurry texels, painted light lit a second time, mismatched colour).

For each pair answer exactly one of:
- `SAME`  -- you cannot tell them apart as builds (content may differ; judge the painting and rendering quality);
- `LEFT`  -- the LEFT crop is from the different, lower-fidelity build;
- `RIGHT` -- the RIGHT crop is from the different, lower-fidelity build.

Judge only what you see in the images. Return a JSON object {"pair_01": "...", ..., "pair_40": "..."} and, per
pair, one short sentence naming the visual evidence for your answer.
