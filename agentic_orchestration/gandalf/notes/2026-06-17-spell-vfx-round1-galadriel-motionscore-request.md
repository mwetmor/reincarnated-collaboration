# Spell-VFX Round-1 Motion-Score Request — galadriel

**STATUS:** ▶ FIRING — drax Round-1 returned (godot `3b1daa2`). Fields patched; this is live.
**Author:** gandalf (design steward / orchestrator). **Date:** 2026-06-17.
**Parent:** `2026-06-17-spell-vfx-runtogreen-log.md` (tracker + design direction — §2.4 criteria + §3 dual gate are the authority).
**Your descent instruments carry forward as REFERENCE, not as the gate:** the static register-2 scorer (LDR/SHF/warmCool) and the blue-slab flat-panel diagnostic. **The static scorer does NOT fit this — a spell is a VERB; a frozen frame cannot score motion.** You build a NEW instrument here.

---

## 0. Why a new instrument (the core problem)

The descent VFX was carried as "inherited PASS" precisely because a static still cannot score a spell — a frozen-charge frame looks the same whether the spell MOVES or just sits as a glyph. Matt's ask is "MEANINGFUL spell effects" — and meaning is carried by **emanation + motion + element-legibility + combat-intent**, none of which a single frame holds. So the instrument is a **TIME-SEQUENCE scorer**: it reads the strip of frames (charge→release→travel→impact→fade) and measures whether energy is a character-driven cast or a static summon-glyph.

## 1. The captures

- Sequence: `/Users/admin/Games/reincarnated-godot/harness_logs/descent_spellfx_warhall_seq_01.png` … `_07.png` (1152×648, walkable in lifecycle order) — **7 frames**, t = 0.08 / 0.18 / 0.30 / 0.47 / 0.63 / 0.74 / 0.92 (charge → charge-peak → release → mid-travel → impact-onset → impact → fade).
- godot commit: `3b1daa2`. Local + git-ignored (Synty-derivative). Reproduce: `bash scripts/run_spellfx.sh`.
- **gandalf eyes-on (recorded BEFORE your read — do NOT consume until after your independent score):** transformation LANDED (emanation + lifecycle + caster→threat travel all read as a verb). Two convergent residuals already named by drax + gandalf eye: (a) **mid-travel bolt (frames 04–05) reads SOFT** — a fire-bloom, not a crisp shaped/aimed projectile; (b) **directionality** reads as "fire migrates rightward," not a crisp bolt aimed at a specific marquee target. Your metrics 1 (energy-travel), 4 (premium-layering variance), 5 (directionality/principal-axis) are the ones I most need quantified — do they CONFIRM these two residuals (→ targeted Round-2) or refute them (→ converge slice-GREEN)?
- **md5-verify the frames are genuinely DISTINCT** (rule out a stale/identical-frame false read — the descent's "cam1 grabbed six times" bug taught this) before reporting. If frames are byte-identical, that itself is a FAIL signal (no motion) — report it.

## 2. The instrument — five motion-aware metrics (build + report each)

The headline question: **does energy EMANATE FROM THE CASTER AND TRAVEL TO THE THREAT, reading as a fire spell** — or does it sit as a static glyph?

1. **★ Energy-travel (the headline).** Compute the center-of-energy-mass (brightness × saturation centroid) of the spell-mask in EACH frame; track its trajectory across the strip. PASS signature: the centroid TRAVELS from the caster position (early/charge frames) toward the threat / `marquee_local` (late/impact frames). FAIL signature: centroid is static at one ground point (a summon-glyph). Report the per-frame centroid + the net caster→threat displacement.
2. **Inter-frame motion-presence.** Frame-to-frame pixel-delta of the spell region. A real cast has high, PROPAGATING delta (the leading edge advances); a static glyph has near-zero delta. Report mean inter-frame delta + whether the high-delta band MOVES across frames (propagation) vs pulses in place.
3. **Element-hue legibility (fire).** Hue histogram of the spell-mask: fire = high-R, mid-G, low-B (orange/red), consistent across the lifecycle. Report the dominant hue + the fraction of spell-mask pixels in the fire band. FAIL = element-ambiguous mush (no dominant warm hue) or a non-fire cast hue.
4. **Premium-layering (not a flat billboard).** Reuse the blue-slab flat-panel signature, INVERTED: a premium spell has HIGH local-luma-variance (core + glow gradient + particle scatter = layered depth); a flat saturated billboard has LOW local variance (cardboard). Report local-variance of the spell-mask. PASS = layered/high-variance; FAIL = flat-saturated-patch.
5. **Directionality / principal-axis alignment.** The spell-mask's principal axis (PCA/elongation) should align with the caster→threat vector. PASS = the spell POINTS at the enemy; FAIL = a radially-symmetric ground-glow (points nowhere = decoration, not a cast).

**Plus a Gate-B-adjacent backdrop-invariance check:** confirm the chamber backdrop is unchanged frame-to-frame EXCEPT where the spell is (the spell is ADDITIVE; the GREEN-locked rig didn't move). If the backdrop LDR/SHF shifts frame-to-frame outside the spell region, flag it — that would mean the cast perturbed the rig (a Gate-B fail).

## 3. Discipline (carried from the descent run — held four directions)

- **Anti-confirmation-bias:** gandalf records the eyes-on read on §2.4 BEFORE consuming your numbers; you read INDEPENDENTLY; we rule on CONVERGENCE, not either eye alone. Report your read without reference to gandalf's.
- **Dual-gate:** your photometry/motion-measurement OWNS the numbers (authoritative); gandalf OWNS the composition/design ruling (does it read as a meaningful cast). Where they diverge, name the divergence precisely — that's the cross-check working, not a conflict.
- **Name residuals precisely** if it fails: which metric, which frames, how far short — so Round-2 is targeted, not blind.

## 4. Output

1. The motion-score instrument (path + the five-metric logic).
2. Per-metric report: energy-travel trajectory, inter-frame motion-presence, fire-hue legibility, premium-layering variance, directionality alignment + the backdrop-invariance check.
3. Your independent PASS / FAILS read: does the sequence read as a character-driven FIRE spell emanating from the caster to the threat — or does it still read as a static summon-glyph (and which metric exposes it)?
4. One-line verdict + precise residual if it fails.

**The headline gandalf needs:** does energy emanate from the caster and travel to the threat as a legible fire cast (→ converge with my eyes-on → slice GREEN → roll out the element set), or does it still sit as a glyph (→ named residual → drax Round-2).

---

**Signed:** gandalf, 2026-06-17. STAGED Round-1 motion-score — a NEW time-sequence instrument (the static scorer can't score a verb). Five motion-aware metrics, headline = energy-travel caster→threat. Anti-confirmation-bias + dual-gate discipline carried from the descent run. Two fields patch on drax return, then fires.
