#!/usr/bin/env python3
"""Read-only installation check for the WordPress root containing this package."""
import argparse
from pathlib import Path
import shutil
import sys
try:
    from .check_environment import inspect
except ImportError:
    from check_environment import inspect

ROOT = Path(__file__).resolve().parents[1]


def check(root, profile='basic'):
    root = root.resolve()
    messages = [f'Projektordner: {root}']
    missing = [name for name in ('wp-admin', 'wp-includes', 'wp-content') if not (root / name).is_dir()]
    if not (root / 'wp-load.php').is_file():
        missing.insert(0, 'wp-load.php')
    if missing:
        return messages + ['[ERROR] Kein vollstaendiger WordPress-Hauptordner. Fehlend: ' + ', '.join(missing),
                           'Den PaketINHALT direkt in den bestehenden WordPress-Ordner kopieren.'], 1
    results, errors = inspect(root, profile)
    messages += results
    messages += [f'[INFO] Python {sys.version.split()[0]}; keine pip-Pakete erforderlich.',
                 '[INFO] PHP CLI: ' + ('gefunden' if shutil.which('php') else 'nicht im PATH; optional fuer Theme-Syntaxpruefung.'),
                 '[INFO] Theme und Plugins im WordPress-Backend aktivieren. Dateipruefung bestaetigt keine Aktivierung.',
                 '[INFO] WordPress-Ordner als Codex-Projekt oeffnen; AGENTS.md und .agents/skills sind bereit.']
    return messages, errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--profile', choices=['basic', 'full'], default='basic')
    args = parser.parse_args()
    messages, errors = check(args.root, args.profile)
    print('\n'.join(messages))
    raise SystemExit(1 if errors else 0)
