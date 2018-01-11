import unittest
import diff
from hypothesis import given
from hypothesis.strategies import text
import html


class TestDiff(unittest.TestCase):
    def test_textDiff_empty_strings(self):
        self.assertEqual(diff.render_text_diff('', ''), '')

    @given(text().filter(lambda x: x is not ''))
    def test_textDiff_same_strings(self, given_string):
        self.assertEqual(diff.render_text_diff(given_string, given_string),
                         '<span>' + html.escape(given_string) + '</span>')

    def test_textDiff_delete_string(self):
        initial_text = '<p>Paragraph 1</p>\n<p>Paragraph 2</p>'
        emended_text = '<p>Paragraph 2</p>'
        self.assertEqual(diff.render_text_diff(initial_text, emended_text),
                         '<span class="red">&lt;p&gt;Paragraph 1&lt;/p&gt;\n</span><span>&lt;p&gt;Paragraph 2&lt;/p&gt;</span>')

    def test_textDiff_insert_string(self):
        initial_text = '<p>Paragraph 1</p>'
        emended_text = '<p>Paragraph 2</p>\n<p>Paragraph 1</p>'
        self.assertEqual(diff.render_text_diff(initial_text, emended_text),
                         '<span class="green">&lt;p&gt;Paragraph 2&lt;/p&gt;\n</span><span>&lt;p&gt;Paragraph 1&lt;/p&gt;</span>')

    def test_textDiff_replace_string(self):
        initial_text = '<p>Paragraph 1</p>'
        emended_text = '<p>Paragraph 1</p>\n<p>Paragraph 2</p>'
        self.assertEqual(diff.render_text_diff(initial_text, emended_text),
                         '<span class="red">&lt;p&gt;Paragraph 1&lt;/p&gt;</span><span class="green">&lt;p&gt;Paragraph 1&lt;/p&gt;\n&lt;p&gt;Paragraph 2&lt;/p&gt;</span>')


if __name__ == '__main__':
    unittest.main()
