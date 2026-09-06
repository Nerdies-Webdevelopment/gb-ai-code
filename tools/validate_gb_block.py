#!/usr/bin/env python3
"""Static validator for GenerateBlocks/Gutenberg serialized HTML.

Zero third-party dependencies.
This tool does not prove WordPress/Gutenberg runtime compatibility.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from .block_checks import Markup, CORE_CLASSES, first_markup, compare_styles
except ImportError:
    from block_checks import Markup, CORE_CLASSES, first_markup, compare_styles

COMMENT_RE = re.compile(
    r"<!--\s*(/?)wp:([a-zA-Z0-9_-]+(?:/[a-zA-Z0-9_-]+)?)(?:\s+(.*?))?\s*(/?)-->",
    re.S,
)

@dataclass
class Finding:
    level: str
    message: str

def validate_text(text: str, label: str = "<memory>") -> list[Finding]:
    findings: list[Finding] = []
    stack: list[str] = []
    unique_ids: list[str] = []

    matches = list(COMMENT_RE.finditer(text))
    recognized = {match.start() for match in matches}
    for start in re.finditer(r"<!--\s*/?wp\s*:", text):
        if start.start() not in recognized:
            findings.append(Finding("ERROR", f"{label}: malformed or incomplete Gutenberg comment at offset {start.start()}"))

    markup = Markup()
    markup.feed(text)
    markup.close()
    for error in markup.errors:
        findings.append(Finding("ERROR", f"{label}: {error}"))
    unclosed = [tag for tag in markup.stack if tag not in Markup.OPTIONAL]
    if unclosed:
        findings.append(Finding("ERROR", f"{label}: unclosed saved HTML tags: {', '.join(unclosed)}"))

    for index, match in enumerate(matches):
        closing, block_name, raw_attrs, self_closing = match.groups()
        raw_attrs = (raw_attrs or '').strip()
        if raw_attrs.endswith('/'):
            raw_attrs = raw_attrs[:-1].rstrip()
            self_closing = '/'
        if closing and (raw_attrs or self_closing):
            findings.append(Finding("ERROR", f"{label}: invalid closing Gutenberg comment: {block_name}"))

        if closing:
            if not stack:
                findings.append(Finding("ERROR", f"{label}: closing block without opener: {block_name}"))
                continue
            expected = stack.pop()
            if expected != block_name:
                findings.append(
                    Finding("ERROR", f"{label}: closing block {block_name!r}; expected {expected!r}")
                )
            continue

        attrs: dict = {}
        if raw_attrs:
            try:
                decoded = json.loads(raw_attrs)
                if not isinstance(decoded, dict):
                    findings.append(Finding("ERROR", f"{label}: block attributes must be a JSON object"))
                else:
                    attrs = decoded
            except json.JSONDecodeError as exc:
                findings.append(
                    Finding("ERROR", f"{label}: invalid JSON in wp:{block_name}: {exc}")
                )

        uid = attrs.get("uniqueId")
        if uid:
            unique_ids.append(str(uid))

            css = attrs.get("css")
            styles = attrs.get("styles")

            if css is not None and str(uid) not in str(css):
                findings.append(
                    Finding("WARN", f"{label}: {uid}: css does not contain the uniqueId")
                )

            if (styles is None) != (css is None):
                findings.append(
                    Finding("WARN", f"{label}: {uid}: structured styles/css presence differs")
                )

        tag_name = attrs.get("tagName")
        fragment_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        saved = first_markup(text[match.end():fragment_end], block_name, attrs) if not self_closing else None
        if saved and tag_name and saved[0] != str(tag_name).lower():
            findings.append(Finding("ERROR", f"{label}: {uid or '?'}: tagName={tag_name!r} but saved markup begins with <{saved[0]}>"))
        if not self_closing and uid and block_name in CORE_CLASSES and saved:
            expected_class = CORE_CLASSES[block_name] + str(uid)
            classes = (saved[1].get('class') or '').split()
            needs_class = attrs.get('css') or attrs.get('styles') or any(c.startswith(CORE_CLASSES[block_name]) for c in classes)
            if needs_class and expected_class not in classes:
                findings.append(Finding("ERROR", f"{label}: {uid}: saved markup is missing native class {expected_class}"))
        if not self_closing and block_name in CORE_CLASSES and not saved:
            findings.append(Finding("ERROR", f"{label}: missing saved root markup for {block_name}"))

        styles, css = attrs.get('styles'), attrs.get('css')
        if styles is not None and not isinstance(styles, dict):
            findings.append(Finding("ERROR", f"{label}: styles must be an object"))
        if css is not None and not isinstance(css, str):
            findings.append(Finding("ERROR", f"{label}: css must be a string"))
        if uid and isinstance(styles, dict) and isinstance(css, str):
            prefix = CORE_CLASSES.get(block_name)
            native = prefix + str(uid) if prefix else next((c for c in ((saved[1].get('class') or '').split() if saved else []) if c.startswith('gb-') and c.endswith('-' + str(uid))), None)
            if native:
                try:
                    for level, message in compare_styles(styles, css, '.' + native):
                        findings.append(Finding(level, f"{label}: {uid}: {message}"))
                except ValueError as exc:
                    findings.append(Finding("WARN", f"{label}: {uid}: styles/css comparison incomplete: {exc}"))
            elif styles:
                findings.append(Finding("WARN", f"{label}: {uid}: no evidenced native selector for styles/css comparison"))

        if (
            block_name == "generateblocks/element"
            and attrs.get("tagName") == "span"
            and not self_closing
        ):
            close_marker = "<!-- /wp:generateblocks/element -->"
            close_index = text.find(close_marker, match.end())
            if close_index != -1 and "<!-- wp:" in text[match.end() : close_index]:
                findings.append(
                    Finding(
                        "ERROR",
                        f"{label}: {uid or '?'}: forbidden generateblocks/element <span> with InnerBlocks; use generateblocks/text span",
                    )
                )

        if not self_closing:
            stack.append(block_name)

    if stack:
        findings.append(
            Finding("ERROR", f"{label}: unclosed blocks: {', '.join(stack[-12:])}")
        )

    duplicates = [uid for uid, count in Counter(unique_ids).items() if count > 1]
    if duplicates:
        findings.append(
            Finding("ERROR", f"{label}: duplicate uniqueId: {', '.join(duplicates)}")
        )

    if re.search(r"href\s*=\s*[\"']#[\"']", text):
        findings.append(Finding("WARN", f'{label}: contains final-looking href="#"'))

    if re.search(r"localhost", text, re.I):
        findings.append(Finding("WARN", f"{label}: contains localhost URL"))

    if re.search(r'overflow(?:Y|-y)?["\']?\s*[:=]\s*["\']?(?:auto|scroll)', text, re.I):
        findings.append(
            Finding("WARN", f"{label}: contains auto/scroll overflow; inspect content-fit intent")
        )

    if '"maxWidth":"1280px"' in text or '"maxWidth":"1200px"' in text:
        findings.append(
            Finding(
                "WARN",
                f"{label}: contains fixed 1200/1280 maxWidth; normalize project inner containers in new work",
            )
        )

    has_767 = bool(re.search(r"max-width\s*:\s*767px", text))
    has_768 = bool(re.search(r"max-width\s*:\s*768px", text))
    if has_767 and has_768:
        findings.append(
            Finding("WARN", f"{label}: mixes 767px and 768px CSS breakpoints")
        )

    if re.search(r"(fonts\.googleapis\.com|use\.typekit\.net|cdnjs\.cloudflare\.com/.*/font)", text, re.I):
        findings.append(
            Finding("WARN", f"{label}: contains an external font/CDN dependency")
        )

    return findings

def iter_html_paths(inputs: Iterable[str]) -> Iterable[Path]:
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            yield from sorted(path.rglob("*.html"))
        else:
            yield path

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="HTML file(s) or directories")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero when warnings are present as well as errors.",
    )
    args = parser.parse_args()

    all_findings: list[Finding] = []
    files = list(iter_html_paths(args.paths))
    if not files:
        print("No HTML files found.", file=sys.stderr)
        return 2

    for path in files:
        if not path.exists():
            all_findings.append(Finding("ERROR", f"{path}: file does not exist"))
            continue
        findings = validate_text(path.read_text(encoding="utf-8"), str(path))
        all_findings.extend(findings)

    for finding in all_findings:
        print(f"[{finding.level}] {finding.message}")

    errors = sum(f.level == "ERROR" for f in all_findings)
    warnings = sum(f.level == "WARN" for f in all_findings)
    print(f"Checked {len(files)} file(s): {errors} error(s), {warnings} warning(s).")

    if errors:
        return 1
    if args.strict and warnings:
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
