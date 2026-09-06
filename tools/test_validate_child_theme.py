import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.validate_child_theme import DEFAULT_THEME, ROOT, validate

class ChildThemeValidatorTests(unittest.TestCase):
    def test_installable_theme_matches_current_source(self):
        with zipfile.ZipFile(ROOT / 'dist/generatepress-child-v0.4.zip') as archive:
            for name in ('style.css', 'functions.php', 'AGENTS.md', 'README.md'):
                self.assertEqual(archive.read('generatepress_child/' + name), (DEFAULT_THEME / name).read_bytes())

    def test_old_semantic_selector_cannot_shadow_size_utility(self):
        theme = self.make_theme('body h2 {font-size:2rem} :where(.fs-h1) {font-size:3rem}', '<?php')
        self.assertTrue(any('Semantic typography overrides' in f.message for f in validate(theme)))

    def test_default_theme_uses_wordpress_root_layout(self):
        self.assertEqual(DEFAULT_THEME, ROOT / "wp-content/themes/generatepress_child")
        self.assertTrue((DEFAULT_THEME / "style.css").is_file())

    def make_theme(self, css: str, php: str) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name)
        (path / "style.css").write_text(css, encoding="utf-8")
        (path / "functions.php").write_text(php, encoding="utf-8")
        return path

    def test_rejects_high_specificity_typography_utilities(self):
        theme = self.make_theme(
            """/*
Template: generatepress
*/
:root {
 --gb-container-width:1280px;
 --fs-h1:1rem; --fs-h2:1rem; --fs-h3:1rem; --fs-h4:1rem;
 --fs-h5:1rem; --fs-h6:1rem; --fs-p:1rem;
}
body .fs-p { font-size:var(--fs-p); }
""",
            """<?php
add_theme_support( 'editor-styles' );
add_editor_style( 'style.css' );
""",
        )
        findings = validate(theme)
        self.assertTrue(any(f.level == "ERROR" and "High-specificity" in f.message for f in findings))

    def test_accepts_low_specificity_utility_contract(self):
        theme = self.make_theme(
            """/*
Template: generatepress
*/
:root {
 --gb-container-width:1280px;
 --fs-h1:1rem; --fs-h2:1rem; --fs-h3:1rem; --fs-h4:1rem;
 --fs-h5:1rem; --fs-h6:1rem; --fs-p:1rem;
}
:where(.fs-p) { font-size:var(--fs-p); }
""",
            """<?php
add_theme_support( 'editor-styles' );
add_editor_style( 'style.css' );
""",
        )
        findings = validate(theme)
        self.assertFalse(any(f.level == "ERROR" for f in findings))

if __name__ == "__main__":
    unittest.main()
