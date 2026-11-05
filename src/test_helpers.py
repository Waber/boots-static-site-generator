import unittest

from src.helpers import extract_markdown_images, extract_markdown_links
from src.splitNode import split_nodes_image
from src.textnode import TextNode, TextType


class MyTestCase(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images_in_order(self):
        text = "![rick roll](https://example.com/rick.gif) and ![obi wan](https://example.com/obi.jpeg)"
        self.assertEqual(extract_markdown_images(text), [
            ("rick roll", "https://example.com/rick.gif"),
            ("obi wan", "https://example.com/obi.jpeg"),
        ])

    def test_images_ignore_links(self):
        text = "[link](https://example.com) ![image](image.png)"
        self.assertEqual(extract_markdown_images(text), [("image", "image.png")])

    def test_image_with_empty_alt_text(self):
        self.assertEqual(extract_markdown_images("![](image.png)"), [("", "image.png")])

    def test_images_without_matches(self):
        for text in ["", "Plain text", "[link](url)", "![image](missing", "![image]url)"]:
            with self.subTest(text=text):
                self.assertEqual(extract_markdown_images(text), [])

    def test_extract_single_link(self):
        self.assertEqual(
            extract_markdown_links("Visit [Boot.dev](https://www.boot.dev) today"),
            [("Boot.dev", "https://www.boot.dev")],
        )

    def test_extract_multiple_links_in_order(self):
        text = "[first](https://example.com/1)[second](https://example.com/2)"
        self.assertEqual(extract_markdown_links(text), [
            ("first", "https://example.com/1"),
            ("second", "https://example.com/2"),
        ])

    def test_links_ignore_images(self):
        text = "![image](image.png) and [link](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [("link", "https://example.com")])

    def test_links_without_matches(self):
        for text in ["", "Plain text", "![image](image.png)", "[link](missing", "[link]url)"]:
            with self.subTest(text=text):
                self.assertEqual(extract_markdown_links(text), [])

    def test_extractors_preserve_url_query_and_fragment(self):
        url = "https://example.com/path?a=1&b=2#section"
        self.assertEqual(extract_markdown_images(f"![image]({url})"), [("image", url)])
        self.assertEqual(extract_markdown_links(f"[link]({url})"), [("link", url)])


if __name__ == '__main__':
    unittest.main()
