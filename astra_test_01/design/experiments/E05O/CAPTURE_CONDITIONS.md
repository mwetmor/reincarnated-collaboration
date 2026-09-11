# Final GPU conditions, frozen before capture

The native-source diagnostic passes two views under the combined partition source condition. Test all8 views across original96cases with three composition methods: independent display-size alpha-over (method control); ordinary alpha-over into a512×512 native intermediate, then uniform display sampling; geometry-mask partition accumulation into same native intermediate, then uniform display sampling. Each compared against a full source reference sampled once identically. No source image enlargement or per-view scale adjustment.

Hypothesis: filtering each overlapping layer before compositing differs from filtering a composite. Native intermediates cost1MiB RGBA each,16MiB nominal for8views×2headstates per method, independent of3backgrounds. This is texture byte arithmetic, not measured GPU residency. Cache work belongs in adapter. Prefer the simpler ordinary native composition only if all96cases pass; otherwise mask method only if all96pass. No method is accepted from the two-view source probe alone.

Bad controls:20source-pixel helmet shift; body visibility mask from180° opposite heading. Secondary hair rays disabled only for this isolated composition source. No interaction-lighting pass.
