import json
from pathlib import Path
import tempfile
import unittest
from tools.inspect_plugin_features import inspect, PLUGINS, TAG_FILES


class PluginInventoryTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for slug, main in PLUGINS.items():
            self.write(slug, main, "<?php\n/*\n * Version: 1.2.3\n */\n" +
                       "if (generatepress_is_module_active( 'generate_package_elements', 'GENERATE_ELEMENTS' )) {}")
            if slug in TAG_FILES:
                self.write(slug, TAG_FILES[slug], "'tag' => 'post_title', 'tag' => 'post_title'")
                self.write(slug, 'dist/blocks/example/block.json', json.dumps({
                    'name': slug + '/example', 'attributes': {'uniqueId': {'type': 'string'}}}))
        self.write('generateblocks-pro', 'includes/feature-settings.php',
                   "$defaults['enable_forms'] = false; $defaults['enable_overlay_panels'] = true;")

    def write(self, slug, name, content):
        path = self.root / 'wp-content/plugins' / slug / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def test_inventory_separates_defaults_from_activation_and_never_loads_php(self):
        result = inspect(self.root)
        self.assertEqual(result['errors'], [])
        pro = result['plugins']['generateblocks-pro']
        self.assertEqual(pro['feature_defaults_in_source'], {'enable_forms': False, 'enable_overlay_panels': True})
        self.assertEqual(pro['activation'], 'not_checked')
        self.assertFalse(result['runtime_verified'])
        self.assertEqual(pro['dynamic_tags_in_registration_file'], ['post_title'])
        self.assertEqual(result['plugins']['gp-premium']['module_option_names'], ['generate_package_elements'])
        self.assertNotIn(str(self.root), json.dumps(result))

    def test_missing_plugin_reports_error_but_keeps_other_results(self):
        (self.root / 'wp-content/plugins/gp-premium/gp-premium.php').unlink()
        result = inspect(self.root)
        self.assertEqual(len(result['errors']), 1)
        self.assertEqual(result['plugins']['generateblocks']['version'], '1.2.3')

    def test_bad_metadata_is_reported_without_crash(self):
        for content in ('{', '[]', '{"name":"core/paragraph"}',
                        '{"name":"generateblocks/example","attributes":[]}'):
            with self.subTest(content=content):
                self.write('generateblocks', 'dist/blocks/example/block.json', content)
                self.assertTrue(inspect(self.root)['errors'])

    def test_duplicate_names_are_rejected(self):
        self.write('generateblocks', 'dist/blocks/duplicate/block.json', '{"name":"generateblocks/example"}')
        self.assertTrue(any('Duplicate' in e for e in inspect(self.root)['errors']))

    def test_missing_metadata_directory_is_not_success(self):
        (self.root / 'wp-content/plugins/generateblocks/dist/blocks/example/block.json').unlink()
        self.assertTrue(any('No dist/blocks' in e for e in inspect(self.root)['errors']))

    def test_missing_version_is_reported(self):
        self.write('generateblocks', 'plugin.php', '<?php // no header')
        self.assertTrue(any('version header' in e for e in inspect(self.root)['errors']))
