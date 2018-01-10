import unittest
import diff
from hypothesis import given
from hypothesis.strategies import text
import html


class TestDiff(unittest.TestCase):
    def test_textDiff_empty_strings(self):
        self.assertEqual(diff.textDiff('', ''), '')
    
    
    @given(text().filter(lambda x: x ))
    def test_textDiff_same_strings(self, given_string):
        self.assertEqual(diff.textDiff(given_string, given_string), '<span>' + html.escape(given_string) + '</span>')
    
    
    def test_textDiff_delete_string(self):
        initial_text = '<p>Paragraph 1</p><p>Paragraph 2</p>'
        emended_text = '<p>Paragraph 2</p>'
        self.assertEqual(diff.textDiff(initial_text, emended_text), '<span class="red">&lt;p&gt;Paragraph 1&lt;/p&gt;</span><span>&lt;p&gt;Paragraph 2&lt;/p&gt;</span>')
    
    
    def test_textDiff_insert_string(self):
        initial_text = '<p>Paragraph 1</p>'
        emended_text = '<p>Paragraph 1</p><p>Paragraph 2</p>'
        self.assertEqual(diff.textDiff(initial_text, emended_text), '<span>&lt;p&gt;Paragraph 1&lt;/p&gt;</span><span class="green">&lt;p&gt;Paragraph 2&lt;/p&gt;</span>')


if __name__ == '__main__':
    unittest.main()
