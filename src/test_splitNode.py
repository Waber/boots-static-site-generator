import unittest

from src.splitNode import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from src.textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_supported_delimiters(self):
        for delimiter, text_type in [
            ("`", TextType.CODE),
            ("**", TextType.BOLD),
            ("_", TextType.ITALIC),
        ]:
            with self.subTest(delimiter=delimiter):
                node = TextNode(f"Before {delimiter}formatted{delimiter} after", TextType.PLAIN)
                self.assertEqual(
                    split_nodes_delimiter([node], delimiter, text_type),
                    [
                        TextNode("Before ", TextType.PLAIN),
                        TextNode("formatted", text_type),
                        TextNode(" after", TextType.PLAIN),
                    ],
                )

    def test_multiple_delimiter_pairs(self):
        node = TextNode("A **first** and **second** end", TextType.PLAIN)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("A ", TextType.PLAIN),
                TextNode("first", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("second", TextType.BOLD),
                TextNode(" end", TextType.PLAIN),
            ],
        )

    def test_delimiters_at_boundaries_skip_empty_fragments(self):
        node = TextNode("`code`", TextType.PLAIN)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [TextNode("code", TextType.CODE)],
        )

    def test_plain_text_without_delimiter(self):
        node = TextNode("Plain text", TextType.PLAIN)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [TextNode("Plain text", TextType.PLAIN)],
        )

    def test_non_plain_nodes_are_preserved(self):
        for text_type in TextType:
            if text_type == TextType.PLAIN:
                continue
            with self.subTest(text_type=text_type):
                node = TextNode("An unmatched ` delimiter", text_type, "https://example.com")
                result = split_nodes_delimiter([node], "`", TextType.CODE)
                self.assertEqual(len(result), 1)
                self.assertIs(result[0], node)

    def test_multiple_nodes_preserve_order(self):
        bold = TextNode("bold", TextType.BOLD)
        plain = TextNode("before `code` after", TextType.PLAIN)
        link = TextNode("link", TextType.LINK, "https://example.com")
        self.assertEqual(
            split_nodes_delimiter([bold, plain, link], "`", TextType.CODE),
            [bold, TextNode("before ", TextType.PLAIN), TextNode("code", TextType.CODE),
             TextNode(" after", TextType.PLAIN), link],
        )

    def test_unclosed_delimiter_raises(self):
        for text in ["before `code", "`first` and `second"]:
            with self.subTest(text=text):
                with self.assertRaisesRegex(Exception, "Invalid markdown syntax"):
                    split_nodes_delimiter([TextNode(text, TextType.PLAIN)], "`", TextType.CODE)

    def test_empty_node_list(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])

    def test_empty_text(self):
        self.assertEqual(
            split_nodes_delimiter([TextNode("", TextType.PLAIN)], "`", TextType.CODE),
            [],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_multiple_links_with_surrounding_text(self):
        node = TextNode("Before [first](one) and [second](two) after", TextType.PLAIN)
        self.assertEqual(split_nodes_link([node]), [
            TextNode("Before ", TextType.PLAIN),
            TextNode("first", TextType.LINK, "one"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("second", TextType.LINK, "two"),
            TextNode(" after", TextType.PLAIN),
        ])

    def test_links_at_boundaries_skip_empty_fragments(self):
        for text, expected in [
            ("[link](url)", [TextNode("link", TextType.LINK, "url")]),
            ("[link](url) after", [TextNode("link", TextType.LINK, "url"),
                                   TextNode(" after", TextType.PLAIN)]),
            ("before [link](url)", [TextNode("before ", TextType.PLAIN),
                                    TextNode("link", TextType.LINK, "url")]),
        ]:
            with self.subTest(text=text):
                self.assertEqual(split_nodes_link([TextNode(text, TextType.PLAIN)]), expected)

    def test_adjacent_identical_links(self):
        node = TextNode("[same](url)[same](url)", TextType.PLAIN)
        self.assertEqual(split_nodes_link([node]), [
            TextNode("same", TextType.LINK, "url"),
            TextNode("same", TextType.LINK, "url"),
        ])

    def test_nodes_without_links_are_preserved(self):
        for text in ["", "Plain text", "[link](missing", "![image](image.png)"]:
            with self.subTest(text=text):
                node = TextNode(text, TextType.PLAIN)
                self.assertEqual(split_nodes_link([node]), [node])

    def test_multiple_nodes_preserve_order(self):
        bold = TextNode("bold", TextType.BOLD)
        link = TextNode("existing", TextType.LINK, "existing-url")
        self.assertEqual(split_nodes_link([
            bold, TextNode("[first](one)", TextType.PLAIN),
            link, TextNode("[second](two)", TextType.PLAIN),
        ]), [bold, TextNode("first", TextType.LINK, "one"),
             link, TextNode("second", TextType.LINK, "two")])

    def test_images_remain_plain_text_when_splitting_links(self):
        node = TextNode("![image](image.png) [link](url)", TextType.PLAIN)
        self.assertEqual(split_nodes_link([node]), [
            TextNode("![image](image.png) ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "url"),
        ])

    def test_empty_label_and_url(self):
        node = TextNode("[]()", TextType.PLAIN)
        self.assertEqual(split_nodes_link([node]), [TextNode("", TextType.LINK, "")])

    def test_url_query_and_fragment_are_preserved(self):
        url = "https://example.com/path?a=1&b=2#section"
        node = TextNode(f"[link]({url})", TextType.PLAIN)
        self.assertEqual(split_nodes_link([node]), [TextNode("link", TextType.LINK, url)])

    def test_empty_node_list(self):
        self.assertEqual(split_nodes_link([]), [])


class TestSplitNodesImage(unittest.TestCase):
    def test_multiple_images_with_surrounding_text(self):
        node = TextNode("Before ![first](one.png) and ![second](two.png) after", TextType.PLAIN)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("Before ", TextType.PLAIN),
            TextNode("first", TextType.IMAGE, "one.png"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("second", TextType.IMAGE, "two.png"),
            TextNode(" after", TextType.PLAIN),
        ])

    def test_images_at_boundaries_skip_empty_fragments(self):
        for text, expected in [
            ("![image](url)", [TextNode("image", TextType.IMAGE, "url")]),
            ("![image](url) after", [TextNode("image", TextType.IMAGE, "url"),
                                     TextNode(" after", TextType.PLAIN)]),
            ("before ![image](url)", [TextNode("before ", TextType.PLAIN),
                                      TextNode("image", TextType.IMAGE, "url")]),
        ]:
            with self.subTest(text=text):
                self.assertEqual(split_nodes_image([TextNode(text, TextType.PLAIN)]), expected)

    def test_adjacent_identical_images(self):
        node = TextNode("![same](url)![same](url)", TextType.PLAIN)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("same", TextType.IMAGE, "url"),
            TextNode("same", TextType.IMAGE, "url"),
        ])

    def test_nodes_without_images_are_preserved(self):
        for text in ["", "Plain text", "![image](missing", "[link](url)"]:
            with self.subTest(text=text):
                node = TextNode(text, TextType.PLAIN)
                self.assertEqual(split_nodes_image([node]), [node])

    def test_multiple_nodes_preserve_order(self):
        bold = TextNode("bold", TextType.BOLD)
        image = TextNode("existing", TextType.IMAGE, "existing.png")
        self.assertEqual(split_nodes_image([
            bold, TextNode("![first](one.png)", TextType.PLAIN),
            image, TextNode("![second](two.png)", TextType.PLAIN),
        ]), [bold, TextNode("first", TextType.IMAGE, "one.png"),
             image, TextNode("second", TextType.IMAGE, "two.png")])

    def test_links_remain_plain_text_when_splitting_images(self):
        node = TextNode("[link](url) ![image](image.png)", TextType.PLAIN)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("[link](url) ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "image.png"),
        ])

    def test_empty_alt_text_and_url(self):
        node = TextNode("![]()", TextType.PLAIN)
        self.assertEqual(split_nodes_image([node]), [TextNode("", TextType.IMAGE, "")])

    def test_url_query_and_fragment_are_preserved(self):
        url = "https://example.com/image.png?a=1&b=2#section"
        node = TextNode(f"![image]({url})", TextType.PLAIN)
        self.assertEqual(split_nodes_image([node]), [TextNode("image", TextType.IMAGE, url)])

    def test_empty_node_list(self):
        self.assertEqual(split_nodes_image([]), [])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_lesson_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        self.assertEqual(text_to_textnodes(text), [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_plain_text_with_apostrophe(self):
        text = "It's plain text."
        self.assertEqual(text_to_textnodes(text), [TextNode(text, TextType.PLAIN)])

    def test_empty_text(self):
        self.assertEqual(text_to_textnodes(""), [])

    def test_each_format_on_its_own(self):
        for text, expected in [
            ("**bold**", TextNode("bold", TextType.BOLD)),
            ("_italic_", TextNode("italic", TextType.ITALIC)),
            ("`code`", TextNode("code", TextType.CODE)),
            ("![image](image.png)", TextNode("image", TextType.IMAGE, "image.png")),
            ("[link](url)", TextNode("link", TextType.LINK, "url")),
        ]:
            with self.subTest(text=text):
                self.assertEqual(text_to_textnodes(text), [expected])

    def test_adjacent_formats_preserve_order(self):
        self.assertEqual(text_to_textnodes("**bold**_italic_`code`![image](img)[link](url)"), [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("image", TextType.IMAGE, "img"),
            TextNode("link", TextType.LINK, "url"),
        ])

    def test_unclosed_delimiters_raise(self):
        for text in ["before **bold", "before _italic", "before `code"]:
            with self.subTest(text=text):
                with self.assertRaisesRegex(Exception, "Invalid markdown syntax"):
                    text_to_textnodes(text)


if __name__ == "__main__":
    unittest.main()
