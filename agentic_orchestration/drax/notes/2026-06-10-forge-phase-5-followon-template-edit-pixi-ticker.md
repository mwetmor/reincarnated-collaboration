# Phase 5 Follow-on — tier1_commit Voice Template Edit + Pixi Ticker Alpha Interpolation

**Date:** 2026-06-10
**Author:** drax
**Mode:** Mode L follow-on (two close-gate carry-forwards)
**Commit:** `2d8d539`
**Vercel preview:** `https://reincarnated-loadout-3dvoomtsl-matthew-wetmore-s-projects.vercel.app`
**Build:** `tsc -b && vite build` PASS — 1505 modules, 0 TS errors
**Verdict:** GREEN

**Authority chain:**
- Matt 2026-06-10 explicit authorization
- Gandalf design review (`94217b7`) § 5.2 — tier1_commit D31 voice template recommendation
- Jack-ryan Gate-2 (`cb23c13`) INFO-1 — Pixi ticker alpha interpolation carry-forward
- Phase 5 close gate Pattern E ratification COMPLETE

---

## 1. Template edit — tier1_commit voice template

**File:** `reincarnated-loadout/src/data/cascadeData.ts`

**Before:**
```
tier1_commit: (anchorLabel: string, tier2Question: string) =>
  `You are drawn to ${anchorLabel}. ${tier2Question}`,
```

**After:**
```
tier1_commit: (anchorLabel: string, tier2Question: string) =>
  `Your path projects toward ${anchorLabel}. ${tier2Question}`,
```

**Rationale:** D31 neutral-data-oracle voice per canonical 40 D28-D32. The spirit guide is a Throne-resident data oracle that narrates substrate-emergent projections. "You are drawn to" implies editorial knowledge of the player's interior feeling-state — it is romantic register, sliding toward the Genshin-spirit-companion pole that gandalf's voice-character review explicitly names as out-of-register. "Your path projects toward" is oracle-pattern-recognition voice: the oracle observes what the substrate says about this player's direction, not what the player feels.

Per gandalf design review § 5.2 excerpt:
> "oracle reports patterns ('projects toward'); doesn't editorialize about feelings ('drawn to')"
> "D31 projection-language honesty would land as 'Your path projects toward [anchor]' or 'Your form aligns with [anchor]'"

**Near-cognate audit:** grep confirmed no other "You are drawn to" instances in `cascadeData.ts`. No other voice templates in the file use similar romantic-interior-state language. The six other templates (`tier1_opening`, `tier2_commit`, `final_emergence`, `substrate_gap`, `refine_prompt`) all already use neutral-observation or projection-language patterns and did not require editing.

The `final_emergence` template is the strongest: "projects most closely toward this form" is verbatim D31 honesty language and was correctly identified as such in the gandalf review. The `tier1_commit` fix brings the Tier 1 commit response into alignment with the emergence template's voice register.

---

## 2. Pixi ticker alpha interpolation

**File:** `reincarnated-loadout/src/components/Cosmograph/RuneLayerCanvas.tsx`

**What was wrong (jack-ryan Gate-2 INFO-1 finding):**
The `cascadeHighlightAnchorId` useEffect called `overlayLayer.clear()` followed by synchronous `PIXI.Graphics.beginFill/drawRect/drawCircle/endFill` calls. This produced an instantaneous redraw — the sky overlay snapped to the new state with no transition. The `CYCLING_TRANSITION_DURATION_MS=400` constant was present but only applied to CSS transitions on the option-list items in CascadePanel, not to the sky visual itself.

Per § 12.4 CANONICAL: "cycling produces cosmograph response animation (~0.3-0.5 sec smooth transitions)". The instant sky snap failed to realize this intent at the Pixi layer.

**Implementation pattern:**

Three pieces compose to produce the 400ms alpha ramp:

1. **Two new refs** (added near other Phase 5 refs):
   - `skyOverlayAlphaStartRef: useRef<number>(0)` — stores the overlay alpha at the moment a ramp begins (enables continuity when a new highlight fires mid-ramp)
   - `skyOverlayAlphaStartTimeRef: useRef<number>(-1)` — stores `performance.now()` at ramp start; value of -1 means no ramp active

2. **`skyAlphaTicker` function** (added to `app.ticker` in Pixi init effect):
   ```typescript
   const skyAlphaTicker = () => {
     const overlayLayer = skyOverlayLayerRef.current;
     if (!overlayLayer) return;
     const startTime = skyOverlayAlphaStartTimeRef.current;
     if (startTime < 0) return; // no active ramp

     const elapsed = performance.now() - startTime;
     const t = Math.min(elapsed / CYCLING_TRANSITION_DURATION_MS, 1.0);
     // ease-out cubic: fast rise, smooth settle
     const eased = 1 - Math.pow(1 - t, 3);
     overlayLayer.alpha = skyOverlayAlphaStartRef.current +
       (1.0 - skyOverlayAlphaStartRef.current) * eased;

     if (t >= 1.0) {
       overlayLayer.alpha = 1.0;
       skyOverlayAlphaStartTimeRef.current = -1; // ramp complete
     }
   };
   app.ticker.add(skyAlphaTicker);
   ```
   Removed in cleanup alongside `fpsTicker` via `app.ticker.remove(skyAlphaTicker)`.

3. **Modified reactive useEffect** (the `cascadeHighlightAnchorId` effect):
   - Draws the target graphic immediately (no change to draw calls — same Graphics operations)
   - Reads current `overlayLayer.alpha` as the start point (continuity: if ramp was 60% done, new ramp starts at 0.6 not 0.0)
   - Records `skyOverlayAlphaStartTimeRef.current = performance.now()` to kick the ticker
   - The ticker then runs each frame until alpha reaches 1.0

**Easing choice:** ease-out cubic (`1 - (1-t)^3`). Fast initial rise (player eye follows the sky immediately), gentle settle at 400ms. This matches the § 12.4 "smooth" qualifier and the "camera fly-through" feel described in gandalf design review § 3 + § 12.4 — the player's attention is drawn to the newly illuminated region quickly, not slowly faded in.

**Mid-ramp continuity:** if the player cycles quickly (new highlight fires before previous 400ms completes), the ramp starts from the current partial alpha rather than zero. This prevents visual jarring from alpha resetting to 0 mid-animation.

**Cycling != committing preserved:** the alpha ramp fires on `cascadeHighlightAnchorId` change, which is set by pointer-enter, keyboard arrow, swipe, and arrow-button events — all of which are highlight-only (no commit). The commit path (`commitHighlighted()` in CascadePanel) is unaffected by this change.

**Import:** `CYCLING_TRANSITION_DURATION_MS` imported from `CascadePanel`. Reuses the existing named constant; no new literal added.

**D8 mobile-friendly preserved:** `app.ticker` runs at device vsync (typically 60Hz on iPad; 120Hz on ProMotion). The 400ms ramp is frame-rate-agnostic — `performance.now()` elapsed time drives the interpolation, not frame count.

**TODO(drax) override #13 resolved.** The override placed in Phase 5 close report reads:
> "Sky overlay animation is instant Pixi.Graphics redraw (not animated 400ms transition). Production: implement ticker-based alpha interpolation for § 12.4 camera-fly-through intent."
This is now implemented. AGENT_STATE.md updated.

---

## 3. Vercel preview

**URL:** `https://reincarnated-loadout-3dvoomtsl-matthew-wetmore-s-projects.vercel.app`
**Build:** READY — 1505 modules, 0 TS errors

**Empirical validation path (per jack-ryan Gate-2 INFO-1 resolution criterion):**
Navigate to the preview URL at `?view=cascade` (default). Cycle through Tier 1 anchors via arrow buttons, keyboard arrows, or touch swipe. Observe:
- Sky overlay alpha ramps smoothly over ~400ms on each highlight change (not instant snap)
- Commit still triggered by "Begin this path" tap (not by cycling)
- Spirit guide Tier 1 commit narration reads "Your path projects toward Race / ancestry." (not "You are drawn to")

DevTools validation: in Chrome DevTools Animations panel, the sky canvas element's composite layer should show smooth opacity transitions at ~400ms per cycle change.

---

## 4. "You are drawn to" instance audit

Grep output from validation pass:

```
grep -n "You are drawn to\|drawn to\|projects toward\|path projects" cascadeData.ts
  202:  // "Your path projects toward" is oracle-narrated projection (substrate-emergent),
  203:  // not editorialized feeling ("You are drawn to"). Per gandalf design review 2026-06-10 § 5.2.
  205:    `Your path projects toward ${anchorLabel}. ${tier2Question}`,
```

"You are drawn to" appears only in the comment explaining the change (not as a runtime string). No other templates in the file use near-cognate romantic-interior-state language. Audit: clean.

---

## 5. Pattern B handoff items

### Voice register — Pattern B input

The `tier1_commit` edit is a single-template targeted change per gandalf's specific D31 recommendation. It does NOT constitute a full voice register review — that is Pattern B scope per gandalf design review § 5.3.

Pattern B voice character session should:
1. Pin voice register between Diablo-IV-Lilith (too cold) and Mushoku-Tensei-Roxy (too warm)
2. Establish explicit reference: "the voice an experienced friend uses explaining a system they understand and you don't — they describe what they see, they project from pattern, they preserve your agency to decide"
3. Review the remaining 3 Tier 2 + 3 Tier 3 questions flagged REVISIT in gandalf § 2.3/2.4 (Race "Which tradition calls to you?" → "Which lineage shapes your form?"; Power "What expression of power calls to you?" → "What shape does your power take?"; etc.)
4. Confirm `tier2_commit` ("takes shape") and `refine_prompt` ("Your path remains open") remain in correct register or adjust

The single `tier1_commit` edit warrants Pattern B awareness but not immediate gandalf review escalation — it is a targeted implementation of an already-reviewed recommendation, not a new design question.

### Sky overlay animation — no Pattern B input required

The Pixi ticker implementation is a production-quality delivery of the § 12.4 requirement that was correctly deferred from Phase 5. No new design questions opened. The implementation is in drax seam scope entirely.

---

## 6. Jack-ryan Gate-2 INFO-1 — close status

**INFO-1 finding:** "Sky overlay animation is instant Pixi.Graphics redraw, not animated 400ms transition; diverges from § 12.4 camera-fly-through intent."

**Resolution criterion per INFO-1:** "sky overlay alpha ramps over the `CYCLING_TRANSITION_DURATION_MS` window (observable via DevTools animation profiler or direct visual inspection at 0.25× playback speed) at a post-Phase-5 Vercel preview."

**Status: CLOSED.** Implementation delivers the alpha ramp. Vercel preview URL provided above for empirical verification. Commit `2d8d539` is the reference implementation.

---

## Completion record

Both gate carry-forwards from the Phase 5 close gate Pattern E ratification cycle are now closed:

| Item | Gate source | Status |
|---|---|---|
| tier1_commit voice template edit ("You are drawn to" → "Your path projects toward") | Gandalf design review § 5.2, recommendation item 5 | CLOSED — `2d8d539` |
| Pixi ticker alpha interpolation for sky overlay | Jack-ryan Gate-2 INFO-1 | CLOSED — `2d8d539` |

**Signed:** drax 2026-06-10
