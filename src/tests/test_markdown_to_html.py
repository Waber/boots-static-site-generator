import unittest

from src.markdown_to_html import text_to_children, paragraph_to_html_node, heading_to_html_node, code_to_html_node, \
    quote_to_html_node, unordered_list_to_html_node, ordered_list_to_html_node, markdown_to_html_node
from src.textnode import TextNode, TextType


class MyTestCase(unittest.TestCase):
    def test_text_to_children_with_simple_text(self):
        bold_string = "to jest **gruby** tekst"
        list_of_nodes = text_to_children(bold_string)
        self.assertEqual(len(list_of_nodes), 3)
        self.assertEqual(list_of_nodes[0].to_html(), "to jest ")
        self.assertEqual(list_of_nodes[1].to_html(), "<b>gruby</b>")
        self.assertEqual(list_of_nodes[2].to_html(), " tekst")

    def test_paragraph_to_html_node(self):
        md = """This is **bolded** paragraph
text in a p
tag here"""
        paragraphed_string = paragraph_to_html_node(md)
        self.assertEqual(paragraphed_string.to_html(), "<p>This is <b>bolded</b> paragraph text in a p tag here</p>")

    def test_heading(self):
        md = "## Witaj w **moim** blogu"
        self.assertEqual(heading_to_html_node(md).to_html(), "<h2>Witaj w <b>moim</b> blogu</h2>")

    def test_code(self):
        md = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""
        self.assertEqual(code_to_html_node(md).to_html(), "<pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre>")

    def test_quote(self):
        md = "> Być albo nie być,\n>oto jest **pytanie**"
        self.assertEqual(quote_to_html_node(md).to_html(), "<blockquote>Być albo nie być, oto jest <b>pytanie</b></blockquote>")

    def test_unordered_list(self):
        md = "- pierwszy **ważny** punkt\n- drugi punkt"
        self.assertEqual(unordered_list_to_html_node(md).to_html(), "<ul><li>pierwszy <b>ważny</b> punkt</li><li>drugi punkt</li></ul>")

    def test_unordered_list_single_item(self):
        md = "- jedyny punkt"
        self.assertEqual(unordered_list_to_html_node(md).to_html(), "<ul><li>jedyny punkt</li></ul>")

    def test_unordered_list_keeps_dash_inside_text(self):
        md = "- od 9 - 17\n- pon - pt"
        self.assertEqual(unordered_list_to_html_node(md).to_html(), "<ul><li>od 9 - 17</li><li>pon - pt</li></ul>")

    def test_ordered_list(self):
        md = "1. pierwszy _ważny_ punkt\n2. drugi z `kodem`"
        self.assertEqual(ordered_list_to_html_node(md).to_html(), "<ol><li>pierwszy <i>ważny</i> punkt</li><li>drugi z <code>kodem</code></li></ol>")

    def test_ordered_list_with_multi_digit_numbers(self):
        md = "\n".join(f"{i}. punkt {i}" for i in range(1, 12))
        expected_items = "".join(f"<li>punkt {i}</li>" for i in range(1, 12))
        self.assertEqual(ordered_list_to_html_node(md).to_html(), f"<ol>{expected_items}</ol>")

    def test_ordered_list_keeps_dots_and_numbers_inside_text(self):
        md = "1. Wstęp. Dalej\n2. 2024. rok"
        self.assertEqual(ordered_list_to_html_node(md).to_html(), "<ol><li>Wstęp. Dalej</li><li>2024. rok</li></ol>")

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_all_block_types_in_one_document(self):
        md = """
# Tytuł

Akapit z **pogrubieniem**
w dwóch liniach

> cytat z _kursywą_
>druga linia cytatu

- jabłko
- gruszka

1. pierwszy
2. drugi

```
kod z **gwiazdkami**
```

###### Najmniejszy nagłówek
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div>"
            "<h1>Tytuł</h1>"
            "<p>Akapit z <b>pogrubieniem</b> w dwóch liniach</p>"
            "<blockquote>cytat z <i>kursywą</i> druga linia cytatu</blockquote>"
            "<ul><li>jabłko</li><li>gruszka</li></ul>"
            "<ol><li>pierwszy</li><li>drugi</li></ol>"
            "<pre><code>kod z **gwiazdkami**\n</code></pre>"
            "<h6>Najmniejszy nagłówek</h6>"
            "</div>",
        )

    def test_empty_document(self):
        self.assertEqual(markdown_to_html_node("").to_html(), "<div></div>")

if __name__ == '__main__':
    unittest.main()
