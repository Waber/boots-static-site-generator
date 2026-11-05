import unittest

from src.htmlnode import HTMLNode


class MyTestCase(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode("a","gugiel","",{"href":"https://www.google.com"})
        self.assertEqual(node1.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_without_props(self):
        node = HTMLNode("p", "Text", None)
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_raises_not_implemented(self):
        node = HTMLNode("p", "Text", None)
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == '__main__':
    unittest.main()
