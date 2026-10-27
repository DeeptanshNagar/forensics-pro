#!/usr/bin/env python3
"""
evidence_tool.py - small evidence-integrity and log-parsing tool.

Used ONLY with SYNTHETIC data for the "IoT Device Forensic Plan" assignment.

Commands:
  init    Hash every file in the evidence folder (SHA-256) and write a baseline
          into the evidence log.
  verify  Re-hash every file and compare with the baseline.
  parse   Check one log file's hash first, then parse it and print observations.

Every command appends an entry (timestamp, command line, result) to the log.
Standard library only. Tested on Python 3.8 or newer.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

CHUNK_SIZE = 65536                      # read files in 64 KB pieces
VENDOR_SUFFIX = ".lumicam.example"      # SYNTHETIC vendor domain
ALLOWED_PROCS = {"camerad", "cloud-agent", "uploader", "busybox"}
CMD_WINDOW_SECONDS = 60                 # a config change needs a cloud command this close before it

# Flag name -> (what was observed, which hypotheses it is CONSISTENT WITH, not proof)
FLAG_INFO = {
    "UNRECOGNISED_SESSION": ("A session is marked known=false", "H2, H4 (not proof)"),
    "CONFIG_WITHOUT_CMD": ("Config change with no cloud command shortly before it", "H1, H3 (not proof)"),
    "UNLISTED_PROCESS": ("A process name is not in the allowed list", "H1 (not proof)"),
    "NON_VENDOR_DEST": ("Traffic to a destination outside the vendor domain", "H1 (not proof)"),
}


# ---------------------------------------------------------------- helpers
def utc_now_iso():
    """Return the current time in UTC, e.g. 2026-01-12T10:00:00Z."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path):
    """Return the SHA-256 hash of a file as a 64-character hex string.
    The file is read in chunks so large files do not fill memory."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def list_files(folder):
    """Return all files under the folder as sorted paths relative to it.
    Posix-style names (with /) are used so the log is the same on every OS."""
    folder = Path(folder)
    return sorted(p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file())


# ---------------------------------------------------------------- evidence log
def load_log(log_path):
    """Load the evidence log, or create an empty one in memory if the file does not exist."""
    p = Path(log_path)
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"case": "IoT Device Forensic Plan (SYNTHETIC)", "baseline": {}, "actions": []}


def save_log(log, log_path):
    """Write the evidence log to disk as readable JSON."""
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)


def record_action(log, action, result, details=None):
    """Append one entry: when it happened (UTC), the exact command line, and the result."""
    entry = {
        "timestamp_utc": utc_now_iso(),
        "command": " ".join(sys.argv),
        "action": action,
        "result": result,
    }
    if details:
        entry["details"] = details
    log["actions"].append(entry)


# ---------------------------------------------------------------- init / verify
def cmd_init(args):
    """Create the baseline: hash every evidence file and store it in the log.
    An existing baseline is not replaced unless --force is given, so the
    'original' fingerprints cannot be changed by accident."""
    log = load_log(args.log)
    if log["baseline"] and not args.force:
        print("Baseline already exists. Use --force only if you are sure (this is recorded in the log).")
        return 2
    files = list_files(args.evidence)
    if not files:
        print("No files found in the evidence folder.")
        return 2
    baseline = {}
    for name in files:
        path = Path(args.evidence) / name
        baseline[name] = {
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
            "hashed_at_utc": utc_now_iso(),
        }
        print(f"HASHED  {name}  {baseline[name]['sha256']}")
    log["baseline"] = baseline
    record_action(log, "init" + (" --force" if args.force else ""), f"{len(files)} file(s) hashed")
    save_log(log, args.log)
    print(f"Baseline written to {args.log}")
    return 0


def check_files(evidence_dir, baseline):
    """Compare the current files with the baseline.
    Returns a dict name -> OK / MISMATCH / MISSING / UNLISTED."""
    results = {}
    for name, info in baseline.items():
        path = Path(evidence_dir) / name
        if not path.exists():
            results[name] = "MISSING"
        elif sha256_file(path) == info["sha256"]:
            results[name] = "OK"
        else:
            results[name] = "MISMATCH"
    for name in list_files(evidence_dir):
        if name not in baseline:
            results[name] = "UNLISTED"
    return results


def cmd_verify(args):
    """Re-hash all files and report. Exit code 0 only if every file is OK."""
    log = load_log(args.log)
    if not log["baseline"]:
        print("No baseline found. Run 'init' first.")
        return 2
    results = check_files(args.evidence, log["baseline"])
    for name, status in sorted(results.items()):
        print(f"{status:9} {name}")
    all_ok = all(s == "OK" for s in results.values())
    record_action(log, "verify", "PASS" if all_ok else "FAIL", results)
    save_log(log, args.log)
    print("OVERALL:", "PASS - all hashes match" if all_ok else "FAIL - evidence changed, missing, or unlisted")
    return 0 if all_ok else 1


# ---------------------------------------------------------------- parsing
def parse_line(line):
    """Parse one log line of the form:
       timestamp | component | event | key=value key=value
    Returns a dict, or None if the line does not fit (comments, blanks, bad lines)."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    parts = [p.strip() for p in line.split("|")]
    if len(parts) != 4:
        return None
    ts_text, component, event, kv_text = parts
    try:
        ts = datetime.fromisoformat(ts_text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if ts.tzinfo is None:
        return None  # a time without a timezone is rejected (see risk R8)
    fields = {}
    for item in kv_text.split():
        if "=" in item:
            k, v = item.split("=", 1)
            fields[k] = v
    return {
        "local_time": ts_text,
        "utc": ts.astimezone(timezone.utc),
        "component": component,
        "event": event,
        "fields": fields,
    }


def parse_log_file(path):
    """Read a log file. Returns (events sorted by UTC time, list of bad line numbers).
    Comment lines starting with # are skipped and are not counted as bad."""
    events, bad = [], []
    with open(path, "r", encoding="utf-8") as f:
        for number, line in enumerate(f, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            ev = parse_line(line)
            if ev is None:
                bad.append(number)
            else:
                ev["line"] = number
                events.append(ev)
    events.sort(key=lambda e: e["utc"])
    return events, bad


def analyse(events):
    """Apply simple fixed rules and return a list of (flag, line number, detail).
    These are OBSERVATIONS only. They do not prove a hypothesis."""
    flags = []
    cmd_times = [e["utc"] for e in events if e["event"] == "CMD_RECEIVED"]
    for e in events:
        f = e["fields"]
        if e["event"] == "SESSION_SEEN" and f.get("known") == "false":
            flags.append(("UNRECOGNISED_SESSION", e["line"], f"session={f.get('session')}"))
        if e["event"] == "CONFIG_CHANGE":
            recent = [t for t in cmd_times if 0 <= (e["utc"] - t).total_seconds() <= CMD_WINDOW_SECONDS]
            if not recent:
                flags.append(("CONFIG_WITHOUT_CMD", e["line"], f"key={f.get('key')} new={f.get('new')}"))
        if e["event"] == "PROC_START" and f.get("name") not in ALLOWED_PROCS:
            flags.append(("UNLISTED_PROCESS", e["line"], f"name={f.get('name')}"))
        dest = f.get("dest")
        if dest and not dest.endswith(VENDOR_SUFFIX):
            flags.append(("NON_VENDOR_DEST", e["line"], f"dest={dest}"))
    return flags


def format_minutes(seconds):
    """Turn seconds into 'X min Y s' for printing."""
    return f"{int(seconds // 60)} min {int(seconds % 60)} s"


def cmd_parse(args):
    """Verify the file's hash against the baseline, then parse and report.
    If the hash does not match, parsing is refused unless --allow-modified is given."""
    log = load_log(args.log)
    file_path = Path(args.file)
    if not file_path.exists():
        print("File not found.")
        return 2
    try:
        rel = file_path.resolve().relative_to(Path(args.evidence).resolve()).as_posix()
    except ValueError:
        print("The file must be inside the evidence folder.")
        return 2

    current = sha256_file(file_path)
    expected = log["baseline"].get(rel, {}).get("sha256")
    if expected is None:
        integrity = "NO BASELINE"
    elif expected == current:
        integrity = "OK"
    else:
        integrity = "MISMATCH"
    print(f"File: {rel}")
    print(f"SHA-256 now : {current}")
    print(f"Integrity   : {integrity}")
    if integrity != "OK" and not args.allow_modified:
        print("Refusing to parse. Re-run 'verify', or use --allow-modified (this will be logged).")
        record_action(log, "parse", f"REFUSED ({integrity})", {"file": rel, "sha256_now": current})
        save_log(log, args.log)
        return 1

    events, bad = parse_log_file(file_path)
    print(f"\nParsed {len(events)} event(s); {len(bad)} malformed line(s)" + (f" at line(s) {bad}" if bad else ""))
    print("\nTimeline (sorted by UTC)")
    print(f"{'UTC time':20} {'Local time as logged':26} {'Component':12} {'Event':16} Fields")
    for e in events:
        fields = " ".join(f"{k}={v}" for k, v in e["fields"].items())
        print(f"{e['utc'].strftime('%Y-%m-%d %H:%M:%S'):20} {e['local_time']:26} {e['component']:12} {e['event']:16} {fields}")

    first_cfg = next((e for e in events if e["event"] == "CONFIG_CHANGE"), None)
    first_up = next((e for e in events if e["event"] == "UPLOAD_START"), None)
    if first_cfg and first_up:
        gap = (first_up["utc"] - first_cfg["utc"]).total_seconds()
        print(f"\nGap, first CONFIG_CHANGE to first UPLOAD_START: {format_minutes(gap)} (timing only, not proof of cause)")

    flags = analyse(events)
    print("\nObservation flags (consistent-with only, NOT proof)")
    if not flags:
        print("  none")
    for flag, line_no, detail in flags:
        what, hyp = FLAG_INFO[flag]
        print(f"  line {line_no:<3} {flag:21} {detail} | {what} | consistent with: {hyp}")

    print("\nNOTE: Flags are observations from fixed rules. They do not show who acted or why.")
    record_action(log, "parse", "DONE", {
        "file": rel, "integrity": integrity, "sha256_now": current,
        "events": len(events), "malformed_lines": bad, "flags": [f[0] for f in flags],
    })
    save_log(log, args.log)
    return 0


# ---------------------------------------------------------------- entry point
def build_parser():
    """Define the command-line options."""
    p = argparse.ArgumentParser(description="SYNTHETIC evidence integrity and log parsing demo")
    sub = p.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--evidence", default="evidence", help="evidence folder (default: evidence)")
    common.add_argument("--log", default="evidence_log.json", help="evidence log file (default: evidence_log.json)")

    s_init = sub.add_parser("init", parents=[common], help="hash files and create the baseline")
    s_init.add_argument("--force", action="store_true", help="replace an existing baseline")
    s_init.set_defaults(func=cmd_init)

    s_ver = sub.add_parser("verify", parents=[common], help="re-hash and compare with the baseline")
    s_ver.set_defaults(func=cmd_verify)

    s_par = sub.add_parser("parse", parents=[common], help="check hash, then parse a SYNTHETIC log")
    s_par.add_argument("--file", required=True, help="log file inside the evidence folder")
    s_par.add_argument("--allow-modified", action="store_true", help="parse even if the hash does not match")
    s_par.set_defaults(func=cmd_parse)
    return p


def main():
    args = build_parser().parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
