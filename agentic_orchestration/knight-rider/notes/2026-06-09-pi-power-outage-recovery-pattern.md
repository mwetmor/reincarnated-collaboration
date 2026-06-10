# Pi power-outage recovery pattern — diagnostic chain + empirical state capture

> **Author:** knight-rider
> **Date:** 2026-06-09
> **Trigger:** Matt session-open report — Pi SSH connection broken after a power outage; could not see Pi in Finder
> **Outcome:** SSH restored via single power cycle; SMB share remounted via `⌘K`; postgres-not-installed re-confirmed (matches deferred-D1 status)
> **Cross-references:**
> - `canonical/story/infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25.md` § 2.2 (SD-card write-wear warning) + § 2.3 (backup discipline) + § 6.2 (single point of failure)
> - `~/.ssh/config` host alias `reincarnated-pi` → `reincarnated-pi.local` user `mwetmor` identity `~/.ssh/reincarnated-pi`

---

## 1. Why this note exists

The Pi recovery pattern is non-obvious under stress. SSH failed with `kex_exchange_identification: read: Connection reset by peer` — a symptom that looks like a network/key problem but is actually sshd-side post-boot degradation. Easy to misdiagnose; worth capturing the empirical chain so future-knight-rider (or future-Matt) can resolve in minutes instead of re-deriving.

The note is also durable evidence for when D1 (Pi-Postgres execution) finally fires — see § 4.

---

## 2. The diagnostic chain (in order of confidence-building)

### 2.1 Confirm network reachability

```bash
ping -c 3 -W 2000 reincarnated-pi.local
```

- If 0% loss → Pi is on the network; problem is service-layer not network-layer
- If 100% loss → check Pi power LED, router, switch port

### 2.2 Confirm TCP layer to port 22

```bash
ssh -4 -v -o ConnectTimeout=6 -o BatchMode=yes reincarnated-pi true 2>&1 | grep -E "(Connecting|kex|Connection|identification)"
```

Look for the diagnostic split:
- `Connection established` → TCP is fine
- `Local version string SSH-2.0-OpenSSH_*` → client sent its banner
- `kex_exchange_identification: read: Connection reset by peer` → **sshd accepted the TCP connection then dropped it before sending its own banner**

That last symptom is the load-bearing signature. It means sshd is *running* (otherwise TCP would refuse outright) but is in a degraded state where it can't complete the handshake.

### 2.3 The IPv4 vs IPv6 sanity check

If the first attempt hits an IPv6 address (e.g., `2600:1700:...`) but ping resolved to a LAN IPv4 (`192.168.1.x`), force IPv4:

```bash
ssh -4 reincarnated-pi
```

Stale SLAAC IPv6 records can persist in DNS for minutes after a Pi reboot. Forcing IPv4 isolates whether the issue is address-routing or sshd-side. In this outage, IPv4 had the same `kex_exchange_identification` symptom — confirming sshd-side, not routing.

### 2.4 Recovery

Since SSH is down, you cannot graceful-shutdown remotely. Physical power cycle:
1. Unplug USB-C power
2. Wait ~10 seconds (capacitor drain + disk cache settle)
3. Plug back in
4. **Wait 60–90 seconds** before retesting SSH (sshd doesn't come up instantly; fresh boot may run `fsck`)

### 2.5 Post-cycle health verification

```bash
ssh -4 reincarnated-pi "hostname; uptime; mount | grep ' / '; systemctl is-active ssh"
```

Look for:
- `uptime` shows minutes since boot (confirms the cycle landed)
- `mount` shows `/dev/mmcblk0p2 on / type ext4 (rw,noatime)` — **must be `rw`, not `ro`**
- If `ro`: rootfs came up read-only (likely fsck issue). Needs physical access + `sudo fsck /dev/mmcblk0p2` then reboot.

### 2.6 If post-cycle SSH still fails

Then physical access is required (monitor + USB keyboard on the Pi):
- `sudo systemctl status ssh`
- `sudo journalctl -u ssh -n 50` — look for host key load errors
- `mount | grep " / "` — look for `ro,` mount
- `dmesg | grep -i "readonly\|remount"`

Cases this catches: corrupted host keys (`/etc/ssh/ssh_host_*`), read-only rootfs from filesystem damage, sshd config syntax errors blocking startup.

---

## 3. Finder SMB-share visibility (parallel problem)

SSH restoration does NOT restore Finder sidebar discovery. Finder's network browser uses Bonjour for `_smb._tcp` advertisements, which can stay stuck on stale state for 10+ minutes after a host returns.

**Fast path — bypass sidebar entirely:**

1. Finder → `⌘K` (Go → Connect to Server)
2. Enter `smb://reincarnated-pi.local`
3. Connect → user `mwetmor` + Samba password
4. Share `reincarnated` mounts → appears in Locations

Right-click mounted share → "Add to Sidebar" to persist.

**If you specifically need sidebar/Network discovery to repopulate:**

```bash
sudo killall -HUP mDNSResponder   # flush macOS mDNS cache
```

Or toggle Mac Wi-Fi off/on. Then open a new Finder window → Network. Repopulates in ~30 seconds typically.

**Pi-side sanity check (if Finder still can't see it):**

```bash
dns-sd -B _smb._tcp local. &   # browse mDNS; should show REINCARNATED-PI
ssh -4 reincarnated-pi "systemctl is-active smbd; ls -la /home/mwetmor/data/shared"
```

In the 2026-06-09 case: smbd was `active`, share path intact, Bonjour advertised the host as `REINCARNATED-PI` — Finder-side staleness was the entire problem.

---

## 4. Empirical evidence captured from this outage (for eventual D1 ops runbook)

| Observation | Evidence | Implication for D1 |
|---|---|---|
| SD card survived ungraceful power loss without filesystem corruption | Post-cycle `mount` showed `rw`; no fsck needed; share contents (`agent-prompts`, `engine-output`, `meshy-handoff`, `visual-artifacts`) all intact | One data point in favor of SD-card durability under outages; does NOT generalize (next outage could go differently). Reinforces § 2.2 NVMe-mandatory + § 2.3 backup-discipline reasoning rather than weakening it. |
| sshd post-outage symptom is misleading | `kex_exchange_identification: read: Connection reset by peer` looks like a client/key problem; was actually post-boot sshd degradation; resolved by power cycle | The eventual D1 ops runbook should pre-bake this recovery pattern so a postgres-down + ssh-down situation doesn't compound into hours of misdiagnosis |
| Recovery time | Single power cycle + 60–90s wait → fully healthy | Acceptable recovery window for D1 if (a) backups are current and (b) NVMe is the data volume. Without NVMe, an SD-corruption outage would be hours-to-days, not seconds. |
| Postgres absence re-confirmed | Pi survey showed `psql: command not found`, `systemctl is-active postgresql → inactive`, `/opt` + `/srv` stock state, no cron, only `:22` listening | Tier 1 / Tier 2 / Tier 3 all still pre-build. No data was at risk this outage because nothing was there yet. This window of pre-build state is the cheapest possible "test our recovery procedure" environment. |

**Recommendation when D1 fires:** the eventual `infrastructure-pi-ops-runbook.md` (post-D1-execution doc; not yet authored) should incorporate § 2 + § 3 verbatim as the first-response checklist. Add postgres-specific recovery (`systemctl status postgresql`, `pg_isready`, WAL recovery state, `pg_dump` latency check) as a second section once postgres is actually installed.

---

## 5. What this note is NOT

- NOT an amendment to the 2026-05-25 recognition record (gandalf's canonical-story doc; un-touched here)
- NOT a commitment to schedule D1 execution; the deferred status holds
- NOT a substitute for the eventual post-D1 ops runbook (that's star-lord territory when Tier 1 fires)

It IS a knight-rider operational note: the recovery pattern, plus durable empirical evidence from this outage that should propagate forward into the D1 ops runbook when it gets authored.
