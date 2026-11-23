import os

from src.markdown_to_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    raise Exception("There is no h1 header in provided text")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        content_from = f.read()
    with open(template_path) as f:
        template = f.read()
    title = extract_title(content_from)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", markdown_to_html_node(content_from).to_html())
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

