# 5 to 8 Minute Defense & Video Demonstration Guide (Video Bytes)

**Student Name:** DEEPTANSH NAGAR  
**Student ID:** 500121033  
**Project Code:** DF-PBL-026  
**Format:** Investigation Memo & Controlled Demonstration  
**Target Duration:** 7 minutes (Allowed: 5 to 8 minutes)  

---

## 1. Video Recording Setup & Preparation

### Tools to Record
- **Windows Game Bar (Built-in):** Press **`Windows Key + G`**, click the **Record** button (or press `Win + Alt + R`).
- **Alternative:** OBS Studio, or open a solo meeting in Zoom/Teams and click **Record to this computer**.

### Screen Layout Before You Hit Record
1. **Left Half (or Window 1):** Have your PDF report [`IoT_Device_Forensic_Plan_Deeptansh_Nagar.pdf`](file:///c:/Users/HP/OneDrive/Desktop/iot_forensic_demo/IoT_Device_Forensic_Plan_Deeptansh_Nagar.pdf) or [`INVESTIGATION_MEMO.html`](file:///c:/Users/HP/OneDrive/Desktop/iot_forensic_demo/INVESTIGATION_MEMO.html) open to the diagrams.
2. **Right Half (or Window 2):** Open PowerShell in `c:\Users\HP\OneDrive\Desktop\iot_forensic_demo\`. Make the terminal font size comfortable (e.g., 18pt or 20pt) so hashes are easily legible on video.
3. **Pre-test State:** Ensure `evidence/` is clean before starting:
   ```powershell
   python evidence_tool.py verify
   # Should output: OVERALL: PASS - all hashes match
   ```

---

## 2. Word-for-Word Spoken Script (Timeline: 7:30)

---

### [0:00 – 0:45] Problem Framing & Synthetic Scenario
> **What to show on screen:** Display the **Title** and **Section 1.1 Incident Timeline** in the PDF/HTML memo.
>
> **What to say:**  
> *"Hello, my name is Deeptansh Nagar, Student ID 500121033. Today I am presenting my Investigation Memo for Project Code DF-PBL-026: IoT Device Forensic Plan.*  
>  
> *First, as required by the assignment rules, I want to explicitly state that all devices, networks, logs, and vendor names in this case are completely **SYNTHETIC**. No real third-party account or physical device was investigated.*  
>  
> *The scenario begins when an office administrator reports that their LumiCam C2 security camera uploaded three video clips between 02:14 and 02:31 while the office was empty. In the morning, they discovered that motion alert notifications had been switched to OFF. Our forensic question is: what technical evidence explains this setting change and the subsequent video uploads, and with what level of confidence?"*

---

### [0:45 – 1:30] Competing Hypotheses
> **What to show on screen:** Scroll to **Section 1.3 Hypotheses Table** (Page 4 of PDF).
>
> **What to say:**  
> *"To avoid confirmation bias, we evaluated four competing alternative hypotheses:*  
> *• **H1: Device Compromise** — where the camera's local software, firmware, or runtime memory was exploited by an unauthorized party.*  
> *• **H2: Cloud Account Misuse** — where credentials or session tokens were stolen, and commands were issued legitimately through the cloud platform.*  
> *• **H3: Benign Malfunction** — an automated cloud sync loop or firmware race condition that caused an unintended setting switch and upload.*  
> *• **H4: Authorized User Action** — where a legitimate user made the change and forgot or didn't report it.*  
>  
> *As shown in our expected patterns table, each hypothesis requires distinct physical or logical evidence to separate them."*

---

### [1:30 – 3:30] Architecture Map, Volatility Hierarchy & Decision Tree
> **What to show on screen:** Show **Section 2.1 Architecture Map** (Page 6) and **Section 3.2 Decision Tree** (Page 10).
>
> **What to say:**  
> *"Looking at our Architecture Map, the LumiCam C2 contains a 32-bit ARM SoC, 128 MB RAM, 16 MB SPI flash, and a MicroSD slot, connected via Wi-Fi to a local router and the vendor cloud.*  
>  
> *Because evidence deteriorates over time, we structure our acquisition plan strictly according to **RFC 3227: Order of Volatility**:*  
> *1. Camera RAM (E1) is the most volatile: it will vanish instantly if power is disconnected.*  
> *2. Next are router DHCP and NAT connection states (E2).*  
> *3. Then mobile companion app data (E5) and cloud transaction records (E6).*  
> *4. Finally, persistent non-volatile media: the MicroSD card (E4) and SPI flash firmware (E3).*  
>  
> *Our On/Off Decision Tree dictates that because the camera was reported still powered on, we do **not** power off the device. We tap the 3.3V UART serial header in a read-only state to capture live volatile memory and processes before network isolation or controlled shutdown."*

---

### [3:30 – 5:15] Risk Register & Evidence Matrix
> **What to show on screen:** Show **Section 3.5 Risk Heatmap** (Page 14) and **Section 4.1 Evidence Matrix** (Page 17).
>
> **What to say:**  
> *"In our Risk Register, two risks reach the maximum priority score of 9: R5 (Cloud legal and authorization limits) and R8 (Clock drift and timezone confusion).*  
>  
> *In our Evidence Matrix, we strictly separate **Observation**, **Interpretation**, and **Inference**:*  
> *• Artifact M1 shows a new cloud session S-0002 was logged at 23:55.*  
> *• Artifact M2 confirms a `CMD_RECEIVED` message over the cloud API changed motion alerts to OFF at 02:10.*  
> *• Artifact M3 records the three video uploads starting at 02:14.*  
>  
> *A critical forensic point here: the 4-minute gap between the setting change and the first upload is **timing only**, not proof of causation. Because the command came through the cloud API, the current facts lean weakly toward cloud-side interaction (H2 or H4). However, because we have not physically acquired the camera's RAM or SPI flash, **H1 (Device Compromise) remains untested, not excluded**."*

---

### [5:15 – 6:30] LIVE TERMINAL DEMONSTRATION (Crucial Step!)
> **What to show on screen:** Switch focus to your **PowerShell Terminal Window**.
>
> **What to say & do (Execute step-by-step):**  

**1. Baseline Verification:**
> *Say:* *"Now I will demonstrate our reproducible forensic tool, `evidence_tool.py`, built using Python 3.11 with standard library modules. First, I run verify against our cryptographic baseline:"*
```powershell
python evidence_tool.py verify
```
> *Say:* *"The tool re-hashes all files with SHA-256 and outputs `OVERALL: PASS - all hashes match`."*

**2. Parse Synthetic Log A (Baseline Case):**
> *Say:* *"Next, we parse Log A. Notice that the tool verifies the file hash BEFORE parsing:"*
```powershell
python evidence_tool.py parse --file evidence/camera_console_synthetic_A.log
```
> *Say:* *"The tool parses 11 events and successfully identifies our deliberate malformed line at line 14. It calculates the 4 min 4 s gap and raises one observation flag: `UNRECOGNISED_SESSION`, consistent with H2 or H4."*

**3. Parse Synthetic Log B (Input Mutation Test):**
> *Say:* *"To prove the script adapts to evidence and does not have hardcoded answers, we parse our second input file, Log B:"*
```powershell
python evidence_tool.py parse --file evidence/camera_console_synthetic_B.log
```
> *Say:* *"The same code now flags 5 anomalies: an unlisted process `unknown_proc`, a config change without prior cloud command, and three non-vendor destination IP connections to 203.0.113.50, consistent with hypothesis H1."*

**4. Tamper Test & Refusal Gate:**
> *Say:* *"Now, we demonstrate our integrity protection. I will simulate unauthorized tampering by appending an edit line to Log A:"*
```powershell
Add-Content evidence\camera_console_synthetic_A.log "# edit"
python evidence_tool.py verify
```
> *Say:* *"Immediately, the tool catches the modification: `MISMATCH` on Log A, `OVERALL: FAIL`, exiting with code 1. Now watch what happens if an analyst tries to parse this modified file:"*
```powershell
python evidence_tool.py parse --file evidence/camera_console_synthetic_A.log
```
> *Say:* *"The integrity gate refuses to parse: `Refusing to parse`. It strictly prevents analysis on contaminated evidence."*

**5. Clean Restoration & Re-verify:**
> *Say:* *"Finally, we restore the original clean file from our verified backup and re-verify:"*
```powershell
Copy-Item ..\backup_A.log evidence\camera_console_synthetic_A.log -Force
python evidence_tool.py verify
```
> *Say:* *"The baseline passes again: `OVERALL: PASS`. Every single one of these actions was automatically logged to `evidence_log.json` with UTC timestamps."*

---

### [6:30 – 7:30] Limitations, Conclusion & Student Declaration
> **What to show on screen:** Switch back to the PDF/HTML memo, showing **Section 6 Limitations** and **Section 9 Student Declaration**.
>
> **What to say:**  
> *"To conclude:*  
> *1. **Explicit Limitations:** All data is synthetic; heuristic flags are observations, not proof; and a SHA-256 match proves only that files have not changed since hashing, not their state when acquired.*  
> *2. **Qualified Conclusion:** With the current evidence, the four hypotheses cannot be separated. The facts lean weakly toward cloud-side interaction, but H1 and H3 remain open until physical artifacts P1 through P6 can be acquired.*  
>  
> *3. **Student Declaration:** I, Deeptansh Nagar (500121033), declare that I ran the tools, verified the references, conducted the live tamper demonstration on my machine, and authored this memo.*  
>  
> *Thank you, and I welcome any questions."*

---

## 3. What to Demonstrate in the Video (Summary Checklist)

1. **The PDF Document Overview:** Show the 7-step overview, timeline, architecture map, and risk heatmap.
2. **The Command Line (Terminal):**
   - `python evidence_tool.py verify` $\to$ Show `OVERALL: PASS`.
   - `python evidence_tool.py parse --file evidence/camera_console_synthetic_A.log` $\to$ Show UTC timeline, line 14 malformed line catch, and `UNRECOGNISED_SESSION` flag.
   - `python evidence_tool.py parse --file evidence/camera_console_synthetic_B.log` $\to$ Show that changing the input produces different flags (`UNLISTED_PROCESS`, `NON_VENDOR_DEST`).
   - Tamper demonstration: Add `# edit` to Log A $\to$ Show `MISMATCH` and parse `REFUSED`.
   - Restore clean Log A $\to$ Show `OVERALL: PASS`.
3. **The Audit Trail:** Briefly open `evidence_log.json` to show that the FAIL and PASS actions are recorded contemporaneously.
4. **The Conclusion & Sign-Off:** Show your name (**DEEPTANSH NAGAR**) and declaration at the end of the PDF.

---

## 4. Top 5 Questions an Examiner Might Ask & How to Answer

1. **Q: Why does the parser refuse to parse when there is a mismatch?**  
   *A:* In digital forensics, conducting analysis on evidence that has been modified or corrupted post-collection compromises the integrity of findings. Enforcing a hash check prior to parsing ensures forensic soundness.

2. **Q: Why can't you eliminate Hypothesis H1 (Device Compromise)?**  
   *A:* Because we have not acquired the device's volatile RAM or dumped the SPI flash image, we cannot verify whether unauthorized rootkits, memory injection, or rogue daemons were present on the physical camera.

3. **Q: What does the 4-minute gap between setting change and upload mean?**  
   *A:* It proves temporal sequence, not causation. A common forensic trap is *post hoc ergo propter hoc*. Only corroborated system logs or API call correlation can prove whether the setting change triggered the uploads.

4. **Q: Why did you remove Reference 11 (Mermaid)?**  
   *A:* The report diagrams are rendered directly as structured visual layouts and ASCII architecture maps, rather than relying on an external Mermaid rendering dependency.

5. **Q: What is the significance of line 14 in Log A?**  
   *A:* It proves that the parser performs strict input validation and defensive error handling—it isolates and reports malformed entries without crashing or discarding the rest of the timeline.
