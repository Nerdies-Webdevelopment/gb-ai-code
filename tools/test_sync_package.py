import tempfile
import unittest
from pathlib import Path
from tools.sync_package import synchronize
from tools import sync_package as sync
from unittest.mock import patch


class PackageSyncTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.source = Path(tmp.name) / 'source'
        self.destination = Path(tmp.name) / 'destination'
        self.source.mkdir()
        (self.source / 'TREE.txt').write_text('README.md\n', encoding='utf-8')
        (self.source / 'README.md').write_text('first', encoding='utf-8')

    def test_copy_and_update(self):
        synchronize(self.source, self.destination, True)
        self.assertEqual(synchronize(self.source, self.destination), [])
        (self.source / 'README.md').write_text('second', encoding='utf-8')
        synchronize(self.source, self.destination, True)
        self.assertEqual((self.destination / 'README.md').read_text(), 'second')

    def test_independent_change_is_not_overwritten(self):
        synchronize(self.source, self.destination, True)
        (self.destination / 'README.md').write_text('user change', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'merge first'):
            synchronize(self.source, self.destination, True)
        self.assertEqual((self.destination / 'README.md').read_text(), 'user change')

    def test_wordpress_configuration_is_excluded(self):
        (self.source / 'TREE.txt').write_text('wp-config.php\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Not a package path'):
            synchronize(self.source, self.destination, True)
        self.assertFalse(self.destination.exists())

    def test_preview_does_not_write(self):
        self.assertEqual(len(synchronize(self.source, self.destination)), 2)
        self.assertFalse(self.destination.exists())

    def test_transaction_path_accepts_equivalent_spelling(self):
        alias = self.destination.parent / 'unused' / '..' / self.destination.name
        self.assertEqual(sync.transaction_path(alias), sync.transaction_path(self.destination))

    def prepare_update(self):
        synchronize(self.source, self.destination, True)
        (self.source / 'README.md').write_text('second', encoding='utf-8')
        (self.source / 'TREE.txt').write_text('README.md\nNEW.md\n', encoding='utf-8')
        (self.source / 'NEW.md').write_text('new file', encoding='utf-8')
        return {p.name: p.read_bytes() for p in self.destination.iterdir() if p.is_file()}

    def assert_restored(self, before):
        self.assertEqual({p.name: p.read_bytes() for p in self.destination.iterdir() if p.is_file()}, before)

    def test_failure_on_state_write_rolls_back_all_files(self):
        before = self.prepare_update()
        original = sync.replace_file
        def fail_once(source, target):
            if source.parent.name == 'new' and target.name == sync.STATE:
                raise OSError('simulated write failure')
            original(source, target)
        with patch.object(sync, 'replace_file', side_effect=fail_once):
            with self.assertRaisesRegex(OSError, 'simulated'):
                synchronize(self.source, self.destination, True)
        self.assert_restored(before)
        self.assertFalse(sync.transaction_path(self.destination).exists())

    def interrupt(self):
        before = self.prepare_update()
        original = sync.replace_file
        def crash(source, target):
            original(source, target)
            raise KeyboardInterrupt('simulated termination')
        with patch.object(sync, 'replace_file', side_effect=crash):
            with self.assertRaises(KeyboardInterrupt):
                synchronize(self.source, self.destination, True)
        return before

    def test_interruption_requires_explicit_recovery(self):
        before = self.interrupt()
        with self.assertRaisesRegex(ValueError, '--recover'):
            synchronize(self.source, self.destination)
        synchronize(self.source, self.destination, recovery=True)
        self.assert_restored(before)
        synchronize(self.source, self.destination, True)
        self.assertEqual(synchronize(self.source, self.destination), [])

    def test_recovery_refuses_later_user_edit(self):
        self.interrupt()
        (self.destination / 'NEW.md').write_text('user edit', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'merge first'):
            synchronize(self.source, self.destination, recovery=True)
        self.assertEqual((self.destination / 'NEW.md').read_text(), 'user edit')
        self.assertTrue(sync.transaction_path(self.destination).exists())

    def test_concurrent_writer_is_refused(self):
        with sync.exclusive(self.destination):
            with self.assertRaises(OSError):
                synchronize(self.source, self.destination, True)
