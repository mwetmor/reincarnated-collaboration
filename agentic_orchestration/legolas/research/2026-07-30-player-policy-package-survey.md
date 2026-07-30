# Research — player-policy package landscape survey — 2026-07-30

**Mode:** A (analytical, UNKNOWN-RESEARCHER)
**Commissioner:** gandalf (`RUN-CONDUCTOR`), run WR3-KITE-COMMIT
**Ruling under review:** R-WR3-9 (charter `agentic_orchestration/gandalf/notes/2026-07-30-wr3-kite-commit-run-charter.md` §2)
**Access date for all sources:** 2026-07-30
**Confidence grading:** HIGH = verified from primary docs / package registry / repo API. MEDIUM = primary source but transfer to our case is inferential. LOW = inference or secondary source.

---

## Summary

The survey **CONFIRMS R-WR3-9 without amendment**, and it confirms it for a sharper reason than the ruling states. Matt's suspicion — that packages are readily available — is **correct about the layer he could see and inverted about the layer that matters**. The off-the-shelf ecosystem is large, healthy, and post-cutoff-current, but every mature package in it is a **training framework or an interface standard**. Not one of them is a *player-behavior implementation*. There is no package on PyPI, maintained or otherwise, that ships an ARPG kite/commit policy, or a utility-AI decision layer for combat, that we could install and point at our sim. The nearest maintained thing in that space is `py_trees` (a tree-structuring library, not behaviors), and the nearest research artifact is CombatVLA — a 3-billion-parameter vision-language-action model trained on video-action pairs, unfit on both our constraints at once.

Second confirmation, from a primary doc: Stable-Baselines3's own reproducibility page states that *"Completely reproducible results are not guaranteed across PyTorch releases or different platforms"* and that *"results need not be reproducible between CPU and GPU executions, even when using identical seeds."* That is the determinism constraint answering itself, in the vendor's words, on the vendor's site.

Third: the infeasibility read on demonstration data **holds** for BC / offline-RL / VPT-style approaches — `imitation`, `d3rlpy`, and Minari all require action-aligned arrays, verified from each project's own schema docs. One genuine exception surfaced that I did not expect and am obliged to report: **preference-comparison (RLHF-style) reward learning needs no demonstrations at all** — only agent-generated trajectory fragments plus pairwise "which is better" labels. It does not change stage 1. It is a real stage-3 option and I name it in §5.

The one change I recommend to *implementation*, not to the ruling: **do not take gymnasium as a core dependency.** The Env contract is a duck-typed protocol; we can satisfy it with zero imports and keep the 450-trace battery hot path free of any RL package. See §6.

---

## §1 — The headline negative result (Matt's hypothesis, adjudicated)

Matt's verbatim suspicion was that *"creating a 'player AI' from scratch would not be the sensible approach as packages may be readily available on the web."* The honest adjudication is a split:

**What IS readily available (and we should take):** the *interface standard*. Gymnasium is the de-facto contract, it is stable, and adopting its shape costs us almost nothing. R-WR3-9 already banks this.

**What is NOT available at any maturity:** the *policy*. Searched PyPI directly for the candidate namespace — `utility-ai`, `pyutilityai`, `pygoap`, `bt-py` do not exist; `goap` last released 2021-10-02; `simpleai` 2021-09-02; `pygame-ai` 2019-06-08. Web search for a packaged ARPG combat/kiting policy library returned tutorials, hobby repos, and research papers — no library. **[HIGH — verified by direct PyPI JSON API queries and search]**

The structural reason is not an accident of search terms. Player-behavior policy is *game-specific by construction*: it is a function of one game's verbs, timings, resource model, and telegraph vocabulary. A package cannot ship it without shipping the game. What packages ship instead is everything *around* the policy — the env contract, the training loop, the replay buffer, the logger. That is exactly the boundary R-WR3-9 drew.

So the sensible reading of Matt's instinct is preserved and satisfied: **do not hand-roll the parts that are commodity (the interface), do hand-roll the part that is ours (the behavior).**

---

## §2 — Adoption matrix

Fit is judged against our four hard constraints: **(D)** byte-identical determinism under seed across a 450-trace battery; **(S)** headless tick-sim speed; **(N)** no action-level demonstration data; **(P)** Python 3.11+ engine with a deliberately lean dependency set (`anthropic`, `pydantic`, `numpy`, `pyyaml`, `rich`).

| Package | Current ver / release | License | Maturity signal | Determinism posture | Fits? | Integration cost | Conf. |
|---|---|---|---|---|---|---|---|
| **Gymnasium** | 1.3.0 · 2026-04-22 | MIT | 12,255★, pushed 2026-07-26, 8 releases since 1.0.0 | `reset(seed=int)` reseeds the env PRNG; determinism is the *env author's* responsibility, which here is ours | **YES — adopt the contract** | Very low. Core deps are `numpy` (already have), `cloudpickle`, `typing-extensions`, `farama-notifications` — all pure-Python, tiny | HIGH |
| **PettingZoo** | 1.26.1 · 2026-04-27 | MIT | 3,482★, pushed 2026-07-28 | inherits Gymnasium seeding | **NOT NOW** — our fight is single-agent (policy vs. scripted boss). Only relevant if the boss ever becomes a *learned* second agent | Deferred | HIGH |
| **Shimmy** | 2.0.1 · 2026-04-10 | MIT | Farama-maintained compat shims | n/a | **NO NEED** — we have no legacy API to bridge | n/a | HIGH |
| **Stable-Baselines3** | 2.9.0 · 2026-06-15 | MIT | 13,633★, pushed 2026-07-25; 2.9.0 relaxed the gymnasium pin to `>=0.29.1,<2.0` | **Vendor disclaims cross-platform/cross-torch reproducibility, verbatim** | **NO as policy-of-record; YES as later probe** | Moderate — pulls `torch>=2.8` (2.9.0 raised the floor). Must stay an optional extra | HIGH |
| **sb3-contrib** | 2.9.0 · 2026-06-15 | MIT | tracks SB3 | as SB3 | as SB3. `MaskablePPO` is the relevant piece if we ever mask illegal verbs | same as SB3 | HIGH |
| **RLlib (Ray)** | ray 2.56.1 · 2026-07-17 | Apache-2.0 | 43,395★, pushed 2026-07-30 | distributed-actor scheduling adds nondeterminism surface | **NO** — built for cluster-scale; grotesque overkill for a 450-trace single-machine battery | High | HIGH |
| **TorchRL** | 0.13.3 · 2026-07-14 | MIT | 3,509★, pushed 2026-07-30, active | torch-level; same disclaimers as SB3 apply | **NO for stage 1** — lower-level than SB3 with no compensating benefit for us | High | HIGH |
| **CleanRL** | 1.2.0 · 2023-05-22 | MIT (repo NOASSERTION) | 10,189★ but PyPI dormant ~3 yr; `requires_python <3.11` — **incompatible with our 3.12** | single-file scripts, easy to audit for seeding | **NO** — and note it is a *reference-implementation collection*, not a dependency, by design | n/a (copy-paste model) | HIGH |
| **sample-factory** | 2.1.1 · 2023-06-19 | MIT | 1,012★; PyPI dormant since 2023 (repo pushed 2026-07-02) | async rollout workers → nondeterministic by architecture | **NO** — its whole value proposition is high-throughput async, which is the opposite of what we need | High | HIGH |
| **PufferLib** | 3.0.0 · 2025-06-23 | MIT | 6,207★, pushed 2026-07-29 — most active newcomer | not documented as deterministic; speed-first design | **NO for stage 1** — plausible future probe if training throughput ever binds | Moderate | MEDIUM (activity HIGH; determinism posture undocumented) |
| **Tianshou** | 2.0.1 · 2026-04-02 | MIT | 10,899★; `requires_python >=3.11` | n/a for us | **NO** — no advantage over SB3 for a probe role | Moderate | HIGH |
| **skrl / AgileRL** | 2.1.0 · 2026-05-10 / 2.8.4 · 2026-07-29 | MIT / — | actively released | n/a | **NO** — niche (Isaac Sim / RLOps) | Moderate | MEDIUM |
| **`imitation`** | 1.0.1 · 2025-01-07 | MIT | 1,773★; repo untouched since 2025-01-07 — **effectively dormant** | n/a | **NO for BC/GAIL/AIRL/DAgger** — `Trajectory` requires `acts` (see §4.3). **Preference-comparisons is the exception** (§5) | Moderate | HIGH |
| **d3rlpy** | 2.8.1 · 2025-03-02 | MIT | 1,675★; repo pushed 2025-09-10 | n/a | **NO** — `MDPDataset(observations, actions, rewards, terminals)`; actions mandatory | n/a | HIGH |
| **Minari** | 0.5.3 · 2025-04-17 | MIT | 1,347★, repo pushed 2026-07-19 | n/a | **NO** — schema mandates a per-step `actions` record | n/a | HIGH |
| **py_trees** | 2.5.0 · 2026-07-14 | BSD | 627★, pushed 2026-07-16; genuinely revived (2.3.0 Jan-25, 2.4.0 Nov-25, 2.5.0 Jul-26) | pure Python, deterministic tick — no determinism objection | **NO — but on cost/benefit, not on fitness** | Low (`pydot` only) — but see §4.4 | HIGH |
| **`goap` / `simpleai` / `pygame-ai` / `owyl`** | 2021 / 2021 / 2019 / 2009 | var. | abandoned | — | **NO** — dead | n/a | HIGH |
| **LLM-agent frameworks** (LangGraph, CrewAI, PydanticAI, …) | current | var. | very active | inference is nondeterministic; latency is 10²–10³ ms/decision | **NO** — see §4.6 | — | HIGH |

*Licensing footnote:* GitHub's API reports `NOASSERTION` for PettingZoo, Minari, CleanRL, and py_trees. In each case the package's own PyPI metadata declares a standard OSI license (MIT/MIT/MIT/BSD). This is a GitHub license-detector artifact, not a licensing risk. **[HIGH]**

---

## §3 — Commission question 1: is Gymnasium still the contract?

**Yes, and it is now a *frozen* contract — which materially strengthens R-WR3-9.** The v1.0.0 release notes state verbatim:

> "This is the complete release of `v1.0.0`, which will be the end of this road to change the project's central API (`Env`, `Space`, `VectorEnv`)."

Since that commitment (2024-10-08) the project has shipped 1.1.0, 1.1.1, 1.2.0, 1.2.1, 1.2.2, 1.2.3 and 1.3.0 (2026-04-22) with no central-API break — the 1.3.0 notes are entirely environments, wrappers, and vector-env fixes. Independent corroboration of the freeze's credibility: **SB3 2.9.0 widened its gymnasium pin from `<1.3.0` to `<2.0`** — a downstream maintainer betting on API stability across an entire unreleased major. **[HIGH — Gymnasium and SB3 release notes, GitHub Releases API]**

The contract we would be implementing:

```
reset(*, seed: int | None = None, options: dict | None = None) -> tuple[ObsType, dict]
step(action: ActType) -> tuple[ObsType, SupportsFloat, bool, bool, dict]
```
plus `observation_space` / `action_space` as `spaces.Space`, and an `np_random` generator. **[HIGH — gymnasium.farama.org/api/env/]**

**No successor exists and none is signalled.** Farama's stated forward work is vectorized-env upgrades and hardware-accelerated built-in environments — not an API-v2. The predecessor `gym` is frozen at 0.26.2 (2022-10-04). Nothing else has displaced it: every maintained training stack in the matrix consumes the Gymnasium API. **[HIGH for the freeze and the absence of a v2 announcement; MEDIUM for "none will appear" — that is a forecast]**

PettingZoo is the multi-agent sibling with the same seeding discipline. It becomes relevant only if the boss is ever promoted from scripted to learned. Not stage 1, not stage 2. **[HIGH]**

---

## §4 — Findings by layer

### 4.2 Training stacks — determinism is the disqualifier, and the vendor says so

The decisive fact is primary and unambiguous. SB3's reproducibility guidance states *"Completely reproducible results are not guaranteed across PyTorch releases or different platforms"* and *"results need not be reproducible between CPU and GPU executions, even when using identical seeds."* **[HIGH — stable-baselines3.readthedocs.io]**

Precision matters here, and I want to be exact rather than convenient for the ruling: **that disclaimer bites hardest on *training*, not on *inference*.** A trained policy with frozen weights, evaluated with `deterministic=True`, is a deterministic function on a fixed machine. The residual risks for a battery are (a) float-op reproducibility across torch versions and platforms, (b) the weights becoming an opaque binary artifact in the gate chain, and (c) `torch>=2.8` in the battery hot path. Risk (b) is arguably the worst for us: a regression battery whose BEFORE/AFTER diff depends on a several-hundred-megabyte non-diffable artifact loses the property that makes it a gate. So the conclusion R-WR3-9 reached survives, but the honest reason is *artifact auditability and platform-float risk*, not "learned policies are nondeterministic" flatly. **[HIGH for the quoted disclaimers; MEDIUM for the auditability argument, which is mine]**

RLlib, sample-factory, and PufferLib add architectural nondeterminism (distributed actors, async rollout workers) or are simply scaled for problems orders of magnitude larger than ours. CleanRL is `<3.11` on PyPI and incompatible with the engine's 3.12 — and is in any case a reference-implementation collection meant to be read and copied, not depended on. **[HIGH]**

### 4.3 Imitation / offline RL — the infeasibility read holds

Verified from each project's own schema documentation:

- **`imitation`**: `Trajectory` requires `obs` *(len+1, obs_shape)*, **`acts` *(len, act_shape)***, `infos`, `terminal`. BC, GAIL, AIRL, DAgger, SQIL, density-based reward modeling, and MCE IRL all consume this. No observation-only pathway is offered. **[HIGH]**
- **`d3rlpy`**: `MDPDataset(observations, actions, rewards, terminals)` — all four required and timestep-aligned. **[HIGH]**
- **Minari**: mandatory per-episode `observations`, **`actions`**, `rewards`, `terminations`, `truncations`, `infos`. **[HIGH]**

The `.gdc` referent save holds aggregate lifetime statistics. It contains no input trace. **The BC path is confirmed closed.** VPT does not rescue it: OpenAI's method needs a contractor set of *video paired with keypress/mouse actions* to train the inverse-dynamics model that labels the unlabeled video — so it needs action labels too, just fewer of them, and we have neither video nor labels of Matt's play. CombatVLA (arXiv 2503.09527, rev. 2026-01-09) is the on-genre 2026 artifact — a 3B-param VLA for 3D ARPG combat — and it is trained on "video-action pairs collected by an action tracker," failing our data constraint and our battery-speed constraint simultaneously. **[HIGH]**

Maintenance note worth carrying: `imitation` has not been touched since 2025-01-07 and d3rlpy's last release was 2025-03-02. Even had the data existed, this sub-ecosystem is the least healthy in the matrix.

### 4.4 Behavior trees / utility AI — nothing worth a dependency

`py_trees` 2.5.0 is real and genuinely revived: three releases in eighteen months, a new experimental Ports API, and a BehaviorTree.CPP-style XML parser. It is deterministic, pure Python, and costs only `pydot`. There is no *fitness* objection. **[HIGH]**

The objection is value. `py_trees` supplies *structure* — `Sequence`, `Selector`, `Parallel`, decorators, a blackboard — not *behaviors*. Against our situation that is a poor trade on three counts. First, the engine already has a priority-ordered role selector (`simulation/ai_strategies.py`, with `ARCHETYPE_ROLE_PRIORITY` and a registry-derived fallback) that *is* a hand-rolled selector node; R-WR3-9's "extend the existing intent system" is extending working code, not starting from nothing. Second, a policy with roughly four to six verbs (kite / advance / hold / attack / evade / form-swap) does not have enough branching to amortize a tree framework's ceremony. Third, py_trees imposes its own tick/blackboard model on a simulation that already has a tick model — an impedance mismatch that buys complexity in the exact loop that runs 450 times. Every other Python option in the space (`goap` 2021, `simpleai` 2021, `pygame-ai` 2019, `owyl` 2009) is abandoned. **[HIGH on the facts; MEDIUM on the cost/benefit judgment, which is mine]**

### 4.5 Human-likeness without demonstration data — the literature backs our approach directly

This is the most useful positive finding for the run, because it says the technique R-WR3-9 already assumes is the *established* one.

**Imposed reaction delay is the standard human-likeness lever, and it requires no demonstration data.** DeepMind's Quake III CTF work (Jaderberg et al., arXiv 1807.01281) measured that *"the time between first seeing an opponent and attempting a tag … is much lower for FTW agents (258ms on average) compared to humans (559ms),"* widening to 233 ms vs 627 ms on successful tags, and then handicapped the agents by injecting response delay — reporting that *"an average response time of up to 375ms did not affect the win probability of the FTW agent — only at 448ms did the win rate drop to 85%."* **[HIGH — verbatim from the paper]**

Two things follow for us. (a) Delay-injection as a human-constraint mechanism is validated precedent, not invention — our 0.30 s reaction delay and 0.70 s actionable window are squarely in the tradition. (b) A calibration datum, offered with an explicit caveat: 300 ms sits nearer the *agent* end (258 ms) than the measured human end (559 ms) of that study. The tasks differ — FPS first-sighting-to-tag is not ARPG telegraph-response, and the study's humans were reacting to opponent *appearance* rather than to a deliberately-authored telegraph — so this is not a number to import. It is a reason to hold 0.30 s as a *fast-competent* human rather than a median one, which is arguably exactly what R-WR3-2 asks for. **[MEDIUM on the transfer; HIGH on the underlying figures]**

Supporting current work: Swiechowski & Slezak, *"The Many Challenges of Human-Like Agents in Virtual Game Environments"* (AAMAS-2025, arXiv 2505.20011) surveys thirteen challenges in implementing human-like AI and frames human-likeness as arising from *biological constraints* — sensory resolution, motor smoothness, fatigue, reaction delay — rather than from imitation of recorded play, and notes that agents optimized purely for reward develop behavior that reads as artificial. Lin, *"Playstyle and Artificial Intelligence"* (arXiv 2508.19152) proposes a general playstyle metric over discretized state spaces — potentially a *measurement* instrument for "does this policy play like the referent," though no tooling release was found. **[HIGH for existence/claims; LOW for immediate applicability of the playstyle metric — no code located]**

Neither yields an installable package. Both endorse the mechanism we are already building.

### 4.6 LLM-agent frameworks — landscape unchanged on the axis that decides it

The expected verdict holds and the reason has, if anything, hardened. The 2026 literature is explicit that per-decision inference latency renders LLM agents unsuitable for real-time game control; action games demand frame-level decision speed that LLM inference cannot sustain, and adding visual input degrades rather than helps because it worsens latency. Against a 450-trace battery of tick-resolution combat this is not a marginal cost — it is several orders of magnitude, plus per-call sampling nondeterminism, plus API cost, plus network dependence in a gate path. **Unfit for policy-of-record.** The landscape did not change. **[HIGH]**

The one place LLMs plausibly touch this run is offline and outside the battery: authoring or reviewing policy *rules* in natural language, which is a design-loop use, not a runtime one.

---

## §5 — The one materially-new path the survey surfaced (and why it does not change stage 1)

I am obliged to report a finding that cuts against the simple "no demonstrations, therefore no learning" framing.

**Preference-comparison reward learning needs no demonstrations.** From the `imitation` library's own documentation: trajectory fragments come from a *trajectory generator the algorithm itself controls*, and the human or oracle supplies only pairwise preferences — which of two fragments is better — modeled with Bradley-Terry. No expert action data enters anywhere. **[HIGH — imitation.readthedocs.io/algorithms/preference_comparisons]**

Applied to us, that describes a path Matt is uniquely positioned to walk: render pairs of fight clips, let Matt label *"this one plays more like I did,"* learn a reward capturing the referent playstyle, and train against it. It is the only surveyed route from "no action traces" to "learned policy," and it converts Matt's judgment — which we have — into the training signal, instead of his inputs, which we do not.

**It does not displace stage 1, for four reasons.** The library implementing it is dormant (untouched since 2025-01-07) and its docs concede human preference gathering is not implemented — *"Human preferences could be implemented here in the future"* — so the labeling harness would be ours to build. It presupposes a working env, a working baseline policy to generate fragments, and a render pipeline. It inherits every determinism and artifact-auditability concern from §4.2. And it answers a *calibration* question ("does this look like Matt's play?") that only becomes askable after stage 1 produces geometry worth comparing.

**Recommendation: bank it as a named stage-3 candidate**, not a stage-1 or stage-2 option. Its existence is another argument *for* the Gymnasium adapter, since it is exactly the kind of future path the adapter keeps cheap.

---

## §6 — One implementation amendment (does not alter the ruling)

R-WR3-9 says "built behind a Gymnasium-compatible env interface from day 1." I endorse this and propose sharpening *how*:

**Gymnasium compatibility does not require a Gymnasium dependency.** The `Env` API is a duck-typed protocol — `reset(*, seed, options) -> (obs, info)` and `step(action) -> (obs, reward, terminated, truncated, info)`. The package itself is needed only for `spaces` objects, `gym.make` registration, wrappers, and `check_env`. So:

- The sim core defines the observation/action contract in plain `numpy` + `dataclasses`, shaped to match the spaces we would declare, and exposes `reset`/`step` with the exact signatures. **Zero new dependencies. The 450-trace battery hot path never imports an RL package.**
- A separate thin `GymEnvAdapter` module imports `gymnasium` lazily and declares the `spaces`, gated behind an optional `[rl]` extra in `pyproject.toml`.
- The full RL stack (`torch`, `stable-baselines3`) lands only in that extra, if it ever lands at all.

This is strictly better than a core dependency on every axis the charter cares about: battery speed (no import cost, no torch), determinism (no third-party RNG anywhere near the gate path), auditability (the gate chain stays pure-Python and diffable), and optionality (the adapter is a ~100-line file whenever we want it). If it helps to have the check: `gymnasium` 1.3.0 requires Python `>=3.10` and the engine is `>=3.11` running 3.12, so compatibility is not the constraint — leanness is the reason. **[HIGH on the API facts and the dependency footprint; MEDIUM on the recommendation, which is my engineering judgment and belongs to the seam owner to accept or refuse]**

---

## §7 — Verdict per R-WR3-9

**The ruling is CONFIRMED. No materially better path exists.** Clause by clause:

**"Stage 1's policy core is a DETERMINISTIC utility policy built in-seam, NOT a learned policy."** Confirmed, and over-determined — three independent constraints each close the learned path alone. There is no demonstration data and every offline/imitation library requires action-aligned arrays (§4.3, three primary schemas). The determinism requirement is disclaimed by the leading training framework in its own documentation (§4.2, verbatim). And the whole 450-trace battery would take a dependency on `torch>=2.8` plus a non-diffable weights artifact in the gate chain, which forfeits the property that makes a regression battery a gate. Meanwhile the in-seam path is not greenfield: `ai_strategies.py` already implements a priority-ordered selector, so "extend the intent system" is extension, not invention. Adding verbs genuinely does not need learning.

**"BUT the policy is built behind a Gymnasium-compatible env interface from day 1."** Confirmed and strengthened by a fact the ruling could not have assumed: the Gymnasium API is **frozen by maintainer commitment** since v1.0.0 — *"the end of this road to change the project's central API"* — with seven subsequent releases honoring it and SB3 betting a `<2.0` pin on it. Building to a frozen contract is a much better bet than building to a moving one. There is no successor and none is signalled. The optionality this buys is real: SB3 2.9.0 (2026-06-15) is healthy and current, and the entire matrix consumes this one contract, so the adapter genuinely unlocks the ecosystem at near-zero marginal cost. My only amendment is §6 — get the compatibility without the dependency.

**"…as a competence probe and exploit-finder, not as the policy of record."** Confirmed, and this framing is precisely right: it is the role in which the training stacks' nondeterminism is *harmless*, because an exploit found by a stochastic search is still an exploit, and no gate depends on reproducing the search.

**On Matt's hypothesis specifically.** He was right that packages exist and right to insist we check. What the check establishes is that the available packages sit on the *interface* and *training* layers, and the *behavior* layer is empty by construction — a policy cannot be packaged without packaging the game it plays. R-WR3-9 already draws the line at exactly that seam: take the commodity interface, build the game-specific behavior. **The survey found nothing that would make me recommend revisiting the ruling.**

---

## §8 — Knowledge gaps not resolved

- **PufferLib's determinism posture is undocumented.** Its README and landing page make speed claims without seeding/reproducibility statements; I did not read its source. Immaterial to stage 1 (it is not a candidate), but if throughput ever binds on a probe, this needs a direct source read. **[gap: MEDIUM importance]**
- **The FTW reaction-time figures do not transfer cleanly.** FPS first-sighting-to-tag is a different task from ARPG telegraph-response. I found no study measuring human reaction latency to *authored telegraphs* in ARPG combat. If stage 2 wants to defend 0.30 s numerically rather than by precedent, that measurement does not exist in what I surveyed and would have to be made — plausibly from Matt himself.
- **No tooling located for Lin's playstyle metric** (arXiv 2508.19152). If a "does this policy play like the referent?" *measurement* is wanted at the stage-2 gate, I could not confirm an implementation exists. Worth a follow-on probe if gandalf wants a quantitative playstyle-similarity column.
- **I did not audit `py_trees` 2.5.0's new Ports API in depth.** My rejection is on cost/benefit at our verb count, not on a defect. If the policy's branching grows well past ~10 verbs, the trade should be re-examined rather than treated as settled.
- **Search-negative results are inherently weaker than source-positive ones.** "No ARPG player-policy package exists" rests on PyPI name probes plus web search. The structural argument in §1 is what makes me confident, not the search coverage. Graded **MEDIUM** as a universal claim; **HIGH** for the specific named packages verified dead or absent.

---

## §9 — Source list

**Package registries and repositories (PyPI JSON API, GitHub REST API — all accessed 2026-07-30):**
- Gymnasium 1.3.0 — https://pypi.org/project/gymnasium/ · https://github.com/Farama-Foundation/Gymnasium
- Gymnasium v1.0.0 release notes (API-freeze commitment) — https://github.com/Farama-Foundation/Gymnasium/releases/tag/v1.0.0
- Gymnasium v1.3.0 release notes — https://github.com/Farama-Foundation/Gymnasium/releases/tag/v1.3.0
- Gymnasium Env API reference — https://gymnasium.farama.org/api/env/
- Gymnasium paper — https://arxiv.org/abs/2407.17032
- PettingZoo 1.26.1 — https://pypi.org/project/pettingzoo/
- Shimmy 2.0.1 — https://pypi.org/project/shimmy/
- Stable-Baselines3 2.9.0 — https://pypi.org/project/stable-baselines3/ · https://github.com/DLR-RM/stable-baselines3/releases/tag/v2.9.0
- SB3 reproducibility + algorithms — https://stable-baselines3.readthedocs.io/en/master/guide/algos.html
- sb3-contrib 2.9.0 — https://pypi.org/project/sb3-contrib/
- Ray/RLlib 2.56.1 — https://pypi.org/project/ray/
- TorchRL 0.13.3 — https://pypi.org/project/torchrl/
- CleanRL 1.2.0 — https://pypi.org/project/cleanrl/
- sample-factory 2.1.1 — https://pypi.org/project/sample-factory/
- PufferLib 3.0.0 — https://pypi.org/project/pufferlib/ · https://github.com/PufferAI/PufferLib
- Tianshou 2.0.1 — https://pypi.org/project/tianshou/ · skrl 2.1.0 · AgileRL 2.8.4
- `imitation` 1.0.1 — https://pypi.org/project/imitation/ · https://imitation.readthedocs.io/en/latest/main-concepts/trajectories.html
- `imitation` preference comparisons — https://imitation.readthedocs.io/en/latest/algorithms/preference_comparisons.html
- d3rlpy 2.8.1 — https://d3rlpy.readthedocs.io/en/latest/references/dataset.html
- Minari 0.5.3 — https://minari.farama.org/main/content/dataset_standards/
- py_trees 2.5.0 — https://pypi.org/project/py_trees/ · https://github.com/splintered-reality/py_trees/releases/tag/2.5.0
- Dormant/absent candidates verified via PyPI JSON API: `goap` (2021-10-02), `simpleai` (2021-09-02), `pygame-ai` (2019-06-08), `owyl` (2009-01-16), `gym` (0.26.2, 2022-10-04); `utility-ai`, `pyutilityai`, `pygoap`, `bt-py` — no such packages

**Research literature:**
- Jaderberg et al., *Human-level performance in first-person multiplayer games with population-based deep reinforcement learning* — https://arxiv.org/abs/1807.01281 (reaction-time figures + delay handicap)
- Swiechowski & Slezak, *The Many Challenges of Human-Like Agents in Virtual Game Environments*, AAMAS-2025 — https://arxiv.org/abs/2505.20011
- Lin, *Playstyle and Artificial Intelligence: An Initial Blueprint Through the Lens of Video Games* — https://arxiv.org/abs/2508.19152
- Baker et al., *Video PreTraining (VPT)* — https://arxiv.org/abs/2206.11795 · https://openai.com/index/vpt/
- Chen et al., *CombatVLA: An Efficient Vision-Language-Action Model for Combat Tasks in 3D Action Role-Playing Games* — https://arxiv.org/abs/2503.09527
- *A Survey on Large Language Model-Based Game Agents* — https://arxiv.org/abs/2404.02039 (LLM latency unsuitability for real-time game control)

**Internal (read-only, for integration-cost scoring):**
- `reincarnated-engine/pyproject.toml` — `requires-python >=3.11`; deps `anthropic`, `pydantic`, `numpy`, `pyyaml`, `rich`; local interpreter 3.12.0
- `reincarnated-engine/src/reincarnated/simulation/ai_strategies.py` — existing priority-ordered role selector (`ARCHETYPE_ROLE_PRIORITY`, registry-derived fallback)

---

*Survey complete. — legolas, UNKNOWN-RESEARCHER*
