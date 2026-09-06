#!/usr/bin/env python3
"""Build a reproducible, inventory-only project ZIP and SHA-256 sidecar."""
import argparse
import hashlib
from pathlib import Path
import re
import zipfile
try:
    from .sync_package import inventory, durable_write
except ImportError:
    from sync_package import inventory, durable_write

VERSION = '3.2.0'


def release_artifact(name):
    return bool(re.fullmatch(r'dist/generateblocks-codex-v[0-9.]+\.(?:zip|sha256)', name))


def build(root):
    root = root.resolve()
    # TREE lists distributable files too. Exclude full releases before checking
    # existence, so a clean checkout can build its first ZIP without recursion.
    verified = inventory(root, exclude=release_artifact)
    if verified:
        output = root / 'dist' / f'generateblocks-codex-v{VERSION}.zip'
        if not output.resolve().is_relative_to(root) or not output.with_suffix('.sha256').resolve().is_relative_to(root):
            raise ValueError('Release output escapes package')
        output.parent.mkdir(parents=True, exist_ok=True)
        from io import BytesIO
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name in verified:
                item = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
                item.create_system = 3
                item.compress_type = zipfile.ZIP_DEFLATED
                item.external_attr = 0o100644 << 16
                data = ('\n'.join(n for n in verified if n != 'TREE.txt') + '\n').encode() if name == 'TREE.txt' else (root / name).read_bytes()
                archive.writestr(item, data)
        data = buffer.getvalue()
        checksum = hashlib.sha256(data).hexdigest()
        durable_write(output, data)
        durable_write(output.with_suffix('.sha256'), f'{checksum}  {output.name}\n'.encode())
        return output, checksum, len(verified)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    path, checksum, count = build(args.root)
    print(f'{path.name}: {count} files, SHA256 {checksum}')
