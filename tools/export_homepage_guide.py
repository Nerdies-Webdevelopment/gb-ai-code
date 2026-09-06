#!/usr/bin/env python3
"""Retarget the native guide's downloads to a site's actual WordPress URL."""
import argparse
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def render(template, site_url):
    parsed = urlsplit(site_url)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('Use an HTTP(S) site URL without credentials, query or fragment.')
    # Root-relative URLs survive host changes and WordPress URL sanitization.
    path = parsed.path.rstrip('/')
    if any(c in path for c in ('"', "'", '<', '>', '\\')) or '..' in path.split('/'):
        raise ValueError('Invalid site URL path')
    return re.sub(r'(?<="href":")/dist/|(?<=href=")/dist/', lambda _: path + '/dist/', template)


def export(root, site_url, output):
    data = render((root / 'docs/examples/homepage-package-guide.html').read_text(encoding='utf-8'), site_url)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-url', required=True)
    parser.add_argument('--output', type=Path, default=ROOT / '.local/homepage-package-guide.html')
    args = parser.parse_args()
    try:
        export(ROOT, args.site_url, args.output)
    except (ValueError, OSError) as exc:
        print(f'[ERROR] {exc}')
        raise SystemExit(1)
    print(f'Created {args.output}. Insert complete content in Gutenberg code editor, then save/reopen.')
