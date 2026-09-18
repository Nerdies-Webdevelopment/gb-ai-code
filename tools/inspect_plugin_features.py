#!/usr/bin/env python3
"""Inventory local plugin source metadata without loading WordPress or the database."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PLUGINS = {
    'generateblocks': 'plugin.php',
    'generateblocks-pro': 'plugin.php',
    'gp-premium': 'gp-premium.php',
}
TAG_FILES = {
    'generateblocks': 'includes/dynamic-tags/class-dynamic-tags.php',
    'generateblocks-pro': 'includes/extend/dynamic-tags/class-register.php',
}


def inspect(root: Path) -> dict:
    root = root.resolve()
    report = {'schema_version': 1, 'scope': 'source_metadata_only',
              'runtime_verified': False, 'plugins': {}, 'errors': []}

    def read(path: Path) -> str:
        if not path.resolve().is_relative_to(root):
            raise ValueError('Source path escapes installation')
        return path.read_text(encoding='utf-8-sig')

    for slug, main in PLUGINS.items():
        base = root / 'wp-content/plugins' / slug
        entry = {'version': None, 'activation': 'not_checked', 'blocks': []}
        report['plugins'][slug] = entry
        try:
            source = read(base / main)
            version = re.search(r'(?mi)^\s*\*?\s*Version:\s*([^\s*]+)', source[:8192])
            if not version:
                raise ValueError('Missing plugin version header')
            entry['version'] = version[1]
            if slug == 'gp-premium':
                entry['module_option_names'] = sorted(set(re.findall(
                    r"generatepress_is_module_active\(\s*'(generate_package_[^']+)'", source)))
                continue
            paths = sorted((base / 'dist/blocks').glob('*/block.json'))
            if not paths:
                raise ValueError('No dist/blocks/*/block.json found')
            seen = set()
            for path in paths:
                relative = path.relative_to(root).as_posix()
                try:
                    block = json.loads(read(path))
                    if not isinstance(block, dict):
                        raise ValueError('Block metadata must be an object')
                    name = block.get('name')
                    attrs = block.get('attributes', {})
                    if not isinstance(name, str) or not name.startswith(slug + '/'):
                        raise ValueError('Missing or unexpected block namespace')
                    if name in seen:
                        raise ValueError('Duplicate block name: ' + name)
                    seen.add(name)
                    if not isinstance(attrs, dict) or any(not isinstance(v, dict) for v in attrs.values()):
                        raise ValueError('Invalid attributes object')
                    entry['blocks'].append({'name': name, 'source': relative,
                        'attributes': sorted(attrs),
                        'parent': block.get('parent', []),
                        'ancestor': block.get('ancestor', [])})
                except (OSError, ValueError) as exc:
                    report['errors'].append(f'{relative}: {exc}')
            tags = read(base / TAG_FILES[slug])
            entry['dynamic_tags_in_registration_file'] = sorted(set(re.findall(
                r"'tag'\s*=>\s*'([^']+)'", tags)))
            if slug == 'generateblocks-pro':
                defaults = read(base / 'includes/feature-settings.php')
                entry['feature_defaults_in_source'] = {
                    key: value == 'true' for key, value in re.findall(
                        r"\$defaults\[\s*'([^']+)'\s*\]\s*=\s*(true|false)\s*;", defaults)}
        except (OSError, ValueError) as exc:
            report['errors'].append(f'{slug}: {exc}')
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT, help='WordPress installation root')
    parser.add_argument('--json', action='store_true', help='Print machine-readable inventory')
    args = parser.parse_args()
    result = inspect(args.root)
    if args.json:
        print(json.dumps(result, ensure_ascii=True, indent=2))
    else:
        for slug, plugin in result['plugins'].items():
            print(f"{slug}: {plugin['version'] or 'unavailable'}; activation not checked")
            for block in plugin['blocks']:
                print('  ' + block['name'])
            for module in plugin.get('module_option_names', []):
                print('  ' + module)
            if 'feature_defaults_in_source' in plugin:
                print('  Source defaults: ' + json.dumps(plugin['feature_defaults_in_source'], sort_keys=True))
        for error in result['errors']:
            print('[ERROR] ' + error)
        print('Metadata inventory only; legacy/PHP-registered blocks and extension-added tags/attributes may be absent.')
        print('Feature defaults are not live settings. Activation, save markup and runtime were not tested.')
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
