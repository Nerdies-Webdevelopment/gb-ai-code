#!/usr/bin/env python3
"""Copy the explicit TREE.txt package inventory, with conflict detection."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import os
import uuid
from contextlib import contextmanager

ROOT = Path(__file__).resolve().parents[1]
LOCAL_CONFIG = '.package-sync.local.json'
STATE = '.package-sync.json'


def digest(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def inventory(source: Path, exclude=lambda name: False) -> list[str]:
    names = {'TREE.txt'}
    for line in (source / 'TREE.txt').read_text(encoding='utf-8-sig').splitlines():
        name = line.strip()
        if not name or name.endswith('/'):
            continue
        path = PurePosixPath(name)
        allowed = (len(path.parts) == 1 and (name.endswith('.md') or name in {'.gitignore', '.gitattributes', 'START-HIER.cmd'})) or name.startswith(('.agents/skills/', '.github/workflows/', 'references/', 'tools/', 'docs/', 'dist/', 'wp-content/themes/generatepress_child/'))
        if not allowed or path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name:
            raise ValueError(f'Not a package path: {name}')
        if exclude(name):
            continue
        names.add(name)
    for name in names:
        path = source / name
        if not path.resolve().is_relative_to(source.resolve()) or not path.is_file():
            raise ValueError(f'Missing or external package file: {name}')
    return sorted(names)


def safe_path(root, name):
    path = root / name
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes package: {name}')
    return path


def durable_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('wb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def replace_file(source, target):
    """Atomic replacement of one file; journal provides multi-file recovery."""
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + '.sync-' + uuid.uuid4().hex)
    try:
        durable_write(temporary, source.read_bytes())
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()


@contextmanager
def exclusive(destination):
    # OS lock releases automatically on process exit, including a crash.
    lock = destination.parent / ('.' + destination.name + '.package-sync.lock')
    if lock.is_symlink():
        raise ValueError('External sync lock')
    with lock.open('a+b') as handle:
        handle.seek(0, 2)
        if handle.tell() == 0:
            handle.write(b'0'); handle.flush()
        handle.seek(0)
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == 'nt':
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def transaction_path(destination):
    destination = destination.resolve()
    path = destination.parent / ('.' + destination.name + '.package-sync-transaction')
    if path.is_symlink() or path.resolve().parent != destination.parent:
        raise ValueError('External transaction directory')
    return path


def archive_transaction(transaction):
    os.replace(transaction, transaction.with_name(transaction.name.replace('-transaction', '-backup-') + uuid.uuid4().hex))


def recover(destination):
    """Restore the pre-sync state, refusing edits made after interruption."""
    transaction = transaction_path(destination)
    journal = transaction / 'journal.json'
    if not journal.exists():
        # Preparation never modifies destination files before journal commit.
        if transaction.exists():
            archive_transaction(transaction)
        return
    entries = json.loads(journal.read_text(encoding='utf-8'))
    for name, entry in entries.items():
        target = safe_path(destination, name)
        if digest(target) not in (entry['before'], entry['after']):
            raise ValueError(f'Changed after interruption; merge first: {name}')
        if entry['before'] is not None and digest(safe_path(transaction / 'old', name)) != entry['before']:
            raise ValueError(f'Damaged recovery backup: {name}')
    for name, entry in entries.items():
        target = safe_path(destination, name)
        if digest(target) == entry['before']:
            continue
        if entry['before'] is None:
            target.unlink()
        else:
            replace_file(safe_path(transaction / 'old', name), target)
    archive_transaction(transaction)


def commit(destination, source, current, changes, baseline):
    transaction = transaction_path(destination)
    transaction.mkdir()
    entries = {}
    try:
        for name in changes + [STATE]:
            target = safe_path(destination, name)
            before = digest(target)
            if before != baseline[name]:
                raise ValueError(f'Destination changed after conflict check: {name}')
            if before is not None:
                durable_write(safe_path(transaction / 'old', name), target.read_bytes())
                if digest(transaction / 'old' / name) != before:
                    raise ValueError(f'Backup verification failed: {name}')
            data = (json.dumps(current, indent=2) + '\n').encode() if name == STATE else (source / name).read_bytes()
            staged = safe_path(transaction / 'new', name)
            durable_write(staged, data)
            after = digest(staged)
            if name != STATE and after != current[name]:
                raise ValueError(f'Source changed during preparation: {name}')
            entries[name] = {'before': before, 'after': after}
        durable_write(transaction / 'journal.tmp', (json.dumps(entries, indent=2) + '\n').encode())
        os.replace(transaction / 'journal.tmp', transaction / 'journal.json')
        for name, entry in entries.items():
            if digest(safe_path(destination, name)) != entry['before']:
                raise ValueError(f'Destination changed during preparation: {name}')
        for name, entry in entries.items():
            replace_file(transaction / 'new' / name, safe_path(destination, name))
            if digest(destination / name) != entry['after']:
                raise ValueError(f'Copy verification failed: {name}')
        for name, expected in current.items():
            if digest(destination / name) != expected:
                raise ValueError(f'Package verification failed: {name}')
        archive_transaction(transaction)
    except Exception:
        recover(destination)
        raise


def synchronize(source: Path, destination: Path, apply: bool = False, recovery: bool = False) -> list[str]:
    source, destination = source.resolve(), destination.resolve()
    if source == destination or source.is_relative_to(destination) or destination.is_relative_to(source):
        raise ValueError('Source and destination must be separate directories')
    if apply or recovery:
        with exclusive(destination):
            if recovery:
                recover(destination)
            return _synchronize(source, destination, apply)
    return _synchronize(source, destination, False)


def _synchronize(source: Path, destination: Path, apply: bool) -> list[str]:
    source, destination = source.resolve(), destination.resolve()
    if source == destination or source.is_relative_to(destination) or destination.is_relative_to(source):
        raise ValueError('Source and destination must be separate directories')
    if transaction_path(destination).exists():
        raise ValueError('Interrupted sync detected. Close other sync processes, then run with --recover.')
    names = inventory(source)
    state_file = destination / STATE
    if not state_file.resolve().is_relative_to(destination):
        raise ValueError('Sync state escapes destination')
    previous = json.loads(state_file.read_text(encoding='utf-8')) if state_file.is_file() else {}
    if not isinstance(previous, dict):
        raise ValueError('Invalid sync state')
    removed = set(previous) - set(names)
    if removed:
        raise ValueError('Inventory removals require manual review: ' + ', '.join(sorted(removed)))
    current, changes = {}, []
    baseline = {STATE: digest(state_file)}
    for name in names:
        target = destination / name
        if not target.resolve().is_relative_to(destination):
            raise ValueError(f'Destination path escapes package: {name}')
        current[name] = digest(source / name)
        target_hash = digest(target)
        baseline[name] = target_hash
        if target.exists() and not target.is_file():
            raise ValueError(f'Destination is not a file: {name}')
        if target_hash == current[name]:
            continue
        if target_hash is not None and target_hash != previous.get(name):
            raise ValueError(f'Desktop file changed independently; merge first: {name}')
        changes.append(name)
    if apply and (changes or previous != current):
        destination.mkdir(parents=True, exist_ok=True)
        commit(destination, source, current, changes, baseline)
    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--apply', action='store_true', help='Copy after conflict checks; default only compares')
    parser.add_argument('--recover', action='store_true', help='Roll back an interrupted sync, then compare (combine with --apply to retry)')
    args = parser.parse_args()
    try:
        source, destination = configured_paths(ROOT, args.source, args.destination)
        changes = synchronize(source, destination, args.apply, args.recover)
    except (ValueError, OSError) as exc:
        print(f'[ERROR] {exc}')
        return 1
    print(f'{len(changes)} package file(s) ' + ('synchronized and verified.' if args.apply else 'differ.'))
    for name in changes:
        print(name)
    return 0 if args.apply or not changes else 1


def configured_paths(root, source=None, destination=None):
    config_file = root / LOCAL_CONFIG
    config = json.loads(config_file.read_text(encoding='utf-8-sig')) if config_file.is_file() else {}
    if not isinstance(config, dict) or any(k not in {'source', 'destination'} or not isinstance(v, str) or not v.strip() for k, v in config.items()):
        raise ValueError('Invalid local sync configuration')
    def resolve(value):
        path = Path(value)
        return (path if path.is_absolute() else root / path).resolve()
    source = Path(source).resolve() if source is not None else resolve(config.get('source', '.'))
    destination = Path(destination).resolve() if destination is not None else resolve(config['destination']) if 'destination' in config else None
    if destination is None:
        raise ValueError('No sync destination configured. Use --destination PATH or .package-sync.local.json; no files copied.')
    return source, destination


if __name__ == '__main__':
    raise SystemExit(main())
