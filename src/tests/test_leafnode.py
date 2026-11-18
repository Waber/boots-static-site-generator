import unittest

from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_paragraph(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_bold(self):
        self.assertEqual(LeafNode("b", "Bold").to_html(), "<b>Bold</b>")

    def test_link_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_raw_text(self):
        self.assertEqual(LeafNode(None, "Text").to_html(), "Text")

    def test_missing_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_empty_value(self):
        self.assertEqual(LeafNode("p", "").to_html(), "<p></p>")

    def test_no_children(self):
        self.assertIsNone(LeafNode("p", "Text").children)

    def test_repr(self):
        self.assertEqual(repr(LeafNode("p", "Text")), "LeafNode(p, Text, None)")
