#!/usr/bin/env python3
"""Run all static package checks; optionally check installed source versions."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--installed", action="store_true", help="Also require installed plugin/theme sources to match PROJECT-CONTEXT.md")
    parser.add_argument('--profile', choices=['basic', 'full'], default='basic')
    args = parser.parse_args()
    checks = [
        ("Validator tests", ["-m", "unittest", "discover", "-s", "tools", "-t", "."]),
        ("Child Theme", ["tools/validate_child_theme.py"]),
        ("Reference library", ["tools/validate_reference_library.py"]),
        ("Homepage guide", ["tools/validate_gb_block.py", "--strict", "docs/examples/homepage-package-guide.html"]),
    ]
    if args.installed:
        checks.append(("Installed source versions", ["tools/check_environment.py", '--profile', args.profile]))
    failed = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    for label, command in checks:
        print(f"\nChecking {label}", flush=True)
        result = subprocess.run([sys.executable, *command], cwd=ROOT, env=env)
        if result.returncode:
            failed.append(label)
    print(f"\n{len(checks) - len(failed)}/{len(checks)} check groups passed.")
    if failed:
        print("Failed: " + ", ".join(failed))
    print("Static checks do not prove Gutenberg/editor/frontend compatibility.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
