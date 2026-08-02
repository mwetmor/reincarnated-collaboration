# BR-1 + BR-2 wind-down — pointers, not prose

**Conductor:** gandalf (`RUN-CONDUCTOR`). **Closed:** 2026-08-02. Read this, then expand only what you need.

## The two runs

| Run | Charter | Outcome |
|---|---|---|
| **BR-1 BATON-RENDER** | `gandalf/notes/2026-07-31-baton-render-run-charter.md` | Lap-1 watch: fully-rendered fight in the crypt corner. Lap 2 parked (G-5 open-gate: rider traces never materialised). |
| **BR-2 TRUE-SHAPE** | `gandalf/notes/2026-08-01-br2-true-shape-run-charter.md` — **Addenda 1–24 are the run's whole record** | Watch shipped with HUD + SFX. Rulings **R-BR-1 … R-BR-57**. |

## The deliverable

`~/Games/reincarnated-godot/tmp/br2watch/BR2W.mp4` — seed **74000909**, 1600×900, 1211 frames / 40.367 s,
h264 + aac, sha256 `ea61b0ee3469d8e0`. Godot HEAD `978a423`, **local only, never pushed**.
Prior cut `BR2W-cell7.mp4`. Engine stamp `16fa7e8d`; traces read-only `tmp/wr3acc/traces/`.

## Where to expand (charter §, not the whole file)

- **What the run learned about its own instrument** → Addenda **16, 17, 18, 19**. The three
  non-determinism terms; **N3 unidentified**, up to 2,305 lit px from ~frame 100. Addendum 19 is the
  blast-radius triage (Class A/B clean · **Class C re-derivation owed** · one Class D).
- **Matt's owner-eye passes** → Addenda **20, 22, 23, 24**. Six rulings, then four, then one.
- **Cell notes** → `drax/notes/2026-08-01-arc-clear.md` · `…-hud-ref.md` (item table + gate line).
- **Reference art Matt supplied** → `gandalf/notes/br2-hud-refs/`.

## The rules this run minted that outlive it

`R-BR-51` instrument must assert determinism · `R-BR-53` a presence gate states its noise floor at the
frames the verdict is taken · `R-BR-54` a visual reference governs frame/layout/ornament/palette, **never
copy** · `R-BR-55` commit per item · `R-BR-56` promote a render only after ffprobe verifies it ·
`R-BR-57` **the split cell** — agent edits, conductor renders (13 tool calls vs 129–278).

**Pattern-doc amendment queued:** `operating-procedures/desirable-run-pattern.md` §6 — R-BR-57, plus §6-obs-2
now evidenced **twice** (two gates passed while failing; both caught by Matt's eye, neither by a gate:
the G-14 presence clauses via the noise floor, and G-5d via a soot **prefab** the burn-shader gate never saw).
jack-ryan ratification per `canonical-doc-format.md § 6.7`.

## BR-3 inherits, in this order

1. **Identify and close N3** — ahead of any pixel-differential work.
2. **Re-derive Addendum 19 Class C**; resolve G-14a's Class D with one look.
3. **Design call, not a cell fix:** both dedicated melee read-channels are now closed (rime crust, slash
   arc — Addendum 23 §last). What carries *committing to a swing* and *locked* when neither may be an
   overlay? Lean: timing + silhouette + the hitstop the audio now exists to punctuate.
4. Unlit-candle asset (the flame **was** the candle) · no 2D bat-skull / skull-pip sprite · shell
   green/blue double-sRGB half · `shape` vs `geometry` naming hazard · G-2a separable-radius ·
   F-CJ-2/3/5 · engine test baseline (10,024 pass / 60 fail / 21 err) → knight-rider ·
   room-size vs CAM-LOCK, undecided.

**Signed:** gandalf, 2026-08-02.
