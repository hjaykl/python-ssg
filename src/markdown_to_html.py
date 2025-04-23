from blocks import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode, ParentNode
from markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def text_to_children(text: str) -> list[HTMLNode]:
    return list(map(text_node_to_html_node, text_to_textnodes(text)))


def paragraph_block_to_html_node(block: str) -> HTMLNode:
    return ParentNode("p", text_to_children(block.replace("\n", " ")))


def heading_block_to_html_node(block: str) -> HTMLNode:
    segments = block.split(" ")
    heading_level = len(segments[0])
    return ParentNode(
        f"h{heading_level}", text_to_children(" ".join(segments[1:]).replace("\n", " "))
    )


def code_block_to_html_node(block: str) -> HTMLNode:
    code = TextNode(block.lstrip("```\n").rstrip("```"), TextType.CODE)
    return ParentNode("pre", [text_node_to_html_node(code)])


def quote_block_to_html_node(block: str) -> HTMLNode:
    return ParentNode(
        "blockquote", text_to_children(block.replace("> ", "").replace("\n", " "))
    )


def list_item_line_to_html_node(line: str) -> HTMLNode:
    item = " ".join(line.split(" ")[1:])
    return ParentNode("li", text_to_children(item.replace("\n", " ")))


def ulist_block_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    children = list(map(list_item_line_to_html_node, items))
    return ParentNode("ul", children)


def olist_block_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    children = list(map(list_item_line_to_html_node, items))
    return ParentNode("ol", children)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    children: list[HTMLNode] = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        match (block_to_block_type(block)):
            case BlockType.PARAGRAPH:
                children.append(paragraph_block_to_html_node(block))
            case BlockType.HEADING:
                children.append(heading_block_to_html_node(block))
            case BlockType.CODE:
                children.append(code_block_to_html_node(block))
            case BlockType.QUOTE:
                children.append(quote_block_to_html_node(block))
            case BlockType.ULIST:
                children.append(ulist_block_to_html_node(block))
            case BlockType.OLIST:
                children.append(olist_block_to_html_node(block))
    return ParentNode("div", children)
