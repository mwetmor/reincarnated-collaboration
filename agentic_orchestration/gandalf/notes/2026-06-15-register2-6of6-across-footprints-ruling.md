# Ruling — register-2 holds across all 6 footprints (6/6), MET + scoped; the placeholder-VFX tension resolves toward DENSITY

**Type:** design ruling (gandalf seam) — the canon call galadriel handed off after the 6/6 re-score.
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-conduit 2026-06-15 (Pattern-B) — relayed galadriel's re-score + Drax's flagged tension; *"handoff to gandalf for the canon call."*
**Evidence input (load-bearing, not the ruling):** galadriel re-score verdict 2026-06-15 — corpus 0/6 → **6/6 PASS**, mean composite ≈ **3.875**, both mandatory gates (lighting ≥4 AND VFX ≥4) clear in every room.
**Parent:**
- `agentic_orchestration/gandalf/notes/2026-06-15-godot-register2-a-holds-ruling.md` — A holds (register-2 on cheap Synty + lift). THIS ruling is the across-footprints extension of A-holds; the §4 scope-exclusion discipline is inherited.
- `agentic_orchestration/gandalf/notes/2026-06-15-drax-brief-bake-to-scene-and-open-arena-camera.md` — the brief whose Change-2 (camera) + Change-3 (placeholder decouple) this validates and corrects.
- **Drax flag** (`render_arena_room.gd:49`, verbatim): *"galadriel's 6/6 register-2 PASS was scored on circle-ON captures — the circle's emissive ramp (SIGIL_CHARGE=7.0) is a load-bearing HLF/bloom source. Before any FUTURE re-capture with this flag false, the durable body-anchored skill-cast VFX must carry that HLF, else VFX/bloom regresses corpus-wide. (drax flag to gandalf/galadriel — unresolved design tension.)"* — THIS ruling resolves it.

---

## 0. The ruling, in one line

**The design claim "one spec-driven room holds register across every footprint" is MET, 6/6 — scoped.** The parametric ArenaRoom thesis (one spec-driven scene, geometry + camera + lighting + lifecycle, holds register-2 across all six footprints) is validated. BUT the VFX-axis pass on the large footprints is currently **placeholder-assisted**: the 6/6 was scored with the ritual-circle decal ON, whose `SIGIL_CHARGE=7.0` emissive ramp is a load-bearing peak-bloom source. So the honest claim is **"register-2 is REACHABLE across all footprints"** — the durable VFX carrier is still owed, and it is **combat VFX DENSITY at the live-combat milestone**, NOT the placeholder disc and NOT an oversized hero bloom.

## 1. Evidence (galadriel's scorecard — I interpret, I do not re-derive)

| Room | HLF now | L | V | M | G | Composite | Gate |
|---|---|---|---|---|---|---|---|
| boss_with_adds | 2.62× | 4 | 4 | 4 | 4 | 4.00 | PASS |
| elite_pack | 2.71× | 4 | 4 | 4 | 4 | 4.00 | PASS |
| mini_boss | 2.03× | 4 | 4 | 4 | 4 | 4.00 | PASS |
| magic_pack | 1.97× | 4 | 4 | 3 | 4 | 3.75 | PASS |
| chokepoint | 1.12× | 4 | 4 | 3 | 4 | 3.75 | PASS |
| open_arena | 1.04× | 4 | 4 | 3 | 4 | 3.75 | PASS (first time) |

- **open_arena clears both gates for the first time** — the Change-2 camera fix did exactly what it was scoped to (3.50 FAIL → 3.75 PASS; the 50×50 all-swarm room now frames the engagement band and anchors bloom on the swarm cluster, not room-center).
- **galadriel's honest caveat (load-bearing for this ruling):** open_arena (1.04×) and chokepoint (1.12×) clear the VFX gate on **manual peak-frame prominence**, not raw HLF — their highlight fractions sit BELOW the other four rooms' carrying band (1.97–2.71×). Four rooms pass on instrument-and-eye agreement; two pass on the eye carrying a footprint-diluted proxy. Stated so 6/6 is not over-read.

## 2. The placeholder tension Drax surfaced — RESOLVED (the core of this ruling)

**What happened (timeline):** Drax implemented the Change-3 decouple — durable hero-VFX (`SummonGlow` OmniLight + `SummonFireColumn` = `FX_Fire_Large_01` + charge→erupt→collapse lifecycle) made **unconditional**; the ritual-circle ground decal (`HeroSummonSigil`) gated behind `USE_RITUAL_CIRCLE_PLACEHOLDER`, **default false**. He then ran the decoupled (circle-OFF) capture → **VFX regressed across all 6 rooms** → restored the circle to get the 6/6 → and committed the file with the flag **false** + a loud warning, flagging the tension to gandalf/galadriel rather than silently keeping the placeholder.

**My Change-3 error, owned precisely:** I asserted the decal was *"HLF-neutral since it's low-luminance dark-red emissive."* That read its **idle** ember state (`SIGIL_EMBER = 0.9`). The rubric is **lifecycle-sampled** and scores the **peak** frame — and at the erupt peak the decal's emission ramps to `SIGIL_CHARGE = 7.0`, a big flat bright ground disc that is a **load-bearing peak-bloom source**, not neutral. I evaluated the wrong frame of the lifecycle. The empirical re-score caught it. (Third substantive call this session corrected by an empirical gate — rogue role-floor sufficiency, and now this — the gate-discipline earning its keep; the machine working, not failing.)

**Drax's handling was model-correct** and I am affirming it: (a) he implemented the decouple as briefed; (b) he ran the falsifying capture; (c) he committed the **design-intent default** (circle off — Matt: not sensible in a generic battle room) with a **loud flagged gap** rather than letting a passing-but-nonsensical state become the silent default. Loud-gap-over-silent-pass is the anti-drift move (§7). **Keep the flag false.**

## 3. The unification — the placeholder, the footprint-dilution, and A-holds' 14.4% are ONE phenomenon

The three facts collapse into one:

1. **A-holds** scored `FX_Fire_Large_01` body-anchored at **HLF 14.4%** (9.6× over) — in a **tight single-figure** frame where the bloom filled the view.
2. **The 6-room build** scales that same effect DOWN (`0.55×0.7×0.55`) and frames the whole **arena footprint** (open_arena 50×50, camera pulled back) → the same bloom subtends far fewer pixels → HLF dilutes below the gate.
3. **The ritual disc masked it** — a big flat bright disc at `SIGIL_CHARGE=7.0` covers many pixels at peak regardless of footprint, brute-forcing HLF up.

→ **Single-bloom HLF dilutes as the framed footprint grows; the placeholder disc was compensating by raw pixel coverage.** The "placeholder is load-bearing" finding and the "open_arena/chokepoint pass on eye not instrument" caveat are the **same** under-instrumentation, seen from two sides. Remove the disc and the dilution is simply *exposed*, not *created*.

## 4. The durable carrier is combat VFX DENSITY (not a bigger bloom, not the disc)

The genre truth from the A-holds ruling itself (§3): premium feel ≈ lighting + VFX, and D2/Hades/Torchlight/Last Epoch carry the "screen is alive" read through **density of transient effects**, not one persistent bloom. A static tableau has exactly **one** animated VFX source (the hero) — which is *why* it leans on the disc. A **live fight** fills a large footprint with distributed highlights: multiple combatants casting, hits landing, **the perception-asymmetry AOE telegraphs rendering** (gamora brief), deaths, ambient fire. Total HLF rises across the whole footprint with **no** single oversized bloom and **no** ritual disc.

**This is the cross-thread convergence:** the **live-combat milestone** — flagged in the heading_rad ruling as where entities initialize state from spec, and the subject of the queued gamora perception-asymmetry wiring — is the **same** milestone that (a) lets the placeholder come out for good and (b) resolves the large-footprint dilution. The summoning circle is a **stand-in for the combat VFX density that does not exist yet because the room is a static tableau.** When the room is a live fight, both problems dissolve together.

## 5. Near-term cheap lever (de-risk before live combat) — ambient density

Circle-OFF-and-still-pass on the two diluting rooms does **not** require waiting for live combat OR oversizing the hero bloom. The cheap lever is **ambient VFX density**: more braziers / embers / ground-fire distributed across the large footprints (`_build_braziers` already emits `FX_Fire_Medium_01` at the perimeter — extend its count/spread on big rooms). This raises total HLF by **distributed** coverage, which is exactly the right shape (it previews the live-combat density), and it **aligns with Matt's own observation** that the rooms "need much more ambient objects." Ambient density is the bridge between circle-ON-placeholder-pass now and live-combat-density-pass later.

## 6. Scope — what 6/6 claims and what it does NOT (parallel to A-holds §4)

**6/6 CLAIMS:** the parametric ArenaRoom thesis holds — one spec-driven scene reaches register-2 across all six encounter footprints (geometry legible, camera framing per-footprint, lighting drama, lifecycle bloom). The cross-footprint generalization of A-holds is **validated**.

**6/6 does NOT claim (each a separate, named gate):**
1. **That the VFX axis is carried by durable production VFX.** On the large footprints the VFX-axis pass is currently **placeholder-assisted** (circle-ON). "Register-2 REACHABLE across footprints" is proven; "register-2 achieved with the durable carrier (density / body-anchored, circle-OUT)" is the owed follow-on, gated per §4–§5.
2. **That the HLF instrument and the eye agree on every room.** Two of six pass on eye-not-instrument; the absolute-fraction metric is footprint-sensitive (§8).
3. **That this is a live combat loop.** Static deterministic captures of a fight-start tableau. Live, sim-driven, multi-form combat is a separate integration milestone — and the one that closes both #1 and #2.

These scope it; they do not weaken it. The claim asked — *does one spec-driven room hold register across every footprint?* — is **yes, measured, 6/6.**

## 7. Discipline-#13 guard — do NOT let HLF lobby for the placeholder (or for an oversized bloom)

The implicit-pillar-drift risk here is concrete and empirical: the HLF instrument **rewards the nonsensical placeholder** (a flat bright disc maximizes pixel-fraction-at-peak) over the sensible durable VFX (a body-anchored bloom sized to read as the character's own power — A-holds: hot core inside the silhouette). Two anti-patterns to refuse:

- **Keeping the circle to pass HLF** — it is not sensible in a chokepoint corridor (Matt); passing a proxy is not the pillar, looking like a genre-credible fight is.
- **Oversizing the hero bloom to game HLF** — inflating the body-anchored fire into a disc-equivalent fights the design the same way; the bloom should read as *power*, not as instrument-bait.

When the proxy (HLF) and the design (sensible per-room VFX, real combat density) diverge, **the design wins and the proxy evolves** (§8). The register rubric is a proxy *for* "looks like a genre-credible ARPG fight"; it must not silently become the pillar in its place.

## 8. Rubric-evolution candidate (galadriel's instrument — flagged, not prescribed)

HLF as an **absolute pixel-fraction** is footprint-sensitive: it under-credits a prominent-but-small bloom in a large frame and over-credits a flat bright disc. A **footprint-normalized** or **bloom-prominence-relative** VFX metric would (a) make instrument and eye agree on the two rooms they currently don't, and (b) stop rewarding the disc. The exact metric is galadriel's instrument to design; I flag the candidate and the two acceptance properties it should satisfy.

## 9. Routing / what this fires

- **gandalf:** this ruling is the canon call (claim MET 6/6, scoped; placeholder tension resolved toward density; keep flag false). My Change-3 idle-vs-peak error owned (§2).
- **drax:** flag-false default **affirmed**. Near-term de-risk path = **ambient density** on the diluting rooms (§5), OR a clearly-labeled "placeholder-assisted (circle-ON)" capture until the durable carrier lands — galadriel + drax coordinate which. The durable removal is terminal at live-combat (§4); the placeholder block is *deleted, not re-flagged*, when real skill-cast VFX lands (drax's own comment at `_build_hero_vfx`).
- **galadriel:** the footprint-normalized VFX metric is the rubric-evolution candidate (§8); the current 6/6 scorecard is durable evidence with the §1 caveat preserved.
- **gamora (queued):** the perception-asymmetry AOE telegraphs are not only a balance-sim fix — when they render in live combat they are a **distributed VFX density** contributor (§4). Cross-thread, not a new dispatch.
- **Not firing any dispatch unprompted** — near-term levers (drax ambient-density; galadriel rubric) are routable when Matt wants them; the terminal carrier rides the already-named live-combat milestone.

---

**Signed:** gandalf, 2026-06-15
**For:** ruling the parametric ArenaRoom claim "one spec-driven room holds register across every footprint" **MET, 6/6** and honestly scoped — the across-footprints extension of A-holds is validated, but the VFX-axis pass on the large footprints is currently **placeholder-assisted** (the ritual disc's `SIGIL_CHARGE=7.0` ramp is a load-bearing peak-bloom that my Change-3 brief wrongly called HLF-neutral, reading idle not peak on a lifecycle-sampled rubric); the placeholder-load-bearing finding, the open_arena/chokepoint footprint-dilution caveat, and A-holds' tight-frame 14.4% are ONE phenomenon (single-bloom HLF dilutes as footprint grows, the disc masked it); the durable carrier is **combat VFX density at the live-combat milestone** (where the gamora telegraphs render and the circle deletes for good), bridged near-term by **ambient density** (aligning with Matt's "need more ambient objects"); keep Drax's flag-false default (loud-gap-over-silent-pass = anti-drift), refuse to let HLF lobby for the placeholder or an oversized bloom (Discipline #13), and flag a footprint-normalized VFX metric as galadriel's rubric-evolution candidate.
