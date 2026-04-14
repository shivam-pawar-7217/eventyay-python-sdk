import os
import sys

BIDI_CHARS = [
    '\u202A', '\u202B', '\u202D', '\u202E', 
    '\u2066', '\u2067', '\u2068', '\u202C', '\u2069'
]

BIDI_HEX = {c: hex(ord(c)) for c in BIDI_CHARS}

directory = "/home/lightning/eventyay-python-sdk"
found_issues = False

for root, _, files in os.walk(directory):
    if '.venv' in root or '.git' in root or '__pycache__' in root:
        continue
    for file in files:
        if not file.endswith('.py'):
            continue
        path = os.path.join(root, file)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                for i, char in enumerate(content):
                    if char in BIDI_CHARS:
                        print(f"BIDI CHAR FOUND in {path} at position {i}: {BIDI_HEX[char]}")
                        found_issues = True
        except Exception:
            pass

if not found_issues:
    print("No bidirectional Unicode characters found in the codebase.")
