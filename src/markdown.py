import re
from textnode import TextType, TextNode


def split_node(
    old_node: TextNode, delimiter: str, text_type: TextType
) -> list[TextNode]:
    if old_node.text_type != TextType.TEXT:
        return [old_node]
    parts = old_node.text.split(delimiter)
    if len(parts) % 2 == 0:
        raise ValueError("markdown syntax error")
    split_nodes: list[TextNode] = []
    for i in range(len(parts)):
        if len(parts[i]) == 0:
            continue
        if i % 2 == 0:
            split_nodes.append(TextNode(parts[i], old_node.text_type))
        else:
            split_nodes.append(TextNode(parts[i], text_type))

    return split_nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        new_nodes.extend(split_node(node, delimiter, text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_node_image(old_node: TextNode) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    parts = re.split(r"(!\[[^\[\]]*\]\([^\(\)]*\))", old_node.text)
    for part in parts:
        extracted_images = extract_markdown_images(part)
        if len(extracted_images) > 0:
            (text, url) = extracted_images[0]
            new_nodes.append(TextNode(text, TextType.IMAGE, url))
        elif len(part) > 0:
            new_nodes.append(TextNode(part, old_node.text_type, old_node.url))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        new_nodes.extend(split_node_image(node))
    return new_nodes


def split_node_link(old_node: TextNode) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    parts = re.split(r"((?<!!)\[[^\[\]]*\]\([^\(\)]*\))", old_node.text)
    for part in parts:
        extracted_links = extract_markdown_links(part)
        if len(extracted_links) > 0:
            (text, url) = extracted_links[0]
            new_nodes.append(TextNode(text, TextType.LINK, url))
        elif len(part) > 0:
            new_nodes.append(TextNode(part, old_node.text_type, old_node.url))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        new_nodes.extend(split_node_link(node))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes
