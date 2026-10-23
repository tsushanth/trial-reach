"""Repository guard: this repo holds code, protocols and documentation only.

It must never contain personal information, data files, record identifiers, or pointers to where data lives on a machine.
Run before every commit (installed as a git pre-commit hook by scripts/install_hooks.sh) and in CI.

  python3 scripts/check_no_data.py            # scan every tracked and staged file
  python3 scripts/check_no_data.py FILE ...   # scan given files

Exit code 1 and a list of findings (file, line, rule; never the matched text) if anything is found.
Rules are listed in RULES. Do not weaken them to get a commit through; remove the offending content instead.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_BYTES = 200_000
SELF = {"scripts/check_no_data.py", "tests/test_check_no_data.py"}  # contain rule patterns / synthetic examples

BAD_EXT = {
    ".csv", ".tsv", ".xlsx", ".xls", ".xpt", ".sas7bdat", ".parquet", ".feather", ".arrow", ".jsonl", ".ndjson", ".db",
    ".sqlite", ".sqlite3", ".zip", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".tar", ".pkl", ".pickle", ".npy", ".npz", ".h5",
    ".hdf5", ".dta", ".sav", ".rds", ".rdata", ".pdf", ".docx", ".gguf", ".safetensors", ".bin", ".pt", ".onnx",
}
BAD_DIRS = {"data", "raw", "datasets", "outputs", "results_raw", "cache", ".cache"}

# (rule name, compiled regex). Patterns that would match their own definition are built by concatenation.
RULES = [
    ("email address", re.compile(r"\b[A-Za-z0-9._%+-]+@(?!users\.noreply\.github\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("phone number", re.compile(r"(?<!\d)(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)")),
    ("US SSN-like number", re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")),
    ("trial registry identifier", re.compile(r"\bNCT" + r"\d{8}\b")),
    ("survey respondent id", re.compile(r"\bSEQN\s*[=:]?\s*\d{3,}", re.I)),  # a respondent number; the bare column name is schema, not an identifier
    ("medical record / patient id", re.compile(r"\b(?:MRN|patient[_ ]?id|record[_ ]?id)\s*[=:]\s*\S+", re.I)),
    ("absolute local path", re.compile(r"(?:/Users/|/home/|C:\\Users\\)[A-Za-z0-9._-]+")),
    ("data directory path", re.compile(r"(?:^|[\s\"'(=])(?:\./)?(?:data|raw|datasets)/[\w./-]+", re.I)),
    ("data file URL", re.compile(r"https?://[^\s\"')]*(?:\.xpt|\.csv|\.zip|\.parquet|\.jsonl|/api/v\d/studies|/Nchs/Data/)\b", re.I)),
    ("secret-like token", re.compile(r"\b(?:sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|hf_[A-Za-z0-9]{30,})\b")),
]


def tracked_and_staged() -> list[str]:
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True)
    return sorted({p for p in out.stdout.splitlines() if p})


def check_path(rel: str) -> list[str]:
    findings = []
    p = Path(rel)
    if p.suffix.lower() in BAD_EXT:
        findings.append(f"{rel}: forbidden file type {p.suffix.lower()}")
    if any(part.lower() in BAD_DIRS for part in p.parts[:-1]):
        findings.append(f"{rel}: forbidden data-like directory")
    full = ROOT / rel
    if full.is_file() and full.stat().st_size > MAX_BYTES:
        findings.append(f"{rel}: file larger than {MAX_BYTES} bytes")
    return findings


def check_text(rel: str, text: str) -> list[str]:
    if rel in SELF:
        return []
    findings = []
    for i, line in enumerate(text.splitlines(), 1):
        for name, rx in RULES:
            if rx.search(line):
                findings.append(f"{rel}:{i}: {name}")
    return findings


def scan(files: list[str]) -> list[str]:
    findings = []
    for rel in files:
        findings += check_path(rel)
        full = ROOT / rel
        if full.is_file() and full.stat().st_size <= MAX_BYTES and Path(rel).suffix.lower() not in BAD_EXT:
            try:
                findings += check_text(rel, full.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                findings.append(f"{rel}: not UTF-8 text (binary files are not allowed)")
    return findings


def main(argv: list[str]) -> int:
    files = argv or tracked_and_staged()
    findings = scan(files)
    if findings:
        print("BLOCKED: this repository must not contain PII, data, record identifiers or data locations.\n")
        print("\n".join(findings))
        return 1
    print(f"ok: {len(files)} files clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
