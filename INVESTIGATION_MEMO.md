# IoT Device Forensic Plan: Investigation Memo (SYNTHETIC Case)

**Student Name:** DEEPTANSH NAGAR  
**Student ID:** 500121033  
**Project Code:** DF-PBL-026  
**Performance Mode:** Investigation Memo  
**Date:** October 27, 2026  
**Status:** Complete Submission Document  

---

## Executive Overview

This investigation memo presents the forensic acquisition planning, integrity management, and analysis for a fictional smart security camera incident. The investigation addresses a reported anomaly involving an unauthorized configuration change and subsequent video clip uploads during non-operational hours. 

All technical artifacts, device names, networks, and logs analyzed in this report are **SYNTHETIC**. The primary objective is to demonstrate defensible forensic methodology: establishing evidence provenance through cryptographic hashing, maintaining chain-of-custody integrity, applying structured hypothesis testing via an evidence matrix, and implementing a controlled reproducible test.

### Report Structure & Assessment Alignment

| Section | Focus Area | Assessment Weight | Rubric Element Addressed |
|---|---|:---:|---|
| **Section 1** | Problem Statement & Hypotheses | 20% | Problem framing, precise question, four competing hypotheses |
| **Section 2** | Evidence Inventory & Volatility | 10% | Architecture map, component volatility ordering (RFC 3227) |
| **Section 3** | Acquisition Plan & Risk Management | 25% | Acquisition steps, decision tree, risk register, chain-of-custody |
| **Section 4** | Analysis & Evidence Matrix | 20% | Evidence matrix separating observation, interpretation, and inference |
| **Section 5** | Reproducible Test & Integrity Tool | 15% | SHA-256 baselining, verification, tamper-detection, execution logs |
| **Section 6** | Limitations | Included in 20% | Explicit boundary conditions, synthetic data limits, untested hypotheses |
| **Section 7** | Qualified Conclusion | Included in 20% | Evidence-supported, non-overstated conclusion |
| **Section 8** | Verified References | Included in 10% | Verified standards (NIST, ISO, RFC) and tool documentation |
| **Section 9** | AI-Use Disclosure & Declaration | 10% | Transparent disclosure and personal student defense statement |

---

## 1. Problem Statement

### 1.1 Incident Scenario (SYNTHETIC)

An office administrator reported that a deployed smart security camera uploaded three distinct video clips between 02:14 and 02:31 while the facility was closed and unoccupied. Upon logging into the management interface the following morning, the owner discovered that motion detection alert notifications had been switched to **OFF**. The owner stated that they did not disable the notifications and did not authorize any video capture or export during that time window.

```
+--------------------------------------------------------------------------------------------------+
|                                    SYNTHETIC INCIDENT TIMELINE                                   |
|                                                                                                  |
|   Day 1, 18:40            Day 1, 23:55        Day 2, 02:10        Day 2, 02:14 - 02:31   Day 2, 09:05    |
|   [ Office Closes ] ----> [ New Session ] --> [ Alert: OFF ] ---> [ 3 Clips Uploaded ] ->[ Reported ]   |
|     Camera armed            Cloud login         Cloud API call      17-min window          Device on     |
|     mode=night              known=false         cmd received        storage.lumicam        RAM active    |
+--------------------------------------------------------------------------------------------------+
```

#### Incident Sequence of Events

| Time (Local: UTC+05:30) | Time (UTC) | Component / Location | Event Summary |
|---|---|---|---|
| **Day 1, 18:40:00** | Day 1, 13:10:00 | Camera (`camerad`) | Office closes; camera armed in `night` mode. |
| **Day 1, 23:55:02** | Day 1, 18:25:02 | Vendor Cloud API | Cloud service records authentication from an unrecognised session (`session=S-0002`, `known=false`). |
| **Day 2, 02:10:07** | Day 2, 20:40:07 | Cloud API / Config | Cloud API command received (`set_motion_alert=off`); camera configuration updated (`motion_alert old=on new=off`). |
| **Day 2, 02:14:11 – 02:31:15** | Day 2, 20:44:11 – 21:01:15 | Camera (`uploader`) | Three video clips (`clip_001`, `clip_002`, `clip_003`) recorded and uploaded to cloud endpoint. |
| **Day 2, 09:05:00** | Day 2, 03:35:00 | Physical Office | Owner discovers disabled alert and unapproved uploads; camera remains powered on. |

#### Synthetic System Profile

| Specification Category | System Parameter (SYNTHETIC) |
|---|---|
| **Target Device** | "LumiCam C2" Indoor Security Camera |
| **Manufacturer** | Brightwave Labs (fictional entity) |
| **Hardware Architecture** | Embedded 32-bit ARM SoC, 128 MB DDR3 RAM, 16 MB SPI NOR Flash, MicroSD slot |
| **Physical Interfaces** | Wi-Fi 802.11 b/g/n (2.4 GHz), Bluetooth LE (setup only), 3.3V UART serial header (unpopulated pins), No JTAG |
| **Operating System** | Embedded Linux (Kernel 4.9.x, BusyBox userland) |
| **Management App** | "LumiView" companion application (Android / iOS) |
| **Cloud Infrastructure** | `api.lumicam.example`, `storage.lumicam.example` (RFC 2606 reserved domains) |
| **Registered Account** | `owner-synth-01@example.org` |
| **Local Network** | `192.0.2.0/24`, Camera allocated `192.0.2.45` via DHCP (RFC 5737 documentation prefix) |

---

### 1.2 Forensic Question

> **Forensic Question:** Based on the evidence that can be lawfully acquired from the synthetic LumiCam C2 camera, its local network environment, its companion application, and associated cloud service records, what best explains the modification of the motion alert setting to OFF at 02:10 and the three video clip uploads between 02:14 and 02:31 on Day 2, and with what level of certainty?

#### Scope Boundaries
- **In Scope:** Technical examination of volatile memory on the live camera, non-volatile onboard flash storage, removable storage (MicroSD), router transaction logs and DHCP leases, mobile companion application artifacts, and vendor cloud API access logs.
- **Out of Scope:** Identification of real-world human actors, legal attribution of motive or intent, and investigation of any real third-party devices, cloud accounts, or proprietary networks.

---

### 1.3 Alternative Competing Hypotheses

To prevent premature confirmation bias, four competing hypotheses have been defined:

| ID | Hypothesis Name | Technical Description |
|:---:|---|---|
| **H1** | **Device Compromise** | The camera's operating system, runtime memory, or firmware was compromised by an unauthorized party via local interface (UART/network) or network exploit, bypassing vendor cloud controls. |
| **H2** | **Cloud Account Misuse** | An unauthorized third party obtained valid account credentials or hijacked an authentication token (`session=S-0002`) to issue legitimate cloud API commands to the camera. |
| **H3** | **Benign Malfunction** | A software defect, race condition, firmware corruption, or cloud synchronization retry fault triggered the configuration change and uploads without malicious user intervention. |
| **H4** | **Authorized User Action** | A legitimate authorized user (e.g., an office keyholder or family member with shared access) logged in, modified the setting, and triggered or allowed uploads, and subsequently forgot or failed to report the action. |

---

### 1.4 Expected Evidence Patterns

The table below outlines what evidence patterns would differentiate the four hypotheses:

| Evidence Source | Supports H1 (Device Compromise) | Supports H2 (Cloud Misuse) | Supports H3 (Benign Fault) | Supports H4 (Authorized User) |
|---|---|---|---|---|
| **Device Console / RAM (E1)** | Unlisted processes, spawned shell, modified binaries, no prior cloud command | Standard `cloud-agent` processes; clean execution of received cloud command | Crash logs, kernel panics, repeated sync retries, memory leak | Normal `cloud-agent` command receipt matching cloud session |
| **Router Logs (E2)** | Outbound connections to unauthorized non-vendor IPs | Exclusively legitimate TLS traffic to vendor endpoints (`lumicam.example`) | Intermittent dropped packets, DNS resolution retry bursts | Exclusively vendor endpoint traffic |
| **Flash Firmware (E3)** | SHA-256 hash differs from vendor gold image v2.3.1 | SHA-256 hash perfectly matches vendor release v2.3.1 | Firmware matches; or known buggy firmware block identified | Firmware hash matches vendor release |
| **MicroSD Card (E4)** | Staged exploit scripts, custom binaries, or orphaned video clips | Normal circular buffer clips with standard naming conventions | Corrupted file system headers, incomplete write fragments | Standard recorded clips matching app requests |
| **Mobile App (E5)** | No record of 23:55 login or 02:10 command on owner device | App shows no local action; login originated from an unrecognised foreign device | App shows synchronization error or retry loop | App local cache confirms login and setting modification from recognized handset |
| **Cloud API Logs (E6)** | No API record corresponding to the 02:10 configuration change | New IP/session (`S-0002`) authenticated at 23:55 issued `set_motion_alert` | Automated backend task or billing/maintenance sync event | Known user device/IP issued command via authenticated session |

---

## 2. Evidence Inventory & Volatility Analysis

### 2.1 System Architecture Map

```
+----------------------------------------------------------------------------------------------------+
|                                    EVIDENCE ARCHITECTURE MAP                                       |
|                                                                                                    |
|    +-----------------------------+                             +------------------------------+    |
|    |      LUMICAM C2 CAMERA      |                             |         VENDOR CLOUD         |    |
|    |                             |      D1: Wi-Fi Traffic      |                              |    |
|    |  +-----------------------+  |   (192.0.2.45 -> Router)    |  +------------------------+  |    |
|    |  |  RAM 128 MB (E1)      |  |                             |  | Cloud API (E6)         |  |    |
|    |  |  *Most Volatile*      |  |                             |  | api.lumicam.example    |  |    |
|    |  +-----------------------+  |                             |  +------------------------+  |    |
|    |  |  SPI Flash 16 MB (E3) |  |                             |  | Cloud Storage (E6)     |  |    |
|    |  |  Firmware v2.3.1      |  |                             |  | storage.lumicam.example|  |    |
|    |  +-----------------------+  |                             |  +------------------------+  |    |
|    |  |  MicroSD Card (E4)    |  |                             +--------------+---------------+    |
|    |  |  Local video / logs   |  |                                            ^                    |
|    |  +-----------------------+  |                                            | D4: HTTPS Admin    |
|    |  |  UART Header 3.3V     |  |                             +--------------+---------------+    |
|    |  +-----------+-----------+  |                             |   MOBILE COMPANION APP (E5)  |    |
|    +--------------|--------------+                             |   "LumiView" Application     |    |
|                   |                                            +------------------------------+    |
|                   | D6: Serial Read-Only Capture                              ^                    |
|                   v                                                           |                    |
|    +-----------------------------+                             +--------------+---------------+    |
|    |     EXAMINER WORKSTATION    |                             |     OFFICE ROUTER / GW (E2)  |    |
|    |   FTDI 3.3V UART Adapter    |                             |     192.0.2.1 / DHCP Server  |    |
|    +-----------------------------+                             +------------------------------+    |
+----------------------------------------------------------------------------------------------------+
```

### 2.2 System Component Specifications

| Component | Physical Type | Data Contained | Forensic Volatility | Interface / Access Method |
|---|---|---|:---:|---|
| **SoC / RAM** | 128 MB DDR3 | Running process table, active network sockets, temporary credentials, volatile `/tmp` logs | **High** (Lost upon power cutoff) | 3.3V UART serial console (live device) |
| **SPI Flash** | 16 MB SPI NOR | Bootloader (U-Boot), Linux kernel, rootfs, persistent `/etc/config` | **Low** (Non-volatile) | Physical desoldering or 8-pin SOIC clip with SPI programmer |
| **MicroSD** | Removable Flash | Buffered video clips, offline motion events, ring-buffer index | **Low** (Non-volatile) | Hardware write-blocked USB SD adapter |
| **UART Header** | 4-pin 0.1" pitch (3.3V) | Serial boot logs, live console shell (diagnostic output path) | **None** (Data path, not storage) | FTDI USB-to-UART bridge (TX/RX/GND, no VCC) |
| **Router** | Embedded Gateway | DHCP lease assignments, NAT connection states, DNS requests | **Medium** (Subject to circular log overwrite) | Administrative web interface export or mirror port |
| **Mobile App** | Smartphone Storage | Cached credentials, session tokens, local SQLite settings history | **Medium** (Subject to auto-sync overwrite) | Forensic logical/physical smartphone extraction |
| **Vendor Cloud** | Remote SaaS | Tenant authentication records, API command telemetry, S3 video objects | **Medium** (Subject to data retention schedules) | Legal preservation request / Authorized tenant export |

---

### 2.3 Evidence Hierarchy Ordered by Volatility (RFC 3227)

Following the standard order of volatility codified in **RFC 3227** (*Guidelines for Evidence Collection and Archiving*), collection must prioritize ephemeral sources over persistent storage:

```
[ Volatility 1: Highest ]  E1: Live Device RAM & Active Network Sockets (SoC)
           |
[ Volatility 2: High ]     E2: Router State, DHCP Tables, and Dynamic NAT Connections
           |
[ Volatility 3: Medium ]   E5: Companion Mobile App State & Cached Session Tokens
           |
[ Volatility 4: Medium ]   E6: Cloud API Transaction Logs & Video Object Metadata
           |
[ Volatility 5: Low ]      E4: Removable MicroSD Storage Media
           |
[ Volatility 6: Lowest ]   E3: Non-Volatile SPI NOR Flash Memory (Firmware & Configuration)
```

1. **E1 (Camera RAM):** Critical live state. Contains current processes, active network connections, and uncommitted log buffers. Lost completely if power is removed.
2. **E2 (Router Logs):** Volatile volatile routing states. DHCP leases and NAT translation tables expire quickly or overwrite under high traffic.
3. **E5 (Mobile App Data):** Local app state. May be overwritten if the device reconnects to the network and synchronizes.
4. **E6 (Cloud Telemetry):** Server-side logs. Retained according to vendor retention limits (often 7–30 days for consumer IoT).
5. **E4 (MicroSD Card):** Removable storage. Relatively stable, but subject to overwriting by camera loop-recording if left running.
6. **E3 (SPI Flash):** Non-volatile firmware. Highly stable; retains stored data indefinitely when powered off.

---

### 2.4 Data Flows

| Flow ID | Source | Destination | Protocol / Data Content | Forensic Significance |
|:---:|---|---|---|---|
| **D1** | Camera (`192.0.2.45`) | Router (`192.0.2.1`) | Wi-Fi / DHCP, DNS, HTTPS | Identifies connection timestamps, local IP allocation, and DNS resolution attempts. |
| **D2** | Router / WAN | Cloud API (`api.lumicam.example`) | HTTPS / Port 443 (REST/JSON) | Establishes whether the 02:10 setting change originated from the cloud platform. |
| **D3** | Camera (`uploader`) | Cloud Storage (`storage.lumicam.example`) | HTTPS / Port 443 (TLS Upload) | Confirms video transfer timestamps, payload volume, and target destination IP. |
| **D4** | Mobile App | Cloud API (`api.lumicam.example`) | HTTPS / Port 443 (OAuth/API) | Records which mobile device and session ID authenticated and issued commands. |
| **D5** | Mobile App | Camera | Bluetooth Low Energy (BLE) | Setup pairing only. Not used for routine operations (assumed inactive). |
| **D6** | Camera UART | Examiner Workstation | 115200 baud Serial / Text Console | Channel used by examiner to acquire volatile operating system state without network interference. |

---

## 3. Acquisition Plan & Risk Management

### 3.1 Planning Rules

1. **Strict Order of Volatility:** Evidence must be captured starting from the most ephemeral (E1) down to the most stable (E3).
2. **Preserve Originals:** Never perform analysis on raw evidence. Immediately duplicate via bit-stream imaging or write-protected export; conduct all testing on verified forensic copies.
3. **Immediate Cryptographic Hashing:** Compute and record SHA-256 hashes immediately upon acquisition of any artifact.
4. **Comprehensive Execution Logging:** Every tool name, version, command string, execution timestamp, and operator identity must be documented.
5. **Clock Drift Calibration:** Document the examiner workstation reference clock against the target device hardware clock before processing.
6. **Read-Only Enforcement:** Use hardware write-blockers for physical media and strictly read-only commands for serial console access.
7. **Legal & Ethical Authorization:** Ensure written authorization from the system owner is obtained before connecting to any device interface or accessing cloud records.

---

### 3.2 Decision Tree: Live vs. Powered-Off State

```
                          [ Physical Device Identified ]
                                         |
                                         v
                      [ Is the camera currently powered ON? ]
                                   /           \
                           YES    /             \   NO
                                 /               \
                                v                 v
                 [ Do NOT unplug / power off ]     [ Do NOT power on ]
                 [ Record clock discrepancy  ]     [ E1 (RAM) lost: log limitation ]
                                |                          |
                                v                          v
                 [ Can read-only UART be tapped? ]         |
                           /          \                    |
                   YES    /            \   NO              |
                         /              \                  |
                        v                v                 |
       +-----------------------+   +--------------------+  |
       | E1: Live RAM Capture  |   | Note limitation:   |  |
       | Run read-only commands|   | live state missed; |  |
       | Log all console I/O   |   | proceed to network |  |
       +-----------+-----------+   +---------+----------+  |
                   |                         |             |
                   +------------+------------+             |
                                |                          |
                                v                          |
               [ Network Isolation Required? ]             |
               [ Cut WAN at router; record time ]          |
                                |                          |
                                v                          |
               [ Controlled Shutdown of Device ]           |
               [ Label, photograph, disconnect ]           |
                                |                          |
                                v                          |
        +--------------------------------------------------+
        |
        v
  [ Non-Volatile Acquisition Sequence ]
   1. E2: Router connection logs & DHCP leases exported
   2. E3: Flash extraction via SOIC-8 clip & flashrom (read twice, compare hashes)
   3. E4: MicroSD card extracted via hardware write-blocker (dd / FTK Imager)
   4. E5: Mobile companion app logical backup (with consent)
   5. E6: Cloud API and S3 bucket metadata subpoena / export
        |
        v
  [ Hash all artifacts with SHA-256 & update Chain-of-Custody ]
```

---

### 3.3 Detailed Acquisition Plan

| ID | Evidence Source | Planned Method | Planned Tooling *(SYNTHETIC)* | Expected Artifact | Hashing & Validation | Legal / Authorization Requirement |
|:---:|---|---|---|---|---|---|
| **E1** | Camera RAM & Live State | Connect 3.3V serial adapter to UART. Execute read-only commands (`cat /proc/uptime`, `ps -ef`, `netstat -an`, `dmesg`). | Serial Terminal (`picocom` / `minicom`), USB-UART adapter *(Planned tool, not run)* | `console_ram_capture.txt` | Calculate SHA-256 immediately upon closing terminal session | System owner consent covering hardware connection |
| **E2** | Network State | Export DHCP leases, DNS request logs, and NAT session tables from router admin interface. | Router Admin Export, `tcpdump` / `Wireshark` *(Planned tool, not run)* | `router_dhcp_nat.log`, `capture.pcap` | SHA-256 of exported log files immediately after download | Network owner consent |
| **E3** | SPI NOR Flash | Power down device. Connect 8-pin SOIC clip to SPI flash. Perform two bit-stream reads. Compare hashes to ensure clean read. | `flashrom` v1.2+, CH341A / Dediprog programmer *(Planned tool, not run)* | `spi_flash_image.bin` | SHA-256 of Read 1 must match Read 2 exactly before processing | System owner consent covering device teardown |
| **E4** | MicroSD Card | Remove card from slot. Insert into hardware write-blocker. Perform raw bit-stream image (`dd` / raw image). | Tableau write-blocker, `dc3dd` / `FTK Imager` *(Planned tool, not run)* | `microsd_image.raw` | SHA-256 calculated of physical card and output image | System owner consent |
| **E5** | Mobile App | Perform authorized logical forensic backup of handset running LumiView companion app. | Android Backup Extractor / iOS backup tool *(Planned tool, not run)* | `lumiview_app_data.tar` | SHA-256 of backup container file | Smartphone owner consent; limited strictly to LumiView app sandbox |
| **E6** | Cloud Telemetry | Request account audit records, OAuth tokens, API call history, and S3 upload logs for target account. | Vendor Compliance Export Portal *(Planned procedure, not run)* | `cloud_api_audit.json`, `clip_metadata.csv` | SHA-256 of export archive upon receipt from vendor | Account owner consent / Vendor legal disclosure process |

---

### 3.4 Chain-of-Custody Template

```
================================================================================
                    DIGITAL EVIDENCE CHAIN-OF-CUSTODY FORM
      (Template Only - Illustrative Model for Synthetic Scenario DF-PBL-026)
================================================================================
Case Identifier       : DF-PBL-026 (IoT Forensic Plan)
Target Device Model   : LumiCam C2 Smart Security Camera
Target Serial / MAC   : [SYNTHETIC: 00:1A:2B:3C:4D:5E]
Lead Examiner         : DEEPTANSH NAGAR (Student ID: 500121033)

[EVIDENCE ITEM RECORD]
Item Number           : E-01
Item Description      : Volatile console and process memory capture text file
Acquisition Source    : 3.3V UART Header (camerad console)
Acquisition Date/Time : 2026-10-27T12:00:00Z (UTC)
Acquisition Tool      : Planned tool, not run (SYNTHETIC case)
Acquisition Command   : Planned procedure, not run (SYNTHETIC case)
Calculated SHA-256    : [Planned artifact - see synthetic test in Section 5]
Primary Storage Path  : [Secure Evidence Repository / Encrypted Volume]

[CUSTODY TRANSFER LOG]
Relinquished By (Name): [Unassigned - Custody Form Signature]   Date/Time: [Pending Transfer]
Received By (Name)    : [Evidence Custodian]                   Reason   : Initial Secure Storage
Storage Location      : Evidence Locker #2 (Digital Vault)

Relinquished By (Name): [Unassigned - Custody Form Signature]   Date/Time: [Pending Transfer]
Received By (Name)    : [Lead Examiner]                        Reason   : Forensic Working Copy
Storage Location      : Analysis Workstation (Read-Only Image)
================================================================================
*Note: Template only; no real physical collection was performed for this synthetic academic exercise.*
```

---

### 3.5 Risk Register & Mitigation Strategy

Scores are calculated as $\text{Likelihood} \times \text{Impact}$ on a 1–3 scale (1 = Low, 2 = Medium, 3 = High). Priority threshold is $\ge 6$.

| Risk ID | Description of Potential Failure | Likelihood (1–3) | Impact (1–3) | Score | Mitigation Strategy | Risk Owner | Residual Risk |
|:---:|---|:---:|:---:|:---:|---|:---:|---|
| **R1** | **Volatile RAM lost at power cut** | 2 | 3 | **6** | Keep device connected to uninterruptible power supply (UPS); label "DO NOT UNPLUG"; capture E1 over UART prior to shutdown. | Examiner | Medium (RAM contents may alter as device continues running). |
| **R2** | **Remote wipe / cloud sync overwrite** | 2 | 3 | **6** | Capture live network state (E2), then immediately block WAN routing at router level; request cloud preservation early. | Examiner | Medium (Network isolation disrupts active connections). |
| **R3** | **Firmware modified during extraction** | 1 | 3 | **3** | Enforce strictly read-only serial commands; read SPI flash with in-circuit clip twice and verify matching hashes. | Examiner | Low. |
| **R4** | **Hardware encryption or locked bootloader** | 2 | 3 | **6** | Check UART for root console prompt; if locked, pivot to non-volatile storage analysis (E2, E4, E5, E6). | Examiner | High (Hardware-level evidence may remain inaccessible). |
| **R5** | **Cloud legal & authorization limits** | 3 | 3 | **9** | Obtain written consent from account holder prior to analysis; request formal preservation letter to cloud vendor immediately. | Legal / Examiner | Medium (Vendor may reject request or prune logs after retention window). |
| **R6** | **Tool incompatibility or software fault** | 2 | 2 | **4** | Pre-test all open-source utilities against known synthetic fixtures; verify tool versions against documentation. | Examiner | Low to Medium. |
| **R7** | **Evidence contamination / alteration** | 2 | 3 | **6** | Employ physical write-blockers; immediately baseline raw evidence with SHA-256; perform all parsing on working copies. | Custodian | Low. |
| **R8** | **Clock drift and timezone confusion** | 3 | 3 | **9** | Compare device hardware clock with examiner NTP reference; convert all logged times to UTC while preserving original strings. | Examiner | Medium (Hardware RTC may have drifted non-linearly). |
| **R9** | **Chain-of-custody documentation gaps** | 2 | 2 | **4** | Maintain contemporaneous evidence log entries; use automated audit logging for all script executions. | Examiner | Low. |
| **R10**| **Accidental corruption of working copies** | 1 | 3 | **3** | Maintain dual copies in geographically separated secure storage; verify SHA-256 hash prior to each analysis session. | Custodian | Low. |
| **R11**| **Electrical overvoltage damage via UART** | 1 | 3 | **3** | Measure pin voltages with a multimeter prior to connection (ensure 3.3V logic level, not 5V); do not connect VCC lead. | Examiner | Low to Medium. |

```
                              RISK MATRIX HEATMAP
       +---------------------------------------------------------------+
       | High (3)   |         | R6, R9       | R5, R8 (Score 9)        |
       | Likelihood |         |              | R1, R2, R4, R7 (Score 6)|
       |------------+---------+--------------+-------------------------|
       | Med (2)    |         |              |                         |
       |------------+---------+--------------+-------------------------|
       | Low (1)    |         |              | R3, R10, R11 (Score 3)  |
       +---------------------------------------------------------------+
                    | Low (1) |  Medium (2)  |  High (3) - Impact      |
```

---

## 4. Analysis & Evidence Matrix

### 4.1 Evaluation Evidence Matrix

The evidence matrix separates **Observation** (raw factual data), **Interpretation** (what the data directly means), and **Inference** (what may be deduced regarding hypotheses), in accordance with the assignment rubric.

| Matrix ID | Factual Observation | Technical Interpretation | Forensic Inference | Supports / Contradicts | Confidence | Explicit Limitations |
|:---:|---|---|---|---|:---:|---|
| **M1** | Cloud audit log records a successful login at Day 1 23:55:02 UTC+05:30 with `session=S-0002 known=false`. | A new web/mobile session was authenticated against the cloud account. | An entity possessing valid credentials logged into the cloud platform; does not identify who controlled the session. | **Weakly supports H2, H4**; Neutral for H1, H3 | **Low** | "New session" is a vendor backend heuristic. No client IP, user-agent, or geographic location was provided in the log. |
| **M2** | Cloud API log records `CMD_RECEIVED` for `cmd=set_motion_alert value=off session=S-0002` at Day 2 02:10:07, matching camera `CONFIG_CHANGE`. | The setting was updated via an authenticated cloud command received by the device. | The setting change can be explained entirely through cloud API messaging without requiring local device exploitation. | **Consistent with H2, H4, H3** (if automated); Does not require H1 | **Low to Medium** | Does not prove the command was malicious or unintentional. Linking S-0002 to a specific device remains an assumption. |
| **M3** | Camera uploaded three video clips (`clip_001`, `clip_002`, `clip_003`) to `storage.lumicam.example` between 02:14:11 and 02:31:15. | The camera transmitted video payloads to the vendor's designated cloud storage endpoint. | Video uploads commenced 4 minutes after the configuration change. Demonstrates a temporal sequence, not causation. | **Compatible with all four hypotheses** (H1, H2, H3, H4) | **Low** | Clip contents were not inspected. Log does not indicate whether uploads were triggered by motion, schedule, or remote query. |
| **M4** | The office owner stated the office was unoccupied and they did not disable alerts or view clips. | The registered account holder disclaims initiating the configuration change or video export. | Weakly suggests the owner did not knowingly make the change, but cannot rule out forgotten actions or shared credentials. | **Weakly contradicts H4**; Consistent with H1, H2, H3 | **Low** | Verbal statement without independent technical corroboration. Untested for reliability or memory error. |
| **M5** | The camera was still powered on and operational at 09:05 when reported. | Volatile memory (E1) was not wiped by power cycling prior to reporting. | Live volatile state could theoretically be acquired if examined prior to power loss. | **Neutral** across all hypotheses | **Medium** | Reported by owner; exact state of volatile memory and kernel ring buffer remains unverified until acquired. |

---

### 4.2 Pending Artifacts Required for Definitive Attribution

Because the current synthetic case facts are high-level, definitive attribution cannot be made. The following pending artifacts (P1–P6) are needed:

```
  [ P1: Cloud Login IP & Device ID ] -------> Distinguishes H2 (Misuse) vs H4 (Authorized User)
  [ P2: Cloud Session Token Attribution ] --> Distinguishes H2 (Misuse) vs H3 (Malfunction)
  [ P3: Camera Console & Kernel Dmesg ] ----> Distinguishes H1 (Compromise) vs H3 (Malfunction)
  [ P4: SPI Flash Gold Hash Comparison ] ---> Proves or disproves H1 (Firmware tampering)
  [ P5: Router Outbound Packet Captures ] --> Identifies command-and-control traffic (H1)
  [ P6: Mobile Device Forensic Extraction ] -> Confirms whether owner device executed session S-0002
```

| ID | Pending Artifact | Technical Question It Resolves | Hypotheses Differentiated |
|:---:|---|---|:---:|
| **P1** | Cloud session IP & Device Fingerprint (E6) | Did session `S-0002` originate from a known owner device, known ISP, or an unrecognised foreign IP? | **H2 vs. H4** |
| **P2** | Cloud API Command Token Audit (E6) | Was the 02:10 `set_motion_alert` command issued by session `S-0002` or an internal maintenance script? | **H2 vs. H3 vs. H4** |
| **P3** | Live Console Process List & Socket Table (E1) | Was an unlisted process executing or listening on local ports at 02:10? | **H1 vs. H2 / H3** |
| **P4** | SPI Flash Bitstream Image Hash (E3) | Does the SHA-256 hash of the device firmware match the vendor v2.3.1 gold master? | **H1 vs. Others** |
| **P5** | Router Outbound Netflow / PCAP (E2) | Did the camera open unauthorized outbound connections to non-vendor IP addresses? | **H1 vs. Others** |
| **P6** | Companion Mobile App Database (E5) | Does the owner's handset cache contain OAuth tokens matching `S-0002`? | **H2 vs. H4** |

---

### 4.3 Analytical Assessment of Hypotheses

| Hypothesis | Current Finding Status | Technical Justification |
|---|:---:|---|
| **H1: Device Compromise** | **Untested (Not Ruled Out)** | No device-level artifacts (RAM, flash, router PCAP) have been physically acquired. While M2 shows the change was received via cloud API, local compromise could independently explain the video uploads. |
| **H2: Cloud Account Misuse** | **Slightly More Consistent** | Fits M1 (unrecognised session S-0002) and M2 (command issued via cloud API). However, without IP geolocation or token attribution, it cannot be differentiated from H4. |
| **H3: Benign Malfunction** | **Not Excluded** | Cloud backend glitches or scheduled tasks can alter settings. However, no error messages or crash loops appear in the high-level logs. |
| **H4: Authorized User Action** | **Not Excluded** | The new session at 23:55 could represent a legitimate secondary device (e.g., tablet, family member). Owner statement (M4) weakly contradicts this, but verbal statements carry low evidential weight. |

---

## 5. Reproducible Test (Technical Execution)

To fulfill the technical execution requirement, a standalone Python utility (`evidence_tool.py`) was developed using only standard library modules (`hashlib`, `argparse`, `json`, `datetime`, `pathlib`). The tool establishes a cryptographically verified SHA-256 baseline, validates evidence integrity prior to analysis, and processes synthetic log files into a normalized UTC timeline.

### 5.1 Tool Architecture & Command Set

| Command | Syntax | Primary Function | Hash-Gate Enforcement |
|---|---|---|:---:|
| `init` | `python evidence_tool.py init` | Hashes all files in `evidence/` and stores baseline in `evidence_log.json`. | Refuses overwrite without `--force`. |
| `verify` | `python evidence_tool.py verify` | Recalculates all file hashes and compares against baseline. | Returns exit code `0` (PASS) or `1` (FAIL). |
| `parse` | `python evidence_tool.py parse --file <path>` | Checks target file against baseline; parses if match; extracts flags. | **Refuses parsing if hash != baseline.** |

```
                       CALL-CHAIN FLOW & INTEGRITY GATE
   [ User Command ]
          |
          v
   [ cmd_init / cmd_verify / cmd_parse ]
          |
          +---> Calls: sha256_file()  [Reads in 64 KB chunks]
          |
   [ In cmd_parse: Hash-Gate Verification ]
          |
         / \
        /   \  Hash Match?
       /     \
     YES      NO ----> [ REFUSE PARSING ] ---> Logs "REFUSED" to evidence_log.json
      |
      v
   [ parse_log_file() ] ---> Strips comments, parses timezone, normalizes to UTC
      |
      v
   [ analyse() ] ----------> Applies 4 rule heuristics -> Generates observation flags
      |
      v
   [ record_action() ] ----> Appends UTC timestamp, CLI command, and result to log
      |
      v
   [ save_log() ] ---------> Writes updated evidence_log.json to disk
```

---

### 5.2 Terminal Execution Output (Real Machine Execution)

The following commands were executed in PowerShell on Windows using `Python 3.11.9`:

#### 1. Baseline Initialization (`init`)
```powershell
python evidence_tool.py init
```
```text
HASHED  camera_console_synthetic_A.log  ad1d0c5f2b7c80aff2ff6739173e5f14369561eb020b51d2476fdc495fe8ec4a
HASHED  camera_console_synthetic_B.log  36f1c40006de149f172b7a9ae8c70911aadc02f3713e3c2e7aa6183dd590a583
Baseline written to evidence_log.json
```

#### 2. Baseline Verification (`verify`)
```powershell
python evidence_tool.py verify
```
```text
OK        camera_console_synthetic_A.log
OK        camera_console_synthetic_B.log
OVERALL: PASS - all hashes match
```

#### 3. Parse Synthetic Log A (`parse`)
```powershell
python evidence_tool.py parse --file evidence/camera_console_synthetic_A.log
```
```text
File: camera_console_synthetic_A.log
SHA-256 now : ad1d0c5f2b7c80aff2ff6739173e5f14369561eb020b51d2476fdc495fe8ec4a
Integrity   : OK

Parsed 11 event(s); 1 malformed line(s) at line(s) [14]

Timeline (sorted by UTC)
UTC time             Local time as logged       Component    Event            Fields
2026-01-10 13:10:00  2026-01-10T18:40:00+05:30  camerad      ARMED            mode=night
2026-01-10 18:25:02  2026-01-10T23:55:02+05:30  cloud-agent  SESSION_SEEN     session=S-0002 known=false
2026-01-10 20:40:07  2026-01-11T02:10:07+05:30  cloud-agent  CMD_RECEIVED     cmd=set_motion_alert value=off session=S-0002
2026-01-10 20:40:07  2026-01-11T02:10:07+05:30  config       CONFIG_CHANGE    key=motion_alert old=on new=off
2026-01-10 20:44:11  2026-01-11T02:14:11+05:30  uploader     UPLOAD_START     clip=clip_001 dest=storage.lumicam.example
2026-01-10 20:44:40  2026-01-11T02:14:40+05:30  uploader     UPLOAD_DONE      clip=clip_001 dest=storage.lumicam.example
2026-01-10 20:52:05  2026-01-11T02:22:05+05:30  uploader     UPLOAD_START     clip=clip_002 dest=storage.lumicam.example
2026-01-10 20:52:33  2026-01-11T02:22:33+05:30  uploader     UPLOAD_DONE      clip=clip_002 dest=storage.lumicam.example
2026-01-10 21:00:48  2026-01-11T02:30:48+05:30  uploader     UPLOAD_START     clip=clip_003 dest=storage.lumicam.example
2026-01-10 21:01:15  2026-01-11T02:31:15+05:30  uploader     UPLOAD_DONE      clip=clip_003 dest=storage.lumicam.example
2026-01-11 03:35:00  2026-01-11T09:05:00+05:30  camerad      STATUS           state=running

Gap, first CONFIG_CHANGE to first UPLOAD_START: 4 min 4 s (timing only, not proof of cause)

Observation flags (consistent-with only, NOT proof)
  line 5   UNRECOGNISED_SESSION  session=S-0002 | A session is marked known=false | consistent with: H2, H4 (not proof)

NOTE: Flags are observations from fixed rules. They do not show who acted or why.
```

#### 4. Parse Synthetic Log B (Input Mutation Test)
```powershell
python evidence_tool.py parse --file evidence/camera_console_synthetic_B.log
```
```text
File: camera_console_synthetic_B.log
SHA-256 now : 36f1c40006de149f172b7a9ae8c70911aadc02f3713e3c2e7aa6183dd590a583
Integrity   : OK

Parsed 9 event(s); 0 malformed line(s)

Timeline (sorted by UTC)
UTC time             Local time as logged       Component    Event            Fields
2026-01-10 13:10:00  2026-01-10T18:40:00+05:30  camerad      ARMED            mode=night
2026-01-10 20:39:58  2026-01-11T02:09:58+05:30  sysmon       PROC_START       name=unknown_proc pid=412
2026-01-10 20:40:07  2026-01-11T02:10:07+05:30  config       CONFIG_CHANGE    key=motion_alert old=on new=off
2026-01-10 20:42:30  2026-01-11T02:12:30+05:30  net          CONN_OUT         dest=203.0.113.50 port=443
2026-01-10 20:44:11  2026-01-11T02:14:11+05:30  uploader     UPLOAD_START     clip=clip_001 dest=storage.lumicam.example
2026-01-10 20:44:40  2026-01-11T02:14:40+05:30  uploader     UPLOAD_DONE      clip=clip_001 dest=storage.lumicam.example
2026-01-10 20:52:05  2026-01-11T02:22:05+05:30  uploader     UPLOAD_START     clip=clip_002 dest=203.0.113.50
2026-01-10 20:52:33  2026-01-11T02:22:33+05:30  uploader     UPLOAD_DONE      clip=clip_002 dest=203.0.113.50
2026-01-11 03:35:00  2026-01-11T09:05:00+05:30  camerad      STATUS           state=running

Gap, first CONFIG_CHANGE to first UPLOAD_START: 4 min 4 s (timing only, not proof of cause)

Observation flags (consistent-with only, NOT proof)
  line 4   UNLISTED_PROCESS      name=unknown_proc | A process name is not in the allowed list | consistent with: H1 (not proof)
  line 5   CONFIG_WITHOUT_CMD    key=motion_alert new=off | Config change with no cloud command shortly before it | consistent with: H1, H3 (not proof)
  line 6   NON_VENDOR_DEST       dest=203.0.113.50 | Traffic to a destination outside the vendor domain | consistent with: H1 (not proof)
  line 9   NON_VENDOR_DEST       dest=203.0.113.50 | Traffic to a destination outside the vendor domain | consistent with: H1 (not proof)
  line 10  NON_VENDOR_DEST       dest=203.0.113.50 | Traffic to a destination outside the vendor domain | consistent with: H1 (not proof)

NOTE: Flags are observations from fixed rules. They do not show who acted or why.
```

---

### 5.3 Comparative Parsing Summary: Log A vs. Log B

| Metric / Flag | Synthetic Log A (Baseline Case) | Synthetic Log B (Altered Case) | Forensic Implication |
|---|:---:|:---:|---|
| **Total Events Parsed** | 11 events | 9 events | Confirms the parser reads actual file records rather than static templates. |
| **Malformed Lines** | 1 (line 14 deliberate error) | 0 malformed lines | Strict format validation successfully caught the corrupted line. |
| **Config-to-Upload Gap** | 4 min 4 s | 4 min 4 s | Consistent timing interval across both test runs. |
| **Flags Detected** | `UNRECOGNISED_SESSION` (line 5) | `UNLISTED_PROCESS` (line 4)<br>`CONFIG_WITHOUT_CMD` (line 5)<br>`NON_VENDOR_DEST` (lines 6, 9, 10) | Log A is consistent with cloud account interaction (H2/H4). Log B simulates local process hijacking and data exfiltration (H1). |

---

### 5.4 Controlled Tamper-Detection Demonstration

To prove that the integrity check functions as a strict gate:

#### Step 1: Tamper with Log A
```powershell
Add-Content evidence\camera_console_synthetic_A.log "# edit"
```

#### Step 2: Verification Failure
```powershell
python evidence_tool.py verify
```
```text
MISMATCH  camera_console_synthetic_A.log
OK        camera_console_synthetic_B.log
OVERALL: FAIL - evidence changed, missing, or unlisted
```
*(Process exit code: `1`)*

#### Step 3: Refusal to Parse Tampered File
```powershell
python evidence_tool.py parse --file evidence/camera_console_synthetic_A.log
```
```text
File: camera_console_synthetic_A.log
SHA-256 now : e10a4ebdcc2beec214ac697d5f20c6ced73533fdddcbe2e8c78eaae7306adf21
Integrity   : MISMATCH
Refusing to parse. Re-run 'verify', or use --allow-modified (this will be logged).
```
*(Process exit code: `1` — Analysis refused; evidence integrity preserved).*

#### Step 4: Restoration & Clean Verification
```powershell
Copy-Item ..\backup_A.log evidence\camera_console_synthetic_A.log -Force
python evidence_tool.py verify
```
```text
OK        camera_console_synthetic_A.log
OK        camera_console_synthetic_B.log
OVERALL: PASS - all hashes match
```
*(Process exit code: `0`)*

---

### 5.5 Audit Trail Excerpt (`evidence_log.json`)

The automated audit trail maintained in `evidence_log.json` records every command:

```json
{
  "case": "IoT Device Forensic Plan (SYNTHETIC)",
  "baseline": {
    "camera_console_synthetic_A.log": {
      "sha256": "ad1d0c5f2b7c80aff2ff6739173e5f14369561eb020b51d2476fdc495fe8ec4a",
      "size_bytes": 1259,
      "hashed_at_utc": "2026-10-27T12:22:21Z"
    },
    "camera_console_synthetic_B.log": {
      "sha256": "36f1c40006de149f172b7a9ae8c70911aadc02f3713e3c2e7aa6183dd590a583",
      "size_bytes": 853,
      "hashed_at_utc": "2026-10-27T12:22:21Z"
    }
  },
  "actions": [
    { "timestamp_utc": "2026-10-27T12:22:21Z", "command": "evidence_tool.py init", "result": "2 file(s) hashed" },
    { "timestamp_utc": "2026-10-27T12:22:29Z", "command": "evidence_tool.py verify", "result": "PASS" },
    { "timestamp_utc": "2026-10-27T12:22:34Z", "command": "evidence_tool.py parse --file evidence/camera_console_synthetic_A.log", "result": "DONE" },
    { "timestamp_utc": "2026-10-27T12:22:40Z", "command": "evidence_tool.py parse --file evidence/camera_console_synthetic_B.log", "result": "DONE" },
    { "timestamp_utc": "2026-10-27T12:34:46Z", "command": "evidence_tool.py verify", "result": "FAIL" },
    { "timestamp_utc": "2026-10-27T12:34:56Z", "command": "evidence_tool.py parse --file evidence/camera_console_synthetic_A.log", "result": "REFUSED (MISMATCH)" },
    { "timestamp_utc": "2026-10-27T12:35:11Z", "command": "evidence_tool.py verify", "result": "PASS" }
  ]
}
```

---

## 6. Limitations

The findings of this forensic plan and demonstration are constrained by the following technical and procedural limitations:

1. **Synthetic Nature of Artifacts:** All logs, IP addresses, session tokens, and file system records analyzed are entirely synthetic. Real-world IoT Linux environments exhibit asynchronous multi-threaded timing, kernel noise, interleaved syslog entries, and proprietary binary log structures that require dedicated reverse engineering.
2. **Device-Level Evidence Untested (H1 Open):** Because this exercise did not involve physical chip desoldering, flash extraction, or memory dumping on live hardware, hypothesis **H1 (Device Compromise) remains untested rather than disproven**. The absence of evidence of compromise in high-level logs cannot be taken as proof of security.
3. **Cryptographic Scope Limits:** A matching SHA-256 hash confirms only that a file has remained unaltered *since the exact moment it was first hashed*. It cannot prove that the file was authentic, complete, or uncompromised when it was initially created on the device.
4. **Heuristic Rule Constraints:** The four detection rules implemented in `evidence_tool.py` are simplified demonstration patterns. They are not an exhaustive intrusion detection system. Real attackers can disguise processes under allowed process names (e.g., masquerading as `camerad`) or channel exfiltration traffic through legitimate vendor endpoints.
5. **Clock Drift and Time Synchronization:** Real embedded devices experience real-time clock (RTC) drift, especially if NTP synchronization is blocked or erratic. Timestamps across cloud endpoints and IoT edge devices may have offsets that skew interval calculations.
6. **Plain JSON Audit Log Vulnerability:** Storing the evidence log as a local plaintext JSON file is vulnerable to deliberate alteration if the analyst workstation is compromised. In production forensics, integrity logs must be written to append-only media, a signed write-once ledger, or a centralized SIEM.

---

## 7. Qualified Conclusion

Based strictly on the synthetic artifacts evaluated in the Section 4 Evidence Matrix:

1. **Competing Hypotheses Cannot Be Definitive:** The available evidence cannot definitively isolate one single hypothesis among the four possibilities. 
2. **Cloud-Side Leaning (Weak Confidence):** The technical facts confirm that the motion alert setting was altered through a command issued via the cloud API (`CMD_RECEIVED` matching `CONFIG_CHANGE` at 02:10:07) following a newly authenticated session (`S-0002` at 23:55:02). This sequence is slightly more consistent with cloud-side account interaction (**H2: Cloud Account Misuse** or **H4: Authorized User Action**) than with an isolated on-device hardware compromise (**H1**).
3. **Device Compromise (H1) and Malfunction (H3) Not Excluded:** Because volatile RAM and SPI flash were not extracted, H1 is **untested, not excluded**. Similarly, backend cloud automation or synchronization failures (**H3**) could account for the setting change without human user interaction.
4. **The 4-Minute Gap is Not Proof of Causation:** The 4-minute 4-second interval between the setting change (02:10) and the first video upload (02:14) represents a temporal correlation only. It does not establish that the setting change caused the uploads or that the same actor initiated both events.
5. **Attribution Boundaries:** The findings do not name any individual, establish motive, or determine criminal intent. Forensic evidence demonstrates what state transitions occurred on the system; attribution of authorship requires corroborating external records.

### Next Steps for an Authentic Case
If this incident occurred on physical hardware:
- Acquire pending items **P1 to P6** in strict RFC 3227 order.
- Issue formal preservation letters to the cloud vendor for session `S-0002` ingress IP addresses and OAuth refresh token lineage.
- Conduct a bit-stream physical image of the SPI flash (E3) and compare with the vendor firmware v2.3.1 gold master image.
- Synchronize all hardware and cloud clocks to UTC and update the evidence matrix with physical artifacts before issuing a final forensic finding.

---

## 8. Verified References

The following authoritative technical standards and documentation were consulted to develop the methodology, volatility sequencing, hashing protocols, and technical implementation:

| No. | Full Citation & Document Title | Primary Application | Verification Status & Notes |
|:---:|---|---|---|
| **1** | **NIST SP 800-86**: *Guide to Integrating Forensic Techniques into Incident Response*. K. Kent, S. Chevalier, T. Grance, H. Dang. National Institute of Standards and Technology, August 2006. DOI: [10.6028/NIST.SP.800-86](https://doi.org/10.6028/NIST.SP.800-86) | Incident handling lifecycle; data acquisition from heterogeneous sources | **Verified** via NIST Computer Security Resource Center (CSRC). |
| **2** | **NIST SP 800-101 Rev. 1**: *Guidelines on Mobile Device Forensics*. R. Ayers, S. Brothers, W. Jansen. National Institute of Standards and Technology, May 2014. DOI: [10.6028/NIST.SP.800-101r1](https://doi.org/10.6028/NIST.SP.800-101r1) | Forensic preservation and logical extraction planning for companion app (E5) | **Verified** via NIST CSRC. |
| **3** | **ISO/IEC 27037:2012**: *Information technology — Security techniques — Guidelines for identification, collection, acquisition and preservation of digital evidence*. International Organization for Standardization / IEC, October 2012. | Core digital evidence handling principles, authenticity, and chain-of-custody | **Verified** via ISO Standards Catalogue. |
| **4** | **IETF RFC 3227**: *Guidelines for Evidence Collection and Archiving*. D. Brezinski, T. Killalea. Internet Engineering Task Force, February 2002. URL: [rfc-editor.org/rfc/rfc3227](https://www.rfc-editor.org/rfc/rfc3227) | Volatility hierarchy structuring the sequence of evidence collection (E1 $\to$ E6) | **Verified** via IETF RFC Editor. |
| **5** | **IETF RFC 2606**: *Reserved Top Level DNS Names*. D. Eastlake 3rd, A. Panitz. Internet Engineering Task Force, June 1999. URL: [rfc-editor.org/rfc/rfc2606](https://www.rfc-editor.org/rfc/rfc2606) | Specification for fictional `.example` top-level domains used in synthetic scenario | **Verified** via IETF RFC Editor. |
| **6** | **IETF RFC 5737**: *IPv4 Address Blocks Reserved for Documentation*. J. Arkko, M. Cotton, L. Vegoda. Internet Engineering Task Force, January 2010. URL: [rfc-editor.org/rfc/rfc5737](https://www.rfc-editor.org/rfc/rfc5737) | Documentation IP ranges (`192.0.2.0/24`, `203.0.113.0/24`) used in synthetic logs | **Verified** via IETF RFC Editor. |
| **7** | **NIST FIPS PUB 180-4**: *Secure Hash Standard (SHS)*. National Institute of Standards and Technology, August 2015. DOI: [10.6028/NIST.FIPS.180-4](https://doi.org/10.6028/NIST.FIPS.180-4) | Specification for SHA-256 cryptographic hashing used in baseline verification | **Verified** via NIST FIPS publications. |
| **8** | **NIST SP 800-30 Rev. 1**: *Guide for Conducting Risk Assessments*. National Institute of Standards and Technology, September 2012. DOI: [10.6028/NIST.SP.800-30r1](https://doi.org/10.6028/NIST.SP.800-30r1) | Likelihood and impact scoring methodology applied in Section 3.5 Risk Register | **Verified** via NIST CSRC. |
| **9** | **Python 3 Documentation**: *The Python Standard Library — Modules `hashlib`, `argparse`, `json`, `datetime`, `pathlib`* (v3.11.9). Python Software Foundation. URL: [docs.python.org/3.11/library/](https://docs.python.org/3.11/library/) | Technical implementation of reproducible test utility (`evidence_tool.py`) | **Verified** via official Python documentation. |
| **10**| **Hardware & Firmware Tooling Documentation**: *flashrom User Documentation* (`flashrom.org`), *picocom Serial Terminal Manual* (`github.com/npat-efault/picocom`), *Wireshark User Guide* (`wireshark.org`). | Procedural acquisition specifications for UART console, flash extraction, and network capture | **Verified** via project documentation portals. |

*(Note: Reference 11 for Mermaid diagram software was removed, as diagrams in this memo are presented using standard structured typographic layouts and ASCII architecture schematics).*

---

## 9. AI-Use Disclosure & Student Declaration

### 9.1 AI Assistance Disclosure

In accordance with academic integrity guidelines, generative AI assistance is disclosed as follows:

- **AI Tools Used:** Claude (Anthropic) and Gemini (Google).
- **Assistance Scope:** 
  - Assistance in drafting the synthetic IoT device incident scenario and parameter tables.
  - Development of the initial Python boilerplate code for `evidence_tool.py` (command-line argument parsing and SHA-256 file hashing logic).
  - Identification of relevant standard citations (NIST SP 800-86, RFC 3227, ISO/IEC 27037).
  - Editorial formatting of Markdown tables, risk registers, and call-chain diagrams.
- **Independent Student Verification:**
  - Configured and executed the Python environment (`Python 3.11.9` in Windows PowerShell).
  - Executed all live commands (`init`, `verify`, `parse`, tamper modification, restoration) directly on the local machine and captured real terminal stdout and return codes.
  - Independently verified each reference citation against NIST CSRC, IETF RFC Editor, and ISO public catalogues.
  - Re-evaluated analytical judgments to ensure that Hypothesis H1 is correctly maintained as "untested, not excluded", ensuring that forensic claims are defensible and not overstated.

### 9.2 Student Declaration

> **Student Declaration:**  
> "I, **DEEPTANSH NAGAR** (Student ID: **500121033**), hereby declare that this submission represents my own individual academic work for Project Code **DF-PBL-026** (*IoT Device Forensic Plan*). All technical commands, terminal outputs, cryptographic hashes, and tamper tests documented in Section 5 were personally executed and validated on my local workstation. I independently checked all literature citations, evaluated the forensic matrix without assuming guilt or intent, and can explain, demonstrate, and defend every function in `evidence_tool.py` and every decision in this investigation memo."

**Signed:**  
*Deeptansh Nagar*  
Date: October 27, 2026  
B.Tech Cyber Security / Digital Forensics  
Student ID: 500121033
