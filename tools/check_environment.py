#!/usr/bin/env python3
"""Read source headers only; never load WordPress, secrets or the database."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = {
    "GeneratePress": "wp-content/themes/generatepress/style.css",
    "GP Premium": "wp-content/plugins/gp-premium/gp-premium.php",
    "GenerateBlocks": "wp-content/plugins/generateblocks/plugin.php",
    "GenerateBlocks Pro": "wp-content/plugins/generateblocks-pro/plugin.php",
}


def inspect(root: Path, profile: str = 'full') -> tuple[list[str], int]:
    messages = []
    errors = 0
    context_path = root / "PROJECT-CONTEXT.md"
    if not context_path.is_file():
        return ["[ERROR] Missing PROJECT-CONTEXT.md"], 1
    context = context_path.read_text(encoding="utf-8-sig")
    for name, relative in SOURCES.items():
        path = root / relative
        if not path.is_file():
            if profile == 'basic' and name in {'GP Premium', 'GenerateBlocks Pro'}:
                messages.append(f'[INFO] Optional for basic blocks, not installed: {name}')
                continue
            messages.append(f"[ERROR] Missing installed source: {relative}")
            errors += 1
            continue
        # WordPress reads plugin/theme metadata from the file header.
        header = path.read_text(encoding="utf-8-sig")[:8192]
        actual = re.search(r"(?mi)^\s*\*?\s*Version:\s*([^\s*]+)", header)
        expected = re.search(rf"(?m)^{re.escape(name)}:\s+(\S+)\s*$", context)
        if not actual or not expected:
            messages.append(f"[ERROR] {name}: missing source or documented version")
            errors += 1
        elif actual[1] != expected[1]:
            messages.append(f"[ERROR] {name}: source {actual[1]}, documented {expected[1]}; inspect changes and revalidate affected blocks before updating context")
            errors += 1
        else:
            messages.append(f"[PASS] {name}: source version {actual[1]} matches context")
    messages.append("Source inspection only: activation, database and Gutenberg compatibility were not checked.")
    return messages, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--profile", choices=['basic', 'full'], default='basic', help='basic: GeneratePress + GenerateBlocks required; full: premium plugins required too')
    args = parser.parse_args()
    messages, errors = inspect(args.root, args.profile)
    print("\n".join(messages))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
