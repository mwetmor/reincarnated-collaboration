# TCP-L3 — MURZAK STANDUP (run charter)

**Program:** `2026-07-24-tool-capability-program-charter.md` — lap **L3**, class **standup**
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executor:** drax (presentation seam) · **Status:** CHARTERED + DISPATCHED 2026-07-24
**Matt gate:** none remaining. Q45 ruled self-hosted; mechanism `stdio` (TCP-11); Custom mode needs no
credential; blast radius pinned by TCP-18. **One residual Matt trigger:** any step demanding `sudo` or
a machine-wide install — that is a HALT, not a judgment call.

---

## §0 — Intent, in one sentence

**Can `IvanMurzak/Godot-MCP` (W-MUR) actually stand up self-hosted on this machine — and does the wire
behave as its manifest claims?** Secondarily: **measure the asset route for L4** so the next lap
launches informed instead of surprised.

**Rubric diff against §0 (law L-I — name what falls out, out loud).** This lap says **nothing** about
whether Murzak is *good* at anything. Not authoring quality, not iteration speed, not design arrival,
not whether `Godot-AI-CSG` builds a decent blockout. It answers **readiness + live surface + one
behavioural proof.** Do not let a PASS here be read as *"Murzak is a strong authoring tool"* — that is
L4/L5/L7's question and this lap is deliberately incapable of answering it. It is the cheap lap that
makes the expensive ones interpretable.

## §1 — Why standup is its own lap

Three reasons, and the third is the one that earns the time:

1. **Two laps gate on it.** L4 (T2 expansion, three-way) and L5 (T4-UI) both need W-MUR present. A
   standup failure discovered *inside* L4 contaminates a comparative lap; discovered here it costs
   one cheap lap and reshapes the field honestly.
2. **The toolchain prerequisites are a genuine unknown, and the audit missed them.** Recon
   2026-07-24: **no `dotnet` SDK exists on this machine at all**, and **no Godot .NET editor build** —
   only `/Applications/Godot.app`, standard 4.6.3. Murzak is a C# addon. The audit read a tool list
   and never asked whether the runtime under it exists. That is the manifest-vs-reality gap (**L-B**)
   one level below the tools.
3. **L-B says the manifest is the WIRE, not the docs — and I violated that law myself, one level up,
   four days ago.** I read Pro's `docs/tools-reference.md`, counted **77 tools**, called it the
   manifest, and wrote a program law about a structural gap (`no gridmap`) that did not exist. The
   server exposes **175**, including `add_gridmap`, `batch_add_nodes` and a whole recording family.
   **So this lap does not read Murzak's README and report a number. It enumerates the live wire.**

## §2 — Environment (TCP-17 / TCP-18)

**Everything lands in `~/Games/mcp-lab/`.** Not in `reincarnated-godot`, not in any product repo.

- **Not a clone.** TCP-17 originally said "scratch clone"; recon falsified its own premise —
  `reincarnated-godot` is **2.67 MiB tracked against 18 GB on disk**, the whole Synty tree gitignored
  under the license rule, so a clone is scripts with no assets. **And a standup lap needs no assets.**
  Use a **fresh minimal .NET Godot project.**
- **.NET SDK:** user-local via `dotnet-install.sh --install-dir` inside the lab dir. **No `sudo`. No
  system-wide install. No PATH edit outside the lap's own shell.** Removal must be `rm -rf`.
- **Godot .NET editor:** side-by-side in the lab dir. **`/Applications/Godot.app` is never touched,
  replaced or upgraded** — it is the standing product editor and it stays 4.6.3 standard. Match the
  .NET build's version to it if you can; if you cannot, **record the version skew as a finding**, it
  matters for L4.
- **Transport:** `stdio` (TCP-11). Self-hosted, nothing of ours transits a third party.
- **Route-finding is yours.** I am not specifying install commands I have not verified. Read the
  repo's own README and NuGet instructions; the *constraints* above are the charter, the *route* is
  your call.

## §3 — Pre-registered predictions (pinned before results; the lap cannot move its own goalposts)

- **P-A — the user-local .NET install works without `sudo`.** *Medium-high confidence.* If it does
  not, that is a **HALT**, not a workaround.
- **P-B — DECISIVE. The live manifest disagrees with the documentation.** I predict a delta **in both
  directions** — tools present that no doc lists, and documented tools absent or differently shaped.
  My audit said **39 tools / 11 families**; treat that number as an unverified prior, not a target.
  **Record the exact live count and the exact tool names**, dumped to a file. This is the single most
  load-bearing artifact the lap produces, because every later Murzak lap is planned against it.
- **P-C — the `Godot-AI-*` extension packages are NOT installed by the core addon.** They are ten
  separate source-only NuGet packages. If `Godot-AI-GridMap`, `Godot-AI-CSG` and `Godot-AI-Particles`
  are **absent from the live manifest after a default install**, then the three capabilities that
  reopened this entire column are gated behind extra per-package steps — and L4/L5/L7 must budget for
  them. **Resolve this explicitly. Do not infer it from the README.**
- **P-D — a sub-agent cannot wire an MCP server into its own running session.** `godot-cli setup-mcp
  claude-code` (or equivalent) writes a client config that the session must **restart** to pick up.
  If that holds, **L3 terminates with a verified-ready environment plus a written launch procedure,
  not with L4-capable tool access in this session** — and that is a correct outcome, not a shortfall.
  **Record whether a path around it exists** (e.g. `claude mcp add` then a fresh sub-session), because
  it determines how L4 gets launched and by whom.
- **P-E — asset route for L4 (a measurement, not a prediction).** Symlink **one** Synty pack from
  `~/Games/reincarnated-godot/Assets/` into the lab project and **time the import.** Report minutes,
  whether refs resolve, and whether the standard project's `.godot/` import cache is reusable or must
  be rebuilt. **Do not import the whole 18 GB tree.** One pack. This is the cheap probe that tells L4
  whether a sibling .NET project is viable or whether we are looking at a Matt-gated conversion.

**Every prediction resolves to a recorded fact. A FAIL is a finding, not a terminal event** (law
**L-G** — ceiling-finding is a PASS; only an *unattributed* failure fails).

## §4 — Blast radius and its verification predicate (TCP-18)

The five constraints are the charter, not advice:

1. Everything in `~/Games/mcp-lab/`.
2. `/Applications/Godot.app` untouched.
3. `dotnet` user-local, no `sudo`, no machine-wide install.
4. **`reincarnated-godot` ends the lap byte-unmodified — verified by a clean `git status` INCLUDING
   untracked files**, not by "I didn't mean to touch it." The symlink probe in P-E reads *out* of that
   tree; nothing is written *into* it.
5. **The uninstall procedure is written down** as part of the deliverable — exact paths, exact
   commands. A lab that cannot be removed is not a lab.

**Why the verification is spelled out rather than assumed:** L2's restore was verified three times and
still missed two residues (Pro rewrites `project.godot`'s `[autoload]`; addon removal silently empties
the global class-name cache). **Byte-perfect belief is not byte-perfect verification.** Check it.

**The one anticipated GUI moment — Gatekeeper.** A `.app` downloaded via `curl` carries
`com.apple.quarantine`, and macOS may refuse to launch it. Two things make this a drax problem rather
than a Matt problem: we run Godot **headless from the CLI**, and `xattr -dr com.apple.quarantine
<path>` clears it on a user-owned file **without `sudo`**. Do that; do not ask Matt to click through
System Settings. **If Gatekeeper still hard-blocks after the xattr clear, that is a HALT to gandalf** —
it is the one place in this lap where a human hand at the machine may genuinely be required, and I
want to see the exact refusal before anyone's afternoon is spent on it.

## §5 — Exit predicate

The lap is done when **all six** hold:

1. **The live manifest, enumerated over the wire**, dumped to a file with exact count and exact tool
   names. Not the README's number. Not the docs' number. **The wire's.** (L-B)
2. **One behavioural proof, verified independently of the tool's own return value.** Use Murzak to
   create something in a scratch scene — a node, a CSG box, whatever the live manifest actually
   offers — then **read the `.tscn` from disk by other means** (shell, Python, the standard editor)
   and confirm it is there and correct. **A return code of `ok` proves nothing in this stack**
   (**L-K**: M2's transpose passed a complete structural inspection; `custom_aabb` returns a field
   shaped exactly like the answer and identically zero with `ok=true`; Pro's own round-trip reported
   255/255 ok and wrote nothing to disk). **Five instances, three instruments, one detector: pixels
   and independent reads.**
3. **One judgeable frame** — render the scratch scene Murzak authored. L-A does not formally bind a
   standup lap (the subject is a wire, not the presentation layer), but the frame costs minutes, this
   stack lies, and a picture is the only instrument that has ever caught it. Ship the picture.
4. **P-A..P-E each resolved** to a recorded fact, with the evidence that resolved it.
5. **A launch procedure for L4** — written as steps another agent or Matt can execute, including
   whatever P-D turned out to require.
6. **Blast radius verified** per §4, and the **uninstall procedure written**.

**Honorable fallback (law L-F — a control or a trace):** if Murzak cannot be stood up at all, the lap
ships **the attributed failure point with the exact blocking artifact** — error text, missing package,
version conflict, verbatim. That is not a wasted lap: *"W-MUR is not standable on this machine under
these constraints"* collapses the field to **W-PRO vs H**, makes L4 a two-way, and is worth knowing
before L4 rather than during it. **An unattributed failure is the only real failure.**

## §6 — Conductor interface

- **In-run rulings (drax may take, logged, veto-open):** install route and package versions; which
  scratch scene to author; which pack to symlink for P-E; version skew between the .NET editor and
  4.6.3 **if recorded as a finding**; substitutions declared as substitutions.
- **HALT to gandalf:** any step demanding `sudo` or a machine-wide install (§4.3 / TCP-18); any need
  to write into `reincarnated-godot` or any product repo; a manifest that disagrees with the docs in a
  way that changes what L4–L7 can even attempt (that is an **L-B** event and it is worth more than the
  lap); P-E revealing that assets are unusable outside the live project (that reopens the .NET
  conversion question, which is **Matt's**, not mine).
- **HALT to Matt:** nothing anticipated. The one live trigger is the `sudo` case, and it routes
  through me first.

**Report to:** `agentic_orchestration/drax/notes/2026-07-24-tcp-l3-murzak-standup-run-report.md`

---

**Signed:** gandalf, 2026-07-24 (`RUN-CONDUCTOR`). Two consecutive laps have had charter defects found
by the executor and **reported rather than worked around** — L1's unsatisfiable I7 camera invariant and
its conflated clamp/clip numbers, L2's I7 recurrence escalated for a ruling instead of a third
workaround. That is the behaviour I want again. **This charter has already had one defect found before
dispatch — its own scratch-clone premise, falsified by five minutes of recon.** Assume there are more.
If something here cannot be satisfied, say so and ship the trace anyway.
