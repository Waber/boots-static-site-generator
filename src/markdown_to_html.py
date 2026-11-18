from src.blocks import markdown_to_blocks, block_to_block_type, BlockType
from src.htmlnode import HTMLNode
from src.leafnode import LeafNode
from src.parentnode import ParentNode
from src.splitNode import text_to_textnodes
from src.textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_html_node(markdown):
    return ParentNode("div", [block_to_html_node(block) for block in markdown_to_blocks(markdown)])

def block_to_html_node(block: str) -> ParentNode:
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)




def text_to_children(text: str) -> list[HTMLNode]:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

def paragraph_to_html_node(block: str) -> ParentNode:
    return ParentNode("p", text_to_children(block.replace("\n", " ")))

def heading_to_html_node(heading: str) -> ParentNode:
    heading_count = len(heading) - len(heading.lstrip("#"))
    heading_tag = f"h{heading_count}"
    return ParentNode(heading_tag, text_to_children(heading[heading_count+1:]))

def code_to_html_node(code: str) -> ParentNode:
    code_text = code.removeprefix("```\n").removesuffix("```")
    code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
    return ParentNode("pre", [code_node])

def quote_to_html_node(quote: str) -> ParentNode:
    quote_lines = quote.split("\n")
    single_line = ' '.join(line[1:].strip() for line in quote_lines)
    return ParentNode("blockquote", text_to_children(single_line))

def unordered_list_to_html_node(unordered_list: str) -> ParentNode:
    list_items = unordered_list.split("\n")
    list_item_nodes = [ParentNode("li", text_to_children(item[2:])) for item in list_items]
    return ParentNode("ul", list_item_nodes)

def ordered_list_to_html_node(ordered_list: str) -> ParentNode:
    list_items = ordered_list.split("\n")
    list_items_nodes = [ParentNode("li", text_to_children(item.split(". ", maxsplit=1)[1])) for item in list_items]
    return ParentNode("ol", list_items_nodes)
