# Offscreen orientation failure and last-batch allocation

Batch3 custom partition shader rendered upside down into the offscreen target. It manually used direct-screen clip coordinates without accounting for the render-target orientation. Partition96comparisons and its negative controls are INVALID for evaluating the representation; preserve pixels/results/adapterv1. Ordinary sprite over-direct46fail and over-native34fail remain valid independent controls.

Before repaired output: replace offscreen vertical clip coordinate with its inverse in named adapter. Fourth/final batch verifies the repaired partition all96cases and its2negative controls, plus saved review. References and unaffected controls reused from batch3. No fifth batch, no new source/configuration, no altered metric. This expands planned review-only allocation within4batch/50MB/30minute ceiling. A future custom offscreen path needs an asymmetric orientation witness before matrix capture.
