def extract_title(markdown: str):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    raise Exception("There is no h1 header in provided text")