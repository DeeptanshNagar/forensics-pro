# IoT Device Forensic Plan: Reproducible Test (Step 7)

All data in this folder is **SYNTHETIC**. The device, vendor, domains, session IDs, IP address, and dates are fictional. No real device or account is involved.

## What the tool does

| Command | Purpose |
|---|---|
| `init` | Hashes every file in `evidence/` with SHA-256 and saves a **baseline** in `evidence_log.json` |
| `verify` | Hashes the files again and compares with the baseline (OK, MISMATCH, MISSING, or UNLISTED) |
| `parse` | Checks one log file's hash first, then parses it and prints a timeline and observation flags |

Every command also appends an entry to the evidence log with a UTC timestamp, the exact command line, and the result.

## Folder layout

```
iot_forensic_demo/
  evidence_tool.py
  README.md
  evidence/
    camera_console_synthetic_A.log   (SYNTHETIC log A, first input)
    camera_console_synthetic_B.log   (SYNTHETIC log B, second input for the live demo)
  evidence_log.json                  (created when you run init)
```

## Requirements
- Python 3.8 or newer. No extra packages are needed.
- Run all commands from inside the `iot_forensic_demo` folder.

**[STUDENT TO RUN AND PASTE]** Python version used: `python3 --version` -> ______

## Run commands

**1. Create the baseline**
```
python3 evidence_tool.py init
```
Expected output (the hashes are what YOUR run prints):
```
HASHED  camera_console_synthetic_A.log  <64-character SHA-256: STUDENT TO RUN AND PASTE>
HASHED  camera_console_synthetic_B.log  <64-character SHA-256: STUDENT TO RUN AND PASTE>
Baseline written to evidence_log.json
```
Running `init` a second time is refused on purpose (see "Why the tool refuses").

**2. Verify (rerun)**
```
python3 evidence_tool.py verify
```
Expected output:
```
OK        camera_console_synthetic_A.log
OK        camera_console_synthetic_B.log
OVERALL: PASS - all hashes match
```

**3. Parse log A**
```
python3 evidence_tool.py parse --file evidence/camera_console_synthetic_A.log
```
Expected result, as produced when I tested the supplied files (the SHA-256 line depends on the file and must come from your run):
- `Integrity   : OK`
- `Parsed 11 event(s); 1 malformed line(s) at line(s) [14]`
- Timeline with 11 events, sorted by UTC time
- `Gap, first CONFIG_CHANGE to first UPLOAD_START: 4 min 4 s (timing only, not proof of cause)`
- One flag: `UNRECOGNISED_SESSION  session=S-0002 ... consistent with: H2, H4 (not proof)`

**4. Parse log B (second input)**
```
python3 evidence_tool.py parse --file evidence/camera_console_synthetic_B.log
```
Expected result:
- `Parsed 9 event(s); 0 malformed line(s)`
- Flags: `UNLISTED_PROCESS` (unknown_proc), `CONFIG_WITHOUT_CMD` (motion_alert), and three `NON_VENDOR_DEST` (203.0.113.50), each marked "consistent with" H1 and/or H3, **not proof**.

**[STUDENT TO RUN AND PASTE]** your own terminal output for steps 1 to 4 into the report appendix.

## Live demo: changing the input

**Demo 1: switch to the second input file.** Run step 4 after step 3. The same code gives different flags because the log content is different. This shows the tool reads the evidence and does not have fixed answers.

**Demo 2: change a file and detect it.**
1. Add one line to log A. Linux or macOS: `echo "# edit" >> evidence/camera_console_synthetic_A.log`. Windows PowerShell: `Add-Content evidence\camera_console_synthetic_A.log "# edit"`.
2. Run `python3 evidence_tool.py verify`. Expected: `MISMATCH` for log A, `OVERALL: FAIL`, exit code 1.
3. Run `python3 evidence_tool.py parse --file evidence/camera_console_synthetic_A.log`. Expected: `Integrity   : MISMATCH` and `Refusing to parse`.
4. Remove the added line (or restore the original file) and run `verify` again. Expected: PASS.

**Demo 3: add an unlisted file.** Create any new file inside `evidence/` and run `verify`. Expected: `UNLISTED` for that file.

Every demo step is also recorded in `evidence_log.json`, so you can show the examiner the log after the demo.

## Explaining every function (for the viva)

| Function | What it does | Why it exists |
|---|---|---|
| `utc_now_iso()` | Returns the current time in UTC as text | All log entries use UTC so times from different sources can be compared (risk R8) |
| `sha256_file(path)` | Reads a file in 64 KB pieces and returns its SHA-256 hash | The hash is the file's fingerprint. Changing even one character changes it completely |
| `list_files(folder)` | Lists all files in the evidence folder, sorted | Finds files that are not in the baseline (UNLISTED) |
| `load_log()` / `save_log()` | Read and write the JSON evidence log | The log is the record of what was hashed and done |
| `record_action()` | Adds one entry with UTC time, the exact command typed, and the result | Another person can repeat the work from the log (assignment rule 4) |
| `cmd_init()` | Creates the baseline. Refuses to overwrite it unless `--force` is used | Stops the "original" fingerprints from being replaced by accident |
| `check_files()` | Compares current hashes with the baseline | The core integrity check. Returns OK, MISMATCH, MISSING, or UNLISTED |
| `cmd_verify()` | Runs `check_files()`, prints the result, logs it, and returns exit code 0 only on PASS | Gives a clear pass or fail, usable in scripts or CI |
| `parse_line()` | Splits one log line into time, component, event, and key=value fields. Rejects bad lines and times without a timezone | Keeps parsing strict so errors are visible and not hidden |
| `parse_log_file()` | Reads the file line by line, skips comments, counts bad lines, sorts events by UTC time | Gives a correct timeline even if the log is out of order |
| `analyse()` | Applies four fixed rules and returns flags | Produces observations in a repeatable way. It does not decide who acted |
| `format_minutes()` | Converts seconds to "X min Y s" | Readable output for the gap calculation |
| `cmd_parse()` | Checks the file hash first. Refuses to parse if it does not match. Then prints the timeline, gap, and flags, and logs the result | Evidence integrity is checked **before** analysis |
| `build_parser()` / `main()` | Define the command-line options and start the program | Make `init`, `verify`, and `parse` available from the terminal |

**The four flag rules**

| Flag | Rule | Consistent with |
|---|---|---|
| `UNRECOGNISED_SESSION` | A `SESSION_SEEN` line has `known=false` | H2, H4 |
| `CONFIG_WITHOUT_CMD` | A `CONFIG_CHANGE` has no `CMD_RECEIVED` in the 60 seconds before it | H1, H3 |
| `UNLISTED_PROCESS` | A `PROC_START` name is not in `ALLOWED_PROCS` | H1 |
| `NON_VENDOR_DEST` | A `dest=` value does not end with `.lumicam.example` | H1 |

"Consistent with" means the pattern is compatible with that hypothesis. It is **not proof**. Several hypotheses can be consistent with the same flag.

## Why the tool refuses
- `init` refuses to replace an existing baseline, so the original fingerprints are protected.
- `parse` refuses to analyse a file whose hash does not match, so analysis is never done on evidence that may have changed. `--allow-modified` exists for testing and is written to the log.

## Log format used by the SYNTHETIC files
```
timestamp | component | event | key=value key=value
```
Timestamps include a timezone offset. **Assumption:** device clock is local time at +05:30 and the dates are SYNTHETIC. The parser converts every time to UTC.

## Limitations of this artefact
- The log format is invented for this assignment. Real device logs have different formats and need their own parser.
- The four rules are simple and can miss real problems or flag harmless events.
- A matching SHA-256 hash shows the file is unchanged **since it was hashed**. It does not show the file was correct or complete when collected.
- The evidence log is a plain JSON file. It is not tamper-proof. Anyone with access could edit it, so a real case would store a copy of the baseline hashes separately (for example in a signed or printed record).
- The tool does not link the device log to cloud logs automatically.

## Sources to verify
- NIST SP 800-86 and ISO/IEC 27037, for the practice of hashing and documenting evidence. **[STUDENT TO VERIFY]**
- FIPS 180-4, *Secure Hash Standard*, for SHA-256. **[STUDENT TO VERIFY]**
- Python documentation for `hashlib`, `argparse`, `json`, and `datetime`. **[STUDENT TO VERIFY version]**
- RFC 5737, for the 203.0.113.0/24 documentation address range used in log B. **[STUDENT TO VERIFY]**

## AI-use disclosure (Step 7)
This script, the two SYNTHETIC log files, and this README were drafted with the help of an AI assistant (Claude). The AI also ran the script once in its own test environment to check that it works. The student must run it again, paste their own output, review every function, and be able to defend and modify the code.
