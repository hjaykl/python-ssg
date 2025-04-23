from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    ULIST = 4
    OLIST = 5


def markdown_to_blocks(markdown: str) -> list[str]:
    return list(
        filter(
            lambda b: len(b) > 0,
            [block.strip() for block in markdown.split("\n\n")],
        )
    )


def all_startswith(match: str, strs: list[str]) -> bool:
    for s in strs:
        if not s.startswith(match):
            return False
    return True


def is_ordered_list(strs: list[str]) -> bool:
    for i in range(len(strs)):
        if not strs[i].startswith(f"{i+1}. "):
            return False
    return True


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"#{1,6}\s", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    if all_startswith(">", lines):
        return BlockType.QUOTE
    if all_startswith("-", lines):
        return BlockType.ULIST
    if is_ordered_list(lines):
        return BlockType.OLIST

    return BlockType.PARAGRAPH
