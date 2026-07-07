# Gate-1 request — rocket: B1-REBASE Phase 1 v3 re-fire — two DoF resolutions + gen-path legs 2-3 scoping

**Filed by:** rocket, 2026-07-07 (arc-close batch, Items 1+2).
**Critique pair:** jack-ryan (DESIGN-MODE technical) + gandalf (design — the A3-energy pick is a fantasy/economy designation).
**Math note under review:** `reincarnated-engine/src/reincarnated/generation/math/proxy-t4-b1-rebase-phase1-v3-refire-2026-07-07.md` (engine `a5adcf1`).
**Governing spec:** `canonical/reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` **v3**.

## Why Gate-1 (not just Gate-2)

Two of the deliverables are **design/cross-seam DoF picks that must be ratified BEFORE code lands** (math-before-code). No code has landed on either — the note is the before-code artifact. This request queues the two picks.

## What is ALREADY DONE (no Gate needed — verification + tag)

- **B1-REBASE Phase 1 is v3-conformant at HEAD** (Disc #11): landed at `40e351e` (= `rocket/v-proxy-t4-rebase-strategies-1`, ancestor of HEAD), 169 tests green across the T4 surface + eval. Re-fire = confirm, NOT rebuild (rebuild = parallel regen of a frozen cert surface, Disc #3).
- **Anchor tag dropped:** `rocket/v-proxy-t4-rebase-phase1-v3-confirmed-1` @ `0e9fc91`. This is gamora's proxy-T4 sim-eval EXTENSION unblocking event (her `proxy-t4-suite-rebase-eval-extension-2026-07-07.md` §7 lists 4 items ALL keyed on this tag).

## The two DoF picks for Gate-1 (note §2, §3)

### DoF-A — A3 energy-designation (note §2) — **gandalf's design call**

gamora's eval hard-codes `_A3_ENERGY="charge_stack"` to open SOVEREIGNTY for the A3 fixture. Two problems: (1) `charge_stack` is NOT a valid `energy_type` (vocab = {mana,rage,focus,stamina}; charge_stack is a substrate *family*); (2) the demo summoner cell is INT ranged/medium → `energy_type="mana"` by pipeline economy (`season_generation_pipeline.py:255`) → SOVEREIGNTY gate CLOSED → **A3 FAILS** (both fixtures top FISSION).

- **R-A1 (recommend):** re-designate the demo summoner fixtures `energy_type="focus"` (valid token, non-mana; death-magic soul/attention reading) → opens SOVEREIGNTY, A3 passes unconditionally, gamora READS it from the landed fixture (removes her eval-side assumption). One additive field on `DemoSummonerSpec`, zero magnitude touch. **Departs from the cell's default INT→mana — a content designation, so gandalf ratifies.**
- **R-A2:** keep mana; separate A3 on the count axis (bone count-2→ASCENSION vs a count-1-full→FISSION); SOVEREIGNTY not demoed by this pair.

### DoF-B — F-f GEOMETRY max-1 enforcement (note §3) — disposition confirm

Consumer `enforce_family_max_one` EXISTS (`t4_catalog_v2.py:159-215`, W0) but UNWIRED. The collision (ZONE_CONTROL + GEOMETRY_COLLAPSE) is **structurally unreachable pre-B4** (pipeline doesn't multi-select GEOMETRY members yet). **Disposition R-B1:** live-wiring is B4-scoped (rides the `select_proxy_t4`→emission wiring that makes it reachable); wiring now = inert-guard churn (Disc #12). gamora keeps her eval-side invariant for now (her §3 sub-case 2). Named in MIGRATION for B4. **Confirm this disposition** (vs. requiring a pre-B4 wire).

## Gen-path legs 2-3 (Item 1) — scoping for a KR dispatch (note §5a)

Leg-1 LANDED + live. **Leg 2 = route summoner kits through `select_proxy_t4` so `primary_t4` carries a ratified proxy-family member** (`select_primary_t4:1831` is hard-coded ALWAYS-DDA = the v1 bug spec v3 §1 names). **Leg 3 = emission run.** Leg 2 is cross-seam (star-lord must widen the DDA-lock emitter validator per sim `MIGRATION:8371`) → **KR owes a co-dispatch (rocket emit-route ∥ star-lord validator-widen) + its own Gate-1.** Not fired blind this session (no dispatch, cross-seam cert path, frozen surface).

## Guards

Kit-side chassis FROZEN; bars/bands FIXED; zero chassis/bar/band/magnitude touch; zero production code (math note + one verification tag only). Auto-committed; NOT pushed (Matt-gated).
