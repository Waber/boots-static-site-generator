def markdown_to_blocks(markdown: str) -> list[str]:
    cleared_blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if block != "":
            cleared_blocks.append(block)
    return cleared_blocks