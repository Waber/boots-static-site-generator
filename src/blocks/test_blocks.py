import unittest

from src.blocks.blocks import markdown_to_blocks


class MyTestCase(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

    def test_empty_or_whitespace_only_input(self):
        for markdown in ["", " ", "\n\n\n", " \t\n\n \t "]:
            with self.subTest(markdown=markdown):
                self.assertEqual(markdown_to_blocks(markdown), [])

    def test_single_block_is_trimmed(self):
        self.assertEqual(markdown_to_blocks(" \t A paragraph \n "), ["A paragraph"])

    def test_multiple_blank_lines_do_not_create_empty_blocks(self):
        self.assertEqual(
            markdown_to_blocks("\n\nFirst\n\n\n\n\nSecond\n\n"),
            ["First", "Second"],
        )

    def test_whitespace_only_blocks_are_skipped(self):
        self.assertEqual(
            markdown_to_blocks("First\n\n \t \n\nSecond"),
            ["First", "Second"],
        )

    def test_single_newlines_and_internal_spaces_are_preserved(self):
        markdown = "First  line\nSecond line\n  Third line"
        self.assertEqual(markdown_to_blocks(markdown), [markdown])

    def test_markdown_syntax_and_block_order_are_preserved(self):
        self.assertEqual(
            markdown_to_blocks("# Heading\n\n> Quote\n\n- First\n- Second\n\n```\ncode\n```"),
            ["# Heading", "> Quote", "- First\n- Second", "```\ncode\n```"],
        )


if __name__ == '__main__':
    unittest.main()
