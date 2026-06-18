# Ruling — Synty Gear-Spec Upstream Wiring (Q2 gates 1 + 2 reconvergence)

**STATUS:** RULING (gandalf design-steward verdict — the all-era-vs-fantasy-first wiring call + axis-3/4 rep-audit curation)
**Date:** 2026-06-17
**Author:** gandalf (story-and-design steward)
**Authority:** the decision envelope of `agentic_orchestration/gandalf/notes/2026-06-17-synty-acquisition-run-ruling.md` § Q2 assigns the wiring call to gandalf; KR reconvergence dispatch routes both gates here.
**Method discipline:** ruled against DISK + substrate (§4.4 semantic-layer rep-audit) — the JSONL substrate (157 rows, 0 nulls, mode-flagged) was read directly, not from the MD prose summary; the LABEL×MODE crosstab was computed, not assumed.
**Closes:** Q2 gate 1 (elrond multi-axis tagging, commit `1995157`) + Q2 gate 2 (galadriel cross-era mask spike, commit `2f24c1d`).
**Companions:**
- `canonical/story/styleprofile-output-shape-ruling-2026-06-17.md` — the §7.6 ruling; `per_region` = the §4.1 palette-remap lever this wiring call scopes.
- `agentic_orchestration/gandalf/notes/2026-06-17-synty-acquisition-run-ruling.md` — the three-gate framing + the consumption-time partition (§4) this builds the genre-half of.
- `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/multiaxis-tags-2026-06-17.{jsonl,md}` — the substrate this curates.
- `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/cross-era-mask-spike-2026-06-17.md` — galadriel's double-collapse this rules on.

---

## 0. The ruling in three lines

1. **Axis-3/4 curation: ACCEPT elrond's partition with TWO semantic-layer corrections** — (a) the Mode-C `cultural_identity` labels are register-genre, NOT culture; relabel the axis or downstream WILL read genre-default as cultural-tradition (the exact §4.4 Mode-C artifact). (b) `modern-western` carries two modes under one label — split it.
2. **Wiring call: FANTASY-FIRST with a documented silhouette-lane degrade path.** galadriel's double-collapse (restyle multiplier AND accent rig both fantasy-Modular-exclusive) makes the bifurcation a substrate fact, not a design preference. The fantasy lane lights the full §3.6 budget; every other era runs the silhouette kit. This is what the additive-nullable StyleProfile (§7.6 ruling) was already built to absorb.
3. **No rig-read hardening needed before the call.** The evidence is already decision-grade; galadriel's optional 5-min Space/Worlds socket-read would harden an inference that does not change the verdict. Decline-with-thanks (see §3).

---

## 1. Axis-3/4 rep-audit curation (closes Q2 gate 1)

### 1.1 The discipline applied — substrate votes geometry, gandalf audits semantic (§4.4)

elrond did exactly the right thing: axes 1+5 substrate-GIVEN (authoritative), axis 2 doc-DERIVED (every pack routes), axes 3+4 substrate-VOTED with name-token basis columns + a `cultural_mode_flag` guarding the A/B/C/D collapse — and flagged them as PROPOSALS, not labels. That is the geometry-layer vote. My job is the semantic-layer audit: does the cluster identity supply the cultural-tradition / time-period semantics a downstream design surface would inherit from it? For most of axis-4 the answer is **no — and the mode flag already says so.**

### 1.2 Axis 3 (time_period) — ACCEPT as-proposed

The 8 strata partition cleanly. The `unresolved` bucket (17) is **correctly** unresolved — I audited every row: 5 ANIMATION (inert rig clips, period-agnostic), 1 INTERFACE-Modern-Menus (ui), 4 weapon-only POLYGON tools (Bow/Crossbow, Bubblegum, 2× Water Guns — period-agnostic tools), 6 SIMPLE-register set-aside packs, 1 Halloween-Masks (seasonal-prop). None of these wants a time-period forced onto it; leaving them unresolved is the honest read. **No relabel. Sign off.**

One note for downstream, not a correction: `renaissance-early-modern` bundling Pirate (age-of-sail) with Samurai (Sengoku feudal-Japan) is a coarse-but-defensible "early-modern" macro-period. They are the same *era-tier*, different *cultural homes* — and axis-4 carries the cultural split (Samurai → east-asian Mode B). The two axes correctly factor era from culture here. Accept.

### 1.3 Axis 4 (cultural_identity) — ACCEPT the Mode-A/B partition; CORRECT the Mode-C/D labels

This is where the semantic-layer audit earns its keep. The LABEL×MODE crosstab (computed from the JSONL, not the MD):

| Label | Mode | n | gandalf semantic verdict |
|---|---|---|---|
| egyptian | A | 1 | **ACCEPT** — real cultural read (geographic-origin, but Egypt-as-culture is unambiguous) |
| east-asian | B | 2 | **ACCEPT** — Samurai = Japanese tradition |
| norse | B | 2 | **ACCEPT** — Viking = Norse tradition |
| greco-roman | B | 1 | **ACCEPT** — Ancient Empire = classical tradition |
| w-euro-medieval | B | 1 | **ACCEPT** — Knights = chivalric tradition |
| modern-western | B | 2 | **ACCEPT as culture** but **SPLIT from the Mode-C homonym** (§1.4) — Western frontier IS a cultural-tradition read |
| generic-fantasy | C | 24 | **RELABEL** — NOT a culture; this is the fantasy *register-default skin* |
| modern-western | C | 30 | **RELABEL** — NOT a culture; apocalypse/city = modern-western *register-default skin* |
| sci-fi | C | 12 | **RELABEL** — NOT a culture; sci-fi *register-default* (acultural by construction) |
| na | D | 8 | **ACCEPT** — nature biomes, no cultural read, correctly null |
| unresolved | ? | 74 | **ACCEPT unresolved** — see §1.5 |

**The load-bearing correction (Mode C, 66 rows):** `generic-fantasy` / `modern-western` / `sci-fi` under Mode-C are **register-genre defaults, not cultural identities.** This is precisely the Mode-C artifact my §4.4 rep-audit discipline exists to catch: a label that passes the name-token vote but fails semantic cultural-coherence. "Dungeon Pack → generic-fantasy" does not mean Dungeon Pack belongs to a *generic-fantasy culture*; it means it carries no culture and defaults to the fantasy register's neutral skin. If a downstream Fate-genre faction-architecture surface or the canonical/48 seasonal-rotation operator inherits `cultural_identity = generic-fantasy` as a *cultural-tradition substrate*, it will manufacture a culture that does not exist — the exact failure the S.-American-Indigenous-Shotgun-Cluster taught us (§4.4 operational instance).

**The correction is NOT a relabel of values — it is a relabel of the AXIS.** The Mode-C rows are correctly tagged as *what register-genre they default to*. The fix is to stop calling that field `cultural_identity` for the Mode-C partition. Two clean ways to land it (elrond's choice of materialization; I rule the intent):

- **Option A (preferred):** rename the *consumed meaning* — `cultural_identity` is authoritative ONLY for Mode A+B rows (the 9 real cultural reads + the 2 modern-western-frontier). For Mode C, the value is `register_default_skin`, not culture; for Mode D, null. Downstream that wants cultural-tradition reads ONLY Mode-A/B rows. The `cultural_mode_flag` is the gate — it is already present and already does this work. **Nothing in the data changes; the consumption rule changes: "cultural_identity is binding iff mode ∈ {A,B}."**
- **Option B:** physically split the column into `cultural_tradition` (Mode A/B only, else null) + `register_default` (the Mode-C genre-skin). Cleaner schema, more migration cost.

I rule **Option A** — the mode flag already partitions it; we add the consumption rule, not a migration. This honors the additive-nullable discipline and avoids a schema churn for a read-time distinction.

### 1.4 The `modern-western` homonym — SPLIT

`modern-western` does double duty: Mode-B (Western Frontier / Western Pack = the *American frontier cultural tradition* — cowboys, a real register with a real cultural read) and Mode-C (Apocalypse / City / Battle Royale = *modern-western-urban default skin*). One label, two meanings, and they are genuinely different design surfaces. **Split the Mode-B rows to `frontier-western`** (cultural-tradition) and let the Mode-C rows keep `modern-western` as the *register-default* sense (which Option A already de-fangs by gating on mode). This prevents a future selector from pulling a cyberpunk-apocalypse city character when it asked for a Western-frontier cultural skin.

### 1.5 The `unresolved` cultural bucket (74) — ACCEPT, do NOT force

74 rows unresolved on culture is the *correct* and honest outcome, not a gap. The overwhelming majority of the catalogue carries no cultural-tradition read because most packs are register-defaults (fantasy/modern/sci-fi neutral skins), environments, weapons, anim, or ui. Forcing a culture onto them would be the pre-imposed-taxonomy failure (Discipline #41). Leaving them unresolved means "this pack has no cultural home" — which is true. The 9 Mode-A/B rows ARE the cultural substrate; everything else is acultural register-fill. **Sign off the unresolved bucket as-is.**

### 1.6 Curated strata sign-off

**Axis 3 (time_period): ACCEPTED as-proposed, all 8 strata + unresolved. No changes.**

**Axis 4 (cultural_identity): ACCEPTED with two corrections:**
1. **Consumption rule (Option A):** `cultural_identity` is binding as cultural-tradition substrate ONLY for `cultural_mode_flag ∈ {A, B}` (**9 rows**, verified against the materialized JSONL at commit `32ba011`: egyptian×1, east-asian×2, norse×2, greco-roman×1, w-euro-medieval×1, frontier-western×2). Mode-C values are `register_default_skin` (genre, not culture); Mode-D is null. Downstream cultural-rotation / faction surfaces read Mode-A/B only. *(Drafting note: this line originally said "11 rows + the 1 remaining" — a prose arithmetic slip; the §1.3 crosstab and the substrate both give 9. Corrected at materialization-verification.)*
2. **Split `modern-western` Mode-B → `frontier-western`** (cultural-tradition); Mode-C rows retain `modern-western` in the register-default sense.

elrond materializes both as an additive consumption-rule note + a 2-row value-split (no schema churn). This is Tier-2 curation, gandalf-owned, now signed.

---

## 2. The all-era-vs-fantasy-first wiring call (the decision the envelope assigns me)

### 2.1 The call: FANTASY-FIRST, with a documented silhouette-lane degrade path

galadriel's spike makes this a substrate fact, not a design preference. **Two load-bearing levers both collapse to the fantasy-Modular lane:**

1. **The per-region restyle multiplier** (§3.6 THIRD lever — "hundreds of distinguishable looks") is fantasy-Modular-exclusive. Every non-fantasy skinned pack (modern/military/sci-fi) ships whole-atlas A/B/C–F palette-swap, NO per-region `_Texture_Mask`.
2. **The `All_NN` accent-socket rig** (§7.2 accent-attachment system) is ALSO fantasy-only. Non-fantasy packs use the UE-Mannequin skeleton with zero named accent sockets — accents ship as standalone skinned meshes mounted by skin-weight, not `BoneAttachment3D`-to-named-socket.

This is exactly the bifurcation my §7.6 ruling was built to absorb. The StyleProfile is already additive-nullable: `mode: per_region | whole_tint`, mesh-derived at bind time, `whole_tint` always present as the degrade target. galadriel's spike does not break that ruling — **it confirms it and extends it one axis.** The §7.6 ruling already said the palette degrades; the spike adds that the *accent system* degrades the same way and needs the same dual-pattern treatment.

**So fantasy-first is not a scoping retreat — it is wiring the system to the shape the substrate actually has.** The fantasy Modular Heroes pack is the one place the full §3.6 budget (per-region restyle + socket accents) renders; we light it up there. Every other era runs the silhouette kit — and per galadriel's nuance (§3 of her spike), the silhouette kit is NOT impoverished: sci-fi ships A–F (6 palettes) + dedicated emissive channels, a glow lever the fantasy whole-tint lane lacks, against deep base-mesh catalogues (40/52/20 distinct sci-fi bodies). Differentiation in the silhouette lane comes from *which body you pick + whole-tint × N + emissive*, not *how you repaint regions*. That is a real, shippable differentiation texture — just a different one.

### 2.2 Why fantasy-first is also the RIGHT design call, not just the substrate-forced one

Three reasons that compose:

- **The locked register IS fantasy-ARPG-core.** Per the acquisition-run ruling §4 consumption-time partition, the design-core consumption set is the POLYGON fantasy/dungeon/nature/character strata — the descent biome is the redundantly-covered spine of a Diablo-class descent. The full restyle budget lands exactly where the season-1 player spends their time. We are lighting the full kit in the lane that matters most for the validated register-2 core.
- **The seasonal-rotation absorbs the degrade gracefully.** canonical/48's rotation is Tolkien-S1 → … → later cultural homes. Season 1 is the fantasy lane (full kit). Later seasons (sci-fi, modern-isekai if they ever fire) run the silhouette kit — and by the time those seasons are real, the additive-nullable degrade path is documented and the emissive lever is in hand. The rotation structure means we never need the full kit in all eras *simultaneously*; we need it in the *current* era, and that is fantasy.
- **It avoids building a port we cannot use yet.** Wiring the accent-socket system to a UE-Mannequin swap-skinned-mesh pattern NOW — for sci-fi/modern eras that are season-N-deferred — is speculative build against deferred need. Fantasy-first defers that second accent pattern to when a non-fantasy season is actually specified, with the substrate finding already on record so it is a known-quantity build, not a surprise.

### 2.3 The degrade path — documented (this is the deliverable, not just the verdict)

The silhouette-lane degrade is already specified by the §7.6 additive-nullable schema. The ONE addition this spike forces, which I record here for rocket §7.2:

> **Accent system dual-pattern (NEW — from galadriel spike §5 finding #2):** §7.2's accent-attachment system as designed against the fantasy `All_NN` socket convention is the **per_region/fantasy pattern**. A SECOND pattern — swap-a-skinned-attachment-mesh on the UE-Mannequin skeleton (no named socket; accent shares the skeleton, mounted by skin-weight) — is the **silhouette/non-fantasy pattern.** §7.2 builds the fantasy pattern NOW (unconditional, per §7.6 ruling §3 — the 17 verified mount points). The silhouette accent pattern is **deferred to first non-fantasy season specification** — NOT built speculatively. The StyleProfile already keys `mode` off mesh-derived mask-presence; the accent system keys its pattern off the same mesh-derived signal (named-socket-present → fantasy pattern; UE-Mannequin-no-socket → silhouette swap-mesh pattern).

### 2.4 Rig-read hardening — DECLINE before the call

galadriel offered an optional 5-min direct socket-read of the Sci-Fi Space + Worlds rigs (she inferred UE-Mannequin + no-socket from recolor-scheme + era-consistency rather than direct read). **Decline before the wiring call.** Reasoning: the verdict does not turn on it. Even if Space/Worlds somehow had sockets (they will not — the recolor-scheme + era-consistency evidence is total, and elrond's independent substrate read corroborates), the wiring call is still fantasy-first, because (a) the *restyle multiplier* collapse is independently confirmed by whole-atlas texture filenames with zero per-region mask, and (b) fantasy-first is the right *design* call (§2.2) regardless of the exact non-fantasy accent mechanism. The hardening would sharpen a deferred-anyway silhouette-accent build, not change the wiring decision. If/when a non-fantasy season is specified and the silhouette accent pattern moves from deferred to active, THAT is when the direct rig-read earns its 5 minutes — fired against real need, not pre-emptively. Recognition-validate-commit (§3.4): the empirical criterion that gates the rig-read is "a non-fantasy season's accent pattern enters active build," not "before the wiring call."

---

## 3. §7.2-honors-§7.6 conformance note

The wiring call does NOT change what rocket §7.2 can assume — it CONFIRMS the §7.6 ruling's assumptions and adds one deferred pattern. Specifically:

- **§7.2 per_region restyle leaf + the 17-mount-point accent system: UNCHANGED.** Both fire unconditionally against the fantasy Modular pack, exactly as the §7.6 ruling §3 specified. galadriel's spike confirms the fantasy lane is real (5-zone mask + `All_NN`+cape sockets verified). The B2 restyle-leaf build (engine `5f85014`, conformance verdict `2026-06-17-gear-spec-b2-restyle-leaf-conformance-verdict.md`) stands.
- **§7.2 gains ONE documented deferral:** the silhouette-lane accent pattern (swap-skinned-mesh on UE-Mannequin) is recorded as a known second pattern, deferred to first non-fantasy season. §7.2 does NOT build it now. This is additive to §7.6, not a reversal — the additive-nullable schema already anticipated the whole-tint palette degrade; this extends the same degrade discipline to the accent axis.
- **No conformance regression.** The wiring call lives entirely inside the additive-nullable envelope the §7.6 ruling locked. rocket §7.2 reads `mode` (mesh-derived) for palette AND now for accent-pattern-selection off the same mesh-derived mask/socket signal. One signal, two consumers, fully consistent.

**Conformance verdict: the wiring call is CONFORMANT with §7.6 and additive-only. No rocket rework. The single addition (accent dual-pattern, silhouette half deferred) is recorded for §7.2's awareness, not for immediate build.**

---

## 4. Authority check — does this exceed gandalf authority?

**No.** Every piece is in-seam:
- Axis-3/4 rep-audit curation: explicitly gandalf-owned Tier-2 (elrond flagged them PROPOSALS for gandalf curation; the dispatch assigns it to me).
- The wiring call: the acquisition-run ruling §Q2 decision envelope assigns it to gandalf; it is a design-seam call about how the locked register consumes the substrate, which is the role-def consumption-time-filter ownership.
- The conformance note: gandalf's §7.2-honors-§7.6 review per endorse-criterion v2 §2.5.

No Matt escalation required. KR holds the push gate (correctly — ADR-006). The consumption-rule materialization (Option A + the modern-western split) routes to elrond as additive Tier-2 catalogue work.

---

## 5. Sign-off

**Recognition → validate → commit honored:** the gear-spec architecture locked 2026-06-16 (recognition); the §4 empirical gate cleared via the two commissions returning (validate — galadriel double-collapse + elrond substrate); this ruling fires the wiring commitment the gate was authored to reconverge at (commit). Not premature, not time-driven — the gated commitment whose gate just resolved.

**What I own next (none blocking):**
- The consumption-rule materialization handoff to elrond (Option A consumption rule + modern-western/frontier-western split) — additive Tier-2, routes through KR.
- The silhouette-lane accent pattern stays deferred; its empirical re-engagement criterion is "first non-fantasy season enters active accent build" — at which point galadriel's rig-read hardening fires against real need.

**Signed:** gandalf, 2026-06-17. Curated strata signed; wiring call rendered; conformance confirmed. Ruling rendered against substrate, not prose — the LABEL×MODE crosstab was computed, and it carried the Mode-C correction the MD summary alone would not have surfaced.
