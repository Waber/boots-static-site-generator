import unittest

from src.leafnode import LeafNode
from src.parentnode import ParentNode


class MyTestCase(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_without_tag(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_without_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_empty_children(self):
        self.assertEqual(ParentNode("div", []).to_html(), "<div></div>")

    def test_to_html_preserves_children_order(self):
        node = ParentNode("p", [
            LeafNode("b", "first"),
            LeafNode("i", "second"),
            LeafNode("span", "third"),
        ])
        self.assertEqual(
            node.to_html(), "<p><b>first</b><i>second</i><span>third</span></p>"
        )

    def test_to_html_with_raw_text_and_elements(self):
        node = ParentNode("p", [
            LeafNode(None, "Hello "),
            LeafNode("b", "world"),
            LeafNode(None, "!"),
        ])
        self.assertEqual(node.to_html(), "<p>Hello <b>world</b>!</p>")

    def test_to_html_with_nested_parents_and_siblings(self):
        node = ParentNode("div", [
            ParentNode("p", [LeafNode("b", "first")]),
            ParentNode("p", [LeafNode(None, "second")]),
            LeafNode("span", "third"),
        ])
        self.assertEqual(
            node.to_html(),
            "<div><p><b>first</b></p><p>second</p><span>third</span></div>",
        )

    def test_to_html_with_empty_nested_parent(self):
        node = ParentNode("div", [ParentNode("span", [])])
        self.assertEqual(node.to_html(), "<div><span></span></div>")

    def test_to_html_preserves_child_attributes(self):
        node = ParentNode("p", [
            LeafNode("a", "link", {"href": "https://example.com"}),
        ])
        self.assertEqual(
            node.to_html(), '<p><a href="https://example.com">link</a></p>'
        )

    def test_to_html_propagates_invalid_child_error(self):
        node = ParentNode("div", [LeafNode("span", None)])
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == '__main__':
    unittest.main()
