# System Specifications & Pipeline Suitability Report

**Purpose of this document:** This Windows PC is the **integration & playtest node** in a three-system pipeline. Two other machines produce **JSON** (logic/config/scene data) and **3D model outputs**; this PC ingests those artifacts and **playtests them integrated into an Unreal Engine game**. This report documents the hardware/software found on the machine and assesses how well it will handle each stage of that workflow.

**Report generated:** 2026-05-30
**Hostname / Model:** MSI MAG Codex R2 (`US Desktop Codex R2`)
**OS install date:** 2025-01-20

---

## 1. Quick Verdict

| | |
|---|---|
| **Overall fitness for the role** | **Good — fully capable of being the Unreal integration/playtest node at 1080p.** |
| **Strongest area** | CPU (20-core i7-14700F) and NVMe storage — excellent for asset import, cooking, compiling, and editor responsiveness. |
| **Primary constraint** | **8 GB GPU VRAM** — the limiting factor for high-fidelity scenes, dense imported 3D models, and 4K. |
| **Secondary constraint** | **32 GB system RAM** — adequate but is the practical floor for Unreal dev; tight if running other tools (e.g. Roblox Studio) concurrently. |
| **Recommended before production use** | Verify memory XMP/EXPO profile, update BIOS for 14th-gen stability, prefer wired Ethernet for the inbound artifact transfers. |

---

## 2. Hardware Specifications

### CPU
| Property | Value |
|---|---|
| Model | **Intel Core i7-14700F** (14th Gen, "Raptor Lake Refresh") |
| Cores / Threads | **20 cores / 28 threads** (8 Performance + 12 Efficiency cores) |
| Base clock (reported) | 2.1 GHz base; boosts to ~5.4 GHz on P-cores |
| L2 / L3 Cache | 28 MB / 33 MB |
| Socket | LGA1700 |
| Integrated graphics | **None** — the "F" suffix means no iGPU; a discrete GPU is mandatory. |

> The 14700F is a strong multi-core part. Unreal's parallel workloads (shader compilation, lightmap/Lumen builds, asset cooking, mesh import processing) scale well across these 28 threads. This is the machine's best asset.

### GPU
| Property | Value |
|---|---|
| Model | **NVIDIA GeForce RTX 4060 Ti** |
| VRAM | **8 GB GDDR6** |
| Driver | 560.94 (DriverVersion 32.0.15.6094, dated 2024-08-13) |
| Architecture | Ada Lovelace — supports DX12 Ultimate, hardware ray tracing, DLSS 3 / Frame Generation, Nanite, Lumen (HW & SW). |
| Current display | 1920 × 1080 @ 60 Hz |
| **VRAM in use at scan time** | **~4.9 GB of 8 GB already consumed** (Roblox Studio + Unreal Editor both running) |

> The 4060 Ti is a capable 1080p Unreal 5 card and supports all of UE5's modern rendering features. **8 GB VRAM is the headline limitation:** dense scenes built from many imported high-poly models with 4K texture sets, or playtesting at 1440p/4K, will pressure or exceed the VRAM budget and force texture streaming / pop-in. DLSS can mitigate the render-resolution cost but not the asset-memory cost.

### Memory (RAM)
| Property | Value |
|---|---|
| Total | **32 GB** (31.84 GB usable) |
| Configuration | 2 × 16 GB Kingston Fury (`KF556C40-16`), dual-channel |
| Module rating | **DDR5-5600 CL40** |
| **Currently running at** | **~2000 MHz / 4000 MT/s (reported)** |
| Slots populated | DIMMA2, DIMMB2 (2 of 4 slots used) |

> ⚠️ **Action item:** The installed kits are rated for DDR5-5600 but report running well below that. Enable the **XMP/EXPO profile in BIOS** to reclaim memory bandwidth (or confirm this is just a WMI reporting quirk via CPU-Z). Bandwidth matters for Unreal streaming and cook performance.
>
> 32 GB is the *working minimum* for serious UE5 development. With the editor open on a non-trivial project, RAM use of 16–24 GB is normal; add a browser, an IDE, and another engine (Roblox Studio was running during this scan) and you approach the ceiling. **64 GB is the recommended upgrade** — two open slots make this a cheap, high-impact improvement.

### Storage
| Property | Value |
|---|---|
| Drive | **MSI M482 2 TB NVMe SSD** (PCIe) |
| Total / Free | 1,863 GB total · **289 GB free** on C: |
| Type | Solid State, NVMe bus — fast random + sequential I/O |
| Page file | 7.95 GB on C: |

> NVMe is ideal for this role: fast ingest of incoming 3D model files, quick asset import, and responsive Derived Data Cache / shader cache. **289 GB free is workable but watch it** — UE5 projects, the DDC, and cooked builds consume space rapidly. Consider a second NVMe drive dedicated to project/build data if the pipeline produces large or frequent artifacts.

### Motherboard / Platform
| Property | Value |
|---|---|
| Board | **MSI PRO B760-VC WIFI 7 (MS-7D98)**, rev 2.0 |
| Chipset | Intel B760 |
| BIOS | AMI `B.H5`, dated **2024-01-11** |

> ⚠️ **Recommended:** The BIOS dates to Jan 2024, which **predates Intel's microcode fixes (0x129/0x12B, mid–late 2024) for the 13th/14th-gen voltage instability issue.** Sustained heavy loads (long Unreal cooks, shader compiles, lightmap bakes) are exactly the kind of workload that exposed that defect. **Update to the latest BIOS** for long-term CPU stability and to protect the chip.

### Networking
| Property | Value |
|---|---|
| Active adapter | **Qualcomm FastConnect 7800 Wi-Fi 7** |
| Link speed | 1.2 Gbps |
| Active LAN IP | 192.168.1.133 (via Wi-Fi) |
| Wired Ethernet | Present but **not connected** (link-local 169.254.x.x — no cable/DHCP) |

> For a multi-system pipeline where this PC continuously **receives JSON + 3D model artifacts over the network**, Wi-Fi 7 at 1.2 Gbps is fast but variable in latency. **A wired Gigabit/2.5G Ethernet connection is recommended** for the inbound transfer link — more deterministic, lower latency, no contention. The board has an onboard NIC; just connect a cable.

---

## 3. Software & Development Environment

| Tool | Status |
|---|---|
| **OS** | Windows 11 Home, 64-bit — Build **26200** (24H2/25H-series), version 10.0.26200 |
| **Unreal Engine** | **UE 5.4 and UE 5.5 installed** (via Epic Launcher). Legacy engine assocs present for 4.27, 5.1–5.5. UnrealEditor was **running** at scan time. |
| **Visual Studio** | **VS 2022 installed** — required toolchain for UE C++ compilation. |
| **.NET SDK** | 10.0.300 |
| **Python** | 3.12 (`Python312`) |
| **Node.js** | Installed (Program Files\nodejs) |
| **Git** | Installed (user-local) |

> The toolchain for the integration role is **already in place**: Unreal 5.4/5.5 + Visual Studio 2022 (C++), plus Python/Node/Git for writing the ingest/automation glue that consumes the incoming JSON and imports the 3D models. No major software gaps for this workflow.

---

## 4. Pipeline Suitability — Process-by-Process

How well this PC handles each stage of "receive JSON + 3D models → integrate → playtest in Unreal":

| Process | Rating | Notes |
|---|---|---|
| **Receiving / ingesting JSON over network** | ⭐⭐⭐⭐⭐ Excellent | Trivial workload. CPU and NVMe handle parsing/writing instantly. Move to wired Ethernet for reliability. |
| **Receiving / ingesting 3D model files** | ⭐⭐⭐⭐ Very good | NVMe write speed is ideal. Only concern is total disk headroom (289 GB) if artifacts are large/frequent. |
| **Importing 3D models into Unreal (FBX/glTF/etc.)** | ⭐⭐⭐⭐ Very good | 20-core CPU chews through import/processing. Watch VRAM/RAM when importing many high-res-texture assets at once. |
| **Automation scripting (Python/Node glue to drive ingest+import)** | ⭐⭐⭐⭐⭐ Excellent | Full toolchain present; CPU is plentiful. |
| **Building/compiling (shaders, C++, Lumen/lightmaps, cooking)** | ⭐⭐⭐⭐ Very good | This is where 28 threads shine. Update BIOS first (stability under sustained load). RAM ceiling can throttle very large cooks. |
| **Playtesting (Play-In-Editor) @ 1080p, moderate scenes** | ⭐⭐⭐⭐ Very good | 4060 Ti runs UE5 + Lumen/Nanite well at 1080p; DLSS available for headroom. |
| **Playtesting high-fidelity / dense imported scenes @ 1080p** | ⭐⭐⭐ Adequate | **8 GB VRAM is the gate.** Expect texture streaming pressure with many high-res assets; tune texture pool / use DLSS. |
| **Playtesting @ 1440p or 4K** | ⭐⭐ Limited | VRAM and raster headroom become real constraints; viable only for lighter scenes or with aggressive DLSS + reduced settings. |
| **Running Unreal *while* other heavy apps are open (e.g. Roblox Studio)** | ⭐⭐ Limited | Observed during scan: RAM and VRAM both already heavily loaded. Close other engines/tools during playtest sessions, or upgrade RAM. |
| **Packaging / shipping builds for distribution** | ⭐⭐⭐⭐ Very good | CPU + NVMe handle it well; ensure disk free space before large cooks. |

---

## 5. Recommendations (Priority Order)

1. **Enable XMP/EXPO in BIOS** — reclaim DDR5-5600 speed (currently appears to run at ~4000 MT/s). Free performance.
2. **Update the motherboard BIOS** — current BIOS (Jan 2024) predates Intel's 13/14th-gen stability microcode. Important for a machine doing sustained heavy compiles/cooks.
3. **Use wired Ethernet for the inbound artifact link** — more deterministic than Wi-Fi for a continuous multi-system transfer pipeline.
4. **Upgrade RAM to 64 GB** *(highest-impact hardware upgrade)* — two slots are free; removes the biggest day-to-day constraint and lets you run ingest tooling + editor comfortably.
5. **Watch / expand storage** — 289 GB free is fine now but UE projects + DDC + cooked builds grow fast; a second NVMe for project data is a clean solution.
6. **VRAM mitigation for playtesting** — target 1080p, lean on DLSS, tune the texture streaming pool, and budget incoming model texture resolution. If the pipeline routinely produces very high-fidelity scenes intended for 1440p/4K playtest, a 16 GB-class GPU (e.g. 4060 Ti 16 GB / 4070 Ti Super / 5070-class) would be the upgrade that matters.

---

## 6. Raw Summary Block (for quick reference)

```
CPU:        Intel Core i7-14700F — 20C/28T (8P+12E), LGA1700, no iGPU
GPU:        NVIDIA GeForce RTX 4060 Ti, 8 GB GDDR6, driver 560.94
RAM:        32 GB DDR5 (2x16 Kingston Fury KF556C40, rated 5600, running ~4000 MT/s)
Storage:    2 TB MSI M482 NVMe SSD — 289 GB free
Board:      MSI PRO B760-VC WIFI 7 (MS-7D98), BIOS AMI B.H5 (2024-01-11)
Network:    Qualcomm Wi-Fi 7 @ 1.2 Gbps (active 192.168.1.133); wired NIC present, unused
OS:         Windows 11 Home 64-bit, build 26200
Engines:    Unreal Engine 5.4 & 5.5 installed
Toolchain:  Visual Studio 2022, .NET SDK 10.0.300, Python 3.12, Node.js, Git
Role:       Integration/playtest node — ingests JSON + 3D models, plays in UE5
Verdict:    Strong 1080p UE5 integration node. CPU+NVMe excellent; 8GB VRAM and
            32GB RAM are the constraints. Capable today; RAM+BIOS+XMP are the
            recommended pre-production fixes.
```
