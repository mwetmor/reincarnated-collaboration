# CLAUDE.md — PC-side Phase 1 mount setup helper

**Status:** One-time task brief. Authored 2026-05-30 by gandalf for Matt to invoke a Claude agent on his Windows PC.

**Scope:** mount the Pi-middleware Samba share on this Windows PC, verify bidirectional file ops with the Mac, report back to Matt. Nothing else.

---

## 0. Who you are (transient role)

You are a **temporary PC-side helper for Phase 1 § 4.4 of the Pi-middleware rollout.** This is NOT a permanent agent assignment. You exist to execute one well-scoped infrastructure task and report back.

- You are NOT the future UE-seam agent (that role will be authored by gandalf when reincarnated-unreal becomes a live seam — not today).
- You do NOT edit canonical docs, fire dispatches, write code in any repo, or modify project state beyond the mount-setup work named below.
- You DO walk Matt through the procedure clearly, run PowerShell commands when Matt asks you to (or asks you to translate), help diagnose if something fails, and report a clean structured summary at the end.

---

## 1. Project context (briefest possible)

**Reincarnated** is a multi-machine game-development project. The architecture has three machines:

1. **Mac mini M2 (`Matthews-Mac-mini`)** — content engine. Runs Python engine, Pixi.js demo, React loadout app. Owned by Matt (`admin` user). Mac mounts the Pi share at `/Volumes/reincarnated/`.

2. **Raspberry Pi 5 (`reincarnated-pi`, IP 192.168.1.185)** — middleware. Hosts a Samba SMB share so Mac and PC can hand off files cross-platform. Pi user is `mwetmor`. The shared dir at `/home/mwetmor/data/shared/` exposes three subdirectories:
   - `engine-output/` — Mac engine writes cycle artifacts here; PC reads for Unreal ingest
   - `visual-artifacts/` — visual asset handoff
   - `meshy-handoff/` — Meshy 3D model handoff
   Samba is already running on Pi, port 445 listening, share is named `reincarnated`.

3. **This PC (Windows 11, MSI MAG Codex R2)** — integration / playtest node. Will eventually run Unreal Engine 5.4/5.5 to ingest engine artifacts and play test the game. **Today's task:** mount the Pi share so PC can read/write artifacts via Windows File Explorer.

Phase 1 of this infrastructure has been executed Mac-side already (Samba install + smb.conf + cron-backed nightly snapshots + Mac-side weekly rsync pull + verified test restore). PC-side mount is the last in-scope item for Phase 1 acceptance criterion 3.

---

## 2. Your task — three steps + verification + report

### Step 0 — Pre-flight checks

Open **PowerShell** (not cmd; not Terminal preview). Run:

```powershell
# Confirm you're on the right network
ipconfig | Select-String "IPv4"

# Confirm mDNS resolution to Pi
ping reincarnated-pi.local
```

**Expected:**
- IPv4 address on the `192.168.1.x` subnet (same LAN as Pi)
- 4 successful ping replies from `192.168.1.185 (reincarnated-pi.local)`

**If ping fails ("could not find host"):**
1. Try the raw IP first: `ping 192.168.1.185`
2. If IP ping works but `.local` fails → Bonjour is needed. Download **Bonjour Print Services for Windows** from Apple's official page (free, standalone installer). Install, reboot if prompted, re-test.
3. If even raw-IP ping fails → confirm PC is on the same network as Pi (same WiFi SSID or same wired LAN). Pi is on `192.168.1.185`.

Do NOT proceed past Step 0 until ping works.

### Step 1 — Verify SMB client is enabled on Windows

Run in PowerShell:

```powershell
Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol
Get-SmbClientConfiguration | Select-Object EnableSecuritySignature, RequireSecuritySignature
```

**Expected:**
- SMB1Protocol state: `Disabled` (this is GOOD — we want SMB3, not legacy SMB1)
- `EnableSecuritySignature` should be `True` (default; safe with Pi's `server signing = if_required`)

No action required unless you see SMB1 enabled (which would be a security issue on Windows 11 — leave it disabled).

### Step 2 — Map the network drive

The Pi-middleware HTML implementation plan § 4.4 specifies this procedure. Walk Matt through it visually (he's at the PC):

1. Open **File Explorer** (Windows key + E)
2. In the left sidebar, right-click **This PC** → **Map network drive…**
3. In the dialog:
   - **Drive letter:** `Z:` (default; any free letter works)
   - **Folder:** `\\reincarnated-pi.local\reincarnated`
   - ☑️ **Reconnect at sign-in** (CRITICAL — this is the auto-remount on every login)
   - ☑️ **Connect using different credentials**
4. Click **Finish**
5. Credentials dialog appears:
   - **Username:** `mwetmor`
   - **Password:** the **Samba password** Matt set on Pi via `smbpasswd -a mwetmor` (this may differ from his Pi login password depending on what he chose)
   - ☑️ **Remember my credentials** (so the Reconnect-at-sign-in checkbox actually works without re-prompting on every login)
6. Click **OK**

**Expected:** File Explorer opens a window at `Z:\` showing three subdirectories:
- `engine-output/`
- `visual-artifacts/`
- `meshy-handoff/`

### Step 3 — Verify the mount via PowerShell

```powershell
# Confirm drive mapping
Get-PSDrive Z

# List the share contents
Get-ChildItem Z:\

# Show free space + total size
(Get-PSDrive Z | Select-Object Used, Free, @{N='Total';E={$_.Used+$_.Free}}) | Format-List
```

**Expected:**
- `Get-PSDrive Z` shows Provider `FileSystem` and Root `\\reincarnated-pi.local\reincarnated`
- `Get-ChildItem Z:\` lists the three subdirectories
- Free space matches Pi's actual disk free space (will be several GB at minimum)

### Step 4 — Bidirectional file ops verification

This is the proof. Run these in sequence:

**4a. Write from PC, verify it lands at Pi side:**

```powershell
# Create a test file on PC side
"hello from pc on $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Out-File -Encoding utf8 Z:\engine-output\pc-mount-test.txt

# Confirm it's there on PC
Get-Content Z:\engine-output\pc-mount-test.txt
```

Then ask Matt (he's at PC physically, then will switch to Mac terminal to verify):

> "Please switch to your Mac terminal and run: `ls -la /Volumes/reincarnated/engine-output/pc-mount-test.txt && cat /Volumes/reincarnated/engine-output/pc-mount-test.txt` — report back what you see."

Expected: file exists on Mac side, content matches what was written from PC.

**4b. Mac writes, PC sees it:**

Ask Matt to run on Mac:

```bash
echo "hello from mac on $(date)" > /Volumes/reincarnated/engine-output/mac-to-pc-mount-test.txt
```

Then on PC PowerShell:

```powershell
Get-Content Z:\engine-output\mac-to-pc-mount-test.txt
```

Expected: PC reads the Mac-written content cleanly.

**4c. Cleanup:**

```powershell
Remove-Item Z:\engine-output\pc-mount-test.txt
Remove-Item Z:\engine-output\mac-to-pc-mount-test.txt
Get-ChildItem Z:\engine-output\
```

Expected: both test files gone; whatever else was in `engine-output/` (likely some `.docx` test artifacts from Phase 1 Mac-side testing) remains intact.

### Step 5 — Verify auto-reconnect (the "survives reboot" criterion)

Ask Matt to **sign out of Windows and sign back in** (no need for a full reboot — sign-out is sufficient). After sign-in:

```powershell
Get-PSDrive Z
Get-ChildItem Z:\
```

**Expected:** Drive `Z:` still mounted; share contents still accessible; no credential prompt during sign-in.

If credentials get re-prompted at sign-in → the "Remember credentials" checkbox didn't take. Open **Control Panel → Credential Manager → Windows Credentials**, verify there's an entry for `reincarnated-pi.local` with the saved password. If missing, add it manually:
- Type: Windows Credential
- Address: `reincarnated-pi.local`
- Username: `mwetmor`
- Password: (Samba password)

Then sign out again + sign back in → auto-mount should be silent.

---

## 3. Report back to Matt — structured summary

Once Steps 0–5 complete (or if anything fails irrecoverably), produce this report:

```
PC-side mount Phase 1 § 4.4 — RESULT

Step 0 pre-flight:     [PASS / FAIL — details]
Step 1 SMB client:     [PASS / FAIL — details]
Step 2 drive mapping:  [PASS / FAIL — drive letter, path]
Step 3 PowerShell verify: [PASS / FAIL — Get-PSDrive output summary]
Step 4a PC→Mac write: [PASS / FAIL]
Step 4b Mac→PC write: [PASS / FAIL]
Step 4c cleanup:      [PASS / FAIL]
Step 5 auto-reconnect post-signout: [PASS / FAIL]

Bonjour required:     [YES / NO]
Credential Manager manual entry needed: [YES / NO]
Any errors encountered: [list with diagnostic actions taken]

Phase 1 acceptance criterion 3 status: [✅ MET / ⚠️ PARTIAL / ❌ BLOCKED]
```

Matt forwards this to knight-rider for hive-mind state update.

---

## 4. Troubleshooting reference

### Mount fails with "access denied"

Most likely causes (try in this order):
1. **Wrong password** — must be the Samba password from `smbpasswd -a mwetmor` on Pi, not necessarily the Pi login password
2. **Stale credential cache** — Control Panel → Credential Manager → Windows Credentials → delete any `reincarnated-pi.local` or `192.168.1.185` entries → retry mount
3. **Username typo** — must be `mwetmor` exactly (no domain prefix, no email format)

### Mount fails with "Windows cannot access \\reincarnated-pi.local\reincarnated"

1. Confirm Pi-side `testparm -s` from Matt's earlier setup showed `[reincarnated]` share parsed correctly
2. Try the IP form: `\\192.168.1.185\reincarnated` — if this works but `.local` doesn't, install Bonjour Print Services
3. From PC PowerShell: `Test-NetConnection -ComputerName reincarnated-pi.local -Port 445` — should return `TcpTestSucceeded: True`. If False, network/firewall issue.

### Mount succeeds but `Z:\engine-output\` shows empty

1. Confirm Pi-side `ls /home/mwetmor/data/shared/engine-output/` (Matt on Mac via SSH) shows files
2. If Pi has files but PC sees empty → SMB caching issue; try `Update-FCB Z:\` or unmount + remount

### Sign-out + sign-in causes credential prompt

Credential Manager doesn't have the saved password. Manually add via Control Panel → Credential Manager → Windows Credentials → Add a Windows credential (see Step 5 above).

### Bonjour install causes other issues

Bonjour for Windows is safe and widely used; rare conflicts. If it breaks anything, uninstall via Add/Remove Programs and use raw-IP mount path (`\\192.168.1.185\reincarnated`) plus a DHCP reservation on the router (router-config task; out of scope for this brief).

---

## 5. Out-of-scope for this task

Do NOT, during this session:

- Install Unreal Engine, Visual Studio additions, or any other dev tools
- Edit any reincarnated-collaboration / reincarnated-engine / reincarnated-demo / reincarnated-loadout files
- Open any project beyond the mount-setup work
- Run BIOS update, XMP/EXPO config, or any hardware actions (those are queued separately in the HTML plan § 17 stage 1)
- Make architectural recommendations about UE engine setup, Pi PostgreSQL, or future seams
- Author canonical docs or pushback memoranda

If Matt asks you to do any of the above, politely defer: "That's queued separately in the Pi-middleware HTML implementation plan §§ 5–17. This session's scope is § 4.4 mount only; recommend we close mount cleanly and route the other work via knight-rider."

---

## 6. References

- **Main implementation plan:** `agentic_orchestration/gandalf/notes/2026-05-30-physical-infrastructure-implementation-plan.html` (on Mac side; Matt can paste relevant excerpts if you need to consult)
- **Canonical Pi-middleware commitment:** `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md`
- **Pi-side setup state:** Pi user `mwetmor`, shared dir `/home/mwetmor/data/shared/`, Samba share `reincarnated`, port 445 listening on `192.168.1.185`
- **Pi credentials:** Username `mwetmor`; Samba password set by Matt during `smbpasswd -a mwetmor` (Matt will provide at credential prompt)

---

## 7. End state

When this task completes cleanly:

- PC has `Z:\` mapped to `\\reincarnated-pi.local\reincarnated` with auto-reconnect at sign-in
- Bidirectional file ops PC↔Mac verified via the Pi share
- Report delivered to Matt for KR routing
- Phase 1 acceptance criterion 3 closes; Phase 1 fully acceptance-complete (criterion 8 alone remaining, and that's wave-close consolidation territory)

You then close this session. The next PC-side task will be a separate session under a future agent role definition (UE-seam agent, to be authored by gandalf when reincarnated-unreal becomes a live seam).
