#!/usr/bin/env python3
"""Check the controlled research package and its single allowlisted data file."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_TOP_LEVEL = {
    ".gitignore",
    "PUBLIC_RELEASE.md",
    "README.md",
    "assets",
    "data",
    "scripts",
}
FORBIDDEN_NAMES = {".DS_Store", ".env"}
FORBIDDEN_SUFFIXES = {
    ".bin",
    ".db",
    ".npy",
    ".npz",
    ".parquet",
    ".pt",
    ".pth",
    ".safetensors",
    ".sqlite",
    ".sqlite3",
}
SECRET_PATTERNS = {
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "Hugging Face token": re.compile(r"\bhf_[A-Za-z0-9]{16,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
}
LOCAL_HOME = re.compile(r"(?<![A-Za-z0-9_])/(?:Users|home)/[^/\s]+/")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
MAX_FILE_BYTES = 2 * 1024 * 1024
ALLOWED_REAL_JSONL = {
    Path("data/actionselect/actionselect_104.jsonl"): {
        "rows": 104,
        "sha256": "55c40c214f10830e650800927acc87f68abf324618f1ec7fd83285524e1f4b4b",
    }
}


def iter_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts
    )


def main() -> int:
    errors: list[str] = []
    top_level = {path.name for path in ROOT.iterdir() if path.name != ".git"}
    extra = sorted(top_level - ALLOWED_TOP_LEVEL)
    if extra:
        errors.append(f"unexpected top-level entries: {', '.join(extra)}")

    files = iter_files()
    for path in files:
        relative = path.relative_to(ROOT)
        if path.is_symlink():
            errors.append(f"symlink is not allowed: {relative}")
            continue
        if path.name in FORBIDDEN_NAMES or path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden artifact: {relative}")
        if path.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"file exceeds 2 MiB: {relative}")
        if path.suffix.lower() == ".jsonl" and path.name != "example.jsonl":
            expected = ALLOWED_REAL_JSONL.get(relative)
            if expected is None:
                errors.append(f"non-allowlisted JSONL is not allowed: {relative}")
            else:
                payload = path.read_bytes()
                row_count = sum(bool(line.strip()) for line in payload.splitlines())
                sha256 = hashlib.sha256(payload).hexdigest()
                if row_count != expected["rows"]:
                    errors.append(
                        f"allowlisted JSONL row mismatch: {relative}: "
                        f"{row_count} != {expected['rows']}"
                    )
                if sha256 != expected["sha256"]:
                    errors.append(f"allowlisted JSONL checksum mismatch: {relative}")

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"non-UTF-8 file: {relative}")
            continue

        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{label} pattern in {relative}")
        if path.resolve() != Path(__file__).resolve() and LOCAL_HOME.search(text):
            errors.append(f"absolute home path in {relative}")

        if path.suffix.lower() == ".md":
            for target in MARKDOWN_LINK.findall(text):
                if "://" in target or target.startswith("#"):
                    continue
                target_path = target.split("#", 1)[0]
                resolved = (path.parent / target_path).resolve()
                if not resolved.exists() or ROOT not in resolved.parents:
                    errors.append(f"broken or external local link in {relative}: {target}")

    if errors:
        print("Release check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Release check passed: {len(files)} files; "
        f"{len(ALLOWED_REAL_JSONL)} controlled data artifact verified."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
