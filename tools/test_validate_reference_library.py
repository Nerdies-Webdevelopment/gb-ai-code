import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import validate_reference_library as validator


class ManifestTests(unittest.TestCase):
    def check(self, value):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'references').mkdir()
            (root / 'references/REFERENCE-MANIFEST.json').write_text(json.dumps(value), encoding='utf-8')
            output = io.StringIO()
            with patch.object(validator, 'ROOT', root), contextlib.redirect_stdout(output):
                return validator.main(), output.getvalue()

    def test_invalid_root_and_entries_report_errors(self):
        for value in ([], None, 42, {'references': [None]}, {'references': [3]}, {'references': [[]]}, {'references': ['bad']}):
            with self.subTest(value=value):
                code, output = self.check(value)
                self.assertEqual(code, 1)
                self.assertIn('[ERROR]', output)

    def test_wrong_field_types_report_errors(self):
        for entry in ({'id': [], 'file': 'references/x.html'}, {'id': 'x', 'file': {}}, {'id': ' ', 'file': 'references/x.html'}):
            with self.subTest(entry=entry):
                self.assertEqual(self.check({'references': [entry]})[0], 1)

    def test_outside_reference_path_is_rejected(self):
        code, output = self.check({'references': [{'id': 'x', 'file': '../outside.html'}]})
        self.assertEqual(code, 1)
        self.assertIn('inside references/', output)

    def test_valid_empty_manifest_does_not_crash(self):
        self.assertEqual(self.check({'references': []})[0], 0)
