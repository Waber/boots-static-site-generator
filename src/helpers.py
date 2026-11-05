import re
text_pattern = r"!\[([^\]]*)\]\([^)]*\)"

def extract_markdown_images(text) -> list[tuple[str,str]]:
    texts = re.findall(text_pattern, text)
    imgs = re.findall(r"!\[[^\]]*\]\(([^)]*)\)", text)
    return list(zip(texts, imgs))

def extract_markdown_links(text) -> list[tuple[str,str]]:
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

