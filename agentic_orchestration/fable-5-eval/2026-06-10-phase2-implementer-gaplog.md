# Fable-5 Phase 2 — Implementer Gap-Log

**Implementer:** rocket
**Date:** 2026-06-10
**Spec:** `agentic_orchestration/gandalf/notes/2026-06-10-kit-to-star-sign-assignment-spec.md`
**Protocol:** entries recorded AT THE MOMENT of each decision, not reconstructed afterward. Classes: G1 silent divergence / G2 would-have-asked / G3 ambiguity resolved by re-reading / G4 over-specification.

---

## Entries (chronological)

### GAP-1 — Script location and filename — **G1 (minor, non-load-bearing)**
**Recorded:** before writing any code, immediately after full spec read + input reads.
The spec names the output artifact path (§ 7.1, "the complete, only output") and the configuration-constant structure (§ 5.4 step 0), but never says where the implementation script itself lives or what it is called. The MVP precedent lives at `agentic_orchestration/elrond/scripts/kit_to_star_sign_mvp_assignment.py`.
**Decision:** `agentic_orchestration/rocket/scripts/kit_to_star_sign_injective_assignment.py` — mirrors the MVP's `<agent>/scripts/` convention under my own seam directory (`rocket/scripts/` did not exist; created).
**Load-bearing?** No — script path does not affect output bytes. But it is a real decision the spec did not pre-decide.

### GAP-2 — Test-harness wiring for § 8.1 items 9–10 (synthetic hard-fail runs) — **G1 (minor)**
**Recorded:** during design, before writing code.
§ 5.4 step 0 specifies configuration as *constants* (two repo roots, fixed input/output paths, SALT, anchor table, flag sets). § 8.1 items 9–10 then require running the procedure against a *synthetic* kit list (400 fabricated kit_ids) and a *mutated* anchor table (duplicated sign_id). The spec does not say how the implementation should accept alternate inputs for these tests (CLI flags? module import? copied script?).
**Decision:** structure the script as a parameterized `run(...)` function whose defaults are the § 5.4 step-0 constants; `main()` calls `run()` with defaults; synthetic tests import the module and call `run()` with temp-file inputs / mutated anchor table. This keeps the normative constant-based configuration intact (no CLI surface added) while making items 9–10 executable without editing the script.
**Load-bearing?** No effect on output; affects only test ergonomics.

### GAP-3 — `generated_at_utc` exact timestamp format — **G3 (resolved by re-reading)**
**Recorded:** during design.
§ 7.2 says only `"<ISO-8601 UTC timestamp>"` — ISO-8601 has several valid renderings (Z-suffix vs +00:00 offset, with/without microseconds). On re-read, § 7.2's closing serialization note ("Matches MVP emission so diffs against v1.0 are clean") plus the sanctioned MVP-as-convention-reference resolves it: the MVP uses `datetime.now(timezone.utc).isoformat()` (microseconds + `+00:00`), and the live v1.0 sidecar confirms that rendering.
**Decision:** `datetime.now(timezone.utc).isoformat()`, bit-identical construction to the MVP.

### GAP-4 — E12: `null` vs *missing* denormalization field — **G1 (trivial)**
**Recorded:** while writing the emission code.
E12 says an entry "missing `sign_name.primary` or `cultural_tradition.primary_culture`" emits `""`. It does not say what to do if the key is *present but null* (or empty). The MVP's `.get("primary", "")` would pass a literal `None` through to JSON as `null` in that case; the § 7.2 schema types both fields as `string`.
**Decision:** coerce any falsy value (missing, `None`, `""`) to `""` via `... or ""` — reads "missing" broadly so the output field is always a string per § 7.2. Did not fire on the live corpus (all 37 assigned signs had both fields populated), so zero output impact at current substrate state.

### GAP-5 — § 8.1 item-9 test construction: real anchors trip E8 before E1 — **G1 (minor, test-only)**
**Recorded:** while building the synthetic E1 test.
Item 9 says "run against a synthetic kit list larger than the pool (e.g., 400 fabricated kit_ids) → non-zero exit." But under the § 5.4 normative step order, anchor validation (step 4) precedes the E1 check (step 5): with the *real* anchor table and a fully fabricated kit list, E8 (anchor kit_id ∉ K_all) fires first — non-zero exit, but not via E1, so the test wouldn't actually exercise the E1 path.
**Decision:** the synthetic test injects a 1-row anchor table pointing at a fabricated kit_id (using `run()`'s parameterization, GAP-2) so step 4 passes and E1 is genuinely reached. Verified: `[E1] ... |K_rand| = 399 > n = 393`, exit non-zero, no output written. (Also re-verified at process level: exit code 1, E1 on stderr, output file absent.)
**Load-bearing?** No — test construction only; the production code path is unchanged.

---

## Closing summary

**5 entries: 4× G1 (all minor/trivial, none load-bearing on output bytes), 1× G3, 0× G2, 0× G4.**

No gap forced a judgment call that affects the output artifact's content: GAP-1 (script location) and GAP-2/GAP-5 (test wiring) are packaging/test-ergonomics; GAP-3 was answerable from the spec on re-read; GAP-4 never fired on the live substrate. There was no point where I would have stopped to ask the author (zero G2), and no spec constraint felt wrong or wasteful (zero G4). All § 8.1 checklist items (11/11) passed and all § 8.2 fixture vectors (1–6) reproduced exactly on first run — including the probe tie-break fixture (kit_physical_000016/000028 at base index 90) and the exactly-one-probe-event count.

**Most significant gap:** GAP-5 — the only place where following the spec's own normative step order (§ 5.4) interacts with its acceptance test (§ 8.1 item 9) in a way the spec didn't anticipate: a naïve item-9 test passes for the wrong reason (E8, not E1). Worth a one-line spec amendment ("use a synthetic anchor table whose kit_ids are in the synthetic list") in any future revision; everything else in the spec was implementable verbatim.

**Verdict on spec sufficiency:** effectively sufficient — not a literal G0, but all gaps were peripheral (placement, test harness, null-coercion edge). The algorithm, constraints, validation rules, output schema, and serialization were fully pre-decided and reproduced fixture-exact.

**Signed:** rocket, 2026-06-10

