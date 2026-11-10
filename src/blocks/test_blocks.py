import unittest

from src.blocks.blocks import BlockType, block_to_block_type, markdown_to_blocks


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


class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        for level in range(1, 7):
            block = f"{'#' * level} Heading"
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_requires_a_space(self):
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_must_open_on_its_own_line_and_close(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```\ncode"), BlockType.PARAGRAPH)

    def test_quote(self):
        block = "> First line\n> Second line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_requires_every_line_to_start_with_gt(self):
        block = "> First line\nSecond line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- First\n- Second"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_requires_a_space_after_the_dash(self):
        self.assertEqual(block_to_block_type("-First\n- Second"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_must_start_at_one_and_increment(self):
        self.assertEqual(block_to_block_type("2. First\n3. Second"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. First\n3. Third"), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a paragraph\nwith two lines"),
            BlockType.PARAGRAPH,
        )


if __name__ == '__main__':
    unittest.main()
