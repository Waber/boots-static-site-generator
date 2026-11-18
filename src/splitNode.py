from src.helpers import extract_markdown_images, extract_markdown_links
from src.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Invalid markdown syntax")
        splitted_text = node.text.split(delimiter)
        for i in range(len(splitted_text)):
            if splitted_text[i] == "":
                continue
            if i % 2 != 0:
                new_nodes.append(TextNode(splitted_text[i], text_type))
            else:
                new_nodes.append(TextNode(splitted_text[i], TextType.PLAIN))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for alt, url in images:
            sections = remaining_text.split(f"![{alt}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))
            new_nodes.append(TextNode(alt,TextType.IMAGE,url))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for alt, url in links:
            sections = remaining_text.split(f"[{alt}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))
            new_nodes.append(TextNode(alt,TextType.LINK,url))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text) -> list[TextNode]:
    new_nodes = [TextNode(text, TextType.PLAIN)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes



