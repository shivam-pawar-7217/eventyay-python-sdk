from pathlib import Path

BIDI_CHARS = {
    "\u202A",  # LRE
    "\u202B",  # RLE
    "\u202D",  # LRO
    "\u202E",  # RLO
    "\u2066",  # LRI
    "\u2067",  # RLI
    "\u2068",  # FSI
    "\u202C",  # PDF
    "\u2069",  # PDI
}

BIDI_HEX = {c: hex(ord(c)) for c in BIDI_CHARS}
IGNORED_PARTS = {".venv", "venv", ".git", "__pycache__", ".mypy_cache", ".pytest_cache"}
SCANNED_SUFFIXES = {
    ".py",
    ".md",
    ".rst",
    ".toml",
    ".yml",
    ".yaml",
    ".json",
    ".ini",
    ".cfg",
    ".txt",
}


def should_scan(path: Path) -> bool:
    return path.suffix.lower() in SCANNED_SUFFIXES


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    found_issues = False

    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        if not should_scan(path):
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for line_num, line in enumerate(content.splitlines(), start=1):
            for col_num, char in enumerate(line, start=1):
                if char in BIDI_CHARS:
                    rel = path.relative_to(repo_root)
                    print(
                        f"BIDI CHAR FOUND in {rel}:{line_num}:{col_num} ({BIDI_HEX[char]})"
                    )
                    found_issues = True

    if found_issues:
        return 1

    print("No bidirectional Unicode characters found in scanned files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
