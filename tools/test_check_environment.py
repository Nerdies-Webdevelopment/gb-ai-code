import tempfile
import unittest
from pathlib import Path

from tools.check_environment import SOURCES, inspect


class EnvironmentTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        (self.root / "PROJECT-CONTEXT.md").write_text(
            "\n".join(f"{name}: 1.2.3" for name in SOURCES), encoding="utf-8"
        )
        for relative in SOURCES.values():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("/*\n * Version: 1.2.3\n */", encoding="utf-8")

    def test_matching_sources_pass(self):
        self.assertEqual(inspect(self.root)[1], 0)

    def test_upgrade_requires_context_review(self):
        (self.root / SOURCES["GenerateBlocks"]).write_text("/*\nVersion: 2.0.0\n*/", encoding="utf-8")
        messages, errors = inspect(self.root)
        self.assertEqual(errors, 1)
        self.assertTrue(any("source 2.0.0, documented 1.2.3" in item for item in messages))

    def test_missing_plugin_fails(self):
        (self.root / SOURCES["GenerateBlocks Pro"]).unlink()
        self.assertEqual(inspect(self.root)[1], 1)

    def test_missing_version_fails(self):
        (self.root / SOURCES["GenerateBlocks"] ).write_text("<?php", encoding="utf-8")
        self.assertEqual(inspect(self.root)[1], 1)

    def test_missing_context_fails_cleanly(self):
        (self.root / "PROJECT-CONTEXT.md").unlink()
        self.assertEqual(inspect(self.root)[1], 1)
