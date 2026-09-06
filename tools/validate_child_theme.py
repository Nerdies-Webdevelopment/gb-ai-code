#!/usr/bin/env python3
"""Static validation for the packaged GeneratePress Child Theme."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_THEME = ROOT / "wp-content" / "themes" / "generatepress_child"

@dataclass
class Finding:
    level: str
    message: str

def validate(theme_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    style = theme_dir / "style.css"
    functions = theme_dir / "functions.php"

    if not style.exists():
        findings.append(Finding("ERROR", f"Missing {style}"))
        return findings
    if not functions.exists():
        findings.append(Finding("ERROR", f"Missing {functions}"))
        return findings

    css = style.read_text(encoding="utf-8")
    php = functions.read_text(encoding="utf-8")

    if re.search(r'body\s+(?:h[1-6]|p)\s*\{', css) and re.search(r':where\(\.fs-', css):
        findings.append(Finding("ERROR", "Semantic typography overrides size utilities; use body :where(h1).../body :where(p) before body :where(.fs-*)"))

    if not re.search(r"(?mi)^\s*Template:\s*generatepress\s*$", css):
        findings.append(Finding("ERROR", "style.css must declare Template: generatepress"))

    for token in (
        "--gb-container-width",
        "--fs-h1",
        "--fs-h2",
        "--fs-h3",
        "--fs-h4",
        "--fs-h5",
        "--fs-h6",
        "--fs-p",
    ):
        if token not in css:
            findings.append(Finding("ERROR", f"Missing required project token: {token}"))

    forbidden_selectors = (
        r"body\s+\.fs-h[1-6]\b",
        r"body\s+\.fs-p\b",
        r"body\s+\.gb-button\b",
    )
    for pattern in forbidden_selectors:
        if re.search(pattern, css):
            findings.append(
                Finding(
                    "ERROR",
                    f"High-specificity typography utility found: /{pattern}/",
                )
            )

    if "@import" in css:
        findings.append(Finding("ERROR", "Do not load the parent stylesheet with @import"))

    if "add_theme_support( 'editor-styles' )" not in php:
        findings.append(Finding("ERROR", "Missing editor-styles theme support"))

    if "add_editor_style( 'style.css' )" not in php:
        findings.append(Finding("ERROR", "Missing add_editor_style( 'style.css' )"))

    frontend_enqueue_hook = re.search(
        r"add_action\s*\(\s*['\"]wp_enqueue_scripts['\"]",
        php,
    )
    direct_style_enqueue = re.search(
        r"(?m)^\s*wp_enqueue_style\s*\(",
        php,
    )
    if frontend_enqueue_hook or direct_style_enqueue:
        findings.append(
            Finding(
                "WARN",
                "Frontend stylesheet enqueue detected; verify it is not duplicating GeneratePress child-theme loading",
            )
        )

    if "gblocks_templates" not in php:
        findings.append(
            Finding(
                "WARN",
                "GenerateBlocks template admin-column integration is absent",
            )
        )

    php_bin = shutil.which("php")
    if php_bin:
        result = subprocess.run(
            [php_bin, "-l", str(functions)],
            capture_output=True,
            text=True,
        )
        if result.returncode:
            findings.append(
                Finding("ERROR", f"php -l failed: {(result.stdout + result.stderr).strip()}")
            )
        else:
            findings.append(Finding("PASS", "php -l: no syntax errors"))
    else:
        findings.append(Finding("WARN", "PHP CLI not available; php -l not executed"))

    return findings

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "theme_dir",
        nargs="?",
        default=str(DEFAULT_THEME),
        help="Path to the GeneratePress Child Theme directory",
    )
    args = parser.parse_args()

    theme_dir = Path(args.theme_dir)
    findings = validate(theme_dir)

    for finding in findings:
        print(f"[{finding.level}] {finding.message}")

    errors = sum(f.level == "ERROR" for f in findings)
    warnings = sum(f.level == "WARN" for f in findings)
    passes = sum(f.level == "PASS" for f in findings)
    print(f"Child Theme: {errors} error(s), {warnings} warning(s), {passes} executed pass(es).")
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
