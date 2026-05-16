# Working Agreement — This Folder

## Purpose

This folder is a workspace for **collaborative discussion** between the project owner (and his son, indirectly) and a Claude session. It is not an implementation workspace.

## Rules for any Claude session opened against this folder

1. **No code changes** in any working repo (`reincarnated-engine` or anywhere else). Discussion only. Note: design docs live in `engine-repo/design/` as a subdirectory; the same no-edit rule applies there.
2. **Markdown notes and design docs may be freely written within this folder** — that is part of the discussion. Drafting proposed changes here is encouraged; executing them is not.
3. Recommendations for code or doc changes in other repos should be drafted as proposals here, not executed directly. When implementation is needed, end the discussion session and start a new session in the appropriate repo.
4. **No exploration of working repos for editing.** Read-only reference of files in other repos is allowed only when needed to ground a discussion (e.g., quoting a current file to evaluate a proposal). Even then, prefer to ask the user to paste the relevant content rather than reaching into another repo.

## Why this separation matters

Architecture, design, and scope decisions deserve deliberate consideration without the gravity of in-progress code edits pulling toward premature execution. Separating the "discuss and decide" workspace from the "implement" workspace keeps both honest. It also matches how the original handoff was set up: this folder was created specifically as the bridge between conversation and action.

## Established

2026-05-08, by project owner. Applies to this and all future sessions opened against `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/`.
