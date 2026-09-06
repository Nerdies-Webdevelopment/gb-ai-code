from pathlib import Path
import tempfile
import unittest
from tools.sync_package import configured_paths, LOCAL_CONFIG
from tools.export_homepage_guide import render, export
from tools.setup_project import check
from tools.check_environment import inspect, SOURCES


class PortabilityTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve() / 'Different WordPress Name'
        self.root.mkdir()

    def test_sync_has_no_machine_default_destination(self):
        with self.assertRaisesRegex(ValueError, 'No sync destination'):
            configured_paths(self.root)

    def test_local_config_is_relative_to_package_not_cwd(self):
        (self.root / LOCAL_CONFIG).write_text('{"destination":"../copy"}')
        source, target = configured_paths(self.root)
        self.assertEqual(source, self.root)
        self.assertEqual(target, self.root.parent / 'copy')

    def test_explicit_sync_paths_override_local_defaults(self):
        (self.root / LOCAL_CONFIG).write_text('{"destination":"../copy"}')
        self.assertEqual(configured_paths(self.root, self.root / 'other', self.root / 'explicit'),
                         (self.root / 'other', self.root / 'explicit'))

    def test_site_download_paths_cover_root_nested_and_ports(self):
        template = '{"href":"/dist/a.zip"}<a href="/dist/a.zip">Download</a>'
        for url, prefix in [('https://example.com/', ''), ('http://localhost:8080/demo/', '/demo'), ('https://example.com/a/b', '/a/b')]:
            result = render(template, url)
            self.assertEqual(result.count(prefix + '/dist/a.zip'), 2)
            self.assertNotIn('localhost', result)

    def test_invalid_site_urls_rejected(self):
        for url in ('javascript:alert(1)', 'https://user:pass@example.com', 'https://example.com/a?b=1', 'https://example.com/a/../b', 'https://example.com/a"b'):
            with self.assertRaises(ValueError):
                render('', url)

    def test_guide_export_never_overwrites_existing_work(self):
        folder = self.root / 'docs/examples'
        folder.mkdir(parents=True)
        (folder / 'homepage-package-guide.html').write_text('<a href="/dist/a.zip">a</a>')
        output = self.root / '.local/guide.html'
        export(self.root, 'http://localhost/different', output)
        self.assertIn('/different/dist/a.zip', output.read_text())
        with self.assertRaises(FileExistsError):
            export(self.root, 'https://example.com/', output)

    def test_wrong_installation_level_has_actionable_error(self):
        messages, errors = check(self.root)
        self.assertEqual(errors, 1)
        self.assertTrue(any('PaketINHALT' in line for line in messages))

    def test_basic_installation_does_not_require_paid_plugins(self):
        (self.root / 'PROJECT-CONTEXT.md').write_text('\n'.join(f'{name}: 1.2.3' for name in SOURCES))
        for name in ('GeneratePress', 'GenerateBlocks'):
            path = self.root / SOURCES[name]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Version: 1.2.3')
        self.assertEqual(inspect(self.root, 'basic')[1], 0)
        self.assertEqual(inspect(self.root, 'full')[1], 2)
