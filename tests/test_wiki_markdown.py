"""Standalone conversion tests without importing the application's dependencies."""
import importlib.util
from pathlib import Path
import unittest


spec = importlib.util.spec_from_file_location(
    "wiki", Path(__file__).resolve().parents[1] / "netai/models/wiki.py")
wiki = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wiki)


class MarkdownTests(unittest.TestCase):
    def test_headings_emphasis_and_section_links(self):
        self.assertEqual(wiki.Markdown("== Title ==\n\n'''bold''' and ''italic'' [[#Title|jump]]"),
                         '<a id="wiki-Title"></a>\n\n## Title\n\n'
                         '**bold** and *italic* [jump](#wiki-Title)')

    def test_mixed_nested_lists(self):
        self.assertEqual(wiki.Markdown('* parent\n*# child\n*# next\n* sibling'),
                         '- parent\n  1. child\n  1. next\n- sibling')

    def test_tables_and_literal_pipes(self):
        self.assertEqual(wiki.Markdown('{|\n! A !! B\n|-\n| a|b || <code>x|y</code>\n|}'),
                         '| A | B |\n| --- | --- |\n| a\\|b | `x\\|y` |')
        self.assertEqual(wiki.Markdown('{|\n| x || y\n|}'),
                         '|  |  |\n| --- | --- |\n| x | y |')

    def test_merged_table_falls_back_to_html(self):
        self.assertEqual(wiki.Markdown('{|\n| colspan="2" | x\n|}'),
                         wiki.HTML('{|\n| colspan="2" | x\n|}'))

    def test_literal_text_and_comments(self):
        self.assertEqual(wiki.Markdown('<nowiki># * [link]</nowiki><!--gone-->'),
                         '\\# \\* \\[link\\]')
        self.assertEqual(wiki.Markdown('1. literal'), '1\\. literal')
        self.assertEqual(wiki.Markdown('<script>alert(1)</script>'),
                         '\\<script\\>alert(1)\\</script\\>')
        self.assertEqual(wiki.Markdown('{{example}}'), '{{example}}')

    def test_code_fences_and_inline_padding(self):
        self.assertEqual(wiki.Markdown('<pre>a```b\nnext</pre>'), '````\na```b\nnext\n````')
        self.assertEqual(wiki.Markdown('<code>`x`</code>'), '`` `x` ``')
        self.assertEqual(wiki.Markdown(' code\n next'), '```\ncode\nnext\n```')

    def test_link_options_and_url_encoding(self):
        self.assertEqual(wiki.Markdown('[[A B]]', wiki_base='/pages'), '[A B](/pages/A_B)')
        self.assertEqual(wiki.Markdown('[[Page|label]]', link_resolver=lambda _: '/a(b)'),
                         '[label](/a%28b%29)')
        self.assertEqual(wiki.Markdown('[[Page|label]]', link_resolver=lambda _: 'javascript:bad'),
                         'label')
        self.assertEqual(wiki.Markdown('[https://example.com label]'),
                         '[label](https://example.com)')

    def test_validation_and_empty_input(self):
        self.assertEqual(wiki.Markdown(''), '')
        with self.assertRaises(TypeError):
            wiki.Markdown(None)
        with self.assertRaises(ValueError):
            wiki.Markdown('long', max_input_chars=3)
        with self.assertRaises(ValueError):
            wiki.Markdown('text', max_list_depth=0)
        with self.assertRaises(ValueError):
            wiki.Markdown('text', wiki_base='javascript:bad')


if __name__ == '__main__':
    unittest.main()
