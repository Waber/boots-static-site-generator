import unittest

from src.textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_different_text(self):
        node = TextNode("First text", TextType.BOLD)
        node2 = TextNode("Second text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_equal_urls(self):
        node = TextNode("Link", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Link", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_different_urls(self):
        node = TextNode("Link", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Link", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_none_url_differs_from_present_url(self):
        node = TextNode("Link", TextType.LINK, None)
        node2 = TextNode("Link", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_default_url_equals_explicit_none(self):
        node = TextNode("Same text", TextType.PLAIN)
        node2 = TextNode("Same text", TextType.PLAIN, None)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_unknown_text_type_raises_value_error(self):
        node = TextNode("This is a text node", "unknown")
        with self.assertRaisesRegex(ValueError, "Unsupported text type: 'unknown'"):
            text_node_to_html_node(node)

    def test_none_text_type_raises_value_error(self):
        node = TextNode("This is a text node", None)
        with self.assertRaisesRegex(ValueError, "Unsupported text type: None"):
            text_node_to_html_node(node)

if __name__ == '__main__':
    unittest.main()
