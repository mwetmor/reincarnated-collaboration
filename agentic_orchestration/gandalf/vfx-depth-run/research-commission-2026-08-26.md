# Research commission — video→editable-VFX literature (Matt-sourced via Codex, 2026-08-26)

**Commissioner:** gandalf (RUN-CONDUCTOR) · **Executor:** legolas (Mode A — analytical) · **Occasion:** Matt's Codex survey found the field's pieces converging on our architecture; ParticleGen's named missing contribution (reference-video-derived spec + comparison) is what this run already does.

## Sources (Matt-provided links, verbatim)

| Work | Link | Priority |
|---|---|---|
| ParticleGen (agents → editable Niagara; JSON effect-IR; render-critique-patch-rollback loop) | https://arxiv.org/html/2608.00629 | **1 — highest** |
| Generative Omnimatte (effect-layer video decomposition) | https://cvpr.thecvf.com/virtual/2025/poster/34367 | **2** |
| Gen-Omnimatte public implementation | https://github.com/gen-omnimatte/gen-omnimatte-public | **2** |
| Search-based co-creation of particle systems (MAP-Elites + human selection) | https://www.sciencedirect.com/science/article/pii/S0950584924000715 | **3** |
| KinemaFX (semantic/kinematic effect structuring) | https://arxiv.org/abs/2507.19782 | 3 |
| Thinking in Blender (VLM analysis-by-synthesis in an editor) | https://arxiv.org/abs/2606.02580 | 4 |
| Grounded-Video-LLM (temporal grounding) | https://aclanthology.org/2025.findings-emnlp.50/ | 5 |
| EffectMaker (reference-video effect transfer — pixels, not assets) | https://openaccess.thecvf.com/content/CVPR2026/html/Yang_EffectMaker_Unifying_Reasoning_and_Generation_for_Customized_Visual_Effect_Creation_CVPR_2026_paper.html | 5 |
| VFXMaster | https://libaolu312.github.io/VFXMaster/ | 5 |

## Questions (deliverable shape: findings note, answers per question, quotes + section cites)

1. **ParticleGen's effect-IR schema, in full** — the JSON fields for phases/emitters/renderers/curves; how parameters are exposed for patching; how rollback + best-state selection are implemented; what the critic actually scores. We want the IR as a template for our VFX-TWIN-DEV SPEC format (Godot particles, not Niagara — structural fit, not literal reuse).
2. **Gen-omnimatte runnability** — model weights public? compute footprint? input constraints (camera motion, length, resolution)? Would it plausibly separate barbarian+whirlwind from a D4 arena at 1080p60? (Consumer: galadriel reference-side effect-region extraction; dust-devil + damage-number confound subtraction.)
3. **MAP-Elites/co-creation paper** — the fitness/behavior-descriptor design for particle systems; how human selection is injected; population sizes and iteration counts that worked. (Consumer: lap-3 amplitude parameter sweep with galadriel bars as fitness.)
4. **KinemaFX** — what "semantic + kinematic" decomposition buys; anything reusable for our feature-family registry?
5. **Field check** — does ANY work do blind differential comparison (reference video vs candidate render, judge blinded to build lineage)? If none: our seats remain the differentiator; say so plainly.

## Boundaries

Read-only, Mode A. No code. Findings to `agentic_orchestration/legolas/notes/`. The run's blind seats (X-5/X-6) are quarantined from this commission and its outputs.
