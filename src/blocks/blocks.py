from enum import Enum


def markdown_to_blocks(markdown: str) -> list[str]:
    cleared_blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if block != "":
            cleared_blocks.append(block)
    return cleared_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_block: str) -> BlockType:
    if markdown_block.startswith(("# ","## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.CODE
    splitted = markdown_block.split("\n")
    if all(line.startswith(">") for line in splitted):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in splitted):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(splitted)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

