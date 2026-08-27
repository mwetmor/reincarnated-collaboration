# Research — video→editable-VFX literature (Matt-sourced field survey) — 2026-08-26

**Mode:** A (analytical)
**Commissioner:** gandalf (RUN-CONDUCTOR, VFX-depth run)
**Executor:** legolas (UNKNOWN-RESEARCHER)
**Commission:** `agentic_orchestration/gandalf/vfx-depth-run/research-commission-2026-08-26.md`
**Access date for all web sources:** 2026-08-26

---

## Summary

ParticleGen is the closest structural analogue to our loop and its effect-IR is **specified as an algebra, not as a JSON schema** — the paper names JSON only as a serialization choice and publishes no field list, so we get a *shape* to copy (emitter = ⟨module-sequence, renderer-config, material⟩; edits = typed patches composed onto state) but no literal fields. Its two most transferable mechanisms are the **objective-segmented patch with selective rollback** and **best-state-over-history selection**, and its stated failure mode — *"ungrounded adjustments can accumulate over time"* (§4.3) — is the exact mirror-image of our lap-2 amplitude standstill, which suggests the run's real risk on lap 3 is drift, not timidity, once amplitude is unlocked. Gen-Omnimatte is genuinely runnable (Apache-2.0 public reimplementation, weights on Google Drive, ~1–2 min/layer on an A100) but its **operating resolution is 384×672 or 480×832 and its temporal window 81–85 frames**, and it is an *object-effect* remover trained on shadows/reflections/splashes — nothing in the paper or repo claims separation of emissive particle VFX or UI overlays, so a D4 arena at 1080p60 is out-of-distribution on three axes at once. The MAP-Elites paper is **paywalled and has no OA copy anywhere I could reach**; I recovered the verbatim abstract and the full reference list, which establish the human-as-fitness design and its lineage, but the behavior-descriptor design, population sizes and generation counts are **NOT OBTAINED**. KinemaFX contributes a genuinely reusable idea for a feature-family registry: a **three-attribute kinematic signature (duration / emission shape / emission trail)** measured in spherical coordinates and made searchable by a Hausdorff-plus-rotation-penalty distance. On the field check: **no work in this set does blind differential comparison in our sense** — the two that blind judges (EffectMaker, VFXMaster) blind them for *preference*, not for *structured difference extraction*, and the one that extracts structured difference against a reference (SEIG/"Thinking in Blender") does not blind at all.

---

## Q1 — ParticleGen's effect-IR schema, in full

**Source:** *ParticleGen*, arXiv `2608.00629` (HTML v1), fetched and text-extracted 2026-08-26.

### 1a. The honest headline: there is no published JSON schema

The paper's own words on JSON are the entirety of what it says about JSON (§4.1):

> "We adopt JavaScript Object Notation (JSON) as the intermediate text-based representation for the synthesized particle systems, as LLMs demonstrate high proficiency in generating this format. To bridge the gap between structured representations and the engine's native binary format, we develop a new Unreal Engine plugin, **FxConverter**, that translates JSON outputs into native engine assets."

Term counts over the full extracted body text: `JSON` ×2 (both in the sentence above), `schema` ×4 (all referring to 𝒮⁰, the *planned structure*, not to a serialization schema), `field` ×0, `Appendix` ×0. **There is no example JSON snippet, no field list, and no appendix in the HTML v1.** Any claim that we "have ParticleGen's JSON schema" would be fabrication. What we have is the **algebra the JSON serializes**, which is fully specified — and that is the part worth copying.

### 1b. The representation (§3.1), verbatim

The generative task is `𝒢 : (𝒟, ℳ, 𝒦) → 𝒮` (Eq. 1), where 𝒟 is the natural-language description, ℳ the material library, 𝒦 the technical documentation.

A system is a set of emitters (Eq. 2): `𝒮 = {E₁, E₂, …, Eₙ}`.

Each emitter is a **triplet** (Eq. 3): `Eᵢ = ⟨Φᵢ, ℛᵢ, 𝐦ᵢ⟩`, with the three components defined verbatim as:

> "• **Behavioral Modules (Φᵢ)**: A sequenced set of modules Φᵢ = {ϕ₁, …, ϕₖ} responsible for particle behavior. Each module ϕ is defined by a configuration parameter set θ. These parameters collectively dictate the evolution of the particle state across successive simulation frames.
> • **Renderer Configuration (ℛᵢ)**: The visual output logic, including the renderer type (e.g., Sprite, Ribbon), orientation modes, etc.
> • **Material (𝐦ᵢ ∈ ℳ)**: The material picked from the available library ℳ that best matches the semantic context of Eᵢ."

Two properties of this that matter for us:

- **Φᵢ is an ordered sequence, not a bag.** The module order is load-bearing — the ablation (§4.3) turns on exactly this: *"the Collision module resets particle velocity to zero upon collision. This prevents the velocity threshold required by the Generate Collision Event module from being met and thereby suppresses secondary ripple effects."* An IR that stores modules as an unordered dict cannot express that failure, and therefore cannot express its fix.
- **Material is a *selection from a library*, not a generated asset.** Named as a limitation (§5): *"Creative range is bounded by a predefined material library."* Implementation (§4.1): "21 assets collected from the Fab marketplace, including static geometric primitives, sequential flipbook animations, and procedural materials with time-varying behaviors."

**On "phases" and "curves" (the commission asked specifically):** neither is a first-class IR construct. `curve` appears once, and only as a *value type* the Generator may emit (§3.2): the agent *"maps linguistic cues to precise numerical values, **procedural curves**, or cross-module attribute bindings."* `phase` appears three times, twice describing the pipeline's own two phases and once in a figure caption about temporal display (Fig. 6). **NOT STATED IN SOURCE:** any phase/stage/timeline construct in the IR. Multi-stage behavior is expressed through event modules and module ordering, not a declared phase list. *(This is a real divergence from the run's assumed spec shape and should be a conscious decision, not an inherited one.)*

### 1c. The knowledge base 𝒦 — three parts (§3.1), verbatim

> "1. **Representation Specification (𝒦_spec)**: The syntax and structural constraints governing the text-based representation of the particle system.
> 2. **Framework Summary (𝒦_sum)**: A high-level overview of the particle system framework, encompassing functional summaries of available modules, renderer types, and their global capabilities. This component is utilized to guide macro-architectural decisions during the planning stage.
> 3. **Behavioral Module Documentation (𝒦_doc)**: An indexed knowledge base of detailed parameter specifications."

𝒦_doc is queryable per module: *"for a given module σ, 𝒦_doc(σ) retrieves the technical parameters and physical meanings."* §4.1 states it documents **35 frequently used Niagara modules**.

**The 𝒦_spec/𝒦_sum split is the reusable governance idea**, independent of Niagara: *macro-architectural* decisions read only the summary; *parameterization* reads only the per-module detail, *"thereby reducing contextual noise"* (§3.2). Our spec format wants the same two-tier documentation, or the Godot equivalent (`ParticleProcessMaterial` property groups vs. per-property semantics).

### 1d. Skeletal plan → parameterized system (§3.2)

The Planner emits `𝒮⁰ = 𝒢_plan(𝒟, ℳ, 𝒦_spec, 𝒦_sum)` (Eq. 4), a set of **skeletal** emitters (Eq. 5–6), each a **quadruple**: `Eᵢ⁰ = ⟨𝐦ᵢ, ℛᵢ, Φ̂ᵢ, Ωᵢ⟩`, where `Φ̂ᵢ = (⟨σᵢ,₁, ωᵢ,₁⟩, …, ⟨σᵢ,ₖ, ωᵢ,ₖ⟩)` — σ is a module *identifier* and ω its assigned **functional responsibility**, with Ωᵢ the emitter-level responsibility.

**This is the single most portable idea in the paper for us.** The skeleton carries, for every slot, a natural-language statement of *what that slot is for* — and that intent string survives into the refinement loop, where the Refiner uses it to judge whether a patch segment achieved its purpose. **An IR that stores only values cannot support rollback; an IR that stores (value, intent) can.** Our current spec format records what to set; it does not record what each setting is *for*, which is precisely why a timid parameter and a correct parameter look identical on re-read.

The Generator then instantiates `Eᵢ = ⟨Φᵢ, ℛᵢ, 𝐦ᵢ⟩` with `Φᵢ = (ϕᵢ,₁(θᵢ,₁), …, ϕᵢ,ₖ(θᵢ,ₖ))`, reading only `𝒦_doc|_Φ̂ᵢ` — the documentation restricted to the modules the Planner actually chose. Generators run **in parallel, one per emitter** (§3.1 figure caption).

### 1e. How parameters are exposed for patching (§3.3)

The patch `Δ𝒥ₜ` encodes:

> "atomic operations to add or remove modules ϕ ∈ Φᵢ, as well as to update materials 𝐦ᵢ, renderer configurations ℛᵢ, and parameter sets θ."

applied by a composition operator (Eq. 12): `𝒮ₜ₊₁ = 𝒮ₜ ⊕ Δ𝒥ₜ`, which lets the agent modify *"without necessitating a full system reconstruction."*

So the patch vocabulary is **four operation classes**: add-module, remove-module, replace-material/renderer, set-parameters. A patch is **segmented by objective** — the segmentation is what makes selective rollback possible (below).

Because the full representation is verbose, the Refiner works on a **reconstructed context 𝒞ₜ** rather than the whole system, and uses ReAct to pull more when it is insufficient: *"invokes targeted queries to both 𝒦_doc and the material library ℳ."*

### 1f. Rollback and best-state selection (§3.3), verbatim

> "To ensure robust convergence, the framework implements a **selective rollback** mechanism facilitated by the objective-based structure of the modification patches. At each iteration, the Critic provides comparative visual feedback by identifying which aspects of the simulation have improved or deteriorated relative to the previous state. Based on this feedback, the Refiner assesses the efficacy of each objective-based segment within the prior modification patch Δ𝒥ₜ₋₁. Any segments that failed to achieve their intended visual outcomes are signaled to rollback, allowing the system to revert unsuccessful changes while persisting with effective ones."

> "Recognizing that the refinement process may occasionally diverge or oscillate due to the stochastic nature of the underlying models, the framework preserves the system state 𝒮ₜ from each iteration. Rather than simply returning the final state 𝒮_T, the framework performs a **best-state selection**, outputting the candidate that achieved the highest historical score."

**DRAG (Diagnostic RAG)** is the companion mechanism (§1, §3.3):

> "we use retrieval-augmented generation (RAG) as a diagnostic tool, which we term Diagnostic RAG (DRAG), to trace observed visual artifacts to their underlying procedural causes."
> "This component utilizes a knowledge base that pairs **characteristic visual symptoms with their underlying root causes** within the particle framework. By performing semantic matching between the visual guidance and this symptom-cause library, the Refiner can accurately identify the parameters responsible for non-obvious simulation errors, keeping the refinement process grounded in established troubleshooting logic."

**Termination (§3.3 + §4.1):** loop ends when `sₜ > τ` or `t = T`; *"We use a score threshold of τ = 0.9 and a maximum of T = 4 iterations, which typically strikes a balance between visual quality and inference time."*

### 1g. What the Critic actually scores (§3.3)

Render then criticize (Eq. 9): `Vₜ = Render(Translate(𝒮ₜ))`. Then (Eq. 10):

```
(Gₜ, sₜ) = 𝒢_critic(V₀, 𝒟, ∅)      for t = 0
           𝒢_critic(Vₜ, 𝒟, Vₜ₋₁)    for t > 0
```

> "sₜ ∈ [0,1] represents the semantic alignment between the visual output and 𝒟. The term Gₜ denotes the **visual guidance**, which explicitly identifies mismatches in spatio-temporal dynamics and visual appearance. These observations serve as a qualitative bridge, translating observed visual flaws into actionable suggestions for the Refiner agent."

Two structural facts worth naming plainly:

1. **The Critic's comparand is the TEXT DESCRIPTION 𝒟, never a reference video.** The third argument `Vₜ₋₁` is the agent's *own previous render* — the loop measures self-improvement, not similarity to an external target. This is exactly the hole our run fills.
2. **The Critic is scalar-plus-prose, with no numeric image metric anywhere in the loop.** CLIP4Clip and the VLM rubric appear only in §4.2 as *post-hoc evaluation*, never as loop fitness. **We are ahead of ParticleGen on this axis**: galadriel's P95/P20 luminance lift, mid-band saturation, ownership and optical-flow bars are precisely the numeric loop-fitness that ParticleGen does not have. Note the paper's own §4.1 caveat on why: *"As the model lacks native video understanding capability, each rendered sequence is converted into a compact set of frames."*

### 1h. Evaluation, and the drift finding

Dataset: **75 natural-language descriptions** across combat skill effects, natural phenomena, fireworks. Baselines are ablations only — *"Given the lack of existing generative baselines, we compare our full framework against the Initial generation (serving as the baseline) and single-iteration refinement."*

| Configuration | CLIP4Clip ↑ | VLM semantic ↑ | User semantic ↑ | VLM aesthetics ↑ | User aesthetics ↑ |
|---|---|---|---|---|---|
| Initial Gen. | 0.267 | 3.259 | 3.255 | 3.570 | 3.190 |
| Single-iter. | 0.273 | 3.586 | 3.680 | 3.492 | 3.620 |
| **Full** | **0.281** | **4.200** | **4.420** | **4.043** | **4.400** |

Human study: *"20 professional technical artists. In a **blind** evaluation of 10 randomly sampled effects"* — blind across **conditions of the same system**, with no reference video (see Q5).

⚑ **The finding gandalf should carry into lap 3.** §4.3, verbatim:

> "In early refinement attempts, the Refiner agent may therefore try to compensate by incrementally increasing the spawn rate or scale over multiple iterations. Although each individual modification may be subtle, these **ungrounded adjustments can accumulate over time**. Without rollback, the effects of previous parameter changes remain in the system even after the agent identifies the correct logic fix. These residual adjustments often require additional iterations to correct, and may occasionally remain unresolved. Furthermore, such uncorrected changes increase the complexity of the simulation state, making it more difficult to identify the underlying causes of failure."

Read against our lap-2 diagnosis this is the **same defect wearing the other face**. Ours: every parameter hand-picked timid, structure right, amplitude dead. Theirs: amplitude nudged repeatedly in the *absence of a working structure*, accumulating into an unattributable state. Both are what happens when a parameter change is not tied to a stated objective that can be tested and reverted. The remedy in both directions is the same and is cheap: **carry ω (the intent) alongside θ (the value), and make every amplitude change a revertible, individually-scored segment.** Unlocking amplitude on lap 3 *without* segment-level rollback converts standstill into drift.

### 1i. ParticleGen's own stated future work — the run's thesis, in their words (§5)

> "Another promising direction involves the integration of multimodal inputs, including hand-drawn sketches or **reference video sequences**, to provide more granular control over the generative process. By incorporating visual cues, the framework could better resolve spatial and temporal constraints that natural language descriptions often struggle to specify."

Other limitations (§5): context-window pressure because *"the refinement process necessitates a comprehensive representation of all parameters"*; material-library boundedness; and *"Natural language descriptions are inherently limited in achieving fine-grained control."*

---

## Q2 — Gen-Omnimatte runnability

**Sources:** arXiv `2411.16683` (HTML v1) · project page `gen-omnimatte.github.io` · repo `github.com/gen-omnimatte/gen-omnimatte-public` (README via `gh api`, repo metadata fetched 2026-08-26: 186 stars, 18 forks, **Apache-2.0**, last push 2025-06-03, 7 open issues).

**Paper:** Lee, Lu, Rumbley, Geyer, Huang, Dekel, Cole — *"Generative Omnimatte: Learning to Decompose Video into Layers"*, CVPR 2025 (**Highlight**). Google DeepMind / UMD / Weizmann.

### 2a. Weights: public — but of a *reimplementation*, not the paper's model

The repo leads with this caveat, verbatim:

> "❗ **This is a public reimplementation of Generative Omnimatte.** We applied the same fine-tuning strategy used for the original Casper model (video object-effect removal) to public video diffusion models, CogVideoX and Wan2.1, with minimum modifications. However, ***the performance of these fine-tuned public models is close to, but does not match that of the Lumiere-based Casper***."

The paper's model is Lumiere-based and is **not released**. Three public Casper variants are, as Google Drive `.safetensors`:

| Backbone | Casper weights | Temporal window | Default inference res (H×W) | Reported runtime |
|---|---|---|---|---|
| CogVideoX-Fun-V1.5-5b-InP | Google Drive (full finetune) | 85 frames (197 w/ temporal multidiffusion) | **384×672** | 1–2 min on A100; 4–5 min on A6000/48GB |
| Wan2.1-Fun-1.3B-InP | Google Drive (full finetune) | 81 frames (197 w/ multidiffusion) | **480×832** | ~10 min on A6000/48GB |
| Wan2.1-Fun-14B-InP | Google Drive (LoRA) | 81 frames (197 w/ multidiffusion) | **480×832** | ~55 min on A6000/64GB |

Each also requires the corresponding pretrained inpainting model from `aigc-apps/VideoX-Fun` (HuggingFace).

### 2b. Compute footprint

Inference is the tractable half: **a single 48GB GPU** runs all three variants; CogVideoX is "recommended… better and faster." The **omnimatte optimization** stage is a separate ~8 min/sequence on an A6000/A5000 (48GB), and the README flags that it *"processes a video of multiple objects sequentially rather than in parallel"* — so wall-clock scales with layer count. The Gradio demo runs on an A6000/48GB (~1 min/layer removal with 4 sampling steps, ~8 min/layer omnimatte). Environment: *"python 3.10, CUDA 12.4, torch 2.5.1, diffusers 0.32.2"*, plus SAM2.

**Training is out of reach and irrelevant to us** (*"We finetuned the public models on 4 H100 GPUs"*), but worth naming because the paper's own ablation says the model *"responds well to small additions to the training data"* — i.e. domain adaptation to game VFX is a real but 4×H100-shaped option, not a weekend.

### 2c. Input constraints

- **Camera motion: explicitly supported.** §3: the method *"does not assume a stationary scene or require camera pose or depth information"* — this is the paper's headline delta over prior omnimatte work, which *"assume a static background or accurate pose and depth estimation and produce poor decompositions when these assumptions are violated."* Training data was augmented with *"Ken Burns effects to simulate camera motion."* **Good for us:** D4 footage is a moving/following camera.
- **Masks:** obtained automatically — §3.2: *"We obtain the binary object masks mᵢ using SegmentAnything2."* For custom sequences the README requires *"your own input video, video masks, and text prompt in a folder."* So masks are an input you supply (SAM2-derived), not something the model infers.
- **Trimask conditioning** — §3.2, verbatim, marking *"three regions: the objects to remove (ℳ=0), objects to preserve (ℳ=1), and background areas (ℳ=0.5) that may contain effects to be removed or preserved."* This is the mechanism that decides effect ownership, and it is **the part most directly useful to galadriel** — the gray band is literally "this region *may* contain effects attributable to the removed object," which is the question ownership scoring asks.
- **Length:** 81–85 frames natively; **197 frames** via temporal multidiffusion. At 60fps that is **~1.4 s natively, ~3.3 s stretched** — a single Whirlwind burst, not a fight.
- **Resolution: 384×672 or 480×832.** The original Lumiere pipeline generated 80 frames at 128×128 with a separate spatial-SR stage to 1024×1024 (§3.1); the public reimplementation offers no such SR stage in the documented inference path.

### 2d. Would it separate barbarian + whirlwind from a D4 arena at 1080p60? — **Assessed: no, not as-is.** Four named obstacles.

I am giving an explicit engineering judgment here (flagged as inference, grounded in the quotes above), because that is what the question asks:

1. **Resolution mismatch is the hard wall.** 1080p60 must be downsampled to 384×672 or 480×832. Whirlwind's discriminating detail — thin dust ribbons, edge highlights, the P95 lift band galadriel measures — lives in exactly the high-frequency content that survives that downsample worst. Any layer we recover comes back at ~1/3 linear resolution and would need upsampling before it could be compared to a 1080p render.
2. **Training distribution is object *side-effects*, not emissive VFX.** The limitations section (§5) is explicit that the effect vocabulary is data-bound: *"this reliance on a data-driven prior can also limit the range of effects the method can handle. For example, since we did not include training data capturing physical deformations, our current model does not remove effects such as bending poles or trampolines."* Demonstrated effect classes are *"soft shadows, glossy reflections, splashing water, and more"* — all **passive, physically-caused, attributable-to-a-body** effects. A self-emissive additive-blended particle plume attached to a rotating character is not in that family. **NOT STATED IN SOURCE:** any claim about emissive/particle/magic VFX, and none of the Pexels training clips listed in the README are game footage.
3. **Multi-object confusion is a named failure mode**, verbatim §5: *"We also observed challenging multi-object cases where, despite apparently appropriate training data, our model fails to correctly remove effects. We hypothesize the model may need to be trained with additional information (e.g., instance segmentation) to disambiguate objects and their effects when multiple, very similar objects are present."* A D4 arena is a crowd of similar monsters — the stated worst case.
4. **UI overlays are not addressed at all.** Damage numbers, streamer overlays and nameplates are *composited in screen space and attached to no object in the scene*. Nothing in the omnimatte formulation gives them an owner, so the trimask has no region to assign them to. **NOT STATED IN SOURCE.**

**Where it IS worth galadriel's time (my recommendation, offered as inference for gandalf/galadriel to rule on):** not as a whole-scene decomposer, but as a **background-plate generator on short, tightly-cropped, downsampled clips**. Run Casper with the barbarian as the removed object over a ~1.4 s window; the returned "clean" background is a plausible negative plate, and reference-minus-plate is a cheap effect-region prior for the VFX-owned pixels. That reframes the tool from "separate the effect" (which it was not trained to do) to "remove the character and its shadow" (which it was), and lets the confound subtraction fall out of the difference. It also does nothing about screen-space overlays — those remain a separate, and much easier, template/temporal-stability problem. The honest cost line: no Apple-silicon path is documented (CUDA 12.4 + `sequential_cpu_offload` on the 14B), so this is rented-GPU work, not Mac-resident.

---

## Q3 — MAP-Elites / search-based co-creation of particle systems

**Identification (established via Crossref, the commissioned PII was the only handle given):** PII `S0950584924000715` → DOI `10.1016/j.infsof.2024.107466` → **Jorge Chueca, Carlos Cetina, Óscar Pastor, Jaime Font, "Search-based co-creation of software models: The case of particle systems for video games," *Information and Software Technology* vol. 171, art. 107466, July 2024.** (Confirmed independently via DBLP `journals/infsof/ChuecaCPF24` and Semantic Scholar CorpusId 268995479.)

### 3a. ⚠ ACCESS FAILURE — declared, not papered over

**The full text is paywalled and I could not obtain it.** Routes attempted and their outcomes:

| Route | Result |
|---|---|
| ScienceDirect (commissioned link), WebFetch | HTTP 403 |
| ScienceDirect, direct `curl` w/ browser UA | HTTP 403 (832 KB bot-challenge page; zero occurrences of "particle", "MAP-Elites", "Abstract") |
| SSRN preprint `abstract_id=4615256` | HTTP 403 both via WebFetch and `curl` |
| OpenAlex OA locations | `oa_status: closed`, `any_repository_has_fulltext: false`, no PDF URL |
| Semantic Scholar `openAccessPdf` | `status: CLOSED`, empty URL |
| Unpaywall (via S2 disclaimer) | no OA location |
| `scholar.archive.org`, institutional-repository search | no copy |
| Text-extraction proxy | blocked (network reputation) |

**Therefore: the fitness-function design, the behavior-descriptor / feature-dimension definitions for the MAP-Elites archive, the population sizes, the generation counts, and the evolved particle-parameter space are NOT OBTAINED.** I will not reconstruct them from the abstract; a plausible reconstruction here would be exactly the class of confident-wrong finding this role exists to prevent.

**Route to close the gap, if the run wants it:** the paper is Elsevier Q1 with an SSRN "first look" record that exists but is IP-blocked here — a request from any university-affiliated network, an ILL, or a direct email to the corresponding author (SVIT Research Group, Universidad San Jorge, `svit.usj.es`) would resolve it. This is a Matt-to-do-shaped item, not something Mode A can force.

### 3b. What IS established — the abstract, verbatim

Recovered in full via a Crossref-metadata mirror (`colab.ws/articles/10.1016/j.infsof.2024.107466`), cross-checked against the ScienceDirect search snippet:

> "The video game industry is one of the fastest-growing industries in the world. However, the creation of content is the bottleneck of the industry nowadays. In this paper, we propose a new approach for co-creating content by means of combining an evolutionary algorithm Map-Elites, and software models. Our approach involves generating a large number of software models and selecting the best ones based on a fitness function. **This fitness function is guided by the human, who chooses which content fits their interests best.** We evaluated this approach in the domain of Particle Systems (PS). PS are a popular type of content used to create visual effects such as explosions, fire, smoke, or rain. Our evaluation also involves industry experts of different roles in the video game development process. Using our approach, they were tasked to create PS for their games. Then, they compared the generated models with handmade ones. Our results show that **practitioners chose the generated models four out of five times over handmade ones** as a better fit for their projects. Furthermore, **models created with our approach by non-experts in five minutes are similar in quality to the ones hand-made by an expert in 15 min.** In conclusion, using human artistic taste to guide the algorithm renders positive results in creative tasks such as content generation for video games. With minor adjustments, the generated content can be game-ready, accelerating development."

Four things this settles without the full text:

- **The fitness function is the human.** Not a proxy metric with a human tiebreak — the abstract makes selection itself the fitness signal. This is a *different architecture* from what the run is contemplating (galadriel's CV bars as fitness with Matt at a taste gate), and the distinction is worth making explicit before lap 3 borrows the name "MAP-Elites."
- **The unit evolved is a software MODEL, not a pixel buffer.** The whole point of the paper's framing is that the archive contains editable engine-side artifacts. That is our situation exactly (Godot `ParticleProcessMaterial` parameter vectors), and it is the reason this paper is the right citation even without its internals.
- **The reported win is a time-to-quality collapse** (non-expert/5 min ≈ expert/15 min), not a quality ceiling raise. Applied to us: search-based sweeps are a defense against *timid hand-picking by a non-specialist*, which is precisely the lap-2 failure. That is an argument for the method that survives the paywall.
- **The comparison design is generated-vs-handmade, judged by practitioners.** Whether that judgment was blinded is **NOT STATED IN THE ABSTRACT** — see Q5.

### 3c. Reference list (recovered via Crossref, 38 entries) — the design lineage

Since the method internals are unreachable, the citations are the next best evidence of what the design is made of. The load-bearing ones:

- **[12] Mouret & Clune 2015** — the canonical MAP-Elites ("Illuminating search spaces by mapping elites"). The BC-archive formulation the paper inherits.
- **[23] Hastings, Guha & Stanley 2008, "Interactive evolution of particle systems for computer graphics and animation," *IEEE TEC*** — ⚑ **the direct ancestor and the one substitute source I would actually recommend the run read.** It is the prior art for human-in-the-loop evolution of *particle systems specifically*, it predates the paywall problem, and it is where the interactive-selection machinery comes from.
- **[24] Hastings et al. 2009, "Automatic content generation in the Galactic Arms Race video game"** — the same lineage shipped in a game.
- **[29] Pérez, Font, Arcega, Cetina 2021, "Empowering the human as the fitness function in search-based model-driven engineering," *IEEE TSE*** — the same lab's own statement of the human-as-fitness architecture; almost certainly where the fitness design in this paper is defined by reference.
- **[19] Lai et al. 2022, "On mixed-initiative content creation for video games," *IEEE ToG*** · **[20][21] Charity et al., "Baba is Y'all" 1.0/2.0** — the mixed-initiative framing.
- **[10] Blasco, Font, Zito, Cetina 2021, "An evolutionary approach for generating software models: The case of Kromaia," *JSS*** — the same group's evolutionary-model-generation predecessor (open copies circulate).
- **[36][37] Kontio, Krueger — focus-group method** · **[38] Wohlin et al., experimentation in SE** — confirms the evaluation is a **focus-group / practitioner-study design**, which further suggests the human-selection injection is protocol-level, not algorithmic.
- **[16] Reeves 1983** — the founding particle-systems paper.

**Inference, flagged as such:** the presence of [29] and [27][28] (Kessentini's interactive metamodel co-evolution) alongside [12] strongly implies the human's role is *replacing or weighting the fitness evaluation over archive cells*, with MAP-Elites supplying the diversity that makes a human-scannable menu possible. I did not verify this and it should not be cited as a finding.

---

## Q4 — KinemaFX

**Sources:** arXiv `2507.19782` (abs + HTML v1). Yifei Zhang, Lin-Ping Yuan, Yuheng Zhao, Jielin Feng, Siming Chen — *"KinemaFX: A Kinematic-Driven Interactive System for Particle Effect Exploration and Customization."* **Venue note:** ParticleGen's bibliography places it at **UIST 2025** (*"Proceedings of the 38th Annual ACM Symposium on User Interface Software and Technology, pp. 1–17"*) — an HCI paper, not a graphics one, which explains its shape.

### 4a. What the decomposition is

The paper proposes *"a conceptual model of particle effects that captures both semantic features and kinematic behaviors,"* formalized as **`R = (S, K)`** (Eq. 1) — S a semantic embedding, K a kinematic encoding.

- **Semantic (S):** natural-language description capturing *"the intended meaning and stylistic qualities"* — colour, emotional tone, texture. Standardized via GPT-4o-mini into embeddings (§4.3.2).
- **Kinematic (K):** motion abstracted as *"dynamic changes of primitive shapes,"* on **three attributes** (§4.3.1):
  - **Duration** — *"the time from when a particle effect appears until it completely disappears."*
  - **Emission shape** — one of **three primitives: circle, cylinder, sphere**, parameterized by radius and height. `shape = (s, r, h)`.
  - **Emission trail** — *"the temporal transformation of the shape over time."* `trail = {(Δrᵢ, Δθᵢ, Δϕᵢ)}ᵢ₌₁..N`, spherical-coordinate deltas, **N = 8 temporal steps**.

The three-primitive reduction is empirically justified: a formative study over **839 particle effects** found *"97.4% demonstrated axial symmetry"* (§3.3).

### 4b. What it buys — measurability

The purchase is that **kinematics become a metric space**. Particles are sampled at *"the outer boundary of the initial shape"*, converted to spherical coordinates with the axis of symmetry aligned to the polar axis, so the coordinate deltas decompose cleanly into **translation (r·cos θ), rotation (ϕ), and scaling (r·sin θ)**. Distance (Eq. 5) is **Hausdorff distance for shape dissimilarity plus a rotation penalty**, summed over the 8 steps; total distance (Eq. 4) is a **user-weighted sum of semantic and kinematic distance**, `R* = argmin D(Rc, T(Rᵢ))`, minimized over transformations T (translate/rotate/scale/retime).

Because distance is defined, two interaction modes fall out (§4.2):
- **Local exploration** — top-K retrieval; the user's pick is an implicit preference signal.
- **Directional exploration** — *"interpret the direction of change between two effects as the user's preferred exploration direction,"* then extrapolate kinematically along that vector while the LLM generates matching semantic variations.

Database: **839 individual effects composing 147 artworks**, from the Unity Asset Store and professional studios. Evaluation: within-subjects, **16 non-experts**, four counterbalanced conditions (semantic-only baseline / preference-guided only / kinematic-driven only / full), 15-item questionnaire over 7 dimensions, repeated-measures ANOVA + Friedman with Bonferroni correction (§5.1).

**Its limitation is structural and named by ParticleGen** (§1): *"its retrieval-based formulation constrains the output space to a predefined effect database. As a result, it has limited ability to create novel effects or represent complex procedural dependencies beyond simple temporal sequencing."* KinemaFX finds you an effect; it does not synthesize one.

### 4c. Reusable for our feature-family registry — yes, one specific thing

**Recommendation (inference, flagged):** adopt the **kinematic signature** — `(duration, emission-shape primitive + params, N-step trail of spherical deltas)` — as a **normalized motion descriptor on feature-family registry entries**. Three concrete reasons it fits our run:

1. **It is a small fixed-width vector, so it is directly usable as a MAP-Elites behavior descriptor** — which is exactly the artifact Q3's paywall denied us. Duration and trail-magnitude are natural BC axes; shape primitive is a natural categorical cell. If lap 3 wants a QD sweep and needs BCs today, this is a published, defensible source for them.
2. **Whirlwind is the ideal case for it.** The effect is axisymmetric about the character's vertical axis — squarely inside the 97.4% majority the primitive reduction was built for. Cylinder primitive, rotation-dominant trail: the descriptor is nearly a closed-form description of the thing we are building.
3. **"Rotation penalty" is a measurement we do not currently have.** Our CV bars measure luminance, saturation, ownership and flow; none of them separately scores *rotational character*. A Whirlwind whose flow field is turbulent-but-not-rotational can pass optical-flow magnitude while being wrong, and KinemaFX gives a principled place to put that check.

**NOT STATED IN SOURCE:** any method for extracting the kinematic signature from *video*. KinemaFX extracts it from *simulation sampling* of existing effect assets it already owns (§4.3.2) — reference-side extraction from footage is our problem, not one it solved.

---

## Q5 — Field check: does ANY work do blind differential comparison?

**Definition I am testing against** (the run's, restated so the negative is falsifiable): *a judge, blinded to build lineage, compares a reference video against a candidate render and returns a **structured difference** that feeds a spec revision.* Three conjuncts: (a) reference-vs-candidate, (b) judge blinded to provenance, (c) output is structured difference driving the next build — not a preference vote.

| Work | (a) ref-vs-candidate? | (b) judge blinded? | (c) structured diff → spec? | Verdict |
|---|---|---|---|---|
| **ParticleGen** (§3.3, §4.2) | **No** — Critic compares render to *text* 𝒟 and to its *own previous render* Vₜ₋₁ | Partly — 20 technical artists, *"blind evaluation of 10 randomly sampled effects"*, blinded across **conditions of one system** | **Yes** — `Gₜ` *"explicitly identifies mismatches in spatio-temporal dynamics and visual appearance"* → objective-segmented patch | **(b)+(c), never (a)** |
| **SEIG / "Thinking in Blender"** (arXiv 2606.02580) | **Yes** — *"a verifier compares the rendered image against the reference"* (single **image**, not video) | **No** — verifier is a VLM inside the loop with full provenance | **Yes** — *"an explicit approval checklist: a concrete, actionable todo list of visual discrepancies that is injected into the generator context for the next attempt"* | **(a)+(c), never (b)** |
| **EffectMaker** (arXiv 2603.06014, App. A) | **Yes** — *"participants were shown side-by-side video results… along with the effect class name and a reference video"*; criteria include *"Reference alignment: how closely the result resembles the reference video"* | **Yes** — *"display order in each question was randomly shuffled"*; 30 participants, 28 questions | **No** — preference/rating only | **(a)+(b), never (c)** |
| **VFXMaster** (arXiv 2510.25772, §4.5) | **Yes** — 2AFC, *"a reference VFX video alongside a pair of generated videos"* | **Yes** (2AFC, one-of-each) — explicit shuffling **NOT STATED IN SOURCE** | **No** — forced-choice preference only | **(a)+(b), never (c)** |
| **KinemaFX** (§5.1) | No — retrieval from a database against user intent | Counterbalanced 4-condition within-subjects ablation | No | no |
| **Gen-Omnimatte** | n/a — decomposition, not authoring | n/a | n/a | n/a |
| **Grounded-VideoLLM** (Findings EMNLP 2025, pp. 959–975) | Temporal grounding benchmark; no candidate render exists | n/a | n/a | n/a |
| **Chueca et al. 2024** | Generated-vs-handmade, practitioner-judged | **NOT STATED IN ABSTRACT**; full text unreachable (§3a) | No — selection, not diff | **unresolved** |
| **VEFX-Bench** (arXiv 2604.16272) — *outside the named set, checked because a negative claim demands it* | Yes — *"jointly processes the source video, the editing instruction, and the edited video"* | *"does not specify whether human annotators were blinded"* | No — scores IF/RQ/EE; pixel-space editing, not parametric authoring | no |

### The ruling, stated plainly

**No work in this field — among the nine commissioned sources or in their immediate citation trail — performs blind differential comparison as this run defines it.** The three conjuncts each appear, and they appear in *every pairing of two*, but nothing in the surveyed literature holds all three at once.

The gap is not accidental; it follows from where each community stands:

- **Generative-video work (EffectMaker, VFXMaster)** has (a) and (b) because it must — a reference-transfer method is *evaluated* against its reference, and preference studies are blinded as a matter of routine hygiene. But its output is pixels, so there is no spec for a structured diff to revise. Blinding is a **publication-integrity** device there, applied once at the end.
- **Agentic-authoring work (ParticleGen, SEIG)** has (c) because the loop needs machine-actionable feedback, and gets (a) or (b) but never both: ParticleGen never had a reference to compare to (its own §5 future work asks for one), and SEIG has a reference but its verifier is an in-loop component with no reason to be blinded.

**Our run's differentiator, stated for the ledger:** we use blinding as a **measurement instrument inside the development loop** rather than as an evaluation ritual at the end of it — the seats are quarantined from build lineage precisely so their structured diff cannot be contaminated by knowledge of what we changed. That combination is, on this evidence, unpublished. The nearest neighbour in the literature is **ParticleGen's `Gₜ` visual guidance**, which is our structured diff with the reference video swapped out for a text prompt — and ParticleGen names swapping it back in as future work.

⚑ **One honest qualifier before anyone leans on this.** The claim is bounded by the survey: nine commissioned sources plus their immediate citation trail, arXiv/CVPR/ACL/Elsevier-indexed venues. Blind A/B against reference footage is **standard practice in game-studio VFX review** and would not necessarily be published; absence from the literature is not absence from the world. What is defensible is the narrower and still useful statement: **no published method we can find has automated it as a loop component**, and one of the field's strongest papers explicitly lists it as work not yet done.

---

## Knowledge gaps not resolved

1. **ParticleGen's literal JSON field names** — not in the paper; no supplementary material or code linked in HTML v1; `FxConverter` is not released. *Next source:* author correspondence, or the AAAI/proceedings supplementary if it appears post-camera-ready.
2. **Chueca et al. 2024 method internals** (fitness, BCs, population, generations) — paywalled, no OA copy on any route tried (§3a). *Next source:* institutional access / ILL / SVIT group at Universidad San Jorge. *Substitute available now:* Hastings et al. 2008 (IEEE TEC), the paper's own cited ancestor for interactive evolution of particle systems.
3. **Gen-Omnimatte on emissive VFX** — no evidence either way; the effect vocabulary in paper, repo and project page is uniformly passive object side-effects. *Next step is empirical, not bibliographic:* one rented-GPU trial on a downsampled 1.4 s Whirlwind clip would settle it faster than more reading.
4. **VFXMaster user-study randomization** — 2AFC with 50 participants confirmed; explicit order-shuffling **NOT STATED IN SOURCE** (unlike EffectMaker, which states it).
5. **Grounded-VideoLLM code/weights** — the ACL Anthology landing page carries no code or checkpoint link. Not pursued further; priority 5 and no consumer identified in the commission.
6. **KinemaFX video-side extraction** — does not exist in the paper; signatures come from simulating owned assets. Reference-side extraction from footage remains an open problem for galadriel either way.

---

## Source list

| # | Source | URL | Access | Notes |
|---|---|---|---|---|
| 1 | ParticleGen (arXiv 2608.00629, HTML v1) | https://arxiv.org/html/2608.00629v1 | ✅ full text | Primary. Text-extracted for exhaustive term search |
| 2 | Generative Omnimatte, CVPR 2025 poster | https://cvpr.thecvf.com/virtual/2025/poster/34367 | ✅ | Title/authors/abstract |
| 3 | Generative Omnimatte (arXiv 2411.16683, HTML v1) | https://arxiv.org/html/2411.16683v1 | ✅ full text | §3.1/§3.2 impl details, limitations verbatim |
| 4 | Gen-Omnimatte project page | https://gen-omnimatte.github.io/ | ✅ | Trimask definition, limitations |
| 5 | gen-omnimatte-public repo (README + metadata) | https://github.com/gen-omnimatte/gen-omnimatte-public | ✅ via `gh api` | Apache-2.0, 186★, weights table, runtimes |
| 6 | Chueca, Cetina, Pastor, Font 2024, *Inf. Softw. Technol.* 171:107466 | https://doi.org/10.1016/j.infsof.2024.107466 | ❌ **paywalled** | Identified via Crossref from PII `S0950584924000715`; abstract + 38-entry reference list recovered |
| 6b | — SSRN preprint record | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4615256 | ❌ 403 | Exists; IP-blocked |
| 6c | — abstract mirror (Crossref-derived) | https://colab.ws/articles/10.1016/j.infsof.2024.107466 | ✅ | Verbatim abstract |
| 7 | KinemaFX (arXiv 2507.19782, abs + HTML v1) | https://arxiv.org/html/2507.19782v1 | ✅ full text | UIST 2025 per ParticleGen bibliography |
| 8 | Thinking in Blender / SEIG (arXiv 2606.02580) | https://arxiv.org/html/2606.02580v1 | ✅ full text | Staged pipeline, verifier checklist, round budgets |
| 9 | Grounded-VideoLLM, Findings of EMNLP 2025 | https://aclanthology.org/2025.findings-emnlp.50/ | ✅ abstract | Priority 5; no in-run consumer identified |
| 10 | EffectMaker — CVPR 2026 openaccess page | https://openaccess.thecvf.com/content/CVPR2026/html/Yang_EffectMaker_... | ❌ 403 | Routed around |
| 10b | — EffectMaker (arXiv 2603.06014, HTML v1) | https://arxiv.org/html/2603.06014v1 | ✅ full text | Metrics + Appendix A user study |
| 10c | — EffectMaker project page | https://effectmaker.github.io/ | ✅ | EffectData 130k/3k; code "Coming Soon" |
| 11 | VFXMaster project page | https://libaolu312.github.io/VFXMaster/ | ✅ | |
| 11b | — VFXMaster (arXiv 2510.25772, HTML v1) | https://arxiv.org/html/2510.25772v1 | ✅ full text | §4.5 2AFC study |
| 12 | VEFX-Bench (arXiv 2604.16272) — *citation-trail, outside commission* | https://arxiv.org/html/2604.16272v2 | ✅ | Checked to harden the Q5 negative |
| 13 | Crossref API — journal 0950-5849 + DOI record | https://api.crossref.org/works/10.1016/j.infsof.2024.107466 | ✅ | PII→DOI resolution; 38 references |
| 14 | DBLP author record, Jorge Chueca | https://dblp.org/search/publ/api?q=author:Jorge_Chueca: | ✅ | Independent confirmation |
| 15 | OpenAlex + Semantic Scholar OA checks | api.openalex.org / api.semanticscholar.org | ✅ | Both report CLOSED, no OA location |

---

**Mode-A boundary note.** Everything above the "Recommendation"/"Inference" flags is source-anchored and quoted. Four passages are analytical inference and are labelled at point of use: the Q1h drift↔standstill reading, the Q2d feasibility assessment and background-plate suggestion, the Q3c lineage inference, and the Q4c registry recommendation. The run's blind seats (X-5/X-6) were not contacted and this note was not routed to them.
