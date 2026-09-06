import unittest
import json

from tools.validate_gb_block import validate_text

class ValidatorTests(unittest.TestCase):
    def block(self, styles=None, css=None, markup='<p class="gb-text-x1">Test</p>'):
        attrs = {"uniqueId": "x1", "tagName": "p"}
        if styles is not None:
            attrs['styles'] = styles
        if css is not None:
            attrs['css'] = css
        return '<!-- wp:generateblocks/text ' + json.dumps(attrs) + ' -->' + markup + '<!-- /wp:generateblocks/text -->'

    def test_malformed_comments_fail(self):
        for text in ('<!-- wp:generateblocks/text {"uniqueId":"x1" /-->',
                     '<!-- wp:generateblocks/text {"uniqueId":"x1"}',
                     '<!-- wp:generateblocks/text [1,2] /-->',
                     '<!-- wp:generateblocks/text null /-->',
                     '<!-- /wp:generateblocks/text {} -->'):
            with self.subTest(text=text):
                self.assertTrue(any(level == 'ERROR' for level, _ in self.levels(text)))

    def test_valid_dynamic_block_and_ordinary_comment(self):
        self.assertEqual(self.levels('<!-- ordinary comment --><!-- wp:core/latest-posts {"postsToShow":3} /-->'), [])

    def test_mismatched_saved_closing_tag_fails(self):
        self.assertTrue(any('saved HTML' in message for _, message in self.levels(self.block(markup='<p class="gb-text-x1">Test</div>'))))

    def test_wrong_native_class_fails(self):
        self.assertTrue(any('native class' in message for _, message in self.levels(self.block(markup='<p class="gb-text-other">Test</p>'))))

    def test_unstyled_global_class_only_block_is_valid(self):
        self.assertEqual(self.levels(self.block(markup='<p class="fs-p">Test</p>')), [])

    def test_contradictory_colors_fail(self):
        findings = self.levels(self.block({'color': 'red'}, '.gb-text-x1{color:blue}'))
        self.assertTrue(any(level == 'ERROR' and 'mismatch' in message for level, message in findings))

    def test_wrong_css_selector_fails(self):
        self.assertTrue(any(level == 'ERROR' for level, _ in self.levels(self.block({'color': 'red'}, '.gb-text-other{color:red}'))))

    def test_responsive_and_pseudo_state_mismatch_fails(self):
        styles = {'color': 'red', '@media (max-width:767px)': {'color': 'blue'}, '&:hover': {'color': 'green'}}
        css = '.gb-text-x1{color:red}@media(max-width:767px){.gb-text-x1{color:red}}.gb-text-x1:hover{color:green}'
        self.assertTrue(any('mismatch' in message and '@media' in message for _, message in self.levels(self.block(styles, css))))

    def test_missing_responsive_rule_fails(self):
        findings = self.levels(self.block({'@media (max-width:767px)': {'color': 'blue'}}, '.gb-text-x1{color:blue}'))
        self.assertTrue(any(level == 'ERROR' for level, _ in findings))

    def test_equivalent_optimized_box_styles_pass(self):
        styles = {'color': '#ffffff', 'opacity': '0.5', 'paddingTop': '2rem', 'paddingBottom': '2rem', 'paddingLeft': '1rem', 'paddingRight': '1rem'}
        self.assertEqual(self.levels(self.block(styles, '.gb-text-x1{color:#fff;opacity:.5;padding:2rem 1rem}')), [])

    def test_strings_and_functions_are_not_split(self):
        styles = {'backgroundImage': 'url("data:image/svg+xml;a:b,{c}")', '&::after': {'content': '"A; B: C /* literal */"'}}
        css = '.gb-text-x1{background-image:url("data:image/svg+xml;a:b,{c}")}.gb-text-x1::after{content:"A; B: C /* literal */"}'
        self.assertEqual(self.levels(self.block(styles, css)), [])

    def test_svg_and_void_html_pass(self):
        markup = '<p class="gb-text-x1"><img src="x.png" alt=""><br><svg><path d="M0 0" /></svg></p>'
        self.assertEqual(self.levels(self.block(markup=markup)), [])

    def levels(self, text):
        return [(f.level, f.message) for f in validate_text(text)]

    def test_valid_simple_text_block(self):
        text = (
            '<!-- wp:generateblocks/text {"uniqueId":"x1","tagName":"span",'
            '"styles":{"display":"inline-block"},"css":".gb-text-x1{display:inline-block}"} -->'
            '<span class="gb-text gb-text-x1">Badge</span>'
            '<!-- /wp:generateblocks/text -->'
        )
        self.assertFalse(any(level == "ERROR" for level, _ in self.levels(text)))

    def test_duplicate_unique_id_is_error(self):
        text = (
            '<!-- wp:generateblocks/text {"uniqueId":"x1","tagName":"p"} -->'
            '<p class="gb-text-x1">A</p><!-- /wp:generateblocks/text -->'
            '<!-- wp:generateblocks/text {"uniqueId":"x1","tagName":"p"} -->'
            '<p class="gb-text-x1">B</p><!-- /wp:generateblocks/text -->'
        )
        self.assertTrue(any("duplicate uniqueId" in msg for _, msg in self.levels(text)))

    def test_element_span_with_innerblocks_is_error(self):
        text = (
            '<!-- wp:generateblocks/element {"uniqueId":"e1","tagName":"span"} -->'
            '<span class="gb-element-e1">'
            '<!-- wp:generateblocks/text {"uniqueId":"t1","tagName":"span"} -->'
            '<span class="gb-text-t1">Badge</span><!-- /wp:generateblocks/text -->'
            '</span><!-- /wp:generateblocks/element -->'
        )
        self.assertTrue(any("forbidden" in msg for _, msg in self.levels(text)))

    def test_href_hash_is_warning(self):
        text = '<a href="#">X</a>'
        self.assertTrue(any(level == "WARN" and 'href="#"' in msg for level, msg in self.levels(text)))

if __name__ == "__main__":
    unittest.main()
