import unittest
from tools.block_checks import compare_styles


class StylesComparisonTests(unittest.TestCase):
    def test_css_only_property(self):
        result = compare_styles({'color': 'red'}, '.x{color:red;padding:1px}', '.x')
        self.assertTrue(any(level == 'WARN' and 'padding' in text for level, text in result))

    def test_css_only_responsive_selector(self):
        result = compare_styles({'color': 'red'}, '.x{color:red}@media(max-width:767px){.x:hover{display:none}}', '.x')
        self.assertTrue(any(level == 'WARN' and 'display' in text for level, text in result))

    def test_equivalent_colors_and_zero_lengths(self):
        for value in ('#F00', '#ff0000', 'rgb(255, 0, 0)', 'rgba(255,0,0,1)'):
            self.assertEqual(compare_styles({'color': 'red', 'padding': '0'}, '.x{color:' + value + ';padding:0px}', '.x'), [])

    def test_preserve_custom_property_and_quoted_values(self):
        for prop, a, b in [('--brand', 'red', '#f00'), ('content', '"a b"', '"ab"'), ('color', 'red', 'blue')]:
            self.assertTrue(compare_styles({prop: a}, '.x{' + prop + ':' + b + '}', '.x'))

    def test_ambiguous_shorthand_is_warning(self):
        result = compare_styles({'backgroundColor': 'red'}, '.x{background:red}', '.x')
        self.assertTrue(result)
        self.assertTrue(all(level == 'WARN' for level, _ in result))
