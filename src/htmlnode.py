from __future__ import annotations
from typing import override


class HTMLNode:
    tag: str | None
    value: str | None
    children: list[HTMLNode] | None
    props: dict[str, str] | None

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props == None:
            return ""
        return " " + " ".join(f'{key}="{value}"' for (key, value) in self.props.items())

    @override
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ):
        super().__init__(tag, value, None, props)

    @override
    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ):
        super().__init__(tag, None, children, props)

    @override
    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("parent nodes must have a tag")
        if self.children == None:
            raise ValueError("parent nodes must have at least 1 child")
        return f"<{self.tag}{self.props_to_html()}>{
                "".join(child.to_html() for child in self.children)
                }</{self.tag}>"
