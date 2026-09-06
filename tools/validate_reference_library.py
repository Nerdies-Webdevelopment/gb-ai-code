#!/usr/bin/env python3
"""Validate reference manifest/file consistency and static GB structure."""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from validate_gb_block import validate_text  # noqa: E402

def main() -> int:
    manifest_path = ROOT / "references" / "REFERENCE-MANIFEST.json"
    if not manifest_path.exists():
        print("[ERROR] Missing references/REFERENCE-MANIFEST.json")
        return 1

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeError) as exc:
        print(f"[ERROR] Invalid manifest JSON: {exc}")
        return 1

    if not isinstance(manifest, dict):
        print("[ERROR] Manifest root must be a JSON object.")
        return 1
    refs = manifest.get("references")
    if not isinstance(refs, list):
        print("[ERROR] Manifest 'references' must be a list.")
        return 1

    errors = 0
    warnings = 0
    seen_ids: set[str] = set()
    seen_files: set[str] = set()

    for entry in refs:
        if not isinstance(entry, dict):
            print("[ERROR] Every manifest entry must be a JSON object.")
            errors += 1
            continue
        ref_id = entry.get("id")
        rel = entry.get("file")
        if not isinstance(ref_id, str) or not ref_id.strip() or not isinstance(rel, str) or not rel.strip():
            print("[ERROR] Every manifest entry requires non-empty string id and file.")
            errors += 1
            continue

        if ref_id in seen_ids:
            print(f"[ERROR] Duplicate manifest id: {ref_id}")
            errors += 1
        seen_ids.add(ref_id)

        if rel in seen_files:
            print(f"[ERROR] Duplicate manifest file: {rel}")
            errors += 1
        seen_files.add(rel)

        path = (ROOT / rel).resolve()
        if not path.is_relative_to((ROOT / 'references').resolve()) or path.suffix.lower() != '.html':
            print(f"[ERROR] Reference path must be an HTML file inside references/: {rel}")
            errors += 1
            continue
        if not path.is_file():
            print(f"[ERROR] Missing reference file: {rel}")
            errors += 1
            continue

        try:
            source = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            print(f"[ERROR] Cannot read reference {rel}: {exc}")
            errors += 1
            continue
        for finding in validate_text(source, rel):
            print(f"[{finding.level}] {finding.message}")
            if finding.level == "ERROR":
                errors += 1
            else:
                warnings += 1

    actual = {
        str(p.relative_to(ROOT)).replace("\\", "/")
        for p in (ROOT / "references").rglob("*.html")
    }
    unlisted = sorted(actual - seen_files)
    for rel in unlisted:
        print(f"[WARN] Reference HTML not listed in manifest: {rel}")
        warnings += 1

    print(
        f"Manifest entries: {len(refs)}; static result: {errors} error(s), {warnings} warning(s)."
    )
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
