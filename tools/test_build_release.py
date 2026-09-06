from pathlib import Path
import tempfile
import unittest
import zipfile
from tools.build_release import build


class ReleaseTests(unittest.TestCase):
    def test_reproducible_archive_excludes_itself_and_unlisted_secrets(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'TREE.txt').write_text('README.md\ndist/generateblocks-codex-v3.2.0.zip\ndist/generateblocks-codex-v3.2.0.sha256\n')
            (root / 'README.md').write_text('hello')
            (root / 'wp-config.php').write_text('must not ship')
            path, first, count = build(root)
            self.assertEqual(build(root)[1], first)
            self.assertEqual(count, 2)
            with zipfile.ZipFile(path) as archive:
                self.assertEqual(sorted(archive.namelist()), ['README.md', 'TREE.txt'])
                self.assertEqual(archive.read('TREE.txt'), b'README.md\n')

    def test_forbidden_inventory_entry_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'TREE.txt').write_text('wp-config.php\n')
            (root / 'wp-config.php').write_text('secret')
            with self.assertRaisesRegex(ValueError, 'Not a package path'):
                build(root)
