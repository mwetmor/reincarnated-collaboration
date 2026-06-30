# Transition Document: Pi Infrastructure Layer as Mac-to-PC Connective Tissue

**To:** Gandalf
**From:** Matt (via strategic conversation context)
**Date:** 2026-05-30
**Scope:** Implementation planning for Raspberry Pi 5 as middleware infrastructure between Mac (content engine) and PC (Unreal game engine)

---

## Purpose of This Document

This document hands off a specific, bounded infrastructure decision for implementation planning. The scope is the Pi's role as connective tissue between two development machines, not broader strategic project direction.

The strategic conversations producing this decision are separate from this scope. What this document captures is what's been decided about the Pi's role specifically, what's open for implementation planning, and what needs to be sequenced.

---

## The Architectural Decision

The Pi 5 (8GB RAM, 128GB SD card) serves as middleware infrastructure between two development machines that handle different aspects of the project:

**Mac:** Content engine in Python, agent orchestration, design work, JSON output generation from engine pipeline runs.

**PC:** Unreal Engine 5 development (substrate dependent, will be installed/built when PC specs are confirmed adequate), game runtime integration with engine-generated content, character creation system implementation.

**Pi:** Always-on middleware layer that both machines interact with rather than direct Mac-to-PC communication.

The decision was driven by several constraints:

1. Mac install corruption issues with Unreal Engine (suspected security software interference)
2. 8GB RAM on Mac making Unreal development impractical regardless of install issues
3. Need for iterative testing workflow where engine outputs flow to Unreal and back
4. Existing PostgreSQL infrastructure already on Pi
5. Desire to use hardware Matt already has rather than acquiring more

---

## The Pi's Specific Role

The Pi handles three connective tissue functions:

### Function 1: File Sharing
Both Mac and PC access shared folders on the Pi via Samba. Engine on Mac writes JSON outputs to Pi's shared folder. PC reads JSON from Pi when Unreal needs to import. The Pi handles being always-available so neither development machine needs to be on for files to be accessible.

### Function 2: HTTP API Endpoint (Phase 2)
Pi runs a small web service (FastAPI or similar) exposing endpoints for dynamic queries. Unreal can request "current state of character X" or "all characters matching criteria Y" via HTTP rather than searching files. Backed by PostgreSQL which already runs on the Pi.

### Function 3: PostgreSQL Database Host (Already Established)
Continues hosting the project's PostgreSQL instance. Engine writes data, queries return data, services consume data. The HTTP API queries this for dynamic responses.

---

## Storage Strategy

### Initial Phase: SD Card (Current)
- OS, applications, services on SD card
- Service data also on SD card initially
- PostgreSQL data on SD card initially
- Acceptable for weeks, not for long-term

### Migration Phase: External USB 3 SSD (Future)
- Mount external SSD at `/data` or similar
- PostgreSQL data files moved to SSD
- Shared folder contents moved to SSD
- OS and applications remain on SD card
- Trigger for migration: SD card approaching 70-80% full, OR write activity wear becoming concerning, OR 6 months elapsed, OR any read/write errors in system logs

### Critical: Make Setup Migration-Ready From the Start
- Use explicit data directories like `/home/matt/data/postgresql` and `/home/matt/data/shared`, NOT default locations
- Document what's installed where
- Use absolute paths in all service configurations
- Set up backup procedures from day one (weekly automated copy minimum)
- When SSD arrives, migration is: mount SSD at `/data`, copy data over, update mount point, restart services

---

## Implementation Phasing

### Phase 1: Basic File Sharing (Immediate Priority)
**Goal:** Mac engine outputs accessible to PC via Pi network share

**Tasks:**
1. Install Samba on Pi (`sudo apt install samba`)
2. Create shared folder at `/home/matt/data/shared` (note: explicit path, not default)
3. Configure smb.conf to expose the folder with appropriate permissions
4. Set Samba passwords for user accounts that Mac and PC will use to connect
5. Restart Samba service
6. Test connection from Mac via Finder → Connect to Server → `smb://[pi-hostname-or-ip]/sharename`
7. Test connection from PC via File Explorer → Map network drive → `\\[pi-hostname-or-ip]\sharename`
8. Verify bidirectional file operations work (write from Mac, read from PC, write from PC, read from Mac)

**Success criteria:** Engine writes a JSON file to the Pi share, PC reads that exact file content within seconds.

**Estimated effort:** 4-8 hours for clean setup including testing.

### Phase 2: HTTP API Service (When Needed)
**Goal:** Dynamic queries from Unreal to Pi-backed data

**Tasks:**
1. Install Python and FastAPI on Pi (`sudo apt install python3-pip`, `pip install fastapi uvicorn`)
2. Create service that exposes endpoints relevant to Unreal's needs
3. Connect service to PostgreSQL for data queries
4. Configure service to run as systemd service for automatic start
5. Test endpoints from Mac (curl or similar)
6. Integrate Unreal-side consumption (VaRest plugin or custom HTTP client)

**Triggered by:** Discovering that file-based transfer isn't sufficient and dynamic queries would help iteration speed.

**Estimated effort:** 8-16 hours for working API service plus Unreal integration.

### Phase 3: SSD Migration (When Triggered)
**Goal:** Move data to reliable storage before SD card limits become problems

**Tasks:**
1. Acquire USB 3 SSD (500GB-1TB recommended, $50-100)
2. Connect SSD to Pi USB 3 port
3. Format SSD with appropriate filesystem (ext4 typical)
4. Mount SSD at `/data` (or wherever absolute paths point)
5. Stop services (PostgreSQL, Samba)
6. Copy data from current locations to SSD
7. Update mount point so applications find data on SSD
8. Restart services
9. Verify functionality
10. Reclaim SD card space (data should now be on SSD)

**Triggered by:** Any of the conditions in Storage Strategy section above.

**Estimated effort:** 2-4 hours for migration once SSD acquired.

---

## Iteration Workflow This Enables

The completed Pi infrastructure supports this development cycle:

1. Matt makes change to engine on Mac
2. Engine generates JSON outputs to Pi shared folder (via Samba)
3. PC's Unreal sees updated files immediately (network share)
4. Unreal reimports (manually triggered or via directory watcher)
5. Matt evaluates result in Unreal on PC
6. Iteration cycle: ~30-90 seconds depending on engine generation time

Without the Pi, this iteration requires either both machines being on simultaneously and sharing directly, or manual file copying between machines, or cloud sync with sync latency. The Pi as middleware removes these friction points.

---

## Critical Considerations for Implementation

### Atomic File Writes
When engine writes JSON to shared folder, write to temporary file first, then rename to final filename. Prevents Unreal from reading partially-written files. Standard pattern: write to `output.json.tmp`, then `mv output.json.tmp output.json`. The rename is atomic from reader perspective.

### Schema Versioning
Include schema version field in every JSON file. Unreal import code checks version before parsing. Prevents Unreal from crashing on unexpected JSON structure. Allows engine and Unreal to evolve at different rates with explicit compatibility tracking.

### Logging on Both Sides
Engine logs what JSON it generated (with version, timestamp, source data). Unreal logs what it imported (with version, timestamp, any parse errors). When iteration produces unexpected results, logs on both sides enable diagnosis.

### File Naming Conventions
Include identifying information in filenames. Timestamp, character ID, iteration counter. Makes it possible to track which version produced which Unreal behavior. Example: `character_form_021_v3_20260530.json` rather than `output.json`.

### Backup From Day One
SD card can fail without warning. Weekly automated copy of `/home/matt/data` to another location (Mac, PC, cloud, second drive on Pi). The backup script doubles as migration script later. This is not optional even for "temporary" SD card setup.

### Network Reliability
The Pi needs reliable network connection. If Pi disconnects from network, both Mac and PC lose access to shared infrastructure. Consider:
- Wired ethernet preferred over WiFi for reliability
- Static IP for Pi so machines always find it at same address
- Network share auto-reconnect configured on Mac and PC

### Performance Expectations
SD card read speeds are adequate for JSON file serving. SD card write speeds are slower but JSON files are small enough this isn't usually a bottleneck. PostgreSQL on SD card has wear concerns but performance for normal queries should be acceptable.

If iteration becomes slow due to Pi performance, that's signal to accelerate SSD migration. Healthy Pi infrastructure should not be a performance bottleneck for the development workflow.

---

## What's Open for Implementation Planning

### Sequencing Within Phase 1
Order of: Samba setup, network configuration, PC connection setup, Mac connection setup, testing. Probably best done in single focused session of 4-8 hours rather than spread across days.

### Specific Samba Configuration
User accounts, permissions model, share definition. Need to balance security (don't expose Pi unnecessarily) with convenience (smooth Mac and PC access).

### Static IP vs Hostname-Based Connection
Whether to give Pi a static IP (more reliable) or rely on `.local` hostname resolution (simpler setup, occasionally flaky). Trade-off between setup complexity and ongoing reliability.

### Backup Strategy Specifics
What gets backed up, how often, to where, with what retention. The principle is "backups exist from day one" but specifics need decision.

### Monitoring Approach
Whether to set up active monitoring (Prometheus or similar) or rely on periodic manual checks. For a single-user solo dev project, manual checks may be sufficient. Monitoring infrastructure has its own complexity cost.

### Documentation Format
How to document the Pi setup so future-Matt (and future-Gandalf) can understand it months later when modifications become necessary. Markdown file in project repository probably appropriate.

---

## What's Out of Scope for This Transition

The following are explicitly NOT part of this Pi infrastructure scope:

- Engine architecture decisions (continue per existing seam-led design process)
- Unreal Engine implementation details (separate work when PC setup is ready)
- Character creation system design (covered in separate strategic conversation)
- Battle simulation restoration (covered in separate strategic conversation)
- Substrate expansion (covered in separate strategic conversation)
- Long-term project commercial strategy (covered in separate strategic conversation)

The Pi handles connecting Mac and PC. Other infrastructure decisions are independent.

---

## Recommended Next Actions

For Gandalf to plan implementation:

1. Review this document and identify any missing context needed for implementation planning
2. Confirm Phase 1 scope is correctly bounded (file sharing only, no HTTP API yet)
3. Plan specific Samba configuration approach
4. Plan backup strategy that's appropriate for SD card period
5. Document the specific paths and configuration that Phase 3 migration will need
6. Coordinate with Matt on timing for Phase 1 execution
7. Establish acceptance criteria for "Phase 1 complete" before starting work

For Matt:

1. Confirm Pi current state (what's currently installed, what configurations exist)
2. Confirm network setup (Pi's current IP, hostname, network topology)
3. Identify what's currently using `/home/matt/data` or similar paths that might conflict
4. Confirm PC specs are adequate for Unreal (this affects whether the workflow this enables is actually usable)
5. Confirm acceptance of approximately 4-8 hours for Phase 1 implementation

---

## A Note on This Document's Limits

This document captures the Pi-as-connective-tissue decision as of the strategic conversation. Specific technical details (exact Samba configuration syntax, specific PostgreSQL data directory location currently in use, exact network topology) need to be determined during implementation planning rather than specified here.

The document's purpose is establishing what was decided and why, plus what's open for implementation planning. It's not a complete implementation specification. Gandalf and Matt will produce that specification together during implementation planning conversations.

If anything in this document conflicts with Gandalf's existing project knowledge or with Matt's current Pi state, the conflict should be flagged and resolved before implementation proceeds. The document represents intent at handoff time, not authoritative current state.

---

**End of transition document.**
